#!/usr/bin/env python3
"""Native Jones +/- reference + full Golden CAR16 GOOD/BAD dephased density product.
36 exact original Palatini source slots plus real full32 Julia numerical checks.
Mathematical readout class only: actual paid full128 Book protocol unproved.
"""
import sympy as s
import numpy as np
from check_car16_jones_reference_top_source import (
    p,a,E,eta,pairs,Ix,G2,STAR,basis,wedge,psi_plus,psi_minus
)
for ij in pairs:
    B=E(*ij)-E(ij[1],ij[0])
    for F in basis:
        L=(s.eye(6)[:,Ix[ij]].T*G2*STAR*
           s.Matrix([(F*eta)[i,j] for i,j in pairs]))[0]
        N=wedge(B)*wedge(F*eta)
        tpm=(psi_plus.T*N*psi_minus)[0]
        tmp=(psi_minus.T*N*psi_plus)[0]
        assert s.simplify((psi_plus.T*(N+N.T)*psi_minus)[0])==0
        assert s.simplify(tpm-a*p*L/2)==0
        assert s.simplify(tmp+a*p*L/2)==0
        qbase=(p**4+p**2)*p**6
        qpmprime=2*(p**2*p**3)*(p**2*tpm)
        qmpprime=2*(p**2*p**3)*(p**2*tmp)
        signed=s.simplify((1+p**2)/(2*a)*(qpmprime-qmpprime)/qbase)
        assert s.simplify(signed-L)==0
print("PASS all36: complete flag-dephased native Golden Jones density-product signed log ratio -> old literal S_star")

pn=float(s.N(p,20));an=float(s.N(a,20))
plus=np.array(psi_plus,dtype=float).reshape(16)
minus=np.array(psi_minus,dtype=float).reshape(16)
B=E(0,1)-E(1,0);F=basis[-1]
N=np.array(wedge(B)*wedge(F*eta),dtype=float)
I=np.eye(16)
def branches(t):
    T=pn*(I+t*N)
    A=I-T.T@T
    eig,U=np.linalg.eigh(A)
    assert eig.min()>0
    BAD=(U*np.sqrt(eig))@U.T
    assert np.linalg.norm(T.T@T+BAD.T@BAD-I)<1e-13
    return T,BAD
def overlap(initial,final,t,parity=False):
    T0,F0=branches(0)
    Tt,Ft=branches(t)
    r0=np.outer(initial,initial);rt=np.outer(final,final)
    if parity:
        Pe=np.diag([float(i.bit_count()%2==0) for i in range(16)])
        Po=I-Pe
        r0=Pe@r0@Pe+Po@r0@Po
        rt=Pe@rt@Pe+Po@rt@Po
    # Both full outcome densities retain their full probability; orthogonal
    # flag mismatches get zero swap-estimator score, NOT conditional renormalization.
    G0=T0@r0@T0.T;B0=F0@r0@F0.T
    Gt=Tt@rt@Tt.T;Bt=Ft@rt@Ft.T
    return float(np.trace(G0@Gt)+np.trace(B0@Bt))
factor=(1+pn**2)/(2*an)
for parity in (False,True):
    q0=overlap(plus,minus,0,parity)
    assert abs(q0-(pn**4+pn**2)*pn**6/(2 if parity else 1))<1e-13
    for t in (0.01,0.002,0.0004):
        qpm=overlap(plus,minus,t,parity)
        qmp=overlap(minus,plus,t,parity)
        assert qpm>0 and qmp>0
        recovery=factor*np.log(qpm/qmp)/t
        assert abs(recovery-1)<.02
        print("dephased_full32",parity,t,"L_star recovered",recovery)
print("PASS full GOOD+BAD and fermionic parity dephasing: signed S_star survives no interhistory phase")
print("FIREWALL: physical original full128 Jones-state prep / complete Book Code−Info price NOT selected; GR_closed=false")
