#!/usr/bin/env python3
"""Guard that v14 P9 Book 04 coefficient-origin closure is synchronized."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[Path, list[str]]] = [
    (LEAN / "Matter" / "Book04CoefficientOrigin.lean", [
        "ChargedLeptonCoefficientRow",
        "ChargedLeptonCoefficientOrigin",
        "concreteChargedLeptonCoefficientOrigin",
        "charged_lepton_coefficient_origin_row_unique",
        "charged_lepton_coefficient_table_forced",
        "charged_lepton_coefficient_no_free_row_alternative",
        "charged_lepton_coefficients_no_free_retuning",
    ]),
    (LEAN / "All.lean", [
        "import D0.Matter.Book04CoefficientOrigin",
    ]),
    (LEAN / "Bridge" / "FinalBridgeIndex.lean", [
        "import D0.Matter.Book04CoefficientOrigin",
        "concreteChargedLeptonCoefficientOrigin",
        "chargedLeptonCoefficientOriginRowUnique",
        "chargedLeptonCoefficientTableForced",
        "chargedLeptonCoefficientNoFreeRowAlternative",
        "chargedLeptonCoefficientsNoFreeRetuning",
    ]),
    (LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean", [
        "D0.Matter.charged_lepton_coefficient_origin_row_unique",
        "D0.Matter.charged_lepton_coefficient_table_forced",
        "D0.Matter.charged_lepton_coefficient_no_free_row_alternative",
        "D0.Matter.charged_lepton_coefficients_no_free_retuning",
    ]),
    (ROOT / "09_LEAN_FORMALIZATION" / "docs" / "HARD_CLOSURE_TARGETS.csv", [
        "T_charged_lepton_coefficient_origin_row_unique",
        "T_charged_lepton_coefficient_table_forced",
        "T_charged_lepton_coefficient_no_free_row_alternative",
        "T_charged_lepton_coefficients_no_free_retuning",
    ]),
    (ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md", [
        "00.25 Book 04 charged-lepton coefficient-origin closure",
        "D0.Matter.Book04CoefficientOrigin",
        "charged_lepton_coefficients_no_free_retuning",
        "external lepton masses -> choose r_g,p_g,B_g -> call the result D0 core",
    ]),
    (BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md", [
        "02.36.3a Charged-lepton coefficient-origin closure",
        "D0.Matter.ChargedLeptonCoefficientOrigin",
        "charged_lepton_coefficient_table_forced",
        "changed ratio row, exponent row or bridge-factor row is impossible",
    ]),
    (BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md", [
        "D0.Matter.ChargedLeptonCoefficientOrigin",
        "D0.Matter.charged_lepton_coefficient_table_forced",
        "D0.Matter.charged_lepton_coefficients_no_free_retuning",
        "These entries are read from the selected coefficient origin",
        "no longer has an independent coefficient knob",
    ]),
    (BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md", [
        "## 05.13 Current v14 priority gates",
        "D0.Matter.Book04CoefficientOrigin",
        "chargedLeptonCoefficientTableForced",
        "chargedLeptonCoefficientsNoFreeRetuning",
    ]),
]

forbidden: list[tuple[Path, list[str]]] = [
    (BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md", [
        "The full derivation of the numerical score coefficients `r_g`, `p_g`, `B_g` from a smaller operator origin remains a v14 target",
        "muon and tau comparisons are not allowed to become free Yukawa inputs",
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
            failures.append(f"{path.relative_to(ROOT)} contains stale coefficient-origin wording {needle!r}")

if failures:
    print("FAIL_V14_BOOK04_COEFFICIENT_ORIGIN_SYNC")
    for failure in failures:
        print(" -", failure)
    sys.exit(1)

print("PASS_V14_BOOK04_COEFFICIENT_ORIGIN_SYNC")
