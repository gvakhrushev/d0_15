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

# --- family (3): trivial-GOAL shells (Iter-21) ---------------------------------------------
# The goal itself is true by syntax, regardless of proof tactic — so the theorem asserts nothing
# about D0. Three shapes the Iter-21 review flagged on LEAN_PROVED/CORE/NO_GO rows:
#   * self-equality  `... : X = X := ...`          (a reflexivity dressed as a theorem)
#   * negated-false  `... : ¬ False := ...`         (vacuously true)
#   * boolean-flag   `... : flag = true := ...`     where `flag` is `def ... : Bool := true`
# These are matched on the GOAL (the text up to the theorem's first `:=`), never the proof body.
SELF_EQ = re.compile(r":\s*([A-Za-z_][\w'.]*)\s*=\s*([A-Za-z_][\w'.]*)\s*:=")
NOT_FALSE = re.compile(r":\s*(?:¬|Not\b)\s*False\b\s*:=")
BOOLTRUE_DEF = re.compile(r"(?:^|\n)\s*(?:noncomputable\s+)?(?:def|abbrev)\s+([A-Za-z_][\w']*)\s*:\s*Bool\s*:=\s*true\b")
BOOL_GOAL = re.compile(r":\s*([A-Za-z_][\w'.]*)\s*=\s*(?:true|Bool\.true)\s*:=")

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

# Iter-21 baseline for family (3) trivial-goal shells. Populated from the current tree (the shells
# that already exist are accepted; the guard FAILS on any NEW one). This set may only SHRINK.
GRANDFATHER_TRIVIAL: set[str] = set()


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


def find_trivial_goal_shells() -> list[str]:
    """Return `relpath::name [tag]` for every theorem whose GOAL is true by syntax: `X = X`,
    `¬ False`, or `flag = true` for a `Bool := true` def. Inspects only the goal (text up to the
    theorem's first `:=`), so proof-body occurrences do not false-positive."""
    hits: list[str] = []
    for p in sorted(D0DIR.rglob("*.lean")):
        text = p.read_text(encoding="utf-8", errors="replace")
        bool_true = {m.group(1) for m in BOOLTRUE_DEF.finditer(text)}
        decls = list(DECL_POS.finditer(text))
        for idx, m in enumerate(decls):
            name = m.group(1)
            end = decls[idx + 1].start() if idx + 1 < len(decls) else len(text)
            span = text[m.start():end]
            cut = span.find(":=")
            head = span if cut < 0 else span[:cut + 2]  # name + binders + `: goal :=`
            tag = None
            em = SELF_EQ.search(head)
            if em and em.group(1) == em.group(2):
                tag = f"self-eq {em.group(1)}={em.group(2)}"
            elif NOT_FALSE.search(head):
                tag = "neg-False"
            else:
                bm = BOOL_GOAL.search(head)
                if bm and bm.group(1) in bool_true:
                    tag = f"bool-flag {bm.group(1)}=true"
            if tag:
                hits.append(f"{p.relative_to(D0DIR).as_posix()}::{name}  [{tag}]")
    return hits


def _key(hit: str) -> str:
    """Strip the trailing `  [tag]` so grandfather membership is by relpath::name."""
    return hit.split("  [", 1)[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-vacuous", action="store_true",
                    help="print the current vacuous-True stub set (for re-baselining the grandfather)")
    ap.add_argument("--list-trivial", action="store_true",
                    help="print the current trivial-goal shell set (for re-baselining GRANDFATHER_TRIVIAL)")
    args = ap.parse_args()

    vac = find_vacuous_true()
    if args.list_vacuous:
        for h in sorted(vac):
            print(h)
        print(f"-- {len(vac)} vacuous-True stub(s)")
        return 0

    triv = find_trivial_goal_shells()
    if args.list_trivial:
        for h in sorted(triv):
            print(h)
        print(f"-- {len(triv)} trivial-goal shell(s)")
        return 0

    ident = find_identity_hits()
    new_vac = sorted(set(vac) - GRANDFATHER)
    stale_gf = sorted(GRANDFATHER - set(vac))  # grandfathered entries that are now gone (good — shrink)
    new_triv = sorted(h for h in triv if _key(h) not in GRANDFATHER_TRIVIAL)
    triv_keys = {_key(h) for h in triv}
    stale_triv = sorted(GRANDFATHER_TRIVIAL - triv_keys)

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
    if new_triv:
        fail = True
        print(f"RESULT: FAIL — {len(new_triv)} NEW trivial-goal shell(s) (`X=X` / `¬False` / `flag=true`); prove a real statement or remove:")
        for h in new_triv[:40]:
            print("  - " + h)
    if fail:
        return 1

    note = ""
    if stale_gf:
        note += f" ({len(stale_gf)} grandfathered stub(s) now removed — tighten GRANDFATHER)"
    if stale_triv:
        note += f" ({len(stale_triv)} grandfathered trivial-goal shell(s) now removed — tighten GRANDFATHER_TRIVIAL)"
    print(f"RESULT: PASS — no identity tautologies; {len(vac)} vacuous-True stub(s) all grandfathered; "
          f"{len(triv)} trivial-goal shell(s) all grandfathered{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
