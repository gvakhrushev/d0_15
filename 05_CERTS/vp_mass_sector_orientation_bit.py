#!/usr/bin/env python3
"""D0-MASS-SECTOR-ORIENTATION-BIT-001 — exact mirror.

After the intrinsic real order pins the labeling (T34), the only combinatorial residue is a
single orientation bit: the increasing and decreasing enumerations of the three transport roots
are the two — and only two — order-respecting identifications, and they differ.
"""
from __future__ import annotations

import sys
from itertools import permutations

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-MASS-SECTOR-ORIENTATION-BIT-001 ===")
    ok = True

    x = sp.symbols("x")
    roots = sp.Poly(x**3 - 359 * x - 2574, x).all_roots()
    vals = sorted(float(sp.re(sp.N(r, 40))) for r in roots)
    if len(vals) != 3 or not all(vals[i] < vals[i + 1] for i in range(2)):
        print(f"  FAIL (A): roots not three strictly-ordered reals: {vals}")
        ok = False
    else:
        print("  ✓ (A) three strictly-ordered transport roots")

    perms = list(permutations(range(3)))
    mono = [p for p in perms if all(vals[p[i]] < vals[p[i + 1]] for i in range(2))]
    anti = [p for p in perms if all(vals[p[i]] > vals[p[i + 1]] for i in range(2))]
    if len(mono) != 1 or len(anti) != 1:
        print(f"  FAIL (B): monotone={len(mono)}, antitone={len(anti)} (expected 1 and 1)")
        ok = False
    else:
        print("  ✓ (B) exactly one increasing and one decreasing enumeration")

    order_respecting = set(mono) | set(anti)
    if len(order_respecting) != 2:
        print(f"  FAIL (C): order-respecting count = {len(order_respecting)} (expected 2)")
        ok = False
    else:
        print("  ✓ (C) the orientation residue is exactly a 2-element (ℤ/2) choice")

    increasing = mono[0]
    decreasing = anti[0]
    if increasing == decreasing:
        print("  FAIL (D): the two orientations coincide")
        ok = False
    else:
        print("  ✓ (D) the increasing and decreasing labelings differ")

    print("\n  -- can-fail controls --")
    # A generic (non-monotone) permutation is neither increasing nor decreasing.
    generic = (1, 0, 2)
    generic_bad = generic not in order_respecting
    # If a root were repeated, no strict orientation would exist (residue not a clean bit).
    degen = [1.0, 1.0, 2.0]
    degen_mono = [p for p in perms if all(degen[p[i]] < degen[p[i + 1]] for i in range(2))]
    if not generic_bad or len(degen_mono) != 0:
        print(f"  FAIL controls: generic_bad={generic_bad}, degen_mono={len(degen_mono)}")
        ok = False
    else:
        print("  ✓ controls: a shuffled labeling is rejected; a degenerate frame has no orientation")

    print("\n" + ("PASS — the mass-sector residual is exactly one orientation bit" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
