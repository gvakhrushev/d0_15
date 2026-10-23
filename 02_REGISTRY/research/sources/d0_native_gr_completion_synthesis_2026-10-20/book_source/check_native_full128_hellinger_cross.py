#!/usr/bin/env python3
"""NUMERICAL ONLY: full original CAR16/Jones 128^2 first-jet Hellinger 10x24.

The exact original native Kraus construction, Julia square roots, 64 Walsh
coefficient rows and Golden two-port labels are used. No new detector or
selected Book03 information/action is inferred. Rank/SVD output is NOT
a characteristic-zero exact certificate; the dark (50,0) support birth
HAS a separate exact SymPy checker.
"""
import numpy as np

p=(np.sqrt(5)-1)/2
a=np.sqrt(p)
nu=.6
b=.8
order=(0,2,3,1)
zlist=(1j,1j,-1,-1j)
Id=np.eye(16,dtype=complex)
zero=np.zeros((16,16),dtype=complex)
C=[]
for role in range(4):
    c=zero.copy()
    prior=order[:order.index(role)]
    for bits in range(16):
        if not bits&(1<<role):
            c[bits | (1<<role),bits]=(-1)**sum(
                bool(bits&(1<<j)) for j in prior)
    C.append(c)
left=[c@c.conj().T for c in C]
right=[c.conj().T@c for c in C]
had=np.array([[(-1)**((lab&j).bit_count()) for j in range(32)]
              for lab in range(32)])

def base_Q():
    words=[[],[]]
    for role in range(4):
        z=zlist[role]
        v=nu*C[role]
        P=z*v
        Pd=P.conj().T
        L=Id+(b-1)*left[role]
        R=Id+(b-1)*right[role]
        rows=((P,L),(Pd,R),(-v,-L),(-v.conj().T,-R))
        for x,y in rows:
            for _ in range(2):
                words[0].append(x)
                words[1].append(y)
    Q=np.empty((64,16,16),dtype=complex)
    for comp in (0,1):
        Q[comp::2]=np.einsum("ab,bjk->ajk",had,np.array(words[comp]))/32
    return Q

Q=base_Q()
A=Q[0]
K=np.empty((128,16,16),dtype=complex)
for j in range(64):
    value=Q[j].conj().T@A
    K[2*j]=-2*p*p*value
    K[2*j+1]=-2*a*p*value
K[0]+=Id
completeness=np.einsum("aij,aik->jk",K.conj(),K)
assert np.linalg.norm(completeness-Id)<1e-11

psi=np.zeros(16,dtype=complex)
psi[0]=psi[14]=-a/np.sqrt(2)
psi[1]=psi[15]=p/np.sqrt(2)
assert abs(np.vdot(psi,psi)-1)<1e-13
first=K@psi
w=np.einsum("kij,aj->aki",K,first,optimize=True)
q0=np.sum(abs(w)**2,axis=-1)
bright=q0>1e-14
dark=~bright
assert bright.sum()==1764 and dark.sum()==14620
assert abs(q0.sum()-1)<1e-12
print("original complete original Jones q: 1764 bright / 14620 dark")

def root_derivative(projector,delta):
    blocks=(Id-projector,projector)
    eigen=(1,b)
    out=zero.copy()
    for j in range(2):
        for k in range(2):
            out-=blocks[j]@delta@blocks[k]/(eigen[j]+eigen[k])
    return out

def unit(j,k):
    mat=np.zeros((4,4),dtype=complex)
    mat[j,k]=1
    return mat

lor=[unit(0,j)+unit(j,0) for j in (1,2,3)]+[
    unit(2,3)-unit(3,2),unit(3,1)-unit(1,3),
    unit(1,2)-unit(2,1)]
gens=[sum((X[j,k]*C[j]@C[k].conj().T
           for j in range(4) for k in range(4)),zero.copy())
      for X in lor]

