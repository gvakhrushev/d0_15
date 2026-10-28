#!/usr/bin/env python3
"""Cross-process controls for the serialized shared Lake cache lock."""
from __future__ import annotations

import os
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lean_task_build

REAL_TOOLCHAIN_SNAPSHOT = lean_task_build.toolchain_snapshot


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


class DependencyProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="d0-build-provenance-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        self.formal = self.root / "03_FORMALIZATION"
        self.package = self.formal / ".lake/packages/fixture"
        self.package.mkdir(parents=True)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        (self.package / ".gitignore").write_text("*.ignored.lean\n.lake/\n", encoding="utf-8")
        (self.package / "Input.lean").write_text("-- pinned\n", encoding="utf-8")
        (self.package / "notes.md").write_text("tracked\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.write_manifest()
        (self.formal / "D0").mkdir()
        (self.formal / "D0/Owned.lean").write_text("-- owned\n", encoding="utf-8")
        (self.formal / "lean-toolchain").write_text("leanprover/lean4:v4\n", encoding="utf-8")
        self.lake = self.formal / ".lake"
        self.stamp = self.lake / "d0-final-build-receipt.json"
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(lean_task_build, "toolchain_snapshot", return_value={"fixture": "v1"}))
        for name, value in (("ROOT", self.root), ("FORMAL", self.formal), ("LAKE", self.lake),
                            ("LOCK", self.lake / "d0-task-build.lock"), ("STAMP", self.stamp)):
            self.stack.enter_context(patch.object(lean_task_build, name, value))

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.package), *args], stderr=subprocess.PIPE).decode().strip()

    def write_manifest(self):
        head = self.git("rev-parse", "HEAD")
        data = {"packagesDir": ".lake/packages", "packages": [{"name": "fixture", "type": "git", "rev": head}]}
        (self.formal / "lake-manifest.json").write_text(json.dumps(data), encoding="utf-8")

    def test_manifest_and_clean_pinned_git_are_bound(self):
        snapshot = lean_task_build.dependency_provenance()
        self.assertEqual(snapshot["packages"][0]["revision"], self.git("rev-parse", "HEAD"))
        before = lean_task_build.dependency_provenance_digest(snapshot)
        manifest = self.formal / "lake-manifest.json"
        manifest.write_text(manifest.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.assertNotEqual(before, lean_task_build.dependency_provenance_digest(lean_task_build.dependency_provenance()))
        manifest.write_text('{"packagesDir":".lake/packages","packages":[]}', encoding="utf-8")
        self.assertEqual(lean_task_build.dependency_provenance()["packages"], [])

    def test_dirty_and_hidden_sources_fail_closed(self):
        mutations = ["notes.md", "Fresh.lean", "new.ignored.lean", "arbitrary-input", ".lake/custom/lakefile.toml", ".lake/build/lib/New.lean"]
        for name in mutations:
            with self.subTest(name=name):
                path = self.package / name
                old = path.read_bytes() if path.exists() else None
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("changed\n", encoding="utf-8")
                with self.assertRaises(lean_task_build.DependencyProvenanceError):
                    lean_task_build.dependency_provenance()
                if old is None:
                    path.unlink()
                else:
                    path.write_bytes(old)
        self.git("update-index", "--assume-unchanged", "Input.lean")
        with self.assertRaises(lean_task_build.DependencyProvenanceError):
            lean_task_build.dependency_provenance()
        self.git("update-index", "--no-assume-unchanged", "Input.lean")
        self.git("update-index", "--skip-worktree", "Input.lean")
        with self.assertRaises(lean_task_build.DependencyProvenanceError):
            lean_task_build.dependency_provenance()

    def test_generated_build_cache_is_explicitly_outside_scope(self):
        artifact = self.package / ".lake/build/ir/Cache.c"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("generated", encoding="utf-8")
        self.assertIn("caches", lean_task_build.dependency_provenance()["boundary"])

    def test_tracked_bytes_verified_even_if_git_diff_misses_edit(self):
        (self.package / "notes.md").write_text("altered\n", encoding="utf-8")
        real_run = subprocess.run
        def pretend_clean(command, *args, **kwargs):
            if isinstance(command, list) and "diff" in command and "--quiet" in command:
                return subprocess.CompletedProcess(command, 0)
            return real_run(command, *args, **kwargs)
        with patch.object(lean_task_build.subprocess, "run", side_effect=pretend_clean):
            with self.assertRaisesRegex(lean_task_build.DependencyProvenanceError, "bytes differ"):
                lean_task_build.dependency_provenance()

    def test_external_source_search_path_refused(self):
        with patch.dict(os.environ, {"LEAN_PATH": str(self.root)}, clear=False):
            with self.assertRaises(lean_task_build.DependencyProvenanceError):
                lean_task_build.build_environment_digest()

    def test_symlink_to_untracked_or_external_source_refused(self):
        (self.package / "Unsafe.lean").symlink_to(self.root / "external.lean")
        (self.root / "external.lean").write_text("-- external\n", encoding="utf-8")
        self.git("add", "Unsafe.lean")
        self.git("commit", "-qm", "external link")
        self.write_manifest()
        with self.assertRaises(lean_task_build.DependencyProvenanceError):
            lean_task_build.dependency_provenance()

    def test_receipt_rejects_dirty_dependency_and_rebuilds_changed_pin(self):
        marker = self.root / "builds"
        command = [sys.executable, "-c", "from pathlib import Path; import sys; p=Path(sys.argv[1]); p.write_text(p.read_text()+'x' if p.exists() else 'x')", str(marker)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 0)
            receipt = json.loads(self.stamp.read_text())
            self.assertEqual(receipt["dependency_sha256"], lean_task_build.dependency_provenance_digest(receipt["dependencies"]))
            # A documentation-only change does not alter verified build inputs.
            (self.root / "DOC.md").write_text("documentation only", encoding="utf-8")
            self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 0)
            self.assertEqual(marker.read_text(), "x")
            # A documentation change over an unbuilt Lean edit must not reuse success.
            (self.formal / "D0/Owned.lean").write_text("-- changed source\n", encoding="utf-8")
            (self.root / "DOC.md").write_text("updated docs", encoding="utf-8")
            self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 0)
            self.assertEqual(marker.read_text(), "xx")
            (self.package / "Input.lean").write_text("-- new\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 3)
            self.assertEqual(marker.read_text(), "xx")
            self.git("add", "Input.lean")
            self.git("commit", "-qm", "new dependency")
            self.write_manifest()
            self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 0)
            self.assertEqual(marker.read_text(), "xxx")
            self.assertNotEqual(receipt["dependency_sha256"], json.loads(self.stamp.read_text())["dependency_sha256"])

    def test_narrow_success_emits_input_receipt(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(lean_task_build.run_locked([sys.executable, "-c", "pass"], "D0.Fixture"), 0)
        line = next(line for line in output.getvalue().splitlines() if line.startswith("D0_BUILD_RECEIPT "))
        receipt = json.loads(line.removeprefix("D0_BUILD_RECEIPT "))
        self.assertEqual(receipt["target"], "D0.Fixture")
        self.assertEqual(receipt["dependency_sha256"], lean_task_build.dependency_provenance_digest(receipt["dependencies"]))
        self.assertFalse(self.stamp.exists())

    def test_toolchain_snapshot_with_isolated_path_and_elan_stubs(self):
        tool_dir = self.root / "bin"
        tool_dir.mkdir()
        lean = tool_dir / "lean"
        lake = tool_dir / "lake"
        elan = tool_dir / "elan"
        lean.write_text("#!" + sys.executable + "\nprint('Lean fixture')\n", encoding="utf-8")
        lake.write_text("#!" + sys.executable + "\nimport sys\nprint('Lean fixture' if sys.argv[1:]==['env','lean','--version'] else 'Lake fixture')\n", encoding="utf-8")
        elan.write_text("#!" + sys.executable + "\nimport sys\nfrom pathlib import Path\nprint(Path(__file__).parent / sys.argv[2])\n", encoding="utf-8")
        for tool in (lean, lake, elan):
            tool.chmod(0o755)
        def which(name):
            return str(tool_dir / name) if name in {"lean", "lake", "elan"} else None
        with patch.object(lean_task_build.shutil, "which", side_effect=which):
            snapshot = REAL_TOOLCHAIN_SNAPSHOT()
            self.assertEqual(snapshot["selected"]["lean"]["resolved_path"], str(lean.resolve()))
            self.assertEqual(snapshot["selected"]["lake"]["resolved_path"], str(lake.resolve()))
            self.assertEqual(snapshot["lean_version"]["stdout"], "Lean fixture")
            self.assertEqual(snapshot["lake_version"]["stdout"], "Lake fixture")
            lean.write_text(lean.read_text() + "# changed executable\n", encoding="utf-8")
            changed = REAL_TOOLCHAIN_SNAPSHOT()
            self.assertNotEqual(snapshot["selected"]["lean"]["sha256"], changed["selected"]["lean"]["sha256"])
            lake.unlink()
            with self.assertRaises(lean_task_build.DependencyProvenanceError):
                REAL_TOOLCHAIN_SNAPSHOT()

    def test_toolchain_path_fallback_and_version_failure(self):
        tool_dir = self.root / "bin"
        tool_dir.mkdir()
        lean, lake = tool_dir / "lean", tool_dir / "lake"
        lean.write_text("#!" + sys.executable + "\nprint('Lean fixture')\n", encoding="utf-8")
        lake.write_text("#!" + sys.executable + "\nprint('Version fixture')\n", encoding="utf-8")
        for tool in (lean, lake):
            tool.chmod(0o755)
        def which(name):
            return str(tool_dir / name) if name in {"lean", "lake"} else None
        with patch.object(lean_task_build.shutil, "which", side_effect=which):
            snapshot = REAL_TOOLCHAIN_SNAPSHOT()
            self.assertEqual(snapshot["resolution"], "PATH")
            self.assertEqual(snapshot["lean_version"]["command"][1:], ["env", "lean", "--version"])
            self.assertEqual(snapshot["lake_version"]["command"][1:], ["--version"])
            lake.write_text("#!" + sys.executable + "\nraise SystemExit(1)\n", encoding="utf-8")
            with self.assertRaises(lean_task_build.DependencyProvenanceError):
                REAL_TOOLCHAIN_SNAPSHOT()

    def test_toolchain_changes_invalidate_final_and_inflight_receipts(self):
        command = [sys.executable, "-c", "pass"]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with patch.object(lean_task_build, "toolchain_snapshot", side_effect=[{"sha": "a"}, {"sha": "b"}]):
                self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 3)
                self.assertFalse(self.stamp.exists())
            with patch.object(lean_task_build, "toolchain_snapshot", return_value={"sha": "a"}):
                self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 0)
                self.assertEqual(json.loads(self.stamp.read_text())["toolchain"], {"sha": "a"})
            with patch.object(lean_task_build, "toolchain_snapshot", return_value={"sha": "b"}) as snapshot:
                self.assertEqual(lean_task_build.run_locked(command, "D0.All", final=True), 0)
                self.assertEqual(snapshot.call_count, 2)  # rebuilt, did not skip
                self.assertEqual(json.loads(self.stamp.read_text())["toolchain"], {"sha": "b"})

    def test_narrow_and_final_reject_dependency_mutation_during_build(self):
        command = [sys.executable, "-c", "from pathlib import Path; import sys; Path(sys.argv[1]).write_text('-- changed\\n')", str(self.package / "Input.lean")]
        for final in (False, True):
            with self.subTest(final=final), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(lean_task_build.run_locked(command, "D0.All" if final else "D0.Fixture", final=final), 3)
                self.assertFalse(self.stamp.exists())
                self.git("restore", "Input.lean")

    def test_failed_forced_rebuild_does_not_leave_old_success(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(lean_task_build.run_locked([sys.executable, "-c", "pass"], "D0.All", final=True), 0)
            self.assertTrue(self.stamp.exists())
            self.assertEqual(lean_task_build.run_locked([sys.executable, "-c", "raise SystemExit(4)"], "D0.All", final=True, force=True), 4)
            self.assertFalse(self.stamp.exists())


if __name__ == "__main__":
    unittest.main()
