#!/usr/bin/env python3
"""Bounded independent content/provenance review of A13+B27 native zeros."""
from pathlib import Path
from collections import Counter
import json,hashlib
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round13')
B=P.parent/'round27';out=D/'NATIVE_ZERO_PREPARATIONS.json';owner=D/'NATIVE_ZERO_CHECK.json';pack=json.loads(out.read_text());summary=json.loads(owner.read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert summary['output_sha256']==sha(out) and summary['B27_all_column_identity_sha256']==sha(B/'NATIVE_Z_CHECK.json')
base=json.loads((B/'NATIVE_Z_CHECK.json').read_text());native=P.parents[5]/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py';assert sha(native)==base['native_source_sha256']==summary['native_source_sha256'];assert base['full_16_columns_exact'] and base['routed_G_inverse_for_fresh_v_to_zero']['full_16_columns_exact']
counts={};total=0
for name,packet in pack.items():
 plan=json.loads((D/name).read_text());q=plan['layout'];N=plan['wire_count'];reads=set(q['palette']+q['golden']+q['fair']);zero=[i for i in range(N) if i not in reads]
 assert packet['logical_circuit_sha256']==sha(D/name) and packet['zero_targets_logical']==zero
 mapping={int(k):v for k,v in packet['logical_to_native_wire'].items()};assert mapping=={i:i+3 for i in range(N)}
 e=packet['execution'];assert e['qubits']==N+4 and e['blank_wires']==[] and e['old_right']==[N+3]
 assert e['profile']=='G_CX_SOURCE_I' and e['source_port']==0 and e['source_spin']==[1,2]
 gates=e['gates'];assert len(gates)==11*len(zero) and packet['physical_RAW_births_required']==len(zero) and not packet['RAW_birth_stage_ledger_emitted']
 counts_expected=Counter()
 for i,logical in enumerate(zero):
  dest=mapping[logical];chunk=gates[i*11:(i+1)*11]
  expected=[('CX',[dest,0]),('CX',[0,dest]),('CX',[dest,0]),('SourceI',[0,1,2]),('SourceI',[0,1,2]),('G',[0]),('SourceI',[0,1,2]),('SourceI',[0,1,2]),('CX',[dest,0]),('CX',[0,dest]),('CX',[dest,0])]
  assert [(g['op'],g['wires']) for g in chunk]==expected
  counts_expected.update(x[0] for x in expected)
  assert all(not set(g['wires'])&{mapping[k] for k in reads} and N+3 not in g['wires'] for g in chunk)
 assert dict(counts_expected)==packet['gate_inventory']==summary['circuits'][name]['gate_inventory']
 counts[name]={'fresh_v_targets':len(zero),'stages':len(gates),'gates':dict(counts_expected),'original_selector_input_wires_touched':False,'native_blank_wires':[]};total+=len(gates)
assert [counts[x]['fresh_v_targets'] for x in ['INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json']]==[1389,1595,118] and total==34122
res={'status':'PASS_BOUNDED_NATIVE_ZERO_CONTENT_AND_PROVENANCE','input_sha256':{str(out):sha(out),str(owner):sha(owner),str(B/'NATIVE_Z_CHECK.json'):sha(B/'NATIVE_Z_CHECK.json')},'circuits':counts,'all_literal_gate_stages_audited':total,
 'plan_sha256':{name:sha(D/name) for name in pack},'native_source_sha256':sha(native),'algebra_scope':'composes B27 exact G^-1_q tensor I_port tensor I_spin for each distinct q; no large matrix reconstructed',
 'native_blank_wires_interpretation':'empty, never substituted for RAW v; birth and clock ledger not emitted','full_selector_native_word':False,'GR_closed':False}
(P/'NATIVE_ZERO_REVIEW.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'stages':total,'targets':[1389,1595,118]}))
