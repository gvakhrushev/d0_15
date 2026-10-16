#!/usr/bin/env python3
"""Check the golden-gate/moving-preparation bridge receipt and Lean output."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECEIPT = ROOT / "02_REGISTRY/research/certificates/a4d_moving_preparation_golden_interferometer_receipt_2026-10-16.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["schema"] == "d0-moving-preparation-golden-interferometer-bridge/1"
    assert receipt["status"] == "PASS"

    source = receipt["source"]
    proof = ROOT / source["source_proof_path"]
    assert proof.is_file() and sha256(proof) == source["source_proof_sha256"]

    baseline = receipt["d0_owner_baseline"]
    for rel, expected in baseline["git_blobs"].items():
        path = ROOT / rel
        assert path.is_file(), ("MISSING_OWNER", rel)
        pinned = git_output("rev-parse", f"{baseline['commit']}:{rel}")
        actual = git_output("hash-object", str(path))
        assert pinned == actual == expected, ("OWNER_BLOB_MISMATCH", rel, pinned, actual)

    formalization = receipt["formalization"]
    lean_file = ROOT / formalization["path"]
    output_file = ROOT / formalization["output_path"]
    assert sha256(lean_file) == formalization["sha256"]
    assert sha256(output_file) == formalization["output_sha256"]
    output = output_file.read_text(encoding="utf-8")
    assert "error:" not in output
    assert "sorryAx" not in output
    for name in formalization["theorems"]:
        assert f"D0.Research.MovingPreparationGoldenBridge.{name}" in output, name
    axiom_sets = re.findall(r"depends on axioms: \[([^\]]*)\]", output, re.S)
    assert len(axiom_sets) == formalization["theorem_count"]
    used_axioms = {
        ax.strip()
        for group in axiom_sets
        for ax in group.replace("\n", " ").split(",")
    }
    used_axioms.discard("")
    assert used_axioms == set(formalization["axioms"]), used_axioms
    assert formalization["role_index"] == "D0.Role"
    assert formalization["role_cardinality"] == 4
    assert formalization["sorryAx"] is False

    report = receipt["bridge_report"]
    report_path = ROOT / report["path"]
    assert sha256(report_path) == report["sha256"]
    scope = receipt["scope"]
    assert scope["operator_formula_from_owned_golden_gate"]
    assert scope["failure_effect_on_role_indexed_matrix_returns"]
    assert not any(value for key, value in scope.items() if key not in {
        "operator_formula_from_owned_golden_gate",
        "failure_effect_on_role_indexed_matrix_returns",
    })
    print("PASS_GOLDEN_PREPARATION_BRIDGE owner_pins=6 theorems=8 role=D0.Role sorryAx=0")


if __name__ == "__main__":
    main()
