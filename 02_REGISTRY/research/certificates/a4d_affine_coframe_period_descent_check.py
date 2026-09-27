#!/usr/bin/env python3
"""Exact finite controls for EXP-A4D-AFFINE-COFRAME-PERIOD-DESCENT.

Separates:
1) the period-generic raw coframe differential d_f;
2) its centered metric tangent;
3) descent of the observer-completed affine translation to quotient coordinates.

This does NOT claim affine translations are a gauge symmetry of the star action.
"""

from itertools import product
import sympy as sp

I = sp.I
ETA = sp.diag(1, -1, -1, -1)
SYM = [(a, b) for a in range(4) for b in range(a, 4)]


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def coframe_symbol(L, z):
    """16x4 symbol e_(r,a)=L*(z_r-1)*v_a."""
    M = sp.zeros(16, 4)
    for r in range(4):
        f = sp.expand(L * (z[r] - 1))
        for a in range(4):
            M[4 * r + a, a] = f
    return M


def centered_metric_symbol(L, z):
    """10x4 centered parent/readout of d_f. This is NOT the J2 quotient Q."""
    d = [sp.simplify(sp.Rational(L, 2) * (zr - 1 / zr)) for zr in z]
    M = sp.zeros(10, 4)
    for row, (a, b) in enumerate(SYM):
        if a == b:
            M[row, a] = 2 * d[a]
        else:
            M[row, b] = d[a]
            M[row, a] = d[b]
    return M


def raw_q_symbol(L, z):
    """10x4 tangent of the actual J2 quotient Q=Theta*eta*Theta^T."""
    M = sp.zeros(10, 4)
    for j in range(4):
        xi = sp.eye(4)[:, j]
        H = sp.zeros(4)
        for r in range(4):
            for a in range(4):
                H[r, a] = L * (z[r] - 1) * xi[a]
        q = sp.expand(H * ETA + ETA * H.T)
        for row, (a, b) in enumerate(SYM):
            M[row, j] = q[a, b]
    return M


roots2 = (sp.Integer(1), sp.Integer(-1))
roots4 = (sp.Integer(1), I, sp.Integer(-1), -I)

l2_raw = {}
l2_metric = {}
for z in product(roots2, repeat=4):
    l2_raw[z] = coframe_symbol(2, z).rank()
    l2_metric[z] = centered_metric_symbol(2, z).rank()

check("L2_RAW_TRIVIAL_RANK0", l2_raw[(1, 1, 1, 1)] == 0)
check(
    "L2_RAW_15_NONTRIVIAL_RANK4",
    sum(r == 4 for z, r in l2_raw.items() if z != (1, 1, 1, 1)) == 15,
)
check("L2_GLOBAL_RAW_RANK60", sum(l2_raw.values()) == 60)
check("L2_CENTERED_METRIC_ALL_ZERO", set(l2_metric.values()) == {0})
l2_q = {z: raw_q_symbol(2, z).rank() for z in product(roots2, repeat=4)}
check("L2_RAW_Q_TRIVIAL_RANK0", l2_q[(1, 1, 1, 1)] == 0)
check("L2_RAW_Q_15_NONTRIVIAL_RANK4",
      sum(r == 4 for z, r in l2_q.items() if z != (1, 1, 1, 1)) == 15)

l4_raw = {}
l4_metric = {}
for z in product(roots4, repeat=4):
    l4_raw[z] = coframe_symbol(4, z).rank()
    l4_metric[z] = centered_metric_symbol(4, z).rank()

check("L4_RAW_TRIVIAL_RANK0", l4_raw[(1, 1, 1, 1)] == 0)
check(
    "L4_RAW_255_NONTRIVIAL_RANK4",
    sum(r == 4 for z, r in l4_raw.items() if z != (1, 1, 1, 1)) == 255,
)
l4_q = {z: raw_q_symbol(4, z).rank() for z in product(roots4, repeat=4)}
check("L4_RAW_Q_TRIVIAL_RANK0", l4_q[(1, 1, 1, 1)] == 0)
check("L4_RAW_Q_255_NONTRIVIAL_RANK4",
      sum(r == 4 for z, r in l4_q.items() if z != (1, 1, 1, 1)) == 255)
