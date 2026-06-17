#!/usr/bin/env python3
"""v14 guard for the concrete finite spin-2 wave operator."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"


CHECKS: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "FiniteSpin2WaveOperator Lean owner",
        LEAN / "Geometry" / "FiniteSpin2WaveOperator.lean",
        [
            "abbrev Role4",
            "def eta4",
            "def k4",
            "def u4",
            "def ePlus4",
            "def eCross4",
            "def PiTT4",
            "def WTT4",
            "theorem PiTT4_idempotent",
            "theorem PiTT4_kills_gauge",
            "theorem PiTT4_kills_trace",
            "theorem WTT4_energy_nonnegative",
            "theorem spin2_coupling_depends_only_on_tt_stress",
            "inductive TTPolarization4",
            "theorem tt_polarization_card_eq_two",
        ],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Finite spin-2 public cert",
        ROOT / "05_CERTS" / "vp_finite_spin2_wave_operator.py",
        ["PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE", "run_certificate"],
        [],
    ),
    (
        "Book 00 spin-2 master chain",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        ["explicit TT projector", "finite spin-2 wave operator", "operator first, passport second"],
        [],
    ),
    (
        "Book 02 spin-2 proof spine",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        ["D0.Geometry.FiniteSpin2WaveOperator", "PiTT4_idempotent", "WTT4_preserves_tt"],
        [],
    ),
    (
        "Book 05 spin-2 verification rule",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        ["explicit TT projector", "basis-wide", "no GR constants"],
        [],
    ),
    (
        "Book 06 eta4 tick-gauge relation",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        ["eta4 = diag(1,-1,-1,-1)", "k4", "u4", "c_D0=1"],
        [],
    ),
    (
        "Book 07 full spin-2 chain",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        ["PiTT4(h)", "WTT4", "vp_finite_spin2_wave_operator_concrete.py"],
        [],
    ),
]


def main() -> int:
    errors: list[str] = []
    for label, path, required, forbidden in CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in required:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")
        for token in forbidden:
            if token in text:
                errors.append(f"{label}: forbidden token {token!r}")

    if errors:
        print("FAIL_V14_SPIN2_WAVE_OPERATOR_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_SPIN2_WAVE_OPERATOR_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
