"""Absolute edge-rooted Q8 classes, determinant contrasts, and the Gram clock test."""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from math import isqrt

import sympy as sp


t, k, b = sp.symbols("t k b")
zone = [0]*9 + [1]*11 + [2]*13
cells = [[0], list(range(1, 9)), [9], list(range(10, 20)), list(range(20, 33))]
nverts = len(zone)
edges = [(i, j) for i, j in product(range(nverts), repeat=2) if zone[i] != zone[j]]
assert len(edges) == 718
out = [[j for i, j in edges if i == v] for v in range(nverts)]


def is_ab(i, j):
    return {zone[i], zone[j]} == {0, 1}


def small_matrix(parity, mark):
    def w(i, j):
        if zone[i] == zone[j]:
            return 0
        sign = parity if {i, j} == {0, 9} else 1
        return sign * (k if is_ab(i, j) else 1) * (mark if (i, j) == (0, 9) else 1)
    rows = [[sum(w(cell[0], j) for j in right) for right in cells] for cell in cells]
    for ci, cell in enumerate(cells):
        for i in cell:
            assert [sum(w(i, j) for j in right) for right in cells] == rows[ci]
    return sp.Matrix(rows)


def determinant(q):
    # All rows are cell-constant in the full matrix, so its image is in the equitable space.
    return sp.expand((sp.eye(5)-t*q).det(method="domain-ge"))


def coefficients(expr, degree):
    numerator, denominator = map(lambda a: sp.Poly(a, t), sp.cancel(expr).as_numer_denom())
    values = []
    for n in range(degree + 1):
        correction = sum(denominator.nth(j)*values[n-j] for j in range(1, n+1))
        values.append(sp.expand((numerator.nth(n)-correction)/denominator.nth(0)))
    return values


def multiply(left, right):
    # Elements of Q8 are numbered as 0..3 = 1,i,j,k and 4..7 = their negatives.
    a, i = divmod(left, 4)
    b, j = divmod(right, 4)
    negative = (i == j and i != 0) or (i, j) in ((2, 1), (3, 2), (1, 3))
    return 4*((a+b+int(negative)) % 2) + (i ^ j)


def inverse(g):
    return g if g % 4 == 0 else g ^ 4


site_frame = [v % 8 for v in range(nverts)]
link = {(i, j): multiply(multiply(inverse(site_frame[i]), site_frame[j]),
                         4 if {i, j} == {0, 9} else 0) for i, j in edges}
assert all(multiply(g, inverse(g)) == 0 for g in range(8))
assert all(multiply(multiply(a, b), c) == multiply(a, multiply(b, c))
           for a, b, c in product(range(8), repeat=3))
assert all(link[j, i] == inverse(v) for (i, j), v in link.items())

degree = 8
counts = {0: [defaultdict(int) for _ in range(degree+1)],
          4: [defaultdict(int) for _ in range(degree+1)]}
front = {(9, link[0, 9], 1): 1}
for n in range(1, degree+1):
    nxt = defaultdict(int)
    for (v, group, h), num in front.items():
        if v == 0:
            counts[group][n][h] += num
        if n < degree:
            for w in out[v]:
                nxt[w, multiply(group, link[v,w]), h+is_ab(v,w)] += num
    front = nxt

answers = {}
for sign in [1, -1]:
    initial = determinant(small_matrix(sign, 1))
    modified = determinant(small_matrix(sign, b))
    answers[sign] = sp.cancel((modified/initial - 1)/(1-b))
    assert b not in answers[sign].free_symbols
    if sign == 1:
        D = 1 - (99*k**2 + 260)*t**2 - 2574*k*t**3
        N = k*t**2*(k+13*t)
        assert sp.expand(initial-D) == 0 and sp.cancel(answers[sign]-N/D) == 0
for group, mark_sign in [(0, 1), (4, -1)]:
    raw = coefficients((answers[1] + mark_sign*answers[-1])/2, degree)
    for n in range(degree+1):
        expected = sum(c*k**h for h, c in counts[group][n].items())
        assert sp.expand(raw[n] - expected) == 0

# The Q8 regular center has four +1 and four -1 eigenvectors.
central = sp.zeros(8)
for g in range(8):
    central[multiply(4, g), g] = 1
assert central.eigenvals() == {-1: 4, 1: 4}

d0 = sp.Poly(D.subs(k, 1), t)
assert sp.gcd(d0, d0.diff()).degree() == 0
assert [sp.sign(d0.eval(sp.Rational(-1, n))) for n in (8, 10, 12, 13)] == [1, -1, -1, 1]
assert sp.gcd(d0, sp.Poly(N.subs(k, 1), t)).degree() == 0
assert sp.factor(D.diff(k) + 198*t**2*(k+13*t)) == 0
speed = -198*(1+13*t)/(718+7722*t)
assert sp.cancel(-D.diff(k).subs(k,1)/(t*D.diff(t).subs(k,1)) - speed) == 0
assert 13*718-7722 == 1612

