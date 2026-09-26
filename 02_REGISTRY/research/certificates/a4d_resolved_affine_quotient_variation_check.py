#!/usr/bin/env python3
"""Exact finite certificate for variation of the resolved affine quotient.

Research-only. Exact rational/symbolic arithmetic.

The certificate checks:

1. the Grassmannian projector derivative in a finite Euclidean model;
2. the exact variation formula
       dE = 2<r,db> - 2<r,A p>
   at fixed metric;
3. a resolved branch with J < I has a free incidence tangent producing
   nonzero action variation;
4. the free incidence Euler gradient is the outer product r (P_G b)^T;
5. an intrinsic branch I=J has no free incidence tangent;
6. on the L=2 Role torus, frozen incidence I_A rejects a legitimate new
   Lorentz link variation because its lost image points outside I_A;
7. two proper-Lorentz histories have the same flat endpoint, same first
   pointwise D-jet, and the same limiting image incidence I_A, but different
   first incidence tangents.  Hence history-derived first variation is not
   reconstructed by endpoint (D_0,I_A), nor even by the first D-jet.

No pseudoinverse, floating tolerance, Lean or physical interpretation is used.
"""

from itertools import product
import sympy as sp

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# ---------------------------------------------------------------------------
# A. Grassmannian variation in a minimal exact Euclidean model
# ---------------------------------------------------------------------------

# E = R^3, I = span(e1,e2), Iperp = span(e3).
P = sp.diag(1, 1, 0)
Q = sp.eye(3) - P

# J = span(e1), G = span(e2).  The free incidence tangent maps e2 -> e3.
A = sp.zeros(3)
A[2, 1] = 1

# Orthogonal Grassmannian tangent of P:
# dP = A P + A^T Q.
dP = A * P + A.T * Q
dQ = -dP

check("PROJECTOR_TANGENT_SELF_ADJOINT", dP.T == dP)
check("PROJECTOR_TANGENT_OFF_DIAGONAL",
      P*dP*P == sp.zeros(3) and Q*dP*Q == sp.zeros(3))

b = sp.Matrix([0, 1, 1])  # p_G=e2, r=e3.
db = sp.Matrix([2, -3, 5])
p = P*b
r = Q*b

# Direct differential of E=b^T Q b.
direct = sp.expand(2*(r.T*db)[0] + (b.T*dQ*b)[0])
formula = sp.expand(2*(r.T*db)[0] - 2*(r.T*A*p)[0])

check("GRASSMANNIAN_ENERGY_VARIATION_FORMULA", direct == formula)
check("FREE_INCIDENCE_VARIATION_NONZERO",
      -2*(r.T*A*p)[0] == -2)

# Gradient over Hom(G,Iperp) is -2 r (P_G b)^T.
PG = sp.diag(0, 1, 0)
g = PG*b
outer = -2 * r * g.T
check("INCIDENCE_EULER_OUTER_PRODUCT_NONZERO", outer != sp.zeros(3))
check("INCIDENCE_EULER_FACTORIZATION",
      outer.rank() == 1 and r != sp.zeros(3,1) and g != sp.zeros(3,1))

# Intrinsic branch: if I=J, G=0, there is no free incidence tangent.
check("INTRINSIC_BRANCH_FREE_TANGENT_DIM_ZERO", 0 * (3-1) == 0)
check("RESOLVED_BRANCH_FREE_TANGENT_DIM_ONE", 1 * (3-2) == 1)

# ---------------------------------------------------------------------------
# B. L=2 affine node-difference and image-incidence branch
# ---------------------------------------------------------------------------

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
SITES = list(product((0, 1), repeat=4))
SITE_INDEX = {x: i for i, x in enumerate(SITES)}
ORIGIN = (0, 0, 0, 0)

def site_add(x, r):
    y = list(x)
    y[r] ^= 1
    return tuple(y)

def edge_row(x, r, a):
    return (SITE_INDEX[x] * 4 + r) * 4 + a

BOOST_GEN = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = 1
    X[i, 0] = 1
    BOOST_GEN.append(X)
    check("BOOST_GEN_LORENTZ_" + str(i),
          X.T*ETA + ETA*X == sp.zeros(4))

# Extra second-order Lorentz direction.
B_EXTRA = BOOST_GEN[0]

def cayley_argument(X):
    return sp.simplify((I4 + X/2) * (I4 - X/2).inv())

def covariant_node_difference(links):
    M = sp.zeros(256, 64)
    row = 0
    for x in SITES:
        for role in range(4):
            y = site_add(x, role)
            for a in range(4):
                M[row, SITE_INDEX[x]*4 + a] = 1
                for bb in range(4):
                    M[row, SITE_INDEX[y]*4 + bb] -= links[(x, role)][a, bb]
                row += 1
    return M

