#!/usr/bin/env python3
"""check_no_tautology_proofs.py - CI guard: no identity-tautology / vacuous-True theorems in D0/.

Two families of non-load-bearing "theorems" are forbidden:

(1) IDENTITY tautologies — `theorem NAME (... ) (v : T) : T := v` proves only `T -> T`
    (the identity function) and asserts nothing about D0. Found in Iteration 2 masquerading as
    `leanCoreProved` placeholders.

(2) VACUOUS-True stubs (added Iter-18) — `theorem NAME ... : True := by trivial` or
    `theorem NAME ... : P := by trivial` where `P` is a Prop defined `:= True`. The goal asserts
    nothing; the proof is a no-op. An audit found ~19 of these, several registered LEAN_PROVED /
    CORE-FORMALIZED. Such a theorem is either proved for real or is not the registry's proof-of-record.

GRANDFATHER ratchet (family 2): the vacuous-True stubs that existed at the Iter-18 audit are listed
in GRANDFATHER below. They are redundant doc/summary markers whose claims were REPOINTED to real
sibling theorems (so no active claim presents one as its proof). The guard FAILS if a vacuous-True
stub appears that is NOT grandfathered (a NEW one), and the list may only SHRINK over time. Run
`--list-vacuous` to print the current set (for re-baselining only when stubs are genuinely removed).

Exit 0 clean, 1 on any new identity tautology or any non-grandfathered vacuous-True stub.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D0DIR = ROOT / "09_LEAN_FORMALIZATION" / "D0"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# --- family (1): single-line identity tautologies ------------------------------------------
PLACEHOLDER = re.compile(r"\(\s*stmt\s*:\s*Prop\s*\)\s*\(\s*h\s*:\s*stmt\s*\)\s*:\s*stmt\s*:=\s*h\b")
IDENTITY = re.compile(r"\(\s*(\w+)\s*:\s*([^()]+?)\s*\)[^:=]*:\s*\2\s*:=\s*\1\s*$")
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:theorem|lemma|example)\b")

# --- family (2): vacuous-True stubs --------------------------------------------------------
VACPROP = re.compile(r"(?:^|\n)\s*(?:noncomputable\s+)?(?:def|abbrev)\s+([A-Za-z_][\w']*)\s*:\s*Prop\s*:=\s*True\b")
DECL_POS = re.compile(r"(?:^|\n)\s*(?:@\[[^\]]*\]\s*)?(?:theorem|lemma|example)\s+([A-Za-z_][\w']*)")
TRIV_GOAL = re.compile(r":\s*([A-Za-z_][\w'.]*)\s*:=\s*(?:by\s+)?trivial\b")

# Iter-18 audit baseline: vacuous-True stubs accepted as redundant doc/summary markers
# (their claims were repointed to real sibling theorems). The set may only shrink.
# Iter-19: the 11 operator-origin / no-go / boundary markers were CONVERTED from `: Prop := True`
# to real statements proved by their module's load-bearing siblings (capacity-core symmetry,
# gauge / non-abelian curvature skew-closure, vector-operator energy >= 0, flat-tensor no-go
# symmetry, edge scalar-leakage no-go, internal Hurwitz-dimension closure, ...). Ratchet 12 -> 1.
# The single remaining entry is a release-status documentation token (no math sibling).
GRANDFATHER: set[str] = {
    "TheoremLedger/ReleaseStatus.lean::lean_bridge_assumptions_explicit",
}


def find_identity_hits() -> list[str]:
    hits: list[str] = []
    for p in sorted(D0DIR.rglob("*.lean")):
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not DECL.match(ln):
                continue
            if PLACEHOLDER.search(ln) or IDENTITY.search(ln):
                hits.append(f"{p.relative_to(D0DIR).as_posix()}:{i}: {ln.strip()[:90]}")
    return hits


def find_vacuous_true() -> list[str]:
    """Return `relpath::theoremName` for every theorem proving `True` (or a Prop defined `:= True`)
    by a bare `trivial`/`by trivial`."""
    hits: list[str] = []
    for p in sorted(D0DIR.rglob("*.lean")):
        text = p.read_text(encoding="utf-8", errors="replace")
        vac_props = {m.group(1) for m in VACPROP.finditer(text)} | {"True"}
        decls = list(DECL_POS.finditer(text))
        for idx, m in enumerate(decls):
            name = m.group(1)
            end = decls[idx + 1].start() if idx + 1 < len(decls) else len(text)
            span = text[m.start():end]
            gm = TRIV_GOAL.search(span)
            if gm and gm.group(1) in vac_props:
                hits.append(f"{p.relative_to(D0DIR).as_posix()}::{name}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-vacuous", action="store_true",
                    help="print the current vacuous-True stub set (for re-baselining the grandfather)")
    args = ap.parse_args()

    vac = find_vacuous_true()
    if args.list_vacuous:
        for h in sorted(vac):
            print(h)
        print(f"-- {len(vac)} vacuous-True stub(s)")
        return 0

    ident = find_identity_hits()
    new_vac = sorted(set(vac) - GRANDFATHER)
    stale_gf = sorted(GRANDFATHER - set(vac))  # grandfathered entries that are now gone (good — shrink)

    fail = False
    if ident:
        fail = True
        print(f"RESULT: FAIL — {len(ident)} identity-tautology theorem(s) (prove for real or remove):")
        for h in ident[:40]:
            print("  - " + h)
    if new_vac:
        fail = True
        print(f"RESULT: FAIL — {len(new_vac)} NEW vacuous-True stub(s) (`: True := by trivial`); prove for real or remove:")
        for h in new_vac[:40]:
            print("  - " + h)
    if fail:
        return 1

    note = ""
    if stale_gf:
        note = f" ({len(stale_gf)} grandfathered stub(s) now removed — tighten GRANDFATHER)"
    print(f"RESULT: PASS — no identity tautologies; {len(vac)} vacuous-True stub(s) all grandfathered{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
