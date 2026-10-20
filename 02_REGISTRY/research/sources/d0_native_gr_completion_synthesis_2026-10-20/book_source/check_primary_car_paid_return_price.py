#!/usr/bin/env python3
"""Exact native norm/entropy budget and matched-code work controls.

No predecessor main, numerical matrix spectrum, logarithm approximation or
physical work assignment is used.  The finite stopping example is a ledger
control, not a replacement for the original native instrument.
"""

import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    PREFIX + "check_primary_car_preparation_source.py":
        "889053f6da84501769d23ab84186c2189e6c026414db623919f4934098fb6c34",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py":
        "c67285c7469db49ff61f3e52597d0bcc6aad991ec1f7af025d6daeb065a43edf",
    PREFIX + "NATIVE_CAR_ACTUATED_METRIC.md":
        "b9dd63f0888a062941c1744d800120e47d20777f429f892f5a98c504a3c0a4be",
    PREFIX + "PRIMARY_CAR_RECORD_PRICE_SOURCE.md":
        "15a058cb96f5fb51d1f086a3e65459d7cfb75d0ffe69761537c8bba46ac76111",
    PREFIX + "PRIMARY_RIGHT_COMPLETE_CODE_SOURCE.md":
        "7a38155f37b98fabdd358271be52ad4919a0b28963a5fb952d91da049eba4424",
    PREFIX + "PRIMARY_RIGHT_COMPLETE_CODE_SOURCE_CERTIFICATE.json":
        "d8fea994bdf698e69a44c2b1d8aae1094d9b199a1c36aded0e267399a1d2c1c9",
    PREFIX + "check_primary_right_complete_code_source.py":
        "178be2f98dd0c6a5263130ed11aa21b548812a99856a121afe43f9193c27c164",
    PREFIX + "GOLDEN_EXACT_DETECTOR.md":
        "d33c9c2cb2322e381723f481eb1fcf58058fd05ad88eda92c5597c026d02eb77",
}


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


