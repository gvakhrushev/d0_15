#!/usr/bin/env python3
"""Read-only replay of the bounded global result-composition packet."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
# Literal complete closure: frozen raw owners, proofs, reviews and replay.
INPUTS = [
    "02_REGISTRY/research/A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/COMPOSITION_INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/FROZEN_REPLAY.json",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/FULL_PRICE_COMPOSITION.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/HOLONOMY_SOURCE_AND_REFINEMENT.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/OPERATIONAL_CURVATURE_RECOVERY.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/OPERATIONAL_INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/PRICE_AND_WRITER_INDEPENDENT_REVIEW.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/README.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/SHA256SUMS.json",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/SOURCE_INPUTS.json",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/check_full_price.py",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/check_holonomy_source.py",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/check_operational_curvature.py",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/FutureExecution.lean",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/ProspectiveExecution.lean",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/TheoryTransfer.lean",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/VerificationCore.lean",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/book_clock_anchor.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/condensed_naturality.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/field_price_bridge.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/foundation_transfer.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/full_price_binding.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/golden_blowup.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/golden_book_mean.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/golden_book_mean_review.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/golden_detector.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/joint_minimum.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/joint_minimum_proof.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/julia_odds_current.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/julia_odds_historical.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/midpoint_recovery.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/native_car_actuation.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/native_car_actuation_review.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/native_compiler_info.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/native_field_writer.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/native_field_writer_review.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/original_all40.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/original_julia_owner.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/paid_paired_source.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/query_minimum.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/reference_cocycle.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/retained_clock_price.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/same_history_price.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/screen_mixed_gate.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/inputs/vsi_lovelock.md",
    "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/replay_packet.py"
]


def main():
    result = subprocess.run(
        [sys.executable, "-B", "-O", str(ROOT / "02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/replay_packet.py")],
        cwd=ROOT, check=False,
    )
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
