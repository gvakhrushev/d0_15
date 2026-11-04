import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import lean_task_build as build


class OrdinaryResolverTests(unittest.TestCase):
    def test_existing_path_does_not_use_windows_fallback(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)
            with patch.object(build, "_windows_handle_guid_path", side_effect=AssertionError("fallback used")):
                self.assertEqual(build._strict_physical_path(path), path.resolve(strict=True))

    @unittest.skipUnless(os.name == "nt", "Windows error codes required")
    def test_fallback_only_for_missing_dos_name(self):
        import ctypes
        path = Path("fixture")
        with patch.object(Path, "resolve", side_effect=ctypes.WinError(5)), patch.object(build, "_windows_handle_guid_path", side_effect=AssertionError("fallback used")):
            with self.assertRaises(OSError):
                build._strict_physical_path(path)
        with patch.object(Path, "resolve", side_effect=ctypes.WinError(3)), patch.object(build, "_windows_handle_guid_path", return_value=path) as fallback:
            self.assertEqual(build._strict_physical_path(path), path)
            fallback.assert_called_once_with(path)

    def test_missing_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(OSError):
                build._strict_physical_path(Path(temporary) / "missing")


@unittest.skipUnless(os.name == "nt", "Windows GUID handles required")
class WindowsGuidPathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="d0-guid-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        (self.root / "tracked.lean").write_bytes(b"-- tracked\n")

    def test_forced_guid_resolution_returns_same_file_and_relative_path(self):
        with patch.object(build, "_strict_physical_path", side_effect=build._windows_handle_guid_path):
            path, relative = build._contained_file(self.root, self.root / "tracked.lean")
        self.assertEqual(relative.as_posix(), "tracked.lean")
        self.assertEqual(path.read_bytes(), b"-- tracked\n")
        self.assertTrue(str(path).startswith("\\\\?\\Volume{"))

    def test_mixed_dos_and_guid_paths_normalize_same_physical_objects(self):
        # Both namespaces name real objects in one physical tree; simulate
        # resolution producing different namespaces, not an OS WinError 3.
        ordinary_root = self.root.resolve(strict=True)
        ordinary_target = (self.root / "tracked.lean").resolve(strict=True)
        guid_root = build._windows_handle_guid_path(self.root)
        guid_target = build._windows_handle_guid_path(self.root / "tracked.lean")
        for root_result, target_result in ((ordinary_root, guid_target), (guid_root, ordinary_target)):
            with self.subTest(root_namespace=root_result.anchor, target_namespace=target_result.anchor):
                self.assertTrue(build._windows_directory_contains(root_result, target_result.parent))
                with patch.object(build, "_strict_physical_path", side_effect=[root_result, target_result]):
                    actual, relative = build._contained_file(self.root, self.root / "tracked.lean")
                self.assertEqual(relative.as_posix(), "tracked.lean")
                self.assertTrue(build._windows_same_file(actual, ordinary_target))

    def test_mixed_namespace_rejects_object_swapped_during_normalization(self):
        ordinary_root = self.root.resolve(strict=True)
        ordinary_target = (self.root / "tracked.lean").resolve(strict=True)
        guid_target = build._windows_handle_guid_path(ordinary_target)
        outside = self.base / "outside.lean"
        outside.write_bytes(b"-- impostor\n")
        guid_outside = build._windows_handle_guid_path(outside)
        guid_root = build._windows_handle_guid_path(ordinary_root)
        with patch.object(build, "_strict_physical_path", side_effect=[ordinary_root, guid_target]):
            with patch.object(build, "_windows_handle_guid_path", side_effect=[guid_root, guid_outside]):
                with self.assertRaisesRegex(ValueError, "normalization changed"):
                    build._contained_file(self.root, ordinary_target)

    def test_mixed_namespace_rejects_root_swapped_during_normalization(self):
        ordinary_root = self.root.resolve(strict=True)
        ordinary_target = (self.root / "tracked.lean").resolve(strict=True)
        guid_target = build._windows_handle_guid_path(ordinary_target)
        outside = self.base / "outside"
        outside.mkdir()
        guid_outside = build._windows_handle_guid_path(outside)
        with patch.object(build, "_strict_physical_path", side_effect=[ordinary_root, guid_target]):
            with patch.object(build, "_windows_handle_guid_path", side_effect=[guid_outside, guid_target]):
                with self.assertRaisesRegex(ValueError, "normalization changed"):
                    build._contained_file(self.root, ordinary_target)

    def test_external_junction_is_rejected_even_if_filename_exists(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "tracked.lean").write_bytes(b"-- outside\n")
        link = self.root / "escape"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], check=True, capture_output=True)
        try:
            with patch.object(build, "_strict_physical_path", side_effect=build._windows_handle_guid_path):
                with self.assertRaises(ValueError):
                    build._contained_file(self.root, link / "tracked.lean")
        finally:
            os.rmdir(link)
        self.assertEqual((outside / "tracked.lean").read_bytes(), b"-- outside\n")

    def test_missing_target_rejected_even_on_guid_fallback(self):
        with patch.object(build, "_strict_physical_path", side_effect=build._windows_handle_guid_path):
            with self.assertRaises(OSError):
                build._contained_file(self.root, self.root / "missing.lean")

    def test_untracked_but_existing_symlink_target_is_rejected(self):
        formal = self.base / "formal"
        package = formal / ".lake" / "packages" / "fixture"
        package.mkdir(parents=True)
        def git(*args, input=None):
            return subprocess.check_output(["git", "-C", str(package), *args], input=input, stderr=subprocess.PIPE).decode().strip()
        git("init", "-q")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "user.name", "Fixture")
        git("config", "core.autocrlf", "false")
        git("config", "core.symlinks", "false")
        (package / ".gitignore").write_bytes(b"target.lean\n")
        (package / "target.lean").write_bytes(b"-- tracked target\n")
        (package / "alias.lean").write_bytes(b"target.lean")
        git("add", ".gitignore")
        git("add", "-f", "target.lean")
        symlink_blob = git("hash-object", "-w", "--stdin", input=b"target.lean")
        git("update-index", "--add", "--cacheinfo", f"120000,{symlink_blob},alias.lean")
        git("commit", "-qm", "tracked target")
        def set_manifest():
            data = {"packagesDir": ".lake/packages", "packages": [{"name": "fixture", "type": "git", "rev": git("rev-parse", "HEAD")}]}
            (formal / "lake-manifest.json").write_text(json.dumps(data), encoding="utf-8")
        set_manifest()
        with patch.object(build, "FORMAL", formal), patch.object(build, "_strict_physical_path", side_effect=build._windows_handle_guid_path):
            self.assertEqual(len(build.dependency_provenance()["packages"]), 1)
            git("rm", "--cached", "-q", "target.lean")
            git("commit", "-qm", "untrack target")
            set_manifest()
            with self.assertRaisesRegex(build.DependencyProvenanceError, "symlink target is not tracked"):
                build.dependency_provenance()

    def test_case_sensitive_sibling_junction_is_rejected(self):
        case_base = self.base / "case_sensitive"
        case_base.mkdir()
        cp = subprocess.run(["fsutil", "file", "setCaseSensitiveInfo", str(case_base), "enable"], capture_output=True)
        if cp.returncode:
            self.skipTest("filesystem did not allow case-sensitive directories")
        physical_base = build._windows_handle_guid_path(case_base)
        inside = physical_base / "repo"
        outside = physical_base / "REPO"
        inside.mkdir()
        outside.mkdir()
        (outside / "tracked.lean").write_bytes(b"-- outside\n")
        link = inside / "escape"
        subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], check=True, capture_output=True)
        try:
            with patch.object(build, "_strict_physical_path", side_effect=build._windows_handle_guid_path):
                with self.assertRaises(ValueError):
                    build._contained_file(inside, link / "tracked.lean")
        finally:
            os.rmdir(link)
        self.assertEqual((outside / "tracked.lean").read_bytes(), b"-- outside\n")


if __name__ == "__main__":
    unittest.main()
