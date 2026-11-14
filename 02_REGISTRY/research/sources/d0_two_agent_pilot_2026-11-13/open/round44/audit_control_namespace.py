#!/usr/bin/env python3
"""Audit all actual SELECT bindings and protected wires without expanding masks."""
from pathlib import Path
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round21');sys.path.insert(0,str(D));import choi_loader as c
lay=c.layout();x=c.inputs();sam=set(lay['SAM']);address=set(lay['address']);ro=sam|address|{lay['branch']};forbid={lay['phase_rebit'],*lay['comparator_scratch'],lay['oldRIGHT_witness'],*lay['choi_input']};outputs=set(lay['choi_output']);lf={r['family']:r for r in x['link']['families']};cf=0;ln=0
for bank in ('y+','y-','f','0','x+','x-','q'):
 for row in x['coframe']['catalogue'][bank]:
  for b,d in c.coframe.sector_units(row,x['coframe'],lay):
   ctrl=b['controls'];pat=b['pattern'];assert len(ctrl)==len(set(ctrl))==len(pat) and lay['branch'] in ctrl and pat[ctrl.index(lay['branch'])]==1
   assert set(lay['address'])<=set(ctrl) and b['target'] not in ro|forbid and not set(ctrl+[b['target']])&forbid
   assert set(b['controls'])&sam=={lay['SAM'][i] for i in row['SAM_indices']}
   assert b['target'] in outputs|{lay['aux_arbitrary']} and d in (0,1)
   for g in b['permutation']:assert g['op']=='CX' and set(g['wires'])<=outputs
   cf+=1
 for row in x['link']['catalogue'][bank]:
  local=c.link.bind_global(lay,row)
  for z in c.link.commands(local,row,lf[row['family_id']],x['link']['controlled_X']):
   ctrl=z['controls'];pat=z['pattern'];assert len(ctrl)==len(set(ctrl))==len(pat) and lay['branch'] in ctrl and pat[ctrl.index(lay['branch'])]==1
   assert set(lay['address'])<=set(ctrl) and z['target'] not in ro|forbid and not set(ctrl+[z['target']])&forbid
   assert set(ctrl)&sam=={lay['SAM'][i] for i in row['SAM_indices']}
   assert z['target'] in outputs
   if z['kind']=='fock':assert {z['cx_control'],z['cx_target']}<=set(lay['modes']) and z['inverse_depth'] in (0,1,2)
   ln+=1
assert cf==294144 and ln==1781504
out={'status':'PASS_A21_ALL_SELECT_READ_ONLY_AND_NAMESPACE_BINDINGS','coframe_units':cf,'link_commands':ln,'all_branch_patterns_equal_one':True,'SAM_and_branch_readonly_all_stages':True,'address_readonly_only_in_SELECT':True,'aux_rebit_comparator_oldRIGHT_and_Choi_input_distinct':True,'no_full_word_expansion':True,'source_sha256':sha256((D/'choi_loader.py').read_bytes()).hexdigest(),'GR_closed':False}
(P/'A21_NAMESPACE_CONTROL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
