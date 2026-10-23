#!/usr/bin/env python3
"""Exact native full128 Walsh/Julia/Golden Jones two-tick BLANK-anchored odds.
No new physical detector, event, Book action or GR closure.
"""
import sympy as s
T=s.symbols('a',real=True);p=T*T
nu=s.Rational(3,5);b=s.Rational(4,5);ph=[s.I,s.I,-1,-s.I]
order=[0,2,3,1];I=s.eye(16);Z=s.zeros(16)
eta=s.diag(1,-1,-1,-1)
C=[]
for role in range(4):
 m=Z.copy();prior=order[:order.index(role)]
 for bits in range(16):
  if not bits&(1<<role):
   m[bits+(1<<role),bits]=(-1)**sum(bool(bits&(1<<j)) for j in prior)
 C.append(m)
lft=[c*c.T for c in C];rgt=[c.T*c for c in C]
def rootder(proj,delta):
 blocks=[I-proj,proj];eig=[1,b];out=Z.copy()
 for i in range(2):
  for j in range(2):out-=blocks[i]*delta*blocks[j]/(eig[i]+eig[j])
 return out
def words(variation=None):
 out=[[],[]]
 for r in range(4):
  z=ph[r];cr=C[r];v=nu*cr;P=nu*z*cr;Pd=P.H
  L=I+(b-1)*lft[r];R=I+(b-1)*rgt[r]
  if variation is None:rows=[(P,L),(Pd,R),(-v,-L),(-v.T,-R)]
  else:
   H=eta*variation
   dv=nu*sum((H[r,j]*C[j] for j in range(4)),Z.copy())
   dP=z*dv;dPd=dP.H
   dL=rootder(lft[r],dP*Pd+P*dPd)
   dR=rootder(rgt[r],dPd*P+Pd*dP)
   rows=[(dP,dL),(dPd,dR),(-dv,-dL),(-dv.T,-dR)]
  for c0,c1 in rows:
   for _ in range(2):out[0].append(c0);out[1].append(c1)
 return out
W=words()
def row(W,label,comp):
 return sum(((-1)**((label&j).bit_count())*W[comp][j] for j in range(32)),Z.copy())/32
A=row(W,0,0)
assert all(s.simplify(x)==0 for x in A*A-(A*A)[0,0]*I)
psi=s.zeros(16,1);psi[0]=psi[14]=-T;psi[1]=psi[15]=p
ks=(17,27,59)
base=[];den=[]
for k in ks:
 u=row(W,k//4,(k%4)//2).H*A*psi
 base.append(u);den.append(s.expand((u.conjugate().T*u)[0]))
Pmod=T**4+T*T-1
Qbasis=s.Matrix([[1,-2,1],[-1,1,0],[0,1,-1],[0,-1,1],
  [1,0,0],[0,-1,0],[0,1,0],[0,0,1],[0,0,-1],[0,0,1]])
columns=[]
for j in range(3):
 Q=s.zeros(4);idx=0
 for r in range(4):
  for k in range(r,4):Q[r,k]=Q[k,r]=Qbasis[idx,j];idx+=1
 Wd=words(Q);dA=row(Wd,0,0)
 assert all(s.simplify(x)==0 for x in A*dA+dA*A)
 scores=[]
 for i,k in enumerate(ks):
  Tj=row(W,k//4,(k%4)//2)
  dTj=row(Wd,k//4,(k%4)//2)
  u=base[i];du=dTj.H*A*psi+Tj.H*dA*psi
  numerator=s.rem(s.expand((du.conjugate().T*u+u.conjugate().T*du)[0]),Pmod,T)
  denominator=s.rem(den[i],Pmod,T)
  scores.append(s.cancel(numerator/denominator))
 columns.append(scores)
 print('native metric Q',j,'true likelihood scores',scores,flush=True)
J=s.Matrix(columns).T
expected=s.Matrix([[0,-s.Rational(4,3),0],
 [s.Rational(16,9),-s.Rational(125,18),s.Rational(5,36)],
 [-16*T**3/13-s.Rational(9,26),32*T**3/13-s.Rational(1,2),
 -16*T**3/13-s.Rational(145,52)]])
assert all(s.simplify(x)==0 for x in J-expected)
assert s.simplify(J.det()+(1888*T**3+4595)/702)==0
assert s.simplify(A*A-s.Rational(9,640)*I)==s.zeros(16)
B0=1-s.Rational(9,320)*p**2
assert (B0-(1-2*p*p*(A*A)[0,0])).expand()==0
assert s.rem((psi.T*psi)[0]-2,Pmod,T)==0
# Jones physically normalized by 1/sqrt(2); two true blank Kraus K00=B0 I.
qblank=s.expand(B0**4)
known=[s.Rational(243,1024000),s.Rational(81,1280000),s.Rational(117,1280000)]
qpositive=[]
for raw,check in zip(den,known):
 assert s.rem(raw-check,Pmod,T)==0
 # true original nonblank port1 K_k=-2 a p Q_k^* A
 qpositive.append(2*p**3*B0**2*check)
anum=0.7861513777574233
assert float(qblank.subs(T,anum))>0
assert all(float(q.subs(T,anum))>0 for q in qpositive)
# All three blank odds gradients are J itself, because q_blank'=0 on screen.
assert all(s.simplify(x)==0 for x in
 J*s.ones(3,1)-s.Matrix([-s.Rational(4,3),-s.Rational(181,36),
                         -s.Rational(189,52)]))
print('PASS true original 128 Kraus source on 3 screened metric directions')
print('PASS blank history probability:',s.factor(qblank))
print('PASS normalized events (0,17),(0,27),(0,59):',qpositive)
print('PASS BLANK-ANCHORED 3 odds determinant:',s.factor(J.det()))
print('BOOK03 relative source only IF w_gamma=q_gamma*N: -d log(q_i/q_blank)/log(phi)')
print('GR_closed=false')
