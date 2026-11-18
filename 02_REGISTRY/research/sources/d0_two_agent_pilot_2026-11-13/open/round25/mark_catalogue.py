#!/usr/bin/env python3
"""Lazy named source operand catalogue. These are not physical stage ordinals."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
DATA=json.loads((P/'SOURCE_LEAF_BINDING.json').read_text())
BANKS=('y+','y-','f','0','x+','x-','q')

def lookup(bank,site_index,leaf_index):
 assert bank in BANKS and 0<=site_index<256 and 0<=leaf_index<282
 row=DATA['site_bindings'][site_index];template=DATA['leaf_templates'][leaf_index]
 return {'bank':bank,'external_SITE_index':site_index,'external_SITE_coordinate':row['site'],
         'PF_probability':row['PF_probability'],'source_leaf_index':leaf_index,
         'leaf':template,'resolved_address':row['leaf_addresses_in_template_order'][leaf_index],
         'physical_stage_ordinal':None}

def entries():
 for bank in BANKS:
  for site in range(256):
   for leaf in range(282):yield lookup(bank,site,leaf)

if __name__=='__main__':
 import sys
 if len(sys.argv)==1:
  n=sum(1 for _ in entries());assert n==505344;print(json.dumps({'status':'PASS','number_of_target_leaf_bindings':n,'physical_stage_ordinals':None}))
 else:
  print(json.dumps(lookup(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))))
