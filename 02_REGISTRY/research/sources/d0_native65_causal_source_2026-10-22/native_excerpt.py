"""Executable excerpt of the five original native CAR16/full128 functions.
Source: gvakhrushev/d0_15, blob ee8de4635d24c668949ac9a0186616ab7d59f2ed,
check_uniform_book_source.py, functions adj, herm, root, creators, native.
Fetched via GitHub connector on 2026-10-22. This is NOT a full-file checkout.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm, solve_sylvester
P = (np.sqrt(5.0)-1.0)/2.0
EYE = np.eye(16, dtype=complex)
def adj(x: np.ndarray) -> np.ndarray:
    return x.conj().T
def herm(x: np.ndarray) -> np.ndarray:
    return (x+adj(x))/2
def root(x: np.ndarray) -> np.ndarray:
    l,u=np.linalg.eigh(herm(x))
    if l.min()<=0:
        raise ArithmeticError('nonpositive root input')
    return (u*np.sqrt(l))@adj(u)
def creators() -> list[np.ndarray]:
    order=(0,2,3,1)
    out=[]
    for r in range(4):
        c=np.zeros((16,16),complex)
        before=order[:order.index(r)]
        for bits in range(16):
            if not ((bits>>r)&1):
                c[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
        out.append(c)
    return out
def native(theta: float, nu: float=0.6, phases: tuple | None=None) -> tuple[np.ndarray,np.ndarray]:
    """Original Walsh/Julia/Golden128 formulas; derivative is d/dtheta."""
    cs=creators()
    gen=cs[0]@adj(cs[1])+cs[1]@adj(cs[0])
    u=expm(theta*gen); du=u@gen
    words=[]; jets=[]
    if phases is None:
        phases=(1j,1j,-1.0,-1j)
    zero=np.zeros_like(EYE)
    for r,c in enumerate(cs):
        base=nu*c
        x=base@(u if r==1 else EYE)*phases[r]
        dx=base@du*phases[r] if r==1 else zero
        left=root(EYE-x@adj(x)); right=root(EYE-adj(x)@x)
        dl=solve_sylvester(left,left,-dx@adj(x)-x@adj(dx))
        dr=solve_sylvester(right,right,-adj(dx)@x-adj(x)@dx)
        l0=root(EYE-base@adj(base)); r0=root(EYE-adj(base)@base)
        for w,dw in zip(((x,left),(adj(x),right),(-base,-l0),(-adj(base),-r0)),
                        ((dx,dl),(adj(dx),dr),(zero,zero),(zero,zero))):
            words.extend((w,w)); jets.extend((dw,dw))
    rows=[]; drows=[]
    for lab in range(32):
        signs=[(-1)**(bin(lab&j).count('1')&1) for j in range(32)]
        for b in range(2):
            rows.append(sum((signs[j]*words[j][b] for j in range(32)),zero.copy())/32)
            drows.append(sum((signs[j]*jets[j][b] for j in range(32)),zero.copy())/32)
    a,da=rows[0],drows[0]
    k=[]; dk=[]
    for j,nj in enumerate(rows):
        v=adj(nj)@a; dv=adj(drows[j])@a+adj(nj)@da
        k.extend(((EYE if j==0 else zero)-2*P**2*v,-2*P*np.sqrt(P)*v))
        dk.extend((-2*P**2*dv,-2*P*np.sqrt(P)*dv))
    return np.asarray(k),np.asarray(dk)
