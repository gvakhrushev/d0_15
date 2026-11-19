"""Normalized incidence heat of K(9,11,13) x an execution cycle.

The base scene is fixed. The same unitary circuit acts on each scene vertex.
This is an explicit connection-incidence realization, NOT an assertion that
Book03 compels this product graph or its active projector. All fine-record
XOR sectors are retained. No independent physical clock cost is assigned.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.special import iv as besseli
sys.path.insert(0, str(Path(__file__).resolve().parent/'inputs'))
from native_excerpt import P, adj
from native_weld import build, native_feedback

SIZES=(9,11,13)
BETA=2*P**2

def scene_matrices():
    groups=np.repeat(np.arange(3),SIZES)
    A=(groups[:,None]!=groups[None,:]).astype(float)
    deg=A.sum(axis=1)+2.0
    W=np.diag(deg**-0.5)
    B=W@A@W;C=np.diag(1.0/deg)
    Q=np.zeros((33,3))
    for j,n in enumerate(SIZES):Q[groups==j,j]=1.0/np.sqrt(n)
    return B,C,Q.T@B@Q,Q.T@C@Q

def scene_symbol(cos_theta: float):
    B,C,_,_=scene_matrices()
    return np.eye(33)-B-2*cos_theta*C

def projected_native(theta: float=np.log(1.25)):
    m=build(theta);N=m['N'].reshape(16,64,16).transpose(1,0,2)
    dN=m['dN'].reshape(16,64,16).transpose(1,0,2)
    gram=N@adj_batch(N);dgram=dN@adj_batch(N)+N@adj_batch(dN)
    chars=np.array([[(-1)**((a&j).bit_count()) for j in range(64)] for a in range(64)])
    rows=np.einsum('aj,jkl->akl',chars,gram)
    drows=np.einsum('aj,jkl->akl',chars,dgram)
    coeff=np.array([1.0,P*P-P])
    blocks=np.stack([c*rows for c in coeff],axis=1).reshape(128,16,16)
    dblocks=np.stack([c*drows for c in coeff],axis=1).reshape(128,16,16)
    return m,blocks,dblocks

def adj_batch(a):return a.conj().transpose(0,2,1)

def recorded_moments(blocks,dblocks,nmax):
    """Exact algebraic recurrence, evaluated in float, not eigenvalue jets.

    Output tr[(C_XOR(U x I_128))^l] and its original rapidity derivative.
    Full holonomy dimension is 2048*128. Two-reflection reduction retains
    128 character sectors, each represented by its true 16x16 compression.
    """
    count,d,_=blocks.shape;ambient=128*d
    vals=[float(ambient*count)];ders=[0.0]
    T0=np.repeat(np.eye(d)[None,:,:],count,axis=0).astype(complex)
    dT0=np.zeros_like(T0);T1=-blocks;dT1=-dblocks
    for ell in range(1,nmax+1):
        if ell>1:
            T2=-2*blocks@T1-T0
            dT2=-2*dblocks@T1-2*blocks@dT1-dT0
            T0,T1=T1,T2;dT0,dT1=dT1,dT2
        base=ambient*count if ell%2==0 else ambient
        val=base-count*d*(1+(-1)**ell)+2*np.trace(T1,axis1=1,axis2=2).sum().real
        der=2*np.trace(dT1,axis1=1,axis2=2).sum().real
        vals.append(float(val));ders.append(float(der))
    return np.array(vals),np.array(ders)

def heat_from_coeffs(coefficients,m,moments,dmoments,beta=BETA):
    """Uses positive Fourier coefficients of the scene heat symbol.

    coefficients[n] = Fourier coefficient of tr exp(beta*(B+2 C cos theta)).
    The finite coefficient/moment truncation error is bounded separately.
    """
    d=moments[0]
    z=d*float(coefficients[0]);dz=0.0
    for ell in range(1,len(moments)):
        n=ell*m
        if n>=len(coefficients):break
        z+=2*float(coefficients[n])*moments[ell]
        dz+=2*float(coefficients[n])*dmoments[ell]
    Z=m*np.exp(-beta)*z
    return float(np.log(Z)/beta),float(dz/(beta*z)),float(Z)

def circuit_laplacian(gates, *, base=True):
    """Direct small-matrix control with genuine transported unitary edges.

    m>=3; gates[t] transports stage t to t+1 mod m. Full K913 product
    is used when base=True, otherwise the degree-two execution cycle.
    """
    m=len(gates);d=gates[0].shape[0]
    if m<3:raise ValueError('cycle length at least 3')
    shift=np.zeros((m*d,m*d),complex)
    for t,g in enumerate(gates):
        shift[((t+1)%m)*d:((t+1)%m+1)*d,t*d:(t+1)*d]=g
    if not base:return np.eye(m*d)-(shift+adj(shift))/2
    B,C,_,_=scene_matrices()
    return np.eye(33*m*d)-np.kron(B,np.eye(m*d))-np.kron(C,shift+adj(shift))

def cycle_trace_from_unitary(V,m,beta=BETA):
    phase=np.angle(np.linalg.eigvals(V))
    angles=(phase[:,None]+2*np.pi*np.arange(m))/m
    return float(np.exp(-beta*(1-np.cos(angles))).sum())
