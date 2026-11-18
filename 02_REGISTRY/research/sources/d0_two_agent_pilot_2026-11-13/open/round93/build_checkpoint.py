#!/usr/bin/env python3
"""Freeze only B93 results, with inherited B42 and B80 provenance."""
from pathlib import Path
from hashlib import sha256
import json,gzip
P=Path(__file__).resolve().parent;B=P.parent
h=lambda x:sha256(Path(x).read_bytes()).hexdigest()
target=json.loads((P/'FULL_TARGET_CHECK.json').read_text());ind=json.loads((P/'INDEPENDENT_CHECK.json').read_text());replay=json.loads((P/'FULL_PRECISION_REPLAY.json').read_text());upper=json.loads((P/'PROPER_LINK_RESOURCE_UPPER.json').read_text())
assert target['status']=='PASS_ALL_TWO_BIT_PROPER_LINK_TARGET_FAMILIES' and target['all_families']==20496 and target['angles']==307416
assert ind['status']=='PASS_FULL_CATALOGUE_GRID_AND_INDEPENDENT_NATIVE_POWER_WITNESSES' and ind['all_catalogue_sectors_checked']==1055488
assert replay['status']=='PASS_ALL_FAMILIES_REPLAY_4352_BITS' and replay['angles']==307416
assert target['family_receipts_sha256']==replay['family_receipts_sha256']==h(P/'TWO_BIT_FAMILY_RECEIPTS.jsonl.gz')
assert upper['status']=='SAFE_COMPONENTWISE_UPPER_NOT_ACTUAL_PRICE'
files=['B93_TWO_BIT_PROPER_LINK_RU.md','proper_link_two_bit_targets.py','proper_link_two_bit_native.py','certify_short_grid.py','full_catalogue_validate.py','full_precision_replay.py','independent_check.py','resource_bounds.py','exact_resource_inventory.py','SHORT_GRID_CERTIFICATE.json','SHORT_GRID_K15_E3460.json','SHORT_GRID_K24_E3460.json','SHORT_GRID_K46_E3460.json','TWO_BIT_FAMILY_RECEIPTS.jsonl.gz','FULL_TARGET_CHECK.json','FULL_PRECISION_REPLAY.json','INDEPENDENT_CHECK.json','PROPER_LINK_RESOURCE_UPPER.json','build_checkpoint.py']
with gzip.open(B/'round42/PROPER_LINK_ANGLE_LIBRARY.json.gz','rt') as f:old=json.load(f)
deps=dict(old['source_sha256'])
for path in [B/'round42/proper_link_targets.py',B/'round42/proper_link_native.py',B/'round42/B42_CHECKPOINT.json',B/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json',P/'certify_short_grid.py']:
 deps[str(path)]=h(path)
for path,sha in deps.items():assert h(path)==sha,path
out={'status':'B93_FULL_TARGET_AND_LAZY_NATIVE_PROPER_LINK_CHECKPOINT','file_sha256':{x:h(P/x) for x in files},'inherited_dependency_sha256':deps,'variable_families':20480,'fixed_families':16,'angles_checked':307416,'logical_sectors':1055488,'short_grid_controls':29,'per_bank_proper_link_error_lt':'2^-3453','native_angles_all_materialized':False,'exact_numeric_full_inventory_evaluated':False,'full_source_or_corner_compiled':False,'sourceI_replacement_compiled':False,'physical_C_closed':False,'GR_closed':False}
(P/'B93_CHECKPOINT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
