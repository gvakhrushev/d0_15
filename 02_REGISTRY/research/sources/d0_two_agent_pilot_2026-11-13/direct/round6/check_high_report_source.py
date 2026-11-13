#!/usr/bin/env python3
"""Exact pulse algebra and bounded noncommuting source diagnostics.

This is not a full native history replay or physical Cost-Info selection.
The analytic full-source argument is in HIGH_REPORT_SOURCE_RU.md.
"""
import itertools
import json
import math

import numpy as np
import sympy as s

exact = []
numeric = []


def need(ok, label, target):
    if not bool(ok):
        raise RuntimeError(label)
    target.append(label)


p = (s.sqrt(5)-1)/2
a0 = s.sqrt(p)
field = s.QQ.algebraic_field(a0)


def eq(x, y=0):
    return field.from_sympy(s.expand(x-y)) == field.zero


def meq(x, y):
    return x.shape == y.shape and all(eq(z) for z in x-y)


G = s.Matrix([[a0, -p], [p, a0]])
R = s.Matrix([[p**3, -2*a0*p], [2*a0*p, p**3]])
q = s.symbols('q', real=True)
pointer = s.Matrix([[1-q, a0*p], [a0*p, q]])
A = 4*p**3+4*p**6
k = 1-2*p**6
U = (147-65*s.sqrt(5))/2
need(meq(G*G, R), 'two actual Golden rotations have the declared coefficients', exact)
need(meq(R.T*R, s.eye(2)), 'pulse is exactly unitary', exact)
expr = s.expand((R*pointer*R.T)[1, 1]-(A-k*q))
need(all(eq(c) for c in s.Poly(expr, q).all_coeffs()), 'coherent cross term gives the affine probability law', exact)
need(eq(A, 28-12*s.sqrt(5)), 'constant offset exact', exact)
need(eq(k, 8*s.sqrt(5)-17), 'actual source gain exact', exact)
need(s.simplify(k > 0), 'gain is strictly positive', exact)
need(s.simplify(k < 1), 'old bit cannot be recovered by a one-bit stochastic decoder', exact)
need(s.simplify(A/k > 1), 'inverse expectation estimator is not a probability decoder', exact)
need(eq(A-k*p, p), 'lower probability endpoint exact', exact)
need(eq(A-k*p**2, U), 'upper probability endpoint exact', exact)
need(s.simplify(p > s.Rational(1, 2)), 'entire new interval is above one half', exact)
need(s.simplify(U < 1), 'new interval stays below one', exact)
need(eq(p/(1-p), 1/p), 'global lower information slope is one Golden unit', exact)
need(eq(p**2*(1-p**2), p**3) and eq(p*(1-p), p**3), 'original pointer positivity endpoints retained', exact)
u, d = (a0+p)/2, (a0-p)/2
need(eq(u*u-d*d, a0*p), 'NPS Hermitian cross coefficient exact', exact)
v = s.kronecker_product(s.Matrix([a0,p]), s.Matrix([a0,p]))
good = s.diag(1,1,1,0)
need(eq((v.T*good*v)[0], p+p**3), 'noisy valid-output born mass exact', exact)
need(s.simplify(p+p**3 < 1), 'noisy repeated support is a strict contraction', exact)
aa, lo, hi, bc, bi = s.symbols('a lo hi bc bi', positive=True)
need(s.cancel(hi/lo-(1+aa*hi)/(1+aa*lo)-(hi-lo)/(lo*(1+aa*lo))) == 0,
     'uniform coefficient ratio identity', exact)
need(s.cancel(1/lo-aa/(1+aa*lo)-1/(lo*(1+aa*lo))) == 0,
     'uniform information coefficient identity', exact)
need(s.cancel((bc+aa*bi)/(1+aa*lo)-(bc/(1+aa*lo)+aa*lo/(1+aa*lo)*(bi/lo))) == 0,
     'old-source bound is a convex combination', exact)

pf = float(p)
af = float(A)
kf = float(k)
ell = math.log(1/pf)
X = np.array([[0.,1.],[1.,0.]])
Z = np.diag([1.,-1.])
effects = np.array([(np.eye(2)+math.sin(t)*X+math.cos(t)*Z)/3
                    for t in (0., 2*math.pi/3, 4*math.pi/3)])
need(np.linalg.norm(sum(effects)-np.eye(2)) < 1e-14, 'compressed POVM is complete', numeric)
need(np.linalg.norm(effects[0]@effects[1]-effects[1]@effects[0]) > .1,
     'compressed effects genuinely do not commute', numeric)
rho = np.array([[.65,.12],[.12,.35]])


