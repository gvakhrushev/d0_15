#!/usr/bin/env python3
"""Audit A29 CZ recognizer on all production copy-call templates.

Counts templates without expanding A25's astronomical repeat powers.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round58';sys.path.insert(0,str(D/'round29'));import gcx_compiler as c
s=c.old.report.s;nb=c.nb;k=c.old.boolean_k()
def atoms(t):
 if t['op']=='seq':
  for z in t['children']:yield from atoms(z)
 elif t['op']=='repeat':yield from atoms(t['child'])
 else:yield t
def test_tree(t,port,spin,helper,depth,expect_cz):
 cc=c.Compiler(port,spin,helper,1);out,pending,counts=cc.transform(t);assert pending==0 and counts['CZ']==expect_cz,(depth,counts)
 if expect_cz:
  assert counts['CZ_depth_'+str(depth)]==expect_cz
  assert counts['CZ_old_SourceI']==expect_cz*5*3**depth
  assert counts['CZ_old_CX']==expect_cz*14
 for x in atoms(out):
  assert x['op'] in ('G','CX') and not set(x['wires']).intersection(spin)
 return counts
# All 86 actual instruction copy templates for the two production roots, both
# global A depth0 and literal inverse A depth1, with true A14 k and no repeats
# expanded. Each copy IR contains exactly one actual A13 CZ subtree.
templates={}
for degree in ((82,0),(2,2)):
 plan=s.instruction_plan(degree);port=plan['wire_count'];spin=(port+1,port+2);aux=port+3;helper=port+4;bykind=Counter()
 for j,call in enumerate(plan['copy_calls']):
  t=s.lower(call['IR'],k,port,spin,aux)
  for depth in (0,1):
   z=nb.inverse_literal(t,port,spin) if depth else t;test_tree(z,port,spin,helper,depth,1)
  bykind[call['kind']]+=1
  if (j+1)%20==0:print('degree',degree,'copy templates',j+1,flush=True)
 templates[str(degree)]={'copy_calls':len(plan['copy_calls']),'kind_counts':dict(bykind),'tested_depths':[0,1]}
# Matcher robustness on exact actual CZ words at additional nested inverse
# depths and both source operand orders; reject malformed/interrupted words.
port=9;spin=(10,11);helper=12
for a,b in ((0,1),(1,0),(0,port),(port,0)):
 t=nb.seq(*(nb.gate(z.op,*z.wires) for z in s.cz.cz_word(a,b,port,spin)))
 for depth in range(4):
  match=c.exact_cz(t,port,spin);assert match and match['inverse_depth']==depth
  assert match['old_CX']==(8 if port in (a,b) else 14)
  if depth==0:
   bad=nb.seq(*t['children']);bad['children'][1]=nb.gate('CX',3,4);assert c.exact_cz(bad,port,spin) is None
  t=nb.inverse_literal(t,port,spin)
# Other provider DAGs are checked by audit_provider_primitives.py; the
# structural no-false-positive proof is documented in the B58 report.
files=[D/'round29/gcx_compiler.py',D/'round16/source_select.py',D/'round13/compile_native_cz.py',D/'round14/native_boolean.py',D/'round25/reversible_report_stream.py']
out={'status':'PASS_ACTUAL_A29_CZ_RECOGNIZER_COPY_TEMPLATES','templates':templates,'each_real_copy_select_CZ_detected_exactly_once_at_depth0_1':True,'actual_CZ_depth0_through3_and_both_operand_orders':True,'all_result_leaves_G_or_CX_only':True,'full_W_expanded':False,'additional_no_false_positives_outside_slots':'proved by even-run language and odd internal CZ run; see report','source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files},'physical_C_closed':False,'GR_closed':False}
(P/'A29_RECOGNIZER_TEMPLATES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'templates':templates}),flush=True)
