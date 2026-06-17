#!/usr/bin/env python3
"""Guard that theory hardening is integrated into the books, not just ledgers."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"

REQUIRED = {
    "BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md": [
        "## 00.23 Theory-improvement rule: no decorative layer",
        "A pure change of status vocabulary" if False else "A pure change of status vocabulary",
    ],
    "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md": [
        "### Born readout as finite effect-frame theorem",
        "finite_effect_born_readout_unique",
    ],
    "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md": [
        "## 02.36 Theorem spine for the matter, gauge, gravity and cosmology sectors",
        "ckm_no_free_matrix_at_fixed_bases",
        "finite_spin2_tt_carrier_closed",
    ],
    "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md": [
        "## 03.22 Action-to-selector closure rule",
        "strict selector certificate or normalized response theorem",
    ],
    "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md": [
        "# BOOK 04 — Spectrum, Matter, and Finite Selector Theory",
        "## 04.19 Claim classification for the active matter book",
        "StrictSelectorCertificate",
        "ckm_no_free_matrix_at_fixed_bases",
    ],
    "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md": [
        "# BOOK 05 — Verification, Proof Ownership, and Certificate Discipline",
        "## 05.12 Theory-improvement gate",
        "## 05.3 Standard-language audit rule",
        "## 05.18 Bridge proof-cell rule",
        "A pure change of status vocabulary",
    ],
    "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md": [
        "## 06.35 Internal cone speed and the role of time",
        "internal_cone_speed_eq_one",
    ],
    "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md": [
        "## 07.35 Finite spin-2 derivation theorem",
        "finite_weak_field_quotient_yields_tt_representative",
    ],
    "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md": [
        "# BOOK 08 — Cosmology, Archive, and Observable Transfer",
        "## 08.40 Observable-transfer boundary",
    ],
}

FORBIDDEN_REGEX = [
    re.compile(r"\bRecovered\b"),
    re.compile(r"\bpre-refactor\b", re.I),
    re.compile(r"current archive generation"),
    re.compile(r"current Lean generation"),
    re.compile(r"^# BOOK 04 .*passport", re.I | re.M),
]

# Do not ban status tokens entirely: Book 05 is allowed to discuss claim states.
# This guard only prevents old version-log and passport-title language from re-entering.

def main() -> int:
    errors: list[str] = []
    for name, needles in REQUIRED.items():
        path = BOOKS / name
        if not path.exists():
            errors.append(f"missing book: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{name}: missing required integration text: {needle}")
        for rx in FORBIDDEN_REGEX:
            if rx.search(text):
                errors.append(f"{name}: forbidden stale wording matched {rx.pattern!r}")
    if errors:
        print("FAIL_BOOK_THEORY_REWRITE")
        for e in errors:
            print("  -", e)
        return 1
    print("PASS_BOOK_THEORY_REWRITE")
    return 0

if __name__ == "__main__":
    sys.exit(main())
