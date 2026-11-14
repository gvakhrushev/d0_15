#!/usr/bin/env python3
"""Independent source-weight and rectangular-power SITE angle replay."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'round42/.deps'))
try:import gmpy2 as g
except ImportError:g=None
import site_targets as t
if g:
 class Fast(t.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
 t.Dyadic=Fast
with gzip.open(P/'SITE_ANGLE_LIBRARY.json.gz','rt') as f:j=json.load(f)
for f,h in j['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
counts,specs,nodes=t.tree_names();assert j['tree_nodes']==nodes and len(counts)==256 and len(nodes)==255 and len(specs)==165
orig=t.Dyadic(7168);iv=t.Dyadic(8448);S=iv.scale;fac=1<<(8448-7168);R=iv.rational
c=iv.sqrt(R(counts[0],sum(counts)));u0=iv.div(iv.add(R(1),c),R(2));den=iv.mul(R(2*sum(counts)),iv.add(R(1),c));weights=[u0]+[iv.div(R(N),den) for N in counts[1:]]
def summ(v):
 z=R(0)
 for x in v:z=iv.add(z,x)
 return z
def digest(a,b):return sha256(('|'.join(hex(int(v)) for v in (*a,*b))).encode()).hexdigest()
def err(a,b,c,d):return max(abs(a[0]-c[1]),abs(a[1]-c[0]))+max(abs(b[0]-d[1]),abs(b[1]-d[0]))
# Independently compute masses directly from all 256 u_i^2, rather than B45's
# common-denominator formula; check every node and each saved source digest.
independent={}
for node in nodes:
 level=node['level'];w=1<<(8-level);start=node['prefix']*w;left=summ(weights[start:start+w//2]);right=summ(weights[start+w//2:start+w]);total=iv.add(left,right);got=(iv.sqrt(iv.div(left,total)),iv.sqrt(iv.div(right,total)))
 sp=specs[node['angle_id']];expected=t.targets(orig,sp,counts);stored=j['angles'][node['angle_id']];assert stored['spec']==sp and stored['target_sha256']==digest(*expected)
 for old,new in zip(expected,got):assert old[0]*fac<=new[0] and new[1]<=old[1]*fac,(node['level'],node['prefix'])
 independent.setdefault(node['angle_id'],got)
# Rectangular complex intervals, no complex-ball code and no floating point.
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def mul(a,b):
 v=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]);return min(v)>>8448,-((-max(v))>>8448)
def cmul(a,b):return add(mul(a[0],b[0]),neg(mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0]))
root=g.isqrt if g else isqrt;s5=root(5*S*S);pp=((s5-S)//2,-((-(s5+1-S))//2));aa=(root(pp[0]*S),root(pp[1]*S)+1);powers=[(aa,pp)]
for _ in range(3364):powers.append(cmul(powers[-1],powers[-1]))
def power(k):
 z=((S,S),(0,0));i=0
 while k:
  if k&1:z=cmul(z,powers[i])
  k>>=1;i+=1
 return z
for name,rec in j['angles'].items():
 a,b=power(int(rec['k'])<<8);cc,ss=independent[name];e=err(a,b,cc,ss);assert e<=S>>3264 and e<=int(rec['error_numerator_hex'],16)*fac,name
phase=j['reflection_phase'];a,b=power(int(phase['k'])<<8);zero=R(0);minus=R(-1);e=err(a,b,minus,zero);assert e<=S>>3264 and e<=int(phase['error_numerator_hex'],16)*fac
out={'status':'PASS_INDEPENDENT_SITE_TREE_TARGETS_AND_RECTANGULAR_POWERS','library_sha256':sha256((P/'SITE_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'tree_nodes_checked':len(nodes),'distinct_tree_angles':len(independent),'phase_angles':1,'source_bit_mapping_checked':True,'independent_bits':8448,'ball_method_used':False,'candidate_used':False,'float_used':False,'GR_closed':False}
(P/'SITE_ANGLE_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
