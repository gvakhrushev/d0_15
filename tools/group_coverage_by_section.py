#!/usr/bin/env python3
"""group_coverage_by_section.py - turn the BR0 ledger into a per-book rewrite
worklist for the BR3/BR4 wave: group the `integrate` rows by the section FILE that
should receive them, and enrich each row with its GOLDEN/v17 SOURCE location (file
+ line range from the chunk manifest) so a rewrite agent can read the original
forcing argument, not just the one-line concept.

Resolution of the audit's target_section (best-effort; the per-book planner refines
the leftovers):
  - strip the leading "BOOK_0X." and a possible doubled "0X." -> a section-id candidate
  - match against the book's actual section ids (exact, then "0X.<cand>", then prefix)
  - conceptual targets with no matching section (e.g. "complexity", "spine",
    "icosian-E8") -> the `unassigned` bucket (new sections / planner decides a home)

Usage: python tools/group_coverage_by_section.py --book BOOK_02_MATHEMATICAL... [--all-strengths]
Writes 03_THEORY_MAP/coverage_audit/worklist_<book>.json and prints a summary.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "01_BOOKS"
AUD = ROOT / "03_THEORY_MAP" / "coverage_audit"
LEDGER = ROOT / "03_THEORY_MAP" / "GOLDEN_COVERAGE_LEDGER.csv"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chunk_sources as cs  # noqa: E402  (reuse the exact slug() the chunker used)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def source_path_map() -> dict[str, str]:
    """book-slug -> repo-relative source file path (reverse of the chunker's slug)."""
    m = {}
    for d in (cs.GOLDEN_DIR, cs.V17_DIR, cs.TRANSFER_DIR):
        if not d.exists():
            continue
        for p in d.glob("*"):
            if p.is_file() and p.suffix in (".txt", ".md"):
                m[cs.slug(p.name)] = p.relative_to(ROOT).as_posix()
    return m


def book_number(stem: str) -> str:
    m = re.search(r"BOOK_(\d+)", stem)
    return m.group(1) if m else ""


def section_index(stem: str) -> dict[str, str]:
    """section-id -> section filename for the book's per-section dir."""
    idx = {}
    d = BOOKS / stem
    for f in sorted(d.glob("*.md")):
        m = re.match(r"\d{4}__([^_]+(?:_[^_]+)*?)__", f.name)
        # id is the middle field between the seq and the slug (split on '__')
        parts = f.name.split("__")
        if len(parts) >= 3:
            idx[parts[1]] = f.name
    return idx


def resolve_section(target: str, num: str, idx: dict[str, str]) -> str | None:
    if not target:
        return None
    t = target.strip()
    t = re.sub(rf"^BOOK_{num}\.", "", t)        # strip BOOK_0X.
    t = re.sub(rf"^{num}\.", "", t)             # strip a doubled 0X.
    nlead = num.lstrip("0") or "0"
    cands = [t, f"{num}.{t}"]
    # normalize an unpadded leading book number: "2.5" -> "02.5"
    if re.match(rf"^{nlead}\.", t):
        cands.append(num + t[len(nlead):])
    # strip a trailing capital-letter subsection suffix: "7A" -> "7", "02.19B" -> "02.19"
    base = re.sub(r"[A-Z]$", "", t)
    if base != t:
        cands += [base, f"{num}.{base}"]
    for c in cands:
        if c in idx:
            return idx[c]
    # prefix match (e.g. cand "5" but section id is "02.5.1"; or base "02.7" for "02.7A")
    for c in cands:
        for sid, fn in idx.items():
            if sid == c or sid.startswith(c + ".") or sid.startswith(f"{num}.{c}."):
                return fn
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, help="book stem, e.g. BOOK_02_MATHEMATICAL...")
    ap.add_argument("--all-strengths", action="store_true",
                    help="include supporting/peripheral integrate rows (default: core-forcing only)")
    args = ap.parse_args()

    stem = args.book
    if not (BOOKS / stem).is_dir():
        cands = [d.name for d in BOOKS.glob(f"{stem}*") if d.is_dir()]
        if len(cands) == 1:
            stem = cands[0]
        else:
            print(f"ambiguous/unknown book '{args.book}': {cands}")
            return 2
    num = book_number(stem)
    idx = section_index(stem)

    manifest = {c["chunk_id"]: c for c in
                json.loads((AUD / "chunk_manifest.json").read_text(encoding="utf-8"))["chunks"]}
    pathmap = source_path_map()
    SRC = {"golden": "add/d0-main/books", "v17": "_QUARANTINE/v17_overshoots/01_BOOKS",
           "transfer": "add/files"}

    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
    want = [r for r in rows if r["verdict"] == "integrate"
            and r["target_section"].startswith(f"BOOK_{num}")
            and (args.all_strengths or r["strength"] == "core-forcing")]

    sections: dict[str, list] = {}
    unassigned: list = []
    for r in want:
        m = manifest.get(r["chunk_id"], {})
        layer = r["chunk_id"].split("-")[0]
        enriched = {
            "chunk_id": r["chunk_id"], "concept": r["concept"], "kind": r["kind"],
            "strength": r["strength"], "present_in_v14": r["present_in_v14"],
            "v14_locations": r["v14_locations"], "note": r["note"],
            "target_section": r["target_section"],
            "source_layer": layer,
            "source_path": pathmap.get(m.get("book", ""), ""),
            "source_lines": f"{m.get('line_start','?')}-{m.get('line_end','?')}",
            "source_book": m.get("book", ""),
        }
        fn = resolve_section(r["target_section"], num, idx)
        if fn:
            sections.setdefault(fn, []).append(enriched)
        else:
            unassigned.append(enriched)

    out = {
        "book": stem, "book_number": num,
        "n_integrate": len(want),
        "n_assigned": sum(len(v) for v in sections.values()),
        "n_unassigned": len(unassigned),
        "source_dirs": SRC,
        "sections": sections,
        "unassigned": unassigned,
    }
    outpath = AUD / f"worklist_{stem}.json"
    outpath.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print(f"{stem}: {len(want)} integrate rows -> {len(sections)} sections assigned "
          f"({out['n_assigned']}), {len(unassigned)} unassigned (conceptual/new)")
    for fn in sorted(sections):
        print(f"  {fn}: {len(sections[fn])}")
    if unassigned:
        from collections import Counter
        print("  unassigned target_sections:",
              dict(Counter(r["target_section"] for r in unassigned)))
    print(f"wrote {outpath.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
