#!/usr/bin/env python3
"""Compose the actual A13 fixed logical word generators with native DAGs.

This emits a complete finite lowering grammar for each decoder, not the still
missing whole source-DAG dispatcher, source loader, payload router or Book map.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import hashlib,importlib.util,json,sys
import native_boolean as nb
P=Path(__file__).resolve().parent;A13=P.parent/'round13'
spec=importlib.util.spec_from_file_location('a14_logical_selectors',A13/'reversible_selectors.py')
logical=importlib.util.module_from_spec(spec);sys.modules[spec.name]=logical;spec.loader.exec_module(logical)


def lower_gate(gate,k,port,spin,aux):
    op,*w=gate
    if op=='CX':return nb.gate('CX',*w)
    if op=='X':return nb.boolean_word('X',k,target=w[0],port=port,spin=spin)
    assert op=='CCX'
    return nb.boolean_word('CCX',k,control=w[:2],target=w[2],aux=aux,port=port,spin=spin)


def macro_stream(circuit,k):
    """All logical occurrences in order, each replaced by its finite native DAG.

No operation depends on runtime data; callers may lazily expand each DAG.
Iterating all macro entries is already 52m for the three actual decoders.
"""
    size=circuit['wire_count'];port=size;spin=(size+1,size+2);aux=size+3
    word=logical.first_success_word(circuit) if circuit['schema']=='d0.logical.first-success-label.v1' else logical.selector_word(circuit)
    for gate in word:yield lower_gate(gate,k,port,spin,aux)


def scale_counts(counts,factor):return {op:value*factor for op,value in counts.items()}
def encode_counts(counts):return {op:str(counts.get(op,0)) for op in ('G','CX','SourceI')}


def main():
    angle=json.loads((P/'NATIVE_BOOLEAN_ANGLE.json').read_text());k=int(angle['k']);bits=angle['certificate']['certified_error_bits']
    templates={}
    for name in ('X','H','CCX'):
        forward=nb.boolean_word(name,k);inverse=nb.inverse_literal(forward,4,(5,6))
        nb.validate_schema(forward,8,4,(5,6),(7,));nb.validate_schema(inverse,8,4,(5,6),(7,))
        templates[name]={'forward':forward,'literal_raw_inverse':inverse,
                         'forward_inventory':encode_counts(nb.counts(forward)),
                         'literal_raw_inverse_inventory':encode_counts(nb.counts(inverse)),
                         'norm_error_upper':f'2^-{bits}'}
    (P/'NATIVE_BOOLEAN_LIBRARY.json').write_text(json.dumps({'k':str(k),'layout':{'controls':[0,1],'target':2,'arbitrary_aux':3,'port':4,'spin':[5,6],'protected_oldRIGHT':7},'templates':templates},separators=(',',':'))+'\n')
    reports=[];circuit_inputs=[]
    for filename in ['INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json']:
        path=A13/filename;circuit_inputs.append((filename,None,path,json.loads(path.read_text())))
    first_path=A13/'FIRST_SUCCESS_CIRCUITS.json'
    for label,circuit in json.loads(first_path.read_text()).items():
        circuit_inputs.append(('FIRST_SUCCESS_CIRCUITS.json',label,first_path,circuit))
    for filename,key,path,circuit in circuit_inputs:
        counts=circuit['terminal_gate_counts'];size=circuit['wire_count']
        total=Counter({'CX':counts['CX']});reverse=Counter({'CX':counts['CX']})
        for op in ('X','CCX'):
            total.update(scale_counts(nb.counts(templates[op]['forward']),counts[op]))
            reverse.update(scale_counts(nb.counts(templates[op]['literal_raw_inverse']),counts[op]))
        replacements=counts['X']+counts['CCX']
        report={'logical_circuit_file':filename,'circuit_dictionary_key':key,'logical_circuit_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'logical_wire_count':size,'native_wire_count':size+5,
                'logical_to_native_wire':'identity address map; bit significance is unchanged, not a dense integer-state reinterpretation',
                'port':size,'spin':[size+1,size+2],'arbitrary_aux':size+3,'protected_oldRIGHT':size+4,
                'logical_gate_counts':counts,'native_forward_inventory':encode_counts(total),
                'native_literal_raw_reverse_inventory':encode_counts(reverse),
                'error_upper':str(F(replacements,2**bits)),
                'error_is_all_column':True,'raw_reverse_is_true_adjoint':True,
                'extra_aux_count':1,'aux_can_be_reused_even_if_entangled':True,
                'aux_restored_only_up_to_stated_error':True,
                'oldRIGHT_untouched_at_every_primitive':True,
                'port_and_spin_restored_exactly_at_macro_boundaries':True,
                'read_only_input_groups':['labels','ready'] if key else ['palette','golden','fair'],
                'declared_inputs_read_only_at_every_primitive':True}
        reports.append(report)
    report_counts=json.loads((A13/'CIRCUIT_COMPILATION.json').read_text())['decoder_label_routing_counts_per_report']
    known=7*(report_counts['X']+report_counts['CCX'])
    assert known<2**37
    result={'status':'FINITE_NATIVE_LOWERING_OF_ALL_A13_SELECTOR_GRAMMARS',
            'k':str(k),'error_bits_per_macro':bits,'circuits':reports,
            'logical_iterator_sha256':hashlib.sha256((A13/'reversible_selectors.py').read_bytes()).hexdigest(),
            'native_macro_source_sha256':hashlib.sha256((P/'native_boolean.py').read_bytes()).hexdigest(),
            'angle_certificate_sha256':hashlib.sha256((P/'NATIVE_BOOLEAN_ANGLE.json').read_bytes()).hexdigest(),
            'native_library_sha256':hashlib.sha256((P/'NATIVE_BOOLEAN_LIBRARY.json').read_bytes()).hexdigest(),
            'expansion_rule':'macro_stream(logical_circuit,k), each macro expanded by native_boolean.expand with explicit stage bound; raw reverse uses reverse order and inverse_literal of actual leaves.',
            'huge_word_flattened_or_executed':False,
            'known_seven_report_approximate_macro_occurrences':known,
            'known_seven_report_error_upper':str(F(known,2**bits)),
            'known_seven_report_error_strict_power_bound':f'2^-{bits-37}',
            'physical_birth_mark_clock_ledger_emitted':False,
            'target_zero_and_fair_preparation':'Separate required inputs; A13 zero component and A12 fair-bank target retained; not skipped by this lowering.',
            'full_source_DAG_dispatch_compiled':False,'quantum_payload_router_compiled':False,
            'full_READY_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'NATIVE_SELECTOR_LOWERING.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'k_bits':k.bit_length(),'macro_error_bits':bits,
                      'native_decoder_wires':[r['native_wire_count'] for r in reports],
                      'approximate_macro_occurrences':[r['logical_gate_counts']['X']+r['logical_gate_counts']['CCX'] for r in reports]}),flush=True)


if __name__=='__main__':main()
