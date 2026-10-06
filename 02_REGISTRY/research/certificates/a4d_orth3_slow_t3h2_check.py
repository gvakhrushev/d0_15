#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=1500
"""Exact full-lattice Orth3 mixed coefficients on the #275 Euler carrier.

Rebuilds the real-COS ray u=(0,0,1,1), its owned t^2 logarithmic
correction, and the #241 solder S_h=I+h(alpha*eta/2)^T. It computes the
complete 96-row connection and 40-row metric coefficients at t^3 h and t^3 h^2,
then tests them against the exact left kernel of the canonical flat operator.
The reproduced t^3 h source has a nonzero Fredholm class, so t^3 h^2 is only
the raw coefficient of the uncorrected ansatz, not a stationary continuation.
All arithmetic is exact over Q.
"""
from __future__ import annotations

import json
import hashlib
from functools import lru_cache
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "a4d_y_slow_joint_cross_matrices.json"
OWNER = HERE / "a4d_diagonal_microstructure_connection_stationary_slow_lift_check.py"
RESULT = HERE / "a4d_orth3_slow_t3h2_results.json"


def check(name, condition, detail=""):
    if not condition:
        raise AssertionError(name + (": " + detail if detail else ""))
    print("PASS_" + name, flush=True)


PAIR = list(combinations(range(4), 2))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIR))
STAR = sp.zeros(6)
PAIR_INDEX = {pair: i for i, pair in enumerate(PAIR)}
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1), (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), 1), (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PAIR_INDEX[dst], PAIR_INDEX[src]] = sign


def boost(j):
    out = sp.zeros(4)
    out[0, j] = out[j, 0] = 1
    return out


def rot(i, j):
    out = sp.zeros(4)
    out[i, j], out[j, i] = 1, -1
    return out


GEN = [boost(1), boost(2), boost(3), rot(1, 2), rot(1, 3), rot(2, 3)]
MS = [
    GEN[3] - GEN[4] + GEN[5],
    GEN[1] - GEN[2] + GEN[5],
    GEN[0] - GEN[2] + GEN[4],
    GEN[0] - GEN[1] + GEN[3],
]
COS = (1, 0, -1, 0)

# The exact t^2 Fourier corrections from the #260 real-COS certificate:
# r_minus[0]=r_minus[6]=r_zero[0]=r_zero[6]=1/4.
R_MINUS = [sp.zeros(4) for _ in range(4)]
R_ZERO = [sp.zeros(4) for _ in range(4)]
R_MINUS[0] = GEN[0] / 4
R_MINUS[1] = GEN[0] / 4
R_ZERO[0] = GEN[0] / 4
R_ZERO[1] = GEN[0] / 4

# The #241 shear alpha_12=alpha_21=1, represented in solder coordinates.
ALPHA = sp.zeros(4)
ALPHA[1, 2] = ALPHA[2, 1] = 1
S1 = (ALPHA * ETA / 2).T

LABELS = [(p, r, g) for p in range(4) for r in range(4) for g in range(6)]
def li(label):
    return LABELS.index(label)


# A bivariate jet is a sparse dict (degree_t, degree_h) -> 4x4 matrix.
MAX_T, MAX_H = 3, 2
ZERO = sp.zeros(4)


def jconst(matrix):
    return {(0, 0): sp.Matrix(matrix)}


def jadd(left, right):
    out = dict(left)
    for degree, value in right.items():
        out[degree] = out.get(degree, ZERO) + value
    return {degree: value for degree, value in out.items() if value != ZERO}


def jscale(scalar, jet):
    return {degree: scalar * value for degree, value in jet.items() if scalar * value != ZERO}


def jmul(left, right):
    out = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            if a + c <= MAX_T and b + d <= MAX_H:
                degree = (a + c, b + d)
                out[degree] = out.get(degree, ZERO) + x * y
    return {degree: value for degree, value in out.items() if value != ZERO}


def jexp(log):
    # Every log term has positive t-degree, so powers above three cannot
    # contribute to the requested t^3 h^2 coefficient.
    acc = jconst(I4)
    power = jconst(I4)
    for n in range(1, MAX_T + 1):
        power = jmul(power, log)
        acc = jadd(acc, jscale(sp.Rational(1, sp.factorial(n)), power))
    return acc