def definitions(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / (PREFIX + filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def native_norm_budget(preparation, mutation):
    counts = preparation.actual_counts(ROOT)
    require(len(counts) == 256 and sum(counts) == 10946 and max(counts) == 78,
            "actual original cost20 full-site density")
    rho_max = F(256 * max(counts), sum(counts))
    require(rho_max == F(768, 421), "same actual density maximum")
    gamma = [F(1, 2), F(2), F(1), F(1)]
    if mutation == "wrong-leg-norm":
        gamma[1] = F(1)
    identity = preparation.eye(16)
    zero = preparation.mscale(identity, 0)
    for creation, squared_norm in zip(preparation.ROLE_CREATION, gamma):
        adjoint = preparation.transpose(creation)
        product = preparation.mmul(adjoint, creation)
        require(preparation.mmul(creation, creation) == zero,
                "literal full16 role creation is nilpotent")
        require(preparation.madd(product, preparation.mmul(creation, adjoint))
                == preparation.mscale(identity, squared_norm),
                "literal full16 role norm uses the actual positive REST pairing")
        require(preparation.mmul(product, product) == preparation.mscale(product, squared_norm)
                and any(product[i][i] for i in range(16)),
                "CAR norm is exactly sqrt(gamma), with no scalar-grade compression")
    require(F(21, 34) ** 2 + F(21, 34) - 1 < 0,
            "positive Golden root p is greater than21/34")
    require(F(17, 12) ** 2 > 2, "sqrt2 less than17/12")
    l_squared_upper = F(17, 2) + 6 * F(17, 12)
    require(l_squared_upper == 17, "full sum-of-role-norms bound")
    # epsilon=p^2 h^2/64; ||D||^2<=16 p^6 rho_max L^2/h^2.
    epsilon_coefficient = F(1, 64)
    dirac_coefficient = F(4) ** 2
    require(epsilon_coefficient * dirac_coefficient == F(1, 4),
            "both true-adjoint legs retained before squaring the Dirac bound")
    bound = F(13, 34) ** 4 * rho_max * l_squared_upper / 4
    require(bound == F(342732, 2068373) and bound < F(1, 6),
            "strict actual full-D nonblank probability budget")
    require(bound.denominator - 6 * bound.numerator == 11981,
            "nonempty rational slack below1/6")
    require(F(8, 5) ** 2 - F(8, 5) - 1 < 0,
            "phi greater than8/5")
    left, right = 6 ** 6 * 127 * 5 ** 13, 8 ** 18
    require(left == 7233046875000000 and right == 18014398509481984 and left < right,
            "strict entropy upper bound3 without floating logarithms")
    return {"sites": len(counts), "total_FR_words": sum(counts), "max_count": max(counts),
            "rho_max": str(rho_max), "full_CAR_dimension": 16,
            "squared_role_norms": list(map(str, gamma)),
            "nonblank_rational_upper": str(bound), "probability_budget": "strictly below1/6",
            "entropy_bound_phi": "strictly below3 per original complete trial",
            "entropy_integer_witness": {"left": str(left), "right": str(right)}}


def stopped_chain_control(logs):
    # Uniform classical reference R2. Conditional trial probabilities differ
    # with R; stop on first success, cap2, retaining the final FF abort.
    rates = (F(1, 4), F(1, 2))
    probabilities = [(r, (1-r)*r, (1-r)**2) for r in rates]
    for row in probabilities:
        require(sum(row) == 1, "complete stopped success and abort leaves")

    def entropy(row):
        return logs.add(*(logs.scale(-x, logs.logarithm(x)) for x in row if x))

    conditional_entropy = logs.scale(F(1, 2), logs.add(*(entropy(row) for row in probabilities)))
    chain = logs.add(*(logs.scale(F(1, 2) * (2-r), entropy((r, 1-r))) for r in rates))
    logs.zero(logs.add(conditional_entropy, logs.scale(-1, chain)),
              "complete stopped record conditional entropy chain, including abort")
    # Direct cq entropy minus prior entropy on all six positive eigenlines.
    joint_eigenvalues = [F(1, 2)*x for row in probabilities for x in row]
    direct = logs.add(entropy(joint_eigenvalues), logs.scale(-1, logs.logarithm(2)))
    logs.zero(logs.add(direct, logs.scale(-1, conditional_entropy)),
              "old reference cannot be discarded at the stopping cut")
    expected_trials = sum(F(1, 2) * (2-r) for r in rates)
    require(expected_trials == F(13, 8), "actual full trial count retains neutral failures")
    require(sum(row[2] for row in probabilities) / 2 == F(13, 32),
            "strictly positive retained finite-cap abort mass")
    return {"scope": "small exact chain control, not the original native detector",
            "conditional_leaf_probabilities": [list(map(str, row)) for row in probabilities],
            "expected_trials": str(expected_trials), "retained_abort_mass": "13/32",
            "exact_conditional_entropy_chain": True}


def work_code_control(mutation):
    # A supplied matched code can attach any c to a certain instruction;
    # its code-relative gain is c too. This is not an owned work charge.
    letters = 6
    cost, gain = F(letters), F(letters)
    if mutation == "omit-code-gain":
        gain = F(0)
    require(cost-gain == 0, "known instruction code cost cancels its matching relative gain")
    work = F(0)
    if mutation == "add-code-to-work":
        work += cost
    require(cost-gain+work == 0,
            "coded instruction cannot be added again as uncancelled work")
    return {"literal_compiled_letters_per_return": letters,
            "literal_autonomous_letters_per_return": 18,
            "certain_instruction_matching_code_cost": str(cost),
            "certain_instruction_matching_gain": str(gain),
            "matching_net": str(cost-gain),
            "one_round_sufficient_actual_uncancelled_work_difference": "3",
            "uncancelled_work_lower_bound_proved": False}


def inherited_source():
    source = json.loads((ROOT / (PREFIX + "PRIMARY_RIGHT_COMPLETE_CODE_SOURCE_CERTIFICATE.json")).read_bytes())
    interval = source["actual_primary_source_transport"]["conditional_net_interval_phi"]
    lower, upper = map(F.from_float, interval)
    require(lower <= upper < 0 and source["status"] == "PASS",
            "inherited strict negative primary angle source")
    return {"conditional_net_angle_coefficient_phi": interval,
            "prior_spectral_replay_performed": False,
            "inherited_interval_arithmetic_premise": source["actual_primary_source_transport"]["inherited_arithmetic_premise"],
            "numerical_t_or_uniform_word_bound_proved": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutate", choices=("wrong-leg-norm", "omit-code-gain", "add-code-to-work"))
    args = parser.parse_args()
    for path, expected in PINS.items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected,
                "immutable input: " + path)
    preparation = definitions("owned_preparation_definitions_only", "check_primary_car_preparation_source.py")
    logs = definitions("owned_exact_log_definitions_only", "check_primary_right_complete_code_source.py")
    report = {"status": "PASS", "arithmetic": "exact Fraction/CAR/integer/log-prime identities",
              "native_budget": native_norm_budget(preparation, args.mutate),
              "stopped_chain": stopped_chain_control(logs),
              "code_and_work": work_code_control(args.mutate),
              "inherited_primary_source": inherited_source(),
              "history_budget_scope": "fixed frozen geometry; complete fixed-n tape<3n; deterministic finite-cap stop<3ET ifET>0",
              "native_work_map_or_Book_Info_selected": False,
              "same_complete_initial_controller_reachability_proved": False,
              "refinement_or_metric_source_bound_inferred": False,
              "source_sha256": PINS}
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
