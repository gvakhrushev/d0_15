#!/usr/bin/env python3
"""Exact independent finite observer/Ward reduction; no repo files mutated."""
import json
import sympy as s
eta=s.diag(1,-1,-1,-1)
I4=s.eye(4); I16=s.eye(16)
C=[]
for a in range(4):
 Q=s.zeros(16)
 for m in range(16):
  if not (m>>a)&1: Q[m|(1<<a),m]=(-1)**((m&((1<<a)-1)).bit_count())
 C.append(Q)
def create(v): return sum((v[a]*C[a] for a in range(4)),s.zeros(16))
def gamma(X): return sum((X[a,b]*C[a]*C[b].T for a in range(4) for b in range(4)),s.zeros(16))
def exterior(A):
 Q=s.zeros(16); idx=[[a for a in range(4) if (m>>a)&1] for m in range(16)]
 for i,aa in enumerate(idx):
  for j,bb in enumerate(idx):
   if len(aa)==len(bb): Q[i,j]=A.extract(aa,bb).det()
 return Q
def L(n):
 g=n[0]; v=n[1:4,0]
 Q=s.eye(4);Q[0,0]=g
 Q[0,1:4]=-v.T;Q[1:4,0]=-v;Q[1:4,1:4]+=v*v.T/(g+1)
 return Q
def dL(n,dn):
 g=n[0];v=n[1:4,0];dg=dn[0];dv=dn[1:4,0]
 Q=s.zeros(4);Q[0,0]=dg;Q[0,1:4]=-dv.T;Q[1:4,0]=-dv
 Q[1:4,1:4]=(dv*v.T+v*dv.T)/(g+1)-v*v.T*dg/(g+1)**2
 return Q
def boost(j,g,w):
 Q=s.eye(4);Q[0,0]=Q[j,j]=g;Q[0,j]=Q[j,0]=w;return Q
def rotation(i,j,c,t):
 Q=s.eye(4);Q[i,i]=Q[j,j]=c;Q[i,j]=-t;Q[j,i]=t;return Q
n=[s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0]),s.Matrix([s.Rational(13,12),0,s.Rational(5,12),0])]
ls=[L(q) for q in n]
for nn,ll in zip(n,ls):
 h=-eta+2*eta*nn*nn.T*eta
 assert ll.T*ll==h and ll.T*eta*ll==eta and ll.det()==1 and ll*nn==I4[:,0]
V=[I4/5,I4/7];V[0][1,2]=s.Rational(1,35);V[1][2,3]=s.Rational(1,49)
A=[[boost(1,s.Rational(5,4),s.Rational(3,4)),rotation(1,2,s.Rational(3,5),s.Rational(4,5)),I4,I4],
   [rotation(2,3,s.Rational(5,13),s.Rational(12,13)),boost(3,s.Rational(17,15),s.Rational(8,15)),I4,I4]]
def forward(V,A):
 Q=s.zeros(32)
 for x in range(2):
  y=1-x
  for r in range(4):
   q=create(V[x][:,r]);Q[16*x:16*x+16,16*y:16*y+16]+=q*exterior(A[x][r]);Q[16*x:16*x+16,16*x:16*x+16]-=q
 return Q
def whites(V,A,ls):
 return [ls[x]*V[x] for x in range(2)],[[ls[x]*a*ls[1-x].inv() for a in A[x]] for x in range(2)]
