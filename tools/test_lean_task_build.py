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
