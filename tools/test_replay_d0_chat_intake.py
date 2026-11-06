"""Small behavioral tests; these do not run the archived calculations."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('replay_chat', Path(__file__).with_name('replay_d0_chat_intake.py'))
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class ReplayTests(unittest.TestCase):
    def test_json_rejects_failure_nan_overflow_and_bad_count(self):
        self.assertEqual(replay.parse_json(b'{"status":"PASS_TEST","checks":2}', 'PASS_TEST', 2)['checks'], 2)
        for raw in (b'{"status":"FAIL","checks":2}',
                    b'{"status":"PASS_TEST","checks":2,"x":NaN}',
                    b'{"status":"PASS_TEST","checks":2,"x":1e999}',
                    b'{"status":"PASS_TEST","checks":2,"x":"Infinity"}',
                    b'{"status":"FAIL","status":"PASS_TEST","checks":2}',
                    b'{"status":"PASS_TEST","checks":true}',
                    b'{"status":"PASS_TEST","checks":2,"unconditional_GR_closed":true}',
                    b'{"status":"PASS_TEST","checks":2,"failure":"error"}',
                    b'{"status":"PASS_TEST","checks":2,"nested":[{"status":"FAIL"}]}',
                    b'{"status":"PASS_TEST","checks":2,"nested":{"failed_count":1}}',
                    b'{"status":"PASS_TEST","checks":2,"nested":{"unconditional_GR_closed":true}}',
                    b'{"status":"PASS_TEST","checks":2,"operator_error_plus_interval":"[nan, +inf]"}',
                    b'{"status":"PASS_TEST","checks":2,"operator_error_minus_interval":"[2, 1]"}'):
            with self.subTest(raw=raw), self.assertRaises(replay.ReplayFailure):
                replay.parse_json(raw, 'PASS_TEST', 2)
        replay.parse_json(b'{"status":"PASS_TEST","checks":2,"nested":{"failure":false,"unconditional_GR_closed":false,"source_error":"0.2"}}', 'PASS_TEST', 2)
        replay.parse_json(b'{"status":"PASS_TEST","checks":2,"operator_error_plus_interval":"[-1.2e-7, +3.4e-7]","scope":"[nan, +inf] is explanatory text"}', 'PASS_TEST', 2)

    def test_car_requires_explicit_zero_diagnostics(self):
        raw = b'quadratic_bad_count 0\nfirst_bad []\ntrace_difference 0\neigenvals {1: 8, 2: 8}\nelapsed 0.1\n'
        self.assertEqual(replay.parse_car(raw)['trace_difference'], 0)
        for changed in (raw.replace(b'bad_count 0', b'bad_count 1'),
                        raw.replace(b'trace_difference 0', b'trace_difference 1'),
                        raw.replace(b'first_bad []', b'first_bad [1]'),
                        raw.replace(b'{1: 8, 2: 8}', b'{1: 7, 2: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{1: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{1: 8, 2: 8, 3: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{1: 8, 1: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{1: True, 2: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{nan: 8, oo: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{sqrt(3): 8, mystery(4): 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{float(2): 8, 1: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{1' + b' ' * 4097 + b': 8, 2: 8}'),
                        raw.replace(b'{1: 8, 2: 8}', b'{' + b'1+' * 50 + b'1: 8, 2: 8}'),
                        raw.replace(b'elapsed 0.1', b'elapsed nan'),
                        raw + b'trace_difference 0\n'):
            with self.subTest(changed=changed), self.assertRaises(replay.ReplayFailure):
                replay.parse_car(changed)

    def test_output_is_outside_checkout_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = base / 'repo'
            repo.mkdir()
            for path in (repo / 'receipt.json', repo):
                with self.assertRaises(replay.ReplayFailure):
                    replay.safe_output(path, repo)
            existing = base / 'exists.json'
            existing.write_text('old')
            with self.assertRaises(replay.ReplayFailure):
                replay.safe_output(existing, repo)
            self.assertEqual(replay.safe_output(base / 'new.json', repo), (base / 'new.json').resolve())

    def test_copy_isolation_and_warnings_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            intake = Path(directory)
            pkg = intake / 'packages' / 'fixture'
            pkg.mkdir(parents=True)
            script = pkg / 'check.py'
            original = ("from pathlib import Path\nimport sys\n"
                        "Path(__file__).with_name('result.json').write_text('changed')\n"
                        "print('warning visible', file=sys.stderr)\n"
                        "print('{\"status\":\"PASS_TEST\",\"checks\":2}')\n")
            script.write_text(original)
            (pkg / 'result.json').write_text('historical')
            case = ('fixture/check.py', 'PASS_TEST', 2)
            normal = replay.run_case(intake, case, False, 10, False)
            optimized = replay.run_case(intake, case, True, 10, False)
            self.assertEqual(normal['parsed'], optimized['parsed'])
            self.assertIn('warning visible', normal['stderr'])
            self.assertEqual(normal['stderr_sha256'], replay.digest(b'warning visible\n'))
            self.assertEqual((pkg / 'result.json').read_text(), 'historical')
            self.assertEqual(script.read_text(), original)
            self.assertNotEqual(normal['command'][-1], optimized['command'][-1])
            self.assertFalse(Path(normal['command'][-1]).exists())

    def test_failure_or_invalid_result_stops_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            intake = Path(directory)
            pkg = intake / 'packages' / 'fixture'
            pkg.mkdir(parents=True)
            script = pkg / 'check.py'
            case = ('fixture/check.py', 'PASS_TEST', 2)
            with patch.object(replay, 'verifier', return_value={'result': 'verified'}):
                for source in ("raise SystemExit(7)\n", "print('{\"status\":\"FAIL\",\"checks\":2}')\n"):
                    script.write_text(source)
                    receipt = replay.replay(intake, [case], 10, False)
                    self.assertEqual(receipt['status'], 'FAIL')
                    self.assertEqual(len(receipt['runs']), 1)
                    self.assertIn('error', receipt['runs'][0])

    def test_failed_verifier_never_runs_archived_code(self):
        with patch.object(replay, 'verifier', side_effect=replay.ReplayFailure('bad archive')):
            with patch.object(replay, 'run_case') as call:
                receipt = replay.replay(Path('/does-not-matter'), [('x', 'PASS', 1)], 10, False)
        self.assertEqual(receipt['status'], 'FAIL')
        self.assertEqual(receipt['runs'], [])
        call.assert_not_called()

    def test_different_optimized_result_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            intake = Path(directory)
            pkg = intake / 'packages' / 'fixture'
            pkg.mkdir(parents=True)
            (pkg / 'check.py').write_text("import json\nprint(json.dumps({'status':'PASS_TEST','checks':2,'debug':__debug__}))\n")
            with patch.object(replay, 'verifier', return_value={'result': 'verified'}):
                receipt = replay.replay(intake, [('fixture/check.py', 'PASS_TEST', 2)], 10, False)
            self.assertEqual(receipt['status'], 'FAIL')
            self.assertIn('results differ', receipt['error'])


if __name__ == '__main__':
    unittest.main()
