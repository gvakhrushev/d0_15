"""Replay both serial B121 assignments, including the actual occupied WORK fibre."""

from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
sys.path.insert(0, str(PILOT / "open/round121"))
sys.path.insert(0, str(PILOT / "direct/round80/price"))
from check_book03_identity_pair import BOOK03, REPO, actual_words, ne, require
from check_parity_price import a, action, gate_columns, one, p


def prefixes(word, initial):
    states = [initial]
    for gate in word:
        states.append(tuple(action(column, gate, 4) for column in states[-1]))
    return states


def overlap(left, right):
    return sum(amplitude * right.get(row, 0) for row, amplitude in left.items())


def gram(left, right):
    return tuple(overlap(column, other) for column, other in product(left, right))


def period_failures(states, period):
    """First failed slot-isometry test, with phases allowed at the cuts."""
    for phase in range(period):
        calls = range(phase, len(states) - 1, period)
        for first, second in combinations(calls, 2):
            before = gram(states[first], states[second])
            after = gram(states[first + 1], states[second + 1])
            if any(b*b != d*d for b, d in zip(before, after)):
                return [first + 1, second + 1]
    return None


def literal_periods(word):
    return [n for n in range(1, len(word) + 1)
            if all(word[i] == word[i+n] for i in range(len(word) - n))]


def test_serial():
    words = actual_words()
    w0, w1 = words["CX_18"], words["G_Z_G_Z"]
    occupied = tuple({spin:a, spin+4:p} for spin in range(4))
    all_columns = tuple({k:one} for k in range(16))
    require(len(w0) == len(w1) == 18, "Changed B121 length")
    require(all(s == occupied for s in prefixes(w0, occupied)),
            "The comparator must fix occupied PORT=0 at every tick")
    for word in (w0, w1):
        require(prefixes(word, all_columns)[-1] == all_columns,
                "Each block endpoint must be identity on all columns")

    theta = math.acos(math.sqrt((math.sqrt(5) - 1) / 2))
    receipts = {}
    cases = [("W0_W1", w0+w1, 3, 19, 4), ("W1_W0", w1+w0, 1, 33, 3)]
    for label, word, first, second, imperfect_cuts in cases:
        states = prefixes(word, occupied)
        before1, before2 = states[first-1], states[second-1]
        after1, after2 = states[first], states[second]
        require((second-first) % 16 == 0 and before1 == before2 == occupied,
                "The two calls must address the same slot on the same input")
        diagonal = [overlap(x,y) for x,y in zip(after1,after2)]
        require(diagonal == [a]*4, "Wrong outgoing overlap on canonical WORK")
        failures = {n: period_failures(states, n) for n in range(1, 37)}
        admissible = [n for n, conflict in failures.items() if conflict is None]
        literal = literal_periods(word)
        receipts[label] = {
            "occupied_collision_calls": [first, second],
            "outgoing_overlap": "sqrt(p) I4",
            "phase_optimized_prefix_error_lower_bound": 2 * math.sin(theta/(2*imperfect_cuts)),
            "literal_periods_up_to_36": literal,
            "periods_without_pairwise_Gram_magnitude_obstruction_up_to_36": admissible,
            "period_gram_obstruction_first_call_pair": {
                n: pair for n, pair in failures.items() if pair is not None
            },
        }
    return receipts


def test_clean_switch():
    words = actual_words()
    roots = tuple({spin:a, spin+4:p} for spin in range(4))
    k = a+p

    def residue(x):
        return tuple(c % 2 for c in x.coefficients)

    require(residue(k*k) == residue(one) and residue(k) != residue(one),
            "Column-sum factor must be a distinct involutive unit")
    for gate in set(words["G_Z_G_Z"] + words["CX_18"]):
        expected = k if gate.op == "G" else one
        require(all(residue(sum((one*c for _, c in col), 0)) == residue(expected)
                    for col in gate_columns(gate)), "Wrong local residue column sum")
    steady = prefixes(words["CX_18"], roots)
    echo = prefixes(words["G_Z_G_Z"], roots)
    different = []
    for tick, (same, changed) in enumerate(zip(steady, echo)):
        different_at_cut = [
            residue(sum(c.values())) != residue(sum(d.values())) for c, d in zip(same, changed)
        ]
        require(len(set(different_at_cut)) == 1, "Spin column choice changes the residue test")
        if different_at_cut[0]:
            different.append(tick)
    require(different == list(range(1, 10)), "Wrong clean-switch obstruction stages")
    return {"cuts_with_distinct_column_sums_mod_2": different,
            "fixed_program_input_columns": 8, "requires_clean_integral_auxiliary_return": True}


def primary_words():
    owner = ("c6ee5faa6bc0078d78b025499d0724d3add13616:"
             "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md")
    text = subprocess.check_output(["git", "show", owner], cwd=REPO, text=True)
    tag = "7ds RETURN RECORD COMPILER RECEIPT"
    payload = text.split(f"<!-- BEGIN {tag} -->\n")[1].removeprefix("```json\n")
    raw = payload.split(f"\n```\n<!-- END {tag} -->")[0]
    base = json.loads(raw)["literal_words"]["reference31"]
    wires = {0:0, 11:1, 13:2, 14:3}
    retargeted = [
        ne.Gate(item["op"], tuple(wires[wire] for wire in item["wires"]))
        for item in base[24:31] + base[5:16]
    ]
    forward, inverse = tuple(retargeted[:7]), tuple(retargeted[7:])
    return forward+inverse, forward+forward+(ne.Gate("SourceI",(0,2,3)),)*4


