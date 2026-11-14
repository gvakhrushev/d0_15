#!/usr/bin/env python3
"""Exact A22 wrapper chronology with independent primitive-by-primitive inverse."""
from pathlib import Path
from hashlib import sha256
from itertools import zip_longest
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round22');sys.path.insert(0,str(D));import full_choi_bank as b
nb=b.nb;toy={'SAM':[],'address':[],'choi_input':[],'choi_output':[0],'branch':1,'phase_rebit':2,'comparator_scratch':[],'port':4,'spin':[5,6],'aux_arbitrary':3,'oldRIGHT_witness':7,'qubits':8};p=4;spin=(5,6)
U=nb.seq(nb.gate('G',0),nb.gate('CX',1,0),nb.gate('SourceI',p,*spin),nb.gate('G',3))
def words(blocks):
 for t in blocks:yield from nb.expand(t,1000000)
def inverse(word):
 out=[];src={'op':'SourceI','wires':[p,*spin]};cx=lambda i,j:{'op':'CX','wires':[i,j]}
 for q in reversed(word):
  if q['op']=='CX':out.append(q)
  elif q['op']=='SourceI':out.extend([q,q,q])
  else:
   x=q['wires'][0];swap=[] if x==p else [cx(x,p),cx(p,x),cx(x,p)];out.extend([*swap,src,src,{'op':'G','wires':[p]},src,src,*swap])
 return out
def eq(x,y):
 count=0
 for a,z in zip_longest(x,y):assert a==z,(count,a,z);count+=1
 return count
saved=(b.validate,b.reflection_k,b.c.half_blocks)
def toyU(bank,lay=None,levels=8,inverse_depth=0):
 t=U
 for _ in range(inverse_depth):t=nb.inverse_literal(t,p,spin)
 yield t
b.validate=lambda lay,extra_external=():None;b.reflection_k=lambda:1;b.c.half_blocks=toyU
reports=[]
try:
 for initialize in (False,True):
  initial=list(words(b.bank_blocks('f',toy,initialize_private=initialize)));target=initial
  for depth in range(4):
   if depth:target=inverse(target)
   got=words(b.bank_blocks('f',toy,depth,initialize_private=initialize));count=eq(got,target);reports.append({'initialize_private':initialize,'literal_depth':depth,'exact_native_primitive_leaves':count})
finally:b.validate,b.reflection_k,b.c.half_blocks=saved
out={'status':'PASS_INDEPENDENT_A22_LITERAL_RAW_CHOI_WRAPPER','source_sha256':sha256((D/'full_choi_bank.py').read_bytes()).hexdigest(),'cases':reports,'independent_primitive_inverse_not_parity_simplified':True,'real_SourceI_two_Spin_bits':True,'actual_K46_giant_word_executed':False,'GR_closed':False}
(P/'FULL_CHOI_LITERAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(reports),'max_leaves':max(q['exact_native_primitive_leaves'] for q in reports)}))
