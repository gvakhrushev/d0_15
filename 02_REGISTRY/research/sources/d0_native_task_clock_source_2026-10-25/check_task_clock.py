#!/usr/bin/env python3
"""Bounded actual tail and all-terminal-task cyclic heat/source controls.

Consumes the old native32Y proof/receipt. It does not rerun that suite,
construct the full128 endpoint, or construct its11008-mode clock matrix.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp
import task_clock as tc

CHECKS = []
SOURCES = Path(__file__).resolve().parent.parent
REPO = SOURCES.parents[2]


def check(name, statement):
    if not statement:
        raise AssertionError(name)
    CHECKS.append(name)


def trace(a):
    return mp.fsum(a[j, j] for j in range(a.rows))


def norm(a):
    if a.cols == 1:
        return mp.sqrt(mp.re((a.H*a)[0]))
    eigenvalues = mp.eighe(a.H*a, eigvals_only=True)
    return mp.sqrt(max(mp.mpf(0), max(mp.re(v) for v in eigenvalues)))


def kron(a, b):
    return mp.matrix([[a[i//b.rows, j//b.cols]*b[i % b.rows, j % b.cols]
                       for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])


def matrix_gibbs(gates, beta):
    shift, delta = tc.clock(gates)
    heat = mp.expm(-beta*delta)
    z = trace(heat)
    return shift, delta, heat/z, 2*z


def edge_source(gates, rho, edge, derivative):
    dimension, stages = gates[0].rows, len(gates)
    row = ((edge+1) % stages)*dimension
    return mp.re(mp.fsum(rho[edge*dimension+b, row+a]*derivative[a, b]
                          for a in range(dimension) for b in range(dimension)))


def run():
    mp.mp.dps = 220
    tol = mp.mpf("1e-180")
    ne = tc.ne
    p = (mp.sqrt(5)-1)/2
    theta, stages, beta = mp.asin(p), 43, mp.mpf(1)
    alpha = 2*theta
    old_receipt_path = SOURCES/"d0_native_bilinear_return_echo_2026-10-25/CHECK_RESULT.json"
    old = json.loads(old_receipt_path.read_text())
    check("old native ALL32 Y/return proof is consumed from its immutable PASS41 receipt, not replayed",
          old["status"] == "PASS" and old["checks_passed"] == 41
          and old["full_dimension"] == 32 and old["input_cut_rank"] == 8
          and old["original_return_corner_realized"]
          and not old["original_full8_logical_query_realized"])

    local = tc.local_tail()
    b_native = ne.word_matrix(local, max_qubits=5, max_expanded_stages=10000)
    b4 = sp.diag(sp.eye(2), ne.G_LOCAL**2)
    expected = sp.kronecker_product(sp.eye(2), b4, sp.eye(4))
    local_inventory = ne.inventory(local, max_qubits=5, max_expanded_stages=10000)
    check("new14-stage tail is I_port tensor controlled G squared tensor I_spin on ALL32 dirty columns",
          ne.exact_matrix_equal(b_native, expected)
          and local_inventory.gate_count == 14 and local_inventory.g_count == 2
          and local_inventory.cx_count == 8 and local_inventory.source_i_count == 4)
    check("tail is exactly all-column orthogonal and genuinely changes unprepared control1 columns",
          ne.exact_matrix_equal(b_native.T*b_native, sp.eye(32))
          and not ne.exact_matrix_equal(b_native, sp.eye(32)))
    blank = sp.Matrix([1, 0, 0, 0])
    pblank = blank*blank.T
    check("tail fixes the full blank ancilla input column and projector exactly",
          ne.exact_matrix_equal(b4*blank, blank)
          and ne.exact_matrix_equal(b4*pblank, pblank)
          and ne.exact_matrix_equal(b4.T*pblank*b4, pblank))
    check("the first even winding has the exact positive native coefficient1 minus cos4theta equals8p cubed",
          ne.exact_matrix_equal(sp.Matrix([[1-(ne.G_LOCAL**4)[0, 0]]]),
                                sp.Matrix([[8*ne.P**3]]))
          and 8*p**3 > 0)

    baseline, edited = tc.fixture()
    rows = []
    for label, execution, counts in (
            ("baseline", baseline, (4, 27, 12)),
            ("edited", edited, (6, 21, 16))):
        inv = ne.inventory(execution, max_qubits=7, max_expanded_stages=10000)
        check(label+" pays every actual gate at commonT43 dimension128 inputrank8",
              inv.gate_count == 43 and inv.full_dimension == 128 and inv.cut_rank == 8
              and (inv.g_count, inv.cx_count, inv.source_i_count) == counts
              and execution.blank_wires == (0, 1, 5, 6)
              and execution.source_port == 0 and execution.source_spin == (3, 4))
        rows.append({"word": label, "actual_stages": inv.gate_count,
                     "G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
                     "full_dimension": inv.full_dimension, "input_cut_rank": inv.cut_rank})
    check("both task fixtures have the same initial carrier cut source profile and full paired mode count",
          baseline.qubits == edited.qubits == 7
          and baseline.blank_wires == edited.blank_wires
          and baseline.old_right == edited.old_right == () and 2*43*128 == 11008)

    # The owned32Y endpoint has +/-1 sixteen times each. Together with
    # the newly verified tensor factor and B|00>=|00>, this proves the
    # entire128 prepared output column is equal, without a128 replay.
    c2 = (1-2*p*p)*((1-p*p)*mp.eye(2)-p*p*mp.matrix([[0, 1], [1, 0]]))
    c_old = kron(c2, mp.eye(4))
    factor_on_blank = mp.mpf(str(sp.N((blank.T*b4*blank)[0], 230)))
    c_new = factor_on_blank*c_old
    zeta = mp.mpf(2)**-20
    j_old = -mp.log(mp.det((1-zeta)*mp.eye(8)+zeta*c_old.T*c_old))
    j_new = -mp.log(mp.det((1-zeta)*mp.eye(8)+zeta*c_new.T*c_new))
    check("owned Y tensor the exact tail has equal full input-to-output isometry and identical rank8 feedback",
          factor_on_blank == 1 and norm(c_new-c_old) == 0 and j_new == j_old)

    s0 = tc.even_character(0, stages, beta)
    sa = tc.even_character(alpha, stages, beta)
    z_base, z_edit = 128*s0, 64*(s0+sa)
    phases = [mp.mpf(0)]*32+[mp.pi]*32+[alpha]*16+[-alpha]*16
    phases += [mp.pi+alpha]*16+[mp.pi-alpha]*16
    explicit_z = 2*mp.fsum(tc.character(w, stages, beta) for w in phases)
    check("all128 phase multiplicities and all11008 paired clock modes match the complete heat formula",
          len(phases) == 128 and 2*len(phases)*stages == 11008
          and abs(explicit_z-z_edit) < tol)
    winding = 4*stages*mp.exp(-beta)*mp.fsum(
        mp.besseli(2*m*stages, beta)*(1-mp.cos(2*m*alpha)) for m in range(1, 4))
    first_positive = 4*stages*mp.exp(-beta)*mp.besseli(2*stages, beta)*(8*p**3)
    check("strict heat sign follows the positive EVEN winding86 term rather than a rounded subtraction",
          first_positive > 0 and winding >= first_positive*(1-mp.mpf("1e-210"))
          and s0 > sa and abs((s0-sa)/winding-1) < mp.mpf("1e-55"))
    gap = mp.log(z_edit/z_base)/beta
    gap_stable = mp.log1p(-winding/(2*s0))/beta
    check("actual same-terminal-task native edit strictly lowers complete H plus J at common clock",
          gap < 0 and j_new == j_old
          and abs(gap/gap_stable-1) < mp.mpf("1e-55"))

    # The phase derivative is zero at every involution endpoint, including
    # arbitrary independently moving off-band columns: a base first-source
    # statement, not a minimum or an exact finite-price invariance.
    check("clock character derivatives vanish at BOTH involution phases0 and pi",
          abs(tc.character_derivative(0, stages, beta)) < tol
          and abs(tc.character_derivative(mp.pi, stages, beta)) < tol)
    v4 = mp.diag([1, 1, -1, -1])
    skew = mp.zeros(4)
    for a, b, coefficient in ((0, 1, 1), (0, 2, mp.mpf(".3")), (2, 3, mp.mpf(".2"))):
        skew[a, b], skew[b, a] = -coefficient, coefficient
    base_gates = [mp.eye(4), mp.eye(4), v4]
    _, _, rho4, partition4 = matrix_gibbs(base_gates, beta)
    base_source = edge_source(base_gates, rho4, 2, v4*skew)
    eps = mp.mpf(".01")
    plus_gates = [mp.eye(4), mp.eye(4), v4*mp.expm(eps*skew)]
    minus_gates = [mp.eye(4), mp.eye(4), v4*mp.expm(-eps*skew)]
    _, _, _, zp = matrix_gibbs(plus_gates, beta)
    _, _, _, zm = matrix_gibbs(minus_gates, beta)
    check("nonconjugate real-unitary endpoint motion has exactly zero heat FIRST source at an involution base",
          norm(v4*skew-skew*v4) > 0 and abs(base_source) < tol
          and abs(mp.log(zp/zm)/(2*eps*beta)) < tol
          and abs(mp.log(zp/partition4)/beta) > mp.mpf("1e-10"))

    bound_rows = []
    for t in (3, 5, 8, 16, 43):
        b = tc.source_bounds(t, beta)
        check("owned positive winding tail and factorial majorant are consistent T"+str(t),
              0 < b["winding_partial"] <= b["winding_upper"]
              and b["winding_tail_upper"] > 0
              and b["endpoint_upper"] <= mp.mpf(1)/t)
        bound_rows.append({"T": t, "endpoint_L_upper": mp.nstr(b["endpoint_upper"], 35),
                           "gate_ell2_upper": mp.nstr(b["gate_ell2_upper"], 35),
                           "gate_ellinf_upper": mp.nstr(b["gate_ellinf_upper"], 35),
                           "winding_tail_upper": mp.nstr(b["winding_tail_upper"], 15)})
    q_exact = Fraction(1, 2*(43+1))**43
    check("closed majorant condition q below1 is exact and a growing-beta case falls back to1 overT",
          0 < q_exact < 1 and tc.source_bounds(3, mp.mpf(100))["endpoint_upper"] == mp.mpf(1)/3)

    # A small literal full15-mode clock checks the dimension-free Gibbs
    # argument and gate norms. These are real operator curves, not a new
    # continuously variable Golden primitive.
    angles = [mp.mpf(t) for t in (".1", ".2", ".3", ".4", ".5")]
    gates = [tc.hidden_rotation(a) for a in angles]
    t, d, beta_test = 5, 3, mp.mpf(".7")
    _, _, rho, partition = matrix_gibbs(gates, beta_test)
    diagonal_traces = [trace(rho[j*d:(j+1)*d, j*d:(j+1)*d]) for j in range(t)]
    block = rho[0:d, (t-1)*d:t*d]
    singular_values = mp.eighe(block.H*block, eigvals_only=True)
    block_trace_norm = mp.fsum(mp.sqrt(max(mp.mpf(0), mp.re(x))) for x in singular_values)
    check("full small Gibbs clock has uniform1 overT block mass and closing-block trace norm at most1 overT",
          max(abs(v-mp.mpf(1)/t) for v in diagonal_traces) < tol
          and block_trace_norm <= mp.mpf(1)/t+tol)
    phase = mp.fsum(angles)
    z_character = 2*(tc.character(0, t, beta_test)+2*tc.character(phase, t, beta_test))
    check("small literal full-clock trace retains every phase and both Hodge copies",
          abs(partition-z_character) < tol)
    generator = mp.zeros(3)
    generator[1, 2], generator[2, 1] = -1, 1
    sources = [edge_source(gates, rho, j, gates[j]*generator) for j in range(t)]
    analytic = 2*tc.character_derivative(phase, t, beta_test)/(beta_test*z_character/2)
    b = tc.source_bounds(t, beta_test)
    check("exact Duhamel gate sources agree with the all-phase derivative and uniform endpoint bound",
          max(abs(v-analytic) for v in sources) < tol and abs(analytic) > mp.mpf("1e-8")
          and abs(analytic) <= b["endpoint_upper"])
    check("true task-preserving gate ell2 and ellinfinity dual norms have the stated real T factors",
          mp.sqrt(mp.fsum(v*v for v in sources)) <= b["gate_ell2_upper"]
          and mp.fsum(abs(v) for v in sources) <= b["gate_ellinf_upper"]
          and all(norm(g[:, 0]-mp.matrix([1, 0, 0])) == 0 for g in gates))
    end_a, end_b = mp.mpf(".4"), mp.mpf("1.2")
    heat_a = tc.heat_of_phases((0, end_a, -end_a), t, beta_test)
    heat_b = tc.heat_of_phases((0, end_b, -end_b), t, beta_test)
    chord = norm(tc.hidden_rotation(end_a)-tc.hidden_rotation(end_b))
    length = abs(end_b-end_a)
    check("finite same-output fibre values obey log-path and chord bounds without a native smooth-word assumption",
          abs(heat_b-heat_a) <= b["endpoint_upper"]*length
          and length <= mp.pi*chord/2 and length < mp.pi)

    # The one-cut two-private-DATA refinement guard is small and separate
    # from the clock controls. Exact positive-factor identities establish
    # the sign; high precision only evaluates its size.
    exact = tc.two_block_ratios(ne.P, sp.Rational(1, 2**20))
    A, B, a = exact["A"], exact["B"], exact["a"]
    ze = sp.Rational(1, 2**20)
    posA = a*ze*(A-B)*(1-A)/((a+ze*A*A)*(a+ze*A))
    posB = a*ze*(A-B)*(1-B)/((a+ze*A*B)*(a+ze*A))
    average = (exact["w_A"]*exact["r_A"]+exact["w_B"]*exact["r_B"])/(exact["w_A"]+exact["w_B"])
    positive_gap = 2*ne.P**(-5)*(exact["w_A"]*posA+exact["w_B"]*posB)/(exact["w_A"]+exact["w_B"])
    identities = sp.Matrix([[exact["S_A"]/exact["S_B"]-average,
                             exact["r_A"]-exact["R"]/exact["Q"]-posA,
                             exact["r_B"]-exact["R"]/exact["Q"]-posB,
                             exact["lambda1"]-exact["lambda2"]-positive_gap]])
    # 309/500<p<619/1000 follows by squaring positive rational bounds
    # on sqrt5. It implies 0<B<A<1 and every displayed factor is >0.
    rational_p_bounds = (1+2*Fraction(309, 500))**2 < 5 < (1+2*Fraction(619, 1000))**2
    ratios = tc.two_block_ratios(p, zeta)
    lambda_gap = ratios["lambda1"]-ratios["lambda2"]
    check("two-block coefficient is an exact positive-weight native Q(p) average and lambda2 is strictly below lambda1",
          ne.exact_matrix_equal(identities, sp.zeros(1, 4)) and rational_p_bounds
          and 0 < ratios["B"] < ratios["A"] < 1
          and ratios["w_A"] > 0 and ratios["w_B"] > 0
          and ratios["R"]/ratios["Q"] < ratios["S_A"]/ratios["S_B"] < 1
          and mp.mpf("1e-9") < lambda_gap < mp.mpf("1e-4"))

    def c_original(x, y):
        E, bb = p*p*(1+x), (p-p*p*y)**2
        return (1-2*bb)*((1-E)*mp.eye(2)-E*mp.matrix([[0, 1], [1, 0]]))

    c_reference = c_original(0, 0)

    def cumulative_price(x, y):
        c = c_original(x, y)
        returned4 = kron(c, c_reference)
        return -4*mp.log(mp.det((1-zeta)*mp.eye(4)+zeta*returned4.T*returned4))

    source_x = mp.diff(lambda x: cumulative_price(x, 0), 0)
    source_y = mp.diff(lambda y: cumulative_price(0, y), 0)
    standalone = -4*mp.log(mp.det((1-zeta)*mp.eye(2)+zeta*c_reference.T*c_reference))
    check("literal4by4 cumulative returned-matrix logdet with shared spin4 once differentiates to lambda2 rather than lambda1",
          source_x > 0 and abs(source_x-16*zeta*p**11*ratios["S_B"]) < tol
          and abs(source_y/source_x-ratios["lambda2"]) < tol
          and abs(source_y/source_x-ratios["lambda1"]) > mp.mpf("1e-9")
          and abs(cumulative_price(0, 0)-2*standalone) > mp.mpf("1e-8"))

    return {"checks": CHECKS, "checks_passed": len(CHECKS), "native_fixture": rows,
            "paired_clock_modes": 11008,
            "whole_native_price_gap": {"beta": "1", "T": 43, "J_equal": True,
                "H_edit_minus_baseline": mp.nstr(gap_stable, 60),
                "first_strict_even_winding_index": 86,
                "positive_first_winding_term": mp.nstr(first_positive, 45)},
            "source_bounds": bound_rows,
            "small_full_clock": {"T": 5, "fibre_dimension": 3, "paired_modes": 30,
                "closing_Gibbs_block_trace_norm": mp.nstr(block_trace_norm, 35),
                "each_gate_source": mp.nstr(analytic, 35)},
            "two_private_DATA_cumulative_cut": {"DATA_return_dimension": 4, "shared_spin_multiplier": 4,
                "lambda1": mp.nstr(ratios["lambda1"], 50), "lambda2": mp.nstr(ratios["lambda2"], 50),
                "lambda1_minus_lambda2": mp.nstr(lambda_gap, 35),
                "old_block_Dx": mp.nstr(source_x, 35), "old_block_Dy": mp.nstr(source_y, 35),
                "price_is_sum_of_two_local_prices_claimed": False},
            "exact_involution_base_heat_gradient_zero": True,
            "native_local_tail_all32_replayed": True, "native_old_Y_suite_replayed": False,
            "native_full128_or11008_clock_matrix_replayed": False,
            "full_terminal_task_isometry_equal": True,
            "primitive_prefix_or_code_header_history_equal_claimed": False,
            "continuous_native_angle_primitive_claimed": False,
            "autonomous_controller_or_original_XN_admission_proved": False,
            "task_fibre_price_exactly_constant_claimed": False,
            "full_native_joint_stationarity_proved": False, "GR_closed": False,
            "numeric_arithmetic": "220-digit mpmath non-interval; exact Q(sqrt(p)) tail/matrix identities and rational q separate"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.native-task-clock-source-check/1", status="PASS")
    paths = [Path(__file__).resolve(), Path(tc.__file__).resolve(), Path(__file__).with_name("PROOF.md"),
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25/PROOF.md",
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25/native_echo.py",
             SOURCES/"d0_native_bilinear_return_echo_2026-10-25/CHECK_RESULT.json",
             SOURCES/"d0_native_execution_domain_2026-10-24/native_execution.py",
             SOURCES/"d0_recorded_scene_clock_heat_2026-10-22/THEOREM.md"]
    result["inputs_sha256"] = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    primary = REPO/"02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    text_primary = primary.read_text()
    result["consumed_sections_sha256"] = {}
    for section in ("7ab", "7ac", "7ad"):
        start = text_primary.index("## "+section+".")
        end = text_primary.find("\n## ", start+4)
        body = text_primary[start:end if end >= 0 else len(text_primary)]
        result["consumed_sections_sha256"][section] = hashlib.sha256(body.encode()).hexdigest()
    result["runtime"] = {"python": sys.version.split()[0], "mpmath": mp.__version__, "sympy": sp.__version__}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
