"""All-zero readout against independent Golden bits on the stopped full128 archive."""
import importlib.util
from pathlib import Path

import sympy as sp

helper = Path(__file__).resolve().parents[2] / "round69/primary/check_stopped_fine.py"
spec = importlib.util.spec_from_file_location("archive_7gb", helper)
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)
jet = upstream.original_jet()
ns, dns = jet["ns"], jet["dns"]
a, da = jet["a"], jet["da"]
lam = jet["kappa"]
p = (sp.sqrt(5)-1)/2
r = 16


def simple(matrix):
    return matrix.applyfunc(sp.expand)


def exact(value):
    return sp.collect(sp.expand(value), sp.sqrt(5))


data = []
for j, (n, dn) in enumerate(zip(ns, dns)):
    b = simple(n.H*a)
    db = simple(dn.H*a + n.H*da)
    data.append((bin(j).count("1"), b, db))


def weighted(func):
    bins = [sp.zeros(r) for _ in range(7)]
    for h, block, deriv in data:
        bins[h] += func(block, deriv)
    return sum((exact(p**h)*simple(m) for h,m in enumerate(bins)), sp.zeros(r)).applyfunc(exact)


A = weighted(lambda b, db: b.H*b)
dA = weighted(lambda b, db: db.H*b + b.H*db)
B = weighted(lambda b, db: b*b.H)
dB = weighted(lambda b, db: db*b.H + b*db.H)
effect = (p**7*((1-4*p**2*lam)*sp.eye(r)+4*p**4*A)).applyfunc(exact)
deffect = (4*p**11*dA).applyfunc(exact)
continued = (4*p**11*B/r).applyfunc(exact)
dcontinued = (4*p**11*dB/r).applyfunc(exact)
stopped = exact(sp.trace(effect)/r)
dstopped = exact(sp.trace(deffect)/r)
first_tail = exact(sp.trace(effect*continued))
dfirst_tail = exact(sp.trace(deffect*continued + effect*dcontinued))
assert exact(dstopped-(sp.Rational(253449,102400)-56673*sp.sqrt(5)/51200)) == 0
delta01 = exact(dstopped+dfirst_tail)
continued_twice = (4*p**11*weighted(lambda b, db: b*continued*b.H)).applyfunc(exact)
dcontinued_twice = (4*p**11*weighted(lambda b, db: db*continued*b.H +
                                        b*dcontinued*b.H + b*continued*db.H)).applyfunc(exact)
second_tail = exact(sp.trace(effect*continued_twice))
dsecond_tail = exact(sp.trace(deffect*continued_twice + effect*dcontinued_twice))
delta012 = exact(delta01 + dsecond_tail)
mass012 = exact(stopped + first_tail + second_tail)

# The spectral insertion norms of the two actual marked instruments.
frob = exact(sum(sum(sp.expand(x*sp.conjugate(x)) for x in db) for _,_,db in data))
assert frob < 1                         # conservative; each true sum has a smaller norm
assert 4*p**3 < 1 and 4*p**4 < 1
q = 4*p**3*lam
assert q < sp.Rational(1,50) and p**7 < sp.Rational(1,25) and p**8 < sp.Rational(1,40)
u, v = sp.Rational(1,25), sp.Rational(1,2000)
du, dv = sp.Rational(2,25), sp.Rational(1,100)
# n additional continuing symbols. Sum derivatives of the n>=2 positive terms.
error = du*v**2/(1-v) + u*dv*(1/(1-v)**2-1)
assert error < sp.Rational(43,10**8)
# Determine arbitrary tiny quadratic-field signs by rational squaring, not floats.
def negative(value):
    value = exact(value)
    c, b = value.as_coeff_Add()
    b = sp.simplify(b/sp.sqrt(5))
    if b == 0:
        return c < 0
    if b > 0:
        return c < 0 and c**2 > 5*b**2
    return c <= 0 or 5*b**2 > c**2

assert negative(delta01+error)
error3 = du*v**3/(1-v) + u*dv*(1/(1-v)**2-1-2*v)
mass_error3 = u*v**3/(1-v)
assert negative(delta012+error3+sp.Rational(36444,10**10))
assert negative(-delta012+error3-sp.Rational(36452,10**10))
assert negative(sp.Rational(3381657,10**8)-mass012)
assert negative(mass012+mass_error3-sp.Rational(3381658,10**8))
plow, phigh = sp.Rational(3381657,10**8), sp.Rational(3381658,10**8)
dlow = sp.Rational(36444,10**10)
assert dlow**2/(phigh*(1-plow)) > sp.Rational(406,10**12)
assert dlow/phigh > sp.Rational(1077,10**7)
print("P(immediate STOP, all matching) =", stopped, float(stopped))
print("D P(immediate STOP, all matching) =", dstopped, float(dstopped))
print("P(one CONT then STOP, all matching) =", first_tail, float(first_tail))
print("D P(one CONT then STOP, all matching) =", dfirst_tail, float(dfirst_tail))
print("two-level source =", delta01, float(delta01))
print("uniform tail in first source <=", error, float(error))
print("all stopped source interval:", float(delta01-error), float(delta01+error))
print("with two CONT terms, full match source:", float(delta012-error3), float(delta012+error3))
print("full match probability:", float(mass012), float(mass012+mass_error3))
# Complete additive code length on the actual surviving density and its zero first jet.
unweighted_b = simple(sum((b*b.H for _,b,_ in data), sp.zeros(r)))
dunweighted_b = simple(sum((db*b.H+b*db.H for _,b,db in data), sp.zeros(r)))
assert unweighted_b == lam*sp.eye(r) and dunweighted_b == sp.zeros(r)
hamming_jet = sum(bin(i).count("1")*sp.trace(d*n.H+n*d.H)
                  for i,(n,d) in enumerate(zip(ns,dns)))
