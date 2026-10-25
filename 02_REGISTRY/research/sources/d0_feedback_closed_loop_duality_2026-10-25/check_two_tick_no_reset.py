#!/usr/bin/env python3
"""EXACT original zeta=2^-20 2-tick fully recorded closed CAR Slater source.
15 finite occupation outcomes on active 2 + archive1 2 + archive2 2.
The second field and the first field do NOT commute. All earlier archive
columns are retained, and original DATA is NEVER independently reset.

Finite mathematical Fock Born test; does NOT claim the actual original
CAR16/G/CX clock word implements these 6 fermionic modes at no extra cost.
"""
from __future__ import annotations
import sympy as S
import itertools
import json

r=S.Rational
z=r(1,2**20)
I2=S.eye(2)
O1=S.Matrix([[r(3,5),-r(4,5)],[r(4,5),r(3,5)]])
O2=S.Matrix([[r(5,13),-r(12,13)],[r(12,13),r(5,13)]])

def ab(t):
    return (1-t*t)/(1+t*t),2*t/(1+t*t)

def make(O,t1,t2):
    a1,b1=ab(t1);a2,b2=ab(t2)
    A=O*S.diag(a1,a2)*O.T
    B=O*S.diag(b1,b2)*O.T
    F=B**2/z
    return A,B,F

A1,B1,F1=make(O1,r(1,4096),r(1,3072))
A2,B2,F2=make(O2,r(1,4608),r(1,3584))
checks=0

def check(cond,msg):
    global checks
    checks+=1
    if not bool(cond):
        raise ArithmeticError(msg)

check(F1*F2!=F2*F1,'real sequential original F sources noncommute')

def step(A,B,p):
    W=S.eye(6)
    idx=[0,1,p,p+1]
    V=A.row_join(-B).col_join(B.row_join(A))
    for i in range(4):
        for j in range(4):
            W[idx[i],idx[j]]=V[i,j]
    return W

W1=step(A1,B1,2)
W2=step(A2,B2,4)
Wt=W2*W1
for w in [W1,W2,Wt]:
    check(w.T*w==S.eye(6) and w.det()==1,
          '6 one-particle closed unitary')
check(Wt[:2,:2]==A2*A1,'no leakage reset; retained first archive intact')
check(Wt[2:4,0:2]==B1,'first archive permanently saved')
check(Wt[4:6,0:2]==B2*A1,'second archive sees actual nonreset current data')
labels=list(itertools.combinations(range(6),2))
amp=[Wt.extract(list(pair),[0,1]).det() for pair in labels]
p=[v*v for v in amp]
check(len(labels)==15 and all(x>=0 for x in p),
      'all 15 two-particle records kept')
check(sum(p)==1,'whole output CAR16-style no lost probabilities')
p0=p[0]
q1=(S.eye(2)-z*F1).det()
q2=(S.eye(2)-z*F2).det()
check(p0==q1*q2,'no-reprep all-empty probability product exact')
check(p0==(A2*A1).det()**2,'noncommuting 2tick Slater determinant')
check(p0>0 and p0<1 and sum(p[1:])>0,'true archive events survive')

print(json.dumps({
    'status':'PASS_EXACT_NO_RESET_TWO_TICK_SAME_CLOSED_ARCHIVE_BOOK',
    'checks':checks,
    'archive_modes_per_tick':2,
    'total_one_particle_modes':6,
    'total_two_particle_outcomes':15,
    'noncommuting_first_second_F':True,
    'full_history_archive_reset':False,
    'all_quiet_probability':str(p0),
    'all_quiet_probability_decimal':str(S.N(p0,23)),
    'full_silent_log_price_equals_sum':True,
    'physically_selected_original_G0_task':False,
    'GR_closed':False
},indent=2))
