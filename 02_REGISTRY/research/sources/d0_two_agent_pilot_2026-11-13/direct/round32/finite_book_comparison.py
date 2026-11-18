#!/usr/bin/env python3
"""Actual finite paired G/CX histories with late RAW retention.

Canonical-start witness: H0=C, Omega0=1, P0=I. The full initial A30
WORK/SAM and each late retained bit arise from original RAW births.
These are new histories, not a price equivalence to the former core.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib, json, sys
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round30'))
import marked_source_schedule as core
nb = core.c.nb
K_DEFAULT = 66076


@lru_cache(None)
def certificate():
    j = json.loads((core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json').read_text())
    assert j['status'] == 'PASS_SUFFICIENT_POSITIVE_ENDPOINT_G_POWERS'
    assert j['t'] == '2^-1618' and j['each_rotation_operator_error_strict_lt'] == '2^-4852'
    return j


def powers():
    c = certificate()
    return tuple(int(c['rotations'][name]['power_hex'], 16) for name in ('plus', 'minus'))


def align(a, b):
    """Two actual padding lengths making the entire intervals equal."""
    if a == b:
        return 0, 0
    if a > b:
        y, x = align(b, a)
        return x, y
    difference = b-a
    return {1: (5,4), 2: (2,0), 3: (5,2)}.get(difference, (difference,0))


def identity_counts(length):
    assert type(length) is int and length >= 0
    fives = length % 2
    assert length-5*fives >= 0
    return (length-5*fives)//2, fives


def padding(length):
    layout = core.g.namespace()['layout']
    a, b, c = layout['aux_arbitrary'], layout['port'], layout['qubits']
    A, B, C = nb.gate('CX', a,b), nb.gate('CX', b,c), nb.gate('CX', a,c)
    twos, fives = identity_counts(length)
    out = []
    if twos:
        out.append(nb.repeat(twos, nb.seq(A,A)))
    if fives:
        out.append(nb.seq(A,B,A,B,C))
    return nb.seq(*out)


def endpoint_parts(sign, sam_index=0):
    assert sign in ('plus', 'minus') and type(sam_index) is int and 0 <= sam_index < 2688
    nplus, nminus = powers(); assert min(nplus, nminus) > 1
    pplus, pminus = align(nplus, nminus)
    sam = core.g.namespace()['layout']['SAM'][sam_index]
    a, b, pa, pb = (nplus,nminus,pplus,pminus) if sign == 'plus' else (nminus,nplus,pminus,pplus)
    return {'pre': nb.seq(nb.repeat(a, nb.gate('G', sam)), padding(pa)),
            'post_before_final': nb.seq(nb.repeat(b-1, nb.gate('G', sam)), padding(pb)),
            'last_g': nb.gate('G', sam)}


def before_final_blocks(sign, sam_index=0):
    parts = endpoint_parts(sign, sam_index)
    yield parts['pre']
    yield from core.W_blocks()
    yield parts['post_before_final']


def execution_stages(sign, sam_index=0, retained_pairs=K_DEFAULT):
    assert type(retained_pairs) is int and retained_pairs >= 0
    # Concrete initial empty RAW history. All old-factor extensions require
    # their own actual cut/Gram/source accounting, not this empty-start budget.
    next_wire = 0
    for block in core.b.birth_blocks():
        for q in range(block['start'], block['stop']):
            physical = core.b.physical_wire(q)
            assert physical == next_wire
            next_wire += 1
            yield {'kind': 'canonical_RAW_birth', 'wire': physical, 'logical_wire': q,
                   'role': block['role'], 'carrier_qubits_after': next_wire,
                   'isometry': 'psi -> psi tensor (sqrt(p),p)'}
    for block in before_final_blocks(sign, sam_index):
        for gate in core.b.old_birth.primitive_leaves(core.b.physical_tree(block)):
            yield {'kind': 'square_unitary_edge', 'gate': gate}
    for k in range(retained_pairs):
        wire = next_wire; next_wire += 1
        yield {'kind': 'canonical_RAW_birth', 'wire': wire, 'role': 'late_retention',
               'retention_pair': k, 'carrier_qubits_after': next_wire,
               'isometry': 'psi -> psi tensor (sqrt(p),p)'}
        yield {'kind': 'square_unitary_edge', 'gate': nb.gate('G', wire), 'retention_pair': k}
    yield {'kind': 'final_unitary_g', 'gate': core.b.physical_tree(endpoint_parts(sign, sam_index)['last_g'])}


def budget(nbase, retained_pairs=K_DEFAULT):
    z, t, angular = F(1, 2**20), F(1, 2**1618), F(1, 2**4852)
    assert nbase < 2**11647
    bracket = 64/(1-z)+192*z/(1-z)**2+128*z*z/(1-z)**3
    fd = t*t*2**3158*bracket/16
    synthesis = F(3,2)*2**3158*angular/((1-z)*t)
    assert fd+synthesis < F(1, 2**74)
    assert retained_pairs == K_DEFAULT == 4*(11647+3158+1638+75+1)
    # R11: B_prefix<=2*Nbase*d_base, gamma_under=(8/3)*z*2^-3158.
    # p>3/5, and (5/6)^4<1/2; no floating exponentiation of p^K.
    assert F(5,6)**4 < F(1,2) and retained_pairs % 4 == 0
    gamma_under_without_pK = F(8,3)*z*F(1,2**3158)
    heat = F(6*nbase,359)/(t*gamma_under_without_pK)*F(1,2**(retained_pairs//4))
    assert heat < F(1, 2**76)
    total = fd+synthesis+heat
    assert total < F(1, 2**73) and 55*total < F(1, 2**67)
    return {'fd_truncation': fd, 'endpoint_angle_synthesis': synthesis,
            'all_mode_heat': heat, 'one_SAM_row_total': total,
            'corrected_physical_raw_covector_total': 55*total}


def build(retained_pairs=K_DEFAULT):
    cplan = core.build(); n = cplan['total_RAW_births']; coreL = int(cplan['new_native_call_count'])
    nplus, nminus = powers(); pplus, pminus = align(nplus,nminus)
    interval = nplus+pplus
    assert interval == nminus+pminus
    Lbase = coreL+2*interval
    Nbase = n+Lbase
    bounds = budget(Nbase, retained_pairs)
    count = Counter({key: int(value) for key, value in cplan['new_native_counts'].items()})
    count.update({'G': nplus+nminus+retained_pairs, 'CX': pplus+pminus})
    assert sum(count.values()) == Lbase+retained_pairs
    marks_layer = n+interval+int(cplan['joint_RAW_source_checkpoint_native_prefix_calls'])
    assert marks_layer < Nbase-1
    pins = [Path(__file__), D/'round30/marked_source_schedule.py', D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
            D/'round31/MEAN_GEOMETRY_LIFT_PLAN.json', core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',
            core.g.B/'round63/SUFFICIENT_G_INDEPENDENT_CHECK.json',
            D.parents[1]/'d0_retained_response_concentration_2026-10-28/RAW_CYLINDER_REALIZATION_RU.md',
            D.parents[1]/'d0_retained_response_concentration_2026-10-28/SOURCE_PROOF_RU.md']
    return {'status': 'EXPLICIT_EMPTY_START_PAIRED_G_CX_BOOK_COMPARISON_WITH_LATE_RETENTION',
            'initial_history': {'H0': 'C', 'Omega0': 1, 'P0': 'I_1', 'previous_paid_stages': 0,
                                'old_return_Gram': '1', 'rank_P0': 1, 'Tr_old_Gram': 1},
            'feedback_z': '2^-20, fixed retained-source owner', 'report_event_z0_distinct_role': '2^-20',
            'beta': '2p^2', 't': '2^-1618', 'each_endpoint_rotation_error_lt': '2^-4852',
            'SAM_directions_available': 2688,
            'same_pre_core_calls': str(interval), 'same_post_core_calls': str(interval),
            'pre_plus_padding': str(pplus), 'pre_minus_padding': str(pminus),
            'padding_logical_WORK': [2, 2705, core.g.namespace()['layout']['qubits']],
            'all_column_identity_padding_only': True,
            'early_canonical_RAW_births': n, 'late_retention_pairs': retained_pairs,
            'total_canonical_RAW_births': n+retained_pairs,
            'endpoint_calls_before_retention': str(Lbase),
            'actual_native_counts_per_endpoint': {k: str(v) for k,v in count.items()},
            'actual_clock_layers_N': str(Nbase+2*retained_pairs),
            'clock_dimension_over_initial_dimension': {'formula': '2^n*(Lbase-3+4*2^K)-1',
                'n': n, 'Lbase_minus_3': str(Lbase-3), 'K': retained_pairs, 'coefficient_of_2_to_K': 4},
            'final_carrier_dimension': {'power_of_two_exponent': n+retained_pairs},
            'last_actual_g': 'G on physical SAM wire 2+sam_index, same in both endpoints',
            'last_actual_g_is_not_the_old_core_CX': True,
            'common_original_RAW_source_checkpoint_clock_layer': str(marks_layer),
            'core_marks_shift_by_same_paid_interval': True,
            'source_observables_are_original_A30_at_that_actual_checkpoint': True,
            'physical_detector_or_seal_stages_added': False,
            'retained_cold_return': 'p^(K/2)*c_endpoint, scalar on empty initial carrier',
            'true_Book03_feedback': '-log(1-z+z*p^K*c_endpoint^2)',
            'true_heat_partition': '359*D+2*Tr_(33D) exp(-beta*Delta0(T_endpoint)); all425D modes retained',
            'bounds': {key: core.g.encode_error(value) for key,value in bounds.items()},
            'per_SAM_row_comparison_error_under_Gamma_s_lt': '2^-73',
            'corrected_2688_covector_error_under_Gamma_s_over_s_lt': '2^-67',
            'bound_consumer_conditions': 'original R6/R11 full growing-clock map and heat bound applied to exactly this common layout; source/birth/mark definitions as pinned',
            'original_full_Cost_Info_selection_or_stationarity_inferred': False,
            'central_derivative_scope': 'analytic conjugation of actual native A30 cold corner at zero; no native full padded centre word or native smooth actuation is asserted',
            'Taylor_reference_centre_and_independent_source_rows_included': False,
            'giant_word_clock_or_absolute_price_evaluated': False,
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
            'physical_C_closed': False, 'GR_closed': False}


def main():
    out = build()
    (P/'FINITE_BOOK_COMPARISON_PLAN.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({key: out[key] for key in ('status','late_retention_pairs',
                     'per_SAM_row_comparison_error_under_Gamma_s_lt','corrected_2688_covector_error_under_Gamma_s_over_s_lt')}))


if __name__ == '__main__':
    main()
