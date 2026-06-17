#!/usr/bin/env python3
"""v14 trace-heat-capacity gravity synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"
CERT = ROOT / "05_CERTS" / "vp_trace_heat_capacity_gravity.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


LEAN_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Fixed detector time ladder owner",
        LEAN / "Core" / "FixedDetectorTimeLadder.lean",
        [
            "TimeState",
            "FixedDetector",
            "evolveState",
            "detectorQuadraticReadout",
            "ladderReadout",
            "detector_fixed_under_time_ladder",
            "readout_depends_on_time_power",
            "active_archive_trace_readout_integer",
        ],
    ),
    (
        "Trace heat Lucas core owner",
        LEAN / "Dynamics" / "TraceHeatLucasCore.lean",
        [
            "TimeEnergyOperator",
            "heat_moment_T2_eq_even_lucas_trace",
            "even_trace_eq_lucas_even",
            "heat_moment_eq_even_lucas",
            "NFermionInt",
            "NFermion",
            "lefschetz_spectrum_unfolds_scene",
        ],
    ),
    (
        "Trace heat capacity gravity owner",
        LEAN / "Dynamics" / "TraceHeatCapacityGravity.lean",
        [
            "TraceHeatLucasCore",
            "TraceHeatCapacityRegion",
            "LocalHeatContent",
            "BoundaryCapacityForRegion",
            "TraceHeatDefect",
            "SaturatedRegion",
            "HorizonRegion",
            "RequiresBoundaryEncoding",
            "boundary_capacity_is_quarter_cut_weight",
            "saturated_region_forces_boundary_encoding",
            "black_hole_capacity_saturation_rule",
            "heat_trace_entropy_gradient_admits_gravity_interface",
        ],
    ),
]

TEXT_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Book 00 trace-heat spine",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "Trace-Heat-Capacity Gravity links the fixed D0 time operator",
            "boundary capacity saturation",
        ],
    ),
    (
        "Book 01 fixed detector ladder",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        [
            "The detector is fixed; the division ladder evolves by T^n",
            "Readout is D^dagger D applied to the T^n-state",
        ],
    ),
    (
        "Book 03 Lefschetz scene counts",
        BOOKS / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        [
            "NFermion(3)=4",
            "NFermion(4)=9",
            "NFermion(5)=11",
            "NFermion(3)+NFermion(4)=13",
            "NFermion(6)=20",
        ],
    ),
    (
        "Book 05 verification row",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            # Pinned to the present 05.26 split sentence (line ~1062): sentence-case
            # heading form + the real core/bridge anchors it now names.
            "Trace-heat-capacity gravity",
            "Lucas traces",
            "heat moments",
            "A/4 capacity",
            "macro gravity witness",
        ],
    ),
    (
        "Book 06 trace/heat runtime",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        [
            "Tr(T^n)=(-1)^n L_n",
            "heat moments of `T^2` are even Lucas traces",
            "fixed detector reads `T^n` layers",
        ],
    ),
    (
        "Book 07 capacity gravity",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "Trace-Heat-Capacity Gravity",
            "black-hole capacity saturation",
            "local information-capacity saturation",
            "boundary capacity",
        ],
    ),
    (
        "Book 08 archive branch",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "Dark/archive branch remains the Galois completion",
            "black-hole-like regions = finite boundary-capacity saturation events",
        ],
    ),
    (
        "D0.All imports",
        LEAN / "All.lean",
        [
            "import D0.Core.FixedDetectorTimeLadder",
            "import D0.Dynamics.TraceHeatCapacityGravity",
        ],
    ),
    (
        "FinalBridgeIndex trace-heat checks",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "D0.Core.detector_fixed_under_time_ladder",
            "D0.Core.readout_depends_on_time_power",
            "D0.Core.active_archive_trace_readout_integer",
            "D0.Dynamics.heat_moment_eq_even_lucas",
            "D0.Dynamics.lefschetz_spectrum_unfolds_scene",
            "D0.Dynamics.black_hole_capacity_saturation_rule",
            "D0.Dynamics.heat_trace_entropy_gradient_admits_gravity_interface",
        ],
    ),
    (
        "HardClosureTheoremIndex trace-heat checks",
        LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean",
        [
            "D0.Core.detector_fixed_under_time_ladder",
            "D0.Core.readout_depends_on_time_power",
            "D0.Core.active_archive_trace_readout_integer",
            "D0.Dynamics.heat_moment_eq_even_lucas",
            "D0.Dynamics.lefschetz_spectrum_unfolds_scene",
            "D0.Dynamics.black_hole_capacity_saturation_rule",
            "D0.Dynamics.heat_trace_entropy_gradient_admits_gravity_interface",
        ],
    ),
    (
        "Hard closure target rows",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_fixed_detector_time_ladder_fixed",
            "T_trace_heat_moment_eq_even_lucas",
            "T_trace_heat_lefschetz_spectrum_unfolds_scene",
            "T_trace_heat_black_hole_capacity_saturation_rule",
            "T_trace_heat_entropy_gradient_gravity_interface",
        ],
    ),
    (
        "Claim map trace-heat row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-TRACE-HEAT-CAPACITY-GRAVITY-001",
            "D0.Core.FixedDetectorTimeLadder;D0.Dynamics.TraceHeatCapacityGravity",
            "vp_trace_heat_capacity_gravity.py",
        ],
    ),
    (
        "Hard closure runner integration",
        RUNNER,
        [
            "vp_trace_heat_capacity_gravity.py",
            "PASS_TRACE_HEAT_CAPACITY_GRAVITY",
            "check_v14_trace_heat_capacity_gravity_sync.py",
        ],
    ),
]

FORBIDDEN = ["sorry", "admit", "axiom", "unsafe", "Float"]


def check_tokens(errors: list[str], label: str, path: Path, tokens: list[str]) -> None:
    if not path.exists():
        errors.append(f"{label}: missing {path.relative_to(ROOT)}")
        return
    text = read(path)
    for token in tokens:
        if token not in text:
            errors.append(f"{label}: missing token {token!r}")


def main() -> int:
    errors: list[str] = []

    for label, path, tokens in LEAN_CHECKS:
        check_tokens(errors, label, path, tokens)
        if path.exists():
            code = code_without_line_comments(path)
            for token in FORBIDDEN:
                if re.search(rf"\b{re.escape(token)}\b", code):
                    errors.append(f"{label}: forbidden token {token!r}")

    for label, path, tokens in TEXT_CHECKS:
        check_tokens(errors, label, path, tokens)

    if not CERT.exists():
        errors.append("trace-heat-capacity gravity certificate is missing")
    elif "PASS_TRACE_HEAT_CAPACITY_GRAVITY" not in read(CERT):
        errors.append("trace-heat-capacity gravity certificate missing PASS token")

    if errors:
        print("FAIL_V14_TRACE_HEAT_CAPACITY_GRAVITY_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_TRACE_HEAT_CAPACITY_GRAVITY_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
