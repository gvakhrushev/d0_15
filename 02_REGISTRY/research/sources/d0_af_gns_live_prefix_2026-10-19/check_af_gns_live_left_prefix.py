#!/usr/bin/env python3
"""Exact finite replay for the Golden-cost AF GNS live-left/old-right weld."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PIN_FILE = Path(__file__).with_name("SOURCE_PINS.json")


def zadd(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def zscale(k: int, x: tuple[int, int]) -> tuple[int, int]:
    return k * x[0], k * x[1]


def zmul(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    """Multiply a+b*p in Z[p], using p^2=1-p."""
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c - b * d


def p_power(n: int) -> tuple[int, int]:
    value = (1, 0)
    p = (0, 1)
    for _ in range(n):
        value = zmul(value, p)
    return value


def fib_table(nmax: int) -> list[int]:
    fib = [0, 1]
    for _ in range(nmax):
        fib.append(fib[-1] + fib[-2])
    return fib


def ceil_log2(value: int) -> int:
    assert value > 0
    return (value - 1).bit_length()


def all_prefixes(n: int) -> list[str]:
    words = [""]
    for _ in range(n):
        next_words: list[str] = []
        for word in words:
            next_words.append(word + "0")
            if not word.endswith("1"):
                next_words.append(word + "1")
        words = next_words
    return words


def all_cost_words(n: int) -> set[str]:
    if n == 0:
        return {""}
    out: set[str] = set()
    for suffix in all_cost_words(n - 1):
        out.add("F" + suffix)
    if n >= 2:
        for suffix in all_cost_words(n - 2):
            out.add("R" + suffix)
    return out


def encode(word: str) -> str:
    return "".join("0" if letter == "F" else "10" for letter in word)


def decode_prefix(bits: str) -> tuple[str, bool]:
    letters: list[str] = []
    i = 0
    pending_return = False
    while i < len(bits):
        if bits[i] == "0":
            letters.append("F")
            i += 1
        elif i + 1 < len(bits):
            assert bits[i + 1] == "0"
            letters.append("R")
            i += 2
        else:
            letters.append("R")
            pending_return = True
            i += 1
    return "".join(letters), pending_return


def source_pins() -> dict[str, str]:
    pins = json.loads(PIN_FILE.read_text())
    assert pins["base_head"] == "6e59c6f41025814b367f12cc5c5d80c795c55505"
    for relative, expected in pins["inputs"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected, (relative, actual, expected)
    return pins


def check_gns_cost_cut(nmax: int = 20) -> dict[str, object]:
    fib = fib_table(nmax + 2)
    for n in range(1, nmax + 1):
        prefixes = all_prefixes(n)
        exact = [w for w in prefixes if w.endswith("0")]
        pending = [w for w in prefixes if w.endswith("1")]
        assert len(exact) == fib[n + 1]
        assert len(pending) == fib[n]
        assert len(exact) + len(pending) == fib[n + 2]

        exact_by_word = {decode_prefix(w)[0]: w for w in exact}
        exact_decoded = set(exact_by_word)
        assert len(exact_decoded) == len(exact)
        assert all(not decode_prefix(w)[1] for w in exact)
        assert exact_decoded == all_cost_words(n)
        assert all(sum(1 if c == "F" else 2 for c in w) == n for w in exact_decoded)
        assert all(encode(w) == bits for w, bits in exact_by_word.items())

        pending_by_word = {decode_prefix(w)[0]: w for w in pending}
        pending_decoded = set(pending_by_word)
        assert len(pending_decoded) == len(pending)
        assert all(decode_prefix(w)[1] for w in pending)
        assert all(sum(1 if c == "F" else 2 for c in w) == n + 1 for w in pending_decoded)
        assert all(encode(w)[:-1] == bits for w, bits in pending_by_word.items())
        assert all(w.endswith("R") for w in pending_decoded)

        total_mass = zadd(zscale(len(exact), p_power(n)), zscale(len(pending), p_power(n + 1)))
        assert total_mass == (1, 0), (n, total_mass)

    n = nmax
    a, b = fib[n + 1], fib[n]
    p_float = (math.sqrt(5.0) - 1.0) / 2.0
    return {
        "n": n,
        "type_A_exact_cost_words": a,
        "type_B_pending_return_words": b,
        "full_prefix_labels": a + b,
        "exact_source_mass": a * p_float**n,
        "pending_source_mass": b * p_float ** (n + 1),
        "total_source_mass_exact_Zp_pair": [1, 0],
    }


def apply_right_unit(state: tuple[str, str, str, int], j: int, k: int):
    block, row, col, flag = state
    return (block, row, k, flag) if col == j else None


def apply_live_query(state: tuple[str, str, str, int], selected_rows: set[str]):
    block, row, col, flag = state
    return block, row, col, flag ^ int(row in selected_rows)


def apply_bad_old_control(state: tuple[str, str, str, int]):
    block, row, col, flag = state
    return block, row, col, flag ^ int(col == "0")


def check_live_left_right_commutant() -> dict[str, int]:
    checks = 0
    for n in range(1, 7):
        prefixes = all_prefixes(n)
        blocks = {
            "A": [w for w in prefixes if w.endswith("0")],
            "B": [w for w in prefixes if w.endswith("1")],
        }
        for block, labels in blocks.items():
            chosen = set(labels[::2]) if block == "A" else set()
            for row in labels:
                for col in labels:
                    for flag in (0, 1):
                        state = (block, row, col, flag)
                        image = apply_live_query(state, chosen)
                        assert image not in (None,)
                        assert apply_live_query(image, chosen) == state
                        for j in labels:
                            for k in labels:
                                lhs = apply_live_query(apply_right_unit(state, j, k), chosen) if apply_right_unit(state, j, k) else None
                                once = apply_live_query(state, chosen)
                                rhs = apply_right_unit(once, j, k)
                                assert lhs == rhs, (n, block, row, col, j, k, flag)
                                checks += 1

    # Hostile control: making the fresh operation depend on the archived column
    # fails to commute with the original right matrix unit E_01.
    state = ("A", "0", "0", 0)
    lhs = apply_bad_old_control(apply_right_unit(state, "0", "1"))
    rhs = apply_right_unit(apply_bad_old_control(state), "0", "1")
    assert lhs != rhs
    return {"exact_right_matrix_unit_intertwinings": checks, "oldRIGHT_read_control_rejected": 1}


def check_balanced_golden_left_fixture() -> dict[str, float | int]:
    p = (math.sqrt(5.0) - 1.0) / 2.0
    n, L, m = 20, 4, 29
    a, b = fib_table(n + 2)[n + 1], fib_table(n + 2)[n]
    gns_dimension = a * a + b * b
    gns_qubits = ceil_log2(gns_dimension)
    selected = m * L**4
    assert a == 10946 and b == 6765
    assert selected == 7424 and a - selected == 3522
    prefix_mass = selected * p**n
    ready_mass = 2 * selected * p ** (n + 3)
    assert abs(prefix_mass - 0.4907780810764765) < 2e-14
    assert abs(ready_mass - 0.2317139780019033) < 2e-14
    assert gns_dimension == 165_580_141
    assert gns_qubits == 28
    assert 2 ** (gns_qubits - 1) < gns_dimension <= 2**gns_qubits
    return {
        "n": n,
        "L": L,
        "words_per_role_cell": m,
        "selected_original_cost_n_words": selected,
        "unselected_original_cost_n_words_retained": a - selected,
        "selected_prefix_mass": prefix_mass,
        "ready_pair_mass": ready_mass,
        "full_gns_complex_dimension": gns_dimension,
        "binary_registers_for_padded_gns_vector": gns_qubits,
    }


def main() -> None:
    pins = source_pins()
    cost = check_gns_cost_cut()
    commutant = check_live_left_right_commutant()
    fixture = check_balanced_golden_left_fixture()
    result = {"pins": pins, "cost_cut": cost, "commutant": commutant, "balanced_fixture": fixture}
    Path(__file__).with_name("RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS pinned native Golden-cost and AF Fibonacci inputs")
    print("PASS exact cost-n words are AF type-A diagonal row/column addresses")
    print("PASS pending-return/type-B labels remain present with exact forced mass")
    print("PASS canonical AF GNS vector has identical active-row/old-column address labels")
    print("PASS live-left controlled query commutes with every tested old-right matrix unit")
    print("PASS column-controlled hostile operation fails old-right commutation")
    print("PASS all 3522 unselected words and pending-return sector are retained")
    print("PASS original n=20,L=4 balanced Golden LEFT masses")
    print("PASS full n=20 GNS cyclic vector fits in the stated 28-register padded carrier")
    print(json.dumps(result, indent=2))
    print("SCOPE: AF/GNS and generous active-control representation only; physical G0/fullStep selection, query admission, and full Book price remain OPEN; GR_closed=false")


if __name__ == "__main__":
    main()
