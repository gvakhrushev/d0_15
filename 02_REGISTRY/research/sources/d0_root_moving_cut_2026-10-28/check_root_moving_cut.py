#!/usr/bin/env python3
"""Full finite Book03 first-source identity, with a genuinely moving projector.
Structural matrix controls; NOT a native field writer or a GR proof.
"""
from __future__ import annotations
import json
import numpy as np
from scipy.linalg import expm


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ArithmeticError(message)


def comm(a, b):
    return a @ b-b @ a


def close(a, b, name, tol=2e-9):
    error=float(np.linalg.norm(np.asarray(a)-np.asarray(b)))
    scale=max(1.0,float(np.linalg.norm(np.asarray(a))),float(np.linalg.norm(np.asarray(b))))
    require(error<=tol*scale, f'{name}: {error:.5g}')
    return error


def value(U, P, Delta, beta, z):
    Q=np.eye(len(P))-P
    C=Q@U@P
    F=C.conj().T@C
    heat=np.log(np.trace(expm(-beta*Delta)).real)/beta
    eig=np.linalg.eigvalsh(np.eye(len(P))-z*F)
    require(eig.min()>0,'Feedback resolvent must be positive')
    return float(heat-np.log(eig).sum())


def first_source(U,P,Delta,dU,dP,dDelta,beta,z):
    I=np.eye(len(P));Q=I-P
    C=Q@U@P;F=C.conj().T@C
    R=np.linalg.inv(I-z*F)
    rho=expm(-beta*Delta);rho/=np.trace(rho)
    dC=-dP@U@P+Q@dU@P+Q@U@dP
    dF=dC.conj().T@C+C.conj().T@dC
    direct=(-np.trace(rho@dDelta)+z*np.trace(R@dF)).real
    K=comm(dP,P)
    relativeU=dU-comm(K,U)
    relativeDelta=dDelta-comm(K,Delta)
    relative=(-np.trace(rho@relativeDelta)
              +2*z*np.trace(R@C.conj().T@Q@relativeU@P).real).real
    tangent_error=close(comm(K,P),dP,'Exact tangent lift')
    covariance_error=close(dC-comm(K,C),Q@relativeU@P,'Covariant off-block derivative')
    close(direct,relative,'Full source and covariant source')
    bound=(np.linalg.norm(relativeDelta,2)
           +2*z*np.linalg.norm(C@R,'fro')*np.linalg.norm(Q@relativeU@P,'fro'))
    require(abs(relative)<=bound+1e-10,'Source estimate')
    return float(direct),float(relative),float(bound),tangent_error,covariance_error


def fd5(f,step=2e-4):
    return (-f(2*step)+8*f(step)-8*f(-step)+f(-2*step))/(12*step)


def main():
    rng=np.random.default_rng(20261028)
    def herm(n):
        X=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
        return (X+X.conj().T)/(2*np.sqrt(n))
    errors=[];coverrors=[];gauges=[];rows=[]
    for n in (3,4,6,8):
        rank=n//2;P0=np.diag([1]*rank+[0]*(n-rank)).astype(complex)
        U0=expm(1j*herm(n))
        H=herm(n);D0=H@H+np.eye(n)
        W=1j*herm(n);X=1j*herm(n);dD=herm(n)/5
        beta=.7;z=.23
        dP=comm(W,P0);dU=comm(W,U0)+X@U0;dDelta=comm(W,D0)+dD
        src,rel,bound,err1,err2=first_source(U0,P0,D0,dU,dP,dDelta,beta,z)
        def curve(t):
            V=expm(t*W)
            return value(V@expm(t*X)@U0@V.conj().T,
                         V@P0@V.conj().T,V@(D0+t*dD)@V.conj().T,beta,z)
        fd=fd5(curve);errors.append(close(src,fd,'Five-point total derivative'))
        coverrors.extend([err1,err2])
        g=first_source(U0,P0,D0,comm(W,U0),dP,comm(W,D0),beta,z)[0]
        close(g,0,'Simultaneous internal re-encoding has zero source');gauges.append(abs(g))
        # A different generator for the same dP differs by block diagonal L.
        K=comm(dP,P0);L=1j*(P0@herm(n)@P0+(np.eye(n)-P0)@herm(n)@(np.eye(n)-P0))
        K2=K+L;Q=np.eye(n)-P0;C=Q@U0@P0
        R=np.linalg.inv(np.eye(n)-z*C.conj().T@C)
        rho=expm(-beta*D0);rho/=np.trace(rho)
        alt=(-np.trace(rho@(dDelta-comm(K2,D0)))
             +2*z*np.trace(R@C.conj().T@Q@(dU-comm(K2,U0))@P0).real).real
        close(alt,src,'No arbitrary block-diagonal connection choice')
        rows.append({'dimension':n,'rank':rank,'source':src,'finite_difference':fd,'bound':bound})
    # Move only the active split: its source must NOT be silently set to zero.
    theta=.31;phi=.83;z=.2;beta=.7
    U=np.diag([1,np.exp(1j*phi)]);D=np.diag([.2,.9])
    def proj(t):
        v=np.array([np.cos(t),np.sin(t)]);return np.outer(v,v)
    v=np.array([np.cos(theta),np.sin(theta)])
    dv=np.array([-np.sin(theta),np.cos(theta)])
    dP=np.outer(dv,v)+np.outer(v,dv)
    zero=np.zeros((2,2),complex)
    src=first_source(U,proj(theta),D,zero,dP,zero,beta,z)[0]
    f=np.sin(2*theta)**2*np.sin(phi/2)**2
    exact=2*z*np.sin(4*theta)*np.sin(phi/2)**2/(1-z*f)
    close(src,exact,'Analytical moving-cut source')
    close(src,fd5(lambda t:value(U,proj(theta+t),D,beta,z)),'Moving-cut finite difference')
    require(abs(src)>.01,'Control must have nonzero physical relative response')
    # Golden splitter at its declared base: scalar feedback is retained.
    p=(np.sqrt(5)-1)/2
    G=np.array([[np.sqrt(p),-p],[p,np.sqrt(p)]])
    P=np.diag([1.,0.]);Q=np.eye(2)-P
    close(P@G.T@Q@G@P,p*p*P,'Original Golden base feedback')
    out={'status':'PASS_FULL_BOOTSTRAP_MOVING_CUT',
         'source_owner':'Book03 section 03.25; F=P U^* (I-P) U P',
         'scope':'Fixed rank, beta and z; finite structural matrix controls, not native field realization',
         'random_seed':20261028,'samples':rows,
         'max_fd_error':max(errors),'max_covariance_identity_error':max(coverrors),
         'max_pure_reencoding_source':max(gauges),
         'moving_cut_control_source':float(src),
         'projector_frozen_incorrect_control_source':0.0,
         'native_full42_replayed':False,'lean_or_ci_run':False,'GR_closed':False}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
