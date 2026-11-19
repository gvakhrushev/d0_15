#!/usr/bin/env python3
"""Changed known-port native matrices, true cut/heat and scalar source checks.

No old READY/Cartan/large-native suite is replayed.  Rational kernel
models are diagnostics, not additional primitive physical gates.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp
from sympy.polys.matrices import DomainMatrix

import known_port as kp

CHECKS = []
PACKET = Path(__file__).resolve().parent
SOURCES = PACKET.parent
REPO = SOURCES.parents[2]
PRIMARY = REPO / "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def num(value):
    if isinstance(value, (int, F)):
        value = F(value)
        return mp.mpf(value.numerator)/value.denominator
    return mp.mpf(str(sp.N(value, 110)))


def character(stages, phase, beta):
    return mp.fsum(mp.exp(-beta*(1-mp.cos((2*mp.pi*k+phase)/stages)))
                   for k in range(stages))


def paired_heat(stages, K, phase, beta):
    counts = kp.heat_counts(K)
    trace = 2*mp.fsum(count*character(stages, omega, beta)
                     for count, omega in zip(counts, (0, phase, -phase)))
    return mp.log(trace)/beta


def aa_api_control():
    """New narrow support/API regression only: emits stages, no AA matrix replay."""
    plan, book = kp.aa_support_fixture()
    inv = kp.native.inventory(plan.execution, max_qubits=8, max_expanded_stages=200000)
    book_inv = kp.native.inventory(book, max_qubits=8, max_expanded_stages=200000)
    check("owned AA API actually keeps the reused target port out of its input predicate and raw gate support",
          plan.initial_controls == (1, 2) and plan.ready_controls == (1,)
          and plan.report_bit == 2 and plan.rebit == 3
          and 4 not in plan.initial_controls
          and all(4 not in gate.wires for gate in plan.execution.gates))
    check("actual AA word retains a free-bank input leg while the separate physical Book cut fixes its known source and port",
          7 not in plan.initial_controls
          and book.blank_wires == (0, 1, 2, 3, 4, 7)
          and inv.gate_count == 4404 and book_inv.gate_count == 4404
          and inv.full_dimension == 256 and inv.cut_rank == 32 and book_inv.cut_rank == 4
          and (1 << (plan.execution.qubits-len(plan.initial_controls))) == 64)
    return dict(qubits=plan.execution.qubits, initial_controls=list(plan.initial_controls),
                ready_controls=list(plan.ready_controls), report_bit=plan.report_bit,
                amplifier_rebit=plan.rebit, actual_expanded_stages=inv.gate_count,
                G=inv.g_count, CX=inv.cx_count, SourceI=inv.source_i_count,
                full_dimension=inv.full_dimension, base_declared_input_rank=inv.cut_rank,
                algorithmic_Pref_rank=64, physical_Book_rank=book_inv.cut_rank,
                known_port=4, bank=7, actual_book_blanks=list(book.blank_wires),
                scope="owned API inventory/support only; bank7 spectator in this fixture, real reports may read banks; no long AA matrix or gamma theorem replay")


def run():
    CHECKS.clear()
    mp.mp.dps = 110
    ne, p = kp.native, kp.native.P
    beta, zeta = mp.mpf(".7"), sp.Rational(1, 2**20)
    middle_rows, middle_matrices = [], {}
    for K, repeat in ((1, 1), (2, 9)):
        execution, controls, port, theta_power = kp.middle_execution(K, repeat)
        actual = ne.word_matrix(execution, **kp.rr.bounds(execution))
        expected = kp.expected_middle(execution, controls, port, theta_power)
        inv = ne.inventory(execution, **kp.rr.bounds(execution))
        m = theta_power//2
        check("literal W_K has its exact ALL-column identity/controlled-G definition K%d L%d" % (K, repeat),
              ne.exact_matrix_equal(actual, expected)
              and ne.exact_matrix_equal(actual.T*actual, sp.eye(actual.rows)))
        private_indices = tuple(4*i for i in range(1 << (K+1)))
        private = actual.extract(private_indices, private_indices)
        check("completed W_K restores the dedicated helper and arbitrary Q8 spin on ALL columns K%d L%d" % (K, repeat),
              ne.exact_matrix_equal(actual, sp.kronecker_product(sp.eye(2), private, sp.eye(4))))
        check("known-port middle counts every true inverse and has rank4 rather than an unknown meter rank8 K%d L%d" % (K, repeat),
              (inv.g_count, inv.source_i_count, inv.cx_count) ==
                  (2*m, 4*m, 6*m+(1 << (K+1))-2)
              and inv.gate_count == 12*m+(1 << (K+1))-2
              and inv.full_dimension == (1 << (K+4)) and inv.cut_rank == 4)
        alpha = kp.rr.alpha_interval(K, repeat, bits=110)["alpha"]
        check("the actual compact native choice has d=alpha_old/2 strictly between one half and one K%d L%d" % (K, repeat),
              F(1, 2) < alpha[0]/2 < alpha[1]/2 < 1)
        rotation = DomainMatrix.from_Matrix(ne.G_LOCAL).convert_to(ne.GOLDEN_FIELD).pow(theta_power).to_Matrix()
        n0, plus, minus = kp.heat_counts(K)
        check("the full real spectral multiplicities include every unready work/helper/spin column K%d L%d" % (K, repeat),
              n0+plus+minus == inv.full_dimension
              and ne.exact_matrix_equal(sp.Matrix([[actual.trace()-(n0+(plus+minus)*rotation[0, 0])]]), sp.zeros(1)))
        middle_rows.append({"K": K, "L": repeat, "theta_power": theta_power,
            "stages": inv.gate_count, "G": inv.g_count, "CX": inv.cx_count,
            "SourceI": inv.source_i_count, "full_columns": inv.full_dimension,
            "known_input_rank": inv.cut_rank, "one_degree_phase_multiplicities": [n0, plus, minus],
            "paired_clock_modes": 2*inv.gate_count*inv.full_dimension})
        middle_matrices[K, repeat] = actual

    native_rows, private_matrices, amplitudes = [], {}, {}
    theta = mp.atan2(num(p), mp.sqrt(num(p)))
    for power in (4, 5, 10):
        execution, control, port, theta_power = kp.source_echo(power)
        actual = ne.word_matrix(execution, **kp.rr.bounds(execution))
        injection = ne.input_isometry(execution, **kp.rr.bounds(execution))
        corner = injection.T*actual*injection
        source = DomainMatrix.from_Matrix(ne.G_LOCAL).convert_to(ne.GOLDEN_FIELD).pow(power).to_Matrix()
        q, d = source[1, 0]**2, 1-p**3
        s = 1-d*q
        amplitudes[power] = s
        private = actual.extract((0, 4, 8, 12), (0, 4, 8, 12))
        private_matrices[power] = private
        check("actual source G^r has the known-port rank4 scalar Q8 corner r%d" % power,
              ne.exact_matrix_equal(corner, s*sp.eye(4))
              and ne.exact_matrix_equal(corner.T*corner, s*s*sp.eye(4)))
        check("whole source echo is I_helper,spin on EVERY completed column r%d" % power,
              ne.exact_matrix_equal(actual, sp.kronecker_product(sp.eye(2), private, sp.eye(4))))
        unknown_cut = replace(execution, blank_wires=tuple(w for w in execution.blank_wires if w != port))
        unknown_input = ne.input_isometry(unknown_cut, **kp.rr.bounds(unknown_cut))
        unknown_corner = unknown_input.T*actual*unknown_input
        G2 = ne.G_LOCAL*ne.G_LOCAL
        expected_unknown = sp.kronecker_product((1-q)*sp.eye(2)+q*G2, sp.eye(4))
        check("the SAME word with unknown port has a genuinely different rank8 return task r%d" % power,
              ne.inventory(unknown_cut, **kp.rr.bounds(unknown_cut)).cut_rank == 8
              and ne.exact_matrix_equal(unknown_corner, expected_unknown)
              and not ne.exact_matrix_equal(unknown_corner.T*unknown_corner, s*s*sp.eye(8)))
        inv = ne.inventory(execution, **kp.rr.bounds(execution))
        gap = 134-(14+12*power)
        check("known-port source and true inverse clocks62/74/134 are matched by real two-CX words r%d" % power,
              inv.gate_count == 134 and inv.cut_rank == 4
              and (inv.g_count, inv.source_i_count, inv.cx_count) ==
                  (2*power+2, 4*power+4, 6*power+8+gap))
        sine = kp.rr.native_phase.native_rotation_intervals(power, bits=110)[1]
        qlow = 0 if sine[0] <= 0 <= sine[1] else min(sine[0]**2, sine[1]**2)
        qhigh = max(sine[0]**2, sine[1]**2)
        check("the source contrast has its certified actual positive q below one quarter r%d" % power,
              0 < qlow < qhigh < F(1, 4))
        H = paired_heat(134, 1, 2*theta, beta)
        J = -4*mp.log(1-num(zeta)+num(zeta)*num(s*s))
        native_rows.append({"source_G_power": power, "body_stages": 14+12*power,
            "matched_stages": 134, "full_dimension": inv.full_dimension, "cut_rank": 4,
            "G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
            "paired_clock_modes": 2*134*32, "full_paired_heat": mp.nstr(H, 90),
            "feedback": mp.nstr(J, 90), "q_exact_interval": [str(qlow), str(qhigh)],
            "scope": "native source contrast, not an original GR centre"})
    check("actual full paired heat is constant across fixed-middle source forks while feedback changes",
          len({row["full_paired_heat"] for row in native_rows}) == 1
          and len({row["feedback"] for row in native_rows}) == 3)

    # The old reflected middle is valid on its OWN input, but not a source
    # bridge after changing its protected port to known0.
    old, _, old_port, _ = kp.rr.middle_execution(1, reflected=True)
    old_actual = ne.word_matrix(old, **kp.rr.bounds(old))
    port_only_cut = replace(old, blank_wires=(old_port,))
    port_zero = ne.input_isometry(port_only_cut, **kp.rr.bounds(port_only_cut))
    check("old reflected-middle known-port compression is cos(theta)I on ALL remaining work/spin inputs",
          ne.exact_matrix_equal(port_zero.T*old_actual*port_zero, ne.A*sp.eye(port_zero.cols)))
    check("old reflected known-cut amplitude cannot be substituted for the new source-bearing W_K corner",
          all(not ne.exact_matrix_equal(sp.Matrix([[amplitudes[r]-ne.A]]), sp.zeros(1))
              for r in amplitudes))

    prefix_rows = []
    for length in (2, 3):
        baseline, private = kp.prefix_execution(length)
        fork, _ = kp.prefix_execution(length, fork=(2, 4))
        inv = ne.inventory(fork, **kp.rr.bounds(fork))
        bare, _ = kp.prefix_execution(length, old_right_count=0)
        check("known ports are private BLANK work, so protected Q8/oldRIGHT rank stays constant M%d" % length,
              inv.cut_rank == 8 and ne.inventory(bare, **kp.rr.bounds(bare)).cut_rank == 4
              and inv.full_dimension == 2**(4+2*length))
        check("counterfactual source fork preserves earlier native stages and future base blocks M%d" % length,
              baseline.gates[:134] == fork.gates[:134]
              and baseline.gates[268:] == fork.gates[268:]
              and baseline.gates[134:268] != fork.gates[134:268]
              and inv.gate_count == 134*length)
        check("every later completed block leaves sealed private work and immutable oldRIGHT unaddressed M%d" % length,
              all(3 not in g.wires for g in fork.gates)
              and all(not set(q for pair in private[:j] for q in pair).intersection(g.wires)
                      for j in range(1, length) for g in fork.gates[134*j:]))
        powers = [5]*length
        powers[1] = 4
        combined = sp.kronecker_product(*(private_matrices[r] for r in powers))
        c = sp.prod(amplitudes[r] for r in powers)
        check("actual known-port private corners compose into ONE scalar protected return M%d" % length,
              ne.exact_matrix_equal(sp.Matrix([[combined[0, 0]-c]]), sp.zeros(1)))
        prefix_rows.append({"cohorts": length, "stages": inv.gate_count,
            "full_dimension": inv.full_dimension, "spin_only_input_rank": 4,
            "with_one_arbitrary_oldRIGHT_rank": inv.cut_rank,
            "paired_clock_modes": 2*inv.gate_count*inv.full_dimension,
            "scope": "literal fork/protection/inventory and actual private corner; no huge clock replay"})
    f2, _ = kp.prefix_execution(2, fork=(2, 4))
    f3, _ = kp.prefix_execution(3, fork=(2, 4))
    check("a fixed known-port fork itself is append-only as new base cohorts are added",
          f3.gates[:len(f2.gates)] == f2.gates)

    # Exact scalar-kernel/product-score controls for NEW rank4 input family.
    qq, dd, gg, zz, T = sp.symbols("q d gamma zeta T", positive=True)
    ss = 1-dd*gg*qq
    aa = 2*dd*gg/ss
    Jq = -4*sp.log(1-zz+zz*T*ss**2)
    wq = 4*zz*T*ss**2/(1-zz+zz*T*ss**2)
    check("known-port true FIRST source has its derived new scalar-Gram coefficient",
          sp.cancel(sp.diff(Jq, qq)-wq*aa) == 0)
    loggain = sp.diff(wq*aa, qq)/(wq*aa)
    check("known-port log relative edge gain has its history-independent coefficient bounded by2",
          sp.cancel(loggain-aa*(sp.Rational(1, 2)-(1-zz)/(1-zz+zz*T*ss**2))) == 0)
    model_d, gamma, q0, coupling = sp.Rational(3, 4), sp.Rational(3, 4), sp.Rational(1, 10), sp.Rational(1, 50)
    P = q0*sp.eye(2)+coupling*sp.Matrix([[0, 1], [1, 0]])
    model_zeta = sp.Rational(1, 16)
    for length in (2, 3):
        state = sp.eye(2**length)[:, 0]
        c, weight, gradient = kp.product_gradient(state, [P]*length, model_d, gamma, model_zeta)
        s0 = 1-model_d*gamma*q0
        a0 = 2*model_d*gamma/s0
        v = (a0/2)**2*coupling**2
        score = -4*weight*(sp.kronecker_product(*[(sp.eye(2)-model_d*gamma*P)/s0]*length)*state-state)
        check("new fixed-rank product score includes all entangling bank excitations M%d" % length,
              sp.simplify(c-s0**length) == 0 and gradient == score
              and sp.simplify((gradient.T*gradient)[0]-(4*weight)**2*((1+v)**length-1)) == 0)
    decays = []
    for length in (16, 128, 1024):
        data = kp.scalar_data([F(1, 10)]*length)
        gain = data["weight"]*sum(data["slopes"])
        check("known-port rank is4 and its actual gain never borrows the old rank-growing lower bound M%d" % length,
              data["rank"] == 4 and 0 < data["weight"] < F(4, 2**20))
        decays.append(num(gain))
    check("the actual positive absolute source gain CAN decay despite the surviving normalized source identities",
          decays[0] > decays[1] > decays[2] and decays[-1] < mp.mpf("1e-40"))

    support = aa_api_control()
    # A separate algebraic countercontrol: port-preserving controlled A can
    # still have the correct known-leg compression.  This is NOT a new AA.
    G, G3 = ne.G_LOCAL, ne.G_LOCAL**3
    P0, P1 = sp.diag(1, 0), sp.diag(0, 1)
    A_port = sp.kronecker_product(G, P0)+sp.kronecker_product(G3, P1)
    W_private = middle_matrices[1, 1].extract((0, 4, 8, 12), (0, 4, 8, 12))
    controlled_corner = (A_port.T*W_private*A_port).extract((0, 2), (0, 2))
    expected = G.T*(sp.eye(2)-(1-p**3)*sp.diag(0, 1))*G
    check("free-port AA support is sufficient reuse, NOT a universal prohibition on every port-controlled construction",
          ne.exact_matrix_equal(controlled_corner, expected)
          and not ne.exact_matrix_equal(A_port, sp.kronecker_product(G, sp.eye(2))))

    # Same known output family, same actual clock, DIFFERENT off-input heat.
    mid1, _, _, _ = kp.middle_execution(1, 1, stages=26)
    mid2, _, _, _ = kp.middle_execution(1, 2, stages=26)
    U1 = ne.word_matrix(mid1, **kp.rr.bounds(mid1))
    U2 = ne.word_matrix(mid2, **kp.rr.bounds(mid2))
    initial = ne.input_isometry(mid1, **kp.rr.bounds(mid1))
    check("real26-stage middle edit has the SAME complete known-input output isometry on arbitrary Q8 input",
          ne.exact_matrix_equal(U1*initial, initial)
          and ne.exact_matrix_equal(U2*initial, initial)
          and len(mid1.gates) == len(mid2.gates) == 26)
    H1, H2 = paired_heat(26, 1, 2*theta, mp.mpf(1)), paired_heat(26, 1, 4*theta, mp.mpf(1))
    cosine = kp.rr.native_phase.native_rotation_intervals(2, bits=110)[0]
    tail_certificate = F(4, 54**26)/(1-F(1, 106**26))
    check("configured FULL paired middle heat is strictly different; old involutive ambient heat-zero cannot be transplanted",
          H1 > H2 and 0 < cosine[0] < cosine[1] < F(1, 2) and tail_certificate < 1)

    return {"status": "PASS", "checks": len(CHECKS), "check_names": list(CHECKS),
        "known_middle_rows": middle_rows, "native_source_rows": native_rows,
        "constant_rank_prefixes": prefix_rows,
        "absolute_gain_decay_model": [mp.nstr(v, 70) for v in decays],
        "aa_support": support,
        "matched_middle_heat_control": {"N": 26, "D": 32, "rank": 4, "beta": 1,
            "paired_modes": 1664, "H_L1": mp.nstr(H1, 100), "H_L2": mp.nstr(H2, 100),
            "heat_difference": mp.nstr(H1-H2, 70), "bessel_tail_certificate": str(tail_certificate),
            "scope": "apparatus contrast; L2 outside chosen compact d route, not a GR no-go"},
        "scope": ["all32/64 changed native matrices and exact known-port scalar return",
            "all failures/complements in full paired heat; no unknown private DATA2 cut",
            "new rational product scores are diagnostics, not new physical gate primitives",
            "no long AA/old Cartan/root/large-native suite replay",
            "no SU compiler, SourceJ, physical C1/X_N/selected-action or GR-closure promotion"],
        "numerical_scope": "110-digit configured heat values; algebraic identities, native intervals and stated Bessel sign certificate are exact"}


def pin(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(REPO)), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def section_pin(heading):
    raw = PRIMARY.read_bytes()
    start = raw.index(heading.encode())
    end = raw.find(b"\n## ", start+1)
    raw = raw[start:] if end < 0 else raw[start:end]
    return {"heading": heading, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    paths = [PACKET/n for n in ("known_port.py", "check_known_port.py", "NATIVE_IMPLEMENTATION.md",
                               "SOURCE_TRANSFER.md", "INPUT_AND_RECORD_MAP.md")]
    paths += [SOURCES/"d0_exact_report_reflected_cohorts_2026-10-25"/n for n in
              ("reflected_report.py", "PROOF.md", "COHORT_THEOREM.md")]
    paths += [SOURCES/"d0_native_cofinal_reflected_source_2026-10-25"/n for n in
              ("GEOMETRIC_MAP.md", "COFINAL_THEOREM.md")]
    paths += [SOURCES/"d0_native_price_cofield_forks_2026-10-25"/n for n in
              ("NATIVE_GRAPH.md", "STENCIL_MAP.md", "COFIELD_THEOREM.md")]
    paths += [SOURCES/"d0_native_execution_domain_2026-10-24/native_execution.py"]
    paths += [SOURCES/"d0_native_readiness_amplification_2026-10-24"/n for n in
              ("native_phase.py", "amplified_execution.py", "READINESS_AMPLIFICATION.md")]
    result["source_pins"] = [pin(p) for p in paths]
    result["section_pins"] = [section_pin("## 7e."), section_pin("## 7ai.")]
    result["generated_utc"] = datetime.now(timezone.utc).isoformat()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
