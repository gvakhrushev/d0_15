#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact spatial-rigidity extension of the all-order Y-plane vacuum.

The existing a4d_y_slow_exact_plane_check proves the full joint Y identity
when the three spatial columns share one common vector w.  This checker lets
that common vector vary independently at the three incoming spatial
neighbours and derives the exact connection equations.  No Fourier scan,
floating rank or truncated Euler system is used.
"""
from __future__ import annotations

import sympy as sp
import a4d_y_slow_exact_plane_check as P


def check(name: str, cond: bool) -> None:
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def main() -> None:
    z, a, b, c, d = sp.symbols("z a b c d", real=True)
    Delta = a*d-b*c

    # Canonical spacelike difference plane used by the existing exact owner.
    e0 = sp.Matrix([1, 0, 0, 0])
    e3 = sp.Matrix([0, 0, 0, 1])
    u = sp.Matrix([0, a, b, 0])
    v = sp.Matrix([0, c, d, 0])

    # "d10:4" denotes the empty numeric range 10..3 in SymPy.  Name each
    # coordinate explicitly so the three neighbouring differences stay 4x1.
    ds = [sp.Matrix([sp.Symbol(f"d{r}_{j}", real=True) for j in range(4)])
          for r in (1, 2, 3)]
    check("INDEPENDENT_INCOMING_DIFFERENCE_COORDINATES",
          all(vec.shape == (4, 1) for vec in ds)
          and len({q for vec in ds for q in vec}) == 12)
    site = (0, 0, 0, 0)

    def S(w):
        return sp.Matrix.hstack(e0, w, w+u, w+v)

    def solder(x):
        key = (x[1], x[2], x[3])
        if key == (0, 0, 0):
            return S(e3)
        if key == (-1, 0, 0):
            return S(e3+ds[0])
        if key == (0, -1, 0):
            return S(e3+ds[1])
        if key == (0, 0, -1):
            return S(e3+ds[2])
        # time shifts have the same spatial coframe.
        return S(e3)

    J = P.GEN[3]  # J12
    U = P.cayley_simple(J, 1, z)
    wave = [U, P.I4, P.linv(U), P.I4]
    link = lambda x, r: wave[sum(x) % 4] if r == 0 else P.I4

    rows = {
        role: [sp.factor(P.edge_euler(solder, link, site, role, X))
               for X in P.GEN]
        for role in range(4)
    }

    # Spatial-role rows force equality of the incoming differences in internal
    # components 1,2,3.  These identities are independent of z and of the
    # shape of the spacelike difference plane.
    expected_spatial = {
        1: [0, 0, 0,
            -ds[1][3]+ds[2][3],
            ds[1][2]-ds[2][2],
            -ds[1][1]+ds[2][1]],
        2: [0, 0, 0,
            ds[0][3]-ds[2][3],
            -ds[0][2]+ds[2][2],
            ds[0][1]-ds[2][1]],
        3: [0, 0, 0,
            -ds[0][3]+ds[1][3],
            ds[0][2]-ds[1][2],
            -ds[0][1]+ds[1][1]],
    }
    for role in (1, 2, 3):
        check(f"ROLE_{role}_SPATIAL_DIFFERENCE_ROWS",
              rows[role] == [sp.factor(x) for x in expected_spatial[role]])

    # After the six independent spatial equalities, the only remaining
    # unknown difference components are d1_0,d2_0,d3_0.  The two role-0 boost
    # rows have rank two whenever Delta!=0.  Their three 2x2 minors are
    # +/- 4 Delta/(z^2+4), so no real amplitude z creates an exception.
    x = [ds[r][0] for r in range(3)]
    A0 = sp.Matrix([
        [sp.diff(rows[0][4], q) for q in x],
        [sp.diff(rows[0][5], q) for q in x],
    ])
    minors = [
        sp.factor(A0[:, [0, 1]].det()),
        sp.factor(A0[:, [0, 2]].det()),
        sp.factor(A0[:, [1, 2]].det()),
    ]
    target = [
        4*Delta/(z*z+4),
        -4*Delta/(z*z+4),
        4*Delta/(z*z+4),
    ]
    check("ROLE0_TIME_COMPONENT_MINORS",
          [sp.factor(q-t) for q, t in zip(minors, target)] == [0, 0, 0])

    common = sp.Matrix(sp.symbols("c0:4", real=True))
    subs_common = {
        ds[r][j]: common[j] for r in range(3) for j in range(4)
    }
    check("COMMON_DIFFERENCE_SUFFICIENT",
          all(sp.factor(value.subs(subs_common)) == 0
              for role in range(4) for value in rows[role]))

    # Solder/Gram rows are site-local in this Y vacuum and vanish for arbitrary
    # w.  Check them symbolically once with a completely arbitrary base w.
    w = sp.Matrix(sp.symbols("w0:4", real=True))
    check("ARBITRARY_W_ALL_SOLDER_ROWS",
          P.solder_euler(lambda _x: S(w), link, site) == sp.zeros(4))

    print("RESULT A4D-Y-PLANE-SPATIAL-RIGIDITY-EXACT")
    print("ASSUMPTION plane_det=a*d-b*c != 0; z real")
    print("CONCLUSION D1_w=D2_w=D3_w")
    print("CONTINUUM smooth realization is locally exact coframe and hence flat")
    print("SCOPE canonical spacelike-plane Y family with constant time column")


if __name__ == "__main__":
    main()