def lorentz_inverse(jet):
    return {degree: ETA * value.T * ETA for degree, value in jet.items()}


def phase(site):
    return sum(site) % 4


def shift(site, role, step=1):
    out = list(site)
    out[role] = (out[role] + step) % 4
    return tuple(out)


def orientation(a, b):
    rest = [j for j in range(4) if j not in (a, b)]
    seq = [a, b] + rest
    inversions = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def wedge(left, right):
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIR])


def bivector(matrix):
    lowered = matrix * ETA
    return sp.Matrix([lowered[a, b] for a, b in PAIR])


def logs_for(r1=None, r2=None):
    """Log links with the t^2 germ correction and optional t^3 h^j lifts."""
    r1 = [sp.Rational(0)] * 96 if r1 is None else list(r1)
    r2 = [sp.Rational(0)] * 96 if r2 is None else list(r2)
    logs = {}
    for role in range(4):
        for p in range(4):
            log = {}
            if COS[p] and MS[role] != ZERO:
                log[(1, 0)] = COS[p] * MS[role]
            even_correction = (-1 if p % 2 else 1) * R_MINUS[role] + R_ZERO[role]
            if even_correction != ZERO:
                log[(2, 0)] = even_correction
            cubic_h = sp.zeros(4)
            cubic_h2 = sp.zeros(4)
            for gi in range(6):
                cubic_h += r1[li((p, role, gi))] * GEN[gi]
                cubic_h2 += r2[li((p, role, gi))] * GEN[gi]
            if cubic_h != ZERO:
                log[(3, 1)] = cubic_h
            if cubic_h2 != ZERO:
                log[(3, 2)] = cubic_h2
            logs[(role, p)] = log
    return logs


def make_link_jets(logs):
    @lru_cache(None)
    def link(role, p):
        return jexp(logs[(role, p)])
    return link


def connection_coefficients(logs, order_t, order_h):
    link = make_link_jets(logs)
    solder_area = {}
    solder = I4 + sp.Symbol("h") * S1
    for a, b in PAIR:
        u, v = [j for j in range(4) if j not in (a, b)]
        cols0 = I4[:, u], I4[:, v]
        cols1 = S1[:, u], S1[:, v]
        solder_area[(a, b)] = [
            wedge(*cols0),
            wedge(cols1[0], cols0[1]) + wedge(cols0[0], cols1[1]),
            wedge(*cols1),
        ]
    out = sp.zeros(96, 1)
    for p in range(4):
        site = (p, 0, 0, 0)
        for role in range(4):
            for gi, generator in enumerate(GEN):
                total = 0
                for a, b in PAIR:
                    if role == a:
                        corners = [(site, 0), (shift(site, b, -1), 2)]
                    elif role == b:
                        corners = [(shift(site, a, -1), 1), (site, 3)]
                    else:
                        continue
                    for base_site, corner in corners:
                        places = [
                            (base_site, a, False),
                            (shift(base_site, a), b, False),
                            (shift(base_site, b), a, True),
                            (base_site, b, True),
                        ]
                        factors = []
                        for loc, rel, inverse in places:
                            current = link(rel, phase(loc))
                            factors.append(lorentz_inverse(current) if inverse else current)
                        hol = jconst(I4)
                        for factor in factors:
                            hol = jmul(hol, factor)
                        pinv = lorentz_inverse(hol)
                        varied = list(factors)
                        varied[corner] = (
                            jmul(factors[corner], jconst(generator))
                            if corner < 2 else jscale(-1, jmul(jconst(generator), factors[corner]))
                        )
                        dp = jconst(I4)
                        for factor in varied:
                            dp = jmul(dp, factor)
                        dc = jscale(sp.Rational(1, 2), jadd(dp, jmul(jmul(pinv, dp), pinv)))
                        for area_degree, area in enumerate(solder_area[(a, b)]):
                            curvature = dc.get((order_t, order_h - area_degree), ZERO)
                            if curvature != ZERO:
                                total += orientation(a, b) * (
                                    area.T * G2 * STAR * bivector(curvature)
                                )[0]
                out[li((p, role, gi))] = sp.factor(total)
    return out


