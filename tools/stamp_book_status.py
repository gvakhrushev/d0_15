#!/usr/bin/env python3
"""stamp_book_status.py — cascade the canonical ledger status INTO each book section.

This is the generative half of the cascade (the BR2/BR3 step assemble_books.py
defers). For every per-section source that OWNS claims (cites their ids), it
injects/refreshes a machine-generated status block between stable markers:

  <!-- D0-STATUS-STAMP:BEGIN (generated from CLAIM_TO_LEAN_MAP.csv — do not hand-edit) -->
  ...table of claim | release | Lean | cert...
  <!-- D0-STATUS-STAMP:END -->

Because the block is regenerated from the single source of truth, a claim's
status in the books can never drift from the ledger: update the CSV, re-run this,
and every owning section's stamp updates. Status becomes a generated view, exactly
like theory_status_map.csv and theory_graph.json.

The block is placed immediately after the section's H1/H2 title (or at top if none).
Regeneration is idempotent: an existing block between the markers is replaced, so
--check can enforce "no drift" in CI (like regen_graph --check-only).

DEFAULT IS DRY-RUN. Pass --write to modify files, --check to fail on drift.
"""
from __future__ import annotations
import csv, re, sys, glob, os, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
BOOKS = ROOT / "01_BOOKS"
IDPAT = re.compile(r'D0-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d+')
BEGIN = "<!-- D0-STATUS-STAMP:BEGIN (generated from CLAIM_TO_LEAN_MAP.csv — do not hand-edit) -->"
END   = "<!-- D0-STATUS-STAMP:END -->"
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.S)

def load_ledger():
    return {r["claim_id"]: r for r in csv.DictReader(LEDGER.open(encoding="utf-8")) if r.get("claim_id")}

def owned_ids(text, byid):
    # a section OWNS a claim if it cites the id AND the ledger's `section`/`book` doesn't
    # point elsewhere; here we use citation as ownership (matches the graph's convention).
    seen=[]
    for cid in IDPAT.findall(text):
        if cid in byid and cid not in seen: seen.append(cid)
    return seen

def make_block(ids, byid):
    if not ids: return ""
    lines=[BEGIN, "", "| claim | release | Lean | cert |", "|---|---|---|---|"]
    for cid in ids:
        r=byid[cid]
        lean=(r.get("lean_theorem") or "").strip() or "—"
        ls=(r.get("lean_status") or "").strip()
        cert=(r.get("python_cert") or "").strip() or "—"
        lines.append(f"| `{cid}` | {r.get('release_status','')} | `{lean}` ({ls}) | `{cert}` |")
    lines += ["", END, ""]
    return "\n".join(lines)

def insert_after_title(text, block):
    if not block: return text
    # strip any existing block first (idempotent)
    text = BLOCK_RE.sub("", text)
    lines=text.split("\n")
    # find first markdown heading line
    for i,ln in enumerate(lines):
        if ln.lstrip().startswith("#"):
            return "\n".join(lines[:i+1] + ["", block] + lines[i+1:])
    return block + "\n" + text

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--book")
    ap.add_argument("--limit", type=int, default=0)
    a=ap.parse_args()
    byid=load_ledger()
    files=sorted(glob.glob(str(BOOKS/"BOOK_0*"/"*.md")))
    if a.book: files=[f for f in files if a.book in f]
    changed=0; stamped=0; n=0
    for f in files:
        t=Path(f).read_text(encoding="utf-8", errors="replace")
        ids=owned_ids(t, byid)
        if not ids: continue
        new=insert_after_title(t, make_block(ids, byid))
        if new!=t:
            changed+=1; stamped+=len(ids)
            if a.write: Path(f).write_text(new, encoding="utf-8")
            elif not a.check and (a.limit==0 or n<a.limit):
                print(f"--- would stamp {os.path.basename(f)} ({len(ids)} claims) ---")
                blk=make_block(ids,byid)
                print("\n".join(blk.split("\n")[:8]) + ("\n  ..." if len(ids)>3 else "")); n+=1
    mode = "check" if a.check else ("write" if a.write else "dry-run")
    print(f"\nstamp_book_status [{mode}]: {changed} sections would change / {stamped} claim-stamps")
    if a.check and changed: print("FAIL: book status stamps drift from ledger (run --write)"); return 1
    if a.check: print("PASS"); return 0
    return 0

if __name__=="__main__":
    raise SystemExit(main())
