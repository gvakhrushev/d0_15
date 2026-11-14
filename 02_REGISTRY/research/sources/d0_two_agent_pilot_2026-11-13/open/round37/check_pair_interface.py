#!/usr/bin/env python3
"""Exact small-k semantic/resource checks for reusable pair compiler."""
from pathlib import Path
import json
import build_car_ustar as b
import check_car_ustar_exact as e

def check_pair(a_label,b_label,extra,pattern,external_states=(0,)):
 tree,meta=b.pair_word(1,a_label,b_label,extra_controls=extra,extra_pattern=pattern);K=meta['predicate_control_count'];gates=e.flatten(tree);c,s=e.cs(1<<K);sign=-1 if meta['source_a_pivot_bit'] else 1
 f=b.resources(tree,4);neg=(1<<(K-1)) if any(meta['predicate_pattern']) else 0;pos=(1<<K)-neg
 assert f['G_port']==neg and f['G_other']==pos
 assert f['CX']==K*(1<<K)+6*neg+2*len(meta['C_target_bits']) and f['SourceI']==4*neg
 for leaf in b.nb.leaves(tree):
  if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in extra
  else:assert not set(leaf['wires']).intersection(extra)
 checked=0
 for control_bits in range(1<<len(extra)):
  enabled=all(((control_bits>>j)&1)==v for j,v in enumerate(pattern))
  ext=sum(((control_bits>>i)&1)<<wire for i,wire in enumerate(extra))
  for extstate in external_states:
   for grade in range(16):
    initial=grade|ext|(extstate<<4)
    if enabled and grade==a_label:want={initial:c,(initial&~15)|b_label:s if sign==1 else e.neg(s)}
    elif enabled and grade==b_label:want={initial:c,(initial&~15)|a_label:e.neg(s) if sign==1 else s}
    else:want={initial:e.one}
    assert e.run(gates,{initial:e.one})==want,(a_label,b_label,extra,pattern,grade,control_bits,extstate)
    checked+=1
 return checked
count=0
for x in range(16):
 for y in range(16):
  if x!=y:count+=check_pair(x,y,(),())
assert count==240*16
with_extra=0
for pair in [(0,1),(0,14),(0,15),(1,14),(1,15),(14,15),(15,0),(14,1)]:
 for pattern in ((0,0),(0,1),(1,0),(1,1)):with_extra+=check_pair(*pair,(8,9),pattern)
assert with_extra==8*4*4*16
external_cases=0
for pair in [(0,1),(0,14),(0,15),(1,14),(1,15),(14,15),(15,0),(14,1)]:external_cases+=check_pair(*pair,(),(),range(16))
assert external_cases==8*16*16
# A protected oldRIGHT cannot silently become an extra selector control.
try:b.pair_word(1,1,14,extra_controls=(8,),extra_pattern=(1,),protected=(8,))
except AssertionError:protected_alias_rejected=True
else:raise AssertionError('protected control accepted')
# Test generic proposed-angle API with two independently exact target pairs,
# including turn=0 (must not get stuck returning k=0). These modest targets
# are examples only; A18 must provide verified intervals for its own angles.
S=1<<256;proposals=[]
for turn,c_target,s_target in [('0',(S,S),(0,0)),('-0.25',(0,0),(-S,-S))]:
 k,_=b.propose_target(32,3,lambda turn=turn:b.mp.mpf(turn));assert k>0
 b.certify_target(k,3,c_target,s_target,32,256);proposals.append(turn)
try:b.certify_target(k,3,(S,S),(0,0),32,256)
except AssertionError:bad_target_rejected=True
else:raise AssertionError('incorrect target accepted')
# Ensure exact Ustar specialization remains byte-equivalent as a native DAG.
j=json.loads(Path(__file__).with_name('CAR_USTAR_NATIVE.json').read_text());assert b.pair_word(int(j['k']),1,14)[0]==j['forward_DAG']
out={'status':'PASS_PAIR_EMISSION_INTERFACE_EXACT_SMALL_COLUMNS','ordered_distinct_grade_pairs':240,'all_pairs_grade_columns':count,'extra_control_pair_pattern_cases':8*4,'extra_control_grade_flag_columns':with_extra,'additional_arbitrary_port_spin_oldRIGHT_columns':external_cases,'all_extra_controls_read_only':True,'all_unselected_patterns_exact_identity':True,'actual_ustar_specialization_equal':True,'independent_generic_proposal_targets':proposals,'incorrect_target_interval_rejected':bad_target_rejected,'protected_control_alias_rejected':protected_alias_rejected,'angle_rule':'2^(3+len(extra_controls))*k*theta; input a cross coefficient (-1)^pivot_bit sin(angle)','scope':'exact k=1 native words; caller must separately certify target angle intervals and account resources/births/marks','GR_closed':False}
Path(__file__).with_name('PAIR_INTERFACE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
