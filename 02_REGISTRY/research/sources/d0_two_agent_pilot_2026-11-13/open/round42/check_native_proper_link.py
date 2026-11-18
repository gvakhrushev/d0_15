#!/usr/bin/env python3
"""Exact small native columns and actual DAG resources; no huge-word flatten."""
from pathlib import Path
from collections import Counter
from itertools import product
from hashlib import sha256
import json
import proper_link_native as a
Z=(0,0,0,0);O=(1,0,0,0);A=(0,1,0,0);P=(0,0,1,0)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 v=[0]*7
 for i,x in enumerate(a):
  for j,y in enumerate(b):v[i+j]+=x*y
 for n in (6,5,4):v[n-4]+=v[n];v[n-2]-=v[n]
 return tuple(v[:4])
def run(tree,state):
 op=tree['op']
 if op=='seq':
  for x in tree['children']:state=run(x,state)
  return state
 if op=='repeat':
  for _ in range(int(tree['count'])):state=run(tree['child'],state)
  return state
 out={}
 def put(q,v):out[q]=add(out.get(q,Z),v)
 for ix,v in state.items():
  w=tree['wires']
  if op=='G':
   bit=(ix>>w[0])&1;put(ix,mul(v,A));put(ix^(1<<w[0]),mul(v,neg(P) if bit else P))
  elif op=='CX':put(ix^(((ix>>w[0])&1)<<w[1]),v)
  else:
   assert op=='SourceI';bit=(ix>>w[0])&1;par=((ix>>w[1])^(ix>>w[2]))&1;put(ix^(bit<<w[2]),neg(v) if bit and par else v)
 return {q:v for q,v in out.items() if v!=Z}
def runblocks(blocks,state):
 for b in blocks:state=run(b,state)
 return state
def costs(tree,p):
 op=tree['op']
 if op=='seq':
  out=Counter()
  for x in tree['children']:out.update(costs(x,p))
  return out
 if op=='repeat':return Counter({k:v*int(tree['count']) for k,v in costs(tree['child'],p).items()})
 return Counter({('G_port' if tree['wires'][0]==p else 'G_other') if op=='G' else op:1})
def blocks_cost(blocks,p):
 c=Counter()
 for t in blocks:c.update(costs(t,p))
 return c
# Reduced-K direct selective Walsh audit and literal inverses on every column.
checked=0
for K in range(3):
 lay={'port':K+2,'spin':[K+3,K+4]};target=K;controls=list(range(K));common=2
 for pat in product((0,1),repeat=K):
  f=list(a.selective_terms(controls,list(pat),target,1,lay,common));r=list(a.selective_terms(controls,list(pat),target,1,lay,common,True));assert r==[a.nb.inverse_literal(x,lay['port'],tuple(lay['spin'])) for x in reversed(f)]
  assert blocks_cost(f,lay['port'])==+a.select_cost(controls,list(pat),1,common)
  assert blocks_cost(r,lay['port'])==+a.select_cost(controls,list(pat),1,common,True)
  for col in range(1<<(K+5)):
   state={col:O};active=all(((col>>i)&1)==b for i,b in enumerate(pat));expected=run(a.nb.repeat(1<<common,a.nb.gate('G',target)),state) if active else state
   observed=runblocks(f,state);assert observed==expected and runblocks(r,observed)==state;checked+=1
# Every one of the six mode pairs; active Fock columns and arbitrary port,
# both Spin bits, arbitrary aux and both Julia flag values. Compare to an
# independent two-level formula obtained from G^32 in the exact ring.
lay={'branch':0,'julia_flag':1,'modes':[2,3,4,5],'aux_arbitrary':6,'port':7,'spin':[8,9]};n=lay['modes'];fock_checked=0;reverse_checked=0
base=run(a.nb.repeat(32,a.nb.gate('G',2)),{0:O});co=base[0];si=base[1<<2]
for i in range(4):
 for j in range(i+1,4):
  for left,right,sign in a.pairs(i,j):
   transformed=left^(1<<j);others=[q for q in range(4) if q!=i]
   cs=[lay['branch'],lay['julia_flag']]+[n[q] for q in others];pat=[1,1]+[(transformed>>q)&1 for q in others]
   cmd={'kind':'fock','controls':cs,'pattern':pat,'target':n[i],'cx_control':n[i],'cx_target':n[j],'k':1,'reverse':sign==1}
   forward=list(a.emit_command(cmd,lay,5));back=list(a.emit_command(cmd,lay,5,True));assert back==[a.nb.inverse_literal(x,lay['port'],tuple(lay['spin'])) for x in reversed(forward)]
   assert blocks_cost(forward,lay['port'])==+a.command_cost(cmd,5)
   assert blocks_cost(back,lay['port'])==+a.command_cost(cmd,5,True)
   for bits in range(16):
    ext=((bits&1)<<lay['aux_arbitrary'])|(((bits>>1)&1)<<lay['port'])|(((bits>>2)&1)<<lay['spin'][0])|(((bits>>3)&1)<<lay['spin'][1]);prefix=ext|1|(1<<lay['julia_flag'])
    for mode in (left,right):
     col=prefix|sum(((mode>>q)&1)<<n[q] for q in range(4));other=right if mode==left else left;dest=prefix|sum(((other>>q)&1)<<n[q] for q in range(4));sgn=sign if mode==left else -sign
     want={col:co,dest:si if sgn==1 else neg(si)};actual=runblocks(forward,{col:O});assert actual==want,(i,j,sign,bits,mode);assert runblocks(back,actual)=={col:O};fock_checked+=1;reverse_checked+=1
    # Off-sector branch exactly idle with arbitrary port/spin/aux.
    col=(prefix&~1)|sum(((left>>q)&1)<<n[q] for q in range(4));assert runblocks(forward,{col:O})=={col:O}
