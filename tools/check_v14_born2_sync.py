#!/usr/bin/env python3
"""v14 Born 2.0 guard: finite-effect readout must be theorem-owned and book-owned."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "BornFiniteEffects Lean owner",
        LEAN / "Core" / "BornFiniteEffects.lean",
        [
            "structure FiniteEffectFrame",
            "finite_effect_born_readout_unique",
            "finite_effect_born_no_hidden_response",
            "finite_coarse_born_readout_unique",
            "finite_power_readout_no_alternative",
            "finite_tensor_born_readout_unique",
        ],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "FinalFoundationIndex owns Born 2.0",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "finiteEffectBornReadoutUnique",
            "finiteEffectBornNoHiddenResponse",
            "finiteCoarseBornReadoutUnique",
            "finitePowerReadoutNoAlternative",
            "finiteTensorBornReadoutUnique",
        ],
        ["def FinalFoundationIndex : Prop := True"],
    ),
    (
        "Book 01 explains finite-effect Born 2.0",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        [
            "Finite-frame Born 2.0",
            "D0.finite_effect_born_readout_unique",
            "D0.finite_coarse_born_readout_unique",
            "D0.finite_tensor_born_readout_unique",
            "D0.finite_power_readout_no_alternative",
        ],
        ["two-channel-only", "whatever response was supplied"],
    ),
    (
        "Book 02 proof spine owns Born 2.0",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "Finite Born 2.0 uniqueness",
            "D0.finite_effect_born_readout_unique",
            "D0.finite_effect_born_no_hidden_response",
            "D0.finite_tensor_born_readout_unique",
            "D0.finite_power_readout_no_alternative",
        ],
        [],
    ),
    (
        "Book 04 uses effect-frame readout for matter",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "Finite Born 2.0 in matter language",
            "finite detector/support atoms S",
            "D0.finite_effect_born_readout_unique",
            "D0.finite_power_readout_no_alternative",
            "not a second D0 law",
        ],
        ["full continuum Born rule for arbitrary Hilbert-space effects; that is a v14 target"],
    ),
    (
        "Book 05 integrated contract records Born finite-effect owners",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "## 05.13 Current v14 priority gates",
            "D0.Core.BornFiniteEffects",
            "finite_effect_born_readout_unique",
            "finite_tensor_born_readout_unique",
            "finite_power_readout_no_alternative",
        ],
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

# Ensure no accidental form-feed from non-raw LaTeX strings.
for book in BOOKS.glob("BOOK_*.md"):
    if "\f" in book.read_text(encoding="utf-8"):
        errors.append(f"{book.name}: contains form-feed character, likely broken \\frac")

if errors:
    print("FAIL_V14_BORN2_SYNC")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("PASS_V14_BORN2_SYNC")
