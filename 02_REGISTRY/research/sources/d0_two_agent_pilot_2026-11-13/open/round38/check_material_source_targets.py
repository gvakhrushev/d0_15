#!/usr/bin/env python3
"""Independent catalogue, B25 binding and target vector diagnostics for A18."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import importlib.util,sys,json,random
import mpmath as mp
import numpy as np
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open');P=D/'round18'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
t=load('b38_targets',P/'material_targets.py');m=load('b38_prep',P/'material_preparation.py');bt=load('b38_b25',O/'round25/targets.py')
coords=[json.loads(x) for x in (O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()];sites=[tuple(json.loads(x)['site']) for x in (O/'round21/ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
assert len(coords)==2688 and all(r['sam_index']==i for i,r in enumerate(coords)) and len(sites)==len(set(sites))==256 and sites==bt.SITES
matter={(tuple(r['site']),r['grade']):i for i,r in enumerate(coords) if r['kind']=='matter'};assert len(matter)==128
cat=t.catalogue();assert {k:len(v) for k,v in cat.items()}=={'q':448,'y+':256,'y-':256}
for ix,site in enumerate(sites):
 isfree=(site,0) in matter;assert ((site,15) in matter)==isfree
 rows=[r for r in cat['q'] if r['site']==ix]
 assert len(rows)==(4 if isfree else 1)
 if isfree:
  assert {tuple(r['SAM_pattern']) for r in rows}=={(0,0),(0,1),(1,0),(1,1)}
  assert all(r['SAM_indices']==[matter[site,0],matter[site,15]] and r['vector_id']==f"q{site[0]}_{r['SAM_pattern'][0]}{r['SAM_pattern'][1]}" for r in rows)
 else:assert rows[0]['SAM_indices']==[] and rows[0]['vector_id']==f'q{site[0]}_fixed'
 for bank,axis in [('y+',1),('y-',0)]:
  rr=[r for r in cat[bank] if r['site']==ix];assert len(rr)==1 and rr[0]['vector_id']==('y_positive' if site[axis]%2==0 else 'y_negative')
# Outward primitive arithmetic includes negative intervals and square roots.
iv=t.Dyadic(256);S=iv.scale
for n,d in [(-7,5),(-1,3),(0,1),(1,7),(3,2)]:
 z=iv.rational(n,d);assert F(z[0],S)<=F(n,d)<=F(z[1],S)
for aa,bb in [((-3*S//4,-S//5),(S//7,S//2)),((-S//2,S//3),(-S//3,S//4)),((S//7,S//4),(S//9,S//2))]:
 out=iv.mul(aa,bb)
 for x in aa:
  for y in bb:assert F(out[0],S)<=F(x*y,S*S)<=F(out[1],S)
for x in (iv.rational(2),iv.rational(5),iv.rational(1,3)):
 lo,hi=iv.sqrt(x);assert lo*lo<=x[0]*S and hi*hi>=x[1]*S
cs=t.constants(iv);family=t.family_specs();assert len(family)==22 and len({z['id'] for z in family})==22
with mp.workprec(400):
 p=(mp.sqrt(5)-1)/2;aa=mp.sqrt(p);z=mp.mpf(1)/2**20;L=4*p**3;rr=1-z*L*(1+p**6);Q=1-z*L;k0=2*p**-5*(rr/Q+p**6)
 meta=json.loads((O/'round21/REFERENCE_METADATA.json').read_text());Fh=F(meta['F_h_rational']);ref=mp.sqrt((mp.mpf(Fh.numerator)/Fh.denominator)/k0)/8;phys=mp.pi/(200*mp.sqrt(2));one=mp.mpf(1);den=mp.sqrt(2*(1+aa))
 def in_interval(value,bounds):
  if bounds==(0,0):assert value==0
  else:assert mp.mpf(bounds[0])/S<=value<=mp.mpf(bounds[1])/S,(mp.nstr(value,8),bounds)
 for x,y in [('p',p),('sqrtp',aa),('k0',k0),('reference_amp',ref),('physical_amp',phys)]:in_interval(y,cs[x])
 pi=iv.pi();in_interval(mp.pi,pi)
 for spec in family:
  if spec['kind']=='q':
   xx=spec['x0'];ps=[(1,0,-1,0)[xx]*phys,(0,1,0,-1)[xx]*phys]
   if spec['bits'] is not None:ps=[ps[j]+(mp.mpf(spec['bits'][j])-p*p)/2**30 for j in range(2)]
  else:ps=[spec['sign']*ref,mp.mpf(0)]
  slack=1-p-ps[0]**2-ps[1]**2;vec={1:(1+aa)/den,14:mp.sqrt(slack)/den,0:ps[0]/den,15:ps[1]/den}
  v,gotpsi=t.half_vector(iv,cs,spec)
  for i in (0,1):in_interval(ps[i],gotpsi[i])
  for i in (1,14,0,15):in_interval(vec[i],v[i])
  r1=mp.sqrt(vec[1]**2+vec[0]**2+vec[15]**2);r2=mp.sqrt(vec[1]**2+vec[15]**2);true=[(r1,vec[14]),(r2/r1,vec[0]/r1),(vec[1]/r2,vec[15]/r2)]
  rotations=t.rotations(iv,v);assert [x['other'] for x in rotations]==[14,0,15]
  for target,(c,s) in zip(rotations,true):in_interval(c,target['cos']);in_interval(s,target['sin'])
  state=[mp.mpf(1),mp.mpf(0),mp.mpf(0),mp.mpf(0)]
  # symbolic sequential plane recipe: [grade1,14,0,15]
  for j,(c,s) in enumerate(true,1):old=state[0];state[0]=c*old;state[j]=s*old
  assert max(abs(state[j]-vec[x]) for j,x in enumerate((1,14,0,15)))<mp.mpf(2)**-380
# Check local q source invariance against random *other* bits in B25 evaluator.
rng=random.Random(3818);source_cases=0
for x0 in range(4):
 site=next(x for x in sites if x[0]==x0 and (x,0) in matter);ix=sites.index(site)
 for b0,b15 in [(0,0),(1,1)]:
  labels=[]
  for _ in range(2):
   z=np.array([rng.randrange(2) for _ in range(2688)],dtype=np.int8);z[matter[site,0]]=b0;z[matter[site,15]]=b15;labels.append(z)
  assert sum(labels[0]!=labels[1])>1000
  psi0=bt.fields('q',labels[0])[2][ix];psi1=bt.fields('q',labels[1])[2][ix]
  assert np.array_equal(psi0,psi1);source_cases+=1
out={'status':'PASS_INDEPENDENT_A18_TARGETS_CATALOGUE_AND_LOCALITY','source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in [P/'material_targets.py',P/'material_preparation.py',O/'round25/targets.py',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',O/'round21/ORIGINAL_PF_N20_L4.jsonl']},'SAM_coordinates':2688,'site_count':256,'local_matter_coordinates':128,'q_sectors':448,'y_plus_sectors':256,'y_minus_sectors':256,'distinct_half_vector_families':22,'all_22_half_vectors_and_66_rotations_checked':True,'independent_mp_checks_are_diagnostic_only':True,'outward_integer_arithmetic_reviewed':True,'B25_other_2686_bits_hostile_cases':source_cases,'exact_two_bits_per_free_site':True,'three_plane_product_matches_half_vector':True,'scope':'source and exact formula review; no native huge word or physical bank preparation','GR_closed':False}
Path(__file__).with_name('A18_TARGETS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