assert sp.expand(hamming_jet) == sp.Rational(9,5)
d_length = exact(4*p**2*lam*hamming_jet/r)/(1-q)
assert sp.Rational(2449,10**6) < d_length < sp.Rational(2450,10**6)
# log(phi) = 2*atanh(p^3), using two terms below and a geometric tail above.
t = p**3
l_lo = 2*(t+t**3/3)
l_hi = l_lo+2*t**5/(5*(1-t**2))
assert sp.Rational(48,100) < l_lo and l_hi < sp.Rational(482,1000)
assert sp.Rational(48,100)*sp.Rational(2449,10**6)-sp.Rational(1650,10**5)>-sp.Rational(1533,10**5)
assert sp.Rational(482,1000)*sp.Rational(2450,10**6)-sp.Rational(1636,10**5)<-sp.Rational(1517,10**5)
print("D mean full Golden archive length", float(d_length))
# Flip only the reference port bit. On n CONT and one STOP the likelihood ratio is p^(1-n).
mass_b012 = exact(p*stopped + first_tail + (1+p)*second_tail)
delta_b012 = exact(p*dstopped + dfirst_tail + (1+p)*dsecond_tail)
vb, dvb = sp.Rational(1,1000), sp.Rational(1,50)
assert v/p < vb and dv/p < dvb
mass_b_err = u*vb**3/(1-vb)
delta_b_err = du*vb**3/(1-vb) + u*dvb*(1/(1-vb)**2-1-2*vb)
assert negative(mass_b012 + mass_b_err-sp.Rational(5,8)*mass012)
assert negative(delta_b012+delta_b_err)
assert 0 < q < p**2 < sp.Rational(1,2)
assert exact((1-(1+p)*q)-p*(1-q) - (p**2 - q)) == 0
assert -sp.Rational(1517,10**5)*sp.Rational(3,8) < -sp.Rational(568,10**5)
# Physical blank on an unmeasured wire without SourceI, with all failed attempts retained.
v0 = sp.Matrix([sp.sqrt(p), p])
golden = sp.Matrix([[sp.sqrt(p),-p],[p,sp.sqrt(p)]])
flip = sp.Matrix([[0,1],[1,0]])
assert sp.simplify((golden*flip*v0)[0]) == 0
assert sp.simplify(p*(golden*v0)[0]**2-p**7) == 0
# Finite schedules use only an observed base and k independent auxiliary Golden bits.
from itertools import product
for count in (1,2,4):
    t_plus = t_minus = 0
    for flags in product((0,1),repeat=count+1):
        base, rare = flags[0], all(flags[1:])
        mass = p**(len(flags)+sum(flags))
        t_plus += mass*int(base or rare)
        t_minus += mass*int(base and not rare)
    assert sp.simplify(t_plus-p**2-(1-p**2)*p**(2*count)) == 0
    assert sp.simplify(t_minus-p**2+p**2*p**(2*count)) == 0
print("flipped full match bounds:", float(mass_b012), float(mass_b012+mass_b_err))
print("flipped source bounds:", float(delta_b012-delta_b_err), float(delta_b012+delta_b_err))
print("both measured and unread controls: oriented 2-by-2 determinant < -0.00568")
# A normalized one-visit observer retains all immediate STOP labels and one CONT outcome.
from collections import defaultdict
mass_classes = defaultdict(lambda: sp.Integer(0))
for n, dn in zip(ns, dns):
    eigen_sum = sp.expand(sp.trace(n*n.H))
    slope = sp.expand(sp.trace(dn*n.H+n*dn.H))
    if slope:
        mass_classes[eigen_sum] += slope
rat = sp.Rational
assert dict(mass_classes) == {rat(324,25):-rat(27,10), rat(1,25):rat(3,10),
                              rat(9,40):rat(6,5), rat(27,200):rat(6,5)}
ratio_bound = 2**6*rat(1,25)*rat(9,40)**4*rat(27,200)**4/rat(324,25)**9
assert 1/p < 2 and ratio_bound < 1 and p < 1-q
print("one-visit normalized observer: KL_s<0, KL_t>0, F_s>0, F_t>0")
