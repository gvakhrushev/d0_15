#!/usr/bin/env python3
"""v14 guard: active books must be theorem-first, not historical layer stacking."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"

ERRORS: list[str] = []

OLD_BOOK04 = BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_PARTICLE_PASSPORTS.md"
NEW_BOOK04 = BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md"
BOOK05 = BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md"

if OLD_BOOK04.exists():
    ERRORS.append("old Book 04 particle-passport file is still active")
if not NEW_BOOK04.exists():
    ERRORS.append("new finite-selector Book 04 file is missing")

FORBIDDEN = [
    re.compile(r"\bRecovered\b"),
    re.compile(r"\bpre-refactor\b", re.I),
    re.compile(r"current archive generation", re.I),
    re.compile(r"current Lean generation", re.I),
    re.compile(r"particle passports", re.I),
    re.compile(r"Spin/flavour/decuplet transfer closure", re.I),
    re.compile(r"CHIRAL-VECTOR-OPERATOR-CLOSED / NUMERICAL-PASSPORT-NOT-PROMOTED", re.I),
    re.compile(r"\b400\s*->\s*(pion|mass)", re.I),
]

VERSION_LOG = re.compile(r"\bv\d{2}\.\d+\b", re.I)
CORRUPT_LATEX = ["N\text", "N\text", "N\text", "T_\rho".replace("\\", ""), "arphi", "M_\rho".replace("\\", "")]

for path in sorted(BOOKS.glob("BOOK_*.md")):
    text = path.read_text(encoding="utf-8")
    for rx in FORBIDDEN:
        if rx.search(text):
            ERRORS.append(f"{path.name}: forbidden stale wording matched {rx.pattern!r}")
    if VERSION_LOG.search(text):
        ERRORS.append(f"{path.name}: version-log token found; active books must not be release history")
    if text.count("```") % 2 != 0:
        ERRORS.append(f"{path.name}: unbalanced fenced code/math blocks")

# Book 04 must be a replacement, not an appended patch stack.
if NEW_BOOK04.exists():
    text = NEW_BOOK04.read_text(encoding="utf-8")
    required = [
        "## 04.3 Matter objects are selectors, not passports",
        "## 04.4 Matter as defects and gap-labeled spectra over the φ-quasicrystalline hull",
        "## 04.10 CKM as finite basis origin, not a free matrix",
        "## 04.14 Baryon multiplet boundary as a closed no-go",
        "## 04.15 Meson/chiral boundary as a closed no-go",
        "## 04.22 Remaining matter operator frontiers",
        "## 04.V Nuclear shell-contact SRC operator",
        "nucleon_line_cannot_promote_full_baryon_multiplet",
        "400\\not\\Rightarrow m_\\pi",
    ]
    for needle in required:
        if needle not in text:
            ERRORS.append(f"{NEW_BOOK04.name}: missing v14 replacement text: {needle}")
    if len(re.findall(r"^## ", text, flags=re.M)) > 28:
        ERRORS.append(f"{NEW_BOOK04.name}: too many top-level sections; likely accumulated patch stack")

# Book 05 must be integrated: not tiny, not a preservation appendix dump.
if BOOK05.exists():
    text = BOOK05.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 380:
        ERRORS.append(f"{BOOK05.name}: too short for integrated verification contract ({len(lines)} lines)")
    if len(lines) > 720:
        ERRORS.append(f"{BOOK05.name}: too long for integrated verification contract ({len(lines)} lines)")
    for forbidden_fragment in ["## 05.A Preserved verification corpus", "BOOK_05_v13_RAW_PRESERVED", "RAW_PRESERVED", "raw-copy", "raw copy"]:
        if forbidden_fragment in text:
            ERRORS.append(f"{BOOK05.name}: active Book 05 contains preservation-dump marker: {forbidden_fragment}")
    required = [
        "theory first;",
        "proof owner second;",
        "ledger/status last.",
        "## 05.3 Standard-language audit rule",
        "## 05.12 Theory-improvement gate",
        "## 05.13 Active priority gates",
        "## 05.18 Bridge proof-cell rule",
        "## 05.24 Editorial rule for this book",
    ]
    for needle in required:
        if needle not in text:
            ERRORS.append(f"{BOOK05.name}: missing integrated verification contract text: {needle}")

# Duplicate numeric headings are usually a sign of appended logs.
heading_re = re.compile(r"^## (\d{2}\.\d+)(?:\s|$)", re.M)
for path in sorted(BOOKS.glob("BOOK_*.md")):
    text = path.read_text(encoding="utf-8")
    seen: set[str] = set()
    for h in heading_re.findall(text):
        if h in seen:
            ERRORS.append(f"{path.name}: duplicate heading number {h}")
        seen.add(h)

if ERRORS:
    print("FAIL_V14_CLEAN_CORPUS")
    for e in ERRORS:
        print("  -", e)
    sys.exit(1)
print("PASS_V14_CLEAN_CORPUS")
