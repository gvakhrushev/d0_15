#!/usr/bin/env python3
"""Exact small test of the supplied complete-code/right-posterior application.

This is a rational quantum ledger fixture, not a replacement native gate or
code.  The original primary interval is transported from its pinned accepted
certificate; no matrix, old checker main, or eigensolver is replayed.
"""

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md":
        "3e177e614fb2b30d202f13af65d9896211afeebd68bcb2b497800a7ed0edaba5",
    PREFIX + "check_primary_right_posterior_gain.py":
        "2985ab0b4fb007c424c75d2bd57369b781ad1b1653ec3b8b8c68d4d30780367d",
    PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json":
        "3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a",
    "02_REGISTRY/research/sources/d0_operational_gain_2026-10-15/RESULT.md":
        "428bdda31e27ea6e7bf18ac93528fa4bc21c28677026341af2e86a36ac67ff52",
    PREFIX + "BOOK_SOURCE_BINDING.md":
        "2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea",
}


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


def clean(expression):
    return {key: F(value) for key, value in expression.items() if value}


def add(*expressions):
    result = {}
    for expression in expressions:
        for key, value in expression.items():
            result[key] = result.get(key, F(0)) + value
    return clean(result)


def scale(number, expression):
    return clean({key: number * value for key, value in expression.items()})


def constant(number):
    return {"constant": F(number)} if number else {}


def logarithm(number):
    """Exact log of a positive rational as integer prime-log coefficients."""
    number = F(number)
    require(number > 0, "positive rational logarithm")
    result = {}
    for integer, sign in ((number.numerator, 1), (number.denominator, -1)):
        prime = 2
        while prime * prime <= integer:
            while integer % prime == 0:
                result[prime] = result.get(prime, F(0)) + sign
                integer //= prime
            prime += 1
        if integer > 1:
            result[integer] = result.get(integer, F(0)) + sign
    return clean(result)


def zero(expression, message):
    require(not clean(expression), message)


def matrix_scale(number, matrix):
    return tuple(tuple(number * entry for entry in row) for row in matrix)


def matrix_add(*matrices):
    return tuple(tuple(sum(matrix[i][j] for matrix in matrices) for j in range(2)) for i in range(2))


def matrix_product(left, right):
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


IDENTITY = ((F(1), F(0)), (F(0), F(1)))
ZERO_MATRIX = matrix_scale(0, IDENTITY)
X = ((F(0), F(1)), (F(1), F(0)))
Z = ((F(1), F(0)), (F(0), F(-1)))


