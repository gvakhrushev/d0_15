#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact full-Lorentz fixed-curved-source V4 joint witness.

Exact Fraction arithmetic. The all-mesh proof is in the companion memo.
Finite pi rotations are outside the parent small identity chart; this
certificate does not retire that parent task or promote a public claim.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a4d_identity_quarter_nonlinear_response_check as M

I = np.eye(4, dtype=object)
ETA = np.diag(M.SIG).astype(object)
R1 = np.diag([1, 1, -1, -1]).astype(object)
R2 = np.diag([1, -1, 1, -1]).astype(object)
R3 = np.diag([1, -1, -1, 1]).astype(object)
FACE_P = {
    (0, 1): R3, (0, 2): R3, (0, 3): R2,
    (1, 2): R2, (1, 3): R3, (2, 3): R3,
}
L = 4
SITES = list(product(range(L), repeat=4))
INDEX = {x: k for k, x in enumerate(SITES)}


def inv(u):
    return ETA @ u.T @ ETA


def shift(x, role):
    y = list(x)
    y[role] = (y[role] + 1) % L
    return tuple(y)


def frame(x):
    # Exact samples of f(y)=1+(1-cos(2*pi*y))/50 at y=x_1/4.
    f = (F(1), F(51, 50), F(26, 25), F(51, 50))[x[1]]
    return np.diag([F(1), F(1), f, f]).astype(object)


def face_weights(s, r, t):
    u, v = [j for j in range(4) if j not in (r, t)]
    weight = M.orient(r, t) * M.weight(M.wedge(s[:, u], s[:, v]))
    variations = []
    for column in range(4):
        for component in range(4):
            unit = np.array([F(j == component) for j in range(4)], dtype=object)
            area = (M.wedge(unit, s[:, v]) if column == u else
                    M.wedge(s[:, u], unit) if column == v else
                    np.zeros(6, dtype=object))
            variations.append(M.orient(r, t) * M.weight(area))
    return weight, np.array(variations, dtype=object)


for face, p in FACE_P.items():
    r, t = face
    assert p[0, 0] == 1 and np.prod(np.diag(p)) == 1
    assert np.array_equal(p.T @ ETA @ p, ETA)
    assert np.array_equal(p @ p, I)
    assert p[r, r] + p[t, t] == 0
for p in (I, R1, R2, R3):
    for q in (I, R1, R2, R3):
        assert np.array_equal(p @ q, q @ p)

links = np.zeros((len(SITES), 4, 4, 4), dtype=object)
for x in SITES:
    for role in range(4):
        u = I.copy()
        for previous in range(role):
            if x[previous] % 2:
                u = u @ FACE_P[(previous, role)]
        assert np.array_equal(u.T @ ETA @ u, ETA)
        assert u[0, 0] == 1 and np.prod(np.diag(u)) == 1
        links[INDEX[x], role] = u

ek = np.zeros((len(SITES), 4, 6), dtype=object)
es = np.zeros((len(SITES), 16), dtype=object)
action = F(0)
face_count = 0
for x in SITES:
    ix = INDEX[x]
    s = frame(x)
    for r, t in M.PAIRS:
        weight, dweight = face_weights(s, r, t)
        locations = [(x, r, False), (shift(x, r), t, False),
                     (shift(x, t), r, True), (x, t, True)]
        factors = [inv(links[INDEX[y], role]) if reverse else
                   links[INDEX[y], role] for y, role, reverse in locations]
        prefix = [I]
        for factor in factors:
            prefix.append(prefix[-1] @ factor)
        suffix = [None] * 5
        suffix[4] = I
        for j in range(3, -1, -1):
            suffix[j] = factors[j] @ suffix[j + 1]
        p = prefix[4]
        assert np.array_equal(p, FACE_P[(r, t)])
        curvature = (p - inv(p)) * F(1, 2)
        assert not np.any(curvature)
        action += np.sum(weight * curvature)
        for row in range(16):
            # Literal unrestricted coframe Euler, not a Gram projection.
            es[ix, row] += np.sum(dweight[row] * curvature)
        for generator in M.G:
            face_momentum = np.sum(weight * (p @ generator + generator @ p)) * F(1, 2)
            assert face_momentum == 0
        for j, (y, role, reverse) in enumerate(locations):
            # Exact literal owner's right-trivialized shared-link derivative.
            covector = suffix[j + 1] @ weight.T @ prefix[j]
            jet = -factors[j] @ covector if reverse else covector @ factors[j]
            for a, generator in enumerate(M.G):
                derivative = np.sum(jet.T * generator)
                assert derivative == 0
                ek[INDEX[y], role, a] += derivative
        face_count += 1

assert action == 0
assert not np.any(ek)
assert not np.any(es)

# Full ten-component Gram readout reconstructed from unrestricted solder rows.
xi = np.zeros((len(SITES), 10), dtype=object)
for x in SITES:
    ix = INDEX[x]
    s = frame(x)
    solder = es[ix].reshape(4, 4).T
    for row, (r, t) in enumerate(M.SYM):
        dq = np.zeros((4, 4), dtype=object)
        dq[r, t] = dq[t, r] = F(1)
        ds = np.diag([F(M.SIG[j], 2 * s[j, j]) for j in range(4)]) @ dq
        xi[ix, row] = np.sum(solder * ds)
assert not np.any(xi)

