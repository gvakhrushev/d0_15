#!/usr/bin/env python3
"""Connection determinant on the four complex lines through the NF defects.

Lines, fixed before the determinant is read:
  shear-z0  solder I+E_01+E_12, phase (z, 1, -1, 1)
  shear-z2  solder I+E_01+E_12, phase (-1, 1, z, 1)
  chain-z0  solder I+E_01+E_13, phase (z, 1, 1, -1)
  chain-z3  solder I+E_01+E_13, phase (-1, 1, 1, z)

The varying phase enters each connection entry only as z or 1/z. Clearing
that pole by one factor of z produces a polynomial matrix of entry degree
at most 2, so the determinant has degree at most 48. Exact rational values
determine it, and further integers check the interpolant.

The resulting polynomial is the same on all four lines. Its only root of
modulus 1 is z=-1, the carrier already cut at order u^5. Every other
unitary point of these lines has invertible connection block, hence trivial
joint kernel. The four algebraic roots off the unit circle are not ranked.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "support", HERE / "a4d_joint_response_shear_l4_support_check.py"
)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)

LINES = ("shear-z0", "shear-z2", "chain-z0", "chain-z3")


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def shapes(which: str):
    upper = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    chain = sp.eye(4)
    chain[0, 1] += 1
    chain[1, 3] += 1
    if which.startswith("shear"):
        return upper
    if which.startswith("chain"):
        return chain
    raise AssertionError(which)


def phase_at(which: str, value):
    if which == "shear-z0":
        return (value, 1, -1, 1)
    if which == "shear-z2":
        return (-1, 1, value, 1)
    if which == "chain-z0":
        return (value, 1, 1, -1)
    if which == "chain-z3":
        return (-1, 1, 1, value)
    raise AssertionError(which)


def cleared_connection(stored, which: str, value):
    phase = tuple(sp.sympify(item) for item in phase_at(which, value))
    connection = support.connection(stored, phase)
    return (connection * value).applyfunc(lambda entry: sp.expand(sp.together(entry)))


def entry_degree_bound(which: str, matrix, z) -> int:
    max_degree = 0
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            entry = matrix[i, j]
            if entry.has(sp.Float):
                raise AssertionError(f"{which} float at {(i, j)}")
            numer, denom = sp.fraction(sp.together(entry))
            if sp.Poly(sp.expand(denom), z).degree() > 0:
                raise AssertionError(f"{which} pole at {(i, j)}")
            poly = sp.Poly(sp.expand(sp.together(entry)), z)
            if poly.domain not in (sp.ZZ, sp.QQ):
                raise AssertionError(f"{which} domain {poly.domain}")
            max_degree = max(max_degree, poly.degree())
    check(f"{which}_ENTRY_DEGREE_AT_MOST_2", max_degree <= 2)
    return 24 * max_degree


def det_at(stored, which: str, t: int):
    matrix = cleared_connection(stored, which, sp.Integer(t))
    domain = DomainMatrix.from_Matrix(matrix).convert_to(QQ)
    value = QQ.to_sympy(domain.det())
    if value.has(sp.Float):
        raise AssertionError(f"{which} float det")
    return value


def newton(xs, ys, z):
    coeff = list(ys)
    span = len(xs)
    for level in range(1, span):
        for index in range(span - 1, level - 1, -1):
            coeff[index] = sp.together(
                (coeff[index] - coeff[index - 1]) / (xs[index] - xs[index - level])
            )
    expr = coeff[-1]
    for index in range(span - 2, -1, -1):
        expr = coeff[index] + (z - xs[index]) * expr
    return sp.expand(expr)


def modulus_obstruction(quadratic: sp.Expr, z) -> None:
    """A root of modulus 1 would force x=1/3 and y=0."""
    poly = sp.Poly(sp.expand(quadratic), z)
    a, b, c = poly.all_coeffs()
    x, y = sp.symbols("x y", real=True)
    # a z^2 + b z + c = 0 and z * conjugate(z) = 1 give
    # (a+c) x = -b and (a-c) y = 0.
    check(f"DISC_NEGATIVE_{a}_{b}_{c}", sp.discriminant(poly.as_expr(), z) < 0)
    real_part = sp.Eq((a + c) * x, -b)
    imag_part = sp.Eq((a - c) * y, 0)
    solution = sp.solve([real_part, imag_part], [x, y], dict=True)
    check(f"MODULUS_SYSTEM_{a}_{b}_{c}", len(solution) == 1)
    point = solution[0]
    residue = sp.expand(point[x] ** 2 + point[y] ** 2 - 1)
    check(f"NOT_ON_THE_CIRCLE_{a}_{b}_{c}", residue != 0)


def main() -> None:
    z = sp.symbols("z")
    expected = (
        z**18
        * (z + 1) ** 8
        * (z**2 - 2 * z + 5)
        * (5 * z**2 - 2 * z + 1)
        / 16
    )
    modulus_obstruction(z**2 - 2 * z + 5, z)
    modulus_obstruction(5 * z**2 - 2 * z + 1, z)
    roots = sp.solve(sp.together(expected * 16 / z**18 / (z + 1) ** 8), z)
    for root in roots:
        modulus_sq = sp.simplify(sp.expand(root * sp.conjugate(root)))
        check("OFF_CIRCLE_ROOT", modulus_sq != 1)
        print("OFF_CIRCLE", root, "MODULUS_SQ", modulus_sq, flush=True)
    check("DEFECT_IS_A_ROOT", sp.expand(expected.subs(z, -1)) == 0)
    check("IDENTITY_PHASE_IS_NOT_A_ROOT", sp.expand(expected.subs(z, 1)) != 0)

    upper = shapes("shear-z0")
    chain = shapes("chain-z0")
    stored = {
        "shear": support.brackets(upper),
        "chain": support.brackets(chain),
    }
    for which in LINES:
        family = "shear" if which.startswith("shear") else "chain"
        bracket = stored[family]
        bound = entry_degree_bound(
            which, cleared_connection(bracket, which, z), z
        )
        nodes = list(range(2, 2 + bound + 1))
        checks = list(range(nodes[-1] + 1, nodes[-1] + 7))
        values = [det_at(bracket, which, t) for t in nodes]
        poly = sp.Poly(newton(nodes, values, z), z)
        check(f"{which}_DOMAIN_QQ", poly.domain in (sp.ZZ, sp.QQ))
        for t in checks:
            got = sp.expand(poly.as_expr().subs(z, t))
            expect = det_at(bracket, which, t)
            check(f"{which}_CHECK_{t}", sp.expand(got - expect) == 0)
        check(
            f"{which}_MATCHES_FORMULA",
            sp.expand(poly.as_expr() - expected) == 0,
        )
        print(which, "DEGREE", poly.degree(), "AT_Z2", poly.subs(z, 2), flush=True)

    print()
    print("RESULT: on each of the four lines the cleared connection")
    print("  determinant is z^18 (z+1)^8 (z^2-2z+5)(5z^2-2z+1)/16.")
    print("  Its only root of modulus 1 is z=-1. Every other unitary")
    print("  point of these lines has invertible connection block and")
    print("  therefore trivial joint kernel.")
    print("BOUNDARY: the four lines through the two defect solders.")
    print("  The algebraic roots 1±2i and (1±2i)/5 are off the unit")
    print("  circle and are not ranked. This does not restore (NF) off")
    print("  these lines and is not a response NOGO.")


if __name__ == "__main__":
    main()
