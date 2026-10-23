#!/usr/bin/env python3
"""Exact bounded checker for the nine-null-plus-scale source testing basis.

Consumer: the backward Einstein synthesis within gvakhrushev/d0_15 PR #334.
Context ref: 3f368179627acc9f2c3e9616df729ac2280a77a0.

The independent inputs are a four-dimensional (+---) Lorentz coframe, nine
specified rational null directions, and positive fixed cell mass m.  The
dressing is F_m(e) = sqrt(m / v(e)) e, with v homogeneous of degree four.
No repository module, field equation, fitted source, or optical/history
identity is imported.  The algebraic inverse acts on the existing symmetric
metric covector, including its native density factors.  Its cellwise l1 bound
therefore preserves a common cell sum and the unchanged h^-2 prefactor.

Only Python's standard library is used.  All validation guards raise explicit
exceptions; running Python with -O does not remove any checks.  This script
prints its result and never writes files.
"""

from fractions import Fraction as F
from math import isqrt
import sys


class VerificationError(RuntimeError):
    """An exact stated identity or its required negative control failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def mul(a, b):
    require(len(a[0]) == len(b), "incompatible matrix product")
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def mv(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def outer(u, v):
    return [[x * y for y in v] for x in u]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def rref(a):
    b = [list(row) for row in a]
    lead = 0
    pivots = []
    for col in range(len(b[0])):
        candidates = [i for i in range(lead, len(b)) if b[i][col]]
        if not candidates:
            continue
        pivot = candidates[0]
        b[lead], b[pivot] = b[pivot], b[lead]
        q = b[lead][col]
        b[lead] = [x / q for x in b[lead]]
        for i in range(len(b)):
            if i != lead:
                q = b[i][col]
                b[i] = [x - q * y for x, y in zip(b[i], b[lead])]
        pivots.append(col)
        lead += 1
        if lead == len(b):
            break
    return b, pivots


def inverse(a):
    n = len(a)
    require(all(len(row) == n for row in a), "inverse requires a square matrix")
    augmented = [row + unit for row, unit in zip(a, eye(n))]
    reduced, pivots = rref(augmented)
    require(pivots[:n] == list(range(n)), "matrix is singular")
    require([row[:n] for row in reduced] == eye(n), "inverse elimination failed")
    return [row[n:] for row in reduced]


def determinant(a):
    n = len(a)
    require(all(len(row) == n for row in a), "determinant requires a square matrix")
    b = [list(row) for row in a]
    value = F(1)
    for j in range(n):
        candidates = [i for i in range(j, n) if b[i][j]]
        if not candidates:
            return F(0)
        p = candidates[0]
        if p != j:
            b[p], b[j] = b[j], b[p]
            value = -value
        pivot = b[j][j]
        value *= pivot
        for i in range(j + 1, n):
            q = b[i][j] / pivot
            b[i] = [x - q * y for x, y in zip(b[i], b[j])]
    return value


I4 = eye(4)
ETA = [[F((1, -1, -1, -1)[i] if i == j else 0)
        for j in range(4)] for i in range(4)]
PAIRS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
         (2, 2), (3, 3), (1, 2), (1, 3), (2, 3))
SPATIAL_PAIRS = ((1, 2), (1, 3), (2, 3))


def unpack(v):
    a = [[F(0) for _ in range(4)] for _ in range(4)]
    for (i, j), x in zip(PAIRS, v):
        a[i][j] = x
        a[j][i] = x
    return a


def directions():
    result = []
    for i in range(1, 4):
        for sign in (1, -1):
            v = [F(1), F(0), F(0), F(0)]
            v[i] = F(sign)
            result.append(v)
    for i, j in SPATIAL_PAIRS:
        v = [F(1), F(0), F(0), F(0)]
        v[i], v[j] = F(3, 5), F(4, 5)
        result.append(v)
    return result


def measurement_row(v):
    return [v[a] * v[b] * (1 if a == b else 2) for a, b in PAIRS]


def reconstruct(q):
    """q = (y1+,y1-,y2+,y2-,y3+,y3-,z12,z13,z23,t), t=tr_eta S."""
    d = [(q[2 * i] + q[2 * i + 1]) / 2 for i in range(3)]
    b = [(q[2 * i] - q[2 * i + 1]) / 4 for i in range(3)]
    a = (sum(d) + q[9]) / 4
    diagonal = [x - a for x in d]
    off = []
    for z_index, (i, j) in enumerate(SPATIAL_PAIRS, 6):
        pi, mi = q[2 * (i - 1)], q[2 * (i - 1) + 1]
        pj, mj = q[2 * (j - 1)], q[2 * (j - 1) + 1]
        off.append((25 * q[z_index] - 12 * pi + 3 * mi - 18 * pj + 2 * mj) / 24)
    return [a] + b + diagonal + off


def rational_sqrt(q):
    require(q > 0, "positive mass and volume are required")
    num, den = isqrt(q.numerator), isqrt(q.denominator)
    require(num * num == q.numerator and den * den == q.denominator,
            "fixture square root is not rational")
    return F(num, den)


def volume(e):
    return abs(determinant(e))


def dress(e, mass):
    v = volume(e)
    require(v > 0, "coframe is degenerate")
    return scale(rational_sqrt(mass / v), e)


def check_source_inverse(probes):
    null_matrix = [measurement_row(v) for v in probes]
    eta_vector = [ETA[a][b] for a, b in PAIRS]
    trace_row = list(eta_vector)
    measurement = null_matrix + [trace_row]
    _, pivots = rref(null_matrix)
    require(len(pivots) == 9, "nine null rows are not independent")
    require(mv(null_matrix, eta_vector) == [F(0)] * 9,
            "metric is not in the null-measurement kernel")
    require(any(eta_vector), "missing-trace negative control must be nonzero")

    formula_inverse = transpose([reconstruct(v) for v in eye(10)])
    require(formula_inverse == inverse(measurement), "explicit inverse formula is wrong")
    require(mul(formula_inverse, measurement) == eye(10), "left inverse failed")
    require(mul(measurement, formula_inverse) == eye(10), "right inverse failed")
    det = determinant(measurement)
    require(det == F(3538944, 15625), "unexpected measurement determinant")

    # The actual alpha-scale derivative is r0=-t, since delta g^{-1}=-eta.
    scale_measurement = null_matrix + [[-x for x in trace_row]]
    scale_inverse_columns = []
    for q in eye(10):
        q = list(q)
        q[9] = -q[9]
        scale_inverse_columns.append(reconstruct(q))
    require(mul(transpose(scale_inverse_columns), scale_measurement) == eye(10),
            "density derivative sign was not converted to the trace")
    require(determinant(scale_measurement) == -det, "scale row determinant sign failed")

    packed_columns = [sum(abs(formula_inverse[i][j]) for i in range(10))
                      for j in range(10)]
    multiplicity = [1 if a == b else 2 for a, b in PAIRS]
    full_columns = [sum(multiplicity[i] * abs(formula_inverse[i][j]) for i in range(10))
                    for j in range(10)]
    require(max(packed_columns[:9]) == F(5, 2) and packed_columns[9] == 1,
            "packed raw l1 bound failed")
    require(max(full_columns[:9]) == F(17, 4) and full_columns[9] == 1,
            "full raw l1 bound failed")
    expected_null_rows = [F(3, 4)] + [F(1, 2)] * 3 + [F(5, 4)] * 3 + [F(5, 2)] * 3
    require([sum(abs(x) for x in row[:9]) for row in formula_inverse] == expected_null_rows,
            "componentwise null-residual bound failed")

    # Hostile controls are required to fail the claimed inverse/geometry.
    q_eta = mv(measurement, eta_vector)
    wrong_sign = list(q_eta)
    wrong_sign[9] = -wrong_sign[9]
    require(reconstruct(wrong_sign) != eta_vector,
            "wrong trace-sign mutation was not detected")
    bad_probe = [F(1), F(3), F(4), F(0)]
    require(sum(x * y for x, y in zip(bad_probe, mv(ETA, bad_probe))) == -24,
            "unnormalized-probe negative control is unexpectedly null")
    bad_matrix = [list(row) for row in measurement]
    bad_matrix[6] = measurement_row(bad_probe)
    require(mul(formula_inverse, bad_matrix) != eye(10),
            "unnormalized-probe mutation was not detected")
    return det


def check_finite_coframe_paths(probes):
    # Non-diagonal rational coframe, volume 2; m=1/2 gives sqrt(m/v)=1/2.
    base = [[F(2), F(1, 3), F(-1, 5), F(1, 7)],
            [F(0), F(1), F(2, 5), F(-1, 6)],
            [F(0), F(0), F(1), F(3, 7)],
            [F(0), F(0), F(0), F(1)]]
    mass = F(1, 2)
    require(volume(base) == 2, "coframe fixture volume changed")
    hat = dress(base, mass)
    require(dress(hat, mass) == base, "fixed-mass dressing involution failed")
    require(volume(hat) == mass * mass / volume(base), "dressed volume formula failed")
    metric = mul(mul(transpose(hat), ETA), hat)
    metric_inverse = inverse(metric)
    parameter = F(2, 7)

    for ell in probes:
        lowered = mv(ETA, ell)
        require(sum(x * y for x, y in zip(ell, lowered)) == 0, "probe is not null")
        n = outer(ell, lowered)
        require(mul(n, n) == scale(F(0), I4), "null generator is not nilpotent")
        require(trace(n) == 0, "null generator has nonzero trace")
        require(mul(transpose(n), ETA) == mul(ETA, n), "generator is not eta-self-adjoint")
        left = add(I4, scale(-parameter / 2, n))
        left_inverse = add(I4, scale(parameter / 2, n))
        require(mul(left, left_inverse) == I4, "finite coframe inverse failed")
        require(determinant(left) == 1, "null coframe path changes volume")
        varied_base = mul(left, base)
        varied_hat = mul(left, hat)
        require(dress(varied_base, mass) == varied_hat,
                "null deformation does not commute with fixed-mass dressing")
        require(dress(varied_hat, mass) == varied_base,
                "dressing involution failed on a null path")
        k = mv(inverse(hat), ell)
        k_flat = mv(metric, k)
        varied_metric = mul(mul(transpose(varied_hat), ETA), varied_hat)
        require(varied_metric == add(metric, scale(-parameter, outer(k_flat, k_flat))),
                "exact covariant metric deformation has wrong sign or indices")
        require(inverse(varied_metric) == add(metric_inverse, scale(parameter, outer(k, k))),
                "exact inverse metric deformation has wrong sign or indices")
        require(mv(inverse(varied_hat), ell) == k, "own null vector did not remain fixed")

    # a=exp(alpha/2): base/a produces dressed a*hat, keeping normalized m fixed.
    a = F(3, 2)
    scaled_base = scale(1 / a, base)
    require(volume(scaled_base) == volume(base) / a**4, "base scale volume law failed")
    require(mass / volume(scaled_base) == a**4 * mass / volume(base),
            "fixed-mass density scaling failed")
    require(dress(scaled_base, mass) == scale(a, hat), "fixed-mass local scale path failed")
    require(dress(dress(scaled_base, mass), mass) == scaled_base,
            "dressing involution failed on a scale path")
    require(F(1, 2) + F(1, 2) == 1, "normalized-mass fixture is invalid")

    # The logarithmic coframe differential A -> A-tr(A) I/2 is itself involutive.
    def differential(a_matrix):
        return add(a_matrix, scale(-trace(a_matrix) / 2, I4))

    for i in range(4):
        for j in range(4):
            unit = [[F(r == i and c == j) for c in range(4)] for r in range(4)]
            require(differential(differential(unit)) == unit,
                    "fixed-mass logarithmic differential is not an involution")

    # Normalized mass variations alone do not test every local trace.
    masses = [F(1, 3), F(2, 3)]
    traces = [3 * m for m in masses]
    dm = [F(1, 5), F(-1, 5)]
    require(sum(dm) == 0 and sum(traces[i] * dm[i] / masses[i] for i in range(2)) == 0,
            "mass-only multiplier control failed")
    require(any(traces), "mass-only multiplier control must have a nonzero trace")

    bad = [F(1), F(3), F(4), F(0)]
    bad_n = outer(bad, mv(ETA, bad))
    require(mul(bad_n, bad_n) != scale(F(0), I4), "bad probe became nilpotent")
    require(determinant(add(I4, scale(-parameter / 2, bad_n))) != 1,
            "unnormalized-probe volume defect was not detected")


def main():
    probes = directions()
    det = check_source_inverse(probes)
    check_finite_coframe_paths(probes)
    print("Exact null/source basis: verified with Fraction arithmetic and explicit exceptions.")
    print("Convention: eta=(+---); packed tensor=(00,01,02,03,11,22,33,12,13,23).")
    print("Nine null rows: kernel=span(eta), rank=9; rational inverse with trace is exact.")
    print(f"Measurement determinant: trace row {det}; actual scale row {-det}.")
    print("Scale convention: dQ/dalpha=-tr_eta(S) for hat_e -> exp(alpha/2)*hat_e.")
    print("Raw l1 inverse: packed10 <= (5/2)*sum(abs(null rows))+abs(trace).")
    print("Raw l1 inverse: full16 <= (17/4)*sum(abs(null rows))+abs(trace).")
    print("The bounds commute with a common cell sum and the unchanged h^-2 prefactor.")
    print("Finite coframe paths: N^2=0, det(I-epsilon*N/2)=1, exact metric/inverse signs verified.")
    print("Fixed-mass dressing: F_m(F_m(e))=e; base/a -> a*hat_e; normalized m unchanged.")
    print("Negative controls: missing trace, wrong trace sign, unnormalized probes, mass-only multiplier detected.")
    print("Scope: variation-basis algebra only; no action identification, source root, or optical/history balance claimed.")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as error:
        print(f"VERIFICATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
