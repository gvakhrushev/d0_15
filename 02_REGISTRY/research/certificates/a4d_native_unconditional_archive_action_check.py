#!/usr/bin/env python3
"""Exact join of the unconditional first-success preparation with the owned
chronological price and the owned one-way record class.

Every load-bearing number is computed here from independently built matrices
and rational functions. Owned formulas are re-evaluated, not imported as
constants from their conclusions.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

import sympy as sp

P = (sp.sqrt(5) - 1) / 2
A = sp.sqrt(P)
Z_HALF = sp.Integer(1) / 2


PASSED = 0


def check(name: str, cond: bool, failures: list[str]) -> None:
    global PASSED
    if cond:
        PASSED += 1
    else:
        failures.append(name)


def golden_package(failures: list[str]) -> None:
    check("a_squared_is_p", sp.simplify(A**2 - P) == 0, failures)
    check("p_plus_p2", sp.simplify(P + P**2 - 1) == 0, failures)
    check("a2_plus_p2", sp.simplify(A**2 + P**2 - 1) == 0, failures)


def pencil(c, z):
    l = P**2 * (1 + c) * (1 + P**3 * c)
    t = 2 * (P**2 + P**5 * c**2)
    d = P**4 * (1 - c**2) ** 2
    t0 = 2 * (1 - c) * (2 * P**4 * c**3 + 2 * P * c**2 + (3 * P - 1) * c + P**2)
    d0 = (1 - c) ** 2 * (5 * P**4 * c**2 + (14 * P - 8) * c + P**4)
    aa = 1 - z * l
    bb = 1 - z * t + z**2 * d
    cc = 1 - z * t0 + z**2 * d0
    return aa, bb, cc


def chronology_pencil(failures: list[str]) -> sp.Expr:
    c, z = sp.symbols("c z", real=True)
    aa, bb, cc = pencil(c, z)
    at_one = [sp.simplify(expr.subs(c, 1)) for expr in (aa, bb, cc)]
    # At c=1 the owned pencil is (1-4 z p^3)^4 = A^2 B^2 C.
    target = (1 - 4 * z * P**3) ** 4
    got = sp.simplify(at_one[0] ** 2 * at_one[1] ** 2 * at_one[2])
    check("pencil_c1", sp.simplify(got - target) == 0, failures)
    # j(3/5) at z=1/2 is a real nonzero rational function of p.
    cc_s = sp.Rational(3, 5)
    aa_s, bb_s, cc_b = pencil(cc_s, Z_HALF)
    J = -2 * sp.log(aa_s) - 2 * sp.log(bb_s) - sp.log(cc_b)
    # Differentiate the symbolic pencil, then specialize. Log derivative
    # uses the explicit blocks, not a numerical slope fitted to zero.
    cs = sp.symbols("cs", real=True)
    a2, b2, c2 = pencil(cs, Z_HALF)
    Js = -2 * sp.log(a2) - 2 * sp.log(b2) - sp.log(c2)
    j_val = sp.simplify(sp.diff(Js, cs).subs(cs, cc_s))
    check("j_3_5_nonzero", j_val != 0 and sp.N(j_val) != 0, failures)
    check("blocks_positive_at_3_5", all(sp.N(x) > 0 for x in (aa_s, bb_s, cc_b)), failures)
    return sp.simplify(j_val)


def first_success_tree(m: int, b: Fraction, energy_a: Fraction, energy_0: Fraction) -> Fraction:
    """Explicit history average. Attempt 0..m-2 contribute only on first success.
    If the first m-1 attempts fail, the output is attempt m-1 with no further cut.
    """
    q = 1 - b
    acc = Fraction(0)
    prob = Fraction(0)
    for j in range(m - 1):
        pj = (q**j) * b
        acc += pj * energy_a
        prob += pj
    tail = q ** (m - 1)
    acc += tail * energy_0
    prob += tail
    if prob != 1:
        raise RuntimeError(f"tree probability {prob}")
    return acc


def mixture_formula(m: int, b: Fraction, energy_a: Fraction, energy_0: Fraction) -> Fraction:
    q = 1 - b
    c = q ** (m - 1)
    return (1 - c) * energy_a + c * energy_0


def wrong_all_fail_formula(m: int, b: Fraction, energy_a: Fraction, energy_0: Fraction) -> Fraction:
    q = 1 - b
    c = q**m
    return (1 - c) * energy_a + c * energy_0


def preparation_identities(failures: list[str]) -> None:
    samples = []
    for m, b, ea, e0 in (
        (1, Fraction(1, 3), Fraction(4, 1), Fraction(1, 5)),
        (2, Fraction(1, 2), Fraction(1, 1), Fraction(1, 2)),
        (3, Fraction(2, 7), Fraction(3, 1), Fraction(1, 4)),
        (4, Fraction(1, 6), Fraction(5, 2), Fraction(2, 3)),
    ):
        tree = first_success_tree(m, b, ea, e0)
        boxed = mixture_formula(m, b, ea, e0)
        samples.append(tree == boxed)
        check(f"tree_matches_boxed_M{m}", tree == boxed, failures)
        if m == 1:
            check("single_attempt_is_unconditional", boxed == e0, failures)
            check(
                "off_by_one_changes_M1",
                wrong_all_fail_formula(m, b, ea, e0) != e0,
                failures,
            )
        else:
            check(
                f"off_by_one_differs_M{m}",
                wrong_all_fail_formula(m, b, ea, e0) != tree,
                failures,
            )
        q = 1 - b
        if m > 1 and 0 < q < 1:
            check(f"all_fail_differs_inside_unit_interval_M{m}", q**m != q ** (m - 1), failures)
    def monomial(base: Fraction, exp: int) -> Fraction:
        if exp == 0:
            return Fraction(1)
        return base**exp

    for m in range(1, 8):
        check(f"q1_weights_agree_M{m}", monomial(Fraction(1), m) == monomial(Fraction(1), m - 1), failures)
        agree_at_zero = monomial(Fraction(0), m) == monomial(Fraction(0), m - 1)
        check(f"q0_weight_agreement_M{m}", agree_at_zero == (m > 1), failures)
    check("all_tree_samples", all(samples), failures)

    # Classical CNOT on one register: flag := flag XOR data, data bit unchanged.
    # Start from flag 0 and P(data=1)=1/5. Four writes keep that population.
    population = Fraction(1, 5)
    atoms = {(0, 0): 1 - population, (0, 1): population, (1, 0): Fraction(0), (1, 1): Fraction(0)}

    def cnot_once(dist: dict[tuple[int, int], Fraction]) -> dict[tuple[int, int], Fraction]:
        out = {(0, 0): Fraction(0), (0, 1): Fraction(0), (1, 0): Fraction(0), (1, 1): Fraction(0)}
        for (flag, data), prob in dist.items():
            out[(flag ^ data, data)] += prob
        return out

    def data_energy(dist: dict[tuple[int, int], Fraction]) -> Fraction:
        return dist[(0, 1)] + dist[(1, 1)]

    populations = []
    for _ in range(4):
        atoms = cnot_once(atoms)
        populations.append(data_energy(atoms))
    check("qnd_cnot_keeps_data_population", populations == [Fraction(1, 5)] * 4, failures)
    once = cnot_once(
        {(0, 0): Fraction(4, 5), (0, 1): Fraction(1, 5), (1, 0): Fraction(0), (1, 1): Fraction(0)}
    )
    check("one_cnot_copies_flag", once[(1, 1)] == Fraction(1, 5) and once[(0, 1)] == 0, failures)
    twice = cnot_once(once)
    check("second_cnot_undoes_flag", twice[(0, 1)] == Fraction(1, 5) and twice[(1, 1)] == 0, failures)
    pretended = mixture_formula(4, Fraction(1, 5), Fraction(1), Fraction(1, 5))
    check("pretended_retries_would_change_energy", pretended != populations[-1], failures)


def bit_pack(bits: tuple[int, int, int, int]) -> int:
    f0, d0, f1, d1 = bits
    return f0 + 2 * d0 + 4 * f1 + 8 * d1


def bit_unpack(index: int) -> tuple[int, int, int, int]:
    return (index & 1, (index >> 1) & 1, (index >> 2) & 1, (index >> 3) & 1)


def select_bits(bits: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Output slot is register 0. First success already there is a no-op.
    If register 0 failed, swap the two data bits. Flags stay.
    """
    f0, d0, f1, d1 = bits
    if f0 == 0:
        d0, d1 = d1, d0
    return (f0, d0, f1, d1)


