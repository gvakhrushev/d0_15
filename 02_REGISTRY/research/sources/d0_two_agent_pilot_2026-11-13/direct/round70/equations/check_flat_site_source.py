"""Exact CAR16, flat trace pairing, native reporter derivative, and finite coin."""
from itertools import combinations
import sympy as sp


def unit(i, j):
    return sp.eye(4)[:, i] * sp.eye(4)[:, j].T


def fock_trace(n, p):
    derivative = n*p
    val = 0
    for grade in range(1, 5):
        for ids in combinations(range(4), grade):
            m = p.extract(ids, ids)
            d = derivative.extract(ids, ids)
            for k in range(grade):
                replaced = m.copy()
                replaced[:, k] = d[:, k]
                val += replaced.det()
    return sp.expand(-val/8)


eta = sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
J = unit(2,3)-unit(3,2)
C,S = sp.symbols("C S")
# Parallel operator on the xy plane for d exp(t sigma) dx,dy, positive
# connection convention. The rotation is exp(-theta J).
P = sp.eye(4) + (C-1)*(unit(2,2)+unit(3,3))-S*J
pair = list(combinations(range(4), 2))
basis = [(eta[:,i]*eta[:,j].T-eta[:,j]*eta[:,i].T)*eta for i,j in pair]
assert basis[-1] == -J
assert fock_trace(basis[-1], P) == S
assert all(fock_trace(n, sp.eye(4)) == 0 for n in basis)
metric = sp.Matrix(6,6,lambda i,j: -sp.trace(basis[i]*basis[j])/2)
assert metric.det() != 0
dual = [sum((metric.inv()[k,j]*basis[k] for k in range(6)), sp.zeros(4)) for j in range(6)]
assert all(-sp.trace(n*x)/2 == int(i == j) for i,n in enumerate(basis) for j,x in enumerate(dual))
# Flat derivative at one link gives opposite contributions on two adjacent cells.
for n in (8, 16, 32):
    cell = n//2
    angle = [int(j == cell) for j in range(n)]
    density = [angle[(j+1)%n]-angle[j] for j in range(n)]
    assert sum(density) == 0 and density[cell-1] == 1 and density[cell] == -1
for power in (5, 6, 7):
    n = 2**power
    count_axis = sum(1 for k in range(-n//2, n//2) if -n//8 <= k < n//8)
    assert sp.Rational(count_axis**4, n**4) == sp.Rational(1,256)
for length in (2, 5, 12):
    incidence = sp.Matrix(length,length,lambda i,j: int(i == j)-int(i+1 == j))
    assert incidence.det() == 1

p = (sp.sqrt(5)-1)/2
x, z = sp.symbols("x z", real=True)
E = p*p*(1+x)
ell = 4*E*(1-E)
b = 4*p*p*(1-p*p)
a = ell + (1-ell)*b
r = z*(a+b)-z*z*a*b
r_f = 4*z*p**11*(1-z*4*p**3)
assert sp.simplify(r.diff(x).subs(x,0)-r_f) == 0
assert sp.simplify(r-r.subs(x,-x)-2*r_f*x) == 0
h, t = sp.symbols("h t", positive=True)
assert sp.diff(sp.sin(t*h*h)/(h*h),t).subs(t,0) == 1

# Golden-pair XOR conditional fair bit, followed by 20 paid copies.
assert sp.simplify(p+p*p-1) == 0
assert sp.simplify((p*p**2)/(p*p**2+p**2*p)-sp.Rational(1,2)) == 0
coin = sp.Rational(1,2)**20
assert coin == sp.Rational(1,1048576)
q = sp.symbols("q", positive=True)
Z = 1-coin+coin*q
assert sp.cancel(sp.diff(q/Z,q) - (1-coin)/Z**2) == 0
print("PASS: all CAR16 degrees, Lorentz duals for all six faces, flat telescope, fixed volume 1/256, exact seven-bank coefficient, and retained Doob coin.")
