#!/usr/bin/env python3
"""Read-only replay of the new original-carrier field-minimum packet."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
# Literal input closure, including immutable historical snapshots and reviews.
INPUTS = [
    "02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_MINIMUM_EXCLUSION_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/COMPOSITION_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/CONDITIONAL_NOISE_SOURCE_NOTE.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/FROZEN_REPLAY.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/INDEPENDENT_MINIMUM_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/INFO_CURRENT_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/INFO_INPUTS.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/JOINT_FIELD_MINIMUM_OBSTRUCTION.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/JOINT_MINIMUM_AND_INFO_REVIEW.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/PROSPECTIVE_FIELD_BRIDGE_RESULT.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/PROSPECTIVE_FIELD_REALIZATION_BRIDGE.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/README.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/SHA256SUMS.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/SOURCE_INPUTS.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/VALIDATION.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/WITNESS_RECEIPT.json",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/check_conditional_noise.py",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/check_joint_minimum_witness.py",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/check_prospective_field_bridge.py",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/A4D_GOLDEN_FULL_SOURCE_SELECTION_SYNTHESIS_2026_10_20.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/FIXED_CLOCK_PREPARATION_BANK.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/FutureExecution.lean",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/FutureExecutionCompleteness.lean",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/GOLDEN_EXACT_DETECTOR.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/NATIVE_TASK_SEARCH_4867.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/PAID_RANDOM_CHOICE_MINIMUM.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/VerifiabilityNecessity.lean",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/adaptive_all_cost_extension.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/causal_boundary_completion.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/minimal_golden_source.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/original_all40.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/original_all40_checker.py",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/original_car_j2_source.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/prospective_execution.lean",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/q8_conditional_info.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/schur_completion.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/stopped_all_cost_source.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/stopped_minimum_overview.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/stopped_retained_record_comparison.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/inputs/support_safe_four_corner.md",
    "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/replay_packet.py"
]

def main():
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / "02_REGISTRY/research/sources/d0_native_joint_field_minimum_2026-10-20/replay_packet.py")],
        cwd=ROOT, check=False,
    )
    if result.returncode:
        raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
