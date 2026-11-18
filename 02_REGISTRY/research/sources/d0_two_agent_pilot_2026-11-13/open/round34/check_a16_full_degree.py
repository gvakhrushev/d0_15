#!/usr/bin/env python3
"""Test actual A16 full root instruction plans, selection endpoints and counts."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json,random
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');p=D/'round16/source_select.py';before=sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('b34_a16',p);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
rows=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())['address_rows'];pairs={1:[],2:[]}
for _,_,v in rows:
 kind=v&3
 if len(pairs[kind])<100:pairs[kind].append(((v>>2)&((1<<22)-1),(v>>24)&((1<<22)-1)))
rng=random.Random(3403);results={}
def put(s,ws,v):
 for j,w in enumerate(ws):s|=((v>>j)&1)<<w
 return s
def run(s,gates):
 ph=1
 for op,*w in gates:
  if op=='X':s^=1<<w[0]
  elif op=='CX':s^=((s>>w[0])&1)<<w[1]
  elif op=='CCX':s^=((s>>w[0])&(s>>w[1])&1)<<w[2]
  elif op=='Z':ph*=(-1 if (s>>w[0])&1 else 1)
  elif op=='CZ':ph*=(-1 if ((s>>w[0])&(s>>w[1])&1) else 1)
 return s,ph
for degree in [(82,0),(2,2)]:
 plan=a.instruction_plan(degree);q=plan['layout'];g=list(a.ideal_gates(a.instruction_ir(plan)));immutable=set(q['negative']+q['leaf']+q['coffset']+q['qoffset']+q['kind']+q['a']+q['b']+q['h']+q['delta_choi']+q['delta_car']+sum(q['CAR_RIGHT'],[]))
 for op,*w in g:
  assert op in ('X','CX','CCX','Z','CZ') and len(set(w))==len(w)
  if op in ('X','CX','CCX'):assert w[-1] not in immutable
 cases=0
 for trial in range(128):
  kind=(trial%4);h=(trial//4)%2;neg=(trial//8)%2
  if degree[0]>2:co=[0,1,40,81,82,127][(trial//16)%6]
  else:co=[0,1,2,127][(trial//16)%4]
  qo=[0,1,2,3][(trial//32)%4];tp=kind if kind in (1,2) else 1
  aa,bb=pairs[tp][rng.randrange(len(pairs[tp]))]
  ch=[rng.getrandbits(22) for _ in range(degree[0])];ca=[rng.getrandbits(12) for _ in range(degree[1])];dc=[rng.randrange(2) for _ in ch];dq=[rng.randrange(2) for _ in ca];right=[rng.getrandbits(7) for _ in ca]
  active=kind==1 and co<len(ch) or kind==2 and qo<len(ca)
  if active:
   values=ch if kind==1 else ca;ind=co if kind==1 else qo;values[ind]=[aa,bb,(1<<(22 if kind==1 else 12))-1][(trial//64)%3]
  state=0
  for name,value in [('negative',neg),('leaf',rng.randrange(512)),('coffset',co),('qoffset',qo),('kind',kind),('a',aa),('b',bb),('h',h)]:state=put(state,q[name],value)
  for ws,v in zip(q['choi'],ch):state=put(state,ws,v)
  for ws,v in zip(q['car'],ca):state=put(state,ws,v)
  for ws,v in zip(q['CAR_RIGHT'],right):state=put(state,ws,v)
  state=put(state,q['delta_choi'],sum(v<<i for i,v in enumerate(dc)));state=put(state,q['delta_car'],sum(v<<i for i,v in enumerate(dq)))
  expected=state;ep=-1 if h and neg else 1
  if active and h:
   vals=ch if kind==1 else ca;ws=(q['choi'] if kind==1 else q['car']);ind=co if kind==1 else qo;old=vals[ind];delta=(dc if kind==1 else dq)[ind];new=bb if old==aa else aa if old==bb else old
   for j,w in enumerate(ws[ind]):expected^=(((old^new)>>j)&1)<<w
   if delta and old not in (aa,bb):ep=-ep
  got,phase=run(state,g);assert got==expected and phase==ep,(degree,trial,kind,co,qo)
  cases+=1
 results[str(degree)]={'wires':plan['wire_count'],'logical_gates':len(g),'full_width_actual_instruction_cases':cases,'copy_calls':len(plan['copy_calls'])}
assert sha256(p.read_bytes()).hexdigest()==before
out={'status':'PASS_A16_BOTH_ACTUAL_ROOT_DEGREE_INSTRUCTIONS','source_sha256':before,'roots':results,'A15_sample_pairs_used':True,'first_middle_last_and_invalid_offsets':True,'immutable_inputs_untargeted_every_gate':True,'all_scratch_cleared':True,'scope':'actual logical instruction streams at both full degrees; not full chronological walk/native word','GR_closed':False}
Path(__file__).with_name('A16_FULL_DEGREE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
