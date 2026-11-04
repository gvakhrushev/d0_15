#!/usr/bin/env python3
"""Hostile replay controls: no real owner code is executed by these tests."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

P = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bounded_replay_7fi', P / 'replay_bounded.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ReplayControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='d0-7fi-control-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        files = {'check_born_history.py': b'checker\n', 'original_uniform_source.py': b'original\n',
                 'predecessor_checker.py': b'previous\n'}
        for name, data in files.items():
            (self.root / name).write_bytes(data)
        self.manifest = {'original_uniform_source_path': 'source/original.py',
                         'predecessor_primary_path': 'source/primary.md',
                         'checker_sha256': sha(files['check_born_history.py']),
                         'original_uniform_source_sha256': sha(files['original_uniform_source.py']),
                         'predecessor_checker_sha256': sha(files['predecessor_checker.py']),
                         'owner_reported_check_counts': {'nominal_numeric': 42}}
        self.output = json.dumps({'status': 'PASS', 'check_count': 65,
                                  'classifications': self.manifest['owner_reported_check_counts'],
                                  'runtime': {}}).encode()
        self.rootpatch = patch.object(replay, 'P', self.root)
        self.manifestpatch = patch.object(replay, 'M', self.manifest)
        self.rootpatch.start(); self.addCleanup(self.rootpatch.stop)
        self.manifestpatch.start(); self.addCleanup(self.manifestpatch.stop)

    def test_each_modified_input_fails_before_running_checker(self):
        for name in ('check_born_history.py', 'original_uniform_source.py', 'predecessor_checker.py'):
            with self.subTest(file=name):
                path = self.root / name
                original = path.read_bytes()
                path.write_bytes(original + b'altered')
                try:
                    with patch.object(replay.subprocess, 'run') as run:
                        with self.assertRaisesRegex(ValueError, 'mismatch'):
                            replay.main()
                        run.assert_not_called()
                finally:
                    path.write_bytes(original)

    def test_stderr_rejected_even_when_exit_is_zero(self):
        response = unittest.mock.Mock(returncode=0, stdout=self.output, stderr=b'unexpected warning\n')
        with patch.object(replay.subprocess, 'run', return_value=response):
            with self.assertRaisesRegex(ValueError, 'checker produced stderr'):
                replay.main()

    def test_modified_predecessor_between_modes_stops_second_run(self):
        def modify_after_first(*args, **kwargs):
            (self.root / 'predecessor_checker.py').write_bytes(b'altered')
            return unittest.mock.Mock(returncode=0, stdout=self.output, stderr=b'')
        with contextlib.redirect_stdout(io.StringIO()):
            with patch.object(replay.subprocess, 'run', side_effect=modify_after_first) as run:
                with self.assertRaisesRegex(ValueError, 'predecessor mismatch'):
                    replay.main()
                self.assertEqual(run.call_count, 1)


if __name__ == '__main__':
    unittest.main()
