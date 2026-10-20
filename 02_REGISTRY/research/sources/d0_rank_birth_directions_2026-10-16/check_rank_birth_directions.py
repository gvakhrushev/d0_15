#!/usr/bin/env python3
"""Exact k=8 splitting of the first density derivative on the amplitude sphere.

The 28800 directions are the real coordinates of arbitrary complex maps
ker(C0) -> (im Pi)^perp. Their first density derivative is zero. The second
derivative of the density is nonzero for every nonzero vector of that space.
No physical count is produced.
"""
from __future__ import annotations

import json

import sympy as s

CHECKS: list[str] = []


def require(name: str, cond: bool) -> None:
    if not cond:
        raise ArithmeticError(name)
    CHECKS.append(name)


def eq(name: str, left, right) -> None:
    if isinstance(left, s.MatrixBase) or isinstance(right, s.MatrixBase):
        good = s.Matrix(left).equals(s.Matrix(right))
    else:
        good = s.simplify(left - right) == 0
    require(name, bool(good))


def pack(z: s.Matrix) -> list[s.Expr]:
    coords: list[s.Expr] = []
    for i in range(z.rows):
        for j in range(z.cols):
            coords.append(s.re(z[i, j]))
            coords.append(s.im(z[i, j]))
    return coords


def unpack(coords: list[s.Expr], rows: int, cols: int) -> s.Matrix:
    out = s.zeros(rows, cols)
    at = 0
    for i in range(rows):
        for j in range(cols):
            out[i, j] = coords[at] + s.I * coords[at + 1]
            at += 2
    return out


def c0_of(k: int, m: int, n: int, scale) -> s.Matrix:
    out = s.zeros(k + m, k + n)
    for i in range(k):
        out[i, i] = scale
    return out


def density_derivative(c0: s.Matrix, z: s.Matrix) -> s.Matrix:
    return z * c0.H + c0 * z.H


def hermitian_coords(h: s.Matrix) -> list[s.Expr]:
    coords: list[s.Expr] = []
    for i in range(h.rows):
        coords.append(s.re(h[i, i]))
        for j in range(i + 1, h.cols):
            coords.append(s.re(h[i, j]))
            coords.append(s.im(h[i, j]))
    return coords


def derivative_matrix(c0: s.Matrix) -> s.Matrix:
    rows, cols = c0.shape
    columns: list[list[s.Expr]] = []
    for pos in range(2 * rows * cols):
        coords = [s.Integer(0)] * (2 * rows * cols)
        coords[pos] = s.Integer(1)
        columns.append(hermitian_coords(density_derivative(c0, unpack(coords, rows, cols))))
    return s.Matrix(columns).T


def birth_basis(k: int, m: int, n: int) -> list[s.Matrix]:
    rows, cols = k + m, k + n
    basis: list[s.Matrix] = []
    for a in range(m):
        for b in range(n):
            for part in (s.Integer(1), s.I):
                z = s.zeros(rows, cols)
                z[k + a, k + b] = part
                basis.append(z)
    return basis


def right_basis(k: int, m: int, n: int, scale) -> list[s.Matrix]:
    """Real basis of Z = C0 K for K skew-Hermitian on the reference."""
    ref = k + n
    c0 = c0_of(k, m, n, scale)
    basis: list[s.Matrix] = []
    for i in range(ref):
        k_mat = s.zeros(ref)
        k_mat[i, i] = s.I
        basis.append(c0 * k_mat)
    for i in range(ref):
        for j in range(i + 1, ref):
            k_re = s.zeros(ref)
            k_re[i, j] = 1
            k_re[j, i] = -1
            k_im = s.zeros(ref)
            k_im[i, j] = s.I
            k_im[j, i] = s.I
            basis.append(c0 * k_re)
            basis.append(c0 * k_im)
    return basis


def vk_basis(k: int, m: int) -> list[s.Matrix]:
    """Real basis of trace-free Hermitian matrices with zero empty-empty block."""
    r = k + m
    basis: list[s.Matrix] = []
    for i in range(k - 1):
        h = s.zeros(r)
        h[i, i] = 1
        h[k - 1, k - 1] = -1
        basis.append(h)
    for i in range(k):
        for j in range(i + 1, k):
            h_re = s.zeros(r)
            h_re[i, j] = 1
            h_re[j, i] = 1
            h_im = s.zeros(r)
            h_im[i, j] = s.I
            h_im[j, i] = -s.I
            basis.append(h_re)
            basis.append(h_im)
    for a in range(m):
        for j in range(k):
            h_re = s.zeros(r)
            h_re[k + a, j] = 1
            h_re[j, k + a] = 1
            h_im = s.zeros(r)
            h_im[k + a, j] = s.I
            h_im[j, k + a] = -s.I
            basis.append(h_re)
            basis.append(h_im)
    return basis


def lift_amplitude(h: s.Matrix, k: int, n: int) -> s.Matrix:
    """Equation (15): occupied columns only, Hermitian square root on the diagonal block."""
    r = h.rows
    out = s.zeros(r, k + n)
    scale = s.sqrt(k)
    out[:k, :k] = scale * h[:k, :k] / 2
    out[k:, :k] = scale * h[k:, :k]
    return out


