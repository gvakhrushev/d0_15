#!/usr/bin/env python3
"""Bind every source-DAG leaf to the real finite periodic Choi/CAR catalogue."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

parser=argparse.ArgumentParser();parser.add_argument('b21',type=Path);parser.add_argument('b24',type=Path)
args=parser.parse_args();here=Path(__file__).resolve().parent
readrows=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
pf=readrows(args.b21/'ORIGINAL_PF_N20_L4.jsonl')
addresses=readrows(args.b24/'TORUS_CHOI_ADDRESSES.jsonl')
deps=readrows(args.b24/'SITE_DEPENDENCIES.jsonl')
dag=json.loads((here/'SOURCE_TENSOR_DAG.json').read_text())
assert len(addresses)==2049 and addresses[0]['kind']=='identity_anchor'
assert [a['a'] for a in addresses]==list(range(2049))
lookup={(a['kind'],tuple(a['site']),a['direction']):a['a'] for a in addresses[1:]}
site_ids={tuple(r['site']):i for i,r in enumerate(pf)}
dep_by_site={tuple(r['site']):r for r in deps}
templates=[]
for index,n in enumerate(dag['nodes']):
 if n['op']!='var':continue
 p=n['name'].split('/')
 if p[0]=='u':
  r,i=map(int,p[1:]);t={'kind':'Choi','location':'base','catalogue_kind':'inverse_coframe_column',
                      'direction':r,'input':0,'output':1<<i,'anchor_moment_multiplier':1}
 elif p[0]=='M':
  loc,r,i,j=p[1:];r,i,j=map(int,(r,i,j))
  t={'kind':'Choi','location':loc,'catalogue_kind':'proper_link','direction':r,
     'input':1<<j,'output':1<<i,'anchor_moment_multiplier':2}
 else:
  loc,a=p[1:];t={'kind':'CAR','location':loc,'cross_masks':[1,int(a)],'RIGHT_action':'identity'}
 t.update({'node':index,'name':n['name']});templates.append(t)
assert len(templates)==282
bindings=[];resolved=0
for row in pf:
 x=tuple(row['site']);index=site_ids[x]
 locations={'base':x}
 for r in range(4):locations[f'plus{r}']=tuple((v+int(i==r))%4 for i,v in enumerate(x))
 # Actual dense vectors of addresses, one per scalar leaf, avoid an exponential state matrix.
 vector=[]
 for t in templates:
  loc=locations[t['location']]
  if t['kind']=='Choi':
   address=lookup[t['catalogue_kind'],loc,t['direction']]
   assert 1<=address<2049 and 0<=t['input']<16 and 0<=t['output']<16
   vector.append(address)
  else:
   vector.append(site_ids[loc])
  resolved+=1
 dep=dep_by_site[x]
 assert [lookup['inverse_coframe_column',x,r] for r in range(4)]==dep['coframe_addresses']
 assert [list(locations[f'plus{r}']) for r in range(4)]==dep['matter_forward_torus']
 for face in dag['faces']:
  r,s=face['roles']
  linked=[lookup['proper_link',locations[loc],direction] for loc,direction in face['links']]
  owned=next(f for f in dep['faces'] if (f['r'],f['s'])==(r,s))
  assert linked==owned['torus_addresses']
 rho=F(row['rho_numerator'],row['rho_denominator'])
 assert rho>=F(3712,5473)
 bindings.append({'SITE_index':index,'site':x,'PF_probability':str(F(row['N'],10946)),
                  'inverse_PF_once':str(1/rho),'leaf_addresses_in_template_order':vector})
assert resolved==256*282 and sum(F(r['PF_probability']) for r in bindings)==1
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result={'schema':'d0-periodic-all-site-source-binding-v1','status':'ALL_SOURCE_LEAVES_BOUND_NOT_NATIVE_WORD',
        'A_active':2049,'julia_d':32,'anchor_square':'1/65568',
        'choi_active_dimension':2049*1024,'choi_padded_dimension':2**22,
        'CAR_internal_sites':256,'CAR_full_grades':16,'CAR_RIGHT_dimension':128,
        'unknown_oldRIGHT':'separate identity spectator, not one of the fresh CAR references',
        'SITE':'one fresh shared PF control for all seven conditional calls; not the internal CAR site',
        'dag_roots':dag['roots'],'leaf_templates':templates,'site_bindings':bindings,
        'Choi_anchor_basis':[0,0,0],
        'meaning':'H_kind=direct_sum_SITE (1/rho_x)*DAG_kind(bound leaves at x); exact block operator, norm<=2^1525',
        'seven_calls':'same fixed bound operator reads separately regenerated Z_j(Y_b) banks; no independent SITE averaging',
        'copy_semantics':dag['tensor_semantics'],
        'source_dag_sha256':sha(here/'SOURCE_TENSOR_DAG.json'),
        'B24_catalogue_sha256':sha(args.b24/'TORUS_CHOI_ADDRESSES.jsonl'),
        'B24_dependencies_sha256':sha(args.b24/'SITE_DEPENDENCIES.jsonl'),
        'B21_PF_sha256':sha(args.b21/'ORIGINAL_PF_N20_L4.jsonl'),
        'free_chart':'64 transverse-interior sites, additive raw u/link/matter, all boundary and PF fixed',
        'full_native_word_or_READY':False,'GR_closed':False}
(here/'PERIODIC_SOURCE_BINDING.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
print(json.dumps({'status':result['status'],'source_sites':len(bindings),'leaf_templates':len(templates),
                  'resolved_source_leaves':resolved,'all_face_bindings_checked':256*6,
                  'A_active':2049,'anchor_square':result['anchor_square']}))
