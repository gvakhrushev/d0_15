#!/usr/bin/env python3
"""B56: actual odd SourceI CZ, exact ideal parity gadgets, and bounds.

No giant A25 expansion, no certified new G exponents, no physical admission.
"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json,sys,sympy as s
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=Path(__file__).resolve().parent
sys.path.insert(0,str(D/'round25'));import global_h1 as g
src=g.report.s;nb=src.nb;cz=src.cz
# Actual A16 production CZ, not a fixture.
w=cz.cz_word(0,1,2,(3,4));ops=[z.op for z in w];runs=[];i=0
while i<len(ops):
 if ops[i]!='SourceI':i+=1;continue
 j=i
 while j<len(ops) and ops[j]=='SourceI':j+=1
 runs.append(j-i);i=j
assert runs==[3,1,1] and ops.count('SourceI')==5
# A16 production pair_ir for both actual source copy widths includes one CZ.
logical={}
for n in (12,22):
 tree=src.pair_plan(n)['logical_IR'];c=src.logical_counts(tree);assert c['CZ']==1
 logical[str(n)]={k:int(v) for k,v in c.items()}
# Actual A25 roots include CAR and Choi; actual code puts these copy calls
# into walk_blocks SLOTS, report blocks, and global stage schedule.
tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());assert tables['roots']['H_q_before_inverse_PF']['degree']==[2,2]
plan=src.instruction_plan((2,2));assert len(plan['copy_calls'])==4 and {c['n'] for c in plan['copy_calls']}=={12,22}
assert all(src.logical_counts(c['IR'])['CZ']==1 for c in plan['copy_calls'])
# As a useful contrast, SC6's actual forward source runs really are all even.
sc=g.sc6_word();cr=Counter();i=0
while i<len(sc):
 if sc[i]['op']!='SourceI':i+=1;continue
 j=i
 while j<len(sc) and sc[j]['op']=='SourceI':j+=1
 cr[j-i]+=1;i=j
assert cr=={2:4096}
# Exact ideal two-control parity gadgets, in port/control computational blocks.
# A helper rotation R(phi) conjugated by X for each active control has sign
# (-1)^sum controls. The product angle is pi*a*b.
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);t=s.sqrt(2)/2;Rp=s.Matrix([[t,-t],[t,t]]);Rm=Rp.T
for a in (0,1):
 for b in (0,1):
  M=I
  for u,v,R in [(0,0,Rp),(1,0,Rm),(0,1,Rm),(1,1,Rp)]:
   flip=X**((u*a+v*b)%2);M=flip*R*flip*M
  assert s.simplify(M-((-1)**(a*b))*I)==s.zeros(2)
# One-control +/-pi/2 gadget produces Z_control x I on arbitrary helper.
R=s.Matrix([[0,-1],[1,0]])
for a in (0,1):
 C=X**a;assert C*R*C*R.T==(-1)**a*I
# All-column telescoping: <=L replacements each <=delta; same helper need
# not be reset. δ=(2^-3235)/(L+1) and per G-power error δ/4.
a25=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text());L=int(a25['W_primitive_call_count_decimal']);assert L.bit_length()==4188
# Golden angle irrationality: 2 cos(2θ)=2√5−4, conjugate −2√5−4<−2;
# a root-of-unity sum would have every algebraic conjugate in [−2,2].
assert -2*s.sqrt(5)-4 < -2
pins=[D/'round13/compile_native_cz.py',D/'round16/source_select.py',D/'round25/reversible_report_stream.py',D/'round25/global_h1.py',D/'round25/GLOBAL_H1_PLAN.json']
out={'status':'PASS_ODD_CZ_COUNTEREXAMPLE_AND_IDEAL_GADGETS','odd_CZ_SourceI_runs':runs,'SourceI_per_CZ':5,'a16_pair_logical_counts':logical,'actual_Hq_degree':[2,2],'actual_Hq_copy_SELECT_CZ_per_slot':4,'SC6_SourceI_runs':dict(cr),'exact_ideal_CZ_on_arbitrary_helper':True,'exact_ideal_Z_on_arbitrary_helper':True,'existing_W_native_call_count_bits':L.bit_length(),'delta_per_macro':'2^-3235/(L+1)','each_rotation_operator_error_below':'delta/4','global_all_column_error_lt':'2^-3235, conditional on complete macro coverage and certified rotation powers','new_positive_G_exponents_certified':False,'full_macro_coverage_proved':False,'macro_level_compiler_implemented':False,'marks_or_physical_admission_proved':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in pins}}
(P/'B56_ODD_CZ_AND_GADGET_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'actual_CZ_runs':runs,'Hq_CZ_per_slot':4}))
