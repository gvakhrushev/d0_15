#!/usr/bin/env python3
"""Exact controlled Z from the actual shared quaternion SourceI port.

No zero/one ancilla, measurement, selection or assumed Spin eigenstate.
"""
from pathlib import Path
from collections import Counter
import hashlib,importlib.util,json,sys
import sympy as s
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
source=ROOT/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
spec=importlib.util.spec_from_file_location('a13_cz_native',source)
nt=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nt;spec.loader.exec_module(nt)
SOURCE_SHA=hashlib.sha256(source.read_bytes()).hexdigest()
assert SOURCE_SHA=='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'


def swap(a,b):
    return [nt.Gate('CX',(a,b)),nt.Gate('CX',(b,a)),nt.Gate('CX',(a,b))]


def cz_word(control,target,port,spin):
    assert control!=target and len(set((port,*spin)))==3
    assert control not in spin and target not in spin
    if control==port:
        control,target=target,control  # CZ is symmetric, never retarget Spin.
    src=nt.Gate('SourceI',(port,*spin))
    # Chronological order: CX; S_port^-1; CX; S_port; routed S_control.
    # S^-1=S^3 retains all three actual SourceI calls.
    core=[nt.Gate('CX',(control,port)),src,src,src,
          nt.Gate('CX',(control,port)),src]+swap(control,port)+[src]+swap(control,port)
    if target==port:
        return core
    return swap(target,port)+core+swap(target,port)


def main():
    reports=[]
    for n,control,target,port,spin in [(4,0,1,1,(2,3)),(4,1,0,1,(2,3)),
                                       (5,0,1,2,(3,4)),(5,1,0,2,(3,4))]:
        gates=cz_word(control,target,port,spin)
        execution=nt.Execution(n,(),(),tuple(gates),nt.G_CX_SOURCE_I,port,spin)
        nt.validate_execution(execution,max_qubits=n,max_expanded_stages=19)
        actual=nt.word_matrix(execution,max_qubits=n,max_expanded_stages=19)
        expected=s.diag(*[(-1)**(((x>>(n-1-control))&1)*((x>>(n-1-target))&1)) for x in range(2**n)])
        assert nt.exact_matrix_equal(actual,expected)
        counts=dict(Counter(g.op for g in gates))
        assert counts=={'CX':8 if port in (control,target) else 14,'SourceI':5}
        reports.append({'control':control,'target':target,'port':port,'spin':spin,
                        'all_columns_exact':2**n,'inventory':counts,'word':nt.execution_to_dict(execution)})
    result={'status':'PASS_EXACT_NATIVE_CZ_ALL_COLUMNS_WITH_UNKNOWN_SPIN',
            'native_source_sha256':SOURCE_SHA,'examples':reports,
            'owned_identity':'Residual owner section7dk formula971 and retained-history RP1; already-owned parity CZ, not a new existence theorem.',
            'implementation_delta':'Emit shared-port route with19 calls instead of separately routed25, or13 when one argument is port. Old/new marked histories and prices are not identified.',
            'proof':'S_c S_t CX(c,t) S_t^-1 CX(c,t)=L_i^(c+t-(c xor t))=(-1)^(ct) I_Spin; routed port restored.',
            'uses_clean_resource':False,'uses_measurement_or_feedforward':False,
            'uses_selected_ready_branch':False,'full_word_exact_without_approximation':True,
            'remaining_logical_primitives':['X','CCX','H_test'],
            'full_source_processor_native':False,'full_READY_proved':False,
            'physical_C_closed':False,'GR_closed':False}
    (P/'NATIVE_CZ_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','uses_clean_resource','uses_measurement_or_feedforward','remaining_logical_primitives']}))


if __name__=='__main__':main()
