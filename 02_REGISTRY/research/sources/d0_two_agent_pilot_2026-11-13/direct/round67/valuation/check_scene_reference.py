"""Exact tests for the two native scene measurements and the four-edge curve."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


root = Path(__file__).resolve().parents[7]
owner = (root / "03_FORMALIZATION/D0/Integration/V15/RawZone.lean").read_text()
assert "!![0, 11, 13; 9, 0, 13; 9, 11, 0]" in owner
zone = [0]*9 + [1]*11 + [2]*13
dim = len(zone)
adj = sp.Matrix(dim, dim, lambda i, j: int(zone[i] != zone[j]))
basis = sp.eye(dim)
u = basis[:, 0] - basis[:, 1]
v = basis[:, 9] - basis[:, 10]
edge = u*v.T + v*u.T
assert sum(adj) == 718 and adj.rank() == 3
assert sum(abs(x) for x in edge) == 8
assert adj*edge == edge*adj == sp.zeros(dim)
assert edge*u == 2*v and edge*v == 2*u
deg = list(adj*sp.ones(dim, 1))
assert deg == [24]*9 + [22]*11 + [20]*13
assert edge*sp.ones(dim, 1) == sp.zeros(dim, 1)
c_squared = sp.Rational(4, deg[0]*deg[9])
assert c_squared == sp.Rational(1, 132)
t = sp.Rational(1, 4)
P = sp.diag(*(1/d for d in deg))*(adj+t*edge)
assert P*u == 2*t*v/22 and P*v == 2*t*u/24
assert P*P*u == c_squared*t*t*u
quotient = sp.Matrix([[0,11,13],[9,0,13],[9,11,0]])
quotient = sp.diag(sp.Rational(1,24), sp.Rational(1,22), sp.Rational(1,20))*quotient

# Both series, reconstructed from 32 moments after removing the Perron root.
x = sp.Symbol("x")
r = c_squared*t*t
kappa = sp.Rational(39, 160)
power = sp.eye(3)
traces = []
for k in range(1, 65):
    power = power*quotient
    pair = 2*r**(k//2) if k % 2 == 0 else 0
    traces.append(sp.trace(power) + pair)
assert sp.trace(P**2) == traces[1]


def polynomial(moments):
    coeff = [sp.S.One]
    for k in range(1, len(moments)+1):
        coeff.append(-sum(coeff[k-j]*moments[j-1] for j in range(1, k+1))/k)
    return sp.Poly.from_list(coeff, x).as_expr()


heat_rest = polynomial([a-1 for a in traces[:32]])
return_rest = polynomial([a-1 for a in traces[1::2]])
assert sp.expand(heat_rest - x**28*(x*x+x+kappa)*(x*x-r)) == 0
assert sp.expand(return_rest - x**28*(x*x-(1-2*kappa)*x+kappa**2)*(x-r)**2) == 0
assert F(14, 10*99) > F(4, 2**20-1)

# Test alternation of two different projectors for a non-normal T.
n = 3
mix = sp.Matrix([[2, 2, 0], [1, 1, 2], [1, 1, 2]])/4
mix = (mix + sp.ones(n)/3)/2
assert mix*mix.T != mix.T*mix
source, target = sp.zeros(n*n, n), sp.zeros(n*n, n)
for i in range(n):
    for j in range(n):
        source[n*i+j,i] = target[n*i+j,j] = sp.sqrt(mix[i,j])
assert source.T*source == target.T*target == sp.eye(n)
assert source.T*target == mix
state = target
test = (source*source.T, target*target.T)
for step in range(1, 6):
    state = test[(step-1) % 2] * state
    assert (state.T*state).applyfunc(sp.simplify) == (mix.T*mix)**step

# Fixed Golden selector and a uniform bound on the trace reweighting.
leaves = [("", 0)]
while len(leaves) < dim:
    word, cost = min(leaves, key=lambda item: (item[1], item[0]))
    leaves.remove((word, cost))
    leaves.extend(((word + "0", cost+1), (word + "1", cost+2)))
assert Counter(cost for _, cost in leaves) == {6: 1, 7: 20, 8: 12}
assert max(len(word) for word, _ in leaves) == 7
assert all(not a.startswith(b) for a, _ in leaves for b, _ in leaves if a != b)
p = (sp.sqrt(5)-1)/2
assert sp.simplify(sum(p**cost for _, cost in leaves)-1) == 0
assert F(618, 1000)**8 * 33 > F(2, 3)
assert F(618, 1000)**7 * 33 > 1

# Closed ordered histories on three actual vertices with genuinely moving
# preparation, Perron factor and row kernel. K need not be reversible.
y = sp.Symbol("y")
pressure = 2 + y
alpha = (0, 9, 0)
triangle = (0, 9, 20, 0)
twice = alpha + alpha[1:]


def transitions(path):
    return list(zip(path, path[1:]))


def prob(i, j):
    assert adj[i, j] == 1
    return 1/deg[i] + (int(j == 9)-int(j == 10))*int(i == 0)*y


def raw(i, j):
    return pressure*prob(i, j)*(1+(i+1)*y)/(1+(j+1)*y)


def product(path, factor):
    return sp.factor(sp.prod(factor(i, j) for i, j in transitions(path)))


def ld(expr):
    return sp.factor(sp.diff(expr, y)/expr)


def measured(path, memory, cost):
    return (2-y)*cost*product(path, raw)**2*memory


memory, meter = 2+y*y, 3-y
reference = measured(alpha, memory, meter**2)
for path, mem in ((twice, memory), (triangle, 1+2*y)):
    n = len(path)-1
    assert sp.cancel(product(path, raw) / (pressure**n*product(path, prob))) == 1
    ratio = measured(path, mem, meter**n)/reference
    corrected = ld(ratio) - 2*ld(product(path, prob)/product(alpha, prob))
    corrected -= ld(mem*meter**n/(memory*meter**2))
    assert sp.factor(corrected-2*(n-2)*ld(pressure)) == 0

# Regular Q8 action, including genuinely noncommuting oriented edge maps.
# Elements use signed basis 1,i,j,k encoded by integers ±1,...,±4.
elts = (1,-1,2,-2,3,-3,4,-4)
table = ((1,2,3,4), (2,-1,4,-3), (3,-4,-1,2), (4,3,-2,-1))


def multiply(a, b):
    return (1 if a*b > 0 else -1)*table[abs(a)-1][abs(b)-1]


def inverse(a):
    return next(b for b in elts if multiply(a, b) == 1)


def hclass(path, links):
    value = 1
    for i, j in transitions(path):
        value = multiply(links[i,j],value)
    return value


assert multiply(2, 3) != multiply(3, 2)
for last in elts:
    links = {(0,9): 2, (9,20): 3, (20,0): last}
    links.update({(j,i): inverse(z) for (i,j), z in list(links.items())})
    tclass = hclass(triangle, links)
    assert hclass(alpha, links) == hclass(twice, links) == 1
    assert hclass(triangle + triangle[-2::-1], links) == 1
    assert hclass(triangle + triangle[1:]*3, links) == 1
    assert multiply(tclass, tclass) in (1,-1)
    if last == 1:
        assert multiply(tclass, tclass) == -1
        # H = I + |1><1| distinguishes |1> from L_{-1}|1>.
        effect = lambda g: 1+int(g == 1)
        assert effect(1) == 2*effect(multiply(tclass,tclass))
print("PASS: 718 directed edges, two normalized scene prices, 32 moments, "
      "non-normal alternating projectors, 33-address selector and calibrated Q8 loops.")
