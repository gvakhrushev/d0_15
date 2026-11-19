"""Finite exact native clock examples and the 33-scene low-band decoder (no project files needed)."""
import json
import math
from fractions import Fraction
import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

p=(sp.sqrt(5)-1)/2
a=sp.sqrt(p)
field=sp.QQ.algebraic_field(a)
def dm(M): return DomainMatrix.from_Matrix(M).convert_to(field).to_sparse()
def trace(M): return sum((M[i,i].element for i in range(M.shape[0])),field.zero)
def kron(*M): return sp.kronecker_product(*M)
v=sp.Matrix([a,p]); w=sp.Matrix([-p,a]); G=sp.Matrix.hstack(v,w)
Li=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
S=sp.diag(sp.eye(4),Li)
CX=sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
# Real wires bus and data, quaternion spin always a returning spectator carrier.
spin=sp.eye(4)
src=kron(sp.eye(2),S)   # data (high wire), bus (low wire), Spin4
mix=kron(sp.eye(2),G,spin)
cx=kron(CX,spin)        # control=data, target=bus
# Two births (bus first, then data); dictionaries indexed as (data,bus).
born=kron(G,G,spin)
j=kron(v,v,spin)
ages=[7]*4+[6]*4+[5]*8
N,L=min(ages)+2,min(ages)
r=4; D=sum(ages)
assert N==7 and L==5 and L>2*(N-L) and D==92
seats={};i=0
for s,b in enumerate(ages):
    for t in range(b):
        seats[s,t]=i;i+=1
def temporal(W):
    T=sp.zeros(D)
    for s,b in enumerate(ages):
        for t in range(b-1): T[seats[s,t+1],seats[s,t]]=1
        for dest in range(len(ages)):
            T[seats[dest,0],seats[s,b-1]]=W[dest,s]
    return dm(T)

groups=np.array([9.,11.,13.]); deg=33-groups
cs=1/(deg+2); equiv=np.sqrt(np.outer(groups*cs,groups*cs));np.fill_diagonal(equiv,0)
adj_eq=np.sqrt(np.outer(groups,groups));np.fill_diagonal(adj_eq,0)
assert int(sum(groups))==33 and int(sum(groups*deg))==718
assert np.linalg.eigvalsh(equiv)[-2]<0
def scene_spectrum(x):
    aeq=np.diag(1-x*cs)-equiv
    return np.r_[np.linalg.eigvalsh(aeq),np.repeat(1-x*cs,(groups-1).astype(int))]
def invert_low(lam):
    return np.linalg.eigvalsh(np.diag((1-lam)*(deg+2))-adj_eq)[0]
pp=(math.sqrt(5)-1)/2; beta=2*pp**2;z=2**(-20)
rows=[]
for name,actual,expected in [('fixed_port_SourceI',src,p**2+p**4),('G_bus',mix,p)]:
    # Both tails have four paid CX (two literal CX;CX pairs), then a real final gate.
    W=dm(actual)*dm(cx)**4
    assert W.transpose()*W==dm(sp.eye(16))
    C=dm(j).transpose()*W*dm(j)
    assert C.transpose()*C==dm(expected*spin)
    bornW=dm(born).transpose()*W*dm(born)
    T=temporal(bornW.to_Matrix())
    assert T.transpose()*T==dm(sp.eye(D))
    t1=trace(T**N);t2=trace(T**(2*N))
    assert t1==N*trace(C) and t2==N*trace(C**2)
    x0=t1/(field(N*r))
    s0=2*x0**2-t2/field(N*r)
    assert s0==field.from_sympy(expected.expand())
    realT=np.array(T.to_Matrix().evalf(18).tolist(),dtype=float)
    xs=np.linalg.eigvalsh(realT+realT.T)
    eig=np.sort(np.concatenate([scene_spectrum(x) for x in xs]))
    # Synthetic whole Hodge eigenvalue list, then only the actual low band is used.
    whole=np.sort(np.r_[np.zeros(359*D),eig,eig]); low=whole[359*D:359*D+2*D:2]
    assert eig[D-1] <= 33/196+1e-12 and eig[D]>=10/11-1e-12
    recovered=np.clip([invert_low(value) for value in low],-2,2)
    assert np.max(np.abs(np.sort(recovered)-np.sort(xs)))<1e-11
    cos=np.clip(np.array(recovered)/2,-1,1)
    tN=np.cos(N*np.arccos(cos)).sum()
    tNN=np.cos(2*N*np.arccos(cos)).sum()
    s=2*(tN/(N*r))**2-tNN/(N*r)
    assert abs(s-float(expected))<1e-10
    H=np.log(np.exp(-beta*whole).sum())/beta
    Zall=359*D+2*sum(np.exp(-beta*scene_spectrum(x)).sum() for x in recovered)
    Hlow=math.log(Zall)/beta
    assert abs(Hlow-H)<5e-13
    J=-r*math.log1p(-z*(1-s))
    rows.append(dict(name=name,exact_s=str(sp.simplify(expected)),s_from_low_band=s,
                     low_min=float(low.min()),low_max=float(low.max()),
                     next_mode=float(eig[D]),all_modes=len(whole),
                     H_from_all=H,H_rebuilt_from_low=Hlow,J_from_low=J))
print(json.dumps(dict(status="PASS",earliest_age=N,youngest_age=L,clock_dimension=D,
    pure_rational_gap=[str(Fraction(33,196)),str(Fraction(10,11))],
    cases=rows, scope="Exact clock traces and gaps; decimals in the low-band reconstruction are a floating diagnostic. No primitive-rate or readout admission is claimed."),indent=2))
