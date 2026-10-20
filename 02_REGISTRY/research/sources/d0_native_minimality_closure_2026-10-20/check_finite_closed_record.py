#!/usr/bin/env python3
"""New finite symmetric-record cut/source and actual full-spectrum cost checks.

Consumes the original full128 Kraus and return-cost identities; does not
replay those proofs or identify this extra ensemble as compulsory Book Info.
The mathematical proofs, including dimension-uniform bounds, are in
finite_closed_record.md. Numpy values check applications, not universal claims.
"""
import math

import numpy as np
import sympy as s

if not __debug__:
    raise RuntimeError("This checker requires enabled assertions; invoke Python without -O")


def complete_homogeneous(variables, count):
    hs = [s.Integer(1)]
    powers = [None] + [sum(x**j for x in variables) for j in range(1, count + 1)]
    for r in range(1, count + 1):
        hs.append(s.expand(sum(powers[j] * hs[r-j] for j in range(1, r+1)) / r))
    return hs


# This identity controls the WHOLE polynomial tail derivative, including
# rank births, rather than bounding only the value and then differentiating.
variables = s.symbols("l0:3")
hs = complete_homogeneous(variables, 7)
for r in range(1, 8):
    assert s.expand(sum(s.diff(hs[r], x) for x in variables)
                    - (len(variables)+r-1)*hs[r-1]) == 0
print("exact complete-symmetric derivative identity, through degree 7: PASS")

# A moving, genuinely noncommuting PSD family with a dark eigenvalue.
# U is rational orthogonal. X is the derivative of a conjugated diagonal
# family with eigenvalues (t^2,1/4+t/40,1/2-t/50).
U = s.Matrix([[s.Rational(3, 5), -s.Rational(4, 5), 0],
              [s.Rational(4, 5), s.Rational(3, 5), 0], [0, 0, 1]])
F = U*s.diag(0, s.Rational(1, 4), s.Rational(1, 2))*U.T
S = s.Matrix([[0, 0, s.Rational(1, 10)], [0, 0, 0],
              [-s.Rational(1, 10), 0, 0]])
X = S*F-F*S+U*s.diag(0, s.Rational(1, 40), -s.Rational(1, 50))*U.T
assert F*X != X*F
assert F.det() == 0
z = s.Rational(1, 10)
q = s.Rational(1, 20)
a = s.Integer(2)
dimension = 3
Z = 1/(s.eye(3)-z*F).det()
dlogZ = z*s.trace((s.eye(3)-z*F).inv()*X)
h = [s.Integer(1)]
dh = [s.Integer(0)]
for r in range(1, 13):
    h.append(s.cancel(sum(s.trace(F**j)*h[r-j] for j in range(1, r+1))/r))
    dh.append(s.cancel(sum(j*s.trace(F**(j-1)*X)*h[r-j]
                          +s.trace(F**j)*dh[r-j]
                          for j in range(1, r+1))/r))
Xbound = s.sqrt(s.trace(X.T*X))  # Frobenius >= required operator norm.
for R in (6, 9, 12):
    ZR = sum(z**r*h[r] for r in range(R+1))
    dZR = sum(z**r*dh[r] for r in range(R+1))
    M = ((1-q)/(1-a*q))**dimension
    e = a**(-(R+1))*M
    tau = 1-ZR/Z
    assert 0 <= tau <= e < 1
    error = abs(dlogZ-dZR/ZR)
    bound = z*dimension*Xbound*M*a**(-R)/(1-e) * (1/(1-a*q)+1/(a*(1-q)))
    assert float(error) <= float(bound)
    assert float(s.log(Z/ZR)) <= float(-s.log(1-e)) + 1e-18
print("finite positive-occupation value/source cut with dark mode and noncommuting jet: PASS")

# The literal finite-clock source is NOT the continuum exponential source.
# Check its cost insertion algebra independently before numerical spectra.
n = s.symbols("n", positive=True, integer=True)
eps, lam, p = s.symbols("epsilon lambda p", positive=True)
x = s.symbols("x", positive=True)
b = 1-eps*lam/2
marked = x**n*((1+p*eps*lam*(x-1))**n-b**(2*n))
exit_cost = s.diff(marked, x).subs(x, 1)
assert s.simplify(exit_cost - (n*(1-b**(2*n))+n*p*eps*lam)) == 0
print("exact original shell exit-cost insertion, including n paid blank ticks: PASS")

