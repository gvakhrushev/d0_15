#!/usr/bin/env python3
"""Full stopped compact Golden-Julia flag code/coherence source.

The first group checks the complete native stopped-word code in Q(sqrt(5)).
The rest checks its actual full-CAR16 J23 Choi compression, all failure
prefixes, analytic source and no-floor bound using 90-digit arithmetic.
No choice of compulsory Book03 price or native G0 admission is asserted.
"""
from itertools import combinations
from math import ceil
import json
import mpmath as mp
import sympy as sp

mp.mp.dps = 90
p = (mp.sqrt(5) - 1) / 2
g = p*p
ell = -mp.log(p)
ps = (sp.sqrt(5)-1)/2
gs = sp.simplify(ps**2)

def matrix_trace(A):
    return sum(A[j,j] for j in range(A.rows))

def exact_zero(x):
    return sp.simplify(x) == 0

def stopped_leaves(m, cap):
    leaves = []
    def visit(word, successes):
        if successes == m or len(word) == cap:
            leaves.append((word, successes))
            return
        visit(word+(0,), successes)
        visit(word+(1,), successes+1)
    visit((), 0)
    return leaves

# This is the whole finite leaf tree; completed words have different lengths.
m, cap = 2, 7
leaves = stopped_leaves(m, cap)
mass = cost = attempts = successes = sp.S.Zero
by_k = [sp.S.Zero for _ in range(m+1)]
for word, k in leaves:
    t = len(word)
    wt = gs**k * ps**(t-k)
    assert exact_zero(wt-ps**(t+k))
    mass += wt
    cost += (t+k)*wt
    attempts += t*wt
    successes += k*wt
    by_k[k] += wt
assert exact_zero(mass-1)
assert exact_zero(successes-gs*attempts)
assert exact_zero(cost-(1+gs)*attempts)
for k in range(m):
    assert exact_zero(by_k[k]-sp.binomial(cap,k)*gs**k*ps**(cap-k))
print('PASS exact complete stopped-tree Golden/Kraft equality and real clock budget')

# The actual CAR16 representation on all exterior grades, not a replacement
# qubit. This exhibits the Choi charge multiplicities used below.
subsets = [s for degree in range(5) for s in combinations(range(4), degree)]
P = sp.eye(4)
P[2,2] = P[3,3] = sp.Rational(3,5)
P[2,3] = -sp.Rational(4,5)
P[3,2] = sp.Rational(4,5)
V = sp.Matrix([[0 if len(a)!=len(b) else
                (1 if not a else P.extract(a,b).det())
                for b in subsets] for a in subsets])
assert V.T*V == sp.eye(16)
assert exact_zero(sp.trace(V)/16-sp.Rational(4,5))
assert V.eigenvals() == {sp.S.One:8, sp.Rational(3,5)-sp.I*sp.Rational(4,5):4,
                        sp.Rational(3,5)+sp.I*sp.Rational(4,5):4}
assert V.T*(sp.eye(16)/16)*V == sp.eye(16)/16
print('PASS full CAR16 compact Choi charges (0,+1,-1) with weights (1/2,1/4,1/4)')

charges = (0,1,-1)
amplitudes = (1/mp.sqrt(2), mp.mpf('0.5'), mp.mpf('0.5'))

def prefix_weights(m, cap):
    failed = [mp.binomial(cap,k)*g**k*p**(cap-k) for k in range(m)]
    epsilon = sum(failed)
    return failed+[1-epsilon], epsilon

def complementary_density(m, cap, delta, field):
    weights, epsilon = prefix_weights(m, cap)
    A = mp.matrix(3, m+1)
    DA = mp.matrix(3, m+1)
    for k, wt in enumerate(weights):
        offset = (k-m)*delta
        for a, charge in enumerate(charges):
            z = mp.sqrt(wt)*amplitudes[a]*mp.exp(1j*charge*offset*field)
            A[a,k] = z
            DA[a,k] = 1j*charge*offset*z
    sigma = A*A.H
    dsigma = DA*A.H+A*DA.H
    assert abs(matrix_trace(sigma)-1) < mp.mpf('1e-80')
    assert abs(matrix_trace(dsigma)) < mp.mpf('1e-80')
    # m*delta/sqrt(2) is an exact norm bound for every failed prefix jet.
    B = m*delta/mp.sqrt(2)
    actual_amplitude_jet = mp.sqrt(sum(abs(z)**2 for z in DA))
    assert actual_amplitude_jet <= B*mp.sqrt(epsilon)+mp.mpf('1e-80')
    return sigma, dsigma, epsilon, B

