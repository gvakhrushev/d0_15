#!/usr/bin/env python3
"""Fast fixture-repository controls for snapshot isolation and replay failures."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import run_research_certs as runner


class ReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="d0-replay-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Replay fixture")
        (self.repo / "tracked.txt").write_text("original\n")
        self.cert_dir = self.repo / runner.CERT_DIR
        self.cert_dir.mkdir(parents=True)
        self.commit()

    def git(self, *args: str) -> str:
        return runner.git(self.repo, *args).decode().strip()

    def commit(self) -> str:
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def certificate(self, name: str, body: str) -> str:
        path = self.cert_dir / name
        path.write_text(body, encoding="utf-8")
        return str(path.relative_to(self.repo))

    def run_one(self, name: str, body: str) -> tuple[dict, Path]:
        cert = self.certificate(name, body)
        commit = self.commit()
        logs = self.root / f"logs-{name}"
        logs.mkdir()
        result = runner.run_certificate(self.repo, commit, cert, logs)
        # Only the source fixture checkout survives, including on failure.
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual((self.repo / "tracked.txt").read_text(), "original\n")
        return result, Path(result["logs"])

    def test_exit_failure_preserves_both_output_streams(self) -> None:
        result, logs = self.run_one("failure.py", "import os\nos.write(1, b'out\\x00\\n')\nos.write(2, b'err\\xff\\n')\nraise SystemExit(7)\n")
        self.assertEqual((result["status"], result["returncode"]), ("FAIL", 7), result)
        self.assertEqual((logs / "stdout.log").read_bytes(), b"out\x00\n")
        self.assertEqual((logs / "stderr.log").read_bytes(), b"err\xff\n")

    def test_timeout_keeps_output_and_removes_worktree(self) -> None:
        with patch.object(runner, "certificate_timeout", return_value=0.15):
            result, logs = self.run_one("slow.py", "import time\nprint('before timeout', flush=True)\ntime.sleep(30)\n")
        self.assertEqual((result["status"], result["returncode"]), ("TIMEOUT", 124))
        self.assertIn(b"before timeout", (logs / "stdout.log").read_bytes())

    def test_tracked_and_index_mutations_fail_with_diagnostics(self) -> None:
        for staged in (False, True):
            with self.subTest(staged=staged):
                body = "from pathlib import Path\nPath('tracked.txt').write_text('changed\\n')\n"
                if staged:
                    body += "import subprocess\nsubprocess.run(['git', 'add', 'tracked.txt'], check=True)\n"
                result, logs = self.run_one(f"mutate_{int(staged)}.py", body)
                self.assertEqual(result["status"], "MUTATION")
                self.assertEqual(result["execution_status"], "PASS")
                self.assertIn(b"changed", (logs / "tracked.patch").read_bytes())
                self.assertTrue((logs / "tracked-status.txt").read_bytes())
                if staged:
                    self.assertIn(b"changed", (logs / "index.patch").read_bytes())

    def test_committing_a_mutation_cannot_hide_it(self) -> None:
        result, logs = self.run_one("commit.py", "import subprocess\nfrom pathlib import Path\nPath('tracked.txt').write_text('committed change\\n')\nsubprocess.run(['git', 'add', '.'], check=True)\nsubprocess.run(['git', 'commit', '-qm', 'hidden mutation'], check=True)\n")
        self.assertEqual(result["status"], "MUTATION")
        self.assertNotEqual(result["head_after"], result["commit"])
        self.assertIn(b"committed change", (logs / "tracked.patch").read_bytes())

    def test_parallel_generators_have_independent_products(self) -> None:
        barrier = self.root / "barrier"
        barrier.mkdir()
        certs = []
        for name, partner in (("a", "b"), ("b", "a")):
            body = (
                "from pathlib import Path\nimport time\n"
                "with open('common-product.json', 'x') as output: output.write('isolated')\n"
                f"barrier = Path({str(barrier)!r})\n"
                f"(barrier / {name!r}).touch()\n"
                "deadline = time.monotonic() + 3\n"
                f"while not (barrier / {partner!r}).exists():\n"
                "    assert time.monotonic() < deadline, 'not parallel'\n"
                "    time.sleep(0.01)\n"
                "print('parallel isolated pass')\n"
            )
            certs.append(self.certificate(f"{name}.py", body))
        commit = self.commit()
        logs = self.root / "parallel-logs"
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            results = runner.replay(self.repo, commit, certs, 2, logs)
        self.assertEqual([result["status"] for result in results], ["PASS", "PASS"])
        self.assertFalse((self.repo / "common-product.json").exists())
        self.assertEqual(json.loads((logs / "results.json").read_text())["commit"], commit)
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)

    def test_selection_and_execution_use_exact_committed_snapshot(self) -> None:
        base = self.git("rev-parse", "HEAD")
        cert = self.certificate("snapshot.py", "print('committed snapshot')\n")
        commit = self.commit()
        (self.cert_dir / "snapshot.py").write_text("raise RuntimeError('working edit')\n")
        self.certificate("untracked.py", "raise RuntimeError('untracked')\n")
        self.assertEqual(runner.select_certificates(self.repo, commit, base), [cert])
        self.assertEqual(runner.select_certificates(self.repo, commit, None), [cert])
        logs = self.root / "snapshot-logs"
        logs.mkdir()
        result = runner.run_certificate(self.repo, commit, cert, logs)
        self.assertEqual(result["status"], "PASS")
        self.assertIn(b"committed snapshot", (Path(result["logs"]) / "stdout.log").read_bytes())

    def test_cli_failure_is_nonzero_and_logs_the_checked_commit(self) -> None:
        self.certificate("failed.py", "raise SystemExit(9)\n")
        commit = self.commit()
        logs = self.root / "cli-logs"
        result = subprocess.run([sys.executable, str(Path(runner.__file__).resolve()),
                                 "--repo", str(self.repo), "--ref", commit, "--all", "--log-dir", str(logs)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads((logs / "results.json").read_text())["commit"], commit)

    def test_deleted_certificates_are_excluded_and_renames_use_new_path(self) -> None:
        self.certificate("old.py", "print('old')\n")
        self.certificate("deleted.py", "print('deleted')\n")
        base = self.commit()
        self.git("mv", f"{runner.CERT_DIR}/old.py", f"{runner.CERT_DIR}/renamed.py")
        self.git("rm", f"{runner.CERT_DIR}/deleted.py")
        commit = self.commit()
        self.assertEqual(runner.select_certificates(self.repo, commit, base),
                         [f"{runner.CERT_DIR}/renamed.py"])

    def assert_process_stopped(self, pid: int) -> None:
        # An orphan can briefly remain a zombie until the OS reaps it.
        state = subprocess.run(["ps", "-p", str(pid), "-o", "stat="],
                               capture_output=True, text=True).stdout.strip()
        self.assertTrue(not state or state.startswith("Z"), f"process {pid} still running: {state}")

    def test_successful_certificate_cannot_leave_a_background_child(self) -> None:
        pid_file = self.root / "background-pid"
        body = (
            "import subprocess, sys\nfrom pathlib import Path\n"
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])\n"
            f"Path({str(pid_file)!r}).write_text(str(child.pid))\n"
        )
        result, _logs = self.run_one("background.py", body)
        self.assertEqual(result["status"], "PASS", result)
        self.assert_process_stopped(int(pid_file.read_text()))

    def test_cli_signals_stop_process_groups_and_do_not_execute_queued_certificates(self) -> None:
        for signum in (signal.SIGINT, signal.SIGTERM):
            with self.subTest(signum=signum):
                pid_file = self.root / f"pids-{signum}"
                queued_file = self.root / f"queued-{signum}"
                # The first certificate has a descendant and occupies the only
                # worker. The second must never start after cancellation.
                body = (
                    "import json, os, subprocess, sys, time\nfrom pathlib import Path\n"
                    "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])\n"
                    f"pid_file = Path({str(pid_file)!r})\n"
                    "temporary = pid_file.with_suffix('.tmp')\n"
                    "temporary.write_text(json.dumps([os.getpid(), child.pid]))\n"
                    "temporary.replace(pid_file)\n"
                    "print('running before cancel', flush=True)\ntime.sleep(30)\n"
                )
                self.certificate("a_running.py", body)
                self.certificate("z_queued.py", f"from pathlib import Path\nPath({str(queued_file)!r}).touch()\n")
                commit = self.commit()
                logs = self.root / f"cancel-logs-{signum}"
                process = subprocess.Popen(
                    [sys.executable, str(Path(runner.__file__).resolve()), "--repo", str(self.repo),
                     "--ref", commit, "--all", "--workers", "1", "--log-dir", str(logs)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True,
                )
                pids = []
                try:
                    deadline = time.monotonic() + 5
                    while not pid_file.exists() and process.poll() is None and time.monotonic() < deadline:
                        time.sleep(0.01)
                    self.assertTrue(pid_file.exists(), "certificate did not start")
                    pids = json.loads(pid_file.read_text())
                    process.send_signal(signum)
                    stdout, stderr = process.communicate(timeout=5)
                    self.assertEqual(process.returncode, 128 + signum, stdout + stderr)
                    self.assertFalse(queued_file.exists(), "queued certificate executed after cancellation")
                    for pid in pids:
                        self.assert_process_stopped(pid)
                    summary = json.loads((logs / "results.json").read_text())
                    self.assertEqual(summary["signal"], signum)
                    self.assertTrue(all(result["status"] == "CANCELLED" for result in summary["results"]), summary)
                    self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)
                    self.assertTrue(any(b"running before cancel" in log.read_bytes() for log in logs.rglob("stdout.log")))
                finally:
                    if process.poll() is None:
                        process.kill()
                        process.communicate()
                    for pid in pids:
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass


class TimeoutDeclarationTests(unittest.TestCase):
    def test_timeout_contract(self) -> None:
        self.assertEqual(runner.certificate_timeout("print('default')\n"), 180)
        for seconds in (180, 900, 1800):
            self.assertEqual(runner.certificate_timeout(f"# D0_CI_TIMEOUT_SECONDS={seconds}\n"), seconds)
        self.assertEqual(runner.certificate_timeout("\n" * 40 + "# D0_CI_TIMEOUT_SECONDS=900\n"), 180)
        self.assertEqual(runner.certificate_timeout("\n" * 39 + "# D0_CI_TIMEOUT_SECONDS=900\n"), 900)
        for source in ("# D0_CI_TIMEOUT_SECONDS=179\n", "# D0_CI_TIMEOUT_SECONDS=1801\n",
                       "# D0_CI_TIMEOUT_SECONDS=180\n# D0_CI_TIMEOUT_SECONDS=180\n"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                runner.certificate_timeout(source)


if __name__ == "__main__":
    unittest.main()
