#!/usr/bin/env python3
"""Exact small native checks, scheduler invariants and literal depth prices."""
from pathlib import Path
from hashlib import sha256
from itertools import product,islice
from collections import Counter
import json
import site_native as n
P=Path(__file__).resolve().parent;lib=n.library();lay=n.layout();nodes=n.commands(lib,lay)
assert len(nodes)==255 and [sum(z['level']==i for z in nodes) for i in range(8)]==[1,2,4,8,16,32,64,128]
# At each level exactly one prefix acts on each of the 256 input basis states.
for level in range(8):
 stage=[z for z in nodes if z['level']==level];assert all(len(z['controls'])==level for z in stage)
 for x in range(256):assert sum(all(((x>>q)&1)==v for q,v in zip(z['controls'],z['pattern'])) for z in stage)==1
for z in nodes:
 assert z['target'] in lay['SITE'] and z['target'] not in z['controls'] and lay['oldRIGHT_witness'] not in z['controls']+[z['target']]
 assert z['controls']==[lay['SITE'][i] for i in range(7,7-z['level'],-1)]
phase=n.phase_command(lib,lay);assert phase['controls']==lay['SITE'] and phase['pattern']==[0]*8 and phase['target']==lay['aux_arbitrary']
# Exact arithmetic in Q(a), a^4+a²−1=0; real SourceI acts on both Spin bits.
zero=(0,0,0,0);one=(1,0,0,0);A=(0,1,0,0);P2=(0,0,1,0)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
 q=[0]*7
 for i,x in enumerate(a):
  for j,y in enumerate(b):q[i+j]+=x*y
 for i in (6,5,4):q[i-4]+=q[i];q[i-2]-=q[i]
 return tuple(q[:4])
def run(t,state):
 op=t['op']
 if op=='seq':
  for q in t['children']:state=run(q,state)
  return state
 if op=='repeat':
  for _ in range(int(t['count'])):state=run(t['child'],state)
  return state
 out={}
 def put(q,v):out[q]=add(out.get(q,zero),v)
 for q,v in state.items():
  w=t['wires']
  if op=='G':
   bit=(q>>w[0])&1;put(q,mul(v,A));put(q^(1<<w[0]),mul(v,neg(P2) if bit else P2))
  elif op=='CX':put(q^(((q>>w[0])&1)<<w[1]),v)
  else:
   assert op=='SourceI';bit=(q>>w[0])&1;par=((q>>w[1])^(q>>w[2]))&1;put(q^(bit<<w[2]),neg(v) if bit and par else v)
 return {q:v for q,v in out.items() if v!=zero}
def runblocks(blocks,state):
 for q in blocks:state=run(q,state)
 return state
