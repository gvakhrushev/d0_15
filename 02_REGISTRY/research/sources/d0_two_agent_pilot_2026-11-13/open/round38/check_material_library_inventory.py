#!/usr/bin/env python3
"""Independent all-sector A18 library binding and native inventory check."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=D/'round18';lp=P/'MATERIAL_PREPARATION_LIBRARY.json';ip=P/'MATERIAL_PREPARATION_INVENTORY.json';lib=json.loads(lp.read_text());inventory=json.loads(ip.read_text());sha=lambda p:sha256(p.read_bytes()).hexdigest();digest=sha(lp);assert inventory['library_sha256']==digest
assert lib['source_sha256']==sha(P/'certify_material_preparation.py')
for path,value in lib['input_sha256'].items():assert sha(Path(path))==value,path
assert len(lib['vectors'])==22 and len(lib['angles'])==38
specs={}
for x in range(4):
 specs[f'q{x}_fixed']={'id':f'q{x}_fixed','kind':'q','x0':x,'bits':None}
 for b0 in (0,1):
  for b15 in (0,1):
   key=f'q{x}_{b0}{b15}';specs[key]={'id':key,'kind':'q','x0':x,'bits':[b0,b15]}
specs['y_positive']={'id':'y_positive','kind':'y','sign':1};specs['y_negative']={'id':'y_negative','kind':'y','sign':-1}
assert {name:v['spec'] for name,v in lib['vectors'].items()}==specs
# Catalogue coverage from source data alone, no A18 catalogue() or bind_plane.
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open');rows=[json.loads(x) for x in (root/'round21/ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()];coords=[json.loads(x) for x in (root/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()];matter={(tuple(r['site']),r['grade']):i for i,r in enumerate(coords) if r['kind']=='matter'};assert len(matter)==128
expected={'q':[],'y+':[],'y-':[]}
for site,r in enumerate(rows):
 x=tuple(r['site']);free=(x,0) in matter;assert free==((x,15) in matter)
 if free:
  for b0 in (0,1):
   for b15 in (0,1):expected['q'].append({'site':site,'site_coordinates':list(x),'SAM_indices':[matter[x,0],matter[x,15]],'SAM_pattern':[b0,b15],'vector_id':f'q{x[0]}_{b0}{b15}'})
 else:expected['q'].append({'site':site,'site_coordinates':list(x),'SAM_indices':[],'SAM_pattern':[],'vector_id':f'q{x[0]}_fixed'})
 for bank,axis in [('y+',1),('y-',0)]:expected[bank].append({'site':site,'site_coordinates':list(x),'SAM_indices':[],'SAM_pattern':[],'vector_id':'y_positive' if x[axis]%2==0 else 'y_negative'})
assert expected==lib['catalogue']
def eq(x,y):return all(x.get(k,0)==int(y.get(k,0)) for k in ('G_port','G_other','CX','SourceI'))
summary={}
for bank,sectors in expected.items():
 total=Counter();occ=0;zero=0;selected=Counter()
 for row in sectors:
  for rotation in lib['vectors'][row['vector_id']]['rotations']:
   aid=rotation['angle_id']
   if aid is None:zero+=1;continue
   other=rotation['other'];d=1^other;pivot=next(i for i in range(4) if d>>i&1);flips=[i for i in range(4) if i!=pivot and d>>i&1];trans=1
   for i in flips:trans^=((trans>>pivot)&1)<<i
   pattern=[(row['site']>>i)&1 for i in range(8)]+row['SAM_pattern']+[(trans>>i)&1 for i in range(4) if i!=pivot];K=len(pattern);assert K in (11,13)
   k=int(lib['angles'][aid]['k'])<<(13-K);n=1<<K;neg=n//2 if any(pattern) else 0
   total.update({'G_port':neg*k,'G_other':(n-neg)*k,'CX':K*n+6*neg+2*len(flips),'SourceI':4*neg});occ+=1;selected[K]+=1
  
 check=inventory['banks'][bank];assert check['sectors']==len(sectors) and check['nonidentity_planar_rotation_occurrences']==occ and eq(total,check['native_forward'])
 reverse=Counter({'G_port':total['G_port']+total['G_other'],'G_other':0,'CX':total['CX']+6*total['G_other'],'SourceI':3*total['SourceI']+4*(total['G_port']+total['G_other'])})
 assert eq(reverse,check['native_literal_inverse']);summary[bank]={'sectors':len(sectors),'nonidentity_rotation_occurrences':occ,'omitted_structural_identities':zero,'K_counts':dict(selected)}
assert sha(lp)==digest
out={'status':'PASS_INDEPENDENT_A18_ALL_SECTOR_INVENTORY','library_sha256':digest,'inventory_sha256':sha(ip),'vectors':22,'unique_angles':38,'all_source_hashes_verified':True,'all_vector_ids_match_independent_specs':True,'banks':summary,'all_forward_and_literal_inverse_resources_match':True,'counts_include_inactive_sectors':True,'full_native_execution':False,'GR_closed':False}
Path(__file__).with_name('A18_LIBRARY_INVENTORY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
