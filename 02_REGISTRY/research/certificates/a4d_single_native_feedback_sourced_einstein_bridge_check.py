#!/usr/bin/env python3
"""Exact golden feedback source split, finite-t isocoupling witness and
full-scene weak-source checks. Research only: no native matter forcing/GR.
No matrix dimensions are silently removed: 264+184+36+44=528.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import sqrt, log
import json


@dataclass(frozen=True)
class Golden:
    # a+b*p, p=(sqrt(5)-1)/2, p*p=1-p, p'=-1-p.
    a: Fraction
    b: Fraction = Fraction(0)

    def __init__(self, a=0, b=0):
        object.__setattr__(self, "a", Fraction(a))
        object.__setattr__(self, "b", Fraction(b))

    @staticmethod
    def put(x):
        return x if isinstance(x, Golden) else Golden(x)

    def __add__(self, other):
        v = self.put(other)
        return Golden(self.a + v.a, self.b + v.b)

    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-self.put(other))

    def __rsub__(self, other):
        return self.put(other) - self

    def __mul__(self, other):
        v = self.put(other)
        return Golden(self.a*v.a + self.b*v.b,
                      self.a*v.b + self.b*v.a - self.b*v.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*(self.a-self.b)-self.b*self.b
        if norm == 0:
            raise ZeroDivisionError("zero golden norm")
        return Golden((self.a-self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self*self.put(other).inverse()

    def __rtruediv__(self, other):
        return self.put(other)/self

    def __pow__(self, k):
        assert isinstance(k, int) and k >= 0
        out = Golden(1)
        for _ in range(k):
            out = out*self
        return out

    def value(self):
        return float(self.a) + float(self.b)*(sqrt(5)-1)/2


p = Golden(0, 1)
one = Golden(1)
z = p**2
e0 = p**2
L = 4*p**3
a = one-L
assert p**2 + p == one
assert a == p**6
assert 4*(one-2*e0) == L
assert one-z == p

L3 = one-(130*p-81)**2
Lv = one-((854*p-531)/11)**2
spectrum = [
    ("zero", Golden(0), 264),
    ("L", L, 184),
    ("L3", L3, 36),
    ("Lv", Lv, 44),
]
assert sum(m for _,_,m in spectrum) == 528
assert all(Golden(0).value() <= b.value() < 1 for _,b,_ in spectrum)
assert L != L3

Q = lambda b: one-z*b
R = lambda b: one-z*(L+a*b)
C = lambda b: (one-b)/R(b)
W = lambda b: one/Q(b)+a/R(b)
H = lambda b: R(b)**2/Q(b) + a*R(b)
C0 = sum(m*C(b) for _,b,m in spectrum)
assert C0.value() > 0
assert all(W(b).value() > 0 for _,b,_ in spectrum)

# The operator-J covariance split and isocoupling tangents are exact
# in the field Q(p), with NO sampled floating-point matrix rank.
m1,m2 = 184,36
b1,b2=L,L3
db1=R(b1)**2/m1
db2=-(R(b2)**2)/m2
dC = -(one-z)*(m1*db1/R(b1)**2+m2*db2/R(b2)**2)
assert dC == Golden(0)
dJ = m1*W(b1)*db1 + m2*W(b2)*db2
assert dJ == H(b1)-H(b2)
assert dJ == (Q(b1)-Q(b2))*(
    2*a**2 - L**2*(one-z)**2/(Q(b1)*Q(b2)))
assert L**2*(one-z)**2 - 2*a**2 == 2*p**8*(8-p**4)
assert dJ != Golden(0) and dJ.value() > 0

# Directly independent full finite determinant source check:
# AF eigenvalue e0+c f_i, SCENE b_j+c m_j; every original mode kept.
zf, Lf, af, e0f = z.value(), L.value(), a.value(), e0.value()
scene=[(b.value(),mult) for _,b,mult in spectrum]
mvalues=[0,.17,-.09,.04]
old=[(-.15,2),(.27,3)]
gavg=sum(w*f for f,w in old)/sum(w for _,w in old)
Wm = sum(mult*W(b).value()*dv
         for (_,b,mult),dv in zip(spectrum,mvalues))
target=gavg+Wm/(Lf*C0.value())

def lam(e):
    return 4*e*(1-e)

def det_price(c):
    bvals=[b+c*dm for (b,_),dm in zip(scene,mvalues)]
    assert all(0 <= b < 1 for b in bvals)
    qpart=-sum(mult*log(1-zf*b) for b,(_,mult) in zip(bvals,scene))
    rpart=-sum(
        w*sum(mult*log(1-zf*(lam(e0f+c*f)
                      +(1-lam(e0f+c*f))*b))
              for b,(_,mult) in zip(bvals,scene))
        for f,w in old
    )/sum(w for _,w in old)
    return qpart+rpart

J0=det_price(0)
errors=[]
for c in (0.04,0.02,0.01,0.005,0.0025):
    value=(det_price(c)-J0)/(c*zf*Lf*C0.value())
    err=abs(value-target)
    errors.append(err)
    assert err < 0.25*c
assert all(errors[i+1] < errors[i] for i in range(len(errors)-1))
assert abs(dJ.value()-0.09642053726030697)<3e-12
assert abs(C0.value()-460.1712924619965)<1e-9

# A pure commutator [X,B0] is off-diagonal in the B0 eigenbasis;
# its full source and coupling scalar derivatives vanish because
# W(B0) and R(B0)^-2 are diagonal. A constant fixed B has NO
# rho/preparation derivative of the state-independent determinant.
Bdiag=(L.value(),L3.value())
skew=((0,1),(-1,0))
comm=((0,Bdiag[1]-Bdiag[0]),(Bdiag[1]-Bdiag[0],0))
assert comm[0][0] == comm[1][1] == 0
assert sum((W(L).value(),W(L3).value())[i]*comm[i][i]
           for i in range(2))==0

# Exact full-metric-null source discriminator on a 2x2 eigenpreparation.
# Delta=diag(1,3); rho=diag(1,0), tau=diag(1/4,3/4),
# h'=I. A=rho-tau=diag(3/4,-3/4) commutes with Delta.
# A true conjugacy direction [K,Delta] is symmetric/offdiagonal and
# has ZERO source; the spectral diagonal direction has 3/4 source.
from fractions import Fraction as FQ
At=(FQ(3,4),-FQ(3,4))
commutator_delta=((0,2),(2,0))
metric_diagonal=((1,0),(0,0))
source_offdiag=sum(At[i]*commutator_delta[i][i] for i in range(2))
source_diagonal=sum(At[i]*metric_diagonal[i][i] for i in range(2))
assert source_offdiag==0
assert source_diagonal==FQ(3,4)
# The spectral pinch of the first direction is zero, whereas the
# second is unchanged: no Hessian inverse or spectral-gap premise.

print(json.dumps({
    "terminal":"PASS: exact Q(phi) sourced feedback/isocoupling",
    "golden_test_z":"p^2 (research evaluation, not physical selection)",
    "scene528":{name:mult for name,_,mult in spectrum},
    "C0":C0.value(),
    "coupling_coefficient_zLC0":zf*Lf*C0.value(),
    "fixed_coupling_dC":dC.value(),
    "nonzero_scene_dJ_over_nuKz":dJ.value(),
    "two_source_weak_target":target,
    "weak_normalized_abs_errors":errors,
    "isospectral_gauge_source":"ZERO",
    "native_physical_matter_source":"OPEN"
},indent=2,sort_keys=True))
