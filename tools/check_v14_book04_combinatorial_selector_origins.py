#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
checks = {
    "09_LEAN_FORMALIZATION/D0/Matter/Book04CombinatorialSelectorOrigins.lean": [
        "electroweak_selector_radius_from_omega8",
        "proton_readout_selector_radius_from_high_gain",
        "beta_unlock_selector_radius_from_weak_unlock",
        "book04CombinatorialSelectorOriginsClosed",
    ],
    "01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md": [
        "combinatorial origin of the supports",
        "D0.Matter.Book04CombinatorialSelectorOrigins",
    ],
    "09_LEAN_FORMALIZATION/D0/Bridge/FinalBridgeIndex.lean": [
        "book04CombinatorialSelectorOriginsClosed",
        "electroweakSelectorRadiusFromOmega8",
    ],
}
missing=[]
for rel, needles in checks.items():
    text=(root/rel).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            missing.append(f"{rel}: missing {needle}")
if missing:
    raise SystemExit("\n".join(missing))
print("PASS_V14_BOOK04_COMBINATORIAL_SELECTOR_ORIGINS")