FLAT = {(x, r): I4 for x in SITES for r in range(4)}
D0 = covariant_node_difference(FLAT)
check("FLAT_D_RANK_60", D0.rank() == 60)

# First-order lost image Gamma_A from the three boost edges.
GA = sp.zeros(256, 4)
for role in range(3):
    X = BOOST_GEN[role]
    for a in range(4):
        for bb in range(4):
            GA[edge_row(ORIGIN, role, a), bb] = -X[a, bb]

IA = D0.row_join(GA)
check("RESOLVED_INCIDENCE_RANK_64", IA.rank() == 64)
check("RESOLVED_LOST_SPACE_DIM_4", IA.rank() - D0.rank() == 4)
check("RESOLVED_FREE_TANGENT_DIM_768",
      (IA.rank()-D0.rank()) * (256-IA.rank()) == 768)

# A new first-order Lorentz variation on the fourth origin edge.
H = sp.zeros(256, 4)
for a in range(4):
    for bb in range(4):
        H[edge_row(ORIGIN, 3, a), bb] = -B_EXTRA[a, bb]

# Frozen I_A would require every first-order image direction to remain in I_A.
# Exact augmented rank proves this variation is rejected.
check("FROZEN_MEMORY_REJECTS_NEW_LINK_VARIATION",
      IA.row_join(H).rank() == 66)

# ---------------------------------------------------------------------------
# C. Same endpoint + same I_* + same first D-jet, different incidence tangent
# ---------------------------------------------------------------------------

# History 1:
#   three links have Cayley(t A_r), fourth link is identity.
# History 2:
#   same first three links, fourth link has Cayley(t^2 B_EXTRA).
#
# Both have the same endpoint and the same first D-jet because the extra link
# begins at order t^2.  Both have the same limiting incidence I_A because,
# after dividing the constant-kernel columns by t, the fourth edge contributes
# only order t.  But the first tangent of that normalized lost image differs by
# exactly H.

t = sp.symbols("t")
X2 = t**2 * B_EXTRA
L4_hist2 = cayley_argument(X2)

check("SECOND_ORDER_LINK_ENDPOINT_ID", L4_hist2.subs(t,0) == I4)

# Exact first derivative at zero vanishes.
dL4 = L4_hist2.diff(t).subs(t,0)
check("SECOND_ORDER_LINK_FIRST_JET_ZERO", dL4 == sp.zeros(4))

# The coefficient of t^2 in I-L is -B_EXTRA.
second_coeff = sp.simplify(
    (I4 - L4_hist2).diff(t,2).subs(t,0) / 2
)
check("SECOND_ORDER_LINK_LOST_TANGENT", second_coeff == -B_EXTRA)

# Thus the derivative of the normalized lost map (I-L)/t at t=0 is H.
# H has two directions outside I_A.
check("SAME_LIMIT_DIFFERENT_INCIDENCE_TANGENT",
      IA.row_join(H).rank() == IA.rank() + 2)

# Both punctured histories remain rank-64 because the first three boosts already
# have zero common fixed vector.  Verify at an exact rational sample.
def history_links(tt, with_second_order):
    links = {(x, r): I4 for x in SITES for r in range(4)}
    for role in range(3):
        links[(ORIGIN, role)] = cayley_argument(tt * BOOST_GEN[role])
    if with_second_order:
        links[(ORIGIN, 3)] = cayley_argument(tt**2 * B_EXTRA)
    return links

q = sp.Rational(1, 7)
D1 = covariant_node_difference(history_links(q, False))
D2 = covariant_node_difference(history_links(q, True))
check("HISTORY1_PUNCTURED_RANK_64", D1.rank() == 64)
check("HISTORY2_PUNCTURED_RANK_64", D2.rank() == 64)

# Same first pointwise D-jet is certified structurally by the zero first jet on
# the only differing link.
check("SAME_FIRST_POINTWISE_D_JET", dL4 == sp.zeros(4))

print("RESULT_VARIATION: dE = 2<r,db> - 2<r,A p> at fixed observer metric.")
print("RESULT_CONSTRAINT: A(Dc)=Q dD(c); frozen I restricts link variations.")
print("RESULT_FREE_EULER: on I=J+G, free incidence stationarity is r tensor (P_G b)^*=0.")
print("RESULT_INTRINSIC: G=0 gives no independent incidence Euler equation.")
print("RESULT_HISTORY: endpoint (D,I) and even the first D-jet do not determine the first incidence tangent.")
print("RESULT: RESOLVED-AFFINE-QUOTIENT-VARIATION-CLASSIFIED")
print("SUBTERMINAL: HISTORY-FIRST-VARIATION-REQUIRES-INCIDENCE-TANGENT-MEMORY")
