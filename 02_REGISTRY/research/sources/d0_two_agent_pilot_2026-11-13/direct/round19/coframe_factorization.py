#!/usr/bin/env python3
"""Small ideal factors of the ORIGINAL coframe Julia matrix on all 32 columns.

Numerical routines here diagnose the exact algebraic factorization; they are
not native angle certificates or a replacement for the physical source.
"""
from itertools import product
import numpy as np
mm=lambda a,b:np.einsum('ij,jk->ik',a,b,optimize=False)
ORDER=(0,2,3,1)
def plane(dim,a,b,c,s):
    out=np.eye(dim);out[a,a]=out[b,b]=c;out[b,a]=s;out[a,b]=-s;return out
def fock_pairs(j):
    assert j in (1,2,3)
    rest=[i for i in range(4) if i not in (0,j)]
    between=ORDER[1:ORDER.index(j)]
    for pattern in product((0,1),repeat=2):
        spectator=sum(b<<i for b,i in zip(pattern,rest))
        sign=(-1)**sum((spectator>>i)&1 for i in between)
        yield spectator|1,spectator|(1<<j),sign
def fock_plane(j,c,s):
    out=np.eye(16)
    for a,b,sign in fock_pairs(j):out=mm(plane(16,a,b,c,sign*s),out)
    return out
def mode_alignment(v):
    v=np.asarray(v,dtype=float);assert v.shape==(4,);n=float(np.linalg.norm(v));assert 0<n<1
    # Start with the dominant component, so every nontrivial denominator is
    # at least n/2. An interval compiler must certify its chosen order.
    dominant=int(np.argmax(np.abs(v)));first=dominant if dominant else 1
    order=[first]+[j for j in (1,2,3) if j!=first];cur=v.copy();elim=[]
    for j in order:
        radius=float(np.hypot(cur[0],cur[j]));assert radius>=n/2-1e-15
        c,s=float(cur[0]/radius),float(cur[j]/radius)
        elim.append((j,c,s));cur[0]=radius;cur[j]=0
    return n,list(reversed(elim))
def base_julia(n):
    # Chronology: X on Julia flag t, then the pair (t,q0)=01,10 with
    # cos=sqrt(1-n²), sin=-n. All other occupation wires are spectators.
    X=np.zeros((32,32))
    for x in range(32):X[x^16,x]=1
    R=np.eye(32);c=float(np.sqrt(1-n*n))
    for rest in range(0,16,2):
        a=rest|1;b=rest|16;R[a,a]=R[b,b]=c;R[b,a]=-n;R[a,b]=n
    return mm(R,X)
def compiled_target(v):
    n,rots=mode_alignment(v);F=np.eye(16);V=np.eye(4)
    for j,c,s in rots:F=mm(fock_plane(j,c,s),F);V=mm(plane(4,0,j,c,s),V)
    W=np.zeros((32,32));W[:16,:16]=F;W[16:,16:]=F
    return mm(mm(W,base_julia(n)),W.T),V,F,rots
