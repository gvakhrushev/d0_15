#!/usr/bin/env python3
"""check_book_assembly.py - CI guard for the per-section book infrastructure (BR1).

Fails if:
  - any committed 01_BOOKS/BOOK_0X.md differs from a fresh assembly of its
    01_BOOKS/<book>/ section files (idempotence — the book is a generated view,
    never hand-edited; edit the section files instead);
  - a book has section files but no generated book, or a generated book has no
    section dir (orphan);
  - section filenames are malformed or their sequence has gaps/duplicates
    (would scramble document order on assembly).

Mirrors regen_graph.ps1 --check-only / generate_lean_aggregates.py --check: the
source (section files) and the generated view (book) are kept provably in sync.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import assemble_books as ab  # noqa: E402

NAME_RE = re.compile(r"^(\d{4})__([0-9A-Za-z.]+|NOID|FRONT)__[a-z0-9-]+\.md$")


def main() -> int:
    problems: list[str] = []
    dirs = {d.name: d for d in BOOKS.glob("BOOK_0*") if d.is_dir()}
    books = {p.stem: p for p in BOOKS.glob("BOOK_0*.md") if p.is_file()}

    # orphans both ways
    for stem in books:
        if stem not in dirs:
            problems.append(f"{stem}.md has no per-section dir 01_BOOKS/{stem}/")
    for stem in dirs:
        if stem not in books:
            problems.append(f"01_BOOKS/{stem}/ has no generated {stem}.md")

    n_sections = 0
    for stem, d in sorted(dirs.items()):
        files = sorted(d.glob("*.md"))
        n_sections += len(files)
        if not files:
            problems.append(f"01_BOOKS/{stem}/ is empty")
            continue
        # filename well-formedness + contiguous sequence
        seqs = []
        for f in files:
            m = NAME_RE.match(f.name)
            if not m:
                problems.append(f"malformed section filename: {stem}/{f.name}")
                continue
            seqs.append(int(m.group(1)))
        if seqs:
            expected = list(range(len(seqs)))
            if sorted(seqs) != expected:
                problems.append(f"{stem}: section seq not contiguous 0..{len(seqs)-1} "
                                f"(got {sorted(seqs)[:5]}…)")
        # idempotence: committed book == fresh assembly
        if stem in books:
            fresh = ab.assemble(d)
            committed = books[stem].read_text(encoding="utf-8")
            if fresh != committed:
                problems.append(f"{stem}.md is STALE vs its section files "
                                f"(run: python tools/assemble_books.py)")

    if problems:
        print(f"RESULT: FAIL — {len(problems)} problem(s)")
        for p in problems:
            print("  - " + p)
        return 1
    print(f"RESULT: PASS — {len(dirs)} books, {n_sections} section files, all assemblies idempotent")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
