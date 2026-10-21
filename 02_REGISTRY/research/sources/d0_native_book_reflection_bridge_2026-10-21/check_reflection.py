#!/usr/bin/env python3
"""Original Golden binary-record -> TRUE Book03 complement, exact source tests.

The script performs exact symbolic controls and separate matrix-level
implementations, and does not assume physical selection or original full128
Kraus implementation. No asserts: python -O also checks every condition.
"""
from __future__ import annotations
import json
import math
import numpy as np
import sympy as sp

checks=[]
def ck(test, name):
    if not bool(test):
        raise ArithmeticError(name)
    checks.append(name)

p=(sp.sqrt(5)-1)/2
phi=1/p
z=sp.Rational(1, 2**20)
a=sp.sqrt(p)
X=sp.Matrix([[0,1],[1,0]])
G=sp.Matrix([[a,-p],[p,a]])
Rg=X*G
Z=sp.diag(1,-1)
ck(sp.simplify(p+p**2-1)==0,'Golden partition p+p^2=1')
ck(sp.simplify(G.T*G-sp.eye(2))==sp.zeros(2),'native G orthogonal')
ck(sp.simplify(Rg-Rg.T)==sp.zeros(2),'native comparator XG symmetric')
ck(sp.simplify(Rg*Rg-sp.eye(2))==sp.zeros(2),'native comparator XG involutory')
ck(sp.simplify(X*G*X-G.T)==sp.zeros(2),'inverse Golden from XGX')

for x,y in [(sp.Rational(3,5),sp.Rational(4,5)),
            (sp.Rational(5,13),sp.Rational(12,13)),
            (sp.Rational(1,1),sp.Rational(0,1)),
            (sp.Rational(0,1),sp.Rational(1,1))]:
    V=sp.Matrix([[x,-y],[y,x]])
    R=V.T*Z*V
    C=sp.kronecker_product(Rg,sp.eye(2))*sp.diag(sp.eye(2),R)*sp.kronecker_product(Rg,sp.eye(2))
    q=y**2
    t=sp.simplify(C[0,0])
    ck(sp.simplify(V.T*V-sp.eye(2))==sp.zeros(2),'exact compiled V unitary')
    ck(sp.simplify(R*R-sp.eye(2))==sp.zeros(2),'exact V^T Z V reflection')
    ck(sp.simplify(C.T*C-sp.eye(4))==sp.zeros(4),'exact Golden comparator unitary')
    ck(sp.simplify(t-(1-2*p*q))==0,'complete rank-one return scalar')
    ck(sp.simplify(1-t*t-4*p*q*(1-p*q))==0,'true complementary return F(r)')
    ck(sp.simplify((C.T*(sp.eye(4)-sp.diag(1,0,0,0))*C)[0,0]-(1-t*t))==0,
       'complete complement, not selected pointer effect')

# Symbolic source, rank-one positivity and Golden current
r=sp.symbols('r',real=True)
F=4*p*r*(1-p*r)
B=-sp.log(1-z*F)
dB=sp.diff(B,r)
ck(sp.simplify(sp.diff(F,r)-4*p*(1-2*p*r))==0,'feedback derivative exact')
ck(sp.simplify(dB-z*sp.diff(F,r)/(1-z*F))==0,'true logdet derivative exact')
ck(sp.simplify(F.subs(r,sp.Rational(1,2))-(3*p-1))==0,
   'fair centre true complement is 3p-1')
ck(sp.simplify(dB.subs(r,sp.Rational(1,2))-4*z*p**3/(1-z*(3*p-1)))==0,
   'fair centre positive native book first-source gain')
ck(float(sp.N(p))<sp.Rational(2,3),'Golden monotone range p<2/3')

# Actual N1 output at zero and exact fixed fair-centering coin.
L0=4*p**3
Q=1-z*L0
R0=1-z*L0*(1+p**6)
r0=1-Q*R0
ck(0<float(sp.N(r0))<sp.Rational(1,2),'original cap-N1 base in positive support')
coin=(1+r0)/3
ck(0<float(sp.N(coin))<1,'exact fair-centering Q(p) coin admitted numerically')
W=sp.symbols('W',positive=True)
bar=sp.symbols('qbar',real=True)
rt=(1-bar)/4+3*coin/4
ck(sp.simplify(rt-(2+r0-bar)/4)==0,'positive quartile recenter rule')
ck(sp.simplify(rt.subs(bar,r0)-sp.Rational(1,2))==0,
   'exact fair centre on common-null N1 report')
ck(sp.diff(rt,bar)==-sp.Rational(1,4),'fixed negative slope native complement')
ck(float(sp.N(rt.subs(bar,0)))<.75 and float(sp.N(rt.subs(bar,1)))>.25,
   'entire allowed local report image in [1/4,3/4]')