def coordinate_rank(mats: list[s.Matrix]) -> int:
    if not mats:
        return 0
    return s.Matrix([pack(mat) for mat in mats]).T.rank()


def ee_block(h: s.Matrix, k: int) -> s.Matrix:
    return s.Matrix(h[k:, k:])


def counts(shell: int, ref: int, k: int) -> dict[str, int]:
    m = shell - k
    n = ref - k
    visible = 2 * shell * k - k * k - 1
    sphere = 2 * shell * ref - 1
    kernel = sphere - visible
    right = k * k + 2 * k * n
    birth = 2 * m * n
    return {
        "shell": shell,
        "reference": ref,
        "occupied_rank": k,
        "visible_density_directions": visible,
        "sphere_dimension": sphere,
        "kernel_dimension": kernel,
        "right_unitary_directions": right,
        "rank_birth_directions": birth,
    }


def assert_splitting(k: int, m: int, n: int, scale, tag: str) -> None:
    c0 = c0_of(k, m, n, scale)
    rows, cols = c0.shape
    linear = derivative_matrix(c0)
    ambient_rank = linear.rank()
    require(f"{tag}_ambient_rank", ambient_rank == k * k + 2 * k * m)
    kernel_dim = 2 * rows * cols - ambient_rank
    right = k * k + 2 * k * n
    birth = 2 * m * n
    require(f"{tag}_kernel_dimension", kernel_dim == right + birth)

    birth_vecs = birth_basis(k, m, n)
    right_vecs = right_basis(k, m, n, scale)
    zero = s.zeros(rows)
    require(f"{tag}_birth_count", len(birth_vecs) == birth)
    # The skew-Hermitian basis has ref^2 vectors; its image under K |-> C0 K has rank `right`.
    require(f"{tag}_right_lie_count", len(right_vecs) == (k + n) ** 2)
    require(f"{tag}_right_count", coordinate_rank(right_vecs) == right)
    for z in birth_vecs + right_vecs:
        if density_derivative(c0, z) != zero:
            raise ArithmeticError(f"{tag}_summand_first_derivative")
        if s.re(s.trace(c0.H * z)) != 0:
            raise ArithmeticError(f"{tag}_summand_tangent")
    CHECKS.append(f"{tag}_summands_in_kernel")
    require(f"{tag}_direct_sum", coordinate_rank(birth_vecs + right_vecs) == kernel_dim)
    require(f"{tag}_radial_not_tangent", s.re(s.trace(c0.H * c0)) != 0)

    # Empty-occupied and Hermitian occupied-occupied directions are visible.
    visible_ea = s.zeros(rows, cols)
    visible_ea[k, 0] = 1
    require(f"{tag}_empty_occupied_is_visible", density_derivative(c0, visible_ea) != zero)
    visible_oa = s.zeros(rows, cols)
    visible_oa[0, 0] = 1
    require(f"{tag}_hermitian_occupied_is_visible", density_derivative(c0, visible_oa) != zero)

    # Every real coordinate direction has zero empty-empty density derivative.
    for pos in range(2 * rows * cols):
        coords = [s.Integer(0)] * (2 * rows * cols)
        coords[pos] = s.Integer(1)
        block = ee_block(density_derivative(c0, unpack(coords, rows, cols)), k)
        if block != s.zeros(m):
            raise ArithmeticError(f"{tag}_acceleration_ee_{pos}")
    CHECKS.append(f"{tag}_acceleration_ee_zero")

    if s.simplify(scale - 1 / s.sqrt(k)) != 0:
        return
    targets = vk_basis(k, m)
    require(f"{tag}_target_dimension", len(targets) == 2 * (k + m) * k - k * k - 1)
    lifts = [lift_amplitude(h, k, n) for h in targets]
    require(f"{tag}_lift_independent", coordinate_rank(lifts) == len(lifts))
    require(
        f"{tag}_sphere_splitting",
        coordinate_rank(lifts + birth_vecs + right_vecs) == 2 * rows * cols - 1,
    )
    for h, z in zip(targets, lifts):
        if s.expand(density_derivative(c0, z) - h) != zero:
            raise ArithmeticError(f"{tag}_lift_reproduces")
        if s.expand(s.re(s.trace(c0.H * z)) - s.trace(h) / 2) != 0:
            raise ArithmeticError(f"{tag}_lift_tangent")
    CHECKS.append(f"{tag}_lift_is_equation_15")


