#!/usr/bin/env python3
"""v14 CKM basis-origin guard.

This guard prevents the CKM P4 integration from being only a prose claim or only
an isolated Lean file.  CKM must be represented as a finite up/down basis-origin
object in Lean, assembled into FinalFoundationIndex, imported by aggregate
indexes, and reflected in Books 00/02/04/05.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "CKMBasisOrigin Lean owner",
        LEAN / "Matter" / "CKMBasisOrigin.lean",
        [
            "structure FiniteOperatorBasisFamily",
            "structure StrictOperatorBasisSelection",
            "structure CKMBasisOrigin",
            "structure CKMOriginCandidate",
            "theorem ckm_origin_candidate_matrix_unique",
            "theorem ckm_no_free_matrix_at_fixed_basis_origin",
            "theorem ckm_origin_no_alternative_up_basis",
            "theorem ckm_origin_no_alternative_down_basis",
            "def concreteCKMBasisOrigin",
            "theorem concrete_ckm_origin_no_free_matrix",
        ],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "FinalFoundationIndex owns CKM origin",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "import D0.Matter.CKMBasisOrigin",
            "ckmOriginCandidateMatrixUnique",
            "ckmNoFreeMatrixAtFixedBasisOrigin",
            "concreteCKMBasisOrigin",
            "D0.Matter.ckm_origin_candidate_matrix_unique",
            "D0.Matter.ckm_no_free_matrix_at_fixed_basis_origin",
        ],
        ["def FinalFoundationIndex : Prop := True"],
    ),
    (
        "Book 04 CKM basis-origin rewrite",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "CKM as finite basis origin, not a free matrix",
            "D0.Matter.CKMBasisOrigin",
            "ckm_origin_candidate_matrix_unique",
            "ckm_no_free_matrix_at_fixed_basis_origin",
            "finite up/down basis-origin selectors",
            "concrete physical score terms",
        ],
        [
            "basis-origin theorem remains v14 target",
            "derive the up/down bases themselves from D0 matter operators rather than taking them as fixed inputs",
        ],
    ),
    (
        "Book 02 proof spine CKM origin",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "CKM finite basis origin",
            "D0.Matter.CKMBasisOrigin",
            "ckm_origin_candidate_matrix_unique",
            "ckm_no_free_matrix_at_fixed_basis_origin",
        ],
        ["CKM basis mismatch"],
    ),
    (
        "Book 00 entry contract CKM origin",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "CKM basis origin:",
            "ckm_origin_candidate_matrix_unique",
            "ckm_no_free_matrix_at_fixed_basis_origin",
            "up/down bases are selected by finite basis-origin selectors",
        ],
        [],
    ),
    (
        "Book 05 verification contract CKM origin",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "CKM basis-origin theorem",
            "ckm_origin_candidate_matrix_unique",
            "ckm_no_free_matrix_at_fixed_basis_origin",
            "closed at the finite selector level by `CKMBasisOrigin`",
        ],
        ["P3 CKM basis-origin theorem: derive the bases, not only the matrix after bases are fixed"],
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
    if "import D0.Matter.CKMBasisOrigin" not in text:
        errors.append(f"{rel}: missing CKMBasisOrigin import")
    if rel.endswith("HardClosureTheoremIndex.lean"):
        for token in [
            "D0.Matter.ckm_origin_candidate_matrix_unique",
            "D0.Matter.ckm_no_free_matrix_at_fixed_basis_origin",
            "D0.Matter.concrete_ckm_origin_no_free_matrix",
        ]:
            if token not in text:
                errors.append(f"{rel}: missing #check token {token}")

if errors:
    print("FAIL_V14_CKM_ORIGIN_SYNC")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("PASS_V14_CKM_ORIGIN_SYNC")
