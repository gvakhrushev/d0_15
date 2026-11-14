#!/usr/bin/env python3
"""Contain high-precision independent true target bounds in saved intervals."""
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent
# Reuse the independently implemented B38 dyadic target formulas, not A18's
# Dyadic class or any builder function, at precision above the saved file.
source=(P/'verify_all_material_intervals.py').read_text();marker="assert lib['precision_bits']>bits;";assert marker in source
prefix=source.split(marker,1)[0].replace('bits=8448;S=1<<bits','bits=17408;S=1<<bits')
ns={'__name__':'b38_saved_target_engine','__file__':str(P/'verify_all_material_intervals.py')};exec(compile(prefix,str(P/'verify_all_material_intervals.py'),'exec'),ns)
lib=ns['lib'];S=ns['S'];bits=ns['bits'];factor=1<<(bits-lib['precision_bits']);I=ns['I'];own_target=ns['own_target'];checked=0;zeros=0
for vid,entry in lib['vectors'].items():
 v,rots=own_target(entry['spec'])
 for grade,own in v.items():
  lo,hi=[int(x,16) for x in entry['half_vector_bounds_hex'][str(grade)]]
  assert lo*factor<=own[0] and own[1]<=hi*factor,(vid,grade)
 for other,(cc,ss),rotation in zip((14,0,15),rots,entry['rotations']):
  assert rotation['other']==other;aid=rotation['angle_id']
  if aid is None:assert ss==(0,0) and cc[0]<=S<=cc[1];zeros+=1;continue
  if other in (14,0):ss=I.neg(ss)
  e=lib['angles'][aid]
  for own,key in ((cc,'target_cos_hex'),(ss,'target_sin_hex')):
   lo,hi=[int(x,16) for x in e[key]]
   assert lo*factor<=own[0] and own[1]<=hi*factor,(vid,other,key)
  # Verify the reported interval separation inequality independently.
  tc=[int(x,16) for x in e['target_cos_hex']];ts=[int(x,16) for x in e['target_sin_hex']];nc=[int(x,16) for x in e['native_cos_hex']];nsine=[int(x,16) for x in e['native_sin_hex']]
  error=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(nsine[0]-ts[1]),abs(nsine[1]-ts[0]))
  assert error==int(e['operator_error_L1_numerator_hex'],16) and error<=(1<<(lib['precision_bits']-4096));checked+=1
assert len(lib['vectors'])==22 and checked+zeros==66
out={'status':'PASS_ALL_SAVED_TARGET_INTERVALS_CONTAIN_INDEPENDENT_BOUNDS','library_sha256':sha256(ns['p'].read_bytes()).hexdigest(),'independent_precision_bits':bits,'saved_precision_bits':lib['precision_bits'],'vector_families':22,'nonzero_rotations_checked':checked,'exact_zero_rotations':zeros,'all_saved_half_vector_and_angle_bounds_contain_tighter_independent_bounds':True,'all_saved_reported_separation_integers_recomputed':True,'source_builder_reexecuted':False,'float_used_in_proof':False,'GR_closed':False}
(P/'SAVED_TARGET_INTERVALS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
