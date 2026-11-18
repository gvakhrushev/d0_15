#!/usr/bin/env python3
"""Pin actual A30/A32 structure for D-contract review, not task admission."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json,sys
import sympy as s
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round32'))
import finite_book_comparison as a32
S=a32.core
ns=S.g.namespace();st=S.stages();reports=ns['reports'];layout=ns['layout']
assert [r['bank'] for r in reports]==['y+','y-','f','0','x+','x-','q']
assert len({r['all_READY'] for r in reports})==7 and len({r['REPORT'] for r in reports})==7
assert len(layout['SAM'])==2688 and len(layout['SITE'])==8 and len(layout['SC6_selectors'])==5
assert all(len(r['source_slots'])==196 for r in reports)
assert len(ns['source_slots'])==1372
counts=Counter(v['kind'] for v in st)
assert counts=={'SITE':1,'SIGMA':7,'SOURCE':1372,'RAW_RESOURCE_FRAME':2,'REPORT':7,'PORT_ZERO':1,'SC6':1}
firstframe=next(i for i,v in enumerate(st) if v['kind']=='RAW_RESOURCE_FRAME')
assert all(v['kind']!='REPORT' for v in st[:firstframe+1])
assert st[firstframe:firstframe+2]==[{'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0},{'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}]
assert len(S.resource_wires())==29848
plan=json.loads((D/'round32/FINITE_BOOK_COMPARISON_PLAN.json').read_text())
assert plan['initial_history']['H0']=='C' and plan['initial_history']['P0']=='I_1'
assert plan['early_canonical_RAW_births']==10407050782 and plan['late_retention_pairs']==66076
plus=a32.endpoint_parts('plus',2);minus=a32.endpoint_parts('minus',2)
assert plus['last_g']==minus['last_g'] and S.b.physical_tree(plus['last_g'])=={'op':'G','wires':[4]}
assert int(plan['same_pre_core_calls'])==int(plan['same_post_core_calls'])
ready=json.loads((O/'round53/READY_NATIVE_APPROX_INTERVAL.json').read_text())
assert ready['status']=='PASS_UNIFORM_APPROXIMATE_NATIVE_READY_BOUND'
assert ready['READY_effect_distance_to_ideal_scalar_I_lt']=='2^-4060'
assert ready['exact_actual_effect_scalar_or_field_independent'] is False
# Exact original ideal-comparator derivatives at a fixed SITE.  This does
# not assert an actual independent operand or a native continuous path.
lam,yp,ym,pxp,pxm,pf,pq,p0=s.symbols('lam yp ym pxp pxm pf pq p0')
xi=(yp-ym)*(pf-p0)+(pxp-pxm)*(pq-p0)
Q=lam*(4+xi)
assert s.expand(s.diff(Q,p0)+lam*(yp-ym+pxp-pxm))==0
assert s.expand(s.diff(Q,lam)-(4+xi))==0
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
files=[Path(__file__),D/'round25/h1_namespace.py',D/'round26/FULL_READY_AND_GAIN_RU.md',D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round30/marked_source_schedule.py',D/'round30/COMMON_RAW_SOURCE_MARKS_RU.md',D/'round32/finite_book_comparison.py',D/'round32/FINITE_BOOK_COMPARISON_PLAN.json',D/'round32/FINITE_FULL_BOOK_COMPARISON_RU.md',O/'round53/READY_NATIVE_APPROX_INTERVAL.json',O/'round60/B60_ORIGINAL_MARKS_COMMON_CHECKPOINT_RU.md',O/'round68/B68_A35_BINDING_AUDIT_RU.md',root/'02_REGISTRY/research/A4D_SCOPED_NATIVE_KAPPA_CONTRACT_2026_11_03.md',root/'02_REGISTRY/research/A4D_NATIVE_RETURN_RECORD_SOURCE_GATE_2026_11_03.md',root/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md',root/'02_REGISTRY/research/sources/d0_retained_response_concentration_2026-10-28/KAPPA_CLOSURE_RU.md',root/'03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean',root/'03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean']
out={'status':'STRUCTURAL_TASK_INPUT_LEDGER_PINNED_NOT_ADMISSION_PROOF','A30_banks':[r['bank'] for r in reports],'separate_READY_and_REPORT_outputs_per_bank':7,'source_slots':len(ns['source_slots']),'A30_paid_B_R_data_wires':len(S.resource_wires()),'A30_one_shared_SITE':True,'A32_initial_cut_P0':'I_1 on H0=C, not reporter reference P_0','A32_SAM_j2_last_physical_G_wire':4,'A32_actual_native_READY_is_exact_scalar_proved':False,'original_task_same_pair_membership_proved_by_this_checker':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in files}}
(P/'ACTUAL_TASK_INPUT_LEDGER.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'bank_count':len(reports),'BR_wires':out['A30_paid_B_R_data_wires']}))
