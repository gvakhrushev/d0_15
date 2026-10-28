"""Negative controls for the pinned, Git-independent moving-cut byte verifier."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '02_REGISTRY/research/sources/d0_chat_integration_checks_2026-10-28/verify_moving_cut_sources.py'
spec = importlib.util.spec_from_file_location('moving_cut_integrity', SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)

DELTA_SCRIPT = ROOT / '02_REGISTRY/research/sources/d0_334_refoliation_delta_2026-10-28/verify_refoliation_source_delta.py'
delta_spec = importlib.util.spec_from_file_location('refoliation_source_integrity', DELTA_SCRIPT)
delta_verifier = importlib.util.module_from_spec(delta_spec)
delta_spec.loader.exec_module(delta_verifier)


class MovingCutSourceIntegrityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo_without_git'
        self.repo.mkdir()
        for relative in verifier.EXPECTED:
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.memo = self.repo / '02_REGISTRY/research/A4D_ROOT_BOOTSTRAP_MOVING_CUT_SOURCE_2026_10_28.md'
        self.packet = self.repo / '02_REGISTRY/research/sources/d0_root_moving_cut_2026-10-28'
        self.checker = self.packet / 'check_root_moving_cut.py'

    def test_git_not_required_and_verification_is_read_only(self) -> None:
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                  for p in self.repo.rglob('*') if p.is_file()}
        result = verifier.verify(self.repo)
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                 for p in self.repo.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['file_count'], 6)
        self.assertFalse(result['actual_git_object_store_checked'])
        self.assertFalse(result['source_code_executed'])
        self.assertFalse(result['scientific_acceptance'])
        self.assertFalse((self.repo / '.git').exists())

    def test_modified_memo_same_size_is_rejected(self) -> None:
        data = self.memo.read_bytes()
        self.memo.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            verifier.verify(self.repo)

    def test_missing_source_is_rejected(self) -> None:
        self.checker.unlink()
        with self.assertRaises(FileNotFoundError):
            verifier.verify(self.repo)

    def test_symlink_to_exact_bytes_is_rejected(self) -> None:
        data = self.checker.read_bytes()
        external = Path(self.tmp.name) / 'outside.py'
        external.write_bytes(data)
        self.checker.unlink()
        self.checker.symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Expected regular file'):
            verifier.verify(self.repo)

    def test_symlinked_packet_directory_is_rejected(self) -> None:
        external = Path(self.tmp.name) / 'outside_packet'
        self.packet.rename(external)
        self.packet.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Expected real directory'):
            verifier.verify(self.repo)

    def test_git_blob_checked_independently_of_sha256(self) -> None:
        key = next(iter(verifier.EXPECTED))
        old_sha, old_blob = verifier.EXPECTED[key]
        self.assertEqual(verifier.git_blob_sha1((self.repo / key).read_bytes()), old_blob)
        with patch.dict(verifier.EXPECTED, {key: (old_sha, '0' * 40)}):
            with self.assertRaisesRegex(ValueError, 'Git blob ID mismatch'):
                verifier.verify(self.repo)


class RefoliationDeltaSourceIntegrityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo_without_git'
        self.repo.mkdir()
        for relative in delta_verifier.EXPECTED:
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def test_pinned_source_bytes_are_read_only_and_do_not_require_git(self) -> None:
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                  for p in self.repo.rglob('*') if p.is_file()}
        result = delta_verifier.verify(self.repo)
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                 for p in self.repo.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['status'], 'PASS_PINNED_REFOLIATION_SOURCE_BYTES')
        self.assertEqual(result['source_commit'], 'c4a92cb0f2326bf7ae2a8127c49f5b65ea71ce5a')
        self.assertEqual(result['file_count'], 4)
        self.assertFalse(result['actual_git_object_store_checked'])
        self.assertFalse(result['source_code_executed'])
        self.assertFalse(result['scientific_acceptance'])

    def test_same_size_mutation_is_rejected(self) -> None:
        path = self.repo / next(iter(delta_verifier.EXPECTED))
        data = path.read_bytes()
        path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            delta_verifier.verify(self.repo)

    def test_symlink_source_is_rejected(self) -> None:
        relative = next(iter(delta_verifier.EXPECTED))
        path = self.repo / relative
        external = Path(self.tmp.name) / 'outside.md'
        external.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Expected regular file'):
            delta_verifier.verify(self.repo)


if __name__ == '__main__':
    unittest.main()
