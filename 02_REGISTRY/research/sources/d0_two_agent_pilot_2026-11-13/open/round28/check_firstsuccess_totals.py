#!/usr/bin/env python3
"""Count actual first-success words and recompute per-report logical totals."""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,hashlib
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round13')
spec=importlib.util.spec_from_file_location('a13_review_total',D/'reversible_selectors.py');r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)
plans=json.loads((D/'FIRST_SUCCESS_CIRCUITS.json').read_text());summary=json.loads((D/'CIRCUIT_COMPILATION.json').read_text());stream=json.loads((P/'STREAM_AUDIT.json').read_text());counts={}
for name,plan in plans.items():
 q=plan['layout'];readonly=set(q['labels']+q['ready']);c=Counter()
 for gate in r.first_success_word(plan):
  assert gate[0] in ('X','CX','CCX') and gate[-1] not in readonly and len(set(gate[1:]))==len(gate)-1
  c[gate[0]]+=1
 assert dict(c)==plan['terminal_gate_counts'];counts[name]=c
s={row['file']:row['gate_counts'] for row in stream['circuits']};total=Counter()
for name,mult in [('INTERNAL_SELECTOR_CIRCUIT.json',1054*7),('TOP_SOURCE_SELECTOR_CIRCUIT.json',10*7),('TEN_SIGN_REPORT_CIRCUIT.json',1)]:total.update({k:v*mult for k,v in s[name].items()})
for name,mult in [('internal',1054),('top',10)]:total.update({k:v*mult for k,v in counts[name].items()})
assert dict(total)==summary['decoder_label_routing_counts_per_report']
res={'status':'PASS_FIRST_SUCCESS_AND_PER_REPORT_COUNTS','first_success_counts':{k:dict(v) for k,v in counts.items()},'per_report_decoder_label_routing_counts':dict(total),'input_and_attempt_wires_never_targeted':True,'counts_scope':'fixed decoders/label routes only; no DAG stack, payload router or native compiler','GR_closed':False}
(P/'FIRST_SUCCESS_COUNT_REVIEW.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
