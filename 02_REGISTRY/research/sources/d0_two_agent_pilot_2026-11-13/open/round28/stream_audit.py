#!/usr/bin/env python3
"""Stream every A13 selector logical gate; no huge gate list or state vector."""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,hashlib
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round13')
spec=importlib.util.spec_from_file_location('a13_review_selectors',D/'reversible_selectors.py');r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)
names=['INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json'];results=[]
for name in names:
 path=D/name;plan=json.loads(path.read_text());q=plan['layout'];readonly=set(q['palette']+q['golden']+q['fair']);counts=Counter();arity={'X':2,'CX':3,'CCX':4};total=0
 for gate in r.selector_word(plan):
  op=gate[0];assert op in arity and len(gate)==arity[op]
  ws=gate[1:];assert all(0<=w<plan['wire_count'] for w in ws) and len(set(ws))==len(ws)
  assert ws[-1] not in readonly
  counts[op]+=1;total+=1
 assert dict(counts)==plan['terminal_gate_counts']
 results.append({'file':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'gate_counts':dict(counts),'logical_gates_streamed':total,'input_targets':0})
 print(json.dumps(results[-1]),flush=True)
out={'status':'PASS_ALL_EMITTED_LOGICAL_GATES_STREAMED','circuits':results,'gates_streamed':sum(x['logical_gates_streamed'] for x in results),'flat_word_materialized':False,'gates_executed_on_quantum_state':False,'GR_closed':False}
(P/'STREAM_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