check(
    "L4_CENTERED_METRIC_RANK_COUNTS",
    sum(r == 0 for r in l4_metric.values()) == 16
    and sum(r == 4 for r in l4_metric.values()) == 240,
)

fibres = {}
for z in product(roots4, repeat=4):
    eps = tuple(sp.simplify(x * x) for x in z)
    fibres.setdefault(eps, []).append(z)

check("SQUARE_MAP_16_FIBRES", len(fibres) == 16)
check("EVERY_SQUARE_FIBRE_SIZE16", all(len(v) == 16 for v in fibres.values()))

alt = (-1, -1, -1, -1)
check("ALTERNATING_FIBRE_HAS_DIAGONAL", (I, I, I, I) in fibres[alt])
check("ALTERNATING_FIBRE_HAS_MIXED", (I, I, -I, -I) in fibres[alt])

for eps, zs in fibres.items():
    if eps == (1, 1, 1, 1):
        check("CENTERED_READOUT_TRIVIAL_FIBRE_RANK0", all(l4_metric[z] == 0 for z in zs))
    else:
        if not all(l4_metric[z] == 4 for z in zs):
            raise AssertionError("CENTERED_READOUT_NONTRIVIAL_FIBRE_RANK4")
check("CENTERED_READOUT_NONTRIVIAL_SQUARE_ROOTS_RANK4", True)

# Exact observer-dependence witness for the already-owned observer-completed
# affine solder representation.
n0 = sp.Matrix([1, 0, 0, 0])
G = sp.Matrix(
    [
        [sp.Rational(5, 3), sp.Rational(4, 3), 0, 0],
        [sp.Rational(4, 3), sp.Rational(5, 3), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
n1 = G * n0

check("RATIONAL_BOOST_LORENTZ", sp.simplify(G.T * ETA * G) == ETA)
check("RATIONAL_BOOST_DET1", sp.simplify(G.det()) == 1)
check(
    "OBSERVERS_UNIT_TIMELIKE",
    sp.simplify((n0.T * ETA * n0)[0]) == 1
    and sp.simplify((n1.T * ETA * n1)[0]) == 1,
)


def observer_flat(n):
    nf = ETA * n
    return sp.simplify(-ETA + 2 * nf * nf.T)


H0 = observer_flat(n0)
H1 = observer_flat(n1)
check("REST_OBSERVER_FLAT_IS_I", H0 == sp.eye(4))
check("BOOSTED_OBSERVER_FLAT_DIFFERS", H1 != H0)

tau = sp.Matrix([1, 0, 0, 0])


def translated_theta(H):
    T = ETA.copy()
    row = tau.T * H
    for j in range(4):
        T[0, j] += row[0, j]
    return T


T0 = translated_theta(H0)
T1 = translated_theta(H1)
Q0 = sp.simplify(T0 * ETA * T0.T)
Q1 = sp.simplify(T1 * ETA * T1.T)

check("OBSERVER_CHANGES_TRANSLATED_Q", Q0 != Q1)
check("REST_TRANSLATED_Q_EXACT", Q0 == sp.diag(4, -1, -1, -1))
check(
    "BOOSTED_TRANSLATED_Q_EXACT",
    Q1
    == sp.Matrix(
        [
            [sp.Rational(100, 9), -sp.Rational(40, 9), 0, 0],
            [-sp.Rational(40, 9), -1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, -1],
        ]
    ),
)

print("RESULT RAW_DF_PERIOD_GENERIC: L2 rank 60 is 15 rank-4 nontrivial characters.")
print("RESULT SQUARE_FIBRE: coordinatewise squaring is 16-to-1 and does not select the diagonal quarter-wave.")
print("RESULT READOUT_FIREWALL: centered coframeMetricReadout is L2-invisible but is NOT the J2 quotient Q.")
print("RESULT RAW_Q: actual J2 quotient dQ has rank 4 on every nontrivial L2 and L4 forward-coframe character.")
print("RESULT QK_DESCENT_BLOCKER: observer-completed affine translation is not a function of starting (Q,K) alone because translated Q depends on observer data.")
print("BOUNDARY: no claim that affine translations are a gauge symmetry of the selected star action.")
