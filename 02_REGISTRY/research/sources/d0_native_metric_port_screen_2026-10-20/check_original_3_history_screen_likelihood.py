#!/usr/bin/env python3
"""Exact native full128 Walsh/Julia/Golden two-tick log-likelihood on a metric screen.

Field: Q(a,i), p=a^2, a^4+a^2=1. Same original L=4 Fourier character
(i,i,-1,-i), native Jones+ input, all left/right Julia roots, port 1.
This validates only three genuine positive two-tick events (0,17),(0,27),(0,59).
It does NOT choose a full Book03 Cost-Info action or prove Einstein equations.
"""
import sympy as s

a=s.symbols('a',real=True);p=a*a
nu=s.Rational(3,5);b=s.Rational(4,5);ph=[s.I,s.I,-1,-s.I]
order=[0,2,3,1];I=s.eye(16);Z=s.zeros(16)
eta=s.diag(1,-1,-1,-1)
C=[]
for r in range(4):
    m=Z.copy();before=order[:order.index(r)]
    for bits in range(16):
        if not bits&(1<<r):
            m[bits+(1<<r),bits]=(-1)**sum(bool(bits&(1<<j)) for j in before)
    C.append(m)
lft=[c*c.T for c in C];rgt=[c.T*c for c in C]

def rootder(proj,d):
    blk=[I-proj,proj];eig=[1,b];out=Z.copy()
    for i in range(2):
        for j in range(2):
            out-=blk[i]*d*blk[j]/(eig[i]+eig[j])
    return out

def words(variation=None):
    out=[[],[]]
    for r in range(4):
        z=ph[r];cr=C[r];v=nu*cr;P=nu*z*cr;Pd=P.H
        L=I+(b-1)*lft[r];R=I+(b-1)*rgt[r]
        if variation is None:
            rows=[(P,L),(Pd,R),(-v,-L),(-v.T,-R)]
        else:
            H=eta*variation
            dv=nu*sum((H[r,j]*C[j] for j in range(4)),Z.copy())
            dP=z*dv;dPd=dP.H
            dL=rootder(lft[r],dP*Pd+P*dPd)
            dR=rootder(rgt[r],dPd*P+Pd*dP)
            rows=[(dP,dL),(dPd,dR),(-dv,-dL),(-dv.T,-dR)]
        for c0,c1 in rows:
            for _ in range(2):
                out[0].append(c0);out[1].append(c1)
    return out

W=words()
def row(W,label,comp):
    return sum(((-1)**((label&j).bit_count())*W[comp][j]
                for j in range(32)),Z.copy())/32

A=row(W,0,0)
assert all(s.simplify(v)==0 for v in A*A-(A*A)[0,0]*I)
psi=s.zeros(16,1)
psi[0]=psi[14]=-a
psi[1]=psi[15]=p # Jones+; /sqrt(2) cancels in log derivatives
events=(17,27,59)
base=[];den=[]
for event in events:
    u=row(W,event//4,(event%4)//2).H*A*psi
    base.append(u)
    den.append(s.expand((u.conjugate().T*u)[0]))

# Three EXACT real-symmetric Q directions with Qk=0 (k=(z_r-1)).
N=s.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
            [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
Pmod=a**4+a*a-1
k=s.Matrix([z-1 for z in ph])
dlog=[]
for j in range(3):
    Q=s.zeros(4);idx=0
    for r in range(4):
        for c in range(r,4):
            Q[r,c]=Q[c,r]=N[idx,j];idx+=1
    assert Q.T==Q and Q*k==s.zeros(4,1)
    Wd=words(Q)
    dA=row(Wd,0,0)
    assert all(s.simplify(v)==0 for v in A*dA+dA*A)
    col=[]
    for i,event in enumerate(events):
        Tj=row(W,event//4,(event%4)//2)
        dTj=row(Wd,event//4,(event%4)//2)
        u=base[i]
        du=dTj.H*A*psi+Tj.H*dA*psi
        numerator=s.expand((du.conjugate().T*u+u.conjugate().T*du)[0])
        numer=s.rem(numerator,Pmod,a).expand()
        denom=s.rem(den[i],Pmod,a).expand()
        col.append(s.cancel(numer/denom))
    dlog.append(col)

J=s.Matrix(dlog).T
expected=s.Matrix([[0,-s.Rational(4,3),0],
                   [s.Rational(16,9),-s.Rational(125,18),s.Rational(5,36)],
                   [-16*a**3/13-s.Rational(9,26),
                    32*a**3/13-s.Rational(1,2),
                    -16*a**3/13-s.Rational(145,52)]])
assert s.simplify(J-expected)==s.zeros(3)
assert s.simplify(J.det()+(1888*a**3+4595)/702)==0
assert J.det()!=0
assert s.simplify(J*s.ones(3,1)-s.Matrix([
    -s.Rational(4,3),-s.Rational(181,36),-s.Rational(189,52)]))==s.zeros(3,1)
print('PASS exact original full128 two-tick events (0,17),(0,27),(0,59)')
print('PASS 3x3 metric-screen likelihood is invertible:',s.factor(J.det()))
print('PASS rank-one finite port-dark line: -4/3,-181/36,-189/52')
print('GR_closed=false: Book03 physical source selection remains OPEN')
