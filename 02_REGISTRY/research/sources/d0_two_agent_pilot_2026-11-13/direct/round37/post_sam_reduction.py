#!/usr/bin/env python3
"""Apply the owned SAM stationary-section principle to actual A30 compression.

This computes a target and analytic feedback source bounds. It does not emit
or price a new giant native implementation of the target rotation.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json
import sympy as S

P=Path(__file__).resolve().parent
D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')


def rotate_to_reference(M, psi, chi):
    """Exact finite-dimensional SO target U M psi = ||M psi|| chi.

    The current A30 centre has positive diagonal M and chi=psi>0,
    so d>0. The same chart extends to nearby normalized psi with d>-1.
    """
    r=S.sqrt((psi.T*M.T*M*psi)[0])
    xi=M*psi/r
    d=(chi.T*xi)[0]
    K=chi*xi.T-xi*chi.T
    return S.eye(M.rows)+K+K*K/(1+d), r, xi, d


def budget():
    # B65 actual reporter/reference bounds, A33 remainder, A30 compression.
    delta=F(1,2**1543); epsilon=F(1,2**1531)
    derivative_bound=2**21
    g_upper=2*delta*epsilon*derivative_bound**2
    assert g_upper < F(1,2**3030)
    I_upper=2**13+24*16+F(1,2**1457)
    assert I_upper < 2**14
    # p^7=13p-8 and the rational p bound used in B72.
    p_upper=F(618034,10**6)
    c_ref_lower=1-8*(13*p_upper-8)
    assert c_ref_lower > F(2,3)
    e=F(1,2**3231)
    sigma=2*g_upper*I_upper+e
    assert sigma < F(1,2**3014)
    gs_lower=F(1,2**3158)
    row=sigma*sigma/(2*c_ref_lower*gs_lower)
    assert row < F(1,2**2870)
    full=55*row
    assert full < F(1,2**2864)
    # Bounds for the reduced FEEDBACK covector in the actual mean chart.
    # A34's full finite H+J C is used only as a pinned comparator, with
    # A32's finite-to-analytic error removed explicitly.
    upper=F(1,2**17)+F(1,2**67)+full
    lower=F(1,2**45)-F(1,2**67)-full
    geom=F(1,2**16)+F(1,2**67)+full
    assert upper < F(1,2**16) and lower > F(1,2**46)
    assert geom < F(1,2**15)
    return {'g_upper':g_upper, 'I_tau_uniform_upper':I_upper,
            'c_ref_lower':c_ref_lower, 'actual_sigma_upper':sigma,
            'one_unit_SAM_generator_normalized_source_difference_upper':row,
            'corrected_2688_source_difference_upper':full,
            'reduced_feedback_covector_norm_lower':lower,
            'reduced_feedback_covector_norm_upper':upper,
            'reduced_feedback_to_actual_mean_geometric_source_upper':geom}


def encode(v):
    v=F(v)
    return {'numerator_hex':hex(v.numerator),'denominator_hex':hex(v.denominator)}


def build():
    bounds=budget()
    root=D.parents[4]
    pins=[Path(__file__), D/'round2/SAM_BACKWARD_RU.md',
          D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',
          D/'round29/G_CX_ONLY_REALIZATION_RU.md',
          D/'round30/COMMON_RAW_SOURCE_MARKS_RU.md',
          D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
          D/'round31/ACTUAL_MEAN_GEOMETRY_LIFT_RU.md',
          D/'round32/FINITE_FULL_BOOK_COMPARISON_RU.md',
          D/'round33/SAMPLING_SOURCE_BIAS_RU.md',
          D/'round34/RESULT.json',
          B/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',
          B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',
          B/'round67/B67_A34_INDEPENDENT_AUDIT_RU.md',
          B/'round72/B72_BACKWARD_MARKED_OUTPUT_SUBSYSTEM_RU.md',
          root/'01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md']
    return {'status':'ACTUAL_A30_ANALYTIC_POST_SAM_FEEDBACK_STATIONARY_SECTION',
            'owned_parent':'A2 SAM backward eigensection, newly applied to coherent A30 return without its old fine-reader weights',
            'actual_M':'real diagonal canonical compression of actual A30, 2/3 I < M <= I',
            'current_input':'chi=(sqrt(p),p)^tensor2688; psi=chi at centre',
            'target':'U*=I+K+K^2/(1+d), xi=M psi/||M psi||, K=chi xi^T-xi chi^T, d=chi^T xi',
            'post_stationary_scope':'all real skew post-SAM generators for feedback J only',
            'reduced_return_squared':'q=psi^T M^T M psi; at centre E_b c_b^2',
            'reduced_feedback':'-log(1-z+z*p^K*q)',
            'reduced_gain':'Gamma_red=4*z*p^K*c_ref*g*s/(1-z+z*p^K*q)',
            'paired_gain':'Gamma_old=4*z*p^K*c*g*s/(1-z+z*p^K*c^2)',
            'source_difference':'-D_psi <(M-c_ref I)^2>/(4*c_ref*g*s)',
            'uniform_one_operator_norm_SAM_direction_difference_lt':'2^-2870',
            'corrected_2688_raw_mean_covector_difference_lt':'2^-2864',
            'reduced_feedback_raw_covector_norm_interval':['2^-46','2^-16'],
            'reduced_feedback_minus_geometric_source_at_actual_mean_lt':'2^-15',
            'source_direction_scope':'fixed actual table; incoming SAM variations, same A31 mean chart',
            'forward_mark_geometry_changed_by_post_target':False,
            'full_joint_SAM_output_preserved':False,
            'new_paid_native_target_word_emitted':False,
            'new_full_heat_or_H_plus_J_stationarity_proved':False,
            'task_admission_Cost_Info_binding_or_refinement_proved':False,
            'bounds':{k:encode(v) for k,v in bounds.items()},
            'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins},
            'physical_C_closed':False,'GR_closed':False}


if __name__=='__main__':
    out=build()
    (P/'POST_SAM_REDUCTION_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','uniform_one_operator_norm_SAM_direction_difference_lt',
                                      'new_paid_native_target_word_emitted')}))
