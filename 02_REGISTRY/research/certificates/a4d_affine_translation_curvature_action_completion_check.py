#!/usr/bin/env python3
"""Exact invariant-theory controls for affine translation curvature.

Research-only certificate. Exact rational/symbolic arithmetic.

It verifies:
  * an exact proper loxodromic Lorentz holonomy P with det(I-P) != 0;
  * pure affine translation conjugation is transitive on t for such P;
  * open-torsion translation can likewise be gauged arbitrarily when F is
    invertible;
  * the rational one-parameter proper-Lorentz path approaching I has
    det(I-P(q)) nonzero for q != 0, supporting the continuity boundary;
  * traces of the 5x5 homogeneous affine-matrix powers are translation-blind;
  * the polynomial TWO-holonomy residual
        R_{2|1}=det(I-P1)t2-(I-P2)adj(I-P1)t1
    transforms as a Lorentz vector under full affine conjugation;
  * Lorentz norm of R is a full-affine scalar;
  * reversal controls for the two loops;
  * an exact L=2 one-edge affine-shift witness outside the node-gauge image is
    invisible to a relative-solder-only completion but is detected by R.

The continuity theorem itself is mathematical:
on the open dense det(I-P) != 0 stratum every invariant is t-independent;
joint continuity extends that independence to singular strata.  The exact
path/determinant checks below certify the nonempty generic stratum and an
explicit approach to P=I.
"""

from itertools import combinations, product
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

BOOST = sp.eye(4)
BOOST[0, 0] = sp.Rational(5, 3)
BOOST[0, 1] = sp.Rational(4, 3)
BOOST[1, 0] = sp.Rational(4, 3)
BOOST[1, 1] = sp.Rational(5, 3)

RBC = sp.eye(4)
RBC[1, 1] = 0
RBC[1, 2] = 1
RBC[2, 1] = -1
RBC[2, 2] = 0

RCD = sp.eye(4)
RCD[2, 2] = 0
RCD[2, 3] = 1
RCD[3, 2] = -1
RCD[3, 3] = 0

for name, g in (("BOOST", BOOST), ("RBC", RBC), ("RCD", RCD)):
    check(name + "_LORENTZ", g.T * ETA * g == ETA)
    check(name + "_DET_ONE", g.det() == 1)

# ---------------------------------------------------------------------------
# Single-loop generic transitivity
# ---------------------------------------------------------------------------

# Boost in AB and quarter-turn in CD commute and give a rational loxodromic
# proper Lorentz matrix with no eigenvalue 1.
P_LOX = sp.simplify(BOOST * RCD)
M_LOX = I4 - P_LOX

check("LOXODROMIC_LORENTZ", P_LOX.T * ETA * P_LOX == ETA)
check("LOXODROMIC_DET_ONE", P_LOX.det() == 1)
check("I_MINUS_P_INVERTIBLE", sp.factor(M_LOX.det()) == sp.Rational(-8, 3))

t = sp.Matrix([1, 2, -1, 3])
s = sp.Matrix([-2, 0, 4, 1])
c = sp.simplify(M_LOX.inv() * (s - t))
check("PURE_TRANSLATION_TRANSITIVE",
      sp.simplify(t + M_LOX * c - s) == sp.zeros(4, 1))

# Observer-positive or Lorentz norms are therefore not translation invariant
# on the generic stratum: the same affine orbit reaches vectors with different
# norms.
check("EUCLIDEAN_OBSERVER_NORM_CHANGES",
      (t.T * t)[0] != (s.T * s)[0])
check("LORENTZ_NORM_CHANGES",
      (t.T * ETA * t)[0] != (s.T * ETA * s)[0])

# Open torsion has T' = T - F c_far for a pure translation.  With square-B
# linear map I, F=P-I is invertible on the same loxodromic control.
F = P_LOX - I4
T = sp.Matrix([2, -1, 3, 4])
c_far = sp.simplify(F.inv() * T)
check("OPEN_TORSION_GENERIC_GAUGE_TO_ZERO",
      sp.simplify(T - F * c_far) == sp.zeros(4, 1))

# ---------------------------------------------------------------------------
# Explicit proper-Lorentz path approaching the singular identity
# ---------------------------------------------------------------------------

q = sp.symbols("q")
ch = (1 + q**2) / (1 - q**2)
sh = 2*q / (1 - q**2)
co = (1 - q**2) / (1 + q**2)
si = 2*q / (1 + q**2)

