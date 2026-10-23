#!/usr/bin/env python3
"""Actual finite order-memory stage clock: exact active-corner obstruction.

Only whitelisted definitions are loaded from the two owned Python sources.
The complete 16-row apparatus and every cyclic 15-step window are retained.
No old certificate main, large autonomous matrix or Lean build is executed.
"""
import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    "04_CERTIFICATES/order_memory_control_verify.py": "bb72fe40326dc2d65d55f4f6d73564b7faef8f247774bf51771e3110f04e0c1a",
    "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean": "c350ead450996bfb7da20a987454b57da94dc098d17efeafc85a56b751664aa4",
    "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean": "76c7082b4f600f7b178579b8a2a859d6f692c96ce5a769920fb3ff427532292c",
    "03_FORMALIZATION/D0/Representation/OrderMemoryControl.lean": "2f36d015408ddac279515bde6d52dde5c8d347a8572be73c95d0046beef849dc",
    "03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean": "955bcffc5b927faf039cb15aae13e250b71c5e7b26fa811c30c61df423c005cc",
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md": "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
    PREFIX + "NATIVE_COHERENT_BOOK_COMPLEMENT.md": "d0cf0e29b79123410daae93e23899e824dc4746548d3c6af6da431fa1a15d04c",
    PREFIX + "check_native_car_actuated_metric.py": "72b2743f2f4c9408ceafe29dc691786c5011c4d1133d5fa6ebdb671a230bc3fa",
    "02_REGISTRY/research/A4D_NATIVE_CONDENSED_PRICE_NATURALITY.md": "4d90266d5f471ba3cac621e3ea3a32545b4622a16d7c0227bc771694ad851a08",
    "02_REGISTRY/research/A4D_CONDENSED_HISTORY_SOURCE_OBSTRUCTION.md": "5698a416d80f32b865c53af72809a4638207ca5b1470736cf719520a6262138b",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md": "577cbc909f766468fbef8ab38a5986ae761d348b075c2f38b2e1a88b704d4b3e",
}


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def load_selected(path, assignments, functions, environment):
    """AST selection excludes every import, check, loop and old main."""
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"), filename=path)
    selected = []
    found = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and name.id in assignments:
                selected.append(node)
                found.add(name.id)
        elif isinstance(node, ast.FunctionDef) and node.name in functions:
            selected.append(node)
            found.add(node.name)
    require(found == assignments | functions, "exact AST definition whitelist: " + path)
    exec(compile(ast.Module(body=selected, type_ignores=[]), path, "exec"), environment)
    return environment


def field_definitions():
    scope = load_selected(PREFIX + "check_native_car_actuated_metric.py",
                          {"Z", "O", "A", "P"},
                          {"add", "sub", "scale", "mul", "power", "dot"}, {"F": F})
    return tuple(scope[n] for n in ("Z", "O", "A", "P", "add", "sub", "scale", "mul", "power", "dot"))


for pinned_path, pinned_digest in PINS.items():
    require(hashlib.sha256((ROOT / pinned_path).read_bytes()).hexdigest() == pinned_digest,
            "immutable stage-clock input: " + pinned_path)

Z, ONE, A, P, add, sub, scale, mul, power, dot = field_definitions()


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def mm(left, right):
    columns = transpose(right)
    return [[dot(row, column) for column in columns] for row in left]


def eye(n):
    return [[ONE if i == j else Z for j in range(n)] for i in range(n)]


def ms(coefficient, matrix):
    return [[mul(coefficient, x) for x in row] for row in matrix]


def difference(left, right):
    return [[sub(x, y) for x, y in zip(r, s)] for r, s in zip(left, right)]


def parse_lean_matrix(path, marker, environment):
    text = (ROOT / path).read_text(encoding="utf-8")
    require(text.count(marker) == 1, "unique literal Lean matrix marker")
    body = text.split(marker, 1)[1].split("!![", 1)[1].split("]", 1)[0]

    def entry(source):
        node = ast.parse(source.strip(), mode="eval").body
        sign = 1
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            sign, node = -1, node.operand
        if isinstance(node, ast.Name):
            require(node.id in environment, "literal Lean matrix parameter")
            return scale(sign, environment[node.id])
        require(isinstance(node, ast.Constant) and isinstance(node.value, int),
                "literal Lean matrix integer")
        return scale(sign * node.value, ONE)

    matrix = [[entry(x) for x in row.split(",")] for row in body.split(";")]
    require(all(len(row) == len(matrix) for row in matrix), "square literal Lean matrix")
    return matrix


