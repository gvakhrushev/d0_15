#!/usr/bin/env python3
"""Exhaust finite A15 event maps and A16 static IR roles; not primitive execution."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import importlib.util,json,sys
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
s=load('b49_a16',D/'round16/source_select.py');tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());plan=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_text());post=json.loads((D/plan['postprocessor_file']).read_text());m=plan['postprocessor_map'];N=plan['logical_wire_count'];aux=plan['native_aux_arbitrary'];port=plan['native_port'];sp=plan['native_spin'];old=plan['protected_oldRIGHT_witness']
assert (port,sp,aux,old)==(N,[N+1,N+2],N+3,N+4);assert len(m)==post['wire_count'] and all(0<=w<N for w in m) and len(set(m))==len(m)
assert all(w<N for w in (plan['post_READY_wire'],plan['post_label_wire'],plan['report_wire'],plan['all_READY_wire']));assert len({plan['post_READY_wire'],plan['post_label_wire'],plan['report_wire']})==3
# Every A15 retained event is inspected at mapping level: this does not expand
# event_word gates, their native substitutions, or execute the controller.
events={}
for name,root in tables['roots'].items():
 counts=Counter();mapped=0;end=None
 for e in s.dispatch.walk_events(tables,name):
  counts[e['kind']]+=1;n=e['allocated_wires']
  if 'map' in e:
   mm=e['map'];assert len(mm)==e['plan']['wire_count'];assert all(type(q) is int and 0<=q<n for q in mm);assert len(mm)==len(set(mm));mapped+=len(mm)
  if e['kind']=='kind_init':assert all(0<=q<n for op,*ws in e['gates'] for q in ws)
  if e['kind']=='root_init':
   roles=[*e['controls'],*e['outputs'],e['flag'],*e['work']];assert all(0<=q<n for q in roles) and len(roles)==len(set(roles))
  if e['kind']=='end':end=e
 assert end is not None and end['external_SITE']==list(range(8))
 matching=[w for w in plan['walks'] if w['root']==name];assert len(matching)==(2 if name.startswith('H_f') else 8)
 local=s.instruction_plan(root['degree']);l=s.dispatch.Layout();l.n=end['allocated_wires'];w=matching[0];assert w['local_wires']==l.n+local['wire_count']-65
 for row in matching:assert row['local_wires']==w['local_wires'] and row['private_start']+row['private_width']<=plan['compiler_region_end']
 events[name]={'event_counts':dict(counts),'event_map_wire_entries_checked':mapped,'controller_end_allocated':end['allocated_wires'],'bound_A17_walk_logical_wires':w['local_wires']}
# Inspect all static A16 source instruction trees, not slot-expanded millions
# of calls. All gate operands remain below local logical width, so the later
# dedicated native aux cannot accidentally be a logical control/target.
templates={}
for name,root in tables['roots'].items():
 instr=s.instruction_plan(root['degree']);width=instr['wire_count'];counts=Counter()
 def audit(t):
  op=t['op']
  if op=='seq':
   for c in t['children']:audit(c)
  elif op=='adjoint':audit(t['child'])
  else:
   assert op in ('X','CX','CCX','Z','CZ','H');w=t['wires'];assert all(type(i) is int and 0<=i<width for i in w);assert len(w)==len(set(w));counts[op]+=1
 audit(s.instruction_ir(instr));templates[name]={'local_width':width,'syntactic_logical_leaves':dict(counts),'copy_calls':len(instr['copy_calls'])}
# Existing exhaustive A21 catalogue namespace audit is reused only when its
# source pin matches the actual current provider.
ck=json.loads((O/'round44/B44_CHECKPOINT.json').read_text());h=lambda p:sha256(p.read_bytes()).hexdigest()
for p,digest in ck['A21_input_sha256'].items():assert h(Path(p))==digest
ns=json.loads((O/'round44/A21_NAMESPACE_CONTROL_CHECK.json').read_text());assert ns['status']=='PASS_A21_ALL_SELECT_READ_ONLY_AND_NAMESPACE_BINDINGS' and ns['aux_rebit_comparator_oldRIGHT_and_Choi_input_distinct']
files=[D/'round15/source_dispatcher.py',D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round16/source_select.py',D/'round17/report_assembly.py',D/'round17/GLOBAL_REPORT_PLAN.json',D/'round13/TEN_SIGN_REPORT_CIRCUIT.json',O/'round44/B44_CHECKPOINT.json',O/'round44/A21_NAMESPACE_CONTROL_CHECK.json']
out={'status':'PASS_FINITE_A15_EVENT_AND_A16_IR_AUX_NAMESPACE_CHECK','source_sha256':{str(p):h(p) for p in files},'event_mapping_by_root':events,'A16_static_instruction_trees':templates,'A17_postprocessor_mapping_all_roles_inside_logical_namespace':True,'global_report_and_ready_distinct_from_aux':True,'A21_existing_pinned_coframe_units':ns['coframe_units'],'A21_existing_pinned_link_commands':ns['link_commands'],'proof_scope':'All finite event maps and all A16 static instruction IR leaves were checked; huge event_word, native leaves and whole H1 run were not enumerated. Relies on A14 macro structure and source provider checks for semantic J commutation.','sigma_source_and_binding_proved':False,'A25_or_whole_H1_shared_layout_proved':False,'marks_and_birth_admission_proved':False,'GR_closed':False}
(P/'REPORT_SELECT_AUX_NAMESPACE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'events':{k:v['event_counts'] for k,v in events.items()},'templates':templates}))
