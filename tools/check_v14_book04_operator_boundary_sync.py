#!/usr/bin/env python3
"""Guard that final v14 Book 04 operator boundaries are synchronized."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[Path, list[str]]] = [
    (LEAN / "Matter" / "Book04OperatorBoundary.lean", [
        "BaryonMultipletOperator",
        "CanPromoteBaryonMultiplet",
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "MesonTransferOperator",
        "CanPromoteMesonMasses",
        "lower_hodge_400_cannot_promote_meson_masses",
        "HiggsYukawaProjectorBridge",
        "CanPromoteHiggsYukawaCore",
        "missing_scalar_projector_cannot_promote_higgs_yukawa_core",
        "Book04OperatorBoundaryClosed",
        "book04_operator_boundaries_closed",
    ]),
    (LEAN / "All.lean", [
        "import D0.Matter.Book04OperatorBoundary",
    ]),
    (LEAN / "Bridge" / "FinalBridgeIndex.lean", [
        "import D0.Matter.Book04OperatorBoundary",
        "book04BaryonMultipletBoundary",
        "book04Meson400Boundary",
        "book04HiggsScalarProjectorBoundary",
        "book04OperatorBoundariesClosed",
    ]),
    (LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean", [
        "D0.Matter.nucleon_line_cannot_promote_full_baryon_multiplet",
        "D0.Matter.lower_hodge_400_cannot_promote_meson_masses",
        "D0.Matter.missing_scalar_projector_cannot_promote_higgs_yukawa_core",
        "D0.Matter.book04_operator_boundaries_closed",
    ]),
    (ROOT / "09_LEAN_FORMALIZATION" / "docs" / "HARD_CLOSURE_TARGETS.csv", [
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "lower_hodge_400_cannot_promote_meson_masses",
        "missing_scalar_projector_cannot_promote_higgs_yukawa_core",
        "book04_operator_boundaries_closed",
    ]),
    (ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md", [
        "00.26 Book 04 operator-boundary closure",
        "D0.Matter.book04_operator_boundaries_closed",
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "lower_hodge_400_cannot_promote_meson_masses",
        "missing_scalar_projector_cannot_promote_higgs_yukawa_core",
    ]),
    (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md", [
        "02.36.3b Book 04 operator-boundary closure",
        "D0.Matter.book04_operator_boundaries_closed",
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "lower_hodge_400_cannot_promote_meson_masses",
        "missing_scalar_projector_cannot_promote_higgs_yukawa_core",
    ]),
    (BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md", [
        "Baryon multiplet boundary as a closed no-go",
        "Meson/chiral boundary as a closed no-go",
        "Higgs/scalar projector boundary",
        "D0.Matter.book04_operator_boundaries_closed",
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "lower_hodge_400_cannot_promote_meson_masses",
        "missing_scalar_projector_cannot_promote_higgs_yukawa_core",
    ]),
    (BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md", [
        "## 05.13 Current v14 priority gates",
        "D0.Matter.Book04OperatorBoundary",
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "lower_hodge_400_cannot_promote_meson_masses",
    ]),
]

forbidden: list[tuple[Path, list[str]]] = [
    (BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md", [
        "The active statement is operator-level only: D0 exposes the missing operator type and forbids direct Hodge-mass reading.",
        "The previous attempt to write direct `Δ, Λ, Ω` formulas is not part of the active v14 matter theorem.",
        "Higgs projector still required for full scalar sector",
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

for path, needles in forbidden:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            failures.append(f"{path.relative_to(ROOT)} contains stale operator-boundary wording {needle!r}")

if failures:
    print("FAIL_V14_BOOK04_OPERATOR_BOUNDARY_SYNC")
    for failure in failures:
        print(" -", failure)
    sys.exit(1)

print("PASS_V14_BOOK04_OPERATOR_BOUNDARY_SYNC")