def entropy_source(sigma, dsigma):
    values, vectors = mp.eighe(sigma)
    entropy = mp.mpf(0)
    derivative = mp.mpf(0)
    for j, lam in enumerate(values):
        assert lam > -mp.mpf('1e-80')
        if lam < mp.mpf('1e-75'):
            # Numerical representation of exact zero modes. The actual
            # analytic C1 theorem, not a discarded source, treats these.
            col = vectors[:,j]
            assert abs((col.H*dsigma*col)[0]) < mp.mpf('1e-70')
            continue
        col = vectors[:,j]
        dlam = mp.re((col.H*dsigma*col)[0])
        entropy -= lam*mp.log(lam)
        derivative -= dlam*mp.log(lam)
    return entropy, derivative

def source_bound(epsilon, B, rank):
    assert 0 < epsilon <= mp.exp(-2)
    moment = (1-epsilon)*mp.log1p(-epsilon)**2 + epsilon*mp.log(epsilon/(rank-1))**2
    return 2*B*mp.sqrt(epsilon*moment)

# Direct ALL-LEAF Gram and its reduced three-dimensional spectrum agree.
# Every complete chronological leaf remains represented, including failures.
theta = mp.mpf('0.37')
A_full = mp.matrix(3,len(leaves))
for j,(word,k) in enumerate(leaves):
    wt = g**k*p**(len(word)-k)
    for a,charge in enumerate(charges):
        A_full[a,j] = mp.sqrt(wt)*amplitudes[a]*mp.exp(1j*charge*(k-m)*theta)
sigma_full = A_full*A_full.H
sigma_grouped, _, _, _ = complementary_density(m,cap,mp.mpf(1),theta)
assert mp.norm(sigma_full-sigma_grouped) < mp.mpf('1e-80')
# Gram purity checks the large record directly without an unnecessary large
# eigenvalue computation; AA* and A*A share all nonzero singular values.
gram = A_full.H*A_full
assert abs(matrix_trace(gram*gram)-matrix_trace(sigma_full*sigma_full)) < mp.mpf('1e-75')
for j,(word,k) in enumerate(leaves):
    wt = g**k*p**(len(word)-k)
    assert abs(gram[j,j]-wt) < mp.mpf('1e-80')
print('PASS all retained stopped leaves: exact Born diagonal and full coherent Gram reduction')

rows=[]
for m in (4,8,16,32,64):
    cap = int(mp.ceil(2*m/g))
    delta = mp.mpf(1)/m  # actual geometric tau=m*delta=1
    maximum=mp.mpf(0)
    for field in (mp.mpf('-0.8'),mp.mpf(0),mp.mpf('0.3'),mp.mpf('1.1')):
        sigma,dsigma,epsilon,B = complementary_density(m,cap,delta,field)
        entropy,derivative = entropy_source(sigma,dsigma)
        bound=source_bound(epsilon,B,3)
        assert abs(derivative) <= bound+mp.mpf('1e-65')
        assert bound <= source_bound(epsilon,B,256)
        if field == 0:
            assert abs(entropy) < mp.mpf('1e-70')
            assert abs(derivative) < mp.mpf('1e-70')
        maximum=max(maximum,abs(derivative)/ell)
    # Chernoff is checked against the real cap law, not used in place of it.
    assert epsilon <= mp.exp(-mp.mpf(m)/4)
    rows.append({'m':m,'N':cap,'epsilon':mp.nstr(epsilon,14),
                 'max_tested_code_source':mp.nstr(maximum,14),
                 'normalized_code_source':mp.nstr(m*maximum,14),
                 'uniform_normalized_CAR16_bound':mp.nstr(m*source_bound(epsilon,B,256)/ell,14)})
print('PASS analytic full coherent code source and no-floor bound for every retained cap prefix')
print(json.dumps({'refinement':rows},indent=2))

# ACTUAL full-CAR16 rank-birth control: one success, N=6, all bad branch
# epsilon=p^6 and overlap Tr Lambda(J23(theta))/16=cos(theta/2)^2.
eps=p**6
assert eps < mp.exp(-2)
coefficient=eps*(1-eps)/2
ratios=[]
for theta in (mp.mpf('1e-2'),mp.mpf('1e-4'),mp.mpf('1e-6'),mp.mpf('1e-8')):
    determinant=eps*(1-eps)*(1-mp.cos(theta/2)**4)
    small=2*determinant/(1+mp.sqrt(1-4*determinant))
    entropy=-small*mp.log(small)-(1-small)*mp.log1p(-small)
    ratios.append(entropy/theta**2)
    assert abs(small/(theta**2)-coefficient) < mp.mpf('0.01')*coefficient
assert all(a<b for a,b in zip(ratios,ratios[1:]))
print('PASS actual CAR16 rank birth: C1 entropy but unbounded second difference at the common-output base')
print(json.dumps({'rank_birth_entropy_over_theta_squared':[mp.nstr(z,14) for z in ratios]},indent=2))
print('SCOPE: one coherent compact stopped FLAG archive. Final readout, full128, physical admission and compulsory full Book03 action remain separate.')
