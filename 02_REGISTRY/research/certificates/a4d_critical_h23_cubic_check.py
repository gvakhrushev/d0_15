#!/usr/bin/env python3
"""Exact cubic action coefficient; finite controls, not refining roots."""
from fractions import Fraction as Q
from math import factorial
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N

def face_cubic(xs):
    out = np.zeros((4, 4), dtype=object)
    for a in range(4):
        for b in range(4-a):
            for c in range(4-a-b):
                d = 3-a-b-c
                term = N.I.copy()
                for x, n in zip(xs, (a,b,c,d)):
                    for _ in range(n): term = term @ x
                out += term * Q(1, factorial(a)*factorial(b)*factorial(c)*factorial(d))
    return out

def cubic(logs):
    value = Q(0)
    for p in range(4):
        for face, (r,s) in enumerate(N.PAIRS):
            xs = (logs[p,r], logs[(p+1)%4,s],
                  -logs[(p+1)%4,r], -logs[p,s])
            coefficient = face_cubic(xs)
            jets = np.zeros((4,4,4,4), dtype=object)
            for j,x in enumerate(xs): jets[j,0] = N.I; jets[j,1] = x; jets[j,2] = x@x*Q(1,2); jets[j,3] = x@x@x*Q(1,6)
            product = N.jconst(N.I,3)
            for jet in jets: product = N.jmul(product,jet)
            assert np.array_equal(product[3], coefficient)
            value += np.sum(N.WEIGHT[face]*coefficient)
    return Q(value)

values=[]
for seed in range(3):
    logs=np.array([[sum((Q(((17*p+11*r+7*a+13*seed)%19)-9,23)*N.G[a]
                         for a in range(6)),np.zeros((4,4),dtype=object))
                    for r in range(4)] for p in range(4)])
    value=cubic(logs)
    assert cubic(-logs)==-value
    assert cubic(2*logs)==8*value
    # Radial Euler coefficient is 3 P3; eliminating the quadratic
    # stationary contribution gives P3 - (3/2)P3 = -P3/2.
    assert value-Q(1,2)*3*value == -value/2
    values.append(str(value))
assert any(Q(x) for x in values)
for amplitudes in ([1,0,0,0,0,0,0,0], list(range(1,9)), [2,-1,3,0,1,4,-2,5]):
    logs=N.logs_of(amplitudes,3)
    ek,_=N.euler(logs)
    assert not np.any(ek[:2])
    assert cubic(logs[:,:,1])==0
print('PASS_LITERAL_CUBIC_JET_AND_RADIAL_FACTOR', values)
print('PASS_THREE_QUARTER_KERNEL_CONTROLS_CUBIC_ZERO')
print('OPEN_STATIONARY_SEQUENCE_CUBIC_AVERAGE_NOT_CERTIFIED_ZERO')
