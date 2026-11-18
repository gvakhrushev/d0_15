#!/usr/bin/env python3
"""Independent 12288-bit integer-rectangle verification of K8/K46 phases."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round22');sys.path.insert(0,str(P.parent/'round42/.deps'))
try:import gmpy2 as g
except ImportError:g=None
Z=g.mpz if g else int;root=g.isqrt if g else isqrt
paths=[D/x for x in ('gray_reflection.py','certify_gray_reflection.py','check_gray_reflection.py','GRAY_REFLECTION_CERTIFICATE.json','GRAY_REFLECTION_CHECK.json')];digests={str(x):sha256(x.read_bytes()).hexdigest() for x in paths};j=json.loads(paths[3].read_bytes());check=json.loads(paths[4].read_bytes());assert check['certificate_sha256']==digests[str(paths[3])] and j['source_sha256']==digests[str(paths[1])]
for f,h in j['input_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
B=12288;S=Z(1)<<B;fac=1<<(B-j['precision_bits'])
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def mul(a,b):
 z=[x*y for x in a for y in b];return min(z)>>B,-((-max(z))>>B)
def cmul(a,b):return add(mul(a[0],b[0]),neg(mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0]))
s5=root(5*S*S);p=((s5-S)//2,-((-(s5+1-S))//2));a=(root(p[0]*S),root(p[1]*S)+1);powers=[(a,p)]
for _ in range(3400):powers.append(cmul(powers[-1],powers[-1]))
def power(n):
 out=((S,S),(0,0));i=0
 while n:
  if n&1:out=cmul(out,powers[i])
  n>>=1;i+=1
 return out
def err(a,b,c,d):return max(abs(a[0]-c[1]),abs(a[1]-c[0]))+max(abs(b[0]-d[1]),abs(b[1]-d[0]))
for K in (8,46):
 e=j['entries'][str(K)];assert e['controls']==K and e['native_exponent_multiplier']==1<<K and e['denominator_power_of_two']==7168
 a,b=power(int(e['k'])<<K);old=[tuple(int(v,16) for v in e[q]) for q in ('native_cos_hex','native_sin_hex','target_cos_hex','target_sin_hex')];nc,ns,tc,ts=old
 for small,big in ((nc,a),(ns,b)):assert small[0]*fac<=big[0] and big[1]<=small[1]*fac
 assert tc==(-(1<<7168),-(1<<7168)) and ts==(0,0)
 olderr=err(nc,ns,tc,ts);assert olderr==int(e['error_L1_numerator_hex'],16) and olderr<=1<<(7168-3264)
 E=err(a,b,(-S,-S),(0,0));assert E<=S>>3264
 assert all(e[q] is True for q in ('off_anchor_exact_identity','aux_may_be_arbitrary')) and e['new_clean_wires']==0
for f,h in digests.items():assert sha256(Path(f).read_bytes()).hexdigest()==h
out={'status':'PASS_B46_INDEPENDENT_RECTANGULAR_PHASE_CERTIFICATES','input_sha256':digests,'controlled_widths':[8,46],'bits':B,'source_bits':7168,'native_intervals_contain_independent_replay':True,'target_phase_minus_identity_error_le':'2^-3264','candidate_or_float_used':False,'GR_closed':False}
(P/'GRAY_PHASE_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'controls':out['controlled_widths'],'bits':B}))
