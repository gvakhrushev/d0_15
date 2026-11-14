#!/usr/bin/env python3
"""Pin completed B42 sources, finite receipts and explicit open boundary."""
from pathlib import Path
from hashlib import sha256
import json,gzip
P=Path(__file__).resolve().parent
names=['SOURCE_NAME_CHECK.json','INDEPENDENT_PROPER_LINK_ANGLES.json','RECTANGULAR_SAMPLE_CHECK.json','NATIVE_PROPER_LINK_CHECK.json','FULL_JULIA_SCHEDULE_CHECK.json','PYTHON_FALLBACK_CHECK.json','PROPER_LINK_NATIVE_RESOURCES.json']
results={x:json.loads((P/x).read_text()) for x in names}
for x,r in results.items():assert r['status'].startswith('PASS_') or r['status']=='EXACT_PROPER_LINK_BANK_NATIVE_INVENTORIES',x
with gzip.open(P/'PROPER_LINK_ANGLE_LIBRARY.json.gz','rt') as f:lib=json.load(f)
lh=sha256((P/'PROPER_LINK_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest();nh=sha256((P/'proper_link_native.py').read_bytes()).hexdigest()
for x in ('INDEPENDENT_PROPER_LINK_ANGLES.json','RECTANGULAR_SAMPLE_CHECK.json','NATIVE_PROPER_LINK_CHECK.json','FULL_JULIA_SCHEDULE_CHECK.json','PROPER_LINK_NATIVE_RESOURCES.json'):assert results[x]['library_sha256' if x=='INDEPENDENT_PROPER_LINK_ANGLES.json' else 'angle_library_sha256' if x in ('NATIVE_PROPER_LINK_CHECK.json','FULL_JULIA_SCHEDULE_CHECK.json','PROPER_LINK_NATIVE_RESOURCES.json') else 'library_sha256']==lh
assert results['NATIVE_PROPER_LINK_CHECK.json']['actual_native_source_sha256']==nh and results['FULL_JULIA_SCHEDULE_CHECK.json']['native_emitter_sha256']==nh and results['PROPER_LINK_NATIVE_RESOURCES.json']['native_emitter_sha256']==nh
assert lib['angles']==5018 and results['INDEPENDENT_PROPER_LINK_ANGLES.json']['angles']==5018 and results['NATIVE_PROPER_LINK_CHECK.json']['actual_lift_depth2_and_outer_depth3_checked']
files=['PROPER_LINK_NATIVE_RU.md','PROPER_LINK_ANGLE_LIBRARY.json.gz','proper_link_targets.py','certify_proper_link.py','proper_link_native.py','verify_source_names.py','verify_proper_link_angles.py','verify_rectangular_sample.py','check_native_proper_link.py','check_full_julia_schedule.py','check_python_fallback.py','build_resource_receipt.py',*names]
out={'status':'B42_PROPER_LINK_NATIVE_CHECKPOINT','file_sha256':{x:sha256((P/x).read_bytes()).hexdigest() for x in files},'families':336,'angles':5018,'sector_entries':23296,'max_native_multiplier_power':23,'proper_link_bank_operator_error_lt':'2^-3257','literal_inverse_depth3_checked':True,'huge_word_executed':False,'full_Julia_SELECT_complete':False,'physical_C_closed':False,'GR_closed':False}
(P/'B42_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'files':len(files),'library_sha256':lh}))
