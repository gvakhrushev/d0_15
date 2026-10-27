#!/usr/bin/env python3
"""Fixture controls for the narrowly scoped historical pairing overlay."""
from __future__ import annotations

from contextlib import ExitStack
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import native_pairing_refinement_inputs as pairing
import run_research_certs as runner


class PairingOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="d0-pairing-overlay-tests-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Pairing fixture")
        self.sources = tuple(pairing.EXPECTED_SOURCES[:2])
        self.old = {self.sources[0]: b"historical A\n", self.sources[1]: b"historical B\n"}
        self.current = {self.sources[0]: b"maintained A\n", self.sources[1]: b"maintained B\n"}
        for path, data in self.old.items():
            self.write(path, data)
        self.source_commit = self.commit()
        for path, data in self.current.items():
            self.write(path, data)
        self.other = "02_REGISTRY/research/fixture-pairing-input.md"
        self.write(self.other, b"pinned non-Lean input\n")
        self.checker_body = self.checker()
        self.prepare_artifacts()
        self.commit()

    def git(self, *args: str) -> str:
        return runner.git(self.repo, *args).decode().strip()

    def commit(self) -> str:
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def write(self, relative: str, data: bytes) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def checker(self, mutation: bool = False) -> bytes:
        body = "from pathlib import Path\n"
        for path, data in self.old.items():
            body += f"assert Path({path!r}).read_bytes() == {data!r}\n"
        if mutation:
            body += f"Path({self.sources[0]!r}).write_text('checker mutation\\n')\n"
        return (body + "print('historical fixture executed')\n").encode()

    def prepare_artifacts(self) -> None:
        self.write(pairing.ENTRYPOINT, self.checker_body)
        self.write(pairing.BASE + ".py", b"# fixture program\n")
        self.write(pairing.BASE + ".lean", b"-- fixture capsule\n")
        self.write(pairing.BASE + "_lean_output.txt", b"fixture output\n")
        proof = "02_REGISTRY/research/A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md"
        self.write(proof, b"fixture proof\n")
        inputs = {path: pairing.sha256(data) for path, data in self.old.items()}
        inputs[self.other] = pairing.sha256(b"pinned non-Lean input\n")
        receipt = {"status": "PASS", "compiler_exit_code": 0,
                   "source_commit": self.source_commit,
                   "input_sha256": {path: inputs[path] for path in self.sources}}
        self.write(pairing.RECEIPT, (json.dumps(receipt, sort_keys=True) + "\n").encode())
        binding_fields = {
            "checker_sha256": pairing.ENTRYPOINT, "program_sha256": pairing.BASE + ".py",
            "proof_sha256": proof, "Lean_capsule_sha256": pairing.BASE + ".lean",
            "Lean_output_sha256": pairing.BASE + "_lean_output.txt",
            "Lean_receipt_sha256": pairing.RECEIPT,
        }
        ledger = {"schema": "d0-native-pairing-refinement-source/1",
                  "input_source_sha": self.source_commit, "input_sha256": inputs}
        ledger.update({field: pairing.sha256((self.repo / path).read_bytes())
                       for field, path in binding_fields.items()})
        self.write(pairing.LEDGER, (json.dumps(ledger, sort_keys=True) + "\n").encode())
        self.artifacts = {path: pairing.sha256((self.repo / path).read_bytes())
                          for path in [*binding_fields.values(), pairing.LEDGER]}
        entries = []
        for path, data in self.old.items():
            snapshot = pairing.DIRECTORY + "/lean/" + path
            self.write(snapshot, data)
            entries.append({"source_path": path, "snapshot_path": snapshot,
                            "sha256": pairing.sha256(data), "git_blob": pairing.git_blob(data)})
        manifest = {"schema": "d0-pairing-refinement-historical-input/1",
                    "scope": pairing.SCOPE, "source_commit": self.source_commit,
                    "entrypoint": pairing.ENTRYPOINT, "ledger_path": pairing.LEDGER,
                    "lean_receipt_path": pairing.RECEIPT, "artifact_sha256": self.artifacts,
                    "sources": entries}
        data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        self.write(pairing.MANIFEST, data)
        self.manifest_hash = pairing.sha256(data)

    def run_checker(self) -> tuple[dict, Path]:
        logs = Path(tempfile.mkdtemp(prefix="logs-", dir=self.root))
        with ExitStack() as stack:
            for key, value in {
                "SOURCE_COMMIT": self.source_commit, "EXPECTED_SOURCES": self.sources,
                "ARTIFACT_HASHES": self.artifacts, "MANIFEST_SHA256": self.manifest_hash,
                "LEDGER_INPUT_COUNT": 3, "RECEIPT_INPUT_COUNT": 2,
            }.items():
                stack.enter_context(patch.object(pairing, key, value))
            result = runner.run_certificate(self.repo, self.git("rev-parse", "HEAD"),
                                            pairing.ENTRYPOINT, logs)
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)
        self.assertEqual(self.git("status", "--porcelain"), "")
        return result, Path(result["logs"])

    def test_isolated_replay_uses_pinned_blobs_and_restores(self) -> None:
        result, logs = self.run_checker()
        self.assertEqual((result["status"], result["returncode"]), ("PASS", 0), result)
        self.assertFalse(result["tracked_mutation"])
        self.assertFalse(result["historical_input_mutation"])
        self.assertEqual((self.repo / self.sources[0]).read_bytes(), self.current[self.sources[0]])
        evidence = json.loads((logs / "historical-input.json").read_text())
        self.assertEqual(evidence["mode"], pairing.SCOPE)
        self.assertEqual(evidence["source_head"], self.source_commit)
        self.assertEqual(evidence["ledger_input_count"], 3)
        self.assertTrue(all(item["overlaid"] for item in evidence["sources"]))
        self.assertIn(b"historical fixture executed", (logs / "stdout.log").read_bytes())

    def test_live_checkout_is_never_overlaid(self) -> None:
        with self.assertRaisesRegex(ValueError, "isolated runner worktree"):
            pairing.apply(self.repo, pairing.ENTRYPOINT, isolation_parent=self.root)
        self.assertEqual((self.repo / self.sources[0]).read_bytes(), self.current[self.sources[0]])

    def test_saved_blobs_do_not_require_the_historical_commit_object(self) -> None:
        self.source_commit = "f" * 40
        self.prepare_artifacts()
        self.commit()
        result, _logs = self.run_checker()
        self.assertEqual((result["status"], result["returncode"]), ("PASS", 0), result)
        self.assertEqual(result["historical_input"]["source_head"], self.source_commit)

    def test_missing_manifest_on_bound_version_is_rejected(self) -> None:
        self.write("tools/native_pairing_refinement_inputs.py", b"# fixture binding\n")
        (self.repo / pairing.MANIFEST).unlink()
        self.commit()
        result, logs = self.run_checker()
        self.assertEqual(result["status"], "ERROR", result)
        self.assertIn("manifest is missing", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_altered_manifest_or_receipt_fails_before_execution(self) -> None:
        for path in (pairing.MANIFEST, pairing.RECEIPT, pairing.ENTRYPOINT):
            with self.subTest(path=path):
                original = (self.repo / path).read_bytes()
                (self.repo / path).write_bytes(original + b"\n")
                self.commit()
                result, logs = self.run_checker()
                self.assertEqual(result["status"], "ERROR", result)
                self.assertFalse((logs / "stdout.log").exists())
                (self.repo / path).write_bytes(original)
                self.commit()

    def test_snapshot_corruption_fails_before_execution(self) -> None:
        path = pairing.DIRECTORY + "/lean/" + self.sources[0]
        self.write(path, b"altered snapshot\n")
        self.commit()
        result, logs = self.run_checker()
        self.assertEqual(result["status"], "ERROR", result)
        self.assertIn("source blob mismatch", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_unbound_input_mismatch_fails_before_execution(self) -> None:
        self.write(self.other, b"changed non-Lean input\n")
        self.commit()
        result, logs = self.run_checker()
        self.assertEqual(result["status"], "ERROR", result)
        self.assertIn("unbound input mismatch", result["error"])
        self.assertFalse((logs / "stdout.log").exists())

    def test_checker_mutation_is_not_hidden_by_restore(self) -> None:
        self.checker_body = self.checker(mutation=True)
        self.prepare_artifacts()
        self.commit()
        result, logs = self.run_checker()
        self.assertEqual(result["status"], "MUTATION", result)
        self.assertTrue(result["historical_input_mutation"])
        self.assertIn(b"checker mutation", (logs / "tracked.patch").read_bytes())
        self.assertEqual((self.repo / self.sources[0]).read_bytes(), self.current[self.sources[0]])

    def test_unsafe_and_symlink_paths_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            pairing.safe_path(self.repo, "../outside")
        link = self.repo / "link"
        try:
            link.symlink_to(self.repo / self.sources[0])
        except OSError as error:
            self.skipTest(f"symlink unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "symlink"):
            pairing.safe_path(self.repo, "link")


if __name__ == "__main__":
    unittest.main()
