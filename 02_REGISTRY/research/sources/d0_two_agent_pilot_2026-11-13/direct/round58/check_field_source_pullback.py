#!/usr/bin/env python3
"""Exact finite checks of all spectators, ordering and source transpose."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import islice
import json
import math
import sys
import sympy as sp

sys.dont_write_bytecode = True
import field_source_pullback as p

P = Path(__file__).resolve().parent
Q = p.mg.e.Q4


def digit(index, axis, m):
    return ((index >> axis) & 1)+2*((index >> (m+axis)) & 1)


def exact_all_spectators():
    phi, _, weights = p.mg.mg2()
    X = [[Q() for _ in range(4)] for _ in range(4)]
    for (a, b), weight in weights.items():
        X[a][b] = -weight
        X[b][a] = weight
    evidence = []
    for m in range(1, 5):
        dim = 1 << (2*m)
        state = []
        for k in range(dim):
            value = Q(1)
            for j in range(m):
                value *= phi[digit(k, j, m)]
            state.append(value)
        assert sum((z*z for z in state), Q()) == 1
        for axis in range(m):
            terms = list(p.plane_terms(axis, m))
            assert len(terms) == 6*(1 << (2*m-2))
            assert len({t.pair for t in terms}) == len(terms)
            actual = {}
            for term in terms:
                a, b = term.pair
                actual[a, b] = -term.coefficient
                actual[b, a] = term.coefficient
            # Independent tensor definition: coordinates other than axis
            # are preserved, not projected to a prepared spectator state.
            mask = ((1 << (2*m))-1) ^ ((1 << axis) | (1 << (m+axis)))
            expected = {}
            for a in range(dim):
                for local in range(4):
                    b = (a & mask) | ((local & 1) << axis) | ((local >> 1) << (m+axis))
                    value = X[digit(a, axis, m)][local]
                    if value != 0:
                        expected[a, b] = value
            assert actual == expected
            # Full vector commutator identity on every coordinate.
            for target_axis in range(m):
                out = [Q() for _ in range(dim)]
                for (a, b), value in actual.items():
                    out[a] += (digit(a, target_axis, m)-digit(b, target_axis, m))*value*state[b]
                assert out == (state if axis == target_axis else [Q()]*dim)
            # A generic rational test covector; exact independent Frobenius
            # evaluation establishes orientation and factor, not physics.
            def row(a, b):
                return F((a+2)*(b+7) % 101-50, 137)
            got = p.bounded_raw_row(row, axis, m)
            want = sum((value*row(b, a) for (a, b), value in expected.items() if a > b), Q())
            assert got == want
        evidence.append({'coordinates': m, 'full_columns': dim,
                         'axes': m, 'all_spectators_and_vector_commutators': True})
    return evidence


def production_addresses():
    source = p.family.prior.source
    sam = tuple(source.physical_wire(q) for q in source.namespace()['layout']['SAM'])
    assert len(sam) == 2*p.M
    tested = []
    for axis in (0, 1, p.M//2, p.M-1):
        assert (sam[axis], sam[p.M+axis]) == p.mg.code_wires(axis)
        for spectator in (0, 1, (1 << (2*p.M-2))-1):
            base = p.embed_spectator(spectator, axis)
            for local in range(4):
                index = p.local_index(base, local, axis)
                assert digit(index, axis, p.M) == local
                # Removing two positions independently recovers the index.
                compressed = 0
                outbit = 0
                for bit in range(2*p.M):
                    if bit in (axis, p.M+axis):
                        continue
                    compressed |= ((index >> bit) & 1) << outbit
                    outbit += 1
                assert compressed == spectator
        for _, plus, minus in islice(p.signed_requests(p.family.FieldCentre(), axis), 6):
            assert plus.label.arm == minus.label.arm == 'Pf'
            assert plus.label.sign == 1 and minus.label.sign == -1
            assert plus.label.plane == minus.label.plane
            assert p.family.Request.decode(plus.encode()) == plus
            assert p.family.Request.decode(minus.encode()) == minus
        tested.append(axis)
    try:
        p.bounded_raw_row(lambda a,b: F(0), 0)
    except ValueError:
        pass
    else:
        raise AssertionError('production sum ran without sufficient declared budget')
    return {'tested_actual_CODE_axes': tested, 'all_low_then_all_high_verified': True,
            'signed_A57_request_roundtrips': 48, 'production_exponential_sum_refused': True}


def exact_transpose():
    # Deliberately includes a nontrivial kernel: forward pullback does not
    # quietly promote a finite holonomy chart to all continuum variations.
    matrix = [[F(1), F(2), F(0)], [F(3), F(-1), F(0)]]
    covector = [F(7, 13), F(-5, 11)]
    physical = p.pullback(covector, matrix)
    assert physical[2] == 0
    for tangent in ([F(2), F(-3), F(19)], [F(0), F(0), F(1)]):
        raw = [sum((a*b for a,b in zip(row,tangent)), F()) for row in matrix]
        assert sum((a*b for a,b in zip(covector,raw)), F()) == sum((a*b for a,b in zip(physical,tangent)), F())
    assert p.norm_budget(F(49,45)) == F(49,45*(1 << 34))
    assert p.M < 52**2
    return {'exact_pairing': True, 'kernel_not_implicitly_inverted': True,
            'original_Vh_numeric_normalization_inferred': False}


def smooth_link_kernel():
    # A diagnostic for why finite link-coordinate invertibility alone
    # cannot invert all C2 connection fields. This is not an assertion
    # about the actual Einstein covector on an admitted physical kernel.
    t = sp.Symbol('t', real=True)
    q = t**3*(1-t)**3*(2*t-1)
    assert all(sp.diff(q,t,k).subs(t,a) == 0 for k in range(3) for a in (0,1))
    assert sp.integrate(q,(t,0,1)) == 0
    weighted = sp.integrate(t*q,(t,0,1))
    assert weighted != 0
    # For a fixed generator G, all q(t)G commute, so the exact holonomy
    # exp(epsilon G int(q)) is I for every epsilon, not only to first order.
    return {'nonzero_C2_zero_extension': str(sp.expand(q)),
            'ordinary_integral': '0', 'weighted_integral': str(weighted),
            'commuting_identity_background_holonomy_unchanged': True,
            'actual_Einstein_source_nonzero_on_kernel_proved': False}


def same_field_point_and_consumer():
    import numpy as np
    partner = p.family.O/'round114'
    sys.path.insert(0,str(partner))
    import physical_chart_l4 as chart
    offsets = tuple(F(((-1)**i)*(i+1),1 << 48) for i in range(p.M))
    field = p.family.FieldCentre(offsets)
    zero = p.bound_chart_point(p.family.FieldCentre(),128)
    point = p.bound_chart_point(field,128)
    fine = p.bound_chart_point(field,192)
    assert point['field_sha256'] == sha256(field.encode()).hexdigest()
    coords = p.family.prior.source.t.COORD
    pairs = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
    index_by_site = {pt['site']:i for i,pt in enumerate(point['sites'])}
    for j,coordinate in enumerate(coords):
        site_index = index_by_site[tuple(coordinate['site'])]
        pt,base = point['sites'][site_index],zero['sites'][site_index]
        if coordinate['kind'] == 'coframe':
            a,r = coordinate['component'],coordinate['role']
            shift = offsets[j]*(1 << 128)
            assert shift.denominator == 1
            assert pt['u_intervals'][a][r] == tuple(v+int(shift) for v in base['u_intervals'][a][r])
        elif coordinate['kind'] == 'proper_link':
            r,k = coordinate['role'],pairs.index(tuple(coordinate['generator']))
            assert pt['theta'][r][k] == offsets[j]
        else:
            assert coordinate['kind'] == 'matter' # derivative is the identity
    for coarse,finer in zip(point['sites'],fine['sites']):
        assert coarse['site'] == finer['site']
        for a in range(4):
            for r in range(4):
                lo,hi = coarse['u_intervals'][a][r]
                fl,fh = finer['u_intervals'][a][r]
                assert (lo << 64) <= fl <= fh <= (hi << 64)
    # Actual bound centre, illustrative cotangent only. No numerical price
    # or error certificate is inferred from the floating transpose check.
    u = [np.array([[(lo+hi)/(2*(1 << 128)) for lo,hi in row]
                   for row in pt['u_intervals']]) for pt in point['sites']]
    theta = [np.array(pt['theta'],float) for pt in point['sites']]
    rng = np.random.default_rng(58)
    dE = rng.normal(size=(64,4,4));wJ = rng.normal(size=(64,4,6));dpsi = rng.normal(size=(64,2))
    raw = chart.iota_l4(u,theta,dE,wJ,dpsi)
    covector = rng.normal(size=p.M)
    back = chart.pullback_l4(u,theta,covector)
    pairing = sum(np.sum(a*dE[i])+np.sum(b*wJ[i])+c@dpsi[i]
                  for i,(a,b,c) in enumerate(back))
    assert np.all(np.isfinite(raw)) and np.all(np.isfinite(covector)) and math.isfinite(pairing)
    raw_pairing = math.fsum(float(a)*float(b) for a,b in zip(covector,raw))
    assert abs(raw_pairing-pairing) < 1e-10
    try:
        p.bounded_raw_row(lambda a,b: 0.1,0,1)
    except TypeError:
        pass
    else:
        raise AssertionError('float price silently accepted as exact Q4 diagnostic')
    return {'actual_A53_field_bound_sites':64,'all_2688_offset_roles_checked':True,
            'outward_precisions_nested':[128,192],
            'actual_bound_centre_B114_full_2688_transpose_diagnostic':True,
            'rounded_B21_export_used_as_exact_source':False,
            'numerical_pairing_is_price_or_interval_certificate':False}


def main():
    plan = p.plan()
    result = {'status': 'PASS_EXACT_MG2_PLANE_READOUT_AND_FORWARD_PULLBACK',
              'tensor_checks': exact_all_spectators(),
              'production_order': production_addresses(),
              'transpose_and_norm': exact_transpose(),
              'general_connection_kernel_diagnostic': smooth_link_kernel(),
              'same_field_binding': same_field_point_and_consumer(),
              'physical_C_closed': False, 'GR_closed': False}
    paths = [Path(__file__), P/'field_source_pullback.py',
             p.D/'round47/full_vector_controls.py',
             p.D/'round47/FULL_VECTOR_CONTROL_CHECK.json',
             p.D/'round48/two_bit_global_source.py',
             p.D/'round53/regular_field_targets.py', p.D/'round20/coframe_targets.py',
             p.D/'round57/full_plane_family.py', p.D/'round57/RESULT.json',
             p.family.O/'round114/physical_chart_l4.py',
             p.family.O/'round114/check_physical_chart.py',
             p.family.O/'round114/B114_PHYSICAL_CHART_CHECK.json',
             p.family.O/'round114/B114_PHYSICAL_CHART_PULLBACK_RU.md']
    for receipt in (p.D/'round47/FULL_VECTOR_CONTROL_CHECK.json',
                    p.D/'round57/FULL_PLANE_FAMILY_PLAN.json'):
        for name, digest in json.loads(receipt.read_text())['source_sha256'].items():
            assert sha256(Path(name).read_bytes()).hexdigest() == digest
    result['input_sha256'] = {str(path): sha256(path.read_bytes()).hexdigest() for path in paths}
    (P/'FIELD_SOURCE_PULLBACK_PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
    (P/'FIELD_SOURCE_PULLBACK_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
