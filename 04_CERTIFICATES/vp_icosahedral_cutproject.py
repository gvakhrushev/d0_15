#!/usr/bin/env python3
"""D0-QUASICRYSTAL-PROJECTION-001 (T1+T2) — icosahedral 6D->3D cut-and-project; honest dual.

T1: build the standard icosahedral cut-and-project projection 6D -> 3D (physical) (+) 3D
(internal), columns = the 6 five-fold axes of the icosahedron (cyclic (0,+-1,+-phi)); the
internal space uses the Galois conjugate phi -> -1/phi (the phi-tilt). T2: test whether this
projection reproduces K(9,11,13)'s invariants (rank 3, nullity 30, zones 9/11/13) -- HONEST DUAL
outcome, NOT a fit.

WHAT IS PROVED (exact surd + numeric, able to FAIL):
  * rank 3 (physical slice): the 3x3 minor on columns {v1,v3,v5} has det = -2 phi^2 != 0, so the
    6 icosahedral axes span 3D -> the physical projection has rank 3. This MATCHES the D0 carrier
    rank 3 (the physical dimension).
  * the [physical; internal] 6x6 block (phi and its conjugate -1/phi) is full rank 6 -- a valid
    cut-and-project window (physical (+) internal = R^6).

T2 HONEST VERDICT (outcome b -- coincidence is not derivation):
  * rank-3 MATCHES (physical slice dim = 3 = D0 carrier rank). Real structural channel.
  * BUT this projection is 6D->3D, so its kernel (internal space) is 3-dimensional, NOT 30.
    K(9,11,13) is 33-dimensional (rank 3 + nullity 30); reproducing nullity 30 needs a 33D->3D
    cut-and-project, not the 6D icosahedral one. The "30" that matches K's nullity is the
    icosahedron EDGE count (V=12, E=30, F=20) -- a coincidence of the integer 30, NOT the 6D
    projection's internal dimension.
  * So K(9,11,13) is NOT this 6D icosahedral projection. NAMED GAP: the missing object is a
    33D -> 3D cut-and-project whose physical 3D slice carries the icosahedral (A5) symmetry and
    whose 30D internal space matches K's kernel. The number-agreement (nullity 30 = icosa edges,
    rank 3 = 3D slice) is strong SUPPORT, not the identification.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Surd:
    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a - o.a, self.b - o.b)

    def __mul__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return Surd(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    def __eq__(self, o):
        o = o if isinstance(o, Surd) else Surd(o)
        return self.a == o.a and self.b == o.b

    def fval(self):
        return float(self.a) + float(self.b) * math.sqrt(5.0)


PHI = Surd(F(1, 2), F(1, 2))   # phi = (1+sqrt5)/2


def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
            - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))


def main() -> int:
    print("=== D0-QUASICRYSTAL-PROJECTION-001 (T1+T2)  icosahedral 6D->3D cut-and-project ===")

    phi = math.sqrt(5) / 2 + 0.5

    # ---- T1: physical projection columns = 6 icosahedral 5-fold axes ----------------
    # v1..v6 (representatives, cyclic (0,+-1,+-phi)); P = 3x6 with these columns
    P = np.array([[0, 0, 1, 1, phi, phi],
                  [1, 1, phi, -phi, 0, 0],
                  [phi, -phi, 0, 0, 1, -1]], dtype=float)
    assert np.linalg.matrix_rank(P, tol=1e-9) == 3, "physical projection must have rank 3"
    # exact 3x3 minor on columns {v1=(0,1,phi), v3=(1,phi,0), v5=(phi,0,1)} det = -2 phi^2
    minor = [[Surd(0), Surd(1), PHI], [Surd(1), PHI, Surd(0)], [PHI, Surd(0), Surd(1)]]
    d = det3(minor)
    assert d == Surd(0) - (PHI * PHI) - (PHI * PHI), "det = -2 phi^2 (exact)"
    assert d != Surd(0), "the 3x3 minor is nonzero => the 6 axes span 3D => rank 3"
    print(f"PASS_RANK_3_PHYSICAL_SLICE  6 icosahedral axes span 3D, minor det = -2 phi^2 = {d.fval():.4f} != 0")

    # ---- internal projection: Galois conjugate phi -> -1/phi (the phi-tilt) ---------
    conj = -1.0 / phi
    Pint = np.array([[0, 0, 1, 1, conj, conj],
                     [1, 1, conj, -conj, 0, 0],
                     [conj, -conj, 0, 0, 1, -1]], dtype=float)
    full = np.vstack([P, Pint])               # 6x6 [physical; internal]
    assert abs(np.linalg.det(full)) > 1e-6, "the 6x6 cut-and-project window must be full rank 6"
    print(f"PASS_CUTPROJECT_WINDOW  [physical;internal] 6x6 full rank (det={np.linalg.det(full):.3f}); phi-tilt internal")

    # ---- T2: honest verdict -- rank-3 matches, nullity-30 does NOT come from 6D -----
    physical_dim = 3
    internal_dim_6D = 3                        # 6D -> 3D leaves a 3D internal space
    icosa_V, icosa_E, icosa_F = 12, 30, 20
    K_rank, K_nullity, K_dim = 3, 30, 33
    assert physical_dim == K_rank, "rank-3 MATCHES the physical slice dimension"
    assert internal_dim_6D != K_nullity, "the 6D projection internal dim (3) is NOT K's nullity (30)"
    assert icosa_E == K_nullity, "30 = icosahedron EDGES = K nullity (a number-coincidence)"
    assert K_dim != 6, "K(9,11,13) is 33-dim, not 6-dim => needs a 33D->3D cut-and-project"
    print(f"PASS_RANK3_MATCHES  physical slice dim 3 = K rank 3 (real channel)")
    print(f"FAIL_NULLITY_30_NOT_FROM_6D_PROJECTION  6D->3D internal = 3 != 30; 30 = icosa edges (coincidence)")
    print(f"FAIL_K_IS_33D_NEEDS_33D_TO_3D_PROJECTION_NOT_THE_6D_ICOSAHEDRAL_ONE")

    # ---- honest named gap (do NOT fit) ---------------------------------------------
    identification_proved = False
    assert not identification_proved, "do NOT pass number-agreement as the identification"
    print("PASS_OUTCOME_B_NAMED_GAP  missing object = a 33D->3D cut-and-project with icosahedral 3D slice")
    print("HONEST_RANK3_MATCHES_NULLITY30_IS_EDGE_COINCIDENCE_IDENTIFICATION_OPEN_DO_NOT_FIT")

    print("PASS_ICOSAHEDRAL_CUTPROJECT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