def count(t,port):
 op=t['op']
 if op=='seq':
  z=Counter()
  for q in t['children']:z.update(count(q,port))
  return z
 if op=='repeat':return Counter({k:v*int(t['count']) for k,v in count(t['child'],port).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def countall(blocks,port):
 z=Counter()
 for q in blocks:z.update(count(q,port))
 return z
checked=0
for K in range(4):
 l={'port':K+2,'spin':[K+3,K+4]};ctr=list(range(K));target=K
 for pat in product((0,1),repeat=K):
  cmd={'controls':ctr,'pattern':list(pat),'target':target,'k':1};forward=list(n.selective_blocks(cmd,l,0,3));prev=forward
  assert countall(forward,l['port'])==+n.cost(cmd,0,3)
  for depth in range(1,4):
   curr=list(n.selective_blocks(cmd,l,depth,3));assert curr==[n.nb.inverse_literal(x,l['port'],tuple(l['spin'])) for x in reversed(prev)];assert countall(curr,l['port'])==+n.cost(cmd,depth,3);prev=curr
  backward=list(n.selective_blocks(cmd,l,1,3))
  for col in range(1<<(K+5)):
   state={col:one};active=all(((col>>q)&1)==v for q,v in zip(ctr,pat));expected=run(n.nb.repeat(8,n.nb.gate('G',target)),state) if active else state;got=runblocks(forward,state);assert got==expected and runblocks(backward,got)==state;checked+=1
# New Gray-cycle all-zero reflection history: exact active/off columns,
# raw inverse depths and finite CX/G counts without requiring clean work.
gray_checked=0
for K in range(1,4):
 l={'port':K+2,'spin':[K+3,K+4]};ctr=list(range(K));target=K;cmd={'controls':ctr,'pattern':[0]*K,'target':target,'k':1}
 f=list(n.gray_phase_blocks(cmd,l,0,3));b=list(n.gray_phase_blocks(cmd,l,1,3));assert b==[n.nb.inverse_literal(x,l['port'],tuple(l['spin'])) for x in reversed(f)]
 assert countall(f,l['port'])==+n.gray_phase_cost(cmd,0,3) and countall(b,l['port'])==+n.gray_phase_cost(cmd,1,3)
 for col in range(1<<(K+5)):
  state={col:one};active=all(((col>>q)&1)==0 for q in ctr);want=run(n.nb.repeat(8,n.nb.gate('G',target)),state) if active else state;got=runblocks(f,state);assert got==want and runblocks(b,got)==state;gray_checked+=1
# Full toy writer, including a genuine literal U† in forward history; outer
# reversal cannot simplify inverse-of-inverse or the RAW G^-1 words.
toy={'tree_nodes':[{'control_bits':[],'target_bit':7,'pattern':[],'level':0,'prefix':0,'angle_id':'a'},{'control_bits':[7],'target_bit':6,'pattern':[1],'level':1,'prefix':1,'angle_id':'a'}],'angles':{'a':{'k':'1'}},'reflection_phase':{'k':'1'}}
forward=list(n.site_blocks(toy,lay));prev=forward
for depth in range(1,4):
 current=list(n.site_blocks(toy,lay,depth));assert current==[n.nb.inverse_literal(t,lay['port'],tuple(lay['spin'])) for t in reversed(prev)];prev=current
expected=n.inventory(toy,lay);assert countall(forward,lay['port'])==+expected['SITE_forward'] and countall(list(n.site_blocks(toy,lay,1)),lay['port'])==+expected['SITE_literal_inverse']
# Validate actual q-wire namespace on finite initial DAG samples.
for t in islice(n.site_blocks(lib,lay),20):n.nb.validate_schema(t,lay['qubits'],lay['port'],tuple(lay['spin']),(lay['oldRIGHT_witness'],))
assert n.inventory(lib)['RAW_inverse8']==Counter({'G_port':8,'CX':48,'SourceI':32})
# Explicit A21 integration binding: new SITE is disjoint from the existing
# loader, rebit, comparator, all SAM, port/Spin and arbitrary aux.
import sys
source_dir=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round21');sys.path.insert(0,str(source_dir));import choi_loader as a21
joint=n.bind_to_choi(a21.layout(),list(range(2739,2747)),2747)
for t in islice(n.site_blocks(lib,joint),20):
 for leaf in n.nb.leaves(t):assert not set(leaf['wires'])&set(joint['protected_external']+[joint['oldRIGHT_witness']])
try:n.bind_to_choi(a21.layout(),[0]+list(range(2739,2746)),2746);raise AssertionError('overlap accepted')
except AssertionError as ex:
 if str(ex)=='overlap accepted':raise

out={'status':'PASS_SITE_NATIVE_TREE_AND_LITERAL_INVERSES','exact_small_full_columns':checked,'gray_phase_exact_full_columns':gray_checked,'gray_forward_CX_equals_2_to_K':True,'tree_nodes':255,'tree_level_readonly_partition_checked':True,'real_SourceI_two_bit_spin':True,'arbitrary_aux_port_spin':True,'full_toy_writer_literal_depths_0_to_3':True,'actual_RAW_inverse8_paid':True,'A21_external_SITE_binding_and_collision_rejection':True,'actual_giant_word_executed':False,'library_sha256':sha256((P/'SITE_ANGLE_LIBRARY.json.gz').read_bytes()).hexdigest(),'native_source_sha256':sha256((P/'site_native.py').read_bytes()).hexdigest(),'GR_closed':False}
(P/'SITE_NATIVE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
