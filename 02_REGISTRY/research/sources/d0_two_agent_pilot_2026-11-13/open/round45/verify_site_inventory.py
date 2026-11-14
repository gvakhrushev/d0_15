#!/usr/bin/env python3
"""Recount every emitted finite DAG block; no huge G repeat is expanded."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import zip_longest
import json
import site_native as n
P=Path(__file__).resolve().parent;lib=n.library();plan=json.loads((P/'SITE_NATIVE_PLAN.json').read_text());lay=n.layout();port=lay['port']
def count(t):
 op=t['op']
 if op=='seq':
  z=Counter()
  for x in t['children']:z.update(count(x))
  return z
 if op=='repeat':return Counter({k:v*int(t['count']) for k,v in count(t['child']).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def costs(blocks):
 v=Counter();number=0
 for tree in blocks:v.update(count(tree));number+=1
 return v,number
u,ub=costs(n.tree_blocks(lib,lay));ui,uib=costs(n.tree_blocks(lib,lay,1));r,rb=costs(n.gray_phase_blocks(n.phase_command(lib,lay),lay));ri,rib=costs(n.gray_phase_blocks(n.phase_command(lib,lay),lay,1))
assert rb==rib==512 and r['CX']==256 and r['SourceI']==0 and +ui==+n.inv(u) and +ri==+n.inv(r)
for k,v in [('U_forward',u),('U_literal_inverse',ui),('R_zero',r)]:assert all(int(plan['native_inventories'][k][a])==v[a] for a in ('G_port','G_other','CX','SourceI'))
# All finite outer blocks are materialized as compact repeat/seq DAGs; their
# astronomical primitive repeats are never expanded or executed.
forward=list(n.site_blocks(lib,lay));back=n.site_blocks(lib,lay,1);fc=Counter();bc=Counter();number=0
for a,b in zip_longest(reversed(forward),back):
 assert a is not None and b is not None and b==n.nb.inverse_literal(a,port,tuple(lay['spin']));fc.update(count(a));bc.update(count(b));number+=1
assert +bc==+n.inv(fc)
for k,v in [('SITE_forward',fc),('SITE_literal_inverse',bc)]:assert all(int(plan['native_inventories'][k][a])==v[a] for a in ('G_port','G_other','CX','SourceI'))
out={'status':'PASS_SITE_ALL_COMPACT_DAG_BLOCKS_AND_LITERAL_PRICE','U_DAG_blocks':ub,'U_inverse_DAG_blocks':uib,'gray_R_DAG_blocks':rb,'full_SITE_DAG_blocks':number,'native_primitive_repeats_expanded':False,'every_literal_inverse_DAG_block_matches':True,'all_actual_forward_and_inverse_inventories_match':True,'plan_sha256':sha256((P/'SITE_NATIVE_PLAN.json').read_bytes()).hexdigest(),'GR_closed':False}
(P/'SITE_INVENTORY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
