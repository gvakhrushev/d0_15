#!/usr/bin/env python3
"""Recompute A17 stage inventories and B31 gates independently."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open');P=D/'round17'
f=lambda p:json.loads(p.read_text());plan=f(P/'GLOBAL_REPORT_PLAN.json');comp=f(P/'GLOBAL_REPORT_COMPILATION.json');a13=f(D/'round13/CIRCUIT_COMPILATION.json');a15=f(D/'round15/SOURCE_DISPATCH_COMPILATION.json');a16=f(D/'round16/SOURCE_SELECT_COMPILATION.json');bank=f(O/'round31/NATIVE_FAIR_BANK.json');k=int(f(D/'round14/NATIVE_BOOLEAN_ANGLE.json')['k']);M=plan['fair_bank_count'];K=plan['READY_total_flags'];Z=plan['RAW_birth_requirements']['processor_zero']
def scale(x,n):return Counter({a:b*n for a,b in x.items() if b*n})
def count(t,port):
 op=t['op']
 if op=='seq':
  out=Counter()
  for child in t['children']:out.update(count(child,port))
  return out
 if op=='repeat':return scale(count(t['child'],port),int(t['count']))
 if op=='G':return Counter({'G_port' if t['wires'][0]==port else 'G_other':1})
 assert op in ('CX','SourceI');return Counter({op:1})
def reverse(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def eq(a,b):return all(a.get(i,0)==int(b.get(i,0)) for i in ('G_port','G_other','CX','SourceI'))
X=Counter({'G_other':4*k,'CX':6,'SourceI':2});CCX=Counter({'G_port':6*k,'G_other':6*k,'CX':68,'SourceI':24});CX=Counter({'CX':1})
logical=Counter(a13['decoder_label_routing_counts_per_report']);logical.update(a15['ten_sign_report_controller_counts']);stages={}
stages['A13_selectors_labels_post_and_A15_controller']=scale(X,logical['X'])+scale(CCX,logical['CCX'])+scale(CX,logical['CX'])
stages['A16_quantum_SELECT_and_sign_tests']=Counter({a:int(v) for a,v in a16['one_report_SELECT_test_native_resources'].items()})
port=bank['port']; assert port==143
one=count(bank['router_forward_DAG'],port)
for gate in bank['zero_and_kernel_forward']['gates']:one.update(count(gate,port))
inv=bank['native_forward_inventory'];assert one['G_port']+one['G_other']==int(inv['G']) and one['CX']==int(inv['CX']) and one['SourceI']==int(inv['SourceI']);stages['B31_fair_banks_once']=scale(one,M)
stages['processor_RAW_v_to_zero']=Counter({'G_port':Z,'CX':6*Z,'SourceI':4*Z})
stages['actual_READY_conjunction']=scale(CCX,K-1)+scale(reverse(CCX),K-2)
stages['REPORT1_extraction']=CCX+CX
assert set(stages)==set(comp['native_resources_by_stage'])
total=Counter()
for name,c in stages.items():assert eq(c,comp['native_resources_by_stage'][name]),name;total.update(c)
assert eq(total,comp['native_forward_resources']) and eq(reverse(total),comp['native_literal_raw_reverse_resources'])
assert comp['fair_router_logical_counts_counted_once']=={'X':3*M,'CX':169*M,'CCX':56*M}
assert comp['fresh_RAW_v_births_for_processor_and_fair']==Z+76+143*M==1486712521
assert comp['all_READY_logical_CCX']==2*K-3==20498651
assert comp['seven_report_all_known_approximate_macros']==a16['seven_report_all_known_approximate_macros']+7*(2*K-2)==162754649904 < 2**38
assert comp['seven_report_known_error_strictly_below']=='2^-4058'
files=[P/'report_assembly.py',P/'GLOBAL_REPORT_PLAN.json',P/'GLOBAL_REPORT_COMPILATION.json',D/'round13/CIRCUIT_COMPILATION.json',D/'round15/SOURCE_DISPATCH_COMPILATION.json',D/'round16/SOURCE_SELECT_COMPILATION.json',O/'round31/NATIVE_FAIR_BANK.json']
out={'status':'PASS_INDEPENDENT_A17_STAGE_RESOURCES','input_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in files},'stage_count':len(stages),'B31_full_physical_fair_banks_once':M,'exact_READY_CCX_occurrences':2*K-3,'logical_REPORT_extraction_CCX':1,'processor_zero_inputs':Z,'golden_RAW':76,'fair_RAW_including_outputs':143*M,'total_RAW_births_excluding_source_and_SITE':1486712521,'seven_report_known_approximate_gate_occurrences':162754649904,'conditional_known_error_bound':'2^-4058','native_counts_include_full_global_graph':False,'birth_stage_admission_and_marks_certified':False,'GR_closed':False}
Path(__file__).with_name('INDEPENDENT_RESOURCES_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