def rational_quantum_fixture(mutation):
    blocks = (
        matrix_scale(F(1, 60), ((13, 0), (0, 7))),
        matrix_scale(F(1, 60), ((10, 4), (4, 10))),
        matrix_scale(F(1, 60), ((7, -4), (-4, 13))),
    )
    d0 = matrix_add(matrix_scale(F(1, 30), IDENTITY), matrix_scale(F(1, 100), Z))
    d1 = matrix_add(matrix_scale(F(-1, 60), IDENTITY), matrix_scale(F(1, 75), X))
    derivatives = (d0, d1, matrix_scale(-1, matrix_add(d0, d1)))
    eigenvalues = ((F(13, 60), F(7, 60)), (F(7, 30), F(1, 10)), (F(1, 4), F(1, 12)))
    eigenjets = ((F(13, 300), F(7, 300)), (F(-1, 300), F(-3, 100)), (F(0), F(-1, 30)))
    q, dq = (F(1, 3),) * 3, (F(1, 15), F(-1, 30), F(-1, 30))
    mu, dmu = (F(1, 2), F(1, 3), F(1, 6)), (F(1, 10), F(-1, 15), F(-1, 30))
    require(matrix_add(*blocks) == matrix_scale(F(1, 2), IDENTITY), "intrinsic uniform RIGHT prior")
    require(matrix_add(*derivatives) == ZERO_MATRIX, "zero prior derivative")
    commutator = matrix_add(matrix_product(blocks[0], blocks[1]),
                            matrix_scale(-1, matrix_product(blocks[1], blocks[0])))
    require(commutator == ((F(0), F(1, 150)), (F(-1, 150), F(0))),
            "genuinely noncommuting posterior blocks")
    for block, derivative, values, jets, probability, jet in zip(blocks, derivatives, eigenvalues, eigenjets, q, dq):
        require(sum(values) == probability and sum(jets) == jet, "eigenvalue trace and first jet")
        plus = matrix_scale(1 / (values[0] - values[1]),
                            matrix_add(block, matrix_scale(-values[1], IDENTITY)))
        minus = matrix_add(IDENTITY, matrix_scale(-1, plus))
        require(matrix_product(plus, plus) == plus and matrix_product(minus, minus) == minus
                and matrix_product(plus, minus) == ZERO_MATRIX, "exact rational spectral projectors")
        require(matrix_add(matrix_scale(values[0], plus), matrix_scale(values[1], minus)) == block
                and matrix_add(matrix_scale(jets[0], plus), matrix_scale(jets[1], minus)) == derivative,
                "exact block and derivative spectral expansions")
        require(all(value - abs(delta) > 0 for value, delta in zip(values, jets)),
                "positive support for every |t|<=1")
    require(sum(mu) == sum(q) == 1 and sum(dmu) == sum(dq) == 0,
            "complete state/code and normalized first jets")
    require(all(weight - abs(delta) > 0 for weight, delta in zip(mu, dmu)),
            "moving complete code remains positive for |t|<=1")

    cost = add(*(scale(-probability, logarithm(weight)) for probability, weight in zip(q, mu)))
    classical = add(*(scale(probability, logarithm(probability / weight)) for probability, weight in zip(q, mu)))
    posterior = add(*(scale(value, logarithm(2 * value / q[j])) for j in range(3) for value in eigenvalues[j]))
    full_gain = add(*(scale(value, logarithm(2 * value / mu[j])) for j in range(3) for value in eigenvalues[j]))
    pointer = add(*(scale(-probability, logarithm(probability)) for probability in q))
    joint_entropy = add(*(scale(-value, logarithm(value)) for pair in eigenvalues for value in pair))
    conditional = add(pointer, scale(-1, posterior))
    zero(add(full_gain, scale(-1, classical), scale(-1, posterior)), "full central-reference chain at value")
    zero(add(cost, scale(-1, full_gain), scale(-1, conditional)), "label cost minus full gain is H(Y|R)")
    full_operator_cost = add(cost, logarithm(F(2)))
    if mutation == "omit-log-dimension":
        full_operator_cost = cost
    zero(add(full_operator_cost, scale(-1, full_gain), scale(-1, joint_entropy)),
         "full operator cost includes log RIGHT dimension")

    code_motion = -sum(probability * delta / weight for probability, delta, weight in zip(q, dmu, mu))
    require(code_motion == F(1, 15), "nonzero moving-code contribution")
    dcost_fixed = add(*(scale(-delta, logarithm(weight)) for delta, weight in zip(dq, mu)))
    dcost = add(dcost_fixed, constant(code_motion))
    dclassical_fixed = add(*(scale(delta, logarithm(probability / weight))
                              for delta, probability, weight in zip(dq, q, mu)))
    dclassical = add(dclassical_fixed, constant(code_motion))
    dposterior = add(*(scale(delta, logarithm(2 * value / q[j])) for j in range(3)
                      for value, delta in zip(eigenvalues[j], eigenjets[j])))
    dfull_fixed = add(*(scale(delta, logarithm(2 * value / mu[j])) for j in range(3)
                       for value, delta in zip(eigenvalues[j], eigenjets[j])))
    dfull = add(dfull_fixed, constant(code_motion))
    dpointer = add(*(scale(-delta, logarithm(probability)) for delta, probability in zip(dq, q)))
    dconditional = add(dpointer, scale(-1, dposterior))
    djoint = add(*(scale(-delta, logarithm(value)) for values, deltas in zip(eigenvalues, eigenjets)
                  for value, delta in zip(values, deltas)))
    zero(add(dfull, scale(-1, dclassical), scale(-1, dposterior)), "moving-code full chain first jet")
    zero(add(dcost_fixed, scale(-1, dfull_fixed), scale(-1, dconditional)), "fixed-code net jet")
    require(add(dcost_fixed, scale(-1, dfull), scale(-1, dconditional)) == constant(-code_motion),
            "hostile frozen cost term gives a different net source")
    require(add(dcost, scale(-1, dfull_fixed), scale(-1, dconditional)) == constant(code_motion),
            "hostile frozen reference term gives a different net source")
    if mutation == "omit-moving-reference":
        dfull = dfull_fixed
    zero(add(dcost, scale(-1, dfull), scale(-1, dconditional)), "moving-code net jet must cancel both code terms")
    zero(add(dconditional, scale(-1, djoint)), "fixed RIGHT dimension net and joint entropy jets coincide")
    return {
        "blocks": [[[str(entry) for entry in row] for row in matrix] for matrix in blocks],
        "nonzero_commutator": [[str(entry) for entry in row] for row in commutator],
        "eigenvalues": [[str(value) for value in pair] for pair in eigenvalues],
        "eigenjets": [[str(value) for value in pair] for pair in eigenjets],
        "q": list(map(str, q)), "dq": list(map(str, dq)),
        "mu": list(map(str, mu)), "dmu": list(map(str, dmu)),
        "code_motion_in_each_natural_jet": str(code_motion),
        "exact_value_and_first_jet_checks": True,
        "minimum_size": "three blocks on RIGHT2; two blocks summing to I2/2 necessarily commute",
    }, {"cost": cost, "full_gain": full_gain, "posterior_gain": posterior,
        "conditional_entropy": conditional, "dcost": dcost, "dfull_gain": dfull,
        "dposterior_gain": dposterior, "dconditional_entropy": dconditional}


