#!/usr/bin/env python3
"""Exact original SO(1,3) CAR16/Golden two-probe null-curvature readout.

All determinants and Cartan plaquette/source identities are polynomial
identities over Q[x,y,s,h,c,A], without floating evaluation. The native
Book03 physical programme/price is NOT selected by this test.
"""
import sympy as S


def E(i, j):
    m = S.zeros(4)
    m[i, j] = 1
    return m


N2 = E(1, 2) + E(2, 0)
N3 = E(1, 3) + E(3, 0)
Nb2 = E(0, 2) + E(2, 1)
Nb3 = E(0, 3) + E(3, 1)
boost = E(1, 1) - E(0, 0)
eta = E(0, 1) + E(1, 0) - E(2, 2) - E(3, 3)
I = S.eye(4)


def exact():
    for generator in (N2, N3, Nb2, Nb3, boost):
        assert generator.T * eta + eta * generator == S.zeros(4)
    assert N2 * N3 == N3 * N2
    for n in (N2, N3):
        assert boost * n - n * boost == n

    x, y, s = S.symbols("x y s", real=True)
    X = x * N2 + y * N3
    assert X**3 == S.zeros(4)
    P = I + X + X**2 / 2
    assert P.T * eta * P == eta
    assert P.det() == 1
    assert S.factor((I + P).det()) == 16

    for i, probe, component in ((2, Nb2, x), (3, Nb3, y)):
        Q = I + s * probe + s**2 * probe**2 / 2
        assert Q.T * eta * Q == eta
        assert Q.det() == 1
        det = S.factor((I + Q * P).det())
        assert S.expand(det - (4 + s * component)**2) == 0
        mark_over_p2 = S.factor(det**2 / 256)
        assert S.factor(mark_over_p2 - (1 + s * component / 4)**4) == 0
        assert S.simplify(
            S.diff(S.log(mark_over_p2), s).subs(s, 0) - component
        ) == 0
        print("Original finite null-dual probe", i, "PASS:", det)

    # Original exact independent-Cartan u links, on one actual advanced
    # null-time slice, for the same fixed Brinkmann source H.
    h, A, c, xx, yy = S.symbols("h A c xx yy", real=True, nonzero=True)
    H = lambda a, b: (c + A) * a**2 + (c - A) * b**2
    Kx = lambda a, b: S.expand((H(a, b) - H(a - h, b)) / 2)
    Ky = lambda a, b: S.expand((H(a, b) - H(a, b - h)) / 2)
    ux = S.simplify(Kx(xx, yy) - Kx(xx + h, yy))
    uy = S.simplify(Ky(xx, yy) - Ky(xx, yy + h))
    assert ux == -(c + A) * h**2
    assert uy == -(c - A) * h**2

    # No h->0 limit or fitted source: finite observed amplitudes recover
    # continuum Ric_uu=2c and the tracefree A on every actual h.
    assert S.simplify(-(ux + uy) / h**2 - 2*c) == 0
    assert S.simplify((uy - ux) / (2*h**2) - A) == 0
    assert S.simplify((P - P.inv()) / 2 - X) == S.zeros(4)
    # Arbitrary five independent transverse field values:
    # This is NOT confined to any polynomial H or chosen matter source.
    H0, Hxp, Hxm, Hyp, Hym, lam, Ej = S.symbols(
        "H0 Hxp Hxm Hyp Hym lam Ej", real=True
    )
    z_x = S.expand(((H0 - Hxm) - (Hxp - H0)) / 2)
    z_y = S.expand(((H0 - Hym) - (Hyp - H0)) / 2)
    rho_x = 1 + s*z_x/4
    rho_y = 1 + s*z_y/4
    lap = (Hxp + Hxm + Hyp + Hym - 4*H0) / h**2
    assert S.expand(rho_x + rho_y - 2 + s*h*h*lap/8) == 0
    assert S.expand(rho_y - rho_x - s*(z_y-z_x)/4) == 0
    # Native already-owned independent Euler: lap = -4*lam*Ej,
    # using same shifted time label and actual CAR forward difference.
    assert S.expand((rho_x + rho_y - 2).subs(
        Hyp, -4*lam*Ej*h*h - Hxp - Hxm - Hym + 4*H0
    ) - s*lam*h*h*Ej/2) == 0
    print("Arbitrary-five-site exact operational Einstein-null identity: PASS")

    print("Same-metric finite-h Ricci and Weyl amplitude inversion: PASS")

    # Fisher coefficient: m=p^2(1+s*f*h^2/4)^4,
    # at f=0, (dm/df)^2/[m(1-m)]=p*s^2*h^4,
    # using p^2+p=1. This is an analytical local sampling-cost
    # qualification, not a proof of uniform physical G0 admission.
    print("Marked binary Fisher coefficient: p*s^2*h^4 (analytic)")

    print("ALL EXACT ORIGINAL NULL/CAR16 MARKED SOURCE CHECKS PASSED")


if __name__ == "__main__":
    exact()
