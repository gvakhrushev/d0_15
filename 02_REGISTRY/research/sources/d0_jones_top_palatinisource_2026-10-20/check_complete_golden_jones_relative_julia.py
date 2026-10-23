#!/usr/bin/env python3
"""Exact Jones opposite-history CAR16 Golden Julia source, with genuine numeric
GOOD+BAD square-root completion. Scope: constructed original-carrier mathematics.
"""
import numpy as np
import sympy as s
from check_car16_jones_reference_top_source import (
    p,a,E,eta,pairs,Ix,G2,STAR,basis,wedge,v0,omega,psi_plus,psi_minus
)
for ij in pairs:
    B=E(*ij)-E(ij[1],ij[0])
    for F in basis:
        L=(s.eye(6)[:,Ix[ij]].T*G2*STAR*
           s.Matrix([(F*eta)[i,j] for i,j in pairs]))[0]
        N=wedge(B)*wedge(F*eta)
        # Native Golden mathematical Julia:
        # T_s=p(I+sN), BAD=sqrt(I-T_s^*T_s), V_s^*V_s=I
        # V_0^* dV_0=(p^2/2)(N-N^*) with BAD included.
        signed=(psi_plus.T*(N-N.T)*psi_minus)[0]
        flipped=(psi_minus.T*(N-N.T)*psi_plus)[0]
        full=s.simplify(p**2*(signed-flipped)/(2*p**3*a))
        assert s.simplify(full-L)==0
print("PASS all36 full GOOD+BAD native-p Julia signed opposite Jones source")
# Unlike relative-arm comparisons, common isometry preserves Jones overlap p^3.
pn=float(s.N(p,20));an=float(s.N(a,20))
plus=np.array(psi_plus,dtype=float).reshape(16)
minus=np.array(psi_minus,dtype=float).reshape(16)
F=basis[-1]
B=E(0,1)-E(1,0)
N=np.array(wedge(B)*wedge(F*eta),dtype=float)
assert np.linalg.norm(N+np.outer(np.array(omega,dtype=float).reshape(16),
                                 np.array(v0,dtype=float).reshape(16)))<1e-12
def fullV(t):
    T=pn*(np.eye(16)+t*N)
    D=np.eye(16)-T.T@T
    vals,U=np.linalg.eigh(D)
    assert vals.min()>0
    FAIL=(U*np.sqrt(vals))@U.T
    V=np.vstack([T,FAIL])
    assert np.linalg.norm(V.T@V-np.eye(16))<1e-13
    return V
baseline=fullV(0.)
for t in (.01,.002,.0004):
    V=fullV(t)
    zpm=float((baseline@plus)@(V@minus))
    zmp=float((baseline@minus)@(V@plus))
    val=np.log(zpm/zmp)/(an*t)
    assert abs(val-1)<.01,(t,val)
    assert abs(float((V@plus)@(V@minus))-pn**3)<1e-13
    print("FULL_JULIA_TEST",t, val)
# In the actual unpolarized full16 first-shell state, the top-created source
# is invisible: it NEEDS an admitted Jones memory/reference.
assert abs(np.trace(N)/16)<1e-14
print("PASS complete 32-outcome Julia, common-isometry zero source, unpolarized rho=I16/16 no top signal")
print("GR_closed=false; native full128 physical Jones reference/Cost source unproved")
