#!/usr/bin/env python3
"""v14 Book 04 concrete-selector guard.

This guard prevents the concrete selector integration from staying only in Lean or
only in prose.  It checks the new concrete owners, their final-index presence,
and the Book 00/02/04/05 integration points.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

COMMON = [
    "chargedLeptonElectronTerminalClaim",
    "electroweakDepth35Claim",
    "protonReadout306Claim",
    "neutronArchiveSiblingClaim",
    "betaUnlockDepth19Claim",
]

checks: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "Book04ConcreteSelectors Lean owner",
        LEAN / "Matter" / "Book04ConcreteSelectors.lean",
        [
            "inductive ChargedLeptonBranch",
            "charged_lepton_electron_terminal_strict",
            "inductive ElectroweakDepthCandidate",
            "electroweak_depth35_strict",
            "inductive ProtonReadoutCandidate",
            "proton_readout306_strict",
            "inductive NeutronArchiveSiblingCandidate",
            "neutron_archive_sibling_strict",
            "inductive BetaUnlockDepthCandidate",
            "beta_unlock_depth19_strict",
            "charged_lepton_terminal_no_free_alternative",
            "electroweak_depth35_no_free_alternative",
            "proton_readout306_no_free_alternative",
            "neutron_archive_sibling_no_free_alternative",
            "beta_unlock_depth19_no_free_alternative",
        ] + COMMON,
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "FinalFoundationIndex owns concrete Book04 selectors",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "import D0.Matter.Book04ConcreteSelectors",
            "concreteChargedLeptonElectronTerminalClaim",
            "concreteElectroweakDepth35Claim",
            "concreteProtonReadout306Claim",
            "concreteNeutronArchiveSiblingClaim",
            "concreteBetaUnlockDepth19Claim",
        ] + COMMON,
        ["def FinalFoundationIndex : Prop := True"],
    ),
    (
        "Book 04 names concrete selector owners",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "Electroweak radial depth as a concrete selector",
            "D0.Matter.electroweakDepth35FullSupportClaim",
            "D0.Matter.chargedLeptonElectronTerminalClaim",
            "D0.Matter.protonReadout306FullSupportClaim",
            "D0.Matter.neutronArchiveSiblingClaim",
            "D0.Matter.betaUnlockDepth19FullSupportClaim",
            "Fin 71",
            "Fin 613",
            "Fin 39",
            "Those windows are no longer the active theory",
        ],
        ["depth 35\" by prose", "readout 306 is only a mnemonic"],
    ),
    (
        "Book 02 proof spine lists concrete selectors",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "Selector uniqueness and concrete Book 04 instances",
        ] + COMMON,
        [],
    ),
    (
        "Book 00 theory-improvement table lists concrete selectors",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "Concrete Book 04 selectors:",
            "Book 04 selectors as abstract labels",
        ] + COMMON,
        [],
    ),
    (
        "Book 05 integrated contract for concrete selectors",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "## 05.13 Current v14 priority gates",
            "D0.Matter.Book04ConcreteSelectors",
        ] + COMMON,
        [],
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

# Ensure new module is imported by aggregate indexes.
for rel in [
    "09_LEAN_FORMALIZATION/D0/All.lean",
    "09_LEAN_FORMALIZATION/D0/TheoremLedger/HardClosureTheoremIndex.lean",
]:
    path = ROOT / rel
    if path.exists() and "import D0.Matter.Book04ConcreteSelectors" not in path.read_text(encoding="utf-8"):
        errors.append(f"{rel}: missing Book04ConcreteSelectors import")

if errors:
    print("FAIL_V14_BOOK04_SELECTORS_SYNC")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("PASS_V14_BOOK04_SELECTORS_SYNC")
