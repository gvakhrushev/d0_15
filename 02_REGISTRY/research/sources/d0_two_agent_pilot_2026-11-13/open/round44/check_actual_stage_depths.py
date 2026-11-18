#!/usr/bin/env python3
"""Syntactic literal-inverse audit on actual A19/A20/B42 giant-power DAG samples."""
from pathlib import Path
from itertools import islice
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round21');sys.path.insert(0,str(D));import choi_loader as c
n=c.nb;lay=c.layout();inputs=c.inputs();port=lay['port'];spin=tuple(lay['spin'])
def inverse(t):
 op=t['op']
 if op=='seq':return n.seq(*(inverse(x) for x in reversed(t['children'])))
 if op=='repeat':return n.repeat(int(t['count']),inverse(t['child']))
 if op=='CX':return t
 if op=='SourceI':return n.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=n.gate('SourceI',port,*spin);core=n.seq(src,src,n.repeat(1,n.gate('G',port)),src,src)
 if q==port:return core
 def swap(a,b):return n.seq(n.gate('CX',a,b),n.gate('CX',b,a),n.gate('CX',a,b))
 return n.seq(swap(q,port),core,swap(q,port))
def repeat_inverse(t,d):
 for _ in range(d):t=inverse(t)
 return t
# All 22 actual prefix blocks, including enormous repeat powers, without expansion.
prefix=list(c.prefix.prefix_blocks(inputs['prefix'],lay,True));prefix_checks=0
for depth in range(4):
 seq=list(c.prefix.prefix_blocks(inputs['prefix'],lay,True,reverse=bool(depth%2)))
 got=[repeat_inverse(t,depth-depth%2) for t in seq]
 want=[repeat_inverse(t,depth) for t in (reversed(prefix) if depth%2 else prefix)]
 assert got==want;prefix_checks+=len(got)
# Independently reconstruct concrete Walsh parity term.
def term(controls,pattern,target,k,mask):
 subset=[j for j in range(len(controls)) if mask>>j&1];par=[n.gate('CX',controls[j],target) for j in subset];sign=(-1)**sum(pattern[j] for j in subset)
 # Independent explicit exact negative rotation grammar.
 if sign>0:rot=n.repeat(k,n.gate('G',target))
 else:
  src=n.gate('SourceI',port,*spin);core=n.seq(src,src,n.repeat(k,n.gate('G',port)),src,src)
  def swap(a,b):return n.seq(n.gate('CX',a,b),n.gate('CX',b,a),n.gate('CX',a,b))
  rot=core if target==port else n.seq(swap(target,port),core,swap(target,port))
 return n.seq(*par,rot,*reversed(par))
# A20 actual K=20 unit with intrinsic depth 1, plus provider depths 0..3.
rows=inputs['coframe']['catalogue']['f'];bound=None
for row in rows:
 for b,depth in c.coframe.sector_units(row,inputs['coframe'],lay):
  if b['K']==20 and depth==1:bound=b;break
 if bound:break
assert bound;coframe_checks=0
for outer in range(4):
 depth=1+outer;actual=list(islice(c.coframe.unit_blocks(bound,depth,lay),5));N=1<<bound['K'];idxs=list(islice(reversed(range(N+2)) if depth%2 else range(N+2),5));expected=[]
 for ix in idxs:
  if ix==0:t=n.seq(*bound['permutation'])
  elif ix==N+1:t=n.seq(*reversed(bound['permutation']))
  else:t=term(bound['controls'],bound['pattern'],bound['target'],bound['k'],ix-1)
  expected.append(repeat_inverse(t,depth))
 assert actual==expected;coframe_checks+=len(actual)
# B42 actual K=23 Fock command with intrinsic depth2: full provider depths
# produce literal depths 2,3,4,5, rather than reducing them mod 2.
lf={x['family']:x for x in inputs['link']['families']};command=None;local=None
for row in inputs['link']['catalogue']['f']:
 if len(row['SAM_indices'])!=6:continue
 local=c.link.bind_global(lay,row)
 for z in c.link.commands(local,row,lf[row['family_id']],inputs['link']['controlled_X']):
  if z['kind']=='fock' and z['inverse_depth']==2 and len(z['controls'])==23:command=z;break
 if command:break
assert command;link_checks=0
for outer in range(4):
 # Underlying A21 provider inversion is applied to the actual stage stream;
 # bank reverse supplies one depth on odd provider depths, then each yielded
 # tree receives the remaining literal depth.
 odd=bool(outer%2);stream=c.link.emit_command(command,local,23,reverse=odd);actual=[repeat_inverse(t,outer-int(odd)) for t in islice(stream,5)]
 depth=command['inverse_depth']+outer;N=1<<len(command['controls']);masks=range(N-1,-1,-1) if depth%2 else range(N);power=command['k']*(1<<(23-len(command['controls'])));expected=[n.gate('CX',command['cx_control'],command['cx_target'])]
 expected.extend(repeat_inverse(term(command['controls'],command['pattern'],command['target'],power,m),depth) for m in islice(masks,4))
 assert actual==expected;link_checks+=len(actual)
out={'status':'PASS_A21_ACTUAL_GIANT_DAG_DEPTH_SAMPLES','A21_source_sha256':sha256((D/'choi_loader.py').read_bytes()).hexdigest(),'prefix_actual_DAG_comparisons':prefix_checks,'coframe_actual_K20_intrinsic_depth1_outer_depths0_to3':coframe_checks,'proper_link_actual_K23_intrinsic_depth2_outer_depths0_to3':link_checks,'proper_link_literal_depth_through_5':True,'giant_words_expanded':False,'GR_closed':False}
(P/'A21_ACTUAL_DEPTH_SAMPLES.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
