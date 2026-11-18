#!/usr/bin/env python3
"""Independent exhaustive original leaf -> A30 RAW mark descriptor audit."""
from pathlib import Path
from functools import lru_cache
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round60';sys.path.insert(0,str(D/'round30'));import source_mark_registry as r
original=json.loads((D/'round11/PERIODIC_SOURCE_BINDING.json').read_text());backup=json.loads((O/'round25/SOURCE_LEAF_BINDING.json').read_text());assert original['leaf_templates']==backup['leaf_templates'] and original['site_bindings']==backup['site_bindings']
ns=r.s.g.namespace();reg=json.loads((D/'round30/SOURCE_RAW_MARK_REGISTRY.json').read_text());assert len(reg['source_slots'])==1372
pick=reg['selected_common_f_q_slots'];assert pick=={'f_Choi':392,'q_Choi':1340,'q_CAR':1342}
for key,i in pick.items():
 bank,kind=key.split('_');slot=ns['source_slots'][i];assert slot['bank']==bank and slot['kind']==kind and slot['copy']==0 and slot['walk']==('S1' if bank=='f' else 'T1')
# Cache the unmodified chooser result to avoid 100 million redundant slot scans.
r.choose_slot=lru_cache(None)(r.choose_slot);counts=Counter();uses=Counter()
for x,row in enumerate(original['site_bindings']):
 for j,t in enumerate(original['leaf_templates']):
  addr=row['leaf_addresses_in_template_order'][j]
  for bank in (('f','q') if t['kind']=='Choi' else ('q',)):
   d=r.leaf_mark(x,j,bank,0);slot=ns['source_slots'][d['source_slot']];want=pick[bank+'_'+t['kind']];assert d['source_slot']==want
   assert d['logical_support_wires_LE']==slot['source'] and d['physical_support_wires_LE']==[r.s.b.physical_wire(q,0) for q in slot['source']]
   assert not d['PF_or_inverse_PF_factor_inserted'] and d['source_DAG_node']==t['node']
   if t['kind']=='Choi':
    label=(addr<<10)|(t['input']<<5)|t['output'];coef=32784*t['anchor_moment_multiplier'];assert d['r_computational_label']==0 and d['t_computational_label']==label and d['coefficient']=={'integer':coef} and d['operator_norm_upper']=={'integer':coef}
    assert d['original_Julia_address_input_output']==[addr,t['input'],t['output']]
   else:
    assert d['r_computational_label']==(addr<<4)|1 and d['t_computational_label']==(addr<<4)|t['cross_masks'][1]
    assert d['fresh_CAR_RIGHT_identity_wires']==slot['RIGHT'] and d['operator_norm_upper']=={'strict_lt_integer':256}
   assert d['r_G_columns_LE']==[(d['r_computational_label']>>i)&1 for i in range(len(slot['source']))]
   assert d['t_G_columns_LE']==[(d['t_computational_label']>>i)&1 for i in range(len(slot['source']))]
   counts[t['kind']]+=1;uses[bank]+=1
assert counts=={'Choi':139264,'CAR':2560}
for j in (0,15,16,271,272,281):
 m0=r.leaf_mark(0,j,initial_raw_bits=0);m3=r.leaf_mark(0,j,initial_raw_bits=3)
 assert m3['physical_support_wires_LE']==[q+3 for q in m0['physical_support_wires_LE']]
 assert m3['fresh_CAR_RIGHT_physical_identity_wires']==[q+3 for q in m0['fresh_CAR_RIGHT_physical_identity_wires']]
plan=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text());e=plan['common_mark_error_per_unit_operator_norm'];error=F(int(e['numerator_hex'],16),int(e['denominator_hex'],16))
assert 32784*error<F(1,2**3215) and 65568*error<F(1,2**3214) and 256*error<F(1,2**3223)
for i,row in enumerate(reg['source_slots']):
 assert row['slot']==i and row['source_completion_frame'].startswith('computational') and row['original_RAW_mark_checkpoint_after_stage_index']==plan['joint_RAW_source_checkpoint_after_stage_index']
 assert row['logical_resource_frame_wires']==ns['source_slots'][i]['source']+ns['source_slots'][i].get('RIGHT',[])
paths=[D/'round30/source_mark_registry.py',D/'round30/SOURCE_RAW_MARK_REGISTRY.json',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round11/PERIODIC_SOURCE_BINDING.json',D/'round25/H1_NAMESPACE_PLAN.json',O/'round25/SOURCE_LEAF_BINDING.json']
out={'status':'PASS_ALL_ORIGINAL_A30_SOURCE_MARK_DESCRIPTORS','independent_original_binding_equal_to_B25_copy':True,'tested_descriptor_counts':dict(counts),'tested_total':sum(counts.values()),'selected_slots':pick,'all_1372_source_completion_and_common_RAW_checkpoints_checked':True,'strict_mark_bounds':['2^-3215','2^-3214','2^-3223'],'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'physical_readers_or_all_internal_marks_proved':False,'GR_closed':False}
(P/'A30_MARK_REGISTRY_INDEPENDENT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'tested_descriptors':out['tested_total'],'slots':pick}),flush=True)