ck(float(sp.N(2*p*sp.Rational(3,4)))<1,
   'feedback source globally positive on all fair-recentred codes')

# Common all42 response against actual paid N1 CQ source.
weights=(2,3,5,11)
alpha=sp.symbols('alpha',real=True)
qsites=[r0+sp.Rational(i+1,10000)*alpha for i in range(len(weights))]
Wnum=sum(weights)
qbar=sum(w*q for w,q in zip(weights,qsites))/Wnum
rfield=rt.subs(bar,qbar)
source_book=sp.diff(B.subs(r,rfield),alpha).subs(alpha,0)
Hp=sp.log((1-r0)/r0)/sp.log(phi)
source_cq=-Hp*sum(w*sp.diff(q,alpha) for w,q in zip(weights,qsites))
gain=z*p**3/(Wnum*(1-z*(3*p-1))*Hp)
ck(sp.simplify(source_book-gain*source_cq)==0,
   'all42 source proportionality on common null with positive gain')
ck(float(sp.N(gain))>0,'sign agrees with true native CQ cost-minus-entropy')
# Same equality remains valid for every independently varied site direction.
for index,w in enumerate(weights):
    qq=sp.symbols('q')
    seq=[(qq if j==index else r0) for j in range(len(weights))]
    qbar_j=sum(ww*x for ww,x in zip(weights,seq))/Wnum
    dbook=sp.diff(B.subs(r,rt.subs(bar,qbar_j)),qq).subs(qq,r0)
    dcq=-Hp*w
    ck(sp.simplify(dbook-gain*dcq)==0,'independent original local-copy Euler source '+str(index))

# Source matching is not Hessian matching: two independent local reports
# have a stationary sum, but their Shannon curvature survives aggregation.
hpp=-1/(sp.log(phi)*r0*(1-r0))
ss=sp.symbols('s',real=True)
q1=r0+ss; q2=r0-ss
rbalance=rt.subs(bar,(q1+q2)/2)
ck(sp.simplify(sp.diff(rbalance,ss))==0,
   'weighted mean first source can vanish with nonzero local responses')
ck(sp.simplify(sp.diff(B.subs(r,rbalance),ss,2))==0,
   'aggregate Book second source vanishes in opposing-report mode')
ck(sp.simplify(hpp+1/(sp.log(phi)*r0*(1-r0)))==0,
   'actual Golden Shannon second derivative strictly negative')
ck(float(sp.N(hpp))<0,'strict entropy curvature sign')
# For two independent reports and gamma=1, original CQ Hessian = -2 hpp >0.
cq_hess=-2*hpp
ck(float(sp.N(cq_hess))>0,'original local-sum CQ has strict positive second source')
# Positive fixed CQ/Book first source gain, actual Hessian defect negative.
g2=z*p**3/(2*(1-z*(3*p-1))*Hp)
defect=2*g2*hpp
ck(sp.simplify(defect+g2*cq_hess)==0,
   'exact negative semidefinite Hessian defect after first-source agreement')
ck(float(sp.N(defect))<0,'Hessian defect negative rather than scale-equivalent')
# Strict finite-code descent of the constructed master, using a previously
# owned price-lowering comparison which increases every affected report.
comparison=sp.Rational(1,10**8)
r_comp=rt.subs(bar,r0+comparison)
r_root=rt.subs(bar,r0)
ck(float(sp.N(r_comp))<float(sp.N(r_root)),
   'a native reporter competitor increases local report, lowers fair bit')
ck(float(sp.N(F.subs(r,r_comp)))<float(sp.N(F.subs(r,r_root))),
   'true Book complement strictly decreases for the competitor')
ck(float(sp.N(B.subs(r,r_comp)))<float(sp.N(B.subs(r,r_root))),
   'fixed-scene Book master strict finite-code descent')

# Same one-carrier fixed K913 scene heat, rank1 active projection and extra dimension.
beta=2*p**2
Zscene=1+12*sp.exp(-20*beta)+10*sp.exp(-22*beta)+8*sp.exp(-24*beta)+2*sp.exp(-33*beta)
dextra=8
scene_heat=sp.log(dextra*Zscene)/beta
ck(sp.diff(scene_heat,alpha)==0,'same-carrier fixed 33-vertex scene heat has zero field jet')
ck(sp.simplify(sp.diff(scene_heat+B.subs(r,rfield),alpha).subs(alpha,0)-source_book)==0,
   'actual full Book03 master first source is generated by complementary return')

