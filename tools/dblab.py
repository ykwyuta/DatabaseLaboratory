#!/usr/bin/env python3
"""Manage the DatabaseLaboratory lab with Python's standard library and Docker Compose v2."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ('postgres', 'mysql', 'mariadb', 'sqlserver', 'oracle', 'db2',
            'mongo', 'redis', 'clickhouse', 'alloydb', 'spanner')
PASSWORD = 'DatabaseLaboratory_Test_2026!'
COMPOSE = ['docker', 'compose', '--project-directory', str(ROOT),
           '-f', str(ROOT / 'compose.yaml'), '--profile', '*']


def run(args, capture=False):
    result = subprocess.run(args, cwd=ROOT, check=True, text=True,
                            encoding='utf-8', errors='replace',
                            stdout=subprocess.PIPE if capture else None)
    return result.stdout.strip() if capture else ''


def compose(*args, capture=False):
    return run(COMPOSE + list(args), capture)


def client(service, filename):
    """Return a bundled client invocation; host-side drivers are unnecessary."""
    path = '/demo/sql/' + filename
    if service in ('postgres', 'alloydb'):
        return ['psql', '-v', 'ON_ERROR_STOP=1', '-U', 'dblab', '-d', 'dblab', '-tA', '-F', '|', '-f', path]
    if service in ('mysql', 'mariadb'):
        return [service, '--default-character-set=utf8mb4', '-h', '127.0.0.1', '-u', 'dblab',
                '-D', 'dblab', '-NB', '-e', 'source ' + path]
    if service == 'sqlserver':
        return ['/opt/mssql-tools18/bin/sqlcmd', '-S', '127.0.0.1', '-U', 'dblab',
                '-C', '-b', '-d', 'dblab', '-h', '-1', '-W', '-f', '65001', '-s', '|', '-i', path]
    if service == 'oracle':
        return ['sqlplus', '-L', '-s', f'dblab/"{PASSWORD}"@//127.0.0.1:1521/FREEPDB1', '@' + path]
    if service == 'db2':
        return ['su', '-', 'db2inst1', '-c', f'db2 connect to DBLAB >/dev/null && db2 -stf {path}']
    raise ValueError(service)


def query(service, filename):
    args = client(service, filename)
    if service in ('mysql', 'mariadb'):
        return compose('exec', '-T', '-e', 'MYSQL_PWD=' + PASSWORD, service, *args, capture=True)
    return compose('exec', '-T', service, *args, capture=True)


def check_rows(service, output, expected):
    counts = {}
    for line in output.splitlines():
        match = re.fullmatch(r'\s*([a-z_]+)[|\t ]+(\d+)[|\t ]+(\d+)\s*', line)
        if match:
            name, wanted, actual = match.groups()
            if name in counts or name not in expected or int(wanted) != expected[name] or int(actual) != expected[name]:
                raise RuntimeError(f'{service}: unexpected result {line}')
            counts[name] = int(actual)
    if counts != expected:
        raise RuntimeError(f'{service}: incomplete verification: {output}')
    return counts


def verify(service):
    ids = compose('ps', '-q', service, capture=True).splitlines()
    if len(ids) != 1:
        raise RuntimeError(f'{service}: start it first: python tools/dblab.py up {service}')
    state = json.loads(run(['docker', 'inspect', ids[0]], capture=True))[0]
    if state['State'].get('Health', {}).get('Status') != 'healthy':
        raise RuntimeError(f'{service}: not healthy; inspect logs')
    counts = {}
    if service == 'spanner':
        compose('exec', '-T', service, 'python', '/demo/spanner.py', '--verify')
    elif service == 'mongo':
        compose('exec', '-T', service, 'mongosh', '--quiet', '-u', 'dblab', '-p', PASSWORD,
                '--authenticationDatabase', 'admin', 'dblab', '/demo/verify.js')
    elif service == 'redis':
        script = (ROOT / 'sql/redis-verify.lua').read_text(encoding='utf-8')
        prefix = 'dblab:verify:' + uuid.uuid4().hex
        result = compose('exec', '-T', service, 'redis-cli', '--raw', 'EVAL', script,
                         '5', *(prefix + ':' + str(i) for i in range(5)), capture=True)
        if result != 'dblab-redis-ok':
            raise RuntimeError(f'Redis verification failed: {result}')
    elif service == 'clickhouse':
        compose('exec', '-T', service, 'clickhouse-client', '--user', 'dblab', '--password', PASSWORD,
                '--database', 'dblab', '--multiquery', '--queries-file', '/demo/verify.sql')
    else:
        filename = 'verify-oracle.sql' if service == 'oracle' else '00-verify-counts.sql'
        output = query(service, filename)
        expected = json.loads((ROOT / 'data/expected-counts.json').read_text())
        counts = check_rows(service, output, expected)
        values = {'unicode': 1, 'bigint': 1, 'decimal_precision': 1,
                  'skew': 900, 'null_text': 1, 'view_rows': 24}
        filename = 'verify-oracle-values.sql' if service == 'oracle' else 'verify-values.sql'
        if service == 'sqlserver':
            filename = 'verify-sqlserver-values.sql'
        check_rows(service, query(service, filename), values)
        samples = ['01-overview.sql', '02-join-and-plan.sql',
                   '03-index-selectivity.sql', '04-exact-values-and-logical-relation.sql']
        if service == 'oracle':
            samples = ['verify-oracle-samples.sql']
        for sample in samples:
            result = query(service, sample)
            if re.search(r'(?m)^ERROR |^ORA-\d|SQL\d{4}N', result):
                raise RuntimeError(f'{service}: {sample} failed: {result}')
    print(f'{service}: verification passed', flush=True)
    images = {service: state['Image']}
    backend = {'alloydb': 'alloydb-server', 'spanner': 'spanner-emulator'}.get(service)
    if backend:
        backend_id = compose('ps', '-q', backend, capture=True)
        images[backend] = run(['docker', 'inspect', '--format', '{{.Image}}', backend_id], capture=True)
    return {'service': service, 'status': 'passed', 'image': images.get(backend, state['Image']),
            'images': images, 'counts': counts}


def local_database(kind, output):
    path = Path(output).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Refuse overwrite, including an existing empty file.
    with path.open('xb'):
        pass
    sql = (ROOT / 'init' / f'{kind}.sql').read_text(encoding='utf-8')
    try:
        if kind == 'sqlite':
            with closing(sqlite3.connect(path)) as db:
                db.executescript(sql)
        else:
            import duckdb
            path.unlink()  # DuckDB requires a new path, not an empty file.
            with duckdb.connect(str(path)) as db:
                db.execute(sql)
    except Exception:
        if path.exists():
            path.unlink()
        raise
    print(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    for action in ('up', 'stop', 'logs', 'verify'):
        cmd = sub.add_parser(action)
        cmd.add_argument('services', nargs='*', choices=(*SERVICES, 'all'))
        if action == 'up':
            cmd.add_argument('--timeout', type=int, default=1200)
    sub.add_parser('status')
    sub.add_parser('config')
    sub.add_parser('down', help='Remove lab containers; preserve volumes')
    reset = sub.add_parser('reset', help='Delete ALL lab containers and data volumes')
    reset.add_argument('--yes', action='store_true', help='Confirm deleting all lab data')
    local = sub.add_parser('local', help='Create a SQLite or DuckDB file without Docker')
    local.add_argument('kind', choices=('sqlite', 'duckdb'))
    local.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.action == 'local':
        local_database(args.kind, args.output)
        return
    if args.action == 'reset' and not args.yes:
        parser.error('reset deletes every DatabaseLaboratory volume; explicitly pass --yes')
    selected = getattr(args, 'services', [])
    if 'all' in selected:
        selected = list(SERVICES)
    elif not selected:
        selected = ['postgres'] if args.action == 'up' else SERVICES
    if args.action == 'up':
        compose('up', '-d', '--wait', '--wait-timeout', str(args.timeout), *selected)
    elif args.action == 'stop':
        if 'spanner' in selected:
            selected = [*selected, 'spanner-emulator']
        if 'alloydb' in selected:
            selected = [*selected, 'alloydb-server']
        compose('stop', *selected)
    elif args.action == 'logs':
        if 'spanner' in selected:
            selected = [*selected, 'spanner-emulator']
        if 'alloydb' in selected:
            selected = [*selected, 'alloydb-server']
        compose('logs', '--tail', '100', *selected)
    elif args.action == 'status':
        compose('ps', '-a')
    elif args.action == 'config':
        compose('config', '--quiet')
    elif args.action in ('down', 'reset'):
        compose('down', *(['--volumes'] if args.action == 'reset' else []))
    elif args.action == 'verify':
        if not args.services:
            selected = [name for name in compose('ps', '--services', '--status', 'running', capture=True).splitlines() if name in SERVICES]
        if not selected:
            raise RuntimeError('No running databases to verify')
        report = {'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'databases': []}
        try:
            for service in selected:
                try:
                    report['databases'].append(verify(service))
                except Exception as error:
                    report['databases'].append({'service': service, 'status': 'failed', 'error': str(error)})
                    raise
        finally:
            directory = ROOT / 'reports'
            directory.mkdir(exist_ok=True)
            (directory / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except (subprocess.CalledProcessError, RuntimeError, OSError, ImportError) as error:
        print(f'DatabaseLaboratory: {error}', file=sys.stderr)
        sys.exit(1)
