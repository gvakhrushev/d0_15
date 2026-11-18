#!/usr/bin/env python3
"""Independent A30 common-checkpoint schedule, wire frame, and budget audit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round60';sys.path.insert(0,str(D/'round30'));import marked_source_schedule as m
b=m.b;g=m.g;c=m.c;ns=g.namespace();st=m.stages();oldst=g.stages(ns);frame={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0};unframe={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1};fi=st.index(frame);ui=st.index(unframe)
assert fi==1380 and ui==fi+1 and st[0]=={'kind':'SITE'} and not any(x['kind']=='REPORT' for x in st[:fi+1]); assert len(st)==len(oldst)+2
assert [x for x in st if x['kind']=='REPORT']==[x for x in oldst if x['kind']=='REPORT']
assert [x for x in st if x['kind'] in ('SIGMA','SOURCE')]==[x for x in oldst if x['kind'] in ('SIGMA','SOURCE')]
assert len([x for x in st[:fi] if x['kind']=='SOURCE'])==1372 and st[-2:]==[{'kind':'PORT_ZERO'},{'kind':'SC6'}]
# Independently derive resource set and chronological frame sequence.
want=[]
for source in ns['source_slots']:
 want.extend(source['source'])
 if source['kind']=='CAR':want.extend(source['RIGHT'])
assert len(want)==len(set(want))==29848 and tuple(want)==m.resource_wires()
for dep,expect in ((0,want),(1,list(reversed(want)))):
 actual=list(m.stage_blocks({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0},dep))
 # Each tree is an actual G or its literal inverse, preserving target q.
 assert len(actual)==len(expect)
 for q,tree in zip(expect,actual):assert tree==g.invert(c.nb.gate('G',q),dep,ns)
# Same logic for the separately declared literal inverse frame at its actual
# outer depths, without expanding repeated exponents.
for dep in (0,1):
 actual=list(m.stage_blocks(unframe,dep));actualdepth=dep+1;seq=list(reversed(want)) if actualdepth%2 else want
 for q,tree in zip(seq,actual):assert tree==g.invert(c.nb.gate('G',q),actualdepth,ns)
# Independent exact checkpoint and full count arithmetic from component plans.
A=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text());G=json.loads((D/'round29/GCX_BIRTH_CLOCK_PLAN.json').read_text());B=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text());comp=A['global_native_counts']['components'];r=len(want);k=int(json.loads((O/'round57/GADGET_G_POWER_CERTIFICATE.json').read_text())['k_hex'],16)
def group(dic):return Counter({x:int(y) for x,y in dic.items()})
before=sum((group(comp[key]) for key in ('SITE','SIGMA7','Choi1260','CAR112')),Counter());before.update({'G_other':r});assert before['SourceI']%2==0
pairs=before['SourceI']//2;g_before=before['G_port']+before['G_other']+16*k*pairs;cx_before=before['CX']+2*pairs;j=g_before+cx_before
assert g_before==int(B['checkpoint_native_counts']['G']) and cx_before==int(B['checkpoint_native_counts']['CX']) and j==int(B['joint_RAW_source_checkpoint_native_prefix_calls'])
newG=int(G['native_counts']['G'])+r*(4+192*k);newCX=int(G['native_counts']['CX'])+r*42;newL=newG+newCX
assert newG==int(B['new_native_counts']['G']) and newCX==int(B['new_native_counts']['CX']) and newL==int(B['new_native_call_count']) and newL.bit_length()==11647
n=B['total_RAW_births'];assert n==10407050782 and int(B['joint_RAW_source_checkpoint_clock_layer'])==n+j and n+newL<2**11647
# Independent exact relative upper bound to its OWNER source targets.
def frac(x):return F(int(x['numerator_hex'],16),int(x['denominator_hex'],16))
parts=A['conditional_canonical_input_error_components'];eta=sum((frac(parts[z]) for z in ('SITE_once','Choi1260','CAR112')),F());eps=F(2*pairs,2**7432);bound=2*(eta+eps)
assert bound==frac(B['common_mark_error_per_unit_operator_norm']) and bound<F(1,2**3231)
# All source frames before marked point use exact positive G; inverse frame is
# later. No reports were executed; all bank marks refer to one joint state.
paths=[D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',D/'round29/GCX_BIRTH_CLOCK_PLAN.json',O/'round57/GADGET_G_POWER_CERTIFICATE.json']
out={'status':'PASS_A30_COMMON_SOURCE_FRAME_SCHEDULE_AND_BUDGET','source_stage_count':1372,'frame_data_wires':r,'zero_reports_before_checkpoint':True,'checkpoint_after_full_paid_frame':True,'old_source_stage_order_retained':True,'old_report_order_retained':True,'checkpoint_prefix_exact_count_verified':True,'full_word_exact_counts_verified':True,'new_gate_count_bit_length':newL.bit_length(),'common_mark_bound_per_unit_norm_lt':'2^-3231','common_mark_bound_scaled_2^3231_float':float(bound*2**3231),'proof_scope':'ideal canonical reorder by source/report disjoint support and shared control, plus uniform prefix norm; not native exact commutation or all marked prefixes','source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'A30_COMMON_CHECKPOINT_INDEPENDENT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source_stages':1372,'frame_wires':r,'mark_ratio':out['common_mark_bound_scaled_2^3231_float'],'gate_bits':newL.bit_length()}),flush=True)
