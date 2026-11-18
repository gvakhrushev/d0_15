"""Primary L4 vacuum, all prior-preserving real gates on one unrestricted SITE bit."""
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np
from scipy import sparse

DIRECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DIRECT / "round76/geometry"))
sys.path.insert(0, str(DIRECT / "round75/history"))
import check_invisible_geometry as geometry
import check_two_site_source as sites

I = geometry.heat.I
reduce_sum = geometry.heat.interval.reduce_sum


def split_ball(value):
    center = value.lo + (value.hi - value.lo) / 2
    error = np.maximum(center - value.lo, value.hi - center)
    return center, np.nextafter(error, np.inf)


def inner(b1, b2):
    x, ex = b1
    y, ey = b2
    ix = I(np.nextafter(x-ex, -np.inf), np.nextafter(x+ex, np.inf))
    iy = I(np.nextafter(y-ey, -np.inf), np.nextafter(y+ey, np.inf))
    return reduce_sum(ix * iy)


def geometry_derivative(terms, a, b):
    """h=1/4; scales of the two covariant Weyl derivatives are 1/a, -1/b."""
    weights = np.zeros(1024)
    errors = np.zeros(1024)
    for site, sign, coefficient in ((sites.SITE_A, 1, a), (sites.SITE_B, -1, b)):
        start = 4 * geometry.car.site_index(site)
        value = I(float(sign)) / coefficient
        weights[start:start+4], errors[start:start+4] = split_ball(value)
    matrices, radii = [], []
    for t in terms:
        w = weights[t.j]
        dw = errors[t.j]
        vals = 4 * t.dv * w
        rad = 4 * (t.dv_err * (np.abs(w) + dw) + np.abs(t.dv) * dw)
        rad += 5e-15 * np.abs(vals)
        for data, output in ((vals, matrices), (rad, radii)):
            output.append(sparse.csr_matrix((data, (t.r, t.c)), shape=(geometry.N, geometry.N)))
    return sum(matrices), sum(radii) * 1.000001 + 5e-15 * sum(abs(m) for m in matrices)


def min_rotation(A, B, W):
    squares = (A-W).square() + 4*B.square()
    gap = I(np.maximum(0., squares.lo), squares.hi).sqrt()
    return (A+W-gap)/2, gap


def angle_power(k, p):
    def compose(x, y):
        c, s = x
        d, t = y
        return c*d-s*t, c*t+s*d
    result = (I(1.), I(0.))
    power = (p.sqrt(), p)
    while k:
        if k % 2:
            result = compose(result, power)
        k //= 2
        if k:
            power = compose(power, power)
    return result


def limits(x):
    return [float(x.lo), float(x.hi)]


def main():
    terms, _, original, _ = geometry.assemble()
    originals = original.reshape(256, 8, 128)
    numerator = np.array(geometry.car.fourier_numerators(), dtype=np.int64)
    assert np.all(np.sum(numerator**2, axis=1) == 64)
    a, b = sites.material_coefficients()
    geom = geometry.matrix_ball(terms, [1]*16)
    operator = geom[0]*64, geom[1]*64
    derivative = geometry_derivative(terms, a, b)
    real = lambda x: (x.reshape(original.shape), np.full(original.shape, 5e-17))
    index = np.arange(256)
    minima = {}
    winner = None
    for bit in range(8):
        hop = index ^ (1 << bit)
        overlaps = np.sum(numerator * numerator[hop], axis=1)
        neutral = np.all(overlaps == 0)
        assert neutral == (bit in (0, 3, 5))
        sign = np.where(index & (1 << bit), 1., -1.)[:, None, None]
        for det in (1, -1):
            base = originals if det == 1 else -sign * originals
            quad = sign * base[hop]
            x = geometry.ball_apply(operator, real(base))
            y = geometry.ball_apply(operator, real(quad))
            A, B, W = inner(x, x), inner(x, y), inner(y, y)
            if neutral:
                value, gap = min_rotation(A, B, W)
            else:
                value = I(np.minimum(A.lo, W.lo), np.minimum(A.hi, W.hi))
            minima[bit, det] = value
            if bit == 5 and det == 1:
                assert gap.lo > 0.65
                xp = geometry.ball_apply(derivative, real(base))
                yp = geometry.ball_apply(derivative, real(quad))
                dA, dB, dW = 2*inner(x, xp), inner(x, yp)+inner(xp, y), 2*inner(y, yp)
                envelope = (dA+dW-((A-W)*(dA-dW)+4*B*dB)/gap)/2
                assert dA.contains(0)
                assert -0.00149333 < envelope.lo <= envelope.hi < -0.00149330
                assert -0.03414258 < (2*B).lo <= (2*B).hi < -0.03414256
                c1, s1 = angle_power(1, geometry.heat.P)
                one_word = dA*c1.square() + 2*dB*c1*s1 + dW*s1.square()
                assert -0.06976828 < one_word.lo <= one_word.hi < -0.06976826
                heat1_upper = I.rational(Fraction(9473, 100_000_000))/(a*b)
                heat424_lower = I.rational(Fraction(321205, 100_000_000))/(a*b)
                assert (one_word + heat1_upper).hi < -0.04771
                assert (one_word + heat424_lower).lo > 0.6778
                c, s = angle_power(283, geometry.heat.P)
                descent = (W-A)*s.square() + 2*B*c*s
                finite_jet = dA*c.square() + 2*dB*c*s + dW*s.square()
                assert -0.00302763 < finite_jet.lo <= finite_jet.hi < -0.00302760
                print("one-gate geometry jet", limits(one_word), "283-gate geometry jet", limits(finite_jet))
                assert -0.00005353 < descent.lo <= descent.hi < -0.00005352
                heat_bound = I.rational(Fraction(9472, 100_000_000)) / (a*b)
                assert (heat_bound + envelope).lo > 0.0205529
                winner = value
                print("original R", limits(A), "angle source", limits(2*B),
                      "G^283 change", limits(descent), "optimized R", limits(value),
                      "envelope on normalized V", limits(envelope),
                      "all heat depths remaining >", float((heat_bound + envelope).lo))
    assert 6.85614531 < winner.lo <= winner.hi < 6.85614534
    assert min(v.lo for (bit, det), v in minima.items() if bit != 5) > 6.85642079
    # X_5 translates v by two cells. Fourier covariances are translation invariant.
    projector = numerator @ numerator.T
    permuted = index ^ 32
    assert np.array_equal(projector, projector[np.ix_(permuted, permuted)])
    print("minimum by bit, all allowed determinant signs:",
          [min(v.lo for (j, det), v in minima.items() if j == bit) for bit in range(8)])


if __name__ == "__main__":
    main()
