#!/usr/bin/env python3
"""Independent full finite A31 coordinate/mark mapping and norm audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import itertools,json,sys
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round29'));import gcx_birth_clock as b
files=[D/'round31/MEAN_GEOMETRY_LIFT_PLAN.json',D/'round31/mean_geometry_lift.py',D/'round11/PERIODIC_SOURCE_BINDING.json',D/'round25/H1_NAMESPACE_PLAN.json',O/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',D/'round30/COMMON_SOURCE_MARKED_PLAN.json']
plan=json.loads(files[0].read_text());orig=json.loads(files[2].read_text());coords=[json.loads(z) for z in files[4].read_text().splitlines()];ns=b.c.old.namespace();rows=plan['coordinate_binding'];blocks=plan['link_matrix_mark_blocks'];assert len(coords)==len(rows)==2688 and len(blocks)==256
names={t['name']:i for i,t in enumerate(orig['leaf_templates'])};sites={tuple(x['site']):x['SITE_index'] for x in orig['site_bindings']};seen=set();counts=Counter()
for i,(c,row) in enumerate(zip(coords,rows)):
 assert row['sam_index']==c['sam_index']==i and row['site']==c['site'] and row['kind']==c['kind'];counts[c['kind']]+=1
 if c['kind']=='proper_link':
  v=blocks[row['link_block']];assert v['site']==c['site'] and v['role']==c['role'] and row['decoded_component_ab']==c['generator'];seen.add(row['link_block']);continue
 expected=('u/%d/%d'%(c['role'],c['component'])) if c['kind']=='coframe' else ('X/base/%d'%c['grade']);tid=names[expected];slot=392 if c['kind']=='coframe' else 1342;source=ns['source_slots'][slot]
 assert row['source_slot']==slot and row['original_leaf_template']==tid and row['external_SITE_index']==sites[tuple(c['site'])]
 assert row['physical_support_wires_LE_at_m0']==[b.physical_wire(q,0) for q in source['source']]
assert counts=={'coframe':1024,'proper_link':1536,'matter':128} and len(seen)==256
checks=0
for i,block in enumerate(blocks):
 assert block['block']==i and block['external_SITE_index']==sites[tuple(block['site'])] and len(block['matrix_entries'])==16
 for entry in block['matrix_entries']:
  a,j=entry['row'],entry['column'];tid=names['M/base/%d/%d/%d'%(block['role'],a,j)];t=orig['leaf_templates'][tid]
  assert entry['original_leaf_template']==tid and t['input']==1<<j and t['output']==1<<a and t['anchor_moment_multiplier']==2
  assert entry['source_slot']==392 and entry['physical_support_wires_LE_at_m0']==[b.physical_wire(q,0) for q in ns['source_slots'][392]['source']];checks+=1
assert checks==4096
s=F(1,2**30);e=F(1,2**3214);r=6*s;d=r*r/(1-r);dactual=d+8*e;bias=52*dactual/(1-dactual)
assert bias<F(1,2**48) and 6*(r/(1-r)+d)/(1-d)<F(1,2**24)
assert 2688*64*e/s<F(1,2**3166) and 6*(r/(1-r)+d)/(1-d)+2688*64*e/s<F(1,2**23)
u=2*F(309,500)*F(39,50);assert F(52)/(u*(1-F(1,2**23)))<55
assert 55*F(1,2**3231)*2**3158/s<F(1,2**37)
assert 55*F(20,3)*F(1,2**3231)*2**3158/s<F(1,2**34)
for x in plan['finite_Neumann_truncation_examples']:
 bits=int(x['desired_inverse_truncation_error_lt'].split('^-')[1]);k=x['Neumann_terms_if_exact_J_used'];assert F(1,2**(23*k))/(1-F(1,2**23))<F(1,2**bits)
assert plan['actual_decoded_centre_shift_euclidean_lt']=='2^-48' and not plan['actual_full_J_or_mean_values_evaluated']
for f,h in plan['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h,f
out={'status':'PASS_A31_FULL_BINDING_BIAS_AND_NORM','coordinate_rows':len(rows),'link_blocks':len(blocks),'link_matrix_entries':checks,'raw_chart_counts':dict(counts),'mean_centre_bias_lt':'2^-48','actual_J_defect_lt':'2^-23','raw_scaled_and_physical_lift_bounds':['55','55/s'],'e_theta_Psi_Frobenius_lift_bound':'(1100/3)/s','native_only_error_under_owner_Gamma_s':['2^-37','2^-34'],'Neumann_truncation_examples':len(plan['finite_Neumann_truncation_examples']),'bounds_conditional_on_B21_A30_and_gs':'2^-3158','actual_J_reader_and_full_price_not_evaluated':True,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files},'GR_closed':False}
(P/'A31_BINDING_BIAS_NORM_INDEPENDENT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'coordinates':len(rows),'link_entries':checks,'bias_lt':out['mean_centre_bias_lt']}))
