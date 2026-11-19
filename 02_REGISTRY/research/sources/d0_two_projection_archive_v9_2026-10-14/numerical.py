#!/usr/bin/env python3
"""Independent full-space floating-point controls. NOT interval certificates."""
from __future__ import annotations
import json
import itertools
import numpy as np
from scipy.linalg import expm, eigh
p=(np.sqrt(5)-1)/2;a=np.sqrt(p);kap=1/256;alpha=2*p*p*kap;n=2;beta=2*n*alpha;z=.13
G=np.array([[a,-p],[p,a]]);Had=np.array([[1,1],[1,-1]])/np.sqrt(2)
CH=np.eye(4);CH[2:,2:]=Had;prep=CH@np.kron(G,np.eye(2))
d=2;m=6;PP=np.diag([1,1,0,0,0,0]);Id=np.eye(m)
D0=np.array([[.8,.13],[.13,1.3]]);Ddot=np.array([[.2,-.17],[-.17,-.07]])
T=np.zeros((6,6));T[2,5]=.37;T[5,2]=-.37;T[3,4]=.23;T[4,3]=-.23

def one(t, move_frame=True, moving_matter=False):
    D=D0+t*Ddot;Delta=D@D;A=D/16
    v,W=eigh(np.eye(2)-A@A);C=(W*np.sqrt(v))@W.T
    Q=np.eye(6);Q[:4,:4]=np.block([[A,C],[C,-A]])
    O=expm(t*T) if move_frame else np.eye(6);Q=O@Q@O.T
    R=Q.T@PP@Q;S=PP+R-Id;K=S@S;fullDelta=K/kap
    V=-(2*PP-Id)@(2*R-Id)
    B=p*Id+p*p*(V+V.T)/2
    select=np.zeros((24,24))
    for j,Vj in enumerate([Id,Id,V,V.T]):select[j*m:(j+1)*m,j*m:(j+1)*m]=Vj
    E=np.kron(prep,Id);Wfull=E.T@select@E
    # record0, record1, full physical workspace. All 96 basis states.
    U0=np.zeros((96,96));U1=np.zeros((96,96))
    for r0,r1,x in itertools.product(range(4),range(4),range(m)):
        j=(4*r0+r1)*m+x
        for out in range(4):
            U0[(4*out+r1)*m:(4*out+r1+1)*m,j]=Wfull[out*m:(out+1)*m,r0*m+x]
            U1[(4*r0+out)*m:(4*r0+out+1)*m,j]=Wfull[out*m:(out+1)*m,r1*m+x]
    U=U1@U0;P=np.zeros((96,96));P[:2,:2]=np.eye(2)
    F=P@U.T@(np.eye(96)-P)@U@P
    Ldelta=np.kron(np.eye(16),fullDelta)
    if moving_matter:psi=np.array([np.cos(.31+.27*t),np.sin(.31+.27*t)])
    else:psi=eigh(Delta)[1][:,0]
    incoming=np.zeros(96);incoming[:2]=psi;out=U@incoming
    eB=eigh(B)[0]
    H=np.log(16*np.sum(eB**(2*n)))/beta
    sign,logdet=np.linalg.slogdet(np.eye(96)-z*F)
    if sign<=0:raise AssertionError('LOGDET_DOMAIN')
    Rcost=out@Ldelta@out
    return H-logdet+Rcost,{
        'unitarity_error':float(np.linalg.norm(U.T@U-np.eye(96),ord=2)),
        'energy_commutator_error':float(np.linalg.norm(U@Ldelta-Ldelta@U,ord=2)),
        'matter_reading_error':float(abs(Rcost-psi@Delta@psi)),
        'compression_error':float(np.linalg.norm(U[:2,:2]-np.linalg.matrix_power(np.eye(2)-alpha*Delta,n))),
        'rho':np.outer(psi,psi)}

def run():
    X=Ddot@D0+D0@Ddot;Delta=D0@D0;B=np.eye(2)-alpha*Delta
    eB,ev=eigh(B);f=eB**(2*n);Z=f.sum();gamma=p**(6*n)
    kernel=(ev*(-f/eB/(Z+gamma)+beta*z*f/(eB*(1-z+z*f))))@ev.T
    results=[]
    for moving_matter in (False,True):
        s0,info=one(0,moving_matter=moving_matter)
        h=2e-5;plus,_=one(h,moving_matter=moving_matter);minus,_=one(-h,moving_matter=moving_matter)
        deriv=(plus-minus)/(2*h)
        formula=float(np.trace((info.pop('rho')+kernel)@X))
        if moving_matter:
            psi=np.array([np.cos(.31),np.sin(.31)]);dp=.27*np.array([-np.sin(.31),np.cos(.31)])
            formula+=float(2*dp@Delta@psi)
        difference=abs(deriv-formula)
        if difference>3e-7:raise AssertionError(('FULL_FRECHET',deriv,formula,difference))
        if max(info.values())>1e-10:raise AssertionError(info)
        # independent moving completion must not change any full price
        alt,_=one(h,move_frame=False,moving_matter=moving_matter)
        if abs(alt-plus)>1e-10:raise AssertionError('COMPLETION_SOURCE_INVARIANCE')
        results.append({'moving_matter':moving_matter,**info,'finite_difference':float(deriv),
                        'analytic_trace_formula':formula,'error':difference})
    return {'status':'PASS','scope':'FLOATING_POINT_DIAGNOSTIC_NOT_INTERVAL_PROOF',
            'dimension_complete_program':96,'tests':results}
if __name__=='__main__':print(json.dumps(run(),indent=2))
