"""Exact checks for reconstruction of a two-clock law and its finite errors."""
from fractions import Fraction as F
from itertools import product
import sympy as s

p=(s.sqrt(5)-1)/2
a=s.simplify(p*p)
simplify=s.simplify
assert simplify(a*a-3*a+1)==0
assert simplify((1-a)**2-p**2)==0
assert simplify(1+a**3-2*a-2*a*a)==0
for m in range(12):
    target_tail=a**(m+1)*(m+2-(m+1)*a)
    assert simplify(sum((k+1)*p*p*a**k for k in range(m+1))+target_tail-1)==0

w=s.symbols('w0:4')
r0=w[0]+w[2]-3*w[1]
r1=w[1]+w[3]-3*w[2]
exception=w[0]+w[3]-2*w[1]-2*w[2]
assert s.expand(exception-r1-r0)==0

# Exact finite Dirichlet inverse, both endpoint solutions and all forcing signs.
for K in range(2,26):
    U=[0,1]
    for k in range(1,K): U.append(3*U[k]-U[k-1])
    assert all(U[k]==s.fibonacci(2*k) for k in range(K+1))
    for i,j in product(range(1,K),repeat=2):
        def green(i,j):
            return F(U[min(i,j)]*U[K-max(i,j)],U[K])
        gij=green(i,j)
        assert gij>=0
        assert 3*gij-green(i-1,j)-green(i+1,j)==int(i==j)
    for i in range(1,K):
        sharp_forcing=1-F(U[K-i]+U[i],U[K])
        assert 0<=sharp_forcing<=1
        assert sum(green(i,j) for j in range(1,K))==sharp_forcing
        assert 3*U[i]-U[i-1]-U[i+1]==0

# Check the normalization/unknown scale lemma for an interior of two cells,
# and two independent nonzero tail cells; no geometric assumption here.
def laws(total):
    for i,j,k in product(range(total+1),repeat=3):
        if i+j+k<=total:
            yield [F(x,total) for x in (i,j,k,total-i-j-k)]
ncomp=0
for u,v in product(laws(4),repeat=2):
    for c in (F(0),F(1,3),F(1),F(3,2),F(3)):
        discrepancy=sum(abs(u[i]-c*v[i]) for i in (0,1))
        tv=sum(abs(x-y) for x,y in zip(u,v))/2
        assert tv<=discrepancy+max(sum(u[2:]),sum(v[2:]))
        ncomp+=1
y=s.symbols('y',real=True)
K=s.exp(-y)
assert simplify(s.diff(-s.log(K),y)-1)==0
print("PASS: quadratic root, exceptional carry, mass and tails; Dirichlet Green matrices through K=25; TV comparisons:",ncomp)
