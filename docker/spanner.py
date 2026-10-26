"""Seed and verify the local Spanner emulator through its REST API (no SDK)."""
import json
import os
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ENDPOINT = os.environ.get('SPANNER_REST_ENDPOINT', 'http://spanner-emulator:9020')
PROJECT = 'projects/rava-local'
INSTANCE = PROJECT + '/instances/rava'
DATABASE = INSTANCE + '/databases/rava'
DDL = [
    'CREATE TABLE customers (customer_id INT64 NOT NULL, name STRING(100), note STRING(MAX)) PRIMARY KEY (customer_id)',
    'CREATE TABLE orders (order_id INT64 NOT NULL, customer_id INT64 NOT NULL, amount NUMERIC, ordered_at TIMESTAMP, CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers (customer_id)) PRIMARY KEY (order_id)',
    'CREATE INDEX ix_orders_customer ON orders(customer_id)',
    'CREATE TABLE exact_values (id INT64 NOT NULL, big_integer INT64, amount NUMERIC) PRIMARY KEY (id)',
    'CREATE TABLE demo_ready (id INT64 NOT NULL, dataset_version STRING(40)) PRIMARY KEY (id)',
]


def api(path, data=None, method=None):
    request = Request(ENDPOINT + '/v1/' + path,
                      data=None if data is None else json.dumps(data).encode(),
                      headers={'Content-Type': 'application/json'}, method=method)
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode('utf-8', errors='replace')
        error.reason = f'{error.reason}: {detail}'
        raise


def exists(path):
    # List avoids a grpc-gateway bug in emulator 1.5.41 when marshalling
    # a NotFound response containing google.rpc.ResourceInfo.
    parent, collection, _ = path.rsplit('/', 2)
    return any(item['name'] == path for item in api(parent + '/' + collection).get(collection, []))


def operation(result):
    deadline = time.monotonic() + 120
    while not result.get('done'):
        if time.monotonic() > deadline:
            raise TimeoutError('Spanner operation timed out')
        time.sleep(0.2)
        result = api(result['name'])
    if 'error' in result:
        raise RuntimeError(result['error'])


def query(sql):
    session = api(DATABASE + '/sessions', {})['name']
    try:
        return api(session + ':executeSql', {'sql': sql}).get('rows', [])
    finally:
        api(session, method='DELETE')


def initialize():
    if not exists(INSTANCE):
        operation(api(PROJECT + '/instances', {'instanceId': 'rava', 'instance': {
            'config': PROJECT + '/instanceConfigs/emulator-config',
            'displayName': 'Rava local emulator', 'nodeCount': 1}}))
    if not exists(DATABASE):
        operation(api(INSTANCE + '/databases', {'createStatement': 'CREATE DATABASE `rava`',
                                               'extraStatements': DDL}))
    if query('SELECT dataset_version FROM demo_ready WHERE id=1') == [['rava-v1']]:
        return
    mutations = [
        {'insertOrUpdate': {'table': 'customers', 'columns': ['customer_id', 'name', 'note'],
                            'values': [['1', '東京の顧客', None], ['2', '大阪の顧客', ''], ['3', '名古屋の顧客', '日本語']]}},
        {'insertOrUpdate': {'table': 'orders', 'columns': ['order_id', 'customer_id', 'amount', 'ordered_at'],
                            'values': [[str(i + 1), str(1 if i < 900 else i % 2 + 2), '1234.50', '2026-10-01T00:00:00Z'] for i in range(1200)]}},
        {'insertOrUpdate': {'table': 'exact_values', 'columns': ['id', 'big_integer', 'amount'],
                            'values': [['1', '9223372036854775807', '12345678901234567890123.12345678']]}},
        {'insertOrUpdate': {'table': 'demo_ready', 'columns': ['id', 'dataset_version'], 'values': [['1', 'rava-v1']]}},
    ]
    session = api(DATABASE + '/sessions', {})['name']
    try:
        api(session + ':commit', {'singleUseTransaction': {'readWrite': {}}, 'mutations': mutations})
    finally:
        api(session, method='DELETE')
    print('Rava: Spanner GoogleSQL sample data ready', flush=True)


def verify():
    checks = [
        ('SELECT dataset_version FROM demo_ready WHERE id=1', [['rava-v1']]),
        ('SELECT COUNT(*) FROM customers', [['3']]),
        ('SELECT COUNT(*) FROM orders', [['1200']]),
        ('SELECT COUNT(*) FROM orders WHERE customer_id=1', [['900']]),
        ("SELECT COUNT(*) FROM exact_values WHERE big_integer=9223372036854775807 AND amount=NUMERIC '12345678901234567890123.12345678'", [['1']]),
    ]
    for sql, expected in checks:
        actual = query(sql)
        if actual != expected:
            raise RuntimeError(f'{sql}: {actual} != {expected}')


if __name__ == '__main__':
    if '--verify' in sys.argv:
        verify()
        print('rava-spanner-ok')
    else:
        # The emulator is in memory. Recreate fixtures automatically after restart.
        while True:
            try:
                initialize()
            except Exception as error:
                print(f'Spanner initialization: {error}', file=sys.stderr, flush=True)
            time.sleep(5)
