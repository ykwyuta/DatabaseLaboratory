import csv
from contextlib import closing
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import generate
import dblab


class DatasetTests(unittest.TestCase):
    def test_sqlite_schema_data_and_sample_queries(self):
        with closing(sqlite3.connect(':memory:')) as db:
            db.executescript((ROOT / 'init/sqlite.sql').read_text(encoding='utf-8'))
            for table, count in generate.EXPECTED.items():
                self.assertEqual(db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0], count, table)
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
            self.assertEqual(db.execute('SELECT COUNT(*) FROM orders WHERE customer_id=1').fetchone()[0], 900)
            self.assertEqual(db.execute('SELECT big_integer,amount FROM exact_values WHERE value_id=1').fetchone(),
                             (9223372036854775807, '12345678901234567890123.12345678'))
            self.assertEqual(db.execute("SELECT COUNT(*) FROM departments WHERE name='営業部'").fetchone()[0], 1)
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("INSERT INTO order_items VALUES(999999,1,1,1,1)")
            for path in sorted((ROOT / 'sql').glob('0*.sql')):
                db.executescript(path.read_text(encoding='utf-8'))

    def test_generated_sql_is_current(self):
        for kind in generate.KINDS:
            self.assertEqual((ROOT / 'init' / f'{kind}.sql').read_text(encoding='utf-8'),
                             generate.generate_sql(kind, generate.dataset()), kind)

    def test_ready_marker_follows_view_creation(self):
        for kind in generate.KINDS:
            sql = generate.generate_sql(kind, generate.dataset())
            self.assertGreater(sql.index('INSERT INTO demo_ready'), sql.index('CREATE VIEW customer_sales'), kind)

    def test_decimal_literals_do_not_promote_values_to_float(self):
        from decimal import Decimal
        for kind in generate.KINDS:
            self.assertEqual(generate.literal(Decimal('-0.00000001'), kind), '-0.00000001')

    def test_delimited_roundtrip(self):
        reference = None
        for extension, delimiter in [('csv', ','), ('tsv', '\t'), ('psv', '|')]:
            with (ROOT / 'data' / f'import_sample.{extension}').open(encoding='utf-8', newline='') as file:
                rows = list(csv.reader(file, delimiter=delimiter))
            self.assertEqual(len(rows), 6)
            self.assertTrue(all(len(row) == 4 for row in rows))
            if reference is None:
                reference = rows
            self.assertEqual(rows, reference)
        self.assertEqual(reference[2][3], '1行目\r\n2行目')
        self.assertEqual(reference[3][3], '')
        self.assertEqual(reference[4][3], '\\N')


class ToolTests(unittest.TestCase):
    def test_local_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sample.sqlite'
            dblab.local_database('sqlite', path)
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                dblab.local_database('sqlite', path)
            self.assertEqual(path.read_bytes(), before)

    def test_reset_requires_explicit_flag(self):
        with patch.object(sys, 'argv', ['dblab.py', 'reset']), patch.object(dblab, 'compose') as compose:
            with self.assertRaises(SystemExit) as result:
                dblab.main()
            self.assertEqual(result.exception.code, 2)
            compose.assert_not_called()

    def test_up_selects_only_requested_services(self):
        with patch.object(sys, 'argv', ['dblab.py', 'up', 'alloydb', 'spanner']), patch.object(dblab, 'compose') as compose:
            dblab.main()
            compose.assert_called_once_with('up', '-d', '--wait', '--wait-timeout', '1200', 'alloydb', 'spanner')

    def test_verification_rejects_partial_or_incorrect_counts(self):
        expected = generate.EXPECTED
        good = '\n'.join(f'{table}|{count}|{count}' for table, count in expected.items())
        state = json.dumps([{'Image': 'sha256:test', 'State': {'Health': {'Status': 'healthy'}}}])
        for bad in [good.replace('orders|1200|1200', 'orders|1200|1199'), good.splitlines()[0], good + '\n' + good.splitlines()[0]]:
            with patch.object(dblab, 'compose', return_value='id'), patch.object(dblab, 'run', return_value=state), patch.object(dblab, 'query', return_value=bad):
                with self.assertRaises(RuntimeError):
                    dblab.verify('postgres')


class SpannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('spanner', ROOT / 'docker/spanner.py')
        cls.spanner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.spanner)

    def test_existing_marker_prevents_reseeding(self):
        with patch.object(self.spanner, 'exists', return_value=True), patch.object(self.spanner, 'query', return_value=[['dblab-v1']]), patch.object(self.spanner, 'api') as api:
            self.spanner.initialize()
            api.assert_not_called()

    def test_restart_recreates_instance_database_and_atomic_seed(self):
        def api_result(path, data=None, method=None):
            if path.endswith('/sessions'):
                return {'name': 'test-session'}
            return {'done': True}
        with patch.object(self.spanner, 'exists', return_value=False), patch.object(self.spanner, 'query', return_value=[]), patch.object(self.spanner, 'api', side_effect=api_result) as api:
            self.spanner.initialize()
            commits = [call for call in api.call_args_list if call.args[0].endswith(':commit')]
            self.assertEqual(len(commits), 1)
            mutations = commits[0].args[1]['mutations']
            self.assertEqual(len(mutations[1]['insertOrUpdate']['values']), 1200)
            self.assertEqual(mutations[-1]['insertOrUpdate']['table'], 'demo_ready')


if __name__ == '__main__':
    unittest.main()
