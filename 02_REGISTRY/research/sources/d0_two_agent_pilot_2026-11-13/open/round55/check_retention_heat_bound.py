#!/usr/bin/env python3
"""Check the numerical and count inequalities used in conditional B55.

This is not a test of physical admission, the old Gram, marks, or gain law.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
p=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round25/GLOBAL_H1_PLAN.json')
a=json.loads(p.read_text())
L=int(a['W_primitive_call_count_decimal']); n=a['WORK_RAW_birth_count']+a['separate_SAM_RAW_births']+1
assert n==10407050781 and L.bit_length()==4188 and (L+n)<2**4189
assert Q(5,6)**4 < Q(1,2)
assert Q(3,5)**2+Q(3,5)<1 # p solves p²+p=1; hence p>3/5
assert Q(18,2872)<1
out={'status':'PASS_CONDITIONAL_HEAT_ARITHMETIC','a25_gate_count_bits':L.bit_length(),'a28_births_with_fresh_aux':n,'isolated_gates_plus_births_less_than':'2^4189','retention_factor':'(2p)^(-K) < (5/6)^K','sufficient_K':'4*(q+3158+Q+T+1)','scope':'conditional; q bounds actual full prefix stage count; z*Tr(A_old)*abs(t)>=2^(-Q); real gain, old cut, marks, birth admission and common comparison required','physical_C_closed':False,'GR_closed':False}
Path(__file__).with_name('CONDITIONAL_HEAT_ARITHMETIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
