#!/usr/bin/env python3
"""Exact bounded algebra for the native return/record source gate.

This is a consumer check of published formulas, not an execution-admission
certificate or a new Einstein-source construction.  It uses only the standard
library.  In particular, the dense log-determinant differential is calculated
independently from the determinant polynomial, without assuming that A and dA
commute.  Every guard remains active under Python -O.

Run from any directory.  The only output is deterministic JSON on stdout.
The script neither writes evidence nor reruns historical native-word suites.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import permutations
import json


CHECKS = []


def require(condition, label):
    if not condition:
        raise RuntimeError("exact check failed: " + label)
    CHECKS.append(label)


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(k, a):
    return [[k * x for x in row] for row in a]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def zero_matrix(a):
    return all(x == 0 for row in a for x in row)


def sign_of_permutation(p):
    inversions = sum(p[i] > p[j] for i in range(len(p))
                     for j in range(i + 1, len(p)))
    return -1 if inversions % 2 else 1


def determinant(a):
    value = F(0)
    for p in permutations(range(len(a))):
        term = F(sign_of_permutation(p))
        for i, j in enumerate(p):
            term *= a[i][j]
        value += term
    return value


def inverse(a):
    n = len(a)
    aug = [row[:] + unit for row, unit in zip(a, eye(n))]
    for k in range(n):
        pivot = next((j for j in range(k, n) if aug[j][k]), None)
        if pivot is None:
            raise RuntimeError("singular exact matrix")
        aug[k], aug[pivot] = aug[pivot], aug[k]
        q = aug[k][k]
        aug[k] = [x / q for x in aug[k]]
        for i in range(n):
            if i != k:
                q = aug[i][k]
                aug[i] = [x - q * y for x, y in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def principal_minors(a):
    return [determinant([row[:k] for row in a[:k]])
            for k in range(1, len(a) + 1)]


# Univariate rational polynomials, in increasing power order.
def padd(a, b):
    n = max(len(a), len(b))
    return tuple((a[k] if k < len(a) else F(0))
                 + (b[k] if k < len(b) else F(0)) for k in range(n))


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def pdet(a):
    value = (F(0),)
    for p in permutations(range(len(a))):
        term = (F(sign_of_permutation(p)),)
        for i, j in enumerate(p):
            term = pmul(term, a[i][j])
        value = padd(value, term)
    return value


def logdet_derivative(a, da, c, dc, z):
    # Form the actual pencil D(t), including its quadratic/cubic terms,
    # then differentiate det D(t) by coefficient extraction.
    c_squared = pmul((c, dc), (c, dc))
    pencil = []
    for i in range(len(a)):
        row = []
        for j in range(len(a)):
            entry = tuple(z * x for x in pmul(c_squared, (a[i][j], da[i][j])))
            row.append(padd(entry, ((1 - z) * F(i == j),)))
        pencil.append(row)
    det_poly = pdet(pencil)
    if det_poly[0] <= 0:
        raise RuntimeError("log determinant base is not positive")
    return -det_poly[1] / det_poly[0], det_poly[0]


@dataclass(frozen=True)
class Q5:
    """a + b sqrt(5), with exact rational operations and exact ordering."""

    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def lift(x):
        return x if isinstance(x, Q5) else Q5(F(x))

    def __add__(self, other):
        other = self.lift(other)
        return Q5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Q5(self.a * other.a + 5 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        norm = other.a * other.a - 5 * other.b * other.b
        if not norm:
            raise ZeroDivisionError("zero Q(sqrt(5)) divisor")
        return self * Q5(other.a / norm, -other.b / norm)

    def __rtruediv__(self, other):
        return self.lift(other) / self

    def __pow__(self, n):
        if n < 0:
            return Q5(F(1)) / (self ** (-n))
        out, base = Q5(F(1)), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n //= 2
        return out

    def sign(self):
        a, b = self.a, self.b
        if not b:
            return (a > 0) - (a < 0)
        if not a:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        comparison = a * a - 5 * b * b
        sign_comparison = (comparison > 0) - (comparison < 0)
        return sign_comparison if a > 0 else -sign_comparison

    def data(self):
        return {"rational": str(self.a), "sqrt5_coefficient": str(self.b)}


# Bivariate rational polynomials in (Y,t), for the compensated source test.
def qadd(a, b):
    out = a.copy()
    for monomial, value in b.items():
        out[monomial] = out.get(monomial, F(0)) + value
    return {k: v for k, v in out.items() if v}


def qscale(s, a):
    return {k: s * v for k, v in a.items() if s * v}


def qmul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            key = (i + k, j + l)
            out[key] = out.get(key, F(0)) + x * y
    return {k: v for k, v in out.items() if v}


def qdiff(a, axis):
    out = {}
    for powers, value in a.items():
        degree = powers[axis]
        if degree:
            new_powers = list(powers)
            new_powers[axis] -= 1
            out[tuple(new_powers)] = degree * value
    return out


def qeval(a, y, t):
    return sum((v * y**i * t**j for (i, j), v in a.items()), F(0))


def main():
    z, c, dc = F(1, 2**20), F(3, 7), F(2, 11)
    a = mat([[F(1, 2), F(1, 10), F(1, 20)],
             [F(1, 10), F(2, 5), F(1, 15)],
             [F(1, 20), F(1, 15), F(1, 3)]])
    da = mat([[F(1, 7), F(1, 8), F(1, 10)],
              [F(1, 8), -F(1, 11), F(1, 12)],
              [F(1, 10), F(1, 12), F(1, 14)]])
    require(a == transpose(a) and da == transpose(da),
            "dense_fixture_and_variation_are_rational_Hermitian")
    require(all(x > 0 for x in principal_minors(a))
            and all(x > 0 for x in principal_minors(add(eye(3), scale(-1, a)))),
            "dense_fixture_is_strict_positive_contraction")
    require(not zero_matrix(add(mul(a, da), scale(-1, mul(da, a)))),
            "Hermitian_variation_does_not_commute_with_A")
    for step in (F(-1, 1000), F(1, 1000)):
        moved = add(a, scale(step, da))
        require(all(x > 0 for x in principal_minors(moved))
                and all(x > 0 for x in principal_minors(add(eye(3), scale(-1, moved))))
                and 0 < c + step * dc < 1,
                "positive_contraction_and_corner_at_step_" + str(step))

    d = add(scale(1 - z, eye(3)), scale(z * c * c, a))
    d_inv = inverse(d)
    w = z * c * c * trace(mul(a, d_inv))
    direct, det_base = logdet_derivative(a, da, c, dc, z)
    corner_term = -2 * w * dc / c
    gram_term = -z * c * c * trace(mul(d_inv, da))
    require(mul(d, d_inv) == eye(3) and det_base == determinant(d),
            "independent_determinant_base_and_rational_inverse")
    require(w > 0, "actual_resolvent_weight_positive")
    require(direct == corner_term + gram_term,
            "determinant_derivative_equals_complete_return_covector")
    direct_gram, _ = logdet_derivative(a, da, c, F(0), z)
    require(direct_gram == gram_term and direct_gram != 0,
            "fixed_corner_noncommuting_Gram_source_is_nonzero")

    # The published NG15 weight uses the ACTUAL OUTPUT Gram C C^T.
    # Transport to C^T C retains all output-kernel factors of (1-z).
    rectangular_c = mat([[F(1, 3), F(1, 5)],
                         [F(1, 7), F(1, 4)],
                         [F(1, 6), -F(1, 8)]])
    a_in = mul(transpose(rectangular_c), rectangular_c)
    a_out = mul(rectangular_c, transpose(rectangular_c))
    input_dim, output_dim = len(a_in), len(a_out)
    require(a_in != eye(input_dim) and determinant(a_in) > 0
            and determinant(a_out) == 0
            and all(x > 0 for x in principal_minors(add(eye(input_dim), scale(-1, a_in)))),
            "rectangular_nonisometric_contraction_retains_true_output_kernel")
    d0 = 1 - z
    d_in = add(scale(d0, eye(input_dim)), scale(z * c * c, a_in))
    d_out = add(scale(d0, eye(output_dim)), scale(z * c * c, a_out))
    det_in, det_out = determinant(d_in), determinant(d_out)
    require(det_out == d0**(output_dim - input_dim) * det_in,
            "rectangular_input_output_determinants_include_kernel_factor")
    w_in = z * c * c * trace(mul(a_in, inverse(d_in)))
    w_out = z * c * c * trace(mul(a_out, inverse(d_out)))
    require(w_in == w_out and w_in > 0,
            "rectangular_actual_output_weight_equals_input_weight")

    # Independent determinant derivatives on a joint (Y,t) matrix chart.
    # Neither dA/dt nor the controller's scalar susceptibility is zero.
    a_y = da
    a_t = mat([[F(1, 9), -F(1, 13), F(1, 17)],
               [-F(1, 13), F(1, 19), F(1, 23)],
               [F(1, 17), F(1, 23), -F(1, 29)]])
    c_y, c_t = F(5, 13), -F(2, 9)
    compensation = c_y / c_t
    j_y, _ = logdet_derivative(a, a_y, c, c_y, z)
    j_t, _ = logdet_derivative(a, a_t, c, c_t, z)
    horizontal_a = add(a_y, scale(-compensation, a_t))
    matrix_compensated = j_y - compensation * j_t
    gram_compensated = -z * c * c * trace(mul(d_inv, horizontal_a))
    require(a_t == transpose(a_t) and not zero_matrix(a_t)
            and not zero_matrix(add(mul(a, a_t), scale(-1, mul(a_t, a)))),
            "matrix_compensation_retains_nonzero_noncommuting_controller_Gram_jet")
    require(matrix_compensated == gram_compensated and gram_compensated != 0,
            "independent_determinant_sources_equal_compensated_Gram_covector")

    # At a canonical identity endpoint, both the input and its generated
    # reference move together.  i is dense and the two skew generators differ.
    i = scale(F(1, 2), mat([[1, 1], [1, -1], [1, 1], [1, -1]]))
    ki = mat([[0, F(1, 3), -F(1, 5), F(1, 7)],
              [-F(1, 3), 0, F(1, 11), -F(1, 13)],
              [F(1, 5), -F(1, 11), 0, F(1, 17)],
              [-F(1, 7), F(1, 13), -F(1, 17), 0]])
    km = mat([[0, F(1, 2), F(1, 4), -F(1, 6)],
              [-F(1, 2), 0, -F(1, 8), F(1, 10)],
              [-F(1, 4), F(1, 8), 0, F(1, 12)],
              [F(1, 6), -F(1, 10), -F(1, 12), 0]])
    di = mul(ki, i)
    require(mul(transpose(i), i) == eye(2)
            and zero_matrix(add(mul(transpose(di), i), mul(transpose(i), di))),
            "moving_input_has_exact_normalized_Stiefel_tangent")
    require(zero_matrix(add(km, transpose(km)))
            and not zero_matrix(km), "canonical_endpoint_variation_is_nonzero_unitary_tangent")
    dc_matrix = add(add(mul(transpose(di), i), mul(mul(transpose(i), km), i)),
                    mul(transpose(i), di))
    dgram = add(mul(transpose(dc_matrix), eye(2)), mul(eye(2), dc_matrix))
    require(not zero_matrix(dc_matrix) and zero_matrix(dgram),
            "generated_reference_has_nonzero_compressed_jet_but_zero_Gram_first_jet")

    # Hostile extension: proper cut of exp(tK), not a unitary on the input.
    # M(t)=cos(t), A(t)=cos(t)^2: a zero first jet does not make A constant.
    k = mat([[0, -1], [1, 0]])
    cut = mat([[1], [0]])
    m0 = mul(transpose(cut), cut)[0][0]
    m1 = mul(mul(transpose(cut), k), cut)[0][0]
    m2 = mul(mul(transpose(cut), mul(k, k)), cut)[0][0]
    a1 = 2 * m0 * m1
    a2 = 2 * m1 * m1 + 2 * m0 * m2
    require(a1 == 0 and a2 == -2,
            "proper_cut_rotation_has_zero_first_Gram_jet_but_second_jet_minus_two")
    j2 = -z * c * c * a2 / (1 - z + z * c * c)
    require(j2 > 0, "proper_cut_rotation_return_is_not_constant_near_centre")

    # Original Golden scalar corner.  u is the positive root of 4p^3;
    # all sign claims and the squared normal are exact in Q(sqrt(5)).
    p = Q5(-F(1, 2), F(1, 2))
    golden_c, u2 = p**3, 4 * p**3
    require(p * p + p == Q5(F(1))
            and p.sign() > 0 and (1 - p).sign() > 0,
            "Golden_field_relation_and_positive_root")
    require(golden_c * golden_c + u2 == Q5(F(1))
            and golden_c.sign() > 0 and u2.sign() > 0,
            "literal_Golden_corner_c_squared_plus_u_squared_is_one")
    golden_w = 8 * z * golden_c**2 / (1 - z + z * golden_c**2)
    normal2 = (4 * golden_w / golden_c)**2 * u2
    ratio2 = 16 * u2 / golden_c**2
    require(golden_w.sign() > 0 and normal2.sign() > 0,
            "literal_Golden_return_normal_4wu_over_c_is_strictly_positive")
    require(ratio2 == 64 / p**3,
            "literal_Golden_normal_over_weight_has_exact_squared_value")
    with localcontext() as ctx:
        ctx.prec = 70
        pd = (Decimal(5).sqrt() - 1) / 2
        cd, ud = pd**3, 2 * pd * pd.sqrt()
        zd = Decimal(1) / Decimal(2**20)
        wd = 8 * zd * cd**2 / (1 - zd + zd * cd**2)
        golden_diagnostic = {
            "normal_4wu_over_c": str(4 * wd * ud / cd),
            "normal_divided_by_w": str(4 * ud / cd),
        }

    # A complete nuisance counterexample, expressly not a D0 execution.
    # S(Y,t,r)=t^2/2+(r-Y)^2/2.  EY=Y-r cannot factor through Et=t
    # at (Y,t,r)=(2,0,0), yet eliminating BOTH nuisances erases all EY.
    h = mat([[1, 0, -1], [0, 1, 0], [-1, 0, 1]])
    hyn = [h[0][1:]]
    hnn = [row[1:] for row in h[1:]]
    schur = h[0][0] - mul(mul(hyn, inverse(hnn)), transpose(hyn))[0][0]
    nuisance_gradient = mul(h, mat([[2], [0], [0]]))
    require(nuisance_gradient == mat([[2], [0], [-2]]),
            "illustrative_EY_nonzero_while_the_single_Et_is_zero")
    require(schur == 0 and hnn == eye(2),
            "illustrative_complete_nuisance_Schur_complement_zero")
    # On t=0,r=Y the polynomial coefficients of S_eff and all Euler rows
    # vanish identically; check this independently as a quadratic form.
    stationary_lift = mat([[1], [0], [1]])
    require(zero_matrix(mul(h, stationary_lift))
            and mul(mul(transpose(stationary_lift), h), stationary_lift) == [[F(0)]],
            "illustrative_joint_stationary_lift_has_identically_constant_effective_price")

    # Nonlinear c and nonlinear residual, with the whole F(c) differentiated.
    # Clear the nonzero c_t denominator before comparing every coefficient.
    cp = {(1, 0): F(2), (0, 1): F(3), (1, 1): F(1)}
    rp = {(2, 0): F(1), (1, 1): F(1), (0, 2): F(2)}
    cp2 = qmul(cp, cp)
    fp = qadd(qadd(qmul(cp2, cp2), qscale(F(3), cp2)),
              qadd(qscale(F(2), cp), {(0, 0): F(7)}))
    sp = qadd(fp, rp)
    cy, ct = qdiff(cp, 0), qdiff(cp, 1)
    sy, st = qdiff(sp, 0), qdiff(sp, 1)
    ry, rt = qdiff(rp, 0), qdiff(rp, 1)
    compensated = qadd(qmul(sy, ct), qscale(F(-1), qmul(st, cy)))
    residual_only = qadd(qmul(ry, ct), qscale(F(-1), qmul(rt, cy)))
    require(compensated == residual_only and bool(residual_only),
            "compensated_source_cancels_every_coefficient_of_F_of_c")
    at_y, at_t = F(0), F(1)
    ct0, cy0 = qeval(ct, at_y, at_t), qeval(cy, at_y, at_t)
    compensated_value = qeval(sy, at_y, at_t) - cy0 * qeval(st, at_y, at_t) / ct0
    require(ct0 != 0 and compensated_value == -3,
            "compensated_residual_retains_nonzero_regular_chart_value")

    result = {
        "status": "PASS_EXACT_ALGEBRA",
        "reference_commit": "e63ef7a3073f4854a2fc8fd4c69bf004bc42d544",
        "reference_sources": [
            {"path": "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md",
             "sections": "7eo.C NG15-NG19; 7eo.F CD1-CD5; 7eo.I.4",
             "role": "Formula provenance; this checker does not validate native admission or the whole source theorem."},
            {"path": "02_REGISTRY/research/A4D_NATIVE_WORD_NORMAL_SOURCE_2026_10_31.md",
             "sections": "Exact finite construction; general same-reporter application",
             "role": "Original c=p^3,u=2p sqrt(p) and 4wu/c return normal; historical words/heat are not replayed."},
            {"path": "02_REGISTRY/research/A4D_JOINT_THERMAL_STATIONARITY_AND_SHARED_SOURCE_LOSS_2026_10_31.md",
             "sections": "Why the missing normal cannot be selectively cancelled on this route",
             "role": "Shared-scalar chain-rule scope."},
            {"path": "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md",
             "sections": "5 and 5.1",
             "role": "The actual residual requires a supplied price/Info table; none is fabricated here."},
        ],
        "scopes": {
            "dense_fixture": "Exact rational Hermitian matrix check, not a newly admitted D0 history.",
            "Gram_carrier": "NG15 uses the output Gram; the rectangular check transports to the input Gram at fixed dimensions and z without dropping the output-kernel determinant factor.",
            "matrix_compensation": "Exact joint return-source identity with both A_Y and A_t nonzero; no D0 field or controller admission is inferred from this fixture.",
            "canonical_input": "Pointwise first-jet identity at an identity return with generated reference; not global constancy under arbitrary old-gate variations.",
            "proper_cut_hostile_control": "Exact 2x2 unitary rotation shows A'(0)=0 with A''(0)=-2.",
            "golden": "Exact native scalar-corner algebra; decimal values are diagnostic only.",
            "complete_nuisance": "Illustrative counterexample, not D0: S=t^2/2+(r-Y)^2/2.",
            "compensated_source": "Exact polynomial chain-rule check on a regular c_t!=0 chart; no selected D0 residual is claimed.",
            "not_established": "Einstein matching, one-execution Cost-Info binding, admission, complete physical variation coverage, and any GR closure flag.",
        },
        "identities": {
            "complete_return_source": "dJ=-(2w/c)dc-z*c^2*Tr(D^-1*dA), D=(1-z)I+z*c^2*A",
            "rectangular_Gram_transport": "det(D_out)=(1-z)^(m-r)*det(D_in); J_out=J_in-(m-r)*log(1-z); w_out=w_in for fixed m,r,z",
            "compensated_matrix_return_source": "J_Y-(c_Y/c_t)J_t=-z*c^2*Tr(D^-1*(A_Y-(c_Y/c_t)*A_t))",
            "compensated_source": "S_Y-(c_Y/c_t)S_t=R_Y-(c_Y/c_t)R_t for S=F(c)+R",
            "canonical_Gram": "dC=i^T*dM*i is skew at M=I after normalized input/reference terms cancel; d(C^T C)=0",
        },
        "dense_fixture": {
            "z": str(z), "c": str(c), "dc": str(dc),
            "A": [[str(x) for x in row] for row in a],
            "dA": [[str(x) for x in row] for row in da],
            "A_leading_principal_minors": [str(x) for x in principal_minors(a)],
            "I_minus_A_leading_principal_minors": [str(x) for x in principal_minors(add(eye(3), scale(-1, a)))],
            "det_D": str(det_base), "w": str(w),
            "independent_logdet_derivative": str(direct),
            "corner_source": str(corner_term), "Gram_source": str(gram_term),
            "dc_zero_source": str(direct_gram),
        },
        "rectangular_Gram_transport": {
            "C": [[str(x) for x in row] for row in rectangular_c],
            "input_dimension_r": input_dim, "output_dimension_m": output_dim,
            "A_input": [[str(x) for x in row] for row in a_in],
            "A_output": [[str(x) for x in row] for row in a_out],
            "det_D_input": str(det_in), "det_D_output": str(det_out),
            "kernel_factor": str(d0**(output_dim - input_dim)),
            "J_output_minus_J_input": "-(m-r)*log(1-z)",
            "w_input": str(w_in), "w_output": str(w_out),
        },
        "compensated_matrix_fixture": {
            "A_Y": [[str(x) for x in row] for row in a_y],
            "A_t": [[str(x) for x in row] for row in a_t],
            "c_Y": str(c_y), "c_t": str(c_t), "c_Y_over_c_t": str(compensation),
            "J_Y_from_determinant": str(j_y), "J_t_from_determinant": str(j_t),
            "compensated_source_from_determinants": str(matrix_compensated),
            "compensated_source_from_Gram": str(gram_compensated),
        },
        "canonical_input": {
            "compressed_first_derivative": [[str(x) for x in row] for row in dc_matrix],
            "Gram_first_derivative": [["0", "0"], ["0", "0"]],
        },
        "proper_cut_rotation": {
            "M": "cos(t)", "A": "cos(t)^2",
            "A_first_at_zero": str(a1), "A_second_at_zero": str(a2),
            "J_second_at_zero_with_fixed_c": str(j2),
        },
        "golden": {
            "c": golden_c.data(), "u_squared": u2.data(),
            "w": golden_w.data(), "normal_squared": normal2.data(),
            "normal_divided_by_w_squared": ratio2.data(),
            "diagnostic_decimals": golden_diagnostic,
        },
        "illustrative_nuisance": {
            "price": "t^2/2+(r-Y)^2/2", "single_t_counterpoint": ["2", "0", "0"],
            "EY_at_counterpoint": "2", "Et_at_counterpoint": "0",
            "stationary_nuisances": "t=0,r=Y", "effective_price": "0",
            "complete_Schur_complement": str(schur),
        },
        "compensated_polynomial_fixture": {
            "c": "2Y+3t+Yt", "F(c)": "c^4+3c^2+2c+7", "R": "Y^2+Yt+2t^2",
            "cleared_denominator_polynomial_difference": "0",
            "regular_point_Y_t": ["0", "1"], "c_t": str(ct0),
            "compensated_residual_at_point": str(compensated_value),
        },
        "checks": CHECKS,
    }
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
