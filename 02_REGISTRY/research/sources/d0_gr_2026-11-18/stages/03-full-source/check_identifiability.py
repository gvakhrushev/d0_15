"""Symbolic all-column trace and literal Kraft/Born shortfall for the cited A57 subword."""
import sympy as sp
p,a=sp.symbols('p a',real=True)
G=sp.Matrix([[a,-p],[p,a]])
C01=sp.eye(4)[[0,1,3,2],:]
C10=sp.eye(4)[[0,3,2,1],:]
U=C10*C01*sp.kronecker_product(sp.eye(2),G)
assert U.trace()==p+a
ideal=sp.groebner([a**2-p,p**2+p-1],a,p)
def golden(x):
    return sp.expand(ideal.reduce(sp.expand(x))[1])
assert all(golden(x)==0 for x in U.T*U-sp.eye(4))
assert golden(U.trace()*U.T.trace())==1+2*a*p
assert golden(U.trace()*U.T.trace()-(U.subs(a,-a)).trace()**2)==4*a*p
assert golden(p+p**2)==1
assert golden(p*p**2+p**4-p**2)==0
assert golden(1-p*p**2-p**4-p)==0
print('PASS: actual four-column subword, projective Galois obstruction and p Born deficit.')

# Exhaust the translation intertwining of the three actual gate matrices in
# F4 with a literal native bit-ordering. Labels use the low two bits as Spin.
def ff_mul(x,y):
    t=(x if y&1 else 0)^((x<<1) if y&2 else 0)
    return t^7 if t&4 else t

assert ff_mul(2,2)==3 and ff_mul(3,3)==2
n=8
raw_g=[[3 if i==j else 2 if i==j^4 else 0 for j in range(n)] for i in range(n)]
def perm(fn):
    return [[int(i==fn(j)) for j in range(n)] for i in range(n)]
lin=lambda j: j^(1 if j&4 else 0)
raw_c=perm(lin)
li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
source=sp.diag(sp.eye(4),li)
raw_source=[[int(source[i,j])%2 for j in range(n)] for i in range(n)]
assert raw_source==raw_c
for gate,shift in [(raw_g,lambda h:h),(raw_c,lin),(raw_source,lin)]:
    for h in range(n):
        assert all(gate[i][j^h]==gate[i^shift(h)][j] for i in range(n) for j in range(n))
from itertools import product
fl=lambda A,s,B,f: f^((1-A)*(1-s)*B)
assert {fl(A,s,B^1,f)^fl(A,s,B,f) for A,s,B,f in product((0,1),repeat=4)}=={0,1}
print('PASS: all F4 translation identities and non-affine third-coin flag.')
