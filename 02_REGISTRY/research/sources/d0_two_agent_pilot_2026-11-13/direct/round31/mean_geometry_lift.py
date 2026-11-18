#!/usr/bin/env python3
"""Explicit A30 mark-to-geometry binding and certified corrected raw-chart lift.

This defines the actual moment/Jacobian recipe and proves bounds without
evaluating its giant native matrix. It does not emit physical control pulses.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import hashlib, json, sys
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round30'))
import source_mark_registry as marks
sched = marks.s
B = sched.c.old.B


def bound_certificate():
    s = F(1, 2**30); e = F(1, 2**3214); m = 2688
    r = 6*s
    exp_derivative_error = r/(1-r)
    mean_ideal = r*r/(1-r)
    mean_actual = mean_ideal+8*e
    # Six coefficient rows and columns per link; 256 independent ideal blocks.
    geometric_jacobian = 6*(exp_derivative_error+mean_ideal)/(1-mean_ideal)
    assert geometric_jacobian < F(1, 2**24)
    # Dlog_B depends on the actually perturbed mean as well as its derivative.
    # All native error entries, including cross-link effects, are retained.
    native_entry = 16*e/(s*(1-mean_actual))+8*e/((1-mean_actual)**2*(1-r))
    assert native_entry < 64*e/s
    native_jacobian = m*64*e/s
    assert native_jacobian < F(1, 2**3166)
    delta = geometric_jacobian+native_jacobian
    assert delta < F(1, 2**23)
    p_lo = F(309, 500); a_lo = F(39, 50)
    assert a_lo*a_lo < p_lo and m < 52**2
    u_lo = 2*p_lo*a_lo
    assert F(52)/(u_lo*(1-F(1, 2**23))) < 55
    bias = 52*mean_actual/(1-mean_actual)
    assert bias < F(1, 2**48)
    assert e < mean_actual/(1-mean_actual)
    return {'s': s, 'moment_entry_error': e, 'mean_matrix_error': mean_actual,
            'ideal_J_error': geometric_jacobian, 'native_J_error': native_jacobian,
            'total_J_error': delta, 'bias': bias}


def catalogue_binding():
    coord_file = B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl'
    coords = [json.loads(line) for line in coord_file.read_text().splitlines()]
    original = marks.original_binding()
    site_ids = {tuple(r['site']): r['SITE_index'] for r in original['site_bindings']}
    templates = {r['name']: i for i, r in enumerate(original['leaf_templates'])}
    block_ids, link_blocks, rows = {}, [], []
    for index, coord in enumerate(coords):
        assert coord['sam_index'] == index
        x = site_ids[tuple(coord['site'])]
        if coord['kind'] == 'proper_link':
            key = (tuple(coord['site']), coord['role'])
            if key not in block_ids:
                block_ids[key] = len(link_blocks)
                entries = []
                for i in range(4):
                    for j in range(4):
                        t = templates['M/base/%d/%d/%d' % (coord['role'], i, j)]
                        mark = marks.leaf_mark(x, t)
                        assert mark['original_Julia_address_input_output'][1:] == [1 << j, 1 << i]
                        entries.append({'row': i, 'column': j, 'original_leaf_template': t,
                                        'source_slot': mark['source_slot'],
                                        'physical_support_wires_LE_at_m0': mark['physical_support_wires_LE']})
                link_blocks.append({'block': block_ids[key], 'site': coord['site'], 'external_SITE_index': x,
                                    'role': coord['role'], 'matrix_entries': entries,
                                    'base_U0': 'original B25 precision_name.at_site(f,site,label=None).links[role]',
                                    'decoder': 'upper triangular entries of eta_null*principal_log(mean_U*inverse(U0))'})
            rows.append({'sam_index': index, **coord, 'link_block': block_ids[key],
                         'decoded_component_ab': coord['generator']})
        else:
            name = ('u/%d/%d' % (coord['role'], coord['component']) if coord['kind'] == 'coframe'
                    else 'X/base/%d' % coord['grade'])
            t = templates[name]; mark = marks.leaf_mark(x, t)
            rows.append({'sam_index': index, **coord, 'external_SITE_index': x,
                         'original_leaf_template': t, 'source_slot': mark['source_slot'],
                         'physical_support_wires_LE_at_m0': mark['physical_support_wires_LE'],
                         'decoder': 'direct original raw-u moment' if coord['kind'] == 'coframe' else 'direct original Psi moment'})
    assert len(rows) == 2688 and len(link_blocks) == 256
    assert Counter(x['kind'] for x in rows) == {'coframe': 1024, 'proper_link': 1536, 'matter': 128}
    return rows, link_blocks


def main():
    bounds = bound_certificate(); coords, blocks = catalogue_binding()
    prefix = sched.inventory()['common_mark_error_per_unit_norm']
    assert 65568*prefix < bounds['moment_entry_error']
    endpoint_error = sched.inventory()['full_compressed_error']
    assert 55*endpoint_error*2**3188 < F(1, 2**37)
    assert F(20, 3)*55*endpoint_error*2**3188 < F(1, 2**34)
    # The Neumann series is for the ACTUAL defined J, never silently J=I.
    tails = []
    for bits in (32, 64, 128, 256, 512):
        terms = (bits+1+22)//23
        assert F(1, 2**(23*terms))/(1-F(1, 2**23)) < F(1, 2**bits)
        tails.append({'desired_inverse_truncation_error_lt': '2^-'+str(bits),
                      'Neumann_terms_if_exact_J_used': terms,
                      'numerical_J_evaluation_error_not_included': True})
    pins = [Path(__file__), D/'round30/marked_source_schedule.py', D/'round30/source_mark_registry.py',
            D/'round30/COMMON_SOURCE_MARKED_PLAN.json', D/'round30/SOURCE_RAW_MARK_REGISTRY.json',
            B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl', B/'round21/CHART_ENVELOPE_RESULT.json',
            B/'round25/precision_name.py', B/'round25/TARGETS_RU.md']
    out = {'status': 'ACTUAL_MARK_JACOBIAN_RECIPE_AND_CERTIFIED_NEUMANN_LIFT',
            'coordinate_binding': coords, 'link_matrix_mark_blocks': blocks,
            'moment_operator_recipe': 'E_i=V_checkpoint^* O_i V_checkpoint=sum_b h_i(b) Pi_b tensor I_old, with V and O from A30',
            'actual_mean_recipe': 'mean_i=sum_b p^(m-|b|) p^(2|b|) h_i(b)',
            'actual_mean_derivative_recipe': 'd_alpha_j mean_i=u*sum_b_except_j weight*(h_i(b_j=1)-h_i(b_j=0)), u=2p sqrt(p)',
            'normalized_actual_J_recipe': 'J=(1/(u*s))*D_decoder(actual_mean)*D_alpha(actual_mean)',
            'J_is_not_replaced_by_identity': True,
            'incoming_control_generator': 'J_j=[[0,-1],[1,0]] on SAM_j, identity elsewhere',
            'right_inverse_recipe': 'R(y)=(1/(u*s))*sum_j (J^(-1)y)_j J_j, J^(-1)=sum_n>=0 (I-J)^n',
            'Jacobian_spectral_error_lt': '2^-23', 'scaled_generator_lift_norm_lt': '55',
            'physical_raw_chart_generator_lift_norm_lt': '55*2^30',
            'actual_decoded_centre_shift_euclidean_lt': '2^-48',
            'centre_is_not_identified_exactly_with_original_Y0': True,
            'physical_coframe_e_change_to_raw_u_Frobenius_norm_lt': '20/3',
            'lift_for_e_theta_Psi_norm_lt': '(1100/3)*2^30',
            'native_only_source_lift_error_bounds': {'raw_chart': '2^-37', 'e_theta_Psi_Frobenius_chart': '2^-34'},
            'source_error_normalization': 'these are native residual bounds under original Gamma_s=4*w*g*s/c, after multiplying by actual generator norm',
            'leading_source_after_physical_raw_lift': '(1/s)*D I_tau(Y0)[J_actual^(-1)y] under Gamma_s, not automatically D I_tau(actual_decoded_Y)[y]',
            'Jacobian_correction_and_centre_shift_source_terms_still_required': True,
            'full_source_Taylor_heat_old_price_or_reader_errors_included': False,
            'rational_bounds': {k: sched.g.encode_error(v) for k, v in bounds.items()},
            'finite_Neumann_truncation_examples': tails,
            'actual_full_J_or_mean_values_evaluated': False,
            'physical_endpoint_gate_or_reader_program_executed': False,
            'claim_scope': 'local differential at actual A30 canonical incoming SAM state, fixed B25 raw chart, fixed PF/boundary, arbitrary external old state',
            'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
            'physical_C_closed': False, 'GR_closed': False}
    (P/'MEAN_GEOMETRY_LIFT_PLAN.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'coordinates': len(coords), 'link_blocks': len(blocks),
                      'Jacobian_error_lt': '2^-23', 'raw_chart_lift_lt': '55*2^30'}))


if __name__ == '__main__':
    main()
