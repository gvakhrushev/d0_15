#!/usr/bin/env python3
"""Honest componentwise upper inventories; not actual paid counts."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import proper_link_two_bit_targets as target
import proper_link_two_bit_native as native
old=native.old;q=native.Q

def select(K):
 # Real commands all include the fixed branch=1, hence exactly half negatives.
 return old.select_cost(list(range(K)),[1]+[0]*(K-1),q,common_controls=29)
def maxdepth(c,top):
 variants=[c]
 for _ in range(top):variants.append(old.invert_cost(variants[-1]))
 return Counter({k:max(v[k] for v in variants) for k in ('G_port','G_other','CX','SourceI')})
def bound(nsam,outer_inverse):
 base=12+nsam+1;depth=2+int(outer_inverse);c=Counter()
 # 12 single-particle rotations, four occupation pairs each, two flags.
 f=maxdepth(select(base+4),depth);f['CX']+=2
 c.update({k:96*v for k,v in f.items()})
 # one X: conditional pi/2 and conditional phase
 c.update(maxdepth(select(base),int(outer_inverse)))
 c.update(maxdepth(select(base+1),int(outer_inverse)))
 # Four diagonal Julia rotations.
 d=maxdepth(select(base+2),int(outer_inverse))
 c.update({k:4*v for k,v in d.items()})
 return c
_,cat=target.catalogue();outputs={}
for bank,section in cat.items():
 nf=len(section['fixed']);nv=len(section['variable'])*4096
 f0=bound(0,False);f12=bound(12,False);r0=bound(0,True);r12=bound(12,True)
 f=Counter({k:nf*f0[k]+nv*f12[k] for k in f0});r=Counter({k:nf*r0[k]+nv*r12[k] for k in r0})
 outputs[bank]={'fixed_sectors':nf,'variable_sectors':nv,'forward_componentwise_upper_hex':{k:hex(v) for k,v in f.items()},'literal_inverse_componentwise_upper_hex':{k:hex(v) for k,v in r.items()},'max_SourceI_bits':max(f['SourceI'].bit_length(),r['SourceI'].bit_length())}
out={'status':'SAFE_COMPONENTWISE_UPPER_NOT_ACTUAL_PRICE','multiplier_controls':29,'upper_uses_q_for_every_exponent':True,'uses_96_fock_pairs_2_X_4_diagonal_selects_per_sector_even_for_identity':True,'sourceI_replacement_not_included':True,'actual_exact_inventory_materialized':False,'bank_bounds':outputs,'physical_C_closed':False,'GR_closed':False}
(P/'PROPER_LINK_RESOURCE_UPPER.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],{b:r['max_SourceI_bits'] for b,r in outputs.items()})
