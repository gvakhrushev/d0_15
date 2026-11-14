#!/usr/bin/env python3
"""Independent raw inverse depth audit for A23 actual powers and toy program."""
from pathlib import Path
from itertools import zip_longest
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round23');sys.path.insert(0,str(D));import car_vacuum_prefix as n
lay=n.layout();port=lay['port'];spin=tuple(lay['spin']);nb=n.nb;x=n.inputs();commands=list(n.commands(x['kappa'],lay,x['phase_k']))
def inverse(t):
 op=t['op']
 if op=='seq':return nb.seq(*(inverse(q) for q in reversed(t['children'])))
 if op=='repeat':return nb.repeat(int(t['count']),inverse(t['child']))
 if op=='CX':return t
 if op=='SourceI':return nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=nb.gate('SourceI',port,*spin);core=nb.seq(src,src,nb.repeat(1,nb.gate('G',port)),src,src)
 if q==port:return core
 def swap(a,b):return nb.seq(nb.gate('CX',a,b),nb.gate('CX',b,a),nb.gate('CX',a,b))
 return nb.seq(swap(q,port),core,swap(q,port))
def invert(t,d):
 for _ in range(d):t=inverse(t)
 return t
def term(z,mask):
 q=z['target'];idx=[i for i in range(7) if mask>>i&1];cx=[nb.gate('CX',z['controls'][i],q) for i in idx];sign=(-1)**sum(z['pattern'][i] for i in idx);k=z['k']
 if sign>0:r=nb.repeat(k,nb.gate('G',q))
 else:
  src=nb.gate('SourceI',port,*spin);core=nb.seq(src,src,nb.repeat(k,nb.gate('G',port)),src,src);sw=lambda a,b:nb.seq(nb.gate('CX',a,b),nb.gate('CX',b,a),nb.gate('CX',a,b));r=nb.seq(sw(q,port),core,sw(q,port))
 return nb.seq(*cx,r,*reversed(cx))
actual=0
for coeff in (1,2,3):
 z=next(q for q in commands if q['coefficient']==coeff)
 for d in range(4):
  masks=range(127,-1,-1) if d%2 else range(128);want=[invert(term(z,i),d) for i in masks];got=list(n.rotation_blocks(z,lay,d));assert got==want;actual+=len(got)
# Full 19-wire toy instance, no changes to source files.
fixture=[[0]*4 for _ in range(64)];fixture[0][3]=1;saved=n.inputs;n.inputs=lambda:{'kappa':fixture,'boolean_k':1,'phase_k':1}
def leaves(stream):
 for t in stream:yield from nb.expand(t,2000000)
def inverseword(word):
 out=[];src={'op':'SourceI','wires':[port,*spin]};cx=lambda a,b:{'op':'CX','wires':[a,b]}
 for g in reversed(word):
  if g['op']=='CX':out.append(g)
  elif g['op']=='SourceI':out.extend([g,g,g])
  else:
   q=g['wires'][0];sw=[] if q==port else [cx(q,port),cx(port,q),cx(q,port)];out.extend([*sw,src,src,{'op':'G','wires':[port]},src,src,*sw])
 return out
def eq(a,b):
 i=0
 for x,y in zip_longest(a,b):assert x==y,(i,x,y);i+=1
 return i
reports=[]
try:
 want=list(leaves(n.prefix_blocks(lay,0)))
 for d in range(4):
  if d:want=inverseword(want)
  count=eq(leaves(n.prefix_blocks(lay,d)),want);reports.append({'depth':d,'exact_primitive_leaves':count})
finally:n.inputs=saved
out={'status':'PASS_INDEPENDENT_A23_ACTUAL_AND_TOY_LITERAL_DEPTHS','source_sha256':sha256((D/'car_vacuum_prefix.py').read_bytes()).hexdigest(),'actual_K7_a1_a2_a3_all_128_masks_depth0_to3':actual,'toy19_full_word_primitive_replays':reports,'real_SourceI_both_spin_bits':True,'huge_repeats_executed':False,'GR_closed':False}
(P/'A23_LITERAL_DEPTH_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'actual_DAG_comparisons':actual,'toy_max_leaves':reports[-1]['exact_primitive_leaves']}))
