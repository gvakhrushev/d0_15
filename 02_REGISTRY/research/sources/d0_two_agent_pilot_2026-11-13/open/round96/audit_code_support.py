#!/usr/bin/env python3
"""Compositional CODE-control-only proof obligations for actual A48 core."""
from pathlib import Path
from collections import Counter
import sys,json,itertools
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round48'))
import two_bit_global_source as g
s=g.s;ns=g.namespace();lay=ns['layout'];code=set(lay['SAM']);assert len(code)==5376
helper=ns['old_compiler_helper'];assert helper not in code
protected=set(lay['SITE']+[lay['port'],lay['aux_arbitrary'],lay['oldRIGHT_witness'],*lay['spin'],helper]);assert not code&protected
for r in ns['reports']:
 lo=r['private_start'];hi=lo+r['private_width'];assert all(not lo<=q<hi for q in code)
assert set(ns['SC6_local_to_global']).isdisjoint(code)
assert set(g.previous.resource_wires()).isdisjoint(code)
slots=Counter()
for slot in ns['source_slots']:
 slots[slot['kind']]+=1
 owned=slot['source']+slot['private']+slot.get('RIGHT',[])
 assert code.isdisjoint(owned)
 if slot['kind']=='Choi':s.validate_choi(g.ns.choi_layout(ns,slot))
 else:
  car=g.ns.car_layout(ns,slot);pv=[car['predicate_flag'],*car['predicate_work']];s.vac.validate(car,[*pv,car['native_aux_arbitrary']])
assert slots=={'Choi':1440,'CAR':128}
def walk(node):
 op=node['op']
 if op=='seq':
  for z in node['children']:yield from walk(z)
 elif op=='repeat':yield from walk(node['child'])
 else:yield node
def safe(node):
 for z in walk(node):
  op=z['op'];assert op in ('G','CX','SourceI')
  if op in ('G','CX'):assert z['wires'][-1] not in code,(op,z['wires'])
  else:assert set(z['wires']).isdisjoint(code)
choi=g.ns.choi_layout(ns,next(x for x in ns['source_slots'] if x['kind']=='Choi'))
car=g.ns.car_layout(ns,next(x for x in ns['source_slots'] if x['kind']=='CAR'))
inputs=s.inputs()
for tree in s.old.prefix.prefix_blocks(inputs['prefix'],choi,True):safe(tree)
for tree in s.raw_blocks(s.data(choi)+s.private(choi),choi):safe(tree)
fx=s.old.adapter.fixed(s.old.adapter_layout(choi),int(inputs['phase']['phase_k']),int(inputs['level9']['correction_l']),inputs['h_k'])
for key in ('H','correction'):safe(fx[key])
for key in ('start','good'):
 for tree in fx[key]:safe(tree)
for i in (0,1,(1<<46)):
 safe(s.gray.block_at(i,s.data(choi)+s.private(choi),choi['aux_arbitrary'],int(inputs['fixed']['joint_reflection_pi']['k'])))
for kind in ('RAW','H','VAC'):
 for tree in s.vac.fixed_blocks(kind,car,inputs['h_k']):safe(tree)
for cmd in s.vac.commands(s.vac.inputs()['kappa'],car,int(inputs['fixed']['fourier_pi_over_2']['k'])):
 assert cmd['target'] not in code and set(cmd['controls']).isdisjoint(code)
for tree in s.site_blocks(g.ns.site_layout(ns)) :safe(tree)
# All coframe family/width classes, with actual bound target/permutation.
co=s.local.library('COFRAME');cl=s.choi_layout();families=0
for bank in co['catalogue_templates']:
 seen=set()
 for row in s.t.coframe_sectors(co['catalogue_templates'],bank):
  key=(row['family_id'],len(row['SAM_indices']))
  if key in seen:continue
  seen.add(key);families+=1
  for bound,depth in s.local.coframe_units(row,co,cl):
   assert bound['target'] not in set(cl['SAM'])
   assert all(set(z['wires']).isdisjoint(cl['SAM']) for z in bound['permutation'])
# Material bound for every row/rotation: target and swaps remain grade only.
ma=s.local.library('MATERIAL');ml=s.car_layout()
for rows in ma['catalogue'].values():
 for row in rows:
  for rot in ma['vectors'][row['vector_id']]['rotations']:
   if rot['angle_id'] is None:continue
   bound=s.local.bind_material(row,rot,ml,ma['angles']);assert bound['target'] not in set(ml['SAM'])
   assert all(set(z['wires']).isdisjoint(ml['SAM']) for z in bound['permutation'])
# B93's common command grammar covers every pair of modes; target and CX
# endpoints are solely the Choi work modes/flag/aux, CODE is control-only.
link=s.link;stand=link.old.prefix_compatible_global_layout();off=2688
stand={k:(list(range(5376)) if k=='all_SAM' else [q+off for q in v] if isinstance(v,list) else v+off) for k,v in stand.items()}
entry={'address':1,'SAM_indices':list(range(6))+[2688+i for i in range(6)],'SAM_pattern':[0]*12,'family_id':'test'};ll=link.bind(stand,entry)
rots=[{'i':i,'j':j,'k':'1'} for i in range(4) for j in range(i+1,4)];fam={'family':'test','L':rots,'R':rots,'diagonal':{'00':{'k':'1'},'01':{'k':'1'},'10':{'k':'1'}}};cx={'k':'1','phase':{'k':'1'}}
commands=list(link.old.commands(ll,entry,fam,cx))
for cmd in commands:
 assert cmd['target'] not in set(ll['SAM'])
 if cmd['kind']=='fock':assert cmd['cx_control'] not in set(ll['SAM']) and cmd['cx_target'] not in set(ll['SAM'])
# Every compiler primitive uses port/helper targets, never the controls a,b.
compiler=g.compiler();a,b=lay['SITE'][:2]
for tree in (compiler.z(),compiler.cz(a,b),compiler.cz(lay['SAM'][0],a)):safe(tree)
# The global physical map is injective on all CODE and reserved helpers.
phys=[g.physical_wire(q) for q in lay['SAM']+[helper,*lay['SITE'],lay['port'],lay['aux_arbitrary']]];assert len(phys)==len(set(phys))
out={'status':'PASS_COMPOSITIONAL_CODE_CONTROL_ONLY_SUPPORT','CODE_bits':len(code),'all_source_slot_layouts_checked':sum(slots.values()),'source_slot_counts':dict(slots),'coframe_bank_family_width_classes_checked':families,'all_material_rows_and_rotations_checked':True,'proper_link_all_six_mode_pair_grammar_checked':True,'REPORT_private_range_SC6_SITE_and_resources_disjoint_from_CODE':True,'original_helper_and_compiler_targets_disjoint_from_CODE':True,'full_word_enumerated':False,'physical_C_closed':False,'GR_closed':False}
(P/'CODE_SUPPORT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
