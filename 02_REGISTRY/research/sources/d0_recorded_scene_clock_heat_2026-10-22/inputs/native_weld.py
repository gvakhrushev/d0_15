"""Faithful Julia/Walsh projector dilation of the pinned full128 column.

These are finite operator identities on the original register inventory.
No new selected physical Book action or autonomous gate admission is assumed.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm, solve_sylvester, hadamard
from native_excerpt import P, EYE, adj, root, creators


def julia(x: np.ndarray, dx: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    left, right = root(EYE-x@adj(x)), root(EYE-adj(x)@x)
    dl = solve_sylvester(left,left,-dx@adj(x)-x@adj(dx))
    dr = solve_sylvester(right,right,-adj(dx)@x-adj(x)@dx)
    return (np.block([[x,left],[right,-adj(x)]]),
            np.block([[dx,dl],[dr,-adj(dx)]]))


def build(theta: float, nu: float=0.6,
          phases: tuple[complex,...]=(1j,1j,-1.0,-1j)) -> dict:
    """Full 1024-square W, and original native rapidity derivative.

    The output convention is j=2*Walsh_label+Julia_work_bit;
    actual fine labels are alpha=2*j+Golden_port.
    """
    cs=creators(); G=cs[0]@adj(cs[1])+cs[1]@adj(cs[0])
    u=expm(theta*G);du=u@G;zero=np.zeros_like(EYE)
    blocks=[];dblocks=[]
    for r,c in enumerate(cs):
        base=nu*c
        x=base@(u if r==1 else EYE)*phases[r]
        dx=base@du*phases[r] if r==1 else zero
        j,dj=julia(x,dx);j0,dj0=julia(base,zero)
        for a,b in [(j,dj),(adj(j),adj(dj)),(-j0,-dj0),(-adj(j0),-adj(dj0))]:
            blocks.extend((a,a));dblocks.extend((b,b))
    H=hadamard(32)/np.sqrt(32.0)
    W=np.einsum('lk,kab,kr->larb',H,np.array(blocks),H,optimize=True).reshape(1024,1024)
    dW=np.einsum('lk,kab,kr->larb',H,np.array(dblocks),H,optimize=True).reshape(1024,1024)
    N=W[:16,:];dN=dW[:16,:];A=N[:,:16];dA=dN[:,:16]
    D=adj(A)@A;dD=adj(dA)@A+adj(A)@dA
    Q=adj(N)@N;dQ=adj(dN)@N+adj(N)@dN
    JJ=np.eye(1024,dtype=complex)[:,:16]
    c0=JJ-2*P**2*(Q@JJ);c1=-2*P*np.sqrt(P)*(Q@JJ)
    dc0=-2*P**2*dQ@JJ;dc1=-2*P*np.sqrt(P)*dQ@JJ
    K=np.empty((128,16,16),complex);dK=np.empty_like(K)
    K[::2]=c0.reshape(64,16,16);K[1::2]=c1.reshape(64,16,16)
    dK[::2]=dc0.reshape(64,16,16);dK[1::2]=dc1.reshape(64,16,16)
    Zc=np.repeat(np.array([1 if (j&2)==0 else -1 for j in range(32)]),32)
    return dict(W=W,dW=dW,N=N,dN=dN,A=A,dA=dA,D=D,dD=dD,
                Q=Q,dQ=dQ,K=K,dK=dK,J=JJ,Zc=Zc,
                blocks=np.array(blocks),dblocks=np.array(dblocks))


def native_feedback(D: np.ndarray, dD: np.ndarray, *, right_rank: int=128,
                    clock_stages: int=1, beta: float=2*P**2, zeta: float=2**-20) -> dict:
    """Initialized-cut J and paired-cut heat, not compulsory scene heat.

    With one covariantly transported return mismatch per stage cycle,
    ambient dimension=2048*clock_stages; exact zero-Hodge multiplicity=dim-32.
    Retained right is an unchanged identity tensor in both operators.
    """
    if right_rank<1 or clock_stages<1:raise ValueError('positive register ranks required')
    f=4*P**2*(D-P**2*D@D)
    df=4*P**2*(dD-P**2*(dD@D+D@dD))
    e=np.linalg.eigvalsh(f)
    if e.min()<=0 or e.max()>=1:raise ValueError('requires 0<F<1')
    inv=np.linalg.inv(EYE-zeta*f);thermal=expm(-beta*f)
    zeros=2048*clock_stages-32
    Zbase=zeros+2*np.trace(thermal).real
    J=-right_rank*np.log1p(-zeta*e).sum()
    dJ=right_rank*zeta*np.trace(inv@df).real
    H=np.log(right_rank*Zbase)/beta
    dH=-2*np.trace(thermal@df).real/Zbase
    source=4*P**2*right_rank*zeta*inv@(EYE-2*P**2*D)
    return dict(J=float(J),dJ=float(dJ),H_cut=float(H),dH_cut=float(dH),
                dH_plus_J=float(dH+dJ),zeros=zeros,Zbase=float(Zbase),
                source_D=source,F=f,dF=df,eigen_F=e)
