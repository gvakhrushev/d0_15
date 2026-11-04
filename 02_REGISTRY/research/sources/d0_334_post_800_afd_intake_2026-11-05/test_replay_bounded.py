#!/usr/bin/env python3
"""Hostile controls for replay without executing the scientific checker."""
import contextlib
import hashlib
import importlib.util
import io
import json
import lzma
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

P = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bounded_replay_7fj', P / 'replay_bounded.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)

def sha(data):
    return hashlib.sha256(data).hexdigest()

class ReplayControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='d0-7fj-control-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        checker, original, memo = b'checker\n', b'constructor\n', b'previous memo\n'
        (self.root / 'check_clock_price.py').write_bytes(checker)
        (self.root / 'original_uniform_source.py').write_bytes(original)
        (self.root / 'memo.xz').write_bytes(lzma.compress(memo))
        self.manifest = {'original_constructor_path': 'source/original.py',
                         'original_constructor_sha256': sha(original),
                         'changed_blobs': {'02_REGISTRY/source.md': {'snapshot': 'memo.xz', 'head_sha256': sha(memo)}},
                         'checker_sha256': sha(checker), 'owner_counts': {'nominal_numeric': 34}}
        self.output = json.dumps({'status': 'PASS', 'check_count': 90,
                                  'classifications': self.manifest['owner_counts'], 'runtime': {}}).encode()
        rootpatch = patch.object(replay, 'P', self.root)
        manifestpatch = patch.object(replay, 'M', self.manifest)
        rootpatch.start(); self.addCleanup(rootpatch.stop)
        manifestpatch.start(); self.addCleanup(manifestpatch.stop)

    def test_each_modified_file_is_rejected_before_execution(self):
        for name in ('check_clock_price.py', 'original_uniform_source.py', 'memo.xz'):
            with self.subTest(name=name):
                path = self.root / name
                old = path.read_bytes()
                path.write_bytes(lzma.compress(b'changed') if name == 'memo.xz' else old + b'x')
                try:
                    with patch.object(replay.subprocess, 'run') as run:
                        with self.assertRaisesRegex(ValueError, 'mismatch'):
                            replay.main()
                        run.assert_not_called()
                finally:
                    path.write_bytes(old)

    def test_unexpected_stderr_is_rejected(self):
        response = unittest.mock.Mock(returncode=0, stdout=self.output, stderr=b'warning')
        with patch.object(replay.subprocess, 'run', return_value=response):
            with self.assertRaisesRegex(ValueError, 'stderr'):
                replay.main()

    def test_checker_or_scratch_change_stops_second_mode(self):
        for which in ('checker', 'memo', 'constructor'):
            with self.subTest(which=which), contextlib.redirect_stdout(io.StringIO()):
                def mutate(command, **kwargs):
                    root = Path(command[-1])
                    target = (self.root / 'check_clock_price.py' if which == 'checker' else
                              root / ('02_REGISTRY/source.md' if which == 'memo' else 'source/original.py'))
                    target.write_bytes(b'changed')
                    return unittest.mock.Mock(returncode=0, stdout=self.output, stderr=b'')
                with patch.object(replay.subprocess, 'run', side_effect=mutate) as run:
                    with self.assertRaisesRegex(ValueError, 'mismatch'):
                        replay.main()
                    self.assertEqual(run.call_count, 1)
                (self.root / 'check_clock_price.py').write_bytes(b'checker\n')

if __name__ == '__main__':
    unittest.main()
