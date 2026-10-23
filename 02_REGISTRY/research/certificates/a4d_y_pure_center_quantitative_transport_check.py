#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact all-row pure-Y transport and a refinement-independent nonlinear bound.

The literal flat-solder Euler map on arbitrary real even-site Y amplitudes
is linear in u(a)=4a/(4+3a^2), v(a)=2a^2/(4+3a^2). Its coefficient sums
vanish separately. Two boost rows on every transport edge recover du,dv,
with du^2+3dv^2=16(a-b)^2/((4+3a^2)(4+3b^2)).

This supplies a quantitative pure-Y gradient bound and an exact derivative
factor in its nonlinear remainder. Transverse corrections and genuinely
curved metrics are outside this theorem. No task terminal is promoted.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp
import a4d_y_curved_joint_rational_stencil as S
import a4d_y_slow_exact_plane_check as literal

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_pure_center_quantitative_transport_results.json"
ZERO = (0, 0, 0, 0)


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def shift(x, role, step=1):
    return tuple(v + (step if j == role else 0) for j, v in enumerate(x))


def phase(p, x):
    return (p + sum(x)) % 4


def clean(terms):
    return {d: {rc: v for rc, v in entries.items() if v}
            for d, entries in terms.items() if any(entries.values())}


def polynomial_product(items):
    """Every temporal face has only one nonidentity even-phase K0 factor."""
    result = {None: S.I4}
    for polynomial in items:
        out = {}
        for k, left in result.items():
            for ell, right in polynomial.items():
                if k is not None and ell is not None:
                    raise AssertionError("TWO_ACTIVE_TEMPORAL_FACTORS_IN_FACE")
                key = k if k is not None else ell
                value = S.mm(left, right)
                out[key] = S.madd(out.get(key, S.zero()), value)
        result = out
    return result


def link_polynomial(p, site, role, inverse=False):
    result = {None: S.I4}
    ph = phase(p, site)
    if role == 0 and ph in (0, 2):
        result[(site, 0)] = S.mscale(1 if ph == 0 else -1, S.Y)
        result[(site, 1)] = S.Y2
    return ({key: S.linv(value) for key, value in result.items()}
            if inverse else result)


def face_polynomial(p, base, a, b, corner=None, generator=None):
    places = ((base, a, False), (shift(base, a), b, False),
              (shift(base, b), a, True), (base, b, True))
    factors = [link_polynomial(p, x, role, inverse)
               for x, role, inverse in places]
    if corner is not None:
        inverse = places[corner][2]
        factors[corner] = {
            key: S.mscale(-1, S.mm(generator, value)) if inverse
            else S.mm(value, generator)
            for key, value in factors[corner].items()
        }
    # On Lorentz links, inverse differentiation is exactly linv(dP).
    # This form avoids introducing spurious products of Cayley coefficients.
    return {key: S.mscale(F(1, 2), S.msub(value, S.linv(value)))
            for key, value in polynomial_product(factors).items()}


