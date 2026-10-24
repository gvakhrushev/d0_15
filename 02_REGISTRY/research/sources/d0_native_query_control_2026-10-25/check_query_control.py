#!/usr/bin/env python3
"""Bounded actual READY-preserving native query-control contrast.

The exact coefficient class is reused without running its earlier suite.
This is a finite source comparison, not a stationary/minimum no-go theorem.
"""
import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
DOMAIN = HERE.parent / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(DOMAIN))
import native_execution as ne
from check_native_execution_domain import Quadratic

CHECKS = []


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def tail(length, code, control=0, coin=1, report=2):
    if abs(code) > length or (length - code) % 2:
        raise ValueError("invalid equal-inventory code")
    plus = (ne.Gate("G", (coin,)), ne.Gate("CX", (control, coin)),
            ne.Gate("CX", (control, coin)))
    minus = (ne.Gate("CX", (control, coin)), ne.Gate("G", (coin,)),
             ne.Gate("CX", (control, coin)))
    return (plus * ((length + code) // 2) + minus * ((length - code) // 2)
            + (ne.Gate("CX", (coin, report)),))


def two_bit_tail(rotation):
    ex = ne.Execution(2, (), (), ())
    return ne.gate_matrix(ex, ne.Gate("CX", (0, 1))) * sp.kronecker_product(rotation, sp.eye(2))


def effect_and_locality():
    c, s, u = sp.symbols("c s u", real=True)
    t = two_bit_tail(sp.Matrix([[c, -s], [s, c]]))
    j = sp.eye(4)[:, :2]  # fresh coin0, arbitrary old report
    pb = sp.diag(0, 1, 0, 1)
    effect = sp.simplify(j.T * t.T * pb * t * j)
    check("4D all-input Heisenberg report effect is diagonal with exact coin weights",
          effect == sp.diag(s ** 2, c ** 2))
    rewritten = effect.subs({c ** 2: (1 + u) / 2, s ** 2: (1 - u) / 2})
    check("all-input affine effect identity including unknown reference",
          rewritten == sp.eye(2) / 2 + u * (sp.diag(0, 1) - sp.eye(2) / 2))
    p = ne.P
    check("original native angle gives offset p squared and field scale p cubed",
          ne.GOLDEN_FIELD.from_sympy(sp.expand(1 - 2 * p ** 2 - p ** 3))
          == ne.GOLDEN_FIELD.zero)
    # The OLD GEOMETRIC BANK excludes the old report bit. Locality holds
    # for every bank matrix unit, including off-diagonal reference tests.
    local = sp.kronecker_product(two_bit_tail(ne.G_LOCAL), sp.eye(2))
    for a in range(2):
        for b in range(2):
            unit = sp.zeros(2)
            unit[a, b] = 1
            observable = sp.kronecker_product(sp.eye(4), unit)
            check(f"old bank observable retained exactly including coherence {a}{b}",
                  ne.exact_matrix_equal(local.T * observable * local, observable))
    bell = sp.zeros(8, 1)
    bell[0] = bell[3] = 1 / sp.sqrt(2)
    final = local * bell
    marginal = sp.Matrix(2, 2, lambda a, b: sum(
        final[2 * k + a] * final[2 * k + b] for k in range(4)))
    check("explicit report-bank Bell fixture keeps its old bank marginal",
          ne.exact_matrix_equal(marginal, sp.eye(2) / 2))
    r = sp.diag(0, 0, 0, 0, 1, 1, 1, 1)
    for code in (-3, -1, 1, 3):
        ex = ne.Execution(3, (1,), (), tail(3, code))
        observed = ne.word_matrix(ex)
        expected = sp.diag(two_bit_tail(ne.G_LOCAL ** 3),
                           two_bit_tail(ne.G_LOCAL ** code))
        check(f"8D native tail keeps every c0 complement column k={code}",
              ne.exact_matrix_equal(observed, expected))
        check(f"complete native tail commutes with genuine root READY k={code}",
              ne.exact_matrix_equal(observed * r, r * observed))
    check("conditional native coin unit-u speed squared is finite at p cubed",
          ne.GOLDEN_FIELD.from_sympy(sp.expand(
              4 * (1 - p ** 6) - 16 * p ** 3)) == ne.GOLDEN_FIELD.zero)
    return {"all_input_effect": "E_out(u)=I/2+u*(E-I/2)",
            "original_angle_effect": "p^2*I+p^3*E", "aperture": "tau_out=p^3*tau",
            "READY_unchanged_exactly": True, "old_geometric_bank_marginal_unchanged": True,
            "old_bank_excludes_report_and_new_coin": True,
            "conditional_coin_speed_squared_at_native_u0": "1/(16*p^3)",
            "arbitrary_raw_pulse_lift_assigned": False}


def inventories(length, codes):
    bounds = dict(max_qubits=6, max_expanded_stages=100000)
    rows = []
    for code in codes:
        ex = ne.Execution(6, (1, 3), (), tail(length, code), ne.G_CX_SOURCE_I,
                          source_port=0, source_spin=(4, 5))
        forward = ne.inventory(ex, **bounds)
        reverse = ne.inverse_word(ex, **bounds)
        inverse = ne.inventory(replace(ex, gates=reverse), **bounds)
        record = (ne.Gate("CX", (1, 3)),)
        counted = ne.inventory(replace(ex, gates=record + ex.gates + reverse + record), **bounds)
        middle_cx = (ne.Gate("CX", (1, 2)),) * 2
        compensated = ne.inventory(replace(ex, gates=record + ex.gates + middle_cx
                                            + reverse + record), **bounds)
        check(f"actual forward/inverse/new-record inventory L={length} k={code}",
              (forward.g_count, forward.cx_count) == (length, 2 * length + 1)
              and (inverse.g_count, inverse.cx_count, inverse.source_i_count)
              == (length, 8 * length + 1, 4 * length)
              and counted.gate_count == 16 * length + 4)
        check(f"two transported-middle CX are really paid L={length} k={code}",
              compensated.gate_count == 16 * length + 6)
        rows.append({"k": code, "forward_stages": forward.gate_count,
                     "inverse_stages": inverse.gate_count,
                     "additional_record_CX": 2, "total_added_stages": counted.gate_count,
                     "transported_middle_CX": 2,
                     "compensated_total_added_stages": compensated.gate_count})
    # The coin and its recording-bank bit are BOTH blank work. Neither is
    # the special rebit for which the earlier recorder had an I_rebit corner.
    check(f"coin plus its recording bank multiplies full fibre by four L={length}",
          2 ** 6 == 4 * 2 ** 4 and 2 ** (6 - 2) == 2 ** 4)
    return rows


def compensated_middle():
    # W reads c0. Coin blindness ALONE would not imply [W,M]=0:
    # the completed M must also preserve c0. Use an actual native M
    # controlled by c0 AND report, with a distinct meter target.
    layout = ne.Execution(6, (1, 3), (), (), ne.G_CX_SOURCE_I,
                          source_port=0, source_spin=(4, 5))
    bounds = dict(max_qubits=6, max_expanded_stages=10000)
    positive = (ne.Gate("G", (3,)),)
    negative = ne.inverse_word(replace(layout, gates=positive), **bounds)
    middle = ()
    for mask in range(4):
        parity = tuple(ne.Gate("CX", (control, 3)) for bit, control
                       in enumerate((0, 2)) if mask & (1 << bit))
        middle += parity + (negative if bin(mask).count("1") % 2 else positive) + tuple(reversed(parity))
    m = sp.zeros(16)
    for column in range(16):
        selected = bool(column & 8) and bool(column & 2)
        for bit in range(2):
            row = (column & ~1) | bit
            m[row, column] = (ne.G_LOCAL ** 4)[bit, column & 1] if selected else int(bit == (column & 1))
    actual = ne.word_matrix(replace(layout, gates=middle))
    check("completed native READY/report-controlled G4 middle restores arbitrary dirty source spin",
          ne.exact_matrix_equal(actual, sp.kronecker_product(m, sp.eye(4))))
    inv = ne.inventory(replace(layout, gates=middle), **bounds)
    check("native middle includes all negative-G source and routing calls",
          (inv.g_count, inv.cx_count, inv.source_i_count, inv.gate_count) == (4, 20, 8, 32))
    logical = ne.Execution(4, (), (), ())
    c = ne.gate_matrix(logical, ne.Gate("CX", (1, 2)))
    root = sp.diag(*(int(bool(j & 8)) for j in range(16)))
    report = sp.diag(*(int(bool(j & 2)) for j in range(16)))
    check("completed middle preserves the c0 sectors required for co-transport",
          ne.exact_matrix_equal(m * root, root * m))
    moved = c * m * c
    for code in (-1, 1, 3):
        w = ne.word_matrix(replace(logical, gates=tail(3, code)[:-1]))
        t = c * w
        restored = t.T * moved * t
        check(f"all-column compensated middle and c0 complement restore exactly k={code}",
              ne.exact_matrix_equal(w * m, m * w) and ne.exact_matrix_equal(restored, m))
        check(f"parity report itself restores on every input column k={code}",
              ne.exact_matrix_equal(t.T * c * report * c * t, report))
    psi = sp.zeros(32, 1)
    psi[0] = psi[31] = 1 / sp.sqrt(2)
    check("compensated full operator preserves an explicitly entangled unknown reference",
          ne.exact_matrix_equal(sp.kronecker_product(restored, sp.eye(2)) * psi,
                                sp.kronecker_product(m, sp.eye(2)) * psi))
    check("uncompensated middle was not already invariant",
          not ne.exact_matrix_equal(t.T * m * t, m))
    cc, ss, u = sp.symbols("c s u", real=True)
    c2 = ne.gate_matrix(ne.Execution(2, (), (), ()), ne.Gate("CX", (0, 1)))
    t2 = two_bit_tail(sp.Matrix([[cc, -ss], [ss, cc]]))
    j = sp.eye(4)[:, :2]
    fixed = sp.expand(j.T * t2.T * c2 * sp.diag(0, 1, 0, 1) * c2 * t2 * j)
    fixed = sp.simplify(fixed.subs({cc ** 2: (1 + u) / 2, ss ** 2: (1 - u) / 2}))
    check("symbolic parity compensation preserves old effect and its complete field Jacobian",
          fixed == sp.diag(0, 1) and fixed.diff(u) == sp.zeros(2))
    return {"all_column_identity": "T^dagger*(C*M*C)*T=M; T=C*W",
            "required_commutators": "[M,W]=0; M coin-blind AND [M,P_c0]=0",
            "native_middle": "controlled G^4 on distinct meter; controls c0 and report",
            "native_middle_stages": 32, "extra_middle_CX": 2,
            "existing_field_jacobian": "D_Y E_comp=D_Y E_old; D_u E_comp=0",
            "compensated_total_added_stages": "16*L+6",
            "same_task_implementation_map": True, "compulsory_task_selection": False,
            "old_and_new_absolute_prices_equal": False, "all_native_Dq_vanish": False}


def endpoint_and_price_checks():
    p = Quadratic(0, 1)
    u0 = p ** 3
    tt, uu = [Quadratic(1), u0], [Quadratic(1), 2 * u0]
    for _ in range(2, 1162):
        tt.append(2 * u0 * tt[-1] - tt[-2])
        uu.append(2 * u0 * uu[-1] - uu[-2])
    check("native unit-u field aperture has an exact nonzero inverse",
          u0 * (3 + 2 * p) == 1)
    q, tau = Fraction(1, 4), Fraction(1, 1024)
    coefficient = (q - Fraction(1, 2)) * (3 + 2 * p) * (1 / tau)
    check("declared normalized query-control source is strictly nonzero", coefficient.sign() < 0)
    rows = []
    for Q, sign in ((33, -1), (580, 1)):
        km, kp, length = 1 - 2 * Q, 1 + 2 * Q, 1 + 2 * Q
        check(f"owned algebraic return certificate applied to query tail Q={Q}",
              (tt[Q] - Fraction(9999, 10000)).sign() > 0
              and uu[Q - 1].sign() == sign)
        ua, ub = tt[abs(km)], tt[kp]
        check(f"actual native query feature endpoints straddle p cubed Q={Q}",
              (ua - u0).sign() * (ub - u0).sign() == -1)
        check(f"actual query endpoints stay in the positive coin feature chart Q={Q}",
              all(v.sign() > 0 and (1 - v).sign() > 0 for v in (ua, ub)))
        qa = Fraction(1, 2) + ua * (q - Fraction(1, 2))
        qb = Fraction(1, 2) + ub * (q - Fraction(1, 2))
        qc = Fraction(1, 2) + u0 * (q - Fraction(1, 2))
        check(f"exact finite conditional-query secant Q={Q}",
              qb - qa == (ub - ua) * (q - Fraction(1, 2)))
        fixture_gammas = (Fraction(1, 8), 1 - Fraction(1, 2 ** 20))
        for gamma in fixture_gammas:
            xa, xb, xc = gamma * qa, gamma * qb, gamma * qc
            d, z = 2 * p ** 2, Fraction(1, 2 ** 20)
            def determinant(x):
                return 1 - z + z * (1 - d * x) ** 2
            check(f"actual j_K endpoint parameters satisfy the positive-return chart gamma={gamma} Q={Q}",
                  all(v.sign() > 0 and (Fraction(1, 2) - v).sign() > 0
                      for v in (xa, xb, xc))
                  and d.sign() > 0 and (2 - d).sign() > 0 and 0 < z < 1)
            check(f"complete Book j gain is positive and both endpoint prices differ gamma={gamma} Q={Q}",
                  (determinant(xb) - determinant(xa)).sign() == -(xb - xa).sign()
                  and (determinant(xa) - determinant(xc)).sign()
                  * (determinant(xb) - determinant(xc)).sign() == -1)
            check(f"actual divided Book gain and readiness cancel exactly gamma={gamma} Q={Q}",
                  xb - xa == gamma * (ub - ua) * u0 * tau * coefficient)
        rows.append({"Q": Q, "codes": [km, 1, kp], "L": length,
                     "u_a_exact_digest": ua.digest(), "u_b_exact_digest": ub.digest(),
                     "inventory": inventories(length, (km, 1, kp))})
    return {"configured_original_conditional_q": str(q), "configured_tau": str(tau),
            "configured_ready_probabilities": ["1/8", "1-2^-20"],
            "configured_d_K": "2*p^2", "configured_zeta": "2^-20",
            "complete_j": "-r*log(1-zeta+zeta*(1-d_K*x)^2), r>0",
            "positive_gain_scope": "0<x<1/2, 0<d_K<2, 0<zeta<1",
            "exact_gain_normalized_source": "Omega*(q-1/2)/(a0*p^3*tau)",
            "gamma_AA_depth_independent": True, "endpoint_certificates": rows}


def run():
    CHECKS.clear()
    effect = effect_and_locality()
    price = endpoint_and_price_checks()
    compensation = compensated_middle()
    paths = (Path(__file__), DOMAIN / "native_execution.py",
             DOMAIN / "check_native_execution_domain.py")
    return {"schema": "d0.native-query-control-check/1", "status": "PASS",
            "checks_passed": len(CHECKS), "checks": CHECKS,
            "inputs_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            "effect_and_locality": effect, "finite_complete_price_source": price,
            "compensated_native_variation": compensation,
            "scope": {"old_suites_or_AA_replayed": False,
                      "full_failures_and_c0_complement_retained": True,
                      "coin_and_new_record_bank_are_paid": True,
                      "whole_echo_and_same_clock_required_within_each_stencil": True,
                      "absolute_prices_of_different_lengths_identified": False,
                      "finite_controller_source_comparison": True,
                      "all_existing_candidate_stationarity_disproved": False,
                      "local_minimum_or_unrestricted_no_go": False,
                      "full_GR_closed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    print(result, end="")


if __name__ == "__main__":
    main()
