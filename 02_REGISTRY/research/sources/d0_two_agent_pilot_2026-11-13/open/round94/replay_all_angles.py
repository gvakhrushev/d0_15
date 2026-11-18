#!/usr/bin/env python3
"""Full target reconstruction plus independent rectangular power replay of A48."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import multiprocessing as mp
import json,gzip,sys,time
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');sys.path.insert(0,str(A));sys.path.insert(0,str(P.parent/'round42/.deps'))
import gmpy2 as g
import two_bit_source_targets as t
from source_angle_certifier import Dyadic
prep=t.load('b94_old_pair_geometry',t.D/'round18/material_preparation.py');st=t.load('b94_site_targets',t.loc.B/'round45/site_targets.py')
def read(x):
 with (gzip.open(A/x,'rt') if x.endswith('.gz') else (A/x).open()) as f:return json.load(f)
co,ma,site,fx=map(read,['TWO_BIT_COFRAME_LIBRARY.json.gz','TWO_BIT_MATERIAL_LIBRARY.json.gz','RETUNED_SITE_LIBRARY.json.gz','RETUNED_FIXED_ANGLES.json'])
for lib in (co,ma,site,fx):
 for f,h in lib['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h,f
L=Dyadic(8192);H=Dyadic(9216);lc=t.cf.constants(L);hc=t.cf.constants(H);S=H.scale;factor=1<<(9216-8192)
def digest(c,s):return sha256('|'.join(hex(int(x)) for x in (*c,*s)).encode()).hexdigest()
def clip(x,scale):return (max(-scale,x[0]),min(scale,x[1]))
jobs={};occ=Counter()
def bind(lib,tag,aid,orig,target):
 rec=lib['angles'][aid];a,b=[clip(x,L.scale) for x in orig];c,d=[clip(x,H.scale) for x in target]
 assert digest(a,b)==rec['target_sha256'],(tag,aid,'digest')
 assert a[0]*factor<=c[0]<=c[1]<=a[1]*factor and b[0]*factor<=d[0]<=d[1]<=b[1]*factor,(tag,aid,'containment')
 assert int(rec['native_exponent_multiplier'])==1<<lib['controls'] and rec['certified_error_bits']==3456
 key=(tag,aid);record=(int(rec['k'])*(1<<lib['controls']),c,d)
 if key in jobs:
  old=jobs[key];assert old[0]==record[0];record=(old[0],(min(old[1][0],c[0]),max(old[1][1],c[1])),(min(old[2][0],d[0]),max(old[2][1],d[1])))
 jobs[key]=record;occ[tag]+=1
specs,templates,mult=t.coframe_catalogue();assert set(specs)==set(co['families']) and templates==co['catalogue_templates'] and sum(sum(c.values()) for c in mult.values())==137728
for bank,h in mult.items():assert dict(h)==co['family_multiplicity'][bank]
for i,(name,spec) in enumerate(specs.items(),1):
 rec=co['families'][name];assert rec['spec']==json.loads(json.dumps(spec))
 x=t.cf.factors(L,t.coframe_vector(L,lc,spec),spec);y=t.cf.factors(H,t.coframe_vector(H,hc,spec),spec)
 assert x['chosen_elimination_order']==y['chosen_elimination_order']==rec['chosen_elimination_order']
 A0=list(t.cf.native_angle_targets(L,x));A1=list(t.cf.native_angle_targets(H,y));refs=rec['angle_bindings'];assert len(A0)==len(A1)==len(refs)
 for (key,c,s),(key1,c1,s1),ref in zip(A0,A1,refs):
  assert key==key1 and list(key)==ref['factor'];bind(co,'co',ref['angle_id'],(c,s),(c1,s1))
 if i%256==0:print('coframe reconstructed',i,'/',len(specs),flush=True)
x=co['controlled_X_power'];aid=x['rotation_angle_id'];bind(co,'co',aid,(L.rational(0),L.rational(1)),(H.rational(0),H.rational(1)))
# Independent validation of doubled power occurs as a separate target job.
rec=co['angles'][aid];jobs[('coX','phase')]=(int(rec['k'])*(1<<25),H.rational(-1),H.rational(0))
assert x['phase_native_exponent_multiplier']==1<<25
mats=t.material_specs();assert set(z['id'] for z in mats)==set(ma['vectors']) and t.material_catalogue()==ma['catalogue']
for spec in mats:
 rec=ma['vectors'][spec['id']];assert spec==rec['spec'];v0,_=t.material_half_vector(L,lc,spec);v1,_=t.material_half_vector(H,hc,spec);r0=t.mat.rotations(L,v0);r1=t.mat.rotations(H,v1);assert len(r0)==len(r1)==len(rec['rotations'])
 for a,b,row in zip(r0,r1,rec['rotations']):
  assert a['other']==b['other']==row['other'];aid=row['angle_id']
  if aid is None:assert a['sin']==b['sin']==(0,0);continue
  orient=prep.plane_geometry(a['other'])['orientation'];s0=L.neg(a['sin']) if orient==-1 else a['sin'];s1=H.neg(b['sin']) if orient==-1 else b['sin']
  bind(ma,'mat',aid,(a['cos'],s0),(b['cos'],s1))
counts,names,nodes=st.tree_names();assert len(names)==len(site['angles']) and nodes==site['tree_nodes']
for name,spec in names.items():
 rec=site['angles'][name];assert rec['spec']==spec
 class Dummy:pass
 # reuse common binding after wrapping by logical name
 pseudo={'angles':{name:rec},'controls':8};bind(pseudo,'site',name,st.targets(L,spec,counts),st.targets(H,spec,counts))
rec=site['reflection_phase'];bind({'angles':{'phase':rec},'controls':8},'site','phase',(L.rational(-1),L.rational(0)),(H.rational(-1),H.rational(0)))
for name,want in [('fourier_pi_over_2',(0,1)),('joint_reflection_pi',(-1,0))]:
 lib=fx['fixed_angles'][name];aid=lib['selected_angle_id'];assert int(lib['k'])==int(lib['angles'][aid]['k'])
 bind(lib,'fixed',name,(L.rational(want[0]),L.rational(want[1])),(H.rational(want[0]),H.rational(want[1]))) if False else bind({'angles':{name:lib['angles'][aid]},'controls':lib['controls']},'fixed',name,(L.rational(want[0]),L.rational(want[1])),(H.rational(want[0]),H.rational(want[1])))
assert {aid for tag,aid in jobs if tag=='co'}==set(co['angles'])
assert {aid for tag,aid in jobs if tag=='mat'}==set(ma['angles'])
print('all source targets reconstructed, unique actual powers',len(jobs),'occurrences',dict(occ),flush=True)
# Separate rectangular arithmetic (not producer's complex balls), exact GMP.
B=9216;powers=None

def init_power():
 global powers
 def add(x,y):return x[0]+y[0],x[1]+y[1]
 def neg(x):return -x[1],-x[0]
 def mul(x,y):
  z=(x[0]*y[0],x[0]*y[1],x[1]*y[0],x[1]*y[1]);return min(z)>>B,-((-max(z))>>B)
 def cmul(x,y):return add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0]))
 c=t.cf.constants(H);powers=[(c['sqrtp'],c['p'])]
 for _ in range(3600):powers.append(cmul(powers[-1],powers[-1]))
def cmul(x,y):
 def mul(a,b):
  z=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]);return min(z)>>B,-((-max(z))>>B)
 a=mul(x[0],y[0]);b=mul(x[1],y[1]);c=mul(x[0],y[1]);d=mul(x[1],y[0]);return (a[0]-b[1],a[1]-b[0]),(c[0]+d[0],c[1]+d[1])
def check(job):
 key,(n,c,s)=job;out=((S,S),(0,0));i=0
 while n:
  if n&1:out=cmul(out,powers[i])
  n>>=1;i+=1
 e=max(abs(out[0][0]-c[1]),abs(out[0][1]-c[0]))+max(abs(out[1][0]-s[1]),abs(out[1][1]-s[0]));assert e<(S>>3456),key
 return key
if __name__=='__main__':
 start=time.monotonic();done=0
 with mp.get_context('fork').Pool(8,initializer=init_power) as pool:
  for key in pool.imap_unordered(check,jobs.items(),chunksize=8):
   done+=1
   if done%512==0:print('rectangular powers',done,'/',len(jobs),'seconds',round(time.monotonic()-start,1),flush=True)
 assert done==len(jobs)
 out={'status':'PASS_ALL_A48_TARGETS_AND_ALL_ACTUAL_POWERS_RECTANGULAR','source_target_occurrences':dict(occ),'coframe_families':len(specs),'coframe_sectors':137728,'material_vectors':len(mats),'material_q_sectors':len(ma['catalogue']['q']),'coframe_unique_actual_powers':len(co['angles']),'material_unique_actual_powers':len(ma['angles']),'site_angles_and_phase':len(site['angles'])+1,'fixed_powers':2,'coframe_X_doubled_phase_power':1,'total_actual_powers_checked':done,'target_precision':8192,'replay_precision':9216,'actual_power_error_lt':'2^-3456','all_target_hashes_and_containment_checked':True,'independent_rectangular_arithmetic':True,'full_source_or_composition_compiled':False,'GR_closed':False}
 (P/'ALL_ANGLES_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
