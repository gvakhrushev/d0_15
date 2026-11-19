#!/usr/bin/env python3
"""General original Book03 feedback as exact native Golden-marked P/Q pingpong.

Uses only U and U-adjoint, alternating original projective P/Q reads, and
independent original F/R Golden fair-bit extraction (20 bits => 2^-20).
No sqrt(F), no inverse polar return, no invisible discarded stop branches.
An explicit 6x6 rational noncommuting source is checked EXACTLY.
Original U-adjoint's physical native availability / Book H+J+R selection
is NOT established by the algebraic feedback identity.
"""
from functools import reduce
from math import log, sqrt
from mpmath import mp
import sympy as s

D=6
Q=s.Rational
P=s.diag(1,1,1,0,0,0)
C=s.eye(D)-P

def rot(i,j,a,b):
    out=s.eye(D)
    out[i,i]=out[j,j]=a
    out[i,j]=-b;out[j,i]=b
    return out
U=reduce(lambda a,b:a*b,(
    rot(1,4,Q(3,5),Q(4,5)), rot(0,3,Q(5,13),Q(12,13)),
    rot(0,1,Q(3,5),Q(4,5)), rot(2,5,Q(3,5),Q(4,5)),
    rot(1,5,Q(5,13),Q(12,13))),s.eye(D))
