#!/usr/bin/env python3
"""Original full128 Golden Walsh/Julia/Jones two-tick screen likelihood.
Exact Q(a,i)/(a^4+a^2-1) verification, no invented detector or Book action.
"""
import sympy as s
from time import perf_counter

a=s.symbols('a', real=True)
p=a*a
nu=s.Rational(3,5)
b=s.Rational(4,5)
phase=[s.I,s.I,-1,-s.I]
ORDER=(0,2,3,1)
I=s.eye(16)
Z=s.zeros(16)
eta=s.diag(1,-1,-1,-1)
C=[]
for r in range(4):
    m=Z.copy()
    before=ORDER[:ORDER.index(r)]
    for bits in range(16):
        if not(bits>>r)&1:
            m[bits | (1<<r),bits]=(-1)**sum(bool(bits&(1<<j)) for j in before)
    C.append(m)
left=[c*c.T for c in C]
right=[c.T*c for c in C]

def rootjet(proj,d):
    blocks=(I-proj,proj)
    eigen=(1,b)
    out=Z.copy()
    for i in range(2):
        for j in range(2):
            out-=blocks[i]*d*blocks[j]/(eigen[i]+eigen[j])
    return out

def words(Q=None):
    out=[[],[]]
    for r in range(4):
        z=phase[r]
        cr=C[r]
        v=nu*cr
        P=nu*z*cr
        Pd=P.H
        L=I+(b-1)*left[r]
        R=I+(b-1)*right[r]
        if Q is None:
            rows=((P,L),(Pd,R),(-v,-L),(-v.T,-R))
        else:
            H=eta*Q
            dv=nu*sum((H[r,j]*C[j] for j in range(4)),Z.copy())
            dP=z*dv
            dPd=dP.H
            dL=rootjet(left[r],dP*Pd+P*dPd)
            dR=rootjet(right[r],dPd*P+Pd*dP)
            rows=((dP,dL),(dPd,dR),(-dv,-dL),(-dv.T,-dR))
        for c0,c1 in rows:
            for _ in range(2):
                out[0].append(c0)
                out[1].append(c1)
    assert len(out[0])==len(out[1])==32
    return out

W=words()
def row(components,label,comp):
    return sum(((-1)**((label&j).bit_count())*components[comp][j]
               for j in range(32)),Z.copy())/32

A=row(W,0,0)
assert all(s.simplify(x)==0 for x in A*A-(A*A)[0,0]*I)
psi=s.zeros(16,1)
psi[0]=psi[14]=-a
psi[1]=psi[15]=p
# psi is unnormalized by sqrt2: this cancels from likelihood scores.
ids=(17,27,59)
baseline=[]
denominator=[]
for k in ids:
    v=row(W,k//4,(k%4)//2).H*A*psi
    baseline.append(v)
    denominator.append(s.expand((v.conjugate().T*v)[0]))
N=s.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
            [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
Ppoly=a**4+a*a-1
result=[]
for j in range(3):
    Q=s.zeros(4)
    slot=0
    for r in range(4):
        for k in range(r,4):
            Q[r,k]=Q[k,r]=N[slot,j]
            slot+=1
    dW=words(Q)
    dA=row(dW,0,0)
    assert all(s.simplify(v)==0 for v in dA), 'true native blank jet vanishes'
    output=[]
    for i,k in enumerate(ids):
        Wk=row(W,k//4,(k%4)//2)
        dWk=row(dW,k//4,(k%4)//2)
        v=baseline[i]
        dv=dWk.H*A*psi+Wk.H*dA*psi
        numerator=s.expand((dv.conjugate().T*v+v.conjugate().T*dv)[0])
        top=s.rem(numerator,Ppoly,a)
        bottom=s.rem(denominator[i],Ppoly,a)
        output.append(s.factor(s.cancel(top/bottom)))
    result.append(output)
    print('screen Q',j,'log history scores',output,flush=True)
J=s.Matrix(result).T
expected=s.Matrix([
    [0,-s.Rational(4,3),0],
    [s.Rational(16,9),-s.Rational(125,18),s.Rational(5,36)],
    [-16*a**3/13-s.Rational(9,26),
     32*a**3/13-s.Rational(1,2),
     -16*a**3/13-s.Rational(145,52)]
])
assert all(s.rem(s.together(u-v).as_numer_denom()[0],Ppoly,a)==0
           for u,v in zip(J,expected))
assert s.rem(s.together(J.det()+(1888*a**3+4595)/702).as_numer_denom()[0],Ppoly,a)==0
qstar=J*s.ones(3,1)
assert all(s.rem(s.together(u-v).as_numer_denom()[0],Ppoly,a)==0
           for u,v in zip(qstar,s.Matrix([-s.Rational(4,3),-s.Rational(181,36),-s.Rational(189,52)])))
print('PASS exact three full128 two-round Jones history likelihood directions')
print('det J=-(1888*a^3+4595)/702, a^4+a^2=1')
print('GR_closed=false: Book03 native history Info/action binding still conditional')
