#!/usr/bin/env python3
"""check_no_tautology_proofs.py - CI guard: no identity-tautology theorems in D0/.

A theorem of the form `theorem NAME (... ) (v : T) : T := v` proves only `T -> T`
(the identity function) and asserts nothing about D0. In Iteration 2 these were
found masquerading as `leanCoreProved` (e.g. K-theory / spectral-triple
`(stmt : Prop) (h : stmt) : stmt := h` placeholders). Lean must be valuable, not
for-show: such a theorem is either proved for real or removed. This guard fails if
any reappear, so a placeholder can never again be marked proved.

Detects (single-line declarations):
  - the exact `(stmt : Prop) (h : stmt) : stmt := h` placeholder, and
  - the general identity `(v : T) ... : T := v` (argument type == goal == body).

Exit 0 clean, 1 if any tautology is found.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D0DIR = ROOT / "09_LEAN_FORMALIZATION" / "D0"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PLACEHOLDER = re.compile(r"\(\s*stmt\s*:\s*Prop\s*\)\s*\(\s*h\s*:\s*stmt\s*\)\s*:\s*stmt\s*:=\s*h\b")
# general identity: `(v : T) ... : T := v`  (T captured, repeated as goal; body == v)
IDENTITY = re.compile(r"\(\s*(\w+)\s*:\s*([^()]+?)\s*\)[^:=]*:\s*\2\s*:=\s*\1\s*$")
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:theorem|lemma|example)\b")


def main() -> int:
    hits: list[str] = []
    for p in sorted(D0DIR.rglob("*.lean")):
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not DECL.match(ln):
                continue
            if PLACEHOLDER.search(ln) or IDENTITY.search(ln):
                hits.append(f"{p.relative_to(D0DIR).as_posix()}:{i}: {ln.strip()[:90]}")
    if hits:
        print(f"RESULT: FAIL — {len(hits)} identity-tautology theorem(s) (prove for real or remove):")
        for h in hits[:40]:
            print("  - " + h)
        return 1
    print("RESULT: PASS — no identity-tautology theorems in D0/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
