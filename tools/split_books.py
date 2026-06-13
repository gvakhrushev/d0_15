#!/usr/bin/env python3
"""split_books.py - one-time (idempotent) BR1 migration: split each monolithic
01_BOOKS/BOOK_0X_*.md into per-section source files so agents can rewrite sections
in parallel with zero merge conflicts (the same property the per-claim Lean modules
get). The book itself becomes a GENERATED view (tools/assemble_books.py).

Split unit = level-2 heading (`## NN.M ...`). Everything before the first `## `
(the `# ` title + intro) becomes the FRONT section. The slice is byte-lossless:
concatenating all section files in filename order reproduces the original prose
exactly (verified by tools/check_book_assembly.py / assemble_books.py --check).

Section files:  01_BOOKS/<book-basename>/<seq>__<sectionid>__<slug>.md
  seq        zero-padded document order (so lexical sort == reading order)
  sectionid  parsed from the heading (e.g. 01.4a, 01.v15, 00.x) or NOID
  slug       kebab of the heading text

Idempotent: re-running clears and rewrites the per-book dir from the current book.
After splitting, run assemble_books.py to (re)generate the BOOK_0X.md view.
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

SECTION_RE = re.compile(r"(?m)^## ")
# parse a leading section id like 01.4a / 01.v15 / 00.x / 2.5.1 after the '## '
ID_RE = re.compile(r"^##\s+([0-9]+(?:\.[0-9A-Za-z]+)+|[0-9]+)\b")


def book_files() -> list[Path]:
    # the monolithic books only (skip per-section dirs)
    return sorted(p for p in BOOKS.glob("BOOK_0*.md") if p.is_file())


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[`*_$\\{}()\[\]]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:48] or "section"


def heading_id_slug(first_line: str) -> tuple[str, str]:
    m = ID_RE.match(first_line)
    sid = m.group(1) if m else "NOID"
    rest = first_line[2:].strip()
    if m:
        rest = rest[len(m.group(1)):].strip()
    return sid, slugify(rest)


def split_one(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    bounds = [m.start() for m in SECTION_RE.finditer(text)]
    out_dir = BOOKS / path.stem
    # clear existing section files (idempotent rewrite)
    if out_dir.exists():
        for f in out_dir.glob("*.md"):
            f.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)

    segments: list[tuple[str, str, str]] = []  # (sectionid, slug, body)
    front_end = bounds[0] if bounds else len(text)
    front = text[:front_end]
    if front:
        segments.append(("FRONT", slugify(path.stem.replace("BOOK_", "book-")), front))
    for i, b in enumerate(bounds):
        end = bounds[i + 1] if i + 1 < len(bounds) else len(text)
        body = text[b:end]
        first_line = body.splitlines()[0] if body else ""
        sid, slug = heading_id_slug(first_line)
        segments.append((sid, slug, body))

    for seq, (sid, slug, body) in enumerate(segments):
        name = f"{seq:04d}__{sid}__{slug}.md"
        (out_dir / name).write_text(body, encoding="utf-8", newline="\n")

    # losslessness self-check: concat(section files in order) == original
    rebuilt = "".join(
        (out_dir / f"{seq:04d}__{sid}__{slug}.md").read_text(encoding="utf-8")
        for seq, (sid, slug, _) in enumerate(segments)
    )
    if rebuilt != text:
        raise SystemExit(f"LOSSY SPLIT for {path.name}: rebuilt != original")
    return len(segments)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", help="split only this book file basename (default: all)")
    args = ap.parse_args()
    files = book_files()
    if args.book:
        files = [p for p in files if p.name == args.book or p.stem == args.book]
        if not files:
            print(f"no such book: {args.book}")
            return 2
    total = 0
    for p in files:
        n = split_one(p)
        total += n
        print(f"{p.name}: {n} sections -> 01_BOOKS/{p.stem}/")
    print(f"split {len(files)} books into {total} section files (lossless)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