# At the actual feedback fugacity, enclose the historical values using positive
# words only. No cancellation of small signed contributions and no eigenvalue rounding.
scale = 10**36
s5 = isqrt(5*scale**2)
plo, phi = (Q(s5+i, scale)-1 for i in (0, 1))
plo, phi = plo/2, phi/2
tlo, thi = plo**2/2**20, phi**2/2**20
ratio = 24*thi
assert ratio < 1
# Beyond the last depth: at most 24^(n-1) completions, j<=n charged AB visits.
tail = thi*ratio**degree/(1-ratio)
tail_j = tail*(degree+1+ratio/(1-ratio))


def logphi_at(p):
    # ln(1+p) = 2 atanh(p/(2+p)).
    v = p/(2+p)
    partial = 2*sum(v**(2*i+1)/(2*i+1) for i in range(18))
    return partial, partial + 2*v**37/(37*(1-v*v))


loglo, loghi = logphi_at(plo)[0], logphi_at(phi)[1]
masses = {}
for q, name in ((0, "+1"), (4, "-1")):
    def partial(tick, moment):
        return sum(tick**n * sum(c*(h if moment else 1) for h, c in row.items())
                   for n, row in enumerate(counts[q]))
    lo, hi = partial(tlo, False), partial(thi, False) + tail
    masses[q] = (lo, hi)
    lowj, highj = partial(tlo, True), partial(thi, True) + tail_j
    gradlo, gradhi = -loghi*highj/lo, -loglo*lowj/hi
    print(name, "absolute M approx", format(float(lo), ".13g"),
          "enclosure width <", format(float(hi-lo)*1.01, ".3g"),
          "D_tau ln(M)", format(float(gradlo), ".13g"), format(float(gradhi), ".13g"))
    assert lo > Q(1,10**(13 if q == 0 else 19)) and hi-lo < Q(1, 10**42)
    assert (-Q(963,1000) < gradlo <= gradhi < -Q(962,1000) if q == 0
            else -Q(482,1000) < gradlo <= gradhi < -Q(481,1000))
print("718 directed edges, Q8 words through length 8, exact determinant ratios, two distinct pole speeds verified.")


# Two normalized class histograms recover an absolute mass at the same fixed clock.
Tlo, Thi = masses[0][0]+masses[4][0], masses[0][1]+masses[4][1]
Hlo, Hhi = masses[0][0]-masses[4][1], masses[0][1]-masses[4][0]
ylo, yhi = Hlo/Thi, Hhi/Tlo
clo, chi = 1-phi, 1-plo
gaplo = clo*Tlo*ylo*(1-yhi)/(1+chi*Thi*yhi)
gaphi = chi*Thi*yhi*(1-ylo)/(1+clo*Tlo*ylo)
assert Q(47,10**20) < gaplo < gaphi < Q(49,10**20)
print("paid parity gap y_p-y at actual fugacity:",float(gaplo),float(gaphi))

def cq(a, b):
    c = [sp.Integer(0)]*8
    for i, j in product(range(8),repeat=2):
        c[multiply(i,j)] += a[i]*b[j]
    return sp.Matrix(c)

def all_returns(primitive):
    basis = sp.eye(8)
    left = sp.Matrix.hstack(*(cq(primitive,basis[:,i]) for i in range(8)))
    return (basis-left).inv()*primitive

# Noncentral exact finite group algebra; the physical 718-edge example is above.
unit = sp.eye(8)[:,0]
primitive = sp.Matrix([0,7,3,1,2,3,0,1])/64
M = all_returns(primitive)
for frac in (sp.Rational(1,2), sp.Rational(2,3)):
    changed = all_returns(frac*primitive)
    first, second = M/sum(M), changed/sum(changed)
    v = first-cq(second,first)
    assert v != sp.zeros(8,1)
    inferred = (second-first).dot(v)/((1-frac)*v.dot(v))
    assert inferred == sum(M) and first*inferred == M
    # Degenerate cause: Haar on a subgroup, arbitrary total primitive weight.
    haar = (unit + sp.eye(8)[:,4])/2
    baseline = all_returns(haar/4)
    after = all_returns(frac*haar/4)
    assert baseline/sum(baseline) == after/sum(after) == haar
# Canonical simulator uses real address and exact Golden success probabilities;
# word 01 (p^3) is selected only under the genuine raised charge.
gold = (sp.sqrt(5)-1)/2
assert sp.simplify(gold + gold**2 - 1) == 0
assert len(edges) <= 33**2 and 33 < 2**20
assert sp.simplify(2*gold**3 / (1 - gold**2 - gold**4) - 1) == 0

# One registered repeat count, or three specified full words, suffice as well.
ell = sum(primitive)
total = sum(M)
repeat_chance = (total-ell)/total
assert repeat_chance == ell and repeat_chance/(1-repeat_chance) == total
power = primitive
for n in range(1, 5):
    assert sum(power)/total == (1-ell)*ell**(n-1)
    power = cq(power, primitive)
# Actual two-tick returns via vertices 9 or 20, and their concatenation.
w, v = t**2*k**2, t**2
clock2, clock4 = sp.symbols("clock2 clock4", positive=True)
Z = clock2*w + clock2*v + clock4*w*v
assert sp.cancel(((clock4*w*v/Z)/((clock2*w/Z)*(clock2*v/Z))
                  * clock2**2/clock4) - Z) == 0
