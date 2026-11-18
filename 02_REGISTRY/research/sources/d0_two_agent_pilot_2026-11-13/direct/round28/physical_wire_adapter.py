#!/usr/bin/env python3
"""Bind A28 logical labels to actual append-order raw-cylinder coordinates.

This is an explicit coordinate naming map at construction, not an executed
free SWAP. Every newly born physical wire is the next raw-letter coordinate.
The declared old profile (opaque Spin0/1) still requires physical binding.
"""
from pathlib import Path
import hashlib,itertools,json
import fresh_aux_birth_clock as f
P=Path(__file__).resolve().parent
def physical_wire(q,initial_raw_bits=3):
    assert type(q) is int and type(initial_raw_bits) is int and initial_raw_bits>=3
    assert 0<=q<f.g.namespace()['layout']['qubits']
    if q==0:return 0
    if q==1:return 1
    if q==3:return 2
    if q==2705:p=3
    elif q==2:p=4
    elif 4<=q<=2704:p=q+1
    else:assert q>=2706;p=q
    return p+initial_raw_bits-3
def logical_wire(q,initial_raw_bits=3):
    assert type(q) is int and 0<=q<f.g.namespace()['layout']['qubits']+initial_raw_bits-3
    if q<2:return q
    if q==2:return 3
    if q<initial_raw_bits:return None # additional old input, never addressed
    p=q-initial_raw_bits+3
    if p==3:return 2705
    if p==4:return 2
    if 5<=p<=2705:return p-1
    return p
def remap_gate(gate,initial_raw_bits=3):
    return {'op':gate['op'],'wires':[physical_wire(q,initial_raw_bits) for q in gate['wires']]}
def physical_stages(initial_raw_bits=3):
    """Complete lazy stage interface with actually appended integer wires."""
    next_wire=initial_raw_bits
    for stage in f.execution_stages():
        if stage['kind']=='canonical_RAW_birth':
            p=physical_wire(stage['wire'],initial_raw_bits);assert p==next_wire;next_wire+=1
            yield {**stage,'logical_wire':stage['wire'],'wire':p,'carrier_qubits_after':next_wire}
        else:yield {**stage,'gate':remap_gate(stage['gate'],initial_raw_bits)}
def main():
    plan=f.g.namespace();N=plan['layout']['qubits'];blocks=f.birth_blocks(plan);cases=[]
    for initial in (3,4,17):
        cursor=initial;physical=[]
        for block in blocks:
            start,stop=block['start'],block['stop'];ps=physical_wire(start,initial);pe=physical_wire(stop-1,initial)+1
            assert ps==cursor and pe-ps==stop-start;cursor=pe
            for q in {start,stop-1,(start+stop-1)//2}:assert logical_wire(physical_wire(q,initial),initial)==q
            physical.append({'role':block['role'],'start':ps,'stop':pe})
        assert cursor==N+initial-3
        # Exhaust all exceptional/shifted address roles; the rest is affine.
        for q in range(2707):assert logical_wire(physical_wire(q,initial),initial)==q
        assert all(logical_wire(q,initial) is None for q in range(3,initial))
        assert remap_gate({'op':'SourceI','wires':[2705,0,1]},initial)=={'op':'SourceI','wires':[initial,0,1]}
        cases.append({'initial_raw_bits':initial,'physical_birth_blocks':physical,'final_qubits':cursor})
    # Final actual g found without expanding repeats in independent B55.
    closing=remap_gate({'op':'CX','wires':[2692,2705]},3)
    assert closing=={'op':'CX','wires':[2693,3]}
    first=list(itertools.islice(physical_stages(3),4));assert [s['wire'] for s in first]==[3,4,5,6]
    pins=[Path(__file__),P/'fresh_aux_birth_clock.py',P/'FRESH_AUX_BIRTH_CLOCK_PLAN.json']
    out={'status':'EXPLICIT_APPEND_ORDER_PHYSICAL_WIRE_BINDING','source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
         'checked_initial_raw_prefix_sizes':cases,'all_new_physical_wires_are_next_raw_coordinates':True,
         'additional_old_coordinates_are_unaddressed':True,'logical_A25_word_unchanged':True,
         'physical_gate_addresses_are_explicitly_relabelled':True,'no_physical_SWAP_or_price_equivalence_inferred':True,
         'last_actual_g_for_three_old_bits':closing,
         'initial_source_spin_frame_0_1_requires_actual_profile_binding':True,
         'old_P0_and_history_not_chosen':True,'physical_C_closed':False,'GR_closed':False}
    (P/'PHYSICAL_WIRE_BINDING_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'tested_initial_sizes':[3,4,17],'closing_g_for_initial3':closing}))
if __name__=='__main__':main()
