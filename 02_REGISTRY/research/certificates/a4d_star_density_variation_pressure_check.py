#!/usr/bin/env python3
"""Exact L=2 pressure test for the selected A4D star linear-curvature density.

Research-only certificate.  It expands the accepted finite density to quadratic
order around flat nondegenerate solder and identity Lorentz links, momentum by
momentum on the period-two four-Role torus.

It checks:
  * the connection block is algebraically eliminable (rank 24);
  * the full Hessian is not a boundary/zero action;
  * the 10 expected flat gauge tangents (6 local Lorentz + 4 forward-coframe)
    exhaust the generic nonzero-momentum kernel;
  * exactly the three nonzero Lorentz-null checkerboard momenta acquire two
    additional quotient null directions;
  * the naive finite forward torsion equation is NOT identical to the actual
    connection Euler equation at finite L=2.

No continuum Einstein/time/wave interpretation is encoded here.
"""

from itertools import combinations, product
import sympy as sp

PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)

def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)

# Lorentz tangent basis for X^T eta + eta X = 0.
LORENTZ = []
for i in (1, 2, 3):
    X = sp.zeros(4)
    X[0, i] = 1
    X[i, 0] = 1
    LORENTZ.append(X)
for i, j in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[i, j] = 1
    X[j, i] = -1
    LORENTZ.append(X)

for X in LORENTZ:
    check("LORENTZ_TANGENT", X.T * ETA + ETA * X == sp.zeros(4))

# Metric induced on Lambda^2 and the accepted Lorentz middle-degree star.
G2 = sp.zeros(6)
for i, (a, b) in enumerate(PAIRS):
    G2[i, i] = ETA[a, a] * ETA[b, b]

STAR = sp.zeros(6)
STAR_MAP = {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}
for p, (q, s) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = s
check("STAR_SQUARE_MINUS_ID", STAR * STAR == -sp.eye(6))

def wedge_vec(u, v):
    out = sp.zeros(6, 1)
    for i, (a, b) in enumerate(PAIRS):
        out[i] = u[a] * v[b] - u[b] * v[a]
    return out

def bivector_of_tangent(X):
    Y = X * ETA
    return sp.Matrix([Y[a, b] for a, b in PAIRS])

def complement_orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1

# Truncated t^2 matrix jets.
def mul_jet(X, Y):
    return (
        X[0] * Y[0],
        X[0] * Y[1] + X[1] * Y[0],
        X[0] * Y[2] + X[1] * Y[1] + X[2] * Y[0],
    )

def exp_link(A, scale=1, inverse=False):
    B = scale * A
    return (sp.eye(4), -B if inverse else B, B * B / 2)

def quadratic_density(amplitudes, signs):
    """Coefficient of t^2 in one-site density for one L=2 momentum character.

    amplitudes = 16 solder-leg perturbations + 24 Lorentz-link amplitudes.
    Since every L=2 character squares to one, the periodic site sum differs only
    by the positive factor 16 and has the same rank/kernel.
    """
    h = [sp.Matrix(amplitudes[4 * r:4 * r + 4]) for r in range(4)]
    A = []
    offset = 16
    for r in range(4):
        X = sp.zeros(4)
        for k, B in enumerate(LORENTZ):
            X += amplitudes[offset + 6 * r + k] * B
        A.append(X)

    basis = [sp.eye(4)[:, r] for r in range(4)]
    total = sp.Integer(0)

    for r, s in PAIRS:
        # Based plaquette:
        # P = L_r(x) L_s(x+r) L_r(x+s)^(-1) L_s(x)^(-1).
        P = (sp.eye(4), sp.zeros(4), sp.zeros(4))
        P = mul_jet(P, exp_link(A[r]))
        P = mul_jet(P, exp_link(A[s], signs[r]))
        P = mul_jet(P, exp_link(A[r], signs[s], inverse=True))
        P = mul_jet(P, exp_link(A[s], inverse=True))

        P1, P2 = P[1], P[2]
        # R(P)=1/2(P-P^{-1}) has jets R1=P1, R2=P2-P1^2/2.
        R1 = P1
        R2 = P2 - P1 * P1 / 2

        C1 = bivector_of_tangent(R1)
        C2 = bivector_of_tangent(R2)

        u, v = [i for i in range(4) if i not in (r, s)]
        B0 = wedge_vec(basis[u], basis[v])
        B1 = wedge_vec(h[u], basis[v]) + wedge_vec(basis[u], h[v])

        eps = complement_orientation((r, s))
        total += eps * (
            (B0.T * G2 * STAR * C2)[0]
            + (B1.T * G2 * STAR * C1)[0]
        )
    return sp.expand(total)

def hessian(signs):
    x = sp.symbols("x0:40")
    q = quadratic_density(x, signs)
    return sp.hessian(q, x)

def gauge_matrix(signs):
    cols = []
    basis = [sp.eye(4)[:, r] for r in range(4)]

    # Local Lorentz: delta h_r = lambda e_r,
    # delta a_r = (1-chi_r) lambda.
    for k, X in enumerate(LORENTZ):
        v = []
        for r in range(4):
            v += list(X * basis[r])
        for r in range(4):
            for j in range(6):
                v.append((1 - signs[r]) if j == k else 0)
        cols.append(sp.Matrix(v))

    # Flat forward-coframe gauge tangent: delta h_r=(chi_r-1) xi, delta a=0.
    # The eta musical map is invertible, so this spans the same four directions
    # as the raw forwardGaugeCoframe field.
    for a in range(4):
        xi = sp.eye(4)[:, a]
        v = []
        for r in range(4):
            v += list((signs[r] - 1) * xi)
        v += [0] * 24
        cols.append(sp.Matrix(v))

    return sp.Matrix.hstack(*cols)

