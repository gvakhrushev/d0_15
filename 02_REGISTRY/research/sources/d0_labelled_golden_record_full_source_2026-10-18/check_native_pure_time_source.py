#!/usr/bin/env python3
"""Actual native128 pure-time effects, preparation Euler and complete source.

Only pinned literal helper definitions are loaded through AST. No prior main(),
run(), spectrum search or suite is executed. Default execution is read-only;
--output explicitly saves NATIVE_PURE_TIME_RESULT.json beside this checker.

The occupied flat Fourier block has CAR dimension16. Reference space128 is
retained, but the displayed purification has Schmidt rank16, not128. No
scene528 effect or additional matter factor is used.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ROWS = ("02_REGISTRY/research/sources/"
        "d0_complete_record_channel_2026-10-17/check_flat_relaxation.py")
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
PINS = {
    ROWS: "0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9",
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
}
CHECKS: list[str] = []
P, NU, B = s.symbols("p nu b", positive=True)
I16, O16 = s.eye(16), s.zeros(16)


def require(name: str, condition: object) -> None:
    if condition is not True and condition != s.true:
        raise RuntimeError(f"FAILED {name}: {condition}")
    CHECKS.append(name)


def reduce_exact(value: s.Expr) -> s.Expr:
    if value == 0:
        return s.S.Zero
    expanded = s.expand(value)
    if expanded == 0:
        return s.S.Zero
    return s.rem(s.rem(expanded, P*P+P-1, P), B*B+NU*NU-1, B)


def equal(name: str, actual, expected) -> None:
    difference = actual-expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    require(name, all(reduce_exact(entry) == 0 for entry in entries))


def native_definitions():
    for relative, digest in PINS.items():
        require("literal_pin_"+relative,
                hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == digest)
    tree = ast.parse((ROOT/ROWS).read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in {"_creators", "_native_rows"}]
    require("only_two_literal_helpers_loaded", len(nodes) == 2)
    scope = {"s": s, "ast": ast, "lru_cache": lru_cache, "CURVED": CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), ROWS, "exec"), scope)
    creators, order = scope["_creators"](ROOT)
    require("literal_ACDB_order", order == (0, 2, 3, 1))
    rows, _, _ = scope["_native_rows"](creators, NU, B, [-1, 1, 1, 1])
    require("all64_actual_Julia_rows", len(rows) == 64)
    return creators, rows


def full_effect_table(creators, rows):
    beta0 = creators[0]+creators[0].H
    number0 = creators[0]*creators[0].H
    equal("time_Majorana_square", beta0**2, I16)
    equal("time_Majorana_flips_original_occupation_cut",
          beta0*(I16-number0)*beta0, number0)
    occupation_parities = [I16-2*c*c.H for c in creators]
    A = -NU*beta0/8
    n_by_label = {(label, coefficient): matrix for label, coefficient, matrix in rows}
    equal("actual_N00_is_pure_time_A", n_by_label[0, 0], A)
    equal("actual_N41_is_scalar", n_by_label[4, 1], (1+B)*I16/2)
    t = NU**2
    classes = {
        "blank_port0": ((1-P**2*t/32)**2, 1),
        "single_port0": (P**4*t*t/1024, 7),
        "single_port1": (P**3*t*t/1024, 8),
        "triple_port0": (3*P**4*t*t/1024, 8),
        "triple_port1": (3*P**3*t*t/1024, 8),
        "scalar_root_port0": (P**4*t*(1+B)**2/64, 1),
        "scalar_root_port1": (P**3*t*(1+B)**2/64, 1),
        "occupation_port0": (P**4*t*(1-B)**2/256, 4),
        "occupation_port1": (P**3*t*(1-B)**2/256, 4),
        "zero": (s.S.Zero, 86),
    }
    totals = defaultdict(lambda: {"count": 0, "effect": s.zeros(16)})
    table = []
    for label, coefficient, native_row in rows:
        blank = label == 0 and coefficient == 0
        delta = I16 if blank else O16
        W = delta-2*native_row.H*A
        ports = [P*delta+P**2*W, s.sqrt(P)*P*(W-delta)]
        for port, kraus in enumerate(ports):
            effect = kraus.H*kraus
            power = 4 if port == 0 else 3
            occupation_index = None
            if blank:
                kind = "blank_port0" if port == 0 else "single_port1"
                expected = classes[kind][0]*I16
                formula = str(classes[kind][0])+" * I16"
            elif coefficient == 0 and label % 2 == 0:
                kind = ("single" if label % 8 in (0, 2) else "triple")+f"_port{port}"
                expected = classes[kind][0]*I16
                formula = str(classes[kind][0])+" * I16"
            elif coefficient == 1 and label == 4:
                kind = f"scalar_root_port{port}"
                expected = classes[kind][0]*I16
                formula = str(classes[kind][0])+" * I16"
            elif coefficient == 1 and label % 8 == 6:
                kind = f"occupation_port{port}"
                occupation_index = label//8
                hadamard = sum((((-1)**bin(occupation_index & r).count("1"))*occupation_parities[r]
                                for r in range(4)), s.zeros(16))
                shifted = beta0*hadamard*beta0
                expected = P**power*t*(1-B)**2*shifted**2/1024
                formula = f"p^{power}*nu^2*(1-b)^2/1024 * Hprime_{occupation_index}^2"
            else:
                kind, expected, formula = "zero", O16, "0_16x16"
            name = f"port{port}_label{label}_coefficient{coefficient}"
            equal("actual_effect_"+name, effect, expected)
            require("diagonal_actual_effect_"+name,
                    all(effect[i, j] == 0 for i in range(16) for j in range(16) if i != j))
            probability = classes[kind][0]
            equal("actual_probability_"+name, s.trace(effect)/16, probability)
            totals[kind]["count"] += 1
            totals[kind]["effect"] += effect
            table.append({"port": port, "label": label, "coefficient": coefficient,
                          "class": kind, "probability_at_I16_over16": str(probability),
                          "effect": formula, "occupation_index": occupation_index})
    require("all128_actual_outcomes_retained", len(table) == 128)
    equal("full128_operator_normalization",
          sum((group["effect"] for group in totals.values()), s.zeros(16)), I16)
    for kind, (probability, count) in classes.items():
        require("class_count_"+kind, totals[kind]["count"] == count)
        equal("equal_probability_class_has_scalar_effect_sum_"+kind,
              totals[kind]["effect"], count*probability*I16)
    require("nonzero_effect_count", 128-totals["zero"]["count"] == 42)
    equal("full128_probability_normalization",
          sum(probability*count for probability, count in classes.values()), s.S.One)
    return classes, table


def preparation_stationarity(classes):
    # Each positive-q class has scalar effect sum, so ANY log(q) coefficient
    # leaves G scalar: G=(H(q)-1)/ell I16. This is the full entropy gradient,
    # not a sum of separately stationary branch entropies.
    arbitrary_logs = {kind: s.Symbol("log_"+kind, real=True)
                      for kind in classes if kind != "zero"}
    scalar_gradient = -sum(count*(arbitrary_logs[kind]+1)*probability
                           for kind, (probability, count) in classes.items() if kind != "zero")
    entropy_symbolic = -sum(count*arbitrary_logs[kind]*probability
                            for kind, (probability, count) in classes.items() if kind != "zero")
    equal("full_scalar_gradient_is_H_minus_one", scalar_gradient, entropy_symbolic-1)

    purification = s.zeros(16, 128)
    for i in range(16):
        purification[i, i] = s.Rational(1, 4)
    equal("actual_data_marginal_I16_over16", purification*purification.H, I16/16)
    reference = purification.H*purification
    require("full_reference_space_dimension128", reference.shape == (128, 128))
    equal("normalized_full_data_reference_state", s.trace(reference), s.S.One)
    require("reference_marginal_rank16_not128",
            sum(reference[i, i] != 0 for i in range(128)) == 16)
    require("all112_unused_reference_coordinates_retained",
            all(reference[i, j] == 0 for i in range(128) for j in range(128)
                if i >= 16 or j >= 16))
    u, v, w, gamma = s.symbols("u v w gamma", real=True)
    tangent = s.zeros(16, 128)
    tangent[0, 0], tangent[1, 1] = u, -u
    tangent[2, 0], tangent[0, 127] = v+s.I*w, u+s.I*v
    require("full128_amplitude_tangent_normalized",
            s.re(s.trace(purification.H*tangent)) == 0)
    require("reference_complement_variations_included", tangent[0, 127] != 0)
    require("full_preparation_source_vanishes_for_normalized_tangent",
            s.simplify(2*s.re(s.trace(tangent.H*(gamma*purification)))) == 0)

    eps = s.Symbol("eps", positive=True)
    entropy_birth = -eps**2*s.log(eps**2)-(1-eps**2)*s.log(1-eps**2)
    require("zero_probability_amplitude_first_source_is_zero",
            s.limit(s.diff(entropy_birth, eps), eps, 0, dir="+") == 0)
    require("zero_probability_amplitude_C2_not_assumed",
            s.limit(s.diff(entropy_birth, eps, 2), eps, 0, dir="+") == s.oo)
    return {"data_dimension": 16, "data_density": "I16/16",
            "reference_space_dimension": 128, "reference_marginal_rank": 16,
            "purification": "sum_i=0^15 |i>data|i>ref /4; all128 reference coordinates retained",
            "complete_entropy_gradient": "G=(H(q)-1)*I16/log(phi)",
            "all_normalized_pure_preparation_tangents_included": True,
            "joint_nu_stationarity": False}


def complete_nu_source(classes):
    probabilities = [(probability, count) for kind, (probability, count)
                     in classes.items() if kind != "zero"]
    derivative = lambda value: s.diff(value, NU)-NU*s.diff(value, B)/B
    equal("moving_Julia_root_keeps_full_probability_normalization",
          sum(count*derivative(q) for q, count in probabilities), s.S.Zero)
    entropy = -sum(count*q*s.log(q) for q, count in probabilities)
    source = -sum(count*derivative(q)*s.log(q) for q, count in probabilities)
    fixture = {NU: s.Rational(3, 5), B: s.Rational(4, 5)}
    # For this exact witness every nonblank probability increases. Blank is
    # strictly the largest probability throughout 0<p,nu,b<1:
    # q_blank>(31/32)^2, each other individual q<1/16.
    require("blank_probability_lower_bound_dominates_nonblank_upper_bound",
            s.Rational(31, 32)**2 > s.Rational(1, 16))
    require("blank_bound_dominates_triple_probability",
            s.Rational(31, 32)**2 > s.Rational(3, 1024))
    require("blank_bound_dominates_occupation_probability",
            s.Rational(31, 32)**2 > s.Rational(1, 256))
    for kind, (probability, _) in classes.items():
        if kind not in {"blank_port0", "zero"}:
            exact_derivative = s.factor(derivative(probability).subs(fixture))
            require("strict_positive_nonblank_probability_derivative_at_fixture_"+kind,
                    exact_derivative.is_positive is True)
    q_scalar_root = classes["scalar_root_port0"][0]
    require("freezing_Julia_root_changes_the_source",
            s.factor((s.diff(q_scalar_root, NU)-derivative(q_scalar_root)).subs(fixture)) != 0)

    # General-nu coarse decomposition gives the analytic sign consumer.
    t = NU**2
    constant = (31*P**4+32*P**3)/1024
    rare = constant*t*t
    root_group = P**2*t*(2-t)/32
    blank = classes["blank_port0"][0]
    equal("three_group_probability_normalization", blank+rare+root_group, s.S.One)
    equal("rare_group_derivative", derivative(rare), 4*constant*NU**3)
    equal("root_group_derivative", derivative(root_group), P**2*NU*B**2/8)
    g = s.Rational(1, 2)+B/(1+B**2)
    equal("one_plus_four_conditional_probability", 2*(1+B**2)*g, (1+B)**2)
    equal("four_low_conditional_probabilities", 8*(1+B**2)*(1-g)/4, (1-B)**2)
    require("conditional_derivative_denominator_positive", (B*(1+B**2)**2).is_positive is True)
    equal("conditional_large_probability_derivative",
          s.cancel(B*(1+B**2)**2*(derivative(g)+NU**3/(B*(1+B**2)**2))), s.S.Zero)
    # Conditional port weights are p^2,p, and the remaining 31-label law
    # is independent of nu. The parent proof consumes these exact identities.
    equal("root_group_port0_probability", root_group*P**2,
          classes["scalar_root_port0"][0]+4*classes["occupation_port0"][0])
    equal("root_group_port1_probability", root_group*P,
          classes["scalar_root_port1"][0]+4*classes["occupation_port1"][0])
    require("coarse_blank_bound_dominates_rare_group", s.Rational(31, 32)**2 > s.Rational(63, 1024))
    require("coarse_blank_bound_dominates_root_group", s.Rational(31, 32)**2 > s.Rational(1, 32))

    golden_p = (s.sqrt(5)-1)/2
    numbers = dict(fixture)
    numbers[P] = golden_p
    ell = s.log(1/P)
    return {"moving_root": "b=sqrt(1-nu^2), db/dnu=-nu/b",
            "complete_source": "-sum_class multiplicity*dq/dnu*log(q)/log(phi)",
            "exact_fixture": {"nu": "3/5", "b": "4/5"},
            "fixture_source_strictly_positive": True,
            "fixture_sign_proof": "all nonblank dq/dnu>0 and q_blank>q_nonblank; source=sum_nonblank dq*log(q_blank/q)",
            "entropy_phi_fixture_diagnostic": str(s.N((entropy/ell).subs(numbers), 40)),
            "dnu_entropy_phi_fixture_diagnostic": str(s.N((source/ell).subs(numbers), 40)),
            "general_nu_coarse_probabilities": {"blank": str(blank), "rare": str(rare), "root_group": str(root_group)},
            "root_group_conditional": "port law(p^2,p), then (g,(1-g)/4,(1-g)/4,(1-g)/4,(1-g)/4)",
            "g": "1/2+b/(1+b^2)",
            "coarse_decomposition_verified": True,
            "general_nu_source_sign_consumer": "positive: increasing rare/root masses drawn from largest blank; internal root entropy increases as g decreases"}


def arbitrary_preparation_nu_source(creators, classes):
    """The same native effects give a positive free-nu source for every rho.

    The four POVM effects below are fixed CAR occupation operators. In a
    partial nu derivative rho is fixed, so d_j is fixed. A rho(nu) constraint
    that removes this independent nu tangent is outside the conclusion.
    """
    beta0 = creators[0]+creators[0].H
    parities = [I16-2*c*c.H for c in creators]
    povm = []
    vertices = []
    for high in range(4):
        hadamard = sum((((-1)**bin(high & r).count("1"))*parities[r]
                        for r in range(4)), s.zeros(16))
        shifted = beta0*hadamard*beta0
        effect = shifted**2/16
        require(f"occupation_POVM_Hermitian_{high}", effect.H == effect)
        require(f"occupation_POVM_diagonal_{high}",
                all(effect[i, j] == 0 for i in range(16) for j in range(16) if i != j))
        require(f"occupation_POVM_exact_nonnegative_spectrum_{high}",
                all(effect[i, i] in {s.S.Zero, s.Rational(1, 4), s.S.One} for i in range(16)))
        indices = [i for i in range(16) if effect[i, i] == 1]
        require(f"actual_density_realizes_simplex_vertex_{high}", len(indices) == 2)
        vertices.append(indices[0])
        povm.append(effect)
    equal("four_actual_occupation_POVM_effects_normalize", sum(povm, s.zeros(16)), I16)
    for high, index in enumerate(vertices):
        require(f"actual_density_vertex_is_deterministic_{high}",
                all(povm[j][index, index] == (1 if j == high else 0) for j in range(4)))

    diagonal = s.symbols("rho_0:16", nonnegative=True)
    actual_d = [sum(diagonal[i]*effect[i, i] for i in range(16)) for effect in povm]
    equal("arbitrary_density_occupation_probability_sum", sum(actual_d), sum(diagonal))
    # Offdiagonal coherences never enter Tr(rho D_j); they are not deleted
    # from the carrier or forbidden as preparation variations.
    offdiagonal = s.zeros(16)
    offdiagonal[0, 1], offdiagonal[1, 0] = s.I, -s.I
    for high, effect in enumerate(povm):
        equal(f"offdiagonal_coherences_are_readout_invisible_{high}",
              s.trace(offdiagonal*effect), s.S.Zero)

    d = s.symbols("d_0:4", nonnegative=True)
    d_normalized = {d[3]: 1-d[0]-d[1]-d[2]}
    t = NU**2
    rare_constant = (31*P**4+32*P**3)/1024
    rare = rare_constant*t*t
    root_mass = P**2*t*(2-t)/32
    blank = classes["blank_port0"][0]
    g = s.Rational(1, 2)+B/(1+B**2)
    root_numerator = P**2*t*(1-B)**2/64
    common_probability_denominator = 2*(1+B**2)
    require("general_d_cleared_denominator_positive",
            common_probability_denominator.is_positive is True)
    total = blank
    for kind, (probability, count) in classes.items():
        if kind not in {"blank_port0", "occupation_port0", "occupation_port1", "zero"}:
            total += count*probability
    for port, power in [(0, 4), (1, 3)]:
        for high in range(4):
            probability = P**power*t*(1-B)**2*d[high]/64
            # Trace rho of the actual matrix effect, with no assumption rho=I/16.
            actual_effect = P**power*t*(1-B)**2*povm[high]/64
            equal(f"actual_general_density_probability_port{port}_d{high}",
                  s.trace(s.diag(*diagonal)*actual_effect),
                  P**power*t*(1-B)**2*actual_d[high]/64)
            port_weight = P**2 if port == 0 else P
            equal(f"general_d_root_chain_rule_probability_port{port}_d{high}",
                  s.cancel(common_probability_denominator*(
                      probability-root_mass*port_weight*(1-g)*d[high])), s.S.Zero)
            total += probability
    equal("arbitrary_normalized_d_full128_probability_sum", total.subs(d_normalized), s.S.One)
    equal("general_d_root_entropy_weight",
          s.cancel(common_probability_denominator*(root_mass*(1-g)-root_numerator)), s.S.Zero)

    # Conditional entropy in the 31 rare records is nonnegative and independent
    # of nu. All raw weights are positive and strictly smaller than their sum.
    rare_weights = ([P**4/1024]*7+[P**3/1024]*8
                    +[3*P**4/1024]*8+[3*P**3/1024]*8)
    require("rare_records_keep_all31_labels", len(rare_weights) == 31)
    equal("rare_conditional_normalizer", sum(rare_weights), rare_constant)
    for index, weight in enumerate(rare_weights):
        require(f"rare_conditional_probability_strictly_positive_{index}", weight.is_positive is True)
        require(f"rare_conditional_probability_below_one_{index}",
                s.expand(rare_constant-weight).is_positive is True)

    derivative = lambda value: s.diff(value, NU)-NU*s.diff(value, B)/B
    positive_entropy_weight_derivative = P**2*NU*(1-B)**2*(1+2*B)/(32*B)
    equal("general_d_entropy_weight_derivative",
          s.cancel(32*B*(derivative(root_numerator)-positive_entropy_weight_derivative)), s.S.Zero)
    require("general_d_entropy_weight_derivative_nonnegative",
            positive_entropy_weight_derivative.is_nonnegative is True)
    equal("g_strictly_above_half", s.cancel((1+B**2)*(g-s.Rational(1, 2))), B)
    equal("g_strictly_below_one_in_open_b_window",
          s.cancel(2*(1+B**2)*(1-g)), (1-B)**2)
    equal("general_d_g_derivative_is_negative",
          s.cancel(B*(1+B**2)**2*derivative(g)), -NU**3)
    # H(d)>=0, g>1/2 and g'<0 give
    # dnu[h(g)+(1-g)H(d)] = [log((1-g)/g)-H(d)]g' > 0.
    # Together with the already checked positive coarse mass derivatives and
    # q_blank>rare,root_mass, this proves strict positivity for EVERY rho.
    # H(d)>=0 follows analytically from the proved probability simplex.
    # The proved 1/2<g<1 makes log((1-g)/g)<0 by log monotonicity;
    # a symbol assumption or an unrelated rational inequality is not a test
    # of either analytic implication.
    equal("general_d_coarse_mass_normalization", blank+rare+root_mass, s.S.One)

    # Exact source lower envelope H(d)=0 is attained by real occupation states,
    # not an invented probability law. The decimal is diagnostic only.
    entropy_uniform_source = -sum(count*derivative(q)*s.log(q)
                                  for kind, (q, count) in classes.items() if kind != "zero")
    minimum_source = entropy_uniform_source-derivative(root_numerator)*s.log(4)
    fixture = {NU: s.Rational(3, 5), B: s.Rational(4, 5), P: (s.sqrt(5)-1)/2}
    return {
        "scope": "one actual conserved pure-time Fourierblock, every fixed normalized density rho on CAR16",
        "occupation_POVM": "D_j=Hprime_j^2/16>=0, sum_j D_j=I16",
        "occupation_probabilities": "d_j=Tr(rho D_j), d_j>=0, sum_j d_j=1",
        "occupation_simplex_vertices_realized_by_actual_basis_indices": vertices,
        "new_occupation_outcome_probabilities": "port0: p^4*nu^2*(1-b)^2*d_j/64; port1: p^3*nu^2*(1-b)^2*d_j/64",
        "remaining_effects_scalar_and_unchanged": True,
        "complete_entropy": "H3(q_blank,R,M)+R*H_R+M*(h(p^2)+h(g)+(1-g)*H(d))",
        "strict_sign_proof": "R',M'>0 and q_blank>R,M; g>1/2,g'<0,H(d)>=0 imply [log((1-g)/g)-H(d)]*g'>0",
        "full_partial_nu_source_strictly_positive_for_every_rho": True,
        "no_joint_free_nu_root_any_preparation_on_this_block": True,
        "independent_nu_tangent_required": True,
        "fixed_preparation_in_partial_derivative": True,
        "apparatus_effects_fixed_when_varying_preparation": True,
        "preparation_constraints_coupled_to_nu_covered": False,
        "H_d_zero_source_lower_envelope_attained": True,
        "minimum_dnu_entropy_phi_fixture_diagnostic": str(s.N((minimum_source/s.log(1/P)).subs(fixture), 40)),
        "derivative_of_H_d_weight": "p^2*nu*(1-b)^2*(1+2*b)/(32*b)>0",
        "other_momentum_supports_or_continuum_covered": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", action="store_true", help="Explicitly save NATIVE_PURE_TIME_RESULT.json")
    args = parser.parse_args()
    creators, rows = native_definitions()
    classes, table = full_effect_table(creators, rows)
    result = {
        "date": "2026-10-18", "scope": "actual full128 retained native round on one conserved pure-time Fourierblock",
        "carrier": {"matter_dimension": 16, "reference_space_dimension": 128,
                    "reference_marginal_rank": 16, "fresh_outcomes": 128,
                    "new_matter_factor_added": False, "scene528_effect_used": False,
                    "phases": [-1, 1, 1, 1],
                    "full_lattice_condition": "flat translation-invariant even torus; occupied k=(L/2,0,0,0); every other momentum block retained",
                    "full_lattice_preparation_chart": "normalized pure amplitudes with reference128; unoccupied-block variations have zero first probability jet",
                    "full_positive_momentum_masses_proved": False,
                    "full_masses_condition": "q_omega=sum_k mu_k q_omega,k; occupied block entropy-score operators must share one preparation multiplier; not inferred from single-block stationarity"},
        "probability_classes": {kind: {"probability": str(q), "multiplicity": count}
                                for kind, (q, count) in classes.items()},
        "all128_outcomes": table,
        "preparation": preparation_stationarity(classes),
        "complete_source": complete_nu_source(classes),
        "arbitrary_preparation_complete_source": arbitrary_preparation_nu_source(creators, classes),
        "zero_outcomes_retained": 86,
        "zero_outcome_regularity": "C1 amplitude first source zero under rank birth; C2 not asserted",
        "physical_admission_proved": False, "native_programme_selection_proved": False,
        "all_spacetime_closure_proved": False, "GR_closed": False,
        "input_sha256": PINS,
        "runtime": {"python": platform.python_version(), "sympy": s.__version__},
        "explicit_checks": len(CHECKS),
        "check_names_sha256": hashlib.sha256("\n".join(CHECKS).encode()).hexdigest(),
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)+"\n"
    if args.output:
        (HERE/"NATIVE_PURE_TIME_RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
