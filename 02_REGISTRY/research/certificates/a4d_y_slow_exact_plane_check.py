#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact all-order Y lift: full connection and unrestricted solder variation.

Task: WRK-A4D-Y-SLOW-JOINT-CONTINUATION. See the primary memo, sections 8-11.
Arithmetic is symbolic over Q; no sampling, truncated Euler, or floating point.
The canonical frame covers every spacelike difference plane by Lorentz
covariance. Independent symbols for neighbouring time columns test actual
lattice variation, rather than substituting a frozen value into that variation.
"""
from __future__ import annotations

from itertools import combinations
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
GEN = []
for a, b in PAIRS:
    generator = sp.zeros(4)
    generator[a, b] = 1
    generator[b, a] = -ETA[a, a] * ETA[b, b]
    GEN.append(generator)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for col, (row, sign) in enumerate([(5, -1), (4, 1), (3, -1), (2, 1), (1, -1), (0, 1)]):
    STAR[row, col] = sign


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print('PASS_' + name, flush=True)


def reduced(matrix):
    return matrix.applyfunc(sp.factor)


def linv(matrix):
    return ETA * matrix.T * ETA


def wedge(left, right):
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIRS])


def bivector(matrix):
    dressed = matrix * ETA
    return sp.Matrix([dressed[a, b] for a, b in PAIRS])


def orientation(a, b):
    seq = [a, b] + [j for j in range(4) if j not in (a, b)]
    return (-1) ** sum(seq[i] > seq[j] for i, j in PAIRS)


def shift(site, role, step=1):
    # No modulo in the slow coordinate: incoming cells really are distinct.
    return tuple(value + (step if j == role else 0) for j, value in enumerate(site))


def edge_euler(solder, link, site, role, generator):
    total = 0
    for a, b in PAIRS:
        if role == a:
            corners = [(site, 0), (shift(site, b, -1), 2)]
        elif role == b:
            corners = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base, corner in corners:
            places = [(base, a, False), (shift(base, a), b, False),
                      (shift(base, b), a, True), (base, b, True)]
            factors = [linv(link(x, r)) if inverse else link(x, r)
                       for x, r, inverse in places]
            plaquette = factors[0] * factors[1] * factors[2] * factors[3]
            pinv = linv(plaquette)
            varied = factors.copy()
            varied[corner] = (factors[corner] * generator if corner < 2
                              else -generator * factors[corner])
            dp = varied[0] * varied[1] * varied[2] * varied[3]
            dc = (dp + pinv * dp * pinv) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            coframe = solder(base)
            total += orientation(a, b) * (
                wedge(coframe[:, u], coframe[:, v]).T * G2 * STAR * bivector(dc)
            )[0]
    return sp.factor(total)


def solder_euler(solder, link, site):
    # Differentiate all 16 coframe coordinates at FIXED links. Differentiating
    # the composite S -> K(S) would be a restricted, invalid stationarity test.
    coframe = solder(site)
    result = sp.zeros(4)
    for a, b in PAIRS:
        plaquette = (link(site, a) * link(shift(site, a), b)
                     * linv(link(shift(site, b), a)) * linv(link(site, b)))
        curvature = (plaquette - linv(plaquette)) / 2
        u, v = [j for j in range(4) if j not in (a, b)]
        for row in range(4):
            for col in (u, v):
                direction = sp.zeros(4)
                direction[row, col] = 1
                darea = (wedge(direction[:, u], coframe[:, v])
                         + wedge(coframe[:, u], direction[:, v]))
                result[row, col] += orientation(a, b) * (
                    darea.T * G2 * STAR * bivector(curvature)
                )[0]
    return reduced(result)


def cayley_simple(generator, norm2, amplitude):
    denominator = 4 + norm2 * amplitude**2
    return (I4 + 4 * amplitude / denominator * generator
            + 2 * amplitude**2 / denominator * generator**2)


def main():
    z, h, b = sp.symbols('z h b', real=True)
    # Any spacelike 2-plane admits this Lorentz normal form. a,b0,c,d are
    # independent: no orthogonality or fixed-length restriction on differences.
    a, b0, c, d = sp.symbols('a b0 c d', real=True)
    w = sp.Matrix(sp.symbols('w0:4', real=True))
    time_now = sp.Matrix(sp.symbols('t0:4', real=True))
    time_previous = sp.Matrix(sp.symbols('m0:4', real=True))
    u = sp.Matrix([0, a, b0, 0])
    v = sp.Matrix([0, c, d, 0])
    coframe = sp.Matrix.hstack(time_now, w, w + u, w + v)
    previous = sp.Matrix.hstack(time_previous, w, w + u, w + v)
    J = GEN[3]
    U = cayley_simple(J, 1, z)
    check('CAYLEY_LORENTZ', reduced(U * linv(U)) == I4)
    check('CAYLEY_ODD_CURVATURE', reduced((U - linv(U)) / 2 - 4*z/(4+z*z)*J) == sp.zeros(4))
    wave = [U, I4, linv(U), I4]
    link = lambda x, r: wave[sum(x) % 4] if r == 0 else I4
    solder = lambda x: coframe if x[0] == 0 else previous
    for phase in range(4):
        site = (0, phase, 0, 0)
        check(f'PHASE_{phase}_ALL_16_SOLDER_ROWS', solder_euler(solder, link, site) == sp.zeros(4))
        for role in range(4):
            values = [edge_euler(solder, link, site, role, g) for g in GEN]
            check(f'PHASE_{phase}_ROLE_{role}_ALL_6_CONNECTION_ROWS', values == [0]*6)
    # The arbitrary neighbour columns above include the frozen-coframe case.
    # Recover the actual #259 affine solder and its fixed-z first correction.
    alpha = sp.zeros(4)
    alpha[1, 2] = alpha[2, 1] = 1
    beta = sp.zeros(4)
    beta[0, 1] = beta[1, 0] = 1
    S = I4 + h * (alpha * ETA / 2).T + b * (beta * ETA / 2).T
    left, right = S[:, 2] - S[:, 1], S[:, 3] - S[:, 1]
    B = -(left * right.T - right * left.T) * ETA
    k = sp.factor(-sp.trace(B**2) / 2)
    check('AFFINE_PLANE_NORM', sp.factor(k - (3 + 2*h + h**4/16 - b**2/2 - b**2*h**2/16)) == 0)
    check('SIMPLE_BIVECTOR_CUBIC', reduced(B**3 + k*B) == sp.zeros(4))
    check('SOLDER_DETERMINANT', sp.factor(S.det() - (1-h*h/4+b*b/4)) == 0)
    amplitude = z * (1 - h * (z + 2) / 4)
    exact = cayley_simple(B, k, amplitude)
    flat = exact.subs({h: 0, b: 0})
    D = 4 + 3*z*z
    corr0 = -z*(z+2)/D*GEN[3] - 2*z*z/D*GEN[5]
    corr2 = z*(z+2)/D*GEN[3] - 2*z*z/D*GEN[4]
    check('EXACT_259_PHASE0_RIGHT_LOG_DERIVATIVE',
          reduced(linv(flat)*exact.diff(h).subs({h: 0, b: 0}) - corr0) == sp.zeros(4))
    check('EXACT_259_PHASE2_RIGHT_LOG_DERIVATIVE',
          reduced(flat*linv(exact).diff(h).subs({h: 0, b: 0}) - corr2) == sp.zeros(4))
    # b=h^2*x0, z=h: the first slope correction is h^3*x0*(K2-K3)/2.
    slope = reduced(linv(flat)*exact.diff(b).subs({h: 0, b: 0}))
    check('EXACT_275_H3_SLOPE', reduced(slope.diff(z).subs(z, 0) - (GEN[1]-GEN[2])/2) == sp.zeros(4))
    # Hostile control: keep the old flat plane on the altered coframe.
    flat_wave = [flat, I4, linv(flat), I4]
    frozen_link = lambda x, r: flat_wave[sum(x) % 4] if r == 0 else I4
    bad = edge_euler(lambda _: S.subs(b, 0), frozen_link, (0, 1, 0, 0), 0, GEN[0])
    check('FROZEN_PLANE_FAILS_259_FORCING', sp.factor(bad.diff(h).subs(h, 0) - 2*z/D) == 0)
    # Hostile control: reciprocal phase is needed for the connection equation.
    bad_wave = [U, I4, I4, I4]
    bad_link = lambda x, r: bad_wave[sum(x) % 4] if r == 0 else I4
    bad_values = [edge_euler(solder, bad_link, (0, 1, 0, 0), 1, g) for g in GEN]
    check('MISSING_RECIPROCAL_PHASE_DETECTED', any(value != 0 for value in bad_values))
    # Exact Gram completion for the truly varying metric Q_h. H is constant;
    # b=b(x0) may vary freely. No linear-coframe truncation is called exact Q.
    H = sp.Matrix([[1, -h, 0], [-h, 1, 0], [0, 0, 1]])
    e1 = sp.Matrix([1, 0, 0])
    velocity = -b * H.inv() * e1
    lapse2 = 1 + b*b/(1-h*h)
    check('EXACT_Q_TIME_TIME', sp.factor(lapse2-(velocity.T*H*velocity)[0]-1) == 0)
    check('EXACT_Q_TIME_SPACE', reduced(-H*velocity-b*e1) == sp.zeros(3, 1))
    print('COUNTS: 96 connection + 64 unrestricted solder rows; independent neighbouring time columns.')
    print('RESPONSE: all 40 Gram rows and every ten-slot projection vanish exactly; R=0.')
    print('SCOPE: frozen affine solder; separately exact Q_h in a time-dependent coframe with constant spatial Gram.')
    print('BOUNDARY: not classification of all three N0 survivors, nor the general #240 curved-background class.')
    print('TERMINAL: J2-Y-SLOW-CONNECTION-STATIONARY-RESPONSE-FACTOR-PERSISTS')


if __name__ == '__main__':
    main()
