"""Native readout and code/conditional-confirmation sources on the transverse shear."""
from fractions import Fraction as Q

import numpy as np

from check_isochoric_source import geometry, heat, I, material_rows

interval = heat.interval


def noisy_address(values):
    # Independent canonical targets of eight controlled X gates, read by their digits.
    indices = np.arange(256)
    p = heat.P
    for bit in range(8):
        values = p * values + p.square() * values[indices ^ (1 << bit)]
    return values


def early_coefficient(weights, backward, left, right):
    values = I(np.zeros(256))
    for r in range(4):
        values = values + (2 * left[r] + right[r]) * weights[r] + right[r] * weights[r][backward[r]]
    return values * Q(1, 16)


def main():
    terms, _, prepared, _ = geometry.assemble()
    material = material_rows(terms, prepared)
    sites = [(1, 1, 2, 2), (2, 1, 1, 2)]
    ix, iy = (geometry.car.site_index(site) for site in sites)
    a = material[4*ix+2] - material[4*ix+3]
    b = material[4*iy+2] - material[4*iy+3]
    p = heat.P
    counts = geometry.car.actual_counts(heat.ROOT)
    squares = [p.square().square() * p.square() * I.rational(Q(256*n, sum(counts))) for n in counts]
    base = I([x.lo for x in squares], [x.hi for x in squares])
    rates = [I(np.zeros(256)) for _ in range(4)]
    for x, dz in [(ix, -128*b), (iy, 128*a)]:
        for role, sign in [(2, 1), (3, -1)]:
            # q_xr = w_x^2 exp(-2 s_xr)
            loc = I((np.arange(256) == x).astype(float))
            rates[role] = rates[role] - 2*sign*dz*base*loc
    backward = [[geometry.car.site_index(geometry.car.step(x, r, -1))
                 for x in geometry.car.SITES_LIST] for r in range(4)]
    left = [I.rational(Q(1, 4)), I(1.), p.square(), p.square()]
    right = [I.rational(Q(1, 4)), I(1.), p, p]
    latent = early_coefficient([base]*4, backward, left, right)
    latent_jet = early_coefficient(rates, backward, left, right)
    q, dq = noisy_address(latent), noisy_address(latent_jet)
    assert np.min(q.lo) > 0 and np.max(q.hi) < 1 and np.max(abs(dq.lo)) > 1e-7
    mean = lambda value: interval.reduce_sum(value)*Q(1, 256)
    assert mean(dq).contains(0)
    assert (mean(q) - p.square().square()*p.square()*Q(9,16)).contains(0)
    logphi = -interval.logarithm(p)
    odds = (I(1.)-q)/q
    logs = [interval.logarithm(odds[i]) for i in range(256)]
    log_odds = I([x.lo for x in logs], [x.hi for x in logs])
    info = mean(dq * log_odds)/logphi
    code_info = -info
    confirm = 2 * mean((I(1.)-2*q)*dq)
    net = code_info + confirm
    assert 1.24263e-8 < code_info.lo <= code_info.hi < 1.24264e-8
    assert -7.38635e-10 < confirm.lo <= confirm.hi < -7.38632e-10
    assert net.lo > 1.16876e-8
    threshold = -code_info / confirm
    assert 16.82 < threshold.lo <= threshold.hi < 16.83
    print('Constant tick price for zero response of these terms', float(threshold.lo), float(threshold.hi))
    for name,v in [('code minus classical information',code_info),
                   ('conditional final confirmation',confirm),('sum in unit tick',net)]:
        print(name, float(v.lo), float(v.hi))
    print('Largest certified moving conditional bit', float(np.max(dq.lo)))


if __name__ == '__main__':
    main()
