#!/usr/bin/env python3
"""Compare every actual A16 quantum stage, source-slot ordering and remapping.

Native lowering is replaced by identity markers ONLY here; real native literal
inversions and root remaps are independently tested in the other B51 checker.
"""
from pathlib import Path
from hashlib import sha256
from itertools import zip_longest
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import reversible_report_stream as r
s=r.s;d=r.d;h=lambda x:sha256(x.read_bytes()).hexdigest();src=D/'round25/reversible_report_stream.py';pin=h(src);tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']);results=[]
for name in tables['roots']:
 tt,events,records,plan,record,base,hh,phase,size=r.walk_structure(name)
 rec_to_slot={tuple(vals):i for i,vals in enumerate(records)};assert len(rec_to_slot)==len(records)
 tags={id(plan['constant_phase_IR']):('constant',-1)}
 for i,c in enumerate(plan['copy_calls']):tags[id(c['IR'])]=('copy',i)
 seen=set();mode=['owner']
 def map_marker(ir,m):
  slot=rec_to_slot[tuple(m[i] for i in record)];key=(mode[0],slot)
  if key not in seen:
   wanted=list(base)
   for a,b in zip(record,records[slot]):wanted[a]=b
   assert m==wanted;seen.add(key)
  return ('mapped_ir',slot,*tags[id(ir)])
 original=(s.instruction_plan,s.map_ir,s.lower,r.inverse,r.event_word)
 try:
  s.instruction_plan=lambda degree:plan;s.map_ir=map_marker;s.lower=lambda ir,*args:ir;r.inverse=lambda tree,depth,port,spin:(depth,tree);r.event_word=lambda *args,**kwargs:iter(())
  owner=[e['IR'] for e in s.walk_test_events(name,tables) if e['kind']=='quantum'];assert len(owner)==4+len(records)*(1+len(plan['copy_calls']))
  for depth in range(4):
   mode[0]='depth'+str(depth);expected=owner if depth%2==0 else reversed(owner);actual=r.walk_blocks(name,k,depth)
   n=0
   for left,right in zip_longest(actual,expected):assert left==(depth,right),(name,depth,n,left,right);n+=1
   assert n==len(owner);assert sum((mode[0],slot) in seen for slot in range(len(records)))==len(records)
   results.append({'root':name,'literal_depth_marker':depth,'actual_quantum_stage_markers':n,'all_slot_mappings_exact':len(records),'copies_per_slot':len(plan['copy_calls'])})
 finally:s.instruction_plan,s.map_ir,s.lower,r.inverse,r.event_word=original
 print(json.dumps({'root':name,'quantum_markers':len(owner),'records':len(records),'depths_checked':4}),flush=True)
assert h(src)==pin
out={'status':'PASS_ALL_A16_SLOT_STAGE_AND_MAPPING_ORDER','source_sha256':pin,'comparisons':results,'test_method':'Original A16 quantum-event order vs reversible A25 order. For this finite metadata test s.lower and inverse are markers, controller tuple stream suppressed; every slot mapping is separately checked on all indices. Real native DAG inverses and controller rows have separate B51 audits.','logical_depth_not_conflated_with_native_inverse':True,'full_native_primitive_word_executed':False,'GR_closed':False}
(P/'A16_ALL_SLOT_ORDER_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'root_depths':len(results)}))
