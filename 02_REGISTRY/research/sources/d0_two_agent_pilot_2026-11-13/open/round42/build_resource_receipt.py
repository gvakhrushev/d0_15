#!/usr/bin/env python3
"""Exact native resource receipt for all seven streamed bank schedules."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json
import proper_link_native as n
P=Path(__file__).resolve().parent;lib=n.library();families={f['family']:f for f in lib['families']};gl=n.prefix_compatible_global_layout();cache={};out={}
for bank,entries in lib['catalogue'].items():
 forward=Counter();inverse=Counter()
 for entry in entries:
  key=(entry['family_id'],len(entry['SAM_indices']))
  if key not in cache:
   lay=n.bind_global(gl,entry);cs,ps=n.sector_controls(lay,entry);assert 1 in ps
   f=n.sector_cost(lay,entry,families[key[0]],lib['controlled_X']);r=n.sector_cost(lay,entry,families[key[0]],lib['controlled_X'],reverse=True)
   assert +r==+n.invert_cost(f);cache[key]=(f,r)
  f,r=cache[key];forward.update(f);inverse.update(r)
 assert +inverse==+n.invert_cost(forward)
 out[bank]={'sectors':len(entries),'forward':{k:str(forward[k]) for k in ('G_port','G_other','CX','SourceI')},'literal_inverse':{k:str(inverse[k]) for k in ('G_port','G_other','CX','SourceI')}}
receipt={'status':'EXACT_PROPER_LINK_BANK_NATIVE_INVENTORIES','native_emitter_sha256':sha256(Path(n.__file__).read_bytes()).hexdigest(),'angle_library_sha256':sha256((P/'PROPER_LINK_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'pinned_A14_native_boolean_sha256':sha256((n.D/'round14/native_boolean.py').read_bytes()).hexdigest(),'global_layout':gl,'banks':out,'sector_inventory_unique_family_and_control_width':len(cache),'phase_rebit_and_comparator_untouched':True,'inverse_of_inverse_raw_expanded_in_inventory':True,'giant_native_word_expanded':False,'full_Julia_SELECT_complete':False,'GR_closed':False}
(P/'PROPER_LINK_NATIVE_RESOURCES.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'sector_classes':len(cache),'bank_count':len(out)}))
