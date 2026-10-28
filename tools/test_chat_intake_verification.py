"""Tests for read-only verification of the pinned historical chat intake."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / '02_REGISTRY/research/sources/d0_chat_intake_2026-10-28'
spec = importlib.util.spec_from_file_location('chat_intake_verifier', INTAKE / 'verify_intake.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class ChatIntakeVerificationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.copy = Path(self.temp.name) / 'intake'
        shutil.copytree(INTAKE, self.copy)
        self.sample = self.copy / 'packages/D0_closed_source_cone_2026-10-27/README_RU.md'

    def test_actual_member_bytes_and_read_only_behavior(self) -> None:
        def state():
            return {p.relative_to(self.copy).as_posix(): p.read_bytes()
                    for p in self.copy.rglob('*') if p.is_file()}
        before = state()
        result = verifier.verify(self.copy)
        self.assertEqual(state(), before)
        self.assertEqual((result['member_files'], result['member_bytes'], result['packages']),
                         (74, 650121, 9))
        self.assertEqual(result['zip_archive_bytes_and_sha256'], 'NOT_VERIFIED')
        self.assertFalse(result['archived_code_executed'])

    def test_same_size_mutation_fails_digest(self) -> None:
        data = self.sample.read_bytes()
        self.sample.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, 'Member digest mismatch'):
            verifier.verify(self.copy)

    def test_missing_source_fails_path_set(self) -> None:
        self.sample.unlink()
        with self.assertRaisesRegex(ValueError, 'Member path set mismatch'):
            verifier.verify(self.copy)

    def test_extra_source_fails_path_set(self) -> None:
        (self.sample.parent / 'extra.py').write_text('not an archive member')
        with self.assertRaisesRegex(ValueError, 'Member path set mismatch'):
            verifier.verify(self.copy)

    def test_symlink_cannot_replace_source_or_directory(self) -> None:
        target = self.sample.read_bytes()
        self.sample.unlink()
        external = Path(self.temp.name) / 'outside'
        external.write_bytes(target)
        self.sample.symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'non-regular member'):
            verifier.verify(self.copy)
        self.sample.unlink()
        self.sample.write_bytes(target)
        package = self.sample.parent
        moved = Path(self.temp.name) / 'moved_package'
        package.rename(moved)
        package.symlink_to(moved, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'real directory'):
            verifier.verify(self.copy)

    def test_traversal_and_metadata_tampering_fail_closed(self) -> None:
        for path in ('../escape', 'a/../../escape', '/absolute', 'a\\escape', 'a//b', './x', 'C:escape', 'C:/escape'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                verifier.safe_relative(path)
        ledger = self.copy / 'upstream/FILES.md'
        ledger.write_bytes(ledger.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'Upstream digest mismatch'):
            verifier.verify(self.copy)


if __name__ == '__main__':
    unittest.main()
