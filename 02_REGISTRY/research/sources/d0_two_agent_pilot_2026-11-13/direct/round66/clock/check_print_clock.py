"""Exact late return and a finite RC1/Hodge trace check on the native scene."""
from itertools import product
import math
import numpy as np
import scipy.linalg as la
import sympy as sp


field = sp.QQ.algebraic_field(sp.sqrt((sp.sqrt(5)-1)/2))
a = field.unit
one = field.one
p = a*a
zero = field.zero
assert p+p**2 == one
v = (a,p)
def g(v_, inverse=False):
    x,y = v_
    return (a*x+p*y, -p*x+a*y) if inverse else (a*x-p*y, p*x+a*y)


for bit, valid in enumerate((((0,0),(1,0)), ((1,0),(1,1)))):
    prepared = v if bit==0 else tuple(reversed(v))
    left = g(prepared)
    right = g(prepared, inverse=True)
    assert tuple((i,j) for i,j in product(range(2), repeat=2) if left[i]*right[j] != zero)==valid
    for printed in (False,True):
        alpha = []
        for outcome in valid:
            emitted = tuple(t for u in outcome for t in ((1,0) if u else (0,)))
            observed_addresses = outcome + (emitted if printed else ())
            alpha.append(p**sum(1+t for t in observed_addresses))
        base = ((p**4+p**7, p**7+p**10) if printed else (p,p**2))[bit]
        assert sum(alpha, zero) == base
        for m in range(1,6):
            ps = [math.prod(labels, start=one) for labels in product(alpha, repeat=m)]
            assert len(ps) == 2**m and sum(ps, zero)==base**m
assert field.to_sympy(p**4+p**7) < sp.Rational(1,4)
# Rational enclosure; do not power a nearly cancelling algebraic conjugate.
p_upper = sp.Rational(618034,1000000)
assert p_upper+p_upper**2 > 1
assert 4*(p_upper**4+p_upper**7)**24/(2**20-1) < sp.Rational(1,2**77)
assert sp.Rational(6,359*16**24) < sp.Rational(1,2**101)
# Determinant lemma with a noncommuting pair of old positive root matrices.
z = sp.Rational(1,2**20)
A = sp.Matrix([[sp.Rational(1,3),0],[0,0]])
B = sp.Matrix([[1,1],[1,1]])/6
assert A*B != B*A
u,w = sp.symbols("u w", positive=True)
C = sp.Matrix([[u/sp.sqrt(3),w/sp.sqrt(6),0],[0,w/sp.sqrt(6),0]])
assert C*C.T==u*u*A+w*w*B
assert sp.simplify((sp.eye(3)-z*(sp.eye(3)-C.T*C)).det() -
  (1-z)*((1-z)*sp.eye(2)+z*(u*u*A+w*w*B)).det())==0


# Numerical RC1 fixture with a unitary square stage, a genuine measured fork,
# a Golden birth in each child, their full complements and a real final CX.
# This fixture checks the heat bound, not the physical tariff of any gate.
p_num = (np.sqrt(5)-1)/2
v_num = np.array([[np.sqrt(p_num)],[p_num]])
P0 = np.diag([1.,0.])
P1 = np.eye(2)-P0
read = np.vstack((P0,P1))
birth = np.kron(np.eye(4),v_num)
refs = [np.eye(2),read,birth]
dims = [2,2,4,8]
offs = np.cumsum([0]+dims)
tailgate = la.block_diag(*(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]) for _ in range(2)))

def mm(left,right):
    return np.einsum("ij,jk->ik", left, right, optimize=False)

def clock(slot):
    dims_final=dims[-1]
    closure=np.zeros((offs[-1],dims_final))
    shift=np.zeros((offs[-1],offs[-1]))
    for j,dim in enumerate(dims):
        defect=np.eye(dim) if j==0 else np.eye(dim)-mm(refs[j-1],refs[j-1].T)
        passive=np.eye(dim)
        for emb in refs[j:]:
            passive=mm(emb,passive)
        closure[offs[j]:offs[j+1],:] = mm(defect,passive.T)
    for j,stage in enumerate((slot,read,birth)):
        shift[offs[j+1]:offs[j+2],offs[j]:offs[j+1]]=stage
    shift[:,offs[-2]:] += mm(closure,tailgate)
    assert np.isfinite(shift).all() and np.allclose(mm(shift.T,shift),np.eye(offs[-1]))
    return shift


G = np.array([[np.sqrt(p_num),-p_num],[p_num,np.sqrt(p_num)]])
minus,plus = clock(np.eye(2)),clock(G)
Bpre = np.linalg.norm(G-np.eye(2),ord="nuc")
assert np.isclose(np.linalg.norm(plus-minus,ord="nuc"),Bpre)
labels=np.repeat([0,1,2],[9,11,13])
adj = (labels[:,None]!=labels[None,:]).astype(float)
assert adj.sum()==2*359
R=np.diag((adj.sum(axis=1)+2.0)**(-.5))
Bscene=mm(mm(R,adj),R)
Cscene=mm(R,R)
beta=2*p_num**2
def heat(t):
    trace=0.0
    for eig in np.linalg.eigvals(t):
        delta=np.eye(33)-Bscene-2*eig.real*Cscene
        trace+=sum(np.exp(-beta*np.linalg.eigvalsh(delta)))
    return np.log(359*len(t)+2*trace)/beta
dh=abs(heat(plus)-heat(minus))
assert 0 < dh <= 6*Bpre/(359*offs[-1])
print(f"PASS: canonical four outcomes; printed and unprinted RC3 through m=5; noncommuting root determinant; complete 425D heat on D={offs[-1]} routed-clock fixture, |delta H|={dh:.3g}")
