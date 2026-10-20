#!/usr/bin/env python3
"""Original D0 full128 Jones: three exact blank-anchored two-round log odds
on the 3D metric space screened by the genuine Golden port-cost source.
All Walsh/Julia labels reconstructed; not a selected Book03 action or GR.
"""
import sympy as s
T=s.symbols("a",real=True)
p=T*T; nu=s.Rational(3,5); b=s.Rational(4,5)
phase=(s.I,s.I,-1,-s.I); order=(0,2,3,1)
eta=s.diag(1,-1,-1,-1)
I=s.eye(16); Z=s.zeros(16)
C=[]
for role in range(4):
    c=Z.copy(); before=order[:order.index(role)]
    for bits in range(16):
        if not ((bits>>role)&1):
            c[bits+(1<<role),bits]=(-1)**sum(bool(bits&(1<<j)) for j in before)
    C.append(c)
left=[c*c.T for c in C];right=[c.T*c for c in C]
def rootder(projector,delta):
    blocks=(I-projector,projector); eigen=(s.Integer(1),b)
    out=Z.copy()
    for i in range(2):
        for j in range(2):
            out-=blocks[i]*delta*blocks[j]/(eigen[i]+eigen[j])
    return out
def words(variation=None):
    out=[[],[]]
    for r in range(4):
        z=phase[r]; c=C[r]; v=nu*c
        P=nu*z*c; Pd=P.H
        L=I+(b-1)*left[r]; R=I+(b-1)*right[r]
        if variation is None:
            rows=((P,L),(Pd,R),(-v,-L),(-v.T,-R))
        else:
            H=eta*variation
            dv=nu*sum((H[r,j]*C[j] for j in range(4)),Z.copy())
            dP=z*dv; dPd=dP.H
            dL=rootder(left[r],dP*Pd+P*dPd)
            dR=rootder(right[r],dPd*P+Pd*dP)
            rows=((dP,dL),(dPd,dR),(-dv,-dL),(-dv.T,-dR))
        for x,y in rows:
            for _ in range(2):
                out[0].append(x);out[1].append(y)
    return out
def row(W,label,component):
    return sum(((-1)**bin(label&j).count("1")*W[component][j]
                for j in range(32)),Z.copy())/32
W=words(); A=row(W,0,0)
assert A==A.H
assert s.simplify(A*A-s.Rational(9,640)*I)==s.zeros(16)
psi=s.zeros(16,1)
psi[0]=psi[14]=-T;psi[1]=psi[15]=p
mod=T**4+T*T-1
assert s.rem((psi.T*psi)[0]-2,mod,T)==0
# Genuine event label/port index j:
# j//4=Walsh label, (j%4)//2=coefficient, j%2=Golden port.
# At j=17,27,59: all use genuine nonblank port1.
events=(17,27,59)
base=[];den=[]
for j in events:
    v=row(W,j//4,(j%4)//2).H*A*psi
    base.append(v)
    den.append(s.expand((v.conjugate().T*v)[0]))
N=s.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
            [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
def symmetric(coordinates):
    Q=s.zeros(4);index=0
    for i in range(4):
        for j in range(i,4):
            Q[i,j]=Q[j,i]=coordinates[index]
            index+=1
    return Q
k=s.Matrix([z-1 for z in phase])
for t in range(3):
    assert s.simplify(symmetric(N[:,t])*k)==s.zeros(4,1)
jets=[]
for t in range(3):
    Q=symmetric(N[:,t]); dW=words(Q); dA=row(dW,0,0)
    assert s.simplify(A*dA+dA*A)==s.zeros(16)
    vals=[]
    for idx,j in enumerate(events):
        value=row(W,j//4,(j%4)//2)
        dvalue=row(dW,j//4,(j%4)//2)
        u=base[idx]
        du=dvalue.H*A*psi+value.H*dA*psi
        numerator=s.rem(s.expand((du.conjugate().T*u+u.conjugate().T*du)[0]),mod,T)
        denominator=s.rem(den[idx],mod,T)
        vals.append(s.cancel(numerator/denominator))
    jets.append(vals)
J=s.Matrix(jets).T
want=s.Matrix([[0,-s.Rational(4,3),0],
       [s.Rational(16,9),-s.Rational(125,18),s.Rational(5,36)],
       [-16*T**3/13-s.Rational(9,26),32*T**3/13-s.Rational(1,2),
        -16*T**3/13-s.Rational(145,52)]])
assert s.rem(s.together(J.det()-want.det()).as_numer_denom()[0],mod,T)==0
assert s.simplify(J-want)==s.zeros(3)
det=- (1888*T**3+4595)/702
assert s.simplify(J.det()-det)==0
ell=s.Matrix([0,1,-1,1]);Qstar=ell*ell.T
assert Qstar==sum((symmetric(N[:,t]) for t in range(3)),s.zeros(4))
assert s.simplify(Qstar*eta*k)==s.zeros(4,1)
assert J*s.ones(3,1)==s.Matrix([-s.Rational(4,3),
                                -s.Rational(181,36),-s.Rational(189,52)])
# Genuine normalized Jones initial state psi/sqrt2 and two TRUE Kraus
# operators K00=(1-2p² A²)I and K_{j,port1}=-2 a p Q_j† A.
B0=1-s.Rational(9,320)*p*p
q00=B0**4
raw=(s.Rational(243,1024000),s.Rational(81,1280000),
     s.Rational(117,1280000))
for d,expect in zip(den,raw):
    assert s.rem(d-expect,mod,T)==0
q0j=[2*p**3*B0**2*d for d in raw]
assert all(float(s.N(q.subs(T,0.7861513777574233)))>0 for q in [q00]+q0j)
# q00 derivative zero for every screened direction because A dA+dA A=0.
# Thus J is EXACT Jacobian of log(q_(0,j)/q_(0,0)).
print("PASS EXACT ORIGINAL full128 Jones Walsh Julia two-round 3x3 log-odds Jacobian")
print("det =",s.factor(J.det()))
print("single all-order cost-dark metric Qstar yields scores",list(J*s.ones(3,1)))
print("actual baseline two-round probabilities",q0j,"q00",q00)
print("FIREWALL: Book03 physical Cost-Info path-weight selection NOT derived.")
