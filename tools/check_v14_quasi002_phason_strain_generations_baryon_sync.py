#!/usr/bin/env python3
"""v14 QUASI-002 phason-strain generations / baryon S3 synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
CERTS = ROOT / "05_CERTS"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Lean phason/baryon S3 owner",
        LEAN / "Matter" / "PhasonStrainGenerations.lean",
        [
            "D0PhiQuasicrystalVacuum",
            "PhasonMode",
            "phason_mode_card_eq_three",
            "PhasonStrainTensor",
            "generation_phason_mode_card_eq_three",
            "BaryonPhasonTriple",
            "baryon_phason_triple_card_eq_27",
            "baryon_phason_symmetric_sector_dim_eq_ten",
            "phason_s3_symmetrizer_admits_baryon_decuplet_transfer",
            "full_baryon_multiplet_requires_phason_s3_symmetrizer",
            "phason_strain_generations_baryon_closure",
        ],
    ),
    (
        "Python certificate",
        CERTS / "vp_quasi002_phason_strain_generations_baryon.py",
        [
            "PASS_QUASI002_PHASON_STRAIN_GENERATIONS_BARYON",
            "pi_sym_idempotent",
            "pi_sym_rank_eq_10",
            "nucleon_line_does_not_span_decuplet",
        ],
    ),
    (
        "Book 02 proof cell",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "D0-QUASI-002A",
            "Phason Strain Generations / Baryon S3",
            "phason_strain_generations_baryon_closure",
        ],
    ),
    (
        "Book 04 matter integration",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "matter generations and baryons as phason modes",
            "BaryonPhasonTriple",
            "baryon_phason_symmetric_sector_dim_eq_ten",
        ],
    ),
    (
        "Book 05 verification gate",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "baryon S3 carrier",
            "antisymmetric nucleon-line sectors are annihilated",
            "nucleon_line_cannot_promote_full_baryon_multiplet",
        ],
    ),
    (
        "Book 08 archive split",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "phason coordinate reuse does not identify archive dark strain with baryon S3 transfer",
            "baryon phason-strain-generations module",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_quasi002_phason_mode_card_three",
            "T_quasi002_phason_baryon_s3_decuplet",
            "T_quasi002_phason_strain_generations_baryon_closure",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-QUASI002-PHASON-STRAIN-GENERATIONS-BARYON-001",
            "D0.Matter.PhasonStrainGenerations",
            "vp_quasi002_phason_strain_generations_baryon.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        [
            "quasi002-phason-baryon",
            "PASS_QUASI002_PHASON_STRAIN_GENERATIONS_BARYON",
            "check_v14_quasi002_phason_strain_generations_baryon_sync.py",
        ],
    ),
]

FORBIDDEN_LEAN_TOKENS = ["sorry", "admit", "axiom", "unsafe", "Float", "opaque"]


def main() -> int:
    errors: list[str] = []
    for label, path, tokens in CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")

    lean_path = LEAN / "Matter" / "PhasonStrainGenerations.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"Lean phason/baryon S3 owner contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS_QUASI002_PHASON_STRAIN_GENERATIONS_BARYON_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
