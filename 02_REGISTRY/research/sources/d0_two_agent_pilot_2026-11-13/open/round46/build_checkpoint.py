#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;B=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round22');h=lambda p:sha256(Path(p).read_bytes()).hexdigest()
reports=['GRAY_PHASE_INDEPENDENT_CHECK.json','GRAY_GRAMMAR_INDEPENDENT_CHECK.json','FULL_CHOI_INDEPENDENT_AUDIT.json','FULL_CHOI_LITERAL_CHECK.json'];r=[json.loads((P/x).read_text()) for x in reports];assert all(q['status'].startswith('PASS_') for q in r)
assert r[0]['controlled_widths']==[8,46] and r[1]['exact_all_columns_and_inverses']==1920 and r[2]['exact_joint_vs_DATA_only_counterexample'] and len(r[3]['cases'])==8
for path,digest in r[0]['input_sha256'].items():assert h(path)==digest
for path,digest in r[2]['input_sha256'].items():assert h(path)==digest
assert r[1]['source_sha256']==h(D/'gray_reflection.py') and r[3]['source_sha256']==h(D/'full_choi_bank.py')
car=json.loads((P/'CAR_VACUUM_FOURIER_TARGET.json').read_text());budget=json.loads((P/'CONDITIONAL_H1_COMPONENT_BUDGET.json').read_text());assert car['shorter_controlled_quarter_turn_route']['nonzero_coefficient_nodes']==318 and car['shorter_controlled_quarter_turn_route']['max_sum_coefficient_per_k']==18 and budget['this_is_not_eta_A']
for z in (car,budget):
 for path,digest in z['input_sha256'].items():assert h(path)==digest
files=['A22_GRAY_AND_CHOI_INDEPENDENT_RU.md','ORIGINAL_H1_PHYSICAL_GATE_RU.md','audit_gray_powers.py','audit_gray_grammar.py','audit_full_choi_bank.py','check_full_choi_literal.py','audit_car_vacuum_fourier_target.py','conditional_h1_budget.py','CAR_VACUUM_FOURIER_TARGET.json','CONDITIONAL_H1_COMPONENT_BUDGET.json',*reports]
owner=B.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md';assert owner.exists()
out={'status':'B46_GRAY_FULL_CHOI_REVIEW_AND_ORIGINAL_PHYSICAL_GATE','file_sha256':{x:h(P/x) for x in files},'owner_H1_source_sha256':h(owner),'gray_K8_K46_certified':True,'full_Choi_all_DATA_columns_private_initial_zero':True,'actual_full_Choi_word_executed':False,'CAR_fourier_short_route_nodes':318,'CAR_fourier_native_prefix_emitted':False,'component_error_bound_conditional_only':True,'full_H1_writer_admission_proved':False,'full_alpha_lower_bound_proved':False,'actual_T6_scalar_proved':False,'full_Cost_Info_binding_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'B46_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'files':len(files),'owner_sha256':out['owner_H1_source_sha256']}))
