#!/usr/bin/env python3
"""Build finite target-level input/output and reader catalogue; no invented stages."""
from pathlib import Path
import hashlib,json
import targets as t
P=Path(__file__).resolve().parent
A11=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round11')
bind=json.loads((A11/'PERIODIC_SOURCE_BINDING.json').read_text());assert bind['A_active']==2049
assert len(bind['site_bindings'])==256 and len(bind['leaf_templates'])==282
for i,row in enumerate(bind['site_bindings']):
 assert tuple(row['site'])==t.SITES[i] and len(row['leaf_addresses_in_template_order'])==282
 for j,leaf in enumerate(bind['leaf_templates']):
  address=row['leaf_addresses_in_template_order'][j]
  if leaf['kind']=='Choi':assert 1<=address<2049
  else:assert leaf['kind']=='CAR' and 0<=address<256
assert sum(len(r['leaf_addresses_in_template_order']) for r in bind['site_bindings'])==72192
# Preserve exact primary tensor operand mapping locally, without changing it.
raw=(A11/'PERIODIC_SOURCE_BINDING.json').read_bytes();(P/'SOURCE_LEAF_BINDING.json').write_bytes(raw)
slots=[json.loads(x) for x in (P.parent/'round23/COPY_SLOTS.jsonl').read_text().splitlines()]
assert len(slots)==1372
(P/'COPY_SLOTS.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in slots))
copycount={bank:{kind:sum(s['bank']==bank and s['type']==kind for s in slots) for kind in ('Choi','material')} for bank in t.BANKS}
assert all(x=={'Choi':180,'material':16} for x in copycount.values())
counts={}
for leaf in bind['leaf_templates']:counts[leaf['kind']]=counts.get(leaf['kind'],0)+1
assert counts=={'Choi':272,'CAR':10}
cat={'status':'EXACT_TARGET_OPERAND_AND_OUTPUT_CATALOG_NOT_PHYSICAL_STAGE_LIST',
 'banks':[{'call_index':i,'name':b,'per_site_leaf_counts':counts,'sites':256,'logical_leaf_addresses':72192,'Choi_copy_bound':copycount[b]['Choi'],'material_copy_bound':copycount[b]['material'],'retained_outputs':['full_Choi_address_input_output_and_padding','all_CAR_site_grade_and_fresh_RIGHT','signs_selectors_ready_report_and_failure','oldRIGHT_identity']} for i,b in enumerate(t.BANKS)],
 'logical_banks_times_leaf_bindings':7*72192,'leaf_definition':'SOURCE_LEAF_BINDING.json leaf_templates[leaf], site_bindings[site].leaf_addresses_in_template_order[leaf]; exact A11 data','leaf_binding_sha256':hashlib.sha256(raw).hexdigest(),
 'reference_and_current_fields':'targets.fields(bank,label) or precision_name.at_site(bank,site,label)',
 'Choi_input_output':'(a,i,j), a<2049 active; a>=2049 padded; anchor=(0,0,0), all 32×32 local columns',
 'material_input_output':'256 internal sites ×16 grades ×128 independent fresh RIGHT; psi in grades 0,15, filler14 and clock1 retained',
 'shared_external_SITE':'one 8-qubit control with weight N_x/10946, separate from internal sites; all 256 inputs of O_chi (G^tensor8)^T',
 'sampling_input':'2688 born SAM; Y_b = chart^-1(chart(Y0)+2^-30(b-p^2)); central Y0 is distinct from all-zero b',
 'optional_unsplit_current_mark':'one additional full Z_current=(u,U,Psi,rho) bank if demanded by original unsplit mark; not an eighth comparator report; copies and compiled placement depend on actual required mark',
 'logical_checkpoint_contract':['canonical RAW births and bank/Fourier vacuum prefix','SITE prepared and held as control','each Choi and CAR prepared from known fresh resources','original sign selectors/READY/reports/failures','seven-call comparator and pre-sign event','paid reverses and required reader transport; retain protected D/oldRIGHT'],
 'physical_stage_ordinals':None,'marked_prefix_maps_and_reader_seal_list_compiled':False,'gate_addresses_birth_order_and_costs_compiled':False,'native_word':False,'GR_closed':False}
(P/'MARK_OUTPUT_CATALOG.json').write_text(json.dumps(cat,indent=2)+'\n')
print(json.dumps({'banks':len(cat['banks']),'leaves_per_site':counts,'bound_address_entries':cat['logical_banks_times_leaf_bindings'],'copy_slots':len(slots)}))