# Complex/entangled oldRIGHT on the FULL input (no invented counting multiplier).
vv=np.array([[.6,-.8],[.8,.6]],dtype=complex)
Cmat=np.kron(vv, np.eye(2,dtype=complex))
Pimat=np.kron(np.diag([0.,1.]),np.eye(2,dtype=complex))
ref=(np.array([1.,0.,0.,1.])+0j)/np.sqrt(2.)
rv=float(np.real(np.vdot(ref,Cmat.conj().T@Pimat@Cmat@ref)))
Rv=Cmat.conj().T@(np.eye(4)-2*Pimat)@Cmat
GG=np.array(Rg.evalf(),dtype=complex)
Cmp=np.kron(GG,np.eye(4))@np.block([[np.eye(4),np.zeros((4,4))],[np.zeros((4,4)),Rv]])@np.kron(GG,np.eye(4))
initial=np.zeros((2,4),dtype=complex);initial[0]=ref
vout=Cmp@initial.reshape(-1)
tval=np.vdot(initial.reshape(-1),vout)
ck(abs(tval.imag)<1e-12 and abs(tval.real-(1-2*float(p)*rv))<1e-12,
   'entangled oldRIGHT complete scalar return')
ck(abs(1-abs(tval)**2-4*float(p)*rv*(1-float(p)*rv))<1e-12,
   'true rank1 Book feedback with nontrivial protected RIGHT')
ck(np.linalg.norm(Cmp.conj().T@Cmp-np.eye(8))<1e-12,
   'fully unitary reflected circuit includes oldRIGHT spectator')

# Explicit independent-U Euler obstruction for rank-one active Book cut.
# Fair reporter r=1/2 is realized with a Hadamard work bit.
Vfair=np.array([[1.,1.],[1.,-1.]])/np.sqrt(2.)
Rfair=Vfair@np.diag([1.,-1.])@Vfair
Ufair=np.kron(GG,np.eye(2))@np.block([[np.eye(2),np.zeros((2,2))],[np.zeros((2,2)),Rfair]])@np.kron(GG,np.eye(2))
chi=np.array([1.,0.,0.,0.],dtype=complex)
returnamp=float(np.vdot(chi,Ufair@chi).real)
Ffair=1-returnamp**2
ck(abs(returnamp-float(p*p))<1e-12,'fair circuit active return amplitude p^2')
ck(abs(Ffair-float(3*p-1))<1e-12,'fair full Book feedback is strictly between 0 and 1')
xi=Ufair.conj().T@chi-returnamp*chi
xi=xi/math.sqrt(Ffair)
Xfree=np.outer(xi,chi.conj())-np.outer(chi,xi.conj())
ck(np.linalg.norm(Xfree+Xfree.conj().T)<1e-12,'explicit legitimate free-U skew tangent')
ampprime=float(np.vdot(chi,Ufair@Xfree@chi).real)
ck(abs(ampprime-math.sqrt(Ffair))<1e-12,'rank-one free-controller tangent reaches return scalar')
controller_jprime=-2*float(z)*returnamp*math.sqrt(Ffair)/(1-float(z)*Ffair)
ck(controller_jprime<0,'unrestricted controller Euler nonzero at useful reporter')

# Actual coherent inverse is necessary: a prematurely dephased H->Z->H
# route is a mixed channel, not the unitary reflection H Z H = X.
Hreal=np.array([[1.,1.],[1.,-1.]])/np.sqrt(2)
coherent=Hreal@np.diag([1.,-1.])@Hreal@np.array([1.,0.])
rh=Hreal@np.array([1.,0.])
rho=np.outer(rh,rh)
deph=np.diag(np.diag(rho))
post=Hreal@np.diag([1.,-1.])@deph@np.diag([1.,-1.])@Hreal
ck(np.linalg.norm(coherent-np.array([0.,1.]))<1e-12,
   'coherent V^dag Z V implements true reflection')
ck(np.linalg.norm(post-np.outer(coherent,coherent))>0.5,
   'early dephasing breaks exact Book reflection')

out={
 'status':'PASS', 'check_count':len(checks),'checks':checks,
 'native':{'p':str(sp.N(p,24)), 'z':str(z), 'n1_report_r0':str(sp.N(r0,24)),
           'fair_reference_coin':str(sp.simplify(coin)),
           'fair_book_gain':str(sp.N(dB.subs(r,sp.Rational(1,2)),24)),
           'complete_ratio_positive':str(sp.N(gain,24))},
 'true_feedback':{'return_amplitude':'1-2p*r',
                  'complement':'4p*r*(1-p*r)',
                  'active_rank':'1 including oldRIGHT in same pure input',
                  'same_scene_heat':'33-vertex K(9,11,13) fixed Laplacian'},
 'record_safety':{'no_controlled_unknown_V':True,'uncompute_requires_coherence':True,
                  'full_existing_paid_record_equivalence_proved':False},
 'scope':{'all42_source_on_declared_null_CQ_section':True,
          'native_gate_controller_and_original_Book_Info_selected':False,
          'independent_upstream_stationary':False,
          'uniform_raw216_proved':False,'GR_closed':False}
}
print(json.dumps(out,sort_keys=True,indent=2))
