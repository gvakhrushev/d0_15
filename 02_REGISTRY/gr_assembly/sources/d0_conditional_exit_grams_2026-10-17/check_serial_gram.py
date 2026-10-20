#!/usr/bin/env python3
"""Bounded independent finite-carrier check of conditional-Gram serial source.

Proof of the IR coefficient ratio is analytic (see paired memo); this check does
not claim to evaluate continuum curvature or to certify a native admission gate.
"""
from fractions import Fraction
import numpy as np
from scipy.linalg import expm


def cost(d0, d4, d1, beta=0.4, b=1.0, delta=1.0, z=0.2):
    a = 1.0-z
    u0 = expm(-b*beta*d0/2)
    u1 = expm(-b*beta*d1/2)
    v4 = expm(-delta*beta*d4)
    g0 = a*np.eye(len(d0))+z*u0@u0
    g1 = a*np.eye(len(d0))+z*u1@u1
    k = a*np.eye(len(d0))+z*u1@v4@u0
    _, lk = np.linalg.slogdet(k)
    _, lg0 = np.linalg.slogdet(g0)
    _, lg1 = np.linalg.slogdet(g1)
    return -2*lk+lg0+lg1


def ell_diff(d, h, t=0.4, z=0.2):
    a=1-z
    e=expm(-t*d)
    w=np.linalg.solve(a*np.eye(len(d))+z*e, e)
    return float(-z*t*np.trace(w@h).real)


def check():
    # Full 16 grade dimension; positive common reference and independent
    # noncommuting self-adjoint jets deliberately do not assume simultaneous
    # diagonalization.
    rng=np.random.default_rng(20261017)
    a=rng.normal(size=(16,16)); base=0.5*np.eye(16)+a.T@a/32
    hs=[]
    for _ in range(3):
        q=rng.normal(size=(16,16)); h=(q+q.T)/2
        h/=np.linalg.norm(h)
        hs.append(h)
    beta=.4; b=1.; delta=1.; z=.2; x=b+delta
    s0=cost(base,base,base,beta,b,delta,z)
    errs=[]
    for idx,h in enumerate(hs):
        v=[base.copy(),base.copy(),base.copy()]
        eps=1e-5
        v[idx]=base+eps*h
        plus=cost(v[0],v[1],v[2],beta,b,delta,z)
        v[idx]=base-eps*h
        minus=cost(v[0],v[1],v[2],beta,b,delta,z)
        num=(plus-minus)/(2*eps)
        if idx==1:
            theo=-(2*delta/x)*ell_diff(base,h,x*beta,z)
        else:
            theo=ell_diff(base,h,b*beta,z)-(b/x)*ell_diff(base,h,x*beta,z)
        errs.append(abs(num-theo))
    assert max(errs)<2e-8, errs

    # The normalized comparator is a contraction for any PSD Delta_j, from
    # the explicit raw Gram X_i and the middle contraction V4.
    d0=base+0.1*hs[0]; d4=base+0.1*hs[1]; d1=base+0.1*hs[2]
    a=1-z
    u0=expm(-b*beta*d0/2);u1=expm(-b*beta*d1/2);v4=expm(-delta*beta*d4)
    gi=[a*np.eye(16)+z*u@u for u in (u0,u1)]
    k=a*np.eye(16)+z*u1@v4@u0
    def inv_root(g):
        lam,v=np.linalg.eigh(g)
        return (v/np.sqrt(lam))@v.T
    c=inv_root(gi[1])@k@inv_root(gi[0]);sig=np.linalg.svd(c,compute_uv=False)
    assert np.max(sig)<=1+1e-12 and np.min(sig)>0

    # Shared static curve may accidentally match the TARGET curvature
    # coefficient for b=delta=1, but the separate endpoint and bridge jets
    # have ratios 3/4 : -1/2, NOT target 1 : -1.
    bq=Fraction(1,1);dq=Fraction(1,1);xq=bq+dq
    endpoint=1/bq-bq/(xq*xq)
    bridge=-2*dq/(xq*xq)
    assert endpoint==Fraction(3,4) and bridge==Fraction(-1,2)
    assert 2*endpoint+bridge==Fraction(1,1)
    assert endpoint/(-bridge)==Fraction(3,2)

    # Shorter middle yields a full static curvature coefficient 2/3,
    # hence even a static field-source mismatch.
    dshort=Fraction(1,2); xshort=bq+dshort
    a_short=1/bq-bq/(xshort*xshort)
    c_short=-2*dshort/(xshort*xshort)
    assert a_short==Fraction(5,9)
    assert c_short==Fraction(-4,9)
    assert 2*a_short+c_short==Fraction(2,3)
    print('PASS: noncommuting 16x16 complete source tangent check, max error',max(errs))
    print('PASS: comparator singular values in (0,1], interval',min(sig),max(sig))
    print('PASS: exact IR jet weights b=1,d=1: endpoints=3/4 each, bridge=-1/2; ratio=3/2')
    print('PASS: exact static IR coefficient b=1,d=1/2: 2/3 target')

if __name__=='__main__':
    check()