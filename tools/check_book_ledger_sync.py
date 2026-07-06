#!/usr/bin/env python3
"""check_book_ledger_sync.py — cascade guard: books (per-section sources) must not
contradict the canonical claim ledger.

Single source of truth: 09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv.
Books are a generated *view* (tools/assemble_books.py); their per-section sources
(01_BOOKS/<book>/<seq>__<id>__<slug>.md) are prose owners of claims. This guard
joins the two by claim-id citation and fails when prose asserts a *closure tier*
that contradicts the ledger — the structural desync class the corpus accumulates
when the ledger is updated but prose is not.

It is a READ-ONLY guard (like validate_csv.py / check_firewall.py); it never edits.
The closure/open lexicons are disclaimer-aware: a closure word that is negated
("not a closed theorem"), or sits next to a MECH-LIMIT / NO-GO / "named open" /
"missing artifact" marker, is NOT counted as an assertion of closure — otherwise a
scrupulously-hedged section (which the D0 corpus favours) trips false positives.

Run in CI after regen_graph so the whole chain
  CLAIM_TO_LEAN_MAP.csv -> graph/status_map (regen_graph)
                        -> books (assemble_books + stamp_book_status)
                        -> THIS guard (books ⟂ ledger consistent)
is one cascade with no manual sync step.
"""
from __future__ import annotations
import csv, re, sys, os, glob
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
BOOKS = ROOT / "01_BOOKS"

CLOSED = {"CORE-FORMALIZED","CERT-CLOSED","NO_GO_PROVED","PASSPORT-CLOSED","EMPIRICAL-PASSPORT"}
OPEN   = {"PROOF-TARGET","OPEN","DEPRECATED"}
def tier(rs): return "closed" if rs in CLOSED else ("open" if rs in OPEN else "mid")

# --- demoted-row closure-prose check (mechanical batch 2026-07-05) -------------------
# tier() maps CORE_BRIDGE_SPLIT (and NO-GO) to "mid", so the over-claim scan above is
# blind to closure prose written against *demoted/split* rows. This pass closes that
# hole, deliberately conservatively (no false-positive storm): it flags ONLY an exact
# claim_id mention (or an exact lean_theorem-name mention) of a demoted row with
# closure vocabulary within +-DEMOTED_LINES lines, direct negations excluded, same
# allowlist suppression as the over-claim class.
DEMOTED_RS   = {"CORE_BRIDGE_SPLIT"}                      # release-side demotion
DEMOTED_LEAN = {"LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS"}    # lean-side demotion marker
# Release tiers that already disclose the hedge/negative themselves. A lean-demoted row
# sitting on one of these tiers is honestly labeled, and the 2026-07-05 acceptance sweep
# showed prose near such rows trips only benign-attachment hits (closure words belonging
# to ADJACENT CERT-CLOSED claims) — so the lean-side branch skips them. It also skips
# CLOSED tiers (there prose closure agrees with the ledger; ledger-vs-lean inflation is
# vp_status_inflation_audit's jurisdiction, not a book-ledger sync issue).
DEMOTED_LEAN_EXEMPT_RS = CLOSED | {"BRIDGE-ASSUMPTIONS-EXPLICIT","NO-GO","NO_GO_PROVED",
                                   "BRIDGE-CALIBRATION","DEPRECATED"}
DEMOTED_CLOSE_W = re.compile(r'\b(proved|proven|CERT-CLOSED|divergence-free)\b', re.I)
DEMOTED_LINES = 3

def demoted_rows(byid):
    """claim_id -> (row, [exact mention tokens]) for demoted/split ledger rows."""
    out = {}
    for cid, r in byid.items():
        rs = r.get("release_status","").strip()
        if (rs in DEMOTED_RS
                or (r.get("lean_status","").strip() in DEMOTED_LEAN
                    and rs not in DEMOTED_LEAN_EXEMPT_RS)):
            names = []
            for nm in (r.get("lean_theorem","") or "").split(";"):
                nm = nm.strip()
                if not nm: continue
                names.append(nm)
                tail = nm.rsplit(".", 1)[-1]          # prose often cites the bare name
                if tail != nm and len(tail) >= 6: names.append(tail)
            out[cid] = (r, names)
    return out