def actual_palette():
    readout = "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean"
    golden = "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean"
    li = parse_lean_matrix(readout, "def left (", {"a": Z, "b": ONE, "c": Z, "d": Z})
    lj = parse_lean_matrix(readout, "def left (", {"a": Z, "b": Z, "c": ONE, "d": Z})
    gate = parse_lean_matrix(golden, "def gate (", {"a": A, "p": P})
    require(len(li) == len(lj) == 4 and len(gate) == 2, "actual Lean palette dimensions")
    palette = {name: [[Z] * 16 for _ in range(16)]
               for name in ("B", "local_i", "common_j", "write", "idle")}
    for old in range(16):
        arm, spin, record = old // 8, (old // 2) % 4, old % 2
        for target_arm in range(2):
            palette["B"][8 * target_arm + 2 * spin + record][old] = gate[target_arm][arm]
        for target_spin in range(4):
            palette["local_i"][8 * arm + 2 * target_spin + record][old] = (
                li[target_spin][spin] if arm else (ONE if target_spin == spin else Z))
            palette["common_j"][8 * arm + 2 * target_spin + record][old] = lj[target_spin][spin]
        palette["write"][8 * arm + 2 * spin + (record ^ arm)][old] = ONE
        palette["idle"][old][old] = ONE
    for name, matrix in palette.items():
        require(mm(transpose(matrix), matrix) == eye(16), "complete primitive orthogonality: " + name)
    require(mm(palette["write"], palette["write"]) == eye(16), "reversible record write")
    return palette


def actual_programs():
    scope = load_selected("04_CERTIFICATES/order_memory_control_verify.py",
                          {"identity_word", "order_word"}, {"program"}, {})
    programs = {name: scope["program"](scope[name + "_word"])
                for name in ("identity", "order")}
    for names in programs.values():
        require(len(names) == 15, "actual programme has fifteen forward stages")
        require(names[-1] == "write", "actual final stage retains its record")
        require(names.count("B") == 2 and names.count("write") == 1,
                "actual comparison and record inventory")
    require(sorted(programs["identity"]) == sorted(programs["order"]), "matched actual primitive inventory")
    return programs


def selected_corner(state, mutation):
    rows = [list(state[2 * spin]) for spin in range(4)]
    if mutation == "drop-output-record":
        rows = [[add(x, y) for x, y in zip(state[2 * spin], state[2 * spin + 1])]
                for spin in range(4)]
    return rows


def encoded(matrix):
    return [[[str(c) for c in x] for x in row] for row in matrix]


