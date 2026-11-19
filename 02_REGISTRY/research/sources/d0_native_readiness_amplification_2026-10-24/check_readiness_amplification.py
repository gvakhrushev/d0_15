#!/usr/bin/env python3
"""Independent bounded checks of scalar-READY fixed-point amplification.

The all-input theorem is checked on nontrivial small isometries, including
an entangled reference.  Native phases are separately checked as full raw
words.  The receipt does not identify the shared-control comparison with
all independently editable controllers or the free preparer orbit.
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


CHECKS = []
FIXTURE_PHASE = (33 + 56 * sp.I) / 65


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def clean(matrix):
    return matrix.applyfunc(lambda x: sp.simplify(sp.expand_complex(x)))


def equal(left, right):
    return left.shape == right.shape and all(
        sp.simplify(sp.expand_complex(x)) == 0 for x in left - right)


def phase(projector, phase_value=FIXTURE_PHASE):
    return sp.eye(projector.rows) + (phase_value - 1) * projector


def amplify(a, initial, ready, phase_value=FIXTURE_PHASE):
    return clean(a * phase(initial, phase_value) * a.H * phase(ready, phase_value) * a)


def realify(a):
    re, im = a.applyfunc(sp.re), a.applyfunc(sp.im)
    return re.row_join(-im).col_join(im.row_join(re))


def all_input_checks():
    # A mathematical fixture for the theorem, not an added native primitive.
    # The two distinct real logical unitaries make the failure complement
    # and the two protected input columns nontrivial.
    u = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]])
    v = sp.Matrix([[0, 1], [1, 0]])
    initial = sp.diag(1, 1, 0, 0)
    ready = sp.eye(4) - initial
    # Rational point on the stable arc; the actual native phase is checked
    # separately.  Here b=2*cos(beta)-1=1/65, with no pi/3 approximation.
    fixture_phase = FIXTURE_PHASE
    fixture_b = sp.Rational(1, 65)
    phases = []
    fixture_rows = []
    for gamma in (sp.Rational(1, 4), sp.Rational(3, 5)):
        c, s = sp.sqrt(1 - gamma), sp.sqrt(gamma)
        a = (c * v).row_join(-s * v).col_join((s * u).row_join(c * u))
        check(f"all-input fixture is exactly unitary gamma={gamma}",
              equal(a.H * a, sp.eye(4)))
        max_round = 2 if gamma == sp.Rational(1, 4) else 1
        expected_gamma = gamma
        for r in range(max_round + 1):
            good = a[2:, :2]
            scalar = sp.simplify(sp.trace(u.H * good) / 2)
            check(f"entire successful isometry has one scalar gamma={gamma} r={r}",
                  equal(good, scalar * u))
            check(f"READY compression is scalar on every protected input gamma={gamma} r={r}",
                  equal((a.H * ready * a)[:2, :2], expected_gamma * sp.eye(2)))
            check(f"all failure columns retained in exact unitary gamma={gamma} r={r}",
                  equal(a.H * a, sp.eye(4)))

            # Equality of operators already includes arbitrary references.
            # This explicit Bell control checks the coherent off-diagonal.
            bell = sp.Matrix([1 / sp.sqrt(2), 0, 0, 1 / sp.sqrt(2)])
            result = sp.kronecker_product(good, sp.eye(2)) * bell
            ideal = sp.kronecker_product(u, sp.eye(2)) * bell
            check(f"unknown entangled reference retains exact successful channel gamma={gamma} r={r}",
                  equal(result * result.H, expected_gamma * ideal * ideal.H))

            if r == 1:
                phases.append(sp.simplify(scalar / sp.sqrt(expected_gamma)))
            if gamma == sp.Rational(1, 4) and r == 2:
                ra = realify(a)
                check("realification retains every dirty column as an orthogonal matrix",
                      equal(ra.T * ra, sp.eye(8)))
                check("realification is a homomorphism including adjoints",
                      equal(realify(a.H * a), realify(a).T * realify(a)))
                kr, ki = good.applyfunc(sp.re), good.applyfunc(sp.im)
                rho = bell * bell.T
                out_r = sp.kronecker_product(kr, sp.eye(2))
                out_i = sp.kronecker_product(ki, sp.eye(2))
                iu = sp.kronecker_product(u, sp.eye(2))
                check("discarding fresh phase rebit preserves the full entangled CP channel",
                      equal(out_r * rho * out_r.T + out_i * rho * out_i.T,
                            expected_gamma * iu * rho * iu.T))
            if r < max_round:
                a = amplify(a, initial, ready, fixture_phase)
                epsilon = 1 - expected_gamma
                expected_gamma = 1 - epsilon * (fixture_b + (1 - fixture_b) * epsilon) ** 2
        fixture_rows.append({"gamma": str(gamma), "maximum_round_checked": max_round,
                             "protected_input_dimension": 2,
                             "reference_dimension": 2})
    # A readiness-dependent global success phase becomes a state in the
    # fresh rebit.  It is not equality of a coherently controlled full word.
    check("successful phase depends on readiness and must remain in retained rebit",
          sp.simplify(sp.im(phases[0] * sp.conjugate(phases[1]))).is_zero is False)
    return {"fixtures": fixture_rows,
            "exact_fixture_phase": "(33+56*i)/65; b=1/65",
            "failure_recurrence": "epsilon_next=epsilon*(b+(1-b)*epsilon)^2",
            "successful_reduced_CP_channel_preserved_exactly": True,
            "successful_retained_phase_rebit_fixed": False,
            "external_control_against_idle_identified": False}


def stable_native_source_checks():
    import native_phase as np
    e, c, s = sp.symbols("epsilon c s", real=True)
    w = c + sp.I * s
    b, a = 2 * c - 1, 2 - 2 * c
    bad_coefficient = w + (w - 1) ** 2 * (1 - e)
    difference = sp.Poly(sp.expand(bad_coefficient - w * (b + a * e)), s)
    check("general equal-phase failure amplitude uses only the unit-circle identity",
          difference.rem(sp.Poly(s ** 2 + c ** 2 - 1, s)).is_zero)
    bb = sp.symbols("b", positive=True)
    h = e * (bb + (1 - bb) * e) ** 2
    check("exact native failure first jet has the claimed two factors",
          sp.factor(sp.diff(h, e)
                    - (bb + (1 - bb) * e) * (bb + 3 * (1 - bb) * e)) == 0)
    check("uniform warm-region failure ratio bound is one over 144",
          (sp.Rational(1, 16) + sp.Rational(1, 48)) ** 2 == sp.Rational(1, 144))
    check("uniform warm-region first-jet bound is one over 96",
          (sp.Rational(1, 16) + sp.Rational(1, 48))
          * (sp.Rational(1, 16) + sp.Rational(3, 48)) == sp.Rational(1, 96))

    certificate = np.find_stable_native_phase(4, 1000, bits=96)
    check("actual fixed native phase has positive sine and stable exact cosine interval",
          certificate["sine"][0] > 0
          and certificate["cosine"][0] > sp.Rational(1, 2)
          and certificate["cosine"][1] < sp.Rational(17, 32))
    indices = {}
    for arity in (0, 1, 2, 4):
        k = np.matched_phase_index(4, arity, certificate["k"])
        count = np.phase_counts((0,) * arity, k)
        indices[arity] = k
        check(f"different predicate arity has EXACTLY the same native phase K={arity}",
              count["angle_multiplier"] == certificate["angle_multiplier"])

    # Actual 7t resource, with its root prepared inside the raw word.
    # Every cancelled CX is retained.  Unknown source spin is a spectator.
    base = (ne.Gate("G", (0,)), ne.Gate("G", (1,)),
            ne.Gate("CX", (0, 1)), ne.Gate("CX", (0, 1)),
            ne.Gate("G", (2,)), ne.Gate("CX", (0, 2)),
            ne.Gate("CX", (0, 2)), ne.Gate("CX", (1, 3)),
            ne.Gate("CX", (2, 3)), ne.Gate("CX", (1, 2)))
    small = ne.Execution(4, (0, 1, 2, 3), (), base)
    column = ne.word_matrix(small)[:, 0]
    good = sp.Matrix([column[j] if j in (11, 15) else 0 for j in range(16)])
    gamma0 = 2 * ne.P ** 5
    check("actual raw 7t module has scalar spin-spectator readiness two p to fifth",
          ne.exact_matrix_equal(good.T * good, sp.Matrix([[gamma0]]))
          and ne.exact_matrix_equal(sp.Matrix([good[11], good[15]]),
                                    ne.A * ne.P ** 2 * sp.ones(2, 1)))
    # gamma0=10p-6>1/8 follows by squaring the positive rational
    # sqrt(5)>89/40, without a numerical algebraic sign oracle.
    check("actual native gamma0 has certified positive lower bound one eighth",
          ne.GOLDEN_FIELD.from_sympy(sp.expand(gamma0 - (10 * ne.P - 6)))
          == ne.GOLDEN_FIELD.zero
          and Fraction(5) > Fraction(89, 40) ** 2)
    uu = sp.symbols("u", real=True)
    gu = ne.P ** 2 * (1 - uu ** 2) / 2
    check("7t actual resource retains derivative minus gamma0 over two",
          ne.GOLDEN_FIELD.from_sympy(sp.expand(
              sp.diff(gu, uu).subs(uu, ne.P ** 3) + gamma0 / 2))
          == ne.GOLDEN_FIELD.zero)

    layout = ne.Execution(7, (0, 1, 2, 3, 4), (), base, ne.G_CX_SOURCE_I,
                          source_port=0, source_spin=(5, 6))
    bounds = dict(max_qubits=7, max_expanded_stages=100000)
    pp = np.phase_word(layout, (0, 1, 2, 3), (0, 0, 0, 0), 4,
                       indices[4], **bounds)
    pq = np.phase_word(layout, (0, 3), (1, 1), 4, indices[2], **bounds)
    reverse = ne.inverse_word(layout, **bounds)
    # Chronological A ; R_good ; A^-1 ; R_input ; A.
    first = ne.inventory(replace(layout, gates=base + pq + reverse + pp + base), **bounds)
    check("first actual amplified raw word retains all source and inverse stages",
          (first.g_count, first.cx_count, first.source_i_count, first.gate_count)
          == (1257, 1977, 1260, 4494))
    pcount = np.phase_counts((0, 0, 0, 0), indices[4])
    qcount = np.phase_counts((1, 1), indices[2])
    phase_weight = sum(5 * z["g_count"] + z["cx_count"] + z["source_i_count"]
                       for z in (pcount, qcount))
    initial_weight = 5 * 3 + 7
    check("weighted source-aware inverse bound permits fivefold recursion",
          5 * first.g_count + first.cx_count + first.source_i_count
          <= 5 * initial_weight + phase_weight)
    # Exact symbolic count inequality for EVERY raw word, including dirty
    # port routing.  Inverse G has at most six extra CX and four SourceI.
    gg, cc, ii = sp.symbols("g_count cx_count source_i_count", nonnegative=True)
    inverse_weight = 5 * gg + (cc + 6 * gg) + (3 * ii + 4 * gg)
    check("weighted inverse bound holds for all nonnegative primitive inventories",
          sp.expand(3 * (5 * gg + cc + ii) - inverse_weight) == 2 * cc)

    # Outward fixed-dyadic upper bounds: no enormous recursive circuit or
    # ill-conditioned expanded algebraic power is approximated numerically.
    scale = 1 << 1024

    def upward(value):
        value = Fraction(value)
        return Fraction(-(-(value.numerator * scale) // value.denominator), scale)

    eps, derivative = Fraction(7, 8), Fraction(1, 2)
    bmax = Fraction(1, 16)
    constant = Fraction(initial_weight) + Fraction(phase_weight, 4)
    rows = []
    q_over_tau = Fraction(1, 4) * (1 << 20)
    warm = None
    for r in range(81):
        n_bound = constant * 5 ** r
        log_bound = derivative / (1 - eps)
        time_sum_source_squared = 4 * q_over_tau ** 2 * n_bound ** 2 * eps / (1 - eps)
        if eps <= Fraction(1, 48) and warm is None:
            warm = r
        if r in (0, 1, 2, 4, 8, 16, 32, 48, 64, 80):
            rows.append({"r": r, "failure_upper": str(eps),
                         "shared_control_log_source_upper": str(log_bound),
                         "full_time_sum_source_squared_upper": str(time_sum_source_squared)})
        old = eps
        # h increases in b and epsilon.  h' need not increase in b
        # before warmup, so use its uniform bound 3 there.
        eps = upward(old * (bmax + (1 - bmax) * old) ** 2)
        derivative = upward(derivative * 3 if old > Fraction(1, 48)
                            else derivative / 96)
    check("certified finite native example enters the uniform warm region", warm is not None)
    check("certified shared 7t readiness source is small after amplification",
          q_over_tau * Fraction(rows[-1]["shared_control_log_source_upper"])
          < Fraction(1, 10 ** 100))
    check("certified readiness source is small even on the full local time-sum norm",
          Fraction(rows[-1]["full_time_sum_source_squared_upper"])
          < Fraction(1, 10 ** 40))
    # The action still sees x=gamma*q.  On an unconstrained full preparer
    # orbit this tends to q, not to the boundary x=0 or x=1.
    check("free whole-report preparer obstruction survives perfect READY",
          sp.Rational(1, 4) * (1 - sp.Rational(1, 4)) > 0)
    return {"exact_failure_recurrence": "h(epsilon)=epsilon*(b+(1-b)*epsilon)^2",
            "exact_derivative": "h'=(b+(1-b)*epsilon)*(b+3*(1-b)*epsilon)",
            "stable_native_certificate": {k: str(v) for k, v in certificate.items()},
            "matched_indices": {str(k): v for k, v in indices.items()},
            "pi_over_three_approximation_debt": False,
            "actual_raw_base": {"gamma0": "2*p^5", "G": 3, "CX": 7, "stages": 10},
            "actual_first_amplified_word": {"G": first.g_count, "CX": first.cx_count,
                                            "SourceI": first.source_i_count,
                                            "stages": first.gate_count},
            "weighted_inventory": "W=5*#G+#CX+#SourceI; W_r<=5^r*(W0+C_phase/4)",
            "phase_weight": phase_weight, "warm_region": "epsilon<=1/48",
            "uniform_failure_ratio_bound": "1/144", "uniform_derivative_bound": "1/96",
            "finite_example": {"gamma_min": "1/8", "r_final": 80,
                                "q": "1/4", "tau": "2^-20", "Omega_over_a0": "1",
                                "warmup_certified_at": warm, "outward_bits": 1024, "rows": rows},
            "actual_complete_book_normalization": "Omega*q*Dlog(gamma_r)/(a0*tau)",
            "full_time_sum_norm_bound": "2*N_r*sqrt(epsilon_r/gamma_r)",
            "outer_echo_stage_bound": "4*W_r+N_fixed_middle_and_records",
            "free_whole_preparer_source_limit": "2*Omega*sqrt(q*(1-q))/(a0*tau)"}


def operator_readiness_variation_checks():
    gamma = sp.Rational(4, 5)
    root = sp.Rational(2, 5)
    p = sp.diag(1, 1, 0, 0)
    q = sp.kronecker_product(sp.Matrix([[gamma, root], [root, 1 - gamma]]), sp.eye(2))
    check("operator readiness fixture is a full projector", equal(q * q, q))
    check("operator readiness compression is scalar on all inputs", equal(p * q * p, gamma * p))
    off = (sp.eye(4) - p) * q * p
    check("off-diagonal projector block has exact gamma times failure norm",
          equal(off.H * off, gamma * (1 - gamma) * p))
    h = sp.kronecker_product(sp.Matrix([[0, -1], [1, 0]]), sp.eye(2))
    derivative = p * (q * h - h * q) * p
    check("generic unit-speed control attains the sharp operator readiness bound",
          equal(h.H * h, sp.eye(4)) and equal(derivative, 2 * root * p))
    rotation = sp.Matrix([[sp.Rational(99, 101), -sp.Rational(20, 101)],
                          [sp.Rational(20, 101), sp.Rational(99, 101)]])
    column = sp.Matrix([sp.sqrt(gamma), sp.sqrt(1 - gamma)])
    other = rotation * column
    delta_squared = sp.simplify(((other - column).T * (other - column))[0])
    gamma_other = sp.simplify(other[0] ** 2)
    remainder = max(sp.S.Zero, abs(gamma_other - gamma) - delta_squared)
    check("finite isometry endpoint retains the exact quadratic remainder",
          equal(other.T * other, sp.eye(1))
          and remainder ** 2 <= 4 * gamma * (1 - gamma) * delta_squared)
    return {"operator_bound": "||D(P*A^dagger*READY*A*P)||<=2*sqrt(gamma*epsilon)*||A^dagger*DA||",
            "normalized_bound": "2*sqrt(epsilon/gamma)*||A^dagger*DA||",
            "local_l2_lift": "||A^dagger*DA||<=sqrt(N)*sqrt(sum_j||K_j||_op^2)",
            "local_linf_lift": "||A^dagger*DA||<=N*max_local_generator_speed",
            "finite_endpoint_bound": "||DeltaGamma||<=2*sqrt(gamma*epsilon)*||DeltaC||+||DeltaC||^2",
            "summability": "N_r^2*epsilon_r=O((25/144)^r) after finite warmup",
            "scope": "READY compression only; independent conditional-query and other Book sources retained"}


def raw_builder_checks():
    import amplified_execution as ae
    import native_phase as np
    bounds = dict(max_qubits=6, max_expanded_stages=10000)
    base = ne.Execution(6, (0, 1, 5), (),
                        (ne.Gate("G", (0,)), ne.Gate("G", (1,))),
                        ne.G_CX_SOURCE_I, source_port=2, source_spin=(3, 4),
                        report_bits=(1,))
    options = dict(ready_controls=(0,), rebit=5, report_bit=1, rounds=1,
                   max_phase_k=156, interval_bits=96, **bounds)
    plan = ae.amplify_execution(base, **options)
    check("actual builder retains full carrier and literal Book input cut",
          plan.execution.qubits == 6 and plan.execution.blank_wires == (0, 1, 5)
          and plan.levels[-1]["full_fibre_dimension"] == 64
          and plan.levels[-1]["actual_book_input_rank"] == 8)
    check("actual builder raw inverse and phase inventory matches independent count",
          (plan.levels[-1]["G"], plan.levels[-1]["CX"],
           plan.levels[-1]["SourceI"], plan.levels[-1]["stages"],
           plan.levels[-1]["weighted_inventory"]) == (1254, 1894, 1256, 4404, 9420))
    ki = np.matched_phase_index(2, 2, 156)
    kq = np.matched_phase_index(2, 1, 156)
    pin = np.phase_word(base, (0, 1), (0, 0), 5, ki, **bounds)
    good = np.phase_word(base, (0,), (1,), 5, kq, **bounds)
    inverse = ne.inverse_word(base, **bounds)
    check("actual builder chronology is A then good phase then exact inverse then input phase then A",
          plan.execution.gates == base.gates + good + inverse + pin + base.gates)
    serialized = ne.canonical_json(plan.execution)
    check("actual amplified word has strict canonical code roundtrip",
          ne.execution_from_json(serialized, **bounds) == plan.execution)
    for label, change in (("report", {"ready_controls": (1,)}),
                          ("rebit", {"ready_controls": (5,)}),
                          ("source spin", {"ready_controls": (3,)})):
        try:
            ae.amplify_execution(base, **(options | change))
        except ne.DomainError:
            check("actual READY cannot silently include " + label, True)
        else:
            raise AssertionError("builder accepted READY " + label)
    blank_spin = replace(base, blank_wires=(0, 1, 3, 4, 5))
    extended = ae.amplify_execution(blank_spin, **(options | {"rounds": 0}))
    check("algorithmic initial reflection excludes even physically blank source spin and rebit",
          extended.initial_controls == (0, 1)
          and extended.execution.blank_wires == (0, 1, 3, 4, 5)
          and extended.levels[0]["actual_book_input_rank"] == 2)
    return {"canonical_execution_sha256": hashlib.sha256(serialized.encode()).hexdigest(),
            "levels": plan.levels, "initial_controls": list(plan.initial_controls),
            "genuine_ready_controls": list(plan.ready_controls),
            "physical_Book_cut_and_algorithmic_initial_projector_identified": False,
            "constructor_checks_scalar_READY_semantics": False}


def native_phase_checks():
    # Loaded only after the mathematical checks; this imports the sibling
    # compiler owned by a different agent, not a second gate implementation.
    import native_phase as np
    rows = []
    # The compiler's exact selected angle depends on predicate arity.
    # k=1 checks every parity/complement column. The stable common angle
    # and matched indices are certified separately, with no phase error.
    for controls, pattern in (((), ()), ((0,), (1,)), ((0,), (0,)),
                              ((0, 1), (1, 0))):
        layout = ne.Execution(5, (2,), (), (), ne.G_CX_SOURCE_I,
                              source_port=0, source_spin=(3, 4))
        word = np.phase_word(layout, controls, pattern, 2, 1,
                             max_qubits=5, max_expanded_stages=100000)
        actual = ne.word_matrix(ne.Execution(
            5, (), (), word, ne.G_CX_SOURCE_I, source_port=0, source_spin=(3, 4)),
            max_qubits=5, max_expanded_stages=100000)
        expected = sp.zeros(32)
        target = ne.G_LOCAL ** (2 ** len(controls))
        for column in range(32):
            bits = [(column >> (4 - i)) & 1 for i in range(5)]
            selected = all(bits[c] == bit for c, bit in zip(controls, pattern))
            for out_bit in range(2):
                output = list(bits)
                output[2] = out_bit
                row = sum(bit << (4 - i) for i, bit in enumerate(output))
                expected[row, column] = target[out_bit, bits[2]] if selected else int(out_bit == bits[2])
        label = f"controls={controls} pattern={pattern}"
        check("native selective phase exact on ALL columns " + label,
              ne.exact_matrix_equal(actual, expected))
        counts = ne.inventory(ne.Execution(5, (), (), word, ne.G_CX_SOURCE_I,
                                          source_port=0, source_spin=(3, 4)),
                              max_qubits=5, max_expanded_stages=100000)
        check("native phase includes actual inverse/routing/source inventory " + label,
              counts.gate_count == counts.g_count + counts.cx_count + counts.source_i_count)
        rows.append({"controls": list(controls), "pattern": list(pattern),
                     "k": 1, "exact_selected_angle": f"{2 ** len(controls)}*theta0",
                     "full_dimension": 32, "stages": counts.gate_count,
                     "G": counts.g_count, "CX": counts.cx_count,
                     "SourceI": counts.source_i_count})
    try:
        np.phase_word(layout, (3,), (1,), 2, 1,
                      max_qubits=5, max_expanded_stages=100000)
    except (ne.DomainError, ValueError):
        check("source-spin predicate is not silently admitted", True)
    else:
        raise AssertionError("source-spin predicate admitted")
    return {"all_columns": True, "dirty_source_spin_restored": True,
            "selective_angle": "2^K*k*theta0", "fixtures": rows}


def run():
    CHECKS.clear()
    all_input = all_input_checks()
    source = stable_native_source_checks()
    operator = operator_readiness_variation_checks()
    native = native_phase_checks()
    builder = raw_builder_checks()
    pinned = {}
    for path in (Path(__file__), HERE / "native_phase.py", HERE / "amplified_execution.py",
                 DOMAIN / "native_execution.py"):
        pinned[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"schema": "d0.native-readiness-amplification-check/1", "status": "PASS",
            "checks_passed": len(CHECKS), "checks": CHECKS, "inputs_sha256": pinned,
            "all_input": all_input, "readiness_source": source,
            "operator_readiness_variation": operator, "native_phase": native,
            "raw_amplification_builder": builder,
            "scope": {"scalar_all_input_READY_is_required": True,
                      "READY_excludes_report_event": True,
                      "fresh_rebit_is_retained": True,
                      "report_ignores_phase_rebit": True,
                      "full_raw_word_and_inverse_inside_new_echo_required": True,
                      "absolute_old_and_new_heat_prices_identified": False,
                      "independent_copy_control_stationarity": False,
                      "free_whole_preparer_obstruction_removed": False,
                      "original_physical_admission_derived": False,
                      "full_GR_closed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
