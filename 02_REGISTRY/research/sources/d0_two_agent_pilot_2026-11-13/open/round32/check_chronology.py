#!/usr/bin/env python3
"""Audit actual A15 event sequence and all retained-wire aliases."""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,hashlib
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
spec=importlib.util.spec_from_file_location('b32_dispatch_chrono',D/'round15/source_dispatcher.py');r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)
tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());comp=json.loads((D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text());totals={}
for name,root in tables['roots'].items():
 it=iter(r.walk_events(tables,name));counts=Counter();previous=9;fair=gold=0;records=set();attempt_outputs=set()
 def take(kind):
  global previous,fair,gold
  e=next(it);assert e['kind']==kind,(kind,e['kind']);counts[kind]+=1
  if 'map' in e:
   m=e['map'];assert len(m)==len(set(m))==e['plan']['wire_count'] and min(m)>=0 and max(m)<e['allocated_wires']
  assert e['allocated_wires']>=previous
  previous=e['allocated_wires'];return e
 if name.startswith('H_q'):
  e=take('kind_init');assert e['gates']==[('X',8)] and previous==9
 site=list(range(8));kind=[8];top_outputs=[]
 for j in range(7):
  e=take('selector');m=e['map'];q=e['plan']['layout'];assert [m[i] for i in q['palette']]==kind+site
  output=[m[i] for i in q['output']];assert not(set(output)&attempt_outputs);attempt_outputs.update(output);top_outputs.append(output)
  fair+=len(q['fair']);gold+=len(q['golden'])
 e=take('first_success');m=e['map'];q=e['plan']['layout'];assert [m[i] for i in q['labels']]==sum([x[:-1] for x in top_outputs],[]) and [m[i] for i in q['ready']]==[x[-1] for x in top_outputs]
 selected=[m[i] for i in q['output']+q['out_ready']];assert selected==e['selected_output']
 e=take('root_init');assert e['controls']==selected and e['rows']==[[3,4,root['node']],[3,6,1<<15]]
 old=None
 for slot in range(root['slots']):
  e=take('palette');assert e['slot']==slot;plan=e['plan'];q=plan['layout'];m=e['map'];assert [m[i] for i in q['site']]==site
  old_here=[[m[i] for i in f] for f in q['old_stack']]
  if old is not None:assert old_here==old
  # All record locations are disjoint and each comes from fresh step allocation.
  rec={m[i] for i in q['record']};assert not(rec&records);records.update(rec)
  selected_palette=[m[i] for i in q['palette']];out=[]
  for j in range(7):
   s=take('selector');assert s['slot']==slot;sm=s['map'];sq=s['plan']['layout'];assert [sm[i] for i in sq['palette']]==selected_palette
   v=[sm[i] for i in sq['output']];assert not(set(v)&attempt_outputs);attempt_outputs.update(v);out.append(v)
   fair+=len(sq['fair']);gold+=len(sq['golden'])
  f=take('first_success');assert f['slot']==slot;fm=f['map'];fq=f['plan']['layout']
  assert [fm[i] for i in fq['labels']]==sum([x[:-1] for x in out],[]) and [fm[i] for i in fq['ready']]==[x[-1] for x in out]
  assert [fm[i] for i in fq['output']]==[m[i] for i in q['choice']] and [fm[i] for i in fq['out_ready']]==[m[i] for i in q['ready']]
  t=take('transition');assert t['slot']==slot and t['map']==m
  old=[[m[i] for i in frame] for frame in q['new_stack']]
 end=take('end');assert end['external_SITE']==site and end['final_stack']==old and end['all_coin_history_retained'] and len(records)==root['slots']*65
 try:next(it);raise AssertionError('extra event')
 except StopIteration:pass
 assert dict(counts)==comp['walks'][name]['chronological_stage_counts'] and previous==comp['walks'][name]['walk_logical_wire_count']
 assert fair==7*1580+root['slots']*7*1374 and gold==7+root['slots']*7*0
 totals[name]={'stages':dict(counts),'walk_wires':previous,'retained_instruction_bits':len(records),'fair_bits_decoders':fair,'golden_bits_decoders':gold,'retained_attempt_output_bits':len(attempt_outputs)}
# Two f and eight q walks consume 10 top selector banks plus 1054 internal,
# matching A12's decoder-specific fair counts; separate 94 report and196 leaf
# bits are outside this controller and are not claimed created here.
f=totals['H_f_before_inverse_PF'];q=totals['H_q_before_inverse_PF'];fair=2*f['fair_bits_decoders']+8*q['fair_bits_decoders'];gold=2*f['golden_bits_decoders']+8*q['golden_bits_decoders']
assert fair==1054*7*1374+10*7*1580 and gold==70 and fair+94+196==10248262
out={'status':'PASS_CHRONOLOGICAL_FULL_EVENT_MAP_AUDIT','input_sha256':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [D/'round15/source_dispatcher.py',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round15/SOURCE_DISPATCH_COMPILATION.json']},
 'roots':totals,'report_decoder_fair_bits':fair,'report_decoder_golden_bits':gold,'report_fair_with_separate_post_and_leaves':fair+94+196,
 'all_prior_attempt_outputs_retained':True,'all_instruction_records_unique':True,'same_SITE_in_all_steps':True,
 'all_full_walk_gates_executed':False,'quantum_payload_or_SELECT_executed':False,'GR_closed':False}
(P/'CHRONOLOGY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'f_wires':f['walk_wires'],'q_wires':q['walk_wires'],'report_decoder_fair_bits':fair}))
