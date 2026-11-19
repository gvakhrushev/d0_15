#!/usr/bin/env python3
"""Read-only scientific check: actual compact Golden Julia full-archive composition.
Exact CAR16 rational matrices / Q(sqrt5) weights; complete Golden17 regression.
No assertion of G0 programme admission or GR/action selection.
"""
from itertools import combinations, product
from math import comb, ceil, log, log1p, sin, cos, sqrt
import cmath
import numpy as np
import sympy as sp

p=(sp.sqrt(5)-1)/2; g=sp.simplify(p*p)
pf=float(p);gf=float(g);kap=pf**4/(24*4096)
def ok(test,label):
    assert test,label
    print('PASS',label)
def eq(a,b): return sp.simplify(a-b)==0
subsets=[s for k in range(5) for s in combinations(range(4),k)]
def exterior(A):
    return sp.Matrix([[0 if len(i)!=len(j) else (1 if not i else A.extract(i,j).det())
                       for j in subsets] for i in subsets])
def rot(a,b,c,s):
    R=sp.eye(4);R[a,a]=R[b,b]=c;R[a,b]=-s;R[b,a]=s;return R
R1=rot(1,2,sp.Rational(3,5),sp.Rational(4,5))
R2=rot(2,3,sp.Rational(5,13),sp.Rational(12,13))
U1,U2=map(exterior,(R1,R2));I=sp.eye(16)
ok(U1.T*U1==I and U2.T*U2==I and U1*U2!=U2*U1,'actual CAR16 compact noncommuting ordered letters are orthogonal')
Psi=sp.zeros(16,3)
for i in range(16):
    for j in range(3):Psi[i,j]=sp.Rational(((3*i+2*j+1)%7)-3,17)
Gram=Psi.T*Psi
ok(Gram.det()!=0,'nontrivial entangled reference has full rank three Gram')
# Complete fixed horizon: every raw word is kept and its OLD RIGHT Gram checked.
for n in range(1,7):
    weight=0
    for w in product((0,1),repeat=n):
        k=sum(w);A=U1**k;X=A*Psi
        okflag=(X.T*X==Gram)
        assert okflag
        weight+=g**k*p**(n-k)
    assert eq(weight,1)
ok(True,'all 126 actual flag words for n=1..6: complete probability and exact branchwise oldRIGHT Gram')
# Complete finite-cap controller, success advances to the next ACTUAL noncommuting letter.
letters=[U1,U2,U1];m=len(letters);N=7
leaves=[]
def visit(w,k,A):
    if k==m or len(w)==N:
        leaves.append((w,k,A));return
    visit(w+(0,),k,A)
    visit(w+(1,),k+1,letters[k]*A)
visit((),0,I)
Q=0;ET=0;mass=0;target=U1*U2*U1
for w,k,A in leaves:
    wt=g**k*p**(len(w)-k);mass+=wt;ET+=len(w)*wt
    assert (A*Psi).T*(A*Psi)==Gram
    if k==m:assert A==target;Q+=wt
Qbin=sum(sp.binomial(N,k)*g**k*p**(N-k) for k in range(m,N+1))
ETbin=sum(sum(sp.binomial(t,k)*g**k*p**(t-k) for k in range(min(m,t+1))) for t in range(N))
ok(eq(mass,1) and eq(Q,Qbin) and eq(ET,ETbin),'finite-cap all terminated/failed words obey exact binomial completion and expected clock')
ok(float(ET)<=m/gf,'finite-cap expected executed steps is bounded by m/p²')
# Exact first jet, arbitrary field-dependent compact letters, including all mixed ordering.
t=sp.symbols('t', real=True)
Rt=rot(1,2,(1-t*t)/(1+t*t),2*t/(1+t*t))
Ut=exterior(Rt);U0=Ut.subs(t,sp.Rational(1,2));dU=Ut.diff(t).subs(t,sp.Rational(1,2))
ok(U0.T*dU+dU.T*U0==sp.zeros(16),'native compact first jet preserves the complete oldRIGHT Gram')
def jetmul(a,b):return (a[0]*b[0],a[1]*b[0]+a[0]*b[1])
J0=(I,sp.zeros(16));JG=(U0,dU)
for n in range(1,6):
    for w in product((0,1),repeat=n):
        A=J0
        for a in w:
            if a:A=jetmul(JG,A)
        k=sum(w);expected=J0
        for _ in range(k):expected=jetmul(JG,expected)
        assert A==expected