def test_primary():
    identity, rotation = primary_words()
    blank = tuple({j:one} for j in range(4))
    all_columns = tuple({j:one} for j in range(16))
    ab, ba = (prefixes(word, blank) for word in (identity+rotation, rotation+identity))
    require(prefixes(identity, all_columns)[-1] == all_columns, "Primary I18 changed")
    require(prefixes(identity+rotation, all_columns)[-1] ==
            prefixes(rotation+identity, all_columns)[-1], "Primary full endpoints disagree")
    require(gram(ab[0], ab[18]) == gram(ab[0], ab[0]), "Primary midpoint of I must fix blank")
    diag = [overlap(x,y) for x,y in zip(ba[0],ba[18])]
    require(diag == [p*p*p]*4, "Primary rotated midpoint cold coefficient changed")
    slots = [4,20]
    for states, expected in ((ab,one), (ba,p*p*p)):
        first, second = slots
        incoming = [overlap(x,y) for x,y in zip(states[first-1],states[second-1])]
        outgoing = [overlap(x,y) for x,y in zip(states[first],states[second])]
        require(incoming == [expected]*4 and outgoing == [a*expected]*4,
                "The original 16-clock collision must affect the initialized Spin fibre")
    value_a = math.sqrt((math.sqrt(5)-1)/2)

    def real(x):
        return sum(c*value_a**degree for degree, c in enumerate(x.coefficients))

    def squared_motion(states):
        series = []
        for before, after in zip(states,states[1:]):
            squared = [one-overlap(x,y)*overlap(x,y) for x,y in zip(before, after)]
            require(squared == [squared[0]]*4, "Primary work depends on basis Spin")
            require(gram(before, after) == tuple(
                overlap(before[0],after[0]) if i == j else -overlap(before[j],after[i])
                for i,j in product(range(4),repeat=2)
            ), "Symmetric part of call overlap must be scalar for real inputs")
            series.append(squared[0])
        return series

    motions_ab, motions_ba = squared_motion(ab), squared_motion(ba)
    require(motions_ab[18:] == motions_ba[:18], "Rotation starts at the same blank in both orders")
    def motion_for_mass(q):
        return 2*q-q*q

    q1 = p*p
    q2 = 4*p*p*p
    q3 = (4*one-5*p)*(4*one-5*p)
    before = [one*0]*6 + [motion_for_mass(q1)]*6 + [p*p]*2 + [one*0]*4
    after = [motion_for_mass(q2)]*6 + [motion_for_mass(q3)]*6 + [p*p]*2 + [one*0]*4
    # Each 18-call block includes four stationary SWAP substeps in addition
    # to the two G calls and the 6+6 motions counted at the two masses.
    key = lambda x: x.coefficients
    require(sorted(map(key,motions_ab[:18])) == sorted(map(key,before))
            and sorted(map(key,motions_ba[18:])) == sorted(map(key,after)),
            "Exact per-call squared trace movements disagree with the mass formula")
    require(motion_for_mass(q1) == p
            and motion_for_mass(q2) == one-(one-q2)*(one-q2),
            "Wrong Golden identities in the regrouped formula")
    difference = 6*(math.sqrt(real(motion_for_mass(q2))) +
                    math.sqrt(real(motion_for_mass(q3))) - value_a)
    require(difference > 7, "Wrong total trace-movement difference for the primary pair")

    # An equal-length native change is a finite witness that endpoint
    # commutation does not survive all independent modifications.
    source = "SourceI"
    pair = max(i for i in range(17) if identity[i].op == identity[i+1].op == source)
    cx = ne.Gate("CX",(0,1))
    modified = identity[:pair]+(cx,cx)+identity[pair+2:]
    output = prefixes(modified, all_columns)[-1]
    require(output == tuple({j:(-one if j & 4 else one)} for j in range(16)),
            "Replacing the last SourceI pair should give the witness reflection")
    left = prefixes(modified+rotation, blank)[-1]
    right = prefixes(rotation+modified, blank)[-1]
    for x, y in zip(left,right):
        require(2*one-2*overlap(x,y) == 16*p*p*p,
                "Wrong finite commutator on the actual initialized fibre")
    return {"occupied_collision_calls": slots,
            "midpoint_rotation_F16_one_probability": "4 p^3",
            "fixed_trace_movement_difference_formula": "6 [sqrt(1-p^12) + f((4-5p)^2) - sqrt(p)]",
            "trace_movement_difference_BA_minus_AB": difference,
            "modified_I18_equal_length_commutator_norm_on_blank": "4 p^(3/2)",
            "trace_movement_tariff_identified_with_full_Cost_Info": False}


def main():
    data = {
        "scope": "Signed native prefixes, fixed program bit, no new live clock state.",
        "book03_sha256": sha256(BOOK03.read_bytes()).hexdigest(),
        "serial_B121": test_serial(),
        "clean_native_switch_B121": test_clean_switch(),
        "serial_primary_1121": test_primary(),
        "GR_closed": False,
    }
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
