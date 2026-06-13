#!/usr/bin/env python3
"""Guard that v14 P8 tick-gauge / Lorentz strengthening is synchronized."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[Path, list[str]]] = [
    (LEAN / "Bridge" / "InternalConeSpeed.lean", [
        "FiniteCausalTickSection",
        "finiteCausalTickSectionGauge",
        "finite_causal_tick_section_forces_same_tick",
        "finite_causal_tick_section_cone_speed_eq_one",
        "common_tick_rescaling_preserves_internal_cone_speed",
        "asymmetric_ticks_not_internal_gauge",
    ]),
    (LEAN / "Bridge" / "TickGaugeLorentz.lean", [
        "FiniteLorentzTickGaugeClosure",
        "finite_lorentz_tick_gauge_cone_speed_closed",
        "finite_lorentz_tick_gauge_signature_closed",
        "finite_lorentz_tick_gauge_no_euclidean_export",
        "finite_lorentz_tick_gauge_no_split_export",
        "finite_lorentz_tick_rescaling_preserves_closure",
    ]),
    (LEAN / "All.lean", [
        "import D0.Bridge.TickGaugeLorentz",
    ]),
    (LEAN / "Bridge" / "FinalBridgeIndex.lean", [
        "import D0.Bridge.TickGaugeLorentz",
        "finiteCausalTickSectionForcesSameTick",
        "finiteCausalTickSectionConeSpeedIsOne",
        "commonTickRescalingPreservesConeSpeed",
        "asymmetricTicksNotInternalGauge",
        "finiteLorentzTickGaugeConeSpeedClosed",
        "finiteLorentzTickGaugeSignatureClosed",
        "finiteLorentzTickGaugeNoEuclideanExport",
        "finiteLorentzTickGaugeNoSplitExport",
        "finiteLorentzTickRescalingPreservesClosure",
    ]),
    (LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean", [
        "D0.Bridge.finite_causal_tick_section_forces_same_tick",
        "D0.Bridge.finite_causal_tick_section_cone_speed_eq_one",
        "D0.Bridge.common_tick_rescaling_preserves_internal_cone_speed",
        "D0.Bridge.asymmetric_ticks_not_internal_gauge",
        "D0.Bridge.finite_lorentz_tick_gauge_cone_speed_closed",
        "D0.Bridge.finite_lorentz_tick_gauge_signature_closed",
        "D0.Bridge.finite_lorentz_tick_gauge_no_euclidean_export",
        "D0.Bridge.finite_lorentz_tick_gauge_no_split_export",
    ]),
    (ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md", [
        "00.24 Tick-gauge / Lorentz strengthening",
        "D0.Bridge.FiniteCausalTickSection",
        "D0.Bridge.FiniteLorentzTickGaugeClosure",
        "asymmetric meter/second export belongs to SI calibration",
    ]),
    (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md", [
        "02.38 Tick-gauge and Lorentz-compatible cone invariant",
        "finite_causal_tick_section_cone_speed_eq_one",
        "finite_lorentz_tick_gauge_no_euclidean_export",
        "finite_lorentz_tick_rescaling_preserves_closure",
    ]),
    (BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md", [
        "## 05.13 Current v14 priority gates",
        "D0.Bridge.TickGaugeLorentz",
        "may not introduce a second D0 propagation primitive",
    ]),
    (BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md", [
        "06.36 v14 tick-gauge closure",
        "D0.Bridge.FiniteCausalTickSection",
        "D0.Bridge.finite_causal_tick_section_cone_speed_eq_one",
        "D0.Bridge.asymmetric_ticks_not_internal_gauge",
        "D0.Bridge.FiniteLorentzTickGaugeClosure",
    ]),
    (BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md", [
        "07.36 Tick-gauge compatibility of the gravity bridge",
        "finite weak-field quotient -> TT spin-2 representative",
        "finite tick/Lorentz closure -> one cone invariant and signature (1,3)",
    ]),
]

failures: list[str] = []
for path, needles in checks:
    if not path.exists():
        failures.append(f"missing {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            failures.append(f"{path.relative_to(ROOT)} missing {needle!r}")

for path in [
    BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
    BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
]:
    text = path.read_text(encoding="utf-8")
    for forbidden in [
        "SI c is a D0 core primitive",
        "laboratory meters choose the internal cone speed",
        "Euclidean signature can be exported as D0 core geometry",
        "split signature can be exported as D0 core geometry",
    ]:
        if forbidden in text:
            failures.append(f"{path.relative_to(ROOT)} contains forbidden overclaim {forbidden!r}")

if failures:
    print("FAIL_V14_TICK_LORENTZ_SYNC")
    for f in failures:
        print(" -", f)
    sys.exit(1)

print("PASS_V14_TICK_LORENTZ_SYNC")
