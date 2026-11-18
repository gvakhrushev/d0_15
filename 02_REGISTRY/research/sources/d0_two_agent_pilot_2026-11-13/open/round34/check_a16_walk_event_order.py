#!/usr/bin/env python3
"""Independent walk-event connection and selected source-wire audit."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');p=D/'round16/source_select.py';digest=sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('b34_walk_a16',p);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());results={}
for name,root in tables['roots'].items():
 records=[];controller=Counter();roles=Counter();samples={};special={};end=None;stage='controller';slot=0;copy=0
 for event in a.walk_test_events(name,tables):
  k=event['kind']
  if k=='controller':
   assert stage=='controller';ev=event['event'];controller[ev['kind']]+=1
   if ev['kind']=='transition':records.append([ev['map'][i] for i in ev['plan']['layout']['record']])
   continue
  if k=='end':end=event;assert stage=='done';continue
  assert k=='quantum';role=event['role'];roles[role]+=1
  if role in ('prepare_hadamard','top_identity_phase','readout_hadamard','report_sign_convention'):special[role]=event['IR']
  if role=='constant_phase' and event['slot'] in (0,root['slots']-1):special['constant_'+str(event['slot'])]=event['IR']
  if role=='prepare_hadamard':assert stage=='controller' and len(records)==root['slots'];stage='top'
  elif role=='top_identity_phase':assert stage=='top';stage='constant'
  elif role=='constant_phase':assert stage=='constant' and event['slot']==slot;stage='copies';copy=0
  elif role=='copy_SELECT':
   assert stage=='copies' and event['slot']==slot
   nc,nq=root['degree'];assert event['copy_kind']==(1 if copy<nc else 2) and event['copy']==(copy if copy<nc else copy-nc)
   if slot in (0,root['slots']-1) and copy in (0,nc+nq-1):samples[(slot,copy)]=event['IR']
   copy+=1
   if copy==nc+nq:slot+=1;stage='readout' if slot==root['slots'] else 'constant'
  elif role=='readout_hadamard':assert stage=='readout';stage='convention'
  elif role=='report_sign_convention':assert stage=='convention';stage='done'
  else:raise AssertionError(role)
 nc,nq=root['degree'];assert end and slot==root['slots'] and len(end['external_SITE'])==8
 assert roles==Counter({'prepare_hadamard':1,'top_identity_phase':1,'constant_phase':root['slots'],'copy_SELECT':root['slots']*(nc+nq),'readout_hadamard':1,'report_sign_convention':1})
 assert len(set(sum(records,[])))==65*len(records)
 h=end['source_sign_wire'];a15_end=next(e for e in a.dispatch.walk_events(tables,name) if e['kind']=='end');top=a15_end['top_identity_phase'][0]
 assert list(a.ideal_gates(special['prepare_hadamard']))==[('H',h)]
 assert list(a.ideal_gates(special['readout_hadamard']))==[('H',h)]
 assert list(a.ideal_gates(special['report_sign_convention']))==[('X',h)]
 tg=list(a.ideal_gates(special['top_identity_phase'])); assert len(tg)==3 and tg[0][0]=='CCX' and tg[0][1:3]==(h,top) and tg[1]==('Z',tg[0][3]) and tg[2]==tg[0]
 for slot in (0,root['slots']-1):
  cg=list(a.ideal_gates(special['constant_'+str(slot)])); assert len(cg)==3 and cg[0][0]=='CCX' and cg[0][1:3]==(h,records[slot][0]) and cg[1]==('Z',cg[0][3]) and cg[2]==cg[0]
 data=end['Choi_copies']+end['CAR_copies'];delta=end['leaf_delta_wires'];all_data=set(sum(data,[]));right=set(sum(end['CAR_RIGHT'],[]));readonly=set(sum(records,[])+end['external_SITE']+delta+sum(end['CAR_RIGHT'],[])+[h]);all_external=set(end['external_SITE'])
 for (s,c),tree in samples.items():
  gates=list(a.ideal_gates(tree));touched=set(sum((list(g[1:]) for g in gates),[]));targets={g[-1] for g in gates if g[0] in ('X','CX','CCX')}
  assert not targets&readonly and not targets&(all_data-set(data[c]))
  assert set(data[c])<=touched and delta[c] in touched and h in touched
  rec=records[s];n=22 if c<nc else 12
  assert set(rec[21:21+n])<=touched and set(rec[43:43+n])<=touched # a,b
  assert set(rec[19:21])<=touched # kind
  assert set(rec[10:17] if c<nc else rec[17:19])<=touched # correct offset
  assert not (touched & all_external) and not (touched & right)
 results[name]={'controller_stages':dict(controller),'quantum_roles':dict(roles),'walk_wire_count':end['allocated_wires'],'instruction_records':len(records),'unique_record_wires':65*len(records),'sampled_first_last_slots_and_copies':len(samples),'sampled_selected_correct_record_copy_and_delta':True,'top_and_constant_sign_wiring_and_H_X_readout_verified':True}
assert sha256(p.read_bytes()).hexdigest()==digest
out={'status':'PASS_A16_WALK_EVENT_GRAMMAR_AND_SELECTED_WIRING','source_sha256':digest,'roots':results,'different_walks_require_caller_alias_SITE_and_distinct_bank_inputs':True,'control_histories_retained':True,'full_gate_stream_not_simulated':True,'actual_global_birth_assembler_or_clock_proved':False,'GR_closed':False}
Path(__file__).with_name('A16_WALK_WIRING_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