p0 = (math.sqrt(5)-1)/2
beta = 2*p0*p0
z0 = 2**-20
rho = 0.2
samples = []
for L in (4, 8, 16):
    axes = np.indices((L,)*4)
    mu = sum(2-2*np.cos(2*math.pi*axes[j]/L) for j in range(4)).ravel()
    assert abs(float(mu.mean())-8) < 1e-12
    assert np.count_nonzero(mu >= 4-1e-12) >= len(mu)/3
    n0 = 128*L*L
    m = 2*n0
    alpha = p0*p0/(128*L*L)
    d = 2048*L**4
    multiplicity = 16*128
    energy = rho*mu
    logb = np.log1p(-alpha*energy)
    f = -np.expm1(m*logb)
    df = beta*mu*np.exp((m-1)*logb)
    R = 1/(1-z0*f)
    occupation = multiplicity*z0*np.sum(R*f)
    cost = n0*occupation + multiplicity*p0*beta*z0*np.sum(R*energy)
    dcost = multiplicity*(n0*z0*np.sum(R*R*df)
                         +p0*beta*z0*np.sum(R*mu+z0*R*R*df*energy))
    pressure = -multiplicity*np.sum(np.log1p(-z0*f))
    dpressure = multiplicity*z0*np.sum(R*df)
    active = f > 0
    xx = z0*f[active]
    entropy = multiplicity*np.sum(-np.log1p(-xx)-xx*np.log(xx)/(1-xx))
    dentropy = -multiplicity*z0*np.sum(df[active]*np.log(xx)/(1-xx)**2)
    assert n0*occupation <= cost <= 2*n0*occupation
    assert (1-math.exp(-4*beta*rho))*L**6/12 <= cost <= L**6/(2*(1-z0))
    assert dcost >= 2*beta*math.exp(-32*beta*rho)*L**6
    assert 0 <= dpressure <= beta*L**4/(64*(1-z0))
    assert 0 <= dentropy <= d*z0*(-math.log(z0))/(rho*(1-z0)**2)
    assert dcost-dentropy/math.log(1/p0) > dpressure

    # The full normalized preparation ALSO retains failed runs. Its actual
    # input occupation is field-independent, unlike the conditional event
    # ensemble above. Baseline cost has no field source.
    complete_cost = z0/(1-z0)*(n0*d+p0*beta*multiplicity*np.sum(energy))
    complete_cost_source = z0/(1-z0)*p0*beta*multiplicity*np.sum(mu)
    assert abs(complete_cost_source/L**4-p0*beta/(64*(1-z0))) < 1e-14
    assert complete_cost > cost

    # Original first-source norm ||delta F|| <= beta ||delta Delta||.
    # The displayed cap controls h^-2-normalized source with no rank floor.
    norm_power = 2
    cap = math.ceil(d*z0/((1-2*z0)*math.log(2))+(norm_power+6)*math.log2(L))
    logM = d*(math.log1p(-z0)-math.log1p(-2*z0))
    tail = math.exp(logM-(cap+1)*math.log(2))
    assert tail <= 0.5*L**(-(norm_power+6))*(1+1e-10)
    first_source_bound = (z0*d*beta*math.exp(logM-cap*math.log(2))/(1-tail)
                          *(1/(1-2*z0)+1/(2*(1-z0))))
    assert L**norm_power*first_source_bound <= 7000*z0*beta/L**2
    # Finite prior: log recurrence avoids overflow of binomial coefficients.
    raw_prior = [1.0]
    for r in range(cap):
        raw_prior.append(raw_prior[-1]*z0*(d+r)/(r+1))
    prior_norm = math.fsum(raw_prior)
    prior_mean = math.fsum(r*w for r, w in enumerate(raw_prior))/prior_norm
    assert 0 < prior_mean <= d*z0/(1-z0)*(1+1e-14)
    finite_complete_source = prior_mean/d*p0*beta*multiplicity*np.sum(mu)
    assert finite_complete_source > 0
    samples.append({"L": L, "occupation_cap": cap,
                    "cost_per_L6": float(cost/L**6),
                    "cost_source_per_L6": float(dcost/L**6),
                    "pressure_source_per_L4": float(dpressure/L**4),
                    "coherent_info_source_per_L4": float(dentropy/(math.log(1/p0)*L**4)),
                    "complete_port_source_per_L4": float(complete_cost_source/L**4),
                    "finite_complete_port_source_per_L4": float(finite_complete_source/L**4),
                    "h_minus2_source_tail_bound": first_source_bound*L**2})

print("original full site x CAR16 x reference128 CONDITIONAL source separation: PASS")
print("complete finite apparatus retains failures and has its own exact source: PASS")
print("finite cap preserves h^-2-normalized closed-pressure source: PASS")
for item in samples:
    print(item)
