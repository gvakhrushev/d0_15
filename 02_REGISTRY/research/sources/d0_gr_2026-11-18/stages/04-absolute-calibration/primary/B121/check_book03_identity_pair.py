"""Replay the addressed pair, the formal central classes, and the raw binary test."""

from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp


REPO = Path(__file__).resolve().parents[6]
SOURCES = REPO / "02_REGISTRY" / "research" / "sources"
NATIVE = SOURCES / "d0_native_execution_domain_2026-10-24" / "native_execution.py"
BOOK03 = REPO / "01_BOOKS" / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"
ARCHIVE = "4f99c2c46e646d21ae5b9b0491da17bd1b094da0"
BOOK_I = "8add930fe27ab6bb25e5c432127a86a05bca1e6e"
BOOK_II = "19701354c459014fb88e33aace667e0904409f17"

sys.path.insert(0, str(NATIVE.parent))
import native_execution as ne


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def archive_pin(path, expected_blob):
    git_path = f"99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/books/{path}"
    spec = f"{ARCHIVE}:{git_path}"
    blob = subprocess.check_output(["git", "rev-parse", spec], cwd=REPO, text=True).strip()
    require(blob == expected_blob, f"Archive blob changed: {path}")
    data = subprocess.check_output(["git", "cat-file", "blob", blob], cwd=REPO)
    return {"path": git_path, "git_blob": blob, "sha256": sha256(data).hexdigest()}


def cx(control, target):
    return ne.Gate("CX", (control, target))


def actual_words():
    swap = (cx(0, 1), cx(1, 0), cx(0, 1))
    source = ne.Gate("SourceI", (0, 2, 3))
    golden = ne.Gate("G", (1,))
    z = swap + (source, source) + swap
    return {
        "G_Z_G_Z": (golden,) + z + (golden,) + z,
        "CX_18": (cx(0, 1),) * 18,
    }


def paths_for(bits, word):
    # Track chronological WORK states, exponent of i in Q8, and exponent of a=sqrt(p).
    paths = [((bits,), 0, 0)]
    for gate in word:
        updated = []
        for states, order, power in paths:
            current = states[-1]
            if gate.op == "G":
                wire = gate.wires[0]
                old = current[wire]
                for new in (0, 1):
                    out = list(current)
                    out[wire] = new
                    order_step = 2 if old == 1 and new == 0 else 0
                    power_step = 1 if old == new else 2
                    updated.append((states + (tuple(out),), (order + order_step) % 4,
                                    power + power_step))
            elif gate.op == "CX":
                control, target = gate.wires
                out = list(current)
                out[target] ^= current[control]
                updated.append((states + (tuple(out),), order, power))
            elif gate.op == "SourceI":
                port = gate.wires[0]
                updated.append((states + (current,), (order + current[port]) % 4, power))
            else:
                raise ValueError(f"Unexpected literal gate: {gate.op}")
        paths = updated
    return paths


def exact(x, y):
    return ne.GOLDEN_FIELD.from_sympy(sp.expand(x - y)) == ne.GOLDEN_FIELD.zero


def verify_words(words):
    descriptors = {}
    tables = {}
    identity = sp.eye(16)
    for name, word in words.items():
        execution = ne.Execution(4, (), (), word, ne.G_CX_SOURCE_I, 0, (2, 3))
        inventory = ne.inventory(execution, max_qubits=4, max_expanded_stages=18)
        actual = ne.word_matrix(execution, max_qubits=4, max_expanded_stages=18)
        require(ne.exact_matrix_equal(actual, identity), f"{name} fails on the full input")
        require(inventory.expanded_stages == 18, f"{name} changed its chronological length")
        descriptors[name] = {
            "expanded_stages": inventory.expanded_stages,
            "G": inventory.g_count,
            "CX": inventory.cx_count,
            "SourceI": inventory.source_i_count,
            "full_input_dimension": inventory.input_dimension,
            "compact_descriptor_bytes": len(ne.canonical_json(execution).encode("utf-8")),
        }
        columns = {}
        gold_stages = [j + 1 for j, gate in enumerate(word) if gate.op == "G"]
        for port, bit in product((0, 1), repeat=2):
            paths = paths_for((port, bit), word)
            entries = []
            for states, order, amp_power in paths:
                out_port, out_bit = states[-1]
                require(out_port == port, "Routed port must be restored on each path")
                require(order % 2 == 0, "Endpoints lie in the central subgroup")
                entry = {
                    "target_after_G": [states[stage][1] for stage in gold_stages],
                    "terminal_target": out_bit,
                    "central_class": 1 if order == 0 else -1,
                    "native_amplitude_power_of_sqrt_p": amp_power,
                }
                entries.append(entry)
                if name == "G_Z_G_Z":
                    intermediate = states[gold_stages[0]][1]
                    expected_class = -1 if out_bit != bit and intermediate == 0 else 1
                    require(entry["central_class"] == expected_class, "Wrong central class")
            return_paths = [p for p in entries if p["terminal_target"] == bit]
            off_paths = [p for p in entries if p["terminal_target"] != bit]
            if name == "G_Z_G_Z":
                require(len(entries) == 4, "The echo requires exactly four paths per input")
                require(sorted((p["central_class"], p["native_amplitude_power_of_sqrt_p"])
                               for p in return_paths) == [(1, 2), (1, 4)], "Return class table")
                require(sorted((p["central_class"], p["native_amplitude_power_of_sqrt_p"])
                               for p in off_paths) == [(-1, 3), (1, 3)], "Dark class table")
            else:
                require(len(entries) == 1 and not off_paths, "CX reference path count")
                require(return_paths[0]["central_class"] == 1, "CX reference memory")
            columns[f"{port}{bit}"] = entries
        tables[name] = columns
    return descriptors, tables


