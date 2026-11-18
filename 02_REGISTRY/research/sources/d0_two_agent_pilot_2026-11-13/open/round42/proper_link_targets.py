#!/usr/bin/env python3
"""Exact source expressions and outward dyadic proper-link factor targets.

No float SVD, approximate family deduplication, or native gate claim.
"""
from pathlib import Path
from itertools import product
import importlib.util,sys
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
old=load('b42_golden_exact',D/'round18/material_targets.py');loc=load('b42_locality',D/'round19/julia_locality.py');Dyadic=old.Dyadic
GEN=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
def catalogue():
 specs={};banks={}
 for bank,rows in loc.catalogue().items():
  out=[]
  for row in loc.sectors(rows):
   if row['kind']!='proper_link':continue
   role=row['direction'];x=row['site'];ids=row['SAM_indices'];pat=row['SAM_pattern']
   if bank=='f':
    bits=None if not ids else tuple(dict((tuple(loc.COORD[i]['generator']),b) for i,b in zip(ids,pat))[g] for g in GEN)
    xy=(x[2],x[3]) if role==0 else None
    if xy is None and bits is None:name='identity';spec={'type':'identity'}
    else:
     name='f_'+('base_'+str(xy[0])+str(xy[1]) if xy else 'base_identity')+('_fixed' if bits is None else '_'+''.join(map(str,bits)))
     spec={'type':'f','xy':xy,'bits':bits}
   elif bank in ('x+','x-') and role==0:name='ref_boost';spec={'type':'ref_boost'}
   elif bank in ('x+','x-') and role==1:
    name='ref_rot_plus' if bank=='x+' else 'ref_rot_minus';spec={'type':name}
   else:name='identity';spec={'type':'identity'}
   assert name not in specs or specs[name]==spec;specs[name]=spec
   out.append({'address':row['a'],'SAM_indices':ids,'SAM_pattern':pat,'family_id':name})
  banks[bank]=out
 assert sum(map(len,banks.values()))==23296
 return specs,banks
