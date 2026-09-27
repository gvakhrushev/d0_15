#!/usr/bin/env python3
"""The two NF defects are isolated zeros of the joint corank locus.

At each defect the joint symbol is 34x24 of rank 23. The 11x4 matrix of
left-kernel pairings against the four phase derivatives has rank 3. Its
kernel is one line, (11, 0, 8, 9) on the upper shear and (11, 0, 9, 8) on
the chain. The second-order term along that line does not lie in the column
space of the first derivative, so no holomorphic curve of joint corank can
pass through the defect. The corank locus is therefore the single point in
a neighborhood inside (C*)^4.

The same run ranks the sixteen off-circle zeros of the connection
determinant on the four lines of section 8.15. Each joint symbol has rank 24.
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

DIRECTIONS = {
    "shear": (11, 0, 8, 9),
    "chain": (11, 0, 9, 8),
}
OFF_CIRCLE = (
    1 + 2 * sp.I,
    1 - 2 * sp.I,
    (1 + 2 * sp.I) / 5,
    (1 - 2 * sp.I) / 5,
)


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def chain_solder():
    solder = sp.eye(4)
    solder[0, 1] += 1
    solder[1, 3] += 1
    return solder


def assemble(stored, units, phase):
    phase = tuple(sp.sympify(item) for item in phase)
    joint = support.connection(stored, phase).col_join(
        support.metric(units, [1 / item for item in phase])
    )
    return joint.applyfunc(lambda entry: sp.expand(sp.together(entry)))


def qq_matrix(matrix):
    expanded = matrix.applyfunc(lambda entry: sp.expand(sp.together(entry)))
    for entry in expanded:
        if entry.has(sp.Float) or entry.has(sp.I):
            raise AssertionError("non-rational entry")
    return expanded


def qq_rank(matrix):
    return DomainMatrix.from_Matrix(qq_matrix(matrix)).convert_to(QQ).rank()


def right_kernel(matrix):
    domain = DomainMatrix.from_Matrix(qq_matrix(matrix)).convert_to(QQ)
    return domain.nullspace().to_Matrix().T


def primitive_vector(column):
    rationals = [sp.Rational(sp.together(column[i, 0])) for i in range(column.rows)]
    common = 1
    for item in rationals:
        common = sp.ilcm(common, int(sp.fraction(item)[1]))
    nums = [sp.Integer(sp.together(item * common)) for item in rationals]
    content = 0
    for num in nums:
        content = sp.igcd(content, abs(int(num)))
    vector = sp.Matrix([num // content for num in nums])
    for entry in vector:
        if entry != 0:
            if entry < 0:
                vector = -vector
            break
    return vector


def gaussian_rank(matrix):
    expanded = matrix.applyfunc(sp.expand)
    return DomainMatrix.from_Matrix(expanded).convert_to(sp.QQ_I).rank()


def isolate(stored, units, phase, direction_name: str):
    z = sp.symbols("z")
    phase = tuple(sp.Integer(item) for item in phase)
    joint = assemble(stored, units, phase)
    right = right_kernel(joint)
    left = right_kernel(joint.T)
    check(f"{direction_name}_RIGHT_DIM_1", right.cols == 1)
    check(f"{direction_name}_LEFT_DIM_11", left.cols == 11)
    check(f"{direction_name}_RANK_23", 34 - left.cols == 23 and 24 - right.cols == 23)
    columns = []
    for index in range(4):
        varied = list(phase)
        varied[index] = z
        derivative = qq_matrix(
            assemble(stored, units, varied).diff(z).subs(z, phase[index])
        )
        columns.append(left.T * derivative * right)
    stacked = sp.Matrix.hstack(*columns)
    check(f"{direction_name}_TANGENT_RANK_3", qq_rank(stacked) == 3)
    direction = primitive_vector(right_kernel(stacked))
    check(
        f"{direction_name}_DIRECTION",
        [int(entry) for entry in direction] == list(DIRECTIONS[direction_name]),
    )
    t = sp.symbols("t")
    moving = assemble(
        stored,
        units,
        [phase[index] + t * direction[index] for index in range(4)],
    )
    first = qq_matrix(moving.diff(t).subs(t, 0))
    second = qq_matrix(moving.diff(t, 2).subs(t, 0))
    velocity = first * right
    check(
        f"{direction_name}_DIRECTION_IS_TANGENT",
        qq_matrix(left.T * velocity) == sp.zeros(left.cols, 1),
    )
    solution, parameters = joint.gauss_jordan_solve(-velocity)
    if parameters:
        solution = solution.xreplace({parameter: 0 for parameter in parameters})
    check(
        f"{direction_name}_PARTICULAR",
        qq_matrix(joint * solution + velocity) == sp.zeros(joint.rows, 1),
    )
    observed = qq_matrix(left.T * (first * solution + second * right / 2))
    blocked = qq_rank(stacked.row_join(observed)) > qq_rank(stacked)
    check(f"{direction_name}_SECOND_ORDER_BLOCKS", blocked)
    witness_phase = {
        "shear": support.WITNESS,
        "chain": sp.Matrix([
            0, 0, 0, 0, 0, 1,
            0, 0, 0, 0, 0, 0,
            -2, 0, -1, 0, -1, 0,
            0, 1, 0, 1, 0, 1,
        ]),
    }[direction_name]
    check(
        f"{direction_name}_WITNESS_IN_KERNEL",
        qq_matrix(joint * witness_phase) == sp.zeros(34, 1),
    )


def main() -> None:
    upper = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    chain = chain_solder()
    families = {
        "shear": (upper, (-1, 1, -1, 1)),
        "chain": (chain, (-1, 1, 1, -1)),
    }
    prepared = {}
    for name, (solder, phase) in families.items():
        stored = support.brackets(solder)
        units = support.metric_units(solder)
        prepared[name] = (solder, stored, units)
        isolate(stored, units, phase, name)

    lines = {
        "shear-z0": ("shear", lambda root: (root, 1, -1, 1)),
        "shear-z2": ("shear", lambda root: (-1, 1, root, 1)),
        "chain-z0": ("chain", lambda root: (root, 1, 1, -1)),
        "chain-z3": ("chain", lambda root: (-1, 1, 1, root)),
    }
    for label, (family, builder) in lines.items():
        _, stored, units = prepared[family]
        for root in OFF_CIRCLE:
            phase = builder(root)
            rank = gaussian_rank(assemble(stored, units, phase))
            check(f"{label}_RANK_24_{root}", rank == 24)

    print()
    print("RESULT: each NF defect is an isolated point of the joint corank")
    print("  locus in (C*)^4. The tangent line is blocked at second order.")
    print("  The sixteen off-circle connection zeros on the four lines have")
    print("  joint rank 24.")
    print("BOUNDARY: these two solders and a neighborhood of each defect.")
    print("  Distant characters remain open. This is not a global (NF)")
    print("  theorem and not a response NOGO.")


if __name__ == "__main__":
    main()