def metric_coefficients(logs, order_t, order_h):
    link = make_link_jets(logs)
    out = sp.zeros(40, 1)
    solder0 = I4
    for p in range(4):
        site = (p, 0, 0, 0)
        for qi, (qa, qb) in enumerate(SYM):
            q = sp.zeros(4)
            q[qa, qb] = q[qb, qa] = 1
            variation = (q * ETA / 2).T
            total = 0
            for a, b in PAIR:
                places = [
                    (site, a, False),
                    (shift(site, a), b, False),
                    (shift(site, b), a, True),
                    (site, b, True),
                ]
                factors = []
                for loc, rel, inverse in places:
                    current = link(rel, phase(loc))
                    factors.append(lorentz_inverse(current) if inverse else current)
                hol = jconst(I4)
                for factor in factors:
                    hol = jmul(hol, factor)
                curvature = jscale(
                    sp.Rational(1, 2),
                    jadd(hol, jscale(-1, lorentz_inverse(hol))),
                )
                u, v = [j for j in range(4) if j not in (a, b)]
                dw0 = wedge(variation[:, u], solder0[:, v]) + wedge(solder0[:, u], variation[:, v])
                dw1 = wedge(variation[:, u], S1[:, v]) + wedge(S1[:, u], variation[:, v])
                for area_degree, area in enumerate((dw0, dw1)):
                    biv = curvature.get((order_t, order_h - area_degree), ZERO)
                    if biv != ZERO:
                        total += orientation(a, b) * (
                            area.T * G2 * STAR * bivector(biv)
                        )[0]
            out[10 * p + qi] = sp.factor(total)
    return out


def vector_sparse(vector, labels=LABELS):
    return [(labels[i], sp.factor(value)) for i, value in enumerate(vector) if value != 0]


def matrix_from_json(rows):
    return sp.Matrix([[sp.Rational(value) for value in row] for row in rows])


data = json.loads(LEDGER.read_text())
L2 = matrix_from_json(data["L2"])
M2 = matrix_from_json(data["M2"])
P = matrix_from_json(data["P"])
check("FLAT_OPERATOR_SHAPES", L2.shape == (96, 96) and M2.shape == (40, 96))
check("L0_RANK_80", L2.to_DM().rank() == 80)
check("LEFT_KERNEL_16", P.shape == (16, 96) and P.rank() == 16 and P * L2 == sp.zeros(16, 96))
check("JOINT_STACK_RANK_88", sp.Matrix.vstack(L2, M2).to_DM().rank() == 88)

# Rebuild both coefficients from the #260 COS ray and its exact t^2 log.
base_logs = logs_for()
B31 = connection_coefficients(base_logs, 3, 1)
E31 = metric_coefficients(base_logs, 3, 1)
B32 = connection_coefficients(base_logs, 3, 2)
E32 = metric_coefficients(base_logs, 3, 2)
PB31, PB32 = P * B31, P * B32

# Independent first-order calibration against one canonical flat column.
unit_logs = {(role, phase): {} for role in range(4) for phase in range(4)}
unit_logs[(0, 0)][(1, 0)] = GEN[0]
unit_B = connection_coefficients(unit_logs, 1, 0)
unit_E = metric_coefficients(unit_logs, 1, 0)
check("L2_COLUMN_NORMALIZATION", unit_B == L2[:, 0] / 2)
check("M2_COLUMN_NORMALIZATION", unit_E == M2[:, 0] / 2)

# Exact left witness: row 8 of P annihilates L2 and pairs nontrivially with B31.
witness = P.row(8)
check("T3H_LEFT_WITNESS", witness * L2 == sp.zeros(1, 96))
check("T3H_NONZERO_FREDHOLM_PAIRING", (witness * B31)[0] == 1)
check("T3H_PROJECTED_RANK_ONE", PB31.rank() == 1)

