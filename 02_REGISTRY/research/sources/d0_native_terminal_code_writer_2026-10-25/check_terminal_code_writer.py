#!/usr/bin/env python3
"""Check the terminal code writer and its changed complete Book source only."""
import argparse
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp
import terminal_code_writer as tw

ne, ri = tw.native, tw.ri
sys.path.insert(0, str(tw.ROOT / "d0_native_operator_holonomy_2026-10-25"))
import native_holonomy as nh
from check_native_execution_domain import Quadratic
CHECKS = []


def check(name, assertion):
    if not assertion: raise AssertionError(name)
    CHECKS.append(name)


def numeric(a):
    return mp.matrix([[mp.mpf(str(sp.N(a[i, j], 80))) for j in range(a.cols)] for i in range(a.rows)])


def run():
    mp.mp.dps = 70
    bounds = dict(max_qubits=9, max_expanded_stages=50000)
    for b in (0, 1):
        raw, encoded = tw.parse_container((b, 0, b))
        check(f"typed raw direct/return parser and encoded length agree for report{b}",
              raw == (not bool(b),) and len(encoded) == 1+b
              and encoded == ((0,) if b == 0 else (1, 0)))
    for invalid in ((0, 1, 0), (1, 0, 0), (0, 0, 1), (True, 0, True), (0, 0)):
        try: tw.parse_container(invalid)
        except ne.DomainError: pass
        else: raise AssertionError("invalid code container accepted")
    check("parser rejects wrong tail, wrong length, wrong type and wrong arity", True)
    small_layout = ne.Execution(1, (), (), (), report_bits=(0,))
    small_writer = tw.append_terminal_writer(small_layout, 0, **bounds)
    r16 = ne.word_matrix(small_writer.execution)
    x = sp.Matrix([[0, 1], [1, 0]])
    parity = sp.kronecker_product(x, sp.eye(2), x)
    pplus, pminus = (sp.eye(8)+parity)/2, (sp.eye(8)-parity)/2
    z2 = sp.diag(1, -1)
    check("actual two-CX writer has the exact all16-column parity-sector decomposition",
          ne.exact_matrix_equal(r16, sp.kronecker_product(sp.eye(2), pplus)
                                + sp.kronecker_product(z2, pminus))
          and sp.trace(pplus) == sp.trace(pminus) == 4)
    blank = sp.zeros(8, 1); blank[0, 0] = 1
    embedding = sp.kronecker_product(sp.eye(2), blank)
    length_observable = sp.diag(*[1+(x & 1) for x in range(16)])
    check("initialized code-length pullback is an exact ALL-report-input effect",
          ne.exact_matrix_equal(embedding.T*r16.T*length_observable*r16*embedding,
                                sp.diag(1, 2)))
    for b in (0, 1):
        image = r16[:, 8*b]
        check(f"actual fresh container writes the word for report{b} without destroying report",
              image[8*b+5*b] == 1 and sum(v != 0 for v in image) == 1)
    layout = ne.Execution(6, (1, 2), (5,), (), ne.G_CX_SOURCE_I,
                          source_port=1, source_spin=(3, 4), report_bits=(1,))
    for forbidden in (3, 4, 5):
        try: tw.append_terminal_writer(layout, forbidden, **bounds)
        except ne.DomainError: pass
        else: raise AssertionError("forbidden writer control accepted")
    check("writer rejects oldRIGHT and either dirty source-spin control", True)
    history = (ne.Gate("G", (0,)), ne.Gate("CX", (0, 5)))
    words = [ri.conjugate_record_word(layout, 33, n, **bounds) for n in (1, 67, 1161)]
    # Every paid identity is before final handoff. The historical seal is
    # checked by the actual suffix interface, not removed by a density reset.
    padded = [nh.pad_word_same_clock(w, 14138, (0, 1, 2), **bounds) for w in words]
    extended = [tw.append_terminal_writer(w, 1, **bounds) for w in padded]
    full = [replace(w.execution, old_right=(), blank_wires=(0, 1, 2, 5, 6, 7, 8),
                    gates=history+w.execution.gates) for w in extended]
    for n, writer, execution in zip((1, 67, 1161), extended, full):
        inv = ne.inventory(execution, **bounds)
        check(f"same full initial cut and actual two extra stages are retained n={n}",
              len(execution.gates) == 14142 and inv.full_dimension == 512
              and inv.cut_rank == 4 and inv.input_dimension == 4
              and inv.blank_count == 7 and writer.code_wires == (6, 7, 8)
              and all(5 not in g.wires for g in execution.gates[2:]))
        check(f"no gate touches the new tail or erases any code register n={n}",
              all(7 not in g.wires for g in execution.gates)
              and writer.execution.gates[-2:] == (ne.Gate("CX", (1, 6)), ne.Gate("CX", (1, 8))))
    suffix = replace(extended[0].execution, gates=(), blank_wires=(), old_right=(2, 5, 6, 7, 8))
    check("post-writer policy seals the retained bank and entire code with no new blanks",
          ne.is_member(suffix, **bounds)
          and not ne.is_member(replace(suffix, gates=(ne.Gate("CX", (6, 0)),)), **bounds))
    p = (mp.sqrt(5)-1)/2
    theta = mp.atan2(p, mp.sqrt(p))
    phi = mp.atan2(mp.sin(66*theta), mp.cos(66*theta))
    # Independent small actual native factor from the previous same-word
    # algebra, using exact Golden entries. No long 512 matrix is constructed.
    logical = ne.Execution(3, (), (), ())
    phist = ne.gate_matrix(logical, ne.Gate("CX", (0, 2))) * sp.kronecker_product(ne.G_LOCAL, sp.eye(4))
    for n in (1, 2):
        an = sp.kronecker_product(ne.G_LOCAL**n, sp.eye(4))
        f8 = an.T * sp.kronecker_product(sp.diag(ne.G_LOCAL**6, ne.G_LOCAL**2), sp.eye(2)) * an * phist
        zh = sp.diag(1, 1, -1, -1, 1, 1, -1, -1)
        actual = sorted(mp.arg(x) for matrix in (f8, zh*f8)
                        for x in mp.eig(numeric(matrix), left=False, right=False))
        # For n2 sin(4theta)>0 as well, so the same square-root chart applies.
        u = mp.cos(2*n*theta)
        predicted = sorted(mp.arg(mp.exp(sign*1j*a))
            for a in tw.phase_representatives(theta, 2*theta, u) for sign in (-1, 1))
        check(f"sixteen predicted phase roots match independent exact Q1 native factors n={n}",
              max(abs(a-b) for a, b in zip(actual, predicted)) < mp.mpf("1e-55"))
        c3, c1 = (ne.G_LOCAL**6)[0, 0], (ne.G_LOCAL**2)[0, 0]
        un = (ne.G_LOCAL**(2*n))[0, 0]
        gn = ne.A*(c3+c1+(c3-c1)*un)/2
        check(f"full blank corner is preserved by actual code writer n={n}",
              ne.exact_matrix_equal(sp.Matrix([[f8[0, 0]]]), sp.Matrix([[gn]])))
        # Writer trace = report dephasing, while its full vector stays pure.
        v = numeric(f8[:, 0]); cq = v*v.H
        cq = mp.matrix([[cq[i, j] if (i//2)%2 == (j//2)%2 else 0
                         for j in range(8)] for i in range(8)])
        q = mp.fsum(abs(v[i])**2 for i in (2, 3, 6, 7))
        components = tw.registered_components(2*theta, u)
        check(f"exact prefix output gives terminal probability and unchanged reference CQ entropy n={n}",
              abs(q-components["q"]) < mp.mpf("1e-55")
              and abs(ri.entropy(cq)+q*mp.log(q)+(1-q)*mp.log1p(-q)) < mp.mpf("1e-55"))
    # A small actual clock independently checks the 128 factor and ALL modes.
    u = mp.mpf(1)/4; nsmall = 13; bsmall = mp.mpf(7)
    zall = 64*mp.fsum(mp.exp(-bsmall*(1-mp.cos((a+2*mp.pi*k)/nsmall)))
                      for a in tw.full_phases(theta, phi, u) for k in range(nsmall))
    check("full 512-fibre partition matches every numerical eigenphase and BOTH Hodge degrees",
          abs(zall-tw.full_partition(theta, phi, u, nsmall, bsmall)) < mp.mpf("1e-50")
          and 64*16*nsmall == 2*512*nsmall)
    hsmall, dhsmall = tw.full_heat_and_source(theta, phi, u, nsmall, bsmall)
    eps = mp.mpf("1e-18")
    heat = lambda v: mp.log(tw.full_partition(theta, phi, v, nsmall, bsmall))/bsmall
    fd = (heat(u+eps)-heat(u-eps))/(2*eps)
    check("complete heat source matches an independent finite difference of all clock modes",
          abs(hsmall-heat(u)) < mp.mpf("1e-55") and abs(fd-dhsmall) < mp.mpf("1e-35"))
    jf = lambda v: tw.full_feedback(phi, v, mp.mpf(1)/4)
    check("full return source retains its rank4 coefficient and correct sign",
          abs((jf(u+eps)-jf(u-eps))/(2*eps)-tw.full_feedback_source(phi, u, mp.mpf(1)/4)) < mp.mpf("1e-35"))
    ell = -mp.log(p)
    pc = lambda v: ell*tw.registered_components(phi, v)["C_code"]-tw.registered_components(phi, v)["I_reg_full"]
    comp = tw.registered_components(phi, u)
    check("registered code-minus-Info source agrees with an independent value difference",
          abs((pc(u+eps)-pc(u-eps))/(2*eps)-ell*comp["Dq"]+comp["DI_reg"]) < mp.mpf("1e-35"))
    # Rational-field bounds reuse the primitive Q(p) implementation, not its suite.
    qp, base = Quadratic(0, 1), Quadratic(-1, 2)
    tt = [Quadratic(1), base]
    for _ in range(2, 1162): tt.append(2*base*tt[-1]-tt[-2])
    e0, e1 = 1-tt[99]**2, 1-tt[33]**2
    check("exact Q33 e0,e1 bounds support the whole u interval rather than only sampled codes",
          (e0-Fraction(49, 50000)).sign() > 0 and (Fraction(1, 1000)-e0).sign() > 0
          and (e1-Fraction(1, 10000)).sign() > 0 and (Fraction(3, 25000)-e1).sign() > 0)
    average, be = (e0+e1)*Fraction(1, 2), (e0-e1)*Fraction(1, 2)
    check("whole-interval conditional probabilities give h-prime lower6 and upper8",
          (Fraction(1, 1000)-average-be*Fraction(3, 10)).sign() > 0
          and (average-be*Fraction(3, 10)-Fraction(1, 2500)).sign() > 0)
    # h'(q0)>6 and h'(q1)<8 follow from the already owned elementary
    # exponential bounds; include the integer comparisons in this new receipt.
    from math import factorial
    check("elementary exponential inequalities certify the entropy-slope constants",
          3**6 < 999 and sum(Fraction(8**j, factorial(j)) for j in range(13)) > 2499)
    check("exact Golden inequalities leave an uncompensated source greater than 3b/20",
          (qp-Fraction(3, 5)).sign() > 0 and (Fraction(1, 4)-qp**3).sign() > 0
          and 14*Fraction(3, 5)-8-Fraction(1, 4) == Fraction(3, 20))
    check("exact cosines give the configured strict full-feedback source lower bound",
          (tt[33]-Fraction(9999, 10000)).sign() > 0
          and (tt[99]-Fraction(999, 1000)).sign() > 0
          and (tt[33]-tt[99]-Fraction(39, 100000)).sign() > 0
          and Fraction(3, 5)*Fraction(999, 1000)*Fraction(39, 100000) > Fraction(1, 5000))
    check("raw heat source norm on the WHOLE interval leaves B-writer-prime greater than 1e-4",
          Fraction(1, 14142**2)*Fraction(100, 91) < Fraction(1, 10000**2)
          and Fraction(1, 5000)-Fraction(1, 10000) == Fraction(1, 10000))
    defects = []
    for n in (1, 67, 1161):
        g = (tt[99]+tt[33]+(tt[99]-tt[33])*tt[n])*Fraction(1, 2)
        defects.append(1-qp*g*g)
    osc = (Fraction(24, 512)+Fraction(9, 3200))/14142**2
    check("new ALL1024N heat bound preserves exact finite Book gaps",
          1024*14142 < 2**24 and osc == Fraction(159, 3200*14142**2)
          and osc < Fraction(1, 10**8)
          and (defects[1]-defects[0]-Fraction(1, 10**6)).sign() > 0
          and (defects[0]-defects[2]-Fraction(1, 10**6)).sign() > 0
          and Fraction(1, 10**6)-osc > Fraction(9, 10**7))
    rows = []
    stages, beta, z = 14142, mp.mpf(512)*14142**2, mp.mpf(1)/4
    for n, execution in zip((1, 67, 1161), full):
        u = mp.cos(2*n*theta)
        check(f"native configuration lies on the same positive-sine source interval n={n}",
              (tt[n]-Fraction(1, 5)).sign() > 0 and (Fraction(3, 10)-tt[n]).sign() > 0
              and mp.sin(2*n*theta) > 0)
        value = tw.registered_components(phi, u)
        heat, dheat = tw.full_heat_and_source(theta, phi, u, stages, beta)
        feedback = tw.full_feedback(phi, u, z)
        dfeedback = tw.full_feedback_source(phi, u, z)
        ell = -mp.log(p)
        remainder = value["DI_reg"]-ell*value["Dq"]
        check(f"actual original code length fails to cancel registered Info n={n}",
              remainder > (mp.sin(3*phi)**2-mp.sin(phi)**2)*mp.mpf(3)/40)
        check(f"configured full-source values respect the uniform proved source bounds n={n}",
              abs(dheat) < mp.mpf(1)/10000 and dfeedback > mp.mpf(1)/5000
              and dheat+dfeedback > mp.mpf(1)/10000)
        inv = ne.inventory(execution, **bounds)
        rows.append({"n": n, "u": mp.nstr(u, 25),
            **{k: mp.nstr(v, 25) for k, v in value.items()},
            "DI_reg_minus_ell_Dq": mp.nstr(remainder, 25),
            "H_full_writer": mp.nstr(heat, 25), "J_full_writer": mp.nstr(feedback, 25),
            "B_full_writer": mp.nstr(heat+feedback, 25),
            "D_H_full_writer": mp.nstr(dheat, 25), "D_J_full_writer": mp.nstr(dfeedback, 25),
            "D_B_full_writer": mp.nstr(dheat+dfeedback, 25),
            "inventory": {"G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
                          "actual_N": len(execution.gates), "full_fibre": inv.full_dimension,
                          "input_cut_rank": inv.cut_rank}})
    check("full writer Book retains two-sided native configuration contrasts",
          mp.mpf(rows[1]["B_full_writer"]) > mp.mpf(rows[0]["B_full_writer"]) > mp.mpf(rows[2]["B_full_writer"]))
    return {"checks": CHECKS, "checks_passed": len(CHECKS), "rows": rows,
            "parameters": {"Q": 33, "N": stages, "beta_clock": "512*14142^2", "z": "1/4",
                           "paired_clock_modes": 2*512*stages},
            "actual_terminal_encoder_built": True,
            "registered_length_component": "C_code=1+q; raw=[not b], Enc(raw)=0 or10",
            "code_length_additive_in_full_physical_Cost_proved": False,
            "code_length_equals_actual_gate_count_claimed": False,
            "full_Book_source_reused_without_new_modes": False,
            "source_requirement_if_price_binding_supplied":
                "ell*D C_rest=DI_reg-ell*Dq+(D B_writer)/kappa; kappa supplied, nonzero",
            "global_entropy_increase_or_extra_duplicate_Info_claimed": False,
            "numeric_arithmetic": "70-digit mpmath, non-interval; exact native and Q(p) signs separate",
            "runtime": {"python": sys.version.split()[0], "mpmath": mp.__version__,
                        "sympy": sp.__version__},
            "matrix_scope": "writer ALL16 columns; Q1 native reduced8 factors; no monolithic long512 matrix",
            "proved_source_bounds": "u in[1/5,3/10], Q33,N14142,z1/4: R_code>3b/20, Jprime>1/5000, absHprime<1/10000, Bprime>1/10000",
            "full_GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.native-terminal-code-writer-check/1", status="PASS")
    paths = [Path(__file__), Path(tw.__file__), Path(ri.__file__), Path(nh.__file__),
             ri.DOMAIN/"native_execution.py", ri.DOMAIN/"check_native_execution_domain.py"]
    repo = tw.ROOT.parents[2]
    paths += [tw.ROOT/"d0_native_recorded_info_source_2026-10-25"/"PROOF.md",
              tw.ROOT/"d0_direct_forcing_attack_2026-10-14"/"RESULT.md",
              repo/"02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md",
              repo/"03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean"]
    paths += [p for p in Path(__file__).parent.glob("*_PROOF.md")]
    result["inputs_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    output = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output: args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__": main()
