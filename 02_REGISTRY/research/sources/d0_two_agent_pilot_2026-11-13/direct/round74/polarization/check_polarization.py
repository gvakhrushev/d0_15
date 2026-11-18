"""Two CAR preparations with identical Einstein stress on the A73 collar."""
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round73" / "matter"))
import check_matter_root as owner


def check(ok, why):
    if not ok:
        raise ValueError(why)


def bound_distance(y, matrix, vector_error, matrix_error, lower, upper):
    """Enclose the distance to the true column space using rational arithmetic."""
    gram = matrix.T * matrix
    inverse = gram.inv()
    # Positive definite Gram. Its inverse is symmetric, so the maximum row
    # sum bounds its spectral norm. Round the resulting singular bound down.
    inf_norm = max(sum(abs(inverse[i, j]) for j in range(gram.cols)) for i in range(gram.rows))
    singular_lower = sp.floor(sp.sqrt(1 / inf_norm))
    check(singular_lower > matrix_error, "perturbed columns may be dependent")
    coefficients = inverse * matrix.T * y
    residual = y - matrix * coefficients
    distance2 = residual.dot(residual)
    true_coeff_bound = 2 * (sp.ceiling(sp.sqrt(y.dot(y))) + vector_error) / (singular_lower - matrix_error)
    lower_error = vector_error + matrix_error * true_coeff_bound
    upper_error = vector_error + matrix_error * sp.ceiling(sp.sqrt(coefficients.dot(coefficients)))
    # Physical field rows have scale 1/350272 per unit raw boundary amplitude.
    check(distance2 > (350272 * lower + lower_error) ** 2, "lower distance")
    check(350272 * upper > upper_error, "upper bound sign")
    check(distance2 < (350272 * upper - upper_error) ** 2, "upper distance")


def main():
    sites = owner.SITES
    active = [i for i, (u, v, x, y) in enumerate(sites) if u in (1, 2) and x in (1, 2) and y in (1, 2)]
    n = len(active)
    check(n == 32, "A73 domain")
    modes = sp.zeros(len(sites), 2)
    for i in active:
        u, v, x, y = sites[i]
        modes[i, 0] = (-1) ** v
        modes[i, 1] = (-1) ** (u + v + x + y)
    columns = []
    for i in active:
        delta = [0] * len(sites)
        delta[i] = 1
        columns.append([owner.wave_equation(delta, j) for j in active])
    wave = sp.Matrix(columns).T
    check(wave.rank() == 30 and modes.rank() == 2 and wave * modes[active, :] == sp.zeros(n, 2),
          "zero-boundary wave modes")
    profile = sp.Matrix([owner.core.B(site) for site in sites])
    check(all(owner.wave_equation(profile, i) == 0 for i in active), "inhomogeneous target")
    approximations = owner.blocks("rational")
    scalar = sp.Matrix(approximations[0])[active, :]
    top = sp.Matrix(approximations[15])[active, :]
    split = scalar - top
    # Single-entry enclosure from the A73 radical bounds (all matrix entries).
    unit = sp.Rational(1, owner.SCALE)
    gram_error = 64 * 128**2 * 19 * unit
    gram_bound = 64 * 128**2 * 81
    epsilon = sp.Rational(1, 10**7)
    check(gram_error + 256 * (3 * gram_error + gram_bound * unit) < epsilon, "source error")
    profile_l1 = sum(abs(x) for x in profile)
    mode_l1 = max(sum(abs(x) for x in modes[:, j]) for j in range(modes.cols))

    # Full entrywise sums overbound the Euclidean and induced operator errors.
    R = sp.Rational
    bound_distance(split * profile, split * modes,
                   n * 2 * epsilon * profile_l1,
                   n * 2 * 2 * epsilon * mode_l1, R("0.04327"), R("0.04329"))
    nuisance = (scalar * modes).row_join(top * modes).row_join(split * profile)
    bound_distance(top * profile, nuisance,
                   n * epsilon * profile_l1,
                   n * epsilon * (4 * mode_l1 + 2 * profile_l1), R("0.02238"), R("0.02240"))

    # Independent check of the swap/rotation algebra, without fitting a field response.
    a, b, k0, k4, p = sp.symbols("a b k0 k4 p", real=True)
    cos, sin = sp.Rational(3, 5), sp.Rational(4, 5)
    rotated = k0 * (cos*a-sin*b)**2 + k4 * (sin*a+cos*b)**2
    ortho = k0 * (sin*a+cos*b)**2 + k4 * (cos*a-sin*b)**2
    check(sp.expand(rotated + ortho - (k0+k4)*(a*a+b*b)) == 0, "orthogonal average")
    check(sp.expand((p*p-(cos*a-sin*b)**2-(sin*a+cos*b)**2)-(p*p-a*a-b*b)) == 0,
          "full preparation reserve")
    print("PASS |polarization difference| > 0.04327; |source after global mixing| > 0.02238")


if __name__ == "__main__":
    main()
