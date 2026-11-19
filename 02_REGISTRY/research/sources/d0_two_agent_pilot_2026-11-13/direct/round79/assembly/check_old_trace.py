"""Native old prefixes, a positive reciprocal-square-root clock and its source."""
from fractions import Fraction as F
from math import comb, log, sqrt

import numpy as np


def return_series(x, n):
    value, derivative = 1., 0.
    power, weight = 1., 1.
    for i in range(1,n+1):
        weight *= (2*i-1)/(2*i)
        derivative -= i*weight*power
        power *= 1-x
        value += weight*power
    return value, derivative


def budget(n):
    return 1 << n.bit_length()


def certify_menu(n):
    denominator = 4**n*budget(n)
    counts = [comb(2*j,j)*4**(n-j) for j in range(n+1)]
    assert sum(counts) <= denominator
    x = F(3,7)
    positive = sum(count*(1-x)**j for j,count in enumerate(counts))/denominator
    return positive == sum(F(comb(2*j,j),4**j)*(1-x)**j for j in range(n+1))/budget(n)


def old_words():
    p=(sqrt(5)-1)/2
    v=np.array([sqrt(p),p])
    gate=np.array([[sqrt(p),-p],[p,sqrt(p)]])
    swap=np.array([[0.,1.],[1.,0.]])
    controlled=np.block([[np.eye(2),np.zeros((2,2))],[np.zeros((2,2)),swap]])
    birth=np.kron(np.eye(2),v[:,None])
    rotate=np.kron(np.eye(2),gate)
    corners=[birth.T@w@birth for w in (rotate@controlled,controlled@rotate)]
    assert np.allclose(corners[0],np.diag([sqrt(p),p]))
    assert np.allclose(corners[1],np.diag([sqrt(p),3*p-4*p**3]))
    assert abs(np.trace(corners[0].T@corners[0])/2-.5)<1e-14
    return p,corners


def normalized_ledger(a,da,q,dq,n,rounds):
    rank=len(a)
    x,dx=np.trace(a)/rank,np.trace(da)/rank
    k=budget(n)
    p=(sqrt(5)-1)/2
    failure=(1-2*p**3)**rounds
    width=2*n+k.bit_length()
    # log1p/expm1 keep the field-independent readiness failure even near 1.
    miss=-np.expm1(width*np.log1p(-failure))
    sample,dsample=return_series(x,n)
    g=miss*k+(1-miss)*sample
    dg=(1-miss)*dsample*dx
    c,dc=1-2*q,-2*dq
    y=(c*g)**2*a
    dy=(c*g)**2*da + 2*c*g*(dc*g+c*dg)*a
    z=2.**-20
    t=1/k**2
    matrix=np.eye(rank)+(z/(1-z))*t*y
    # D(J)/[rz t/(1-z)], computed without subtracting near-equal logdets.
    return -np.trace(np.linalg.solve(matrix,dy))/rank


def main():
    assert all(certify_menu(n) for n in (0,1,6,18))
    p,corners=old_words()
    old=[c.T@c for c in corners]
    tangent=old[1]-old[0]
    assert np.linalg.norm(tangent)>0.4
    q,dq=.31,.017
    for n in (8,24,64):
        rounds=n+80
        for a in old:
            slope=normalized_ledger(a,tangent,q,dq,n,rounds)
            transverse=normalized_ledger(a,tangent,q,0,n,rounds)
            target=4*(1-2*q)*dq
            print(n, "old return",np.trace(a)/2,"source error",abs(slope-target),
                  "transverse source",abs(transverse))
            if n==64:
                assert abs(slope-target)<2e-9 and abs(transverse)<2e-9
    # Noncommuting positive prefix variation and simultaneous field move.
    a=np.array([[.67,.14],[.14,.41]])
    da=np.array([[.13,-.17],[-.17,.19]])
    assert np.linalg.norm(a@da-da@a)>1e-3
    assert abs(normalized_ledger(a,da,q,dq,64,144)-4*(1-2*q)*dq)<2e-9
    print("cold factors and finite menu verified; the smooth matrix row is a continuation test")


if __name__=='__main__':
    main()
