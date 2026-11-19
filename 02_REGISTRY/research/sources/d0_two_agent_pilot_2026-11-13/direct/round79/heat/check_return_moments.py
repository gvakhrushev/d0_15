"""Exact RAW survival probabilities, using Z[a]/(a^4+a^2-1) for a=sqrt(1/phi)."""
from itertools import product
import json

import numpy as np


class Golden:
    def __init__(self, *coefficients):
        self.coefficients = tuple(coefficients) + (0,) * (4 - len(coefficients))

    @staticmethod
    def cast(value):
        return value if isinstance(value, Golden) else Golden(int(value))

    def __add__(self, other):
        return Golden(*(x+y for x, y in zip(self.coefficients, self.cast(other).coefficients)))

    __radd__ = __add__

    def __neg__(self):
        return Golden(*(-x for x in self.coefficients))

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __mul__(self, other):
        values = [0] * 7
        for i, x in enumerate(self.coefficients):
            for j, y in enumerate(self.cast(other).coefficients):
                values[i+j] += x*y
        for n in range(6, 3, -1):
            values[n-4] += values[n]
            values[n-2] -= values[n]
        return Golden(*values[:4])

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.coefficients == self.cast(other).coefficients


def identity(size):
    return np.eye(size, dtype=int).astype(object)


def same(actual, expected):
    assert np.array_equal(actual, expected)


def controlled_not(bits, control, target):
    transfer = np.zeros((2**bits, 2**bits), dtype=int).astype(object)
    for column, entry in enumerate(product((0, 1), repeat=bits)):
        output = list(entry)
        output[target] ^= output[control]
        row = int(''.join(map(str, output)), 2)
        transfer[row, column] = 1
    return transfer


def corner(transfer, birth, initial):
    lifted = birth @ initial
    projector = lifted @ lifted.T
    cold = lifted.T @ transfer @ lifted
    return projector, cold.T @ cold


def check_survival(transfer, birth, initial, count):
    projector, effect = corner(transfer, birth, initial)
    amplitude = birth @ initial
    effect_power = initial
    for depth in range(1, count+1):
        step = transfer if depth % 2 else transfer.T
        amplitude = projector @ step @ amplitude
        effect_power = effect_power @ effect
        same(amplitude.T @ amplitude, effect_power)
    return effect


def main():
    a = Golden(0, 1)
    p = a*a
    assert p*p + p == 1
    v = np.array([[a], [p]], dtype=object)
    gate = np.array([[a, -p], [p, a]], dtype=object)
    old = identity(2)
    same(gate.T @ gate, old)
    lift = np.kron(old, v)
    cx = controlled_not(2, 0, 1)
    transfer = cx @ np.kron(gate, old)
    same(transfer @ lift, cx @ lift @ gate)  # gate could precede physical birth
    effect = check_survival(transfer, lift, old, 6)
    overlap_sq = 4*p*p*p
    expected = gate.T @ np.diag(np.array([1, overlap_sq], dtype=object)) @ gate
    same(effect, expected)
    assert effect[0, 1] != 0
    trace = lambda mat, exponent: np.trace(np.linalg.matrix_power(mat, exponent))
    for depth in range(1, 7):
        assert trace(effect, depth) == 1 + np.linalg.matrix_power(
            np.array([[overlap_sq]], dtype=object), depth)[0, 0]

    joint = check_survival(np.kron(transfer, transfer), np.kron(lift, lift), identity(4), 3)
    same(joint, np.kron(effect, effect))
    bell = np.array([1, 0, 0, 1], dtype=object)
    for depth in range(1, 4):
        joint_power = np.linalg.matrix_power(joint, depth)
        assert np.trace(joint_power) == trace(effect, depth)*trace(effect, depth)
        bell_numerator = bell @ joint_power @ bell
        assert bell_numerator == trace(effect, 2*depth)
        assert 2*bell_numerator != np.trace(joint_power)

    cut = np.array([[1, 0], [0, 0]], dtype=object)
    only_old_gate = np.kron(gate, old)
    true_effect = check_survival(only_old_gate, lift, cut, 3)
    fresh_only = lift @ lift.T @ only_old_gate @ lift @ cut
    assert true_effect[0, 0] == p
    assert (fresh_only.T @ fresh_only)[0, 0] == 1

    two_births = np.kron(old, np.kron(v, v))
    first = controlled_not(3, 0, 1)
    second = controlled_not(3, 0, 2)
    _, two_targets = corner(second @ first, two_births, old)
    _, one_target = corner(first @ first, two_births, old)
    assert two_targets[0, 0] == one_target[0, 0] == 1
    assert two_targets[1, 1] == overlap_sq*overlap_sq
    same(one_target, old)
    assert np.trace(one_target) != np.trace(two_targets)
    print(json.dumps({"arithmetic": "Z[a]/(a^4+a^2-1)", "one_wire_depths": 6,
                      "joint_wire_depths": 3, "bell_differs_from_product": True,
                      "old_cut_counterexample": True, "single_input_blind_pair": True},
                     sort_keys=True))


if __name__ == '__main__':
    main()