Pq = sp.Matrix([
    [ch, sh, 0, 0],
    [sh, ch, 0, 0],
    [0, 0, co, si],
    [0, 0, -si, co],
])

check("RATIONAL_PATH_LORENTZ",
      sp.simplify(Pq.T * ETA * Pq - ETA) == sp.zeros(4))
check("RATIONAL_PATH_ID_AT_ZERO", Pq.subs(q, 0) == I4)
check("RATIONAL_PATH_DET_I_MINUS_P",
      sp.factor((I4 - Pq).det())
      == 16*q**4 / ((q - 1)*(q + 1)*(q**2 + 1)))

# ---------------------------------------------------------------------------
# Homogeneous affine matrix polynomial invariants are translation blind
# ---------------------------------------------------------------------------

def affine_matrix(P, t):
    H = sp.eye(5)
    H[:4, :4] = P
    H[:4, 4] = t
    return H

H = affine_matrix(P_LOX, t)
for k in range(1, 6):
    check("AFFINE_TRACE_TRANSLATION_BLIND_" + str(k),
          sp.simplify(sp.trace(H**k) - (sp.trace(P_LOX**k) + 1)) == 0)

# ---------------------------------------------------------------------------
# Two-holonomy polynomial residual
# ---------------------------------------------------------------------------

def joint_residual(P1, t1, P2, t2):
    M1 = I4 - P1
    M2 = I4 - P2
    d1 = sp.factor(M1.det())
    qsharp = sp.simplify(M1.adjugate() * t1)
    return sp.simplify(d1 * t2 - M2 * qsharp)

P1 = P_LOX
P2 = sp.simplify(RBC * BOOST * RBC.inv())
t1 = sp.Matrix([1, 2, 0, -1])
t2 = sp.Matrix([0, -1, 3, 2])

g = sp.simplify(RBC * BOOST)
c0 = sp.Matrix([sp.Rational(1, 2), -1, sp.Rational(2, 3), 1])
check("CONJUGATING_G_LORENTZ", g.T * ETA * g == ETA)

R = joint_residual(P1, t1, P2, t2)

P1p = sp.simplify(g * P1 * g.inv())
P2p = sp.simplify(g * P2 * g.inv())
t1p = sp.simplify(g * t1 + (I4 - P1p) * c0)
t2p = sp.simplify(g * t2 + (I4 - P2p) * c0)

Rp = joint_residual(P1p, t1p, P2p, t2p)
check("JOINT_RESIDUAL_FULL_AFFINE_COVARIANCE",
      sp.simplify(Rp - g * R) == sp.zeros(4, 1))
check("JOINT_RESIDUAL_LORENTZ_NORM_INVARIANT",
      sp.simplify((Rp.T * ETA * Rp)[0] - (R.T * ETA * R)[0]) == 0)

# Anchor inversion keeps its affine fixed-point numerator on this generic
# control.  Target inversion transports R by -P2^-1, preserving its norm.
def affine_inverse(P, t):
    Pi = P.inv()
    return Pi, sp.simplify(-Pi * t)

P1i, t1i = affine_inverse(P1, t1)
M1 = I4 - P1
M1i = I4 - P1i
qsharp = sp.simplify(M1.adjugate() * t1)
qsharp_i = sp.simplify(M1i.adjugate() * t1i)
check("ANCHOR_REVERSAL_FIXED_POINT_NUMERATOR", qsharp_i == qsharp)

P2i, t2i = affine_inverse(P2, t2)
R_target_inv = joint_residual(P1, t1, P2i, t2i)
check("TARGET_REVERSAL_RESIDUAL",
      sp.simplify(R_target_inv + P2.inv() * R) == sp.zeros(4, 1))
check("TARGET_REVERSAL_NORM",
      sp.simplify((R_target_inv.T * ETA * R_target_inv)[0]
                  - (R.T * ETA * R)[0]) == 0)

# ---------------------------------------------------------------------------
# Exact L=2 nongauge edge-shift witness from the relative-solder frontier
# ---------------------------------------------------------------------------

SITES = list(product(range(2), repeat=4))
SITE_INDEX = {x: i for i, x in enumerate(SITES)}
origin = (0, 0, 0, 0)

def site_add(x, r):
    y = list(x)
    y[r] ^= 1
    return tuple(y)

links = {(x, r): I4 for x in SITES for r in range(4)}
links[(origin, 0)] = BOOST
links[(origin, 1)] = RBC
links[((1, 0, 0, 0), 2)] = RCD

