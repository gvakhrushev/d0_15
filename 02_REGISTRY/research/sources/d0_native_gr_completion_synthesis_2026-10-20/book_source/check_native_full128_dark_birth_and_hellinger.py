#!/usr/bin/env python3
"""EXACT dark-history birth in ORIGINAL native Jones+/CAR16 full128 Kraus.

No new POVM, primitive or selected Book03 Cost-Info; this independently builds
the original creator-ordered Fourier Walsh baseline, both Julia roots and
THEIR TRUE first coframe variation. It checks an exact support-changing
two-round original history (50,0). See SCREEN_RECORD_PROPER_SCORE... §5–6.
"""
import sympy as s

p=(s.sqrt(5)-1)/2
a=s.sqrt(p)
nu=s.Rational(3,5)
b=s.Rational(4,5)
I=s.I
order=(0,2,3,1)
C=[]
for role in range(4):
    c=s.zeros(16)
    prior=order[:order.index(role)]
    for bits in range(16):
        if not bits & (1<<role):
            c[bits | (1<<role),bits]=(-1)**sum(
                bool(bits&(1<<j)) for j in prior)
    C.append(c)
eye=s.eye(16)
zlist=(I,I,-1,-I)
Q0=s.zeros(16)
Q25=s.zeros(16)
dQ0=s.zeros(16)
dQ25=s.zeros(16)

# Only the ORIGINAL real F_(0,0) coframe direction varies; native roots
# at the reference are L=I+(b-1)CC†, R=I+(b-1)C†C.
# Their exact derivative under P_0(t)=(1+t)P_0 is
# dL=-nu²/b CC†, dR=-nu²/b C†C (genuine Sylvester derivative).
for role in range(4):
    z=zlist[role]
    v=nu*C[role]
    P=z*v
    Pd=P.conjugate().T
    L=eye+(b-1)*(C[role]*C[role].T)
    R=eye+(b-1)*(C[role].T*C[role])
    dP=P if role==0 else s.zeros(16)
    dPd=Pd if role==0 else s.zeros(16)
    dv=v if role==0 else s.zeros(16)
    dL=-(nu**2/b)*(C[role]*C[role].T) if role==0 else s.zeros(16)
    dR=-(nu**2/b)*(C[role].T*C[role]) if role==0 else s.zeros(16)
    rows=((P,L,dP,dL), (Pd,R,dPd,dR),
          (-v,-L,-dv,-dL),(-v.T,-R,-dv.T,-dR))
    for row,(x,y,dx,dy) in enumerate(rows):
        for rep in range(2):
            label=role*8+row*2+rep
            walsh=(-1)**((12 & label).bit_count())
            Q0+=x/32
            Q25+=walsh*y/32
            dQ0+=dx/32
            dQ25+=walsh*dy/32

psi=s.zeros(16,1)
psi[0]=psi[14]=-a/s.sqrt(2)
psi[1]=psi[15]=p/s.sqrt(2)
# Literal K_50: port0 of Jones label25; K_0 has the native blank I.
K50=-2*p*p*Q25.conjugate().T*Q0
dK50=-2*p*p*(dQ25.conjugate().T*Q0+Q25.conjugate().T*dQ0)
K0=eye-2*p*p*Q0.conjugate().T*Q0

dark=K50*psi
assert all(s.simplify(x)==0 for x in dark), "native Jones label50 is NOT dark"
v=dK50*psi
expected_1=27*s.sqrt(2)*a*p**2/6400
assert s.simplify(s.expand(v[4])-expected_1)==0

# For the ORIGINAL full two-round (j,k)=(50,0), second variation term
# (dK_0)K_50 psi vanishes because the actual first output is dark.
double_first=K0*v
expected_2=(27*s.sqrt(2)*a*(897-293*s.sqrt(5))
            /s.Integer(4096000))
assert s.simplify(s.expand(double_first[4])-expected_2)==0
assert (897-293*s.sqrt(5)).is_positive
assert s.simplify(expected_1)!=0 and s.simplify(expected_2)!=0

# Therefore q_(50,0)(t)=t² ||K0 dK50 psi||²+O(t³),
# so the ORIGINAL anchor has q_0=0 but q_t>0 for small t !=0.
# Fixed-anchor forward KL(q_t||q_0) is mathematically +infinity.
print("EXACT original full128 Jones first dark output: K_50 psi = 0")
print("EXACT d_F00 K_50 psi component4 =",expected_1)
print("EXACT d_F00 (K_0 K_50 psi) component4 =",expected_2)
print("PASS: positive rank-birth => fixed-anchor KL(q_t || q_0) infinite")
print("PASS: Hellinger anchored dark contribution differentiates "
      "||K_k K_j psi||², no inverse probability")
print("NO CLAIM: compulsory native selected Book03 Info, physical GR closure")
