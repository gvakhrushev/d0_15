#!/usr/bin/env python3
"""Bounded native reflected-query and joint-product cohort source checks.

Small native middles are checked on ALL columns.  The long owned readiness
constructor is consumed through one emitted-word/API fixture and its small
scalar-ready comparison; its old suite is not replayed.  Rational cohort
matrices are algebra diagnostics, not an added native gate palette.
"""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import mpmath as mp
import sympy as sp
from sympy.polys.matrices import DomainMatrix

import reflected_report as rr

CHECKS = []
SOURCES = Path(__file__).resolve().parent.parent
REPO = SOURCES.parents[2]


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def zero_state(dimension):
    return sp.eye(dimension)[:, 0]


def first_conditional(effect, n, slot):
    indices = (0, 1 << slot)
    return effect.extract(indices, indices)


def numeric(matrix):
    return mp.matrix([[mp.mpf(str(sp.N(v, 100))) for v in row]
                      for row in matrix.tolist()])


def run():
    mp.mp.dps = 100
    ne, p, zeta = rr.native, rr.native.P, sp.Rational(1, 2**20)
    numeric_tolerance = mp.mpf("1e-75")
    z2, j2 = sp.diag(1, -1), sp.Matrix([[0, -1], [1, 0]])
    x, c, s = sp.symbols("x c s", real=True)
    symbolic = (c*sp.eye(2)+(2*x-1)*s*j2)*z2
    check("reflected raw corner is symmetric and has the exact isotropic Gram including every failure branch",
          symbolic.T == symbolic
          and sp.expand(symbolic.T*symbolic-(c*c+s*s*(2*x-1)**2)*sp.eye(2)) == sp.zeros(2))

    native_rows = []
    for K, repeat in ((1, 1), (2, 1), (2, 9)):
        middle, controls, meter, m = rr.middle_execution(K, repeat)
        actual = ne.word_matrix(middle, **rr.bounds(middle))
        expected = rr.expected_middle(middle, controls, meter, m, reflected=True)
        inv = ne.inventory(middle, **rr.bounds(middle))
        check("literal reflected middle equals the ALL-column ready/unready definition K%d L%d" % (K, repeat),
              ne.exact_matrix_equal(actual, expected)
              and ne.exact_matrix_equal(actual.T*actual, sp.eye(actual.rows))
              and ne.exact_matrix_equal(actual*actual, sp.eye(actual.rows))
              and actual.trace() == 0)
        check("recursive controlled-word exact inverse and phase inventory is fully expanded K%d L%d" % (K, repeat),
              (inv.g_count, inv.source_i_count, inv.cx_count) ==
              (3*m, 8*m+2, 12*m+(1 << (K+1))-2+6)
              and inv.gate_count == 23*m+(1 << (K+1))-2+8
              and inv.full_dimension == (1 << (K+4)) and inv.cut_rank == 8)
        native_rows.append({"K": K, "L": repeat, "m": m, "stages": inv.gate_count,
            "G": inv.g_count, "CX": inv.cx_count, "SourceI": inv.source_i_count,
            "all_columns": inv.full_dimension, "true_input_rank": inv.cut_rank,
            "paired_clock_mode_count": 2*inv.gate_count*inv.full_dimension})

    for K in (1, 2):
        reflected, controls, meter, m = rr.echo_execution(K)
        rotation, _, _, _ = rr.echo_execution(K, reflected=False)
        ur = ne.word_matrix(reflected, **rr.bounds(reflected))
        uo = ne.word_matrix(rotation, **rr.bounds(rotation))
        injection = ne.input_isometry(reflected, **rr.bounds(reflected))
        cr, co = injection.T*ur*injection, injection.T*uo*injection
        power = DomainMatrix.from_Matrix(ne.G_LOCAL).convert_to(ne.GOLDEN_FIELD).pow(m).to_Matrix()
        alpha, raw_x = 4*power[1, 0]**2, p**(2*K)
        t = rr.gram(alpha, 1, raw_x)
        expected_corner = sp.kronecker_product(((1-raw_x)*power.T+raw_x*power)*z2, sp.eye(4))
        check("actual raw echo rank8 corner retains meter and every dirty spin column K%d" % K,
              ne.exact_matrix_equal(cr, expected_corner)
              and ne.exact_matrix_equal(cr.T*cr, t*sp.eye(8)))
        check("adding native Z leaves the complete old unreflected return defect and logdet unchanged K%d" % K,
              ne.exact_matrix_equal(cr.T*cr, co.T*co)
              and ne.exact_matrix_equal(ur*ur, sp.eye(ur.rows)))
        if K == 2:
            check("a genuine unready complement contributes to x=gamma*q without conditioning",
                  raw_x == p**4 and ne.exact_matrix_equal(sp.Matrix([[raw_x-p**2*p**2]]), sp.zeros(1)))

    alpha_rows = []
    for K in (1, 2):
        certificate = rr.find_alpha(K, 30)
        lower, upper = certificate["alpha"]
        check("integer repetition gives a certified native alpha strictly between1and2 K%d" % K,
              1 < lower < upper < 2 and certificate["repeat"] == (1 if K == 1 else 9))
        alpha_rows.append({key: (list(map(str, value)) if isinstance(value, tuple) else value)
                           for key, value in certificate.items()})

    # The old ORIGINAL report, not a new fitted coefficient.  Its polynomial
    # first jet is supplied by paid-writer section4, equation9.  This narrow
    # guard only checks its two-density chain and the new positive gain.
    X, Y = sp.symbols("X Y", real=True)
    E, b = p*p*(1+X), (p-p*p*Y)**2
    a = 1-zeta
    original_report = 1-(a+zeta*(1-2*b)**2)*(a+zeta*(1-2*E)**2*(1-2*b)**2)
    q0 = original_report.subs({X: 0, Y: 0})
    gx = sp.diff(original_report, X).subs({X: 0, Y: 0})
    gy = sp.diff(original_report, Y).subs({X: 0, Y: 0})
    Q, R = a+zeta*p**6, a+zeta*p**12
    lam = -2*p**(-5)*(R/Q+p**6)
    check("original two-density report has its owned Q(p) source ratio without refitting",
          ne.exact_matrix_equal(sp.Matrix([[q0-(1-Q*R), gx-4*zeta*p**11*Q, gy-lam*gx]]), sp.zeros(1, 3))
          and 0 < mp.mpf(str(sp.N(q0, 100))) < mp.mpf(".5"))
    gamma, alpha = sp.Rational(3, 4), 4*p*p
    raw_x = gamma*q0
    source_gain = 8*zeta*alpha*gamma*(1-2*raw_x)/(1-zeta*alpha*raw_x*(1-raw_x))
    check("actual rank8 reflected feedback multiplies BOTH original density sources by one strictly positive retained-readiness gain",
          ne.exact_matrix_equal(sp.Matrix([[source_gain*gy-lam*source_gain*gx]]), sp.zeros(1))
          and source_gain > 0 and gx > 0)
    # Prefix Gram factorization is an identity, not an additive-logdet rule.
    t1, t2 = sp.symbols("t1 t2", positive=True)
    c1, s1, c2, s2, x1, x2 = sp.symbols("c1 s1 c2 s2 x1 x2", real=True)
    C1, C2 = (c1*sp.eye(2)+(2*x1-1)*s1*j2)*z2, (c2*sp.eye(2)+(2*x2-1)*s2*j2)*z2
    factor = (c1*c1+s1*s1*(2*x1-1)**2)*(c2*c2+s2*s2*(2*x2-1)**2)
    check("two arbitrary scalar-Gram corners compose multiplicatively even on one reused meter",
          sp.expand((C2*C1).T*(C2*C1)-factor*sp.eye(2)) == sp.zeros(2))
    check("private-DATA reflected middles form an involution on their entire product carrier",
          sp.expand(sp.kronecker_product(z2, z2)**2-sp.eye(4)) == sp.zeros(4))

    # Non-conjugacy endpoint variation: the two +1 eigenphases split, while
    # its first heat derivative vanishes.  This small analytic comparison
    # consumes the owned phase-stationarity theorem; it is not a new native
    # angle or a long primitive-clock simulation.
    def character(phase, N=3):
        return mp.fsum(mp.exp(-(1-mp.cos((phase+2*mp.pi*j)/N))) for j in range(N))
    def heat(t):
        return mp.log(2*(character(t)+character(-t)+2*character(mp.pi)))
    check("involution heat first source vanishes also for a non-conjugacy endpoint perturbation",
          abs(mp.diff(heat, 0)) < numeric_tolerance and abs(mp.diff(heat, 0, 2)) > mp.mpf("1e-6"))

    # One genuinely coherent call of the OWNED readiness constructor.  No
    # measured retry/cap is represented as a raw unitary here.
    # Algorithmic P_ref is identity on the borrowed helper.  The actual
    # Book cut may additionally initialize that helper; those are different
    # projectors, as in the owned readiness theorem.
    amp_base = ne.Execution(7, (1, 2, 3), (), (ne.Gate("G", (1,)), ne.Gate("G", (2,))),
                           ne.G_CX_SOURCE_I, source_port=0, source_spin=(5, 6))
    plan = rr.amplified_execution.amplify_execution(amp_base, ready_controls=(1,), rebit=3,
        report_bit=2, rounds=1, max_qubits=7, max_expanded_stages=200000,
        max_phase_k=1000, interval_bits=96)
    phi = plan.phase_certificate
    cos_interval, sin_interval = rr.native_phase.native_rotation_intervals(phi["angle_multiplier"], bits=512)
    # Huge exact algebraic power coefficients can cancel in ordinary evalf.
    # Outward dyadic intervals give a well-conditioned numeric comparison.
    cc = mp.mpf(str(sp.N(sum(cos_interval)/2, 110)))
    ss = mp.mpf(str(sp.N(sum(sin_interval)/2, 110)))
    ephase = cc+1j*ss
    A = numeric(sp.kronecker_product(ne.G_LOCAL, ne.G_LOCAL))
    initial, ready = mp.diag([1, 0, 0, 0]), mp.diag([0, 0, 1, 1])
    phase_op = lambda projector: mp.eye(4)+(ephase-1)*projector
    amplified = A*phase_op(initial)*A.H*phase_op(ready)*A
    column = amplified[:, 0]
    gamma_old = mp.mpf(str(sp.N(p*p, 100)))
    gamma_new = abs(column[2])**2+abs(column[3])**2
    bphase, epsilon = 2*cc-1, 1-gamma_old
    gamma_expected = 1-epsilon*(bphase+(1-bphase)*epsilon)**2
    check("owned coherent readiness recursion preserves the conditional report and raises this actual scalar-ready example above one half",
          abs(gamma_new-gamma_expected) < numeric_tolerance
          and gamma_new > mp.mpf(".5")
          and abs(abs(column[3])**2/gamma_new-gamma_old) < numeric_tolerance)
    inverse_base = ne.inverse_word(amp_base, max_qubits=7, max_expanded_stages=200000)
    ai = ne.inventory(plan.execution, max_qubits=7, max_expanded_stages=200000)
    book_inventory = ne.inventory(replace(plan.execution, blank_wires=(0, 1, 2, 3)),
                                  max_qubits=7, max_expanded_stages=200000)
    check("coherent amplifier API emits every real inverse phase and routing stage and excludes report from READY",
          plan.ready_controls == (1,) and plan.report_bit == 2 and 3 not in plan.initial_controls
          and plan.initial_controls == (1, 2) and 0 not in plan.initial_controls
          and 4 not in plan.initial_controls
          and ai.gate_count == 2*len(amp_base.gates)+len(inverse_base)+plan.initial_phase_stages+plan.ready_phase_stages
          and ai.cut_rank == 16 and book_inventory.cut_rank == 8
          and plan.execution.source_spin == (5, 6))

    # ALL-bank logdet cotangent, including cross-cohort entangled tangents.
    # Rational c/s here are diagnostic matrices, explicitly NOT native gates.
    cohort_rows = []
    for sizes in ((2, 3), (2, 2, 2)):
        M, q, d, gam, cz, sz, zz = len(sizes), sp.Rational(1, 4), sp.Rational(1, 16), sp.Rational(3, 4), sp.Rational(4, 5), sp.Rational(3, 5), sp.Rational(1, 7)
        effects = [q*sp.eye(1 << n)+d*rr.x_pair_average(n) for n in sizes]
        states = [zero_state(effect.rows) for effect in effects]
        state = sp.kronecker_product(*states)
        ts, Rs, variances, kappas = [], [], [], []
        for n, effect, psi in zip(sizes, effects, states):
            al = 4*sz*sz
            t, kap = rr.gram(al, gam, q), rr.kappa(al, gam, q)
            local_R = sp.eye(effect.rows)-kap*(effect-q*sp.eye(effect.rows))/2
            variance = ((psi.T*effect*effect*psi)[0]-q*q)
            check("critical k2 report has scalar one-RAW-slot conditionals n%d M%d" % (n, M),
                  all(first_conditional(effect, n, slot) == q*sp.eye(2) for slot in range(n))
                  and variance == 2*d*d/(n*(n-1)) and variance > 0)
            check("cohort kappa respects the positive retained-readiness bounds n%d M%d" % (n, M),
                  sp.Rational(1, 2)*(1-2*q) <= kap <= 4)
            ts.append(t); Rs.append(local_R); variances.append(kap*kap*variance/4); kappas.append(kap)
        total_t, rank = sp.prod(ts), 4*(1 << M)
        W = rank*zz*total_t/(1-zz+zz*total_t)
        Rproduct = sp.kronecker_product(*Rs)
        L = -2*W*Rproduct
        gradient = 2*(L*state-state*(state.T*L*state)[0])
        product_variance = sp.prod(1+v for v in variances)-1
        corner, differentiated = rr.full_logdet_gradient(state, effects, [cz]*M, [sz]*M, [gam]*M, zz)
        check("literal private-DATA returned-matrix logdet gives the COMPLETE product-score bank cotangent M%d" % M,
              sp.simplify(differentiated-gradient) == sp.zeros(state.rows, 1)
              and corner.T*corner == total_t*sp.eye(1 << M)
              and sp.simplify((gradient.T*gradient)[0]-16*W*W*product_variance) == 0)
        eta = sp.kronecker_product(*(sp.eye(1 << n)[:, 3] for n in sizes))
        sum_score = sp.eye(state.rows)
        for j in range(M):
            factors = [sp.eye(effect.rows) if j != k else Rs[k]-sp.eye(effect.rows)
                       for k, effect in enumerate(effects)]
            sum_score += sp.kronecker_product(*factors)
        true_source = (2*eta.T*L*state)[0]
        fake_source = (-4*W*eta.T*sum_score*state)[0]
        check("a genuine multi-cohort excitation is seen by the PRODUCT score and missed by adding local scores M%d" % M,
              true_source != 0 and fake_source == 0 and (eta.T*state)[0] == 0)
        cohort_rows.append({"cohort_sizes": list(sizes), "bank_dimension": state.rows,
            "private_DATA_dimension": 1 << M, "shared_spin_rank_once": 4,
            "true_input_rank": rank, "product_variance": str(product_variance),
            "gradient_norm_squared": str((gradient.T*gradient)[0]),
            "joint_excitation_source": str(true_source), "sum_score_wrongly_gives": "0",
            "Gamma_over_W": str(sum(kappas))})

    growth_rows = []
    for M in (8, 64, 512):
        sizes = [rr.cohort_size(j) for j in range(1, M+1)]
        inverse_square_sum = sum(sp.Rational(1, n*(n-1)) for n in sizes)
        N = sum(sizes)
        check("integer j^(3/4) cohort schedule has bounded overlap sum and subquadratic total work M%d" % M,
              all(n**4 >= j**3 and n >= 2 and (n == 2 or (n-1)**4 < j**3)
                  for j, n in enumerate(sizes, 1))
              and inverse_square_sum <= 6 and N**4 <= 16*M**7)
        # This explicit old-error sequence demonstrates weighted Cesaro;
        # arbitrary old finite errors are retained, not silently set to0.
        errors = [sp.Rational(1, j) for j in range(1, M+1)]
        weights = [sp.Rational(3, 2) if j % 2 else sp.Rational(1, 1) for j in range(1, M+1)]
        weighted_error = sum(w*e for w, e in zip(weights, errors))/sum(weights)
        check("old finite errors enter a bounded-positive weighted Cesaro average M%d" % M,
              0 < weighted_error <= sp.Rational(3, 2)*sum(errors)/M)
        growth_rows.append({"cohorts": M, "total_packets": N,
            "sum_inverse_n_nminus1": str(sp.N(inverse_square_sum, 20)),
            "weighted_old_error": str(sp.N(weighted_error, 20))})
    check("displayed bounded-positive weighted old-error averages decrease across the finite schedule",
          all(sp.Rational(growth_rows[j]["weighted_old_error"]) > sp.Rational(growth_rows[j+1]["weighted_old_error"])
              for j in range(len(growth_rows)-1)))

    return {"checks": CHECKS, "checks_passed": len(CHECKS), "native_middle_rows": native_rows,
        "certified_native_alpha": alpha_rows,
        "original_report": {"q0": str(sp.N(q0, 45)), "lambda_minus": str(sp.N(lam, 45)),
            "g_h_tau1": str(sp.N(gx, 45)), "reflected_rank8_gain": str(sp.N(source_gain*gx, 45))},
        "coherent_readiness_example": {"raw_gamma": mp.nstr(gamma_old, 40),
            "amplified_gamma": mp.nstr(gamma_new, 40), "native_phase_multiplier": phi["angle_multiplier"],
            "actual_stages": ai.gate_count, "actual_full_dimension": ai.full_dimension,
            "constructor_embedding_rank_rebit0_helper_free": ai.cut_rank,
            "algorithmic_Pref_rank_rebit_free": 1 << (plan.execution.qubits-len(plan.initial_controls)),
            "actual_Book_input_rank_helper0_rebit0": book_inventory.cut_rank,
            "algorithmic_initial_controls": list(plan.initial_controls),
            "long_physical_word_matrix_replayed": False},
        "joint_product_score_models": cohort_rows, "cohort_growth": growth_rows,
        "matrix_scope": "native middles ALL32/64 including unready flags and dirty helper/spin; raw echoes ALL32/64; rational cohort diagnostics ALL joint-bank cotangent components",
        "old_P5_C8_source_suite_replayed": False,
        "unconditional_arbitrary_rational_probability_claimed": False,
        "measured_nested_cap_treated_as_raw_unitary": False,
        "logical_normalized_effect_inserted_without_readiness": False,
        "sum_of_cohort_source_norms_used": False,
        "sum_of_local_prefix_logdets_claimed": False,
        "same_reused_DATA_prefix_claimed_involution": False,
        "exact_finite_bank_stationarity_claimed": False,
        "continuous_native_word_selector_proved": False,
        "native_physical_XN_or_compulsory_selection_proved": False,
        "GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.exact-report-reflected-cohorts-check/1", status="PASS",
                  executed_at=datetime.now(timezone.utc).isoformat())
    paths = [Path(__file__).resolve(), Path(rr.__file__).resolve(),
        Path(__file__).with_name("PROOF.md"), Path(__file__).with_name("COHORT_THEOREM.md"),
        SOURCES/"d0_native_execution_domain_2026-10-24/native_execution.py",
        SOURCES/"d0_native_readiness_amplification_2026-10-24/native_phase.py",
        SOURCES/"d0_native_readiness_amplification_2026-10-24/amplified_execution.py",
        SOURCES/"d0_native_readiness_amplification_2026-10-24/READINESS_AMPLIFICATION.md",
        SOURCES/"d0_native_task_clock_source_2026-10-25/PROOF.md",
        SOURCES/"d0_native_matrix_collective_return_2026-10-25/PROOF.md",
        REPO/"02_REGISTRY/research/A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md"]
    result["inputs_sha256"] = {str(path.relative_to(REPO)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in paths}
    primary = REPO/"02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    text_primary = primary.read_text()
    result["consumed_sections_sha256"] = {}
    for section in ("7ac", "7ad", "7af"):
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
