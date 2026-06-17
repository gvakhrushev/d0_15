#!/usr/bin/env python3
"""Guard that v14 P7 cosmology reproducibility split is synchronized."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[Path, list[str]]] = [
    (LEAN / "Cosmology" / "SurveyReproducibilitySplit.lean", [
        "InternalArchiveCosmologyObject",
        "SurveyLikelihoodPassport",
        "internal_archive_shape_independent_of_empirical_parameters",
        "survey_passport_preserves_internal_archive_shape",
        "survey_comparison_requires_nonempty_manifest",
        "survey_likelihood_cannot_promote_to_core_cosmology",
        "FrozenArchiveCosmology",
        "frozen_archive_cosmology_core_shape_closed",
    ]),
    (LEAN / "All.lean", [
        "import D0.Cosmology.SurveyReproducibilitySplit",
    ]),
    (LEAN / "Bridge" / "FinalBridgeIndex.lean", [
        "import D0.Cosmology.SurveyReproducibilitySplit",
        "cosmologyInternalShapeIndependent",
        "surveyPassportPreservesInternalShape",
        "surveyComparisonRequiresNonemptyManifest",
        "surveyLikelihoodCannotPromoteToCoreCosmology",
        "frozenArchiveCosmologyCoreShapeClosed",
    ]),
    (LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean", [
        "D0.Cosmology.internal_archive_shape_independent_of_empirical_parameters",
        "D0.Cosmology.survey_passport_preserves_internal_archive_shape",
        "D0.Cosmology.survey_comparison_requires_nonempty_manifest",
        "D0.Cosmology.survey_likelihood_cannot_promote_to_core_cosmology",
        "D0.Cosmology.frozen_archive_cosmology_core_shape_closed",
    ]),
    (ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md", [
        "Cosmology reproducibility split",
        "D0.Cosmology.SurveyReproducibilitySplit",
        "BAO/DESI/SDE/Hubble residual therefore a new D0 primitive is chosen",
    ]),
    (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md", [
        "02.37 Cosmology reproducibility split",
        "InternalArchiveCosmologyObject",
        "SurveyLikelihoodPassport",
        "survey likelihood cannot promote to core cosmology closure",
    ]),
    (BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md", [
        "## 05.13 Current inherited priority gates",
        "D0.Cosmology.SurveyReproducibilitySplit",
        "no BAO/DESI/SDE likelihood is allowed to promote to core cosmology closure",
    ]),
    (BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md", [
        "08.3.1 Frozen archive cosmology before survey likelihood",
        "InternalArchiveCosmologyObject",
        "SurveyLikelihoodPassport",
        "survey_comparison_requires_nonempty_manifest",
        "survey_likelihood_cannot_promote_to_core_cosmology",
        "08.41 Reproducibility split closure",
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

book08 = (BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md").read_text(encoding="utf-8")
for forbidden in [
    "survey residual selects a new D0 primitive",
    "BAO data choose the archive operator",
    "DESI data choose the S_DE window centers",
    "likelihood agreement is a core theorem",
]:
    if forbidden in book08:
        failures.append(f"Book 08 contains forbidden overclaim {forbidden!r}")

if failures:
    print("FAIL_V14_COSMOLOGY_SPLIT_SYNC")
    for f in failures:
        print(" -", f)
    sys.exit(1)

print("PASS_V14_COSMOLOGY_SPLIT_SYNC")
