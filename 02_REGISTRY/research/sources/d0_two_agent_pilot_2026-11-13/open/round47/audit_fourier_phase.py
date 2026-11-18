#!/usr/bin/env python3
"""Independent 12288-bit rectangles for actual Fourier K7 native power."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round23');sys.path.insert(0,str(P.parent/'round42/.deps'))
try:import gmpy2 as g
except ImportError:g=None
root=g.isqrt if g else isqrt;Z=g.mpz if g else int;names=['car_vacuum_prefix.py','certify_fourier_phase.py','FOURIER_PHASE_CERTIFICATE.json','CAR_VACUUM_PREFIX_PLAN.json','check_car_vacuum_prefix.py','CAR_VACUUM_PREFIX_CHECK.json'];files=[D/x for x in names];digests={str(q):sha256(q.read_bytes()).hexdigest() for q in files};j=json.loads(files[2].read_bytes());plan=json.loads(files[3].read_bytes());check=json.loads(files[5].read_bytes());assert j['source_sha256']==digests[str(files[1])] and check['plan_sha256']==digests[str(files[3])] and check['checker_sha256']==digests[str(files[4])]
for f,h in {**j['input_sha256'],**plan['source_sha256']}.items():assert sha256(Path(f).read_bytes()).hexdigest()==h
B=12288;S=Z(1)<<B;factor=1<<(B-j['denominator_power_of_two']);assert j['controls']==7 and j['native_multiplier']==128
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def mul(a,b):
 q=[x*y for x in a for y in b];return min(q)>>B,-((-max(q))>>B)
def cmul(a,b):return add(mul(a[0],b[0]),neg(mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0]))
z=root(5*S*S);p=((z-S)//2,-((-(z+1-S))//2));a=(root(p[0]*S),root(p[1]*S)+1);base=(a,p)
def power(k):
 r=((S,S),(0,0));b=base
 while k:
  if k&1:r=cmul(r,b)
  k>>=1
  if k:b=cmul(b,b)
 return r
def err(a,b,c,d):return max(abs(a[0]-c),abs(a[1]-c))+max(abs(b[0]-d),abs(b[1]-d))
k=int(j['k']);results=[]
for m,(tc,ts) in enumerate(((0,1),(-1,0),(0,-1)),1):
 co,si=power(m*128*k);e=err(co,si,tc*S,ts*S);assert e<=m*(S>>3264)
 if m==1:
  for v,key in ((co,'native_cos_hex'),(si,'native_sin_hex')):
   old=[int(x,16) for x in j[key]];assert old[0]*factor<=v[0] and v[1]<=old[1]*factor
 results.append({'coefficient':m,'error_bound':str(m)+'*2^-3264'})
oldc=[int(x,16) for x in j['native_cos_hex']];olds=[int(x,16) for x in j['native_sin_hex']];S0=1<<7168;olde=err(oldc,olds,0,S0);assert olde==int(j['error_numerator_hex'],16) and olde<=S0>>3264
for f,h in digests.items():assert sha256(Path(f).read_bytes()).hexdigest()==h
out={'status':'PASS_INDEPENDENT_A23_RECTANGULAR_FOURIER_PHASE','input_sha256':digests,'bits':B,'saved_bits':7168,'controls':7,'coefficient_powers':results,'saved_native_intervals_contain_replay':True,'candidate_or_float_used':False,'GR_closed':False}
(P/'A23_PHASE_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'coefficients':[1,2,3]}))
