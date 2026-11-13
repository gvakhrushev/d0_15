#!/usr/bin/env python3
"""Emit paid gate-only prefix and A14 finite native router DAG for cap 28.
RAW v births are explicit requirements, not native_execution blank_wires.
"""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,hashlib
import fair_router as fr
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
source=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
A14=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round14')
def loadmod(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
nt=loadmod('b31_native',source);nb=loadmod('b31_nb',A14/'native_boolean.py')
angle=json.loads((A14/'NATIVE_BOOLEAN_ANGLE.json').read_text());k=int(angle['k']);assert k.bit_length()==4111 and angle['certificate']['certified_error_bits']==4096
layout,logical=fr.router(28);assert layout['qubits']==143
port=143;spin=(144,145);aux=146;old=147;Q=148;G=nt.Gate
# Explicit 143 distinct paid G^-1 macros, each exact on unknown q/port/Spin.
prefix=[]
for q in range(143):
 swap=[G('CX',(q,port)),G('CX',(port,q)),G('CX',(q,port))];src=G('SourceI',(port,*spin))
 prefix.extend(swap+[src,src,G('G',(port,)),src,src]+swap)
for reg in layout['attempts']:
 for op,*w in fr.parity_kernel(reg):prefix.append(G(op,tuple(w)))
ex=nt.Execution(Q,(),(old,),tuple(prefix),nt.G_CX_SOURCE_I,port,spin)
nt.validate_execution(ex,max_qubits=Q,max_expanded_stages=4000);inv=nt.inverse_word(ex,max_qubits=Q,max_expanded_stages=4000)
assert len(prefix)==1713 and len(inv)==3989
assert Counter(g.op for g in prefix)=={'G':199,'CX':942,'SourceI':572}
assert Counter(g.op for g in inv)=={'G':199,'CX':1278,'SourceI':2512}
# Substitute A14 full-column macros in the actual logical router; preserve one
# arbitrary shared aux and protect oldRIGHT. Syntactic repeats are never expanded.
macros=[];flags={r['C'] for r in layout['attempts']}
for op,*w in logical:
 if op=='CX':tree=nb.gate('CX',*w)
 elif op=='X':tree=nb.boolean_word('X',k,target=w[0],port=port,spin=spin)
 else:
  assert op=='CCX';tree=nb.boolean_word('CCX',k,control=w[:2],target=w[2],aux=aux,port=port,spin=spin)
 nb.validate_schema(tree,Q,port,spin,(old,))
 for leaf in nb.leaves(tree):
  op0,ws=leaf['op'],leaf['wires']
  assert old not in ws
  assert not (op0=='G' and ws[0] in flags)
  assert not (op0=='CX' and ws[1] in flags)
  assert not (op0=='SourceI' and set(ws)&flags)
 macros.append(tree)
tree=nb.seq(*macros);reverse=nb.inverse_literal(tree,port,spin);nb.validate_schema(reverse,Q,port,spin,(old,))
fwd=nb.counts(tree);rev=nb.counts(reverse)
assert fwd=={'G':684*k,'CX':3995,'SourceI':1350} and sum(fwd.values())==684*k+5345
assert rev=={'G':684*k,'CX':2088*k+3995,'SourceI':2736*k+4050} and sum(rev.values())==5508*k+8045
fullforward=Counter(fwd);fullforward.update(Counter(g.op for g in prefix))
fullreverse=Counter(rev);fullreverse.update(Counter(g.op for g in inv))
assert sum(fullforward.values())==684*k+7058 and sum(fullreverse.values())==5508*k+12034
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(P/'LOGICAL_FAIR_ROUTER.json').write_text(json.dumps(fr.serial(layout,logical),indent=2)+'\n')
obj={'schema':'d0.fairbank.native.forward-and-paid-reverse.v1','k':str(k),'k_binary_length':k.bit_length(),
 'qubits':Q,'port':port,'spin':spin,'aux_arbitrary':aux,'protected_oldRIGHT':old,'logical_layout':layout,
 'physical_RAW_births_required':143,'birth_stage_ledger_emitted':False,'input_condition':'all 143 logical wires freshly born v=(sqrt(p),p); port/Spin/aux/oldRIGHT arbitrary',
 'zero_and_kernel_forward':nt.execution_to_dict(ex),'zero_and_kernel_literal_inverse':[{'op':g.op,'wires':g.wires} for g in inv],
 'router_forward_DAG':tree,'router_literal_raw_inverse_DAG':reverse,
 'logical_router_counts':{'X':3,'CX':169,'CCX':56},
 'native_forward_inventory':{j:str(fullforward[j]) for j in ('G','CX','SourceI')},
 'native_literal_reverse_inventory':{j:str(fullreverse[j]) for j in ('G','CX','SourceI')},
 'native_forward_total':'684*k+7058','native_literal_reverse_total':'5508*k+12034',
 'macro_error_upper':'59*2^-4096','full_READY_proved':False,'GR_closed':False}
raw=json.dumps(obj,separators=(',',':'))+'\n';(P/'NATIVE_FAIR_BANK.json').write_text(raw)
result={'status':'FINITE_NATIVE_PREFIX_AND_CERTIFIED_ROUTER_DAG','source_native_execution_sha256':sha(source),'A14_native_boolean_sha256':sha(A14/'native_boolean.py'),'A14_angle_sha256':sha(A14/'NATIVE_BOOLEAN_ANGLE.json'),
 'native_bank_sha256':hashlib.sha256(raw.encode()).hexdigest(),'logical_wires':143,'RAW_births_required':143,'birth_stage_ledger_emitted':False,
 'protected_oldRIGHT':old,'port':port,'spin':list(spin),'arbitrary_aux':aux,'zero_and_kernel_calls':1713,'zero_and_kernel_literal_inverse_calls':3989,
 'router_forward_calls':'684*k+5345','router_literal_inverse_calls':'5508*k+8045','full_forward_calls':'684*k+7058','full_literal_inverse_calls':'5508*k+12034',
 'per_bank_all_column_error_upper':'59*2^-4096 < 2^-4090','success_flags_read_only_during_router':True,
 'fixed_gate_stages_in_prefix_native_syntax_validated':True,'giant_router_DAG_flattened_or_executed':False,'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'NATIVE_FAIR_BANK_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
