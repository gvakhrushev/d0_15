#!/usr/bin/env python3
"""v14 P5 spin-2 derivation guard.

The gravity carrier may not be represented only by a TT label.  The active
corpus must contain the finite weak-field quotient owner in Lean, assemble it
into FinalFoundationIndex, and rewrite Books 00/02/05/07 around the quotient
chain before the Einstein--Hilbert bridge.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "FiniteSpin2 quotient Lean owner",
        LEAN / "Geometry" / "FiniteSpin2.lean",
        [
            "structure FiniteWeakFieldQuotient",
            "longitudinalRepresentative",
            "traceRepresentative",
            "ttRepresentative",
            "quotientReconstruction",
            "conservedStressKillsLongitudinal",
            "conservedStressKillsTrace",
            "theorem finite_weak_field_quotient_yields_tt_representative",
            "theorem finite_gauge_trace_quotient_closed",
            "theorem finite_conserved_stress_spin2_coupling_closed",
            "theorem finite_trace_mode_removed_from_spin2_carrier",
        ],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "FiniteSpin2 concrete wave-operator Lean owner",
        LEAN / "Geometry" / "FiniteSpin2WaveOperator.lean",
        [
            "def eta4",
            "def ePlus4",
            "def eCross4",
            "def PiTT4",
            "theorem PiTT4_idempotent",
            "theorem PiTT4_is_tt",
            "theorem PiTT4_kills_trace",
            "theorem PiTT4_kills_gauge",
            "def WTT4",
            "theorem WTT4_preserves_tt",
            "theorem WTT4_energy_nonnegative",
            "theorem spin2_coupling_depends_only_on_tt_stress",
            "theorem tt_polarization_card_eq_two",
        ],
        ["sorry", "admit", "axiom", "unsafe", "Float", "variable (Pi_TT"],
    ),
    (
        "FinalFoundationIndex owns spin-2 derivation",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "finiteWeakFieldQuotientYieldsTT",
            "finiteGaugeTraceQuotientClosed",
            "finiteConservedStressSpin2CouplingClosed",
            "finiteTraceModeRemovedFromSpin2Carrier",
            "D0.Geometry.finite_weak_field_quotient_yields_tt_representative",
            "D0.Geometry.finite_conserved_stress_spin2_coupling_closed",
            "D0.Geometry.PiTT4_idempotent",
            "D0.Geometry.WTT4_preserves_tt",
            "D0.Geometry.spin2_coupling_depends_only_on_tt_stress",
        ],
        ["def FinalFoundationIndex : Prop := True"],
    ),
    (
        "Book 07 gravity rewrite",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "Finite spin-2 derivation theorem",
            "D0.Geometry.FiniteWeakFieldQuotient",
            "finite_weak_field_quotient_yields_tt_representative",
            "finite_gauge_trace_quotient_closed",
            "finite_conserved_stress_spin2_coupling_closed",
            "finite_trace_mode_removed_from_spin2_carrier",
            "finite weak-field gauge/trace quotient",
            "Poisson response plus a declared TT mode was not yet a derivation",
            "D0.Geometry.FiniteSpin2WaveOperator",
            "PiTT4_idempotent",
            "PiTT4_kills_trace",
            "vp_finite_spin2_wave_operator_concrete.py",
        ],
        ["Poisson equation resembles the Newtonian limit"],
    ),
    (
        "Book 02 proof spine spin-2 derivation",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "Spin-2 derivation and internal cone speed",
            "D0.Geometry.FiniteWeakFieldQuotient",
            "finite_weak_field_quotient_yields_tt_representative",
            "finite_conserved_stress_spin2_coupling_closed",
            "Poisson response plus a named TT mode is not enough",
            "D0.Geometry.FiniteSpin2WaveOperator",
            "PiTT4_idempotent",
            "WTT4_preserves_tt",
        ],
        [],
    ),
    (
        "Book 00 entry contract spin-2 quotient",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "finite spin-2 derivation:",
            "finite_weak_field_quotient_yields_tt_representative",
            "finite_conserved_stress_spin2_coupling_closed",
            "FiniteWeakFieldQuotient",
            "Poisson-like response therefore GR",
        ],
        [],
    ),
    (
        "Book 05 integrated contract spin-2 derivation",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "## 05.13 Current inherited priority gates",
            "D0.Geometry.FiniteWeakFieldQuotient",
            "finite_weak_field_quotient_yields_tt_representative",
            "finite_conserved_stress_spin2_coupling_closed",
            "D0.Geometry.FiniteSpin2WaveOperator",
            "PiTT4_idempotent",
            "spin2_coupling_depends_only_on_tt_stress",
        ],
        ["P4 Spin-2 derivation: obtain TT decomposition"],
    ),
]

errors: list[str] = []
for label, path, required, forbidden in checks:
    if not path.exists():
        errors.append(f"{label}: missing file {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for token in required:
        if token not in text:
            errors.append(f"{label}: missing token {token!r}")
    for token in forbidden:
        if token in text:
            errors.append(f"{label}: forbidden token {token!r}")

for rel in [
    "09_LEAN_FORMALIZATION/D0/All.lean",
    "09_LEAN_FORMALIZATION/D0/TheoremLedger/HardClosureTheoremIndex.lean",
]:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"{rel}: missing aggregate file")
        continue
    text = path.read_text(encoding="utf-8")
    if "import D0.Geometry.FiniteSpin2" not in text:
        errors.append(f"{rel}: missing FiniteSpin2 import")
    if "import D0.Geometry.FiniteSpin2WaveOperator" not in text:
        errors.append(f"{rel}: missing FiniteSpin2WaveOperator import")
    if rel.endswith("HardClosureTheoremIndex.lean"):
        for token in [
            "D0.Geometry.finite_weak_field_quotient_yields_tt_representative",
            "D0.Geometry.finite_gauge_trace_quotient_closed",
            "D0.Geometry.finite_conserved_stress_spin2_coupling_closed",
            "D0.Geometry.finite_trace_mode_removed_from_spin2_carrier",
            "D0.Geometry.PiTT4_idempotent",
            "D0.Geometry.PiTT4_kills_trace",
            "D0.Geometry.PiTT4_kills_gauge",
            "D0.Geometry.WTT4_preserves_tt",
            "D0.Geometry.spin2_coupling_depends_only_on_tt_stress",
        ]:
            if token not in text:
                errors.append(f"{rel}: missing #check token {token}")

if errors:
    print("FAIL_V14_SPIN2_DERIVATION_SYNC")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("PASS_V14_SPIN2_DERIVATION_SYNC")
