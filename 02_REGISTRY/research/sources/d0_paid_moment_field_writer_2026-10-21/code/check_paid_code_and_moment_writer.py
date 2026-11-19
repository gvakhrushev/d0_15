#!/usr/bin/env python3
"""Narrow exact controls for code writing, coherent rows and full CQ ledgers.

No old native factories, primary roots, polynomial jets or geometry suites
are replayed. All arithmetic in these bounded controls is exact.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cx(bits, c, t):
    answer = list(bits)
    answer[t] ^= answer[c]
    return tuple(answer)


def ccx(bits, a, b, t):
    answer = list(bits)
    answer[t] ^= answer[a] & answer[b]
    return tuple(answer)


def code_cell(bits, bit):
    word = ((0, 1), (1, 2)) if bit else ((1, 2), (0, 1))
    for c, t in word:
        bits = cx(bits, c, t)
    return bits


def code_controls():
    columns = tuple(itertools.product((0, 1), repeat=3))
    for bit in (0, 1):
        image = tuple(code_cell(column, bit) for column in columns)
        require(f"code_{bit}_full_permutation", len(set(image)) == 8)
        for column, output in zip(columns, image):
            c, u, b = column
            expected = (c, u ^ c, b ^ u ^ (c if bit else 0))
            require(f"code_{bit}_column_{column}", output == expected)
    require("code_common_zero_controller_complement",
            all(code_cell(column, 0) == code_cell(column, 1)
                for column in columns if column[0] == 0))
    require("code_actual_blank_outputs",
            code_cell((1, 0, 0), 0) == (1, 1, 0)
            and code_cell((1, 0, 0), 1) == (1, 1, 1))
    inventory = Counter(((0, 1), (1, 2)))
    require("same_address_inventory",
            inventory == Counter(((1, 2), (0, 1))))
    d, cost_list, tapes = 4, [], []
    for code in range(1 << d):
        bits = (1,) + (0,) * (2 * d)
        tape, cost = [], 0
        for j in range(d):
            a, b = (0, 1 + j), (1 + j, 1 + d + j)
            word = (a, b) if (code >> j) & 1 else (b, a)
            for gate in word:
                bits = cx(bits, *gate)
                tape.append(gate)
                cost += (2 * j + 3) if gate == a else (5 * j + 7)
        require(f"written_code_{code}",
                sum(bits[1 + d + j] << j for j in range(d)) == code)
        require(f"retained_real_work_{code}", bits[:1+d] == (1,) * (1 + d))
        cost_list.append(cost)
        tapes.append(tape)
    require("heterogeneous_address_cost_common", len(set(cost_list)) == 1)
    require("raw_ordered_words_are_distinct", len({tuple(t) for t in tapes}) == 16)
    require("all_words_same_inventory", all(Counter(t) == Counter(tapes[0]) for t in tapes))
    return {"full_cell_columns": 8, "four_bit_words": 16,
            "heterogeneous_cost": cost_list[0], "instructions_retained": True}


def fredkin(bits):
    bits = cx(bits, 1, 2)
    bits = ccx(bits, 0, 2, 1)
    return cx(bits, 1, 2)


def selection_controls():
    for c, x, y in itertools.product((0, 1), repeat=3):
        expected = (c, y, x) if c else (c, x, y)
        require(f"fredkin_full_column_{c}{x}{y}", fredkin((c, x, y)) == expected)
    for code in range(4):
        for row_tuple in itertools.product((0, 1), repeat=4):
            for original_output in (0, 1):
                rows, output = list(row_tuple), original_output
                flags = []
                for j in range(4):
                    flag = int(code == j)
                    flags.append(flag)
                    _, rows[j], output = fredkin((flag, rows[j], output))
                wanted = list(row_tuple)
                wanted[code] = original_output
                require(f"full_selector_{code}_{row_tuple}_{original_output}",
                        rows == wanted and output == row_tuple[code]
                        and sum(flags) == 1)
    return {"fixed_rows": 4, "full_payload_cases": 128,
            "unknown_controlled_operation": False}


def threshold_controls():
    tested = 0
    for m in range(6):
        n = 1 << m
        for code in range(n + 1):
            amplitudes = {}
            for label in range(n):
                comparison = int(label < code)
                sign = 2 * comparison - 1
                # All label/comparison/code records remain orthogonal work.
                amplitudes[(label, code, comparison, 0)] = 1
                amplitudes[(label, code, comparison, 1)] = sign
            norm = sum(v * v for v in amplitudes.values())
            overlap = sum(v * amplitudes[(r, k, b, 1 - car)]
                          for (r, k, b, car), v in amplitudes.items())
            mean = F(overlap, norm)
            require(f"threshold_exact_{m}_{code}", mean == F(2 * code, n) - 1)
            require(f"threshold_complete_purity_{m}_{code}", norm == 2 * n)
            if 0 < code < n:
                require(f"active_pair_is_not_full_work_{m}_{code}",
                        (1 + mean * mean) / 2 < 1)
            tested += 1
    return {"precisions": list(range(6)), "all_endpoint_codes": tested,
            "moment": "2*k/2^m-1", "label_reading": False}


def prime_logs_integer(n):
    result, prime = {}, 2
    while prime * prime <= n:
        while n % prime == 0:
            result[prime] = result.get(prime, 0) + 1
            n //= prime
        prime += 1
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def log_form(q):
    answer = defaultdict(F)
    for prime, power in prime_logs_integer(q.numerator).items():
        answer[prime] += power
    for prime, power in prime_logs_integer(q.denominator).items():
        answer[prime] -= power
    return {p: x for p, x in answer.items() if x}


def entropy(probabilities):
    answer = defaultdict(F)
    for q in probabilities:
        if q:
            for p, coefficient in log_form(q).items():
                answer[p] -= q * coefficient
    return {p: x for p, x in answer.items() if x}


def lincomb(*terms):
    answer = defaultdict(F)
    for factor, vector in terms:
        for prime, coefficient in vector.items():
            answer[prime] += factor * coefficient
    return {p: x for p, x in answer.items() if x}


def coherent_rows(code):
    # Two exact rational catalogue rows, with common eight-label herald.
    # Acceptance label<4 has probability1/2 for EACH row. Within acceptance,
    # the plus-kind counts are1 and2. Kind is never measured.
    plus_counts = (1, 2)
    initial = {}
    for l0, l1, x0, x1 in itertools.product(range(4), range(4), (0, 1), (0, 1)):
        s0 = 1 if l0 < plus_counts[0] else -1
        s1 = 1 if l1 < plus_counts[1] else -1
        rows, out = [x0, x1], 0
        for j in range(2):
            _, rows[j], out = fredkin((int(code == j), rows[j], out))
        key = (code, l0, l1, rows[0], rows[1], out)
        initial[key] = (s0 ** x0) * (s1 ** x1)
    require(f"coherent_rows_{code}_norm", sum(v*v for v in initial.values()) == 64)
    # Apply the genuine fixed H test on the selected pair. Its numerator
    # is integer; denominator gains sqrt(2). No old row/work is traced away.
    final = defaultdict(int)
    for key, value in initial.items():
        for output in (0, 1):
            final[key[:-1] + (output,)] += value * (-1) ** (key[-1] * output)
    final = {key: value for key, value in final.items() if value}
    denominator = sum(value * value for value in final.values())
    require(f"coherent_rows_{code}_complete_unitary", denominator == 128)
    probability = F(sum(v*v for key, v in final.items() if key[-1] == 1), denominator)
    require(f"coherent_rows_{code}_actual_report", probability == 1 - F(plus_counts[code], 4))
    require(f"coherent_rows_{code}_old_output_retained",
            all(key[3 + code] == 0 for key in final))
    return probability


def ledger_controls():
    reports = [coherent_rows(code) for code in range(2)]
    # Literal rational herald fixture: both row accepts=1/2; a separate
    # fixed3/4 herald after the paid code block supplies a late abort.
    # This tests the new composition, not the old Golden factory proof.
    tape = (F(1, 2), F(1, 4), F(1, 16), F(3, 16))
    gamma = tape[-1]
    require("complete_tape_normalization", sum(tape) == 1)
    code_cost = 8
    costs = (2, 5, 8 + code_cost, 11 + code_cost)
    expected_cost = sum(q * c for q, c in zip(tape, costs))
    for k, r in enumerate(reports):
        joint = (*tape[:-1], gamma * (1 - r), gamma * r)
        require(f"complete_not_postselected_{k}", sum(joint) == 1)
        require(f"exact_complete_entropy_chain_{k}",
                entropy(joint) == lincomb((1, entropy(tape)),
                                        (gamma, entropy((1-r, r)))))
        require(f"paid_full_baseline_{k}",
                sum(q*c for q, c in zip(tape, costs)) == expected_cost)
    # A SINGLE fixed uniform-code programme reads code only on completion.
    uniform_joint = list(tape[:-1])
    for r in reports:
        uniform_joint.extend((gamma * (1-r) / 2, gamma * r / 2))
    wanted = lincomb((1, entropy(tape)), (gamma, log_form(F(2))),
                     (gamma / 2, entropy((1-reports[0], reports[0]))),
                     (gamma / 2, entropy((1-reports[1], reports[1]))))
    require("single_fixed_uniform_code_full_entropy", entropy(uniform_joint) == wanted)
    require("single_fixed_both_nodes_reachable", gamma / 2 > 0)
    # Reading code on abort changes the declared instrument and entropy.
    early_read_joint = [q / 2 for q in tape[:-1] for _ in range(2)]
    early_read_joint += uniform_joint[len(tape)-1:]
    require("hostile_early_code_reading_has_real_entropy",
            lincomb((1, entropy(early_read_joint)), (-1, wanted))
            == lincomb((1-gamma, log_form(F(2)))))
    # Reading an internal fair sign before an AND report adds real entropy.
    # K0,R0=1/2; K1,R0=1/4; K1,R1=1/4; P(K1|R0)=1/3.
    premature = entropy((F(1, 2), F(1, 4), F(1, 4)))
    final_only = entropy((F(3, 4), F(1, 4)))
    extra = lincomb((1, premature), (-1, final_only))
    require("hostile_kind_reading_changes_full_ledger",
            extra == lincomb((F(3, 4), entropy((F(1, 3), F(2, 3))))) and bool(extra))
    return {"actual_selected_report_probabilities": [str(r) for r in reports],
            "complete_fixture_tape": [str(q) for q in tape],
            "gamma": str(gamma), "expected_cost_including_aborts": str(expected_cost),
            "uniform_code_probability_each": str(gamma / 2),
            "entropy_checks": "exact rational coefficients of prime logarithms"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pin_bytes = (here / "SOURCE_PINS.json").read_bytes()
    pins = json.loads(pin_bytes)
    for item in pins["sources"]:
        source_ref = item.get("source_ref", pins["source_ref"])
        raw = subprocess.check_output(["git", "show", source_ref + ":" + item["path"]], cwd=args.repo)
        require("historical_pin:" + item["path"], digest(raw) == item["sha256"])
    receipt = {"status": "PASS", "source_ref": pins["source_ref"],
               "scope": "Exact code/row/retained-record controls, not old geometry or physical selection",
               "proof_sha256": digest((here / "PAID_CODE_AND_MOMENT_WRITER.md").read_bytes()),
               "checker_sha256": digest(Path(__file__).read_bytes()),
               "pins_sha256": digest(pin_bytes),
               "code": code_controls(), "selection": selection_controls(),
               "threshold": threshold_controls(), "ledger": ledger_controls(),
               "physical_GR_closed": False, "checks": CHECKS, "check_count": len(CHECKS)}
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
