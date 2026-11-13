#!/usr/bin/env python3
"""Independent arithmetic and scope audit of A15/B31 one-preprocessor composition."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def read(p): return json.loads(p.read_text())
a12=read(D/'round12/SELECTOR_COMPILATION.json'); a13=read(D/'round13/CIRCUIT_COMPILATION.json'); a15=read(D/'round15/SOURCE_DISPATCH_COMPILATION.json'); comp=read(D/'round15/PREPROCESSOR_READY_COMPOSITION.json')
assert 2*455+8*18==1054
M=1054*7*1374+10*7*1580+94+196
assert M==10248262==a12['selector_fair_qubits_per_report']
assert F(447,200)**2 < 5  # 1-2p^3 = 5-2sqrt(5) < 53/100
fi=1-F(a12['ready_probabilities']['internal_slot']); ft=1-F(a12['ready_probabilities']['top_slot'])
bound=M*F(53,100)**28+1054*fi**7+10*ft**7
assert bound==F(comp['failure_union_bound_rational']) and bound<F(1,2)
n13=7*sum(a13['decoder_label_routing_counts_per_report'][op] for op in ('X','CCX'))
n15=7*(144939804+9281032152); assert n15==7*sum(a15['ten_sign_report_controller_counts'][op] for op in ('X','CCX'))
n31=7*M*59; n=n13+n15+n31
assert (n13,n15,n31,n)==(92263351768,65981803692,4232532206,162477687666) and n<2**38
with localcontext() as c:
 c.prec=50
 d=lambda x:Decimal(x.numerator)/Decimal(x.denominator)
 p=(Decimal(5).sqrt()-1)/2
 q=(1-(1-2*p**3)**28)**M
 Q=q*(1-d(fi)**7)**1054*(1-d(ft)**7)**10
 out={'status':'PASS_CONDITIONAL_PREPROCESSOR_ARITHMETIC','fair_bits':M,'slots_internal':1054,'slots_top':10,'failure_union_bound_decimal':str(d(bound)),'ideal_fair_READY_probability_decimal':str(q),'ideal_one_preprocessor_READY_probability_decimal':str(Q),'ideal_seven_independent_preprocessors_joint_probability_decimal':str(Q**7),'known_seven_report_macro_error_count':n,'known_seven_report_macro_norm_error_lt':'2^-4058','assumptions':'Scalar selector success effects and disjoint fresh bank coins; immutable READY; B31 ideal factorization; component schedules and A14 bound assumed, not a complete physical graph.','full_H1_alpha_proved':False,'physical_C_closed':False,'GR_closed':False,'input_sha256':{str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'round12/SELECTOR_COMPILATION.json',D/'round13/CIRCUIT_COMPILATION.json',D/'round15/SOURCE_DISPATCH_COMPILATION.json',D/'round15/PREPROCESSOR_READY_COMPOSITION.json']}}
Path(__file__).with_name('PREPROCESSOR_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
