#!/usr/bin/env python3
"""Native fixed-anchor reflections and quantitative B25 bank reduction."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from fractions import Fraction as F
import importlib.util,sys,json,random
import anchor_reflection as anchors
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');p=D/'round16/source_select.py'
spec=importlib.util.spec_from_file_location('b35_a16',p);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']);reports={};samples=0
for n,pattern in [(22,0),(4,1)]:
 controls=list(range(n));flag=n;work=list(range(n+1,2*n-1));size=2*n-1;port=size;spin=(size+1,size+2);aux=size+3;old=size+4
 word=list(a.logic.pattern_gate(controls,pattern,flag,work));logical=Counter(g[0] for g in word)
 assert logical==({'X':2,'CX':43,'CCX':41} if n==22 else {'CX':5,'CCX':5})
 built=anchors.build(controls,pattern,flag,work,port,spin,aux,k,protected=[old]);IR=built['ideal_IR'];native=built['native_DAG'];assert built['predicate_counts']==dict(logical)
 a.nb.validate_schema(native,size+5,port,spin,(old,));actual=a.native_resource(native,port);pred=a.resource_ir(IR,k);assert actual==pred
 expected_reverse=a.raw_reverse_resource(actual);inverse=a.nb.inverse_literal(native,port,spin);assert a.native_resource(inverse,port)==expected_reverse
 # Full F;Z;F^-1 on all 16 CAR columns; selected Choi columns include
 # anchor, padded basis, and adversarial random words. Work starts clean.
 cases=list(range(16)) if n==4 else [0,1,(1<<21),(1<<22)-1]+[random.Random(3500+j).randrange(1<<n) for j in range(128)]
 elementary=list(a.ideal_gates(IR))
 for x in cases:
  state=x;phase=1
  for op,*w in elementary:
   if op=='X':state^=1<<w[0]
   elif op=='CX':state^=((state>>w[0])&1)<<w[1]
   elif op=='CCX':state^=((state>>w[0])&(state>>w[1])&1)<<w[2]
   else:assert op=='Z';phase*=(-1 if (state>>w[0])&1 else 1)
  assert state==x and phase==(-1 if x==pattern else 1);samples+=1
 reports[str(n)]={'pattern':pattern,'logical_predicate_counts':dict(logical),'approximate_gate_occurrences_in_reflection':2*(logical['X']+logical['CCX']),'reflection_workspace_flag_plus_and_chain':1+len(work),'tested_clean_workspace_input_columns':len(cases),'native_forward_resource':a.encode_resource(actual),'native_literal_inverse_resource':a.encode_resource(expected_reverse)}
assert reports['22']['approximate_gate_occurrences_in_reflection']==86
assert reports['4']['approximate_gate_occurrences_in_reflection']==10
# Generalized joint anchor includes w private clean work wires. Verify
# exact linear gate-count formulas at multiple actual widths (the width-32768
# bound below is evaluated symbolically, not expanded into a giant word).
for w in (0,1,37):
 for base,pattern in ((22,0),(4,1)):
  n=base+w;gg=list(a.logic.pattern_gate(list(range(n)),pattern,n,list(range(n+1,2*n-1))));cc=Counter(x[0] for x in gg)
  expected=Counter({'X':2,'CX':2*n-1,'CCX':2*n-3}) if pattern==0 else Counter({'CX':2*n-3,'CCX':2*n-3})
  assert cc==expected
# 7 * (180 Choi + 16 CAR) copies; each Choi uses two 22-bit
# reflections, each CAR two 4-bit reflections. Two CAR U's per copy.
choi=7*180;car=7*16;eps=F(1,2**3224);d=F(1,2**4096)
statepart=4*(choi+2*car)*eps
reflectionpart=(choi*2*86+car*2*10)*d
assert statepart+reflectionpart<F(1,2**3210)
# Even 32768 private clean wires for each U fit; their joint-reflection
# costs are included, but the enormous cost of synthesizing U remains unknown.
wmax=2**15;general_count=choi*2*(86+4*wmax)+car*((10+4*wmax)+(10+4*wmax))
assert general_count==218960+10080*wmax+448*(wmax+wmax)
assert statepart+general_count*d<F(1,2**3210)
precision_bounds={}
for t in (3224,3228,3230):
 eta=F(5936,2**t)+general_count*d;exponent=t-14
 assert eta<F(1,2**exponent)
 precision_bounds[str(t)]={'eta_banks_lt':'2^-'+str(exponent),'B29_error_ratio_lt_for_alpha_ge_a':'2^-'+str(t-3171)+' / a^2'}
assert 2*(statepart+reflectionpart)*2**3158 < F(1,2**51)
out={'status':'PASS_OWNED_FIXED_ANCHOR_REFLECTIONS_AND_BUDGET','source_sha256':sha256(p.read_bytes()).hexdigest(),'native_angle_sha256':sha256((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_bytes()).hexdigest(),'reflection_grammars':reports,'logical_test_cases':samples,'raw_choi_inverse_G_calls_per_copy':{'G':22,'CX':132,'SourceI':88},'choi_copy_count':choi,'CAR_copy_count':car,'state_preparation_calls_unknown_error_requirement':'each of controlled Choi, controlled CAR and fixed CAR-star on |anchor,zero_private_work> <=2^-3224 uniformly on all protected external spectator columns; joint reflections include private work','state_error_coefficient':4*(choi+2*car),'reflection_approximate_macro_count':choi*2*86+car*2*10,'joint_reflection_macro_count_formula':'218960 + 10080*w_choi + 448*(w_m+w_star)','same_error_bound_holds_if_each_private_clean_work_width_le':wmax,'precision_bounds':precision_bounds,'B29_general_gain_condition':'for alpha_target >= a > 0: g*s > 2^-3156 * a^2, conditional on the remaining B29 reference bounds','total_seven_call_bank_error_strictly_below':'2^-3210','conditional_B29_e_B_over_g_s_bank_part':'<2^-51, only if full alpha_target>=1/2 and B29 structure holds','source_derivative_rule':'for any observable norm K, central difference bank error <= 4 K eta / s, s=2^-30','scope':'fixed-anchor native grammars and conditional error reduction; the controlled anchor-state preparations remain unspecified and unproved','GR_closed':False,'physical_C_closed':False}
Path(__file__).with_name('REFLECTION_REDUCTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({key:out[key] for key in ['status','logical_test_cases','choi_copy_count','CAR_copy_count','state_error_coefficient','reflection_approximate_macro_count','total_seven_call_bank_error_strictly_below','conditional_B29_e_B_over_g_s_bank_part']},indent=2))
