#!/usr/bin/env python3
"""Exact Q(a) Fock-pair/Spin columns independent of the A20 checker."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import sys,json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round20');sys.path.insert(0,str(D));import coframe_native as n
Z=(0,0,0,0);I=(1,0,0,0);a=(0,1,0,0);p=(0,0,1,0)
def add(x,y):return tuple(u+v for u,v in zip(x,y))
def neg(x):return tuple(-u for u in x)
def mul(x,y):
 b=[0]*7
 for i,u in enumerate(x):
  for j,v in enumerate(y):b[i+j]+=u*v
 for k in (6,5,4):b[k-4]+=b[k];b[k-2]-=b[k]
 return tuple(b[:4])
def run(t,state):
 op=t['op']
 if op=='seq':
  for b in t['children']:state=run(b,state)
  return state
 if op=='repeat':
  assert int(t['count'])<1000000
  for _ in range(int(t['count'])):state=run(t['child'],state)
  return state
 out={}
 def put(j,v):out[j]=add(out.get(j,Z),v)
 for x,v in state.items():
  w=t['wires']
  if op=='G':
   bit=(x>>w[0])&1;put(x,mul(v,a));put(x^(1<<w[0]),mul(v,neg(p) if bit else p))
  elif op=='CX':put(x^(((x>>w[0])&1)<<w[1]),v)
  else:
   assert op=='SourceI';bit=(x>>w[0])&1;par=((x>>w[1])^(x>>w[2]))&1;put(x^(bit<<w[2]),neg(v) if bit and par else v)
 return {x:v for x,v in out.items() if v!=Z}
def blocks(xs,x):
 for t in xs:x=run(t,x)
 return x
base=run({'op':'repeat','count':'8','child':{'op':'G','wires':[0]}},{0:I});co=base[0];si=base[1];order=(0,2,3,1);small={'port':4,'spin':[5,6]};cases=0;backcases=0;off=0
for j in (1,2,3):
 rest=[k for k in range(4) if k not in (0,j)];between=order[1:order.index(j)]
 for bits in product((0,1),repeat=2):
  mask=sum(v<<q for v,q in zip(bits,rest));left=mask|1;right=mask|(1<<j);sign=(-1)**sum((mask>>q)&1 for q in between)
  diff=left^right;pivot=(diff&-diff).bit_length()-1;flips=[q for q in range(4) if q!=pivot and diff>>q&1];x=left
  for q in flips:x^=((x>>pivot)&1)<<q
  assert x>>pivot&1;ctrl=[q for q in range(4) if q!=pivot];pattern=[(x>>q)&1 for q in ctrl];bound={'K':3,'controls':ctrl,'pattern':pattern,'target':pivot,'k':1,'permutation':[{'op':'CX','wires':[pivot,q]} for q in flips]}
  # Native angle with positive G^8 sine represents a negative target pair
  # sine; reverse once for positive sign. This tests both parity signs.
  depth=int(sign==1);f=list(n.unit_blocks(bound,depth,small));r=list(n.unit_blocks(bound,depth+1,small))
  for extra in range(16):
   env=((extra&1)<<4)|(((extra>>1)&1)<<5)|(((extra>>2)&1)<<6)|(((extra>>3)&1)<<7)
   for x in (left,right):
    dest=right if x==left else left;sgn=sign if x==left else -sign;target={env|x:co,env|dest:si if sgn==1 else neg(si)};observed=blocks(f,{env|x:I});assert observed==target,(j,bits,extra,x);assert blocks(r,observed)=={env|x:I};cases+=1;backcases+=1
   # Every unselected occupation input is exactly unchanged, including aux,
   # port and the real two-bit Spin state.
   for x in range(16):
    if x in (left,right):continue
    assert blocks(f,{env|x:I})=={env|x:I};off+=1
# Exact controlled-X building blocks with arbitrary aux and true Spin. Toy
# native rotation has angle G^2, conditional aux phase has G^4: no ideal X
# is assumed before the independently certified angle approximation.
XL={'port':3,'spin':[4,5]};phase={'K':2,'controls':[0,1],'pattern':[1,1],'target':2,'k':1,'permutation':[]};rotate={'K':1,'controls':[0],'pattern':[1],'target':1,'k':1,'permutation':[]}
xf=list(n.unit_blocks(phase,0,XL))+list(n.unit_blocks(rotate,0,XL));xr=list(n.unit_blocks(rotate,1,XL))+list(n.unit_blocks(phase,1,XL));xchecks=0
for col in range(128):
 expected={col:I}
 if col&1 and col&2:expected=run({'op':'repeat','count':'4','child':{'op':'G','wires':[2]}},expected)
 if col&1:expected=run({'op':'repeat','count':'2','child':{'op':'G','wires':[1]}},expected)
 actual=blocks(xf,{col:I});assert actual==expected and blocks(xr,actual)=={col:I}
 if not col&1:assert actual=={col:I}
 xchecks+=1
out={'status':'PASS_INDEPENDENT_A20_EXACT_FOCK_COLUMNS','A20_native_sha256':sha256((D/'coframe_native.py').read_bytes()).hexdigest(),'mode_planes':3,'occupation_pairs':12,'active_full_columns':cases,'literal_inverse_columns':backcases,'inactive_full_columns':off,'controlled_X_arbitrary_aux_exact_columns':xchecks,'actual_SourceI_two_bit_spin':True,'aux_and_port_all_basis_states':True,'giant_word_expanded':False,'GR_closed':False}
(P/'A20_EXACT_FOCK_COLUMNS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
