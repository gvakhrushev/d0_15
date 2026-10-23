#!/usr/bin/env python3
"""Original literal A4D S_star face = − CAR16 Julia marked-event mixed log jet.
36 exact coframe-bivector × Lorentz-generator entries; source is research only.
"""
import sympy as s
from itertools import combinations,product
eta=s.diag(1,-1,-1,-1)
def E(i,j):
    A=s.zeros(4);A[i,j]=1;return A
lor=[E(0,i)+E(i,0) for i in (1,2,3)]+[
    E(1,2)-E(2,1),E(1,3)-E(3,1),E(2,3)-E(3,2)]
P=list(combinations(range(4),2));Ix={pair:i for i,pair in enumerate(P)}
G2=s.diag(*(eta[i,i]*eta[j,j] for i,j in P))
STAR=s.zeros(6)
STAR_MAP={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
          (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for pair,(q,sign) in STAR_MAP.items():STAR[Ix[q],Ix[pair]]=sign
assert STAR*STAR==-s.eye(6)
def hodge(B):
    low=eta*B*eta
    return s.Matrix(4,4,lambda a,b:sum(s.LeviCivita(a,b,i,j)*low[i,j]
             for i,j in product(range(4),repeat=2))/2)
def creator(i):
    M=s.zeros(16)
    for bits in range(16):
        if ((bits>>i)&1)==0:
            M[bits+(1<<i),bits]=(-1)**((bits&((1<<i)-1)).bit_count())
    return M
c=[creator(i) for i in range(4)];a=[v.T for v in c]
def gamma(X):
    return sum((X[i,j]*c[i]*a[j] for i,j in product(range(4),repeat=2)),s.zeros(16))
for pair in P:
    v=s.zeros(6,1);v[Ix[pair]]=1
    B=E(*pair)-E(pair[1],pair[0])
    X=hodge(B)*eta
    assert X.T*eta+eta*X==s.zeros(4)
    for F in lor:
        bF=s.Matrix([(F*eta)[i,j] for i,j in P])
        old=(v.T*G2*STAR*bF)[0]
        CAR=-s.trace(gamma(X)*gamma(F))/8
        marked=-s.trace(X*F)/2 # exact −D_s D_t log q_mark at identity
        assert old==CAR==marked
print('PASS 36 literal native S_star G2/STAR slots = −1/8 fullCAR16 trace = −log positive marked-event mixed jet')
print('GR_closed=false: constructed CAR16/Julia measurement NOT physically compulsory full128 Book programme')
