#!/usr/bin/env python3
"""Exact support and word-count checks for the four-row AF zero-word theorem."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SOURCE_REL = Path(
    "02_REGISTRY/research/sources/d0_feasible_gain_source_2026-10-17/"
    "POINTER_BIRTH_CONTINUATION.md"
)
SOURCE_SHA256 = "5cb666b021cac1e3e724e117ca30a524f190c3d7d106081266641cc21b200554"
LABELS = (6, 22, 14, 30)
H = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)
FULL_MASK = (1 << 16) - 1
MAX_LENGTH = 8
CHECKS = 0
SUPPORT_COMPARISONS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def occupation_signs(state: int) -> tuple[int, int, int, int]:
    return tuple(-1 if state & (1 << r) else 1 for r in range(4))  # type: ignore[return-value]


E = tuple(
    tuple(
        sum(H[j][r] * occupation_signs(state)[r] for r in range(4))
        for state in range(16)
    )
    for j in range(4)
)


def extend_support(mask: int, axis: int, row: int, shell_sign: int) -> int:
    """Support of prefix*(E_row D0), using D0=sign*the occupation toggle."""
    if shell_sign not in (-1, 1):
        raise ValueError("shell_sign must be +1 or -1")
    out = 0
    for state in range(16):
        after_d0 = state ^ (1 << axis)
        # D0 contributes a nonzero scalar. Its sign cannot change support.
        if ((mask >> after_d0) & 1) and E[row][after_d0] != 0:
            out |= 1 << state
    return out


def extend_profiles(profiles: tuple[int, ...], row: int) -> tuple[int, ...]:
    return tuple(
        extend_support(profiles[axis * 2 + sign_index], axis, row, sign)
        for axis in range(4)
        for sign_index, sign in enumerate((-1, 1))
    )


def support_profiles(word: tuple[int, ...]) -> tuple[int, ...]:
    profiles = (FULL_MASK,) * 8
    for row in word:
        profiles = extend_profiles(profiles, row)
    return profiles


def is_constant(values: tuple[int, ...]) -> bool:
    return len(values) <= 1 or all(value == values[0] for value in values[1:])


def predicted_nonzero(word: tuple[int, ...]) -> bool:
    return is_constant(word[::2]) or is_constant(word[1::2])


def zero_count_formula(length: int) -> int:
    if length < 4:
        return 0
    odd = (length + 1) // 2
    even = length // 2
    return 4**length - 4 ** (even + 1) - 4 **(odd + 1) + 16


def check_source_pin() -> tuple[str, str]:
    source_bytes = (ROOT / SOURCE_REL).read_bytes()
    source_text = source_bytes.decode("utf-8")
    actual_sha = sha256(source_bytes)
    require(actual_sha == SOURCE_SHA256, "pinned pointer-birth source SHA-256 changed")
    for needle in (
        "(6,22,14,30)",
        "N_j=(1-b)/8 E_j",
        "H rows=(++++),(++--),(+-+-),(+--+)",
        "(E_a D0)(E_b D0)(E_c D0)(E_d D0)",
    ):
        require(needle in source_text, "pinned source is missing: " + needle)
    return actual_sha, git_blob_sha1(source_bytes)


def main() -> dict[str, object]:
    global SUPPORT_COMPARISONS
    source_sha, source_blob = check_source_pin()

    for i in range(4):
        require(
            H[i][0] * H[i][1] * H[i][2] * H[i][3] == 1,
            "Hadamard row does not have even sign parity",
        )
        for j in range(4):
            require(
                sum(H[i][r] * H[j][r] for r in range(4)) == (4 if i == j else 0),
                "Hadamard orthogonality failed",
            )

    for state in range(16):
        signs = occupation_signs(state)
        even = signs[0] * signs[1] * signs[2] * signs[3] == 1
        nonzero = [E[j][state] for j in range(4) if E[j][state] != 0]
        if even:
            require(len(nonzero) == 1, "even occupation does not select one row")
            require(abs(nonzero[0]) == 4, "even occupation selected row is not ±4")
        else:
            require(len(nonzero) == 4, "odd occupation does not support all rows")
            require(all(abs(value) == 2 for value in nonzero), "odd row value is not ±2")

    for axis in range(4):
        for state in range(16):
            require((state ^ (1 << axis)) ^ (1 << axis) == state, "D0 toggle is not involutive")

    zero_counts: dict[str, int] = {}
    total_words = 0
    level: list[tuple[tuple[int, ...], tuple[int, ...]]] = [((), (FULL_MASK,) * 8)]
    require(all(mask != 0 for mask in level[0][1]), "empty word is not identity")

    for length in range(1, MAX_LENGTH + 1):
        next_level: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
        zero_count = 0
        for prefix, prefix_profiles in level:
            for row in range(4):
                word = prefix + (row,)
                profiles = extend_profiles(prefix_profiles, row)
                predicted = predicted_nonzero(word)
                for index, mask in enumerate(profiles):
                    axis = index // 2
                    sign = (-1, 1)[index % 2]
                    require(
                        (mask != 0) == predicted,
                        "support theorem mismatch for word={}, axis={}, sign={}".format(
                            tuple(LABELS[j] for j in word), axis, sign
                        ),
                    )
                    SUPPORT_COMPARISONS += 1
                if not any(profiles):
                    zero_count += 1
                next_level.append((word, profiles))

        expected = zero_count_formula(length)
        require(zero_count == expected, "zero-word count formula mismatch at length {}".format(length))
        require(len(next_level) == 4**length, "alphabet word count mismatch")
        zero_counts[str(length)] = zero_count
        total_words += len(next_level)
        level = next_level

    controls = {
        "zero_crossing": (0, 1, 1, 0),
        "nonzero_alternating": (0, 1, 0, 1),
        "nonzero_one_constant_class": (0, 1, 0, 0),
        "nonzero_constant": (0, 0, 0, 0),
    }
    control_results: dict[str, dict[str, object]] = {}
    for name, word in controls.items():
        masks = support_profiles(word)
        actual_nonzero = all(mask != 0 for mask in masks)
        expected_nonzero = name != "zero_crossing"
        require(actual_nonzero == expected_nonzero, "hostile control failed: " + name)
        require(actual_nonzero == predicted_nonzero(word), "hostile control theorem mismatch: " + name)
        control_results[name] = {
            "labels": [LABELS[j] for j in word],
            "nonzero_on_every_shell": actual_nonzero,
        }

    expected_counts = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 144,
        "5": 720,
        "6": 3600,
        "7": 15120,
        "8": 63504,
    }
    require(zero_counts == expected_counts, "published zero-word table mismatch")
    require(total_words == 87380, "total exhaustive word count mismatch")
    require(SUPPORT_COMPARISONS == total_words * 4 * 2, "support comparison count mismatch")

    return {
        "alphabet_labels": list(LABELS),
        "carrier_scope": "four ordinary coefficient-1 rows on the fixed full-16 shell; nonzero D0 toggle scalars omitted only for support",
        "exact_checks": CHECKS,
        "hadamard_rows": [list(row) for row in H],
        "hostile_controls": control_results,
        "max_word_length": MAX_LENGTH,
        "occupations": 16,
        "shell_axes": [0, 1, 2, 3],
        "shell_signs": [-1, 1],
        "source": {
            "path": SOURCE_REL.as_posix(),
            "sha256": source_sha,
            "git_blob_sha1": source_blob,
        },
        "status": "PASS",
        "support_comparisons": SUPPORT_COMPARISONS,
        "total_words_checked": total_words,
        "zero_word_counts": zero_counts,
        "zero_word_rule": "m>=4: both alternating subsequences are nonconstant; for m<=3 there are no zero words",
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, sort_keys=True, indent=2))
