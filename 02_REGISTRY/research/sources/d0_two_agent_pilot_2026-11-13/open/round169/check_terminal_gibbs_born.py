"""Exact uninitialized-pointer columns for the first terminal winding of B167."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import runpy

import numpy as np


PILOT = Path("02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13")
FILES = {
    "direct/round80/native/check_return_work.py": "fdc0d988a48073b862f92dbe1e3f945f529c32fb3e907421c2f611dbcdea739c",
    "open/round165/check_service_abort.py": "acd22a6c91c789691a4a85c3908fe969b5165651ad477f6a9dc460e419db20d2",
    "open/round167/B167_MEASURED_REPORT_RETURN_RU.md": "2eb8bd1b74e4af7e272a8f00dfe9a65aeae0050fb1c4001483ac6a768ec71bc5",
    "open/round167/GUARD_AND_SITE_RU.md": "52975d84b8b342027b6c65481ac193fad1e9336417f729db4d76f8e580901751",
}


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def source_permutation(owner):
    native = owner["native"]
    context = native.Execution(8, (), (), (), native.G_CX_SOURCE_I, 2, (0, 1))
    matrix = native.gate_matrix(context, owner["src"], max_qubits=8)
    entries = np.asarray(matrix, dtype=np.int64)
    require(matrix == type(matrix)(entries.tolist()), "exact SourceI matrix entries")
    require(np.all(np.isin(entries, (-1, 0, 1))), "SourceI signed entries")
    require(np.all(np.count_nonzero(entries, axis=0) == 1), "SourceI input columns")
    require(np.all(np.count_nonzero(entries, axis=1) == 1), "SourceI output rows")
    rows = np.arange(256)
    columns = np.argmax(np.abs(entries), axis=1)
    return columns, entries[rows, columns]


def propagate_defect(owner, word, first_pointer, times_a, times_p, sources):
    # Exact basis 1,a,a²,a³ with a⁴=1−a², where a=√p.
    # Include all old columns while embedding |first_pointer> ⊗ v_perp.
    rows = np.arange(256)
    old = np.arange(64)
    state = np.zeros((4, 256, 64), dtype=np.int64)
    state[2, 4 * old + 2 * first_pointer, old] = -1
    state[1, 4 * old + 2 * first_pointer + 1, old] = 1
    source_columns, source_signs = sources
    for gate in word:
        masks = tuple(1 << (7 - wire) for wire in gate.wires)
        require(int(np.abs(state).max()) < 2**59, "exact coefficient range for next gate")
        if gate.op == "CX":
            control, target = masks
            state = state[:, rows ^ np.where((rows & control) != 0, target, 0), :]
        elif gate.op == "G":
            target, = masks
            signs = np.where((rows & target) != 0, 1, -1)
            state = times_a(state) + times_p(state[:, rows ^ target, :]) * signs[None, :, None]
        elif gate == owner["src"]:
            state = state[:, source_columns, :] * source_signs[None, :, None]
        else:
            raise ArithmeticError(f"unexpected detector gate {gate}")
    return state


def old_projections(times_a):
    projection = np.zeros((4, 64, 64), dtype=np.int64)
    powers = [np.array([1, 0, 0, 0], dtype=np.int64)]
    for _ in range(16):
        powers.append(times_a(powers[-1]))
    for row in range(64):
        for column in range(64):
            if row // 16 == column // 16:
                exponent = 8 + bin(row % 16).count("1") + bin(column % 16).count("1")
                projection[:, row, column] = powers[exponent]
    complement = -projection.copy()
    complement[0] += np.eye(64, dtype=np.int64)
    return projection, complement


def golden_apply(left, right, times_a, matrix_product):
    result = np.zeros_like(right)
    require(int(np.abs(left).max()) * int(np.abs(right).max()) * 2**12 < 2**62,
            "exact coefficient range for algebraic product")
    for degree in range(4):
        if matrix_product:
            term = left @ right[degree]
        else:
            term = left[:, None, None] * right[degree]
        for _ in range(degree):
            term = times_a(term)
        result += term
    return result


def verify_literal_word():
    owner = runpy.run_path(str(PILOT / "direct/round80/native/check_return_work.py"))
    service = runpy.run_path(str(PILOT / "open/round165/check_service_abort.py"))
    times_a, times_p = service["times_a"], service["times_p"]
    word = owner["measure_word"]()
    require(len(word) == 400, "fully priced literal detector word")
    source = source_permutation(owner)
    from_zero = propagate_defect(owner, word, 0, times_a, times_p, source)
    from_one = propagate_defect(owner, word, 1, times_a, times_p, source)
    projection, complement = old_projections(times_a)

    cosine = np.array([1, 0, 0, 0], dtype=np.int64)
    sine = np.zeros(4, dtype=np.int64)
    for _ in range(16):
        cosine, sine = times_a(cosine) - times_p(sine), times_p(cosine) + times_a(sine)
    require(np.array_equal(cosine, [3273345, 0, -5296384, 0]), "exact detector cosine")
    actual_overflow = golden_apply(from_zero[:, 1::4, :], complement, times_a, True)
    expected_overflow = golden_apply(times_a(cosine), complement, times_a, False)
    require(np.array_equal(actual_overflow, expected_overflow), "full M_01 Q = sqrt(p) cos(16theta) Q")
    actual_return = golden_apply(from_one[:, 2::4, :], projection, times_a, True)
    require(not np.any(actual_return), "full M_10 P = 0")
    return len(word)


def verify_moment_and_tail(detector_gates):
    # Positions after the second detector birth. The second terminal CX is
    # the wrap from the pre-last-gate leaf, not an extra forward step.
    position = 0
    position += detector_gates
    position += 2  # two true computed-bit reads
    position += 1  # canonical terminal helper birth
    position += 1  # first real helper CX
    winding = position + 1
    require(winding == 405, "first possible nonzero winding in the declared suffix")

    p_low = Fraction("0.6180339887498948482")
    p_high = Fraction("0.6180339887498948483")
    require(p_low**2 + p_low < 1 < p_high**2 + p_high, "exact enclosure of p")
    cosine_upper = 3273345 - 5296384 * p_low
    require(p_low * cosine_upper < -Fraction(1, 5), "strict negative leading moment")
    require(2 * p_high**2 < 1, "native beta_heat=2p²<1")
    y = Fraction(1, 22)
    tail = 2 * y / (winding + 1) / (1 - y / (winding + 2))
    require(tail < Fraction(1, 1000), "factorial Fourier tail is strictly smaller")
    require(2 * (p_low * cosine_upper + tail) < -Fraction(39, 100), "certified sign margin")
    return winding


def main():
    for file, expected in FILES.items():
        require(sha256((PILOT / file).read_bytes()).hexdigest() == expected, f"pinned source {file}")
    count = verify_literal_word()
    winding = verify_moment_and_tail(count)
    result = {
        "status": "PASS",
        "source_sha256": FILES,
        "detector_native_gates": count,
        "old_columns_replayed_per_defect_input": 64,
        "terminal_layout": "two sequential detector births, 400 calls, two reads, helper birth, CX, closing CX",
        "first_differing_winding": winding,
        "overflow_01_moment": "p cos(16 theta)",
        "return_10_moment": "0",
        "overflow_minus_return_thermal_bound": "< -0.39 f_405",
        "GR_closed": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
