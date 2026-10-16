#!/usr/bin/env python3
"""Exact variation of the normal-covariance quadratic coefficient.

Candidate DRAFT. Not a gravitational claim and not a measure selection.
The Einstein pullback is quoted from the pinned record; it is not recomputed.
"""

from __future__ import annotations

import subprocess
import sys
from fractions import Fraction
from pathlib import Path

PIN = "dfaf7c8df509d5abd83fa60a185ad530feadc9b5"
ROOT = Path(__file__).resolve().parents[4]
TANGENT = 4

QUOTES = (
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        66,
        "    R=|H|^2-|B|^2.                                      (1)",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        105,
        "    c2=1/(k+2),    c4=1/[(k+2)(k+4)].",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        132,
        "    E e2(A_xi)=c2/2 sum_A[(tr A_A)^2-tr(A_A^2)]=c2 R/2.",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        234,
        "       =-integral_M G(q)^(mu nu) V_mu nu dVol_q.        (10)",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        291,
        "    (t^2/2) sum_AB Sigma_AB (H_A H_B-tr(A_A A_B)).        (12)",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        174,
        "переменные продолжают участвовать в mu и её c2,c4. Весь Riemann равен нулю,",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        247,
        "удаляется из исходной массы (5).",
    ),
    (
        "02_REGISTRY/research/A4D_RECORD_NORMAL_VOLUME_SOURCE.md",
        304,
        "      =integral[-f G^(mu nu)+nabla^mu nabla^nu f-q^(mu nu)Box f]",
    ),
    (
        "02_REGISTRY/research/A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md",
        15,
        "член исключается алгебраически ДО вариации, а не по Гауссу–Бонне.",
    ),
    (
        "02_REGISTRY/research/A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md",
        135,
        "    Q4=sum_j det A_j.                                   (6)",
    ),
    (
        "02_REGISTRY/research/A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md",
        137,
        "Это точный полином. Q4 обычно зависит от normal-frame и НЕ является",
    ),
    (
        "02_REGISTRY/research/A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md",
        170,
        "* Смена normal-frame меняет Q4, но не (8). Допустимо overcomplete",
    ),
    (
        "02_REGISTRY/research/A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md",
        170,
        "B-c R_g+2c(theta²-K²-Omega²)+4theta u(c)+Rem",
    ),
    (
        "02_REGISTRY/research/A4D_NATIVE_LORENTZ_REFLECTION_SOURCE.md",
        176,
        "source must remain. The absolute volume B also remains because the two",
    ),
)


class Quad:
    """Element a + b φ, φ=(1+√5)/2, φ^2=φ+1."""

    def __init__(self, a: Fraction | int, b: Fraction | int = 0) -> None:
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other: Quad) -> Quad:
        return Quad(self.a + other.a, self.b + other.b)

    def __sub__(self, other: Quad) -> Quad:
        return Quad(self.a - other.a, self.b - other.b)

    def __mul__(self, other: Quad | Fraction | int) -> Quad:
        if not isinstance(other, Quad):
            return Quad(self.a * Fraction(other), self.b * Fraction(other))
        # (a+bφ)(c+dφ) = ac+bd + (ad+bc+bd)φ
        return Quad(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a + self.b * other.b,
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Quad) and self.a == other.a and self.b == other.b

    def __repr__(self) -> str:
        return f"{self.a}+{self.b}*phi"


