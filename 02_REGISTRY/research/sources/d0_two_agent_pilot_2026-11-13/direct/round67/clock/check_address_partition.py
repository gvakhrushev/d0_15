"""Exact RC3/Fock address masses, derivatives and native Golden readout bounds."""
from fractions import Fraction as Q
from math import factorial
import sympy as sp


def fock_trace(matrix, n):
    """Tr Sym^n(matrix) by the complete homogeneous Newton identity."""
    h = [sp.Integer(1)]
    for k in range(1,n+1):
        h.append(sum((matrix**i).trace()*h[k-i] for i in range(1,k+1))/k)
    return h[n]


x = sp.Symbol("x", real=True)
z = sp.Rational(1,7)
alpha = z/(1-z)
C = sp.Matrix([[x,sp.Rational(1,5),0],[0,sp.Rational(1,3),sp.Rational(1,4)]])
f = sp.eye(3) - C.T*C
h0 = C[:,:1]*C[:,:1].T
h1 = C[:,1:]*C[:,1:].T
h = h0+h1
assert h0*h1 != h1*h0
empty1 = (sp.eye(3)-z*f).det()/(sp.eye(1)-z*f[:1,:1]).det()
root_empty1 = (1-z)**2*(sp.eye(2)+alpha*h).det()/(sp.eye(2)+alpha*h0).det()
assert sp.factor(empty1-root_empty1)==0
dl = ((sp.eye(2)+alpha*h).inv()*alpha*h.diff(x)).trace() - ((sp.eye(2)+alpha*h0).inv()*alpha*h0.diff(x)).trace()
assert sp.factor(sp.diff(empty1,x)/empty1 - dl) == 0
q=sp.Symbol("q",positive=True)
Z=1/(sp.eye(3)-z*f).det()
assert sp.cancel((1-q)*(Z*empty1/(1-q))+q*(Z*(1-empty1)/q)-Z)==0
# Both labels can be occupied in the same symmetric tensor, starting at n=2.
t = f.subs(x,sp.Rational(1,4))
assert t.is_positive_definite
assert fock_trace(t,1) == fock_trace(t[:1,:1],1)+fock_trace(t[1:,1:],1)
assert all(fock_trace(t,k)>fock_trace(t[:1,:1],k)+fock_trace(t[1:,1:],k) for k in (2,3,4))


p=(sp.sqrt(5)-1)/2
one_label = (1-p**3)/(2-p-p**3)
assert sp.simplify(one_label-sp.Rational(2,3))==0
eps=sp.Rational(1,64)
assert (1-p**3-eps)/(2-p-p**3+2*eps) > sp.Rational(3,5)
zn=Q(1,2**20)
assert ((1-zn)**-8-1-8*zn)/(4*zn) < Q(1,1000)
assert Q(3,5)/(1+Q(1,1000))>Q(1,2)
assert 4*zn < Q(1,3) < p**2
# A66 actual ranks after four pairs; a rational upper bound for ln(2).
log2_upper=Q(694,1000)
assert sum(log2_upper**k/factorial(k) for k in range(6))>2
for Lb in (4*48**4,4*96**4):
    assert zn*Lb-4*zn/(1-zn)>29*log2_upper
print("PASS: noncommuting root minors and source, symmetric mixed occupations, 2/3 single return, finite nonvacuum bound and both-mark A66 bound")
