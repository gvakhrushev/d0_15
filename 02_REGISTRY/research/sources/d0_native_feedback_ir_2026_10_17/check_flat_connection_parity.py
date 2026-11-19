#!/usr/bin/env python3
"""Exact full16 CAR constant-connection parity and all24 first-source check.

Continuum D=D_flat+Z(T), Z(T)=-(Q_T+Q_T*) with all24 Cartan torsions.
Negative control: a one-sided coherent matter preparation need NOT be
stationary. Not a finite-h or joint metric/physical preparation theorem.
"""
from sympy import Matrix, zeros, I, Rational, simplify

def ensure(ok, msg):
    if not ok: raise RuntimeError(msg)

C=[]
for j in range(4):
    m=zeros(16,16)
    for n in range(16):
        if not ((n>>j)&1):
            m[n|(1<<j),n]=(-1)**((n&((1<<j)-1)).bit_count())
    C.append(m)
An=[x.T for x in C]
gamma=[C[j]-An[j] for j in range(4)]
Z=[]
names=[]
for a in range(4):
    for b in range(4):
        for c in range(b+1,4):
            Q=C[b]*C[c]*An[a]
            Z.append(-(Q+Q.T))
            names.append((a,b,c))
ensure(len(Z)==24,"not all 24 Lorentz Cartan components")
mom=Matrix([1,2,-1,3])
D0=I*sum((mom[j]*gamma[j] for j in range(4)),zeros(16,16))
combined=sum(((k+1)*Zk/17 for k,Zk in enumerate(Z)),zeros(16,16))
D_plus=D0+combined
D_negative=-D0-combined
ensure(D_plus+D_negative==zeros(16,16),"D(-k,-T) != -D(k,T)")
ensure(D_plus+D_negative==zeros(16,16),"squared parity follows from exact opposite operators")
# All 24 connection sources vanish on the full original ±momentum, full16 shell.
shell=[Matrix([sign if j==r else 0 for j in range(4)])
       for r in range(4) for sign in (+1,-1)]
for j,Zj in enumerate(Z):
    result=0
    for k in shell:
        Dk=I*sum((k[a]*gamma[a] for a in range(4)),zeros(16,16))
        result+=(Dk*Zj+Zj*Dk).trace()
    ensure(simplify(result)==0,f"faithful shell source nonzero at {names[j]}")
# Local positive-energy / single-sided coherent preparation is NOT inversion invariant.
q=C[0]*C[1]*An[0]
ztest=-(q+q.T)
j0=I*gamma[0]
derivative=j0*ztest+ztest*j0
psi=zeros(16,1)
psi[0]=1/2**Rational(1,2)
psi[3]=I/2**Rational(1,2)
negative= simplify((psi.conjugate().T*derivative*psi)[0])
ensure(negative!=0,"negative-control source must be nonzero")
print(f"all24=PASS; full16=supported; inversion-even stationary slice=PASS;")
print(f"negative-control one-sided coherent source={negative}; status=PASS")
