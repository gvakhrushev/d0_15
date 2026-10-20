#!/usr/bin/env python3
"""Exact full K(9,11,13) Book Info/archive substitution; stdout only."""
import sympy as s


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


zones = [0] * 9 + [1] * 11 + [2] * 13
n = len(zones)
edges = [(u, v) for u in range(n) for v in range(n) if zones[u] != zones[v]]
degrees = [sum(1 for a, b in edges if a == u) for u in range(n)]
require(len(edges) == 718 and n == 33, 'original full directed carrier')
P = s.Matrix(n, n, lambda u, v: s.Rational(1, degrees[u]) if (u, v) in edges else 0)
one = s.ones(n, 1)
pi = s.Matrix([s.Rational(d, 718) for d in degrees])
Pi = one * pi.T
Z = (s.eye(n) - P + Pi).inv()
require(P * one == one and pi.T * P == pi.T, 'Markov/stationary fixture')
require(Z * one == one and pi.T * Z == pi.T, 'fundamental normalization')
require(Z * P == Z - s.eye(n) + Pi, 'fundamental resolvent identity')
require(all(pi[u] * P[u, v] == s.Rational(1, 718) for u, v in edges), 'all edge masses retained')


def mean(vector):
    return (pi.T * vector)[0]


def inner_pi(a, b):
    return sum(pi[i] * a[i] * b[i] for i in range(n))


def old_archive_tilde(b, theta):
    # G=sqrt(mu)*tilde_G. All mu=1/718, so no radicals or dense archive needed.
    d = {(u, v): -theta * b[u] - (1 - theta) * b[v] for u, v in edges}
    m = s.Matrix([sum(P[u, v] * d[u, v] for v in range(n) if (u, v) in d) for u in range(n)])
    potential = Z * m
    row_mean = m + P * potential
    return s.Matrix([d[u, v] + potential[v] - row_mean[u] for u, v in edges])


def new_archive_tilde(b):
    potential = Z * b
    avg = P * potential
    return s.Matrix([-(potential[v] - avg[u]) for u, v in edges])


def archive_norm(a):
    return a.dot(a) / 718


def pressure_hessian_div_log(b, theta):
    # K(y)=diag(exp(log(phi)*theta*y*b)) P
    #       diag(exp(log(phi)*(1-theta)*y*b)).
    # Exact first/second Perron jets with log(phi) factored out.
    K1 = s.Matrix(n, n, lambda u, v: P[u, v] * (theta * b[u] + (1 - theta) * b[v]))
    K2 = s.Matrix(n, n, lambda u, v: P[u, v] * (theta * b[u] + (1 - theta) * b[v]) ** 2)
    lam1 = (pi.T * K1 * one)[0]
    vec1 = Z * (K1 * one - lam1 * one)
    require(mean(vec1) == 0, 'Perron eigenvector derivative normalization')
    require((s.eye(n) - P) * vec1 == K1 * one - lam1 * one, 'Perron eigenvector jet')
    lam2 = (pi.T * K2 * one)[0] + 2 * (pi.T * K1 * vec1)[0]
    require(lam1 == mean(b), 'first pressure source equals minus mean Info')
    return -(lam2 - lam1 ** 2)


localized = s.zeros(n, 1)
localized[0] = 1
localized -= mean(localized) * one
other = s.Matrix([s.Rational((i * 7) % 11 - 5, 3) for i in range(n)])
scores = [localized, other, localized + other, one]
theta_values = [s.Rational(0), s.Rational(1, 2), s.Rational(1), s.Rational(2)]
for b in scores:
    new = new_archive_tilde(b)
    norm = archive_norm(new)
    centered = b - mean(b) * one
    resolvent_norm = 2 * inner_pi(centered, Z * centered) - inner_pi(centered, centered)
    require(norm == resolvent_norm, 'exact archive/Poisson quadratic identity')
    require(norm >= 0, 'archive norm positivity')
    for theta in theta_values:
        require(old_archive_tilde(b, theta) == new, 'literal old-to-new theta-independent source')
        require(pressure_hessian_div_log(b, theta) == -norm, 'direct Perron Hessian has negative archive sign')

require(mean(localized) == 0, 'localized Info direction is stationary to first order')
local_norm = archive_norm(new_archive_tilde(localized))
require(local_norm > 0, 'nonconstant stationary Info direction has strict descent curvature')
require(new_archive_tilde(one) == s.zeros(718, 1), 'common Info direction archive invisible')
require(mean(one) == 1, 'common Info direction has nonzero absolute pressure source')

# Polarized mixed Hessian, checked by direct Perron response rather than defining it.
ga = new_archive_tilde(localized)
gb = new_archive_tilde(other)
mixed = (pressure_hessian_div_log(localized + other, s.Rational(1, 2))
         - pressure_hessian_div_log(localized, s.Rational(1, 2))
         - pressure_hessian_div_log(other, s.Rational(1, 2))) / 2
require(mixed == -ga.dot(gb) / 718, 'mixed full-field archive source')

# Genuine nonlinear Info adds its own primitive curvature, not a fitted Fisher sign.
# I(y)=y*b+y²*c/2; retain log(phi)=ell as an independent positive symbolic constant.
ell = s.symbols('ell', positive=True)
curvature = s.Matrix([s.Rational(i - 13, 7) for i in range(n)])
theta = s.Rational(1, 2)
K2_extra = s.Matrix(n, n, lambda u, v: P[u, v] * (theta * curvature[u] + (1 - theta) * curvature[v]))
extra_pressure = -(pi.T * K2_extra * one)[0]
require(extra_pressure == -mean(curvature), 'nonlinear Info curvature retained')
full_second = ell * pressure_hessian_div_log(localized, theta) + extra_pressure
require(s.expand(full_second + ell * local_norm + mean(curvature)) == 0, 'complete nonlinear Hessian')

print('PASS: all 718 original labels; exact node-Info archive substitution; theta gauge;')
print('      direct Perron first/mixed/second jets; Poisson form; absolute shift; nonlinear Info.')
print('stationary localized Info archive norm =', local_norm)
