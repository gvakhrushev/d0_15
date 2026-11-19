#!/usr/bin/env python3
"""New bounded all-column completion and complete-record source controls.

One six-qubit native body per alternative is evaluated. The actual nine-qubit
record code is validated/counted; its 512-column matrix/clock is NOT simulated.
No old READY, root, 128-carrier or Lean suite is replayed.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

import helper as hp

PACKET = Path(__file__).resolve().parent
SOURCES = PACKET.parent
REPO = SOURCES.parents[2]
PRIMARY = REPO / "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
CHECKS = []


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def eq(a, b):
    if not isinstance(a, sp.MatrixBase):
        a, b = sp.Matrix([[a]]), sp.Matrix([[b]])
    return hp.native.exact_matrix_equal(a, b)


def sign5(value):
    """Exact sign in the selected Q(sqrt5) embedding, using rational squares."""
    cs = sp.to_number_field(value, sp.sqrt(5)).coeffs()
    b, a = (sp.Rational(0), cs[0]) if len(cs) == 1 else cs
    if b == 0:
        return int(sp.sign(a))
    if a == 0 or a*b > 0:
        return int(sp.sign(b))
    difference = a*a-5*b*b
    return int(sp.sign(difference) if a > 0 else -sp.sign(difference))


def number(x):
    return mp.mpf(str(sp.N(x, 110)))


def entropy(ps):
    return -mp.fsum(number(p)*mp.log(number(p)) for p in ps if not eq(p, 0))


def h(x):
    return -x*mp.log(x)-(1-x)*mp.log(1-x)


def winding(N, phase, beta):
    return mp.fsum(mp.exp(-beta*(1-mp.cos((2*mp.pi*k+phase)/N))) for k in range(N))


def run():
    CHECKS.clear()
    mp.mp.dps = 100
    ne, p = hp.native, hp.native.P
    I4, I8 = sp.eye(4), sp.eye(8)
    r = 5
    bare = hp.layout()
    prepared = replace(bare, blank_wires=(hp.CONTROL, hp.JUNK),
                       gates=(ne.Gate("G", (hp.CONTROL,)),)*r)
    Aj = ne.word_matrix(prepared, **hp.BOUNDS)
    j_aux = ne.input_isometry(prepared, **hp.BOUNDS)
    init = ne.input_isometry(bare, **hp.BOUNDS)
    source_private = sp.kronecker_product(hp.rotation(r), sp.eye(4))
    middle_private = sp.diag(sp.eye(4), sp.kronecker_product(hp.rotation(2), sp.eye(2)))
    core = source_private.T*middle_private*source_private
    copy_code = hp.private_copy()
    D = ne.word_matrix(copy_code, **hp.BOUNDS)
    check("the reduced copy is the actual three-CX addressed permutation on ALL64 private/record columns",
          D*D == sp.eye(64)
          and all(D[8*w+(a^w), 8*w+a] == 1 for w in range(8) for a in range(8)))
    rows, matrices, reduced, laws, costs = [], {}, {}, {}, {}
    q, d, b, s, mu = (hp.data(1, r)[key] for key in ("q", "d", "b", "s", "mu"))
    check("the real base probability law is complete before any entropy comparison",
          eq(sum(hp.base_probabilities(r)), 1)
          and sign5(q) > 0 and sign5(1-q) > 0 and sign5(mu) > 0)

    for L in (1, 2):
        code, actual_record = hp.execution(L, r), hp.execution(L, r, recorded=True)
        inv = ne.inventory(code, **hp.BOUNDS)
        rinv, rot = hp.controlled_junk(L, inverse=True), hp.controlled_junk(L)
        check("optimized symbolic R and Rinv have paid twelve-L-plus-two stages L%d" % L,
              len(rinv) == len(rot) == 12*L+2
              and all(type(g) is ne.Gate and g.op in ("G", "CX", "SourceI") for g in rinv+rot))
        actual = ne.word_matrix(code, **hp.BOUNDS)
        expected = hp.expected_private(L, r)
        private = actual.extract(tuple(4*i for i in range(8)), tuple(4*i for i in range(8)))
        check("the actual native completion agrees with R U Rdagger on ALL64 columns L%d" % L,
              eq(actual, sp.kronecker_product(sp.eye(2), expected, I4)))
        check("the completed body is exactly I_helper and I_spin on arbitrary input columns L%d" % L,
              eq(actual, sp.kronecker_product(sp.eye(2), private, I4))
              and eq(actual.T*actual, sp.eye(64)))
        forward = hp.forward_execution(L, r)
        forward_matrix = ne.word_matrix(forward, **hp.BOUNDS)
        check("actual A_L j_aux equals A j_aux with port/helper/spin arbitrary L%d" % L,
              eq(forward_matrix*j_aux, Aj*j_aux)
              and ne.inventory(forward, **hp.BOUNDS).cut_rank == 16)
        check("whole known-input return C and F are the original scalar law L%d" % L,
              eq(init.T*actual*init, s*I4)
              and eq((init.T*actual*init).T*(init.T*actual*init), s*s*I4))
        check("native alternatives have the SAME complete primitive inventory L%d" % L,
              (inv.g_count, inv.source_i_count, inv.cx_count, inv.gate_count) == (20, 40, 66, 126)
              and inv.full_dimension == 64 and inv.cut_rank == 4)
        record_inv = ne.inventory(actual_record, **hp.BOUNDS)
        check("the literal recorded code pays both copy legs and retains all nine-qubit columns L%d" % L,
              (record_inv.g_count, record_inv.source_i_count, record_inv.cx_count,
               record_inv.gate_count, record_inv.full_dimension, record_inv.cut_rank)
                  == (20, 40, 72, 132, 512, 4)
              and record_inv.gate_count*record_inv.full_dimension*2 == 135168
              and actual_record.report_bits == (6, 7, 8))
        probabilities = hp.probabilities(L, r)
        check("all eight actual final ACTIVE labels have the stated scalar protected effects L%d" % L,
              all(eq(actual.extract(tuple(4*i+k for k in range(4)), tuple(range(4))),
                     private[i, 0]*I4)
                  and eq(private[i, 0]**2, probabilities[i]) for i in range(8))
              and eq(sum(probabilities), 1))
        check("every OLD joint control-port marginal stays unchanged L%d" % L,
              all(eq(probabilities[2*i]+probabilities[2*i+1], hp.base_probabilities(r)[i])
                  for i in range(4)))
        recorded = hp.reduced_recorded(private)
        check("reduced ALL64 copy transport is exact and retains the same blank corner L%d" % L,
              eq(recorded, D*sp.kronecker_product(private, sp.eye(8))*D)
              and eq(recorded[0, 0], s))
        check("the actual complete registered label law equals the full private outcome law L%d" % L,
              all(eq(sum(recorded[8*w+label, 0]**2 for w in range(8)), probabilities[label])
                  for label in range(8)))
        # Conjugacy checks the ENTIRE private matrix, not only a prepared column.
        R = sp.diag(sp.eye(4), sp.kronecker_product(sp.eye(2), hp.rotation(2*L)))
        check("all-column conjugacy preserves the full spectrum and every retained heat mode L%d" % L,
              eq(R.T*private*R, core)
              and eq(actual.trace(), 32+32*p**3))
        charges = tuple(range(8))
        t = sp.symbols("mark", real=True)
        marked = hp.marked_scalar(probabilities, charges, t)
        first_charge = sum(c*pi for c, pi in zip(charges, probabilities))
        # Pull back the charge on the ACTUAL full native output carrier.
        # This is an unknown-spin operator check, not only an exp-sum identity.
        C_out = sp.diag(*(charges[(i//4) % 8] for i in range(64)))
        output_isometry = actual*init
        actual_effect = output_isometry.T*C_out*output_isometry
        check("actual full-carrier label charges pull back to their scalar unknown-input cost effect L%d" % L,
              eq(actual_effect, first_charge*I4)
              and eq(-sp.diff(marked, t).subs(t, 0)*I4, actual_effect)
              and eq(sum(probabilities[i]*(charges[i]+1) for i in range(8)), first_charge+1))
        rows.append(dict(L=L, source_power=r, full_body_columns=64, body_stages=126,
                         G=inv.g_count, SourceI=inv.source_i_count, CX=inv.cx_count,
                         recorded_qubits=9, recorded_dimension=512, cut_rank=4,
                         recorded_stages=132, paired_modes=135168,
                         algorithmic_initialized_aux_rank=16,
                         source_forward_stages=len(forward.gates),
                         fine_probabilities=[str(sp.simplify(x)) for x in probabilities],
                         scalar_charge_model=str(sp.simplify(first_charge)),
                         charge_scope="supplied label evaluation model, not physical gate Cost selection"))
        matrices[L], reduced[L], laws[L], costs[L] = actual, private, probabilities, first_charge

    v1, v2 = hp.data(1, r)["v"], hp.data(2, r)["v"]
    check("entropy ordering has an EXACT algebraic certificate, not a floating sign",
          eq(v1, 4*p**3) and eq(1-v1, p**6) and eq(v2, 16*p**9)
          and sign5(v2-p**6) > 0 and sign5(sp.Rational(1, 2)-v2) > 0
          and sign5(p**6) > 0)
    old_info = entropy(hp.base_probabilities(r))
    info = {L: entropy(laws[L]) for L in (1, 2)}
    identity_errors = {L: info[L]-old_info-number(mu)*h(number(hp.data(L,r)["v"]))
                       for L in (1,2)}
    check("independent complete probability entropy agrees with the exact CQ decomposition",
          all(abs(error) < mp.mpf("1e-85") for error in identity_errors.values()))
    check("the strict finite information gap agrees with its proved conditional entropy formula",
          info[2] > info[1]
          and abs((info[2]-info[1])-number(mu)*(h(number(v2))-h(number(v1)))) < mp.mpf("1e-85"))
    tau = s*s
    fine = laws[1]
    conditional = [pi/(1-tau) for i, pi in enumerate(fine) if i != 0]
    check("coarse blank-return entropy omits the actual nonreturn-label entropy",
          abs(info[1]-h(number(tau))-(1-number(tau))*entropy(conditional)) < mp.mpf("1e-85"))
    # Analytic all-field source identity: A may be any real rotation.
    x = sp.symbols("source_q", real=True)
    qlaw = ((1-d*x)**2, b*b*x*x, d*d*x*(1-x), b*b*x*(1-x))
    check("the literal base law depends only on source q and preserves its total first source",
          all(eq(coefficient, 0) for coefficient in
              sp.Poly(sp.expand(sum(qlaw)-1), x).all_coeffs())
          and all(eq(coefficient, 0) for coefficient in
              sp.Poly(sp.expand(sum(sp.diff(pi, x) for pi in qlaw)), x).all_coeffs()))
    beta, N = mp.mpf(1), 132
    theta = mp.atan2(number(p), mp.sqrt(number(p)))
    partition = 512*(winding(N, 0, beta)+winding(N, 2*theta, beta))
    return dict(status="PASS", checks=len(CHECKS), check_names=list(CHECKS),
        native_rows=rows, q=str(sp.simplify(q)), source_column_scope="ALL initialized c0,junk0 inputs, port/helper/spin arbitrary",
        phase_multiplicities_body={"0":32,"+2theta":16,"-2theta":16},
        phase_multiplicities_recorded={"0":256,"+2theta":128,"-2theta":128},
        paired_heat_noninterval_decimal=mp.nstr(mp.log(partition)/beta, 90),
        registered_info_noninterval_decimals={str(L):mp.nstr(info[L],90) for L in (1,2)},
        registered_info_gap_noninterval_decimal=mp.nstr(info[2]-info[1],90),
        strict_gap_proof="mu>0 and 0<p6<v2<1/2, h(v1)=h(p6); binary entropy increases on (0,1/2)",
        scope=["new ALL64 native-body comparison and actual same-inventory 132-stage recording code",
               "actual9-qubit record code validated/counted; reduced64 copy checked; no512 matrix/clock simulation",
               "all old registered diagonal marginals, source isometry, full corner and spectrum fixed",
               "fine registered Info changes; no full future-profile equivalence claimed",
               "full record entropy is a supplied CQ component, not a new compulsory Book Info axiom",
               "scalar charge model is not a physical Cost tariff or additive ledger binding",
               "no continuous native angle/controller admission, old READY/root/Lean replay or GR promotion"])


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path.relative_to(REPO)), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def section_pin(heading):
    raw = PRIMARY.read_bytes()
    start = raw.index(heading.encode())
    end = raw.find(b"\n## ", start+1)
    raw = raw[start:end if end >= 0 else None]
    return dict(heading=heading, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    paths = [PACKET/n for n in ("helper.py","check_complete_record.py","CQ_SOURCE.md","COMPLETION_MAP.md")]
    paths += [SOURCES/"d0_native_execution_domain_2026-10-24"/n for n in ("native_execution.py","book_price.py")]
    paths += [SOURCES/"d0_known_port_native_cofield_2026-10-25"/n
              for n in ("known_port.py","NATIVE_IMPLEMENTATION.md","SOURCE_TRANSFER.md","CHECK_RESULT.json")]
    paths += [SOURCES/"d0_native_recorded_info_source_2026-10-25"/"PROOF.md"]
    paths += [SOURCES/"d0_exact_report_reflected_cohorts_2026-10-25"/n
              for n in ("reflected_report.py", "PROOF.md", "COHORT_THEOREM.md")]
    paths += [SOURCES/"d0_known_port_task_source_2026-10-25"/n
              for n in ("TASK_MAP.md","HEAT_TRANSFER.md","CHECK_RESULT.json")]
    paths += [SOURCES/"d0_native_stopped_quantum_balance_2026-10-22"/"RAW_PARTITION_APPLICATION.md"]
    paths += [SOURCES.parent/n for n in
              ("A4D_LITERAL_GOLDEN_CNOT_ACTIVE_LIE_COMPLETENESS_AND_C2_SOURCE_2026_10_19.md",
               "A4D_ORIGINAL_GOLDEN_READY_COMPLETE_CQ_COST_INFO_PF_SOURCE_2026_10_21.md",
               "A4D_NATIVE_STOPPED_QUANTUM_PRICE_AND_SOURCE_2026_10_22.md")]
    result["source_pins"] = [pin(p) for p in paths]
    result["section_pins"] = [section_pin("## "+s+".") for s in ("7j","7x","7y","7ai","7aj","7ak")]
    result["generated_utc"] = datetime.now(timezone.utc).isoformat()
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
