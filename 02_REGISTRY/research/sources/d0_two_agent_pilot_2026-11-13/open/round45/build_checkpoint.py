#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent
reports=['SITE_ANGLE_INDEPENDENT_CHECK.json','SITE_MATRIX_CHECK.json','SITE_NATIVE_CHECK.json','SITE_INVENTORY_CHECK.json'];r=[json.loads((P/x).read_text()) for x in reports];assert all(x['status'].startswith('PASS_') for x in r)
lib=sha256((P/'SITE_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest();native=sha256((P/'site_native.py').read_bytes()).hexdigest();plan=sha256((P/'SITE_NATIVE_PLAN.json').read_bytes()).hexdigest()
assert all(x['library_sha256']==lib for x in r[:3]) and r[2]['native_source_sha256']==native and r[3]['plan_sha256']==plan
assert r[0]['tree_nodes_checked']==255 and r[0]['distinct_tree_angles']==165 and r[1]['full_256_by_256_entries_checked']==65536 and r[2]['A21_external_SITE_binding_and_collision_rejection'] and r[3]['full_SITE_DAG_blocks']==44722
files=['SITE_NATIVE_RU.md','site_targets.py','certify_site_angles.py','SITE_ANGLE_LIBRARY.json.gz','site_native.py','verify_site_angles.py','check_site_matrix.py','check_site_native.py','build_site_plan.py','SITE_NATIVE_PLAN.json','verify_site_inventory.py',*reports]
out={'status':'B45_SITE_NATIVE_CHECKPOINT','file_sha256':{x:sha256((P/x).read_bytes()).hexdigest() for x in files},'PF_total':10946,'tree_nodes':255,'certified_angle_powers':166,'operator_error_lt':'2^-3259','all_256_input_columns':True,'RAW_inverse8_included':True,'new_clean_scratch':0,'gray_phase_CX':256,'full_giant_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'B45_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'library_sha256':lib}))
