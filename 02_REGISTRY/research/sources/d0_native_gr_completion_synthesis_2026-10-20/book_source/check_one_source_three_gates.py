#!/usr/bin/env python3
"""Exact D0 one-source composition negative controls.

ORIGINAL Golden-J2 native 8D A/B feedback eigenvalues and second-jet Gram,
classical Golden normalization gauge, and original full CAR16 Lorentz
grade-number noncentrality. Abstract integrability is proved in the memo;
this checker checks exact algebra, not native task admission or GR_closed.
"""
import sympy as s

p=(s.sqrt(5)-1)/2
z=s.Rational(1,2**20)
eta=s.symbols("eta",real=True,nonzero=True)
f,q=s.symbols("f q",real=True)
E=p**2*(1+eta**2*f)
b=(p-p**2*eta**2*q)**2
B=4*b*(1-b)
A=B+(1-B)*4*E*(1-E)
B0=s.simplify(B.subs({f:0,q:0}))
A0=s.simplify(A.subs({f:0,q:0}))
assert s.simplify(B0-4*p**3)==0
assert s.simplify(A0-4*p**3*(1+p**6))==0
dA=s.simplify(s.diff(A,f).subs({f:0,q:0}))
assert s.simplify(dA-4*p**2*(1-4*p**3)*(1-2*p**2)*eta**2)==0
assert s.simplify(dA-(178*s.sqrt(5)-398)*eta**2)==0
assert float(dA.subs(eta,1))>0
pi=z/(1-z*A0)
gram=s.factor((pi*dA)**2)
assert float(gram.subs(eta,1))>0

# Exact 2-jet theorem logic: at a stationary point DJ=0,
# an open-neighborhood equality DS=c(y) DJ forces HessS=c0 HessJ.
# Tangent-normal nonzero HessJ fixes c0; actual source Gram violates it.
cc,gg,h,g=s.symbols("c gamma h gram",real=True,nonzero=True)
HS=cc*gg*s.Matrix([[0,h,0],[h,0,0],[0,0,1-g]])
HJ=s.Matrix([[0,h,0],[h,0,0],[0,0,1]])
assert s.simplify(HS[0,1]/HJ[0,1]-cc*gg)==0
assert s.simplify(HS[2,2]-cc*gg*HJ[2,2])==-cc*gg*g
assert s.simplify(HS.det()+cc**3*gg**3*h**2*(1-g))==0

# Projective normalization: every smooth common history charge c(y)
# disappears from the normalized Golden prospective scalar weights.
y=s.symbols("y",real=True)
prices=(y*y,2*y,3+y)
phi=(1+s.sqrt(5))/2
w=[phi**(-v) for v in prices]
extra=y**3+2*y
wnew=[phi**(-v-extra) for v in prices]
for wa,wb in zip(w,wnew):
    assert s.simplify(wa/sum(w)-wb/sum(wnew))==0
assert s.diff(extra,y)!=0

# The ACTUAL proper-Lorentz exterior/CAR16 action preserves every wedge
# grade, so gauge equivariance alone does NOT imply priced effect scalar.
N=s.diag(*[mask.bit_count() for mask in range(16)])
assert set(N.diagonal())=={0,1,2,3,4}
X=s.zeros(4);X[0,1]=X[1,0]=1
ex=s.zeros(16)
for mask in range(16):
    cols=[i for i in range(4) if mask>>i&1]
    for slot,j in enumerate(cols):
        for i in range(4):
            if (mask>>i&1) and i!=j:continue
            remaining=cols.copy();remaining[slot]=i
            if len(set(remaining))<len(remaining):continue
            inversions=sum(remaining[k]>remaining[l]
                           for k in range(len(remaining))
                           for l in range(k+1,len(remaining)))
            newmask=sum(1<<index for index in remaining)
            ex[newmask,mask]+=(-1)**inversions*X[i,j]
assert ex!=s.zeros(16)
assert N*ex-ex*N==s.zeros(16)
assert N[0,0]!=N[1,1]

print("PASS: exact 8D Golden J2 eigenvalues, moving coframe-source derivative")
print("dA/df =",dA)
print("PASS: strictly positive native operator-resolvent Gram =",gram)
print("PASS: transverse stopped-Price 2-jet cannot equal a global scalar DJ2 multiple")
print("PASS: identical normalized Golden laws with different absolute Price source")
print("PASS: full CAR16 Lorentz-covariant positive number operator is noncentral")
print("FIREWALL: a true executable ambient f-direction/compulsory native Price is OPEN")
print("GR_closed=false")
