#!/usr/bin/env python3
"""Numerical evaluator for the typed L4 fixed-PF/collar chart derivative.

Each site point supplies the actual B21 native inverse-leg u[component,role]
and A53 left exponential coordinates theta[role,generator], in B21 order.
The caller must bind these arrays to the SAME validated field Request:
u=computable B21 base u + its coframe offsets; theta=its link offsets.
Sampled CODE digits are added only when evaluating SOURCE corners. This
module neither reads Request nor promotes the approximate-centre JSONL to
an exact production source.
The physical link tangent is left-trivialized in the J2 null frame:
  dU_J U_J^-1 = sum_ab w_J[ab] eta_N(E_ab-E_ba).
This module is floating-point evaluation of the exact formulas in B114, NOT
an interval certificate, a source of the point, or a chosen V_h norm.
"""
from itertools import combinations
import numpy as np
from scipy.linalg import expm,expm_frechet

NU=3/5
ETA=np.array([[0.,1.,0.,0.],[1.,0.,0.,0.],[0.,0.,-1.,0.],[0.,0.,0.,-1.]])
S=np.diag([1.,1.,-1.,-1.])
PAIRS=tuple(combinations(range(4),2))
SIGNS=np.array([1.,-1.,-1.,-1.,-1.,1.])
A=NU*ETA@S
GEN=[]
for i,j in PAIRS:
    anti=np.zeros((4,4));anti[i,j]=1;anti[j,i]=-1;GEN.append(ETA@anti)
GEN=np.array(GEN)

def _point(u,theta):
    u=np.asarray(u,dtype=float);theta=np.asarray(theta,dtype=float)
    if u.shape!=(4,4) or theta.shape!=(4,6):raise ValueError('u=(4,4), theta=(4,6)')
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(theta)):raise ValueError('finite inputs required')
    singular=np.linalg.svd(u,compute_uv=False)
    if singular[-1]<=.5 or singular[0]>=2/3:raise ValueError('outside certified coframe collar')
    if np.max(np.abs(theta))>=2**-32+3*2**-80:raise ValueError('outside declared sampled theta chart')
    E=A.T@np.linalg.inv(u).T
    return u,theta,E

def _link_jac(theta):
    Theta=np.tensordot(theta,GEN,axes=(0,0))
    Uinv=expm(-Theta)
    out=np.zeros((6,6))
    for j,G in enumerate(GEN):
        tangent=expm_frechet(Theta,G,compute_expm=False)@Uinv
        out[:,j]=[np.sum(H*tangent)/2 for H in GEN]
    return out

def iota_site(u,theta,dE,wJ,dpsi):
    """42 B21 raw coordinates from one (dE,wJ,dpsi) tangent.

    Shapes: u,dE=(4,4), theta,wJ=(4,6), dpsi=(2,). wJ is actual
    left-trivialized *link* variation, not an unintegrated connection.
    """
    u,theta,E=_point(u,theta);dE=np.asarray(dE,float);wJ=np.asarray(wJ,float);dpsi=np.asarray(dpsi,float)
    if dE.shape!=(4,4) or wJ.shape!=(4,6) or dpsi.shape!=(2,):raise ValueError('invalid tangent shape')
    if not all(np.all(np.isfinite(x)) for x in (dE,wJ,dpsi)):raise ValueError('finite tangent required')
    du=-u@dE.T@np.linalg.inv(E).T
    dt=np.array([np.linalg.solve(_link_jac(theta[r]),SIGNS*wJ[r]) for r in range(4)])
    return np.concatenate((du.T.reshape(16),dt.reshape(24),dpsi))

def inverse_site(u,theta,raw):
    """Invert the same finite local Jacobian to (dE,wJ,dpsi)."""
    u,theta,E=_point(u,theta);raw=np.asarray(raw,float)
    if raw.shape!=(42,):raise ValueError('42 raw values required')
    if not np.all(np.isfinite(raw)):raise ValueError('finite raw tangent required')
    du=raw[:16].reshape(4,4).T
    dE=-E@du.T@np.linalg.inv(u).T
    dt=raw[16:40].reshape(4,6)
    wJ=np.array([SIGNS*(_link_jac(theta[r])@dt[r]) for r in range(4)])
    return dE,wJ,raw[40:].copy()

def pullback_site(u,theta,raw_covector):
    """Transpose action for Frobenius dE / Euclidean wJ and psi pairing.

    This is an evaluator of the covector pairing only; it does not assert
    that either numerical norm equals the original physical V_h norm.
    """
    u,theta,E=_point(u,theta);raw_covector=np.asarray(raw_covector,float)
    if raw_covector.shape!=(42,):raise ValueError('42 raw covector values required')
    if not np.all(np.isfinite(raw_covector)):raise ValueError('finite covector required')
    R=raw_covector[:16].reshape(4,4).T
    gradE=-np.linalg.inv(E).T@R.T@u
    rtheta=raw_covector[16:40].reshape(4,6)
    gradW=np.array([SIGNS*np.linalg.solve(_link_jac(theta[r]).T,rtheta[r]) for r in range(4)])
    return gradE,gradW,raw_covector[40:].copy()

def iota_l4(u,theta,dE,wJ,dpsi):
    """Stack 64 sites in B21 u,v,x,y order to exactly 2688 coordinates."""
    if len(u)!=64 or len(theta)!=64 or len(dE)!=64 or len(wJ)!=64 or len(dpsi)!=64:
        raise ValueError('exactly 64 interior sites required')
    return np.concatenate([iota_site(u[i],theta[i],dE[i],wJ[i],dpsi[i]) for i in range(64)])

def pullback_l4(u,theta,raw_covector):
    """Return 64 triples of cotangents in the same interior site order."""
    if len(u)!=64 or len(theta)!=64:raise ValueError('exactly 64 interior sites required')
    raw_covector=np.asarray(raw_covector,float)
    if raw_covector.shape!=(2688,):raise ValueError('2688 raw covector values required')
    return [pullback_site(u[i],theta[i],raw_covector[42*i:42*(i+1)]) for i in range(64)]
