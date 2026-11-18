#!/usr/bin/env python3
"""Emit real G/CX/SourceI words for each selector's zero-work requirement.

The native domain's blank_wires injects ZERO, not the physical RAW v. We
therefore leave blank_wires empty and prove an all-column gate-word identity;
the RAW v input condition and still-missing birth/clock ledger are separate.
"""
from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
source=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('a13_native',source)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'
B27=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open/round27')
check=json.loads((B27/'NATIVE_Z_CHECK.json').read_text())
assert check['routed_G_inverse_for_fresh_v_to_zero']['full_16_columns_exact']
assert check['native_source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()

packets={};summary={}
for name in ['INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json']:
    plan=json.loads((P/name).read_text());layout=plan['layout'];N=plan['wire_count']
    inputs=set(layout['palette']+layout['golden']+layout['fair'])
    zeros=[i for i in range(N) if i not in inputs]
    # Native wire numbers are tensor positions MSB-first; logical register
    # little-endian significance is retained by this explicit per-wire map.
    port=0;spin=(1,2);mapping={i:i+3 for i in range(N)};protected=N+3
    gates=[]
    for logical in zeros:
        q=mapping[logical]
        swap=[nt.Gate('CX',(q,port)),nt.Gate('CX',(port,q)),nt.Gate('CX',(q,port))]
        src=nt.Gate('SourceI',(port,*spin))
        gates.extend(swap+[src,src,nt.Gate('G',(port,)),src,src]+swap)
    ex=nt.Execution(N+4,(),(protected,),tuple(gates),nt.G_CX_SOURCE_I,port,spin)
    nt.validate_execution(ex,max_qubits=N+4,max_expanded_stages=11*len(zeros))
    assert len(gates)==11*len(zeros)
    counts=dict(Counter(g.op for g in gates))
    assert counts=={'CX':6*len(zeros),'SourceI':4*len(zeros),'G':len(zeros)}
    # Audit each actual macro, including source port/spin, order and target.
    for i,logical in enumerate(zeros):
        q=mapping[logical];chunk=gates[11*i:11*i+11]
        assert [g.op for g in chunk]==['CX']*3+['SourceI']*2+['G']+['SourceI']*2+['CX']*3
        assert chunk[0].wires==(q,port) and chunk[1].wires==(port,q)
        assert chunk[:3]==chunk[-3:]
        assert all(g.wires==(port,*spin) for g in chunk if g.op=='SourceI')
        assert chunk[5].wires==(port,)
    packets[name]={
        'logical_circuit_sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),
        'logical_to_native_wire':mapping,'zero_targets_logical':zeros,
        'execution':nt.execution_to_dict(ex),
        'word_identity':'tensor G^-1 on precisely zero targets; identity on every other input at word boundary',
        'input_condition':'Each target is a genuine fresh RAW v=(sqrt(p),p); original births are outside this gate-only component.',
        'native_domain_blank_wires_semantics':'Empty: domain blank_wires would inject computational zero, which must not be confused with RAW v.',
        'postcondition':'All listed targets zero; arbitrary input controls, port, Spin and protected oldRIGHT restored exactly.',
        'gate_inventory':counts,'gate_stages':len(gates),
        'physical_RAW_births_required':len(zeros),'RAW_birth_stage_ledger_emitted':False,
        'full_selector_native_word':False,'GR_closed':False}
    summary[name]={'zero_targets':len(zeros),'wire_count_with_port_spin_protected':N+4,
                   'gate_inventory':counts,'gate_stages':len(gates),'native_syntax_validated':True}

raw=json.dumps(packets,separators=(',',':'))+'\n'
(P/'NATIVE_ZERO_PREPARATIONS.json').write_text(raw)
result={'status':'EXPLICIT_NATIVE_G_INVERSE_WORDS_FOR_SELECTOR_ZERO_TARGETS',
        'native_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'B27_all_column_identity_sha256':hashlib.sha256((B27/'NATIVE_Z_CHECK.json').read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(raw.encode()).hexdigest(),'circuits':summary,
        'proof_method':'Composition of verified full 16-column B27 macro with explicit disjoint q addresses; every macro restores arbitrary shared port and Spin.',
        'large_full_matrix_materialized':False,'native_word_component_emitted':True,
        'RAW_birth_stage_ledger_emitted':False,'full_selector_native_word':False,
        'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'NATIVE_ZERO_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
