#!/usr/bin/env python3
"""Compose all four independent MG2-axis price rows of the actual A49 family.

These are proved bounds for the constructed finite native histories, not
production evaluations, exact zeros, an all-control dual norm, original
mark admission, or identification with physical Cost-Info.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import json, sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D / 'round49'))
import two_bit_paid_family as family
B = family.source.t.loc.B


def read(path):
    return json.loads(Path(path).read_text())


def decode(value):
    return F(int(value['numerator_hex'], 16), int(value['denominator_hex'], 16))


def middle_support():
    """Check the new affine binding of the owned CODE-disjoint grammar.

    REPORT interval interiors are certified by their affine map, not by
    enumeration of billions of wires. SourceI replacement adds WORK only.
    Literal profile inverse/selfadjointness is the owned A29/B82 theorem;
    actual native return is deliberately NOT identified with that inverse.
    """
    source = family.source
    plan = source.namespace()
    layout = plan['layout']
    code = set(layout['SAM'])
    schedule = source.previous.stages()
    cut = schedule.index({'kind': 'RAW_RESOURCE_FRAME', 'intrinsic_inverse_depth': 0})
    after = schedule[cut+1:]
    assert Counter(x['kind'] for x in after) == {
        'RAW_RESOURCE_FRAME': 1, 'REPORT': 8, 'PORT_ZERO': 1, 'SC6': 1}
    assert all(x['kind'] not in ('SITE', 'SOURCE', 'SIGMA') for x in after)
    assert not code.intersection(source.previous.resource_wires())
    assert not code.intersection(plan['SC6_local_to_global'])
    shared = [*layout['SITE'], layout['port'], *layout['spin'],
              layout['aux_arbitrary'], layout['oldRIGHT_witness'], plan['old_compiler_helper']]
    assert not code.intersection(shared)
    N = plan['local_report']['logical_wire_count']
    report_intervals = []
    for report in plan['reports']:
        lo = source.ns.report_wire(plan, report, 8)
        hi = source.ns.report_wire(plan, report, N-1) + 1
        assert hi-lo == N-8 and lo == report['private_start']
        assert all(not lo <= q < hi for q in code)
        for q in [*range(8), *range(N, N+5)]:
            assert source.ns.report_wire(plan, report, q) not in code
        report_intervals.append([lo, hi])
    assert len(report_intervals) == 8
    assert tuple(family.CUTS) == ('Qf_dagger_after_common_RAW_mark', 'Qb_before_return_bank')
    return {'CODE_bits': len(code), 'middle_forward_stage_kinds': dict(Counter(x['kind'] for x in after)),
            'report_private_intervals': report_intervals,
            'REPORT_affine_interiors_and_shared_support_disjoint_from_CODE': True,
            'RAW_frames_SC6_central_sign_and_compiler_helper_disjoint_from_CODE': True,
            'actual_S_is_CODE_disjoint': True,
            'actual_S_selfadjoint_or_return_equals_forward_inverse_assumed': False,
            'source_tags_checked_by_closed_transducer_at_emission': True,
            'production_stream_enumerated': False}


def bounds():
    upstream = family.source.upper_inventory_and_error()
    paid = family.bounds(family.production_configuration())
    control = family.control.control_plan()
    b97 = read(B / 'round97/FIXED_POST_WEIGHT_CHECK.json')
    third = read(B / 'round97/SCALAR_THIRD_DERIVATIVE_CHECK.json')
    assert b97['status'] == 'PASS_A49_BORN_PRODUCT_FIXED_POST_WEIGHTED_SCALAR_SOURCE'
    assert third['I_tau_third_derivative_norm_lt'] == '2^31'
    sigma, t, gs, z = (F(1, 1 << k) for k in (80, 1700, 3208, 20))
    a = F(1, 1 << 3083)
    eW = upstream['replacement_error']
    eM = upstream['full_canonical_compressed_error']
    eprefix = upstream['full_SOURCE_DATA_fibre_prefix_error']
    eU = paid['post_full_operator_error']
    eP = decode(control['control_vs_exp_tX_error'])
    heat = paid['heat_one_price_contrast']
    assert eW < F(1, 1 << 15800)
    assert upstream['source_error'] <= eprefix
    # Phi0 uses the OLD exact reflected SourceI profile B0, not the
    # approximate native Bhat. eprefix is a conservative upper for both.
    delta = 156 * 1748 * sigma + 2 * eprefix
    assert 9 * 2688 < 156**2 and delta < F(1, 1 << 61)
    tau = 2*a*104 + (1 << 25)*sigma*104**2 + eM/gs
    assert tau < F(1, 1 << 41)
    # Dimension-free all-insertion identity from A44, with NEW inputs.
    q_kernel = F(3, 4)*(tau*(2*delta**2+2*eW)+eW/gs)
    post = eU/gs
    q_analytic_vs_half_reduced = q_kernel + post
    assert q_analytic_vs_half_reduced < F(1, 1 << 160)
    bracket = 8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
    finite_taylor = t*t*bracket/(16*gs)
    native_control = 2*eP/(t*gs)
    finite = finite_taylor + native_control + heat
    assert finite_taylor < F(1, 1 << 192)
    assert native_control < F(1, 1 << 190) and heat < F(1, 1 << 8139)
    # Recompute the actual B97 product/weight/corner envelope, retaining
    # its hypotheses and original g upper. No full-vector error / g.
    gupper = F(1, 1 << 3061)
    scalar = F(1 << 31)*sigma*sigma*104**3/3
    weight = F(3, 2)*gupper*2*(1 << 15)*3*F(3, 2)*(1 << 20)
    corner = F(3, 2)*eM/gs
    reduced_vs_DI = scalar + weight + corner
    reduced_abs = reduced_vs_DI + a
    pf = reduced_abs + post + finite
    q = reduced_abs/2 + q_analytic_vs_half_reduced + finite
    # Pb is BEFORE the fixed post. At U*, c'_Pb=-r*xi^T X xi=0.
    # Actual post and native negative controls need their own errors.
    pb = post + finite
    assert max(pf, q) < F(1, 1 << 108)
    assert pb < F(1, 1 << 189)
    # A stronger relation compares the two fully paid finite rows on
    # their common A49 clock, without claiming their heat is identical.
    q_vs_half_pf_finite = q_analytic_vs_half_reduced + post/2 + F(3, 2)*finite
    assert q_vs_half_pf_finite < F(1, 1 << 159)
    # These are coordinate Euclidean norms, NOT the original V_h norm.
    all_axes_squared = 2688*(pf*pf+2*q*q+pb*pb)
    assert all_axes_squared < F(1, 1 << 204)
    # Product quadratic cancellation does not extend to every skew X.
    # M and the centred ideal scalar mu are contractions, hence
    # ||M²-mu² I||<=2 tau_M and d_red<=3 tau_M/(2 gs).
    arbitrary_pf_analytic = F(3, 2)*tau + post
    arbitrary_q_analytic = F(3, 4)*tau + q_analytic_vs_half_reduced
    assert arbitrary_pf_analytic < F(1, 1 << 40)
    assert arbitrary_q_analytic < F(1, 1 << 41)
    return {'full_profile_insertion_replacement_error': eW,
            'whole_label_reflected_prefix_distance': delta,
            'centred_M_spread_over_g_sigma': tau,
            'Qb_analytic_minus_half_reduced_Pf': q_analytic_vs_half_reduced,
            'post_analytic_error': post,
            'finite_J_Taylor': finite_taylor,
            'independent_native_control_error': native_control,
            'heat_each_paid_row': heat,
            'reduced_Pf_vs_DI': reduced_vs_DI,
            'Pf_full_price_each_axis': pf,
            'Qf_Qb_full_price_each_axis': q,
            'Pb_full_price_each_axis': pb,
            'Qb_full_price_minus_half_Pf_full_price': q_vs_half_pf_finite,
            'all_four_2688_axis_rows_Euclidean_norm_squared': all_axes_squared,
            'arbitrary_CODE_skew_Pf_analytic_dual': arbitrary_pf_analytic,
            'arbitrary_CODE_skew_Q_analytic_dual': arbitrary_q_analytic}


def build():
    support = middle_support()
    values = bounds()
    inputs = [Path(__file__), D/'round29/gcx_compiler.py',
              D/'round44/JOINT_SOURCE_REDUCTION_RU.md', D/'round46/independent_current_bank.py',
              D/'round47/FULL_VECTOR_CONTROL_PLAN.json', D/'round48/two_bit_global_source.py',
              D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json', D/'round49/two_bit_paid_family.py',
              D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json', D/'round49/CORNER_AND_PRICE_BRIDGE.json',
              D/'round49/RESULT.json', B/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',
              B/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md',
              B/'round96/CODE_SUPPORT_CHECK.json', B/'round97/SCALAR_THIRD_DERIVATIVE_CHECK.json',
              B/'round97/FIXED_POST_WEIGHT_CHECK.json', B/'round97/B97_CHECKPOINT.json']
    return {'status': 'BOUNDED_FOUR_INDEPENDENT_MG2_AXIS_PRICE_ROWS_ON_A49',
            'scope': 'A49 H0=C, born CODE product, chosen typed SOURCE/private RAW, same fixed post, original declared Book H+J reader/gain and paid common clock',
            'support': support,
            'full_profile_all_insertion_error_lt': '2^-15800',
            'Qb_analytic_vs_half_reduced_Pf_lt': '2^-160',
            'Qb_finite_vs_half_Pf_finite_lt': '2^-159',
            'Qf_and_Qb_exact_opposite_full_price': 'same actual +/- words swapped around CODE-disjoint S at equal slot lengths; full clock stage conjugacy, not mark equality',
            'Pf_Qf_Qb_each_axis_full_price_lt': '2^-108',
            'Pb_each_axis_full_price_lt': '2^-189',
            'all_four_2688_axis_rows_Euclidean_norm_lt': '2^-102',
            'arbitrary_CODE_skew_Pf_analytic_dual_lt': '2^-40',
            'arbitrary_CODE_skew_Q_analytic_dual_lt': '2^-41',
            'arbitrary_CODE_skew_Pb_analytic_dual_lt': '2^-6039',
            'original_Vh_or_all_controls_norm_identified': False,
            'exact_stationarity_claimed': False,
            'production_targets_or_word_or_kernel_evaluated': False,
            'original_Dnu_or_vacuum_extension_admission_proved': False,
            'new_action_Info_or_selector_added': False,
            'bounds': {k: family.encode(v) for k, v in values.items()},
            'source_sha256': {str(f): sha256(f.read_bytes()).hexdigest() for f in inputs},
            'physical_C_closed': False, 'GR_closed': False}


if __name__ == '__main__':
    result = build()
    (P/'INDEPENDENT_PRICE_ROWS_PLAN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])
