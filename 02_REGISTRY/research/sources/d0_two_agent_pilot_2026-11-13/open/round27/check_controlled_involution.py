#!/usr/bin/env python3
"""All-column small fixtures, actual source address boundary and phase tests."""
from pathlib import Path
import json,random,collections,math,cmath
import controlled_involution as ci
from independent_interpreter import run
P=Path(__file__).resolve().parent
small_columns=0;small_pairs=0
for n in range(2,7):
 cases=[(0,1),(0,(1<<n)-1),(1,2)]
 if n<=4:cases=[(a,b) for a in range(1<<n) for b in range(a+1,1<<n)]
 for a,b in cases:
  c=ci.compile_pair(n,a,b);L=c['layout'];small_pairs+=1
  for x in range(1<<n):
   for h in (0,1):
    for delta in (0,1):
     inp=x|(h<<L['hadamard'])|(delta<<L['delta']);res,phase=run(c['gates'],inp);out,sign=ci.expected(n,a,b,x,h,delta)
     assert (res,phase)==(out|(h<<L['hadamard'])|(delta<<L['delta']),sign),(n,a,b,x,h,delta)
     small_columns+=1
# All actual bound label pairs: test pair endpoints, an outside column and 2 arbitrary spectators, on both controls.
rows=[json.loads(s) for s in (P/'ACTUAL_PAIR_INVENTORY.jsonl').read_text().splitlines()];assert len(rows)==20992
actual_columns=0;max_gate_count=0;min_gate_count=100000;per_type=collections.Counter()
for row in rows:
 n,a,b=row['data_bits'],row['a'],row['b'];c=ci.compile_pair(n,a,b);L=c['layout'];assert len(c['gates'])==row['gates_total'] and len(c['clean_scratch'])==row['clean_scratch']
 assert not any(w>=L['qubits'] for g in c['gates'] for w in g.wires)
 outside=next(x for x in (0,1,2,(1<<n)-1) if x not in (a,b))
 for x in (a,b,outside):
  for h in (0,1):
   for delta in (0,1):
    # Extra retained RIGHT/oldRIGHT bits are not part of the circuit allocation.
    for spectators in (0,3):
     inp=x|(h<<L['hadamard'])|(delta<<L['delta'])|(spectators<<L['qubits'])
     res,phase=run(c['gates'],inp);out,sign=ci.expected(n,a,b,x,h,delta)
     expected=out|(h<<L['hadamard'])|(delta<<L['delta'])|(spectators<<L['qubits'])
     assert (res,phase)==(expected,sign),(row,x,h,delta,spectators)
     actual_columns+=1
 per_type[row['kind']]+=1;max_gate_count=max(max_gate_count,len(c['gates']));min_gate_count=min(min_gate_count,len(c['gates']))
# Test real 22-bit data at the active/padding boundary and max wire address.
chois=[r for r in rows if r['kind']=='Choi'];boundary_cases=0
for row in (chois[0],chois[len(chois)//2],chois[-1]):
 c=ci.compile_pair(22,row['a'],row['b']);L=c['layout']
 for x in (0,1,row['b'],row['b']^1,2049*1024-1,2049*1024,2**22-1):
  for h in (0,1):
   for d in (0,1):
    inp=x|(h<<L['hadamard'])|(d<<L['delta']);out,sg=run(c['gates'],inp);want,ws=ci.expected(22,row['a'],row['b'],x,h,d)
    assert (out,sg)==(want|(h<<L['hadamard'])|(d<<L['delta']),ws);boundary_cases+=1
# Reverse logical word is exact inverse even on arbitrary DIRTY work columns.
inverse_cases=0;inverse_rng=random.Random(2702)
for row in (next(x for x in rows if x['kind']=='CAR'),next(x for x in rows if x['kind']=='Choi')):
 c=ci.compile_pair(row['data_bits'],row['a'],row['b'])
 for _ in range(128):
  state=inverse_rng.getrandbits(c['layout']['qubits']);f,sg=run(c['gates'],state);back,sg2=run(ci.inverse_gates(c),f)
  assert back==state and sg*sg2==1;inverse_cases+=1
# Coherent complex superposition, joint arbitrary data, h, delta and spectator.
rng=random.Random(2701);n=5;a=7;b=19;c=ci.compile_pair(n,a,b);L=c['layout'];vec={}
for _ in range(30):
 x=rng.randrange(1<<n);h=rng.randrange(2);delta=rng.randrange(2);right=rng.randrange(2)
 inp=x|(h<<L['hadamard'])|(delta<<L['delta'])|(right<<L['qubits'])
 vec[inp]=vec.get(inp,0)+(rng.random()+1j*rng.random())
actual={};expect={}
for inp,amp in vec.items():
 out,sign=run(c['gates'],inp);actual[out]=actual.get(out,0)+sign*amp
 x=inp&((1<<n)-1);h=(inp>>L['hadamard'])&1;d=(inp>>L['delta'])&1;right=(inp>>L['qubits'])&1
 xx,s=ci.expected(n,a,b,x,h,d);target=xx|(h<<L['hadamard'])|(d<<L['delta'])|(right<<L['qubits']);expect[target]=expect.get(target,0)+s*amp
assert actual.keys()==expect.keys() and max(abs(actual[k]-expect[k]) for k in actual)<1e-14
# Hostile wrong uncompute: distinct flags eqa/eqb are values at the pre-swap x.
# Compute both clean flags, swap x=a->b, try toggling each with equality at new x.
a0,b0=1,6;x=a0;qa=int(x==a0);qb=int(x==b0);x^=a0^b0;qa^=int(x==a0);qb^=int(x==b0)
assert x==b0 and (qa,qb)==(1,1)
res={'status':'PASS_FIXED_LABEL_CLEAN_SCRATCH_CONTROLLED_SIGNED_INVOLUTION','small_n_2_to_6_pairs':small_pairs,'small_all_column_cases':small_columns,
 'actual_bound_unique_pairs':len(rows),'actual_by_type':dict(per_type),'actual_endpoint_complement_control_spectator_columns':actual_columns,
 'explicit_active_padding_boundary_cases_22bit':boundary_cases,'actual_gate_count_min':min_gate_count,'actual_gate_count_max':max_gate_count,'coherent_complex_superposition_components':len(vec),'arbitrary_dirty_column_inverse_cases':inverse_cases,
 'uncompute_equals_a_equals_b_separately_hostile':{'initial':'x=a, eqa=eqb=0, h=1','final_x':'b','dirty_flags':[qa,qb]},
 'proof_scope':'all data/h/delta basis inputs with clean scratch; full all-column identity for unknown scratch is NOT asserted',
 'RIGHT_and_oldRIGHT_spectators':True,'dynamic_lookup_compiled':False,'native_admission_claimed':False,'GR_closed':False}
(P/'LOGICAL_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