def main():
    allowed = {"reset-stage-clock", "replace-all-windows-with-seed0", "drop-output-record"}
    require(len(sys.argv) <= 2, "at most one mutation argument")
    mutation = None
    if len(sys.argv) == 2:
        match = re.fullmatch(r"--mutation=(.+)", sys.argv[1])
        require(match is not None and match[1] in allowed, "known stage-clock mutation")
        mutation = match[1]
    require(mul(A, A) == P and add(P, mul(P, P)) == ONE, "exact positive-Golden field relations")
    palette, programs = actual_palette(), actual_programs()
    initial = [[ONE if row == 2 * spin else Z for spin in range(4)] for row in range(16)]
    require(mm(transpose(initial), initial) == eye(4), "four-coordinate input isometry")
    active_rows = set(range(0, 8, 2))
    one_tick_counts = {}
    for label, names in programs.items():
        one_tick_counts[label] = Counter()
        for name in names + ["idle"]:
            state = mm(palette[name], initial)
            require(mm(transpose(state), state) == eye(4), "one-tick complete arbitrary-input norm")
            a = selected_corner(state, None)
            complement_rows = [state[row] for row in range(16) if row not in active_rows]
            feedback = mm(transpose(complement_rows), complement_rows)
            require(feedback == difference(eye(4), mm(transpose(a), a)),
                    "one-tick full output complement")
            require(feedback == ms(feedback[0][0], eye(4)), "one-tick feedback is scalar I4")
            one_tick_counts[label][feedback[0][0]] += 1
        require(one_tick_counts[label] == Counter({Z: 14, power(P, 2): 2}),
                "one autonomous tick retains fourteen zero and two p^2 feedback blocks")
    require(one_tick_counts["identity"] == one_tick_counts["order"],
            "one-tick full-clock feedback has no programme-order contrast")
    states, corners, feedbacks, record_sensitive = {}, {}, {}, []
    clock_outputs = [(seed + 15) % 16 for seed in range(16)]
    require(len(set(clock_outputs)) == 16, "full clock-span phase outputs are distinct")
    for label, names in programs.items():
        stages = names + ["idle"]
        states[label], corners[label], feedbacks[label] = [], [], []
        for seed in range(16):
            used_seed = 0 if mutation == "replace-all-windows-with-seed0" else seed
            state = initial
            for offset in range(15):
                state = mm(palette[stages[(used_seed + offset) % 16]], state)
            require(mm(transpose(state), state) == eye(4), "every window retains arbitrary-input norm")
            a = selected_corner(state, mutation)
            physical_corner = selected_corner(state, None)
            complement_rows = [state[row] for row in range(16) if row not in active_rows]
            full_feedback = mm(transpose(complement_rows), complement_rows)
            require(difference(eye(4), mm(transpose(a), a)) == full_feedback,
                    "full output complement retains the record coordinate")
            states[label].append(state)
            corners[label].append(a)
            feedbacks[label].append(full_feedback)
            erased = selected_corner(state, "drop-output-record")
            if erased != physical_corner:
                record_sensitive.append([label, seed])
    p3, p6 = power(P, 3), power(P, 6)
    require(corners["identity"][0] == eye(4), "seed0 identity compressed corner is I4")
    require(corners["order"][0] == ms(p3, eye(4)), "seed0 order compressed corner is p^3 I4")
    for label in programs:
        require(corners[label][1] == ms(A, eye(4)), "seed1 actual compression is a I4 for both programmes")
        require(feedbacks[label][1] == ms(power(P, 2), eye(4)), "seed1 actual feedback is p^2 I4")
    require(feedbacks["identity"][0] == ms(Z, eye(4)), "seed0 identity feedback vanishes")
    require(feedbacks["order"][0] == ms(sub(ONE, p6), eye(4)), "seed0 order feedback retains the full output complement")
    require(sub(ONE, p6) == scale(4, p3), "actual Golden feedback closure 1-p^6=4p^3")
    scalar_counts = {}
    for label in programs:
        for feedback in feedbacks[label]:
            require(feedback == ms(feedback[0][0], eye(4)), "every complete clock feedback block is scalar I4")
        scalar_counts[label] = Counter(feedback[0][0] for feedback in feedbacks[label])
    require(scalar_counts["identity"] == Counter({Z: 4, power(P, 2): 2, P: 10}),
            "actual identity feedback multiset over all sixteen clock seeds")
    require(scalar_counts["order"] == Counter({scale(4, p3): 4, power(P, 2): 2, P: 10}),
            "actual order feedback multiset over all sixteen clock seeds")
    for label, expected_weight in (("identity", Z), ("order", scale(4, p3))):
        state = states[label][0]
        record_one = [state[row] for row in range(16) if row % 2]
        require(mm(transpose(record_one), record_one) == ms(expected_weight, eye(4)),
                "actual seed0 final record weight")
        require(all(state[row] == [Z] * 4 for row in range(16)
                    if row % 2 != row // 8), "actual seed0 record equals output arm")
    require(record_sensitive, "off-seed windows expose output-record erasure")
    cross = difference(mm(corners["order"][0], corners["identity"][1]),
                       mm(corners["order"][1], corners["identity"][0]))
    expected_cross = mul(A, sub(p3, ONE))
    require(expected_cross != Z and cross == ms(expected_cross, eye(4)),
            "nonzero paired-block obstruction to a common clock tensor factor")
    returned_stage = 0 if mutation == "reset-stage-clock" else clock_outputs[0]
    start_corner = corners["identity"][0] if returned_stage == 0 else ms(Z, eye(4))
    require(start_corner == ms(Z, eye(4)), "initial-stage cut keeps the advanced retained clock orthogonal")
    require(difference(eye(4), mm(transpose(start_corner), start_corner)) == eye(4),
            "initial-stage Book complement is I4")
    require(all(m % 16 != 0 for m in range(1, 16)), "all positive pre-wrap starts are clock-orthogonal")
    # A maps seed c only to c+15. Thus A* A is the direct sum of a_c* a_c;
    # off-diagonal clock blocks vanish without constructing a 256/512 square.
    blocks, block_ids, registry = {}, {}, []
    for label in programs:
        blocks[label] = []
        for seed in range(16):
            pair = (corners[label][seed], feedbacks[label][seed])
            key = repr(pair)
            if key not in block_ids:
                block_ids[key] = len(registry)
                registry.append({"a": encoded(pair[0]), "I-a_transpose_a": encoded(pair[1])})
            blocks[label].append({"input_clock": seed, "output_clock": clock_outputs[seed],
                                  "block_id": block_ids[key]})
    result = {
        "status": "PASS", "field": "Q(a), a^4+a^2-1=0; a>0, p=a^2",
        "field_coefficient_order": ["1", "a", "a^2", "a^3"],
        "actual_programs_chronological": programs,
        "dimensions": {"stage_clock": 16, "apparatus": 16, "arm": 2, "spin": 4, "record": 2,
                       "input_spin_columns": 4, "full_clock_corner_input": 64},
        "primitive_orthogonality": list(palette),
        "full_clock_corner": "sum_c |c+15><c| tensor a_c, clocks modulo16",
        "full_clock_complement": "direct_sum_c(I4-a_c^transpose a_c)",
        "all_clock_seed_blocks": blocks, "distinct_block_registry": registry,
        "seed0": {"identity_a": "I4", "order_a": "p^3 I4", "identity_feedback": "0",
                  "order_feedback": "(1-p^6) I4", "order_record_one": "4p^3 I4"},
        "seed1": {"both_a": "a I4", "both_feedback": "p^2 I4"},
        "full_clock_Book_determinant": {
            "operator_argument": "W^15, the fifteen-tick macrooperator",
            "physical_Book_U_N_binding_proved": False,
            "all_feedback_blocks_scalar_I4": True,
            "identity_feedback_multiset": {"0": 4, "p^2": 2, "p": 10},
            "order_feedback_multiset": {"4p^3=1-p^6": 4, "p^2": 2, "p": 10},
            "identity_det_I_minus_zF": "(1-z*p^2)^8*(1-z*p)^40",
            "order_det_I_minus_zF": "(1-z*p^2)^8*(1-z*p)^40*(1-4*z*p^3)^16",
            "natural_log_price_order_minus_identity": "-16*log(1-4*z*p^3)>0 for 0<z<1",
            "clock_cut": "all16 encoded clock phases; arm0, record0, all4 spin coordinates",
            "oldRIGHT_or_selector_multiplicity_in_this_apparatus": False,
        },
        "one_tick_vs_fifteen_tick": {
            "same_full_clock_cut": "I16 tensor j, j selects arm0 record0 and all4 spin coordinates",
            "one_tick_operator_argument": "W=sum_c |c+1><c| tensor U_c",
            "one_tick_both_feedback_multisets": {"0": 14, "p^2": 2},
            "one_tick_both_det_I_minus_zF": "(1-z*p^2)^8",
            "one_tick_both_natural_log_price": "-8*log(1-z*p^2)",
            "one_tick_price_order_contrast": 0,
            "fifteen_tick_operator_argument": "W^15",
            "fifteen_tick_price_order_contrast": "-16*log(1-4*z*p^3)>0 for 0<z<1",
            "macro_grouping_changes_the_functional": True,
            "physical_Book_U_N_binding_to_W_or_W15_proved": False,
        },
        "paired_common_factor_obstruction": {"cross_product": "a*(p^3-1) I4",
                                              "field_coefficient": [str(c) for c in expected_cross],
                                              "nonzero": True, "common_T_for_B_identity_I_B_order_p3": False},
        "initial_stage_cut": {"input_stage": 0, "output_stage_after15": 15,
                              "compressed_W15": "0", "full_Book_complement": "I4"},
        "record_erasure_sensitive_windows": record_sensitive,
        "scope": {"actual_owned_trial": "seed0, first15 forward transitions",
                  "off_seed_windows": "literal finite cyclic extension with final idle wrap",
                  "encoded_stage_is_physical_elapsed_clock": False,
                  "original_cap2_controller_clock_factor_proved": False,
                  "full_Book_or_physical_GR_selection_proved": False,
                  "old_certificate_main_executed": False, "large_clock_matrix_built": False},
        "source_sha256": PINS,
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
