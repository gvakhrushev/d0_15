#!/usr/bin/env python3
"""Freeze scalar M3 and same-reader fixed-post weight receipts."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=P.parent
h=lambda f:sha256(Path(f).read_bytes()).hexdigest()
checks={'SCALAR_THIRD_DERIVATIVE_CHECK.json':'PASS_UNIFORM_I_TAU_THIRD_DERIVATIVE_ON_B21_CUBE','FIXED_POST_WEIGHT_CHECK.json':'PASS_A49_BORN_PRODUCT_FIXED_POST_WEIGHTED_SCALAR_SOURCE'}
for name,status in checks.items():
 row=json.loads((P/name).read_text());assert row['status']==status
 for path,digest in row['source_sha256'].items():assert h(path)==digest,path
assert json.loads((P/'SCALAR_THIRD_DERIVATIVE_CHECK.json').read_text())['I_tau_third_derivative_norm_lt']=='2^31'
assert json.loads((P/'FIXED_POST_WEIGHT_CHECK.json').read_text())['actual_Pf_price_source_row_lt']=='2^-108'
files=['B97_SCALAR_M3_AND_FIXED_POST_WEIGHT_RU.md','certify_scalar_third_derivative.py','check_fixed_post_weight.py',*checks,'build_checkpoint.py']
inputs=[O/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',O/'round95/B95_CHECKPOINT.json',O/'round96/B96_CHECKPOINT.json',D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json',D/'round49/CORNER_AND_PRICE_BRIDGE.json']
out={'status':'B97_SCOPED_SCALAR_M3_AND_ACTUAL_PF_PRICE_CHECKPOINT','file_sha256':{n:h(P/n) for n in files},'input_sha256':{str(f):h(f) for f in inputs},'uniform_I_tau_M3_lt':'2^31','born_product_scalar_quadratic_bias_lt':'2^-109','actual_A49_Pf_H_plus_J_row_lt':'2^-108','old_correlated_rho_or_other_price_rows_proved':False,'original_Dnu_or_Cost_Info_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'B97_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
