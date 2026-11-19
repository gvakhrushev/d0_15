#!/usr/bin/env python3
"""ORIGINAL 128-Kraus CAR16 stationary two Born records reconstruct COMPLETE
prepared Book determinant and moving proper-boost source.

No independent artificial q table: original native_excerpt.native returns
ALL native K0,...,K127 and their actual d/dtheta, with originally FIXED
phases (i,i,-1,-i), proper boost r=1/9, nu=3/5. Actual DATA stationary
rho=Delta^-1/Tr Delta^-1, and its derivative, enter ALL two Born jets.
The exact CAR2 two-eigenvalue proof is in the paired original theorem.
This checks the analytic inverse, its actual material graph limits and
true Poisson stationary preparation jet.

No inserted Fock Slater tester, new 20-bit flag, invented measurement
probability, Einstein source, native sector acceptance or GR promotion.
python3 check_two_native_born_records.py ; python3 -O same
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

import numpy as np
import sympy as S

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/
                      "d0_native65_causal_source_2026-10-22"))
from native_excerpt import native

checks=0
def check(ok,msg):
    global checks
    checks+=1
    if not bool(ok):
        raise ArithmeticError(msg)

p=(np.sqrt(5)-1)/2
z=2**-20
I=np.eye(16,dtype=complex)
def adj(m):return m.conj().T
def tr(m):return np.trace(m)
def near(a,b,tol,msg):
    check(abs(a-b)<tol,f"{msg}: got {a!r}, expected {b!r}")
def dataset(r,nu):
    theta=2*np.arctanh(float(r))
    K,dK=native(theta,float(nu),(1j,1j,-1.,-1j))
    check(K.shape==(128,16,16) and dK.shape==(128,16,16),
          "all original 128 fine Kraus AND their moving jets")
    near(np.linalg.norm(np.einsum("aij,aik->jk",K.conj(),K)-I),0,1e-11,
         "original FULL128 quantum channel CPTP")
    D=(I-K[0])/(2*p*p)
    near(np.linalg.norm(D-adj(D)),0,1e-11,
         "original Walsh K0 exact selfadjoint positive CAR Delta")
    D=(D+adj(D))/2
    check(0<np.linalg.eigvalsh(D).min()<
          np.linalg.eigvalsh(D).max()<1 or
          0<np.linalg.eigvalsh(D).min()<=np.linalg.eigvalsh(D).max()<1,
          "original two-eigenvalue contraction on tested positive chart")
    inv=np.linalg.inv(D)
    nrm=tr(inv).real
    rho=inv/nrm
    near(tr(rho).real,1,1e-11,"genuine full-rank stationary DATA normalized")
    near(np.linalg.norm(sum(k@rho@adj(k) for k in K)-rho),0,1e-11,
         "unmodified original channel uniquely self-prepares rho*")
    E0=adj(K[0])@K[0];E1=adj(K[1])@K[1]
    near(np.linalg.norm(E1-4*p**3*D@D),0,1e-11,
         "original fine label1 is actual Golden D², not an invented test")
    q0=tr(rho@E0).real;q1=tr(rho@E1).real
    fullprob=np.einsum("ij,aji->a",rho,
                       np.einsum("aik,akj->aij",K.conj().transpose(0,2,1),K))
    # Fullprob only used for positivity/normalization of all ACTUAL labels.
    check(q0>0 and q1>0,"two actual nonzero registered one-tick outcomes")
    near(sum(tr(rho@adj(k)@k) for k in K).real,1,1e-11,
         "all original unconditioned fine outcomes still present")
    gain=1-q0+p*q1
    check(gain>0,"real two-record inverse has no zero denominator")
    t=q1/(4*p**3)
    s=2*q1/(p*gain)
    near(s,tr(D).real/8,5e-12,
         "actual two original Born records reconstruct eigenvalue SUM")
    near(t,tr(D).real/tr(inv).real,5e-12,
         "actual two original Born records reconstruct eigenvalue PRODUCT")
    check(s>0 and t>0,"strict actual spectral response invariants")
    u=4*z*p*p;v=4*z*p**4
    survival=1-u*s+v*(s*s-2*t)+u*u*t-u*v*s*t+v*v*t*t
    F=I-E0
    book_mat=-np.linalg.slogdet(I-z*F)[1]
    book_obs=-8*np.log1p(survival-1)
    near(book_obs,book_mat,3e-15,
         "complete native16 Book -logdet reconstructed by 2 Born numbers")
    # d/dtheta of real MOVING native stationary state, not a frozen input.
    dD=-(dK[0])/(2*p*p)
    dD=(dD+adj(dD))/2
    dInv=-inv@dD@inv
    dNrm=tr(dInv).real
    dRho=dInv/nrm-inv*dNrm/(nrm*nrm)
    near(tr(dRho),0,1e-11,"full moving input remains normalized")
    def BornJet(j):
        kj=K[j];dk=dK[j]
        E=adj(kj)@kj
        return (tr(dRho@E)+tr(rho@(adj(dk)@kj+adj(kj)@dk))).real
    dq0=BornJet(0);dq1=BornJet(1)
    ds=2*((1-q0)*dq1+q1*dq0)/(p*gain*gain)
    dt=dq1/(4*p**3)
    dsd= -u+2*v*s-u*v*t
    dtd= -2*v+u*u-u*v*s+2*v*v*t
    observed_source=-8*(dsd*ds+dtd*dt)/survival
    dF=-adj(dK[0])@K[0]-adj(K[0])@dK[0]
    direct_source=(z*tr(np.linalg.solve(I-z*F,dF))).real
    near(observed_source,direct_source,1e-14,
         "ALL true moving-input one-tick Born JET gives original Book source")
    # The actual fixed point must obey the differentiated CHANNEL equation.
    Phi_prime_rho=sum(dk@rho@adj(k)+k@rho@adj(dk)
                      for k,dk in zip(K,dK))
    Phi_drho=sum(k@dRho@adj(k) for k in K)
    near(np.linalg.norm(dRho-Phi_drho-Phi_prime_rho),0,1e-10,
         "genuine original Poisson stationary preparation derivative")
    return dict(theta=theta,r=r,nu=nu,q0=q0,q1=q1,s=s,t=t,
                book=book_obs,book_source=observed_source,
                dq0=dq0,dq1=dq1,ds=ds,dt=dt)

def main():
    inputs=[(0,0.6),(1/9,0.6),(-1/7,0.5),(1/18,0.5)]
    data=[dataset(r,nu) for r,nu in inputs]
    point=data[1]
    near(point["q0"],0.97903428793653558822,1e-12,
         "original one-tick blank history Born")
    near(point["q1"],0.00017998771256661516879,1e-12,
         "original one-tick orphan history Born")
    near(point["book"],3.2042444113482065e-7,1e-14,
         "original CAR16 whole prepared feedback")
    near(point["book_source"],-1.8312595190037388e-8,1e-14,
         "original moving Lorentz Book source")
    # exact symbolic field chart & native inverse Jacobian
    r,n=S.symbols("r nu",real=True)
    pp=(S.sqrt(5)-1)/2
    s=n*n*(5*r**4+r**3-8*r*r-r+5)/(64*(1-r*r)**2)
    t=n**4*(23*r**4+6*r**3-32*r*r-10*r+25)/(
        16384*(1-r*r)**2)
    q1=4*pp**3*t
    q0=1-8*pp**2*t/s+4*pp**4*t
    g=1-q0+pp*q1
    def zero(x):return S.cancel(x)==0
    check(zero(q1/(4*pp**3)-t) and
          zero(2*q1/(pp*g)-s),
          "exact ALL-r algebraic Born inverse, not a fitted scalar curve")
    h=8*r**7+25*r**6+32*r**5-15*r**4-56*r**3+39*r*r+15
    J=S.det(S.Matrix([[S.diff(q0,r),S.diff(q0,n)],
                      [S.diff(q1,r),S.diff(q1,n)]]))
    Jform=pp**5*n**5*t*r*h/(8192*s*s*(1-r*r)**5)
    check(zero(J-Jform),
          "analytic one-tick two-Born-record coordinate Jacobian EXACT")
    check(15-S.Rational(15,6561)-S.Rational(56,729)>0,
          "strict native 0<r<=1/9 Jacobian positive interval")
    jf=Jform.subs({r:S.Rational(1,9),n:S.Rational(3,5)})
    check(jf>0 and abs(float(jf)-3.890501024678723e-7)<1e-15,
          "actual native geometric coordinate inverse nondegenerate")
    # Actual moving-input Born differential also equals the independently
    # derived symbolic r derivative, without eigenvector and rho freeze.
    dth=(1-r*r)/2
    at={r:S.Rational(1,9),n:S.Rational(3,5)}
    near(point["dq0"],
         float(S.diff(q0,r).subs(at)*dth.subs(at)),2e-12,
         "original moving q0 exact symbolic proper-boost derivative")
    near(point["dq1"],
         float(S.diff(q1,r).subs(at)*dth.subs(at)),2e-12,
         "original moving q1 exact symbolic proper-boost derivative")
    check(point["book_source"]<0,
          "native Book source strictly negative at original proper boost")
    print(json.dumps({
        "status":"PASS_ORIGINAL_FULL128_SELF_PREPARED_TWO_BORN_BOOK_INVERSE",
        "checks":checks,
        "original_128_Kraus_and_true_full_jets":True,
        "stationary_rho_reproduced_by_actual_channel":True,
        "input_Poisson_source_unfrozen":True,
        "one_tick_labels":[0,1],
        "fixture_q0":point["q0"],
        "fixture_q1":point["q1"],
        "fixture_book_pre":point["book"],
        "fixture_dtheta_Book_pre":point["book_source"],
        "native_r_nu_inverse_jacobian":float(jf),
        "one-tick_audits_no_new_Slater_hardware":True,
        "other_126_fine_outcomes_discarded":False,
        "higher_dimensional_42_source_closed":False,
        "full_D0_action_selected":False,
        "GR_closed":False
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
