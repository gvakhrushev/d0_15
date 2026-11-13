#!/usr/bin/env python3
"""Exact conditional readiness for ONE instruction-preprocessor report."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;D=P.parent
a12=json.loads((D/'round12/SELECTOR_COMPILATION.json').read_text())
a13=json.loads((D/'round13/CIRCUIT_COMPILATION.json').read_text())
a15=json.loads((P/'SOURCE_DISPATCH_COMPILATION.json').read_text())
M=a12['selector_fair_qubits_per_report'];T=a12['padded_interpreter_slots_per_ten_sign_report']
ti=F(a12['ready_probabilities']['internal_slot']);tt=F(a12['ready_probabilities']['top_slot'])
failure=M*F(53,100)**28+T*(1-ti)**7+10*(1-tt)**7
assert failure<F(1,2)
n13=7*sum(a13['decoder_label_routing_counts_per_report'][op] for op in ['X','CCX'])
n15=7*sum(a15['ten_sign_report_controller_counts'][op] for op in ['X','CCX'])
n31=7*M*59;n=n13+n15+n31
assert n<2**38
files=[D/'round12/SELECTOR_COMPILATION.json',D/'round13/CIRCUIT_COMPILATION.json',P/'SOURCE_DISPATCH_COMPILATION.json',P/'ROOT_REVIEW_B31.json']
out={'status':'EXACT_CONDITIONAL_INSTRUCTION_PREPROCESSOR_READY_COMPOSITION',
 'component':'ONE report ideal prepared-fair plus fixed top/internal instruction controller; not full H1 source writer',
 'Q_pre_exact':'[1-(1-2p^3)^28]^10248262 * [1-(1-tau_i)^7]^1054 * [1-(1-tau_t)^7]^10',
 'Q_pre_is_probability_not_amplitude':True,'failure_union_bound_rational':str(failure),'ideal_Q_pre_gt':'1/2',
 'seven_report_known_approximate_macros':{'A13_selectors_and_label_routing':n13,'A15_instruction_controller':n15,'B31_prepared_fair_routers':n31,'sum':n},
 'conservative_known_error_lt':'2^-4058',
 'actual_SINGLE_preprocessor_READY_probability_gt':'1/2 - 2^-4057; using the conservative seven-report error upper bound for one report, conditional on admitted fresh inputs and the stated graph composition',
 'seven_independent_preprocessor_joint_ideal_ready':'Q_pre^7, not Q_pre; no full source alpha identification',
 'exact_native_scalar_READY_claimed':False,
 'remaining':['native source-bank SELECT and all bank preparations','admitted whole birth/mark/clock schedule','H1 exact block structure and full source error budget','original full physical Cost-Info source binding'],
 'input_sha256':{str(f.relative_to(D)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
 'full_source_alpha_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'PREPROCESSOR_READY_COMPOSITION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'seven_report_known_macros':n,'bound':'2^-4058','full_source_alpha_proved':False}))
