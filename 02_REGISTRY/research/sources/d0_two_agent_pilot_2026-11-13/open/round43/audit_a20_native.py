#!/usr/bin/env python3
"""Independent all-sector control, chronology, inverse-depth and cost audit."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import product
import sys,json,subprocess
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round20');sys.path.insert(0,str(D))
import coframe_native as n
lib=json.loads((D/'COFRAME_ANGLE_LIBRARY.json').read_bytes());plan=json.loads((D/'COFRAME_NATIVE_PLAN.json').read_bytes());lay=n.layout();order=(0,2,3,1)
assert plan['library_sha256']==sha256((D/'COFRAME_ANGLE_LIBRARY.json').read_bytes()).hexdigest() and plan['source_sha256']==sha256((D/'coframe_native.py').read_bytes()).hexdigest()
for path,digest in plan['input_sha256'].items():assert sha256(Path(path).read_bytes()).hexdigest()==digest

def pairs(j):
 rest=[q for q in range(4) if q not in (0,j)];between=order[1:order.index(j)]
 for bits in product((0,1),repeat=2):
  m=sum(b<<q for b,q in zip(bits,rest));sign=(-1)**sum((m>>q)&1 for q in between);yield m|1,m|(1<<j),sign

def bind(row,grade,a,b,angle):
 ctrl=lay['address']+[lay['SAM'][i] for i in row['SAM_indices']]+[lay['branch']];pat=[(row['address']>>j)&1 for j in range(12)]+row['SAM_pattern']+[1];diff=a^b;pivot=(diff&-diff).bit_length()-1;flips=[j for j in range(len(grade)) if j!=pivot and diff>>j&1];trans=a
 for j in flips:trans^=((trans>>pivot)&1)<<j
 assert trans>>pivot&1
 for j in range(len(grade)):
  if j!=pivot:ctrl.append(grade[j]);pat.append((trans>>j)&1)
 K=len(ctrl);assert K<=20 and angle['native_exponent_multiplier']==1<<20
 return {'K':K,'controls':ctrl,'pattern':pat,'target':grade[pivot],'k':int(angle['k'])*(1<<(20-K)), 'permutation':[{'op':'CX','wires':[grade[pivot],grade[j]]} for j in flips]}
def expected_units(row):
 fam=lib['families'][row['family_id']];binds={tuple(z['factor']):z['angle_id'] for z in fam['angle_bindings']};F=[]
 for i,r in enumerate(fam['mode_rotations']):
  if r['exact_identity']:continue
  for a,b,sign in pairs(r['mode']):F.append(bind(row,lay['choi_output'][:4],a,b,lib['angles'][binds[('mode',i,sign)]]))
 outer=lay['address']+[lay['SAM'][i] for i in row['SAM_indices']]+[lay['branch']];pat=[(row['address']>>j)&1 for j in range(12)]+row['SAM_pattern']+[1];flag=lay['choi_output'][4];aux=lay['aux_arbitrary'];x=lib['controlled_X_power'];k=int(lib['angles'][x['rotation_angle_id']]['k'])
 phase={'K':len(outer)+1,'controls':outer+[flag],'pattern':pat+[1],'target':aux,'k':k*(1<<(21-len(outer)-1)),'permutation':[]}
 rot={'K':len(outer),'controls':outer,'pattern':pat,'target':flag,'k':k*(1<<(20-len(outer))),'permutation':[]}
 base=bind(row,[lay['choi_output'][0],flag],1,2,lib['angles'][binds[('base',0,0)]])
 return [(z,1) for z in reversed(F)]+[(phase,0),(rot,0),(base,0)]+[(z,0) for z in F]
def invert(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def count(b,depth):
 K=b['K'];terms=1<<K;neg=terms//2 if any(b['pattern']) else 0;k=b['k'];c=Counter({'G_port':neg*k,'G_other':(terms-neg)*k,'CX':K*terms+6*neg+2*len(b['permutation']),'SourceI':4*neg})
 for _ in range(depth):c=invert(c)
 return c
readonly=set(lay['SAM']+lay['address']+[lay['branch']]);protected=set(lay['choi_input']+[lay['oldRIGHT_witness']]);banks={};units=0;sectors=0;maxK=0;cache={}
for bank,rows in lib['catalogue'].items():
 total=Counter();macro=0;localmax=0
 for row in rows:
  actual=n.sector_units(row,lib,lay);wanted=expected_units(row);assert actual==wanted and n.sector_units(row,lib,lay,reverse=True)==[(z,d+1) for z,d in reversed(actual)]
  assert len(actual)-1<=26;macro+=len(actual)-1;sectors+=1
  for b,depth in actual:
   assert b['target'] not in readonly|protected and lay['branch'] in b['controls'] and b['pattern'][b['controls'].index(lay['branch'])]==1
   assert not set(b['controls'])&protected and all(g['wires'][-1] not in readonly|protected for g in b['permutation']);assert depth in (0,1);units+=1;maxK=max(maxK,b['K']);localmax=max(localmax,b['K'])
   total.update(count(b,depth))
 b=plan['banks'][bank];assert b['sectors']==len(rows) and b['ideal_macro_occurrences']==macro and b['maximum_predicate_width']==localmax
 for key,val in b['native_forward'].items():assert total[key]==int(val)
 inverse=invert(total)
 for key,val in b['native_literal_inverse'].items():assert inverse[key]==int(val)
 banks[bank]=len(rows)
assert sectors==14848 and units==294144 and maxK==20
# Independent literal expansion for depths 0,1,2,3 including real routed G^-1.
def inverse_word(word,port,spin):
 out=[];src={'op':'SourceI','wires':[port,*spin]};CX=lambda a,b:{'op':'CX','wires':[a,b]}
 for g in reversed(word):
  if g['op']=='CX':out.append(g)
  elif g['op']=='SourceI':out.extend([g,g,g])
  else:
   q=g['wires'][0];sw=[] if q==port else [CX(q,port),CX(port,q),CX(q,port)];out.extend([*sw,src,src,{'op':'G','wires':[port]},src,src,*sw])
 return out
small={'K':3,'controls':[1,2,3],'pattern':[1,0,1],'target':0,'k':1,'permutation':[{'op':'CX','wires':[0,1]}]};sl={'port':4,'spin':[5,6]};prev=None;depths=[]
for depth in range(4):
 blocks=list(n.unit_blocks(small,depth,sl));word=[g for x in blocks for g in n.nb.expand(x,1000000)]
 if prev is not None:assert word==inverse_word(prev,4,[5,6])
 c=Counter()
 for g in word:c['G_port' if g['op']=='G' and g['wires'][0]==4 else 'G_other' if g['op']=='G' else g['op']]+=1
 assert +c==+count(small,depth);depths.append(len(word));prev=word
out={'status':'PASS_INDEPENDENT_A20_BINDINGS_AND_RESOURCES','pinned_commit':'afbaef2f950da70c0fe16dbdb8091c851929bd7a','library_sha256':sha256((D/'COFRAME_ANGLE_LIBRARY.json').read_bytes()).hexdigest(),'plan_sha256':sha256((D/'COFRAME_NATIVE_PLAN.json').read_bytes()).hexdigest(),'banks':banks,'sector_bindings':sectors,'units':units,'max_controls':maxK,'literal_inverse_depth_0_to_3_expanded_leaves':depths,'full_native_word_expanded':False,'GR_closed':False}
(P/'A20_NATIVE_BINDING_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
