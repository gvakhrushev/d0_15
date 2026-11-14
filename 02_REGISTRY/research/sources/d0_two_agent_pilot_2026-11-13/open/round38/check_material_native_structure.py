#!/usr/bin/env python3
"""A18 vs independently structured B37 sector geometry and native resources."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open');P=D/'round18'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
t=load('b38_target2',P/'material_targets.py');a=load('b38_a18',P/'material_preparation.py');b=load('b38_b37',O/'round37/build_car_ustar.py');cat=t.catalogue();lay=a.layout();angles={'test':{'k':'1'}}
assert lay['SAM']==list(range(2688)) and lay['internal_SITE']==list(range(2688,2696)) and lay['grade']==list(range(2696,2700))
assert lay['RIGHT']==list(range(2700,2707)) and lay['port']==2707 and lay['spin']==[2708,2709] and lay['oldRIGHT_witness']==2710 and lay['qubits']==2711 and lay['private_quantum_work']==[]
coverage=0;patterns=Counter();bindings={}
for bank,rows in cat.items():
 seen=set()
 for row in rows:
  key=(row['site'],tuple(row['SAM_pattern']));assert key not in seen;seen.add(key)
  for other in (14,0,15):
   rot={'other':other,'angle_id':'test'};bound=a.bind_plane(row,rot,lay,angles);g=a.plane_geometry(other)
   assert bound['K']==3+8+len(row['SAM_indices']) in (11,13)
   assert bound['controls']==lay['internal_SITE']+[lay['SAM'][i] for i in row['SAM_indices']]+[lay['grade'][i] for i in g['grade_controls']]
   assert bound['pattern']==[(row['site']>>i)&1 for i in range(8)]+row['SAM_pattern']+g['grade_pattern']
   assert bound['k']==2**(13-bound['K']) and (1<<bound['K'])*bound['k']==8192
   # Independent binary-linear permutation from B37 semantics: transform
   # a=1 and b=other into states differing only on pivot.
   diff=1^other;pivot=next(i for i in range(4) if diff>>i&1);flips=[i for i in range(4) if i!=pivot and diff>>i&1]
   def T(x):
    for j in flips:x^=((x>>pivot)&1)<<j
    return x
   ta,tb=T(1),T(other);assert ta^tb==1<<pivot
   assert g['pivot']==pivot and g['flips']==flips and g['orientation']==(-1 if ta>>pivot&1 else 1)
   assert g['grade_pattern']==[(ta>>i)&1 for i in range(4) if i!=pivot]
   assert not set(bound['controls']+[bound['target']]).intersection(lay['RIGHT']+[lay['oldRIGHT_witness']])
   patterns[bound['K']]+=1;coverage+=1
   if bank=='q' and ((bound['K']==11 and 'fixed' not in bindings) or (bound['K']==13 and 'free' not in bindings)) and other==0:bindings['fixed' if bound['K']==11 else 'free']=(row,rot,bound)
assert coverage==(448+256+256)*3==2880 and len(bindings)==2
# Actual B37 emitter differs in Walsh order (grade first versus site first),
# but has precisely the same control->bit predicate, pivot, orientation, k.
for label,(row,rot,bound) in bindings.items():
 extra=lay['internal_SITE']+[lay['SAM'][i] for i in row['SAM_indices']];extra_bits=[(row['site']>>i)&1 for i in range(8)]+row['SAM_pattern']
 tree,meta=b.pair_word(bound['k'],1,rot['other'],grade=lay['grade'],port=lay['port'],spin=lay['spin'],extra_controls=extra,extra_pattern=extra_bits,protected=lay['RIGHT']+[lay['oldRIGHT_witness']])
 grade_ctrl=[lay['grade'][i] for i in range(4) if i!=meta['pivot']];assert dict(zip(grade_ctrl+extra,meta['predicate_pattern']))==dict(zip(bound['controls'],bound['pattern']))
 assert meta['pivot']==a.plane_geometry(rot['other'])['pivot'] and meta['C_target_bits']==a.plane_geometry(rot['other'])['flips']
 # Full A18 actual forward blocks and literal inverse, unexpanded repeats.
 forward=list(a.pair_blocks(bound,lay));assert len(forward)==2**bound['K']+2
 def counts(x):
  op=x['op']
  if op=='seq':
   c=Counter()
   for child in x['children']:c.update(counts(child))
   return c
  if op=='repeat':return Counter({k:int(x['count'])*v for k,v in counts(x['child']).items()})
  if op=='G':return Counter({'G_port' if x['wires'][0]==lay['port'] else 'G_other':1})
  return Counter({op:1})
 total=Counter();reverse=Counter();blocks=0;leaves=0
 for f,r in zip(reversed(forward),a.pair_blocks(bound,lay,True)):
  assert r==a.nb.inverse_literal(f,lay['port'],tuple(lay['spin']))
  for leaf in a.nb.leaves(f):
   if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in bound['controls']
   assert not set(leaf['wires']).intersection(lay['RIGHT']+[lay['oldRIGHT_witness']]);leaves+=1
  total.update(counts(f));reverse.update(counts(r));blocks+=1
 K=bound['K'];n=1<<K;v=n//2 if any(bound['pattern']) else 0;kk=bound['k']
 expected=Counter({'G_port':v*kk,'G_other':(n-v)*kk,'CX':K*n+6*v+2*len(bound['permutation']),'SourceI':4*v})
 assert +total==+expected==+a.pair_counts(bound)
 wanted=Counter({'G_port':total['G_port']+total['G_other'],'CX':total['CX']+6*total['G_other'],'SourceI':3*total['SourceI']+4*(total['G_port']+total['G_other'])})
 assert +reverse==+wanted
 bindings[label]={'K':K,'pattern_nonzero':bool(v),'native_forward_blocks':blocks,'syntactic_forward_leaves':leaves,'actual_literal_inverse_checked':True,'same_projector_and_orientation_as_B37':True}
out={'status':'PASS_A18_INDEPENDENT_SECTOR_AND_NATIVE_GRAMMAR','source_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in [P/'material_targets.py',P/'material_preparation.py',O/'round37/build_car_ustar.py']},'layout_qubits':lay['qubits'],'total_sector_plane_bindings_checked':coverage,'K_occurrences':dict(patterns),'sampled_full_K11_and_K13_blocks':bindings,'sector_disjointness_checked':True,'extra_control_order_differs_but_predicate_matches_B37':True,'full_giant_native_word_executed':False,'GR_closed':False}
Path(__file__).with_name('A18_NATIVE_STRUCTURE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
