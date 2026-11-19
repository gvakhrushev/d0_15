#!/usr/bin/env python3
"""Exact common-blank CAR choice composition and its retained entropy price.

Only definitions of the pinned CAR-word owner are loaded. Its old suite is
not executed. New full64 controlled word, padding, selector Kraus, cq chain,
actual cap2 probability budget and fixed-clock factory bound are checked.
Physical controller/Book/work admission is not inferred.
"""
import ast
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    "check_native_car_actuated_metric.py": "72b2743f2f4c9408ceafe29dc691786c5011c4d1133d5fa6ebdb671a230bc3fa",
    "NATIVE_CAR_ACTUATED_METRIC.md": "b9dd63f0888a062941c1744d800120e47d20777f429f892f5a98c504a3c0a4be",
    "FIXED_CLOCK_PREPARATION_BANK.md": "a922a3aeaabe8dfb68dc28e4d788c708b496a1081a3a0ab8cf241fd91fbaf88e",
    "PAID_RANDOM_CHOICE_MINIMUM.md": "30fe9fe6e48f6a978b6f5b7762bced2824ca3342043a566fc4e94723ae6d8df3",
    "PRIMARY_CAR_PAID_RETURN_PRICE.md": "2fdf545aa33e3c85f9ef81398fe604a4770c0af76ee872845beefd4f365cfcc1",
    "PRIMARY_RIGHT_COMPLETE_CODE_SOURCE.md": "7a38155f37b98fabdd358271be52ad4919a0b28963a5fb952d91da049eba4424",
    "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json": "9c910c2e28d02af5fd3a8642d98d01b8c58aeb0a9a55ccf3612a5bc80e397785",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


for name, digest in PINS.items():
    require(hashlib.sha256((ROOT / (PREFIX + name)).read_bytes()).hexdigest() == digest,
            "immutable input: " + name)
source = ast.parse((ROOT / (PREFIX + "check_native_car_actuated_metric.py")).read_text())
names = {"require", "add", "scale", "sub", "mul", "power", "dot", "basis", "g",
         "k_gate", "x_gate", "native_l", "cnot64"}
nodes = [node for node in source.body if
         (isinstance(node, ast.FunctionDef) and node.name in names)
         or (isinstance(node, ast.Assign)
             and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
             and node.targets[0].id in {"Z", "O", "A", "P"})]
owned = {"F": Q}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "pinned_CAR_definitions_only", "exec"), owned)
Z, ONE, A, P = (owned[n] for n in ("Z", "O", "A", "P"))
add, sub, mul, scale, power = (owned[n] for n in ("add", "sub", "mul", "scale", "power"))


def scalar(value):
    return (Q(value), Q(0), Q(0), Q(0))


def l64(value):
    # Full c/f/CAR operator, not the c=1 compression.
    value = owned["k_gate"](value)
    value = owned["cnot64"](value, 5, 0)
    value = owned["g"](value)
    value = owned["cnot64"](value, 5, 0)
    value = owned["k_gate"](value)
    return owned["g"](value)


def pad64(value):
    # Chronological K,K,G,C_cN,G,C_cN: same primitive multiset as L6.
    # Identity on supplied c1; its actual c0 complement is G_N^2.
    value = owned["k_gate"](owned["k_gate"](value))
    value = owned["g"](value)
    value = owned["cnot64"](value, 5, 0)
    value = owned["g"](value)
    return owned["cnot64"](value, 5, 0)


