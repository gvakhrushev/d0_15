#!/usr/bin/env python3
"""Bounded independent checks for the explicit native execution candidate.

The readiness witness is an actually expanded raw word.  Its continuous
symbols describe a comparison of finite equal-inventory codes, not an added
angle gate or a theorem that this candidate is all of original D0 physics.
No large geometric, root, history, or Lean suite is imported.
"""

import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp

import native_execution as ne
import book_price as bp


class Quadratic:
    """Exact Q(p), p^2=1-p, with a certified positive real embedding."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = Fraction(a), Fraction(b)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Quadratic) else Quadratic(x)

    def __add__(self, other):
        other = self.coerce(other)
        return Quadratic(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Quadratic(self.a * other.a + self.b * other.b,
                         self.a * other.b + self.b * other.a
                         - self.b * other.b)

    __rmul__ = __mul__

    def __pow__(self, n):
        if type(n) is not int or n < 0:
            raise ValueError("only nonnegative integer powers")
        result, base = Quadratic(1), self
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def __eq__(self, other):
        other = self.coerce(other)
        return self.a == other.a and self.b == other.b

    def sign(self):
        # 2(a+b p)=(2a-b)+b sqrt(5).  Opposite signs are decided
        # by an integer square comparison, never floating cancellation.
        c, d = 2 * self.a - self.b, self.b
        if not c:
            return (d > 0) - (d < 0)
        if not d:
            return (c > 0) - (c < 0)
        if c > 0 and d > 0:
            return 1
        if c < 0 and d < 0:
            return -1
        comparison = c * c - 5 * d * d
        signed = (comparison > 0) - (comparison < 0)
        return signed if c > 0 else -signed

    def digest(self):
        return hashlib.sha256(
            f"{self.a.numerator}/{self.a.denominator};"
            f"{self.b.numerator}/{self.b.denominator}".encode()
        ).hexdigest()


P = ne.P
A = ne.A
G = ne.G_LOCAL
CHECKS = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def algebraic_zero(x):
    return ne.GOLDEN_FIELD.from_sympy(sp.expand(x)) == ne.GOLDEN_FIELD.zero


def expect_domain_error(name, callback):
    try:
        callback()
    except ne.DomainError:
        check(name, True)
    else:
        raise AssertionError(name + ": rejected input was accepted")


def source_execution(gates, qubits=4, blanks=(0, 1), old=()):
    return ne.Execution(qubits=qubits, blank_wires=blanks, old_right=old,
                        gates=tuple(gates), profile=ne.G_CX_SOURCE_I,
                        source_port=0, source_spin=(qubits - 2, qubits - 1))


def native_cell(length, code, control, target):
    if abs(code) > length or (length - code) % 2:
        raise ValueError("invalid equal-inventory code")
    positive = (length + code) // 2
    cx = ne.Gate("CX", (control, target))
    g = ne.Gate("G", (target,))
    # Each plus/minus cell pays one G and TWO actual CX letters.
    return ((g, cx, cx) * positive
            + (cx, g, cx) * (length - positive))


def resource_word(length, code):
    return (native_cell(length, code, 0, 1)
            + native_cell(length, code, 0, 2)
            + (ne.Gate("CX", (1, 3)), ne.Gate("CX", (2, 3)),
               ne.Gate("CX", (1, 2))))


def g_power(code):
    return (G ** code) if code >= 0 else (G.T ** (-code))


def resource_matrix(rotation):
    ex = ne.Execution(3, (0, 1, 2), (), ())
    result = sp.kronecker_product(rotation, rotation, sp.eye(2))
    for gate in (ne.Gate("CX", (0, 2)), ne.Gate("CX", (1, 2)),
                 ne.Gate("CX", (0, 1))):
        result = ne.gate_matrix(ex, gate) * result
    return result


def grammar_and_inverse_checks():
    bounds = dict(max_qubits=7, max_expanded_stages=100000)
    valid = ne.Execution(3, (0,), (2,),
                         (ne.Gate("G", (0,)), ne.Gate("CX", (0, 1))),
                         report_bits=(0,))
    check("valid unknown input and immutable oldRIGHT", ne.is_member(valid, **bounds))
    inv = ne.inventory(valid, **bounds)
    check("unknown/protected input rank is not blank rank",
          inv.input_dimension == 4 and inv.cut_rank == 4
          and inv.unknown_wires == (1, 2))
    j = ne.input_isometry(valid)
    p0 = ne.cut_projector(valid)
    check("input isometry retains every unknown basis column",
          ne.exact_matrix_equal(j.T * j, sp.eye(4))
          and ne.exact_matrix_equal(p0, j * j.T) and sp.trace(p0) == 4)
    bad = [
        ("oldRIGHT cannot be targeted", replace(valid, gates=(ne.Gate("G", (2,)),))),
        ("oldRIGHT cannot be used as a coherent control", replace(valid, gates=(ne.Gate("CX", (2, 1)),))),
        ("oldRIGHT cannot be re-declared blank", replace(valid, blank_wires=(0, 2))),
        ("uncharged inverse primitive rejected", replace(valid, gates=(ne.Gate("Gdagger", (0,)),))),
        ("reset primitive rejected", replace(valid, gates=(ne.Gate("RESET", (0,)),))),
        ("repeated CX wire rejected", replace(valid, gates=(ne.Gate("CX", (0, 0)),))),
        ("source profile cannot be inferred from a matrix", replace(valid, gates=(ne.Gate("SourceI", (0, 1, 2)),))),
        ("boolean wire count is not an integer bound", replace(valid, qubits=True)),
    ]
    for label, code in bad:
        expect_domain_error(label, lambda code=code: ne.validate_execution(code, **bounds))
    expect_domain_error("explicit stage cap", lambda: ne.validate_execution(
        valid, max_qubits=7, max_expanded_stages=1))
    expect_domain_error("G/CX has no invented exact inverse", lambda: ne.inverse_word(valid, **bounds))

    source = ne.Gate("SourceI", (0, 2, 3))
    fixture = source_execution((ne.Gate("G", (1,)), ne.Gate("CX", (0, 1)),
                                ne.Gate("G", (0,)), source,
                                ne.Gate("CX", (1, 0)), ne.Gate("G", (1,))))
    reverse = ne.inverse_word(fixture, **bounds)
    forward_matrix = ne.word_matrix(fixture)
    reverse_matrix = ne.word_matrix(replace(fixture, gates=reverse))
    check("16D exact inverse on arbitrary dirty ports/spin",
          ne.exact_matrix_equal(reverse_matrix * forward_matrix, sp.eye(16))
          and ne.exact_matrix_equal(forward_matrix * reverse_matrix, sp.eye(16)))
    spin_i = sp.kronecker_product(sp.eye(4), ne.L_I)
    check("original quaternion spin complex structure retained",
          ne.exact_matrix_equal(forward_matrix * spin_i, spin_i * forward_matrix))
    reverse_inventory = ne.inventory(replace(fixture, gates=reverse), **bounds)
    check("every inverse routing/source call is counted",
          (reverse_inventory.g_count, reverse_inventory.cx_count,
           reverse_inventory.source_i_count, reverse_inventory.gate_count)
          == (3, 14, 15, 32))
    expect_domain_error("expanded inverse obeys its own stage cap", lambda: ne.inverse_word(
        fixture, max_qubits=7, max_expanded_stages=31))
    expect_domain_error("source spin is not free individually", lambda: ne.validate_execution(
        replace(fixture, gates=(ne.Gate("G", (2,)),)), **bounds))
    expect_domain_error("source frame cannot be silently permuted", lambda: ne.validate_execution(
        replace(fixture, gates=(ne.Gate("SourceI", (1, 2, 3)),)), **bounds))

    # A scalar native middle parameter, not a fitted coupling.
    m = source_execution((ne.Gate("G", (0,)), ne.Gate("G", (0,))),
                         qubits=3, blanks=(0,))
    jm = ne.input_isometry(m)
    check("native two-G port compression equals p cubed on all four spin columns",
          ne.exact_matrix_equal(jm.T * ne.word_matrix(m) * jm, P ** 3 * sp.eye(4)))

    # Strict JSON roundtrip and a few semantic hostile controls.  The parser
    # intentionally shares the exact grammar, not a second admission rule.
    encoded = ne.canonical_json(valid)
    check("canonical strict JSON roundtrip",
          ne.execution_from_json(encoded, **bounds) == valid)
    obj = json.loads(encoded)
    obj["gates"][0]["wires"] = [2]
    expect_domain_error("JSON oldRIGHT operation rejected", lambda: ne.execution_from_dict(obj, **bounds))
    expect_domain_error("duplicate JSON keys rejected", lambda: ne.execution_from_json(
        '{"schema":"d0.native-execution/1","schema":"other"}', **bounds))
    obj = json.loads(encoded)
    obj["gates"][0]["op"] = "ARBITRARY_MATRIX"
    expect_domain_error("JSON arbitrary matrix rejected", lambda: ne.execution_from_dict(obj, **bounds))
    return {"dirty_inverse_dimension": 16, "forward_stages": 6,
            "expanded_inverse_stages": reverse_inventory.gate_count,
            "expanded_inverse_inventory": {"G": 3, "CX": 14, "SourceI": 15}}


def readiness_column_and_native_cells():
    c, s, u = sp.symbols("c s u", real=True)
    comparison = resource_matrix(sp.Matrix([[c, -s], [s, c]]))
    column = sp.zeros(8, 1)
    column[0], column[4], column[3], column[7] = c ** 2, s ** 2, c * s, c * s
    check("8D full parity column as an exact polynomial",
          comparison[:, 0] == column)
    accepted = sp.Matrix([column[i] if i & 1 else 0 for i in range(8)])
    check("normalized successful plus does not depend on the angle",
          accepted[3] == accepted[7] == c * s
          and all(accepted[i] == 0 for i in range(8) if i not in (3, 7))
          and sp.expand((accepted.T * accepted)[0]) == 2 * c ** 2 * s ** 2)

    s0 = (1 - u ** 2) / 2
    u0 = P ** 3
    check("native parity success is 2 p cubed", algebraic_zero(s0.subs(u, u0) - 2 * P ** 3))
    check("exact logarithmic readiness derivative is minus one half",
          algebraic_zero((sp.diff(s0, u) / s0).subs(u, u0) + sp.Rational(1, 2)))
    alpha_ratio = 4 * A * P * (P - P ** 2) / (2 * P ** 3)
    check("angle convention gives the same positive readiness source",
          algebraic_zero(alpha_ratio - 2 * A * P)
          and ne.GOLDEN_FIELD.from_sympy(alpha_ratio) != ne.GOLDEN_FIELD.zero)

    # Equations (193)-(194) use the ACTUAL divided feedback gain.
    # Its cancellation is algebraic and does not identify the absolute
    # heat baselines of the different stencils in a limiting sequence.
    ua, ub = sp.symbols("u_a u_b", real=True)
    gr, qr, gain, omega, a0, tau = sp.symbols(
        "gamma_rest q A_ab Omega a0 tau", positive=True)
    xa, xb = gr * qr * (1 - ua ** 2) / 2, gr * qr * (1 - ub ** 2) / 2
    contrast = gain * (xb - xa)
    gamma0 = gr * 2 * P ** 3
    source193 = sp.cancel(contrast / (gain * (ub - ua)))
    source194 = sp.cancel(contrast / (gain * gamma0 * a0 * tau / omega
                                     * (ub - ua)))
    check("193 complete-price divided gain leaves the exact readiness secant",
          sp.simplify(source193 + gr * qr * (ua + ub) / 2) == 0)
    check("193 two-endpoint source limit is minus gamma0 q over two",
          algebraic_zero((source193.subs({ua: u0, ub: u0})
                          + gamma0 * qr / 2) / (gr * qr)))
    check("194 same field calibration retains the full readiness source",
          sp.simplify(source194
                      + omega * qr * (ua + ub) / (4 * P ** 3 * a0 * tau)) == 0)
    check("194 source limit is nonzero and scales as inverse tau",
          sp.simplify(source194.subs({ua: u0, ub: u0})
                      + omega * qr / (2 * a0 * tau)) == 0)

    inventories = []
    for length, code in ((3, -3), (3, -1), (3, 1), (3, 3)):
        ex = ne.Execution(2, (), (), native_cell(length, code, 0, 1))
        observed = ne.word_matrix(ex)
        expected = sp.diag(G ** length, g_power(code))
        check(f"native W all columns L={length} k={code}",
              ne.exact_matrix_equal(observed, expected))
        counts = ne.inventory(ex, max_qubits=2, max_expanded_stages=100)
        inventories.append((counts.g_count, counts.cx_count, counts.gate_count))
    check("matched code cells count their actual cancelling CX stages",
          set(inventories) == {(3, 6, 9)})
    for code in (1, 3):
        ex = ne.Execution(4, (), (), resource_word(3, code))
        expected = sp.diag(resource_matrix(G ** 3), resource_matrix(g_power(code)))
        check(f"16D readiness word retains dirty c0 complement k={code}",
              ne.exact_matrix_equal(ne.word_matrix(ex), expected))
    return {"symbolic_column_dimension": 8, "control_word_dimension": 16,
            "success_at_original_code": "2*p^3",
            "log_readiness_derivative_u": "-1/2",
            "normalized_plus_is_angle_independent": True}


def finite_native_endpoint_certificates():
    p, u0 = Quadratic(0, 1), Quadratic(-1, 2)
    check("quadratic embedding selects positive original p",
          p.sign() > 0 and (1 - p).sign() > 0 and p * p + p == 1)
    # T_n(u0)=cos(2n theta0); U_n supplies the exact sign of
    # sin(2Q theta0)=2 sqrt(p) p U_(Q-1)(u0).
    t = [Quadratic(1), u0]
    uu = [Quadratic(1), 2 * u0]
    for _ in range(2, 2002):
        t.append(2 * u0 * t[-1] - t[-2])
        uu.append(2 * u0 * uu[-1] - uu[-2])
    found = {}
    for q in range(1, 1001):
        if (t[q] - Fraction(9999, 10000)).sign() > 0:
            sign = uu[q - 1].sign()
            if sign and sign not in found:
                found[sign] = q
            if len(found) == 2:
                break
    check("finite exact search finds both signed native returns", found == {-1: 33, 1: 580})
    rows = []
    for sign, q in sorted(found.items()):
        cr, ur = t[q], uu[q - 1]
        check(f"nonzero exact near-identity native return Q={q}",
              (cr - Fraction(9999, 10000)).sign() > 0
              and (1 - cr).sign() > 0 and ur.sign() == sign)
        # These four brackets certify that both actual G^k columns lie
        # in the positive amplitude branch, without estimating an angle.
        check(f"actual endpoint states remain on the positive branch Q={q}",
              all(value.sign() > 0 for value in (
                  cr - 2 * p * p * ur, cr + 2 * p * p * ur,
                  cr + 2 * p * ur, cr - 2 * p * ur)))
        kp, km = 1 + 2 * q, 1 - 2 * q
        up, um = t[abs(kp)], t[abs(km)]
        sp_, sm_ = (1 - up * up) * Fraction(1, 2), (1 - um * um) * Fraction(1, 2)
        sg0 = 2 * p ** 3
        check(f"both actual algebraic feature endpoints straddle u0 Q={q}",
              (up - u0).sign() * (um - u0).sign() == -1)
        check(f"both actual readiness endpoints straddle original price Q={q}",
              (sp_ - sg0).sign() * (sm_ - sg0).sign() == -1)
        check(f"native endpoint readiness secant is exactly quadratic Q={q}",
              sp_ - sm_ == -(up - um) * (up + um) * Fraction(1, 2))
        factor = 2 * cr * cr - 1
        check(f"complete gain-normalized secant has certified negative source Q={q}",
              up + um == 2 * u0 * factor
              and (factor - Fraction(99960002, 100000000)).sign() > 0
              and (1 - factor).sign() > 0)

        length = max(abs(kp), abs(km))
        counts = []
        inverse_counts = []
        for code in (km, 1, kp):
            ex = ne.Execution(6, (1, 2, 3), (), resource_word(length, code),
                              ne.G_CX_SOURCE_I, source_port=0, source_spin=(4, 5))
            inv = ne.inventory(ex, max_qubits=6, max_expanded_stages=100000)
            counts.append((inv.g_count, inv.cx_count, inv.gate_count))
            reverse = ne.inverse_word(ex, max_qubits=6, max_expanded_stages=100000)
            ri = ne.inventory(replace(ex, gates=reverse), max_qubits=6,
                              max_expanded_stages=100000)
            inverse_counts.append((ri.g_count, ri.cx_count, ri.source_i_count,
                                   ri.gate_count))
        check(f"actual common forward inventory Q={q}",
              set(counts) == {(2 * length, 4 * length + 3, 6 * length + 3)})
        check(f"actual common fully expanded reverse inventory Q={q}",
              set(inverse_counts) == {(2 * length, 16 * length + 3,
                                       8 * length, 26 * length + 3)})

        # Configured price fixture, not a claim these constants close GR.
        # The strict sign also follows symbolically for every positive q,
        # gamma_rest with 0<x<1/2 and 0<d_K<2.
        q_report, gamma_rest = Fraction(1, 4), Fraction(1, 8)
        xp, xm, x0 = gamma_rest * q_report * sp_, gamma_rest * q_report * sm_, gamma_rest * q_report * sg0
        d, zeta = 2 * p * p, Fraction(1, 2 ** 20)

        def determinant(x):
            return 1 - zeta + zeta * (1 - d * x) ** 2

        check(f"complete feedback prices change strictly on both sides Q={q}",
              (determinant(xp) - determinant(x0)).sign() == (up - u0).sign()
              and (determinant(xm) - determinant(x0)).sign() == (um - u0).sign()
              and (xp - xm).sign() == -(up - um).sign())
        rows.append({"Q": q, "return_sine_sign": sign,
                     "codes": {"minus": km, "center": 1, "plus": kp},
                     "common_L": length,
                     "forward": {"G": 2 * length, "CX": 4 * length + 3,
                                 "stages": 6 * length + 3},
                     "expanded_inverse": {"G": 2 * length,
                                          "CX": 16 * length + 3,
                                          "SourceI": 8 * length,
                                          "stages": 26 * length + 3},
                     "u_plus_exact_digest": up.digest(),
                     "u_minus_exact_digest": um.digest(),
                     "normalized_readiness_source":
                         "-Omega*q*(u_plus+u_minus)/(4*p^3*a0*tau)",
                     "relative_factor_bounds_exact": ["0.99960002", "1"]})
    return {"exact_search_limit": 1000, "search_embedding": "a+b*p; p>0; p^2+p=1",
            "near_identity_condition_exact": "cos(2*Q*theta0)>9999/10000",
            "configured_price_fixture": {"q": "1/4", "gamma_rest": "1/8",
                                         "d_K": "2*p^2", "zeta": "2^-20"},
            "universality_scope": "readiness/secant identities are symbolic; fixtures alone do not prove universality",
            "endpoint_certificates": rows}


def book_price_checks():
    ex = ne.Execution(1, (0,), (), (ne.Gate("G", (0,)),))
    p0 = ne.cut_projector(ex)
    clock = bp.build_clock([ne.gate_matrix(ex, ex.gates[0])], p0)
    check("literal clock retains paired heat and one feedback copy",
          clock.heat_dimension == 4 and clock.stages == 1
          and clock.input_rank == 1 and sp.trace(clock.paired_cut) == 1)
    check("endpoint feedback is the actual complete G return",
          ne.exact_matrix_equal(clock.endpoint_feedback, sp.diag(P ** 2, 0)))
    check("full one-stage Hodge pair retains both complete G eigenmodes",
          ne.exact_matrix_equal(clock.paired_delta, (1 - A) * sp.eye(4)))
    price = bp.exact_price(clock, sp.Integer(1), sp.Rational(1, 2 ** 20))
    check("exact Book value uses unnormalized full heat trace",
          sp.simplify(price["heat_trace"] - 4 * sp.exp(-(1 - A))) == 0
          and price["heat_mode_count"] == 4)
    two = bp.build_clock([G, G], p0)
    check("two actual stages, no added idle", two.stages == 2 and two.heat_dimension == 8)
    check("transported cut puts feedback at the sole wrap",
          ne.exact_matrix_equal(two.feedback[:2, :2], sp.zeros(2))
          and ne.exact_matrix_equal(two.feedback[2:, 2:],
                                    G * two.endpoint_feedback * G.T))
    try:
        bp.build_clock([sp.Matrix([[1, 0], [0, 2]])], p0)
    except ValueError:
        check("nonunitary full stage cannot be passed as a prepared compression", True)
    else:
        raise AssertionError("nonunitary full stage accepted")
    try:
        bp.build_clock([G], p0, max_clock_dimension=1)
    except ValueError:
        check("price fixture cap is explicit", True)
    else:
        raise AssertionError("price dimension cap ignored")
    return {"first_fixture": {"stages": 1, "full_hodge_dimension": 4,
                              "cut_rank": 1, "heat_trace": "4*exp(-(1-sqrt(p)))"},
            "second_fixture": {"stages": 2, "full_hodge_dimension": 8}}


def run():
    CHECKS.clear()
    inverse = grammar_and_inverse_checks()
    resource = readiness_column_and_native_cells()
    endpoints = finite_native_endpoint_certificates()
    price = book_price_checks()
    return {"schema": "d0.native-execution-check/1", "status": "PASS",
            "checks_passed": len(CHECKS), "checks": CHECKS,
            "inverse": inverse, "resource": resource,
            "readiness": endpoints, "full_price_fixtures": price,
            "scope": {"finite_candidate_domain_checked": True,
                      "full_dirty_inverse_checked": True,
                      "actual_native_readiness_edit_checked": True,
                      "original_M1_admission_derived": False,
                      "physical_stationarity_selected": False,
                      "full_GR_closed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="save the deterministic readable JSON receipt")
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
