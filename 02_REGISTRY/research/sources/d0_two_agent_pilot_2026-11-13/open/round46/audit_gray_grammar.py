#!/usr/bin/env python3
"""Independent Walsh/Gray, exact small-column and raw-inverse native audit."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import islice
import sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round22');sys.path.insert(0,str(D));import gray_reflection as n
j=json.loads((D/'GRAY_REFLECTION_CERTIFICATE.json').read_bytes());Z=(0,0,0,0);I=(1,0,0,0);a=(0,1,0,0);p=(0,0,1,0)
def add(x,y):return tuple(u+v for u,v in zip(x,y))
def neg(x):return tuple(-u for u in x)
def mul(x,y):
 w=[0]*7
 for i,u in enumerate(x):
  for j,v in enumerate(y):w[i+j]+=u*v
 for i in (6,5,4):w[i-4]+=w[i];w[i-2]-=w[i]
 return tuple(w[:4])
def run(t,state):
 op=t['op']
 if op=='seq':
  for z in t['children']:state=run(z,state)
  return state
 if op=='repeat':
  for _ in range(int(t['count'])):state=run(t['child'],state)
  return state
 out={}
 def put(i,z):out[i]=add(out.get(i,Z),z)
 for q,v in state.items():
  w=t['wires']
  if op=='G':
   bit=q>>w[0]&1;put(q,mul(v,a));put(q^(1<<w[0]),mul(v,neg(p) if bit else p))
  elif op=='CX':put(q^(((q>>w[0])&1)<<w[1]),v)
  else:
   assert op=='SourceI';bit=q>>w[0]&1;par=(q>>w[1]^q>>w[2])&1;put(q^(bit<<w[2]),neg(v) if bit and par else v)
 return {q:v for q,v in out.items() if v!=Z}
def apply(trees,state):
 for t in trees:state=run(t,state)
 return state
def rawinv(t,port,spin):
 op=t['op']
 if op=='seq':return n.nb.seq(*(rawinv(q,port,spin) for q in reversed(t['children'])))
 if op=='repeat':return n.nb.repeat(int(t['count']),rawinv(t['child'],port,spin))
 if op=='CX':return t
 if op=='SourceI':return n.nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=n.nb.gate('SourceI',port,*spin);core=n.nb.seq(src,src,n.nb.repeat(1,n.nb.gate('G',port)),src,src)
 if q==port:return core
 def swap(x,y):return n.nb.seq(n.nb.gate('CX',x,y),n.nb.gate('CX',y,x),n.nb.gate('CX',x,y))
 return n.nb.seq(swap(q,port),core,swap(q,port))
def applyinv(t,d,port,spin):
 for _ in range(d):t=rawinv(t,port,spin)
 return t
def treecounts(t,port):
 op=t['op']
 if op=='seq':
  z=Counter()
  for x in t['children']:z.update(treecounts(x,port))
  return z
 if op=='repeat':return Counter({k:v*int(t['count']) for k,v in treecounts(t['child'],port).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def costs(trees,port):
 z=Counter()
 for t in trees:z.update(treecounts(t,port))
 return z
def T(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
# Independent Gray bijection and all Walsh character sums up to width 8.
for K in range(1,13):
 N=1<<K;walk=0;seen={0}
 for i in range(1,N):walk^=1<<((i&-i).bit_length()-1);assert walk==i^(i>>1) and walk not in seen;seen.add(walk)
 assert len(seen)==N and walk==1<<(K-1) and walk^(1<<(K-1))==0
 if K<=8:
  for b in range(N):assert sum((-1)**(bin(b&z).count('1')%2) for z in seen)==(N if b==0 else 0)

# Exact all-column native word for all controls/aux/port/two Spin bits/old.
columns=0;depthtests=0
for K in range(1,5):
 ctr=list(range(K));aux=K;port=K+1;spin=(K+2,K+3);old=K+4
 for k in (1,2):
  f=list(n.blocks(ctr,aux,k,port,spin,(old,)));r=list(n.blocks(ctr,aux,k,port,spin,(old,),1));assert r==[rawinv(q,port,spin) for q in reversed(f)]
  raw=Counter({'G_other':(1<<K)*k,'CX':1<<K});prev=f
  for depth in range(4):
   got=list(n.blocks(ctr,aux,k,port,spin,(old,),depth));assert costs(got,port)==+raw and +n.counts(K,k,depth)==+raw
   if depth:assert got==[rawinv(q,port,spin) for q in reversed(prev)]
   prev=got;raw=T(raw);depthtests+=1
  for col in range(1<<(K+5)):
   state={col:I};expect=run(n.nb.repeat((1<<K)*k,n.nb.gate('G',aux)),state) if col&((1<<K)-1)==0 else state;actual=apply(f,state);assert actual==expect and apply(r,actual)==state;columns+=1
# Actual K8/K46 enormous-repeat blocks: independently reconstruct first
# blocks in both orders and all raw inverse depths, never expanding 2^K.
sampled=0;counts={}
for K in (8,46):
 ctr=list(range(K));aux=K;port=K+1;spin=(K+2,K+3);old=K+4;e=j['entries'][str(K)];k=int(e['k']);N=1<<K
 def block(i):
  if i==0:return n.nb.repeat(k,n.nb.gate('G',aux))
  if i==N:return n.nb.gate('CX',ctr[-1],aux)
  z=(i&-i).bit_length()-1;return n.nb.seq(n.nb.gate('CX',ctr[z],aux),n.nb.repeat(k,n.nb.gate('G',aux)))
 for depth in range(4):
  indices=range(N,-1,-1) if depth%2 else range(N+1);wanted=[applyinv(block(i),depth,port,spin) for i in islice(indices,6)];actual=list(islice(n.blocks(ctr,aux,k,port,spin,(old,),depth),6));assert actual==wanted;sampled+=len(actual)
  expected=Counter({'G_other':N*k,'CX':N})
  for _ in range(depth):expected=T(expected)
  assert +n.counts(K,k,depth)==+expected
  if depth<=1:
   saved=e['forward_counts' if depth==0 else 'literal_inverse_counts'];assert all(int(saved.get(q,'0'))==expected[q] for q in ('G_port','G_other','CX','SourceI'))
 counts[str(K)]={'forward_G_blocks':str(N),'forward_CX':str(N),'literal_inverse_sourceI_formula':'4*2^K*k'}
# Namespace guard rejects reuse of aux, Spin or protected external as control.
for test in (([0],0,2,(3,4),()),([0],1,2,(3,0),()),([0],1,2,(3,4),(0,))):
 try:n.validate(*test);raise AssertionError('invalid layout accepted')
 except AssertionError as e:
  if str(e)=='invalid layout accepted':raise
out={'status':'PASS_B46_INDEPENDENT_GRAY_AND_NATIVE_GRAMMAR','exact_all_columns_and_inverses':columns,'raw_depth_resource_checks':depthtests,'gray_bijection_K1_to_12':True,'all_Walsh_characters_through_K8':True,'actual_K8_K46_depth_samples':sampled,'actual_forward_and_literal_inverse_counts_match':True,'nonclean_aux_port_spin_arbitrary':True,'protected_wire_collision_rejected':True,'clean_wires_required':0,'exact_involution_claimed':False,'full_K46_word_executed':False,'source_sha256':sha256((D/'gray_reflection.py').read_bytes()).hexdigest(),'certificate_sha256':sha256((D/'GRAY_REFLECTION_CERTIFICATE.json').read_bytes()).hexdigest(),'GR_closed':False}
(P/'GRAY_GRAMMAR_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
