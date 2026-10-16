#!/usr/bin/env python3
"""Literal full-row cofactor currents for the temporal Y seed.

Exact rational inputs for A4D_NULL_SHEAR_FIXED_SOURCE_EXISTENCE_AUDIT.md.
This does not exclude unrestricted fixed-source joint roots. The curved-warp
hostile has identically zero metric response but nonzero connection Euler rows.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import sys
import numpy as np

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--repo', type=Path)
ap.add_argument('--output', type=Path)
ap.add_argument('--expect', type=Path, default=Path(__file__).with_name(
    'a4d_y_temporal_cofactor_current_results.json'))
args = ap.parse_args()
repo = args.repo or next((p for p in Path(__file__).resolve().parents
                         if (p / 'AGENTS.md').is_file()), None)
if repo is None:
    ap.error('Cannot locate the D0 repository; supply --repo')
cert = repo.resolve() / '02_REGISTRY/research/certificates'
owner_hashes = {
    'a4d_identity_quarter_nonlinear_response_check.py':
    'f930d5d674b62f0c500b1aa1e28c1b3076a900899767d13b2dd2cd6a59142865',
    'a4d_designated_full_gap_check.py':
    'fb76349e723ff532ef9b2222fd07cef5d7fa3e7e2b5d2c94b01ad4b056b8885d',
}
for name, expected in owner_hashes.items():
    actual = hashlib.sha256((cert / name).read_bytes()).hexdigest()
    assert actual == expected, f'Input owner drift: {name}: {actual}'
sys.path.insert(0, str(cert))
import a4d_identity_quarter_nonlinear_response_check as N

I = N.I
ETA = np.diag(N.SIG).astype(object)
Y = N.G[3] - N.G[4] + N.G[5]
PAX = np.full((3, 3), F(1, 3), dtype=object)
PPER = np.eye(3, dtype=object) - PAX


def det3(m):
    return (m[0, 0] * (m[1, 1] * m[2, 2] - m[1, 2] * m[2, 1])
            - m[0, 1] * (m[1, 0] * m[2, 2] - m[1, 2] * m[2, 0])
            + m[0, 2] * (m[1, 0] * m[2, 1] - m[1, 1] * m[2, 0]))


def cofactor(m):
    d = det3(m)
    assert d != 0
    return d * N.inverse(m).T


def rotation(a):
    out = N.inverse(I - a * Y * F(1, 2)) @ (I + a * Y * F(1, 2))
    assert np.array_equal(out.T @ ETA @ out, ETA)
    assert np.array_equal(out[1:, 1:] @ PAX, PAX)
    return out


def weights(solder):
    q = solder.T @ ETA @ solder
    qi = N.inverse(q)
    w = []
    dw = []
    for r, s in N.PAIRS:
        a, b = [j for j in range(4) if j not in (r, s)]
        w.append(N.orient(r, s) * N.weight(N.wedge(solder[:, a], solder[:, b])))
        rows = []
        for i, j in N.SYM:
            dq = np.zeros((4, 4), dtype=object)
            dq[i, j] = dq[j, i] = 1
            ds = solder @ qi @ dq * F(1, 2)
            assert np.array_equal(ds.T @ ETA @ solder + solder.T @ ETA @ ds, dq)
            rows.append(N.orient(r, s) * N.weight(
                N.wedge(ds[:, a], solder[:, b]) + N.wedge(solder[:, a], ds[:, b])))
        dw.append(rows)
    c = cofactor(solder[1:, 1:])
    for i in (1, 2, 3):
        face = N.PAIRS.index((0, i))
        assert np.array_equal(w[face][0, 1:], c[:, i - 1] * F(1, 2))
        assert np.array_equal(w[face][1:, 0], c[:, i - 1] * F(1, 2))
    return w, dw


def evaluate(matrices, amplitudes):
    length = len(matrices)
    assert length == len(amplitudes)
    solders = []
    for m in matrices:
        ss = I.copy()
        ss[1:, 1:] = m
        solders.append(ss)
    data = [weights(s) for s in solders]
    rotations = [rotation(a) for a in amplitudes]
    phase_links = [[r, I, ETA @ r.T @ ETA, I] for r in rotations]
    ek = np.zeros((length, 4, 4, 6), dtype=object)
    xi = np.zeros((length, 4, 10), dtype=object)
    for n in range(length):
        ww, ddw = data[n]
        for p in range(4):
            for face, (r, s) in enumerate(N.PAIRS):
                loc = [(n, p, r, False),
                       ((n + (r == 0)) % length, (p + 1) % 4, s, False),
                       ((n + (s == 0)) % length, (p + 1) % 4, r, True),
                       (n, p, s, True)]
                factors = []
                for site, phase, role, inv in loc:
                    aa = phase_links[site][phase] if role == 0 else I
                    factors.append(ETA @ aa.T @ ETA if inv else aa)
                prefix = [I]
                for aa in factors:
                    prefix.append(prefix[-1] @ aa)
                suffix = [None] * 5
                suffix[4] = I
                for i in range(3, -1, -1):
                    suffix[i] = factors[i] @ suffix[i + 1]
                for j in range(10):
                    xi[n, p, j] += np.sum(ddw[face][j] * prefix[4])
                for i, (nn, pp, rr, inv) in enumerate(loc):
                    covector = suffix[i + 1] @ ww[face].T @ prefix[i]
                    jet = -factors[i] @ covector if inv else covector @ factors[i]
                    for g in range(6):
                        ek[nn, pp, rr, g] += np.sum(jet.T * N.G[g])
    for n in range(length):
        old = (n - 1) % length
        cc = cofactor(matrices[n])
        cp = cofactor(matrices[old])
        rr = rotations[n][1:, 1:]
        rp = rotations[old][1:, 1:]
        eye = np.eye(3, dtype=object)
        jp = (eye + rr) @ cc
        jm = (eye + rr.T) @ cc
        assert np.array_equal(jm, rr.T @ jp)
        assert np.array_equal(jp @ N.inverse(jm), rr)
        assert np.array_equal(N.inverse(eye + rr) @ jp, cc)
        assert det3(cc) == det3(matrices[n]) ** 2
        assert np.array_equal(det3(matrices[n]) * N.inverse(cc).T, matrices[n])
        for p in range(4):
            rn = rr.T if p < 2 else rr
            ro = rp.T if p < 2 else rp
            predicted = ((eye + ro) @ cp - (eye + rn) @ cc) * F(1, 2)
            for i in (1, 2, 3):
                for g in range(3):
                    assert ek[n, p, i, g] == predicted[g, i - 1]
                assert not np.any(ek[n, p, i, 3:])
    return ek, xi


def packed(a):
    return [[[str(F(v)) for v in row] for row in stage] for stage in a]


def case(name, matrices, amplitudes, stationary, source_null):
    ek, xi = evaluate(matrices, amplitudes)
    assert (not np.any(ek)) == stationary
    assert (not np.any(xi)) == source_null
    return {'name': name, 'spatial_matrices': [[[str(F(v)) for v in row] for row in m] for m in matrices],
            'cayley_parameters': [str(a) for a in amplitudes],
            'full_connection_Euler_24': packed(ek.reshape(len(matrices), 4, 24)),
            'raw_Gram_response_10': packed(xi),
            'connection_nonzero_count': int(np.count_nonzero(ek)),
            'response_nonzero_count': int(np.count_nonzero(xi))}


def calculate():
    plane = lambda f: PAX + f * PPER
    m1 = np.array([[F(6, 5), F(1, 7), 0], [0, F(4, 5), F(1, 9)],
                   [F(1, 11), 0, F(7, 6)]], dtype=object)
    m2 = np.array([[F(5, 4), 0, F(1, 13)], [F(1, 8), F(6, 5), 0],
                   [0, F(1, 10), F(8, 7)]], dtype=object)
    rows = [case('constant_identity_spatial_solder', [plane(F(1))], [F(1, 10)], True, True),
            case('constant_nonidentity_transverse_factor', [plane(F(2))], [F(1, 10)], True, True),
            case('source_null_varying_transverse_factor_hostile', [plane(F(1)), plane(F(2))],
                 [F(1, 10), F(1, 10)], False, True),
            case('varying_factor_and_angle_hostile', [plane(F(1)), plane(F(2))],
                 [F(1, 10), F(1, 7)], False, True),
            case('varying_angle_only_hostile', [plane(F(1)), plane(F(1)), plane(F(1))],
                 [F(1, 10), F(1, 7), F(1, 11)], False, True),
            case('arbitrary_nonsymmetric_cofactor_identity', [m1, m2],
                 [F(1, 10), F(1, 7)], False, False)]
    assert rows[2]['full_connection_Euler_24'][0][0][6] == '2009/1209'
    return {'schema': 'a4d-temporal-y-cofactor-current/1',
            'input_commit': 'f4f88161325574e4c5750e0af4a8cc14a2f4b48e',
            'input_owner_sha256': owner_hashes,
            'arithmetic': 'exact rational literal 4x4 matrices; all 24 connection and 10 raw Gram rows retained',
            'theorem_scope': 'temporal-only block-spatial solder and role0 phases (R,I,Rinverse,I)',
            'current': 'E_i_boost=1/2*(Jsign(n-1)-Jsign(n))*e_i; Jsign=(I+Rsign)*cof(M)',
            'algebra': 'Jminus=Rinverse*Jplus; R=Jplus*JminusInverse; C=(I+R)Inverse*Jplus',
            'positive_orientation_recovery': 'det C=(det M)^2; M=det(M)*CinverseTranspose',
            'parent_terminal': 'OPEN; no unrestricted fixed-source existence or nonexistence conclusion',
            'cases': rows}


def main():
    result = calculate()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert json.loads(args.expect.read_text()) == result, 'pinned result mismatch'
    print('PASS_LITERAL_ALL24_CONNECTION_ALL10_RESPONSE_ROWS')
    print('PASS_ARBITRARY_COFACTOR_OPPOSITE_PHASE_CURRENT_IDENTITY')
    print('PASS_NONDEGENERATE_CURRENT_RECOVERY_AND_CURVED_WARP_HOSTILE')
    print('PARENT_FIXED_SOURCE_TERMINAL_OPEN')


if __name__ == '__main__':
    main()
