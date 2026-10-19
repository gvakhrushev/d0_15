#!/usr/bin/env python3
"""Check the pinned Lean receipt for the joint scene/field interface capsule."""

import hashlib
import json
import re
from pathlib import Path


PREFIX = "02_REGISTRY/research/certificates/a4d_native_history_field_coupling"
RECEIPT = PREFIX + "_results.json"
STANDARD_AXIOMS = {"Classical.choice", "Quot.sound", "propext"}
DECLARATIONS = [
    "scene_protocol_verified",
    "path_sum_composition",
    "fieldAction",
    "fieldHistoryPrice",
    "fieldHistoryPrice_refines",
    "matched_baseline_action_protocols",
    "native_scalar_block_preserves_matched_baseline_energies",
    "matched_baseline_history_price_refines",
    "matched_baseline_same_value_different_response",
    "concrete_nonzero_memory_same_value_different_response",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    receipt = json.loads((root / RECEIPT).read_text())
    assert receipt["status"] == "PASS_SCOPED_TYPED_HISTORY_BOUNDARY"
    assert receipt["compiler_exit_code"] == 0 and receipt["sorryAx"] is False
    assert set(receipt["axioms"]) <= STANDARD_AXIOMS

    pins = dict(receipt["source_sha256"])
    pins.update(receipt["toolchain_sha256"])
    pins[receipt["capsule"]] = receipt["capsule_sha256"]
    pins[receipt["output"]] = receipt["output_sha256"]
    pins[receipt["checker"]] = receipt["checker_sha256"]
    assert all(sha256(root / path) == digest for path, digest in pins.items())

    capsule = (root / receipt["capsule"]).read_text()
    report = (root / "02_REGISTRY/research/A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md").read_text()
    output = (root / receipt["output"]).read_text()
    assert re.search(r"\bsorry\b", capsule) is None
    assert all(token not in output for token in ("error:", "warning:", "sorryAx"))
    assert all(f"D0.Research.NativeHistoryFieldCoupling.{name}" in output
               for name in DECLARATIONS)
    printed = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", output, re.S)
    assert len(printed) >= len(DECLARATIONS)
    used = {name.strip() for group in printed for name in group.split(",") if name.strip()}
    assert used <= STANDARD_AXIOMS
    packet = receipt["re_supplied_packet"]
    assert packet["remote_blobs_reverified"] is True
    assert packet["recovery_sha256"] in report and packet["result_sha256"] in report
    assert packet["head"] in report
    assert receipt["scope"] == {
        "G0_closed": False,
        "GR_closed": False,
        "D0_readout_derived": False,
        "full_native_refinement_constructed": False,
        "physical_action_selected": False,
    }
    print("PASS_NATIVE_HISTORY_FIELD_COUPLING", len(DECLARATIONS), "declarations; standard axioms only")


if __name__ == "__main__":
    main()