# The previously reported 12-slot vector and sparse correction are controls,
# not substitutes for the full-lattice coefficient rebuilt above.
reported = sp.zeros(96, 1)
for phase, sign in ((1, 1), (3, -1)):
    for role, gen, value in (
        (2, 0, -sp.Rational(1, 12)), (2, 2, -sp.Rational(1, 4)),
        (2, 4, -sp.Rational(1, 6)), (3, 2, sp.Rational(1, 4)),
        (3, 4, sp.Rational(1, 6)), (3, 5, sp.Rational(1, 12)),
    ):
        reported[li((phase, role, gen))] = sign * value
reported_r = sp.zeros(96, 1)
for key, value in {
    (0, 2, 1): -sp.Rational(1, 8), (0, 2, 3): sp.Rational(1, 12),
    (0, 3, 0): -sp.Rational(1, 12), (0, 3, 1): -sp.Rational(1, 24),
    (2, 2, 1): sp.Rational(1, 8), (2, 2, 3): -sp.Rational(1, 12),
    (2, 3, 0): sp.Rational(1, 12), (2, 3, 1): sp.Rational(1, 24),
}.items():
    reported_r[li(key)] = value
check("REPORTED_12_VECTOR_DIFFERS", reported != B31)
check("REPORTED_12_VECTOR_IS_IN_FLAT_RANGE", P * reported == sp.zeros(16, 1))
check("REPORTED_RANGE_CORRECTION_FAILS_REBUILT_SOURCE",
      L2 * reported_r + 2 * B31 != sp.zeros(96, 1))

# The next coefficient is computed for the same uncorrected ansatz. Since
# B31 is not in im L0, this is not a stationary-branch continuation.
check("T3H2_PROJECTED_RANK_ONE", PB32.rank() == 1)
check("T3H2_RAW_METRIC_ZERO", E32 == sp.zeros(40, 1))

labels_metric = [(p, a, b) for p in range(4) for a, b in SYM]
def encode_sparse(vector, labels):
    return [{"row": list(labels[i]), "value": str(value)}
            for i, value in enumerate(vector) if value != 0]

result = {
    "schema": 2,
    "model": "#275 four-phase edge Euler; full 96 rows; site=(phase,0,0,0)",
    "source_ray": "COS=(1,0,-1,0), roles 0,1 zero; roles 2,3 are M_2,M_3",
    "solder": "I+h*(alpha*eta/2)^T, alpha_12=alpha_21=1",
    "log_t2": "r_minus and r_zero have K1/4 on roles 0,1; phase sign=(-1)^phase",
    "normalization": "L2=2L0; M2=2M0; Euler coefficients undoubled",
    "owner_sha256": hashlib.sha256(OWNER.read_bytes()).hexdigest(),
    "flat_matrix_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
    "ranks": {"L0": 80, "left_kernel": 16, "stack_L0_M0": 88},
    "t3h": {
        "B_connection_96": encode_sparse(B31, LABELS),
        "E_metric_40": encode_sparse(E31, labels_metric),
        "P_times_B": [str(x) for x in PB31],
        "fredholm_rank_gain": PB31.rank(),
        "left_witness_P_row_8": [str(x) for x in witness],
        "witness_pairing": str((witness * B31)[0]),
        "range_correction_exists": False,
    },
    "t3h2_raw_uncorrected_ansatz": {
        "B_connection_96": encode_sparse(B32, LABELS),
        "P_times_B": [str(x) for x in PB32],
        "fredholm_rank_gain": PB32.rank(),
        "E_metric_40": encode_sparse(E32, labels_metric),
        "continuation_after_range_correction": False,
    },
    "reported_prior_values": {
        "12_slot_vector_equals_rebuilt_B31": False,
        "12_slot_vector_is_in_im_L0": True,
        "previous_sparse_r_fixes_rebuilt_B31": False,
    },
}
RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print("T3H_B96", encode_sparse(B31, LABELS))
print("T3H_PB", [str(x) for x in PB31])
print("T3H_LEFT_WITNESS", [str(x) for x in witness])
print("T3H2_RAW_B96", encode_sparse(B32, LABELS))
print("T3H2_RAW_PB", [str(x) for x in PB32])
print("T3H2_RAW_E40", encode_sparse(E32, labels_metric))
print("TERMINAL", "ORTH3_T3H_COKERNEL_OBSTRUCTION_PRECEDES_T3H2")
print("RESULT_JSON", RESULT)