# Naive vector-valued forward torsion at flat solder:
# T_rs = (chi_r-1) h_s - (chi_s-1) h_r + a_r e_s - a_s e_r.
def torsion_matrices(signs):
    Ta = sp.zeros(24, 24)
    Th = sp.zeros(24, 16)
    basis = [sp.eye(4)[:, r] for r in range(4)]
    row = 0
    for r, s in PAIRS:
        for c in range(4):
            Th[row, 4 * s + c] += signs[r] - 1
            Th[row, 4 * r + c] -= signs[s] - 1
            for k, X in enumerate(LORENTZ):
                Ta[row, 6 * r + k] += (X * basis[s])[c]
                Ta[row, 6 * s + k] -= (X * basis[r])[c]
            row += 1
    return Ta, Th

records = []
nonzero_seen = False
null_shells = []
torsion_mismatch_witnesses = []

for signs in product((1, -1), repeat=4):
    H = hessian(signs)
    Haa = H[16:, 16:]
    rank_H = H.rank()
    rank_A = Haa.rank()
    check("CONNECTION_BLOCK_RANK_24_" + "".join("P" if s == 1 else "M" for s in signs),
          rank_A == 24)

    # Since Haa is invertible, Schur rank = rank(H)-24.
    rank_eff = rank_H - 24

    if signs == (1, 1, 1, 1):
        check("ZERO_MOMENTUM_EFFECTIVE_RANK_0", rank_eff == 0)
        records.append((signs, rank_H, rank_eff, 0, 0))
        continue

    nonzero_seen = True
    G = gauge_matrix(signs)
    check("GAUGE_RANK_10_" + "".join("P" if s == 1 else "M" for s in signs),
          G.rank() == 10)
    check("GAUGE_IS_HESSIAN_NULL_" + "".join("P" if s == 1 else "M" for s in signs),
          H * G == sp.zeros(40, 10))

    # Discrete momentum magnitude kappa_r = 1-chi_r; scale factors do not alter
    # the null condition.  eta=(+---).
    kappa = [1 - s for s in signs]
    lorentz_norm = (
        kappa[0] ** 2 - kappa[1] ** 2 - kappa[2] ** 2 - kappa[3] ** 2
    )
    is_null = lorentz_norm == 0

    quotient_kernel = (40 - rank_H) - 10
    if is_null:
        null_shells.append(signs)
        check("NULL_SECTOR_FULL_RANK_28_" + "".join("P" if s == 1 else "M" for s in signs),
              rank_H == 28)
        check("NULL_SECTOR_EFFECTIVE_RANK_4_" + "".join("P" if s == 1 else "M" for s in signs),
              rank_eff == 4)
        check("NULL_SECTOR_QUOTIENT_KERNEL_2_" + "".join("P" if s == 1 else "M" for s in signs),
              quotient_kernel == 2)
    else:
        check("GENERIC_FULL_RANK_30_" + "".join("P" if s == 1 else "M" for s in signs),
              rank_H == 30)
        check("GENERIC_EFFECTIVE_RANK_6_" + "".join("P" if s == 1 else "M" for s in signs),
              rank_eff == 6)
        check("GENERIC_KERNEL_EQUALS_GAUGE_" + "".join("P" if s == 1 else "M" for s in signs),
              quotient_kernel == 0)

    # Compare the actual connection EL equation with the naive finite torsion.
    Ta, Th = torsion_matrices(signs)
    check("NAIVE_TORSION_CONNECTION_MAP_RANK_24_" + "".join("P" if s == 1 else "M" for s in signs),
          Ta.rank() == 24)

    Hah = H[16:, :16]
    # EL_a = Haa a + Hah h.
    # If this were exactly an invertible recombination of T=Ta a+Th h, then
    # Hah == Haa Ta^{-1} Th.
    mismatch = sp.simplify(Hah - Haa * Ta.inv() * Th)
    mismatch_rank = mismatch.rank()
    if mismatch_rank:
        torsion_mismatch_witnesses.append((signs, mismatch_rank))

    records.append((signs, rank_H, rank_eff, quotient_kernel, mismatch_rank))

check("ACTION_HESSIAN_NONZERO", nonzero_seen and any(r[1] > 0 for r in records))
check("EXACTLY_THREE_NONZERO_LORENTZ_NULL_SECTORS", len(null_shells) == 3)
check("NULL_SECTORS_ARE_TIME_PLUS_ONE_SPATIAL",
      set(null_shells) == {
          (-1, -1, 1, 1),
          (-1, 1, -1, 1),
          (-1, 1, 1, -1),
      })
check("FINITE_TORSION_IDENTITY_HAS_COUNTEREXAMPLE", len(torsion_mismatch_witnesses) > 0)
check("SINGLE_DIRECTION_TORSION_MISMATCH",
      ((1, 1, 1, -1), 6) in torsion_mismatch_witnesses)

print("SUMMARY")
for r in records:
    print("SECTOR", r)
print("TORSION_MISMATCH_WITNESSES", torsion_mismatch_witnesses)
print("RESULT: dA-star density does not collapse under flat quadratic variation;")
print("RESULT: L=2 connection block is auxiliary/invertible and the flat gauge quotient is nonzero;")
print("RESULT: naive finite forward torsion is not the exact connection EL equation for this placement.")
