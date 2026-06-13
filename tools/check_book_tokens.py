#!/usr/bin/env python3
"""check_book_tokens.py - BR2 hygiene guard for the book prose (01_BOOKS).

Two token sets:

  FORBIDDEN (exit 1 if any appear) - the contamination the refactor must never let
  back in. Currently zero in v14; this guard is PREVENTIVE, because BR3 integrates
  content from v17 (`_QUARANTINE/v17_overshoots/`) where the three overshoots live,
  and from GOLDEN. It is the firewall that keeps the v17 overshoots + the deprecated
  delta0 form out of the generated books:
    - Immutable / Grand Singularity Lock status language (v17 overshoot #1)
    - Golod-Shafarevich as a core Lambda driver (v17 overshoot #2)
    - fabricated "OpenAI 2026" citation (v17 overshoot #3)
    - deprecated delta0 = phi^-3  (canonical is delta0 = (sqrt5-2)/2 = 1/(2 phi^3))

  STALE (reported, not yet failing) - pre-existing cruft the rewrite wave drives to
  zero: dangling "(marker moved to 06_AUDIT/...)" refs (06_AUDIT was deleted) and the
  "v16 publication-proofread draft" version boilerplate. Promote into FORBIDDEN once
  the books are clean (set --strict-stale to gate now).

Scans the GENERATED books 01_BOOKS/BOOK_0X.md (what a reader sees).
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FORBIDDEN = {
    "immutable-status": re.compile(r"\bImmutable\b", re.I),
    "grand-singularity-lock": re.compile(r"Grand[\s-]*Singularity", re.I),
    "golod-shafarevich": re.compile(r"Golod", re.I),
    "openai-2026-citation": re.compile(r"OpenAI", re.I),
    "deprecated-delta0-phi3": re.compile(r"(?:δ0|δ₀|delta0)\s*=\s*[φϕ]\s*\^?\s*-?\s*3\b"),
}
STALE = {
    "marker-moved-06audit": re.compile(r"\(marker moved"),
    "v16-proofread-boilerplate": re.compile(r"v16 publication-proofread", re.I),
    "dangling-06audit-ref": re.compile(r"06_AUDIT/"),
}


def scan(patterns: dict) -> dict[str, list[tuple[str, int]]]:
    hits: dict[str, list[tuple[str, int]]] = {k: [] for k in patterns}
    for book in sorted(BOOKS.glob("BOOK_0*.md")):
        for i, line in enumerate(book.read_text(encoding="utf-8").splitlines(), 1):
            for name, rx in patterns.items():
                if rx.search(line):
                    hits[name].append((book.name, i))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-stale", action="store_true",
                    help="also fail on STALE tokens (use once the rewrite wave is done)")
    args = ap.parse_args()

    forb = scan(FORBIDDEN)
    stale = scan(STALE)
    n_forb = sum(len(v) for v in forb.values())
    n_stale = sum(len(v) for v in stale.values())

    print(f"FORBIDDEN tokens: {n_forb}")
    for name, occ in forb.items():
        if occ:
            print(f"  ✗ {name}: {len(occ)}  e.g. {occ[0][0]}:{occ[0][1]}")
    print(f"STALE tokens (cleanup worklist): {n_stale}")
    for name, occ in stale.items():
        if occ:
            print(f"  · {name}: {len(occ)}  e.g. {occ[0][0]}:{occ[0][1]}")

    fail = n_forb > 0 or (args.strict_stale and n_stale > 0)
    if fail:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS" + (f" (forbidden clean; {n_stale} stale still to retire)" if n_stale else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
