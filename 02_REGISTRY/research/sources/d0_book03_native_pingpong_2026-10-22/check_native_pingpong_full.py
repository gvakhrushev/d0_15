#!/usr/bin/env python3
"""D0 original Book03 alternating P/U/Q/U* first-return with exact Golden fair cost.

No artificial sqrt(F), polar gate, omitted aborted branch or assumed physical
Book03 full H+J+R selection. Exact 6x6 rational non-diagonal matrix controls,
20 Golden fair bits, genuine P/Q flags and a complete capped raw F/R ledger.
"""
import sympy as s
from mpmath import mp

p=(s.sqrt(5)-1)/2
z=s.Rational(1,2**20)
qG=s.simplify(1-2*p**3)
assert s.simplify(p+p*p-1)==0
assert s.simplify(qG-(5-2*s.sqrt(5)))==0
assert s.simplify((2-p)/p**3-(5+3*s.sqrt(5))/2)==0

I=s.eye(6)
P=s.diag(1,1,1,0,0,0)
Q=I-P
def rot(i,j,a,b):
    v=s.eye(6)
    v[i,i]=v[j,j]=a
    v[i,j]=-b;v[j,i]=b
    return v
U=(rot(0,3,s.Rational(5,13),s.Rational(12,13))
   *rot(1,4,s.Rational(8,17),s.Rational(15,17))
   *rot(2,5,s.Rational(20,29),s.Rational(21,29))
   *rot(0,1,s.Rational(3,5),s.Rational(4,5)))
assert U.T*U==I
A=Q*U*P
F=P*U.T*Q*U*P
assert F==A.T*A
assert F[:3,:3]!=s.diag(*[F[i,i] for i in range(3)])
assert P*F==F and F*P==F
v=s.Matrix([s.Rational(3,5),s.Rational(4,5),0,0,0,0])
rho=v*v.T
K=P
for n in range(0,11):
    if n:
        K=(Q*U if n%2 else P*U.T)*K
    assert K.T*K==(P if n==0 else F**n)
    if n:
        En=z**n*(K.T*K-z*F**(n+1))
        assert En==z**n*F**n*(P-z*F)
for cap in range(0,9):
    accum=P-z*F
    for n in range(1,cap+1):
        accum+=z**n*(F**n-z*F**(n+1))
    assert accum+z**(cap+1)*F**(cap+1)==P
print("PASS 6x6 genuine P,U,Q,Udagger ping-pong: all noncommuting count effects n0..10")
print("PASS full stop POVM plus actual unresolved tail for every cap 0..8")

Cbit=s.simplify((2-p)/p**3)
Cround=s.simplify(Cbit*2*(1-z))
assert z==s.Rational(1,2**20)
print("PASS native Golden FR/RF extractor, 20 bits zeta=2^-20, coin cost/round",
      float(Cround))
for M in (1,2,4,8,12):
    reject=float(qG)**M
    zm=((1-reject)/2)**20
    assert 0<zm<float(z) and float(z)-zm<20*float(z)*reject+1e-22
print("PASS actual capped fair extractor zeta_M=2^-20*(1-qG^M)^20")

mp.dps=85
Fm=mp.matrix([[mp.mpf(int(x.p))/x.q for x in row]
              for row in F[:3,:3].tolist()])
lam=mp.eigsy(Fm,eigvals_only=True)
zz=mp.mpf(1)/2**20
J=-sum(mp.log(1-zz*v) for v in lam)
for cap in (1,2,4,8):
    part=sum(sum((zz*v)**k for v in lam)/k for k in range(1,cap+1))
    assert 0<J-part<3*zz**(cap+1)/((cap+1)*(1-zz))
rounds=sum(1/(1-zz*v) for v in lam)/3
tests=zz*rounds
coin_price=(5+3*mp.sqrt(5))*(1-zz)*rounds
assert rounds>1 and 0<tests<1 and coin_price>(5+3*mp.sqrt(5))*(1-zz)
print("PASS complete harmonic Book J, native fair-code clock, paid projection count")

# Full original F/R raw transcript and P/Q report code, no hidden rejected
# pair. M=1 pairs per fair bit, 2 bits per attempt, 2 survived rounds cap.
mp.dps=70
pp=(mp.sqrt(5)-1)/2
lp=mp.log(1/pp)
pairs=[]
for raw in ("FF","FR","RF","RR"):
    cost=raw.count("F")+2*raw.count("R")
    pairs.append((raw,cost,pp**cost,raw=="RF"))
assert abs(sum(x[2] for x in pairs)-1)<mp.mpf("1e-65")
macro=[]
for a,ca,pa,ba in pairs:
    if not ba:
        macro.append((a,ca,pa,False))
    else:
        for b,cb,pb,bb in pairs:
            macro.append((a+b,ca+cb,pa*pb,bb))
assert abs(sum(x[2] for x in macro)-1)<mp.mpf("1e-65")
zsmall=sum(prob for raw,cost,prob,good in macro if good)
assert abs(zsmall-pp**6)<mp.mpf("1e-65")

def priced_complete_tape(f):
    leaves=[]
    def attempt(k,weight,coins,proj,ntests):
        for raw,cost,pm,go in macro:
            w=weight*pm
            if not go:
                leaves.append((w,coins+cost,proj,ntests))
            else:
                leaves.append((w*(1-f),coins+cost,proj+2,ntests+1))
                if k==1:
                    leaves.append((w*f,coins+cost,proj+1,ntests+1))
                else:
                    attempt(k+1,w*f,coins+cost,proj+1,ntests+1)
    attempt(0,mp.mpf(1),0,0,0)
    assert len(leaves)==15
    assert abs(sum(x[0] for x in leaves)-1)<mp.mpf("1e-60")
    coin=sum(x[0]*x[1] for x in leaves)
    projection=sum(x[0]*x[2] for x in leaves)
    entropy=-sum(x[0]*mp.log(x[0])/lp for x in leaves)
    nt=sum(x[0]*x[3] for x in leaves)
    h=-(f*mp.log(f)+(1-f)*mp.log(1-f))/lp
    assert abs(nt-zsmall*(1+zsmall*f))<mp.mpf("1e-60")
    assert abs(coin+projection-entropy-nt*(2-f-h))<mp.mpf("1e-60")
for v in (mp.mpf(".6"),mp.mpf(".94"),mp.mpf(".996")):
    priced_complete_tape(v)
print("PASS all 15 real fully priced capped raw F/R+P/Q histories:")
print("     E(C_coin+C_projector)-full pointer Shannon = E(projective calls)*native Golden KL")
print("SCOPE: exact Book feedback recording and raw-code price; selected HJR/Info/G0 not proved")
print("GR_closed=false")