def F(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def zeros(n: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def eye(n: int) -> list[list[Fraction]]:
    out = zeros(n)
    for i in range(n):
        out[i][i] = Fraction(1)
    return out


def mat(rows: list[list[Fraction | int]]) -> list[list[Fraction]]:
    return [[F(value) for value in row] for row in rows]


def diag(*values: Fraction | int) -> list[list[Fraction]]:
    out = zeros(len(values))
    for i, value in enumerate(values):
        out[i][i] = F(value)
    return out


def add(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(left, right)]


def sub(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a - b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(left, right)]


def scale(factor: Fraction | int, matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    factor = F(factor)
    return [[factor * value for value in row] for row in matrix]


def mul(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(left)
    shared = len(left[0])
    m = len(right[0])
    if len(right) != shared:
        raise ValueError("matrix inner dimension mismatch")
    out = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(shared):
            if left[i][k] == 0:
                continue
            for j in range(m):
                out[i][j] += left[i][k] * right[k][j]
    return out


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def trace(matrix: list[list[Fraction]]) -> Fraction:
    return sum((matrix[i][i] for i in range(len(matrix))), Fraction(0))


def frobenius(left: list[list[Fraction]], right: list[list[Fraction]]) -> Fraction:
    total = Fraction(0)
    for row_a, row_b in zip(left, right):
        total += sum((a * b for a, b in zip(row_a, row_b)), Fraction(0))
    return total


def det(matrix: list[list[Fraction]]) -> Fraction:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    total = Fraction(0)
    for col in range(n):
        minor = [
            [matrix[row][j] for j in range(n) if j != col]
            for row in range(1, n)
        ]
        sign = Fraction(1) if col % 2 == 0 else Fraction(-1)
        total += sign * matrix[0][col] * det(minor)
    return total


def leading_minors_positive(matrix: list[list[Fraction]]) -> bool:
    for n in range(1, len(matrix) + 1):
        minor = [row[:n] for row in matrix[:n]]
        if det(minor) <= 0:
            return False
    return True


def shape_gram(shapes: list[list[list[Fraction]]]) -> list[list[Fraction]]:
    means = [trace(shape) for shape in shapes]
    size = len(shapes)
    gram = zeros(size)
    for i, left in enumerate(shapes):
        for j, right in enumerate(shapes):
            gram[i][j] = means[i] * means[j] - trace(mul(left, right))
    return gram


def q2(shapes: list[list[list[Fraction]]], sigma: list[list[Fraction]]) -> Fraction:
    return Fraction(1, 2) * frobenius(sigma, shape_gram(shapes))


def split_sigma(sigma: list[list[Fraction]]) -> tuple[Fraction, list[list[Fraction]]]:
    size = len(sigma)
    scalar = trace(sigma) / size
    return scalar, sub(sigma, scale(scalar, eye(size)))


def curvature(shapes: list[list[list[Fraction]]]) -> dict[str, Fraction]:
    ricci = zeros(TANGENT)
    mean_square = Fraction(0)
    bend_square = Fraction(0)
    for shape in shapes:
        mean = trace(shape)
        ricci = add(ricci, sub(scale(mean, shape), mul(shape, shape)))
        mean_square += mean * mean
        bend_square += trace(mul(shape, shape))
    scalar = trace(ricci)
    riemann_square = Fraction(0)
    for i in range(TANGENT):
        for j in range(TANGENT):
            for k in range(TANGENT):
                for ell in range(TANGENT):
                    value = Fraction(0)
                    for shape in shapes:
                        value += shape[i][k] * shape[j][ell] - shape[i][ell] * shape[j][k]
                    riemann_square += value * value
    ricci_square = trace(mul(ricci, ricci))
    euler = riemann_square - 4 * ricci_square + scalar * scalar
    return {
        "R": scalar,
        "H2": mean_square,
        "B2": bend_square,
        "E4": euler,
        "R_from_gram": trace(shape_gram(shapes)),
    }


def shape_operators(sigma: list[list[Fraction]], shapes: list[list[list[Fraction]]]) -> list[list[list[Fraction]]]:
    means = [trace(shape) for shape in shapes]
    operators = []
    for row in sigma:
        total = zeros(TANGENT)
        for weight, mean, shape in zip(row, means, shapes):
            total = add(total, scale(weight, sub(scale(mean, eye(TANGENT)), shape)))
        operators.append(total)
    return operators


def variation(
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
    d_shapes: list[list[list[Fraction]]],
    d_sigma: list[list[Fraction]],
) -> dict[str, Fraction]:
    gram = shape_gram(shapes)
    measure = Fraction(1, 2) * frobenius(d_sigma, gram)
    shape_term = Fraction(0)
    for operator, delta in zip(shape_operators(sigma, shapes), d_shapes):
        shape_term += trace(mul(operator, delta))
    scalar, traceless = split_sigma(sigma)
    d_scalar, d_traceless = split_sigma(d_sigma)
    iso_measure = (d_scalar / 2) * trace(gram)
    an_measure = Fraction(1, 2) * frobenius(d_traceless, gram)
    return {
        "dQ2": measure + shape_term,
        "measure": measure,
        "shape": shape_term,
        "iso_measure": iso_measure,
        "an_measure": an_measure,
        "c": scalar,
        "dc": d_scalar,
    }


def delta_scalar(shapes: list[list[list[Fraction]]], d_shapes: list[list[list[Fraction]]]) -> Fraction:
    total = Fraction(0)
    for shape, delta in zip(shapes, d_shapes):
        mean = trace(shape)
        total += trace(mul(sub(scale(mean, eye(TANGENT)), shape), delta))
    return 2 * total


def frame_deltas(
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
    omega: list[list[Fraction]],
) -> tuple[list[list[list[Fraction]]], list[list[Fraction]]]:
    size = len(shapes)
    d_shapes = []
    for col in range(size):
        total = zeros(TANGENT)
        for row in range(size):
            total = add(total, scale(omega[row][col], shapes[row]))
        d_shapes.append(total)
    d_sigma = sub(mul(sigma, omega), mul(omega, sigma))
    return d_shapes, d_sigma


def apply_frame(
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
    group: list[list[Fraction]],
    *,
    rotate_shapes: bool,
    rotate_sigma: bool,
) -> tuple[list[list[list[Fraction]]], list[list[Fraction]]]:
    size = len(shapes)
    new_shapes = shapes
    if rotate_shapes:
        new_shapes = []
        for col in range(size):
            total = zeros(TANGENT)
            for row in range(size):
                total = add(total, scale(group[row][col], shapes[row]))
            new_shapes.append(total)
    new_sigma = sigma
    if rotate_sigma:
        new_sigma = mul(transpose(group), mul(sigma, group))
    return new_shapes, new_sigma


def cubic_linear_coeff(samples: list[Fraction]) -> Fraction:
    """Linear coefficient of a cubic sampled at 0,1,2,3."""
    p0, p1, p2, p3 = samples
    r1, r2, r3 = p1 - p0, p2 - p0, p3 - p0
    d_coeff = (r3 - 3 * r1) / 6 - (r2 - 2 * r1) / 2
    c_coeff = (r2 - 2 * r1) / 2 - 3 * d_coeff
    return r1 - c_coeff - d_coeff


def polynomial_variation(
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
    d_shapes: list[list[list[Fraction]]],
    d_sigma: list[list[Fraction]],
) -> Fraction:
    samples = []
    for step in range(4):
        moved_shapes = [add(shape, scale(step, delta)) for shape, delta in zip(shapes, d_shapes)]
        moved_sigma = add(sigma, scale(step, d_sigma))
        samples.append(q2(moved_shapes, moved_sigma))
    return cubic_linear_coeff(samples)


def e2(shape: list[list[Fraction]]) -> Fraction:
    mean = trace(shape)
    return Fraction(1, 2) * (mean * mean - trace(mul(shape, shape)))


def expect_det(shapes: list[list[list[Fraction]]], c4: Fraction) -> Fraction:
    """Isotropic fourth-moment contraction. Not valid for a traceless Σ."""
    size = len(shapes)
    total = Fraction(0)
    for a in range(size):
        for b in range(size):
            for c in range(size):
                for d in range(size):
                    moment = 0
                    if a == b and c == d:
                        moment += 1
                    if a == c and b == d:
                        moment += 1
                    if a == d and b == c:
                        moment += 1
                    if moment == 0:
                        continue
                    chosen = (a, b, c, d)
                    rows = [
                        [shapes[chosen[col]][row][col] for col in range(TANGENT)]
                        for row in range(TANGENT)
                    ]
                    total += (c4 * moment) * det(rows)
    return total


def q4_sum(shapes: list[list[list[Fraction]]]) -> Fraction:
    return sum((det(shape) for shape in shapes), Fraction(0))


def ball_moments(carrier: int) -> tuple[Fraction, Fraction]:
    c2 = Fraction(1, carrier + 2)
    c4 = Fraction(1, (carrier + 2) * (carrier + 4))
    return c2, c4


def git_show(path: str) -> list[str]:
    text = subprocess.check_output(
        ["git", "show", f"{PIN}:{path}"],
        cwd=ROOT,
        text=True,
    )
    return text.splitlines()


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.witness: list[str] = []

    def check(self, condition: bool, name: str) -> None:
        if not condition:
            self.failures.append(name)

    def note(self, key: str, value: object) -> None:
        self.witness.append(f"{key}={value}")


def require_same_variation(
    report: Report,
    name: str,
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
    d_shapes: list[list[list[Fraction]]],
    d_sigma: list[list[Fraction]],
) -> Fraction:
    analytic = variation(shapes, sigma, d_shapes, d_sigma)["dQ2"]
    sampled = polynomial_variation(shapes, sigma, d_shapes, d_sigma)
    report.check(analytic == sampled, name)
    return analytic


def fixture_matrices() -> tuple[list[list[Fraction]], list[list[Fraction]], list[list[Fraction]]]:
    # Same three matrices as the pinned normal-volume checker. Not a new shape law.
    first = diag(1, 2, 3, 4)
    second = mat(
        [
            [2, 1, 0, 1],
            [1, -1, 2, 0],
            [0, 2, 3, 1],
            [1, 0, 1, 2],
        ]
    )
    third = mat(
        [
            [0, 1, 1, 0],
            [1, 2, 0, 1],
            [1, 0, -1, 2],
            [0, 1, 2, 1],
        ]
    )
    return first, second, third


def plane_rotation() -> list[list[Fraction]]:
    return mat([[Fraction(3, 5), Fraction(-4, 5)], [Fraction(4, 5), Fraction(3, 5)]])


def embed_rotation(size: int) -> list[list[Fraction]]:
    group = eye(size)
    block = plane_rotation()
    for i in range(2):
        for j in range(2):
            group[i][j] = block[i][j]
    return group


def plane_generator(size: int) -> list[list[Fraction]]:
    omega = zeros(size)
    omega[0][1] = Fraction(1)
    omega[1][0] = Fraction(-1)
    return omega


def check_quotes(report: Report) -> None:
    for path, line, text in QUOTES:
        rows = git_show(path)
        report.check(1 <= line <= len(rows) and rows[line - 1] == text, f"quote:{path}:{line}")
    checker = git_show(
        "02_REGISTRY/research/sources/d0_record_normal_volume_2026-10-15/check_normal_volume.py"
    )
    report.check(any(row.strip() == "B1 = s.diag(1,2,3,4)" for row in checker), "pinned fixture B1")
    claims = (ROOT / "02_REGISTRY" / "claims.csv").read_text(encoding="utf-8")
    report.check(
        "FALSIFIABLE ANISOTROPY: zones 9!=11!=13" in claims,
        "rank3 anisotropy is a different carrier",
    )
    report.check("q-(Arf1) anisotropic" in claims, "Q8 anisotropy is a different carrier")
    report.check(
        "No canonical K, no coefficient c, no metric star, no Lorentz covariance, no stress conservation, no Einstein equation"
        in claims,
        "cell-energy claim does not select Einstein",
    )


def check_algebra(report: Report) -> None:
    probe = [Fraction(7), Fraction(16), Fraction(41), Fraction(94)]  # 7+5e+3e^2+e^3
    report.check(cubic_linear_coeff(probe) == 5, "cubic solver")
    phi = Quad(0, 1)
    report.check(phi * phi == Quad(1, 1), "phi square")
    phi4 = Quad(2, 3)
    phi2 = Quad(1, 1)
    p3 = Quad(-3, 2)
    report.check((phi4 - phi2) * p3 == Quad(1, 0), "p^3(phi^4-phi^2)=1")
    sphere = [eye(TANGENT)]
    curv = curvature(sphere)
    report.check(curv["R"] == 12 and curv["E4"] == 24, "unit sphere curvature")
    report.check(curv["R"] == curv["H2"] - curv["B2"] == curv["R_from_gram"], "scalar contraction")
    report.check(expect_det(sphere, Fraction(1)) == 3, "sphere fourth moment")
    report.check(expect_det(sphere, Fraction(1, 15)) == Fraction(1, 5), "ball c4 on the sphere")


def check_definition(
    report: Report,
    name: str,
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
) -> dict[str, Fraction]:
    report.check(all(shape == transpose(shape) for shape in shapes), f"{name}:symmetric shapes")
    report.check(sigma == transpose(sigma) and leading_minors_positive(sigma), f"{name}:psd")
    gram = shape_gram(shapes)
    report.check(gram == transpose(gram), f"{name}:S symmetric")
    size = len(shapes)
    for i in range(size):
        report.check(e2(shapes[i]) * 2 == gram[i][i], f"{name}:diagonal e2")
        for j in range(i + 1, size):
            paired = e2(add(shapes[i], shapes[j])) - e2(shapes[i]) - e2(shapes[j])
            report.check(paired == gram[i][j], f"{name}:polarization")
    curv = curvature(shapes)
    report.check(curv["R"] == curv["H2"] - curv["B2"] == trace(gram), f"{name}:Gauss scalar")
    scalar, traceless = split_sigma(sigma)
    value = q2(shapes, sigma)
    isotropic = (scalar / 2) * curv["R"]
    anisotropic = Fraction(1, 2) * frobenius(traceless, gram)
    report.check(value == isotropic + anisotropic, f"{name}:split")
    report.check(trace(traceless) == 0, f"{name}:traceless")
    report.note(f"{name}.R", curv["R"])
    report.note(f"{name}.E4", curv["E4"])
    report.note(f"{name}.Q4", q4_sum(shapes))
    report.note(f"{name}.Q2", value)
    report.note(f"{name}.Q2_iso", isotropic)
    report.note(f"{name}.Q2_an", anisotropic)
    report.note(f"{name}.c", scalar)
    return {"Q2": value, "Q2_iso": isotropic, "Q2_an": anisotropic, "R": curv["R"], "E4": curv["E4"]}


def check_frame(
    report: Report,
    name: str,
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
) -> None:
    group = embed_rotation(len(shapes))
    report.check(mul(transpose(group), group) == eye(len(shapes)), f"{name}:rotation orthogonal")
    both_shapes, both_sigma = apply_frame(shapes, sigma, group, rotate_shapes=True, rotate_sigma=True)
    only_shapes, _ = apply_frame(shapes, sigma, group, rotate_shapes=True, rotate_sigma=False)
    only_sigma_shapes, only_sigma = apply_frame(
        shapes, sigma, group, rotate_shapes=False, rotate_sigma=True
    )
    before = check_definition(report, name, shapes, sigma)
    after = check_definition(report, f"{name}.both", both_shapes, both_sigma)
    shapes_only = check_definition(report, f"{name}.A_only", only_shapes, sigma)
    sigma_only = check_definition(report, f"{name}.Sigma_only", only_sigma_shapes, only_sigma)
    report.check(before["Q2"] == after["Q2"] == after["Q2_iso"] + after["Q2_an"], f"{name}:joint invariant")
    report.check(before["R"] == after["R"] == shapes_only["R"] == sigma_only["R"], f"{name}:R frame invariant")
    report.check(before["E4"] == after["E4"] == shapes_only["E4"], f"{name}:E4 frame invariant")
    report.check(before["Q2_iso"] == shapes_only["Q2_iso"] == sigma_only["Q2_iso"], f"{name}:isotropic label invariant")
    # Decisive: rotating A without Sigma moves only the anisotropic remainder.
    report.check(shapes_only["Q2"] != before["Q2"], f"{name}:rotate A without Sigma changes Q2")
    report.check(shapes_only["Q2_an"] != before["Q2_an"], f"{name}:rotate A without Sigma changes remainder")
    report.check(q4_sum(only_shapes) != q4_sum(shapes), f"{name}:rotate A changes Q4")
    report.check(sigma_only["Q2"] != before["Q2"], f"{name}:rotate Sigma without A changes Q2")
    report.check(q4_sum(only_sigma_shapes) == q4_sum(shapes), f"{name}:Sigma rotation keeps Q4")

    omega = plane_generator(len(shapes))
    d_shapes, d_sigma = frame_deltas(shapes, sigma, omega)
    joint = require_same_variation(report, f"{name}:joint frame derivative", shapes, sigma, d_shapes, d_sigma)
    frozen = require_same_variation(
        report,
        f"{name}:frozen dSigma derivative",
        shapes,
        sigma,
        d_shapes,
        zeros(len(shapes)),
    )
    parts = variation(shapes, sigma, d_shapes, d_sigma)
    gram = shape_gram(shapes)
    commutator = sub(mul(sigma, gram), mul(gram, sigma))
    predicted = Fraction(1, 2) * trace(mul(omega, commutator))
    report.check(joint == 0, f"{name}:joint frame derivative vanishes")
    report.check(frozen != 0, f"{name}:frozen dSigma is visible")
    report.check(frozen == parts["shape"] == predicted, f"{name}:frozen equals commutator")
    report.check(parts["measure"] == -predicted, f"{name}:measure cancels frame")
    report.note(f"{name}.frozen_dQ2", frozen)
    zero_dc = zeros(len(shapes))
    pure_c = require_same_variation(report, f"{name}:dc", shapes, sigma, zero_shapes_like(shapes), eye(len(shapes)))
    report.check(pure_c == before["R"] / 2, f"{name}:dc pairs with R/2")


def zero_shapes_like(shapes: list[list[list[Fraction]]]) -> list[list[list[Fraction]]]:
    return [zeros(TANGENT) for _ in shapes]


def check_shape_chain(report: Report, name: str, shapes: list[list[list[Fraction]]], sigma: list[list[Fraction]]) -> None:
    d_shapes = [eye(TANGENT)] + zero_shapes_like(shapes)[1:]
    delta = require_same_variation(report, f"{name}:shape chain", shapes, sigma, d_shapes, zeros(len(shapes)))
    d_r = delta_scalar(shapes, d_shapes)
    scalar, _ = split_sigma(sigma)
    iso = (scalar / 2) * d_r
    report.check(delta != iso, f"{name}:anisotropic shape response is not (c/2) dR")
    report.note(f"{name}.shape_dQ2", delta)
    report.note(f"{name}.iso_shape_dQ2", iso)


def cylinder_contrast(alpha: Quad, beta: Quad) -> Quad:
    phi4 = Quad(2, 3)
    phi2 = Quad(1, 1)
    return (phi4 - phi2) * alpha


def check_cylinder_not_gb(report: Report, shapes: list[list[list[Fraction]]]) -> None:
    curv = curvature(shapes)
    quartic = q4_sum(shapes)
    report.check(quartic != 0 and quartic != curv["E4"], "Q4 is not E4")
    group = embed_rotation(len(shapes))
    rotated, _ = apply_frame(shapes, eye(len(shapes)), group, rotate_shapes=True, rotate_sigma=False)
    report.check(q4_sum(rotated) != quartic, "Q4 moves")
    report.check(curvature(rotated)["E4"] == curv["E4"], "E4 does not move")
    c2, c4 = ball_moments(len(shapes))
    continuous = c4 * curv["E4"] / 8
    cylinder = Quad(-3, 2) * (2 * quartic)  # 2 p^3 Q4
    report.check(cylinder != Quad(continuous, 0), "continuous fourth law is not the cylinder coefficient")
    alpha = Quad(-3, 2) * curv["R"]
    beta = cylinder
    report.check(cylinder_contrast(alpha, beta) == Quad(curv["R"], 0), "cylinder contrast cancels every quartic")
    # The same algebraic cancellation still returns R after Q4 moves. Invariance is not Gauss-Bonnet.
    alpha_rot = Quad(-3, 2) * curvature(rotated)["R"]
    beta_rot = Quad(-3, 2) * (2 * q4_sum(rotated))
    report.check(beta_rot != beta, "rotated cylinder quartic differs")
    report.check(cylinder_contrast(alpha_rot, beta_rot) == Quad(curv["R"], 0), "contrast survives the Q4 motion")
    report.check(expect_det(shapes, c4) == continuous, "isotropic fourth moment owns E4/8, not sum det")
    report.note("cylinder.Q4", quartic)
    report.note("cylinder.Q4_rotated", q4_sum(rotated))
    report.note("cylinder.E4", curv["E4"])
    report.note("cylinder.continuous_t4", continuous)
    report.note("cylinder.c2R_over_2", (c2 / 2) * curv["R"])
    report.note("sphere_like_Q2_uses_c2_not_p3", True)


def check_scalar_isotropic_zero(report: Report, active: list[list[list[Fraction]]]) -> None:
    curv = curvature(active)
    report.check(curv["R"] != 0 and curv["E4"] != 0, "controls have curvature")
    scalar_sigma = scale(5, eye(len(active)))
    scalar = check_definition(report, "scalar", active, scalar_sigma)
    report.check(scalar["Q2_an"] == 0 and scalar["Q2"] == Fraction(5, 2) * curv["R"], "scalar remainder vanishes")
    group = embed_rotation(len(active))
    rotated, _ = apply_frame(active, scalar_sigma, group, rotate_shapes=True, rotate_sigma=False)
    report.check(q2(rotated, scalar_sigma) == scalar["Q2"], "scalar Q2 is frame-blind")
    # Freezing dc drops a real isotropic term. This is silent if the test only rotates frames.
    frozen_dc = variation(active, scalar_sigma, zero_shapes_like(active), zeros(len(active)))["dQ2"]
    full_dc = variation(active, scalar_sigma, zero_shapes_like(active), eye(len(active)))["dQ2"]
    report.check(frozen_dc == 0 and full_dc == curv["R"] / 2, "scalar detects frozen dc")

    c2, c4 = ball_moments(len(active))
    isotropic_sigma = scale(c2, eye(len(active)))
    isotropic = check_definition(report, "isotropic", active, isotropic_sigma)
    report.check(isotropic["Q2_an"] == 0 and isotropic["Q2"] == (c2 / 2) * curv["R"], "ball Q2")
    report.check(expect_det(active, c4) == c4 * curv["E4"] / 8, "ball fourth moment")
    report.check(q4_sum(active) != curv["E4"] / 8, "sum of dets is not E4/8")
    d_shapes, _ = frame_deltas(active, isotropic_sigma, plane_generator(len(active)))
    silent = variation(active, isotropic_sigma, d_shapes, zeros(len(active)))["dQ2"]
    report.check(silent == 0, "isotropic frame defect is silent; it cannot police anisotropy")

    explicit = active + [zeros(TANGENT)]
    report.check(curvature(explicit)["R"] == curv["R"], "explicit zero shape keeps R")
    report.check(q4_sum(explicit) == q4_sum(active), "explicit zero shape keeps Q4")
    old_c2, old_c4 = ball_moments(3)
    new_c2, new_c4 = ball_moments(2)
    kept = (old_c2 / 2) * curv["R"]
    reduced = (new_c2 / 2) * curv["R"]
    report.check(kept != reduced, "delete zero direction and keep old c2 changes Q2")
    report.check(old_c4 * curv["E4"] / 8 != new_c4 * curv["E4"] / 8, "old c4 is not the reduced ball")
    report.note("zero.c2_old", old_c2)
    report.note("zero.c2_new", new_c2)
    report.note("zero.Q2_old", kept)
    report.note("zero.Q2_new", reduced)
    report.note("zero.c4E4_old", old_c4 * curv["E4"] / 8)
    report.note("zero.c4E4_new", new_c4 * curv["E4"] / 8)

    # Variance on the zero slot does not change Q2, but it changes the isotropic label.
    padded = mat([[3, 0, 0], [0, 1, 0], [0, 0, 5]])
    reduced_sigma = mat([[3, 0], [0, 1]])
    report.check(q2(explicit, padded) == q2(active, reduced_sigma), "zero-slot variance misses S")
    full_split = check_definition(report, "zero_slot", explicit, padded)
    reduced_split = check_definition(report, "zero_slot_reduced", active, reduced_sigma)
    report.check(full_split["Q2"] == reduced_split["Q2"], "deletion keeps the quadratic number")
    report.check(full_split["Q2_iso"] != reduced_split["Q2_iso"], "deletion relabels isotropic versus anisotropic")
    report.note("zero_slot.Q2_iso_full", full_split["Q2_iso"])
    report.note("zero_slot.Q2_iso_reduced", reduced_split["Q2_iso"])

    wide_c2, wide_c4 = ball_moments(572)
    narrow_c2, narrow_c4 = ball_moments(2)
    report.check((wide_c2 / 2) * curv["R"] != (narrow_c2 / 2) * curv["R"], "k=572 to k=2 keeps neither c2")
    report.check(wide_c4 != narrow_c4, "k=572 to k=2 keeps neither c4")
    report.note("carrier572.Q2", (wide_c2 / 2) * curv["R"])
    report.note("carrier2.Q2", (narrow_c2 / 2) * curv["R"])


def conditional_stress(
    shapes: list[list[list[Fraction]]],
    sigma: list[list[Fraction]],
    *,
    factor: str | None,
    dc: Fraction,
    omega_present: bool,
) -> str | None:
    """A spacetime label is emitted only for the quoted isotropic record pullback."""
    if factor != "record_theorem_B_fixed_c":
        return None
    _, traceless = split_sigma(sigma)
    if any(value != 0 for row in traceless for value in row):
        return None
    if dc != 0 or omega_present:
        return None
    return "conditional_record_pullback_not_matter"


def check_stress_gate(report: Report, shapes: list[list[list[Fraction]]], sigma: list[list[Fraction]]) -> None:
    report.check(
        conditional_stress(shapes, sigma, factor=None, dc=Fraction(0), omega_present=False) is None,
        "no factorization means no stress",
    )
    report.check(
        conditional_stress(shapes, sigma, factor="record_theorem_B_fixed_c", dc=Fraction(0), omega_present=False)
        is None,
        "anisotropic packet is not a stress",
    )
    report.check(
        conditional_stress(shapes, sigma, factor="record_theorem_B_fixed_c", dc=Fraction(1), omega_present=False)
        is None,
        "moving c is not the fixed record pullback",
    )
    scalar_sigma = scale(5, eye(len(shapes)))
    report.check(
        conditional_stress(shapes, scalar_sigma, factor="record_theorem_B_fixed_c", dc=Fraction(0), omega_present=False)
        == "conditional_record_pullback_not_matter",
        "isotropic fixed-c pullback stays conditional",
    )
    report.check(
        conditional_stress(shapes, scalar_sigma, factor="record_theorem_B_fixed_c", dc=Fraction(0), omega_present=True)
        is None,
        "frame motion blocks the fixed pullback",
    )


def main() -> int:
    report = Report()
    check_quotes(report)
    check_algebra(report)
    first, second, third = fixture_matrices()
    report.check(mul(first, second) != mul(second, first), "fixture two does not commute")
    report.check(mul(second, third) != mul(third, second), "fixture three does not commute")
    fixture_two = [first, second]
    fixture_three = [first, second, third]
    sigma_two = mat([[2, Fraction(1, 2)], [Fraction(1, 2), 1]])
    sigma_three = mat([[2, 1, 0], [1, 2, 1], [0, 1, 2]])
    check_frame(report, "two", fixture_two, sigma_two)
    check_frame(report, "three", fixture_three, sigma_three)
    check_shape_chain(report, "two", fixture_two, sigma_two)
    check_shape_chain(report, "three", fixture_three, sigma_three)
    check_cylinder_not_gb(report, fixture_two)
    check_scalar_isotropic_zero(report, fixture_two)
    check_stress_gate(report, fixture_two, sigma_two)

    # Record (12) is the excess over an isotropic moment, not a second copy of it.
    excess = mat([[1, Fraction(1, 2)], [Fraction(1, 2), 0]])
    c2, _ = ball_moments(2)
    full = add(scale(c2, eye(2)), excess)
    report.check(
        q2(fixture_two, full) == q2(fixture_two, scale(c2, eye(2))) + q2(fixture_two, excess),
        "excess adds once",
    )
    report.note("record12.Q2_excess", q2(fixture_two, excess))
    memo = (
        ROOT
        / "02_REGISTRY/research/sources/d0_medium_anisotropic_normal_source_2026-10-16/RESULT_RU.md"
    ).read_text(encoding="utf-8")
    for token in (
        "Q2 = (1/2) ∑_{A,B} Σ_AB S_AB",
        "δQ2|_{δΣ=0} = (1/2) tr(ω [Σ, S])",
        "187/2",
        "2483/50",
        "-146/25",
        "192/25",
        "-10",
        "81",
        "37/5",
        "37/4",
        "37/574",
        "-12556/625",
        "113/2",
        "conditional_record_pullback_not_matter",
        "stress: covector_only",
    ):
        report.check(token in memo, f"memo cites {token}")

    for line in report.witness:
        print(line)
    if report.failures:
        print(f"FAIL {len(report.failures)}")
        for name in report.failures:
            print(name)
        return 1
    print("PASS anisotropic normal covariance variation")
    print("stress: covector_only")
    print("defects_detected: rotate_A_without_Sigma freeze_dSigma delete_zero_keep_c2_c4 Q4_not_Gauss_Bonnet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
