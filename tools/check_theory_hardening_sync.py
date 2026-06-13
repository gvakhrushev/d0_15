#!/usr/bin/env python3
"""Check that hardening theorems are synchronized with active books.

This is deliberately not a status renaming check.  It guards against two
failure modes:
1. a formal theorem is added but never becomes part of the theory narrative;
2. a book claims a hardening result whose Lean owner is absent from the final
   index/import spine.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"

checks: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "Final index must be non-vacuous",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        ["structure FinalFoundationIndex", "finalFoundationIndexWitness", "def D0_FINAL_FOUNDATION_INDEX"],
        ["def FinalFoundationIndex : Prop := True", "trivial\n"],
    ),
    (
        "Finite selector must carry finite support",
        LEAN / "Matter" / "FiniteSelector.lean",
        ["support_fintype : Fintype α", "finiteSelectorSupportFintype", "strict_selected_unique"],
        [],
    ),
    (
        "Born finite theorem must be in final index",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        ["finite_born_readout_unique_on_finite_outcomes", "finite_born_no_alternative_readout"],
        [],
    ),
    (
        "CKM no-free theorem must be in final index",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        ["ckm_no_free_matrix_at_fixed_bases"],
        [],
    ),
    (
        "Book 04 selectors must be in final index",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        ["finiteSelectorSupportFintype", "book04_selector_claim_no_free_alternative"],
        [],
    ),
    (
        "Spin-2 and c=1 hardening must be in final index",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        ["finite_spin2_tt_carrier_closed", "finite_causal_tick_section_cone_speed_eq_one"],
        [],
    ),
    (
        "Born hardening must be integrated in Book 01",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        ["D0.finite_effect_born_readout_unique", "D0.finite_effect_born_no_hidden_response"],
        [],
    ),
    (
        "Born hardening must be integrated in Book 02",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        ["D0.finite_effect_born_readout_unique", "D0.finite_effect_born_no_hidden_response"],
        [],
    ),
    (
        "Book 04 must expose selector and CKM theorem owners",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        ["D0.Matter.StrictSelectorCertificate", "D0.Matter.ckm_no_free_matrix_at_fixed_bases", "D0.Matter.book04_selector_claim_no_free_alternative"],
        [],
    ),
    (
        "Book 06 must expose internal cone speed owner",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        ["D0.Bridge.finite_causal_tick_section_cone_speed_eq_one"],
        [],
    ),
    (
        "Book 07 must expose finite spin-2 owner",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        ["D0.Geometry.finite_spin2_tt_carrier_closed"],
        [],
    ),
    (
        "Book 00 must define synchronization as theory test",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        ["Lean/book synchronization is a theory test", "D0.Bridge.D0_FINAL_FOUNDATION_INDEX"],
        [],
    ),
]

failed: list[str] = []
for label, path, required, forbidden in checks:
    if not path.exists():
        failed.append(f"{label}: missing file {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for token in required:
        if token not in text:
            failed.append(f"{label}: required token missing: {token}")
    for token in forbidden:
        if token in text:
            failed.append(f"{label}: forbidden token present: {token!r}")

if failed:
    print("FAIL_THEORY_HARDENING_SYNC")
    for f in failed:
        print("  -", f)
    sys.exit(1)

print("PASS_THEORY_HARDENING_SYNC")
