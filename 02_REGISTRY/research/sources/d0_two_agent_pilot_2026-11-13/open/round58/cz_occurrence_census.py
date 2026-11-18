#!/usr/bin/env python3
"""Exact production CZ counts, from source root records and A25 report wiring."""
from pathlib import Path
from hashlib import sha256
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round58';sys.path.insert(0,str(D/'round25'));import global_h1 as g
r=g.report;s=r.s;tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());counts={}
for name,expected in [('H_f_before_inverse_PF',455),('H_q_before_inverse_PF',18)]:
 print('counting actual source walk',name,flush=True)
 events=0;records=0;end=None
 for event in s.dispatch.walk_events(tables,name):
  events+=1
  if event['kind']=='transition':records+=1
  if event['kind']=='end':end=event
 assert end is not None and records==expected
 degree=tables['roots'][name]['degree'];plan=s.instruction_plan(tuple(degree));copy=len(plan['copy_calls']);assert copy==sum(degree)
 for call in plan['copy_calls']:assert s.logical_counts(call['IR'])['CZ']==1
 assert s.logical_counts(plan['constant_phase_IR'])['CZ']==0
 counts[name]={'transition_records':records,'copy_selects_per_slot':copy,'degree':degree,'CZ_per_call':1,'CZ_per_walk':records*copy,'event_count':events}
namespace=g.namespace();walks=namespace['local_report']['walks'];assert len(walks)==10
by_walk=[{'label':z['label'],'root':z['root'],'CZ':counts[z['root']]['CZ_per_walk']} for z in walks]
per=sum(z['CZ'] for z in by_walk);assert per==75196
schedule=g.stages(namespace);report_schedule=[z for z in schedule if z['kind']=='REPORT'];assert len(report_schedule)==7 and sorted(z['report'] for z in report_schedule)==list(range(7))
A=per*len(report_schedule);assert A==526372;W=2*A
# A copy_SELECT has exactly one s.lower('CZ') at depth 0; applying the
# actual inverse_literal to whole lower IR retains its CZ subtree at depth 1.
# CZ depth-d contains 14 CX and 5*3^d SourceI, no G.
SI=5*A+15*A;CX=14*W
native=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text())['global_native_counts']['W_literal_echo'];totalSI=int(native['SourceI']);totalCX=int(native['CX']);assert totalSI>=SI and totalCX>=CX and (totalSI-SI)%2==0
paths=[D/'round15/SOURCE_DISPATCH_TABLES.json',D/'round15/source_dispatcher.py',D/'round16/source_select.py',D/'round13/compile_native_cz.py',D/'round25/reversible_report_stream.py',D/'round25/global_h1.py',D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json']
out={'status':'PASS_A25_COMPLETE_LOGICAL_CZ_CENSUS','source_roots':counts,'ten_report_walks':by_walk,'CZ_per_report':per,'report_count_A':len(report_schedule),'A_CZ_depth0':A,'W_CZ_depth0':A,'W_CZ_depth1':A,'W_CZ_total':W,'W_CZ_old_SourceI_count':SI,'W_CZ_old_CX_count':CX,'W_nonCZ_SourceI_count':str(totalSI-SI),'W_nonCZ_SourceI_pair_count':str((totalSI-SI)//2),'W_old_CX_after_removing_CZ_CX':str(totalCX-CX),'count_not_dependent_on_READY_compute_inverse':True,'count_is_semantic_full_CZ_not_a_matcher_success_certificate':True,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'physical_C_closed':False,'GR_closed':False}
(P/'CZ_EXACT_OCCURRENCES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'A':A,'W':W,'W_CZ_SourceI':SI,'W_CZ_CX':CX}),flush=True)