def verify_raw_binary_model():
    p, a = ne.P, ne.A
    c = p**2 + p**4
    e = p**3
    accepted = []
    for first, wrong_after_zero, wrong_after_one in product((1, 2), repeat=3):
        r = p**first
        left = r * p**wrong_after_zero
        right = (1 - r) * p**wrong_after_one
        if exact(left, right):
            require(exact(left, e), "A dark branch did not have weight p cubed")
            bright_zero = r * (1 - p**wrong_after_zero)
            bright_one = (1 - r) * (1 - p**wrong_after_one)
            require(exact(bright_zero + bright_one, c), "Wrong bright weight")
            accepted.append([first, wrong_after_zero, wrong_after_one])
    require(accepted == [[1, 2, 1], [2, 1, 2]], "Unexpected binary dark assignments")
    p_conjugate = (-sp.sqrt(5) - 1) / 2
    require(exact(c, 3 - 4*p), "Bright scalar in the quadratic field")
    require(exact(c * (3 - 4*p_conjugate), sp.Integer(5)), "Norm of bright scalar")
    require(exact(p * p_conjugate, -sp.Integer(1)), "Norm of Golden unit")
    require(exact(c + 2*e, sp.Integer(1)) and exact(c - 2*e, p**6),
            "Wrong regular-memory spectrum")

    selector = sp.Matrix([[0, 1], [1, 0]])
    swap_central = sp.kronecker_product(sp.eye(4), selector)
    regular = c * sp.eye(16) + e * sp.kronecker_product(selector, sp.eye(8) + swap_central)
    basis = sp.eye(16)[:, 0]
    regular_mass = (basis.T * regular.T * regular * basis)[0]
    require(exact(regular_mass, c**2 + 2*e**2), "Wrong mass from the regular unit class")

    # The two dark-compatible identical raw G matrices fail the independent born-frame readout.
    for stay in (p, p**2):
        lower = (1 - stay) * a + stay * p
        readout = lower**2 / c
        require(not exact(readout, 4*p**3), "A raw binary gate passed the native fresh-bit reading")
    return {
        "allowed_dark_parameter_exponents": accepted,
        "dark_path_weight_each": "p^3",
        "bright_total_amplitude": "p^2 + p^4 = 3 - 4p",
        "spin_mass_ratio_to_unit_reference": "(3 - 4p)^2",
        "field_norm_bright_amplitude": 5,
        "rational_golden_exponent_can_supply_compensator": False,
        "regular_gram_extrema": ["p^12", "1"],
        "regular_mass_from_initialized_unit_class": "(3 - 4p)^2 + 2p^6",
        "same_raw_gate_passes_fresh_bit_readout": False,
    }


def main():
    books = {
        "Book_I": archive_pin("BOOK_I_ARCHITECTURE_GOLDEN_PASS30.txt", BOOK_I),
        "Book_II": archive_pin("BOOK_II_MECHANISM_GOLDEN_PASS30.txt", BOOK_II),
    }
    native_words, paths = verify_words(actual_words())
    result = {
        "archive_commit": ARCHIVE,
        "archive_books": books,
        "book03_sha256": sha256(BOOK03.read_bytes()).hexdigest(),
        "native_execution_sha256": sha256(NATIVE.read_bytes()).hexdigest(),
        "native_words": native_words,
        "chronological_paths_by_initial_port_and_target": paths,
        "conditional_raw_binary_model": verify_raw_binary_model(),
        "book03_physical_valuation_identified": False,
        "book03_preparer_absolute_normalizer_identified": False,
        "physical_C_closed": False,
        "GR_closed": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
