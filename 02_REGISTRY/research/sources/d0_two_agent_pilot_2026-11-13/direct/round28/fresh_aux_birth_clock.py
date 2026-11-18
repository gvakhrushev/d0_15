#!/usr/bin/env python3
"""Separate fresh-aux input construction for the unchanged A25 word.

Canonical RAW births below denote the OWNED isometries I_j, not a new
unitary alphabet or a permission theorem. Every birth is its own stage.
No old unknown input is reset; the old factor is retained externally.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round25'));import global_h1 as g
def birth_blocks(plan):
    l=plan['layout'];N=l['qubits']
    # Half-open intervals; source port exists before every SourceI operation.
    return [{'role':'active_port_WORK','start':l['port'],'stop':l['port']+1},
            {'role':'fresh_aux_WORK','start':l['aux_arbitrary'],'stop':l['aux_arbitrary']+1},
            {'role':'SAM','start':4,'stop':2692},
            {'role':'shared_SITE_WORK','start':2692,'stop':2700},
            {'role':'SC6_selector_WORK','start':2700,'stop':2705},
            {'role':'report_source_private_WORK','start':2706,'stop':N}]
def births(plan=None):
    """Lazy finite chronological birth list; never allocate all its entries."""
    plan=g.namespace() if plan is None else plan
    for block in birth_blocks(plan):
        for q in range(block['start'],block['stop']):
            yield {'kind':'canonical_RAW_birth','wire':q,'role':block['role'],
                   'isometry':'psi -> psi tensor v on the new labelled factor','v':'(sqrt(p),p)'}
def primitive_leaves(tree):
    if tree['op']=='seq':
        for child in tree['children']:yield from primitive_leaves(child)
    elif tree['op']=='repeat':
        for _ in range(int(tree['count'])):yield from primitive_leaves(tree['child'])
    else:yield tree
def word_primitives(plan=None):
    plan=g.namespace() if plan is None else plan
    for block in g.W_blocks(plan):yield from primitive_leaves(block)
def execution_stages(plan=None):
    """The last ACTUAL primitive is g; earlier ones are square F_j edges.

One-element lookahead, no free closing gate, no artificial birth batching.
The complete enormous iterator is specified, not executed by this script.
"""
    plan=g.namespace() if plan is None else plan
    yield from births(plan)
    it=iter(word_primitives(plan));previous=next(it)
    for gate in it:
        yield {'kind':'square_unitary_edge','gate':previous};previous=gate
    yield {'kind':'final_unitary_g','gate':previous}
def counts(plan):
    blocks=birth_blocks(plan);n=sum(b['stop']-b['start'] for b in blocks)
    word=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text())
    native=Counter({k:int(v) for k,v in word['global_native_counts']['W_literal_echo'].items()})
    L=sum(native.values());assert L==int(word['W_primitive_call_count_decimal']) and L>=1
    return n,L,native
def build():
    plan=g.namespace();l=plan['layout'];blocks=birth_blocks(plan);n,L,native=counts(plan)
    assert l['spin']==[0,1] and l['aux_arbitrary']==2 and l['oldRIGHT_witness']==3
    sorted_intervals=sorted((b['start'],b['stop']) for b in blocks)
    assert sorted_intervals==[(2,3),(4,2692),(2692,2700),(2700,2705),(2705,2706),(2706,l['qubits'])]
    assert n==l['qubits']-3==10407050781
    work=n-2688;assert work==plan['WORK_RAW_birth_count']+1==10407048093
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),D/'round25/global_h1.py',D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',
          D/'round25/ROOT_REVIEW_B52.json',D/'round27/ROOT_REVIEW_B54.json',D/'round27/SCALAR_SOURCE_BOUND.json']
    return {'status':'SEPARATE_FRESH_AUX_CANONICAL_BIRTH_AND_CLOCK_CONSTRUCTION',
            'source_sha256':{str(p):sha(p) for p in pins},
            'native_word_is_unchanged_A25_W':True,'namespace_numeric_addresses_unchanged':True,
            'input_contract_is_distinct_from_A25_unknown_aux_contract':True,
            'unknown_initial_numeric_wires':[0,1,3],
            'initial_factor':'opaque Spin C^4 tensor arbitrary D_old; wire3 witnesses D_old, with any further old factor unaddressed',
            'fresh_aux_wire':2,'any_preexisting_unknown_aux_is_retained_in_external_D_old_not_reset':True,
            'chronological_birth_blocks':blocks,'all_births_are_separate_before_first_unitary':True,
            'WORK_RAW_births':work,'SAM_RAW_births':2688,'total_canonical_RAW_birth_stages':n,
            'declared_native_unitary_calls':{k:str(v) for k,v in native.items()},
            'native_unitary_call_count':str(L),'square_unitary_edge_count':str(L-1),
            'closing_g_is_last_actual_paid_primitive':True,'extra_free_closing_unitary_inserted':False,
            'clock_layer_count_N':str(n+L),'final_layer_index_f':str(n+L-1),
            'clock_dimension_over_initial_dimension':{'coefficient':str(L+1),'power_of_two_exponent':n,'additive_constant':-1,
                                                     'formula':'(L+1)*2^n-1'},
            'final_carrier_dimension_over_initial_dimension':{'power_of_two_exponent':n},
            'initial_dimension_or_cut_rank_not_chosen_by_this_script':True,
            'scalar_corner':'<v_aux| M_A25 |v_aux> = sum_b c_hat_b Pi_b tensor I_(Spin,D_old)',
            'canonical_input_error_lt':'2^-3232','compressed_error_lt':'2^-3231','scalar_c_hat_gt':'2/3',
            'same_old_heat_price_or_input_rank_equivalence_claimed':False,
            'birth_layer_preservation_ST4_claimed':False,'heat_source_zero_claimed':False,
            'full_giant_birth_or_unitary_stream_executed':False,
            'physical_birth_or_SourceI_profile_permission_proved':False,'original_marked_map_binding_proved':False,
            'physical_C_closed':False,'GR_closed':False}
def main():
    out=build();(P/'FRESH_AUX_BIRTH_CLOCK_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'WORK_RAW_births':out['WORK_RAW_births'],'total_births':out['total_canonical_RAW_birth_stages'],
                      'native_word_changed':not out['native_word_is_unchanged_A25_W']}))
if __name__=='__main__':main()
