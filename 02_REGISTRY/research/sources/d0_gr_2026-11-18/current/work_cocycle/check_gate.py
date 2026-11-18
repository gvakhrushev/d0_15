"""Real fixed-port SOURCE on two live WORK wires and Spin4. No project files needed."""
import json
from collections import deque
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp

def need(x,description):
    if not x: raise ArithmeticError(description)
def mul(*matrices):
    out=matrices[0]
    for right in matrices[1:]:
        out=np.einsum("ij,jk->ik",out,right,optimize=False)
    return out
def power(mat,n):
    out=np.eye(len(mat),dtype=mat.dtype)
    for _ in range(n): out=mul(out,mat)
    return out
def compose(f,g):
    # Read f, then g.
    perm,k=f; sig,h=g
    return tuple(sig[x] for x in perm),tuple((k[x]+h[perm[x]])%4 for x in range(4))
def cx(control,target):
    return tuple(x^(((x>>control)&1)<<target) for x in range(4)),(0,0,0,0)
ident=((0,1,2,3),(0,0,0,0)); source=(ident[0],(0,1,0,1))
gens=(cx(1,0),cx(0,1),source)
group={ident:0}; q=deque([ident])
while q:
    f=q.popleft()
    for g in gens:
        nxt=compose(f,g)
        if nxt not in group:
            group[nxt]=1+group[f];q.append(nxt)
need(len(group)==192,"true finite subgroup order")
def parity(f):
    perm,k=f
    return (sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4)) + sum(k)//2)%2
need(all(k[0]==0 and sum(k)%2==0 for _,k in group),"controlled phase subgroup")
need(all(parity(f)==n%2 for f,n in group.items()),"length parity of each positive word")
J=np.array([[0,-1],[1,0]],dtype=int)
Li=np.kron(np.eye(2,dtype=int),J)
def actual(f):
    out=np.zeros((16,16),dtype=int)
    for index,(dest,phase) in enumerate(zip(*f)):
        out[4*dest:4*dest+4,4*index:4*index+4]=np.linalg.matrix_power(Li,phase)
    return out
