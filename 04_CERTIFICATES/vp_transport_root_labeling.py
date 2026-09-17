#!/usr/bin/env python3
"""D0-TRANSPORT-ROOT-LABELING-CANONICAL-001 — exact mirror.

The three transport roots are distinct reals, so they carry a canonical strictly-increasing
labeling: there is a unique monotone enumeration, and every non-identity relabeling breaks
monotonicity. Combined with the T33 ladder, this collapses the S3 residue to the identity;
the only remaining external step is the order-preserving generation identification.
"""
from __future__ import annotations

import sys
from itertools import permutations

import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-TRANSPORT-ROOT-LABELING-CANONICAL-001 ===")
    ok = True

    x = sp.symbols("x")
    roots = sp.Poly(x**3 - 359 * x - 2574, x).all_roots()
    approx = [complex(sp.N(r, 40)) for r in roots]
    if len(roots) != 3 or any(abs(z.imag) > 1e-20 for z in approx):
        print(f"  FAIL (A): expected three real roots, got {approx}")
        ok = False
    else:
        print("  ✓ (A) three real transport roots")

    vals = sorted(z.real for z in approx)
    strictly_increasing = all(vals[i] < vals[i + 1] for i in range(2))
    if not strictly_increasing:
        print(f"  FAIL (B): roots not strictly separated: {vals}")
        ok = False
    else:
        print(f"  ✓ (B) canonical increasing order exists: {[round(v,3) for v in vals]}")

    # Uniqueness: among all 6 relabelings of the sorted values, exactly one is monotone.
    monotone_count = 0
    for perm in permutations(range(3)):
        seq = [vals[perm[i]] for i in range(3)]
        if all(seq[i] < seq[i + 1] for i in range(2)):
            monotone_count += 1
    if monotone_count != 1:
        print(f"  FAIL (C): {monotone_count} monotone labelings (expected exactly 1)")
        ok = False
    else:
        print("  ✓ (C) the strictly-increasing enumeration is unique (1 of 6 relabelings)")

    print("\n  -- can-fail controls --")
    # A degenerate multiset (repeated value) would admit no strict order / break uniqueness.
    degen = [1.0, 1.0, 2.0]
    degen_monotone = sum(
        1 for perm in permutations(range(3))
        if all([degen[perm[i]] for i in range(3)][k] < [degen[perm[i]] for i in range(3)][k + 1]
                for k in range(2))
    )
    # A non-identity relabel of the sorted roots is not monotone.
    swapped = [vals[1], vals[0], vals[2]]
    swapped_bad = not all(swapped[i] < swapped[i + 1] for i in range(2))
    if degen_monotone != 0 or not swapped_bad:
        print(f"  FAIL controls: degen_monotone={degen_monotone}, swapped_bad={swapped_bad}")
        ok = False
    else:
        print("  ✓ controls: repeated-root frame has no strict order; a swap breaks monotonicity")

    print("\n" + ("PASS — transport roots carry a unique canonical generation labeling"
                  if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
