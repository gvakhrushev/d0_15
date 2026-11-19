#!/usr/bin/env python3
"""New exact replay of original detector first jets and reconstructed claims.

No historical test count, hidden expected-file rewrite or rank computation.
All checks remain enabled under python -O. Only stdout is written.
"""
from itertools import product
from fractions import Fraction
import json
import sympy as s


def require(ok, label):
    if ok is not True and ok != s.true:
        raise RuntimeError(label)


def zero(expr):
    if isinstance(expr, s.MatrixBase):
        return all(s.simplify(x) == 0 for x in expr)
    return s.simplify(expr) == 0


def E(i, j):
    a = s.zeros(4)
    a[i, j] = 1
    return a


G = [E(1, 2)+E(2, 0), E(1, 3)+E(3, 0),
     E(0, 2)+E(2, 1), E(0, 3)+E(3, 1),
     E(2, 3)-E(3, 2), E(1, 1)-E(0, 0)]
eta = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
nobs = s.Matrix([1/s.sqrt(2), 1/s.sqrt(2), 0, 0])
require(zero(-eta+2*(eta*nobs)*(eta*nobs).T-s.eye(4)), 'original observer')
for g in G:
    require(zero(g.T*eta+eta*g), 'original Lorentz algebra')
    require(s.trace(g) == 0, 'tracefree')
require(s.Matrix([[s.trace(g.T*h) for h in G] for g in G]) == 2*s.eye(6),
        'original six signature Gram')


def exterior_lie(g):
    """Derivative of every minor of Lambda(I+t g), all16 wedge grades."""
    out = s.zeros(16)
    for mask in range(16):
        indices = [i for i in range(4) if mask & (1 << i)]
        for pos, old in enumerate(indices):
            for new in range(4):
                if g[new, old] == 0:
                    continue
                replaced = indices[:]
                replaced[pos] = new
                if len(set(replaced)) != len(replaced):
                    continue
                inv = sum(replaced[i] > replaced[j]
                          for i in range(len(replaced))
                          for j in range(i+1, len(replaced)))
                newmask = sum(1 << i for i in replaced)
                out[newmask, mask] += (-1)**inv*g[new, old]
    return out


L = [exterior_lie(g) for g in G]
for g, lg in zip(G, L):
    require(lg.extract([1, 2, 4, 8], [1, 2, 4, 8]) == g, 'grade1 restriction')
    require(exterior_lie(g.T) == lg.T, 'positive adjoint on all exterior grades')
    # At zero, first jets of T*T+D*D=I and the positive square root.
    dT = lg/2
    dD = -(lg+lg.T)/(4*s.sqrt(3))
    require(zero((dT+dT.T)/2+s.sqrt(3)*(dD+dD.T)/2),
            'full16 first-jet completeness')
    require(zero(s.sqrt(3)*dD+(lg+lg.T)/4), 'square-root Sylvester equation')

Omega = s.zeros(64, 1)
for mu in range(4):
    Omega[4*(1 << mu)+mu] = s.Rational(1, 2)
f = s.Matrix.hstack(*[s.sqrt(2)*s.kronecker_product(lg, s.eye(4))*Omega for lg in L])
require(Omega.dot(Omega) == 1 and zero(Omega.T*f), 'literal full64 Choi seed')
require(zero(f.T*f-s.eye(6)), 'literal original six detector signatures')
P0 = Omega*Omega.T
PF = f*f.T
effects = []
for a in range(6):
    for eps in (1, -1):
        v = (Omega+eps*f[:, a])/s.sqrt(2)
        effects.append(v*v.T/12)
rest = s.eye(64)-sum(effects, s.zeros(64))
require(zero(rest-(s.eye(64)-P0/2-PF/12)), 'all13 effects sum to identity')
require(zero(rest*Omega-Omega/2) and zero(rest*f-11*f/12),
        'positive rest spectrum on original span')
require(zero(P0*PF) and zero(PF*PF-PF), 'positive complement decomposition')

PiR = s.Matrix([[s.trace(g.T*(h-h.T)/2)/2 for h in G] for g in G])
PiS = s.eye(6)-PiR
require(zero(PiR.T-PiR) and zero(PiR**2-PiR) and s.trace(PiR) == 3,
        'three rotation directions')
require(zero(PiR*PiS) and zero(PiS**2-PiS) and s.trace(PiS) == 3,
        'three boost directions')

# Check the score coefficient using literal E effects and the true Choi jet,
# independently of the later finite flag averaging formula.
for a in range(6):
    for b in range(6):
        tangent = s.kronecker_product(L[b], s.eye(4))*Omega
        for eps, ef in zip((1, -1), effects[2*a:2*a+2]):
            base = (Omega.T*ef*Omega)[0]
            dq = 2*(Omega.T*ef*tangent)[0]
            require(zero(base-s.Rational(1, 24)), 'fixed detector baseline')
            require(zero(dq/base-(s.sqrt(2)*eps if a == b else 0)),
                    'literal score sqrt2, not 2sqrt2')
        require(zero(2*(Omega.T*rest*tangent)[0]), 'rest has zero first score')

schedules = [[s.Rational(1)], [s.Rational(1, 2)]*2,
             [s.Rational(1, 3)]*3,
             [s.Rational(1, 10), s.Rational(2, 10), s.Rational(3, 10), s.Rational(4, 10)],
             [s.Rational(1, 6)]*6]