mats=[actual(f) for f in group]
symchar=sum((np.trace(U)**2+np.trace(mul(U,U)))//2 for U in mats)
need(symchar==14*192,"14-dimensional fixed real symmetric observable space")
C10,C01,S=map(actual,gens)
swap=mul(C10,C01,C10)
S_e=mul(swap,S,swap)
CZ=mul(C10,power(S,3),C10,S,S_e)
need(np.array_equal(CZ,np.kron(np.diag([1,1,1,-1]),np.eye(4))),"literal two-bit CZ with restored Spin")
p=(5**.5-1)/2;a=p**.5;v=np.array([a,p])
G=np.array([[a,-p],[p,a]])
Ug=np.kron(np.kron(np.eye(2),G),np.eye(4)); Z=mul(S,S)
Kg=np.kron(np.eye(2),np.kron(J,Li))
need(np.array_equal(Kg.T,Kg) and np.array_equal(mul(Kg,Kg),np.eye(16)),"admissible real bounded Hermitian drift")
need(np.max(abs(mul(Ug.T,Kg,Ug)-Kg))<1e-14 and np.array_equal(mul(Z.T,Kg,Z),-Kg),"true dihedral covariance")
jv=np.kron(np.kron(np.eye(2),v[:,None]),np.eye(4))
pref=mul(S,CZ)
effect=mul(jv.T,pref.T,Kg,pref,jv)
need(np.max(abs(effect-2*a*p*np.kron(np.diag([1,-1]),np.eye(4))))<1e-14,"all-column event/Spin drift effect")
n=33
U1=mul(Z,power(Ug,n),Z,power(Ug,n))
U2=mul(Z,Z,power(Ug,2*n))
need(np.max(abs(U1-np.eye(16)))<3e-14,"literal echo endpoint")
def price(word):
    V=np.eye(16);W=np.zeros((16,16))
    for g in word:
        K,U=(2*np.eye(16)+Kg,Ug) if g=="G" else (np.eye(16),S)
        W+=mul(V.T,K,V);V=mul(U,V)
    return W
echo="G"*n+"SS"+"G"*n+"SS"
plain="G"*(2*n)+"SSSS"
need(sorted(echo)==sorted(plain),"equal paid native inventory")
diff=mul(jv.T,pref.T,price(plain)-price(echo),pref,jv)
need(np.max(abs(diff-2*n*effect))<1e-10,"cumulative observable on all physical event/Spin columns")
# One common exact generator potential can be recovered after finite twirling.
trial=np.arange(256).reshape(16,16).astype(int);A=trial+trial.T
avg=sum(mul(U.T,A,U)-A for U in mats)
AF=-avg/len(group)
for U in map(actual,gens):
    need(np.max(abs((mul(U.T,AF,U)-AF)-(mul(U.T,A,U)-A)))<1e-11,"finite group potential calibration")
# Certified interval for the actual numerical word; no eigensolver needed.
iv=mp.iv;iv.dps=60
pi=(iv.sqrt(5)-1)/2;aa=iv.sqrt(pi)
g=iv.matrix([[aa,-pi],[pi,aa]])
high=g**(2*n)
eta=iv.sqrt(2*(1-high[0,0]))
need(eta<iv.mpf(11)/1000,"near original endpoint")
size=4*n*pi*aa
need(size>64,"true test cost contrast at Q=0")
L=70; x=Fr(2,55); z=Fr(1,2**20)
import math
AL=Fr(176,359)*x**L/(math.factorial(L)*(1-x*x)*(1-x/L))
price_bound=Fr(11,1000)*(AL+8*z/(1-z))
need(price_bound<Fr(1,10**7),"full original uniform H+J value bound")
pop=np.kron(np.eye(2),np.kron(np.diag([0.,1.]),np.eye(4)))
local_g=np.eye(16)+mul(Ug.T,pop,Ug)-pop
local_c=np.eye(16)
def marked_local(word, cx_tariff):
    V=np.eye(16);W=np.zeros((16,16))
    for x in word:
        gate,cost=(Ug,local_g) if x=="G" else (C10,cx_tariff)
        W+=mul(V.T,cost,V);V=mul(gate,V)
    return V,W
exp_full=np.kron(np.diag([0.,1.]),np.kron(np.diag([1.,-1.]),np.eye(4)))
for blocks in (1,3):
    vl,wl=marked_local("GCGC"*blocks,local_c)
    vr,wr=marked_local("CGCG"*blocks,local_c)
    need(np.max(abs(vl-vr))<1e-14,"literal equal native endpoints")
    need(np.max(abs(wl-wr-4*p**2*blocks*exp_full))<5e-14,"strictly local all-column price contrast")
    born_effect=mul(jv.T,wl-wr,jv)
    need(np.max(abs(born_effect-4*p**5*blocks*np.kron(np.diag([0,1]),np.eye(4))))<1e-13,
         "actual scalar field lift on arbitrary opaque Spin")
    corrected=2*np.eye(16)+mul(C10.T,pop,C10)-pop
    _,al=marked_local("GCGC"*blocks,corrected)
    _,ar=marked_local("CGCG"*blocks,corrected)
    need(np.max(abs(al-ar))<5e-14,"the paid CX exchange restores exact endpoint work")
print(json.dumps(dict(status="PASS",finite_subgroup_order=192,finite_subgroup_diameter=max(group.values()),
  real_symmetric_fixed_dimension=symchar.item()//192, n=n,G_per_body=2*n,SourceI_per_body=4,
  field_event_work_operator="4*n*p*sqrt(p)*(I-2*event)",absolute_work_at_Q0=str(size),
  centered_drift_gain_per_DQ=-8*n*p*a,endpoint_norm=str(eta), master_value_difference_bound="< 1/10000000",
  four_gate_strict_local=dict(words=["GCGC","CGCG"],equal_H_and_J_exactly=True,
       cost_gap_per_event_Q="4*p^5",cost_gap_per_DQ=float(4*p**5),
       compensated_controlled_x="CX* P1 CX - P1 = event times Z"),
  full_body_readout_required=True,physical_complete_binding_proved=False),indent=2))
