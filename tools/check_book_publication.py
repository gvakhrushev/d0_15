#!/usr/bin/env python3
"""check_book_publication.py - CI guard: the BODY of each book reads as a publishable
monograph. Trace metadata is allowed ONLY in the trailing `## Apparatus — sources …`
endnotes block (produced by extract_apparatus.py); the body must be clean.

Fails (in the body, i.e. before the Apparatus heading) on:
  - dangling section refs: `§` not followed by a number (`BOOK_01 §,` / `owned … §`)
  - duplicate `## NN.X` heading numbers (appended-stub / register-stub artifact)
  - claim-ids in headings (`### NN.M … D0-XXX-001 …`)
  - developer `# …` notes (fence/math-aware: not inside ``` and not `\#`)
  - inline repo tokens in prose: `vp_*.py`, `05_CERTS/…`, `D0.<Module>.<member>`

Scans the GENERATED 01_BOOKS/BOOK_0X.md (what a reader sees). Exit 0/1.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

APPARATUS = re.compile(r"^##\s+Apparatus\b", re.M)
DANGLING = re.compile(r"§\s*(?=[,.)]|$)", re.M)        # empty § ref (followed by punctuation/EOL),
#   not `§01.6` (number), `§V` (roman section) or `§§` (plural "sections")
HEADING = re.compile(r"^#{2,4}\s+(\d+\.[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)(?=\s|$)", re.M)
CLAIMID_HEAD = re.compile(r"^#{2,4}\s+.*\bD0-[A-Z0-9]+-[A-Z0-9]", re.M)
DEV = re.compile(r"(?<![\\#])\S[ \t]+#[ \t]+\S")
INLINE_REF = re.compile(r"vp_\w+\.py|05_CERTS/|\bD0\.[A-Z]\w+\.[a-z]\w+")


def body_of(text: str) -> str:
    m = APPARATUS.search(text)
    return text[:m.start()] if m else text


def main() -> int:
    problems: list[str] = []
    for book in sorted(BOOKS.glob("BOOK_0*.md")):
        body = body_of(book.read_text(encoding="utf-8"))
        name = book.name

        for m in DANGLING.finditer(body):
            ctx = body[max(0, m.start() - 30):m.start() + 2].replace("\n", " ")
            problems.append(f"{name}: dangling § — …{ctx}")

        seen: set[str] = set()
        for h in HEADING.findall(body):
            if h in seen:
                problems.append(f"{name}: duplicate heading number {h}")
            seen.add(h)

        for m in CLAIMID_HEAD.finditer(body):
            problems.append(f"{name}: claim-id in heading — {body[m.start():m.start()+60].strip()}")

        in_fence = False
        for i, ln in enumerate(body.splitlines(), 1):
            st = ln.lstrip()
            if st.startswith("```"):
                in_fence = not in_fence
                continue
            # Skip code fences, headings, and STRUCTURED registers (markdown table rows
            # `| … |` — claim-coverage / certificate ledgers are allowed reference, not prose).
            if in_fence or st.startswith("#") or st.startswith("|") or ln.count("|") >= 2:
                continue
            # strip inline-code spans (`D0.X`, `vp_*.py` named as code are reference, not prose drops)
            prose = re.sub(r"`[^`]*`", "", ln)
            if DEV.search(prose):
                problems.append(f"{name}:{i}: dev-comment — {ln.strip()[:60]}")
            for mm in INLINE_REF.finditer(prose):
                problems.append(f"{name}:{i}: inline repo-ref '{mm.group(0)}' in body prose")

    # cap the report so it stays a worklist, not a wall
    if problems:
        from collections import Counter
        kinds = Counter(p.split(": ", 1)[1].split(" —")[0].split(" '")[0][:18] for p in problems)
        print(f"RESULT: FAIL — {len(problems)} publication issue(s); kinds: {dict(kinds)}")
        for p in problems[:40]:
            print("  - " + p)
        if len(problems) > 40:
            print(f"  … +{len(problems) - 40} more")
        return 1
    print("RESULT: PASS — book bodies are publication-clean (trace metadata only in apparatus)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
