#!/usr/bin/env python3
"""Freeze B96 audit receipts and current A49 executable scientific inputs."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');A=D/'round49'
h=lambda f:sha256(Path(f).read_bytes()).hexdigest()
checks={'PAID_PADDING_CHECK.json':'PASS_ONE_PASS_PAID_PADDING_FIXTURES','ACTUAL_TARGET_FIXTURE_CHECK.json':'PASS_A49_ACTUAL_FINITE_PATH_AND_POST_FIXTURES','CODE_SUPPORT_CHECK.json':'PASS_COMPOSITIONAL_CODE_CONTROL_ONLY_SUPPORT','FOUR_SLOT_SCHEDULE_CHECK.json':'PASS_INDEPENDENT_13_ARMS_PAD_MARKS_CLOCK','PRODUCTION_PLAN_CHECK.json':'PASS_A49_PRODUCTION_PADDED_UPPER_CLOCK_ARITHMETIC','CORNER_LAW_CHECK.json':'PASS_FOUR_VALUED_A27_CORNER_EXTENSION_CONDITIONAL_OWNERS','PRICE_BRIDGE_CHECK.json':'PASS_A49_TYPED_CORNER_GAIN_AND_SHARED_BANK_BRIDGE'}
for f,status in checks.items():assert json.loads((P/f).read_text())['status']==status
for x in ('ACTUAL_TARGET_FIXTURE_CHECK.json','CORNER_LAW_CHECK.json'):
 for f,sha in json.loads((P/x).read_text()).get('source_sha256',{}).items():assert h(f)==sha,f
inputs=['paid_padding.py','finite_actual_target.py','two_bit_paid_family.py','TWO_BIT_PAID_FAMILY_PLAN.json','check_two_bit_paid_family.py','TWO_BIT_PAID_FAMILY_CHECK.json','corner_and_price_bridge.py','CORNER_AND_PRICE_BRIDGE.json']
files=['B96_A49_PAID_SCHEDULE_AND_CORNER_RU.md','audit_paid_padding.py','audit_actual_target.py','audit_code_support.py','audit_four_slot_schedule.py','audit_production_plan.py','audit_corner_law.py','audit_price_bridge.py',*checks,'build_checkpoint.py']
out={'status':'B96_A49_SCOPED_INDEPENDENT_AUDIT_CHECKPOINT','A49_inputs_sha256':{n:h(A/n) for n in inputs},'B96_files_sha256':{n:h(P/n) for n in files},'Python39_popcount_failure_corrected_before_freeze':True,'production_target_or_word_evaluated':False,'conditional_A27_typed_corner_error_lt':'2^-3421','conditional_typed_actual_M_gt':'2/3','original_Dnu_or_vacuum_extension_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'B96_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
