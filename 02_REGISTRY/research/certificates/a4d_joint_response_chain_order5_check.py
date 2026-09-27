#!/usr/bin/env python3
"""Order-u^5 cut of the chain I+E_01+E_13.

The witness-orthogonal solution of the order-u^3 connection equation, and
that solution plus each witness-orthogonal kernel direction, has order-u^5
witness projection -432 after the unique order-u^4 correction. The witness
lies in the left kernel, so the projection is a Fredholm obstruction.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cubic = load("a4d_joint_response_shear_cubic_check")
order5 = load("a4d_joint_response_shear_order5_check")
WITNESS_ROWS = [
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [-2, 0, -1, 0, -1, 0],
    [0, 1, 0, 1, 0, 1],
]
FLAT = [coeff for role in WITNESS_ROWS for coeff in role]
ZETA = sp.sympify(
    "[-1/2, 1/2, 1/2, 1/2, 1/2, 0, 0, 0, 0, 0, 0, 0,"
    " -2, 1, -1, 1, -1, 2, -1/2, -1/2, -1, -1/2, -1, 0]"
)
SOLDER = sp.eye(4)
SOLDER[0, 1] += 1
SOLDER[1, 3] += 1


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def sigma(site):
    return 1 if (site[0] + site[3]) % 2 == 0 else -1


def install(module):
    module.SHEAR = SOLDER
    module.sigma = sigma
    roles = []
    for role in range(4):
        matrix = module.Z4 * 0
        for j, generator in enumerate(module.GENERATORS):
            matrix += FLAT[6 * role + j] * generator
        roles.append(matrix)
    module.ROLES = roles


install(cubic)
install(order5)
cubic.WITNESS = WITNESS_ROWS
cubic.ZETA = list(ZETA)


def resonant(odd, order):
    value = 0
    for role in range(4):
        for j in range(6):
            value += WITNESS_ROWS[role][j] * odd[6 * role + j][order]
    return sp.expand(value)


def jet(eta, xi):
    def link(site, role):
        generator = cubic.ROLES[role]
        sign = cubic.sigma(site)
        zed = cubic.algebra(list(ZETA)[6 * role: 6 * role + 6])
        series = [cubic.Z4 for _ in range(cubic.N)]
        series[1] = sign * generator
        series[2] = zed
        series[3] = sign * cubic.algebra(eta[6 * role: 6 * role + 6])
        series[4] = cubic.algebra(xi[6 * role: 6 * role + 6])
        step = cubic.eye()
        out = cubic.eye()
        for k in range(1, cubic.N):
            step = cubic.smul(sp.Rational(1, k), cubic.mul(step, tuple(series)))
            out = tuple(out[i] + step[i] for i in range(cubic.N))
        return out

    cubic.link = link
    return cubic.euler_parities()


def solve_particular(operator, rhs):
    solution, _params = operator.gauss_jordan_solve(rhs)
    plugged = sp.Matrix([sp.together(entry) for entry in solution.subs(
        {symbol: 0 for symbol in solution.free_symbols}
    )])
    witness = sp.Matrix(FLAT)
    kernel = [sp.Matrix([sp.together(entry) for entry in vector]) for vector in operator.nullspace()]
    gram = sp.Matrix([[vector.dot(other) for other in kernel] for vector in kernel])
    if kernel:
        coeff = gram.LUsolve(sp.Matrix([vector.dot(plugged) for vector in kernel]))
        plugged = sp.Matrix([
            sp.together(plugged[i] - sum(coeff[j] * kernel[j][i] for j in range(len(kernel))))
            for i in range(24)
        ])
    check_dot = all(sp.together(plugged.dot(vector)) == 0 for vector in kernel)
    return plugged, kernel, check_dot, witness


def reduced_projection(eta, even_op):
    even, odd = jet(list(eta), [sp.Integer(0)] * 24)
    if any(sp.expand(odd[s][3]) != 0 for s in range(24)):
        raise AssertionError("order-3 residual")
    source = sp.Matrix([sp.expand(even[s][4]) for s in range(24)])
    xi, _kernel, _ok, _witness = solve_particular(even_op, -source)
    even2, odd2 = jet(list(eta), list(xi))
    if any(sp.expand(even2[s][4]) != 0 for s in range(24)):
        raise AssertionError("order-4 residual")
    return resonant(odd2, 5)


def main():
    _even, odd = jet([sp.Integer(0)] * 24, [sp.Integer(0)] * 24)
    check("DIRECT_KERNEL3_ZERO", resonant(odd, 3) == 0)
    source3 = sp.Matrix([sp.expand(odd[s][3]) for s in range(24)])
    odd_columns = []
    even_columns = []
    for index in range(24):
        direction = [0] * 24
        direction[index] = 1
        odd_columns.append(order5.euler_linear(direction, True))
        even_columns.append(order5.euler_linear(direction, False))
    odd_op = sp.Matrix(odd_columns).T
    even_op = sp.Matrix(even_columns).T
    witness = sp.Matrix(FLAT)
    check(
        "WITNESS_IN_LEFT_KERNEL",
        [sp.expand(sp.Matrix(column).dot(witness)) for column in odd_columns] == [0] * 24,
    )
    check("ODD_RANK_20", odd_op.rank() == 20)
    check("EVEN_RANK_24", even_op.rank() == 24)
    check("ORDER3_SOLVABLE", odd_op.rank() == odd_op.row_join(-source3).rank())
    eta, kernel, orthogonal, _witness = solve_particular(odd_op, -source3)
    check("ETA_ORTHOGONAL_TO_KERNEL", orthogonal)
    check("KERNEL_DIMENSION_4", len(kernel) == 4)
    check("BASE_KERNEL5", reduced_projection(eta, even_op) == -432)
    dots = sp.Matrix([[sp.together(vector.dot(witness)) for vector in kernel]])
    steps = []
    for coeff in dots.nullspace():
        steps.append(sum((coeff[j] * kernel[j] for j in range(len(kernel))), sp.zeros(24, 1)))
    check("THREE_WITNESS_ORTHOGONAL_DIRECTIONS", len(steps) == 3)
    for index, vector in enumerate(steps):
        check(f"STEP_{index}_KERNEL5", reduced_projection(eta + vector, even_op) == -432)
    print("RESULT_CHAIN_KERNEL5: -432")
    print("RESULT_AMPLITUDE: the order-u^5 connection equation forces u=0")
    print("BOUNDARY: period-2 chain only; not a smooth-background response NOGO")


if __name__ == "__main__":
    main()
