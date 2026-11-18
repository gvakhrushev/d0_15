#!/usr/bin/env python3
"""Independent census of A48 two-bit local emitters, literal costs and bindings."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json,sys,itertools
P=Path(__file__).resolve().parent;A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round48');sys.path.insert(0,str(A))
import two_bit_source_targets as t
import two_bit_local_native as n
plan=json.loads((A/'TWO_BIT_LOCAL_NATIVE_PLAN.json').read_text());assert plan['status']=='CONCRETE_TWO_BIT_LOCAL_NATIVE_GRAMMARS'
co=n.library('COFRAME');ma=n.library('MATERIAL');layout=n.coframe_layout();mlayout=n.material_layout()
def pair(bound):
 K=bound['K'];N=1<<K;neg=N//2 if any(bound['pattern']) else 0;power=bound['k']
 return Counter(G_port=neg*power,G_other=(N-neg)*power,CX=K*N+6*neg+2*len(bound['permutation']),SourceI=4*neg)
def inverse(c):return Counter(G_port=c['G_port']+c['G_other'],G_other=0,CX=c['CX']+6*c['G_other'],SourceI=3*c['SourceI']+4*(c['G_port']+c['G_other']))
def nested(c,depth):
 for _ in range(depth):c=inverse(c)
 return c
def verifycounts(c,row):
 return all(c[k]==int(row.get(k,'0')) for k in ('G_port','G_other','CX','SourceI'))
co_results={};max_co=0
for bank in co['catalogue_templates']:
 groups={};sectors=0
 for row in t.coframe_sectors(co['catalogue_templates'],bank):
  ids=row['SAM_indices'];pat=row['SAM_pattern'];assert len(ids)==len(pat) and len(ids) in (0,8)
  assert all(ids[i+1]==2688+ids[i] for i in range(0,len(ids),2))
  assert len(set(ids))==len(ids) and all(x in (0,1) for x in pat)
  key=(row['family_id'],len(ids));g=groups.setdefault(key,[row,0]);g[1]+=1;sectors+=1
 total=Counter();macros=0;maxk=0
 for row,mult in groups.values():
  units=n.coframe_units(row,co,layout);reverse=n.coframe_units(row,co,layout,depth=1)
  assert reverse==[(b,d+1) for b,d in reversed(units)]
  macros+=mult*(len(units)-1)
  for bound,depth in units:
   assert len(bound['controls'])==bound['K'] and 1 in bound['pattern'] and bound['target'] not in bound['controls']
   assert len(set(bound['controls']+[bound['target'],layout['port'],*layout['spin']]))==bound['K']+4
   maxk=max(maxk,bound['K']);total.update({k:mult*v for k,v in nested(pair(bound),depth).items()})
 r=plan['coframe'][bank];assert sectors==r['sectors'] and macros==r['ideal_macro_occurrences'] and maxk==r['maximum_predicate_width']
 assert verifycounts(total,r['native_forward']) and verifycounts(inverse(total),r['native_literal_inverse'])
 max_co=max(max_co,maxk);co_results[bank]={'sectors':sectors,'independent_family_width_classes':len(groups),'maxK':maxk}
assert max_co==24
# Material preparations count every row; unlike coframe, all-zero patterns
# exist and must not be replaced by the half-negative branch shortcut.
mat_results={};max_mat=0;prep_counts={}
for bank,rows in ma['catalogue'].items():
 total=Counter();rots=0
 for row in rows:
  ids=row['SAM_indices'];assert len(ids) in (0,4) and all(ids[i+1]==2688+ids[i] for i in range(0,len(ids),2))
  for rot in ma['vectors'][row['vector_id']]['rotations']:
   if rot['angle_id'] is None:continue
   bound=n.bind_material(row,rot,mlayout,ma['angles']);assert bound['K'] in (11,15)
   total.update(pair(bound));rots+=1;max_mat=max(max_mat,bound['K'])
 r=plan['material']['preparations'][bank];assert len(rows)==r['sectors'] and rots==r['rotations']
 assert verifycounts(total,r['native_forward']) and verifycounts(inverse(total),r['native_literal_inverse'])
 prep_counts[bank]=total;mat_results[bank]={'sectors':len(rows),'rotations':rots}
assert max_mat==15
# Count fixed native DAG recursively without consulting A48's inventory function.
def treecounts(node,port):
 op=node['op']
 if op=='seq':
  c=Counter()
  for x in node['children']:c.update(treecounts(x,port))
  return c
 if op=='repeat':return Counter({k:int(node['count'])*v for k,v in treecounts(node['child'],port).items()})
 return Counter({('G_port' if node['wires'][0]==port else 'G_other') if op=='G' else op:1})
U,Ui,R=n.car.fixed_components(mlayout);assert Ui==n.nb.inverse_literal(U,mlayout['port'],tuple(mlayout['spin']))
cu,ci,cr=[treecounts(z,mlayout['port']) for z in (U,Ui,R)];assert +ci==+inverse(cu)
for bank,row in plan['material']['frames'].items():
 c=cu+ci+Counter({k:2*v for k,v in cr.items()})
 if bank in prep_counts:c+=prep_counts[bank]+inverse(prep_counts[bank])
 else:c+=cu+ci
 assert verifycounts(c,row['native_forward']) and verifycounts(inverse(c),row['native_literal_inverse'])
# Expand a tiny stand-in Walsh pair only, compare actual syntax at depths 0..3.
bound={'K':2,'controls':[0,1],'pattern':[0,1],'target':2,'k':2,'permutation':[n.nb.gate('CX',2,3)]};toy={'port':4,'spin':[5,6]}
for depth in range(4):
 c=Counter()
 for tree in n.cf.unit_blocks(bound,depth,toy):c.update(treecounts(tree,4))
 assert +c==+nested(pair(bound),depth)
out={'status':'PASS_A48_LOCAL_ALL_BINDINGS_AND_COMPRESSED_COUNTS','coframe':co_results,'material':mat_results,'material_frames_all_seven_checked':True,'maximum_coframe_controls':max_co,'maximum_material_controls':max_mat,'toy_literal_depths_checked':[0,1,2,3],'giant_native_words_expanded':False,'COFRAME_target_error_le':plan['coframe_operator_error_le'],'MATERIAL_half_vector_error_le':plan['material_half_vector_operator_error_le'],'physical_C_closed':False,'GR_closed':False}
(P/'LOCAL_INVENTORY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
