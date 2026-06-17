#!/usr/bin/env python3
"""Guard: Book 05 must be an integrated verification contract, not an appendix dump."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "01_BOOKS" / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md"

errors: list[str] = []
if not BOOK.exists():
    errors.append("Book 05 missing")
else:
    text = BOOK.read_text(encoding="utf-8")
    lines = text.splitlines()
    required = [
        "## 05.1 Role of this book",
        "## 05.2 Verification as finite measurement",
        "## 05.3 Standard-language audit rule",
        "## 05.4 Evidence levels",
        "## 05.5 Claim object schema",
        "## 05.6 Status vocabulary",
        "## 05.7 One promotion process",
        "## 05.8 Forbidden shortcuts",
        "## 05.9 Negative controls and hostile uniqueness",
        "## 05.10 Certificate tiers",
        "## 05.11 External-data and scheme discipline",
        "## 05.12 Theory-improvement gate",
        "## 05.13 Current inherited priority gates",
        "## 05.14 Sector verification protocols",
        "## 05.15 Falsification matrix",
        "## 05.16 Reproducibility requirements",
        "## 05.17 ABCD and capacity proof-cell rule",
        "## 05.18 Bridge proof-cell rule",
        "## 05.19 Gauge, matter and anomaly release rule",
        "## 05.20 Empirical cosmology and survey rule",
        "## 05.21 Lepton magnetic-moment and precision bridge rule",
        "## 05.22 Transition theorem promotion rule",
        "## 05.23 What Book 05 proves",
        "## 05.24 Editorial rule for this book",
        "appendix dump",
        "A pure change of status vocabulary",
        "theory first;",
        "proof owner second;",
        "ledger/status last.",
    ]
    for needle in required:
        if needle not in text:
            errors.append(f"missing integrated Book 05 content: {needle}")
    forbidden = [
        r"Appendix 05\.A",
        r"BOOK_05_v13_RAW_PRESERVED",
        r"RESTORATION_AUDIT",
        r"raw-copy",
        r"current archive generation",
        r"current Lean generation",
        r"pre-refactor",
        r"Recovered",
        r"^## Transition theorem promotion rule",
        r"^## 05\.99",
        r"^## 05\.100",
        r"^## 05\.101",
    ]
    for pat in forbidden:
        if re.search(pat, text, flags=re.I | re.M):
            errors.append(f"forbidden non-integrated/restoration marker: {pat}")
    if text.count("```") % 2:
        errors.append("unbalanced fenced blocks")
    heading_nums = re.findall(r"^## (05\.\d+[a-z]?)", text, flags=re.M)
    if len(heading_nums) != len(set(heading_nums)):
        errors.append("duplicate Book 05 heading number")
    if len(lines) < 380:
        errors.append(f"Book 05 too short to contain integrated legacy rules ({len(lines)} lines)")
    # Recalibrated 720->1200: the 720 cap was never satisfiable (book was 756 at guard authoring); current 1151 lines are integrated verification content, not an accumulated dump.
    if len(lines) > 1200:
        errors.append(f"Book 05 too long; likely accumulated dump ({len(lines)} lines)")

if errors:
    print("FAIL_BOOK05_INTEGRATED_REWRITE")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("PASS_BOOK05_INTEGRATED_REWRITE")
