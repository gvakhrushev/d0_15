#!/usr/bin/env python3
"""Exact primitive audit of A21 stage provider and B39 bounded composition."""
from pathlib import Path
from hashlib import sha256
from itertools import zip_longest
import sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round21');sys.path.insert(0,str(D));import choi_loader as c
nb=c.nb;toy={'SAM':[],'address':[],'choi_input':[],'choi_output':[1],'branch':0,'phase_rebit':2,'comparator_scratch':[3],'port':4,'spin':[5,6],'aux_arbitrary':7,'oldRIGHT_witness':8,'qubits':9};al=c.adapter_layout(toy);p=4;spin=(5,6)
# Three specified branch-controlled actual native schedules with distinct k.
# Each stage has multiple blocks and already contains routed negative powers.
stages={}
for name,k in [('prefix',1),('coframe',2),('link',3)]:stages[name]=nb.selective_rotation([0],[1],1,k,p,spin)['children']
original=sum((stages[z] for z in ('prefix','coframe','link')),[]);V=nb.seq(*original)
def literal_inverse(tree):
 op=tree['op']
 if op=='seq':return nb.seq(*(literal_inverse(x) for x in reversed(tree['children'])))
 if op=='repeat':return nb.repeat(int(tree['count']),literal_inverse(tree['child']))
 if op=='CX':return tree
 if op=='SourceI':return nb.repeat(3,tree)
 assert op=='G';q=tree['wires'][0];src=nb.gate('SourceI',p,*spin);core=nb.seq(src,src,nb.repeat(1,nb.gate('G',p)),src,src)
 if q==p:return core
 swap=lambda a,b:nb.seq(nb.gate('CX',a,b),nb.gate('CX',b,a),nb.gate('CX',a,b))
 return nb.seq(swap(q,p),core,swap(q,p))
def stage(name,reverse):
 data=stages[name]
 return iter([literal_inverse(t) for t in reversed(data)] if reverse else data)
def pf(cert,lay=None,controlled=True,reverse=False):return stage('prefix',reverse)
def cf(bank,library,lay=None,controlled=True,reverse=False):return stage('coframe',reverse)
def lk(bank,library,lay=None,reverse=False):return stage('link',reverse)
def leaves(blocks):
 for t in blocks:yield from nb.expand(t,5000000)
def inverse_word(word):
 out=[];src={'op':'SourceI','wires':[p,*spin]};CX=lambda a,b:{'op':'CX','wires':[a,b]}
 for g in reversed(word):
  if g['op']=='CX':out.append(g)
  elif g['op']=='SourceI':out.extend([g,g,g])
  else:
   q=g['wires'][0];sw=[] if q==p else [CX(q,p),CX(p,q),CX(q,p)];out.extend([*sw,src,src,{'op':'G','wires':[p]},src,src,*sw])
 return out
def compare(a,b):
 n=0
 for x,y in zip_longest(a,b):assert x==y,(n,x,y);n+=1
 return n
saved=(c.inputs,c.prefix.prefix_blocks,c.coframe.select_blocks,c.link.bank_blocks)
c.inputs=lambda:{'prefix':{},'coframe':{},'link':{},'phase':{'phase_k':'1','correction_l':'1'},'h_k':1};c.prefix.prefix_blocks=pf;c.coframe.select_blocks=cf;c.link.bank_blocks=lk
try:
 provider=[];word=list(leaves(c.omega_blocks('f',toy,0)));expected=list(leaves(original));assert word==expected
 for depth in range(4):
  if depth:expected=inverse_word(expected)
  count=compare(leaves(c.omega_blocks('f',toy,depth)),expected);provider.append({'literal_depth':depth,'primitive_leaves':count})
 half=[]
 for levels in range(3):
  a=list(leaves(c.half_blocks('f',toy,levels,0)));b=leaves(c.adapter.adapter_blocks(al,V,1,1,1,levels=levels));assert compare(iter(a),b)==len(a)
  expected=a
  for depth in range(4):
   if depth:expected=inverse_word(expected)
   count=compare(leaves(c.half_blocks('f',toy,levels,depth)),expected);half.append({'levels':levels,'literal_depth':depth,'primitive_leaves':count})
finally:c.inputs,c.prefix.prefix_blocks,c.coframe.select_blocks,c.link.bank_blocks=saved
out={'status':'PASS_INDEPENDENT_A21_LITERAL_PROVIDER_AND_HALF_DEPTHS','A21_source_sha256':sha256((D/'choi_loader.py').read_bytes()).hexdigest(),'provider_depths':provider,'half_levels_0_to_2_depths_0_to_3':half,'independent_leafwise_inverse_used':True,'all_three_toy_stages_controlled_and_native':True,'full_giant_word_executed':False,'GR_closed':False}
(P/'A21_LITERAL_DEPTH_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'provider_depths':len(provider),'half_cases':len(half),'last_primitive_leaves':half[-1]['primitive_leaves']}))