u,M=whites(V,A,ls)
draw=forward(V,A); W=s.diag(*[exterior(a) for a in ls]);G=W.T*W
Dh=W*(draw+G.inv()*draw.T*G)*W.inv();dw=forward(u,M)
assert Dh==dw+dw.T
# A nonconstant, noncommuting local proper Lorentz change.
S=[boost(2,s.Rational(5,4),s.Rational(3,4)),boost(1,s.Rational(13,12),s.Rational(5,12))]
n2=[S[x]*n[x] for x in range(2)];ls2=[L(q) for q in n2]
V2=[S[x]*V[x] for x in range(2)]
A2=[[S[x]*a*S[1-x].inv() for a in A[x]] for x in range(2)]
u2,M2=whites(V2,A2,ls2);d2=forward(u2,M2);D2=d2+d2.T
O=[ls2[x]*S[x]*ls[x].inv() for x in range(2)]
assert all(a.T*a==I4 for a in O) and any(a!=I4 for a in O)
T=s.diag(*[exterior(a) for a in O]);assert D2==T*Dh*T.T and T.T*T==s.eye(32)
amp=s.zeros(32,2);amp[0,0]=1/s.sqrt(2);amp[18,1]=1/s.sqrt(2)
assert amp.T*amp==s.eye(2)/2 and (T*amp).T*T*amp==s.eye(2)/2
assert s.trace(amp.T*Dh**2*amp)==s.trace((T*amp).T*D2**2*(T*amp))
# Every independent observer direction has a canonical K=0 Lorentz lift.
checks=0
for xx in range(2):
 for j in range(1,4):
  dn=s.zeros(4,1);dn[j]=1;dn[0]=n[xx][j]/n[xx][0]
  dl=[s.zeros(4),s.zeros(4)];dl[xx]=dL(n[xx],dn)
  X=[-ls[x].inv()*dl[x] for x in range(2)]
  assert X[xx]*n[xx]==dn and X[xx].T*eta+eta*X[xx]==s.zeros(4)
  # K=Gamma(dL L^-1+L X L^-1)=0 before any prep equation.
  assert dl[xx]*ls[xx].inv()+ls[xx]*X[xx]*ls[xx].inv()==s.zeros(4)
  du_obs=[dl[x]*V[x] for x in range(2)]
  du_geo=[ls[x]*X[x]*V[x] for x in range(2)]
  for x in range(2):
   y=1-x
   assert du_obs[x]+du_geo[x]==s.zeros(4)
   for r in range(4):
    dmobs=dl[x]*A[x][r]*ls[y].inv()-M[x][r]*dl[y]*ls[y].inv()
    dmgeo=ls[x]*(X[x]*A[x][r]-A[x][r]*X[y])*ls[y].inv()
    assert dmobs+dmgeo==s.zeros(4)
    # All16 exterior transported-creation derivative rows cancel.
    dliftobs=gamma(dmobs*M[x][r].inv())*exterior(M[x][r])
    dliftgeo=gamma(dmgeo*M[x][r].inv())*exterior(M[x][r])
    q=(create(du_obs[x][:,r])+create(du_geo[x][:,r]))*exterior(M[x][r])+create(u[x][:,r])*(dliftobs+dliftgeo)
    assert q==s.zeros(16)
  checks+=1
# Nonzero observer partial source: freezing it would be false.
q=s.Matrix([1,-1,0,0])/s.sqrt(2);nu=s.Rational(1,4);z=s.I
B=s.zeros(4);B[0,1]=B[1,0]=1
Q=create(nu*q)*(z-1);DD=Q+Q.conjugate().T
Qn=create(-B*nu*q)*(z-1);Dn=Qn+Qn.conjugate().T
Qg=create(B*nu*q)*(z-1);Dg=Qg+Qg.conjugate().T
vac=I16[:,0];R=(vac.T*DD**2*vac)[0]
Rn=s.simplify((vac.T*(DD*Dn+Dn*DD)*vac)[0]);Rg=s.simplify((vac.T*(DD*Dg+Dg*DD)*vac)[0])
assert R==s.Rational(1,8) and Rn==2*R and Rg==-2*R
print(json.dumps({'status':'PASS','full_CAR_components':16,'nonconstant_sites':2,'all_four_roles':True,'exact_moving_adjoint_whitening':True,'noncommuting_Lorentz_full_D_covariance':True,'fixed_RIGHT_Gram_gauge_invariant':True,'canonical_observer_directions':checks,'K_zero_before_preparation_Euler':True,'observer_control_R':str(R),'observer_partial_derivative':str(Rn),'compensating_coframe_derivative':str(Rg),'scope':'Exact observer/Ward redundancy of declared Lorentz-covariant full HJR; not joint root, native admission or GR.'},indent=2))
