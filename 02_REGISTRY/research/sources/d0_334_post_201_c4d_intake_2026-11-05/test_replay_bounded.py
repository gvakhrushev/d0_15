#!/usr/bin/env python3
"""Hostile controls for the bounded owner replay, with no owner code execution."""
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
spec = importlib.util.spec_from_file_location('bounded_replay', P / 'replay_bounded.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ReplayControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='d0-7fh-control-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.checker = self.root / 'check_transport.py'
        self.checker.write_bytes(b'pinned checker\n')
        source = b'pinned original constructor\n'
        (self.root / 'original_uniform_source.py').write_bytes(source)
        self.manifest = {
            'original_uniform_source_path': 'source/original.py',
            'original_uniform_source_sha256': sha(source),
            'checker_sha256': sha(self.checker.read_bytes()),
            'owner_reported_check_counts': {'nominal_numeric': 45},
        }
        self.output = json.dumps({'check_count': 65,
                                  'check_counts_by_kind': self.manifest['owner_reported_check_counts'],
                                  'environment': {}}).encode()
        self.mock_root = patch.object(replay, 'P', self.root)
        self.mock_manifest = patch.object(replay, 'M', self.manifest)
        self.mock_root.start(); self.addCleanup(self.mock_root.stop)
        self.mock_manifest.start(); self.addCleanup(self.mock_manifest.stop)

    def test_changed_checker_is_rejected_before_execution(self):
        self.checker.write_bytes(b'altered checker\n')
        with patch.object(replay.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'checker source mismatch'):
                replay.main()
            run.assert_not_called()

    def test_stderr_is_rejected_even_with_success_exit(self):
        response = unittest.mock.Mock(returncode=0, stdout=self.output, stderr=b'unexpected warning\n')
        with patch.object(replay.subprocess, 'run', return_value=response):
            with self.assertRaisesRegex(ValueError, 'checker produced stderr'):
                replay.main()

    def test_change_between_modes_is_rejected_before_second_execution(self):
        def altered_after_first(*args, **kwargs):
            self.checker.write_bytes(b'altered between modes\n')
            return unittest.mock.Mock(returncode=0, stdout=self.output, stderr=b'')
        with contextlib.redirect_stdout(io.StringIO()):
            with patch.object(replay.subprocess, 'run', side_effect=altered_after_first) as run:
                with self.assertRaisesRegex(ValueError, 'checker source mismatch'):
                    replay.main()
                self.assertEqual(run.call_count, 1)


if __name__ == '__main__':
    unittest.main()
