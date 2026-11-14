#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round21')
reports=['A21_INDEPENDENT_INTEGRATION_CHECK.json','A21_NAMESPACE_CONTROL_CHECK.json','A21_LITERAL_DEPTH_CHECK.json','A21_ACTUAL_DEPTH_SAMPLES.json'];results=[json.loads((P/x).read_text()) for x in reports];assert all(x['status'].startswith('PASS_') for x in results)
assert results[0]['data_wires']==22 and results[0]['private_wires']==24 and results[0]['standard_outer_comparator_extra_clean_wires']==45
assert results[1]['coframe_units']==294144 and results[1]['link_commands']==1781504 and results[2]['half_levels_0_to_2_depths_0_to_3'][-1]['primitive_leaves']==73763 and results[3]['proper_link_literal_depth_through_5']
hashes=results[0]['input_sha256'];assert all(sha256(Path(q).read_bytes()).hexdigest()==h for q,h in hashes.items())
sourcehash=sha256((D/'choi_loader.py').read_bytes()).hexdigest();assert all(r['source_sha256' if i==1 else 'A21_source_sha256']==sourcehash for i,r in enumerate(results) if i in (1,2,3))
files=['A21_INDEPENDENT_INTEGRATION_RU.md','audit_loader_integration.py','audit_control_namespace.py','check_provider_literal_depths.py','check_actual_stage_depths.py',*reports]
out={'status':'B44_INDEPENDENT_A21_INTEGRATION_CHECKPOINT','A21_input_sha256':hashes,'file_sha256':{f:sha256((P/f).read_bytes()).hexdigest() for f in files},'Omega_error_lt':'2^-3250','half_joint_anchor_error_lt':'2^-3230','private_clean_wires':24,'joint_anchor_wires':46,'additional_A13_comparator_clean_wires':45,'outer_reflection_compiled':False,'full_giant_word_executed':False,'physical_C_closed':False,'GR_closed':False}
(P/'B44_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'A21_source_sha256':sourcehash}))