assert U.T*U==s.eye(D)
F=P*U.T*C*U*P
assert F==F.T and F.rank()==3
assert F[0,1]!=0 and F[1,2]!=0
assert F != s.diag(*list(F.diagonal()))
V=C*U*P
assert F==V.T*V
T=P
for n in range(1,13):
    T=(C*U if n%2 else P*U.T)*T
    assert T.T*T==F**n
    if n%2==0: assert T==F**(n//2)
    else: assert T==V*(F**((n-1)//2))
print('PASS 12 rational exact full original P/U/Q alternated-success operators F^n, non-diagonal rank3, arbitrary oldRIGHT states')

p=s.simplify((s.sqrt(5)-1)/2)
phi=1/p
z=Q(1,2**20)
assert s.simplify(p+p**2-1)==0
assert s.simplify(p**6+4*p**3-1)==0
coin_fail=s.simplify(1-2*p**3)
coin_code=s.simplify((p+2*p**2)/p**3)
assert s.simplify(coin_code-(3*phi+1))==0
bank_code=20*coin_code
print('PASS original FAIR Golden pair FR/RF native p^3 each, 20 bits exactly zeta, real expected Golden cost 20(3phi+1)')

# Arbitrary strictly positive noncommuting initial active density.
psi=s.Matrix([1,2,3,0,0,0])/s.sqrt(14)
rho=psi*psi.T
assert s.trace(rho)==1 and P*rho*P==rho
m=[s.trace(rho*F**n) for n in range(13)]
assert m[0]==1
for n in range(1,12):
    assert 0<m[n+1]<m[n]<1
    survival=z**n*m[n]
    # All Golden-bank failures are retained; when bank passes, actual P/Q
    # test fails or passes. The terminal measures sum exactly to 1.
    stop=(1-z)*z**n*m[n]+z**(n+1)*(m[n]-m[n+1])
    assert s.simplify(stop-(z**n*m[n]-z**(n+1)*m[n+1]))==0
    assert survival>0 and stop>0
# From the first attempt: no coin bank accept -> stop, or coin passes and
# the first P/Q test fails. Its weight 1-z*m1 includes BOTH outcomes.
assert 1-z*m[1]>0
print('PASS full geometrical original stop law by coin-fail OR projective-fail, all histories and arbitrary initial rho')

# Original full Book03 first-source, including a truly noncommuting F' jet.
X=s.zeros(D)
for i,j,a in ((0,4,Q(1,3)),(1,3,Q(2,5)),(2,5,Q(1,7))):
    X[i,j]=-a;X[j,i]=a
DF=P*U.T*(X.T*C+C*X)*U*P
assert DF==DF.T and DF!=s.zeros(D)
R=(s.eye(D)-z*F).inv()
book_source=z*s.trace(R*DF)
assert book_source != 0
partial=sum((z**n)*s.trace(F**(n-1)*DF) for n in range(1,8))
assert abs(float(book_source-partial))<1e-33
print('PASS original P/U/Q matrix logdet first jet equals complete harmonic stop-moment derivative, noncommuting DF')

# Native full archived Golden budget when generating 20 bits on EVERY
# reached stage, BEFORE deciding whether to execute the next P/Q test.
# This is a true paid expected code and expected number of primitive U tests.
A_pure=s.trace(rho*R)
A_trace=s.trace(P*R)/3
E_coin_pure=bank_code*A_pure
E_test_pure=z*A_pure
assert A_pure>1 and A_pure<1/(1-z)
assert E_test_pure<z/(1-z)
assert E_coin_pure>bank_code
A_source=z*s.trace(rho*R*DF*R)
J_per_active_source=book_source/3
E_coin_trace_source=z*bank_code*s.trace(R*DF*R)/3
assert A_source!=0 and E_coin_trace_source!=0
print('PASS exact paid Golden coin Cost=20(3phi+1) Tr[rho (I-zF)^-1]; nonzero moving physical clock/work source')

# Finite terminating approximation: each of 20 fair bits capped at M pair
# draws. Every pair-tie, bit abort and terminal projective event is archived.
# At most K stages. No exact fair bit is asserted at fixed finite M.
for paircap in (3,6,12,24):
    zM=z*(1-coin_fail**paircap)**20
    assert 0<zM<z
    assert float(z-zM)<float(20*z*coin_fail**paircap)
    for K in (1,2,3):
        # Finite state estimator = E [H_{min(N,K)}] * d.
        estimator=sum(zM**n*s.trace(F**n)/n for n in range(1,K+1))
        assert estimator>0
        if paircap==24 and K==3:
            mp.dps=80
            detr=(s.eye(D)-z*F).det()
            exact=-mp.log(mp.mpf(detr.p)/detr.q)
            term=mp.mpf(str(s.N(estimator,75)))
            zm=mp.mpf(str(s.N(zM,75)))
            zz=mp.mpf(str(s.N(z,75)))
            qm=mp.mpf(str(s.N(coin_fail,75)))
            bound=D*20*zz*qm**paircap/(1-zz)+D*zm**(K+1)/((K+1)*(1-zm))
            assert abs(term-exact)<bound
print('PASS native exactly specified finite-cap Golden bit and geometric stopping hist; no free zeta at bounded depth')

# The complete SAME recorded fine-history Cost−Shannon is calculable;
# it is NOT the same functional as Book J=d E H_N. Golden banks themselves
# contribute exactly zero conditional KL when retained with their native
# F/R code; projective outcome probabilities still have genuine source.
pnum=float(p);golden_log=log(1/pnum);zn=float(z)
def net(t):
    entropy=-(t*log(t)+(1-t)*log(1-t))/golden_log
    return 1+t-entropy
fine_score=zn*sum(zn**n*float(m[n])*net(float(m[n+1]/m[n])) for n in range(8))
assert fine_score>0
Jscore=-log(float((s.eye(D)-z*F).det()))/3
assert abs(fine_score-Jscore)>1e-9
print('PASS one SAME stopped record has distinct exact observables: Book J=d EH_N; full paid measured Cost−Shannon from conditional native geometry flags')

# Standalone literal small-prefix enumeration of all native Golden coins AND
# projective results at finite cap, independent of operator calculus.
records=[]
test_pass=Q(71,100)

def enum_prefix(word,prob,cost,depth,cap):
    if depth==cap:
        records.append((word,float(prob),cost));return
    # Native Golden R=10 coin failure; native Golden F=0 coin success.
    records.append((word+'10',float(prob*p**2),cost+2))
    # On the F coin, the projective failure is ALSO recorded as F=0.
    records.append((word+'00',float(prob*p*(1-test_pass)),cost+2))
    # Projective pass is recorded as native R=10.
    enum_prefix(word+'010',prob*p*test_pass,cost+3,depth+1,cap)

enum_prefix('',s.Integer(1),0,0,4)
assert abs(sum(prob for word,prob,c in records)-1)<1e-12
assert all(not a[0].startswith(b[0]) and not b[0].startswith(a[0])
           for i,a in enumerate(records) for b in records[i+1:])
Ecost=sum(prob*cost for word,prob,cost in records)
H=-sum(prob*log(prob)/golden_log for word,prob,cost in records)
expected=pnum*sum((pnum*float(test_pass))**n for n in range(4))*net(float(test_pass))
assert abs(Ecost-H-expected)<1e-12
# At native Q8 F=p²P, net(p²)=0 while the Book return J is positive.
assert abs(net(pnum*pnum))<1e-13
assert -log(1-zn*pnum*pnum)>0
print('PASS explicit fully retained Golden-code prefix tree Cost−Shannon = conditional Bernoulli KL; p² reference zero but Book J positive')


# Finite original Golden-only bounded halted programme achieving ANY requested
# polynomial C1 source accuracy with maximum O((log L)^2) primitive draws.
# The inequality is for the mathematical Book feedback, not a selected full
# Book03 heat/Info/actuation, and all genuine native cap-abort flags remain.
from math import ceil
mp.dps=65
znum=mp.mpf(str(s.N(z,70)))
qnum=mp.mpf(str(s.N(coin_fail,70)))
Jnum=-mp.log(mp.mpf((s.eye(D)-z*F).det().p)/mp.mpf((s.eye(D)-z*F).det().q))
DJnum=mp.mpf(str(s.N(book_source,65)))
DFfro=mp.sqrt(sum(mp.mpf(str(s.N(value,65)))**2 for value in DF))
for L in (4,16,256,1024):
    for order in (2,4):
        capM=ceil(float((order*mp.log(L)+mp.log(40))/(-mp.log(qnum))))
        capK=ceil(float((order*mp.log(L)+mp.log(4))/(-mp.log(znum))))
        zcap=znum*(1-qnum**capM)**20
        delta=znum-zcap
        assert delta<=znum/(2*L**order)
        assert znum**capK<=1/(4*L**order)
        Jcap=mp.mpf(0); DJcap=mp.mpf(0)
        for n in range(1,capK+1):
            traceF=mp.mpf(str(s.N(s.trace(F**n),65)))
            traceDF=mp.mpf(str(s.N(s.trace(F**(n-1)*DF),65)))
            Jcap+=zcap**n*traceF/n
            DJcap+=zcap**n*traceDF
        err_value=D*delta/(1-znum)+D*zcap**(capK+1)/((capK+1)*(1-zcap))
        err_source=mp.sqrt(3)*DFfro*(delta/(1-znum)**2+zcap**(capK+1)/(1-zcap))
        assert abs(Jnum-Jcap)<err_value
        assert abs(DJnum-DJcap)<err_source
        actual_stages=sum(zcap**n*mp.mpf(str(s.N(m[n],65))) for n in range(capK))
        cost_bit=mp.mpf(str(s.N(coin_code,65)))
        coin_charge=20*cost_bit*(1-qnum**capM)*actual_stages
        assert coin_charge<=20*cost_bit/(1-znum)
        assert 40*capM*capK<10**8  # Actual finite worst-case Golden draw count.
        if L in (4,1024):
            print('PASS FINITE native programme L',L,'accuracy',order,
                  'paircap',capM,'stagecap',capK,'max Golden draws',40*capM*capK,
                  'Book value/source bounds',mp.nstr(err_value,7),mp.nstr(err_source,7))
print('PASS worst-case O(log(L)^2) full finite Golden/PQ programme with uniform C1 Book feedback source error O(L^-r)')

# A physically known ORIGINAL Book03 §03.26 Q8 splitter realizes a true
# forward-only inverse: Z=diag(1,-1)=X^2 on the declared arm/spin block.
G=s.Matrix([[s.sqrt(p),-p],[p,s.sqrt(p)]])
Z=s.diag(1,-1)
assert s.simplify(G.T*G-s.eye(2))==s.zeros(2)
assert s.simplify(Z*G*Z-G.T)==s.zeros(2)
P2=s.diag(1,0);Q2=s.eye(2)-P2
assert s.simplify(P2*G.T*Q2*G*P2-p**2*P2)==s.zeros(2)
print('PASS concrete original Q8 hardware G inverse uses only already owned forward X X G X X; F=p^2P')

print('BOOK_J_source_noncommuting=',s.N(book_source,18))
print('mean_original_Golden_bank_code_units=',s.N(bank_code,18))
print('mean_FULL_trajectory_Golden_bank_cost=',s.N(E_coin_pure,18))
print('mean_queries_U_or_Udagger=',s.N(E_test_pure,18))
print('physical_selected_Udagger_and_Book03_HJR_Info_writable=false; GR_closed=false')
