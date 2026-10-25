#!/usr/bin/env python3
"""Cross-process controls for the serialized shared Lake cache lock."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lean_task_build


class BuildLockTests(unittest.TestCase):
    def test_source_digest_excludes_lake_dependency_checkouts(self):
        with tempfile.TemporaryDirectory(prefix="d0-source-digest-") as directory:
            formal = Path(directory)
            (formal / "D0").mkdir()
            (formal / ".lake" / "packages" / "mathlib").mkdir(parents=True)
            owned = formal / "D0" / "Owned.lean"
            dependency = formal / ".lake" / "packages" / "mathlib" / "Imported.lean"
            owned.write_text("theorem owned : True := by trivial\n", encoding="utf-8")
            dependency.write_text("-- dependency checkout\n", encoding="utf-8")

            with patch.object(lean_task_build, "FORMAL", formal):
                digest_with_dependency = lean_task_build.source_digest()
                dependency.write_text("-- changed dependency checkout\n", encoding="utf-8")
                digest_after_dependency_change = lean_task_build.source_digest()
                owned.write_text("theorem owned : True := True.intro\n", encoding="utf-8")
                digest_after_project_change = lean_task_build.source_digest()

        self.assertEqual(digest_with_dependency, digest_after_dependency_change)
        self.assertNotEqual(digest_after_dependency_change, digest_after_project_change)

    def test_source_digest_normalizes_checkout_line_endings(self):
        with tempfile.TemporaryDirectory(prefix="d0-source-line-endings-") as directory:
            root = Path(directory)
            lf_formal = root / "lf"
            crlf_formal = root / "crlf"
            for formal in (lf_formal, crlf_formal):
                (formal / "D0").mkdir(parents=True)
            source = b"theorem owned : True := by trivial\n"
            (lf_formal / "D0" / "Owned.lean").write_bytes(source)
            (crlf_formal / "D0" / "Owned.lean").write_bytes(source.replace(b"\n", b"\r\n"))

            with patch.object(lean_task_build, "FORMAL", lf_formal):
                lf_digest = lean_task_build.source_digest()
            with patch.object(lean_task_build, "FORMAL", crlf_formal):
                crlf_digest = lean_task_build.source_digest()

        self.assertEqual(lf_digest, crlf_digest)

    def test_windows_symlink_materialization_preserves_dereferenced_digest(self):
        with tempfile.TemporaryDirectory(prefix="d0-windows-symlink-") as directory:
            root = Path(directory)
            formal = root / "03_FORMALIZATION"
            link = formal / "D0" / "Research" / "Alias.lean"
            target = root / "02_REGISTRY" / "research" / "proof.lean"
            link.parent.mkdir(parents=True)
            target.parent.mkdir(parents=True)
            source = b"theorem source : True := by trivial\n"
            target.write_bytes(source)
            link_text = b"../../../02_REGISTRY/research/proof.lean"
            link.write_bytes(link_text)

            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "core.symlinks", "false"], cwd=root, check=True)
            blob = subprocess.check_output(
                ["git", "hash-object", "-w", "--stdin"], cwd=root, input=link_text
            ).decode().strip()
            subprocess.run(
                ["git", "update-index", "--add", "--cacheinfo",
                 f"120000,{blob},03_FORMALIZATION/D0/Research/Alias.lean"],
                cwd=root,
                check=True,
            )

            with patch.object(lean_task_build, "ROOT", root), patch.object(
                lean_task_build, "FORMAL", formal
            ):
                placeholder_digest = lean_task_build.source_digest()
                with lean_task_build.materialize_windows_lean_symlinks(enabled=True):
                    self.assertEqual(link.read_bytes(), source)
                    self.assertEqual(lean_task_build.source_digest(), placeholder_digest)
                self.assertEqual(link.read_bytes(), link_text)
                self.assertEqual(lean_task_build.source_digest(), placeholder_digest)

    def test_windows_symlink_materialization_refuses_local_placeholder_edits(self):
        with tempfile.TemporaryDirectory(prefix="d0-windows-symlink-edit-") as directory:
            root = Path(directory)
            formal = root / "03_FORMALIZATION"
            link = formal / "D0" / "Research" / "Alias.lean"
            target = root / "02_REGISTRY" / "research" / "proof.lean"
            link.parent.mkdir(parents=True)
            target.parent.mkdir(parents=True)
            link_text = b"../../../02_REGISTRY/research/proof.lean"
            link.write_bytes(b"local edit\n")
            target.write_bytes(b"theorem source : True := by trivial\n")

            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "core.symlinks", "false"], cwd=root, check=True)
            blob = subprocess.check_output(
                ["git", "hash-object", "-w", "--stdin"], cwd=root, input=link_text
            ).decode().strip()
            subprocess.run(
                ["git", "update-index", "--add", "--cacheinfo",
                 f"120000,{blob},03_FORMALIZATION/D0/Research/Alias.lean"],
                cwd=root,
                check=True,
            )
            original = link.read_bytes()

            with patch.object(lean_task_build, "ROOT", root), patch.object(
                lean_task_build, "FORMAL", formal
            ):
                with self.assertRaisesRegex(RuntimeError, "local edits"):
                    with lean_task_build.materialize_windows_lean_symlinks(enabled=True):
                        self.fail("a locally edited symlink placeholder was accepted")
            self.assertEqual(link.read_bytes(), original)

    def test_windows_symlink_materialization_recovers_after_interrupted_run(self):
        with tempfile.TemporaryDirectory(prefix="d0-windows-symlink-recover-") as directory:
            root = Path(directory)
            formal = root / "03_FORMALIZATION"
            link = formal / "D0" / "Research" / "Alias.lean"
            target = root / "02_REGISTRY" / "research" / "proof.lean"
            link.parent.mkdir(parents=True)
            target.parent.mkdir(parents=True)
            source = b"theorem source : True := by trivial\n"
            target.write_bytes(source)
            link_text = b"../../../02_REGISTRY/research/proof.lean"
            link.write_bytes(link_text)

            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "core.symlinks", "false"], cwd=root, check=True)
            blob = subprocess.check_output(
                ["git", "hash-object", "-w", "--stdin"], cwd=root, input=link_text
            ).decode().strip()
            subprocess.run(
                ["git", "update-index", "--add", "--cacheinfo",
                 f"120000,{blob},03_FORMALIZATION/D0/Research/Alias.lean"],
                cwd=root,
                check=True,
            )

            # Simulate a process killed after materializing the pointer but
            # before its finally block restored the checked-out representation.
            link.write_bytes(source)
            with patch.object(lean_task_build, "ROOT", root), patch.object(
                lean_task_build, "FORMAL", formal
            ):
                with lean_task_build.materialize_windows_lean_symlinks(enabled=True):
                    self.assertEqual(link.read_bytes(), source)
                self.assertEqual(link.read_bytes(), link_text)

    def test_cross_process_exclusion_preserves_lock_file_and_releases(self):
        with tempfile.TemporaryDirectory(prefix="d0-build-lock-") as directory:
            lock_path = Path(directory) / "d0-task-build.lock"
            original = b"persistent lock metadata\n"
            lock_path.write_bytes(original)
            child = (
                "import sys, time\n"
                "from pathlib import Path\n"
                "from lean_task_build import build_lock\n"
                "with build_lock(Path(sys.argv[1])):\n"
                "    print('LOCKED', flush=True)\n"
                "    time.sleep(0.5)\n"
            )
            env = os.environ.copy()
            tool_dir = str(Path(lean_task_build.__file__).resolve().parent)
            env["PYTHONPATH"] = tool_dir + os.pathsep + env.get("PYTHONPATH", "")
            proc = subprocess.Popen(
                [sys.executable, "-X", "utf8", "-c", child, str(lock_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                env=env,
            )
            self.addCleanup(self._terminate, proc)
            self.assertEqual(proc.stdout.readline().strip(), "LOCKED")

            with self.assertRaises(lean_task_build.BuildLockBusy):
                with lean_task_build.build_lock(lock_path):
                    self.fail("a second process entered the locked Lake cache")
            stdout, stderr = proc.communicate(timeout=5)
            self.assertEqual(proc.returncode, 0, stderr)
            self.assertEqual(stdout, "")
            with lean_task_build.build_lock(lock_path):
                pass
            self.assertEqual(lock_path.read_bytes(), original)

    @staticmethod
    def _terminate(proc: subprocess.Popen[str]) -> None:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
        if proc.stdout is not None:
            proc.stdout.close()
        if proc.stderr is not None:
            proc.stderr.close()


if __name__ == "__main__":
    unittest.main()
