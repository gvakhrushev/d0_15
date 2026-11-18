#!/usr/bin/env python3
"""Exact/rational plus-resource success and A14 full-column error budgets."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,mpmath as mp
P=Path(__file__).resolve().parent
A12=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round12/SELECTOR_COMPILATION.json')
a12=json.loads(A12.read_text());M=a12['selector_fair_qubits_per_report'];assert M==10248262 and a12['retained_selector_caps']['fair_plus_bank']==28
assert F(3)-4*F(309,500)<F(53,100) and F(3)-4*F(619,1000)>0
upper=F(53,100)**28;assert M*upper<F(1,4)
assert 59<2**6 and M*59<2**30 and 7*M*59<2**32
mp.iv.dps=80;iv=mp.iv;p=(iv.sqrt(5)-1)/2;fail=1-2*p**3;q=1-fail**28
assert q>iv.mpf(1)/2 and q<1
mp.mp.dps=80;pp=(mp.sqrt(5)-1)/2;rf=1-2*pp**3;qq=1-rf**28
result={'status':'PASS_FAIR_COMPONENT_READINESS_AND_ERROR_BUDGET','A12_input_sha256':hashlib.sha256(A12.read_bytes()).hexdigest(),
 'single_attempt_success':'2p^3','single_attempt_failure':'1-2p^3=3-4p=5-2sqrt(5)',
 'ideal_cap28_ready':'1-(1-2p^3)^28','ideal_cap28_ready_interval':str(q),'ideal_cap28_ready_decimal':mp.nstr(qq,35),
 'fixed_28_independent_attempts':True,'ideal_single_report_M_fair_banks':M,'ideal_all_fair_ready':'[1-(1-2p^3)^28]^10248262',
 'ideal_all_fair_ready_gt':'3/4 by union bound; only this fair-bank component',
 'A14_assumed_per_X_or_CCX_error':'<=2^-4096, as certified in A14/B30',
 'single_bank_all_column_error':'<=59*2^-4096 <2^-4090',
 'M_banks_per_report_error':'<=59*M*2^-4096 <2^-4066',
 'seven_reports_error':'<=59*7*M*2^-4096 <2^-4064',
 'actual_ready_probability_lower':'q_28-2*59*2^-4096, on the stated canonical births and exact remaining inputs',
 'actual_conditional_joint_state_trace_distance_upper':'2*59*2^-4096/sqrt(q_28) <3*59*2^-4096',
 'exact_output_factorization':'ideal ready projection only; physical native router has residual bounded above, not exact factorization',
 'full_report_alpha_or_physical_C_proved':False,'GR_closed':False}
(P/'FAIR_READINESS_CERT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','ideal_cap28_ready_decimal','ideal_all_fair_ready_gt','single_bank_all_column_error','M_banks_per_report_error','seven_reports_error']}))