def build_euler_coefficients():
    constant = defaultdict(F)
    coefficients = [defaultdict(dict), defaultdict(dict)]

    def add(row, p, key, value):
        if not value:
            return
        if key is None:
            constant[row] += value
            return
        d, component = key
        input_phase = phase(p, d)
        if input_phase not in (0, 2):
            raise AssertionError("INPUT_IS_NOT_AN_EVEN_PHASE_Y_LINK")
        rc = (row, input_phase // 2)
        coefficients[component][d][rc] = (
            coefficients[component][d].get(rc, F(0)) + value)

    for p in range(4):
        for role in range(4):
            for gi, generator in enumerate(S.GEN):
                row = 24*p + 6*role + gi
                for a, b in S.PAIRS:
                    if role == a:
                        corners = ((ZERO, 0), (shift(ZERO, b, -1), 2))
                    elif role == b:
                        corners = ((shift(ZERO, a, -1), 1), (ZERO, 3))
                    else:
                        continue
                    u, v = [j for j in range(4) if j not in (a, b)]
                    area = S.wedge(S.BASIS[u], S.BASIS[v])
                    for base, corner in corners:
                        for key, curvature in face_polynomial(
                                p, base, a, b, corner, generator).items():
                            add(row, p, key, F(S.orient(a, b)) *
                                S.pair_star(area, S.biv(curvature)))
        for mi, (qa, qb) in enumerate(S.SYM):
            row = 96 + 10*p + mi
            metric_lift = S.metric_lift(qa, qb)
            for a, b in S.PAIRS:
                u, v = [j for j in range(4) if j not in (a, b)]
                first = S.wedge([metric_lift[i][u] for i in range(4)],
                                S.BASIS[v])
                second = S.wedge(S.BASIS[u],
                                 [metric_lift[i][v] for i in range(4)])
                area = [x + y for x, y in zip(first, second)]
                for key, curvature in face_polynomial(p, ZERO, a, b).items():
                    add(row, p, key, F(S.orient(a, b)) *
                        S.pair_star(area, S.biv(curvature)))
    ck("ALL_136_ROWS_HAVE_ZERO_CONSTANT_PART",
       all(not value for value in constant.values()))
    return [clean(eq) for eq in coefficients]


def encode(terms):
    return [{"shift": list(d), "entries": [
        [r, c, str(value)] for (r, c), value in sorted(entries.items())]}
        for d, entries in sorted(terms.items())]


def row_coefficients(terms, row):
    return {d: value for d, entries in terms.items()
            for (r, c), value in entries.items() if r == row}


def run(write=False):
    owned = json.loads((HERE / "a4d_y_pure_center_transport_results.json").read_text())
    ck("CONSUME_SIGN_FREE_TRANSPORT_OWNER",
       owned["schema"] == "a4d-y-pure-center-transport-v3" and
       owned["transport_lattice"]["index_in_Z4"] == 2)
    ck("Y_CUBIC", S.mm(S.Y2, S.Y) == S.mscale(-3, S.Y))
    E = build_euler_coefficients()
    counts = [sum(map(len, eq.values())) for eq in E]
    ck("FULL_EULER_COEFFICIENT_COUNTS", counts == [84, 108])

    for index, eq in enumerate(E):
        sums = defaultdict(F)
        for entries in eq.values():
            for (r, c), value in entries.items():
                sums[r] += value
        ck("CONSTANT_FAMILY_COMPONENT_SUMS_ZERO_" + str(index),
           all(not value for value in sums.values()))
    ck("METRIC_EULER_U_ONLY",
       all(row < 96 for entries in E[1].values() for row, col in entries))

    a, b, z = sp.symbols("a b z", real=True)
    D = 4 + 3*z*z
    u = 4*z/D
    v = 2*z*z/D
    uprime, vprime = [F(sp.diff(fun, z).subs(z, 1)) for fun in (u, v)]
    ck("CAYLEY_SCALAR_DERIVATIVES_AT_ONE", (uprime, vprime) == (F(4, 49), F(16, 49)))
    linear = defaultdict(dict)
    for eq, factor in zip(E, (uprime, vprime)):
        for d, entries in eq.items():
            for rc, value in entries.items():
                linear[d][rc] = linear[d].get(rc, F(0)) + factor*value
    expected = defaultdict(dict)
    for source, offset in ((S.ATERMS, 0), (S.QTERMS, 96)):
        for d, entries in source.items():
            for (row, col), value in entries.items():
                ph, role, generator = S.LABELS[col]
                if role == 0 and ph in (0, 2) and generator in (3, 4, 5):
                    rc = (offset+row, ph//2)
                    sign = (1 if ph == 0 else -1) * (1 if generator in (3, 5) else -1)
                    expected[d][rc] = expected[d].get(rc, F(0)) + F(4, 7)*sign*value
    ck("ALL_ROW_TANGENT_MATCHES_LITERAL_JOINT_LAURENT_STENCIL",
       clean(linear) == clean(expected))

    # Independently replay the nonlinear identity, including all incoming
    # incidences, using the old owner's inverse-plaquette derivative rather
    # than our coefficientwise Lorentz-transpose derivative.
    def amplitude(site):
        return F(1) + F(sum((j+1)*((x+2) % 3-1)
                            for j, x in enumerate(site)), 30)

    def scalar_values(value):
        den = 4+3*value*value
        return (4*value/den, 2*value*value/den)

    @lru_cache(None)
    def rational_link(site, role):
        if role != 0 or sum(site) % 4 not in (0, 2):
            return literal.I4
        wave = literal.cayley_simple(literal.GEN[3]-literal.GEN[4]+literal.GEN[5],
                                    3, sp.Rational(amplitude(site)))
        return wave if sum(site) % 4 == 0 else literal.linv(wave)

    direct = []
    for ph in range(4):
        site = (0, ph, 0, 0)
        direct += [literal.edge_euler(lambda _: literal.I4, rational_link,
                                     site, role, generator)
                   for role in range(4) for generator in literal.GEN]
    for ph in range(4):
        site = (0, ph, 0, 0)
        solder_rows = literal.solder_euler(lambda _: literal.I4, rational_link, site)
        for qa, qb in S.SYM:
            lift = S.metric_lift(qa, qb)
            direct.append(sum(solder_rows[i, j]*sp.Rational(lift[i][j])
                              for i in range(4) for j in range(4)))
    nonlinear = [F(0) for _ in range(136)]
    for component, eq in enumerate(E):
        for d, entries in eq.items():
            for (row, col), value in entries.items():
                ph = row//24 if row < 96 else (row-96)//10
                site = (0, ph, 0, 0)
                source_site = tuple(x+y for x, y in zip(site, d))
                nonlinear[row] += value*scalar_values(amplitude(source_site))[component]
    ck("NONCONSTANT_RATIONAL_FIELD_ALL_136_LITERAL_EULER_ROWS",
       nonlinear == [F(value) for value in direct] and any(nonlinear))

    edge_records = []
    for ph in range(4):
        for role in (1, 2, 3):
            if ph % 2 == 0:
                left, right = ZERO, shift(shift(ZERO, 0, -1), role)
            else:
                left, right = shift(ZERO, role), shift(ZERO, 0, -1)
            primary = 24*ph + 6*role + role-1
            secondary = 24*ph + 6*role + role % 3
            sign = -1 if ph in (0, 1) else 1
            ck(f"EDGE_{ph}_{role}_PRIMARY_DV",
               not row_coefficients(E[0], primary) and
               row_coefficients(E[1], primary) == {left: F(1), right: F(-1)})
            ck(f"EDGE_{ph}_{role}_SECONDARY_DU_DV",
               row_coefficients(E[0], secondary) == {left: F(sign, 2), right: F(-sign, 2)} and
               row_coefficients(E[1], secondary) == {left: F(-1, 2), right: F(1, 2)})
            edge_records.append({"phase": ph, "role": role,
                                 "rows": [primary, secondary],
                                 "left_shift": list(left), "right_shift": list(right),
                                 "secondary_du_sign": sign})

    du = sp.factor(u.subs(z, a)-u.subs(z, b))
    dv = sp.factor(v.subs(z, a)-v.subs(z, b))
    chord = 16*(a-b)**2/((4+3*a*a)*(4+3*b*b))
    ck("EXACT_CAYLEY_CHORD_IDENTITY", sp.factor(du*du+3*dv*dv-chord) == 0)
    e1, e2 = sp.symbols("e1 e2", real=True)
    ck("TWO_BOOST_ROWS_CONTROL_CAYLEY_CHORD",
       sp.expand(6*(e1*e1+e2*e2)-((2*e2+e1)**2+3*e1*e1)-2*(e1-e2)**2) == 0)
    max_den = F(43, 4)  # |a|,|b| <= 3/2
    ck("COMPACT_CHART_GRADIENT_CONSTANT_SEVEN", 6*max_den**2 < 16*7**2)
    ck("PRIMARY_ONLY_SIGN_FLIP_NEGATIVE_CONTROL",
       dv.subs({a: 1, b: -1}) == 0 and du.subs({a: 1, b: -1}) != 0)
    large_du, large_dv = [fun.subs({a: 100, b: 101}) for fun in (du, dv)]
    large_secondary = (large_du+large_dv)/2
    ck("UNBOUNDED_AMPLITUDE_NEGATIVE_CONTROL",
       49*(large_dv**2+large_secondary**2) < 1)

    moves = [shift(shift(ZERO, role), 0, sign)
             for role in (1, 2, 3) for sign in (-1, 1)]
    signed_moves = sorted(moves + [tuple(-x for x in move) for move in moves])
    words = {ZERO: []}
    for move in signed_moves:
        words.setdefault(move, [move])
    for first in signed_moves:
        for second in signed_moves:
            total = tuple(x+y for x, y in zip(first, second))
            words.setdefault(total, [first, second])
    difference_paths = {}
    for eq in E:
        for d, entries in eq.items():
            for row, col in entries:
                ph = row//24 if row < 96 else (row-96)//10
                reference = ZERO if ph % 2 == 0 else shift(ZERO, 0)
                delta = tuple(x-y for x, y in zip(d, reference))
                if delta not in words:
                    raise AssertionError(("NO_FINITE_DIFFERENCE_PATH", delta))
                difference_paths[delta] = words[delta]
    ck("FINITE_DIFFERENCE_PATHS_REPLAY",
       all(tuple(sum(move[j] for move in path) for j in range(4)) == delta
           for delta, path in difference_paths.items()))
    ck("AT_MOST_TWO_TRANSPORT_STEPS",
       max(map(len, difference_paths.values())) == 2)

    u2 = 72*z*(z*z-4)/D**3
    v2 = 16*(4-9*z*z)/D**3
    ck("EXACT_SECOND_DERIVATIVES",
       sp.factor(sp.diff(u, z, 2)-u2) == 0 and sp.factor(sp.diff(v, z, 2)-v2) == 0)
    # |z|<=3/2: D>=4, |z^2-4|<=4, |4-9z^2|<=65/4.
    mu, mv = F(27, 4), F(65, 16)
    ck("COMPACT_SECOND_DERIVATIVE_BOUNDS",
       F(72)*F(3, 2)*4/4**3 == mu and
       F(16)*F(65, 4)/4**3 == mv and F(9)*F(3, 2)**2-4 == F(65, 4))
    totals = [sum(abs(value) for entries in eq.values() for value in entries.values()) for eq in E]
    metric_totals = [sum(abs(value) for entries in eq.values()
                         for (row, col), value in entries.items() if row >= 96) for eq in E]
    ck("FULL_COEFFICIENT_SUMS", totals == [F(42), F(72)])
    remainder_constant = 2*(totals[0]*mu+totals[1]*mv)
    metric_constant = 2*(metric_totals[0]*mu+metric_totals[1]*mv)
    ck("FULL_NONLINEAR_REMAINDER_CONSTANT", remainder_constant == 1152)
    ck("METRIC_NONLINEAR_REMAINDER_CONSTANT", metric_totals == [F(6), F(0)] and metric_constant == 81)

    ledger = [encode(eq) for eq in E]
    ledger_hash = hashlib.sha256(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "schema": "a4d-y-pure-center-quantitative-transport-v1",
        "terminal": "A4D-Y-PURE-CENTER-QUANTITATIVE-TRANSPORT-CERTIFIED",
        "background": "fixed standard solder; spatial links identity; arbitrary real even-site Y Cayley amplitudes",
        "scalar_functions": {"u": "4*a/(4+3*a^2)", "v": "2*a^2/(4+3*a^2)"},
        "full_euler_shape": [136, 2],
        "connection_rows": 96, "metric_rows": 40,
        "coefficient_counts": counts,
        "coefficient_ledgers": ledger,
        "coefficient_ledgers_sha256": ledger_hash,
        "exact_formula": "E_Y(a)=T_u u(a)+T_v v(a); T_u 1=T_v 1=0",
        "all_row_derivative_control": "D E_Y(1) equals Q_Bloch times the exact Cayley family tangent, coefficient by coefficient",
        "independent_nonlinear_control": "all 136 components agree on a nonconstant rational field with the literal inverse-plaquette and unrestricted solder owner",
        "edge_records": edge_records,
        "chord_identity": "du^2+3*dv^2=16*(a-b)^2/((4+3*a^2)*(4+3*b^2))",
        "compact_amplitude_interval": "[-3/2,3/2]",
        "edge_gradient_bound": "|a-b| <= 7*sqrt(primary_boost_row^2+secondary_boost_row^2)",
        "transport_moves": [list(move) for move in moves],
        "difference_paths": [{"difference": list(delta), "moves": [list(move) for move in path]}
                             for delta, path in sorted(difference_paths.items())],
        "periodic_oscillation_bound": "osc(a) <= 28*L*max_selected_boost_pair_norm for L in 4N",
        "second_derivative_bounds": {"u": str(mu), "v": str(mv)},
        "coefficient_absolute_sums": [str(total) for total in totals],
        "metric_coefficient_absolute_sums": [str(total) for total in metric_totals],
        "nonlinear_remainder_bound": "||E_Y(z0+c)-D E_Y(z0)c||_p,comp <= 1152*||c||_infinity*max_move||Delta_move c||_p",
        "nonlinear_remainder_constant": str(remainder_constant),
        "metric_remainder_constant": str(metric_constant),
        "remainder_hypotheses": "z0 and z0+c in [-3/2,3/2]; 1<=p<=infinity; coordinate component-sum output norm; constant site weighting allowed",
        "scaling_consequence": "if ||c_h||_infinity=O(h) and the actual gradient norm is O(h^2), the remainder in that norm is O(h^3)",
        "negative_controls": ["primary row alone misses nonzero sign flips", "compact gradient constant fails without an amplitude bound"],
        "scope_fence": [
            "pure-Y sector at the flat metric only; transverse/non-Y corrections are excluded from the theorem, not from the physical equations",
            "does not close the global full-joint Bloch locus or its compact-complement gap",
            "does not solve the genuinely curved reduced compatibility equations",
            "pointwise O(h^3) is not O(h^3) in the unweighted owner sum norm without its actual gradient-norm hypothesis",
            "no exact curved sheet, nonlinear contraction, source-response universality, or task-level terminal is asserted",
        ],
    }
    if write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT, flush=True)
    else:
        ck("RESULTS_MATCH_PINNED_JSON", OUT.exists() and json.loads(OUT.read_text()) == result)
    print("TERMINAL", result["terminal"], flush=True)
    return result


if __name__ == "__main__":
    run("--write" in sys.argv[1:])
