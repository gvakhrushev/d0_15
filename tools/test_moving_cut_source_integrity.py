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

BOUNDARY_SCRIPT = ROOT / '02_REGISTRY/research/sources/d0_334_boundary_rigidity_delta_2026-10-28/verify_boundary_rigidity_source_delta.py'
boundary_spec = importlib.util.spec_from_file_location('boundary_source_integrity', BOUNDARY_SCRIPT)
boundary_verifier = importlib.util.module_from_spec(boundary_spec)
boundary_spec.loader.exec_module(boundary_verifier)

PAID_SOURCE_SCRIPT = ROOT / '02_REGISTRY/research/sources/d0_334_paid_source_delta_2026-10-28/verify_paid_source_delta.py'
paid_source_spec = importlib.util.spec_from_file_location('paid_source_integrity', PAID_SOURCE_SCRIPT)
paid_source_verifier = importlib.util.module_from_spec(paid_source_spec)
paid_source_spec.loader.exec_module(paid_source_verifier)

GENERATED_CUT_SCRIPT = ROOT / '02_REGISTRY/research/sources/d0_334_generated_cut_application_delta_2026-10-28/verify_generated_cut_application_delta.py'
generated_cut_spec = importlib.util.spec_from_file_location('generated_cut_integrity', GENERATED_CUT_SCRIPT)
generated_cut_verifier = importlib.util.module_from_spec(generated_cut_spec)
generated_cut_spec.loader.exec_module(generated_cut_verifier)

FINAL_COMPOSITION_SCRIPT = ROOT / '02_REGISTRY/research/sources/d0_334_final_composition_delta_2026-10-28/verify_final_composition_delta.py'
final_composition_spec = importlib.util.spec_from_file_location(
    'final_composition_integrity', FINAL_COMPOSITION_SCRIPT
)
final_composition_verifier = importlib.util.module_from_spec(final_composition_spec)
final_composition_spec.loader.exec_module(final_composition_verifier)


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


class PR334DeltaSourceIntegrityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo_without_git'
        self.repo.mkdir()

    def copy_packet(self, packet: str) -> Path:
        target = self.repo / packet
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(ROOT / packet, target)
        return target

    def test_boundary_delta_is_read_only_and_detects_same_size_mutation(self) -> None:
        packet = self.copy_packet(boundary_verifier.PACKET)
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                  for p in self.repo.rglob('*') if p.is_file()}
        result = boundary_verifier.verify(self.repo)
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                 for p in self.repo.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['status'], 'PASS_PINNED_BOUNDARY_RIGIDITY_SOURCE_BYTES')
        self.assertEqual(result['file_count'], 21)
        self.assertFalse(result['source_code_executed_by_verifier'])
        self.assertFalse(result['scientific_acceptance'])
        manifest = __import__('json').loads((packet / 'MANIFEST.json').read_bytes())
        source = packet / manifest['files'][0]['snapshot_path']
        data = source.read_bytes()
        source.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            boundary_verifier.verify(self.repo)

    def test_paid_source_delta_is_read_only_and_detects_symlinks(self) -> None:
        packet = self.copy_packet(paid_source_verifier.PACKET)
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                  for p in self.repo.rglob('*') if p.is_file()}
        result = paid_source_verifier.verify(self.repo)
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                 for p in self.repo.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['status'], 'PASS_PINNED_PAID_SOURCE_AND_REPLAY_BYTES')
        self.assertEqual(result['replay_input_count'], 7)
        self.assertEqual(result['replayed_checker_count'], 3)
        self.assertFalse(result['source_code_executed_by_verifier'])
        self.assertFalse(result['scientific_acceptance'])
        extracted = __import__('json').loads((packet / 'EXTRACTED_CHECKS.json').read_bytes())
        source = packet / 'replay' / 'inputs' / extracted['replay_input_files'][0]['snapshot_path'].split('replay/inputs/', 1)[-1]
        external = Path(self.tmp.name) / 'external-input'
        external.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Expected regular file'):
            paid_source_verifier.verify(self.repo)

    def test_generated_cut_delta_is_read_only_and_detects_same_size_mutation(self) -> None:
        self.copy_packet(paid_source_verifier.PACKET)
        packet = self.copy_packet(generated_cut_verifier.PACKET)
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                  for p in self.repo.rglob('*') if p.is_file()}
        result = generated_cut_verifier.verify(self.repo)
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                 for p in self.repo.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['status'], 'PASS_PINNED_GENERATED_CUT_SOURCE_AND_REPLAY_BYTES')
        self.assertEqual(result['source_commit'], '5fe5203da2439d325dc9ef70f52c1111822fc22b')
        self.assertEqual(result['upstream_file_count'], 6)
        self.assertEqual(result['replay_input_count'], 3)
        self.assertEqual(result['replayed_checker_count'], 2)
        self.assertLessEqual(result['max_numeric_difference_from_published'], 3e-14)
        self.assertFalse(result['source_code_executed_by_verifier'])
        self.assertFalse(result['scientific_acceptance'])
        manifest = __import__('json').loads((packet / 'MANIFEST.json').read_bytes())
        memo_entry = next(row for row in manifest['files'] if row['storage'] == 'patch' and
                          row['upstream_path'].endswith('A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'))
        patch = packet / memo_entry['patch_path']
        data = patch.read_bytes()
        patch.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, 'Pinned source patch mismatch'):
            generated_cut_verifier.verify(self.repo)


class PR334FinalCompositionSourceIntegrityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo_without_git'
        self.repo.mkdir()
        self.packet = self.repo / final_composition_verifier.PACKET
        self.packet.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            ROOT / final_composition_verifier.PACKET,
            self.packet,
        )

    def test_source_and_replay_receipts_verify_without_git_or_execution(self) -> None:
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                  for p in self.repo.rglob('*') if p.is_file()}
        result = final_composition_verifier.verify(self.repo)
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes()
                 for p in self.repo.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['status'], 'PASS_PINNED_FINAL_COMPOSITION_SOURCE_AND_REPLAYS')
        self.assertEqual(result['source_commit'], '22e729996b70a699710a2d1120a0caa7a08decf8')
        self.assertEqual(result['file_count'], 31)
        self.assertEqual(result['source_bytes'], 248546)
        self.assertEqual(result['replayed_checker_count'], 7)
        self.assertFalse(result['source_code_executed_by_verifier'])
        self.assertFalse(result['scientific_acceptance'])
        self.assertFalse(result['physical_admission'])
        self.assertFalse(result['GR_closed'])
        self.assertFalse((self.repo / '.git').exists())

    def test_same_size_upstream_mutation_is_rejected(self) -> None:
        import json
        manifest = json.loads((self.packet / 'MANIFEST.json').read_bytes())
        source = self.packet / manifest['files'][0]['snapshot_path']
        data = source.read_bytes()
        source.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            final_composition_verifier.verify(self.repo)

    def test_symlinked_source_snapshot_is_rejected(self) -> None:
        import json
        manifest = json.loads((self.packet / 'MANIFEST.json').read_bytes())
        source = self.packet / manifest['files'][0]['snapshot_path']
        external = Path(self.tmp.name) / 'external-source'
        external.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(external)
        with self.assertRaisesRegex(ValueError, 'Expected regular file'):
            final_composition_verifier.verify(self.repo)


if __name__ == '__main__':
    unittest.main()
