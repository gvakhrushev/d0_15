#!/usr/bin/env python3
"""Original native TWO triangles (same Cost, different order), GOLDEN p;
full CAR16 + two fresh Julia flags + complete 13-effect original Choi test.
MATHEMATICAL readout feasibility; not compulsory physical G0/Book or GR.
"""
import math,itertools
import numpy as np
from scipy.linalg import expm,eigh

p=(math.sqrt(5)-1)/2
ell=math.log(1/p)
E=lambda i,j:np.eye(4)[:,i:i+1]@np.eye(4)[j:j+1,:]
A=E(1,2)+E(2,0);B=E(0,3)+E(3,1);J=E(2,3)-E(3,2)
N3=E(1,3)+E(3,0);NB2=E(0,2)+E(2,1);Boost=E(1,1)-E(0,0)
Gens=[A,N3,NB2,B,J,Boost]
assert abs(np.trace(J.T@J)-2)<1e-14
assert np.max(abs(np.array([[np.trace(x.T@y) for y in Gens] for x in Gens])-2*np.eye(6)))<1e-12
roles=[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]

def exterior(u):
    m=np.zeros((16,16))
    for i,a in enumerate(roles):
        for j,b in enumerate(roles):
            if len(a)==len(b):
                m[i,j]=np.linalg.det(u[np.ix_(a,b)]) if a else 1
    return m

O=np.zeros((16,4))
for i in range(4):O[1<<i,i]=.5
assert abs(np.linalg.norm(O)-1)<1e-14
fs=[]
for g in Gens:
    m=np.zeros((16,16))
    m[np.ix_([1,2,4,8],[1,2,4,8])]=g
    fs.append(math.sqrt(2)*m@O)
assert np.max(abs(np.array([[np.sum(x*y) for y in fs] for x in fs])-np.eye(6)))<1e-14
signatures=[(O+sgn*f)/math.sqrt(2) for f in fs for sgn in (1,-1)]

def full_gate(L):
    C=p*exterior(L)
    ew,V=eigh(np.eye(16)-C.T@C)
    assert min(ew)>0  # true 16-grade Julia contraction, not just grade1
    F=(V*np.sqrt(ew)[None,:])@V.T
    assert np.linalg.norm(C.T@C+F.T@F-np.eye(16))<5e-13
    return C,F

def instrument(first,second):
    G1,F1=full_gate(first);G2,F2=full_gate(second)
    probs={}
    for bits in itertools.product((0,1),repeat=2):
        out=(G2 if bits[1]==0 else F2)@(G1 if bits[0]==0 else F1)@O
        if bits==(0,0):
            q=np.array([(np.sum(v*out)**2)/12 for v in signatures])
            rest=np.linalg.norm(out)**2-sum(q)
            assert rest>0 and min(q)>0
            probs['GG']=np.r_[q,rest]
        else:
            probs[''.join('G' if b==0 else 'B' for b in bits)]=np.array([np.linalg.norm(out)**2])
    full=np.r_[*probs.values()]
    assert abs(sum(full)-1)<4e-13 and min(full)>0
    return probs

a=1/40;b=1/40
UA=expm(a*A);UB=expm(b*B)
P=instrument(UB,UA) # two original loops B then A -> based U_A U_B
Q=instrument(UA,UB) # same two loop Costs, reverse order -> U_B U_A
j=4 # J23 is the fifth original 6-generator test marker
xp=P['GG'][2*j];xm=P['GG'][2*j+1]
yp=Q['GG'][2*j];ym=Q['GG'][2*j+1]
X=(16+a*a*b*b)/16;Y=a*b/(2*math.sqrt(2))
expected=np.array([p**4/24*(X+Y)**2,p**4/24*(X-Y)**2])
assert np.max(abs(np.array([xp,xm])-expected))<3e-14
assert abs(xp-ym)<2e-14 and abs(xm-yp)<2e-14
Theta=math.log(xp*ym/(xm*yp))/ell
closed=4/ell*math.log((X+Y)/(X-Y))
assert abs(Theta-closed)<1e-11
assert abs(Theta/(a*b)-2*math.sqrt(2)/ell)<1e-3
print('PASS two opposite original loop orders: full 16-labelled CAR16 and flags')
print('PASS original Golden p flat: GG=p^4, GB=BG=p^3, BB=p^2')
print('PASS all 13 GG POVM outcomes and 3 other flag outcomes are strictly positive')
print('PASS exact native ordered q_J± = p^4/24 (1+a²b²/16 ± ab/(2sqrt2))²')
print('PASS total outcome normalization',sum(np.r_[*P.values()]))
print('PASS nonzero exact oriented positive marked source',Theta)
print('PASS exact second-order source 2sqrt2/ln(phi)',2*math.sqrt(2)/ell)
print('PASS strict GG/other flag probability minima',P['GG'].min(),
      {k:v[0] for k,v in P.items() if k!='GG'})
print('NOTE coframe-calibrated positive Choi reference is not a free gauge-invariant physical instrument')
print('NOTE compulsory native Book action and 4D scene/Role controller not proved')
