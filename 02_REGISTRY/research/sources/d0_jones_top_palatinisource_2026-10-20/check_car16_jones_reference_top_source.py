#!/usr/bin/env python3
"""Original CAR16 + literal S_star + actual Jones reference psi±: exact 36-source weld.
RESEARCH, not compulsory physical full128/Kraus/Book admission.
"""
import sympy as s
from itertools import combinations
eta=s.diag(1,-1,-1,-1)
p=(s.sqrt(5)-1)/2
a=s.sqrt(p)
def E(i,j):
    out=s.zeros(4);out[i,j]=1;return out
pairs=list(combinations(range(4),2));Ix={x:i for i,x in enumerate(pairs)}
G2=s.diag(*[eta[i,i]*eta[j,j] for i,j in pairs])
STAR=s.zeros(6)
sm={(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
    (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for x,(y,v) in sm.items():STAR[Ix[y],Ix[x]]=v
cc=[]
for i in range(4):
    M=s.zeros(16)
    for bit in range(16):
        if not (bit>>i)&1:
            M[bit+(1<<i),bit]=(-1)**((bit&((1<<i)-1)).bit_count())
    cc.append(M)
def wedge(B):
    return sum((B[i,j]*cc[i]*cc[j] for i,j in pairs),s.zeros(16))
v0=s.eye(16)[:,0];omega=s.eye(16)[:,15]
u=-(v0+s.eye(16)[:,14])/s.sqrt(2)
v=(s.eye(16)[:,1]+omega)/s.sqrt(2)
psi_plus=a*u+p*v
psi_minus=a*u-p*v
rho_plus=psi_plus*psi_plus.T
rho_minus=psi_minus*psi_minus.T
basis=[E(0,i)+E(i,0) for i in (1,2,3)]+[
    E(1,2)-E(2,1),E(1,3)-E(3,1),E(2,3)-E(3,2)]
assert s.simplify((psi_plus.T*psi_plus)[0]-1)==0
assert s.simplify((psi_minus.T*psi_minus)[0]-1)==0
assert s.simplify((psi_plus.T*psi_minus)[0]-p**3)==0
assert s.simplify(p**6+4*a*a*p*p-1)==0
par=s.diag(*[1 if i.bit_count()%2==0 else 0 for i in range(16)])
deltarho=rho_plus-rho_minus
deltaeven=par*deltarho*par+(s.eye(16)-par)*deltarho*(s.eye(16)-par)
for ij in pairs:
    B=E(*ij)-E(ij[1],ij[0])
    face=s.eye(6)[:,Ix[ij]]
    for F in basis:
        f=s.Matrix([(F*eta)[i,j] for i,j in pairs])
        L=(face.T*G2*STAR*f)[0]
        N=wedge(B)*wedge(F*eta)
        assert N == -L*omega*v0.T
        assert s.simplify(s.trace(deltarho*(N+N.T))/(2*a*p)-L)==0
        assert s.simplify(s.trace(deltaeven*(N+N.T))/(2*a*p)-L)==0
        assert s.simplify((psi_plus.T*N*psi_plus)[0]-a*p*L/2)==0
        assert s.simplify((psi_minus.T*N*psi_minus)[0]+a*p*L/2)==0
# Native observer Gram covariance on actual full 16 exterior coordinates.
g=s.eye(4)
g[0,0]=g[1,1]=s.Rational(5,4);g[0,1]=g[1,0]=s.Rational(3,4)
assert g.T*eta*g==eta and g.det()==1
subs=[tuple(i for i in range(4) if (bits>>i)&1) for bits in range(16)]
R=s.Matrix(16,16,lambda i,j:s.det(g.extract(subs[i],subs[j]))
           if len(subs[i])==len(subs[j]) else 0)
H=R.inv().T*R.inv()
assert s.simplify(R.T*H*R-s.eye(16))==s.zeros(16)
for ij in pairs:
    B=E(*ij)-E(ij[1],ij[0])
    for F in basis:
        N=wedge(B)*wedge(F*eta)
        Np=wedge(g*B*g.T)*wedge(g*(F*eta)*g.T)
        assert s.simplify(Np-R*N*R.inv())==s.zeros(16)
        lhs=(psi_plus.T*R.T*H*Np*R*psi_plus)[0]
        rhs=(psi_plus.T*N*psi_plus)[0]
        assert s.simplify(lhs-rhs)==0
print("PASS native CAR16 Jones: all36 original literal Palatini = normalized Golden trace-distance contrast")
print("PASS parity dephasing and full CAR16 moving-observer proper-Lorentz covariance")
print("FIREWALL: actual full128 Jones code execution / Book action / GR unproved")
