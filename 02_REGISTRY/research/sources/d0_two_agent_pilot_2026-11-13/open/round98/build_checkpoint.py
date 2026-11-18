#!/usr/bin/env python3
"""Pin A50 inputs and independent B98 receipts."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');A=D/'round50'
h=lambda f:sha256(Path(f).read_bytes()).hexdigest()
checks={'NONSYMMETRIC_CLOCK_FIXTURE_CHECK.json':'PASS_NONSYMMETRIC_KERNEL_AND_EXACT_GROWING_CLOCK_SWAP','SPLIT_INSERTION_CHECK.json':'PASS_A48_CLOSED_Q_CUTS_AND_ALL_INSERTION_TELESCOPE','KERNEL_AND_PB_CHECK.json':'PASS_SYMBOLIC_DIMENSION_FREE_KERNEL_AND_PB_SLOT','INDEPENDENT_ROW_BOUNDS_CHECK.json':'PASS_INDEPENDENT_A50_ROW_ARITHMETIC_AND_NORM'}
for name,status in checks.items():assert json.loads((P/name).read_text())['status']==status
for p,digest in json.loads((P/'SPLIT_INSERTION_CHECK.json').read_text())['source_sha256'].items():assert h(p)==digest,p
plan=json.loads((A/'INDEPENDENT_PRICE_ROWS_PLAN.json').read_text())
for p,digest in plan['source_sha256'].items():assert h(p)==digest,p
files=['B98_A50_INDEPENDENT_PRICE_ROWS_RU.md','check_nonsymmetric_and_clock.py','audit_split_and_transducer.py','check_kernel_and_pb.py','audit_price_bounds.py',*checks,'build_checkpoint.py']
inputs=['independent_price_rows.py','INDEPENDENT_PRICE_ROWS_PLAN.json','check_independent_price_rows.py','INDEPENDENT_PRICE_ROWS_CHECK.json','FOUR_INDEPENDENT_PRICE_ROWS_RU.md','ROOT_REVIEW_B97.json']
out={'status':'B98_SCOPED_FOUR_INDEPENDENT_PRICE_ROWS_AUDIT','A50_input_sha256':{x:h(A/x) for x in inputs},'B98_file_sha256':{x:h(P/x) for x in files},'all_insertion_replacement_bound_lt':'2^-15800','four_2688_axis_price_rows_Euclidean_norm_lt':'2^-102','actual_kernel_assumed_symmetric':False,'full_clock_Q_swap_proved_with_stated_scope':True,'full_original_marks_transport_proved':False,'all_skew_finite_or_original_Vh_norm_proved':False,'production_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'B98_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
