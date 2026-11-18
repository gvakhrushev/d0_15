#!/usr/bin/env python3
"""Confirm GMP acceleration and Python-integer fallback give identical bounds."""
from pathlib import Path
import sys,json,gzip
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'.deps'));import gmpy2 as g
import proper_link_targets as p
pure=p.Dyadic
class Fast(pure):
 def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
 def sqrt(self,a):
  assert a[0]>=0;lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
specs,_=p.catalogue();chosen=[next(v for v in specs.values() if v['type']==typ) for typ in ('identity','ref_boost','ref_rot_plus')]
chosen += [next(v for v in specs.values() if v['type']=='f' and v['xy'] is None and v['bits'] is not None),next(v for v in specs.values() if v['type']=='f' and v['xy'] is not None and v['bits'] is not None)]
def all_targets(cls):
 p.Dyadic=cls;iv=p.Interval(7168);cache={};res=[]
 for sp in chosen:
  f=p.factor(iv,sp,cache);L=p.givens(iv,f['L'],sp['type'] in ('identity','ref_rot_plus','ref_rot_minus'));R=p.givens(iv,f['R'],sp['type']=='identity');res.append((f,L,R,p.diagonal_targets(iv,f)))
 return res
regular=all_targets(pure);accelerated=all_targets(Fast);assert regular==accelerated
# Native complex-ball recurrence also matches bit for bit.
with gzip.open(P/'PROPER_LINK_ANGLE_LIBRARY.json.gz','rt') as f:lib=json.load(f)
ks=[int(lib['controlled_X']['k']),int(lib['controlled_X']['phase']['k'])]+[int(r['diagonal']['10']['k']) for r in lib['families'][::167]]
def power(k,cls):
 p.Dyadic=cls;iv=p.Interval(7168);S=iv.S;a=iv.c['sqrtp'];b=iv.c['p'];base=(a[0],b[0],a[1]-a[0]+b[1]-b[0]);acc=(S,0,0);n=k<<23
 def mul(x,y):
  c,s,r=x;C,T,R=y;return ((c*C-s*T)>>7168,(c*T+s*C)>>7168,r+R+((r*R+S-1)>>7168)+2)
 while n:
  if n&1:acc=mul(acc,base)
  n>>=1
  if n:base=mul(base,base)
 return acc
for k in ks:assert power(k,pure)==power(k,Fast)
out={'status':'PASS_PYTHON_INTEGER_FALLBACK_BIT_FOR_BIT','families_at_7168':len(chosen),'power_exponents_at_7168':len(ks),'gmpy2_version':g.version(),'GMP_version':g.mp_version(),'acceleration_is_optional':True,'GR_closed':False}
(P/'PYTHON_FALLBACK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