class Interval:
 def __init__(self,bits):
  self.iv=Dyadic(bits);self.R=self.iv.rational;self.S=self.iv.scale;self.bits=bits;self.c=old.constants(self.iv);self.c['pi']=self.iv.pi()
  assert self.c['k0'][1]<24*self.S and self.c['pi'][1]*7<22*self.S
  self.one=self.R(1);self.zero=self.R(0)
 def add(self,a,b):return self.iv.add(a,b)
 def sub(self,a,b):return self.iv.sub(a,b)
 def neg(self,a):return self.iv.neg(a)
 def mul(self,a,b):return self.iv.mul(a,b)
 def div(self,a,b):return self.iv.div(a,b)
 def sqrt(self,a):return self.iv.sqrt((max(0,a[0]),a[1]))
 def square(self,a):
  lo=0 if a[0]<=0<=a[1] else min(a[0]*a[0],a[1]*a[1]);hi=max(a[0]*a[0],a[1]*a[1]);return lo//self.S,-((-hi)//self.S)
 def sum(self,items):
  a=self.zero
  for x in items:a=self.add(a,x)
  return a
 def eye(self,n):return [[self.one if i==j else self.zero for j in range(n)] for i in range(n)]
 def transpose(self,a):return [list(x) for x in zip(*a)]
 def mm(self,a,b):return [[self.sum(self.mul(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
 def madd(self,a,b):return [[self.add(x,y) for x,y in zip(u,v)] for u,v in zip(a,b)]
 def mscale(self,a,b):return [[self.mul(x,b) for x in row] for row in a]
 def absbounds(self,a):return (0 if a[0]<=0<=a[1] else min(abs(a[0]),abs(a[1]))),max(abs(a[0]),abs(a[1]))
 def scalar(self,a,n):return self.mul(a,self.R(n))
 def transform(self):
  z=self.zero;one=self.one;q=self.div(one,self.sqrt(self.R(2)))
  return [[q,q,z,z],[q,self.neg(q),z,z],[z,z,one,z],[z,z,z,self.neg(one)]]
 def baseline(self,xy):
  U=self.eye(4)
  if xy is None:return U
  x,y=xy; pi2=self.square(self.c['pi']); k=self.c['k0'];A=self.mul(self.mul(k,pi2),self.R(1,2500));
  kx=self.mul(self.add(A,self.R(3,100)),self.R(2*x-1,32));ky=self.mul(self.sub(A,self.R(3,100)),self.R(2*y-1,32))
  U[1][2]=self.neg(kx);U[2][0]=self.neg(kx);U[1][3]=self.neg(ky);U[3][0]=self.neg(ky);U[1][0]=self.div(self.add(self.square(kx),self.square(ky)),self.R(2))
  return U
 def exp_theta(self,bits):
  eta=[[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]];theta=[[self.zero for _ in range(4)] for _ in range(4)];p2=self.square(self.c['p'])
  for (i,j),b in zip(GEN,bits):
   d=self.mul(self.R(1,2**30),self.sub(self.R(b),p2))
   for k in range(4):
    if eta[k][i]:theta[k][j]=self.add(theta[k][j],self.scalar(d,eta[k][i]))
    if eta[k][j]:theta[k][i]=self.sub(theta[k][i],self.scalar(d,eta[k][j]))
  term=self.eye(4);out=term;fact=1;n=0
  # ||theta||_infty <= 6*2^-30 < 2^-27.
  # Tail <= 2 * (2^-27)^(n+1)/(n+1)!; bound < 2^-(bits+16).
  while True:
   n+=1;fact*=n;term=self.mscale(self.mm(term,theta),self.R(1,n));out=self.madd(out,term)
   if 27*(n+1)+(fact*(n+1)).bit_length()-1 >= self.bits+18:break
  # Tail < 1 ulp; widen each entry by one.
  return [[(v[0]-1,v[1]+1) for v in row] for row in out],n
 def source(self,spec,exp_cache):
  typ=spec['type'];I=self.eye(4)
  if typ=='identity':return I
  if typ=='f':
   base=self.baseline(spec['xy']);bits=spec['bits']
   if bits is None:return base
   if bits not in exp_cache:exp_cache[bits]=self.exp_theta(bits)
   return self.mm(exp_cache[bits][0],base)
  T=self.transform();U=self.eye(4)
  if typ=='ref_boost':
   # Rational boost h=1/4: cosh=65/63, sinh=16/63.
   U[0][0]=U[2][2]=self.R(65,63);U[0][2]=U[2][0]=self.R(16,63)
  else:
   assert typ in ('ref_rot_plus','ref_rot_minus');vb=self.R(1,80);b2=self.square(vb);den=self.add(self.one,b2)
   c=self.div(self.sub(self.one,b2),den);s=self.div(self.scalar(vb,2),den)
   if typ=='ref_rot_minus':s=self.neg(s)
   U[1][1]=U[2][2]=c;U[1][2]=s;U[2][1]=self.neg(s)
  return self.mm(self.mm(T,U),self.transpose(T))

def columns(iv,a,j):return [a[i][j] for i in range(len(a))]
def divide_signed(iv,a,b):
 assert b[0]>0
 return iv.div(a,b)
def factor(iv,spec,exp_cache):
 R=iv.R;S=iv.S;one=iv.one;zero=iv.zero;U=iv.source(spec,exp_cache)
 if spec['type'] in ('identity','ref_rot_plus','ref_rot_minus'):
  return {'L':iv.eye(4),'R':iv.transpose(U),'dplus':one,'dminus':one,'h':zero,'source':U,'zero_boost_exact':True}
 T=iv.transform();A=iv.mm(iv.mm(iv.transpose(T),U),T)
 sp=[A[j][0] for j in (1,2,3)];h=iv.sqrt(iv.sum(iv.square(x) for x in sp));assert h[0]>0,(spec,'boost lower bound')
 n=[iv.div(x,h) for x in sp]; gamma=iv.sqrt(iv.add(one,iv.square(h)));plus=iv.add(gamma,h);minus=iv.div(one,plus)
 eligible=[j for j,x in enumerate(n) if 4*iv.absbounds(x)[1]<3*S];assert eligible,(spec,'frame')
 j=eligible[0];nv=n[j];root=iv.sqrt(iv.sub(one,iv.square(nv)));assert 2*root[0]>S
 v=[iv.div(iv.sub(one if k==j else zero,iv.mul(nv,n[k])),root) for k in range(3)]
 cross=[iv.sub(iv.mul(n[1],v[2]),iv.mul(n[2],v[1])),iv.sub(iv.mul(n[2],v[0]),iv.mul(n[0],v[2])),iv.sub(iv.mul(n[0],v[1]),iv.mul(n[1],v[0]))]
 O=iv.eye(4)
 for k in range(3):O[k+1][1]=n[k];O[k+1][2]=v[k];O[k+1][3]=cross[k]
 Binv=iv.eye(4);Binv[0][0]=gamma
 for k in range(3):
  Binv[0][k+1]=Binv[k+1][0]=iv.neg(iv.mul(h,n[k]))
  for l in range(3):Binv[k+1][l+1]=iv.add(one if k==l else zero,iv.mul(iv.sub(gamma,one),iv.mul(n[k],n[l])))
 K=iv.mm(Binv,A);P=iv.eye(4);q=iv.div(one,iv.sqrt(R(2)));P[0][0]=P[0][1]=P[1][0]=q;P[1][1]=iv.neg(q);P[3][3]=iv.neg(one)
 L=iv.mm(iv.mm(T,O),P);Rr=iv.mm(iv.mm(iv.mm(T,iv.transpose(K)),O),P)
 return {'L':L,'R':Rr,'dplus':plus,'dminus':minus,'h':h,'source':U,'zero_boost_exact':False,'frame_index':j}

def givens(iv,M,known_identity=False):
 if known_identity:return []
 Q=[row[:] for row in M];out=[];S=iv.S
 for col in range(3):
  candidates=sorted(range(col,4),key=lambda j:sum(iv.absbounds(Q[j][col])),reverse=True)
  # The source expressions may have exact ties; the decisive certificate is
  # the stronger radius bound, established after including the pivot column.
  selected=None
  for candidate in candidates:
   if candidate==col:
    rho=iv.sqrt(iv.square(Q[col][col]))
   else:rho=iv.sqrt(iv.add(iv.square(Q[col][col]),iv.square(Q[candidate][col])))
   if (4-col)*rho[0]*rho[0]>=S*S:selected=candidate;break
  assert selected is not None,('pivot radius unresolved',col,candidates)
  proven_largest=iv.absbounds(Q[selected][col])[0]>=max((iv.absbounds(Q[k][col])[1] for k in range(col,4) if k!=selected),default=0)
  assert proven_largest,('largest pivot unresolved',col,selected)
  rows=([selected] if selected!=col else [])+[j for j in range(3,col,-1) if j!=selected]
  assert len(rows)==3-col
  for j in rows:
   a,b=Q[col][col],Q[j][col];rad=iv.sqrt(iv.add(iv.square(a),iv.square(b)))
   assert (4-col)*rad[0]*rad[0]>=S*S,('Givens radius',col,j)
   co=iv.div(a,rad);si=iv.neg(iv.div(b,rad))
   G=iv.eye(4);G[col][col]=G[j][j]=co;G[j][col]=si;G[col][j]=iv.neg(si)
   Q=iv.mm(G,Q);out.append({'i':col,'j':j,'cos':co,'sin':si,'radius':rad,'selected_pivot':selected,'largest_certified':proven_largest})
  # Exact rotation makes eliminated entries mathematically zero; replacing
  # their outward intervals by [0,0] is sound and prevents width explosion.
  for j in range(col+1,4):Q[j][col]=zero=iv.zero
 return [{'i':x['i'],'j':x['j'],'cos':x['cos'],'sin':iv.neg(x['sin']),'radius':x['radius'],'selected_pivot':x['selected_pivot'],'largest_certified':x['largest_certified']} for x in reversed(out)]

def diagonal_targets(iv,f):
 out={}
 for b0 in (0,1):
  for b1 in (0,1):
   value=iv.one
   if b0:value=iv.mul(value,f['dplus'])
   if b1:value=iv.mul(value,f['dminus'])
   value=iv.div(value,iv.R(2));assert 0<value[0] and value[1]<iv.S
   out[(b0,b1)]={'cos':iv.sqrt(iv.sub(iv.one,iv.square(value))),'sin':iv.neg(value)}
 return out