zero_b = {(x, r): sp.zeros(4, 1) for x in SITES for r in range(4)}

def acomp(A, B):
    L1, b1 = A
    L2, b2 = B
    return sp.simplify(L1 * L2), sp.simplify(b1 + L1 * b2)

def ainv(A):
    L, b = A
    Li = L.inv()
    return Li, sp.simplify(-Li * b)

def alink(x, r, bfield):
    return links[(x, r)], bfield[(x, r)]

def square_a(x, r, s, bfield):
    return acomp(alink(x, r, bfield), alink(site_add(x, r), s, bfield))

def square_b(x, r, s, bfield):
    return acomp(alink(x, s, bfield), alink(site_add(x, s), r, bfield))

def based_holonomy(x, r, s, bfield):
    return acomp(square_a(x, r, s, bfield),
                 ainv(square_b(x, r, s, bfield)))

# Before the nongauge edge shift all affine shifts are zero, so both loop
# translations vanish and the joint residual is zero.
P02_0, t02_0 = based_holonomy(origin, 0, 2, zero_b)
P01_0, t01_0 = based_holonomy(origin, 0, 1, zero_b)
R0 = joint_residual(P02_0, t02_0, P01_0, t01_0)
check("L2_BASE_JOINT_RESIDUAL_ZERO", R0 == sp.zeros(4, 1))

# Add a single target-fibre edge shift u to b_(origin,A).  The preceding
# frontier showed the matched (Theta,b) change leaves relative solder/action
# unchanged.  We now test that the joint affine holonomy sees it.
b1 = {k: sp.Matrix(v) for k, v in zero_b.items()}
b1[(origin, 0)] = sp.Matrix([1, 0, 0, 0])

P02, t02 = based_holonomy(origin, 0, 2, b1)
P01, t01 = based_holonomy(origin, 0, 1, b1)

check("L2_ANCHOR_I_MINUS_P_INVERTIBLE",
      sp.factor((I4 - P02).det()) == sp.Rational(-8, 3))

R1 = joint_residual(P02, t02, P01, t01)
check("L2_JOINT_RESIDUAL_VECTOR",
      R1 == sp.Matrix([
          sp.Rational(-32, 9),
          sp.Rational(-40, 9),
          sp.Rational(8, 3),
          0,
      ]))
check("L2_JOINT_RESIDUAL_LORENTZ_NORM",
      sp.simplify((R1.T * ETA * R1)[0]) == sp.Rational(-128, 9))
check("L2_JOINT_RESIDUAL_DETECTS_EDGE_SHIFT", R1 != R0)

# Prove the one-edge shift is not a node-gauge image for this curved linear
# connection: D_L has rank 64; appending u raises rank to 65.
def covariant_node_difference_matrix():
    M = sp.zeros(len(SITES) * 4 * 4, len(SITES) * 4)
    row = 0
    for x in SITES:
        for r in range(4):
            y = site_add(x, r)
            for a in range(4):
                M[row, SITE_INDEX[x]*4 + a] = 1
                for bb in range(4):
                    M[row, SITE_INDEX[y]*4 + bb] -= links[(x, r)][a, bb]
                row += 1
    return M

DL = covariant_node_difference_matrix()
u = sp.zeros(256, 1)
row = 0
for x in SITES:
    for r in range(4):
        for a in range(4):
            if x == origin and r == 0 and a == 0:
                u[row] = 1
            row += 1

check("L2_NODE_DIFFERENCE_RANK_64", DL.rank() == 64)
check("L2_ONE_EDGE_SHIFT_NONGAUGE", DL.row_join(u).rank() == 65)

print("RESULT_SINGLE_LOOP: continuous full-affine single-holonomy scalars are translation-blind.")
print("RESULT_OPEN_TORSION: generic invertible curvature makes open torsion translation-transitive as well.")
print("RESULT_TWO_LOOP: R_{2|1}=det(I-P1)t2-(I-P2)adj(I-P1)t1 is a polynomial affine-covariant vector.")
print("RESULT_WITNESS: the two-loop residual detects the exact nongauge one-edge shift missed by relative solder.")
print("RESULT: SINGLE-PLAQUETTE-AFFINE-TRANSLATION-SCALAR-NOGO-IN-CONTINUOUS-CLASS")
print("SURVIVOR: JOINT-TWO-HOLONOMY-TRANSLATION-RESIDUAL")
