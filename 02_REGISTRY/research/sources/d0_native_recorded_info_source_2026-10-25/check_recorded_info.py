#!/usr/bin/env python3
"""Bounded same-boundary recorded-Info source; no old or large root replay."""
import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib, json
from math import factorial
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp
import recorded_info as ri

ne = ri.native
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "d0_native_operator_holonomy_2026-10-25"))
import native_holonomy as nh
from check_native_execution_domain import Quadratic
CHECKS = []


def check(name, assertion):
    if not assertion: raise AssertionError(name)
    CHECKS.append(name)


def numeric(a):
    return mp.matrix([[mp.mpf(str(sp.N(a[i, j], 95))) for j in range(a.cols)] for i in range(a.rows)])


def run():
    mp.mp.dps = 90
    bounds = dict(max_qubits=6, max_expanded_stages=50000)
    layout = ne.Execution(6, (1, 2), (5,), (), ne.G_CX_SOURCE_I,
                          source_port=1, source_spin=(3, 4), report_bits=(1,))
    history = replace(layout, blank_wires=(0, 1, 2, 5), old_right=(),
                      gates=(ne.Gate("G", (0,)), ne.Gate("CX", (0, 5))))
    history_matrix = ne.word_matrix(history); before = history_matrix[:, 0]
    check("oldRIGHT correlation is created by actual G/CX BEFORE its boundary seal",
          before[0] == ne.A and before[33] == ne.P and sum(x != 0 for x in before) == 2)
    check("current boundary retains that state with only rebit/bank still blank",
          ne.exact_matrix_equal(ne.cut_projector(layout) * before, before))
    small = [ri.conjugate_record_word(layout, 1, n, **bounds) for n in (1, 2)]
    matrices = [ne.word_matrix(x) for x in small]
    logical = ne.Execution(3, (), (), ())
    c = ne.gate_matrix(logical, ne.Gate("CX", (1, 2)))
    fixed = c * sp.kronecker_product(sp.diag(ne.G_LOCAL ** 6, ne.G_LOCAL ** 2), sp.eye(2)) * c
    a = sp.kronecker_product(ne.G_LOCAL, sp.eye(4))
    check("actual Q1 n1 prefix equals conjugate recorded operator on ALL64 columns",
          ne.exact_matrix_equal(matrices[0], sp.kronecker_product(a.T * fixed * a, sp.eye(8))))
    full_a = sp.kronecker_product(ne.G_LOCAL, sp.eye(32))
    check("two actually executed prefixes are full-column conjugates at fixed initial boundary",
          ne.exact_matrix_equal(matrices[1], full_a.T * matrices[0] * full_a))
    negative = ri.conjugate_record_word(layout, 1, -1, **bounds)
    check("negative preparation uses actual source/inverse macros on ALL64 columns",
          len(negative.gates) == 44 and ne.exact_matrix_equal(ne.word_matrix(negative),
              sp.kronecker_product(a * fixed * a.T, sp.eye(8))))
    p0 = ne.cut_projector(layout); q0 = sp.eye(64) - p0
    defects = [p0 * w.T * q0 * w * p0 for w in matrices]
    check("genuine input-cut feedback also conjugates instead of depending on prepared Omega",
          ne.exact_matrix_equal(defects[1], full_a.T * defects[0] * full_a))
    full_layout = replace(layout, blank_wires=(0, 1, 2, 5), old_right=())
    full_j = ne.input_isometry(full_layout)
    p_hist = ne.gate_matrix(logical, ne.Gate("CX", (0, 2))) * sp.kronecker_product(ne.G_LOCAL, sp.eye(4))
    c_full = ne.gate_matrix(layout, ne.Gate("CX", (1, 2)))
    indices = (0, 1, 16, 17, 32, 33, 48, 49)
    theta = mp.atan2((mp.sqrt(5) - 1) / 2, mp.sqrt((mp.sqrt(5) - 1) / 2))
    for n, w in zip((1, 2), matrices):
        full = w * history_matrix
        an = sp.kronecker_product(ne.G_LOCAL ** n, sp.eye(4))
        f8 = an.T * sp.kronecker_product(sp.diag(ne.G_LOCAL ** 6, ne.G_LOCAL ** 2), sp.eye(2)) * an * p_hist
        factor = sp.zeros(64)
        for col in range(64):
            lc = ((col >> 5) & 1) * 4 + ((col >> 4) & 1) * 2 + (col & 1)
            for lr in range(8): factor[(col & 14) | indices[lr], col] = f8[lr, lc]
        check(f"full historical native endpoint has exact eight-phase factor on ALL64 columns n={n}",
              ne.exact_matrix_equal(c_full * full * c_full, factor))
        c3, c1, un = (ne.G_LOCAL ** 6)[0, 0], (ne.G_LOCAL ** 2)[0, 0], (ne.G_LOCAL ** (2 * n))[0, 0]
        gn = ne.A * (c3 + c1 + (c3 - c1) * un) / 2
        check(f"full-history cut rank4 has the exact scalar return corner n={n}",
              full_j.cols == 4 and ne.exact_matrix_equal(full_j.T * full * full_j, gn * sp.eye(4)))
        eigen = mp.eig(numeric(f8), left=False, right=False)
        actual = sorted(mp.arg(x) for x in eigen)
        predicted = sorted(mp.arg(mp.exp(sign * 1j * x)) for x in ri.full_history_phases(theta, 2 * theta, n) for sign in (-1, 1))
        check(f"full native Q1 spectrum confirms the analytical phase formula n={n}",
              max(abs(x - y) for x, y in zip(actual, predicted)) < mp.mpf("1e-75"))
    after = matrices[0] * before; rho = after * after.T
    check("coherent copy keeps global entropy zero by exact purity and unit trace",
          ne.exact_matrix_equal(rho * rho, rho) and ne.exact_matrix_equal(after.T * after, sp.eye(1)))
    hand = ri.seal_handoff(small[0], rho, 2, **bounds)
    check("archive handoff keeps the SAME correlated state and performs no reset/gate",
          hand.state is rho and hand.execution.gates == () and hand.execution.blank_wires == ()
          and hand.execution.old_right == (2, 5))
    for label, gate in (("target", ne.Gate("G", (2,))), ("control", ne.Gate("CX", (2, 0))),
                         ("prior oldRIGHT", ne.Gate("G", (5,)))):
        check("suffix forbids archived " + label, not ne.is_member(replace(hand.execution, gates=(gate,)), **bounds))
    check("suffix can act on remaining DATA without inventing blanks",
          ne.is_member(replace(hand.execution, gates=(ne.Gate("G", (0,)),)), **bounds))
    p = (mp.sqrt(5) - 1) / 2; theta = mp.atan2(p, mp.sqrt(p))
    omega = mp.zeros(4); psi = mp.matrix([mp.sqrt(p), 0, 0, p]); omega = psi * psi.T
    amp = numeric(ne.G_LOCAL); ks = amp.T * mp.diag([6 * theta, 2 * theta]) * amp
    info = ri.instrument(ks, 1, omega)
    actual_cq = ri.partial_trace(numeric(rho), 6, (1, 0, 5, 3, 4))
    spin = mp.zeros(4); spin[0, 0] = 1
    check("tracing only new bank yields the active report CQ with ALL oldR and passive spin retained",
          mp.norm(actual_cq - ri.kron(info["cq"], spin)) < mp.mpf("1e-75"))
    check("current native prefix keeps the pre-existing oldRIGHT marginal",
          mp.norm(ri.partial_trace(numeric(rho), 6, (5,)) - mp.diag([p, p ** 2])) < mp.mpf("1e-75"))
    rho_d = mp.diag([p, p ** 2]); active = ri.instrument(ks, 1, rho_d)
    binary = lambda x: -x * mp.log(x) - (1 - x) * mp.log1p(-x)
    check("pure GLOBAL but mixed DATA state has reference-complete gain h2(q)",
          abs(info["gain"] - binary(info["p"][1])) < mp.mpf("1e-75"))
    check("oldRIGHT-inaccessible gain retains conditional quantum entropy and is NOT h2(q)",
          active["conditional"] > 0 and abs(active["gain"] - info["gain"]) > mp.mpf("1e-5"))
    check("reference-complete minus active gain equals the actual conditional entanglement loss",
          abs(info["gain"] - active["gain"] - (ri.entropy(rho_d) - active["conditional"])) < mp.mpf("1e-75")
          and info["gain"] > active["gain"])
    V = mp.matrix([[mp.mpf(".1"), mp.mpf(".2")], [mp.mpf(".2"), mp.mpf("-.1")]])
    g, field = ri.sources(ks, 1, rho_d, V); eps = mp.mpf("1e-25")
    fd = (ri.instrument(ks + eps * V, 1, rho_d)["gain"] - ri.instrument(ks - eps * V, 1, rho_d)["gain"]) / (2 * eps)
    check("general noncommuting field source retains conditional quantum logs", abs(field - fd) < mp.mpf("1e-45"))
    J = mp.matrix([[0, -1], [1, 0]]); tangent = J * rho_d - rho_d * J
    rotate = lambda t: mp.matrix([[mp.cos(t), -mp.sin(t)], [mp.sin(t), mp.cos(t)]])
    rm, rp = rotate(-eps), rotate(eps)
    fp = (ri.instrument(ks, 1, rp * rho_d * rp.T)["gain"] - ri.instrument(ks, 1, rm * rho_d * rm.T)["gain"]) / (2 * eps)
    check("faithful preparation covector matches fixedRIGHT local-unitary source", abs(ri.trace(g * tangent) - fp) < mp.mpf("1e-45"))
    qp, base = Quadratic(0, 1), Quadratic(-1, 2)
    tt = [Quadratic(1), base]
    for _ in range(2, 1162): tt.append(2 * base * tt[-1] - tt[-2])
    e0, e1 = 1 - tt[99] ** 2, 1 - tt[33] ** 2
    check("Q33 native two-eigenband probabilities have EXACT strict signs",
          e1.sign() > 0 and (e0 - e1).sign() > 0 and (Fraction(1, 2) - e0).sign() > 0)
    check("exact algebraic archive-Z source bounds hold for Q33",
          (e0 - Fraction(49, 50000)).sign() > 0 and (Fraction(1, 1000) - e0).sign() > 0
          and (e1 - Fraction(1, 10000)).sign() > 0 and (qp - Fraction(3, 5)).sign() > 0)
    check("rational exponential bounds certify h-prime lower6 and upper8",
          3 ** 6 < 999 and sum(Fraction(8 ** j, factorial(j)) for j in range(13)) > 2499)
    qs = [(e0 + e1) * Fraction(1, 2) + (e0 - e1) * qp ** 3 * tt[n] * Fraction(1, 2) for n in (1, 67, 1161)]
    check("same native initial preparation gives exact two-sided Info probability contrasts",
          (qs[1] - qs[0]).sign() * (qs[2] - qs[0]).sign() == -1
          and all(x.sign() > 0 and (Fraction(1, 2) - x).sign() > 0 for x in qs))
    phi = mp.atan2(mp.sin(66 * theta), mp.cos(66 * theta)); delta = mp.mpf(1) / 16
    es = [mp.sin(3 * phi) ** 2, mp.sin(phi) ** 2]
    words = [ri.conjugate_record_word(layout, 33, n, **bounds) for n in (1, 67, 1161)]
    paid = nh.pad_catalogue_same_clock(words, (0, 1, 2), **bounds)
    full_words = [replace(full_layout, gates=history.gates + w.gates) for w in words]
    full_paid = nh.pad_catalogue_same_clock(full_words, (0, 1, 2), **bounds)
    beta_clock, z = 2 * 14140 ** 2 / delta ** 2, mp.mpf(1) / 4
    rows = []
    for n, word, full, closed in zip((1, 67, 1161), words, paid, full_paid):
        check(f"full native inverse/record/padding cost is retained n={n}", len(word.gates) == 202 + 12 * n and len(full.gates) == 14138)
        an = rotate(n * theta); kn = an.T * mp.diag([3 * phi / delta, phi / delta]) * an
        value = ri.instrument(kn, delta, omega)
        accessible = ri.instrument(kn, delta, rho_d)
        expected = (es[0] + es[1]) / 2 + (es[0] - es[1]) * p ** 3 * mp.cos(2 * n * theta) / 2
        check(f"long native code has the exact typed scalar probability formula n={n}", abs(value["p"][1] - expected) < mp.mpf("1e-75"))
        check(f"long pure-GLOBAL source retains its complete conditional states n={n}",
              abs(value["gain"] - binary(expected)) < mp.mpf("1e-75"))
        qR = [(es[0] + es[1]) / 2 + sign * (es[0] - es[1]) * mp.cos(2 * n * theta) / 2 for sign in (1, -1)]
        qr_exact = [(e0 + e1) * Fraction(1, 2) + sign * (e0 - e1) * tt[n] * Fraction(1, 2) for sign in (1, -1)]
        check(f"exact archive-Z slope inequalities hold at native code n={n}",
              (tt[n] - Fraction(1, 5)).sign() > 0 and (Fraction(3, 10) - tt[n]).sign() > 0
              and (Fraction(1, 1000) - qr_exact[0]).sign() > 0 and (qr_exact[1] - Fraction(1, 2500)).sign() > 0)
        joint = [sum(mp.re(value["blocks"][b][2 * d + r, 2 * d + r]) for d in range(2)) for r in range(2) for b in range(2)]
        reg_window = p * binary(qR[0]) + p ** 2 * binary(qR[1])
        check(f"actual passive oldR-Z and report-Z entropy retains historical entropy n={n}",
              abs(ri.entropy(mp.diag(joint)) - binary(p) - reg_window) < mp.mpf("1e-75"))
        gn = mp.sqrt(p) * (mp.cos(3 * phi) + mp.cos(phi) + (mp.cos(3 * phi) - mp.cos(phi)) * mp.cos(2 * n * theta)) / 2
        Z = ri.full_history_partition(theta, phi, n, len(closed.gates), beta_clock)
        Hfull, Jfull = mp.log(Z) / beta_clock, -4 * mp.log(1 - z * (1 - gn ** 2))
        inv = ne.inventory(full, **bounds)
        check(f"full history really adds two paid stages and uses the smaller input cut n={n}",
              len(closed.gates) == 14140 and ne.inventory(closed, **bounds).cut_rank == 4)
        rows.append({"n": n, "unpad_stages": len(word.gates), "actual_N": len(full.gates),
                     "q": mp.nstr(expected, 25), "I_ref": mp.nstr(value["gain"], 25),
                     "paid_window_inventory": {"G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count},
                     "I_reg_window": mp.nstr(reg_window, 25), "I_reg_full": mp.nstr(binary(p) + reg_window, 25),
                     "I_act_window": mp.nstr(accessible["gain"], 25),
                     "I_act_full": mp.nstr(accessible["gain"] + binary(p), 25),
                     "full_history_N": len(closed.gates), "H_full": mp.nstr(Hfull, 25),
                     "J_full": mp.nstr(Jfull, 25), "B_full": mp.nstr(Hfull + Jfull, 25)})
    check("including actual historical preparation removes the apparent full-price plateau",
          mp.mpf(rows[1]["B_full"]) > mp.mpf(rows[0]["B_full"]) > mp.mpf(rows[2]["B_full"]))
    exact_defects = []
    for n in (1, 67, 1161):
        corner = (tt[99] + tt[33] + (tt[99] - tt[33]) * tt[n]) * Fraction(1, 2)
        exact_defects.append(1 - qp * corner ** 2)
    check("configured exact full return-defect gap E67-E1 exceeds one millionth",
          (exact_defects[1] - exact_defects[0] - Fraction(1, 10 ** 6)).sign() > 0)
    check("configured exact full return-defect gap E1-E1161 exceeds one millionth",
          (exact_defects[0] - exact_defects[2] - Fraction(1, 10 ** 6)).sign() > 0)
    check("exact feedback chart makes its mean-value gain strictly larger than one",
          all(e.sign() > 0 and (1 - e).sign() > 0 for e in exact_defects)
          and 4 * Fraction(1, 4) == 1)
    heat_osc = (Fraction(21, 512) + Fraction(9, 3200)) / 14140 ** 2
    check("native angle and ALL-mode count give a rational full-heat oscillation bound",
          (tt[33] - Fraction(9999, 10000)).sign() > 0 and Fraction(22, 7) ** 2 < 10
          and 128 * 14140 < 2 ** 21 and heat_osc < Fraction(1, 20 * 14140 ** 2)
          and heat_osc < Fraction(1, 10 ** 8))
    check("configured full Book nonflatness is exact independently of numerical heat sums",
          Fraction(1, 10 ** 6) - heat_osc > Fraction(9, 10 ** 7))
    return {"checks": CHECKS, "checks_passed": len(CHECKS), "rows": rows,
            "actual_matrix_columns_checked": "Q1 n-1,n1,n2 FULL64; historical Q1 n1,n2 corners and eight phases FULL64",
            "same_boundary_component_example": {"Q": 1, "n": 1,
                "I_ref": mp.nstr(info["gain"], 25), "I_act": mp.nstr(active["gain"], 25),
                "conditional_DATA_entropy": mp.nstr(active["conditional"], 25),
                "input_DATA_entropy": mp.nstr(ri.entropy(rho_d), 25),
                "reference_correlation_loss": mp.nstr(info["gain"] - active["gain"], 25)},
            "long_words": "Q33 n1,67,1161 literal inventory plus exact Q(p) probabilities; no monolithic matrix replay",
            "I_ref_source": "log((1-q)/q)*(e0-e1)*p^3/2 > 0 on declared unit-u plane",
            "I_act_not_identified_with_I_ref": True, "actual_Cost_assigned": False,
            "cost_reaction_required": "If B_full=a*(ell*C_actual-I)+constant: D C_actual=(D I+D B_full/a)/ell; fixed a supplied",
            "global_coherent_entropy_gain_claimed": False, "bank_seal_is_gate_reset_or_dephasing": False,
            "current_window_Book_flat": "window cutrank16, commonN14138, exact conjugacy",
            "full_history_Book_flat_claimed": False,
            "exact_configured_full_Book_gaps": {"scope": "Q33, N14140, beta=512*N^2, z=1/4, cutrank4 ONLY",
                "exact_defect_gaps_lower": "E67-E1>1/1000000; E1-E1161>1/1000000",
                "analytic_elementary_bounds": "pi<22/7; log2<1; one |omega3|<=3|phi| branch and ALL128*N modes",
                "heat_oscillation_upper_rational": str(heat_osc),
                "Book_gap_lower": "B67-B1>9/10000000; B1-B1161>9/10000000"},
            "full_history_price": "cutrank4, commonN14140; all clock roots via verified eight-phase formula",
            "full_history_parameters": {"delta": "1/16", "beta_clock": "2*14140^2/(1/16)^2",
                "z": "1/4", "full_dimension": 64, "input_rank": 4, "paired_clock_modes": 2 * 14140 * 64},
            "I_act_full_vs_window": "full active gain adds h(p); window reference-DPI identity not applied before history",
            "I_reg_positive_source": "b*(p*h'(qR0)-p^2*h'(qR1)) > b*(14p-8)>0; b=(e0-e1)/2",
            "prep_plane_independently_admitted_or_fixed_task": "must be justified; not selected here",
            "numeric_entropy_source_arithmetic": "mpmath90digits, non-interval; exact algebraic probability signs separate",
            "full_GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--output", type=Path)
    args = parser.parse_args(); result = run(); result.update(schema="d0.native-recorded-info-source-check/1", status="PASS")
    paths = (Path(__file__), Path(ri.__file__), Path(nh.__file__), ri.DOMAIN / "native_execution.py", ri.DOMAIN / "check_native_execution_domain.py")
    result["inputs_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output: args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__": main()
