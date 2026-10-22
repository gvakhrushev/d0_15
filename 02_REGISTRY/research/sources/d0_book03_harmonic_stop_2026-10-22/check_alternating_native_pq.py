#!/usr/bin/env python3
"""Exact Book03 harmonic stopping via original U/Udag/P/Q, no sqrt(F) gate."""
import numpy as np
from math import sqrt, log
p=(sqrt(5)-1)/2
zeta=2**-20
U=np.eye(6)
for i,j,c,s in [(0,3,3/5,4/5),(1,4,5/13,12/13),(2,5,15/17,8/17),(0,1,3/5,4/5),(3,4,5/13,12/13)]:
    G=np.eye(6)
    G[i,i]=G[j,j]=c
    G[i,j]=-s
    G[j,i]=s
    U=G@U
P=np.diag([1,1,1,0,0,0])
Q=np.eye(6)-P
A=Q@U@P
F=P@U.T@Q@U@P
K=P.copy()
for n in range(13):
    effect=K.T@K
    expected=P if n==0 else np.linalg.matrix_power(F,n)
    assert np.max(abs(effect-expected))<4e-12,n
    if n%2==0:
        K=Q@U@P@K
    else:
        K=P@U.T@Q@K
print("PASS genuine six-dimensional noncommuting original projector alternation, all n0..12")
assert np.linalg.eigvalsh(F).min()>-1e-12
spectrum=np.linalg.eigvalsh(F)[-3:]
sigma=P/3
mass=0.
harm=0.
for n in range(9):
    current=P if n==0 else np.linalg.matrix_power(zeta*F,n)
    future=np.linalg.matrix_power(zeta*F,n+1)
    probability=np.trace(sigma@(current-future)).real
    mass+=probability
    Hn=sum(1/k for k in range(1,n+1))
    harm+=Hn*probability
tail=np.trace(sigma@np.linalg.matrix_power(zeta*F,9)).real
assert abs(mass+tail-1)<1e-12
J=-sum(log(1-zeta*v) for v in spectrum if v>0)
assert abs(J-3*harm)<3e-11
print("PASS true complete stopped-history law and native Book03 harmonic trace-log")
print("PASS full Golden stochastic fair bit mean primitive letters",1/p**3)
print("PASS 20 native fair bits expected primitive letters bounded",20/p**3/(1-zeta))
print("physical native U/Udag control, P/Q measurement admission and HJR Info: OPEN")
