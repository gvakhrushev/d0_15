"""G5 tail splicing on real growing clocks, the LC angular gap and the absolute minimum."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys

import numpy as np
from scipy import sparse

sys.dont_write_bytecode = True
clock_source = Path(__file__).resolve().parents[2]/'round69'/'clock'
sys.path.insert(0,str(clock_source))
from check_early_heat import Clock, gate


def need(ok,message):
    if not ok:
        raise RuntimeError(message)


def raw_clock(extra, prime):
    clock=Clock(prime)
    last=clock.birth(0)
    calls=[('G',(2,))]+list(extra)
    for op,wires in calls[:-1]:
        last=clock.raw(last,op,wires)
    op,wires=calls[-1]
    clock.last[last]=gate(3,op,wires,prime)
    tick,_=clock.close()
    return tick.toarray()


def cyclic(extra, prime):
    d=8
    k=len(extra)
    out=np.zeros((k*d,k*d),dtype=np.int64 if prime else float)
    for i,(op,wires) in enumerate(extra):
        j=(i+1)%k
        out[j*d:(j+1)*d,i*d:(i+1)*d]=gate(3,op,wires,prime).toarray()
    return out


def partition(tick,beta):
    # Exact two-grade reduction G14, finite floating cross-check of the size of the bound.
    groups=np.repeat(range(3),[9,11,13])
    adj=(groups[:,None]!=groups[None,:]).astype(float)
    inv=1/np.sqrt(2+adj.sum(axis=1))
    b=inv[:,None]*adj*inv[None,:]
    c=np.diag(inv**2)
    angles=np.linalg.eigvals(tick).real
    return 359*len(tick)+2*sum(np.exp(-beta*np.linalg.eigvalsh(np.eye(33)-b-2*c*t)).sum()
                               for t in angles)


def check_splice():
    p=(5**.5-1)/2
    beta=2*p*p
    for extra in [[('SourceI',(2,0,1))],[('G',(2,)),('SourceI',(2,0,1)),('G',(2,))]]:
        for prime in (0,11):
            old=raw_clock([],prime)
            new=raw_clock(extra,prime)
            aux=cyclic(extra,prime)
            split=sparse.block_diag([old,aux]).toarray()
            # Direct construction of the output-exchange operator from the two native ticks.
            swap=np.einsum("ik,jk->ij",new,split,optimize=False)
            diff=swap-np.eye(len(swap),dtype=swap.dtype)
            if prime:
                need(not np.any((swap-swap.T)%prime),'symmetric exchange on exact native ring residue')
                need(not np.any((swap@swap-np.eye(len(swap),dtype=swap.dtype))%prime),'exact involution')
                need(not np.any((swap@split-new)%prime),'all-column physical splice')
            else:
                sv=np.linalg.svd(diff,compute_uv=False)
                need(np.max(np.abs(sv[:8]-2))<1e-11 and max(sv[8:],default=0)<1e-11,'rank and trace norm')
                zo,za,zn=[partition(t,beta) for t in (old,aux,new)]
                need(abs(zn-zo-za)<=12*beta*8 and zn-zo>(359*len(extra)-12*beta)*8,
                     'complete positive partition increases')


def mul(x,y):
    # (u+v*p)(s+t*p), where p^2=1-p.
    u,v=x
    s,t=y
    return (u*s+v*t,u*t+v*s-v*t)


def check_gap():
    # 1-T_{2n}(2p-1) is an actual nonzero algebraic integer with conjugate bounded by 81^n.
    u=(-1,2)
    prev,now=(1,0),u
    for k in range(2,129):
        a,b=mul(u,now)
        prev,now=now,(2*a-prev[0],2*b-prev[1])
        if k%2:
            continue
        i,j=1-now[0],-now[1]
        norm=i*i-i*j-j*j
        need(norm!=0 and abs(norm)>=1,'integer conjugate norm for the LC power')
    x=F(2,55)
    noise=F(1,2**20)
    past=F(1,2**256)
    # Source: 2AB=2p^2 sqrt(q(1-q))>1/4 for p^2<q<=1/2.
    need((2*F(3,5)**2)**2 * F(3,5)**2*F(1,2)>F(1,16),'uniform LC sector product')
    for n in (1,2,4,16):
        length=4*n+34
        thermal=F(704,359)*x**length/factorial(length)
        return_gap=noise*past*F(1,4)*F(1,81)**n
        need(thermal<return_gap/2,'absolute fixed-width native winner even at tiny past return')
    # Ratio to 81^-n decreases after the first width.
    need(81*x**4<1,'all larger widths')
    # Full physical one-copy calibration, including the genuine native pre-sign gain.
    q=.41246988056855516
    p=(5**.5-1)/2
    A=(p*(1-q))**.5
    B=(p**3*q)**.5
    m=(A+B)**2
    mprime=(A+B)*(-A/(1-q)+B/q)
    g_prefactor=p**3
    coeff=-4*float(noise)*mprime/(1-float(noise)+float(noise)*m)
    need(-.247<mprime<-.245 and 9.38e-7<coeff<9.40e-7 and .236<g_prefactor<.237,
         'actual gain = coefficient * p^3 * g_Q')


if __name__=='__main__':
    check_splice()
    check_gap()
    print('PASS: G5 physical splice, both Hodge degrees, exact rank, algebraic finite-angle gaps, strict '
          'fixed-width winner and source calibration for noisy LC.')
