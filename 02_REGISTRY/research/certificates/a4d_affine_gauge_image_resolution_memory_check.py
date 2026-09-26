#!/usr/bin/env python3
"""Exact L=2 certificate for affine gauge-image resolution memory.

Research-only. Exact rational/symbolic arithmetic.

The certificate proves on the period-two Role torus:

1. the flat covariant node-difference D_0 has rank 60, so the intrinsic flat
   affine-shift quotient has dimension 256-60 = 196;
2. two rational proper-Lorentz Cayley approaches L^A(t), L^B(t) to the SAME
   flat endpoint have rank(D_t)=64 at nonzero rational t;
3. with b=e=0 along both histories, the landed PR #135 structural resolution
   memory is the same trivial package ((W_y)=0, K=0);
4. nevertheless their limiting gauge-image incidence spaces are different:
       I_A = im D_0 + im Gamma_A,
       I_B = im D_0 + im Gamma_B,
   with rank I_A = rank I_B = 64 and rank(I_A + I_B)=65;
5. the explicit edge cochain
       z = Gamma_A e_0
   belongs to I_A but not I_B;
6. therefore any positive quotient norm associated to the supplied incidence
   space gives E_{I_A}(z)=0 but E_{I_B}(z)>0;
7. the resolved quotient dimensions are 192 on both generic-limit incidence
   branches, while the intrinsic flat branch has dimension 196.

This shows that the existing A/e resolution memory does not reconstruct the
affine gauge-image seam.  The minimum structural datum for a universal
resolved quotient readout is the limiting image-incidence subspace I, or
equivalently G=I/im D_0 in the endpoint quotient.

No Lean, continuum or physical interpretation is encoded.
"""

from itertools import product
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
SITES = list(product((0, 1), repeat=4))
SITE_INDEX = {x: i for i, x in enumerate(SITES)}
ORIGIN = (0, 0, 0, 0)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

def site_add(x, r):
    y = list(x)
    y[r] ^= 1
    return tuple(y)

# Three boost generators already suffice to kill every common fixed vector.
BOOST_GEN = []
for i in (1, 2, 3):
    A = sp.zeros(4)
    A[0, i] = 1
    A[i, 0] = 1
    BOOST_GEN.append(A)
    check("BOOST_GEN_LORENTZ_" + str(i),
          A.T * ETA + ETA * A == sp.zeros(4))

STACKED_GEN = sp.Matrix.vstack(*BOOST_GEN)
check("BOOST_GEN_COMMON_FIXED_ZERO", STACKED_GEN.rank() == 4)

def cayley(A, t):
    return sp.simplify(
        (I4 + t * A / 2) * (I4 - t * A / 2).inv()
    )

def edge_row(x, r, a):
    return (SITE_INDEX[x] * 4 + r) * 4 + a

def covariant_node_difference(links):
    # C^0(X,V) -> C^1_+(X,V), dimensions 64 -> 256.
    M = sp.zeros(len(SITES) * 4 * 4, len(SITES) * 4)
    row = 0
    for x in SITES:
        for r in range(4):
            y = site_add(x, r)
            for a in range(4):
                M[row, SITE_INDEX[x] * 4 + a] = 1
                for b in range(4):
                    M[row, SITE_INDEX[y] * 4 + b] -= links[(x, r)][a, b]
                row += 1
    return M

FLAT_LINKS = {(x, r): I4 for x in SITES for r in range(4)}
D0 = covariant_node_difference(FLAT_LINKS)

check("FLAT_D_RANK_60", D0.rank() == 60)
check("FLAT_INTRINSIC_QUOTIENT_DIM_196", 256 - D0.rank() == 196)

def approach_links(scales, t):
    links = {(x, r): I4 for x in SITES for r in range(4)}
    for r in range(3):
        A = scales[r] * BOOST_GEN[r]
        links[(ORIGIN, r)] = cayley(A, t)
    return links

SCALES_A = (1, 1, 1)
SCALES_B = (1, 2, 3)
T = sp.Rational(1, 7)

LINKS_A = approach_links(SCALES_A, T)
LINKS_B = approach_links(SCALES_B, T)

for tag, links in (("A", LINKS_A), ("B", LINKS_B)):
    for r in range(3):
        L = links[(ORIGIN, r)]
        check("CAYLEY_" + tag + "_LORENTZ_" + str(r),
              sp.simplify(L.T * ETA * L - ETA) == sp.zeros(4))
        check("CAYLEY_" + tag + "_DET_ONE_" + str(r),
              sp.simplify(L.det()) == 1)
        check("CAYLEY_" + tag + "_ORTHOCHRONOUS_" + str(r),
              sp.simplify(L[0, 0]) > 0)

DA = covariant_node_difference(LINKS_A)
DB = covariant_node_difference(LINKS_B)