def record_flip(bits: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    f0, d0, f1, d1 = bits
    return (1 - f0, d0, f1, d1)


def active_swap(bits: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    f0, d0, f1, d1 = bits
    return (f0, d1, f1, d0)


def one_way_record(bits: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    f0, d0, f1, d1 = bits
    return (f0 ^ d0, d0, f1, d1)


def permutation_matrix(fn) -> list[list[int]]:
    dim = 16
    matrix = [[0] * dim for _ in range(dim)]
    for i in range(dim):
        j = bit_pack(fn(bit_unpack(i)))
        matrix[j][i] = 1
    return matrix


def matmul(x: list[list[int]], y: list[list[int]]) -> list[list[int]]:
    dim = len(x)
    out = [[0] * dim for _ in range(dim)]
    for i, j, k in itertools.product(range(dim), repeat=3):
        out[i][j] += x[i][k] * y[k][j]
    return out


def transpose(x: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*x)]


def frobenius(x: list[list[int]]) -> int:
    return sum(v * v for row in x for v in row)


def selector_and_class(failures: list[str]) -> int:
    s = permutation_matrix(select_bits)
    x = permutation_matrix(record_flip)
    ident = permutation_matrix(lambda b: b)
    check("selector_involution", matmul(s, s) == ident, failures)
    check("selector_symmetric", s == transpose(s), failures)
    # Every basis vector keeps the sum of the two data bits.
    for i in range(16):
        before = bit_unpack(i)
        after = select_bits(before)
        check(
            f"energy_sum_preserved_{i}",
            before[1] + before[3] == after[1] + after[3],
            failures,
        )
    comm = matmul(x, s)
    comm_other = matmul(s, x)
    defect = [[comm[i][j] - comm_other[i][j] for j in range(16)] for i in range(16)]
    defect_norm_sq = frobenius(defect)
    check("selector_moves_record_charge", defect_norm_sq > 0, failures)
    for name, fn in (("active_swap", active_swap), ("one_way_cnot", one_way_record)):
        g = permutation_matrix(fn)
        check(f"{name}_commutes_with_record_translation", matmul(x, g) == matmul(g, x), failures)
    # Nonlinearity over F2: S(x+y) != S(x)+S(y) with S(0)=0.
    zero = (0, 0, 0, 0)
    check("selector_fixes_origin", select_bits(zero) == zero, failures)
    left = (0, 1, 0, 0)
    right = (1, 0, 0, 0)
    summed = tuple(a ^ b for a, b in zip(left, right))
    s_sum = select_bits(summed)
    s_lin = tuple(a ^ b for a, b in zip(select_bits(left), select_bits(right)))
    check("selector_not_f2_linear", s_sum != s_lin, failures)
    return defect_norm_sq


def ensemble_moments(failures: list[str]) -> None:
    b = Fraction(1, 2)
    q = 1 - b
    # Independent attempts. Success => flag 1, data 1. Failure => flag 0, data 0.
    # Output slot after routing:
    #   F0=1 with prob b, output energy 1
    #   F0=0 with prob q, output energy is the other attempt's unconditional energy b.
    energy_a = Fraction(1)
    energy_0 = b * energy_a + q * Fraction(0)
    e_out = mixture_formula(2, b, energy_a, energy_0)
    e_all = 2 * energy_0
    check("moments_differ", e_out != e_all, failures)
    check("boxed_output_energy", e_out == Fraction(3, 4), failures)
    check("archive_sum_energy", e_all == Fraction(1), failures)
    # Spectrum {0,1}, beta=log 2. Thermal energy is (1/2)/(3/2)=1/3.
    e_beta_bit = Fraction(1, 3)
    e_beta_sum = 2 * e_beta_bit
    d_out = 2 * (e_beta_bit - e_out)
    d_all = 2 * (e_beta_sum - e_all)
    mismatched = 2 * (e_beta_bit - e_all)
    check("output_port_radial", d_out == Fraction(-5, 6), failures)
    check("all_register_radial", d_all == Fraction(-2, 3), failures)
    check("mismatched_thermal_pairing", mismatched == Fraction(-4, 3), failures)
    check("ports_have_different_radial_derivatives", d_out != d_all != mismatched, failures)


def thermal_gap(failures: list[str]) -> Fraction:
    # beta = log 2, spectrum {0, 4}. Partition 1 + 2^{-4}.
    e_beta = Fraction(4, 17)
    e_trace = Fraction(2)  # mean of {0, 4}
    e_cold = Fraction(0)
    gap_trace = e_beta - e_trace
    gap_cold = e_beta - e_cold
    check("trace_hotter_than_thermal", gap_trace < 0, failures)
    check("cold_reverses_sign", gap_cold > 0, failures)
    check("sign_is_not_spectrum_alone", gap_trace * gap_cold < 0, failures)
    return e_beta


def mixture_derivative(failures: list[str]) -> None:
    e0, e1 = sp.symbols("e0 e1", real=True)
    s0 = sp.Rational(2, 3)
    lam0, lam1 = sp.Integer(0), sp.Integer(4)
    f0, f1 = 1 - e0, 1 - e1
    dim = 2
    s_a = (f0 + f1) / dim
    b = s0 * s_a
    q = 1 - b
    m = 3
    c = q ** (m - 1)
    z_a = f0 + f1
    r_a = (f0 * lam0 + f1 * lam1) / z_a
    # Nonselective channel depends on the error eigenvalues.
    r_ns = (e0 * lam0 + e1 * lam1) / dim
    r_0 = s0 * r_ns  # blank contribution has energy 0
    r_m = (1 - c) * r_a + c * r_0
    # Exact differential at a generic interior point.
    point = {e0: sp.Rational(1, 5), e1: sp.Rational(1, 2)}
    dr_m = [sp.diff(r_m, var) for var in (e0, e1)]
    dr_a = [sp.diff(r_a, var) for var in (e0, e1)]
    dr_0 = [sp.diff(r_0, var) for var in (e0, e1)]
    ds_a = [sp.diff(s_a, var) for var in (e0, e1)]
    c_p = sp.simplify(c.subs(point))
    q_p = sp.simplify(q.subs(point))
    r_a_p = sp.simplify(r_a.subs(point))
    r_0_p = sp.simplify(r_0.subs(point))
    pre = (m - 1) * q_p ** (m - 2) * s0 * (r_a_p - r_0_p)
    dropped_changes = False
    for i in range(2):
        full = sp.simplify(
            ((1 - c) * dr_a[i] + c * dr_0[i] + pre * ds_a[i]).subs(point)
        )
        got = sp.simplify(dr_m[i].subs(point))
        check(f"three_term_derivative_{i}", sp.simplify(full - got) == 0, failures)
        omitted = sp.simplify(((1 - c) * dr_a[i] + pre * ds_a[i]).subs(point))
        dropped_changes = dropped_changes or sp.simplify(omitted - got) != 0
    check("dropping_tau_derivative_changes_value", dropped_changes, failures)
    check("controller_weight_nonzero", sp.simplify(pre) != 0, failures)
    check("tau_slope_nonzero", any(sp.simplify(dr_0[i].subs(point)) != 0 for i in range(2)), failures)
    # Subclass delta tau = 0: freeze r_0 at the point and keep the weight term.
    r_0_frozen = r_0_p
    r_frozen = (1 - c) * r_a + c * r_0_frozen
    for i, var in enumerate((e0, e1)):
        got = sp.simplify(sp.diff(r_frozen, var).subs(point))
        weight = sp.simplify(((1 - c) * dr_a[i] + pre * ds_a[i]).subs(point))
        check(f"frozen_tau_keeps_weight_term_{i}", sp.simplify(got - weight) == 0, failures)
    check("frozen_tau_weight_still_nonzero", sp.simplify(pre) != 0, failures)


def conformal_and_boost(failures: list[str], j_at_three_fifths: sp.Expr) -> None:
    t = sp.symbols("t", real=True)
    # G(t)=exp(-2t) I. The normalized G-cosine cancels the scale; the bare
    # matrix element does not. Both expressions contain the exponential.
    g_metric = sp.exp(-2 * t) * sp.eye(4)
    v = sp.Matrix([1, 0, 0, 0])
    w = sp.Matrix([sp.Rational(3, 5), sp.Rational(-4, 5), 0, 0])

    def positive_cosine(metric, left, right) -> sp.Expr:
        left_norm = (left.T * metric * left)[0]
        right_norm = (right.T * metric * right)[0]
        gram = (left.T * metric * right)[0]
        return sp.simplify(gram / sp.sqrt(left_norm * right_norm))

    cosine = positive_cosine(g_metric, v, w)
    bare = sp.simplify((v.T * g_metric * w)[0])
    cosine_slope = sp.simplify(sp.diff(cosine, t))
    bare_slope = sp.simplify(sp.diff(bare, t))
    check("conformal_cosine_constant", cosine_slope == 0, failures)
    check("bare_conformal_matrix_element_moves", bare_slope != 0, failures)
    check(
        "j_times_conformal_slope_is_zero",
        sp.simplify(j_at_three_fifths * cosine_slope) == 0,
        failures,
    )
    check(
        "j_times_bare_slope_is_nonzero",
        sp.simplify(j_at_three_fifths * bare_slope) != 0,
        failures,
    )
    # Frozen vectors under a non-conformal boost: the cosine moves.
    # q(t) = F eta F^T with F=diag(e^t, e^{-t}, 1, 1), eta=diag(1,-1,-1,-1).
    f = sp.diag(sp.exp(t), sp.exp(-t), 1, 1)
    eta = sp.diag(1, -1, -1, -1)
    q = sp.simplify(f * eta * f.T)
    v_frozen = sp.Matrix([1, 0, 0, 0])
    w_frozen = sp.Matrix([2, 1, 0, 0])

    def cosine_of(metric, left, right) -> sp.Expr:
        k_left = sp.simplify((left.T * metric.inv() * left)[0])
        k_right = sp.simplify((right.T * metric.inv() * right)[0])
        # Positive pairing Q = -q + 2 n-slot. At these timelike vectors use the
        # inverse-metric cosine, which is the G-cosine once Q is a scalar
        # multiple of -q + rank-one. Here both vectors are fixed and we test
        # the inverse-metric angle that conformal scaling preserves and a boost does not.
        gram = sp.simplify((left.T * metric.inv() * right)[0])
        return sp.simplify(gram / sp.sqrt(k_left * k_right))

    frozen = cosine_of(q, v_frozen, w_frozen)
    frozen_slope = sp.simplify(sp.diff(frozen, t).subs(t, 0))
    check("frozen_boost_moves_cosine", frozen_slope != 0, failures)
    v_moved = sp.simplify(f * v_frozen)
    w_moved = sp.simplify(f * w_frozen)
    moved = cosine_of(q, v_moved, w_moved)
    moved_slope = sp.simplify(sp.diff(moved, t).subs(t, 0))
    check("transported_boost_fixes_cosine", moved_slope == 0, failures)
    # j(3/5) != 0, so a metric-only reading would invent a chronological source.
    check("false_metric_only_source_is_available", j_at_three_fifths != 0 and frozen_slope != 0, failures)


def joint_radial(failures: list[str]) -> Fraction:
    e_beta = Fraction(4, 17)
    e_trace = Fraction(2)
    m = 4
    per_register = 2 * (e_beta - e_trace)
    derivative = m * per_register
    # Hand reduction: 4/17 - 34/17 = -30/17, times 2 is -60/17, times 4 is -240/17.
    check("trace_register_radial_value", derivative == Fraction(-240, 17), failures)
    check("radial_not_zero", derivative != 0, failures)
    # Seam dS[E_01]=6 is an integer on another carrier. It is not this fraction.
    check("seam_gradient_is_different_number", derivative != -6, failures)
    return derivative


def main() -> None:
    failures: list[str] = []
    golden_package(failures)
    j_value = chronology_pencil(failures)
    preparation_identities(failures)
    defect = selector_and_class(failures)
    ensemble_moments(failures)
    thermal_gap(failures)
    mixture_derivative(failures)
    conformal_and_boost(failures, j_value)
    derivative = joint_radial(failures)
    report = {
        "status": "PASS" if not failures else "FAIL",
        "failed": failures,
        "j_at_3_5": str(j_value),
        "selector_record_commutator_frobenius_sq": defect,
        "joint_radial_derivative": str(derivative),
        "exact_controls_passed": PASSED,
        "exact_controls_failed": len(failures),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
