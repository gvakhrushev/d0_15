#!/usr/bin/env python3
"""Independent combined X phase+rotation error, with rectangular intervals."""
from pathlib import Path
import sys,json,gzip
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');sys.path.insert(0,str(P.parent/'round42/.deps'));import gmpy2 as g
with gzip.open(A/'TWO_BIT_COFRAME_LIBRARY.json.gz','rt') as f:j=json.load(f)
r=j['controlled_X_power'];entry=j['angles'][r['rotation_angle_id']];k=int(entry['k']);B=9216;S=g.mpz(1)<<B
ceil=lambda x:-((-x)>>B)
def mul(x,y):
 z=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(z)>>B,ceil(max(z))
def cmul(x,y):
 a=mul(x[0],y[0]);b=mul(x[1],y[1]);c=mul(x[0],y[1]);d=mul(x[1],y[0]);return (a[0]-b[1],a[1]-b[0]),(c[0]+d[0],c[1]+d[1])
s5=g.isqrt(5*S*S);p=((s5-S)//2,-((-(s5+1-S))//2));root=(g.isqrt(p[0]*S),g.isqrt(p[1]*S)+1)
def power(n):
 out=((S,S),(0,0));x=(root,p)
 while n:
  if n&1:out=cmul(out,x)
  n>>=1
  if n:x=cmul(x,x)
 return out
def err(got,c,s):return max(abs(got[0][0]-c),abs(got[0][1]-c))+max(abs(got[1][0]-s),abs(got[1][1]-s))
e=err(power(k<<24),0,S)+err(power(k<<25),-S,0);assert e*(1<<3456)<S
out={'status':'PASS_COMBINED_CONTROLLED_X_RECTANGULAR','independent_bits':B,'sum_actual_errors_lt':'2^-3456','uses_same_k_for_k2_power':True,'GR_closed':False}
(P/'CONTROLLED_X_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
