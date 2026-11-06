#!/usr/bin/env python3
"""Hostile controls: never execute owner code in this test."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('replay_7fk',P/'replay_bounded.py')
replay=importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)

class ReplayControls(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='d0-7fk-control-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.checker=self.root/'check_retention_collar.py'
        self.checker.write_bytes(b'original\n')
        manifest={'checker_sha256':hashlib.sha256(self.checker.read_bytes()).hexdigest(),
                  'owner_reported_check_count':140,'owner_reported_check_counts':{'nominal_numeric':5}}
        self.output=json.dumps({'status':'PASS','check_count':140,'classifications':{'nominal_numeric':5},'runtime':{}}).encode()
        rootpatch=patch.object(replay,'P',self.root);rootpatch.start();self.addCleanup(rootpatch.stop)
        manpatch=patch.object(replay,'M',manifest);manpatch.start();self.addCleanup(manpatch.stop)

    def test_modified_checker_not_executed(self):
        self.checker.write_bytes(b'altered')
        with patch.object(replay.subprocess,'run') as run:
            with self.assertRaisesRegex(ValueError,'checker source mismatch'):replay.main()
            run.assert_not_called()

    def test_changed_between_modes_stops_second_execution(self):
        def first(*args,**kwargs):
            self.checker.write_bytes(b'altered')
            return unittest.mock.Mock(returncode=0,stdout=self.output,stderr=b'')
        with contextlib.redirect_stdout(io.StringIO()), patch.object(replay.subprocess,'run',side_effect=first) as run:
            with self.assertRaisesRegex(ValueError,'checker source mismatch'):replay.main()
            self.assertEqual(run.call_count,1)

    def test_stderr_even_with_exit_zero_is_rejected(self):
        response=unittest.mock.Mock(returncode=0,stdout=self.output,stderr=b'warning')
        with patch.object(replay.subprocess,'run',return_value=response):
            with self.assertRaisesRegex(ValueError,'checker produced stderr'):replay.main()

if __name__=='__main__':unittest.main()
