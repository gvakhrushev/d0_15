#!/usr/bin/env python3
"""extract_apparatus.py - move the regular trace-metadata tags out of book prose
into a per-book apparatus/endnotes section, so the published book reads as a
monograph while traceability is preserved as numbered endnotes.

Handles the two HIGH-VOLUME, REGULAR tags deterministically and safely (no nested
parentheses, line-anchored):
  - forcing provenance:  `(forcing: GOLDEN THE x.y)` / `(... ; forcing: ...)`  (~383)
  - open-obligation:     `Status: PROOF-TARGET (cert obligation open)` and its
                         parenthetical variants                                 (~88)

Each hit is replaced in place by a markdown footnote ref `[^b<NN>-<K>]` and its text
collected; `assemble_books.py` then renders the collected `[^id]: ...` lines as a
`## Apparatus — sources & open obligations` block at the end of the generated book.

The irregular, judgement tags (inline `vp_*.py` / `D0.Mod` / claim-ids in sentence
text, dangling `§`, dev narration) are left for the section rewrite pass — this tool
only does the safe bulk extraction.

Idempotent: a re-run finds no remaining `(forcing: …)` / `Status: PROOF-TARGET …`
(they are already footnote refs) and changes nothing. `--check` verifies that.
Footnote definitions are written into a generated `_apparatus.json` per book dir
(consumed by assemble_books.py), NOT into the section sources, so section files stay
prose-only.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FORCING = re.compile(r"\((?:[^()]*?;\s*)?forcing:[^()]*\)")
STATUS = re.compile(r"Status:\s*PROOF-TARGET\s*\([^()]*\)")
SECTION_FILE = re.compile(r"^\d{4}__")


def book_num(stem: str) -> str:
    m = re.search(r"BOOK_(\d+)", stem)
    return m.group(1) if m else "00"


def extract_one(stem_dir: Path) -> tuple[int, dict]:
    num = book_num(stem_dir.name)
    notes: dict[str, str] = {}
    k = 0
    changed = 0
    for f in sorted(stem_dir.glob("*.md")):
        if not SECTION_FILE.match(f.name) or "apparatus" in f.name:
            continue
        text = f.read_text(encoding="utf-8")
        out = []
        pos = 0

        def repl(m: re.Match) -> str:
            nonlocal k
            k += 1
            rid = f"b{num}-{k}"
            raw = m.group(0)
            # normalize the note text for the apparatus
            if raw.startswith("Status:"):
                inner = raw[raw.find("(") + 1:raw.rfind(")")]
                notes[rid] = f"open obligation — {inner.strip()}"
            else:
                inner = raw[1:-1].strip()  # drop the surrounding ()
                notes[rid] = inner
            return f"[^{rid}]"

        new = STATUS.sub(repl, text)
        new = FORCING.sub(repl, new)
        if new != text:
            f.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
    # persist the apparatus map for assemble_books.py
    apx = stem_dir / "_apparatus.json"
    if notes:
        apx.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    elif apx.exists() and k == 0:
        pass  # keep an existing apparatus map on an idempotent re-run
    return changed, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", help="book stem (default: all)")
    ap.add_argument("--check", action="store_true", help="fail if any regular tag remains in prose")
    args = ap.parse_args()
    dirs = sorted(d for d in BOOKS.glob("BOOK_0*") if d.is_dir())
    if args.book:
        dirs = [d for d in dirs if d.name == args.book or d.name.startswith(args.book)]

    if args.check:
        bad = []
        for d in dirs:
            for f in sorted(d.glob("*.md")):
                if not SECTION_FILE.match(f.name) or "apparatus" in f.name:
                    continue
                t = f.read_text(encoding="utf-8")
                if FORCING.search(t) or STATUS.search(t):
                    bad.append(f.relative_to(BOOKS).as_posix())
        if bad:
            print(f"RESULT: FAIL — {len(bad)} section(s) still carry raw forcing/Status tags:")
            for b in bad[:20]:
                print("  - " + b)
            return 1
        print("RESULT: PASS — no raw forcing/Status tags in prose (all in apparatus)")
        return 0

    total_notes = 0
    for d in dirs:
        changed, notes = extract_one(d)
        total_notes += len(notes)
        print(f"{d.name}: {len(notes)} tags -> apparatus, {changed} section files edited")
    print(f"extracted {total_notes} apparatus notes across {len(dirs)} books")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
