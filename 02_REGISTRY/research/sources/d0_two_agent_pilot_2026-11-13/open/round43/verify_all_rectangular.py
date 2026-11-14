#!/usr/bin/env python3
"""Independent integer rectangle replay of all A20 angles and X phase."""
from pathlib import Path
from hashlib import sha256
from math import isqrt
import sys,json,subprocess
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round20');sys.path.insert(0,str(P.parent/'round42/.deps'))
try:import gmpy2 as g
except ImportError:g=None
Z=g.mpz if g else int;root=g.isqrt if g else isqrt
file=D/'COFRAME_ANGLE_LIBRARY.json';raw=file.read_bytes();lib=json.loads(raw);B=8448;S=Z(1)<<B;shift=B-lib['precision_bits'];fac=1<<shift
assert lib['precision_bits']==7168 and len(lib['angles'])==556
for f,h in lib['input_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
assert sha256((D/'certify_coframe_angles.py').read_bytes()).hexdigest()==lib['source_sha256']
# Verify every studied A20 file has the exact pinned Git blob, even if HEAD
# later moves and unrelated files are untracked.
rootdir=D.parents[5];commit='afbaef2f950da70c0fe16dbdb8091c851929bd7a';pinned={}
for f in ['COFRAME_ANGLE_LIBRARY.json','coframe_targets.py','certify_coframe_angles.py','coframe_native.py','COFRAME_NATIVE_PLAN.json','check_coframe_native.py','check_native_pair_columns.py']:
 q=D/f;rel=q.relative_to(rootdir);blob=subprocess.check_output(['git','show',commit+':'+str(rel)],cwd=rootdir);assert blob==q.read_bytes(),f;pinned[f]=sha256(blob).hexdigest()
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
 v=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(v)>>B,-((-max(v))>>B)
def cmul(x,y):return add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0]))
r5=root(5*S*S);p=((r5-S)//2,-((-(r5+1-S))//2));al=root(p[0]*S);ah=root(p[1]*S)+1;powers=[((al,ah),p)]
for _ in range(3360):powers.append(cmul(powers[-1],powers[-1]))
def power(n):
 q=((S,S),(0,0));i=0
 while n:
  if n&1:q=cmul(q,powers[i])
  n>>=1;i+=1
 return q
def bounds(entry,key):return tuple(int(x,16) for x in entry[key])
def contain(saved,new):return saved[0]*fac<=new[0] and new[1]<=saved[1]*fac
def err(a,b,c,d):return max(abs(a[0]-c[1]),abs(a[1]-c[0]))+max(abs(b[0]-d[1]),abs(b[1]-d[0]))
for i,(name,e) in enumerate(lib['angles'].items(),1):
 assert e['native_exponent_multiplier']==1<<20 and e['denominator_power_of_two']==7168
 c,s=power(int(e['k'])<<20);nc,ns,tc,ts=[bounds(e,k) for k in ('native_cos_hex','native_sin_hex','target_cos_hex','target_sin_hex')]
 assert contain(nc,c) and contain(ns,s),(name,'native interval')
 exact=err(nc,ns,tc,ts);assert exact==int(e['operator_error_L1_numerator_hex'],16) and exact<=1<<(7168-3264)
 assert err(c,s,(tc[0]*fac,tc[1]*fac),(ts[0]*fac,ts[1]*fac))<=S>>3264
 if i%100==0:print('independent rectangular coframe powers',i,flush=True)
x=lib['controlled_X_power'];a=lib['angles'][x['rotation_angle_id']];c,s=power(int(a['k'])<<21);nc,ns,tc,ts=[bounds(x,k) for k in ('phase_cos_hex','phase_sin_hex','phase_target_cos_hex','phase_target_sin_hex')]
assert x['phase_native_exponent_multiplier']==1<<21 and contain(nc,c) and contain(ns,s)
phase=err(nc,ns,tc,ts);rot=int(a['operator_error_L1_numerator_hex'],16);assert phase+rot==int(x['X_error_L1_numerator_hex'],16) and phase+rot<=1<<(7168-3264)
out={'status':'PASS_A20_ALL_INDEPENDENT_RECTANGULAR_POWERS','pinned_commit':commit,'pinned_files_sha256':pinned,'source_library_sha256':sha256(raw).hexdigest(),'angles':556,'X_phase_independent_power_checked':True,'bits':8448,'candidate_grid_used':False,'floats_used':False,'GR_closed':False}
(P/'A20_RECTANGULAR_POWER_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'angles':556,'X_phase_checked':True}),flush=True)
