"""Literal 128-row reflection cross on its real amplitude domain.

The aligned-phase law and the role-1 sign-flip law are computed from the
published SELECT rows and the blank-row reflection. They are not defined as
a gap to the Einstein tensor. No coefficient is solved to match a curvature
component.
"""
from __future__ import annotations

from functools import lru_cache

import sympy as sp

ORDER = (0, 2, 3, 1)
I16 = sp.eye(16)
Z16 = sp.zeros(16)
P = (sp.sqrt(5) - 1) / 2


def popcount(n: int) -> int:
    return bin(int(n)).count("1")


@lru_cache(None)
def creator(role: int) -> sp.Matrix:
    matrix = sp.zeros(16)
    for mask in range(16):
        if mask & (1 << role):
            continue
        sign = (-1) ** sum(bool(mask & (1 << earlier)) for earlier in ORDER[: ORDER.index(role)])
        matrix[mask | (1 << role), mask] = sign
    return matrix


def native_select(nu, amplitude_b, phases):
    words = []
    for role in range(4):
        column = creator(role)
        creation = nu * phases[role] * column
        plain = nu * column
        left = I16 + (amplitude_b - 1) * column * column.T
        right = I16 + (amplitude_b - 1) * column.T * column
        for term in ((creation, left), (creation.H, right), (-plain, -left), (-plain.H, -right)):
            words.extend((term, term))
    rows = []
    for label in range(32):
        for coeff in range(2):
            row = Z16
            for word in range(32):
                sign = (-1) ** popcount(label & word)
                row += sign * words[word][coeff]
            rows.append(row / 32)
    return rows


def reflection(rows):
    blank = rows[0]
    return [(I16 if index == 0 else Z16) - 2 * row.H * blank for index, row in enumerate(rows)]


def column_cross(left_rows, right_rows):
    """Sum of right.H @ left, the order in the published cross of W(y) against W(x) when left is x."""
    total = Z16
    for left, right in zip(left_rows, right_rows):
        total += right.H * left
    return total


def select_overlap(left_rows, right_rows):
    total = Z16
    for left, right in zip(left_rows, right_rows):
        total += right * left.H
    return total


def aligned_scalar(nu_x, b_x, nu_y, b_y):
    overlap = (1 + nu_x * nu_y + b_x * b_y) / 2
    density = nu_x**2 + nu_y**2 - 2 * overlap * nu_x * nu_y
    return overlap, 1 - 2 * density / 128


def role1_flip_prediction(nu_x, b_x, nu_y, b_y):
    """Blank-row reflection cross when only the y role-1 phase is flipped to -1.

    Phases otherwise stay (I, +1, +1, +1) against (I, -1, +1, +1).
    """
    polynomial = 4 * b_x * b_y + 3 * nu_x * nu_y + 4
    gamma = nu_x * nu_y * polynomial / 256
    mean = (
        4 * b_x * b_y * nu_x * nu_y
        + 3 * nu_x**2 * nu_y**2
        - 4 * nu_x**2
        + 4 * nu_x * nu_y
        - 12 * nu_y**2
        + 256
    ) / 256
    created_0 = creator(0)
    created_1 = creator(1)
    pattern = (
        (-1 + sp.I) * created_0 * created_1.T
        + (1 + sp.I) * created_1 * created_0.T
        + (-1 + sp.I) * created_0 * created_1
        + (-1 - sp.I) * created_0.T * created_1.T
    )
    return mean, gamma, sp.expand(mean * I16 + gamma * pattern)


def port_cross_from_reflection(reflection_cross):
    """Full two-port contraction. The single-column terms cancel for any cross."""
    return sp.expand(P * I16 + P**2 * reflection_cross)


def gram_shift(mean, gamma):
    """Amount by which C.H @ C exceeds the square of its scalar part.

    Both sides are scalars times I16 on the role-1 flip. The shift is
    2 p^4 gamma^2 and is not a metric component.
    """
    scalar_part = P + P**2 * mean
    return sp.factor(2 * P**4 * gamma**2), sp.factor(scalar_part**2)


def circle_density_derivative():
    """Derivative of the aligned density along the published amplitude circle."""
    angle = sp.symbols("t", real=True)
    nu_x = sp.Rational(3, 5) * sp.cos(angle) + sp.Rational(4, 5) * sp.sin(angle)
    b_x = sp.Rational(4, 5) * sp.cos(angle) - sp.Rational(3, 5) * sp.sin(angle)
    nu_y = sp.Rational(5, 13)
    b_y = sp.Rational(12, 13)
    overlap, _ = aligned_scalar(nu_x, b_x, nu_y, b_y)
    density = sp.simplify(nu_x**2 + nu_y**2 - 2 * overlap * nu_x * nu_y)
    value = sp.simplify(density.subs(angle, 0))
    first = sp.simplify(sp.diff(density, angle).subs(angle, 0))
    diagonal_b = sp.Rational(4, 5)
    diagonal_nu = sp.Rational(3, 5)
    diagonal_overlap, _ = aligned_scalar(nu_x, b_x, diagonal_nu, diagonal_b)
    diagonal = sp.simplify(nu_x**2 + diagonal_nu**2 - 2 * diagonal_overlap * nu_x * diagonal_nu)
    second = sp.simplify(sp.diff(diagonal, angle, 2).subs(angle, 0))
    return value, first, second
