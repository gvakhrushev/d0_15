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
import native_checkpoint_inputs as historical


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

    def historical_fixture(self, body: str) -> tuple[str, dict]:
        real = Path(__file__).resolve().parents[1]
        manifest = json.loads((real / historical.MANIFEST).read_text())
        paths = ({historical.MANIFEST, historical.SNAPSHOT, historical.TARGET,
                  historical.REPORT_SNAPSHOT, historical.REPORT_TARGET}
                 | set(manifest["entrypoints"]) | set(manifest["receipts"])
                 | set(manifest["compatibility_capsules"]) | historical.REPORT_RECEIPTS
                 | historical.REPORT_ENTRYPOINTS)
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((real / name).read_bytes())
        name = "a4d_native_history_action_check.py"
        entry = historical.CERT + name
        (self.repo / entry).write_text(body)
        manifest["entrypoints"][entry]["sha256"] = historical.sha(body.encode())
        manifest["report_input"]["entrypoint_sha256"][entry] = historical.sha(body.encode())
        (self.repo / historical.MANIFEST).write_text(json.dumps(manifest))
        return name, manifest

    def historical_body(self) -> str:
        return ("from pathlib import Path\nimport hashlib\n"
                f"assert hashlib.sha256(Path({historical.TARGET!r}).read_bytes()).hexdigest() == {historical.SOURCE_SHA256!r}\n"
                f"assert hashlib.sha256(Path({historical.REPORT_TARGET!r}).read_bytes()).hexdigest() == {historical.REPORT_SHA256!r}\n"
                "print('executed declared historical input')\n")

    def test_scoped_historical_input_is_logged_and_never_changes_main(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        maintained = (self.repo / historical.TARGET).read_bytes()
        report_maintained = (self.repo / historical.REPORT_TARGET).read_bytes()
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "PASS", result)
        self.assertFalse(result["tracked_mutation"])
        self.assertFalse(result["historical_input_mutation"])
        self.assertEqual((self.repo / historical.TARGET).read_bytes(), maintained)
        self.assertEqual((self.repo / historical.REPORT_TARGET).read_bytes(), report_maintained)
        evidence = json.loads((logs / "historical-input.json").read_text())
        self.assertEqual(evidence["historical_sha256"], historical.SOURCE_SHA256)
        self.assertEqual(evidence["maintained_sha256"], historical.sha(maintained))
        self.assertIn("NOT_CURRENT_SOURCE_PROOF", evidence["mode"])
        self.assertEqual(evidence["report_input"]["historical_sha256"], historical.REPORT_SHA256)
        self.assertEqual(evidence["report_input"]["maintained_sha256"], historical.sha(report_maintained))
        self.assertEqual(evidence["report_input"]["mode"], "HISTORICAL_REPORT_INPUT_NOT_CURRENT_ROUTE")

    def test_historical_snapshot_corruption_fails_before_execution(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        (self.repo / historical.SNAPSHOT).write_text("wrong source\n")
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("snapshot hash mismatch", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_historical_undeclared_target_is_rejected(self) -> None:
        body = self.historical_body()
        name, manifest = self.historical_fixture(body)
        manifest["target_path"] = "tracked.txt"
        (self.repo / historical.MANIFEST).write_text(json.dumps(manifest))
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("scope, source or path", result["error"])

    def test_historical_entrypoint_mismatch_is_rejected(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        result, _ = self.run_one(name, body + "# altered entrypoint\n")
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("entrypoint binding mismatch", result["error"])

    def test_historical_receipt_mismatch_is_rejected(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        receipt = sorted(historical.RECEIPTS)[0]
        (self.repo / receipt).write_text("{}\n")
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("artifact binding mismatch", result["error"])

    def test_historical_overlay_mutation_is_not_hidden_by_restoration(self) -> None:
        body = self.historical_body() + f"Path({historical.TARGET!r}).write_text('mutated source\\n')\n"
        name, _ = self.historical_fixture(body)
        maintained = (self.repo / historical.TARGET).read_bytes()
        report_maintained = (self.repo / historical.REPORT_TARGET).read_bytes()
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "MUTATION")
        self.assertTrue(result["historical_input_mutation"])
        self.assertIn(b"mutated source", (logs / "tracked.patch").read_bytes())
        self.assertNotIn(historical.REPORT_TARGET.encode(), (logs / "tracked.patch").read_bytes())
        self.assertEqual((self.repo / historical.TARGET).read_bytes(), maintained)
        self.assertEqual((self.repo / historical.REPORT_TARGET).read_bytes(), report_maintained)

    def test_historical_report_snapshot_corruption_fails_before_execution(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        (self.repo / historical.REPORT_SNAPSHOT).write_text("wrong report\n")
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("report snapshot hash mismatch", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_historical_report_extra_entrypoint_is_rejected(self) -> None:
        body = self.historical_body()
        name, manifest = self.historical_fixture(body)
        manifest["report_input"]["entrypoints"][historical.CERT + "undeclared_check.py"] = sorted(historical.REPORT_RECEIPTS)[0]
        (self.repo / historical.MANIFEST).write_text(json.dumps(manifest))
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("report scope, source, path or entrypoint set", result["error"])

    def test_historical_report_undeclared_target_is_rejected(self) -> None:
        body = self.historical_body()
        name, manifest = self.historical_fixture(body)
        manifest["report_input"]["target_path"] = "tracked.txt"
        (self.repo / historical.MANIFEST).write_text(json.dumps(manifest))
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("report scope, source, path or entrypoint set", result["error"])

    def test_historical_report_receipt_mismatch_is_rejected(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        (self.repo / sorted(historical.REPORT_RECEIPTS)[0]).write_text("{}\n")
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("report receipt binding mismatch", result["error"])

    def test_historical_report_overlay_mutation_is_not_hidden_by_restoration(self) -> None:
        body = self.historical_body() + f"Path({historical.REPORT_TARGET!r}).write_text('mutated report\\n')\n"
        name, _ = self.historical_fixture(body)
        maintained = (self.repo / historical.TARGET).read_bytes()
        report_maintained = (self.repo / historical.REPORT_TARGET).read_bytes()
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "MUTATION")
        self.assertTrue(result["historical_input_mutation"])
        self.assertIn(b"mutated report", (logs / "tracked.patch").read_bytes())
        self.assertNotIn(historical.TARGET.encode(), (logs / "tracked.patch").read_bytes())
        self.assertEqual((self.repo / historical.TARGET).read_bytes(), maintained)
        self.assertEqual((self.repo / historical.REPORT_TARGET).read_bytes(), report_maintained)

    def test_source_only_entry_does_not_receive_historical_report(self) -> None:
        self.historical_fixture(self.historical_body())
        name = "a4d_native_history_field_coupling_check.py"
        entry = historical.CERT + name
        current = historical.sha((self.repo / historical.REPORT_TARGET).read_bytes())
        body = ("from pathlib import Path\nimport hashlib\n"
                f"assert hashlib.sha256(Path({historical.TARGET!r}).read_bytes()).hexdigest() == {historical.SOURCE_SHA256!r}\n"
                f"assert hashlib.sha256(Path({historical.REPORT_TARGET!r}).read_bytes()).hexdigest() == {current!r}\n")
        manifest = json.loads((self.repo / historical.MANIFEST).read_text())
        manifest["entrypoints"][entry]["sha256"] = historical.sha(body.encode())
        (self.repo / historical.MANIFEST).write_text(json.dumps(manifest))
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "PASS", result)
        self.assertNotIn("report_input", result["historical_input"])

    def historical_report_only_fixture(self, tail: str = "") -> tuple[str, str]:
        real = Path(__file__).resolve().parents[1]
        manifest = json.loads((real / historical.MANIFEST).read_text())
        paths = ({historical.MANIFEST, historical.REPORT_SNAPSHOT, historical.REPORT_TARGET}
                 | historical.REPORT_RECEIPTS | historical.REPORT_ENTRYPOINTS)
        for name in paths:
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((real / name).read_bytes())
        # No historical Quantum snapshot, capsules or action declarations exist.
        maintained = self.repo / historical.TARGET
        maintained.parent.mkdir(parents=True, exist_ok=True)
        maintained.write_text("unrelated maintained Quantum fixture\n")
        name = "a4d_native_time_field_intertwiner_check.py"
        entry = historical.CERT + name
        body = ("from pathlib import Path\nimport hashlib\n"
                f"assert hashlib.sha256(Path({historical.REPORT_TARGET!r}).read_bytes()).hexdigest() == {historical.REPORT_SHA256!r}\n"
                f"assert Path({historical.TARGET!r}).read_text() == 'unrelated maintained Quantum fixture\\n'\n"
                "print('executed report-only input')\n" + tail)
        (self.repo / entry).write_text(body)
        manifest["report_input"]["entrypoint_sha256"][entry] = historical.sha(body.encode())
        (self.repo / historical.MANIFEST).write_text(json.dumps(manifest))
        return name, body

    def test_report_only_entry_never_reads_or_overlays_quantum_inputs(self) -> None:
        name, body = self.historical_report_only_fixture()
        maintained = (self.repo / historical.REPORT_TARGET).read_bytes()
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "PASS", result)
        self.assertFalse(result["tracked_mutation"])
        self.assertFalse(result["historical_input_mutation"])
        self.assertFalse((self.repo / historical.SNAPSHOT).exists())
        self.assertEqual((self.repo / historical.REPORT_TARGET).read_bytes(), maintained)
        evidence = json.loads((logs / "historical-input.json").read_text())
        self.assertEqual(evidence["mode"], "HISTORICAL_REPORT_INPUT_NOT_CURRENT_ROUTE")
        self.assertEqual(evidence["target_path"], historical.REPORT_TARGET)
        self.assertEqual(evidence["historical_sha256"], historical.REPORT_SHA256)
        self.assertNotIn("current_source_compilation", evidence)
        self.assertNotIn("report_input", evidence)

    def test_report_only_mutation_is_not_hidden_by_restoration(self) -> None:
        name, body = self.historical_report_only_fixture(
            f"Path({historical.REPORT_TARGET!r}).write_text('mutated report-only input\\n')\n")
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "MUTATION", result)
        self.assertTrue(result["historical_input_mutation"])
        self.assertIn(b"mutated report-only input", (logs / "tracked.patch").read_bytes())
        self.assertNotIn(historical.TARGET.encode(), (logs / "tracked.patch").read_bytes())

    def test_report_only_entrypoint_change_fails_before_execution(self) -> None:
        name, body = self.historical_report_only_fixture()
        result, logs = self.run_one(name, body + "# unbound change\n")
        self.assertEqual(result["status"], "ERROR", result)
        self.assertIn("report entrypoint binding mismatch", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_report_only_ledger_change_fails_before_execution(self) -> None:
        name, body = self.historical_report_only_fixture()
        receipt = historical.REPORT_BINDINGS[historical.CERT + name]
        (self.repo / receipt).write_text("{}\n")
        result, logs = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR", result)
        self.assertIn("report receipt binding mismatch", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_report_only_execution_failure_is_preserved(self) -> None:
        name, body = self.historical_report_only_fixture("raise SystemExit(7)\n")
        result, _ = self.run_one(name, body)
        self.assertEqual((result["status"], result["returncode"]), ("FAIL", 7), result)
        self.assertFalse(result["tracked_mutation"])

    def test_undeclared_consumer_uses_maintained_source(self) -> None:
        self.historical_fixture(self.historical_body())
        current = historical.sha((self.repo / historical.TARGET).read_bytes())
        body = ("from pathlib import Path\nimport hashlib\n"
                f"assert hashlib.sha256(Path({historical.TARGET!r}).read_bytes()).hexdigest() == {current!r}\n")
        result, _ = self.run_one("undeclared_consumer.py", body)
        self.assertEqual(result["status"], "PASS")
        self.assertNotIn("historical_input", result)

    def test_changed_action_floor_cannot_pass_as_current_compatibility(self) -> None:
        body = self.historical_body()
        name, _ = self.historical_fixture(body)
        target = self.repo / historical.TARGET
        target.write_text(target.read_text().replace("def S_min : ℝ := 1", "def S_min : ℝ := 2"))
        result, _ = self.run_one(name, body)
        self.assertEqual(result["status"], "ERROR")
        self.assertIn("action interface changed", result["error"])

    def test_historical_binding_change_adds_consumers_to_normal_selection(self) -> None:
        import research_input_closure as closure
        self.historical_fixture(self.historical_body())
        base = self.commit()
        snapshot = self.repo / historical.SNAPSHOT
        snapshot.write_bytes(snapshot.read_bytes() + b"\n")
        head = self.commit()
        report = closure.select(self.repo, head, base)
        selected = {row["certificate"]: row for row in report["selected"]}
        for entry in historical.ENTRYPOINTS:
            self.assertIn(entry, selected)
            self.assertIn("historical-input-binding", selected[entry]["reasons"])

    def test_report_binding_selection_reason_is_scoped_to_its_three_consumers(self) -> None:
        import research_input_closure as closure
        self.historical_fixture(self.historical_body())
        base = self.commit()
        snapshot = self.repo / historical.REPORT_SNAPSHOT
        snapshot.write_bytes(snapshot.read_bytes() + b"\n")
        report = closure.select(self.repo, self.commit(), base)
        bound = {row["certificate"] for row in report["selected"]
                 if "historical-report-input-binding" in row["reasons"]}
        self.assertEqual(bound, historical.REPORT_ENTRYPOINTS)

    def test_report_only_consumer_is_selected_when_binding_manifest_changes(self) -> None:
        import research_input_closure as closure
        name, _ = self.historical_report_only_fixture()
        base = self.commit()
        manifest = self.repo / historical.MANIFEST
        manifest.write_bytes(manifest.read_bytes() + b"\n")
        report = closure.select(self.repo, self.commit(), base)
        selected = {row["certificate"]: row for row in report["selected"]}
        entry = historical.CERT + name
        self.assertIn("historical-report-input-binding", selected[entry]["reasons"])
        self.assertNotIn("historical-input-binding", selected[entry]["reasons"])
        self.assertNotIn(entry, historical.ENTRYPOINTS)
        self.assertEqual(len(historical.ENTRYPOINTS), 11)

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
