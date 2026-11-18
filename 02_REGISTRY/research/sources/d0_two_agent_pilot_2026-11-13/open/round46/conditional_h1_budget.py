#!/usr/bin/env python3
"""Conditional component budget; NOT complete H1 error or admission."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;B=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
files=[D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round18/CAR_PREPARATION_RU.md',D/'round21/CHOI_LOADER_PLAN.json',D/'round22/GRAY_REFLECTION_CERTIFICATE.json',B/'round45/SITE_NATIVE_PLAN.json',B/'round29/BUDGET_CERTIFICATE.json',D/'round22/FULL_CHOI_BANK_PLAN.json'];h=lambda p:sha256(p.read_bytes()).hexdigest()
report=json.loads(files[0].read_text());a21=json.loads(files[2].read_text());phase=json.loads(files[3].read_text());site=json.loads(files[4].read_text());assert report['prepared_Choi_copies']==180 and report['prepared_CAR_copies_with_RIGHT']==16 and report['seven_report_all_known_approximate_macros']==162754649904
bank=json.loads(files[6].read_text());assert bank['unitary_operator_error_on_clean_private_lt']=='2^-3227' and bank['error_formula']=='4 eta_U +2 delta_R; for 1260 copies use 5040 eta_U+2520 delta_R'
assert a21['half_vector_uniform_joint_anchor_isometry_error_lt']=='2^-3230' and phase['entries']['46']['uniform_operator_error_le']=='2^-3264' and site['site_operator_error_le']=='18*2^-3264'
# H.1 declares seven calls sharing one SITE. These occurrence counts are
# conditional on an actual emitted schedule with the required clean fibres.
delta=F(1,2**3264);etaU=F(1,2**3230);choi_per=4*etaU+2*delta;car_per=28*F(1,2**4096);site_per=18*delta
pieces={'1260_Choi_writers':1260*choi_per,'112_CAR_maps':112*car_per,'SITE_prepare_and_literal_unprepare':2*site_per,'seven_A17_known_approximate_macros':F(1,2**4058)}
total=sum(pieces.values(),F(0));assert total<F(1,2**3217) and total<F(1,2**3206)/1024
out={'status':'CONDITIONAL_COMPONENT_ARITHMETIC_ONLY','input_sha256':{str(q):h(q) for q in files},'occurrences_assumed':{'Choi':1260,'CAR':112,'shared_SITE_prepare':1,'shared_SITE_unprepare':1,'A17_report_calls':7},'components':{k:{'numerator_hex':hex(v.numerator),'denominator_hex':hex(v.denominator)} for k,v in pieces.items()},'conditional_sum_lt':'2^-3217','fraction_of_B29_2^-3206_reserve_lt':'2^-10','conditions':['actual A22 Choi bound verified and emitted for each real occurrence','fixed native schedule really has these occurrence counts and literal SITE inverse remains live','CAR clean-work isometry accepted at every actual prefix or stronger all-column bound proved','same canonical fibres and all controlled external factors preserved','other physical sources, births, marks, readers, comparisons, clock and error terms separately priced'], 'this_is_not_eta_A':True,'alpha_target_ge_half_proved':False,'actual_T6_scalar_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'CONDITIONAL_H1_COMPONENT_BUDGET.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'conditional_sum_lt':out['conditional_sum_lt'],'not_complete_eta_A':True}))
