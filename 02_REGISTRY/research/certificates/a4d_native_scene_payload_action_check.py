#!/usr/bin/env python3
"""Replay and validate the scoped joint scene/full-payload Lean certificate."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FORMALIZATION = ROOT / "03_FORMALIZATION"
CERT_DIR = ROOT / "02_REGISTRY/research/certificates"
CAPSULE = CERT_DIR / "a4d_native_scene_payload_action.lean"
OUTPUT = CERT_DIR / "a4d_native_scene_payload_action_output.txt"
RESULTS = CERT_DIR / "a4d_native_scene_payload_action_results.json"
NOTE = ROOT / "02_REGISTRY/research/A4D_NATIVE_SCENE_PAYLOAD_ACTION_BOUNDARY.md"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
DECLARATIONS = (
    "complete_product_edge_cost_fiber",
    "subunit_profile_rejected",
    "every_additive_history_is_forced_by_observed_edges",
    "genuine_root_difference",
    "same_state_different_matter_jet",
    "same_state_different_edge_price",
    "scalar_refinement_preserves_energies",
    "full_archive_lift_is_scalar_compatible",
    "one_action_edge_refines",
    "two_action_edge_refines",
    "one_action_archive_projection_refines",
    "two_action_archive_projection_refines",
    "background_variation_is_blind_one",
    "background_variation_is_blind_two",
)
SCOPE = {
    "observable_edge_cost_fiber": "EXACTLY_ALL_PROFILES_C_GE_1",
    "additive_scene_history_given_edges": "UNIQUE",
    "same_payload_full_coframe_link_all_grade_matter": True,
    "two_refinement_compatible_matter_responses": True,
    "subunit_edge_cost_rejected": True,
    "background_variation_for_both_profiles": "ZERO_FOR_EVERY_ADMISSIBLE_CURVE",
    "physical_native_preparation_derived": False,
    "physical_edge_cost_selected": False,
    "physical_metric_link_refinement_derived": False,
    "native_source_or_ward_derived": False,
    "positive_gr": False,
    "G0_closed": False,
    "global_closure": False,
    "whole_core_no_go": False,
    "original_parent_terminals_changed": False,
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def d0_import_closure() -> dict[str, Path]:
    pending = [CAPSULE]
    found: dict[str, Path] = {}
    while pending:
        source = pending.pop()
        for module in re.findall(r"^import (D0(?:\.[A-Za-z0-9_]+)+)\s*$", source.read_text(), re.M):
            rel = Path(*module.split("."))
            path = FORMALIZATION / rel.with_suffix(".lean")
            key = path.relative_to(ROOT).as_posix()
            if key not in found:
                if not path.is_file():
                    raise AssertionError(f"MISSING_D0_SOURCE {key}")
                found[key] = path
                pending.append(path)
    return found


def run_lean() -> str:
    proc = subprocess.run(
        ["lake", "env", "lean", "../02_REGISTRY/research/certificates/a4d_native_scene_payload_action.lean"],
        cwd=FORMALIZATION,
        text=True,
        capture_output=True,
        timeout=900,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        raise AssertionError(f"LEAN_FAILED rc={proc.returncode}\n{output[-5000:]}")
    return output


def check_output(output: str) -> tuple[list[str], int]:
    if any(token in output for token in ("error:", "warning:", "sorryAx")):
        raise AssertionError("LEAN_OUTPUT_HAS_ERROR_WARNING_OR_SORRYAX")
    missing = [name for name in DECLARATIONS if f"NativeScenePayloadAction.{name}" not in output]
    if missing:
        raise AssertionError(f"MISSING_RESOLVED_DECLARATIONS {missing}")
    printed = re.findall(r"'D0\.Research\.NativeScenePayloadAction\.[^']+' depends on axioms: \[(.*?)\]", output, re.S)
    if len(printed) != len(DECLARATIONS):
        raise AssertionError(f"AXIOM_PRINT_COUNT {len(printed)} != {len(DECLARATIONS)}")
    axioms: set[str] = set()
    for block in printed:
        axioms.update(x.strip() for x in block.replace("\n", " ").split(",") if x.strip())
    if axioms != EXPECTED_AXIOMS:
        raise AssertionError(f"AXIOM_SET {sorted(axioms)}")
    return sorted(axioms), len(printed)


def make_receipt(output: str, axioms: list[str], printed_count: int) -> dict:
    d0_sources = d0_import_closure()
    toolchain = [
        ROOT / "03_FORMALIZATION/lakefile.lean",
        ROOT / "03_FORMALIZATION/lake-manifest.json",
        ROOT / "03_FORMALIZATION/lean-toolchain",
    ]
    return {
        "status": "PASS_TYPED_PRODUCT_INTERFACE_UNDERDETERMINATION",
        "capsule": CAPSULE.relative_to(ROOT).as_posix(),
        "capsule_sha256": sha(CAPSULE),
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
        "proof_note": NOTE.relative_to(ROOT).as_posix(),
        "proof_note_sha256": sha(NOTE),
        "command": "lake env lean ../02_REGISTRY/research/certificates/a4d_native_scene_payload_action.lean",
        "command_cwd": "03_FORMALIZATION",
        "compiler_exit_code": 0,
        "sorryAx": False,
        "axioms": axioms,
        "printed_axiom_dependencies": printed_count,
        "compiled_declarations": list(DECLARATIONS),
        "input_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "transitive_d0_source_sha256": {name: sha(path) for name, path in sorted(d0_sources.items())},
        "toolchain_input_sha256": {
            path.relative_to(ROOT).as_posix(): sha(path) for path in toolchain
        },
        "scope": SCOPE,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true", help="run Lean and refresh the output receipt")
    parser.add_argument("--recompile", action="store_true", help="run Lean and compare with the pinned output")
    args = parser.parse_args()
    if args.record and args.recompile:
        raise SystemExit("choose at most one of --record and --recompile")

    if args.record:
        output = run_lean()
        axioms, printed_count = check_output(output)
        OUTPUT.write_text(output, encoding="utf-8")
        RESULTS.write_text(json.dumps(make_receipt(output, axioms, printed_count), indent=2) + "\n", encoding="utf-8")
    else:
        receipt = json.loads(RESULTS.read_text(encoding="utf-8"))
        if receipt["scope"] != SCOPE:
            raise AssertionError("PINNED_SCOPE_CHANGED")
        if sha(CAPSULE) != receipt["capsule_sha256"]:
            raise AssertionError("STALE_CAPSULE_PIN")
        if sha(NOTE) != receipt["proof_note_sha256"]:
            raise AssertionError("STALE_NOTE_PIN")
        output = OUTPUT.read_text(encoding="utf-8")
        if hashlib.sha256(output.encode()).hexdigest() != receipt["output_sha256"]:
            raise AssertionError("STALE_OUTPUT_PIN")
        axioms, printed_count = check_output(output)
        if axioms != receipt["axioms"] or printed_count != receipt["printed_axiom_dependencies"]:
            raise AssertionError("RECEIPT_AXIOM_MISMATCH")
        if args.recompile and run_lean() != output:
            raise AssertionError("LEAN_REPLAY_DIFFERS_FROM_PINNED_OUTPUT")
        current_sources = {name: sha(path) for name, path in d0_import_closure().items()}
        if current_sources != receipt["transitive_d0_source_sha256"]:
            raise AssertionError("STALE_TRANSITIVE_D0_SOURCE_PINS")
        current_toolchain = {
            name: sha(ROOT / name) for name in receipt["toolchain_input_sha256"]
        }
        if current_toolchain != receipt["toolchain_input_sha256"]:
            raise AssertionError("STALE_TOOLCHAIN_PINS")
    print(f"PASS_DECLARATIONS={len(DECLARATIONS)} AXIOMS={','.join(axioms)}")


if __name__ == "__main__":
    main()
