#!/usr/bin/env python3
"""Four actual G/CX endpoints with one independently varied outer leg.

Consume A30/A32. The backward pair shares its entire forward core prefix,
not merely the values of selected marks. No full-task membership assertion.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, sys

P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round32'))
import finite_book_comparison as old
core, nb = old.core, old.nb


def parameters():
    a, b = old.powers()
    # G^(a+b) is within 2 delta of I by the two certified operator bounds.
    return a, b, a+b, a+b+4


def endpoint_parts(leg, sign, sam_index=2):
    assert leg in ('forward', 'backward') and sign in ('plus', 'minus')
    assert type(sam_index) is int and 0 <= sam_index < 2688
    a, b, frozen, interval = parameters()
    if leg == 'forward':
        pre, post = (a if sign == 'plus' else b), frozen
    else:
        pre, post = frozen, (b if sign == 'plus' else a)
    sam = core.g.namespace()['layout']['SAM'][sam_index]
    return {
        'pre': nb.seq(nb.repeat(pre, nb.gate('G', sam)), old.padding(interval-pre)),
        'post_before_final': nb.seq(nb.repeat(post-1, nb.gate('G', sam)), old.padding(interval-post)),
        'last_g': nb.gate('G', sam),
    }


def execution_stages(leg, sign, sam_index=2, retained_pairs=old.K_DEFAULT):
    assert type(retained_pairs) is int and retained_pairs >= 0
    next_wire = 0
    for block in core.b.birth_blocks():
        for q in range(block['start'], block['stop']):
            physical = core.b.physical_wire(q)
            assert physical == next_wire
            next_wire += 1
            yield {'kind': 'canonical_RAW_birth', 'wire': physical,
                   'logical_wire': q, 'role': block['role'],
                   'carrier_qubits_after': next_wire}
    parts = endpoint_parts(leg, sign, sam_index)
    def blocks():
        yield parts['pre']
        yield from core.W_blocks()
        yield parts['post_before_final']
    for block in blocks():
        for gate in core.b.old_birth.primitive_leaves(core.b.physical_tree(block)):
            yield {'kind': 'square_unitary_edge', 'gate': gate}
    for k in range(retained_pairs):
        wire = next_wire
        next_wire += 1
        yield {'kind': 'canonical_RAW_birth', 'wire': wire, 'role': 'late_retention',
               'retention_pair': k, 'carrier_qubits_after': next_wire}
        yield {'kind': 'square_unitary_edge', 'gate': nb.gate('G', wire), 'retention_pair': k}
    yield {'kind': 'final_unitary_g', 'gate': core.b.physical_tree(parts['last_g'])}


def bounds(nbase):
    previous = old.budget(nbase)
    # Active leg: delta. Frozen leg: 2 delta. A32 had two delta.
    angular = F(3, 2)*previous['endpoint_angle_synthesis']
    total = previous['fd_truncation']+angular+previous['all_mode_heat']
    assert total < F(1, 2**73)
    # Actual M need not be symmetric. Its ideal comparison is real diagonal.
    asymmetric_half_split = F(1, 2**74)
    # A33: paired FD/(u Gamma_s)>2^-44. u>1/2. Consume its
    # own finite comparison error, the nonsymmetry bound, and this new FD.
    lower = F(1, 2**45)-F(1, 2**73)-F(1, 2**73)-2*total
    assert lower > F(1, 2**46)
    return {'fd_truncation': previous['fd_truncation'],
            'three_delta_endpoint_synthesis': angular,
            'full_heat': previous['all_mode_heat'],
            'one_leg_finite_to_analytic_under_Gamma_s': total,
            'analytic_half_split_under_Gamma_s_strict_upper': asymmetric_half_split,
            'j2_each_leg_under_u_Gamma_s_strict_lower': lower}


def build():
    cplan = core.build()
    a, b, frozen, interval = parameters()
    n = cplan['total_RAW_births']
    L = int(cplan['new_native_call_count'])+2*interval
    nbase = n+L
    assert nbase < 2**11647
    budget = bounds(nbase)
    pins = [Path(__file__), D/'round32/finite_book_comparison.py',
            D/'round32/FINITE_FULL_BOOK_COMPARISON_RU.md',
            D/'round30/marked_source_schedule.py', D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
            D/'round33/SAMPLING_SOURCE_BIAS_RU.md', D/'round33/RESULT.json',
            D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',
            core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',
            core.g.B/'round63/SUFFICIENT_G_INDEPENDENT_CHECK.json',
            D.parents[1]/'d0_retained_response_concentration_2026-10-28/RAW_CYLINDER_REALIZATION_RU.md',
            D.parents[1]/'d0_retained_response_concentration_2026-10-28/SOURCE_PROOF_RU.md']
    return {
        'status': 'EXPLICIT_INDEPENDENT_OUTER_FINITE_COMPARISONS_WITH_CHECKPOINT_FIBRE_SOURCE',
        'initial_history': {'H0': 'C', 'Omega0': 1, 'P0': 'I_1', 'previous_paid_stages': 0},
        'sample_direction': 2, 'sample_physical_SAM_wire': 4,
        'available_directions': 2688,
        'n_plus_hex': hex(a), 'n_minus_hex': hex(b), 'frozen_n0_hex': hex(frozen),
        'frozen_rotation_error_strict_lt': '2*2^-4852',
        'each_complete_endpoint_error_strict_lt': '3*2^-4852',
        'common_each_outer_interval_hex': hex(interval),
        'early_births': n, 'late_retention_pairs': old.K_DEFAULT,
        'Lbase_hex': hex(L), 'Nbase_hex': hex(nbase),
        'Nbase_strict_lt': '2^11647',
        'actual_clock_layers_N_hex': hex(nbase+2*old.K_DEFAULT),
        'clock_dimension': '2^n*(Lbase-3+4*2^K)-1',
        'final_dimension': '2^(n+K)',
        'RAW_source_checkpoint_layer_hex': hex(n+interval+int(cplan['joint_RAW_source_checkpoint_native_prefix_calls'])),
        'last_actual_gate': 'G on physical SAM 2+j in all four words',
        'forward_ideal_comparison': '<v|Mhat R(+-t)|v>',
        'backward_ideal_comparison': '<v|R(-+t) Mhat|v>',
        'actual_core_exact_symmetry_used': False,
        'actual_core_ideal_compression_error_lt': '2^-3231',
        'g_times_s_gt': '2^-3158',
        'analytic_leg_sum_equals_paired_derivative': True,
        'each_analytic_leg_half_split_error_under_Gamma_s_lt': '2^-74',
        'each_leg_full_finite_comparison_error_under_Gamma_s_lt': '2^-73',
        'j2_each_finite_price_comparison_under_u_Gamma_s_gt': '2^-46',
        'backward_pair_has_identical_complete_prefix_through_A30_core': True,
        'backward_pair_original_RAW_checkpoint_marks_identical': True,
        'backward_variation_decoded_forward_field_tangent': False,
        'A31_inverse_J_applied_to_backward_variation': False,
        'same_complete_task_membership_or_FN_fibre_proved': False,
        'four_preparation_occurrences_all_closed': False,
        'new_padded_native_centre_or_joint_stationarity_proved': False,
        'Cost_Info_binding_or_selected_physical_history_proved': False,
        'bound_conditions': 'A30 canonical compression and same R6/R11 growing-clock hypotheses as A32; actual K and final g retained',
        'bounds': {k: core.g.encode_error(v) for k,v in budget.items()},
        'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
        'physical_C_closed': False, 'GR_closed': False,
    }


if __name__ == '__main__':
    result = build()
    (P/'INDEPENDENT_OUTER_PAIRS_PLAN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status', 'j2_each_finite_price_comparison_under_u_Gamma_s_gt',
                                         'backward_pair_original_RAW_checkpoint_marks_identical')}))
