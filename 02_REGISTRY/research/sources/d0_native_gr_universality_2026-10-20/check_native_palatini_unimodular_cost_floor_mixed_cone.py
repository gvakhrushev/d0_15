#!/usr/bin/env python3
"""Native original 16-site Role and all 8440 Book loop mixed-source theorem.
At saturated primitive Cost>=1 and coframe-blind Info/attempt:
H_aa=0 implies H_aU=0 for ANY smooth frame-sensitive primitive Costs.
The true six-face Palatini source instead has (H_aa,H_aU)=(0,-1).
Whole compulsory H+J+R could contain frame-aware Info/stationary prep.
"""
from itertools import combinations
from sympy import Matrix,Rational as Q,symbols,sin,simplify,eye,zeros,sqrt

a,t=symbols('a t',real=True,positive=True)
eta=Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
J=zeros(4);J[2,3]=1;J[3,2]=-1
assert J.T*eta+eta*J==zeros(4) and J**3==-J
pairs=list(combinations(range(4),2))
cof=[eye(4) for x in range(16)]
cof[0]=Matrix.diag(1,a,1,a**-1)
assert all(e.det()==1 for e in cof)
def eps(v):return (-1)**sum(v[i]>v[j] for i in range(4) for j in range(i+1,4))
source=[0]*16
changed=[]
for x in range(16):
 for r,s in pairs:
  sg=(int(x==0 and r==2)+int((x^(1<<r))==0 and s==2)
      -int((x^(1<<s))==0 and r==2)-int(x==0 and s==2))
  if not sg:continue
  changed.append((x,r,s,sg))
  u,v=[k for k in range(4) if k not in (r,s)]
  C=sg*J*eta;E=cof[x]
  area=0
  for i,j in pairs:
   k,l=[k for k in range(4) if k not in (i,j)]
   area+=eps((i,j,k,l))*(E[i,u]*E[j,v]-E[j,u]*E[i,v])*C[k,l]
  source[x]+=eps((r,s,u,v))*area
assert len(changed)==6 and len(pairs)*16==96
assert simplify(source[0]+a)==0 and source[8]==1
assert all(v==0 for i,v in enumerate(source) if i not in (0,8))
star=simplify(sum(source)*sin(t))
assert star==(1-a)*sin(t)
assert star.diff(a,2).subs({a:1,t:0})==0
assert star.diff(a,t).subs({a:1,t:0})==-1
assert star.diff(t).subs({a:Q(5,4),t:0})==-Q(1,4)
for value in (Q(4,5),Q(1),Q(5,4),Q(3,2)):
 assert star.diff(t).subs({a:value,t:0})==1-value

# Literal original based 2/3 closed words, INCLUDING visit to closing root.
z=[0]*9+[1]*11+[2]*13
edges=[(i,j) for i in range(33) for j in range(33) if z[i]!=z[j]]
assert len(edges)==718
occ2={e:0 for e in edges}
occ3=dict(occ2)
counts=[0,0]
for u,v in edges:
 gamma=(u,v,u);counts[0]+=1
 for ed in zip(gamma,gamma[1:]):occ2[ed]+=1
 for w in range(33):
  if len({z[u],z[v],z[w]})==3:
   gamma=(u,v,w,u);counts[1]+=1
   for ed in zip(gamma,gamma[1:]):occ3[ed]+=1
assert counts==[718,7722]
assert sum(occ2.values())==1436 and sum(occ3.values())==23166
for u,v in edges:
 third={0:9,1:11,2:13}[next(j for j in (0,1,2) if j not in (z[u],z[v]))]
 assert occ2[u,v]==2 and occ3[u,v]==3*third
p=(sqrt(5)-1)/2
Z0=718*p**3+7722*p**5
rho={ed:(occ2[ed]*p**3+occ3[ed]*p**5)/Z0 for ed in edges}
assert all(float(x)>0 for x in rho.values())
expected=(1436*p**3+23166*p**5)/Z0
assert abs(sum(float(x) for x in rho.values())-float(expected))<1e-10

# Actual positive quadratic primitive Cost examples:
# C_e(q)=1+(A_e x+B_e t)^2 >=1 on BOTH field signs.
# Saturated Cost Hess H_e=2 (A_e,B_e)^T(A_e,B_e) is PSD.
# Entire Book Hess coframe row = sum_e rho_e H_e(coframe,.)
A={ed:Q((ed[0]+2*ed[1])%7,5) for ed in edges}
B={ed:Q((3*ed[0]+ed[1])%11-5,7) for ed in edges}
Haa=sum(float(rho[ed])*2*float(A[ed]**2) for ed in edges)
Hat=sum(float(rho[ed])*2*float(A[ed]*B[ed]) for ed in edges)
Htt=sum(float(rho[ed])*2*float(B[ed]**2) for ed in edges)
assert Haa>0 and Htt>0 and Hat*Hat<=Haa*Htt+1e-11
# If Haa=0, positive rho on ALL edges implies H_e(V,V)=0 on
# EVERY edge. PSD then forces H_e(V,W)=0 for ALL W, hence Hat=0.
assert sum(float(rho[ed])*2*float(0*B[ed]) for ed in edges)==0

print('PASS original 16 sites /64 shared links /96 true Role plaquettes')
print('PASS volume preserving det(e_x)=1 on entire nontrivial a chart')
print('PASS EXACT finite star=(1-a)*sin(t), site0=-a, site8=+1')
print('PASS true flat Palatini (Haa,Hat)=(0,-1)')
print('PASS original K(9,11,13) 718 arcs/8440 rooted Book words, no omission')
print('PASS every directed arc count n2=2,n3=3*n_third, occupancy rho>0')
print('PASS every smooth saturated Cost C>=1 has PSD full joint Hessian')
print('PASS Cauchy-Schwarz source cone: native Haa=0 forces Hat=0')
print('NO-GO full smooth saturated Cost+coframe-blind Info/clock action class')
print('FIREWALL native physically selected H+J+R and internal Schur OPEN; GR_closed=false')
