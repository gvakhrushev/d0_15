#!/usr/bin/env python3
"""Independently reconstruct A20 coframe sources and dyadic rotation targets."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import importlib.util,sys,json
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round20');sys.path.insert(0,str(O/'round42/.deps'))
try:import gmpy2 as g
except ImportError:g=None
# Use the established A18 dyadic arithmetic only; target expressions,
# catalogue and factor bindings are independently written here.
pth=D.parent/'round18/material_targets.py';sp=importlib.util.spec_from_file_location('b43_dyadic',pth);mod=importlib.util.module_from_spec(sp);sys.modules[sp.name]=mod;sp.loader.exec_module(mod)
if g:
 class Fast(mod.Dyadic):
  def __init__(self,bits):self.bits=bits;self.scale=g.mpz(1)<<bits
  def sqrt(self,a):
   assert a[0]>=0;lo=g.isqrt(a[0]*self.scale);v=a[1]*self.scale;hi=g.isqrt(v);return lo,hi+(hi*hi<v)
 Dyadic=Fast
else:Dyadic=mod.Dyadic
lib=json.loads((D/'COFRAME_ANGLE_LIBRARY.json').read_bytes());iv=Dyadic(8448);S=iv.scale;R=iv.rational;shift=8448-lib['precision_bits'];fac=1<<shift;c=mod.constants(iv);c['pi']=iv.pi();assert c['k0'][1]<24*S and c['pi'][1]*7<22*S
B=O/'round21';C=O/'round24';coords=[json.loads(x) for x in (B/'L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()];addresses=[json.loads(x) for x in (C/'TORUS_CHOI_ADDRESSES.jsonl').read_text().splitlines()];pf={tuple(x['site']):x['N'] for x in map(json.loads,(B/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines())};groups={}
for i,row in enumerate(coords):
 if row['kind']=='coframe':groups.setdefault((tuple(row['site']),row['role']),[]).append(i)
banks={};specs={}
for bank in ('y+','y-','f','0','x+','x-','q'):
 rows=[]
 for row in addresses:
  if row['kind']!='inverse_coframe_column':continue
  role=row['direction'];site=tuple(row['site']);ids=groups.get((site,role),[]) if bank in ('f','q') else [];assert len(ids) in (0,4)
  for bits in product((0,1),repeat=len(ids)):
   if bank in ('f','q'):
    spec={'family':'current','role':role,'x2':site[2] if role==1 else 0,'x3':site[3] if role==1 else 0,'bits':list(bits) if ids else None};name='c_'+str(role)+'_'+str(spec['x2'])+str(spec['x3'])+'_'+(''.join(map(str,bits)) if ids else 'fixed')
   else:
    spec={'family':'reference','role':role,'PF_count':pf[site]};name='r_'+str(role)+'_'+str(pf[site])
   assert name not in specs or specs[name]==spec;specs[name]=spec;rows.append({'address':row['a'],'SAM_indices':ids,'SAM_pattern':list(bits),'family_id':name})
 banks[bank]=rows
assert banks==lib['catalogue'] and set(specs)==set(lib['families']) and len(specs)==247 and sum(map(len,banks.values()))==14848

def square(a):
 x,y=a;lo=0 if x<=0<=y else min(x*x,y*y);hi=max(x*x,y*y);return lo//S,-((-hi)//S)
def summ(xs):
 r=R(0)
 for x in xs:r=iv.add(r,x)
 return r
def contains(saved,new):
 a,b=[int(v,16) for v in saved];return a*fac<=new[0] and new[1]<=b*fac
def clip(x):return max(-S,x[0]),min(S,x[1])
def vector(spec):
 role=spec['role'];v=[R(0) for _ in range(4)]
 if spec['family']=='current':
  if role==1:
   x,y=spec['x2'],spec['x3'];first=iv.mul(iv.mul(c['k0'],square(c['pi'])),R(x*x+y*y,40000));h=iv.add(first,R(3*(x*x-y*y),1600));v[0]=R(3,5);v[1]=iv.neg(iv.div(iv.mul(R(3,5),h),R(2)))
  else:v[{0:1,2:2,3:3}[role]]=R(3,5)
  if spec['bits'] is not None:
   for j,bit in enumerate(spec['bits']):v[j]=iv.add(v[j],iv.mul(R(1,2**30),iv.sub(R(bit),square(c['p']))))
 else:
  x=iv.div(iv.sqrt(R(256*spec['PF_count'],10946)),R(10))
  if role in (0,1):
   z=iv.div(x,iv.sqrt(R(2)));v[0]=z if role==0 else iv.neg(z);v[1]=z
  else:v[role]=iv.neg(x) if role==2 else x
 return v
order=(0,2,3,1)
def signs(j):
 rest=[q for q in range(4) if q not in (0,j)];between=order[1:order.index(j)];out=set()
 for bits in product((0,1),repeat=2):
  m=sum(b<<q for b,q in zip(bits,rest));out.add((-1)**sum((m>>q)&1 for q in between))
 return out
bindings=0
for name,spec in specs.items():
 fam=lib['families'][name];assert fam['spec']==spec;v=vector(spec)
 for saved,new in zip(fam['vector_bounds_hex'],v):assert contains(saved,new),(name,'vector')
 n2=summ(square(x) for x in v);n=iv.sqrt(n2);assert n[0]>0 and n[1]<S
 assert contains(fam['norm_hex'],n) and contains(fam['norm_squared_hex'],n2)
 # Reconstruct the exact elimination order independently from the source role.
 role=spec['role'];dominant=({0:1,1:0,2:2,3:3}[role] if spec['family']=='current' else {0:0,1:0,2:2,3:3}[role]);first=dominant if dominant else 1;ordering=[first]+[x for x in (1,2,3) if x!=first];assert fam['chosen_elimination_order']==ordering
 cur=v[:];el=[]
 for q in ordering:
  rad=iv.sqrt(iv.add(square(cur[0]),square(cur[q])));assert 2*rad[0]>=n[1];cc=iv.div(cur[0],rad);ss=iv.div(cur[q],rad);identity=cur[q]==(0,0) and cur[0][0]>0
  el.append({'mode':q,'cos':cc,'sin':ss,'radius':rad,'exact_identity':identity});cur[0]=rad;cur[q]=R(0)
 rotations=list(reversed(el));targetmap={}
 for i,(expected,stored) in enumerate(zip(rotations,fam['mode_rotations'])):
  assert stored['mode']==expected['mode'] and stored['exact_identity']==expected['exact_identity']
  for key in ('cos','sin','radius'):assert contains(stored[key+'_hex'],expected[key]),(name,key)
  if not expected['exact_identity']:
   for sign in signs(expected['mode']):targetmap[('mode',i,sign)]=(clip(expected['cos']),clip(expected['sin'] if sign==-1 else iv.neg(expected['sin'])))
 targetmap[('base',0,0)]=(clip(iv.sqrt(iv.sub(R(1),n2))),clip(n))
 assert {tuple(z['factor']) for z in fam['angle_bindings']}==set(targetmap)
 for z in fam['angle_bindings']:
  tc,ts=targetmap[tuple(z['factor'])];angle=lib['angles'][z['angle_id']];assert contains(angle['target_cos_hex'],tc) and contains(angle['target_sin_hex'],ts),(name,z['factor']);bindings+=1
out={'status':'PASS_INDEPENDENT_A20_SOURCE_TARGETS','families':len(specs),'sector_bindings':sum(map(len,banks.values())),'target_factor_bindings':bindings,'dyadic_precision_bits':8448,'source_library_sha256':sha256((D/'COFRAME_ANGLE_LIBRARY.json').read_bytes()).hexdigest(),'native_targets_contain_independently_reconstructed_intervals':True,'original_Golden_k0_and_Machin_pi_verified':True,'GR_closed':False}
(P/'A20_SOURCE_TARGET_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
