#!/usr/bin/env python3
"""Distinguish the owner's SC6 inverse program from raw letterwise inverse."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import importlib.util,json,sys
P=Path(__file__).resolve().parent;O=P.parent;owner=O/'round21';root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13');f=root/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('b48_native',f);n=importlib.util.module_from_spec(spec);sys.modules[spec.name]=n;spec.loader.exec_module(n)
def read(x):return [n.Gate(g['op'],tuple(g['wires'])) for g in map(json.loads,(owner/x).read_text().splitlines())]
a=read('SC6_FORWARD.jsonl');b=read('SC6_INVERSE.jsonl');e=n.Execution(23,(),(22,),tuple(a),n.G_CX_SOURCE_I,19,(20,21));inv=n.inverse_word(e,max_qubits=23,max_expanded_stages=100000)
assert len(a)==len(b)==18176 and len(inv)==58112 and tuple(b)!=inv
counts=lambda z:dict(Counter(g.op for g in z));assert counts(inv)=={'G':5888,'CX':4096,'SourceI':48128}
out={'status':'PASS_SC6_ORIGINAL_AND_RAW_INVERSE_ARE_DISTINCT_WORDS','forward_calls':len(a),'forward_counts':counts(a),'owner_inverse_calls':len(b),'owner_inverse_counts':counts(b),'raw_letterwise_inverse_calls':len(inv),'raw_letterwise_inverse_counts':counts(inv),'same_primitive_sequence':False,'interpretation':'The owner inverse uses paid regrouped rotations and remains a concrete exact inverse under the source-I algebra; it is not inverse_word expanded leaf by leaf. Choose the history and marks required by the actual contract before pricing; do not silently replace one with the other.','inputs_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in (owner/'SC6_FORWARD.jsonl',owner/'SC6_INVERSE.jsonl',f)},'actual_global_H1_history_binding_proved':False,'GR_closed':False}
(P/'SC6_INVERSE_PRICE_DISTINCTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'owner_inverse_calls':len(b),'raw_letterwise_inverse_calls':len(inv)}))
