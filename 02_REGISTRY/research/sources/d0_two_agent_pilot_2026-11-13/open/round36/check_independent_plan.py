#!/usr/bin/env python3
"""Independent A17 namespace and input-role reconstruction from actual events."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');p=D/'round17';source=p/'report_assembly.py';files=[source,p/'GLOBAL_REPORT_PLAN.json',p/'GLOBAL_REPORT_COMPILATION.json']; hashes={str(x):sha256(x.read_bytes()).hexdigest() for x in files}
spec=importlib.util.spec_from_file_location('b36_a17',source);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
plan=json.loads(files[1].read_text());comp=json.loads(files[2].read_text());tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());assert comp['source_sha256']==hashes[str(source)] and comp['plan_sha256']==hashes[str(files[1])]
def span(ws):
 assert ws and ws==list(range(ws[0],ws[0]+len(ws)))
 return [ws[0],len(ws)]
def local(root):
 fair=[];golden=[];ready=[];first=None;end=None;counts=Counter()
 for e in a.s.dispatch.walk_events(tables,root):
  kind=e['kind'];counts[kind]+=1
  if kind=='selector':
   q=e['plan']['layout'];m=e['map'];fair.append(span([m[i] for i in q['fair']]))
   if q['golden']:golden.append(span([m[i] for i in q['golden']]))
  elif kind=='first_success':ready.append(e['map'][e['plan']['layout']['out_ready'][0]])
  elif kind=='transition' and first is None:first=[e['map'][i] for i in e['plan']['layout']['record']]
  elif kind=='end':end=e
 assert end['external_SITE']==list(range(8)) and len(first)==65
 instr=a.s.instruction_plan(tables['roots'][root]['degree']);q=instr['layout'];record=sum([q[k] for k in ('negative','leaf','coffset','qoffset','kind','a','b')],[])
 assert len(record)==65 and len(set(record))==65
 mapping=dict(zip(record,first));cursor=end['allocated_wires']
 for i in range(instr['wire_count']):
  if i not in mapping:mapping[i]=cursor;cursor+=1
 assert len(set(mapping.values()))==len(mapping)
 sources=[]
 for kind,key in [('Choi','choi'),('CAR_DATA','car'),('CAR_RIGHT','CAR_RIGHT')]:
  for i,ws in enumerate(q[key]):sources.append({'kind':kind,'copy':i,'range':span([mapping[w] for w in ws])})
 delta=[mapping[i] for i in q['delta_choi']+q['delta_car']];fair.append(span(delta))
 return {'fair':fair,'golden':golden,'ready':ready,'sources':sources,'sign':mapping[q['h'][0]],'delta':delta,'local_wires':cursor,'counts':dict(counts)}
localdata={root:local(root) for root in tables['roots']};expected_fair=[];expected_golden=[];expected_ready=[];expected_sources=[];expected_sign=[];cursor=9
assert plan['incoming_shared_SITE']==list(range(8)) and plan['incoming_sigma_wire']==8
for i,w in enumerate(plan['walks']):
 expected_label=('S'+str(i+1)) if i<2 else ('T'+str(i-1));assert w['label']==expected_label
 r='H_f_before_inverse_PF' if i<2 else 'H_q_before_inverse_PF';assert w['root']==r;L=localdata[r]
 assert w['private_start']==cursor and w['local_wires']==L['local_wires'] and w['private_width']==L['local_wires']-8
 m=lambda x:x if x<8 else cursor+x-8
 expected_fair.extend([[m(x),n] for x,n in L['fair']]);expected_golden.extend([[m(x),n] for x,n in L['golden']]);expected_ready.extend(m(x) for x in L['ready']);expected_sign.append(m(L['sign']))
 for row in L['sources']:expected_sources.append({**row,'walk':w['label'],'range':[m(row['range'][0]),row['range'][1]]})
 cursor+=w['private_width']
assert expected_sources==plan['source_buffers'] and expected_sign==plan['sign_wires_S1_S2_T1_to_T8']
post=json.loads((D/'round13/TEN_SIGN_REPORT_CIRCUIT.json').read_text());aliases=dict(zip(post['layout']['palette'],expected_sign+[8]));mapping=[]
for i in range(post['wire_count']):
 if i in aliases:mapping.append(aliases[i])
 else:mapping.append(cursor);cursor+=1
assert mapping==plan['postprocessor_map'] and len(set(mapping))==len(mapping)
q=post['layout'];expected_fair.append(span([mapping[x] for x in q['fair']]));expected_golden.append(span([mapping[x] for x in q['golden']]));pout=[mapping[x] for x in q['output']];expected_ready.append(pout[-1])
assert pout==[plan['post_label_wire'],plan['post_READY_wire']] and expected_ready==plan['selector_and_post_READY_wires'];assert cursor==plan['report_wire'] and cursor+1==plan['all_READY_wire']
rows=plan['fair_output_ranges'];assert len(rows)==len(expected_fair);start=0
for e,r in zip(expected_fair,rows):
 assert r=={'bank_index_start':start,'output_wire_start':e[0],'count':e[1]};start+=e[1]
assert start==plan['fair_bank_count']==10248262 and expected_golden==plan['Golden_RAW_ranges']
assert len(expected_ready)==1065 and plan['READY_total_flags']==start+1065
# Independent exhaustive interval partition: 31,463,581 logical roles are
# covered once by ranges, not by enumerating 1.5 billion individual wires.
roles=[(x,n,'fair') for x,n in expected_fair]+[(x,n,'golden') for x,n in expected_golden]+[(e['range'][0],e['range'][1],e['kind']) for e in expected_sources]+[(x,n,'zero') for x,n in plan['processor_zero_ranges']]
roles.sort();at=9;cnt=Counter()
for x,n,k in roles:assert x==at and n>0;at+=n;cnt[k]+=n
assert at==plan['compiler_region_end'] and plan['fair_bank_extra_start']==at
assert (cnt['Choi'],cnt['CAR_DATA'],cnt['CAR_RIGHT'],cnt['fair'],cnt['golden'])==(3960,192,112,10248262,76)
assert plan['RAW_birth_requirements']=={'processor_zero':cnt['zero'],'Golden_coins':cnt['golden'],'fair_banks_including_output':143*cnt['fair']}
assert plan['logical_wire_count']==at+142*cnt['fair'] and plan['native_port']==plan['logical_wire_count']
# Every interval is globally disjoint, so it is enough to check the affine
# actual map at both boundaries and midpoint of each fair-output range.
binding=0
for r in rows:
 for off in set((0,r['count']//2,r['count']-1)):
  index=r['bank_index_start']+off;out=r['output_wire_start']+off
  assert a.fair_output(plan,index)==out
  wires=[a.fair_bank_wire(plan,index,i) for i in range(143)];assert len(set(wires))==143 and wires[84]==out
  assert sorted(w for i,w in enumerate(wires) if i!=84)==list(range(at+142*index,at+142*(index+1)))
  assert a.ready_flag(plan,index)==at+142*index+84;binding+=1
assert all(sha256(x.read_bytes()).hexdigest()==hashes[str(x)] for x in files)
out={'status':'PASS_INDEPENDENT_A17_GLOBAL_NAMESPACE','input_sha256':hashes,'source_walk_local_events':{k:v['counts'] for k,v in localdata.items()},'same_SITE_and_sigma_disjoint':True,'independent_maps_of_all_walks':len(plan['walks']),'source_buffers':len(expected_sources),'disjoint_source_qubit_counts':{k:cnt[k] for k in ('Choi','CAR_DATA','CAR_RIGHT')},'unique_fair_outputs':cnt['fair'],'independent_fair_bank_range_boundary_checks':binding,'ready_selector_and_post_flags':len(expected_ready),'all_ready_flags':plan['READY_total_flags'],'golden_RAW_count':cnt['golden'],'processor_zero_count':cnt['zero'],'fair_bank_RAW_count':143*cnt['fair'],'total_new_RAW_births':sum(plan['RAW_birth_requirements'].values()),'shared_SITE_and_source_state_prepared_here':False,'full_native_execution':False,'GR_closed':False}
Path(__file__).with_name('INDEPENDENT_PLAN_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
