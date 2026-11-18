#!/usr/bin/env python3
"""Independent high-precision diagnostic vs original B25 precision names.

Dyadic containment is checked against mpmath values; mpmath itself is NOT
an outward interval certificate. The interval proof is in target source.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import mpmath as mp
import proper_link_targets as a
SRC=a.loc.B/'round25';sys.path.insert(0,str(SRC));import precision_name as orig
specs,banks=a.catalogue();lookup={}
for bank,rows in banks.items():
 for r in rows:
  lookup.setdefault(r['family_id'],(bank,r))
coords=a.loc.COORD;catalog=a.loc.catalogue();rowmap={bank:{r['a']:r for r in rows} for bank,rows in catalog.items()}
iv=a.Interval(192);cache={};maxdiff=mp.mpf(0)
with mp.workprec(600):
 for n,(name,spec) in enumerate(specs.items()):
  bank,r=lookup[name];row=rowmap[bank][r['address']];label=np.zeros(2688,dtype=np.int8)
  for i,b in zip(r['SAM_indices'],r['SAM_pattern']):label[i]=b
  expected=orig.at_site(bank,row['site'],label)[1][row['direction']];got=iv.source(spec,cache)
  for i in range(4):
   for j in range(4):
    lo,hi=got[i][j];x=expected[i,j]
    assert mp.mpf(lo)/iv.S<=x<=mp.mpf(hi)/iv.S,(name,i,j)
  if (n+1)%50==0:print('source names cross-checked',n+1,flush=True)
out={'status':'PASS_ALL_FORMULA_NAMES_VS_B25_MP_DIAGNOSTIC','families':len(specs),'sector_entries':sum(map(len,banks.values())),'precision_bits':192,'reference_precision_bits':600,'mp_values_not_a_formal_interval_proof':True,'source_sha256':hashlib.sha256(Path(a.__file__).read_bytes()).hexdigest(),'GR_closed':False}
Path(__file__).with_name('SOURCE_NAME_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