def dQarray(direction):
    words=[[],[]]
    for role in range(4):
        z=zlist[role]
        v=nu*C[role]
        P=z*v
        Pd=P.conj().T
        if direction[1]!=role:
            dP=dPd=dL=dR=dv=zero
        elif len(direction)==2:
            j=direction[0]
            dP=nu*z*C[j]
            dPd=dP.conj().T
            dv=nu*C[j]
            dL=root_derivative(left[role],nu*nu*(
                C[j]@C[role].conj().T+C[role]@C[j].conj().T))
            dR=root_derivative(right[role],nu*nu*(
                C[j].conj().T@C[role]+C[role].conj().T@C[j]))
        else:
            G=gens[direction[0]]
            dP=nu*z*C[role]@G
            dPd=dP.conj().T
            dv=zero
            dL=root_derivative(left[role],dP@Pd+P@dPd)
            dR=root_derivative(right[role],dPd@P+Pd@dP)
        fixed_dL=dL if len(direction)==2 else zero
        fixed_dR=dR if len(direction)==2 else zero
        rows=((dP,dL),(dPd,dR),(-dv,-fixed_dL),
              (-dv.conj().T,-fixed_dR))
        for x,y in rows:
            for _ in range(2):
                words[0].append(x)
                words[1].append(y)
    out=np.empty((64,16,16),dtype=complex)
    for comp in (0,1):
        out[comp::2]=np.einsum(
            "ab,bjk->ajk",had,np.array(words[comp]))/32
    return out

def dk(direction):
    dQ=dQarray(direction)
    dA=dQ[0]
    dK=np.empty((128,16,16),dtype=complex)
    for j in range(64):
        value=dQ[j].conj().T@A+Q[j].conj().T@dA
        dK[2*j]=-2*p*p*value
        dK[2*j+1]=-2*a*p*value
    return dK

def amplitude_first(dK):
    df=dK@psi
    dw=(np.einsum("kij,aj->aki",dK,first,optimize=True)
       +np.einsum("kij,aj->aki",K,df,optimize=True))
    dq=2*np.real(np.sum(np.conj(w)*dw,axis=-1))
    return dw,dq

metric=[]
eta=np.diag([1,-1,-1,-1])
for i in range(4):
    for j in range(i,4):
        symmetric=unit(i,j)+(unit(j,i) if i!=j else
                              np.zeros((4,4),dtype=complex))
        metric.append((eta@symmetric).reshape(16))

dm=[]
for h in metric:
    value=sum((h[4*r+j]*dk((j,r))
               for r in range(4) for j in range(4)
               if h[4*r+j]!=0),
              np.zeros((128,16,16),dtype=complex))
    dm.append(value)
dl=[dk((j,r,1)) for r in range(4) for j in range(6)]
DW=[];DQ=[]
for derivative in dm+dl:
    dw,dq=amplitude_first(derivative)
    DW.append(dw)
    DQ.append(dq)
DW=np.asarray(DW)
DQ=np.asarray(DQ)
assert np.max(abs(DQ.sum(axis=(1,2))))<1e-12
assert np.max(abs(DQ[:,dark]))<1e-12

# Exact mathematical anchored squared-Hellinger mixed Hessian:
# bright half Fisher + dark double REAL first-amplitude Gram.
B=DQ[:,bright]/np.sqrt(q0[bright])
brightH=(B@B.T)/2
darkW=DW[:,dark,:]
darkH=2*np.einsum(
    "ank,bnk->ab",np.conj(darkW),darkW,optimize=True).real
totalH=brightH+darkH
for name,mat in (("bright-only",brightH),("dark-only",darkH),
                 ("full-Hellinger",totalH)):
    cross=mat[:10,10:]
    singular=np.linalg.svd(cross,compute_uv=False)
    print(name,"10x24 numeric-rank",sum(singular>1e-11),
          "Frobenius",np.linalg.norm(cross),
          "singular",singular)
assert np.linalg.norm(darkH[:10,10:])>1e-6
print("NUMERICAL diagnostic PASS, not a native Book03 physical selector")
print("Do not use J^T diag(q^-1) J without dark-history compensation")
