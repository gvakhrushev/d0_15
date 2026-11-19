#!/usr/bin/env python3
"""Exact nonlinear detector for the owned quarter first-slow joint reduction.

The detector kills every spatial transport column pointwise. Its radial
cubic pairing is a positive quartic role-mixing moment modulo three fast
metric coefficients. This is an identity of the reduced polynomial system,
not an exact fixed-source or varying-coframe theorem. No carrier search.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N
import a4d_identity_physical_resonance_circles_check as L
from a4d_designated_full_gap_check import QI

HERE = Path(__file__).resolve().parent
SPATIAL = (1, 2, 3, 5, 6, 7)
FAST_SLOTS = (8, 6, 5)
CP, CR = 577, 1704
SOURCE_BLOBS = {
    "a4d_identity_quarter_nonlinear_response_results.json": "481db19fe7f42daf470ed8caea3af358ea8ff91f",
    "a4d_identity_physical_resonance_circles_check.py": "f3a388d12737d8814f134f02eba4daa5c34c857d",
    "a4d_identity_quarter_nonlinear_response_check.py": "55d2268c12049e613a4cb07be7744c980a6eac97",
    "a4d_identity_physical_resonance_circles_results.json": "519187197feb9a96e7e2d0fe45a92f2ba5224bf8"
}
P_ROWS = '''
-90824/1113 -247355/1484 -932593/4452 320009/4452 -127712/1113 108861/742 -1429417/4452 80949/742 -105167/742 117637/2226 182783/742 -430712/1113 -215356/1113 0 147638/1113 -1685807/4452 -367541/1484 -316951/4452 87644/1113 0 785495/4452 0 0 -1391/7 -1139/7 -72 -36 0
-362368/5565 185866/1855 19433/1113 604468/5565 88024/1855 -39868/795 39567/1855 185508/1855 -56752/1855 746324/5565 43636/1113 352096/1855 176048/1855 0 94296/1855 -353608/5565 -127604/1113 -11248/1855 -88024/1855 -377788/5565 0 0 0 0 0 0 0 0
-920/7 449/7 -950/7 -19 0 400/7 40/7 -660/7 0 660/7 660/7 0 0 0 660/7 0 0 0 0 0 0 0 0 0 0 0 0 0
130/7 -8 4 -60/7 0 50/7 -24/7 -8/7 0 0 0 0 0 0 6 12 0 0 0 0 0 0 0 0 0 0 0 0
4 -4 -88/7 24/7 0 -24/7 0 -8/7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
'''
R_ROWS = '''
0 183865/1484 133179/1484 0 -326601/1484 -264951/1484 -89419/1113 25353/742 -286985/4452 3243/14 -733595/8904 249155/2226 -235483/4452 279155/8904 -483205/2226 0 -17003/212 -98199/1484 1289/159 -54827/2226 13975/2226
-746261/4452 -36207/1484 8947/53 0 -59389/1113 -20591/5565 0 3043/106 -43549/371 0 40756/371 22577/1113 -394103/11130 59624/1113 10496/1113 89995/4452 -4091/212 -10307/2226 0 13679/742 -7544/1113
551291/4452 1339/14 -165/28 0 44439/742 -835/14 -52400/1113 -495/14 320/53 0 -380/7 0 -2115/14 -120 0 -699/28 17 -495/28 169/7 -165/14 0
'''


def matrix(rows):
    return [[F(x) for x in row.split()] for row in rows.strip().splitlines()]


P = matrix(P_ROWS)
R = matrix(R_ROWS)
QUADRATICS = list(combinations_with_replacement(range(6), 2))


def strings(values):
    if isinstance(values, list):
        return [strings(x) for x in values]
    return str(F(values))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def matvec(a, b):
    return [dot(row, b) for row in a]


def monomial(indices, values):
    out = F(1)
    for j in indices:
        out *= values[j]
    return out


def evaluate(coefficients, values, dimension):
    out = [F(0)]*dimension
    for m, row in coefficients.items():
        v = monomial(m, values)
        out = [x+v*y for x, y in zip(out, row)]
    return out


def add(poly, indices, value):
    m = tuple(sorted(indices))
    poly[m] = poly.get(m, F(0))+value


def production(c):
    z = [c[r]**2+c[r+3]**2 for r in range(3)]
    return sum((z[r]*z[s] for r in range(3) for s in range(r+1, 3)), F(0))


def literal_gamma():
    """Actual Laurent incidence derivative, with the physical H=A^T."""
    columns, transform = N.quarter_reduction()
    b = transform[20:]
    centers = np.array([[QI() for _ in range(4)] for _ in range(24)], dtype=object)
    for r in range(4):
        for j in range(6):
            centers[6*r+j, r] = QI.of(int(N.TC[r, j]))
    j0 = L.literal_joint([QI(0, 1)]*4)
    assert columns == [j for j in range(24) if j not in (5, 11, 16, 21)]
    assert not np.any(j0@centers)
    assert not np.any(b@j0)
    wrong = L.joint([QI(0, 1)]*4, wrong=True)
    assert np.any(b@wrong)
    powers = (QI.of(1), QI(0, 1), QI.of(-1), QI(0, -1))
    output = []
    for mu in range(4):
        dj = np.array([[QI() for _ in range(24)] for _ in range(34)], dtype=object)
        for offset, terms in ((0, L.H_LITERAL), (24, L.C_LITERAL)):
            for shift, entries in terms.items():
                phase = powers[sum(shift) % 4]
                for (r, c), value in entries.items():
                    dj[offset+r, c] += QI(0, shift[mu])*phase*value
        g = b@dj@centers
        real = [[F(0)]*8 for _ in range(28)]
        for o in range(14):
            for j in range(4):
                real[o][j] = F(g[o, j].im)/2
                real[o][j+4] = -F(g[o, j].re)/2
                real[o+14][j] = -F(g[o, j].re)/2
                real[o+14][j+4] = -F(g[o, j].im)/2
        output.append(real)
    return output


def owned_coefficients():
    for name, sha in SOURCE_BLOBS.items():
        data = (HERE/name).read_bytes()
        git_blob = b'blob '+str(len(data)).encode('ascii')+b'\0'+data
        assert hashlib.sha1(git_blob).hexdigest() == sha, ('owner pin changed', name)
    data = json.loads((HERE/'a4d_identity_quarter_nonlinear_response_results.json').read_text())
    q2 = {tuple(m): [F(x) for x in row]
          for m, row in zip(data['quadratic_monomials'], data['quadratic_gate_coefficients'])}
    q3 = {tuple(m): [F(x) for x in row]
          for m, row in zip(data['cubic_monomials'], data['cubic_gate_coefficients'])}
    assert len(q2) == 36 and len(q3) == 120
    return q2, q3


def restrict(coefficients):
    return {tuple(SPATIAL.index(j) for j in m): row
            for m, row in coefficients.items() if all(j in SPATIAL for j in m)}


def derivative(coefficients, axis, dimension):
    out = [[F(0)]*6 for _ in range(dimension)]
    for m, row in coefficients.items():
        for k, j in enumerate(m):
            if all(x == axis for x in m[:k]+m[k+1:]):
                for o, v in enumerate(row):
                    out[o][j] += v
    return out


def polynomial_checks(q2, q3, gamma):
    quadratic, cubic = restrict(q2), restrict(q3)
    lhs, rhs = {}, {}
    for m, row in cubic.items():
        for i in range(6):
            add(lhs, (*m, i), dot(P[i], row))
    for r in range(3):
        for s in range(r+1, 3):
            for i in (r, r+3):
                for j in (s, s+3):
                    add(rhs, (i, i, j, j), 1)
    for r in range(3):
        for k, m in enumerate(QUADRATICS):
            add(rhs, (r, r+3, *m), R[r][k])
    for m in combinations_with_replacement(range(6), 4):
        assert lhs.get(m, 0) == rhs.get(m, 0), ('quartic coefficient', m)
    for mu in range(4):
        for i in range(6):
            for j in SPATIAL:
                assert dot(P[i], [row[j] for row in gamma[mu]]) == 0
    for m, row in quadratic.items():
        for r, slot in enumerate(FAST_SLOTS):
            assert row[slot] == int(m == (r, r+3))
    detector = {m: matvec(P, row) for m, row in cubic.items()}
    ranks = []
    for axis in range(6):
        d2 = derivative(quadratic, axis, 10)
        d3 = derivative(detector, axis, 6)
        rank = len(N.row_reduce([d2[j] for j in FAST_SLOTS]+d3))
        assert rank == 5
        unit = [F(int(j == axis)) for j in range(6)]
        assert not any(evaluate(quadratic, unit, 10))
        assert not any(evaluate(detector, unit, 6))
        ranks.append(rank)
    cp = max(sum(abs(P[i][o]) for i in range(6)) for o in range(28))
    cr = max(sum(abs(x) for x in row) for row in R)
    assert cp <= CP and cr <= CR
    # Removing one detector coefficient must destroy the polynomial identity.
    altered = dict(lhs)
    for m, row in cubic.items():
        add(altered, (*m, 0), -P[0][0]*row[0])
    assert any(altered.get(m, 0) != rhs.get(m, 0)
               for m in combinations_with_replacement(range(6), 4))
    dense = [F(j+1, 11) for j in range(6)]
    missing_fast_terms = dot(dense, matvec(P, evaluate(cubic, dense, 28)))-production(dense)
    assert missing_fast_terms
    return quadratic, cubic, ranks, cp, cr, missing_fast_terms


def temporal_checks(q2, q3, gamma):
    transfer = [[[dot(row, [g[o][j] for o in range(28)]) for j in (0, 4)]
                 for row in P] for g in gamma]
    nonzero = [sum(bool(x) for row in g for x in row) for g in transfer]
    assert nonzero == [10]*4
    transport_bound = max(sum(abs(row[j]) for row in g)
                          for g in transfer for j in range(2))
    assert transport_bound == F(304751, 1113) and transport_bound <= 274
    radial = {}
    for m, row in q3.items():
        for i, j in enumerate(SPATIAL):
            add(radial, (*m, j), dot(P[i], row))
    temporal = {m: v for m, v in radial.items()
                if v and (0 in m or 4 in m)}
    assert len(temporal) == 179
    assert all(any(j in SPATIAL for j in m) for m in temporal)
    bound = sum(abs(v) for v in temporal.values())
    assert bound == F(43759468, 5565) and bound <= 7864
    fast_remainders = []
    for r, slot in enumerate(FAST_SLOTS):
        remainder = {m: row[slot]-int(m == (SPATIAL[r], SPATIAL[r+3]))
                     for m, row in q2.items()}
        remainder = {m: v for m, v in remainder.items() if v}
        assert len(remainder) == 5
        assert all((0 in m or 4 in m) and abs(v) == 1
                   for m, v in remainder.items())
        fast_remainders.append({','.join(map(str, m)): str(v)
                                for m, v in sorted(remainder.items())})
    return transfer, nonzero, transport_bound, bound, fast_remainders


def grid_check(cubic, gamma):
    shape = (4, 4, 4, 4)
    sites = list(product(range(4), repeat=4))
    fields = {x: [F(((j+2)*(x[0]+2*x[1]+3*x[2]+5*x[3])
                     +j*j+x[1]*x[2]) % 13-6, 19+j) for j in range(6)]
              for x in sites}
    rho = max(abs(v) for c in fields.values() for v in c)
    moment = residual_norm = fast_norm = F(0)
    for x in sites:
        c = fields[x]
        cubic_value = evaluate(cubic, c, 28)
        residual = cubic_value[:]
        for mu in range(4):
            y = list(x)
            y[mu] = (y[mu]+1) % 4
            difference = [a-b for a, b in zip(fields[tuple(y)], c)]
            term = [dot([row[j] for j in SPATIAL], difference)
                    for row in gamma[mu]]
            residual = [a+b for a, b in zip(residual, term)]
        assert matvec(P, residual) == matvec(P, cubic_value)
        fast = [c[r]*c[r+3] for r in range(3)]
        multipliers = [dot(row, [monomial(m, c) for m in QUADRATICS]) for row in R]
        d = production(c)
        assert dot(c, matvec(P, residual)) == d+dot(fast, multipliers)
        moment += d
        residual_norm += sum(abs(v) for v in residual)
        fast_norm += sum(abs(v) for v in fast)
    bound = CP*rho*residual_norm+CR*rho*rho*fast_norm
    assert moment <= bound
    return {'shape': list(shape), 'sites': len(sites), 'rho': str(rho),
            'production': str(moment), 'joint_residual_raw1': str(residual_norm),
            'fast_products_raw1': str(fast_norm), 'bound': str(bound)}


def run_checks():
    q2, q3 = owned_coefficients()
    gamma = literal_gamma()
    quadratic, cubic, ranks, cp, cr, hostile = polynomial_checks(q2, q3, gamma)
    transfer, nonzero, cb, ct, remainders = temporal_checks(q2, q3, gamma)
    grid = grid_check(cubic, gamma)
    assert grid['production'] == '257516831499439/86957199436800'
    assert grid['joint_residual_raw1'] == '33918176162409107/52174319662080'
    assert grid['fast_products_raw1'] == '71552263/4037880'
    assert grid['bound'] == '20068288694031777107/165218678929920'
    print('PASS_LITERAL_FIRST_SLOW_SPATIAL_CANCELLATION_144', flush=True)
    print('PASS_QUARTIC_PRODUCTION_126_AND_SIX_AXIS_RANKS', flush=True)
    print('PASS_RAW_256_SITE_BALANCE_AND_HOSTILE_CONTROLS', flush=True)
    return {
        'arithmetic': 'exact Q and Q(i); NumPy object arrays; no floats',
        'model': 'owned identity quarter center and quadratic normal graph; cubic first-slow reduction',
        'source_blobs': SOURCE_BLOBS,
        'full_amplitude_order': ['a0', 'a1', 'a2', 'a3', 'b0', 'b1', 'b2', 'b3'],
        'spatial_amplitude_order': ['a1', 'a2', 'a3', 'b1', 'b2', 'b3'],
        'fast_metric_packed_slots': ['23', '13', '12'],
        'fast_metric_slot_indices': list(FAST_SLOTS),
        'detector_P': strings(P),
        'quadratic_multiplier_monomials': [list(m) for m in QUADRATICS],
        'fast_metric_multipliers_R': strings(R),
        'first_slow_full_gamma': strings(gamma),
        'quartic_coefficients_checked': 126,
        'spatial_transport_entries_zero': 144,
        'axis_derivative_ranks': ranks,
        'raw_C_P_exact': str(cp), 'raw_C_R_exact': str(cr),
        'raw_C_P': CP, 'raw_C_R': CR,
        'temporal_transfer': strings(transfer),
        'temporal_transfer_nonzero_entries': nonzero,
        'temporal_transport_column_bound': str(cb),
        'raw_C_temporal_transport': 274,
        'temporal_radial_quartic_nonzero_monomials': 179,
        'temporal_radial_quartic_coefficient_sum': str(ct),
        'raw_C_temporal_quartic': 7864,
        'fast_metric_temporal_remainders': remainders,
        'grid': grid,
        'hostile_omit_fast_terms_nonzero': str(hostile),
        'hostile_detector_coefficient_mutation_rejected': True,
        'hostile_wrong_euler_placement_rejected': True,
        'verdict': 'SPATIAL-REDUCED-TRANSPORT-ENTROPY-CERTIFIED',
        'nonclaims': [
            'No identification of the reduced residual with the exact full-link source image.',
            'No arbitrary-envelope spectral separation or remainder bound is inferred.',
            'The temporal carrier and varying-coframe transport are retained as uncontrolled terms.',
            'No fixed-source parent theorem, NO-GO, retirement, or promotion.'
        ]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-json', action='store_true')
    args = parser.parse_args()
    result = run_checks()
    path = Path(__file__).with_name('a4d_spatial_transport_entropy_results.json')
    if args.write_json:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert json.loads(path.read_text()) == result, 'pinned result ledger changed'
    print('PASS_PINNED_SPATIAL_TRANSPORT_ENTROPY_LEDGER')
