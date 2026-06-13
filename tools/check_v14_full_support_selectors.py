#!/usr/bin/env python3
"""Guard that Book 04 numerical selectors use full admissible supports, not local windows."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

REQUIRED = {
    LEAN / "Matter" / "Book04FullSupportSelectors.lean": [
        "ElectroweakDepthFullSupport := Fin 71",
        "ProtonReadoutFullSupport := Fin 613",
        "BetaUnlockDepthFullSupport := Fin 39",
        "electroweak_depth35_full_support_strict",
        "proton_readout306_full_support_strict",
        "beta_unlock_depth19_full_support_strict",
        "electroweak_depth35_full_support_no_free_alternative",
        "proton_readout306_full_support_no_free_alternative",
        "beta_unlock_depth19_full_support_no_free_alternative",
    ],
    LEAN / "Bridge" / "FinalBridgeIndex.lean": [
        "import D0.Matter.Book04FullSupportSelectors",
        "fullSupportElectroweakDepth35Claim",
        "fullSupportProtonReadout306Claim",
        "fullSupportBetaUnlockDepth19Claim",
        "book04FullSupportSelectorsClosed",
    ],
    LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean": [
        "import D0.Matter.Book04FullSupportSelectors",
        "D0.Matter.electroweak_depth35_full_support_strict",
        "D0.Matter.proton_readout306_full_support_strict",
        "D0.Matter.beta_unlock_depth19_full_support_strict",
    ],
    LEAN.parent / "docs" / "HARD_CLOSURE_TARGETS.csv": [
        "D0.Matter.Book04FullSupportSelectors,Matter.electroweak_depth35_full_support_strict,THEOREM",
        "D0.Matter.Book04FullSupportSelectors,Matter.proton_readout306_full_support_strict,THEOREM",
        "D0.Matter.Book04FullSupportSelectors,Matter.beta_unlock_depth19_full_support_strict,THEOREM",
    ],
    BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md": [
        "full-support finite selector owners",
        "D0.Matter.Book04FullSupportSelectors",
        "Fin 71",
        "Fin 613",
        "Fin 39",
        "Those windows are no longer the active theory",
    ],
    ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md": [
        "00.27 Book 04 full-support selector closure",
        "D0.Matter.Book04FullSupportSelectors",
    ],
    BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md": [
        "02.39 Book 04 full-support selector closure",
        "D0.Matter.Book04FullSupportSelectors",
    ],
    BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md": [
        "Full-support Book 04 selectors",
        "D0.Matter.Book04FullSupportSelectors",
    ],
}


def main() -> int:
    missing: list[str] = []
    for path, needles in REQUIRED.items():
        if not path.exists():
            missing.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                missing.append(f"{path.relative_to(ROOT)} lacks {needle!r}")
    if missing:
        print("FAIL_V14_FULL_SUPPORT_SELECTORS")
        for item in missing:
            print(" -", item)
        return 1
    print("PASS_V14_FULL_SUPPORT_SELECTORS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
