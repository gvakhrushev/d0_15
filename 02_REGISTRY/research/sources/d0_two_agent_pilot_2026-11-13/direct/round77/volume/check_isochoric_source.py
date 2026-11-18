"""A fixed-volume, constant-preparation-energy tangent for all 8192 thermal depths."""
from fractions import Fraction as Q
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np
from scipy import sparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round76/geometry"))
import check_invisible_geometry as geometry

heat = geometry.heat
I = heat.I


def material_rows(atoms, prepared):
    state = (prepared, np.full(prepared.shape, 5e-17))
    ac = geometry.ball_apply(geometry.matrix_ball(atoms, [1] * 16), state)
    pulls = [atom.bounded_pull(ac, state) for atom in atoms]
    # R=4096||AC||^2 and each A leg carries 1/16.
    center = 512 * sum(x for x, _ in pulls)
    error = 513 * sum(e + 6e-15 * np.abs(x) for x, e in pulls) + 1e-290
    return I(np.nextafter(center - error, -np.inf), np.nextafter(center + error, np.inf))


def mixed_source(atoms, coordinates):
    # The heat owner orders the parity blocks oppositely and uses D=64A.
    # Its source insertion is -delta D. Each 'dv' differentiates a covariant log leg.
    shape = (geometry.N, geometry.N)
    center = sparse.csr_matrix(shape)
    maximum_error = sparse.csr_matrix(shape)
    rows, columns = set(), set()
    for atom in atoms:
        weight = coordinates[atom.j]
        selected = weight != 0
        rows.update(atom.c[selected])
        columns.update(atom.r[selected])
        values = -4 * atom.dv * weight
        center += sparse.csr_matrix((values, (atom.c, atom.r)), shape=shape)
        rounding = 4 * np.abs(weight) * atom.dv_err + 6e-15 * np.abs(values)
        maximum_error += sparse.csr_matrix((rounding, (atom.c, atom.r)), shape=shape)
    # Nonnegative error matrix bounds both maximum row and column sums, including
    # accumulation of the 16 signed sparse terms; their geometric weights are dyadic
    # coordinates multiplying the bounded original source coefficients.
    assert max([maximum_error.sum(axis=axis).max() for axis in (0, 1)]) * 1.000001 < 1e-12
    center.eliminate_zeros()
    assert max(center.getnnz(axis=axis).max() for axis in (0, 1)) <= 12
    # The same support contains the exact entries even if nominal entries cancel.
    hs = float(np.linalg.norm(center.data)) + .01
    heat.frobenius_over(center.data, hs)
    nuclear = int(np.ceil(2 * np.sqrt(min(len(rows), len(columns))) * (hs + 1e-9))) + 1
    assert nuclear <= 32
    return center, nuclear


def enclosed_source(s, diagonal, left, right, nuclear):
    m0, m1 = 2 * left, 2 * right
    b = I(1.) - heat.ALPHA * I(s).square()
    weighted = I(heat.power(b, m1 - 1).lo, heat.power(b, m0 - 1).hi)
    mass = I(heat.power(b, m1).lo, heat.power(b, m0).hi)
    zhat = 2 * heat.interval.reduce_sum(mass)
    trace = 2 * heat.interval.reduce_sum(I(s) * weighted * I(diagonal))
    delta = I.rational(Q(12, 10**9))
    ez = 4096 * m1 * 10 * heat.ALPHA * delta
    z = zhat + I(-ez.hi, ez.hi)
    assert z.lo > 0
    # For the two exact self-adjoint models compare D B^k by telescoping,
    # retaining D on both sides of B-B0. For 0<=x<=1, x(1-x)^j<=1/(j+1).
    # The resulting Lipschitz factor is 1+2 sum_{q=1}^k min(25 alpha,1/q).
    # First 256 terms <=256*25 alpha. Each of the next six dyadic blocks <=1.
    assert m1 <= 16384 and (1 + 2 * (256 * 25 * heat.ALPHA + 6)).hi < 16
    lip = I(min(16., (1 + 50 * (m1 - 1) * heat.ALPHA).hi))
    et = nuclear * lip * delta + I.rational(Q(nuclear * 5 * 3, 10**9) + Q(2 * 5, 10**7))
    trace = trace + I(-et.hi, et.hi)
    beta = I(m0, m1) * heat.ALPHA
    correction = 256 * heat.ZETA * beta * 5 * nuclear * I.rational(heat.ZETA / (1 - heat.ZETA))
    value = 2 * ((I(1.) / z) - 128 * heat.ZETA * beta) * trace
    return value + I(-correction.hi, correction.hi), z


def test_pair(atoms, material, sites, legs, scale, initial_step, target):
    indices = [4 * geometry.car.site_index(site) + leg for site in sites for leg in legs]
    assert all(j in geometry.ACTIVE for j in indices)
    i, j, k, l = indices
    a, b = material[i] - material[j], material[k] - material[l]
    assert (a.lo > 0 or a.hi < 0) and (b.lo > 0 or b.hi < 0)
    u, v = (a.lo + a.hi) / 2, (b.lo + b.hi) / 2
    coordinates = np.zeros(4 * 256)
    coordinates[[i, j, k, l]] = scale * np.array([-v, v, u, -u])
    # Norm <=64 for each leg by A76. The resulting exact combination lies
    # strictly inside this bound. Separate the small error of the two input slopes.
    slope_error = scale * 2 * (max(u - a.lo, a.hi - u) + max(v - b.lo, b.hi - v)) * 1.00001
    assert np.sum(abs(coordinates)) + slope_error < .999
    assert 64 * slope_error < 1e-7
    matrix, _ = heat.operators()
    source, nuclear = mixed_source(atoms, coordinates)
    with patch.object(heat, "operators", return_value=(matrix, source)):
        spectrum, diagonal = heat.numerical_basis()
    beta_max = 16384 * heat.ALPHA
    lower_bounds = []

    def prove(left, right):
        try:
            value, z = enclosed_source(spectrum, diagonal, left, right, nuclear)
            # Both parity blocks and the resolvent in the feedback term are allowed.
            # Full trace <=2*5*64*slope_error, ||F^-1|| <=1/(1-zeta).
            factor = 2 / float(z.lo) + float((256 * heat.ZETA * beta_max / (1 - heat.ZETA)).hi)
            bound = float(value.lo) - 1.00001 * 10 * 64 * slope_error * factor - 1e-15
        except AssertionError:
            bound = -np.inf
        if bound > target:
            lower_bounds.append((left, right, bound))
            return
        assert left < right, (sites, legs, left, bound)
        mid = (left + right) // 2
        prove(left, mid)
        prove(mid + 1, right)

    left = 1
    while left <= 8192:
        right = min(8192, left + max(1, left // initial_step))
        prove(left, right)
        left = right + 1
    assert sum(r - l + 1 for l, r, _ in lower_bounds) == 8192
    print(sites, legs, "dR", (float(a.lo), float(a.hi)), (float(b.lo), float(b.hi)),
          "bins", len(lower_bounds), "least lower bound", min(x for _, _, x in lower_bounds),
          flush=True)


def main():
    d, _, prepared, _ = geometry.assemble()
    material = material_rows(d, prepared)
    test_pair(d, material, [(1, 0, 1, 1), (1, 2, 2, 2)], (1, 3), 16, 48, 0.000010)
    test_pair(d, material, [(1, 1, 2, 2), (2, 1, 1, 2)], (2, 3), 128, 48, 0.00000001)


if __name__ == "__main__":
    main()
