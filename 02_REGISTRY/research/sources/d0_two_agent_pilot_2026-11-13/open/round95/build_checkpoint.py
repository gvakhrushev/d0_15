#!/usr/bin/env python3
"""Pin B95 conditional bounds and original owner dependencies."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;B=P.parent;repo=B.parents[3];D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
h=lambda f:sha256(Path(f).read_bytes()).hexdigest()
checks={'FOUR_SLOT_CONDITIONAL_CHECK.json':'PASS_CONDITIONAL_FOUR_SLOT_HEAT_AND_KERNEL_CONTRACT','QUADRATIC_LIFT_CHECK.json':'PASS_EXACT_CENTERED_PRODUCT_QUADRATIC_CANCELLATION','FOUR_SLOT_FIXTURE_CHECK.json':'PASS_INDEPENDENT_Q_SLOTS_COUNTEREXAMPLE'}
for f,status in checks.items():assert json.loads((P/f).read_text())['status']==status
for rec in ('FOUR_SLOT_CONDITIONAL_CHECK.json','QUADRATIC_LIFT_CHECK.json'):
 for f,digest in json.loads((P/rec).read_text())['source_sha256'].items():assert h(f)==digest,f
source=B.parents[2]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
assert source.exists(),source
inputs=[source,B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',B/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',B/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',B/'round94/B94_CHECKPOINT.json',D/'round42/FIXED_POST_PAID_FAMILY_RU.md',D/'round43/LOCAL_Q_PRICE_RU.md',D/'round44/JOINT_SOURCE_REDUCTION_RU.md',D/'round47/FULL_VECTOR_CONTROL_PLAN.json',D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json',D/'round48/ACTUAL_FULL_VECTOR_SOURCE_JET.json']
files=['B95_FOUR_SLOT_PRICE_AND_MARK_CONTRACT_RU.md','check_four_slot_contract.py','check_quadratic_lift.py','check_independent_slot_fixture.py',*checks,'build_checkpoint.py']
out={'status':'B95_CONDITIONAL_FOUR_SLOT_PRICE_AND_MARK_CONTRACT','B95_files_sha256':{n:h(P/n) for n in files},'source_sha256':{str(f):h(f) for f in inputs},'four_control_slots_independent':True,'joint_matched_chronology':'plus,minus,plus,minus; fixed post afterwards','full_native_heat_or_price_executed':False,'quad_scalar_lemma_product_state_only':True,'M3_or_new_physical_price_proved':False,'Q_kernel_bound_conditional_on_A44_insertion_and_corner_contracts':True,'original_Dnu_mark_transport_or_physical_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'B95_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
