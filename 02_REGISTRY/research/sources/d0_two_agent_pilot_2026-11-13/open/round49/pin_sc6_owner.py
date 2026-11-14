#!/usr/bin/env python3
"""Pin exact owner wording of the pre-sign interface, not its physical admission."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;owner=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md');data=owner.read_bytes();s=data.decode();phrases=['Convert the actual canonical born port v=(sqrt(p),p)=G|0> by the paid G^-1.','All five selector bits are canonical raw births','T=V G_port^-1.','The first 20\nare the same specified canonical born factors','SAM is a NEW m-bit sampling register born AFTER the old physical cut:','SITE is fresh WORK with paid loader O_chi B_SITE*','The canonical bank checkpoint fixes WORK/SITE at the writer\'s entry;','The actual reverse is the paid reverse of the actual\nforward word']
for phrase in phrases:assert phrase in s,phrase
out={'status':'PASS_LITERAL_SC6_AND_H1_OWNER_INPUT_PINS','owner_path':str(owner),'owner_sha256':sha256(data).hexdigest(),'anchored_phrases':phrases,'owner_ranges':{'born_port':'112343–112350','selector_raw':'112354–112365','SC6_T_W_canonical_cut':'113496–113535','H1_canonical_SAM_SITE_WORK':'171556–171592','H1_scalar_corner_and_native_T6':'171596–171690'},'owner_mathematical_statement_is_not_global_stage_admission_proof':True,'GR_closed':False}
(P/'SC6_OWNER_PIN.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'sha256':out['owner_sha256']}))
