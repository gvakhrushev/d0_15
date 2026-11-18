#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent
files=['A20_INDEPENDENT_AUDIT_RU.md','verify_source_targets.py','verify_all_rectangular.py','audit_a20_native.py','check_a20_exact_pairs.py','A20_SOURCE_TARGET_CHECK.json','A20_RECTANGULAR_POWER_CHECK.json','A20_NATIVE_BINDING_AUDIT.json','A20_EXACT_FOCK_COLUMNS.json']
checks=[json.loads((P/x).read_text()) for x in files if x.endswith('.json')]
assert len(checks)==4 and all(x['status'].startswith('PASS_') for x in checks)
assert checks[0]['families']==247 and checks[0]['target_factor_bindings']==1044 and checks[1]['angles']==556 and checks[2]['sector_bindings']==14848 and checks[2]['units']==294144 and checks[3]['controlled_X_arbitrary_aux_exact_columns']==128
h=checks[0]['source_library_sha256'];assert checks[1]['source_library_sha256']==h and checks[2]['library_sha256']==h
out={'status':'B43_INDEPENDENT_A20_CHECKPOINT','pinned_A20_commit':'afbaef2f950da70c0fe16dbdb8091c851929bd7a','A20_library_sha256':h,'file_sha256':{x:sha256((P/x).read_bytes()).hexdigest() for x in files},'families':247,'angles':556,'sector_bindings':14848,'error_lt':'2^-3259','full_native_word_executed':False,'full_Julia_SELECT_complete':False,'physical_C_closed':False,'GR_closed':False}
(P/'B43_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'library_sha256':h}))