def mean_exponential_control():
    q = (F(1, 2), F(1, 4), F(1, 4))
    posterior_spectra = ((F(1, 2), F(1, 2)), (F(1), F(0)), (F(0), F(1)))
    blocks = tuple(tuple(probability * value for value in spectrum)
                   for probability, spectrum in zip(q, posterior_spectra))
    require(tuple(sum(pair[i] for pair in blocks) for i in range(2)) == (F(1, 2), F(1, 2)),
            "mean-exponential control has the same intrinsic RIGHT prior")
    # Derive each conditional mean D(rho_gamma||I2/2), keeping the pure
    # posteriors' exact zero eigenvalues out of finite logarithms.
    mean_gains = tuple(add(*(scale(value, logarithm(2 * value))
                            for value in spectrum if value))
                       for spectrum in posterior_spectra)
    require(mean_gains == ({}, logarithm(F(2)), logarithm(F(2))),
            "exact conditional mean gain values before exponentiation")
    mean_gain_exponentials = tuple(F(1) if not gain else F(2) for gain in mean_gains)
    wrong_weights = tuple(weight * ratio for weight, ratio in zip(q, mean_gain_exponentials))
    require(wrong_weights == (F(1, 2),) * 3, "conditional mean inserted inside exponential changes the weights")
    wrong_law = tuple(weight / sum(wrong_weights) for weight in wrong_weights)
    require(wrong_law == (F(1, 3),) * 3 and wrong_law != q,
            "conditional mean-gain weights do not reproduce the true pointer law")
    fine_weights = []
    label_only_weights = []
    for probability, pair in zip(q, blocks):
        row, label_row = [], []
        for value in pair:
            reference = probability / 2
            likelihood = value / reference  # zero eigenvalues have zero weight, no log needed.
            row.append(reference * likelihood)
            label_row.append(probability * likelihood)
        fine_weights.append(tuple(row))
        label_only_weights.append(tuple(label_row))
    require(tuple(fine_weights) == blocks and sum(sum(row) for row in fine_weights) == 1,
            "fine matching reference-code weights recover the true complete eigenleaf probabilities")
    require(tuple(label_only_weights) == tuple(tuple(2 * x for x in row) for row in blocks),
            "label-only costs leave the explicit common RIGHT-dimension normalizer")
    return {"q_equals_mu": list(map(str, q)), "wrong_unnormalized_weights": list(map(str, wrong_weights)),
            "wrong_normalized_pointer_law": list(map(str, wrong_law)),
            "correct_fine_eigenleaf_weights": [[str(x) for x in row] for row in fine_weights],
            "label_only_fine_weight_sum": str(sum(sum(row) for row in label_only_weights))}


def golden_pair_control():
    # Exact identities: q(0|k)=p^2,q(1|k)=p; mu_port=(p,p^2).
    # Hence log_phi(q1/q0)=1 and the scalar log-likelihood gain difference=2.
    def golden_product(left, right):
        # a+b*p with p^2=1-p; all coefficients are exact rationals.
        a, b = left
        c, d = right
        return a * c + b * d, a * d + b * c - b * d
    p, phi, one = (F(0), F(1)), (F(1), F(1)), (F(1), F(0))
    p2 = golden_product(p, p)
    require(golden_product(p, phi) == one and golden_product(p2, phi) == p,
            "exact Golden q1/q0=phi, with p^2+p=1")
    require(golden_product(p, p) == p2 and golden_product(p2, phi) == p,
            "exact scalar port likelihood ratios are p and phi")
    dcost, log_probability_ratio, dposterior_gain = F(1), F(1), F(0)
    amplitude_info = dcost + log_probability_ratio / 2
    scalar_info = dcost + log_probability_ratio
    require(amplitude_info == F(3, 2) and scalar_info == 2,
            "original Golden pair absolute amplitude/scalar Info requirements")
    require(amplitude_info - dcost == F(1, 2) and scalar_info - dcost == 1,
            "distinguish Delta Info from Delta(Info-Cost)")
    require(dposterior_gain != amplitude_info and dposterior_gain != scalar_info,
            "identical conditional RIGHT posteriors do not supply the required branch Info difference")
    standalone_info_minus_cost = dposterior_gain - dcost
    amplitude_extra = amplitude_info - dcost - standalone_info_minus_cost
    scalar_extra = scalar_info - dcost - standalone_info_minus_cost
    marker_extra = -standalone_info_minus_cost
    require((amplitude_extra, scalar_extra, marker_extra) == (F(3, 2), F(2), F(1)),
            "extra ledger required on top of standalone port Cost minus RIGHT gain")
    return {"log_phi_q1_over_q0": str(log_probability_ratio), "Delta_Cost": str(dcost),
            "Delta_conditional_RIGHT_gain": str(dposterior_gain),
            "required_Delta_Info_amplitude": str(amplitude_info), "required_Delta_Info_scalar": str(scalar_info),
            "required_Delta_Info_minus_Cost_amplitude": str(amplitude_info - dcost),
            "required_Delta_Info_minus_Cost_scalar": str(scalar_info - dcost),
            "standalone_Delta_RIGHT_gain_minus_port_Cost": str(standalone_info_minus_cost),
            "required_extra_Delta_Info_minus_Cost_amplitude": str(amplitude_extra),
            "required_extra_Delta_Info_minus_Cost_scalar": str(scalar_extra),
            "required_extra_Delta_Info_minus_Cost_marker": str(marker_extra),
            "actual_scalar_port_log_likelihood_Delta": "2"}