def sqrt_psd(mat):
    values, vectors = np.linalg.eigh(mat)
    return (vectors*np.sqrt(np.maximum(values, 0)))@vectors.T


def entropy(mat):
    values = np.linalg.eigvalsh(mat)
    need(np.min(values) >= -1e-12, 'positive conditional block', scratch)
    positive = values[values > 1e-14]
    return float(-np.sum(positive*np.log(positive)))


scratch = []  # Internal numerical sanity checks are not counted as proof conditions.


def values(qs, state):
    sr = sqrt_psd(state)
    blocks = []
    probabilities = []
    for omega in itertools.product((0,1), repeat=qs.shape[1]):
        weights = np.prod(np.array([qs[:,j] if b else 1-qs[:,j]
                                    for j,b in enumerate(omega)]), axis=0)
        effect = sum(w*m for w,m in zip(weights,effects))
        block = sr@effect@sr
        blocks.append(block)
        probabilities.append(float(np.trace(block)))
    probabilities = np.array(probabilities)
    rtheta = np.array([np.trace(state@m) for m in effects])
    return np.array([qs.shape[1]+np.sum(rtheta[:,None]*qs),
                     sum(entropy(b) for b in blocks)-entropy(state),
                     -np.sum(probabilities*np.log(probabilities))])


low = np.array([[pf**2+.02*t+.013*j for j in range(2)] for t in range(3)])
high = af-kf*low
rtheta = np.array([np.trace(rho@m) for m in effects])
Lmin = math.log(np.min(high)/(1-np.min(high)))/ell
Lmax = math.log(np.max(high)/(1-np.max(high)))/ell
step = 2e-6
coefficients = [(0.,0.),(.2,0.),(0.,.4),(.3,.7),(1.,1.5)]
max_difference = 0.
for theta,j in itertools.product(range(3),range(2)):
    plus, minus = high.copy(), high.copy()
    plus[theta,j] += step
    minus[theta,j] -= step
    derivative = (values(plus,rho)-values(minus,rho))/(2*step)
    for idx, name in [(1,'CQ'),(2,'classical joint')]:
        scaled = -derivative[idx]/ell
        need(Lmin*rtheta[theta]-2e-8 <= scaled <= Lmax*rtheta[theta]+2e-8,
             f'{name} full derivative bounds at {theta},{j}', numeric)
    for bq, bcl in coefficients:
        slope = derivative[0]-(bq*derivative[1]+bcl*derivative[2])/ell
        bound = (1+(bq+bcl)*Lmin)*rtheta[theta]
        need(slope >= bound-2e-8, f'positive registration slope {theta},{j},{bq},{bcl}', numeric)
        max_difference = max(max_difference,abs(derivative[0]-rtheta[theta]))

ideal = np.tile([.70,.76],(3,1))
expected = np.array([2+1.46, sum(-x*math.log(x)-(1-x)*math.log(1-x) for x in (.70,.76))])
states = [rho, np.eye(2)/2, np.array([[1.,0.],[0.,0.]]), np.array([[.5,.5],[.5,.5]])]
for idx, state in enumerate(states):
    cost, iq, hc = values(ideal,state)
    need(max(abs(cost-expected[0]),abs(iq-expected[1]),abs(hc-expected[1])) < 1e-13,
         f'ideal scalar price independent of mixed or rank-one input {idx}', numeric)

q_noisy = pf**2+pf**3*(4*math.sin(512*math.asin(pf))**2*pf**7)
L_noisy = math.log((1-q_noisy)/q_noisy)/ell
cancellation_coefficient = 1/L_noisy
q_new = af-kf*q_noisy
new_full_slope = -kf*(1-cancellation_coefficient*math.log((1-q_new)/q_new)/ell)
need(1 < cancellation_coefficient < 1.5, 'old noisy cancellation lies in the known coefficient range', numeric)
need(new_full_slope < -kf, 'same fixed coefficient cannot cancel the new source', numeric)
print(json.dumps({
    'status':'PASS_SCOPED_SOURCE_CHECK',
    'exact_count':len(exact),'exact_checks':exact,
    'numeric_count':len(numeric),'numeric_checks':numeric,
    'fixture':{'new_probability_range':[pf,float(U)],'actual_k':kf,
               'old_noisy_probability':q_noisy,'new_noisy_probability':q_new,
               'old_cancelling_coefficient':cancellation_coefficient,
               'new_full_slope_at_old_cancellation':new_full_slope,
               'max_registration_derivative_error':max_difference},
    'scope':'Exact Golden pulse algebra and bounded noncommuting full-CQ diagnostics; full theorem is analytic. Not full native H1 admission or physical Cost-Info binding.',
    'physical_C_closed':False,'GR_closed':False
},indent=2))
