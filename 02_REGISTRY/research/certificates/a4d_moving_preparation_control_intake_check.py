#!/usr/bin/env python3
"""Verify the byte-preserved moving-preparation intake and its replay receipt."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14"
RECEIPT = ROOT / "02_REGISTRY/research/certificates/a4d_moving_preparation_control_intake_2026-10-16.json"
REPLAY = ROOT / "02_REGISTRY/research/certificates/a4d_local_record_to_matter_intake_replay_2026-10-16.json"
EXPECTED_SOURCE_HEAD = "ef782fe3d64cd973ff2d328a01bdacb934c7c8ec"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)], cwd=ROOT, text=True
    ).strip()


def main() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["schema"] == "d0-moving-preparation-control-intake/1"
    assert receipt["status"] == "PASS"
    source = receipt["source"]
    assert source["pull_request"] == 310
    assert source["head"] == EXPECTED_SOURCE_HEAD
    assert source["path"] == BASE
    assert receipt["control"]["pull_request"] == 322

    manifest_path = ROOT / BASE / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["file_count"] == 102
    assert sha256(manifest_path) == receipt["manifest_sha256"]
    assert receipt["user_inputs"]["manifest_file_count"] == len(manifest["files"])
    assert receipt["user_inputs"]["tree_file_count_including_manifest"] == 103

    manifest_rows = {f"{BASE}/{row['path']}": row for row in manifest["files"]}
    assert len(manifest_rows) == 102
    receipt_rows = receipt["source_copy"]["file_entries"]
    indexed = {row["path"]: row for row in receipt_rows}
    assert len(indexed) == len(receipt_rows) == 104
    assert len([path for path in indexed if path.startswith(BASE + "/")]) == 103
    assert "02_REGISTRY/research/certificates/a4d_local_record_to_matter_intake_check.py" in indexed
    assert set(path for path in indexed if path.startswith(BASE + "/")) == {
        *manifest_rows.keys(), f"{BASE}/MANIFEST.json"
    }

    for rel, row in indexed.items():
        path = ROOT / rel
        assert path.is_file() and not path.is_symlink(), ("NOT_REGULAR_FILE", rel)
        data = path.read_bytes()
        assert len(data) == row["bytes"], ("SIZE_MISMATCH", rel)
        assert hashlib.sha256(data).hexdigest() == row["sha256"], ("SHA256_MISMATCH", rel)
        actual_blob = git_blob(path)
        assert actual_blob == row["control_git_blob"] == row["source_git_blob"], ("BLOB_MISMATCH", rel)
        if rel in manifest_rows:
            expected = manifest_rows[rel]
            assert len(data) == expected["bytes"] and hashlib.sha256(data).hexdigest() == expected["sha256"]

    report = json.loads(REPLAY.read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    assert sha256(REPLAY) == receipt["source_replay"]["report_sha256"]
    assert receipt["source_replay"]["status"] == "PASS"
    assert all(item["returncode"] == 0 for item in report["commands"])
    assert [item["name"] for item in report["commands"]] == [
        item["name"] for item in receipt["source_replay"]["command_groups"]
    ]
    assert receipt["source_replay"]["v3_exact_controls"] == 169
    assert receipt["source_replay"]["v3_interval_controls"] == 56
    assert receipt["source_replay"]["v3_executed_program_mutations"] == 4
    assert receipt["source_replay"]["L8"]["event"] == [355, 1064]

    direct_proof = ROOT / BASE / "continuation_v3/proofs/MOVING_PREPARATION_SOURCE_RU.md"
    proof_hash = hashlib.sha256(direct_proof.read_bytes()).hexdigest()
    assert proof_hash == receipt["user_inputs"]["moving_preparation_sha256"]
    assert receipt["scope"] == {
        "native_D0_admission_derived": False,
        "full_H_J_R_closed": False,
        "full_q_D_b_m_map_and_tangent_derived": False,
        "native_AF_refinement_derived": False,
        "physical_Ward_derived": False,
        "curved_Einstein_or_GR_closed": False,
        "new_Lean_compilation": False,
    }
    assert re.fullmatch(r"[0-9a-f]{40}", source["head"])
    print("PASS_MOVING_PREPARATION_CONTROL_INTAKE files=104 source_blobs=104 replay_groups=7")


if __name__ == "__main__":
    main()
