#!/usr/bin/env python3
"""B89 independent A45 paid echo, prefix budget and normalization audit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json,sys,itertools
import sympy as sp
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round45'));import composite_processor_echo as a45
b88=json.loads((O/'round88/B88_COMPOSITE_PROCESSOR_CHECK.json').read_text())
inv=a45.inventory();cfg=a45.production_configuration();bd=a45.budgets()
assert inv['total']['G']==int(b88['echo_G_hex'],16) and inv['total']['CX']==int(b88['echo_CX_hex'],16)
assert inv['pairs']==int(b88['echo_SI_pairs_hex'],16)
assert inv['weight']==int(b88['echo_error_numerator_hex'],16)
assert inv['error']==F(inv['weight'],2**20000)<F(1,2**15846)
assert inv['computational_source_prefix_error']<F(1,2**3232)
assert inv['original_processor_error_upper']<F(1,2**4058)
assert inv['full_genuine_prefix_error']==inv['computational_source_prefix_error']+inv['forward_error']+inv['original_processor_error_upper']
assert inv['full_genuine_prefix_error']<F(1,2**3231)
assert cfg['Nbase']==int(b88['new_Nbase_hex'],16) and cfg['Nbase'].bit_length()==25457 and cfg['K']==137444
# Compare the complete explicit 304-pair address map to independent B88.
ri,sw,rows,choi=a45.address_binding();assert len(sw)==608 and len(rows)==16 and len(choi)==180
bykey={(r['walk'],r['copy']):r for r in rows}
for r in b88['q_car_physical_bindings']:
 q=bykey[r['walk'],r['copy']];assert q['f_slot']==r['f_slot'] and q['q_slot']==r['q_slot']
 assert a45.a.b.physical_wire(q['f_wires'][0])==r['f_DATA_physical_start']
 assert a45.a.b.physical_wire(q['q_wires'][0])==r['q_DATA_physical_start']
 assert a45.a.b.physical_wire(q['f_wires'][12])==r['f_RIGHT_physical_start']
 assert a45.a.b.physical_wire(q['q_wires'][12])==r['q_RIGHT_physical_start']
# Analytic normalized row: c,c' differences <= eps and |c|,|c'|<=1,
# then |c c'−cnew cnew'| <=2 eps; 1/(2 cref)<3/4.
e=inv['error'];gs=F(1,2**3158);z=F(1,2**20);t=F(1,2**1618);u=F(1,2**14623)
extra=F(3,2)*e/gs
assert bd['new_analytic_row_vs_old_actual_row_error']==extra
oldq=a45.p43.budget(cfg);base=a45.old.bounds(cfg)
q=oldq['Qb_full_finite_price_minus_half_ideal_Pf_bound']+extra
assert q==bd['new_Qb_finite_vs_half_old_reduced_Pf_error']<F(1,2**75)
qlow=oldq['concrete_j2_reduced_Pf_lower']/2-q
assert qlow==bd['new_Qb_finite_positive_lower']>F(1,2**45)
incoming=base['incoming_full_H_plus_J_vs_reduced_each_row']+extra
assert incoming==bd['new_Pf_finite_vs_old_reduced_error']<F(1,2**75) and 55*incoming<F(1,2**70)
allq=a45.p44.bounds()['all_SAM_Qb_minus_half_Pf_dual_operator_norm_upper']+extra
assert allq==bd['new_all_real_SAM_Q_analytic_reduction_error']<F(1,2**32)
# Normalizing a perturbed post vector can AMPLIFY its error when ||Mχ||<1.
# r=3/4, eps=1/20 gives an exact counterexample to a general <=eps claim.
R=sp.Rational;rr=R(3,4);ee=R(1,20);rnew=sp.sqrt(rr*rr+ee*ee)
d2=2-2*rr/rnew
assert sp.simplify(d2-ee*ee)>0
# Safe proof: ||a/||a||−b/||b|||| <= 2||a−b||/||b||,
# and ||Mχ||>2/3 ⇒ at most 3 eps. The budget has huge margin.
m=len(cfg['sam']);half=(m+1)//2;mu=base['outgoing_probe_full_op_error'];delta=u+3*e+mu
assert delta<F(1,2**14622)
post=(1<<half)*((1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*t*gs))
post+=base['outgoing_heat_full_finite_covector_dual']
assert post<F(1,2**75)
# Exercise REAL mapped processor boundary emission at both depths. Marks are
# metadata after a completed raw block; every emitted physical gate is G/CX.
nb_leaves=a45.a.c.nb.leaves
for depth in (0,1):
 observed=list(itertools.islice(a45.observer_blocks(depth,include_macro_marks=True),4))
 assert len(observed)==4 and observed[1]['op']=='A45_MARK' and observed[3]['op']=='A45_MARK'
 for tree in (observed[0],observed[2]):
  for gate in nb_leaves(tree):
   assert gate['op'] in ('G','CX') and not set(gate['wires']).intersection(set(range(2,2690)))
# Macro compiler requires a barrier at pending=0. Exercise actual insertion
# skeleton and a genuinely unfinished pair, with tiny artificial trees.
nb=a45.a.c.nb;port=0;spin=(3,4);helper=2;compiler=a45.a.c.Compiler(port,spin,helper,1)
def bad():
 yield nb.gate('SourceI',port,*spin)
 yield {'op':a45.BARRIER}
try:
 list(a45.compile_tagged(bad,compiler,lambda:iter(()),lambda x:x));raise AssertionError('barrier failed')
except AssertionError as exc:assert 'SourceI pair' in str(exc)
# Validate independent file pins after creating the receipt below.
report=(D/'round45/COMPOSITE_PROCESSOR_ECHO_RU.md').read_text()
assert 'δ=e_U+3ε_echo+μ_probe' in report
assert 'НЕ создаёт восьмой независимый tensor' in report
assert 'Mark внутри' in report and 'не переносится автоматически' in report
plan=json.loads((D/'round45/COMPOSITE_PROCESSOR_ECHO_PLAN.json').read_text())
for f,h in plan['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h
outgoing_code=a45.budgets()['new_outgoing_finite_dual_upper']
assert outgoing_code==post
needs_fix=False
files=[Path(__file__),D/'round45/composite_processor_echo.py',D/'round45/COMPOSITE_PROCESSOR_ECHO_PLAN.json',
 D/'round45/check_composite_processor_echo.py',D/'round45/COMPOSITE_PROCESSOR_ECHO_CHECK.json',D/'round45/COMPOSITE_PROCESSOR_ECHO_RU.md',
 D/'round42/FIXED_POST_PAID_FAMILY_RU.md',D/'round43/LOCAL_Q_PRICE_RU.md',D/'round44/JOINT_SOURCE_REDUCTION_RU.md',
 O/'round88/B88_COMPOSITE_PREPARED_PROCESSOR_RU.md',O/'round88/B88_COMPOSITE_PROCESSOR_CHECK.json']
out={'status':'OUTGOING_NORMALIZATION_FACTOR_NEEDS_CORRECTION' if needs_fix else 'PASS_PAID_COMPOSITE_ECHO_WITH_NORMALIZATION',
 'final_A45_report_checked_and_pinned':True,'explicit_304_address_pairs_match_B88':True,'echo_G_CX_counts_and_full_clock_match_B88':True,
 'genuine_full_processor_map_error_lt':'2^-3231, at closed processor boundaries and stated source-input domain',
 'q_and_incoming_recomputed_budgets_pass':True,'Qb_finite_j2_lower_gt':'2^-45',
 'normalization_counterexample_exact':True,'safe_outgoing_state_delta':'eU+3*eEcho+probeError',
 'safe_outgoing_feedback_plus_heat_dual_lt':'2^-75',
 'code_outgoing_bound_smaller_than_conservative_3eps_bound':needs_fix,
 'real_closed_report_templates_tested_both_depths':True,'incomplete_SourceI_barrier_rejected':True,'all_original_prefixes_or_strong_unsplit_admission_proved':False,
 'GR_closed':False,'source_sha256':{str(f.resolve()):sha256(f.read_bytes()).hexdigest() for f in files}}
Path(__file__).with_name('B89_COMPOSITE_ECHO_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
