"""Absolute calibration and normalization-free economic target at three actual lengths."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round75/work"))
import check_pointer_weyl as owner

O, I = owner.O, owner.I


def main():
    p, initial, w, dw, forward, back, _, _, _ = owner.site_vector()

    def action(x, weights):
        return owner.dirac(x, weights, forward, back)

    def delta(x, jet):
        # X-I for the native blank X=B^2 at n=1, with dX on the same C.
        base, rate = x, jet
        for degree in range(1, 5):
            rate = action(rate, w) + action(base, dw)
            base = action(base, w)
            if degree == 2:
                square, dsquare = base, rate
        return -4*p*p*(square-p*p*base), -4*p*p*(dsquare-p*p*rate)

    import numpy as np
    e, de = delta(initial, I(np.zeros_like(initial.lo)))
    ee, dee = delta(e, de)
    inner = lambda x,y: O.reduce_sum(x*y)
    v, dv = inner(initial,e), inner(initial,de)
    h, dh = inner(e,e), 2*inner(e,de)
    j, dj = inner(e,ee), inner(de,ee)+inner(e,dee)
    p1, p2, p3 = 1+v, 1+2*v+h, 1+3*v+3*h+j
    d1, d2, d3 = dv, 2*dv+dh, 3*dv+3*dh+dj
    logphi = -O.logarithm(p)
    two = (d2/p2-2*d1/p1)/logphi
    ratio = p1*p3/p2.square()
    three = (d1/p1+d3/p3-2*d2/p2)/logphi
    assert ratio.lo > 1
    print("P3", O.bounds(p3), "DP3", O.bounds(d3))
    print("two-length memory D log_phi[P2/P1^2]", O.bounds(two))
    print("three-length invariant P1 P3/P2^2", O.bounds(ratio))
    print("D log_phi[f1 f3/f2^2]", O.bounds(three))
    assert 4.1654e-6 < two.lo <= two.hi < 4.1655e-6
    assert 4.14502e-6 < three.lo <= three.hi < 4.14503e-6
    assert 1.00000128608 < ratio.lo <= ratio.hi < 1.00000128609


if __name__ == '__main__':
    main()
