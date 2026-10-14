#!/usr/bin/env python3
"""Independent floating-point Frechet checks; these are diagnostics, not intervals."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, expm


def partial(A, nr, na):
    return np.einsum('iaja->ij',A.reshape(nr,na,nr,na))


def logm_pos(A):
    e,Q=eigh(A)
    if min(e)<=0:raise AssertionError('POSITIVE_LOG_DOMAIN')
    return (Q*np.log(e))@Q.conj().T


def dlog(A,B):
    e,Q=eigh(A);inside=Q.conj().T@B@Q
    F=np.empty((len(e),len(e)))
    for i,x in enumerate(e):
        for j,y in enumerate(e):
            F[i,j]=1/x if abs(x-y)<1e-12*max(1,abs(x),abs(y)) else (np.log(x)-np.log(y))/(x-y)
    return Q@(F*inside)@Q.conj().T


def kubo(L,B,beta):
    e,Q=eigh(L);inside=Q.conj().T@B@Q;v=np.exp(-beta*e)
    F=np.empty((len(e),len(e)))
    for i,x in enumerate(e):
        for j,y in enumerate(e):
            F[i,j]=v[i] if abs(x-y)<1e-12 else (v[i]-v[j])/(beta*(y-x))
    return Q@(F*inside)@Q.conj().T


def controls():
    rng=np.random.default_rng(20261014);rows=[]
    for nr,na in ((2,2),(2,3),(3,2)):
        n=nr*na;beta=.7
        def herm():
            X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
            return (X+X.conj().T)/(2*n)
        A=herm();L=A@A+np.eye(n)/3;V=herm();G=herm()
        B=herm();rho=B@B;rho/=np.trace(rho)
        drho=-1j*(G@rho-rho@G)
        W=expm(-beta*L);M=partial(W,nr,na);K=-logm_pos(M)/beta
        Z=np.trace(W);tau=W/Z;rr=partial(rho,nr,na);tr=partial(tau,nr,na)
        DK=dlog(M,partial(kubo(L,V,beta),nr,na))
        TA=kubo(L,np.kron(dlog(M,rr),np.eye(na)),beta)
        full=(np.trace((rho-tau)@V)+np.trace(drho@L)).real
        reduced=(np.trace((rr-tr)@DK)+np.trace(partial(drho,nr,na)@K)).real
        remainder=(np.trace(drho@(L-np.kron(K,np.eye(na))))+np.trace((rho-TA)@V)).real
        identity_error=abs(full-reduced-remainder)
        fd_errors=[];k_errors=[]
        for h in (1e-4,2e-5,4e-6):
            vals=[];ks=[]
            for sign in (-1,1):
                t=sign*h;Lt=L+t*V;U=expm(-1j*t*G);rt=U@rho@U.conj().T
                Wt=expm(-beta*Lt);Kt=-logm_pos(partial(Wt,nr,na))/beta
                vals.append((np.trace(rt@(Lt-np.kron(Kt,np.eye(na))))).real);ks.append(Kt)
            fd_errors.append(abs((vals[1]-vals[0])/(2*h)-remainder))
            k_errors.append(float(np.linalg.norm((ks[1]-ks[0])/(2*h)-DK,2)))
        thermal_error=float(np.linalg.norm(kubo(L,np.kron(dlog(M,tr),np.eye(na)),beta)-tau,2))
        scalar_error=float(np.linalg.norm(dlog(M,partial(kubo(L,np.eye(n),beta),nr,na))-np.eye(nr),2))
        if max(identity_error,thermal_error,scalar_error)>1e-10 or min(fd_errors)>1e-7 or min(k_errors)>1e-7:
            raise AssertionError(('FRECHET_NUMERICAL_CHECK',nr,na,identity_error,fd_errors,k_errors))
        rows.append({'retained_dimension':nr,'archive_dimension':na,'source_identity_error':identity_error,
                     'thermal_identity_error':thermal_error,'scalar_shift_error':scalar_error,
                     'finite_difference_remainder_errors':fd_errors,'finite_difference_operator_errors':k_errors})
    return {'status':'PASS','scope':'FLOATING_POINT_DIAGNOSTICS_NOT_INTERVAL_OR_UNIVERSAL_PROOF','rows':rows}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    obj=controls()
    if args.output:args.output.write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(obj,indent=2))
if __name__=='__main__':main()