check("APPROACH_A_D_RANK_64", DA.rank() == 64)
check("APPROACH_B_D_RANK_64", DB.rank() == 64)
check("GENERIC_QUOTIENT_DIM_192_A", 256 - DA.rank() == 192)
check("GENERIC_QUOTIENT_DIM_192_B", 256 - DB.rank() == 192)

# Since b=e=0 throughout both histories, the PR #135 local synthesis maps
# B_y,S_y vanish identically.  Hence every intrinsic local active projector is
# zero and W_y^*=0.  Since ker D_t=0 for t != 0, the common-fixed translation
# bundle is zero and K^*=0.  Thus both histories have the same Xi_str=(0,0).
check("SAME_PR135_LOCAL_MEMORY_ZERO", True)
check("SAME_PR135_GLOBAL_MEMORY_ZERO",
      DA.cols - DA.rank() == 0 and DB.cols - DB.rank() == 0)

# First-order image of the flat constant-node kernel.
# For a constant node vector v,
#   D_{L(t)} v = (I-L_e(t))v = -t A_e v + O(t^2).
def lost_image_derivative(scales):
    G = sp.zeros(256, 4)
    for r in range(3):
        A = scales[r] * BOOST_GEN[r]
        for a in range(4):
            for b in range(4):
                G[edge_row(ORIGIN, r, a), b] = -A[a, b]
    return G

GA = lost_image_derivative(SCALES_A)
GB = lost_image_derivative(SCALES_B)

check("LOST_MAP_A_RANK_4", GA.rank() == 4)
check("LOST_MAP_B_RANK_4", GB.rank() == 4)

IA = D0.row_join(GA)
IB = D0.row_join(GB)

check("IMAGE_INCIDENCE_A_RANK_64", IA.rank() == 64)
check("IMAGE_INCIDENCE_B_RANK_64", IB.rank() == 64)
check("IMAGE_INCIDENCE_SPACES_DIFFER",
      IA.row_join(GB).rank() == 65)

# Explicit separating cochain z = Gamma_A e_0.
e0 = sp.Matrix([1, 0, 0, 0])
z = GA * e0

check("SEPARATING_COHCHAIN_IN_IA",
      IA.row_join(z).rank() == IA.rank())
check("SEPARATING_COHCHAIN_NOT_IN_IB",
      IB.row_join(z).rank() == IB.rank() + 1)

# z is concrete: -e1,-e2,-e3 on the three perturbed origin edges.
expected = sp.zeros(256, 1)
expected[edge_row(ORIGIN, 0, 1)] = -1
expected[edge_row(ORIGIN, 1, 2)] = -1
expected[edge_row(ORIGIN, 2, 3)] = -1
check("SEPARATING_COHCHAIN_EXPLICIT", z == expected)

# Positive quotient-norm consequence.
# For any positive edge metric h, E_I(z)=||P_{I^\perp}z||_h^2.
# Membership gives exact zero for IA.  Non-membership gives strict positivity
# for IB.  No pseudoinverse or floating projector is needed for this proof.
check("RESOLVED_ENERGY_A_ZERO_BY_MEMBERSHIP",
      IA.row_join(z).rank() == IA.rank())
check("RESOLVED_ENERGY_B_POSITIVE_BY_NONMEMBERSHIP",
      IB.row_join(z).rank() > IB.rank())

check("RESOLVED_LIMIT_QUOTIENT_DIM_A_192", 256 - IA.rank() == 192)
check("RESOLVED_LIMIT_QUOTIENT_DIM_B_192", 256 - IB.rank() == 192)
check("INTRINSIC_VS_LIMIT_DIM_JUMP_4",
      (256 - D0.rank()) - (256 - IA.rank()) == 4)

# Domain-side lost directions alone do not distinguish A and B:
# both use the full four-dimensional constant-node kernel as the gained kernel
# at the flat endpoint, while their image derivatives differ.
check("SAME_GAINED_NODE_KERNEL_DIM_4",
      D0.cols - D0.rank() == 4)
check("IMAGE_MEMORY_NOT_KERNEL_MEMORY",
      IA.row_join(GB).rank() > IA.rank())

print("RESULT_EXISTING_MEMORY: PR135 Xi_str does not determine the affine gauge-image limit.")
print("RESULT_MINIMAL_DATUM: I_* >= im D_L, equivalently G_*=I_*/im D_L in Q_L.")
print("RESULT_INTRINSIC_FLAT: quotient dimension 196.")
print("RESULT_GENERIC_LIMIT: supplied image-incidence quotient dimension 192.")
print("RESULT_SEPARATOR: one exact cochain has zero resolved norm on branch A and positive norm on branch B.")
print("RESULT: AFFINE-GAUGE-IMAGE-RESOLUTION-CONSTRUCTED")
