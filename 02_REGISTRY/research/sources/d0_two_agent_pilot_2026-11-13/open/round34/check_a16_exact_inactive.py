#!/usr/bin/env python3
"""Structural certificate of the h=0 native-inactive sector of A16 SELECT.

Uses A14's proved exact identity of CCX_hat when first control is 0,
plus exact CX/Z/CZ and literal-native inverse, not its approximation error.
"""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');p=D/'round16/source_select.py';digest=sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('b34_h0_a16',p);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
checks=0
# Every listed gate is exactly identity when named wires are clean zero. A14
# CCX_hat with first control 0 is exact I on arbitrary other target/aux/port.
def all_inert(tree,known_zero):
 global checks
 for op,*w in a.ideal_gates(tree):
  if op=='CX':assert w[0] in known_zero
  elif op=='CCX':assert w[0] in known_zero
  elif op=='Z':assert w[0] in known_zero
  elif op=='CZ':assert w[0] in known_zero or w[1] in known_zero
  else:raise AssertionError((op,w))
  checks+=1
plans=[]
for degree in [(82,0),(2,2)]:
 plan=a.instruction_plan(degree);q=plan['layout'];h=q['h'][0]
 # Constant sign compute CCX(h,neg,q), Z(q), exact inverse.
 all_inert(plan['constant_phase_IR'],{h,q['constant_work'][0]})
 for call in plan['copy_calls']:
  tree=call['IR'];assert tree['op']=='seq' and len(tree['children'])==3
  enable,pair,inverse=tree['children'];assert inverse=={'op':'adjoint','child':enable}
  # At h=0 every enable elementary gate is exactly I by a zero first control,
  # since all enable scratch and output start zero. No inference from ideal
  # Toffoli alone is used.
  all_inert(enable,{h,q['enabled'][0],*q['enable_work']})
  assert pair['op']=='seq' and len(pair['children'])==3
  membership,body,inv=pair['children'];assert inv=={'op':'adjoint','child':membership}
  # M acts only on membership/diff/member_work and arbitrary native aux, not
  # on enabled or phase_work; thus M may entangle but q remains clean zero.
  protected={q['enabled'][0],q['phase_work'][0]}
  for op,*w in a.ideal_gates(membership):
   if op in ('X','CX','CCX'):assert w[-1] not in protected
  all_inert(body,{q['enabled'][0],q['phase_work'][0]})
 plans.append({'degree':list(degree),'copy_enables_proved':len(plan['copy_calls'])})
assert sha256(p.read_bytes()).hexdigest()==digest
out={'status':'PASS_A16_STRUCTURAL_H0_EXACT_NATIVE_INACTIVE','source_sha256':digest,'plans':plans,'inert_ideal_gate_instances_covered':checks,'basis':'A14 CCX_hat first-control-zero exact for arbitrary target/aux/port/spin; CX,Z,CZ exact; native literal inverse; protected q/h and declared disjoint port','clean_zero_required':'SELECT enabled, enable_work, phase_work, constant_work; membership scratch per stated plan','input_data_and_native_aux_need_not_be_clean':True,'claims_limited_to':'SELECT/constant/top sign sections; does not include approximate H preparation or readout and does not assert ideal behaviour for h=1','GR_closed':False}
Path(__file__).with_name('A16_H0_STRUCTURAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
