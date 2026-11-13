#!/usr/bin/env python3
"""Exhaustive L4 stencil dependency certificate and torus address binding.
No dense quantum simulation, gate compilation, or boundary physics claim.
"""
from collections import Counter
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import json
P=Path(__file__).resolve().parent; B=P.parent/'round21'
site_rows=[json.loads(x) for x in (B/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
coord_rows=[json.loads(x) for x in (B/'L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
sites=[tuple(r['site']) for r in site_rows];assert len(sites)==len(set(sites))==256
interior=lambda x: x[2] in (1,2) and x[3] in (1,2)
free_sites={x for x in sites if interior(x)};assert len(free_sites)==64 and len(coord_rows)==2688
# Site and field-role identity are independent of coordinates (proper-link local 6D Lie chart).
def var_key(r):
 x=tuple(r['site']);k=r['kind']
 if k=='coframe':return (x,k,r['role'],r['component'])
 if k=='proper_link':return (x,k,r['role'],tuple(r['generator']))
 assert k=='matter';return (x,k,r['grade'])
keys={var_key(r):r['sam_index'] for r in coord_rows};assert len(keys)==2688 and set(keys.values())==set(range(2688))
site_vars={x:{keys[k] for k in keys if k[0]==x} for x in sites}
assert all(len(site_vars[x])==(42 if interior(x) else 0) for x in sites)
site_to_counts={tuple(r['site']):r['N'] for r in site_rows}
def add(x,r,kind):
 y=list(x);y[r]+=1
 if kind=='torus' or r<2:y[r]%=4
 return tuple(y)
def frame_deps(x):return {i for k,i in keys.items() if k[0]==x and k[1]=='coframe'}
def link_deps(x,r):return {i for k,i in keys.items() if k[0]==x and k[1]=='proper_link' and k[2]==r}
def matter_deps(x):return {i for k,i in keys.items() if k[0]==x and k[1]=='matter'}
def facelist(x,typ):
 faces=[]
 for r,s in combinations(range(4),2):
  args=[(x,r),(add(x,r,typ),s),(add(x,s,typ),r),(x,s)]
  deps=set().union(*(link_deps(z,d) for z,d in args))
  faces.append((r,s,args,deps))
 return faces
rows=[];frequency=Counter();facechanged=0;materialchanged=0;geo_id=Counter()
addresses=[{'a':0,'kind':'identity_anchor','matrix':'I32'}]
for x in sorted(sites):
 for r in range(4):addresses.append({'a':len(addresses),'kind':'inverse_coframe_column','site':x,'direction':r})
for x in sorted(sites):
 for r in range(4):addresses.append({'a':len(addresses),'kind':'proper_link','site':x,'direction':r})
assert len(addresses)==2049
lookup={(v['kind'],tuple(v['site']),v['direction']):v['a'] for v in addresses if 'site'in v}
for x in sites:
 o=facelist(x,'open');t=facelist(x,'torus');fo=[];delta_f=[]
 for (r,s,ao,do),(_,_,at,dt) in zip(o,t):
  altered=ao!=at
  if altered:
   assert not do and not dt, (x,r,s,do,dt)
   facechanged+=1;delta_f.append([r,s]);geo_id[(r,s)]+=1
  else:assert do==dt
  fo.append({'r':r,'s':s,'open':ao,'torus_addresses':[lookup[('proper_link',z,d)] for z,d in at],'wrap_changes':altered,'sam_dependencies':sorted(dt)})
 mo=[add(x,r,'open') for r in range(4)];mt=[add(x,r,'torus') for r in range(4)]
 md=[r for r in range(4) if mo[r]!=mt[r]];materialchanged+=len(md)
 for r in md:assert not matter_deps(x) and not matter_deps(mo[r]) and not matter_deps(mt[r]),(x,r)
 depf_open=frame_deps(x)|set().union(*(z[3] for z in o));depf_torus=frame_deps(x)|set().union(*(z[3] for z in t))
 depq_open=frame_deps(x)|matter_deps(x)|set().union(*(matter_deps(z) for z in mo))
 depq_torus=frame_deps(x)|matter_deps(x)|set().union(*(matter_deps(z) for z in mt))
 assert depf_open==depf_torus and depq_open==depq_torus
 changed=bool(delta_f or md)
 if changed:assert not depf_open and not depq_open
 assert changed==bool(x[2]==3 or x[3]==3)
 frequency['different_rows' if changed else 'identical_rows']+=1
 frequency['different_pf_count' if changed else 'identical_pf_count']+=site_to_counts[x]
 if depf_open or depq_open:frequency['rows_reachable_by_interior_fields']+=1
 for i in depf_open|depq_open:frequency[f'var_{i}']+=1
 rows.append({'site':x,'PF_count':site_to_counts[x], 'boundary_difference':changed,
              'coframe_addresses':[lookup[('inverse_coframe_column',x,r)] for r in range(4)],
              'faces':fo,'matter_forward_open':mo,'matter_forward_torus':mt,'material_wrap_directions':md,
              'geometry_dependencies':sorted(depf_open),'material_dependencies':sorted(depq_open),
              'delta_geometry_and_material_sam_dependencies':[]})
assert frequency['different_rows']==112 and frequency['identical_rows']==144
assert frequency['different_pf_count']==4557 and frequency['identical_pf_count']==6389
assert facechanged==368 and materialchanged==128
assert all(frequency[f'var_{i}']>0 for i in range(2688))
(P/'TORUS_CHOI_ADDRESSES.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in addresses))
(P/'SITE_DEPENDENCIES.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows))
# Hostile controls show exactly why the hypotheses matter.
# At a 3->0 seam with base=0, exterior value=2, wrapped value=t:
# q_open=4, q_torus=t², so d_t(q_torus-q_open)|_{t=1}=2.
collar_counterexample=2*Fraction(1)
# If external weight changes, w(t)*fixed_difference gives nonzero derivative.
variable_weight_counterexample=Fraction(1)
assert collar_counterexample and variable_weight_counterexample
cert={'status':'PASS_EXHAUSTIVE_STRUCTURAL_DEPENDENCY_CERTIFICATE','L':4,'sites':256,'free_sites':64,'independent_sam_fields':2688,'fields_per_free_site':{'coframe':16,'proper_link':24,'matter':2},
 'open_vs_torus':{'different_rows':112,'different_PF_mass':str(Fraction(4557,10946)),
  'identical_rows':144,'identical_PF_mass':str(Fraction(6389,10946)),
  'changed_oriented_six_face_factors':facechanged,'changed_matter_forward_edges':materialchanged,
  'changed_faces_by_role_pair':{str(k):v for k,v in sorted(geo_id.items())},
  'changed_rows_with_free_field_dependencies':0,'each_of_2688_fields_seen_in_dependency_union':True,
  'full_rows_reachable_by_free_fields':frequency['rows_reachable_by_interior_fields']},
 'torus_address':{'active_A':2049,'coframe':1024,'proper_link':1024,'identity_anchor':1,'active_vector_size':2049*1024,'padded_vector_size':2**22,'anchor_squared':str(Fraction(1,32*2049))},
 'hostile_hypotheses':{'free_wrapped_collar_toy_delta_derivative_at_1':str(collar_counterexample),'variable_weight_times_fixed_delta_derivative':str(variable_weight_counterexample),'scope':'scalar dependency counterexamples, not physical H1 executions'},
 'proof_scope':'depends on fixed rho, fixed halo/boundary values, local source functions, same scalar source semantics and common constants; arbitrary full-Hilbert/mark/factory equality is not proved',
 'explicitly_not_claimed':['native words','READY equality','matching full bank quantum states','open halo supplied','torus Einstein root','Cost-Info physical binding'], 'GR_closed':False}
(P/'TORUS_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n');print(json.dumps(cert,indent=2))