def actual_source_transport():
    path = ROOT / (PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json")
    certificate = json.loads(path.read_text(encoding="utf-8"))
    require(certificate["status"] == "PASS"
            and certificate["complete_normalization"]["active_fine_labels"] == 64
            and certificate["complete_normalization"]["exact_Walsh_dark_labels"] == 64
            and certificate["support"]["every_active_posterior_rank"] == 128
            and certificate["support"]["probability_or_eigenvalue_floor"] is False,
            "accepted actual full-fine support contract")
    positive = certificate["linear_coefficients"]["wrong_omitted_conditional_normalizer_phi"]
    lower, upper = F.from_float(positive[0]), F.from_float(positive[1])
    require(0 < lower <= upper, "pinned source interval is strictly positive")
    net_lower, net_upper = -upper, -lower
    require(F.from_float(float(net_lower)) == net_lower
            and F.from_float(float(net_upper)) == net_upper, "negation is exact at the stored dyadic endpoints")
    require(net_lower <= net_upper < 0, "actual conditional code/gain net source strictly negative")
    return {"formula": "h1-i1=-(i1-h1)", "prior_wrong_unconditional_interval_phi": positive,
            "conditional_net_interval_phi": [float(net_lower), float(net_upper)],
            "exact_dyadic_endpoints": [str(net_lower), str(net_upper)],
            "matrix_replay_performed": False,
            "inherited_arithmetic_premise": certificate["arithmetic_premise"]}


def decimal_supplement(expressions):
    with localcontext() as context:
        context.prec = 65
        log_phi = ((Decimal(1) + Decimal(5).sqrt()) / 2).ln()
        def evaluate(expression):
            result = Decimal(0)
            for key, value in expression.items():
                coefficient = Decimal(value.numerator) / Decimal(value.denominator)
                result += coefficient * (Decimal(1) if key == "constant" else Decimal(key).ln())
            return str(result / log_phi)
        return {key: evaluate(value) for key, value in expressions.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutate", choices=("omit-moving-reference", "omit-log-dimension"))
    arguments = parser.parse_args()
    for path, expected in PINS.items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected,
                "immutable owner changed: " + path)
    fixture, expressions = rational_quantum_fixture(arguments.mutate)
    report = {
        "status": "PASS", "arithmetic": "stdlib Fraction matrices and exact rational prime-log coefficient identities",
        "fixture_scope": "small noncommuting quantum ledger, not a native replacement instrument or selected code",
        "identities": ["D(Omega||M_mu)=D(q||mu)+I(R:Y)",
                       "E[-log_phi mu]-D_phi(Omega||M_mu)=H_phi(Y|R)",
                       "E[-log_phi M_mu]-D_phi(Omega||M_mu)=S_phi(Omega)",
                       "-log_phi M_mu=-log_phi mu+log_phi RIGHT_dimension"],
        "noncommuting_fixture": fixture, "decimal_supplement_phi_not_used_for_proof": decimal_supplement(expressions),
        "mean_inside_exponential_counterexample": mean_exponential_control(),
        "original_Golden_pair_control": golden_pair_control(),
        "actual_primary_source_transport": actual_source_transport(),
        "negative_controls": ["omitting either moving-code term changes the net source by nonzero 1/(15 ln(phi))",
                              "conditional mean gain inside a branch exponential changes the actual probabilities",
                              "full operator reference cost includes the RIGHT-dimension constant"],
        "mutation_hooks": ["--mutate omit-moving-reference", "--mutate omit-log-dimension"],
        "complete_code_selected": False, "Book_absolute_amplitude_binding_proved": False,
        "spectral_RIGHT_read_admitted": False, "work_or_preparation_cost_removed": False,
        "source_sha256": PINS,
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
