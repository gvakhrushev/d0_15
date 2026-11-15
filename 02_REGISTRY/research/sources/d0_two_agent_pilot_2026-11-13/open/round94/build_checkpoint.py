#!/usr/bin/env python3
"""Freeze A48 scientific inputs and all independent B94 receipts."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48')
h=lambda p:sha256(Path(p).read_bytes()).hexdigest()
expected={'ALL_ANGLES_REPLAY.json':'PASS_ALL_A48_TARGETS_AND_ALL_ACTUAL_POWERS_RECTANGULAR','LEVEL9_INDEPENDENT_CHECK.json':'PASS_INDEPENDENT_LEVEL9_PHASE_AND_IDEAL_BOUND','CONTROLLED_X_CHECK.json':'PASS_COMBINED_CONTROLLED_X_RECTANGULAR','LOCAL_INVENTORY_CHECK.json':'PASS_A48_LOCAL_ALL_BINDINGS_AND_COMPRESSED_COUNTS','COMPONENT_INVENTORY_CHECK.json':'PASS_ALL_CHOI_UPPER_AND_CAR_EXACT_COMPONENT_INVENTORIES','SOURCE_COMPOSITION_CHECK.json':'PASS_A48_SOURCE_COMPONENT_AND_CORE_STRUCTURE_CONDITIONAL_BUDGET','ACTUAL_VECTOR_JET_CHECK.json':'PASS_ACTUAL_A48_CONTROL_ORDER_SOURCE_PREFIX_AND_JET_BUDGET'}
for name,status in expected.items():assert json.loads((P/name).read_text())['status']==status
checks=json.loads((P/'ALL_ANGLES_REPLAY.json').read_text());assert checks['total_actual_powers_checked']==4306 and checks['all_target_hashes_and_containment_checked']
assert json.loads((P/'LEVEL9_INDEPENDENT_CHECK.json').read_text())['frozen_sha256']==h(A/'LEVEL9_CORRECTION_CERTIFICATE.json')
jet=json.loads((A/'ACTUAL_FULL_VECTOR_SOURCE_JET.json').read_text())
for q,sha in jet['source_sha256'].items():assert h(q)==sha,q
inputs=['two_bit_source_targets.py','source_angle_certifier.py','certify_two_bit_sources.py','TWO_BIT_COFRAME_LIBRARY.json.gz','TWO_BIT_MATERIAL_LIBRARY.json.gz','certify_fixed_source_angles.py','RETUNED_SITE_LIBRARY.json.gz','RETUNED_FIXED_ANGLES.json','certify_level9_correction.py','LEVEL9_CORRECTION_CERTIFICATE.json','two_bit_local_native.py','TWO_BIT_LOCAL_NATIVE_PLAN.json','two_bit_source_native.py','TWO_BIT_SOURCE_COMPONENT_PLAN.json','two_bit_global_source.py','TWO_BIT_GLOBAL_SOURCE_PLAN.json','actual_full_vector_source_jet.py','ACTUAL_FULL_VECTOR_SOURCE_JET.json']
files=['B94_A48_INDEPENDENT_AUDIT_RU.md','replay_all_angles.py','check_level9_phase.py','check_controlled_x.py','audit_local_inventory.py','audit_component_inventory.py','audit_source_composition.py','audit_actual_vector_jet.py',*expected,'build_checkpoint.py']
out={'status':'B94_A48_COMPLETE_SCOPED_INDEPENDENT_AUDIT_CHECKPOINT','A48_inputs_sha256':{n:h(A/n) for n in inputs},'B94_files_sha256':{n:h(P/n) for n in files},'all_4306_native_powers_checked':True,'independent_level9_correction_checked':True,'independent_local_exact_inventory_checked':True,'component_global_counts_are_upper_where_stated':True,'full_SOURCE_DATA_prefix_error_lt':'2^-3423','actual_control_finite_difference_extra_lt':'2^-1642','full_axis_jet_lt':'2^-44','claims_depend_on_B39_A22_A24_B45_and_B93':True,'full_corner_post_clock_or_physical_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'B94_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
