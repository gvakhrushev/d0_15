#!/usr/bin/env python3
"""Exact shared-denominator rational orthogonal compiler, with finite complexity bounds."""
import math
from functools import reduce
import json
import sympy as sp
import numpy as np

def require(x, message):
    if not bool(x): raise ArithmeticError(message)

checks=[]
def check(x,name):
    require(x,name);checks.append(name)


def rot(d,i,j,c,s):
    A=sp.eye(d)
    A[i,i]=c;A[j,j]=c;A[i,j]=-s;A[j,i]=s
    return A

def rot_np(d,i,j,angle):
    A=np.eye(d); c=math.cos(angle); s=math.sin(angle)
    A[i,i]=c;A[j,j]=c;A[i,j]=-s;A[j,i]=s
    return A

# A deterministic set of full O(4) targets, not a reduced rank-two claim.
d=4
pairs=[(i,j) for i in range(d) for j in range(i+1,d)]
m=d*(d-1) # two half-angle factors for each original plane rotation
N=3
eps=1/100
Q=math.ceil(2*m/eps)
matrices=[]
Ds=[]
for a in range(N):
    exact=sp.eye(d); float_ref=np.eye(d)
    for k,(i,j) in enumerate(pairs):
        angle=((a+2)*(k+1)*0.173+0.041*(k-a)) % (2*math.pi)-math.pi
        float_ref=rot_np(d,i,j,angle)@float_ref
        r=math.tan(angle/4)
        check(abs(r)<=1+1e-12,'all half-angle rational parameters bounded')
        n=round(r*Q)
        den=Q*Q+n*n
        c=sp.Rational(Q*Q-n*n,den)
        s=sp.Rational(2*Q*n,den)
        for _ in range(2):
            exact=rot(d,i,j,c,s)@exact
            Ds.append(den)
    check(exact.T*exact==sp.eye(d),'whole 4D rational orthogonality exactly')
    err=float(np.linalg.norm(np.array(exact.tolist(),float)-float_ref,2))
    check(err<=m/Q+1e-12,'all-target operator error bounded by m/Q')
    matrices.append({'exact':exact,'error':err})

R=math.prod(Ds)
B=1 << (R-1).bit_length()
check(R<=B and 2*R>B,'common padded denominator between half and whole power of two')
check(R.bit_length()<=N*m*(1+2*math.ceil(math.log2(Q)))+1,'uniform polynomial bit-length bound')
for x in matrices:
    A=x['exact']
    check(all((R*entry).q==1 for entry in A),'same R clears every addressed matrix entry')
s=sp.Rational(R**2,d*d*B**2)
check(s>sp.Rational(1,4*d*d) and s<=sp.Rational(1,d*d), 'readiness independent of number and precision of codes')
check(math.log2(R)<=N*m*(1+2*math.log2(Q)), 'explicit log denominator bound')
output={'status':'PASS_SHARED_RATIONAL_COMPILER','check_count':len(checks),'checks':checks,
        'd':d,'addressed_targets':N,'half_angle_factors_per_target':m,
        'precision_target':eps,'Q':Q,'operator_errors':[round(x['error'],12) for x in matrices],
        'common_denominator_bits':R.bit_length(),'success_probability':str(s),
        'bound':'bits(R) <= 1+A*d*(d-1)*(1+2 log2 Q); success >1/(4d^2)',
        'GR_closed':False}
print(json.dumps(output,indent=2))