# Hostile face: the wrong involution remains source-null but has nonzero
# face momentum, so the momentum test is not a zero-curvature tautology.
weight, _ = face_weights(frame((0, 0, 0, 0)), 0, 1)
wrong = [np.sum(weight * (R1 @ g + g @ R1)) * F(1, 2) for g in M.G]
assert any(wrong)

nonidentity = sum(not np.array_equal(u, I) for site in links for u in site)
assert nonidentity > 0
assert all(np.prod(np.diag(I + u)) == 0
           for site in links for u in site if not np.array_equal(u, I))
print('PASS_V4_PROPER_LORENTZ_FACE_INVOLUTIONS_AND_COMMUTATIVITY')
print('PASS_ALL_' + str(face_count) + '_ACTUAL_PLAQUETTES')
print('PASS_EACH_FACE_ALL_SIX_MOMENTA_AND_ALL_FOUR_LINK_VARIATIONS')
print('PASS_ALL_' + str(ek.size) + '_SHARED_LINK_EULER_ROWS')
print('PASS_ALL_' + str(es.size) + '_UNRESTRICTED_SOLDER_ROWS')
print('PASS_ALL_' + str(xi.size) + '_GRAM_METRIC_ROWS')
print('PASS_HOSTILE_WRONG_INVOLUTION_MOMENTUM_NONZERO')
print('ACTION_EXACT_ZERO; PREDECLARED_SOURCE_EXACT_ZERO')
print('NONIDENTITY_LINKS=' + str(nonidentity))
print('SCOPE: finite-pi-rotation construction; outside log-O(h) and identity Cayley chart')


# Actual node-dependent proper-Lorentz dressing, including a periodic wrap.
def gauge(x):
    t = F(x[0] + 1, 7)
    return M.inverse(I - t * M.G[0] * F(1, 2)) @ (I + t * M.G[0] * F(1, 2))

base = (L - 1, 1, 2, 3)
gbase = gauge(base)
sbase = gbase @ frame(base)
assert np.array_equal(sbase.T @ ETA @ sbase, frame(base).T @ ETA @ frame(base))
for r, t in M.PAIRS:
    spots = [(base, r, False), (shift(base, r), t, False),
             (shift(base, t), r, True), (base, t, True)]
    factors = []
    for y, role, reverse in spots:
        u = gauge(y) @ links[INDEX[y], role] @ inv(gauge(shift(y, role)))
        assert np.array_equal(u.T @ ETA @ u, ETA) and u[0, 0] > 0
        factors.append(inv(u) if reverse else u)
    p = factors[0] @ factors[1] @ factors[2] @ factors[3]
    assert np.array_equal(p, gbase @ FACE_P[(r, t)] @ inv(gbase))
    assert np.trace(p) == 0 and np.array_equal(p @ p, I)
    weight, _ = face_weights(sbase, r, t)
    for generator in M.G:
        assert np.sum(weight * (p @ generator + generator @ p)) == 0
print('PASS_ACTUAL_NODE_GAUGE_DRESSING_PERIODIC_WRAP_AND_FULL_FACE_MOMENTA')

report = {
    'schema': 'a4d-global-lorentz-fixed-source-v4-v1',
    'input_head': 'f317a3b842b2d10c5a3a381b6b03cb9850e77f66',
    'certificate_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'inputs_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                      for name in ('a4d_identity_quarter_nonlinear_response_check.py',
                                   'a4d_designated_full_gap_check.py')},
    'arithmetic': 'exact rationals; all actual face products and unrestricted derivatives',
    'geometry': 'f(y1)=1+(1-cos(2*pi*y1))/50; E=diag(1,1,f,f); g=E^T eta E',
    'source': 'one independently predeclared tau=0, exact on every mesh',
    'fluxes': {str(face): list(map(int, np.diag(p))) for face, p in FACE_P.items()},
    'links': 'U_r(x)=product_{s<r} P_sr^x_s; all matrices in proper-Lorentz V4',
    'finite_replay': {'L': L, 'sites': len(SITES), 'actual_plaquettes': face_count,
                      'shared_link_Euler_rows': ek.size, 'unrestricted_solder_rows': es.size,
                      'Gram_metric_rows': xi.size, 'nonidentity_links': nonidentity,
                      'action': '0', 'E_K': '0', 'Xi': '0'},
    'all_mesh_proof': 'even L; each individual face momentum and curvature are zero',
    'holonomy': 'trace 0; characteristic polynomial (z-1)^2*(z+1)^2; nongauge',
    'continuum_gap': 'h^4*(h^-2*||Xi-Xi_sm||_owner1) -> integral ||rho0||_packed1',
    'strict_gap_lower_bound': 'pi^2/2500 from the rho0_11 component',
    'domain': 'full finite proper-Lorentz nondegenerate configuration domain',
    'excluded_domain': 'identity Cayley and sufficiently small identity log chart; in particular log-O(h)',
    'verdict': 'FULL-LORENTZ-FIXED-CURVED-SOURCE-RESPONSE-NOGO; ORIGINAL-SMALL-CHART-TASK-OPEN',
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
parser.add_argument('--expect', type=Path)
args = parser.parse_args()
expected = args.expect or (HERE / 'a4d_global_lorentz_fixed_source_v4_results.json'
                           if args.output is None else None)
if expected is not None:
    assert json.loads(expected.read_text()) == report
    print('PASS_PINNED_LEDGER')
if args.output is not None:
    args.output.write_text(json.dumps(report, indent=2) + '\n')
print('VERDICT', report['verdict'])
