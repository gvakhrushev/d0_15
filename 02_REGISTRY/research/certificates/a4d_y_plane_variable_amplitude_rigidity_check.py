#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact variable-amplitude rigidity in the canonical Y-plane joint class.

This extends a4d_y_plane_spatial_rigidity_check.py.  The common spatial
column may vary arbitrarily, and the real Y Cayley amplitude is an arbitrary
field on the even carrier.  Selected literal independent-edge Euler rows
force equality across all six physical graph moves.  No Fourier scan,
linearization, floating rank, or ansatz-gradient substitution is used.
"""
from __future__ import annotations

import sympy as sp
import a4d_y_slow_exact_plane_check as P


def ck(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def main() -> None:
    aa, bb, cc, dd = sp.symbols("aa bb cc dd", real=True)
    W = sp.Matrix(sp.symbols("W0:4", real=True))
    dvec = [sp.Matrix(sp.symbols(f"d{r}0:4", real=True)) for r in (1, 2, 3)]
    Delta = sp.expand(aa*dd-bb*cc)

    e0 = sp.Matrix([1,0,0,0])
    u = sp.Matrix([0,aa,bb,0])
    v = sp.Matrix([0,cc,dd,0])

    def coframe(w):
        return sp.Matrix.hstack(e0, w, w+u, w+v)

    def w_at(x):
        return W - x[1]*dvec[0] - x[2]*dvec[1] - x[3]*dvec[2]

    solder = lambda x: coframe(w_at(x))

    amps = {}
    def amp(x):
        if x not in amps:
            amps[x] = sp.symbols("a_"+"_".join(map(str,x)), real=True)
        return amps[x]

    J = P.GEN[3]
    def link(x, role):
        if role != 0:
            return P.I4
        ph = sum(x) % 4
        if ph == 0:
            return P.cayley_simple(J, 1, amp(x))
        if ph == 2:
            return P.linv(P.cayley_simple(J, 1, amp(x)))
        return P.I4

    # For role s, the two selected boost rows depend on a nonzero plane vector:
    # s=1 -> u-v, s=2 -> v, s=3 -> u.
    AB = {
        1: (aa-cc, bb-dd),
        2: (cc, dd),
        3: (aa, bb),
    }
    signs0 = {1:-1, 2:-1, 3:1}
    signs3 = {1:1, 2:1, 3:-1}

    # Fast phase 0 compares amplitudes at x and x+e_s-e_0.
    site0=(0,0,0,0)
    # Fast phase 3 compares the adjacent even amplitudes separated by e_s+e_0.
    site3=(3,0,0,0)

    for role in (1,2,3):
        A,B=AB[role]

        x0=amp(P.shift(site0,0,-1))
        # The actual incoming temporal corner for this role is -e0+e_s.
        xm=amp(P.shift(P.shift(site0,0,-1),role))
        # At phase 0 the other even amplitude is the base Role-0 link.
        y0=amp(site0)
        # xm is the symbol that literal edge_euler uses; x0 is not active here.
        del x0

        denm=(xm*xm+4)*(y0*y0+4)
        commonm=2*W[3]*(xm-y0)/denm
        fminus=A*(xm*y0-4)+2*B*(xm+y0)
        gminus=B*(xm*y0-4)-2*A*(xm+y0)
        expected0=[
            sp.factor(signs0[role]*commonm*fminus),
            sp.factor(signs0[role]*commonm*gminus),
        ]
        actual0=[
            sp.factor(P.edge_euler(solder,link,site0,role,P.GEN[0])),
            sp.factor(P.edge_euler(solder,link,site0,role,P.GEN[1])),
        ]
        ck(f"ROLE_{role}_MINUS_MOVE_SELECTED_ROWS",
           [sp.factor(a-b) for a,b in zip(actual0,expected0)] == [0,0])

        yp=amp(P.shift(site3,0,-1))  # phase-2 even link
        xp=amp(P.shift(site3,role))  # phase-0 even link after +e_s
        denp=(xp*xp+4)*(yp*yp+4)
        commonp=2*W[3]*(yp-xp)/denp
        fplus=A*(xp*yp-4)-2*B*(xp+yp)
        gplus=B*(xp*yp-4)+2*A*(xp+yp)
        expected3=[
            sp.factor(signs3[role]*commonp*fplus),
            sp.factor(signs3[role]*commonp*gplus),
        ]
        actual3=[
            sp.factor(P.edge_euler(solder,link,site3,role,P.GEN[0])),
            sp.factor(P.edge_euler(solder,link,site3,role,P.GEN[1])),
        ]
        ck(f"ROLE_{role}_PLUS_MOVE_SELECTED_ROWS",
           [sp.factor(a-b) for a,b in zip(actual3,expected3)] == [0,0])

        # If amplitudes differ, the two brackets must vanish.  Their coefficient
        # matrix in (xy-4, x+y) has determinant +/-2(A^2+B^2), so over R this
        # forces xy=4 and x+y=0, impossible.  Record the exact determinant.
        Mminus=sp.Matrix([[A,2*B],[B,-2*A]])
        Mplus=sp.Matrix([[A,-2*B],[B,2*A]])
        ck(f"ROLE_{role}_BRACKET_DETERMINANTS",
           sp.factor(Mminus.det()+2*(A*A+B*B)) == 0 and
           sp.factor(Mplus.det()-2*(A*A+B*B)) == 0)

    # Nondegenerate plane Delta != 0 implies each of u, v, u-v is nonzero:
    # encode the contrapositive polynomial controls used by the proof.
    ck("U_ZERO_FORCES_DELTA_ZERO",
       sp.factor(Delta.subs({aa:0,bb:0})) == 0)
    ck("V_ZERO_FORCES_DELTA_ZERO",
       sp.factor(Delta.subs({cc:0,dd:0})) == 0)
    ck("U_MINUS_V_ZERO_FORCES_DELTA_ZERO",
       sp.factor(Delta.subs({aa:cc,bb:dd})) == 0)

    # The six graph moves generate the even-sum carrier.  An explicit basis:
    # e_s-e_0 and e_s+e_0 give 2e_0 by subtraction for any s, hence all
    # even-sum displacements.
    moves=[
        sp.Matrix([-1,1,0,0]), sp.Matrix([-1,0,1,0]), sp.Matrix([-1,0,0,1]),
        sp.Matrix([1,1,0,0]), sp.Matrix([1,0,1,0]), sp.Matrix([1,0,0,1]),
    ]
    M=sp.Matrix.hstack(*moves)
    # gcd of all 4x4 minors is 2, the index of the even-sum sublattice in Z^4.
    minors=[]
    from itertools import combinations
    for cols in combinations(range(6),4):
        minors.append(abs(int(M[:,cols].det())))
    g=0
    from math import gcd
    for value in minors:
        g=gcd(g,value)
    ck("SIX_MOVES_GENERATE_EVEN_SUM_CARRIER", g == 2)

    print("RESULT A4D-Y-PLANE-VARIABLE-AMPLITUDE-RIGIDITY-EXACT")
    print("ASSUMPTIONS real amplitudes; Delta=aa*dd-bb*cc != 0; nondegenerate coframe W3 != 0")
    print("CONCLUSION amplitude is constant on the connected even carrier")
    print("COMBINE a4d_y_plane_spatial_rigidity_check.py -> continuum coframe is locally flat")


if __name__ == "__main__":
    main()
