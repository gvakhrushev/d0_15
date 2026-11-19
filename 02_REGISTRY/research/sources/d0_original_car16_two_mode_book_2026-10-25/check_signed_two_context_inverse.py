#!/usr/bin/env python3
"""SIGNED GLOBAL original CAR16 inverse from TWO ACTUAL K1 Born preparations.

Checks exact polynomial s/t, unique stationary rho as POLYNOMIAL in original
Delta, original CAR vacuum Delta_00, K1 on prepared stationary and vacuum
DATA, signed boost ratio strictly increasing on [-1/9,1/9], uniform
r-inverse conditioning and a NONZERO full signed-chart Jacobian at r=0.
Only built-in sympy/numpy/scipy and the OWNED unchanged original native
five-function excerpt from immutable source blob ee8de4635d24 are used.

Original 128 fine outcomes remain in the actual Kraus array. The two
preparations are two different PAID physical tasks; no cloned unknown
DATA state, free Born mean, original whole Book03 HJR source or full42 GR
admission is presumed.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as S

ROOT = Path(__file__).resolve().parent.parent / "d0_native65_causal_source_2026-10-22"
sys.path.insert(0, str(ROOT))
from native_excerpt import native, creators  # unchanged original CAR16/Julia/Walsh/Golden128

r,nu,p = S.symbols("r nu p",real=True,positive=True)
# For signed r, symbolic r is not constrained positive in all sympy versions:
r = S.symbols("r",real=True)
pnum=(math.sqrt(5.0)-1)/2
zeta=2**-20
A=5*r**4+r**3-8*r**2-r+5
B=23*r**4+6*r**3-32*r**2-10*r+25
C=27*r*r-50*r+25
G=7*r**4+48*r**3-58*r**2+80*r-25
s=nu*nu*A/(64*(1-r*r)**2)
t=nu**4*B/(16384*(1-r*r)**2)
qstat=p**3*nu**4*B/(4096*(1-r*r)**2)
qvac=p**3*nu**4*C/(4096*(1-r)**2)
ratio=(1+r)**2*C/B

checks=0
def check(cond, msg):
    global checks
    checks+=1
    if not bool(cond):raise AssertionError(msg)
def eq(lhs,rhs,msg):
    check(S.cancel(lhs-rhs)==0,msg)
def near(lhs,rhs,tol,msg):
    check(float(abs(lhs-rhs))<tol,f"{msg}: {lhs}, {rhs}")

# ALL-r symbolic equations -- no finite sampling substituted for algebra.
eq(qstat,4*p**3*t,"original stationary true K1 probability")
eq(qvac,4*p**3*(5*s*nu**2/128-t),"ORIGINAL vacuum K1 probability")
eq(qvac/qstat,ratio,"exact native two-preparation ratio")
expected_prime=-10*(1-r*r)*G/B**2
eq(S.diff(ratio,r),expected_prime,"global ratio derivative factorized")
eq(S.diff(s,r),
   nu**2*(1+r*r)*(r*r+4*r-1)/(64*(1-r*r)**3),
   "native s signed boost derivative")
f=A/(1-r*r)**2
eq(S.diff(f,r),(1+r*r)*(r*r+4*r-1)/(1-r*r)**3,
   "native s/nu² strictly monotone on entire signed chart")
eq(qvac,
   p**3*nu**4*(27*r*r-50*r+25)/(4096*(1-r)**2),
   "vacuum record original closed simplified law")
jac=S.det(S.Matrix([[S.diff(qstat,r),S.diff(qstat,nu)],
                    [S.diff(qvac,r),S.diff(qvac,nu)]]))
eq(jac,5*p**6*nu**7*G/(2**21*(1-r*r)**3),
   "signed original qstat/qvac Jacobian on ENTIRE native chart")
eq(jac.subs(r,0),-125*p**6*nu**7/(2**21),
   "r0 physically observable Jacobian does NOT vanish")
eq(ratio.subs(r,0),1,"zero boost is equality of TWO native K1 rates")
eq(ratio.subs(r,S.Rational(1,9)),S.Rational(8010,7711),
   "true original r=1/9 calibrated native ratio")
eq(ratio.subs(r,-S.Rational(1,9)),S.Rational(40032,42173),
   "opposite native signed chart endpoint")

# Exact signed-domain rational bounds, all j sample inequalities have
# symbolic interval proofs in the new parent, not a numerical scan.
Bmin=25-S.Rational(6,729)-S.Rational(32,81)-S.Rational(10,9)
Bmax=25+S.Rational(23,6561)+S.Rational(6,729)+S.Rational(32,81)+S.Rational(10,9)
Gmax=S.Rational(7,6561)+S.Rational(48,729)+S.Rational(80,9)-25
check(Bmin>0 and Bmax<27,"literal B(r)>0 with B(r)<27 for |r|<=1/9")
check(Gmax< -16,"literal G(r)<-16 for |r|<=1/9")
check((S.Rational(80,81)*10*16/27**2)==S.Rational(12800,59049),
      "rigorous global signed inverse Lipschitz derivative")
check(S.Rational(1,81)+S.Rational(4,9)-1<0,
      "s/nu² coordinate strictly decreasing across signed interval")
check(ratio.subs(r,-S.Rational(1,9))<1<
      ratio.subs(r,S.Rational(1,9)),
      "exact signed boost sign is the sign of qvac-qstat")

# Full original CAR vacuum is the UNIQUE common kernel of the original
# four ANNIHILATORS. This is the state of original four empty source
# grades, not a new chosen eigenvector or U(16) resource.
annihilators=np.vstack([cc.conj().T for cc in creators()])
singular_values=np.linalg.svd(annihilators,compute_uv=False)
check(int(np.sum(singular_values>1e-12))==15,
      "true original four CAR annihilators have 1D COMMON vacuum kernel")
check(np.linalg.norm(annihilators@I16[:,0])<1e-12,
      "the ORIGINAL computational allblank is the canonical CAR vacuum")
# Exact joint SOURCE inversion. No eigenvalue gap or division by r:
# rdot is reconstructed from the ratio of genuine q1 jets;
# nudot/nu then from the original qstat source.
rprime=S.diff(ratio,r)
dr_from_r=S.factor((qstat*S.diff(qvac,r)-qvac*S.diff(qstat,r))
                   /(qstat*qstat*rprime))
dr_from_nu=S.factor((qstat*S.diff(qvac,nu)-qvac*S.diff(qstat,nu))
                    /(qstat*qstat*rprime))
check(S.cancel(dr_from_r-1)==0 and S.cancel(dr_from_nu)==0,
      "two native Born SOURCE jets EXACTLY recover dr even at r=0")
coef=S.diff(B,r)/B+4*r/(1-r*r)
dn_from_r=S.factor((S.diff(qstat,r)/qstat-coef*dr_from_r)/4)
dn_from_nu=S.factor((S.diff(qstat,nu)/qstat-coef*dr_from_nu)/4)
check(S.cancel(dn_from_r)==0 and
      S.cancel(dn_from_nu-1/nu)==0,
      "two native Born SOURCE jets EXACTLY recover moving dnu/nu")

# Exact SIGNED signed-boost COLLISION of the older two-stationary-outcome
# q0,q1 route: Rspec=t/s² folds across r=0. A second paid vacuum
# context is truly needed if the task must distinguish both native signs.
Rspec=S.factor(B*(1-r*r)**2/(4*A*A))
HH=8*r**7+25*r**6+32*r**5-15*r**4-56*r**3+39*r*r+15
check(S.cancel(S.diff(Rspec,r)+r*(1-r*r)*HH/(2*A**3))==0,
      "exact signed spectral-fold derivative with original CAR polynomial")
check(15-S.Rational(8,9**7)-S.Rational(32,9**5)-
      S.Rational(15,9**4)-S.Rational(56,9**3)>14,
      "exact H(r)>14 on both signed boost branches")
f_spec=S.factor(A/(1-r*r)**2)
r_plus=S.Rational(1,20)
nu_plus=S.Rational(3,5)
check(Rspec.subs(r,-S.Rational(1,9))<
      Rspec.subs(r,r_plus)<S.Rational(1,4),
      "exact rational IVT: unique distinct negative signed CAR collision")
from scipy.optimize import brentq
r_minus=brentq(lambda xx:float(Rspec.subs(r,xx)-
                                 Rspec.subs(r,r_plus)),
               -1/9,0,xtol=1e-14)
nu_minus=float(nu_plus)*math.sqrt(
    float(f_spec.subs(r,r_plus))/float(f_spec.subs(r,r_minus)))
check(-1/9<r_minus<0 and 0<nu_minus<float(nu_plus),
      "same spectral action but DIFFERENT regular native signed parameters")
Kplus,_=native(2*math.atanh(float(r_plus)),float(nu_plus),(1j,1j,-1.,-1j))
Kminus,_=native(2*math.atanh(r_minus),nu_minus,(1j,1j,-1.,-1j))
def selfprepared_probs(ks):
    dl=(I16-ks[0])/(2*pnum*pnum)
    rho=np.linalg.inv(dl)
    rho/=np.trace(rho)
    return [float(np.trace(rho@ks[i].conj().T@ks[i]).real)
            for i in (0,1)]
pplus=selfprepared_probs(Kplus)
pminus=selfprepared_probs(Kminus)
near(max(abs(x-y) for x,y in zip(pplus,pminus)),0,2e-12,
     "TWO original self-prepared native fine probabilities EXACTLY COLLIDE")
vp=float(np.vdot(Kplus[1][:,0],Kplus[1][:,0]).real)
vm=float(np.vdot(Kminus[1][:,0],Kminus[1][:,0]).real)
check(vp>vm and vp-vm>7e-6,
      "SAME original K1 on canonical CAR vacuum DISTINGUISHES signed collision")


# Original whole 16x16 native CAR/Julia/Walsh constructor, including
# every one of the 128 fine outcomes and all dark operators.
I16=np.eye(16,dtype=np.complex128)
samples=[(-1/9,.6),(-.075,.55),(-.025,.5),(0,.6),
         (.025,.5),(.075,.55),(1/9,.6)]
results=[]
for rv,nv in samples:
    theta=2*math.atanh(rv)
    K,dK=native(theta,nv,(1j,1j,-1.0,-1j))
    check(K.shape==(128,16,16) and dK.shape==(128,16,16),
          "unaltered all128 real original Kraus and theta jets retained")
    total=np.einsum("aij,aik->jk",K.conj(),K,optimize=True)
    near(np.linalg.norm(total-I16),0,1e-11,
         "ALL full128 actual outcomes physical normalization")
    delta=(I16-K[0])/(2*pnum*pnum)
    delta=(delta+delta.conj().T)/2
    sv=float(s.subs({r:rv,nu:nv}))
    tv=float(t.subs({r:rv,nu:nv}))
    near(np.linalg.norm(delta@delta-sv*delta+tv*I16),0,1e-11,
         "exact original CAR minimal polynomial Delta²-sDelta+t=0")
    near(delta[0,0].real,5*nv**2/128,2e-13,
         "native vacuum CAR Delta00=5nu²/128, ALL true boosts")
    rho=np.linalg.inv(delta)
    rho=rho/np.trace(rho)
    rho2=(sv*I16-delta)/(8*sv)
    near(np.linalg.norm(rho-rho2),0,1e-11,
         "true self-prepared full128 state POLYNOMIAL not new free rho")
    near(float(np.trace(rho2).real),1,1e-13,
         "original physical stationary DATA trace exactly one")
    # Input-independent stationary native Kraus channel is the owner.
    rho_after=np.einsum("aij,jk,alk->il",K,rho2,K.conj(),optimize=True)
    near(np.linalg.norm(rho_after-rho2),0,1e-11,
         "TRUE ORIGINAL full128 channel fixes generated stationary rho")
    parity=np.diag([1 if (i.bit_count()%2==0) else -1 for i in range(16)])
    near(abs(np.trace(rho2@parity)),0,1e-12,
         "both genuinely distinguishable CAR parity sectors have mass1/2")
    qstat_native=float(np.trace(rho@K[1].conj().T@K[1]).real)
    qvac_native=float(np.vdot(K[1][:,0],K[1][:,0]).real)
    qstat_theory=float(qstat.subs({r:rv,nu:nv,p:pnum}))
    qvac_theory=float(qvac.subs({r:rv,nu:nv,p:pnum}))
    near(qstat_native,qstat_theory,2e-12,
         "original K1 on TRUE self-prepared rho_star")
    near(qvac_native,qvac_theory,2e-12,
         "original SAME K1 on ORIGINAL CAR blank state")
    ratio_native=qvac_native/qstat_native
    near(ratio_native,float(ratio.subs(r,rv)),5e-10,
         "global signed original K1 ratio is instrument-observable")
    check((ratio_native>1)==(rv>0) if rv!=0 else abs(ratio_native-1)<1e-10,
          "physical sign from comparing TWO Born probabilities")
    # Full original moving theta derivative of the observed rho*.
    dsdr=float(S.diff(s,r).subs({r:rv,nu:nv}))
    dsdtheta=dsdr*(1-rv*rv)/2
    ddelta=-dK[0]/(2*pnum*pnum)
    drho=-ddelta/(8*sv)+delta*dsdtheta/(8*sv*sv)
    dinv=-np.linalg.inv(delta)@ddelta@np.linalg.inv(delta)
    drho_inv=dinv/np.trace(np.linalg.inv(delta)) - np.linalg.inv(delta)*np.trace(dinv)/(np.trace(np.linalg.inv(delta))**2)
    near(np.linalg.norm(drho-drho_inv),0,1e-10,
         "moving self-preparation SOURCE exact polynomial vs inverse jet")
    dstat=(np.trace(drho@K[1].conj().T@K[1])+
           np.trace(rho@(dK[1].conj().T@K[1]+K[1].conj().T@dK[1]))).real
    dvac=(np.vdot(dK[1][:,0],K[1][:,0])+np.vdot(K[1][:,0],dK[1][:,0])).real
    exprstat=float(S.diff(qstat,r).subs({r:rv,nu:nv,p:pnum}))*(1-rv*rv)/2
    exprvac=float(S.diff(qvac,r).subs({r:rv,nu:nv,p:pnum}))*(1-rv*rv)/2
    near(dstat,exprstat,1e-10,"TRUE original Poisson/moving rho source")
    near(dvac,exprvac,1e-10,"TRUE original vacuum K1 Lorentz source")
    # Reconstruct all original coordinates from TWO probabilities.
    target=ratio_native
    from scipy.optimize import brentq
    lower=float(ratio.subs(r,-S.Rational(1,9)))
    upper=float(ratio.subs(r,S.Rational(1,9)))
    # The original floating Kraus at a CLOSED endpoint may differ by
    # 1e-15 from the exact algebraic endpoint ratio. Avoid an unphysical
    # brentq bracket failure; interval check is separately exact.
    if abs(target-lower)<1e-12:
        rb=-1/9
    elif abs(target-upper)<1e-12:
        rb=1/9
    else:
        check(lower<target<upper,"actual sampled Born ratio inside chart")
        rb=brentq(lambda zz:float(ratio.subs(r,zz))-target,
                  -1/9,1/9,xtol=1e-13)
    nub=(4096*(1-rb*rb)**2*qstat_native/
         (pnum**3*float(B.subs(r,rb))))**.25
    near(rb,rv,1e-10,"global signed inverse native r with NO branch choice")
    near(nub,nv,1e-10,"global signed inverse native nu")
    results.append({"r":rv,"nu":nv,"q_stat":qstat_native,
                    "q_vac":qvac_native,"ratio":ratio_native,
                    "recovered_r":rb,"recovered_nu":nub})

print(json.dumps({
    "status":"PASS_ORIGINAL_FULL128_TWO_PAID_K1_CONTEXT_GLOBAL_SIGNED_INVERSE",
    "checks":checks,
    "sample_count":len(samples),
    "r_domain":"[-1/9,1/9]",
    "nu_domain":"(0,3/5]",
    "original_native_Kraus_labels":128,
    "r_inverse_lipschitz_upper":"59049/12800",
    "r_zero_jacobian_nonzero":True,
    "one_label_two_distinct_preparations":True,
    "physically_admitted_and_paid_two_context_experiment":False,
    "signed_born_ratio_results":results,
    "stationary_same_q0_q1_signed_collision":{
        "r_plus":str(r_plus),"r_minus_numeric":r_minus,
        "nu_plus":str(nu_plus),"nu_minus_numeric":nu_minus,
        "native_q0_q1_plus":pplus,"native_q0_q1_minus":pminus,
        "original_vacuum_K1_strict_gap":vp-vm},
    "source_jets_globally_signed_invertible":True,
    "physical_two_context_task_selected_by_M1":False,
    "full42_GR_closed":False
},indent=2,sort_keys=True))
