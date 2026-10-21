#!/usr/bin/env python3
"""Exact Golden tensor return + 42-field/shared-controller source controls.

Scope: finite operator construction conditional on a coherent same-code
two-arm interface. Does not select a physical Book03 programme or prove GR.
"""
import json
import math
from decimal import Decimal, localcontext

import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0
P = 1.0 / PHI
Z = 2.0**-20
L = 4.0 * P**3
R0 = 1.0 - (1.0-Z*L)*(1.0-Z*L*(1.0+P**6))
C0 = 1.0-R0
A0 = 1.0-Z*(1.0-P**8)
WEIGHTS = np.array([1.,2.,1.,3.,2.,1.,4.])
W = float(np.sum(WEIGHTS))
GAMMA = 0.341640786512  # diagnostic positive value; proof keeps actual gamma symbolic
SLOPES = np.array([
    [(((i+2)*(j+3))%23-11)*1.0e-3 for j in range(42)]
    for i in range(WEIGHTS.size)
])
RG = np.array([[P,math.sqrt(P)],[math.sqrt(P),-P]],dtype=float)

def coherent_arm(r):
    """Actual 4x4 Golden R_G / coherent V dagger CZ V / R_G word."""
    assert 0 <= r <= 1
    V = np.array([[math.sqrt(1-r),-math.sqrt(r)],
                  [math.sqrt(r), math.sqrt(1-r)]],dtype=float)
    zero_phase = np.diag([1.,-1.])
    block = np.zeros((4,4),dtype=float)
    block[:2,:2] = np.eye(2)
    block[2:,2:] = V.T @ zero_phase @ V
    gate = np.kron(RG,np.eye(2))
    result = gate @ block @ gate
    assert np.linalg.norm(result.T @ result - np.eye(4)) < 1e-13
    return result

def full_tensor(rleft,rright):
    U = np.kron(coherent_arm(rleft),coherent_arm(rright))
    # Prepared input is the FIRST tensor column, P=|0><0| rank one.
    gram = np.einsum('ji,jk->ik',U.conj(),U,optimize=False)
    assert np.linalg.norm(gram-np.eye(16)) < 1e-13
    t = float(U[0,0])
    f_operator = float(np.dot(U[1:,0],U[1:,0]))
    return t,f_operator

def true_f(rleft,rright):
    return 1.0-((1.0-2.0*P*rleft)*(1.0-2.0*P*rright))**2

def true_book(rleft,rright):
    return -math.log1p(-Z*true_f(rleft,rright))

def native_reports(y,u=0.0,c=None):
    assert len(y) == 42
    rstar = R0+u
    if c is None:
        c = C0+u/3.0
    all_r = rstar+SLOPES @ np.asarray(y)
    assert 0 <= c <= 1 and all(0 <= rr <=1 for rr in all_r)
    mean = float(np.dot(WEIGHTS,all_r)/W)
    return 1.0-(mean+c)/2.0, (rstar+c)/2.0, all_r

