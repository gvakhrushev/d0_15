#!/usr/bin/env python3
"""Read-only independent checks of the current actual A16 instruction IR."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json,random
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
p=D/'round16/source_select.py';before=sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('b33_a16',p);a16=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a16;spec.loader.exec_module(a16)
plan=a16.instruction_plan((2,2));q=plan['layout'];gates=list(a16.ideal_gates(a16.instruction_ir(plan)))
assert set(x[0] for x in gates)<=set(('X','CX','CCX','Z','CZ'))
immutable=set(q['negative']+q['leaf']+q['coffset']+q['qoffset']+q['kind']+q['a']+q['b']+q['h']+q['delta_choi']+q['delta_car']+sum(q['CAR_RIGHT'],[]))
for gate in gates:
 op,*w=gate
 if op in ('X','CX','CCX'):assert w[-1] not in immutable
 assert len(set(w))==len(w)
def put(state,ws,value):
 assert 0<=value<2**len(ws)
 for j,w in enumerate(ws):state|=((value>>j)&1)<<w
 return state
def read(state,ws):return sum(((state>>w)&1)<<j for j,w in enumerate(ws))
def run(state):
 phase=1
 for op,*w in gates:
  if op=='X':state^=1<<w[0]
  elif op=='CX':state^=((state>>w[0])&1)<<w[1]
  elif op=='CCX':state^=((state>>w[0])&(state>>w[1])&1)<<w[2]
  elif op=='Z':phase*= -1 if (state>>w[0])&1 else 1
  elif op=='CZ':phase*= -1 if (state>>w[0])&(state>>w[1])&1 else 1
 return state,phase
rows=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text())['address_rows']
groups={1:[],2:[]}
for width,key,v in rows:
 kind=v&3
 if len(groups[kind])<200:
  groups[kind].append(((v>>2)&((1<<22)-1),(v>>24)&((1<<22)-1)))
assert all(len(v)==200 for v in groups.values())
rng=random.Random(16033);cases=0
for n in range(800):
 kind=n%4;h=(n//4)%2;negative=(n//8)%2;co=(n//16)%4;qo=(n//64)%4
 actual=kind if kind in (1,2) else (1 if n%8<4 else 2)
 a,b=groups[actual][rng.randrange(200)];ch=[rng.getrandbits(22),rng.getrandbits(22)];ca=[rng.getrandbits(12),rng.getrandbits(12)];right=[rng.getrandbits(7),rng.getrandbits(7)]
 dc=[rng.randrange(2),rng.randrange(2)];dq=[rng.randrange(2),rng.randrange(2)]
 active=(kind==1 and co<2) or (kind==2 and qo<2)
 if active:
  dest=ch if kind==1 else ca;idx=co if kind==1 else qo;dest[idx]=[a,b,(1<<(22 if kind==1 else 12))-1][(n//128)%3]
 state=0
 for name,value in [('negative',negative),('leaf',rng.randrange(512)),('coffset',co),('qoffset',qo),('kind',kind),('a',a),('b',b),('h',h)]:state=put(state,q[name],value)
 for ws,v in zip(q['choi'],ch):state=put(state,ws,v)
 for ws,v in zip(q['car'],ca):state=put(state,ws,v)
 for ws,v in zip(q['CAR_RIGHT'],right):state=put(state,ws,v)
 state=put(state,q['delta_choi'],dc[0]+2*dc[1]);state=put(state,q['delta_car'],dq[0]+2*dq[1]);new,phase=run(state)
 expected=state;ep=-1 if h and negative else 1
 if active and h:
  dest=q['choi'] if kind==1 else q['car'];idx=co if kind==1 else qo;old=read(state,dest[idx]);delta=(dc if kind==1 else dq)[idx]
  newx=b if old==a else a if old==b else old
  if delta and old not in (a,b):ep=-ep
  for bit,w in enumerate(dest[idx]):
   if ((old^newx)>>bit)&1:expected^=1<<w
 assert new==expected and phase==ep,(n,kind,h,negative,co,qo,a,b)
 cases+=1
assert sha256(p.read_bytes()).hexdigest()==before,'A16 changed during test'
out={'status':'PASS_A16_ACTUAL_INSTRUCTION_IR_INTEGRATION','source_sha256':before,'plan_degree':[2,2],'one_instruction_elementary_logical_gates':len(gates),'representative_full_instruction_cases':cases,'actual_A15_address_pairs_sampled':True,'choi_and_nonzero_car_pair_inputs':True,'data_copy_routing_and_invalid_offset':True,'negative_phase_and_sign_controls':True,'logical_read_only_records_SITE_controls_deltas_and_CAR_RIGHT':True,'all_work_restored_zero':True,'scope':'actual source_select.py ideal logical instruction IR; not full f/q degree, complete walk, native lowering or physical graph','GR_closed':False}
Path(__file__).with_name('A16_INSTRUCTION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
