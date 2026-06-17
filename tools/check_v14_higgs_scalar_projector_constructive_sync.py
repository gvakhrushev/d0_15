#!/usr/bin/env python3
"""v14 constructive Higgs/scalar projector synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"

OWNER = LEAN / "Matter" / "HiggsScalarProjectorConstructive.lean"
CERT = ROOT / "05_CERTS" / "vp_higgs_scalar_projector_constructive.py"

LEAN_TOKENS = [
    "FrozenSU2_X",
    "FrozenSU2_Z",
    "IntertwinesFrozenSU2",
    "IsProjector",
    "commutes_XZ_forces_scalar_matrix",
    "nonzero_gauge_idempotent_eq_identity",
    "rank1_scalar_projector_breaks_su2_gauge_compatibility",
    "rank2_scalar_projector_exists",
    "minimal_positive_scalar_projector_rank_two",
    "minimal_positive_scalar_projector_unique",
    "higgs_yukawa_core_promotion_valid",
]

BOOK_CHECKS = [
    (
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "Constructive Scalar Projector Closure",
            "FrozenSU2_X",
            "FrozenSU2_Z",
            "P=aI",
            "trace-rank is 2",
            "Torus radius is not Higgs VEV",
            "torus aspect is not Higgs mass",
        ],
    ),
    (
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "commutes_XZ_forces_scalar_matrix",
            "nonzero_gauge_idempotent_eq_identity",
            "rank1_scalar_projector_breaks_su2_gauge_compatibility",
            "rank2_scalar_projector_exists",
            "minimal_positive_scalar_projector_rank_two",
            "minimal_positive_scalar_projector_unique",
            "higgs_yukawa_core_promotion_valid",
        ],
    ),
    (
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "Scalar/Yukawa promotion is accepted only if it points to the constructive",
            "rank-2 scalar projector theorem",
            "External Higgs mass, VEV, SM potential, or",
            "PDG data cannot promote Yukawa core terms",
        ],
    ),
    (
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "Higgs/scalar projector closure",
            "finite left/right matter-transfer bridge",
            "before scalar/Yukawa terms can enter the D0 core",
        ],
    ),
]

INDEX_CHECKS = [
    (
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "D0.Matter.commutes_XZ_forces_scalar_matrix",
            "D0.Matter.nonzero_gauge_idempotent_eq_identity",
            "D0.Matter.higgs_yukawa_core_promotion_valid",
        ],
    ),
    (
        LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean",
        [
            "D0.Matter.rank1_scalar_projector_breaks_su2_gauge_compatibility",
            "D0.Matter.rank2_scalar_projector_exists",
            "D0.Matter.minimal_positive_scalar_projector_unique",
        ],
    ),
    (
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001",
            "vp_higgs_scalar_projector_constructive.py",
        ],
    ),
    (
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_higgs_commutes_xz_scalar_matrix",
            "T_higgs_yukawa_core_promotion_valid",
        ],
    ),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


def main() -> int:
    errors: list[str] = []

    if not OWNER.exists():
        errors.append(f"missing Lean owner {OWNER.relative_to(ROOT)}")
    else:
        text = read(OWNER)
        code = code_without_line_comments(OWNER)
        for token in LEAN_TOKENS:
            if token not in text:
                errors.append(f"Lean owner missing token {token!r}")
        for token in ["sorry", "admit", "axiom", "unsafe", "Float"]:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"Lean owner contains forbidden token {token!r}")

    if not CERT.exists():
        errors.append("missing vp_higgs_scalar_projector_constructive.py")
    elif "PASS_HIGGS_SCALAR_PROJECTOR_RANK_TWO" not in read(CERT):
        errors.append("constructive Higgs cert missing PASS token")

    for path, tokens in BOOK_CHECKS + INDEX_CHECKS:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{path.relative_to(ROOT)} missing token {token!r}")

    if errors:
        print("FAIL_V14_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
