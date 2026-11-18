#!/usr/bin/env python3
"""Exact small-K native Walsh words from A18 pair_blocks, true Spin."""
from pathlib import Path
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=D/'round18';sys.path.insert(0,str(P));spec=importlib.util.spec_from_file_location('b38_walsh',P/'material_preparation.py');a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
zero=(0,0,0,0);one=(1,0,0,0)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ma(x):return x[3],x[0],x[1]-x[3],x[2]
def mp(x):return x[2],x[3],x[0]-x[2],x[1]-x[3]
def cs(n):
 c,s=one,zero
 for _ in range(n):c,s=add(ma(c),neg(mp(s))),add(mp(c),ma(s))
 return c,s
def run(word,state):
 for op,*w in word:
  out={}
  if op=='G':
   for x,z in state.items():
    bit=(x>>w[0])&1;base=x&~(1<<w[0]);p=neg(mp(z)) if bit else ma(z);q=ma(z) if bit else mp(z)
    out[base]=add(out.get(base,zero),p);j=base|(1<<w[0]);out[j]=add(out.get(j,zero),q)
  elif op=='CX':
   for x,z in state.items():j=x^(((x>>w[0])&1)<<w[1]);out[j]=add(out.get(j,zero),z)
  else:
   assert op=='SourceI'
   for x,z in state.items():
    bit=(x>>w[0])&1;parity=((x>>w[1])^(x>>w[2]))&1;j=x^(bit<<w[2]);v=neg(z) if bit and parity else z;out[j]=add(out.get(j,zero),v)
  state={x:v for x,v in out.items() if v!=zero}
 return state
reports=[]
for K,patterns in [(2,[(0,0),(1,0),(1,1)]),(3,[(0,0,0),(1,0,1),(1,1,1)])]:
 port=K+1;spin=[port+1,port+2];old=port+3;layout={'port':port,'spin':spin};controls=list(range(1,K+1))
 for pat in patterns:
  bound={'K':K,'controls':controls,'pattern':list(pat),'target':0,'permutation':[],'k':1}
  blocks=list(a.pair_blocks(bound,layout));invs=list(a.pair_blocks(bound,layout,True));assert len(blocks)==len(invs)==(1<<K)+2
  for f,r in zip(reversed(blocks),invs):assert r==a.nb.inverse_literal(f,port,tuple(spin))
  forward=[(g['op'],*g['wires']) for block in blocks for g in a.nb.expand(block,10000)];back=[(g['op'],*g['wires']) for block in invs for g in a.nb.expand(block,10000)];c,s=cs(1<<K)
  for col in range(1<<(old+1)):
   active=all(((col>>w)&1)==v for w,v in zip(controls,pat));bit=col&1
   if active:want={col:c,col^1:neg(s) if bit else s}
   else:want={col:one}
   got=run(forward,{col:one});assert got==want,(K,pat,col)
   assert run(back,got)=={col:one}
  reports.append({'K':K,'pattern':pat,'all_columns':1<<(old+1),'forward_gates':len(forward),'literal_inverse_gates':len(back)})
out={'status':'PASS_A18_SMALL_NATIVE_WALSH_EXACT_TRUE_SPIN','reports':reports,'all_columns':sum(x['all_columns'] for x in reports),'all_inverse_cases':sum(x['all_columns'] for x in reports),'true_spin':'diag(J,-J)','general_K_argument':'Walsh parity identity exactly cancels all off-predicate rotations; on-sector exponent=2^K*k*theta','full_K11_K13_huge_words_executed':False,'GR_closed':False}
Path(__file__).with_name('A18_WALSH_EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
