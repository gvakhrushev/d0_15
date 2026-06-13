#!/usr/bin/env python3
"""chunk_sources.py - deterministic chunker for the BR0 GOLDEN->v14 coverage audit.

Splits the three source layers into formal-statement chunks so every DEF/THE/LEM
of GOLDEN (and every condensed section of v17 + framing chunk of the transfer docs)
gets an explicit verdict row in GOLDEN_COVERAGE_LEDGER.csv. This is the deterministic
backbone: the chunk list never changes between runs, so the audit is reproducible and
"nothing is missed" is a checkable property (M1-class omissions become impossible).

Layers (co-primary GOLDEN + v17, per the approved plan):
  golden   add/d0-main/books/BOOK_*.txt        - the forcing logic (chunk per [STATUS] marker + heading)
  v17      _QUARANTINE/v17_overshoots/01_BOOKS/ - more idea-rich (chunk per ## / ### section)
  transfer add/files/*.md                       - framing docs (chunk per ## / ### section)

Outputs (under 03_THEORY_MAP/coverage_audit/, a scratch dir):
  chunk_manifest.json   - every chunk: id, layer, book, kind, marker/title, line range, n_chars
  batches/<batch_id>.md - uniform ~N-char batches (never split a chunk) for one agent each
  CHUNK_SUMMARY.md      - per-layer / per-book chunk + batch counts

Deterministic + idempotent: same sources => byte-identical manifest + batches.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "03_THEORY_MAP" / "coverage_audit"
BATCHES = OUT / "batches"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# --- source layers -----------------------------------------------------------
GOLDEN_DIR = ROOT / "add" / "d0-main" / "books"
V17_DIR = ROOT / "_QUARANTINE" / "v17_overshoots" / "01_BOOKS"
TRANSFER_DIR = ROOT / "add" / "files"
# transfer docs that carry conceptual framing (not the iteration report / cert script)
TRANSFER_FILES = [
    "D0_PHILOSOPHY_AND_METHOD.md",
    "D0_THEORY_DOSSIER.md",
    "D0_RESEARCH_ADDENDUM_cosmology_sterile_2D.md",
    "D0_v14_ARCHITECT_PLAN.md",
    "D0_CKM_INTERFACE_ITERATION_REPORT.md",
]

# GOLDEN: a chunk starts at a bracketed formal statement OR a structural heading.
GOLDEN_BRACKET = re.compile(r"^\s*\[(DEF|THE|THM|LEM|COR|PROP|AXM|VER|CHK|APPX|REM|BRIDGE|HYP)\b")
GOLDEN_HEADING = re.compile(r"^(#{1,6} |CHAPTER\s|D0\s§|###\sD0\s§)")
# markdown layers: a chunk starts at any ATX heading.
MD_HEADING = re.compile(r"^#{1,6} ")

KIND_OF_BRACKET = {
    "DEF": "DEF", "THE": "THE", "THM": "THE", "LEM": "LEM", "COR": "COR",
    "PROP": "PROP", "AXM": "AXM", "VER": "VER", "CHK": "CHK",
    "APPX": "APPX", "REM": "REM", "BRIDGE": "BRIDGE", "HYP": "HYP",
}


@dataclass
class Chunk:
    chunk_id: str
    layer: str
    book: str
    kind: str          # DEF/THE/LEM/.../SECTION/FRONT
    marker: str        # the boundary line, trimmed (the concept label seed)
    line_start: int    # 1-based, inclusive
    line_end: int      # 1-based, inclusive
    n_chars: int
    batch_id: str = ""


def slug(name: str) -> str:
    s = re.sub(r"\.(txt|md)$", "", name)
    s = re.sub(r"_GOLDEN_PASS30.*$|_FULL.*$", "", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return s


def boundary_kind(layer: str, line: str) -> str | None:
    """Return the chunk-kind if `line` opens a new chunk, else None."""
    if layer == "golden":
        m = GOLDEN_BRACKET.match(line)
        if m:
            return KIND_OF_BRACKET[m.group(1)]
        if GOLDEN_HEADING.match(line):
            return "SECTION"
        return None
    # markdown layers
    if MD_HEADING.match(line):
        return "SECTION"
    return None


def marker_label(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())[:160]


def chunk_file(path: Path, layer: str, idx_start: int) -> list[Chunk]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    book = slug(path.name)
    chunks: list[Chunk] = []
    # find boundary line indices (0-based)
    bounds: list[tuple[int, str, str]] = []  # (line_idx, kind, marker)
    for i, ln in enumerate(lines):
        k = boundary_kind(layer, ln)
        if k:
            bounds.append((i, k, marker_label(ln)))
    # a leading front-matter chunk if file does not start on a boundary
    if not bounds or bounds[0][0] != 0:
        bounds.insert(0, (0, "FRONT", marker_label(lines[0]) if lines else ""))
    n = idx_start
    for j, (li, kind, marker) in enumerate(bounds):
        end = bounds[j + 1][0] - 1 if j + 1 < len(bounds) else len(lines) - 1
        body = "\n".join(lines[li:end + 1])
        chunks.append(Chunk(
            chunk_id=f"{layer}-{book}-{n:04d}",
            layer=layer, book=book, kind=kind, marker=marker,
            line_start=li + 1, line_end=end + 1, n_chars=len(body),
        ))
        n += 1
    return chunks


def assign_batches(chunks: list[Chunk], batch_chars: int) -> None:
    """Greedily pack consecutive same-file chunks into ~batch_chars batches."""
    bnum = 0
    cur_book = None
    cur_chars = 0
    for c in chunks:
        if c.book != cur_book or cur_chars + c.n_chars > batch_chars:
            bnum += 1
            cur_book = c.book
            cur_chars = 0
        c.batch_id = f"B{bnum:03d}"
        cur_chars += c.n_chars


def write_batches(chunks: list[Chunk], sources: dict[str, Path]) -> None:
    if BATCHES.exists():
        for f in BATCHES.glob("*.md"):
            f.unlink()
    BATCHES.mkdir(parents=True, exist_ok=True)
    by_batch: dict[str, list[Chunk]] = {}
    for c in chunks:
        by_batch.setdefault(c.batch_id, []).append(c)
    for bid, cs in by_batch.items():
        layer = cs[0].layer
        book = cs[0].book
        src = sources[book]
        lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
        out = [f"# BATCH {bid} — layer={layer} book={book}",
               f"_source: {src.relative_to(ROOT).as_posix()}_  ",
               f"_chunks: {len(cs)} ({cs[0].chunk_id} … {cs[-1].chunk_id})_", ""]
        for c in cs:
            body = "\n".join(lines[c.line_start - 1:c.line_end])
            out.append(f"<<<CHUNK {c.chunk_id} kind={c.kind} lines={c.line_start}-{c.line_end}>>>")
            out.append(body)
            out.append(f"<<<END {c.chunk_id}>>>\n")
        (BATCHES / f"{bid}.md").write_text("\n".join(out), encoding="utf-8", newline="\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-chars", type=int, default=18000)
    ap.add_argument("--no-batches", action="store_true", help="manifest + summary only")
    args = ap.parse_args()

    sources: dict[str, Path] = {}
    all_chunks: list[Chunk] = []
    idx = 0

    def take(path: Path, layer: str):
        nonlocal idx
        cs = chunk_file(path, layer, idx)
        for c in cs:
            sources[c.book] = path
        all_chunks.extend(cs)
        idx += len(cs)

    for p in sorted(GOLDEN_DIR.glob("*.txt")):
        take(p, "golden")
    for p in sorted(V17_DIR.glob("*.md")):
        take(p, "v17")
    for name in TRANSFER_FILES:
        p = TRANSFER_DIR / name
        if p.exists():
            take(p, "transfer")

    assign_batches(all_chunks, args.batch_chars)

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "n_chunks": len(all_chunks),
        "n_batches": len({c.batch_id for c in all_chunks}),
        "batch_chars": args.batch_chars,
        "chunks": [asdict(c) for c in all_chunks],
    }
    (OUT / "chunk_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    if not args.no_batches:
        write_batches(all_chunks, sources)

    # summary
    from collections import Counter
    by_layer = Counter(c.layer for c in all_chunks)
    by_kind = Counter(c.kind for c in all_chunks)
    by_book: dict[str, list[int]] = {}
    for c in all_chunks:
        by_book.setdefault(f"{c.layer}/{c.book}", [0, set()])
        by_book[f"{c.layer}/{c.book}"][0] += 1
        by_book[f"{c.layer}/{c.book}"][1].add(c.batch_id)
    lines = ["# Coverage-audit chunk summary", "",
             f"- total chunks: **{len(all_chunks)}**",
             f"- total batches: **{manifest['n_batches']}** (~{args.batch_chars} chars each)",
             f"- by layer: {dict(by_layer)}",
             f"- by kind: {dict(by_kind)}", "",
             "| layer/book | chunks | batches |", "|---|---|---|"]
    for k in sorted(by_book):
        lines.append(f"| {k} | {by_book[k][0]} | {len(by_book[k][1])} |")
    (OUT / "CHUNK_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"chunks={len(all_chunks)} batches={manifest['n_batches']} "
          f"layers={dict(by_layer)} kinds={dict(by_kind)}")
    print(f"wrote {(OUT / 'chunk_manifest.json').relative_to(ROOT).as_posix()}")
    if not args.no_batches:
        print(f"wrote {manifest['n_batches']} batch files to {BATCHES.relative_to(ROOT).as_posix()}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
