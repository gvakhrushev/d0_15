#!/usr/bin/env python3
"""Isolated controls for conservative research-certificate input closure."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import research_input_closure as closure
import run_research_certs as runner
import native_pairing_refinement_inputs as pairing_historical


PIN = "dfaf7c8df509d5abd83fa60a185ad530feadc9b5"
PINNED_SOURCES = (
    "02_REGISTRY/research/A4D_NATIVE_PREPARATION_FACTOR_SHEAR.md",
    "02_REGISTRY/research/A4D_COHERENT_COMPILATION_COST_DESCENT.md",
)


class ClosureFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="d0-input-closure-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Input closure fixture")
        self.cert_dir = self.repo / runner.CERT_DIR
        self.cert_dir.mkdir(parents=True)
        self.shared = self.repo / "shared"
        self.shared.mkdir()
        (self.repo / "requirements.txt").write_text("sympy>=1.12\n", encoding="utf-8")
        (self.shared / "owner.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.shared / "mid.py").write_text("import shared.owner\nVALUE = shared.owner.VALUE\n", encoding="utf-8")
        (self.repo / "historical-receipt.json").write_text("historical\n", encoding="utf-8")
        (self.repo / "notes.txt").write_text("unchanged\n", encoding="utf-8")
        self.base = self.commit()

    def git(self, *args: str) -> str:
        return runner.git(self.repo, *args).decode().strip()

    def commit(self) -> str:
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def write_cert(self, name: str, body: str) -> str:
        path = self.cert_dir / name
        path.write_text(body, encoding="utf-8")
        return f"{runner.CERT_DIR}/{name}"

    def receipt_bytes(self) -> bytes:
        return (self.repo / "historical-receipt.json").read_bytes()

    def assert_repo_untouched(self, receipt: bytes) -> None:
        self.assertEqual(self.receipt_bytes(), receipt)
        self.assertEqual((self.repo / "notes.txt").read_text(encoding="utf-8"), "unchanged\n")
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)


class SelectorTests(ClosureFixture):
    def test_context_binding_uses_snapshot_and_rejects_changed_caller(self) -> None:
        cert = self.write_cert("context.py", "INPUTS = ['shared/child.py']\n")
        owner = "shared/child.py"
        (self.repo / owner).write_text("VALUE = 1\n")
        source = "shared/value.md"
        (self.repo / source).write_text("expected\n")
        snap = self.repo / "packet/inputs/shared/value.md"
        snap.parent.mkdir(parents=True)
        snap.write_text("expected\n")
        commit = self.commit()
        hashes = {p: hashlib.sha256((self.repo / p).read_bytes()).hexdigest() for p in (cert, owner)}
        pin = hashlib.sha256(b"expected\n").hexdigest()
        item = {"path": source, "kind": "pin", "pin_sha256": pin, "pin_commit": None}
        with mock.patch.dict(closure.CONTEXT_SHA256, hashes), mock.patch.dict(closure.ROOT_BINDINGS, {(cert, owner): "packet/inputs"}):
            closure.require_context(self.repo, commit, cert, owner)
            row = closure.contextual_record(item, cert, owner, {})
            self.assertEqual(row["path"], "packet/inputs/shared/value.md")
            self.assertEqual(closure.provenance_status(self.repo, commit, row)["status"], "match")
            snap.write_text("wrong\n")
            changed = self.commit()
            self.assertEqual(closure.provenance_status(self.repo, changed, row)["status"], "sha-mismatch")
            snap.unlink()
            deleted = self.commit()
            self.assertEqual(closure.provenance_status(self.repo, deleted, row)["status"], "deleted-input")
            (self.repo / cert).write_text("INPUTS = ['shared/child.py']\n# changed root\n")
            changed_caller = self.commit()
            with self.assertRaisesRegex(ValueError, "context changed"):
                closure.require_context(self.repo, changed_caller, cert, owner)

    def test_overlay_requires_unique_safe_mapping_and_matching_checker_pin(self) -> None:
        packet = self.repo / "packet"
        packet.mkdir()
        digest = hashlib.sha256(b"historic").hexdigest()
        row = {"source_path": "old/source.lean", "snapshot": "inputs/source.lean", "sha256": digest}
        manifest = packet / "SOURCE_INPUTS.json"

        def read_overlay(rows):
            data = json.dumps({"files": rows}).encode()
            manifest.write_bytes(data)
            commit = self.commit()
            with mock.patch.object(closure, "JOINT", "packet/"), mock.patch.object(closure, "SOURCE_DIR", ""), mock.patch.object(closure, "JOINT_MANIFEST_SHA256", hashlib.sha256(data).hexdigest()):
                return closure.joint_overlay(self.repo, commit)

        mapping = read_overlay([row])
        pin = {"path": "old/source.lean", "kind": "pin", "pin_sha256": digest, "pin_commit": None}
        resolved = closure.contextual_record(pin, closure.JOINT_CERT, closure.JOINT_OWNER, mapping)
        self.assertEqual(resolved["path"], "packet/inputs/source.lean")
        with self.assertRaisesRegex(ValueError, "mismatched overlay pin"):
            closure.contextual_record(dict(pin, pin_sha256="0" * 64), closure.JOINT_CERT, closure.JOINT_OWNER, mapping)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            read_overlay([row, row])
        with self.assertRaisesRegex(ValueError, "invalid"):
            read_overlay([dict(row, snapshot="inputs/../escape")])

        # The replay verifies every copied file, including those the bridge
        # does not mention in its own PINS.
        untouched = dict(row, source_path="old/unused.lean", snapshot="inputs/unused.lean")
        mapping = read_overlay([row, untouched])
        snapshot = packet / "inputs/unused.lean"
        snapshot.parent.mkdir()
        snapshot.write_bytes(b"corrupt")
        head = self.commit()
        records = closure.overlay_snapshot_records(mapping)
        unused = next(item for item in records if item["source_path"] == "old/unused.lean")
        self.assertEqual(closure.provenance_status(self.repo, head, unused)["status"], "sha-mismatch")

    def test_blob_pin_does_not_guess_commit_and_detects_wrong_oid(self) -> None:
        data = b"VALUE = 1\n"
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        item = {"path": "shared/owner.py", "kind": "pin", "pin_commit": oid, "pin_sha256": None}
        resolved = closure.contextual_record(item, closure.SHEET, closure.SHEET, {})
        self.assertEqual(closure.provenance_status(self.repo, self.base, resolved)["status"], "match")
        self.assertEqual(closure.provenance_status(self.repo, self.base, dict(resolved, pin_blob="0" * 40))["status"], "sha-mismatch")
        self.assertEqual(closure.provenance_status(self.repo, self.base, item)["status"], "deleted-input")

    def test_joint_sums_end_to_end_pin_all_entries_and_reject_tampering(self) -> None:
        packet = self.repo / "packets/joint"
        (packet / "inputs").mkdir(parents=True)
        (packet / "inputs/source.md").write_text("snapshot\n")
        source_sha = hashlib.sha256(b"snapshot\n").hexdigest()
        overlay_data = json.dumps({"files": [{"source_path": "old/source.md", "snapshot": "inputs/source.md", "sha256": source_sha}]}).encode()
        (packet / "SOURCE_INPUTS.json").write_bytes(overlay_data)
        (packet / "bridge.py").write_text(f"PINS = {{'old/source.md': '{source_sha}'}}\n")
        (packet / "replay_packet.py").write_text("VALUE = 1\n")
        (packet / "check_conditional_noise.py").write_text("VALUE = 2\n")
        (packet / "WITNESS_RECEIPT.json").write_text('{}\n')
        (self.repo / "proof.md").write_text("proof\n")
        entries = {
            "../../proof.md": hashlib.sha256(b"proof\n").hexdigest(),
            "check_conditional_noise.py": hashlib.sha256(b"VALUE = 2\n").hexdigest(),
            "WITNESS_RECEIPT.json": hashlib.sha256(b"{}\n").hexdigest(),
        }
        sums_data = json.dumps({"schema": "d0.joint-field-minimum.pins.v1", "files": entries}).encode()
        (packet / "SHA256SUMS.json").write_bytes(sums_data)
        cert = self.write_cert("joint_fixture.py", "INPUTS = ['packets/joint/bridge.py', 'packets/joint/check_conditional_noise.py']\n")
        owner = "packets/joint/bridge.py"
        replay = "packets/joint/replay_packet.py"
        hashes = {p: hashlib.sha256((self.repo / p).read_bytes()).hexdigest() for p in (cert, owner, replay)}
        base = self.commit()
        with mock.patch.object(closure, "SOURCE_DIR", ""), mock.patch.object(closure, "JOINT", "packets/joint/"), mock.patch.object(closure, "JOINT_CERT", cert), mock.patch.object(closure, "JOINT_OWNER", owner), mock.patch.object(closure, "JOINT_MANIFEST_SHA256", hashlib.sha256(overlay_data).hexdigest()), mock.patch.object(closure, "JOINT_SUMS_SHA256", hashlib.sha256(sums_data).hexdigest()), mock.patch.dict(closure.CONTEXT_SHA256, hashes):
            report = closure.select(self.repo, base, None)
            rows = [r for r in report["provenance"] if r["certificate"] == cert and r["kind"] == "manifest-pin"]
            self.assertEqual({r["path"] for r in rows}, {"proof.md", "packets/joint/check_conditional_noise.py", "packets/joint/WITNESS_RECEIPT.json", "packets/joint/SHA256SUMS.json"})
            self.assertTrue(all(r["status"] == "match" for r in rows))
            (packet / "check_conditional_noise.py").write_text("VALUE = 3\n")
            changed = self.commit()
            report = closure.select(self.repo, changed, base)
            self.assertFalse(report["provenance_ok"])
            self.assertTrue(any(r["path"].endswith("check_conditional_noise.py") and r["status"] == "sha-mismatch" for r in report["provenance"]))
            (self.repo / "proof.md").unlink()
            deleted = self.commit()
            report = closure.select(self.repo, deleted, changed)
            self.assertTrue(any(r["path"] == "proof.md" and r["status"] == "deleted-input" for r in report["provenance"]))
            (packet / "SHA256SUMS.json").write_text('{}')
            altered_manifest = self.commit()
            with self.assertRaisesRegex(ValueError, "SHA256SUMS changed"):
                closure.select(self.repo, altered_manifest, deleted)
        self.assertEqual(closure.resolve_manifest_path("packets/joint", "../../proof.md"), "proof.md")
        with self.assertRaisesRegex(ValueError, "escapes"):
            closure.resolve_manifest_path("packets/joint", "../../../escape")
        with self.assertRaisesRegex(ValueError, "invalid"):
            closure.resolve_manifest_path("packets/joint", "/absolute")


    def test_opaque_hash_only_edge_does_not_hide_changed_or_executed_code(self) -> None:
        child = "shared/opaque.py"
        code = "PINNED_SHA256 = {'shared/missing.md': '" + "1" * 64 + "'}\n"
        (self.repo / child).write_text(code)
        digest = hashlib.sha256(code.encode()).hexdigest()
        cert = self.write_cert("opaque.py", f"PINNED_SHA256 = {{'{child}': '{digest}'}}\n")
        head = self.commit()
        hashes = {p: hashlib.sha256((self.repo / p).read_bytes()).hexdigest() for p in (cert, child)}
        with mock.patch.dict(closure.CONTEXT_SHA256, hashes), mock.patch.dict(closure.OPAQUE_EDGES, {cert: {child: {cert}}}):
            index = closure.build_index(self.repo, head)
            inputs = index["by_certificate"][cert]["transitive"]
            self.assertEqual([r["path"] for r in inputs], [child])
            self.assertEqual(closure.provenance_status(self.repo, head, inputs[0])["status"], "match")
            (self.repo / child).write_text(code + "# changed into executable code\n")
            changed = self.commit()
            with self.assertRaisesRegex(ValueError, "context changed"):
                closure.build_index(self.repo, changed)
            # A separate real import of the same file is still traversed,
            # irrespective of whether its pin is visited first.
            (self.repo / cert).write_text(f"PINNED_SHA256 = {{'{child}': '{digest}'}}\nimport shared.opaque\n")
            (self.repo / child).write_text(code)
            both = self.commit()
            hashes[cert] = hashlib.sha256((self.repo / cert).read_bytes()).hexdigest()
            with mock.patch.dict(closure.CONTEXT_SHA256, hashes):
                index = closure.build_index(self.repo, both)
                paths = {r["path"] for r in index["by_certificate"][cert]["transitive"]}
                self.assertIn("shared/missing.md", paths)
        # Without the audited opaque edge, recursive inspection is retained.
        index = closure.build_index(self.repo, head)
        paths = {r["path"] for r in index["by_certificate"][cert]["transitive"]}
        self.assertIn("shared/missing.md", paths)

    def test_constant_suffixes_track_real_files_not_the_prefix(self) -> None:
        consumer = self.write_cert(
            "suffix_consumer.py",
            "from pathlib import Path\nimport importlib.util\n"
            "ROOT = Path(__file__).resolve().parents[3]\n"
            "BASE = '02_REGISTRY/research/certificates/suffix_owner'\n"
            "importlib.util.spec_from_file_location('owner', ROOT / (BASE + '.py'))\n"
            "(ROOT / (BASE + '.lean')).read_text()\n",
        )
        self.write_cert("suffix_owner.py", "VALUE = 1\n")
        owner = self.cert_dir / "suffix_owner.lean"
        owner.write_text("-- old source\n", encoding="utf-8")
        base = self.commit()
        owner.write_text("-- changed source\n", encoding="utf-8")
        head = self.commit()
        report = closure.select(self.repo, head, base)
        item = next(item for item in report["selected"] if item["certificate"] == consumer)
        self.assertIn("changed-input", item["reasons"])
        paths = {row["path"] for row in item["inputs"]}
        self.assertIn(f"{runner.CERT_DIR}/suffix_owner.lean", paths)
        self.assertIn(f"{runner.CERT_DIR}/suffix_owner.py", paths)
        self.assertNotIn(f"{runner.CERT_DIR}/suffix_owner", paths)
        self.assertTrue(report["provenance_ok"])

    def test_pairing_manifest_change_selects_only_its_checker(self) -> None:
        checker = self.write_cert(Path(pairing_historical.ENTRYPOINT).name, "pass\n")
        unrelated = self.write_cert("other.py", "pass\n")
        base = self.commit()
        manifest = self.repo / pairing_historical.MANIFEST
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text("{}\n", encoding="utf-8")
        head = self.commit()
        report = closure.select(self.repo, head, base)
        selected = {item["certificate"]: item["reasons"] for item in report["selected"]}
        self.assertIn("historical-pairing-input-binding", selected[checker])
        self.assertNotIn(unrelated, selected)

    def test_imported_owner_change_selects_consumer_and_keeps_runner_narrow(self) -> None:
        consumer = self.write_cert(
            "consumer.py",
            "import importlib.util\n"
            "importlib.util.spec_from_file_location('owner', 'shared/owner.py')\n"
            "import shared.mid\n",
        )
        unrelated = self.write_cert("unrelated.py", "VALUE = 1\n")
        base = self.commit()
        owner = self.shared / "owner.py"
        owner.write_text("VALUE = 2\n", encoding="utf-8")
        head = self.commit()
        receipt = self.receipt_bytes()
        report = closure.select(self.repo, head, base)
        self.assertEqual(runner.select_certificates(self.repo, head, base), [])
        selected = {item["certificate"]: item["reasons"] for item in report["selected"]}
        self.assertIn(consumer, selected)
        self.assertIn("changed-input", selected[consumer])
        self.assertNotIn(unrelated, selected)
        self.assertNotIn("changed-entrypoint", selected[consumer])
        self.assertTrue(report["superset_of_runner"])
        self.assertTrue(report["provenance_ok"])
        self.assertFalse(report["scientific_replay"])
        owner_rows = [row for row in report["provenance"] if row["path"] == "shared/owner.py"]
        self.assertTrue(owner_rows)
        self.assertEqual(owner_rows[0]["actual_sha256"], hashlib.sha256(b"VALUE = 2\n").hexdigest())
        self.assert_repo_untouched(receipt)

    def test_changed_entrypoint_remains_a_superset_of_the_runner(self) -> None:
        cert = self.write_cert("direct.py", "print('one')\n")
        base = self.commit()
        self.write_cert("direct.py", "print('two')\n")
        head = self.commit()
        report = closure.select(self.repo, head, base)
        self.assertEqual(runner.select_certificates(self.repo, head, base), [cert])
        self.assertEqual([item["certificate"] for item in report["selected"]], [cert])
        self.assertIn("changed-entrypoint", report["selected"][0]["reasons"])
        self.assertEqual(closure.certificate_paths(self.repo, head, base), [cert])

    def test_mismatched_sha_fails_without_rewriting_the_pin(self) -> None:
        pinned = "shared/owner.py"
        body = (
            "PINNED_SHA256 = {\n"
            f"    {pinned!r}: {'0' * 64!r},\n"
            "}\n"
        )
        cert = self.write_cert("pinned.py", body)
        head = self.commit()
        original = (self.cert_dir / "pinned.py").read_bytes()
        report = closure.select(self.repo, head, self.base)
        self.assertIn(cert, closure.certificate_paths(self.repo, head, self.base))
        reasons = next(item["reasons"] for item in report["selected"] if item["certificate"] == cert)
        self.assertIn("sha-mismatch", reasons)
        self.assertFalse(report["provenance_ok"])
        self.assertFalse(report["scientific_replay"])
        row = next(item for item in report["provenance"] if item["certificate"] == cert and item["path"] == pinned)
        self.assertEqual(row["status"], "sha-mismatch")
        self.assertEqual(row["pin_sha256"], "0" * 64)
        self.assertNotEqual(row["actual_sha256"], row["pin_sha256"])
        self.assertEqual((self.cert_dir / "pinned.py").read_bytes(), original)

    def test_deleted_input_is_a_failure_and_still_selects_the_consumer(self) -> None:
        cert = self.write_cert(
            "needs_owner.py",
            "INPUTS = ['shared/owner.py']\nVALIDATION = ['shared/mid.py']\n",
        )
        base = self.commit()
        self.git("rm", "-q", "shared/owner.py")
        head = self.commit()
        report = closure.select(self.repo, head, base)
        self.assertEqual(runner.select_certificates(self.repo, head, base), [])
        reasons = next(item["reasons"] for item in report["selected"] if item["certificate"] == cert)
        self.assertIn("deleted-input", reasons)
        self.assertIn("changed-input", reasons)
        self.assertFalse(report["provenance_ok"])
        row = next(item for item in report["provenance"] if item["path"] == "shared/owner.py")
        self.assertEqual(row["status"], "deleted-input")
        self.assertIsNone(row["actual_sha256"])
        self.assertFalse((self.repo / "shared/owner.py").exists())

    def test_dynamic_import_is_unknown_and_is_not_skipped(self) -> None:
        dynamic = self.write_cert(
            "dynamic.py",
            "import sys\n__import__(sys.argv[1])\n",
        )
        resolved = self.write_cert("resolved.py", "import shared.owner\n")
        base = self.commit()
        (self.repo / "notes.txt").write_text("edited\n", encoding="utf-8")
        head = self.commit()
        (self.repo / "notes.txt").write_text("unchanged\n", encoding="utf-8")
        report = closure.select(self.repo, head, base)
        selected = {item["certificate"]: item for item in report["selected"]}
        self.assertIn(dynamic, selected)
        self.assertIn("unknown-dependency", selected[dynamic]["reasons"])
        self.assertTrue(any(item["reason"] == "dynamic-import" for item in selected[dynamic]["unknown"]))
        self.assertNotIn(resolved, selected)
        self.assertIn(resolved, report["unselected"])

    def test_transitive_owner_change_selects_the_certificate(self) -> None:
        cert = self.write_cert("chain.py", "import shared.mid\n")
        base = self.commit()
        (self.shared / "owner.py").write_text("VALUE = 3\n", encoding="utf-8")
        head = self.commit()
        selected = closure.certificate_paths(self.repo, head, base)
        self.assertEqual(selected, [cert])
        report = closure.select(self.repo, head, base)
        paths = {item["path"] for item in report["selected"][0]["inputs"]}
        self.assertIn("shared/owner.py", paths)
        self.assertIn("shared/mid.py", paths)

    def test_commit_pin_mismatch_fails_closed(self) -> None:
        owner = self.shared / "owner.py"
        old = self.base
        owner.write_text("VALUE = 9\n", encoding="utf-8")
        self.commit()
        # The certificate on head pins the previous blob, which no longer matches.
        self.write_cert(
            "commit_pin.py",
            "PINNED_COMMITS = {\n"
            f"    'shared/owner.py': {old!r},\n"
            "}\n",
        )
        head = self.commit()
        report = closure.select(self.repo, head, old)
        row = next(item for item in report["provenance"] if item["path"] == "shared/owner.py" and item["pin_commit"])
        self.assertEqual(row["status"], "sha-mismatch")
        self.assertFalse(report["provenance_ok"])

    def test_full_snapshot_selects_every_certificate_the_runner_lists(self) -> None:
        first = self.write_cert("a.py", "import shared.owner\n")
        second = self.write_cert("b.py", "VALUE = 1\n")
        head = self.commit()
        report = closure.select(self.repo, head, None)
        self.assertEqual(
            [item["certificate"] for item in report["selected"]],
            runner.select_certificates(self.repo, head, None),
        )
        self.assertEqual(set(closure.certificate_paths(self.repo, head, None)), {first, second})
        self.assertTrue(all("full-snapshot" in item["reasons"] for item in report["selected"]))
        self.assertFalse(report["scientific_replay"])


class ExecutionTests(ClosureFixture):
    def test_tracked_write_is_mutation_and_historical_receipt_stays_immutable(self) -> None:
        cert = self.write_cert(
            "writer.py",
            "from pathlib import Path\nPath('notes.txt').write_text('mutated\\n')\n",
        )
        head = self.commit()
        receipt = self.receipt_bytes()
        logs = self.root / "execution"
        report = closure.close_inputs(
            self.repo, head, self.base, logs, preserve=[self.repo / "historical-receipt.json"])
        self.assertEqual([item["certificate"] for item in report["selection"]["selected"]], [cert])
        self.assertEqual(report["execution"][0]["status"], "MUTATION")
        self.assertNotEqual(report["selection"]["scientific_replay"], True)
        self.assertFalse(report["scientific_replay"])
        self.assertTrue((logs / "execution.json").is_file())
        self.assert_repo_untouched(receipt)
        with self.assertRaises(FileExistsError):
            closure.execute_isolated(self.repo, head, [cert], logs)
        with self.assertRaises(FileExistsError):
            closure.write_exclusive(self.repo / "historical-receipt.json", "rewritten\n")
        self.assertEqual(self.receipt_bytes(), receipt)

    def test_workflow_success_with_skipped_scientific_step_is_not_replay(self) -> None:
        passed = [{"certificate": f"{runner.CERT_DIR}/ok.py", "status": "PASS"}]
        skipped = {
            "conclusion": "success",
            "steps": [
                {"name": closure.SCIENTIFIC_STEP, "status": "completed", "conclusion": "skipped"},
            ],
        }
        self.assertEqual(
            closure.workflow_replay(skipped)["reason"],
            "workflow SUCCESS skipped scientific step",
        )
        self.assertFalse(closure.workflow_replay(skipped)["replay"])
        self.assertFalse(closure.scientific_replay(passed, skipped, ran=True))
        absent = {"conclusion": "success", "steps": [{"name": "Validate canonical architecture", "conclusion": "success"}]}
        self.assertFalse(closure.workflow_replay(absent)["replay"])
        self.assertIn("skipped scientific step", closure.workflow_replay(absent)["reason"])
        succeeded = {
            "conclusion": "success",
            "steps": [
                {"name": closure.SCIENTIFIC_STEP, "status": "completed", "conclusion": "success"},
            ],
        }
        self.assertTrue(closure.scientific_replay(passed, succeeded, ran=True))
        self.assertFalse(closure.scientific_replay(passed, ran=False))
        mutated = [{"certificate": f"{runner.CERT_DIR}/writer.py", "status": "MUTATION"}]
        self.assertFalse(closure.scientific_replay(mutated, succeeded, ran=True))

    def test_cli_mismatch_is_nonzero_and_refuses_an_existing_report(self) -> None:
        self.write_cert(
            "pinned.py",
            "PINNED_SHA256 = {'shared/owner.py': '" + ("ab" * 32) + "'}\n",
        )
        head = self.commit()
        report_path = self.root / "report.json"
        result = subprocess.run(
            [sys.executable, str(Path(closure.__file__).resolve()),
             "--repo", str(self.repo), "--ref", head, "--base", self.base, "--report", str(report_path)],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("provenance_ok=false", result.stdout)
        self.assertIn("scientific_replay=false", result.stdout)
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertFalse(payload["selection"]["provenance_ok"])
        self.assertIsNone(payload["execution"])
        again = subprocess.run(
            [sys.executable, str(Path(closure.__file__).resolve()),
             "--repo", str(self.repo), "--ref", head, "--base", self.base, "--report", str(report_path)],
            capture_output=True, text=True)
        self.assertEqual(again.returncode, 1)
        self.assertIn("refusing to rewrite", again.stderr)
        self.assertFalse(payload["selection"]["provenance_ok"])


class RunnerHookTests(ClosureFixture):
    def test_cli_executes_dependents_and_keeps_unresolved_entries(self) -> None:
        depth = runner.CERT_DIR.count("/") + 1
        preamble = (
            "import sys\n"
            "from pathlib import Path\n"
            f"sys.path.insert(0, str(Path(__file__).resolve().parents[{depth}]))\n"
        )
        dep_a = self.write_cert("dep_a.py", preamble + "import shared.owner\nprint('dep-a', shared.owner.VALUE)\n")
        dep_b = self.write_cert("dep_b.py", preamble + "import shared.mid\nprint('dep-b', shared.mid.VALUE)\n")
        independent = self.write_cert("independent.py", "print('independent')\n")
        dynamic = self.write_cert(
            "dynamic.py",
            "import sys\n"
            "mod = sys.argv[1] if len(sys.argv) > 1 else 'json'\n"
            "__import__(mod)\n"
            "print('dynamic-ok')\n",
        )
        parse_error = self.write_cert("parse_error.py", "def broken(\n")
        owner_digest = hashlib.sha256((self.shared / "owner.py").read_bytes()).hexdigest()
        sha_pin = self.write_cert(
            "sha_pin.py",
            "PINNED_SHA256 = {\n"
            f"    'shared/owner.py': '{owner_digest}',\n"
            "}\n"
            "print('sha-pin')\n",
        )
        (self.shared / "will_move.py").write_text("PIN = 1\n", encoding="utf-8")
        renamed = self.write_cert(
            "renamed_pin.py",
            "INPUTS = ['shared/will_move.py']\nprint('renamed-pin')\n",
        )
        mutator = self.write_cert(
            "mutator.py",
            preamble + "import shared.owner\nPath('notes.txt').write_text('mutated\\n')\nprint('mutator', shared.owner.VALUE)\n",
        )
        base = self.commit()
        receipt = self.receipt_bytes()
        sha_bytes = (self.cert_dir / "sha_pin.py").read_bytes()
        (self.shared / "owner.py").write_text("VALUE = 2\n", encoding="utf-8")
        self.git("mv", "shared/will_move.py", "shared/moved.py")
        head = self.commit()
        self.assertEqual(runner.select_certificates(self.repo, head, base), [])
        logs = self.root / "runner-logs"
        started = time.perf_counter()
        result = subprocess.run(
            [sys.executable, str(Path(runner.__file__).resolve()),
             "--repo", str(self.repo), "--ref", head, "--base", base,
             "--workers", "1", "--log-dir", str(logs)],
            capture_output=True, text=True)
        elapsed = time.perf_counter() - started
        self.assertTrue((logs / "results.json").is_file(), result.stdout + result.stderr)
        payload = json.loads((logs / "results.json").read_text(encoding="utf-8"))
        by_cert = {item["certificate"]: item for item in payload["results"]}
        report = closure.select(self.repo, head, base)
        selected = [item["certificate"] for item in report["selected"]]
        reasons = {item["certificate"]: item["reasons"] for item in report["selected"]}
        self.assertEqual(sorted(by_cert), selected)
        self.assertEqual(closure.certificate_paths(self.repo, head, base), selected)
        self.assertEqual(selected, sorted([dep_a, dep_b, dynamic, parse_error, sha_pin, renamed, mutator]))
        self.assertNotIn(independent, selected)
        self.assertIn(independent, report["unselected"])
        self.assertEqual(reasons[dep_a], ["changed-input"])
        self.assertEqual(reasons[dep_b], ["changed-input"])
        self.assertEqual(reasons[dynamic], ["unknown-dependency"])
        dynamic_unknown = next(item["unknown"] for item in report["selected"] if item["certificate"] == dynamic)
        self.assertTrue(any(item["reason"] == "dynamic-import" for item in dynamic_unknown))
        self.assertEqual(reasons[parse_error], ["unknown-dependency"])
        self.assertTrue(any(item["reason"] == "unparsed" for item in next(
            row["unknown"] for row in report["selected"] if row["certificate"] == parse_error)))
        self.assertEqual(reasons[sha_pin], ["changed-input", "sha-mismatch"])
        self.assertEqual(reasons[renamed], ["changed-input", "deleted-input"])
        self.assertEqual(reasons[mutator], ["changed-input"])
        self.assertFalse(report["provenance_ok"])
        self.assertTrue(report["superset_of_runner"])
        self.assertFalse(report["scientific_replay"])
        self.assertEqual(by_cert[dep_a]["status"], "PASS")
        self.assertEqual(by_cert[dep_b]["status"], "PASS")
        self.assertEqual(by_cert[dynamic]["status"], "PASS")
        self.assertEqual(by_cert[parse_error]["status"], "FAIL")
        self.assertEqual(by_cert[sha_pin]["status"], "PASS")
        self.assertEqual(by_cert[renamed]["status"], "PASS")
        self.assertEqual(by_cert[mutator]["status"], "MUTATION")
        self.assertIn(b"dep-a 2", (Path(by_cert[dep_a]["logs"]) / "stdout.log").read_bytes())
        self.assertIn(b"dep-b 2", (Path(by_cert[dep_b]["logs"]) / "stdout.log").read_bytes())
        self.assertIn(b"mutated", (Path(by_cert[mutator]["logs"]) / "tracked.patch").read_bytes())
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"{len(selected)} certificate(s)", result.stdout)
        self.assertEqual((self.cert_dir / "sha_pin.py").read_bytes(), sha_bytes)
        skipped = {
            "conclusion": "success",
            "steps": [{"name": closure.SCIENTIFIC_STEP, "status": "completed", "conclusion": "skipped"}],
        }
        failed_step = {
            "conclusion": "success",
            "steps": [{"name": closure.SCIENTIFIC_STEP, "status": "completed", "conclusion": "failure"}],
        }
        self.assertEqual(closure.workflow_replay(skipped)["reason"], "workflow SUCCESS skipped scientific step")
        self.assertEqual(closure.workflow_replay(failed_step)["reason"], "workflow SUCCESS skipped scientific step")
        self.assertFalse(closure.workflow_replay(skipped)["replay"])
        self.assertFalse(closure.workflow_replay(failed_step)["replay"])
        self.assertFalse(closure.scientific_replay(payload["results"], skipped, ran=True))
        self.assertFalse(closure.scientific_replay(payload["results"], failed_step, ran=True))
        self.assert_repo_untouched(receipt)
        print(
            f"FIXTURE selected={len(selected)} seconds={elapsed:.3f} returncode={result.returncode}",
            file=sys.stderr,
        )


class LiveBoundaryTests(unittest.TestCase):
    def test_runner_and_workflow_call_this_selector(self) -> None:
        root = Path(__file__).resolve().parents[1]
        runner_source = (root / "tools/run_research_certs.py").read_text(encoding="utf-8")
        workflow = (root / ".github/workflows/guards.yml").read_text(encoding="utf-8")
        hook = 'certs = __import__("research_input_closure").certificate_paths(args.repo, commit, base)'
        self.assertIn(hook, runner_source)
        self.assertIn("python tools/test_research_input_closure.py\n", workflow)
        self.assertIn(closure.SCIENTIFIC_STEP, workflow)
        self.assertIn('python tools/run_research_certs.py --ref "$CHECKED_REF" --base "$BASE" --workers 2', workflow)
        before = runner.git(root, "status", "--porcelain=v1", "--untracked-files=no")
        head = runner.git(root, "rev-parse", "HEAD").decode().strip()
        selected = closure.certificate_paths(root, head, head)
        after = runner.git(root, "status", "--porcelain=v1", "--untracked-files=no")
        self.assertEqual(before, after)
        self.assertEqual(runner.select_certificates(root, head, head), [])
        closure_packet = f"{runner.CERT_DIR}/a4d_closure_packet_integration_check.py"
        cartan = f"{runner.CERT_DIR}/a4d_cartan_nonlinear_rigidity_check.py"
        self.assertIn(closure_packet, closure.tree_paths(root, head))
        self.assertIn(cartan, closure.tree_paths(root, head))
        self.assertIn(closure_packet, selected)
        self.assertNotIn(cartan, selected)

    def test_pinned_source_is_readable_and_not_merged(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for rel in PINNED_SOURCES:
            blob = runner.git(root, "show", f"{PIN}:{rel}")
            self.assertTrue(blob.startswith(b"#"), rel)
            self.assertFalse((root / rel).exists(), rel)
        self.assertIn(b"not a native-action or GR theorem", runner.git(root, "show", f"{PIN}:{PINNED_SOURCES[0]}"))

    def test_live_index_is_read_only_and_does_not_weaken_full_selection(self) -> None:
        root = Path(__file__).resolve().parents[1]
        before = runner.git(root, "status", "--porcelain=v1", "--untracked-files=no")
        head = runner.git(root, "rev-parse", "HEAD").decode().strip()
        report = closure.select(root, head, None)
        after = runner.git(root, "status", "--porcelain=v1", "--untracked-files=no")
        self.assertEqual(before, after)
        self.assertEqual(
            [item["certificate"] for item in report["selected"]],
            runner.select_certificates(root, head, None),
        )
        self.assertTrue(report["superset_of_runner"])
        self.assertFalse(report["scientific_replay"])


if __name__ == "__main__":
    unittest.main()
