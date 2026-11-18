#!/usr/bin/env python3
"""Structured full 2688-row bound for the unchanged B25/A30/A32 sampler.

Checks exact incidence counts and rational constants of the proof. No matrix
of the enormous quantum circuit and no new geometric root is evaluated.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json
import sympy as S

P = Path(__file__).resolve().parent
D = P.parent
B = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')


def main():
    readrows = lambda f: [json.loads(x) for x in f.read_text().splitlines()]
    coords = readrows(B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl')
    counts = Counter(c['kind'] for c in coords)
    assert counts == {'coframe': 1024, 'proper_link': 1536, 'matter': 128}, counts
    addresses = readrows(B/'round24/TORUS_CHOI_ADDRESSES.jsonl')
    addr = {(a['kind'], tuple(a['site']), a['direction']):a['a'] for a in addresses if 'site' in a}
    stencil = readrows(B/'round24/SITE_DEPENDENCIES.jsonl')
    link_incidence = Counter()
    matter_incidence = Counter()
    for x in stencil:
        for face in x['faces']:
            assert len(set(face['torus_addresses'])) == 4
            link_incidence.update(face['torus_addresses'])
        matter_incidence.update([tuple(x['site'])] + [tuple(z) for z in x['matter_forward_torus']])
    for c in coords:
        if c['kind'] == 'proper_link':
            assert link_incidence[addr['proper_link',tuple(c['site']),c['role']]] == 6
        elif c['kind'] == 'matter':
            assert matter_incidence[tuple(c['site'])] == 5

    s, h, nu = F(1,2**30), F(1,4), F(3,5)
    assert F(22,7)/50 + 24*s < 1  # actual two-component central Dpsi and all cube noise
    assert 24/(1-24*s) < 25
    assert F(17,16)**4 < F(4,3)
    assert F(4,3) + 34*s*s < F(3,2)
    # One own link-coordinate secant: E exp(A1)-exp(A0) divided by s.
    # Linear term K; quadratic term s*(1-2p^2)*K^2/2; remainder below.
    third_remainder_coefficient = F(4,3)*F(2*24**3,6)/(1-24*s)
    assert third_remainder_coefficient < 6145
    own_link_secant_error = F(8,3)*s + third_remainder_coefficient*s*s
    assert own_link_secant_error < 3*s
    assert F(16,3)+own_link_secant_error < 6
    # Other three independent mean-link factors each differ by <34s^2.
    loop_secant_error = 3*s*F(3,2)**3 + 3*34*s*s*6*F(3,2)**2
    assert loop_secant_error < 11*s
    f_link_row = 6*h**4*F(1600,9)*11*s
    assert f_link_row < 46*s
    f_coframe_row = 2**10*s*s

    # Scalar matter: Var(one free field)=V=s^2*p^3<s^2/4.
    # One row of Dpsi covariance has norm <=8 V/h^2; ||u||<2.
    vbound = s*s/4
    q_coframe_local = s/(4*nu*nu) + 32*vbound/(nu*nu*h*h)
    assert q_coframe_local < s
    q_coframe_row = h**4*q_coframe_local
    assert f_coframe_row + 24*q_coframe_row < s

    # Exact averaged metric identity at a free coframe base point:
    # E[u^T eta u]-u0^T eta u0 = V*trace(eta)*I = -2V I.
    eta = S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    assert eta.trace() == -2 and eta.T*eta == S.eye(4)
    metric_error = 2*vbound/(nu*nu)
    assert metric_error < 2*s*s
    assert F(4)/(nu*nu) < 12
    assert 12+metric_error < 13
    q_matter_local = 2*8*(2*s*s) + (s/4)*13*64
    assert q_matter_local < 209*s
    q_matter_row = 24*5*h**4*q_matter_local
    assert q_matter_row < 98*s

    # Full Euclidean covector, not a per-row estimate presented as a vector.
    squared_coefficient = 1024 + 1536*46**2 + 128*98**2
    assert squared_coefficient == 4480512 < 2**24
    geometric_sampling = 2**12*s
    assert geometric_sampling == F(1,2**18)
    # E_geom(Y0)=0 from B65. Reference multiplier, scalar report remainder.
    reference = F(1,2**3084)*2**19
    reporter = 55*F(1,2**1426)
    assert reference == F(1,2**3065) and reporter < F(1,2**1420)
    jacobian_inverse = 1/(1-F(1,2**23))
    native_and_finite = F(2,2**67)
    raw_covector = jacobian_inverse*(geometric_sampling+reference+reporter)+native_and_finite
    assert raw_covector < F(1,2**17)
    decoded_centre_difference = F(1,2**24)
    assert raw_covector+decoded_centre_difference < F(1,2**16)
    paths = [Path(__file__), B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',
             B/'round24/TORUS_CHOI_ADDRESSES.jsonl', B/'round24/SITE_DEPENDENCIES.jsonl',
             B/'round25/targets.py', B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',
             B/'round65/SCALAR_HESSIAN_ENVELOPE.json', D/'round11/source_operator_dag.py',
             D/'round30/COMMON_SOURCE_MARKED_PLAN.json', D/'round31/RESULT.json',
             D/'round32/RESULT.json', D/'round33/SAMPLING_SOURCE_BIAS_RU.md',
             D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json']
    out = {'status':'PASS_STRUCTURED_FULL_SAMPLING_SOURCE_UPPER_BOUND',
           'fixed_sampling_s':'2^-30', 'coordinates_by_kind':dict(counts),
           'all_actual_free_links_have_six_face_occurrences':True,
           'all_matter_coordinates_have_five_base_stencils':True,
           'each_face_has_four_distinct_link_addresses':True,
           'geometric_f_coframe_row_error_lt':'2^10*s^2',
           'geometric_f_link_row_error_lt':'46*s',
           'k0_q_coframe_and_f_joint_row_error_lt':'s',
           'k0_q_matter_row_error_lt':'98*s',
           'squared_full_vector_coefficient_lt':squared_coefficient,
           'unadjusted_geometric_sampling_vector_error_lt':'2^-18',
           'finite_reference_vector_error_lt':'2^-3065',
           'finite_reporter_vector_error_lt':'2^-1420',
           'actual_corrected_finite_H_plus_J_raw_covector_norm_lt':'2^-17',
           'actual_corrected_finite_covector_minus_Egeom_at_decoded_mean_norm_lt':'2^-16',
           'combined_with_A33_norm_strictly_between':['2^-45','2^-17'],
           'no_change_to_sampler_writer_or_operator_price':True,
           'independent_physical_rows_and_Cost_Info_selection_included':False,
           'refinement_uniform_theorem':False,
           'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},
           'physical_C_closed':False,'GR_closed':False}
    (P/'FULL_SAMPLING_SOURCE_BOUND.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','actual_corrected_finite_H_plus_J_raw_covector_norm_lt','actual_corrected_finite_covector_minus_Egeom_at_decoded_mean_norm_lt')}))


if __name__ == '__main__':
    main()
