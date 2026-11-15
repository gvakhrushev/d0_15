#!/usr/bin/env python3
"""Check actual two-bit comparison order and rigorous finite jet substitution."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');sys.path.insert(0,str(A))
import actual_full_vector_source_jet as x
import two_bit_global_source as g
receipt=json.loads((A/'ACTUAL_FULL_VECTOR_SOURCE_JET.json').read_text());ap=x.control_plan();gp=json.loads((A/'TWO_BIT_GLOBAL_SOURCE_PLAN.json').read_text())
for path,h in receipt['source_sha256'].items():assert sha256(Path(path).read_bytes()).hexdigest()==h,path
# Full compressed actual control trees match the independently audited A47
# words on both extreme coordinate addresses, for each +/-/identity variant.
counts={}
for j in (0,2687):
 for sign in (-1,0,1):
  actual=list(x.control_blocks(j,sign));original=list(x.a47.control_blocks(j,sign));assert actual==original,(j,sign)
  c=x.a47.count_blocks(lambda:iter(actual));assert sum(c.values())==int(ap['each_padded_control_calls_hex'],16)
  assert {k:hex(v) for k,v in c.items()}==receipt['control_native_counts'][str(sign)];counts[str(sign)]=True
for j in range(2688):
 pair=(g.physical_wire(g.namespace()['layout']['SAM'][j]),g.physical_wire(g.namespace()['layout']['SAM'][2688+j]))
 assert pair==x.a47.code_wires(j)==(2+j,11893771936+j)
# Instrument only orchestration; this does not execute SOURCE or pretend
# that the independently compiled plus/minus controls are exact inverses.
oldcontrol=x.control_blocks;oldprefix=g.source_prefix_blocks
x.control_blocks=lambda index,sign:iter([('P',index,sign)])
g.source_prefix_blocks=lambda:iter([('B',)])
try:
 for sign in (-1,0,1):assert list(x.comparison_prefix_blocks(7,sign))==[('P',7,sign),('B',),('P',7,-sign)]
finally:x.control_blocks=oldcontrol;g.source_prefix_blocks=oldprefix
oldstage=g.stage_blocks;oldcompiler=g.compiler;oldphysical=g.physical_tree
class IdentityCompiler:
 def stream(self,it):return it
g.stage_blocks=lambda stage:iter([stage]);g.compiler=lambda:IdentityCompiler();g.physical_tree=lambda node:node
try:
 expected=[]
 for st in g.previous.stages():
  expected.append(st)
  if st=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}:break
 assert list(g.source_prefix_blocks())==expected and expected[-1]['kind']=='RAW_RESOURCE_FRAME'
 assert all(st['kind'] not in ('REPORT','SC6','PORT_ZERO') for st in expected)
finally:g.stage_blocks=oldstage;g.compiler=oldcompiler;g.physical_tree=oldphysical
D=lambda z:F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
sigma=F(1,1<<80);step=F(1,1<<1700);eB=D(gp['errors']['full_SOURCE_DATA_fibre_prefix_error']);eP=D(ap['control_vs_exp_tX_error']);M1=1748;M2=3233036
ideal=sigma*104**2*M2;extra=(eB+2*eP)/(sigma*step)+F(4,3)*104*M1*step**2;total=ideal+extra
assert D(receipt['source_error'])==eB and D(receipt['actual_control_finite_difference_extra'])==extra and D(receipt['full_axis_jet_error'])==total
assert eB<F(1,1<<3423) and extra<F(1,1<<1642) and total<F(1,1<<44)
assert receipt['all_four_comparison_controls_paid'] and receipt['no_exact_inverse_assumption_for_actual_controls']
assert not receipt['complete_corner_post_clock_price_family_constructed']
out={'status':'PASS_ACTUAL_A48_CONTROL_ORDER_SOURCE_PREFIX_AND_JET_BUDGET','all_CODE_physical_pairs_checked':2688,'A47_literal_control_trees_checked_coordinates':[0,2687],'both_signed_and_zero_variants_checked':True,'comparison_order':'P_sign; SOURCE-prefix; P_minus_sign','both_comparisons_four_control_occurrences':4,'source_prefix_ends_at_first_RAW_frame_before_REPORT':True,'native_error_extra_lt':'2^-1642','full_axis_jet_lt':'2^-44','source_typed_extension_and_private_RAW_fibre_only':True,'control_words_exact_inverse_assumed':False,'full_corner_post_clock_or_physical_admission_proved':False,'GR_closed':False}
(P/'ACTUAL_VECTOR_JET_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
