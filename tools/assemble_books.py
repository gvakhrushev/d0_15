#!/usr/bin/env python3
"""assemble_books.py - regenerate each 01_BOOKS/BOOK_0X_*.md from its per-section
source files (01_BOOKS/<book>/<seq>__<id>__<slug>.md), so the monolithic book is a
GENERATED view and the per-section files are the source of truth (mirrors the Lean
All.lean = generated, per-claim modules = source split).

The book = a deterministic banner line + the section files concatenated in filename
(== document) order. Byte-lossless apart from the banner: stripping the banner
recovers the exact pre-split prose, and re-assembling is idempotent (the property
check_book_assembly.py / --check enforces, like regen_graph --check-only).

Status-table injection (claim_id | Lean | cert | release | points) is intentionally
NOT done here yet: BR1 is a pure lossless restructure. It is added once a normalized
book_section ownership column exists (BR2/BR3), behind an opt-in flag, so the
round-trip stays verifiable in the meantime.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"


def banner(stem: str) -> str:
    return (f"<!-- AUTO-ASSEMBLED from 01_BOOKS/{stem}/ by tools/assemble_books.py — "
            f"edit the per-section files, never this generated book. -->\n")


def section_dirs() -> list[Path]:
    return sorted(d for d in BOOKS.glob("BOOK_0*") if d.is_dir())


def apparatus_block(stem_dir: Path) -> str:
    """Render the per-book apparatus (footnote definitions) collected by
    tools/extract_apparatus.py into `_apparatus.json`, as a trailing endnotes section."""
    apx = stem_dir / "_apparatus.json"
    if not apx.exists():
        return ""
    notes = json.loads(apx.read_text(encoding="utf-8"))
    if not notes:
        return ""
    out = ["\n\n## Apparatus — sources & open obligations\n",
           "_Traceability for the integrated forcing arguments and the open proof obligations. "
           "The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance "
           "and cert/Lean status so nothing is lost._\n"]
    for rid, txt in notes.items():
        out.append(f"[^{rid}]: {txt}")
    return "\n".join(out) + "\n"


def assemble(stem_dir: Path) -> str:
    parts = []
    for f in sorted(stem_dir.glob("*.md")):
        parts.append(f.read_text(encoding="utf-8"))
    return banner(stem_dir.name) + "".join(parts) + apparatus_block(stem_dir)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail if any committed BOOK_0X.md differs from a fresh assembly")
    ap.add_argument("--book", help="only this book stem (e.g. BOOK_01_CONDENSED...)")
    args = ap.parse_args()

    dirs = section_dirs()
    if args.book:
        dirs = [d for d in dirs if d.name == args.book]
    if not dirs:
        print("no per-section book dirs found (run tools/split_books.py first)")
        return 0 if args.check else 2

    stale = []
    for d in dirs:
        new = assemble(d)
        book = BOOKS / f"{d.name}.md"
        old = book.read_text(encoding="utf-8") if book.exists() else None
        if args.check:
            if old != new:
                stale.append(book.name)
        else:
            # py3.9-compatible (Path.write_text gained newline= only in 3.10)
            with book.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(new)
            print(f"assembled {book.name} ({len(list(d.glob('*.md')))} sections)")

    if args.check:
        if stale:
            print("STALE (run assemble_books.py): " + ", ".join(stale))
            print("RESULT: FAIL")
            return 1
        print(f"RESULT: PASS (all {len(dirs)} books idempotent)")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