# Common-X cost and inverse syntax on small predicates; exact target is not
# X for toy k=1, but off-branch identity and literal reversibility are exact.
lay={'port':4,'spin':[5,6],'aux_arbitrary':3};cmd={'kind':'X','controls':[0],'pattern':[1],'target':1,'k':1,'phase_k':1};f=list(a.emit_command(cmd,lay,3));r=list(a.emit_command(cmd,lay,3,True));assert r==[a.nb.inverse_literal(x,lay['port'],tuple(lay['spin'])) for x in reversed(f)]
assert blocks_cost(f,lay['port'])==+a.command_cost(cmd,3) and blocks_cost(r,lay['port'])==+a.command_cost(cmd,3,True)
for col in range(128):
 out=runblocks(f,{col:O});assert runblocks(r,out)=={col:O}
 if not col&1:assert out=={col:O}
# Full nested toy sector: literal inverse of all actual emitted blocks,
# including inverse-of-inverse, and exact inventory including both directions.
toy={'address':[],'SAM':[],'branch':0,'julia_flag':1,'modes':[2,3,4,5],'aux_arbitrary':6,'port':7,'spin':[8,9]}
toyentry={'address':0,'SAM_pattern':[]};z={'i':0,'j':2,'k':'1'};famtoy={'L':[z],'R':[z],'diagonal':{v:{'k':'1'} for v in ('00','10','01')}};xtoy={'k':'1','phase':{'k':'1'}}
toy_commands=list(a.commands(toy,toyentry,famtoy,xtoy));assert any(q.get('inverse_depth')==2 for q in toy_commands)
for q in toy_commands:
 if q.get('inverse_depth')==2:
  direct=list(a.emit_command(q,toy,5));reverse=list(a.emit_command(q,toy,5,True));assert reverse==[a.nb.inverse_literal(x,toy['port'],tuple(toy['spin'])) for x in reversed(direct)]
ff=list(a.sector_blocks(toy,toyentry,famtoy,xtoy,5));rr=list(a.sector_blocks(toy,toyentry,famtoy,xtoy,5,True))
assert rr==[a.nb.inverse_literal(x,toy['port'],tuple(toy['spin'])) for x in reversed(ff)]
assert blocks_cost(ff,toy['port'])==+a.sector_cost(toy,toyentry,famtoy,xtoy,5)
assert blocks_cost(rr,toy['port'])==+a.sector_cost(toy,toyentry,famtoy,xtoy,5,True)
# Inspect every high-level command over all families and every bank binding;
# no 2^23 terms are expanded. Check max controls and coherent selector policy.
lib=a.library();fam={x['family']:x for x in lib['families']};count=0;maxcontrol=0;maxmacro=0
for bank,entries in lib['catalogue'].items():
 for entry in entries:
  lay=a.bind_global(a.prefix_compatible_global_layout(),entry);cmd=list(a.commands(lay,entry,fam[entry['family_id']],lib['controlled_X']));maxmacro=max(maxmacro,len(cmd));assert len(cmd)<=101
  for x in cmd:
   assert len(set(x['controls']))==len(x['controls']) and x['target'] not in x['controls']
   q=len(x['controls'])+(1 if x['kind']=='X' else 0);maxcontrol=max(maxcontrol,q);assert q<=23
   assert not set(x['controls']+[x['target']]).intersection([lay['oldRIGHT_witness'],lay['phase_rebit'],*lay['comparator_scratch'],*lay['choi_input']])
  count+=1
assert count==23296 and maxcontrol<=23
out={'status':'PASS_LAZY_NATIVE_JULIA_SCHEDULE_AND_LITERAL_COUNTS','actual_native_source_sha256':sha256(Path(a.__file__).read_bytes()).hexdigest(),'angle_library_sha256':sha256((Path(a.__file__).parent/'PROPER_LINK_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'selective_exact_columns':checked,'fock_exact_active_columns':fock_checked,'fock_exact_inverse_columns':reverse_checked,'x_exact_inverse_and_offbranch_columns':128,'sector_schedules_checked':count,'max_macro_count':maxmacro,'max_controls':maxcontrol,'literal_inverse_syntax_and_inventories_match':True,'nested_toy_sector_inverse_of_inverse_literal_checked':True,'actual_lift_depth2_and_outer_depth3_checked':True,'A19_compatible_global_layout_checked':True,'real_SourceI_and_arbitrary_aux_port_spin':True,'giant_2_to_23_word_expanded':False,'physical_C_closed':False,'GR_closed':False}
Path(__file__).with_name('NATIVE_PROPER_LINK_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
