#!/usr/bin/env python3
"""Bounded new cofinal-source arithmetic and native request checks.

Old reflected/AA/polynomial/Cartan matrix proofs are consumed, not replayed.
The new keyed star adapter is checked on all32/64 native columns.  The
rational source/lift examples are diagnostics, not added physical gates.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import cofinal_source as cs

CHECKS = []
PACKET = Path(__file__).resolve().parent
SOURCES = PACKET.parent
REFLECTED = cs.REFLECTED
REPO = SOURCES.parents[2]
PRIMARY = REPO / "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def raises(error, function, *args):
    try:
        function(*args)
    except error:
        return True
    return False


def expected_star(execution, work, keys, a, request, angle_power):
    power = DomainMatrix.from_Matrix(cs.native.G_LOCAL).convert_to(
        cs.native.GOLDEN_FIELD).pow(angle_power).to_Matrix()
    result = sp.zeros(1 << execution.qubits)
    mask = sum(1 << (execution.qubits-1-wire) for wire in work)
    endpoint = sum(1 << (execution.qubits-1-wire) for bit, wire in
                   enumerate(work) if a & (1 << bit))
    for column in range(result.cols):
        key = sum((int(bool(column & (1 << (execution.qubits-1-wire)))) << bit)
                  for bit, wire in enumerate(keys))
        local = sum(int(bool(column & (1 << (execution.qubits-1-wire)))) << bit
                    for bit, wire in enumerate(work))
        if key != request or local not in (0, a):
            result[column, column] = 1
        else:
            old = int(local == a)
            for new in (0, 1):
                result[(column & ~mask) | new*endpoint, column] = power[new, old]
    return result


def run():
    CHECKS.clear()
    ne = cs.native
    # New normalization: physical quadrature is part of the gain, once.
    rows = [dict(alpha=F(3, 2), gamma=F(3, 4), q=F(1, 100),
                 g=F(1, 3), c_quad=F(2)),
            dict(alpha=F(7, 4), gamma=F(4, 5), q=F(1, 100),
                 g=F(1, 5), c_quad=F(3, 2)),
            dict(alpha=F(4, 3), gamma=F(2, 3), q=F(1, 100),
                 g=F(2, 7), c_quad=F(5, 4))]
    tangent = F(7, 11)
    derivatives = [r["g"]*r["c_quad"]*tangent for r in rows]
    correct = cs.normalized_source(rows, derivatives)
    quantities = cs.prefix_quantities(rows)
    wrong_denominator = sum(a*r["g"] for (a, _, _), r in
                            zip(quantities["coefficients"], rows))
    wrong_source = sum(a*dq for (a, _, _), dq in
                       zip(quantities["coefficients"], derivatives))/wrong_denominator
    check("actual gain includes c_quad once and recovers the common physical test source",
          correct == tangent and quantities["gain"] > 0)
    check("omitting actual quadrature produces a different source, not a harmless convention",
          wrong_source != tangent)
    check("new source helper rejects fake continuous/floating or negative gain metadata",
          raises(TypeError, cs.rational, .5)
          and raises(TypeError, cs.rational, True)
          and raises(ValueError, cs.prefix_quantities,
                     [dict(rows[0], c_quad=F(-1))]))

    # Independently differentiate the one cumulative logdet, not sum J_j.
    q_symbols = sp.symbols("q0:3", real=True)
    alpha, gamma = sp.Rational(3, 2), sp.Rational(3, 4)
    zeta = sp.Rational(1, 2**20)
    t_symbols = [1-alpha*gamma*q*(1-gamma*q) for q in q_symbols]
    product = sp.prod(t_symbols)
    rank = 4*2**3
    determinant_price = -rank*sp.log(1-zeta+zeta*product)
    weight = rank*zeta*product/(1-zeta+zeta*product)
    coefficient = [alpha*gamma*(1-2*gamma*q)/t for q, t in
                   zip(q_symbols, t_symbols)]
    check("all variable report rows differentiate the actual product determinant with one rank factor",
          all(sp.cancel(sp.diff(determinant_price, q)-weight*a) == 0
              for q, a in zip(q_symbols, coefficient)))
    check("cumulative price has a genuine mixed derivative and is not sum of standalone prices",
          sp.cancel(sp.diff(determinant_price, q_symbols[0], q_symbols[1])) != 0)
    errors = (F(1, 101), F(-1, 73), F(1, 89))
    actual = cs.normalized_source(rows, [dq+e for dq, e in zip(derivatives, errors)])
    error_average = sum(a*e for (a, _, _), e in
                        zip(quantities["coefficients"], errors))/quantities["A"]
    check("actual heterogeneous gains retain their exact bounded-positive source-error mean",
          actual-tangent == error_average)
    check("each compact Gram is at least one half, slopes stay positive and spin rank is counted once",
          quantities["rank"] == 32
          and all(t >= F(1, 2) and a > 0 and gbar > 0
                  for a, gbar, t in quantities["coefficients"]))

    # An independent real horizontal product lift diagnostic.
    a, b, epsilon = sp.symbols("a b epsilon", real=True)
    va = sp.Matrix([sp.cos(3*epsilon), sp.sin(3*epsilon)])
    vb = sp.Matrix([sp.cos(5*epsilon), sp.sin(5*epsilon)])
    psi = sp.kronecker_product(va, va, vb, vb, vb)
    derivative = psi.diff(epsilon).subs(epsilon, 0)
    lift_sq = cs.physical_lift_sq((2, 3), (F(9), F(25)))
    check("the common physical product lift is sqrt(sum n_j ell_j squared) on horizontal packets",
          (derivative.T*derivative)[0] == lift_sq == 93)
    check("packet number alone is not the physical lift when mesh norms differ",
          lift_sq != 5 and lift_sq/F(5) == F(93, 5))
    variances = (F(1, 19), F(1, 47), F(1, 83))
    product_variance = sp.prod(1+v for v in variances)-1
    certificate_sq = cs.physical_certificate_sq(rows, variances, lift_sq)
    old_half_certificate_sq = 4*lift_sq*product_variance/(quantities["A"]**2)
    check("physical pullback certificate retains factor4; older /(2Gamma) convention is exactly half",
          certificate_sq == 4*old_half_certificate_sq
          and certificate_sq == 16*lift_sq*product_variance/(quantities["A"]**2))
    transport = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                           [sp.Rational(4, 5), sp.Rational(3, 5)]])
    base, base_tangent, effect = sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.diag(0, 1)
    old_dq = (2*base.T*effect*base_tangent)[0]
    new_dq = (2*(transport*base).T*effect*(transport*base_tangent))[0]
    eta_sq = sp.Rational(4, 5)
    check("constant SO transport certifies the same comparison lift through an actual native base without being executed",
          transport.T*transport == sp.eye(2)
          and ((transport-sp.eye(2)).T*(transport-sp.eye(2))) == eta_sq*sp.eye(2)
          and ((transport*base_tangent).T*(transport*base_tangent))[0] == 1
          and (new_dq-old_dq)**2 <= 16*eta_sq)

    budgets = (cs.MeshBudget(2, F(3), F(1, 2), F(1, 2)),
               cs.MeshBudget(3, F(25), F(1, 4), F(1, 2)),
               cs.MeshBudget(4, F(5), F(1, 16), F(1, 2), (F(37),)))
    envelopes = cs.integer_envelopes(budgets)
    check("integer slow envelopes dominate report order squared, physical lift squared and inverse physical gain",
          envelopes == (4, 25, 37)
          and all(C >= max(i, budget.k**2, budget.ell_sq, 1/budget.gbar)
                  for i, (C, budget) in enumerate(zip(envelopes, budgets), 1)))
    check("cofinal threshold transitions are exact integer comparisons with no floating root",
          all(cs.mesh_level(C**64, envelopes) == i for i, C in
                  enumerate(envelopes, 1))
          and cs.mesh_level(25**64-1, envelopes) == 1
          and cs.mesh_level(37**64-1, envelopes) == 2)
    check("only a finite initial envelope exception is used, with no retroactive old catalogue upgrade",
          cs.mesh_level(1, envelopes) == 1
          and cs.mesh_level(10**250, envelopes) == len(envelopes))
    for index, order in ((1, 1), (2, 2), (17, 3), (997, 9), (37**64, 4)):
        count = cs.cohort_size(index, order)
        target = order**8*index**3
        check("actual cohort integer is the minimal fourth-root ceiling j%d k%d" % (index, order),
              count >= 2 and count**4 >= target
              and (count == 2 or (count-1)**4 < target))
        variance = F(2*order**4, count*(count-1))
        check("summable overlap variance obeys its true k-dependent count budget j%d k%d" % (index, order),
              variance**2 * index**3 <= 16)

    eps, growth = F(1, 64), F(3, 4)
    packet_exponent = 1+growth+eps
    lift_sq_exponent = 1+growth+2*eps
    gain_exponent = 1-eps
    rate = lift_sq_exponent/2-gain_exponent
    check("physical all-prefix exponents retain both lift factors and the inverse quadrature gain",
          packet_exponent == F(113, 64)
          and lift_sq_exponent == F(57, 32)
          and gain_exponent == F(63, 64) and rate == F(-3, 32))
    # Exact p-series comparison: sum j^-3/2 <= 1+integral_1^infty x^-3/2 =3.
    check("variance tail has an explicit summable majorant rather than a finite-prefix convergence assertion",
          4*(1+F(1, F(3, 2)-1)) == 12
          and sum(F(1, 4**j) for j in range(1, 13)) < F(1, 3))
    fast_gain = [sum(F(1, 2**j) for j in range(1, M+1)) for M in (8, 32, 128)]
    fast_bound_sq = [F(M, 1)/(gain*gain) for M, gain in zip((8, 32, 128), fast_gain)]
    check("too-fast cofinal physical gains 2^-j are summable and do not yield the vanishing source bound",
          all(gain < 1 for gain in fast_gain)
          and fast_bound_sq[0] < fast_bound_sq[1] < fast_bound_sq[2]
          and fast_bound_sq[-1] > 128)

    native_rows = []
    for count in (2, 3):
        execution, private = cs.native_prefix(count)
        inv = ne.inventory(execution, **cs.rr.bounds(execution))
        check("fresh native prefix has disjoint private work and one immutable oldRIGHT M%d" % count,
              len(set(q for pair in private for q in pair)) == 2*count
              and execution.old_right == (3,)
              and all(3 not in gate.wires for gate in execution.gates))
        check("actual private-prefix raw inventory includes every owned echo and one shared helper/spin M%d" % count,
              inv.gate_count == 45*count
              and (inv.g_count, inv.cx_count, inv.source_i_count) ==
                  (5*count, 26*count, 14*count)
              and inv.full_dimension == 2**(4+2*count)
              and inv.cut_rank == 4*2*2**count)
        stage_length = len(execution.gates)//count
        check("later macros never touch earlier sealed private registers M%d" % count,
              all(not set(q for pair in private[:j] for q in pair).intersection(gate.wires)
                  for j in range(1, count) for gate in execution.gates[j*stage_length:]))
        native_rows.append({"cohorts": count, "stages": inv.gate_count,
            "G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
            "full_dimension": inv.full_dimension, "cut_rank": inv.cut_rank,
            "paired_clock_modes": 2*inv.gate_count*inv.full_dimension,
            "scope": "inventory/protection only; old all-column echo identities consumed"})
    e0, _ = cs.native_prefix(3, old_right_count=0)
    e2, _ = cs.native_prefix(3, old_right_count=2)
    i0 = ne.inventory(e0, **cs.rr.bounds(e0))
    i2 = ne.inventory(e2, **cs.rr.bounds(e2))
    check("additional immutable oldRIGHT input rank is counted once, not once per new macro",
          i2.cut_rank == 4*i0.cut_rank and i2.gate_count == i0.gate_count)

    request_rows = []
    for key_count, request in ((1, 1), (2, 0), (2, 3)):
        keys = tuple(range(4, 4+key_count))
        base = ne.Execution(4+key_count, (0, *keys), (), (),
                            ne.G_CX_SOURCE_I, 0, (1, 2))
        word = cs.keyed_star_word(base, (3,), keys, 1, request=request)
        execution = replace(base, gates=word)
        actual = ne.word_matrix(execution, **cs.rr.bounds(execution))
        expected = expected_star(execution, (3,), keys, 1, request, 1 << key_count)
        inv = ne.inventory(execution, **cs.rr.bounds(execution))
        check("new keyed star adapter equals its ALL-column chosen-sector rotation and exact off-sector identity d%d q%d" % (key_count, request),
              ne.exact_matrix_equal(actual, expected)
              and ne.exact_matrix_equal(actual.T*actual, sp.eye(actual.rows)))
        check("every request is exactly read-only and raw helper/spin is returned d%d q%d" % (key_count, request),
              all(not (gate.op == "G" and gate.wires[0] in keys)
                  and not (gate.op == "CX" and gate.wires[1] in keys)
                  for gate in word)
              and inv.cut_rank == 8)
        all_key_input = replace(execution, blank_wires=(0,))
        all_inv = ne.inventory(all_key_input, **cs.rr.bounds(all_key_input))
        check("known-key and arbitrary-key Book cuts have different actual ranks with the same full thermal carrier d%d q%d" % (key_count, request),
              all_inv.cut_rank == inv.cut_rank*(1 << key_count)
              and all_inv.full_dimension == inv.full_dimension)
        request_rows.append({"key_bits": key_count, "chosen_key": request,
            "all_columns": inv.full_dimension, "stages": inv.gate_count,
            "G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
            "known_blank_key_rank": inv.cut_rank, "arbitrary_key_rank": all_inv.cut_rank})
    base2 = ne.Execution(6, (0, 5), (), (), ne.G_CX_SOURCE_I, 0, (1, 2))
    word2 = cs.keyed_star_word(base2, (3, 4), (5,), 3, request=1)
    execution2 = replace(base2, gates=word2)
    actual2 = ne.word_matrix(execution2, **cs.rr.bounds(execution2))
    expected2 = expected_star(execution2, (3, 4), (5,), 3, 1, 4)
    check("generic native star-plane Q_b construction fixes every other work column with a retained request",
          ne.exact_matrix_equal(actual2, expected2))
    check("new adapter rejects oldRIGHT and individually addressed source-spin keys",
          raises(ne.DomainError, cs.keyed_star_word,
                 ne.Execution(5, (0,), (4,), (), ne.G_CX_SOURCE_I, 0, (1, 2)),
                 (3,), (4,), 1)
          and raises(ne.DomainError, cs.keyed_star_word,
                 ne.Execution(5, (0,), (), (), ne.G_CX_SOURCE_I, 0, (1, 2)),
                 (3,), (1,), 1))

    # Reuse the owned pure-key normal theorem at a read-only block boundary.
    angle = sp.symbols("angle", real=True)
    b0 = sp.diag(sp.Rational(1, 3), sp.Rational(2, 5))
    b1 = sp.diag(sp.Rational(3, 7), sp.Rational(4, 9))
    returned = sp.cos(angle)**2*b0 + sp.sin(angle)**2*b1
    gram = (1-zeta)*sp.eye(2)+zeta*returned.T*returned
    price = -4*sp.log(gram.det())
    check("sharp pure-key preparation has zero first corner and feedback source without adding a native angle primitive",
          returned.diff(angle).subs(angle, 0) == sp.zeros(2)
          and sp.diff(price, angle).subs(angle, 0) == 0)
    eta0, eta1 = sp.symbols("eta0 eta1", real=True)
    psi0 = sp.Matrix([1, 0, 0, 0])
    tangent_key = sp.Matrix([0, 0, eta0, eta1])
    block_kernel = sp.diag(b0, b1)
    check("the same sharp-key first-source cancellation includes entangled off-key/work tangent normals",
          (psi0.T*block_kernel*tangent_key)[0] == 0
          and (tangent_key.T*block_kernel*psi0)[0] == 0)

    return {"status": "PASS", "checks": len(CHECKS), "check_names": list(CHECKS),
            "exact_arithmetic": "Fraction and selected Golden algebraic field",
            "native_prefixes": native_rows, "native_request_adapter": request_rows,
            "cofinal_exponents": {"epsilon": str(eps), "b": str(growth),
                "packet_count": str(packet_exponent), "lift_squared": str(lift_sq_exponent),
                "physical_gain_sum": str(gain_exponent), "source_rate": str(rate)},
            "scopes": ["actual old native echo identity consumed; inventory/protection only",
                "new keyed star word checked on all32/64 columns",
                "no long amplified/factory/Cartan/native bank replay",
                "rational source/lift models are diagnostics, not new native gates",
                "no native C1 selector, source birth, geometric static operator refinement or GR closure"]}


def pin(path):
    data = path.read_bytes()
    return {"path": str(path.relative_to(REPO)), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def section_pin(heading):
    raw = PRIMARY.read_bytes()
    start = raw.index(heading.encode())
    end = raw.find(b"\n## ", start+1)
    section = raw[start:] if end < 0 else raw[start:end]
    return {"heading": heading, "bytes": len(section),
            "sha256": hashlib.sha256(section).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    # New proof files are owned by the disjoint map/theorem assistants.
    inputs = [PACKET / name for name in
              ("cofinal_source.py", "check_cofinal_source.py", "NATIVE_REQUEST.md",
               "GEOMETRIC_MAP.md", "COFINAL_THEOREM.md")]
    inputs += [REFLECTED / name for name in
               ("reflected_report.py", "PROOF.md", "COHORT_THEOREM.md")]
    inputs += [SOURCES / "d0_native_execution_domain_2026-10-24/native_execution.py",
               SOURCES / "d0_native_matrix_collective_return_2026-10-25/PROOF.md"]
    result["source_pins"] = [pin(path) for path in inputs]
    result["section_pins"] = [section_pin("## 7af."), section_pin("## 7ag.")]
    result["generated_utc"] = datetime.now(timezone.utc).isoformat()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
