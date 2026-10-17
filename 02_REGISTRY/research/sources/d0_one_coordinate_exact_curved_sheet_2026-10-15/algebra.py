"""Literal six-face naked-star symbol, independently reconstructed."""
import sympy as s
from itertools import combinations
PAIR=list(combinations(range(4),2));eta=s.diag(1,-1,-1,-1)
GEN=[]
for a,b in PAIR:
 x=s.zeros(4);x[a,b]=1;x[b,a]=-eta[a,a]*eta[b,b];GEN.append(x)
G2=s.diag(*[eta[a,a]*eta[b,b] for a,b in PAIR]); STAR=s.zeros(6)
for a,(b,sg) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),(1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():STAR[PAIR.index(b),PAIR.index(a)]=sg

def wedge(u,v):return s.Matrix([u[a]*v[b]-u[b]*v[a] for a,b in PAIR])
def symbol(E,z):
 out=s.zeros(24)
 for r,ss in PAIR:
  u,v=[i for i in range(4) if i not in (r,ss)]; seq=[r,ss,u,v];sg=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2))
  pairing=sg*wedge(E[:,u],E[:,v]).T*G2*STAR;br=s.zeros(6)
  for i,X in enumerate(GEN):
   for j,Y in enumerate(GEN):
    Z=(X*Y-Y*X)*eta;br[i,j]=(pairing*s.Matrix([Z[a,b] for a,b in PAIR]))[0]
  roles=[r,ss,r,ss];direct=[1,z[r],-z[ss],-1];inverse=[1,1/z[r],-1/z[ss],-1];role=s.zeros(4)
  for i,j in combinations(range(4),2):
   role[roles[i],roles[j]]+=direct[i]*inverse[j]/2
   role[roles[j],roles[i]]-=inverse[i]*direct[j]/2
  out+=s.kronecker_product(role,br)
 return out.applyfunc(s.expand)

from functools import lru_cache
@lru_cache(maxsize=1)
def inverse_coefficients():
    """Derived, not prescribed: the complete 24-by-24 inverse numerator."""
    z=s.symbols('z',nonzero=True)
    C=symbol(s.eye(4),[s.Integer(1),z,s.Integer(1),s.Integer(1)]).T
    Q=14+z*z+z**-2
    N=(Q*C.inv()).applyfunc(s.cancel).applyfunc(s.expand)
    ans={}
    for i in range(24):
        for j in range(24):
            for term in s.Add.make_args(N[i,j]):
                if term==0:continue
                power=int(term.as_powers_dict().get(z,0))
                value=s.cancel(term/z**power)
                if not value.is_Rational:raise AssertionError('not a Laurent numerator')
                ans.setdefault(power,s.zeros(24))[i,j]+=value
    return ans
