#!/usr/bin/env python3
"""Rational values of S(a)=I+a(E_01+E_12) on the whole L=4 grid.

det S(a)=1 for every a. For each of the 256 characters, det H(a) is a
polynomial of degree at most 48. A joint kernel can occur only where that
polynomial vanishes, except on the eight characters where it vanishes
identically. Those eight are handled by one explicit joint minor, or by the
diagonal quarter-wave theorem for the two characters (i,i,i,i) and
(-i,-i,-i,-i).

The only rational point with joint rank below 24 and a nonzero moment is
a=±1 at (-1,1,-1,1).
"""
from __future__ import annotations

import importlib.util
from itertools import product
from multiprocessing import Pool
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
ROOTS = (sp.Integer(1), sp.I, sp.Integer(-1), -sp.I)
CHARS = list(product(ROOTS, repeat=4))
BOUND = 48
NODES = list(range(2, 2 + BOUND + 1))
CHECKS = list(range(NODES[-1] + 1, NODES[-1] + 5))
AA = sp.symbols("aa")
ZERO_DET = {
    (sp.I, sp.I, -1, 1),
    (sp.I, -1, sp.I, 1),
    (-1, sp.I, sp.I, 1),
    (-1, -sp.I, -sp.I, 1),
    (-sp.I, -1, -sp.I, 1),
    (-sp.I, -sp.I, -1, 1),
    (sp.I, sp.I, sp.I, sp.I),
    (-sp.I, -sp.I, -sp.I, -sp.I),
}
DIAGONAL = {
    (sp.I, sp.I, sp.I, sp.I),
    (-sp.I, -sp.I, -sp.I, -sp.I),
}
SHEAR_CHAR = (-1, 1, -1, 1)
ALLOWED_CONNECTION_ROOTS = {
    sp.Integer(-2), sp.Rational(-4, 3), sp.Integer(-1),
    sp.Integer(0), sp.Integer(1), sp.Integer(2),
}


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def load_support():
    spec = importlib.util.spec_from_file_location(
        "support", HERE / "a4d_joint_response_shear_l4_support_check.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shear(value):
    return sp.Matrix([[1, value, 0, 0], [0, 1, value, 0],
                      [0, 0, 1, 0], [0, 0, 0, 1]])


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


def connection_det(support, stored, phase):
    matrix = support.connection(stored, phase).applyfunc(sp.expand)
    return QQ_I.to_sympy(DomainMatrix.from_Matrix(matrix).convert_to(QQ_I).det())


def shard(shard_index: int):
    support = load_support()
    mine = [item for index, item in enumerate(CHARS) if index % 4 == shard_index]
    cache = {
        value: support.brackets(shear(sp.Integer(value)))
        for value in NODES + CHECKS
    }
    found = []
    for phase in mine:
        values = [connection_det(support, cache[value], phase) for value in NODES]
        poly = sp.Poly(newton(NODES, values, AA), AA)
        for value in CHECKS:
            got = sp.expand(poly.as_expr().subs(AA, value))
            expect = connection_det(support, cache[value], phase)
            if sp.expand(got - expect) != 0:
                raise AssertionError(f"check {phase} at {value}")
        expr = sp.factor(poly.as_expr())
        roots = []
        if expr != 0:
            _, factors = sp.factor_list(expr, AA)
            for factor, _mult in factors:
                piece = sp.Poly(sp.expand(factor), AA)
                if piece.degree() == 1:
                    lead, constant = piece.all_coeffs()
                    roots.append(sp.Rational(-constant, lead))
        found.append((phase, expr == 0, roots))
    return found


def canon(phase):
    return tuple(sp.sympify(item) for item in phase)


def joint_rank(support, value, phase, cache):
    phase = canon(phase)
    stored, units = cache[value]
    joint = support.connection(stored, phase).col_join(
        support.metric(units, [1 / component for component in phase])
    ).applyfunc(sp.expand)
    return support.nf.exact_rank(joint)


def prepare(support, value, cache):
    if value not in cache:
        solder = shear(value)
        cache[value] = (support.brackets(solder), support.metric_units(solder))
    return cache


def rational_roots(expr):
    if expr == 0:
        return None
    roots = []
    _, factors = sp.factor_list(expr, AA)
    for factor, _mult in factors:
        piece = sp.Poly(sp.expand(factor), AA)
        if piece.degree() == 1:
            lead, constant = piece.all_coeffs()
            roots.append(sp.Rational(-constant, lead))
    return roots


def minor_polynomial(support, phase):
    solder = shear(3)
    stored = support.brackets(solder)
    units = support.metric_units(solder)
    joint = support.connection(stored, phase).col_join(
        support.metric(units, [1 / component for component in phase])
    ).applyfunc(sp.expand)
    _rref, rows = joint.T.rref()
    rows = list(rows)
    nodes = list(range(2, 28))
    checks = [28, 29, 30]
    cache = {}
    for value in nodes + checks:
        sample = shear(value)
        cache[value] = (
            support.brackets(sample),
            support.metric_units(sample),
        )

    def det_at(value):
        stored_a, units_a = cache[value]
        matrix = support.connection(stored_a, phase).col_join(
            support.metric(units_a, [1 / component for component in phase])
        ).applyfunc(sp.expand)
        minor = matrix[rows, :]
        return QQ_I.to_sympy(DomainMatrix.from_Matrix(minor).convert_to(QQ_I).det())

    values = [det_at(value) for value in nodes]
    poly = sp.Poly(newton(nodes, values, AA), AA)
    for value in checks:
        if sp.expand(poly.as_expr().subs(AA, value) - det_at(value)) != 0:
            raise AssertionError(f"minor check {phase}")
    return sp.factor(poly.as_expr())


def main() -> None:
    support = load_support()
    aa = sp.symbols("aa")
    check("UNIPOTENT_DET_ONE", sp.factor(shear(aa).det()) == 1)
    symbolic = support.connection(
        support.brackets(shear(aa)),
        tuple(sp.Integer(item) for item in SHEAR_CHAR),
    )
    expected = 256 * (aa - 1) ** 4 * (aa + 1) ** 4 * (aa ** 2 + 1) ** 4
    check(
        "SHEAR_CHARACTER_DETERMINANT",
        sp.expand(sp.factor(symbolic.det()) - expected) == 0,
    )
    with Pool(4) as pool:
        parts = pool.map(shard, (0, 1, 2, 3))
    rows = [item for part in parts for item in part]
    check("ALL_CHARACTERS", len(rows) == 256)
    zeros = {canon(phase) for phase, zero, _roots in rows if zero}
    check("ZERO_DET_SET", zeros == {canon(phase) for phase in ZERO_DET})
    for _phase, zero, roots in rows:
        if zero:
            continue
        check("RATIONAL_ROOTS_IN_THE_LIST", set(roots) <= ALLOWED_CONNECTION_ROOTS)
    cache = {}
    # Connection roots outside the flat solder and the sign partners.
    extras = [
        (sp.Integer(2), (1, 1, sp.I, sp.I)),
        (sp.Integer(2), (-1, -1, sp.I, sp.I)),
        (sp.Integer(2), (1, 1, -sp.I, -sp.I)),
        (sp.Integer(2), (-1, -1, -sp.I, -sp.I)),
        (sp.Integer(-2), (sp.I, -sp.I, -1, -1)),
        (sp.Integer(-2), (-sp.I, sp.I, -1, -1)),
        (sp.Rational(-4, 3), (-1, sp.I, -sp.I, -1)),
        (sp.Rational(-4, 3), (-1, -sp.I, sp.I, -1)),
    ]
    for value, phase in extras:
        prepare(support, value, cache)
        check(
            f"EXTRA_ROOT_RANK_24_{value}_{canon(phase)}",
            joint_rank(support, value, phase, cache) == 24,
        )
    expected_low = {
        (canon(SHEAR_CHAR), 23),
        (canon((sp.I, sp.I, sp.I, sp.I)), 20),
        (canon((-sp.I, -sp.I, -sp.I, -sp.I)), 20),
    }
    for value in (sp.Integer(1), sp.Integer(-1)):
        prepare(support, value, cache)
        low = set()
        for phase, zero, roots in rows:
            if zero or value in roots:
                rank = joint_rank(support, value, phase, cache)
                if rank < 24:
                    low.add((canon(phase), rank))
        check(f"SIGN_PARTNER_LOW_SET_{value}", low == expected_low)
    special = [tuple(sp.sympify(item) for item in phase) for phase in ZERO_DET - DIAGONAL]
    for phase in special:
        factor = minor_polynomial(support, phase)
        roots = rational_roots(factor)
        check(f"MINOR_NONZERO_{phase}", roots is not None)
        for root in roots:
            if root == 0:
                continue
            prepare(support, root, cache)
            check(
                f"MINOR_ROOT_RANK_24_{phase}_{root}",
                joint_rank(support, root, phase, cache) == 24,
            )
    print()
    print("RESULT: on S(a) for rational a, the only L=4 character with")
    print("  joint rank below 24 and a nonzero moment is (-1,1,-1,1)")
    print("  at a=±1. Both diagonal quarter-waves stay moment-free.")
    print("BOUNDARY: this one-parameter family and the L=4 grid.")
    print("  Not the whole torus, not a global (NF) theorem, and not")
    print("  a response NOGO.")


if __name__ == "__main__":
    main()
