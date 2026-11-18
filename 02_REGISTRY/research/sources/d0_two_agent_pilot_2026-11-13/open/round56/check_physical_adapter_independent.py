#!/usr/bin/env python3
"""Independent piecewise append-order mapping checks, no actual SWAP."""
from pathlib import Path
from hashlib import sha256
import importlib.util,json,sys,random
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=Path(__file__).resolve().parent
sys.path.insert(0,str(D/'round28'));import physical_wire_adapter as a
N=a.f.g.namespace()['layout']['qubits'];rng=random.Random(20261114);cases=[]
for m in (3,4,17,103):
 # Independent formulas derived from explicit chronological birth blocks.
 def expected(q):
  if q==0:return 0
  if q==1:return 1
  if q==3:return 2
  if q==2705:return m
  if q==2:return m+1
  if 4<=q<=2704:return m+q-2
  assert 2706<=q<N;return m+q-3
 samples=list(range(2707))+[N-1,N-2,(N+2706)//2]+[rng.randrange(2706,N) for _ in range(1000)]
 for q in samples:
  p=expected(q);assert a.physical_wire(q,m)==p and a.logical_wire(p,m)==q
 assert all(a.logical_wire(q,m) is None for q in range(3,m))
 intervals=[(m,m+1),(m+1,m+2),(m+2,m+2690),(m+2690,m+2698),(m+2698,m+2703),(m+2703,N+m-3)]
 assert all(x[1]==y[0] for x,y in zip(intervals,intervals[1:])) and sum(b-c for c,b in intervals)==N-3
 assert a.remap_gate({'op':'CX','wires':[2692,2705]},m)=={'op':'CX','wires':[m+2690,m]}
 cases.append({'initial_raw_bits':m,'sample_count':len(samples),'last_CX':[m+2690,m]})
f=D/'round28/physical_wire_adapter.py';out={'status':'PASS_INDEPENDENT_PHYSICAL_APPEND_ORDER_ADAPTER','cases':cases,'affine_intervals_prove_full_bijection':True,'no_swap_price_or_old_cut_equivalence_inferred':True,'physical_admission_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest()}}
(P/'PHYSICAL_ADAPTER_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(cases)}))