def scan_demoted(demoted, allow):
    flags = []; seen = set()
    for f in section_files():
        lines = Path(f).read_text(encoding="utf-8", errors="replace").splitlines()
        base = os.path.basename(f)
        for i, ln in enumerate(lines):
            for cid, (row, names) in demoted.items():
                if (cid, base) in seen: continue
                hit = cid in ln or any(
                    re.search(r'(?<![A-Za-z0-9_])' + re.escape(nm) + r'(?![A-Za-z0-9_])', ln)
                    for nm in names)
                if not hit: continue
                win = "\n".join(lines[max(0, i - DEMOTED_LINES): i + DEMOTED_LINES + 1])
                if DEMOTED_CLOSE_W.search(win) and not NEG_CLOSE.search(win):
                    seen.add((cid, base))
                    if any(cid == ac and asub in base for ac, asub in allow):
                        continue  # verified-benign suppression (see allowlist)
                    flags.append((cid, row.get("release_status"), row.get("lean_status"),
                                  base, i + 1))
    return flags

IDPAT = re.compile(r'D0-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d+')
CLOSED_W = re.compile(r'\b(доказан\w*|теорем\w*|theorem|proved|forced|форсир\w*|выведен\w*|закрыт\w*|established|QED)\b|□', re.I)
# a closure word negated within ~30 chars is NOT an assertion of closure
NEG_CLOSE = re.compile(r'\b(not|no|не|без|never|neither)\b[^.]{0,30}?(доказан|теорем|theorem|proved|forced|closed|established|core theorem)', re.I)
OPEN_W = re.compile(r'\b(гипотез\w*|conjecture|PROOF-TARGET|PROOF_TARGET|open\s+problem|не\s+доказан\w*|'
                    r'frontier|обязательств\w*|obligation|TODO|scaffold|леса|MECH-LIMIT|mechanism-limit|'
                    r'bridge\s+owner|named\s+open|missing\s+artifact|NO-GO|no-go|not\s+(?:a\s+)?(?:closed\s+)?(?:CORE\s+)?theorem|'
                    r'not\s+closed|remains?\s+open|stays?\s+open|still\s+open)\b', re.I)
WIN = 240

def load_ledger():
    return {r["claim_id"]: r for r in csv.DictReader(LEDGER.open(encoding="utf-8")) if r.get("claim_id")}

def load_allowlist():
    p = ROOT / "tools" / "book_ledger_sync_allowlist.txt"
    allow = set()
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line=line.strip()
            if not line or line.startswith("#"): continue
            parts=[x.strip() for x in line.split("|")]
            if len(parts)>=2: allow.add((parts[0],parts[1]))
    return allow

def section_files():
    return sorted(glob.glob(str(BOOKS / "BOOK_0*" / "*.md")))

def main() -> int:
    strict = "--strict" in sys.argv
    byid = load_ledger()
    allow = load_allowlist()
    overs=[]; unders=[]
    seen=set()
    for f in section_files():
        t = Path(f).read_text(encoding="utf-8", errors="replace")
        for m in IDPAT.finditer(t):
            cid = m.group(0)
            row = byid.get(cid)
            if not row: continue
            rt = tier(row.get("release_status",""))
            w = t[max(0,m.start()-WIN):m.end()+WIN]
            closed = bool(CLOSED_W.search(w)) and not bool(NEG_CLOSE.search(w))
            openw = bool(OPEN_W.search(w))
            key=(cid, os.path.basename(f))
            if rt=="open" and closed and not openw and key not in seen:
                if any(cid==ac and asub in os.path.basename(f) for ac,asub in allow):
                    seen.add(key)  # verified-benign suppression (see allowlist)
                else:
                    overs.append((cid, row.get("release_status"), os.path.basename(f))); seen.add(key)
            elif rt=="closed" and openw and not closed and strict and key not in seen:
                unders.append((cid, row.get("release_status"), os.path.basename(f))); seen.add(key)
    dflags = scan_demoted(demoted_rows(byid), allow)
    print(f"check_book_ledger_sync: scanned {len(section_files())} sections against {len(byid)} ledger claims")
    print(f"  PROSE-OVERCLAIM (prose claims closure the ledger denies): {len(overs)}")
    for cid,rs,fn in overs: print(f"    [PROSE-OVERCLAIM] {cid}  ledger={rs}  in {fn}")
    print(f"  DEMOTED-CLOSURE-PROSE (prose asserts closure of a bridge-demoted/split row): {len(dflags)}")
    for cid,rs,ls,fn,line in dflags:
        print(f"    [DEMOTED-CLOSURE-PROSE] {cid}  ledger={rs}/{ls}  in {fn}:{line}")
    if strict:
        print(f"  PROSE-UNDERCLAIM (prose calls open what the ledger closed): {len(unders)}")
        for cid,rs,fn in unders: print(f"    [PROSE-UNDERCLAIM] {cid}  ledger={rs}  in {fn}")
    if overs:
        print("FAIL: prose over-claims closure beyond the ledger."); return 1
    if dflags:
        print("FAIL: prose asserts closure of demoted/split ledger rows."); return 1
    if strict and unders:
        print("FAIL (strict): prose under-claims closed ledger results."); return 1
    print("PASS"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
