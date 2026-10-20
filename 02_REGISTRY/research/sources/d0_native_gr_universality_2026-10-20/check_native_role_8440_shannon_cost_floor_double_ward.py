#!/usr/bin/env python3
"""Original physical-carrier two-Ward native no-go:
4D Role L2 all16 sites/64 shared SO links/96 real plaquettes,
all original K9,11,13 8440 based Book two-/three-return histories,
genuine full17 Golden/Bell Shannon, literal repeated-root vertex Info.
Any C>=1 smooth two-sided saturated primitive Cost has C'=0,C''>=0;
cannot repair BOTH orientation first star and vertical second Book source.
Not a no-go for compulsory full H+J+R G0 action (not selected).
"""
import math
import itertools
import numpy as np
p=(math.sqrt(5)-1)/2; phi=1/p;ell=math.log(phi)
h=1/4096
def golden17(t):
 m=(1+math.cos(t))/2;v=math.sin(t)/math.sqrt(2)
 k=h*p**4/24
 qq=[k*m*m]*10+[k*(m+v)**2,k*(m-v)**2]
 gg=h*p**4-sum(qq)
 gb=h*p*p*(1-p*p);bg=h*p**3
 bb=h*(1-p**4-p*p*(1-p*p)-p**3)
 qq+= [gg,gb,bg,bb,1-h]
 assert len(qq)==17 and min(qq)>0 and abs(sum(qq)-1)<1e-13
 return qq
def H17(t):return -sum(q*math.log(q) for q in golden17(t))/ell
def H96(t):return 90*H17(0)+6*H17(t)
H2=-6*h*p**4/ell*(5*math.log(12)/12+1/6)
assert H2<0
assert abs((H96(.001)-2*H96(0)+H96(-.001))/.001**2-H2)<1e-6

# Genuine native Role L=2 geometry with FOUR SHARED 4x4 links / site.
def ee(i,j):
 M=np.zeros((4,4));M[i,j]=1;return M
ident=np.eye(4)
eta=ee(0,1)+ee(1,0)-ee(2,2)-ee(3,3)
J=ee(2,3)-ee(3,2); JJ=J@J
pairs=list(itertools.combinations(range(4),2))
def sign(ar):return (-1)**sum(ar[i]>ar[j] for i in range(4) for j in range(i+1,4))
def group(t):return ident+math.sin(t)*J+(1-math.cos(t))*JJ
def inverse(A):return eta@A.T@eta
def star(t,linkrole):
 links=[[ident.copy() for _ in range(4)] for _ in range(16)]
 links[0][linkrole]=group(t)
 cof=[ident.copy() for _ in range(16)]
 cof[0]=1.25*ident
 f=np.zeros(16);changed=0
 for x in range(16):
  for r,s in pairs:
   P=links[x][r]@links[x^(1<<r)][s]@inverse(links[x^(1<<s)][r])@inverse(links[x][s])
   F=(P-inverse(P))/2
   if np.max(abs(P-ident))>1e-12:changed+=1
   u,v=[k for k in range(4) if k not in (r,s)]
   C=F@eta
   ff=0.
   for a,b in pairs:
    c,d=[k for k in range(4) if k not in (a,b)]
    ff+=sign((a,b,c,d))*(cof[x][a,u]*cof[x][b,v]-cof[x][b,u]*cof[x][a,v])*C[c,d]
   f[x]+=sign((r,s,u,v))*ff
 return f,changed
for t in (0,.08,-.11,.2):
 f,k=star(t,0);assert max(abs(f))<1e-13
 if t:assert k==6
step=1e-5
geom=(star(step,2)[0]-star(-step,2)[0])/(2*step)
assert abs(geom[0]+25/16)<1e-9
assert abs(geom[8]-1)<1e-9
assert abs(sum(geom)+9/16)<1e-9
assert star(step,2)[1]==6

# ACTUAL native complete scene 33/718 and all8440 rooted 2-/3-step
# histories, with node book Info charged INCLUDING repeated v0.
zone=[0]*9+[1]*11+[2]*13
edges=[(u,v) for u in range(33) for v in range(33) if zone[u]!=zone[v]]
assert len(edges)==718
paths=[]
for u,v in edges:
 paths.append((u,v,u))
 for w in range(33):
  if len({zone[u],zone[v],zone[w]})==3:
   paths.append((u,v,w,u))
assert len(paths)==8440
n=np.array([len(z)-1 for z in paths],dtype=float)
visits=n+1
clock=np.where(n==2,p,p*p)
# Fixed Golden blank attempt priors; no postselection over the 17 flags.
h0=H96(0)
w0=clock*np.power(p,n)*np.power(phi,h0*visits)
pi=w0/w0.sum()
ev=float(pi@visits)
assert 3<ev<4
# Each real primitive edge receives independently admissible C(t)=1+alpha_e t².
alpha={(u,v):(0 if (u+v)%4==0 else (1+(7*u+11*v)%13)/1800) for u,v in edges}
ac=np.array([sum(alpha[u,v] for u,v in zip(path,path[1:])) for path in paths])
cost_second=float(pi@(2*ac))
A2=-ev*H2+cost_second
minA2=-ev*H2
assert minA2>3*(-H2)>0 and cost_second>=0
def fullBook(t,with_cost=True):
 price=n + (t*t*ac if with_cost else 0)-visits*H96(t)
 lw=np.log(clock)-ell*price
 mx=float(np.max(lw))
 return -(mx+math.log(float(np.exp(lw-mx).sum())))/ell
for dt in (.01,.004,.002):
 measured=(fullBook(dt)-2*fullBook(0)+fullBook(-dt))/dt**2
 pure=(fullBook(dt,False)-2*fullBook(0,False)+fullBook(-dt,False))/dt**2
 assert abs(measured-A2)<2e-7
 assert abs(pure-minA2)<2e-7
assert abs((fullBook(step)-fullBook(-step))/(2*step))<1e-8
# SAME Shannon even for Role2; Cost-floor first source still zero while
# true nonconstant-coframe Einstein source has total first jet -9/16.
assert abs(H96(.1)-H96(-.1))<1e-12

print('PASS original Role 16 sites, 64 shared links, all96 true based faces')
print('PASS star-flat Role0 J23 source ALL jets exactly zero')
print('PASS Role2 J23 NONZERO fully integrated Palatini first source = -9/16')
print('PASS Golden17 complete positive 16 Bell herald + failure, all96 faces')
print('PASS genuine 718 directed native scene +8440 complete based histories')
print('PASS literal Book repeated closing vertex Info, Golden p and p² clocks')
print('PASS exact native full96 Golden17 H_second =',H2)
print('PASS full8440 Book minimum second source at quantum Cost floor =',minA2)
print('PASS full8440 heterogeneous admissible Cost second source =',A2)
print('PASS STRICT analytic no-go for ALL smooth primitive Cost-only repairs')
print('         while physical Info selected as full Golden17 pointer Shannon')
print('FIREWALL: true compulsory native H+J+R/oldRIGHT/full archive not selected')
print('GR_closed=false')