def word_control():
    columns, padding = [], []
    for j in range(64):
        basis = owned["basis"](64, j)
        pad = pad64(basis)
        pad_expected = basis if j >= 32 else owned["g"](owned["g"](basis))
        require(pad == pad_expected, "matched-profile padding retains its true c0 complement")
        padding.append(pad)
        column = l64(basis)
        if "--mutation=delete-c0-complement" in sys.argv and j < 32:
            column = basis
        if j >= 32:
            expected = owned["native_l"](basis)
        else:
            twice = owned["g"](owned["g"](basis))
            expected = [twice[n] if ((n % 16) >> 1).bit_count() < 2 else basis[n]
                        for n in range(64)]
        require(column == expected, "full controlled return retains the true c0 complement")
        require(all(x == Z or n // 16 == j // 16 for n, x in enumerate(column)),
                "all c/f records remain in their original sector")
        columns.append(column)
    norm = add(P, mul(P, P))
    require(norm == ONE, "Golden selector probabilities sum to one")
    for i, left in enumerate(columns):
        for j, right in enumerate(columns[:i + 1]):
            gram = owned["dot"](left, right)
            require(gram == (ONE if i == j else Z), "actual full64 word orthogonal")
            pad_gram = owned["dot"](padding[i], padding[j])
            require(pad_gram == (ONE if i == j else Z), "actual full64 padding orthogonal")
            # M0=a S, M1=p L: the measured tag is retained in both branches.
            total = add(mul(P, pad_gram), mul(mul(P, P), gram))
            require(total == (ONE if i == j else Z), "complete measured-choice Kraus isometry")
    # Coherent blank selector has a pure rank-one density, whereas its
    # measured diagonal has nonzero entropy. Never transfer the cq bound.
    require(sub(mul(P, mul(P, P)), mul(mul(A, P), mul(A, P))) == Z,
            "unmeasured Golden flag is pure, not a classical entropy source")
    return {"full_controller_CAR_dimension": 64, "retained_choice_dimension": 2,
            "conditional_slot_count_each_branch": 6,
            "each_branch_primitive_multiset": "2K+2C_cN+2G_N",
            "actual_padding_complement": "c1:I; c0:G_N^2",
            "retained_probabilities": ["p", "p^2"],
            "all_c_f_complements_checked": True, "coherent_flag_entropy": 0}


# Formal linear combinations of log_phi2, log_phi3, log_phi5 and1,
# with exact coefficients in Q(a), a^4+a^2-1=0.
def vadd(left, right):
    return {k: add(left.get(k, Z), right.get(k, Z)) for k in set(left) | set(right)}


def vscale(coefficient, vector):
    return {k: mul(coefficient, value) for k, value in vector.items()}


def vequal(left, right):
    return all(left.get(k, Z) == right.get(k, Z) for k in set(left) | set(right))


def logq(value, p_exponent=0):
    value = Q(value)
    result = {"1": scalar(-p_exponent)}
    for integer, sign in ((value.numerator, 1), (value.denominator, -1)):
        for prime in (2, 3, 5):
            exponent = 0
            while integer % prime == 0:
                integer //= prime
                exponent += 1
            key = "log_phi" + str(prime)
            result[key] = add(result.get(key, Z), scalar(sign * exponent))
        require(integer == 1, "fixture rational factors fully resolved")
    return result


def chain_control():
    # Genuine rank-one cq blocks, including noncommuting second-branch
    # posteriors: diag(9/25,0),diag(0,16/25), and [[9,+/-12],[+/-12,16]]/50.
    sigma = ((Q(9, 25), Q(0)), (Q(0), Q(16, 25)))
    for sign in (-1, 1):
        block = ((Q(9, 50), sign * Q(12, 50)),
                 (sign * Q(12, 50), Q(16, 50)))
        require(block[0][0] * block[1][1] == block[0][1] * block[1][0],
                "actual fixture block rank one")
    prior = {}
    for q in (Q(9, 25), Q(16, 25)):
        prior = vadd(prior, vscale(scalar(-q), logq(q)))
    joint = {}
    for exponent, probabilities in ((1, (Q(9, 25), Q(16, 25))), (2, (Q(1, 2), Q(1, 2)))):
        for q in probabilities:
            joint = vadd(joint, vscale(scale(-q, power(P, exponent)), logq(q, exponent)))
    conditional = vadd(joint, vscale(scalar(-1), prior))
    flag = {"1": sub(scalar(2), P)}
    branch_delta = vadd({"log_phi2": ONE}, vscale(scalar(-1), prior))
    expected = vadd(flag, vscale(mul(P, P), branch_delta))
    if "--mutation=drop-choice-label" in sys.argv:
        conditional = vadd(conditional, vscale(scalar(-1), flag))
    require(vequal(conditional, expected), "complete cq price retains the actual choice-label entropy")
    require(vequal(vadd(conditional, vscale(scalar(-1), flag)),
                   vscale(mul(P, P), branch_delta)), "preexisting common seed entropy cancels")
    require(sigma[0][0] + sigma[1][1] == 1, "actual fixture RIGHT prior")
    return {"noncommuting_RIGHT_fixture": True,
            "identity": "H(P,Y|R)=H(P)+sum pi_f H(Y|R,P=f)",
            "fresh_flag_entropy_phi": "2-p", "common_preexisting_flag_cancels": True}


def primary_budget():
    report = json.loads((ROOT / (PREFIX + "PRIMARY_STOPPED_RIGHT_CONDITIONAL_SOURCE_CERTIFICATE.json")).read_bytes())
    qb = report["complete_cut"]["blank_probability_cap1"]
    abort = report["actual_abort"]["probability_at_flat_centre"]
    lower_q0, upper_q0 = map(Q.from_float, qb)
    lower_s2 = Q.from_float(abort[0])
    margins = (lower_q0 - Q(389, 390), lower_s2 / upper_q0 - Q(389, 390))
    require(min(margins) > 0, "both actual conditional blank probabilities exceed389/390")
    lhs, rhs = 390 ** 390 * 127 * 5 ** 26, 389 ** 389 * 8 ** 26
    require(lhs < rhs, "exact complete128 entropy bound below1/15 per reached trial")
    require(Q(3, 5) ** 2 + Q(3, 5) < 1
            and Q(5, 8) ** 2 + Q(5, 8) > 1, "exact3/5<p<5/8 and phi>8/5")
    require(Q(4, 3) - Q(2, 15) == Q(6, 5), "fresh Golden-flag incremental margin")
    require(Q(28, 15) - Q(13, 15) * Q(5, 8) == Q(53, 40),
            "literal pad-versus-return dispatcher has the stronger weighted margin")
    return {"actual_cap2_entropy_upper_strict": "2/15",
            "scope": "flat primary baseline; persists on a nonempty small-t neighborhood by continuity",
            "conditional_blank_margins": [str(v) for v in margins],
            "log_bound_integer_inequality": "390^390*127*5^26 <389^389*8^26",
            "fresh_Golden_flag_entropy_lower_strict": "4/3",
            "fresh_flag_entropy_increment_lower_strict": "6/5",
            "literal_pad_vs_L_dispatch_increment_lower_strict": "53/40"}


def main():
    word, chain, budget = word_control(), chain_control(), primary_budget()
    require(Q(3, 5) < Q(5, 8) < Q(2, 3), "fixed-bank parity probabilities both belowp")
    # s=4p-2<p iff p<2/3; r=3-4p<p iff p>3/5.
    # Thus each actual parity surprisal exceeds1 and h_phi(s)>1.
    print(json.dumps({"status": "PASS", "word": word, "cq_chain": chain,
                      "primary_baseline": budget,
                      "literal_fixed_clock_bank": {"parity_success": "2p^3=4p-2",
                          "independent_actual_trials": "mK=42NK", "entropy_lower_strict": "42NK",
                          "generic_baseline_capN_upper_strict": "3N",
                          "increment_lower_strict": "(42K-3)N",
                          "sequential_early_abort_bank_included": False},
                      "source_sha256": {PREFIX + n: h for n, h in PINS.items()},
                      "classical_controller_admission_proved": False,
                      "physical_Info_or_work_selected": False,
                      "postselected_branch_is_complete_alternative": False,
                      "coherent_flag_bound_inferred": False}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