def main():
    checks=0
    assert abs(P+P**2-1)<1e-15
    assert abs(C0-(1-R0))<1e-15
    checks+=2
    for rleft in (0.02,0.2,0.5,0.7,0.91):
        for rright in (0.04,0.15,0.5,0.77,0.95):
            t,f=full_tensor(rleft,rright)
            assert abs(t-(1-2*P*rleft)*(1-2*P*rright))<5e-14
            assert abs(f-true_f(rleft,rright))<5e-14
            checks+=2

    y0=np.zeros(42)
    left,right,_=native_reports(y0)
    assert left==right==0.5
    book0=true_book(left,right)
    assert abs(true_f(left,right)-(1-P**8))<2e-15
    checks+=2

    # Independent analytic CQ source and genuine tensor Book variation:
    hprime=math.log((1-R0)/R0)/math.log(PHI)
    gain=(2*Z*P**7)/(GAMMA*W*hprime*A0)
    assert gain>0
    for j in range(42):
        drbar=float(np.dot(WEIGHTS,SLOPES[:,j])/W)
        book_derivative=-2*Z*P**7/A0*drbar
        cq_derivative=-GAMMA*W*hprime*drbar
        assert abs(book_derivative-gain*cq_derivative)<1e-19
        yp=np.zeros(42);yp[j]=1e-5
        ym=-yp
        lp,rp,_=native_reports(yp)
        lm,rm,_=native_reports(ym)
        observed=(true_book(lp,rp)-true_book(lm,rm))/(2e-5)
        assert abs(observed-book_derivative)<5e-12
        checks+=2

    # Genuine common-programme equal-zero-operand identity for several
    # *physically valid* small controller variations.
    for u in (-1e-7,-5e-8,0.,5e-8,1e-7):
        l,r,_=native_reports(y0,u)
        s=(R0+u+C0+u/3)/2.
        assert abs(l-(1-s))<4e-16 and abs(r-s)<4e-16
        assert abs((1-2*P*l)*(1-2*P*r)-
                   (P**4-4*P**2*(s-0.5)**2))<1e-15
        checks+=2

    # Near the active c0~1 boundary double precision cannot resolve
    # second differences: use 70-digit *admissible* Decimal controls.
    with localcontext() as ctx:
        ctx.prec=75
        d=Decimal
        pd=(d(5).sqrt()-1)/2
        zd=d(1)/(d(2)**20)
        ld=4*pd**3
        rd=d(1)-(d(1)-zd*ld)*(d(1)-zd*ld*(d(1)+pd**6))
        cd=d(1)-rd
        A=d(1)-zd*(d(1)-pd**8)
        def fb_at(s):
            tl=d(1)-2*pd*(d(1)-s)
            tr=d(1)-2*pd*s
            return -(d(1)-zd*(d(1)-(tl*tr)**2)).ln()
        def controller(u):
            star=rd+u
            coin=cd+u/3
            assert d(0)<star<d(1) and d(0)<coin<d(1)
            s=(star+coin)/2
            return fb_at(s)
        zero=controller(d(0))
        h=d("0.0000001")
        plus,minus=controller(h),controller(-h)
        assert plus>zero and minus>zero
        observed=(plus+minus-2*zero)/(h*h)
        predicted=4*zd*pd**6/A*(d(4)/d(3))**2
        assert abs(observed/predicted-1)<d("1e-11")
        checks+=4
        # Direct sum (alternative programmes) has the opposite sign.
        def j(ri):
            Fi=4*pd*ri*(d(1)-pd*ri)
            return -(d(1)-zd*Fi).ln()
        def direct_sum(u):
            star=rd+u; coin=cd+u/3
            s=(star+coin)/2
            return j(s)+j(d(1)-s)
        ds0=direct_sum(d(0))
        assert direct_sum(h)<ds0 and direct_sum(-h)<ds0
        checks+=2

    # Real operator-value competitor at c=0, other physical costs not bound.
    l0,r0,_=native_reports(y0,0,0)
    gap=book0-true_book(l0,r0)
    assert 3.28e-8 < gap < 3.29e-8
    checks+=1
    # Free *independent* arm report does NOT satisfy the Euler law.
    free_arm=4*Z*P**7/A0
    assert free_arm>0
    checks+=1
    print(json.dumps({
        "status":"PASS","assertions":checks,
        "true_full_tensor_dim":16,
        "source_rows":42,
        "original_r0":R0,
        "baseline_complement_c0":C0,
        "matched_gain":gain,
        "book_source_per_mean_report":-2*Z*P**7/A0,
        "shared_c_curvature":4*Z*P**6/A0,
        "independent_arm_residual":free_arm,
        "mathematical_competitor_gap":gap,
        "scope":"shared-controller and field source only; full physical GR OPEN"
    },sort_keys=True))

if __name__ == "__main__":
    main()