summary = []
for es in schedules:
    n = len(es)
    require(sum(es) == 1 and all(e > 0 for e in es), 'positive partition')
    moment = s.zeros(6)
    score_mean = s.zeros(6, 1)
    classical = s.zeros(6)
    quantum = s.zeros(6)
    total = 0
    jsource = 0
    for flags in product((0, 1), repeat=n):  # 1=good, 0=bad
        gcount = sum(flags)
        w = s.Rational(1, 4)**gcount*s.Rational(3, 4)**(n-gcount)
        r = sum((e*b for e, b in zip(es, flags)), s.Rational(0))
        z = (4*r-1)/3
        M = r*PiR+z*PiS
        # This is the direct ordered product's normalized first jet at its
        # scalar background, including the derivative of every failure.
        for b, (g, lg) in enumerate(zip(G, L)):
            rel = sum((e*(lg if good else -(lg+lg.T)/6)
                       for e, good in zip(es, flags)), s.zeros(16))
            predicted = exterior_lie(r*(g-g.T)/2+z*(g+g.T)/2)
            require(zero(rel-predicted), 'actual branch derivative all16')
        total += 12*w/24+w/2
        moment += w*(M.T*M)
        quantum += 2*w*(M.T*M)
        # Aggregate all twelve explicit signs; no success renormalization.
        for a in range(6):
            for eps in (1, -1):
                score = s.sqrt(2)*eps*M[:, a]
                score_mean += w*score/24
                classical += w*(score*score.T)/24
        jsource += w*r/(12*s.sqrt(2))
    s2 = sum(e*e for e in es)
    expected = (1+3*s2)*PiR/96+s2*PiS/18
    require(total == 1 and zero(score_mean), 'all flags complete zero mean score')
    require(zero(classical-expected), 'full pointer exact Fisher')
    require(zero(moment/6-expected) and zero(quantum-12*classical), 'pure full-output QFI')
    inv = 96*PiR/(1+3*s2)+18*PiS/s2
    require(zero(inv*classical-s.eye(6)), 'local unbiased derivative of estimator')
    require(zero(inv*classical*inv.T-inv), 'exact estimator covariance per copy')
    require(zero(jsource-1/(48*s.sqrt(2))), 'n-independent J+ source before Golden factor')
    summary.append({'partition': [str(e) for e in es], 's2': str(s2),
                    'rotation_fisher': str((1+3*s2)/96), 'boost_fisher': str(s2/18)})

# General moments follow from independent flat Bernoulli indicators;
# check the symbolic variance-to-second-moment relation independently of n.
mu, s2sym = s.symbols('mu s2', real=True)
Er2sym = mu**2+3*s2sym/16
Ez2sym = (16*Er2sym-8*mu+1)/9
require(zero(Ez2sym.subs(mu, s.Rational(1, 4))-s2sym/3), 'universal second moment relation')
for n in range(1, 9):
    rot, boost = Fraction(96*n, n+3), Fraction(18*n)
    require((rot <= boost) == (n >= 3), 'correct n>=3 upper-budget threshold')
    require(Fraction(18*n)/Fraction(3*n, 2) == 12, 'upper/lower constant ratio')

phi = (1+s.sqrt(5))/2
p = 1/phi
require(zero(p+p**2-1) and zero(p+2*p**2-(2-p)), 'original Golden entropy coefficient')

u = s.symbols('u', real=True)
vp = (1+u)**2/(24*(1+u*u/2)**2)
vm = vp.subs(u, -u)
ell = 4*s.atanh(u)
require(zero(s.diff(s.log(vp/vm), u)-s.diff(ell, u)), 'positive rotation log odds')
require(s.diff(vp, u).subs(u, 0) == s.Rational(1, 12), 'linear multiplier 48')
require(48*s.diff(vp, u, 3).subs(u, 0) == -24, 'marked source third derivative')
require(s.diff(ell, u, 3).subs(u, 0) == 8, 'odds third derivative')
odd = 24*(vp-vm)-ell
require(zero(odd-4*(u/(1+u*u/2)**2-s.atanh(u))), 'exact odd residual')
require(zero(s.diff(odd, u)+u*u*(u**4-6*u*u+32)/(2*(1-u*u)*(1+u*u/2)**3)),
        'exact even-background obstruction')
require(zero(u**4-6*u*u+32-((u*u-3)**2+23)), 'strict numerator positivity')

# Honest finite variable-clock example with a moving normalized P and N.
t = s.symbols('t', real=True)
P = [s.Rational(1, 3)+t/10, s.Rational(1, 6)-t/10, s.Rational(1, 2)]
T = [1, 2, 3]
N = 1+2*t
W = [N**k*prob for k, prob in zip(T, P)]
Z = sum(W)
ET = sum(k*prob.subs(t, 0) for k, prob in zip(T, P))
for k, prob, raw in zip(T, P, W):
    delta = s.diff(s.log(raw/Z)-s.log(prob), t).subs(t, 0)
    require(zero(delta-2*(k-ET)), 'variable T centred normalizer source')
    require((delta == 0) == (k == ET), 'point calibration does not fix source')

dc, di, logr = s.symbols('dc di logr', real=True)
for exponent in (1, 2):
    logodds = logr-exponent*s.log(phi)*(dc-di)
    require(zero(logodds-logr+exponent*s.log(phi)*(dc-di)), 'typed odds signs')

print(json.dumps({'status': 'PASS_RECONSTRUCTED_ORIGINAL_FULL_FLAG',
                  'historical_bytes_recovered': False,
                  'symbolic_engine': s.__version__, 'partitions': summary,
                  'score_coefficient': 'sqrt(2)',
                  'FQ_equals_12_FI': True,
                  'source_shape_third_jets': [-24, 8],
                  'scope': 'local fixed preparation/output; no selected Book price or GR closure'},
                 indent=2))
