#!/usr/bin/env python3
"""v14 toral automorphism / Galois dark-balance synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"

LEAN_CHECKS = [
    (
        LEAN / "Dynamics" / "ToralAutomorphism.lean",
        [
            "def T",
            "trace_T2",
            "trace_T3",
            "trace_T5",
            "trace_evolution_unfolds_d0_geometry",
            "det_T",
            "det_T_pow",
            "toral_volume_conservation_square",
            "lucas",
            "signedLucasTrace",
            "trace_T_pow_eq_signed_lucas",
        ],
    ),
    (
        LEAN / "Dynamics" / "GaloisConjugateBalance.lean",
        [
            "ActiveArchiveTrace",
            "integer_trace_requires_full_time_matrix",
            "d0_integer_trace_layers",
            "generationTrace_eq_three",
            "abcdTrace_eq_four",
            "memoryTorusTrace_eq_eleven",
            "galoisConjugateBalanceClosure",
        ],
    ),
    (
        LEAN / "Dynamics" / "DarkSectorCoarseGrain.lean",
        [
            "darkSign",
            "dark_sign_even",
            "dark_sign_odd",
            "alternating_even_window_sum_zero",
            "dark_sector_even_window_readout_zero",
        ],
    ),
]

BOOK_CHECKS = [
    (
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "D0 time operator T unfolds integer geometry layers through signed Lucas traces",
            "dark/archive branch is the Galois conjugate required for integer finite traces",
        ],
    ),
    (
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        [
            "x^2+x-1=0",
            "time automorphism spectrum",
        ],
    ),
    (
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "Toral automorphism / Galois balance",
            "trace_evolution_unfolds_d0_geometry",
            "toral_volume_conservation_square",
            "dark_sector_even_window_readout_zero",
        ],
    ),
    (
        BOOKS / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        [
            "|Tr(T^2)|=3 generation carrier",
            "|Tr(T^3)|=4 ABCD capacity",
            "|Tr(T^5)|=11 memory torus",
        ],
    ),
    (
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        [
            "chi_T(lambda)=lambda^2+lambda-1",
            "spec(T)={phi^-1,-phi}",
            "Tr(T^n)=(-1)^n L_n",
        ],
    ),
    (
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "active contraction and archive expansion are eigen-branches of one toral automorphism",
            "determinant invariant gives exact phase-volume balance",
        ],
    ),
    (
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "dark sector = archive Galois branch",
            "coarse-grained phase-stable readout cancels alternating sign",
            "expansion is determinant balance, not fitted missing component",
        ],
    ),
]

INDEX_CHECKS = [
    (
        LEAN / "All.lean",
        [
            "import D0.Dynamics.ToralAutomorphism",
            "import D0.Dynamics.GaloisConjugateBalance",
            "import D0.Dynamics.DarkSectorCoarseGrain",
        ],
    ),
    (
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "D0.Dynamics.trace_evolution_unfolds_d0_geometry",
            "D0.Dynamics.toral_volume_conservation_square",
            "D0.Dynamics.dark_sector_even_window_readout_zero",
        ],
    ),
    (
        LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean",
        [
            "D0.Dynamics.trace_T2",
            "D0.Dynamics.det_T_pow",
            "D0.Dynamics.generationTrace_eq_three",
            "D0.Dynamics.memoryTorusTrace_eq_eleven",
        ],
    ),
    (
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_toral_trace_evolution_unfolds_d0_geometry",
            "T_toral_dark_sector_even_window_readout_zero",
        ],
    ),
    (
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-TORAL-AUTOMORPHISM-GALOIS-BALANCE-001",
            "vp_toral_automorphism_galois_balance.py",
        ],
    ),
]

CERT = ROOT / "05_CERTS" / "vp_toral_automorphism_galois_balance.py"
PDG_CERT = ROOT / "05_CERTS" / "vp_pdg_strict_passport.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


def check_tokens(
    errors: list[str], label: str, path: Path, tokens: list[str]
) -> None:
    if not path.exists():
        errors.append(f"{label}: missing {path.relative_to(ROOT)}")
        return
    text = read(path)
    for token in tokens:
        if token not in text:
            errors.append(f"{label}: missing token {token!r}")


def main() -> int:
    errors: list[str] = []

    for path, tokens in LEAN_CHECKS:
        check_tokens(errors, "Lean", path, tokens)
        if path.exists():
            code = code_without_line_comments(path)
            for token in ["sorry", "admit", "axiom", "unsafe", "Float"]:
                if re.search(rf"\b{re.escape(token)}\b", code):
                    errors.append(
                        f"{path.relative_to(ROOT)} contains forbidden token {token!r}"
                    )

    for path, tokens in BOOK_CHECKS + INDEX_CHECKS:
        check_tokens(errors, "sync", path, tokens)

    if not CERT.exists():
        errors.append("missing toral automorphism certificate")
    elif "PASS_TORAL_AUTOMORPHISM_GALOIS_BALANCE" not in read(CERT):
        errors.append("toral automorphism certificate missing PASS token")

    if not PDG_CERT.exists():
        errors.append("missing PDG strict passport cert")
    elif "lucas_trace_layer_diagnostic" not in read(PDG_CERT):
        errors.append("PDG strict passport missing optional Lucas diagnostic")

    if errors:
        print("FAIL_V14_TORAL_AUTOMORPHISM_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_TORAL_AUTOMORPHISM_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