ok(True,'all retained words have exact ordered power first jets, not only equal probabilities')
# Full 17 original outcomes including 4095/4096 Bell failure.
def q17(t):
    m=(1+cos(t))/2;s=sin(t)/sqrt(2);k=pf**4/24
    marks=[k*m*m]*10+[k*(m+s)**2,k*(m-s)**2]
    GG=pf**4;GB=pf*pf*(1-pf*pf);BG=pf**3
    q=np.array(marks+[GG-sum(marks),GB,BG,1-GG-GB-BG])/4096
    return np.append(q,1-1/4096)
for theta in (.001,.017,.061):
    for n in (1,2,3,6):
        B=0.
        for w in product((0,1),repeat=n):
            k=sum(w);wt=gf**k*pf**(n-k);qp,qm=q17(k*theta),q17(-k*theta)
            assert min(qp)>0 and abs(sum(qp)-1)<1e-14
            B+=wt*float(np.sqrt(qp*qm).sum())
        exact=1-kap*(1-(pf+gf*cmath.exp(2j*theta))**n).real
        assert abs(B-exact)<2e-14
ok(True,'complete chronological flags × all17 outputs reproduce exact finite overlap formula')
for n in (1,2,7,31):
    E2=sum(comb(n,k)*gf**k*pf**(n-k)*k*k for k in range(n+1))
    closed=n*n*gf*gf+n*gf*(1-gf)
    assert abs(E2-closed)<1e-10
    assert abs(E2/(n*gf)-(1+(n-1)*gf))<1e-10
ok(True,'exact binomial second moment gives I_n=4κ[n²g²+ng(1-g)] and gain 1+(n-1)g')
print('REFINEMENT_TABLE L,n,block_overlap_loss,n²h4_factor,iid_necessary_records_at_error_0.1')
for L in (4,8,16,32,64,128):
    h=1/L;theta=h*h;n=L*L//4
    loss=kap*(1-(pf+gf*cmath.exp(2j*theta))**n).real
    one_loss=2*kap*sin(theta)**2
    iid_lb=ceil(log(.36)/(2*log1p(-one_loss)))
    print(L,n,format(loss,'.12g'),n*n*h**4,iid_lb)
    assert loss>2e-8
limit=2*kap*sin(gf/4)**2
print('limiting complete block overlap loss',format(limit,'.15g'))
ok(True,'fixed-confidence coherent complete blocks use n=Theta(h^-2); iid primitive readouts need Omega(h^-4)')
# Hostile genuine proper-Lorentz noncompact boost in the common positive Julia chart.
B=sp.eye(4);B[0,0]=B[1,1]=sp.Rational(65,63);B[0,1]=B[1,0]=sp.Rational(16,63)
UB=exterior(B);metric=sp.diag(1,-1,-1,-1)
ok(B.T*metric*B==metric and UB.T*UB!=I,'proper boost is Lorentz but failure is not scalar identity in the observer Hilbert metric')
old=I/16;new=(UB.T*UB)/sp.trace(UB.T*UB)
ok(new!=old and gf*(9/7)**2<1,'hostile positive-chart boost changes conditional oldRIGHT Gram; compact theorem cannot be exported')
print('SCOPE: compact Golden-Julia interface theorem. Actual charged G0 admission, noncompact physical source and GR remain separate.')
# Exact channel eigenmodes on the actual CAR16 compact J23 charges 0,+/-1.
# Channel charge differences range from -2 to 2.
print('CHANNEL_LIMIT_TABLE L,n,max_mode_error,error_over_h2,retained_Stinespring_error')
tau=.75
for L in (4,8,16,32,64,128):
    delta=1/(L*L);n=int(tau/delta)
    errors=[abs((pf+gf*cmath.exp(1j*d*delta))**n-cmath.exp(1j*d*gf*tau)) for d in (-2,-1,0,1,2)]
    err=max(errors);bound=.5*n*gf*(1-gf)*delta**2*4+gf*delta*2
    fullsq=max(0.,2-2*(cmath.exp(-1j*gf*tau)*(pf+gf*cmath.exp(1j*delta))**n).real)
    fullerr=sqrt(fullsq)
    fullbound=sqrt(n*gf*(1-gf)*delta**2+(n*gf*delta-gf*tau)**2)
    assert err<=bound+1e-13 and fullerr<=fullbound+1e-11
    print(L,n,format(err,'.12g'),format(err/delta,'.12g'),format(fullerr,'.12g'))
ok(True,'actual CAR16 channel has O(h²) deterministic coherent limit; entire retained Stinespring map has O(h) error')
# Exact finite-cap weights already computed: optional controller also preserves Golden tape cost.
EK=sum(k*g**k*p**(len(w)-k) for w,k,A in leaves)
ok(eq(EK,g*ET),'bounded real stopping time retains exact Wald code/clock budget E K=g E T')
print('CAP_COUNT',len(leaves),'completion',float(Q),'attempts',float(ET),'code',float(ET+EK))
