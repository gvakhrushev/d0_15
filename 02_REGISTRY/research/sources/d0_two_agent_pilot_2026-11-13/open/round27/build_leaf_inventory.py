#!/usr/bin/env python3
"""Bind logical paired involutions to actual A11/B25 local source leaves."""
from pathlib import Path
from collections import Counter
import json,hashlib
import controlled_involution as ci
P=Path(__file__).resolve().parent;B=P.parent/'round25';raw=(B/'SOURCE_LEAF_BINDING.json').read_bytes();d=json.loads(raw)
assert len(d['site_bindings'])==256 and len(d['leaf_templates'])==282
pairs=Counter();kinds=Counter()
for row in d['site_bindings']:
 for leaf,addr in zip(d['leaf_templates'],row['leaf_addresses_in_template_order']):
  if leaf['kind']=='Choi':
   a=0;b=ci.choi_label(addr,leaf['input'],leaf['output']);kind='Choi';n=22
  else:
   assert leaf['kind']=='CAR';a=ci.car_label(addr,leaf['cross_masks'][0]);b=ci.car_label(addr,leaf['cross_masks'][1]);kind='CAR';n=12
  assert a!=b;pairs[(kind,n,a,b)]+=1;kinds[kind]+=1
assert sum(kinds.values())==72192 and kinds=={'Choi':69632,'CAR':2560}
rows=[];hist=Counter()
for (kind,n,a,b),multiplicity in sorted(pairs.items()):
 c=ci.compile_pair(n,a,b);hist[(kind,len(c['diff_bits']),len(c['normalization_flips']),len(c['gates']))]+=1
 rows.append({'kind':kind,'data_bits':n,'a':a,'b':b,'leaf_occurrences':multiplicity,'counts':c['counts'],'gates_total':len(c['gates']),'clean_scratch':len(c['clean_scratch'])})
(P/'ACTUAL_PAIR_INVENTORY.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in rows))
# One owned concrete full gate list for each carrier, including all controls.
for kind in ('Choi','CAR'):
 row=next(r for r in rows if r['kind']==kind and r['b'] not in (1,))
 c=ci.compile_pair(row['data_bits'],row['a'],row['b'])
 (P/(kind.upper()+'_EXAMPLE_GATE_LIST.json')).write_text(json.dumps(ci.serial(c),indent=2)+'\n')
result={'status':'BOUND_FIXED_LABEL_LOGICAL_PAIR_INVENTORY','source_binding_sha256':hashlib.sha256(raw).hexdigest(),'source_leaf_occurrences':dict(kinds),'distinct_pairs_by_kind':dict(Counter(r['kind'] for r in rows)),
 'distinct_pair_count':len(rows),'histogram':[{'kind':k,'hamming_distance':hd,'zero_normalizations':z,'total_logical_gates':g,'unique_pairs':v} for (k,hd,z,g),v in sorted(hist.items())],
 'control_delta_and_h_unchanged':True,'RIGHT_and_oldRIGHT':'not addressed; CAR data x=(internal_site<<4)|grade',
 'physical_SITE_versus_internal_site':'source binding determines a known local address; no dynamic external SITE lookup circuit emitted',
 'logical_gate_grammar':['X','CX','CCX','Z','CZ'],'native_admission_claimed':False,'GR_closed':False}
(P/'PAIR_INVENTORY_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','source_leaf_occurrences','distinct_pairs_by_kind','distinct_pair_count']}))
