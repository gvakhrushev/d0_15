#!/usr/bin/env python3
"""Exact ideal A18 grade-reflection extension on every dirty-predicate column."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round13'));import reversible_selectors as logic
word=list(logic.pattern_gate([0,1,2,3],1,4,[5,6]));counts=Counter(t[0] for t in word);assert counts=={'CX':5,'CCX':5}
def step(s,g):
 op,*w=g
 if op=='CX' and (s>>w[0])&1:s^=1<<w[1]
 if op=='CCX' and (s>>w[0])&1 and (s>>w[1])&1:s^=1<<w[2]
 return s
neg=[];different=[]
for s in range(128):
 t=s
 for gate in word:t=step(t,gate)
 phase=(-1)**((t>>4)&1)
 if phase==-1:neg.append(s)
 ideal=(-1 if (s&15)==1 else 1)
 if phase!=ideal:different.append(s)
 if s>>4==0:assert phase==ideal
 # Uncompute returns exactly all seven input bits.
 for gate in reversed(word):t=step(t,gate)
 assert t==s
assert len(neg)==64 and len(different)>0
assert next(s for s in different if s&15!=1)==16
# Full global target: exact F_ideal Boolean action on arbitrary private data;
# 5 all-column CCX errors per F imply R=F†ZF error ≤10δ,
# material/star each used twice give 2*3δ+2δ+20δ=28δ.
delta=Fraction(1,2**4096);assert 2*3*delta+2*delta+2*10*delta==28*delta
out={'status':'PASS_EXACT_A18_BOOLEAN_DIRTY_HELPER_TARGET','word':word,'five_approximate_CCX_per_F':True,'all_128_columns_boolean_truth_table_checked':True,'clean_3_predicate_bits_matches_grade1_reflection':True,'dirty_columns_differ_from_grade_only':len(different),'example_dirty_input':{'grade':0,'flag':1,'work':[0,0],'ideal_phase':-1,'naive_grade_only_phase':1},'conditional_global_norm_bounds':{'F_native_minus_F_boolean':'<=5*delta','R_native_minus_F_boolean_dagger_Z_F_boolean':'<=10*delta','A18_nonconstant_native_minus_helper_aware_target':'<=28*delta','assumptions':'A14 all-column per-CCX bound delta, A18 all-column U_m <=3delta and U_star <=delta, exact Z macro, fixed true port/Spin and any aux as stated by those bounds'},'target_chronological':'Ustar†; R_boolean; Ustar; Um†; R_boolean; Um','warning':'Target is explicit new dirty-helper extension; neither I_private outside clean fibre nor equivalence of old marked prefix, source/heat/birth/clock costs follows. Common growing-fibre embedding must be proved.','source_sha256':sha256((D/'round13/reversible_selectors.py').read_bytes()).hexdigest(),'physical_C_closed':False,'GR_closed':False}
(P/'A18_DIRTY_HELPER_TARGET_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'different_dirty_columns':len(different)}))
