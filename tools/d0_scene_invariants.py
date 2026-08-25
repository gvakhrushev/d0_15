#!/usr/bin/env python3
"""
d0_scene_invariants.py — every invariant of a complete multipartite scene, from the zone sizes.

Written after a session in which 359, 1287, 2574, 10560, 39/160, the transport eigenvalues, the
archive degeneracies and the degeneracy gap were each recomputed by hand, several of them twice.
None of that needs repeating: they are all elementary symmetric functions of the zone sizes.

    python3 tools/d0_scene_invariants.py              # the frozen scene 9 11 13
    python3 tools/d0_scene_invariants.py 9 11 13 15   # any candidate scene

Machine-checked counterparts (all `sorry`-free, all built):
    D0.Spectral.TransportClosedForm            Q = 𝟙nᵀ − diag n; secular equation = transport cubic
    D0.Spectral.TransportSelfAdjoint           D·Q = Qᵀ·D — self-adjoint in the zone-size measure
    D0.Spectral.DarkArchiveStructure           ker A = zone-balanced vectors; no invariant in it
    D0.Spectral.JointCommutant                 centraliser of {Aut, A} has dimension 6 = 3 + 3
    D0.Synthesis.ZoneIsGeneration              per zone: 1 visible + (n−1) dark
    D0.Synthesis.DarkSectorCensus              dark degeneracies 8, 10, 12; three couplings
    D0.Synthesis.SymmetricFunctionCalculus     ∏(N−nᵢ) = N·e₂ − e₃; §04.2 readout from e₂, e₃
    D0.Synthesis.ActiveSplittingFromDistinctness  gap = Σ a(b−c)²; zero iff zones equal
"""

import sys
from fractions import Fraction as F
from itertools import combinations


def invariants(n):
    k = len(n)
    N = sum(n)
    e2 = sum(a * b for a, b in combinations(n, 2))
    e3 = None
    if k == 3:
        e3 = n[0] * n[1] * n[2]
    deg = [N - x for x in n]
    out = {
        "zone sizes": n,
        "k (zone count)": k,
        "N = e1 = |V|": N,
        "e2": e2,
        "degrees (N - n_i)": deg,
        "D = prod n_i (top-chain dim)": prod(n),
        "H = prod (n_i - 1) (top Betti)": prod([x - 1 for x in n]),
        "archive block dims (n_i - 1)": [x - 1 for x in n],
        "archive dim = sum (n_i - 1)": sum(x - 1 for x in n),
        "visible dim = k": k,
        "total check (k + archive)": k + sum(x - 1 for x in n),
    }
    if k == 3:
        a, b, c = n
        out["e3"] = e3
        out["transport cubic"] = f"x^3 - {e2}x - {2 * e3}"
        out["  (= x^3 - e2 x - 2 e3)"] = ""
        out["degree product"] = prod(deg)
        out["identity  prod(N-n_i) = N*e2 - e3"] = f"{prod(deg)} == {N * e2 - e3}  " \
            f"{'OK' if prod(deg) == N * e2 - e3 else 'MISMATCH'}"
        out["det S = 2 e3 / prod(deg)"] = F(2 * e3, prod(deg))
        out["active eigenvalue sum"] = 3
        out["active eigenvalue product"] = F(2 * N * e2, prod(deg))
        gap = N * e2 - 9 * e3
        out["degeneracy gap  N*e2 - 9*e3"] = gap
        out["  = a(b-c)^2+b(c-a)^2+c(a-b)^2"] = a * (b - c) ** 2 + b * (c - a) ** 2 + c * (a - b) ** 2
        out["active spectrum"] = "DEGENERATE (zones equal)" if gap == 0 else "split"
        out["joint commutant dim"] = 3 + k
        out["Aut-commutant dim"] = k * k + k
    return out


def prod(xs):
    r = 1
    for x in xs:
        r *= x
    return r


def transport_roots(n):
    """Numeric roots of the transport cubic, for orientation only."""
    if len(n) != 3:
        return None
    try:
        import numpy as np
    except ImportError:
        return None
    N, e2, e3 = sum(n), sum(a * b for a, b in combinations(n, 2)), prod(n)
    return sorted(np.roots([1, 0, -e2, -2 * e3]).real, reverse=True)


def main():
    args = sys.argv[1:]
    n = [int(x) for x in args] if args else [9, 11, 13]
    if any(x < 1 for x in n):
        print("zone sizes must be positive")
        return 1
    inv = invariants(n)
    width = max(len(k) for k in inv)
    print("=" * (width + 34))
    for k, v in inv.items():
        print(f"{k:<{width}}  {v}")
    r = transport_roots(n)
    if r is not None:
        print(f"{'transport eigenvalues (numeric)':<{width}}  {[round(x, 5) for x in r]}")
    print("=" * (width + 34))
    if len(set(n)) != len(n):
        print("NOTE: repeated zone sizes — Aut gains zone swaps, zone rigidity is lost.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