def second_derivative_identity() -> None:
    k = m = n = 2
    a_re = s.symbols("a0:4", real=True)
    a_im = s.symbols("b0:4", real=True)
    variables = list(a_re) + list(a_im)
    a = s.zeros(m, n)
    at = 0
    for i in range(m):
        for j in range(n):
            a[i, j] = a_re[at] + s.I * a_im[at]
            at += 1
    z = s.zeros(k + m, k + n)
    z[k:, k:] = a
    eq("birth_square_is_empty_block", s.expand(ee_block(z * z.H, k)), s.expand(a * a.H))
    trace = s.expand(s.trace(a * a.H))
    squares = sum(entry**2 for entry in variables)
    eq("birth_trace_is_sum_of_squares", trace, squares)
    poly = s.Poly(s.expand(trace), variables)
    require(
        "only_real_zero_of_birth_square",
        all(poly.coeff_monomial(var**2) == 1 for var in variables) and len(poly.terms()) == len(variables),
    )

    # Calculus identity on a smaller carrier; the empty-block cancellation is size-free.
    k = m = n = 1
    c0 = c0_of(k, m, n, 1 / s.sqrt(k))
    ar, ai = s.symbols("ar ai", real=True)
    z = s.zeros(2)
    z[1, 1] = ar + s.I * ai
    t = s.symbols("t", real=True)
    w = unpack(list(s.symbols("w0:8", real=True)), 2, 2)
    gamma = c0 + t * z + (t**2) * w / 2
    rho = s.expand(gamma * gamma.H)
    second = rho.applyfunc(lambda entry: s.diff(entry, t, 2).subs(t, 0))
    predicted = s.expand(density_derivative(c0, w) + 2 * z * z.H)
    eq("curve_second_derivative", s.expand(second - predicted), s.zeros(2))
    ee = s.expand(ee_block(second, k) - s.Matrix([[2 * (ar**2 + ai**2)]]))
    eq("curve_second_ee_independent_of_acceleration", ee, s.zeros(1))


def right_orbit_preserves_density() -> None:
    theta = s.symbols("theta", real=True)
    c0 = s.Matrix([[1, 0], [0, 0]])
    rotation = s.Matrix([[s.cos(theta), -s.sin(theta)], [s.sin(theta), s.cos(theta)]])
    curve = s.simplify(c0 * rotation)
    rho = s.simplify(curve * curve.H)
    eq("right_orbit_density_constant", rho, c0 * c0.H)
    speed = s.simplify(s.diff(curve, theta).subs(theta, 0))
    eq("right_orbit_speed_is_tangent", speed, c0 * s.Matrix([[0, -1], [1, 0]]))
    require("right_orbit_speed_nonzero", speed != s.zeros(2))


def k8_witness() -> None:
    k = 8
    shell = ref = 128
    c0 = c0_of(k, shell - k, ref - k, 1 / s.sqrt(k))
    z = s.zeros(shell, ref)
    z[k, k] = 1
    eq("k8_witness_first_derivative", density_derivative(c0, z), s.zeros(shell))
    eq("k8_witness_tangent", s.re(s.trace(c0.H * z)), 0)
    block = ee_block(z * z.H, k)
    expect = s.zeros(shell - k)
    expect[0, 0] = 1
    eq("k8_witness_second_ee", block, expect)
    eq("k8_norm", s.trace(c0.H * c0), 1)


def main() -> dict:
    arithmetic = counts(128, 128, 8)
    require("k8_kernel", arithmetic["kernel_dimension"] == 30784)
    require("k8_right", arithmetic["right_unitary_directions"] == 1984)
    require("k8_birth", arithmetic["rank_birth_directions"] == 28800)
    require(
        "k8_sum",
        arithmetic["right_unitary_directions"] + arithmetic["rank_birth_directions"]
        == arithmetic["kernel_dimension"],
    )
    require(
        "k8_sphere_sum",
        arithmetic["visible_density_directions"] + arithmetic["kernel_dimension"]
        == arithmetic["sphere_dimension"]
        == 32767,
    )
    # Same polynomials at a second occupied rank, so the k=8 evaluation is not a hardcoded triple.
    other = counts(128, 128, 4)
    require("rank4_birth_changes", other["rank_birth_directions"] == 2 * 124 * 124)
    require("rank4_not_the_k8_triple", other["kernel_dimension"] != 30784)

    assert_splitting(2, 2, 2, s.Integer(1), "shape")
    assert_splitting(1, 2, 2, s.Integer(1), "normalized_rank1")
    assert_splitting(4, 1, 1, s.Rational(1, 2), "normalized_rank4")
    second_derivative_identity()
    right_orbit_preserves_density()
    k8_witness()
    # Positive rescaling does not change the kernel: both summands stay inside it.
    c_symbol = s.symbols("c", nonzero=True)
    c0 = c0_of(2, 2, 2, c_symbol)
    for z in birth_basis(2, 2, 2)[:2] + right_basis(2, 2, 2, s.Integer(1))[:2]:
        eq("scale_keeps_kernel", density_derivative(c0, z), s.zeros(4))
    return {
        "schema": "d0-rank-birth-directions/1",
        "exact_checks": len(CHECKS),
        "counts": arithmetic,
        "source_commit": "ec45c8cc4085e7bce888d97439251be9e578d4ff",
        "source_memo_blob": "d267ba0916c83d8972f27651950e3503f0bf9d96",
        "physical_count_produced": False,
        "gravitational_equations_derived": False,
        "field_kernel_solved": False,
        "nonlinear_branch_constructed": False,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
