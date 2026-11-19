#!/usr/bin/env python3
"""Exact scoped source/conormal controls; no original A4D terminal.

Default mode recomputes and compares the immutable adjacent JSON ledger.
--output writes a new candidate ledger explicitly. --repo selects any checkout
with the pinned literal finite action owners. NumPy indexes Fraction matrices;
no floating calculation, SVD, fitting or finite-difference decisions occur.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys
import numpy as np

INPUT_HEAD = 'f4f88161325574e4c5750e0af4a8cc14a2f4b48e'
CERT = Path('02_REGISTRY/research/certificates')
INPUTS = [
    str(CERT / 'a4d_identity_quarter_nonlinear_response_check.py'),
    str(CERT / 'a4d_designated_full_gap_check.py'),
    '02_REGISTRY/research/MEMO_A4D_JOINT_PALATINI_LOCAL_UNIQUENESS.md',
    '00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md',
]


def find_repo(arg):
    if arg is not None:
        return arg.resolve()
    for candidate in [Path.cwd(), *Path(__file__).resolve().parents]:
        if (candidate / INPUTS[0]).is_file():
            return candidate
    raise RuntimeError('Pass --repo with the D0 checkout path')


def hashes(repo):
    return {p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in INPUTS}


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    r = 0
    for j in range(len(a[0])):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        z = a[r][j]
        a[r] = [x / z for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                z = a[i][j]
                a[i] = [x-z*y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def packed(matrix):
    a = np.asarray(matrix, dtype=object)
    if a.ndim == 1:
        return [str(F(x)) for x in a]
    return [packed(row) for row in a]


def exact_y_control(N, t):
    eta = np.diag(N.SIG).astype(object)
    eye = N.I
    y = N.G[3]-N.G[4]+N.G[5]
    assert np.array_equal(y.T @ eta + eta @ y, np.zeros((4, 4), dtype=object))
    assert np.array_equal(y @ y @ y, -3*y)
    u = N.inverse(eye-t*y*F(1, 2)) @ (eye+t*y*F(1, 2))
    ui = eta @ u.T @ eta
    assert np.array_equal(u.T @ eta @ u, eta)
    assert np.array_equal(ui @ u, eye)
    links = np.array([[eye.copy() for _ in range(4)] for _ in range(4)], dtype=object)
    links[0, 0] = u
    links[2, 0] = ui
    jetlinks = np.zeros((4, 4, 1, 4, 4), dtype=object)
    jetlinks[:, :, 0] = links
    owned_ek, owned_xi = N.euler_links(jetlinks)
    assert not np.any(owned_ek) and not np.any(owned_xi)

    lifts = []
    for r, s in N.SYM:
        dq = np.zeros((4, 4), dtype=object)
        dq[r, s] = dq[s, r] = 1
        ds = eta @ dq * F(1, 2)
        assert np.array_equal(ds.T @ eta+eta @ ds, dq)
        lifts.append(ds)
    lifts = np.array(lifts, dtype=object)
    ek = np.zeros((4, 4, 6), dtype=object)
    xi = np.zeros((4, 10), dtype=object)
    solder = np.zeros((4, 16), dtype=object)
    b = np.zeros((4, 10, 10), dtype=object)
    normalized = np.zeros((10, 10), dtype=object)
    odd_pairing_count = 0

    def pair(weight, p, pi):
        nonlocal odd_pairing_count
        # This pins why using P in the owned Euler code agrees with the
        # literal odd curvature (P-P^-1)/2 on the Lorentz manifold.
        assert np.array_equal(eta @ weight.T @ eta, -weight)
        direct = np.sum(weight*p)
        assert np.sum(weight*(p-pi)*F(1, 2)) == direct
        odd_pairing_count += 1
        return direct

    for phase in range(4):
        for face, (r, s) in enumerate(N.PAIRS):
            a, c = [j for j in range(4) if j not in (r, s)]
            loc = [(phase, r, False), ((phase+1) % 4, s, False),
                   ((phase+1) % 4, r, True), (phase, s, True)]
            factors = [eta @ links[ph, role].T @ eta if inv else links[ph, role]
                       for ph, role, inv in loc]
            prefix = [eye]
            for z in factors:
                prefix.append(prefix[-1] @ z)
            suffix = [None]*5
            suffix[4] = eye
            for i in range(3, -1, -1):
                suffix[i] = factors[i] @ suffix[i+1]
            p = prefix[4]
            pi = eta @ p.T @ eta
            curvature = (p-pi)*F(1, 2)
            assert np.array_equal(p.T @ eta @ p, eta)
            pair(N.WEIGHT[face], p, pi)
            for i in range(10):
                xi[phase, i] += pair(N.DWEIGHT[face][i], p, pi)
            for row in range(4):
                for col in (a, c):
                    ds = np.zeros((4, 4), dtype=object)
                    ds[row, col] = 1
                    weight = N.orient(r, s)*N.weight(
                        N.wedge(ds[:, a], eye[:, c])+N.wedge(eye[:, a], ds[:, c]))
                    solder[phase, 4*row+col] += pair(weight, p, pi)
            for i in range(10):
                for j in range(10):
                    weight = N.orient(r, s)*N.weight(
                        N.wedge(lifts[i, :, a], lifts[j, :, c])
                        +N.wedge(lifts[j, :, a], lifts[i, :, c]))
                    b[phase, i, j] += pair(weight, p, pi)
                    if phase == 0:
                        normalized[i, j] += np.sum(weight*y)*(r == 0)
            # Independent literal full right-trivialized Euler of odd
            # curvature, including all four shared-link incidences.
            for occurrence, (ph, role, inv) in enumerate(loc):
                for g in range(6):
                    df = -N.G[g] @ factors[occurrence] if inv else factors[occurrence] @ N.G[g]
                    dp = prefix[occurrence] @ df @ suffix[occurrence+1]
                    dc = (dp+pi @ dp @ pi)*F(1, 2)
                    ek[ph, role, g] += np.sum(N.WEIGHT[face]*dc)
    assert not np.any(solder)
    assert not np.any(ek) and not np.any(xi)
    assert np.array_equal(ek.reshape(4, 24), owned_ek[0])
    assert np.array_equal(xi, owned_xi[0])
    assert all(F(4*x).denominator == 1 for x in normalized.flat)
    assert rank(normalized) == 4
    scalar = 4*t/(4+3*t*t)
    assert np.array_equal(b[0], scalar*normalized)
    assert np.array_equal(b[0], b[1])
    assert np.array_equal(b[2], -b[0]) and np.array_equal(b[3], -b[0])
    assert all(np.array_equal(v, v.T) for v in b)
    assert not np.any(sum(b))
    assert all(rank(v) == 4 for v in b)
    nonzero = [[i, j, str(F(b[0, i, j]))] for i in range(10) for j in range(10) if b[0, i, j]]
    if t == F(1, 5):
        assert b[0, 1, 5] == -F(5, 103)
        assert b[0, 2, 4] == F(5, 103)
        assert len(nonzero) == 24
    return {
        'parameter': str(t),
        'physical_link_U': packed(u),
        'all_24_connection_rows_each_phase': packed(ek.reshape(4, 24)),
        'all_10_Gram_response_rows_each_phase': packed(xi),
        'all_16_solder_rows_each_phase': packed(solder),
        'true_metric_normal_Hessian_each_phase': packed(b),
        'rank_each_phase': [rank(v) for v in b],
        'pattern': [1, 1, -1, -1],
        'mean': packed(sum(b)*F(1, 4)),
        'normalized_B0_by_4t_over_4plus3t2': packed(normalized),
        'nonzero_B0_entries': nonzero,
        'literal_odd_curvature_pairing_checks': odd_pairing_count,
    }


def toy_control():
    eta = np.array([1, 0, 0, 0, -1, 0, 0, -1, 0, -1], dtype=object)
    ell = np.array([1, 0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=object)
    assert sum(eta*ell) == 0
    rows = []
    for length in (4, 8, 16, 32, 64):
        h = F(1, length)
        # tau is declared first, before root u is selected.
        tau = ell
        u = h
        q = sum(eta*ell)
        action = q*u*u
        ek = 2*q*u
        xi = u*u*ell
        assert action == 0 and ek == 0 and any(xi)
        assert np.array_equal(xi, h*h*tau)
        assert sum(eta*xi) == action
        raw_gap = h**-2 * length**4 * sum(abs(x) for x in xi)
        assert raw_gap == 2*length**4
        rows.append({'L': length, 'h': str(h), 'root_u': str(u),
                     'connection_Euler': str(ek), 'action_and_radial_trace': str(action),
                     'Xi': packed(xi), 'raw_normalized_gap': str(raw_gap)})
    # All identities here are complete degree-three polynomial coefficient
    # identities: A=q*u^2, A_u=2*q*u, A_q=u^2; no truncated jets.
    return {
        'scope': 'abstract polynomial proof-obligation negative control; NOT the D0 action',
        'action': 'A(Q,u)=(Q00+Q11)*u^2',
        'complete_polynomial_coefficients_q_u': {
            'action': [[1, 2, '1']], 'connection_Euler': [[1, 1, '2']],
            'metric_response': [[0, 2, '1']],
        },
        'metric_homogeneity_degree': 1,
        'fixed_metric': packed(eta), 'fixed_source_declared_before_roots': packed(ell),
        'fixed_metric_only_stationary_critical_value': '0',
        'stationary_source_fiber': 'u^2*ell, a nonzero eta-trace-free ray',
        'horizontal_lift_obstruction': '2*q*u=0 cannot extend u!=0 across q=0',
        'linearized_vertical_source_image': 'Ctranspose*ker(H)=span(2*u*ell) at q=0,u!=0',
        'mesh_checks': rows,
    }


def calculate(N, owner_hashes):
    cases = [exact_y_control(N, t) for t in (F(1, 5), F(-2, 7), F(1, 11), F(3, 10))]
    first = cases[0]['normalized_B0_by_4t_over_4plus3t2']
    assert all(c['normalized_B0_by_4t_over_4plus3t2'] == first for c in cases)
    return {
        'schema': 'a4d-stationary-source-conormal-control/1',
        'audited_input_head': INPUT_HEAD,
        'owner_sha256': owner_hashes,
        'arithmetic': 'exact Fraction rational matrices and polynomial coefficients; no floating decisions',
        'Y_statement': 'Xi=0 and EK=0 at eta; fixed-link metric normal rank4 is fast with zero phase mean',
        'general_parameter_factor': 'B0=t/(4+3*t^2) times a fixed signed integer matrix',
        'Y_cases': cases,
        'abstract_negative_control': toy_control(),
        'theorem_boundary': 'pullback symplectic form vanishes on each stationary smooth stratum; image isotropy requires local constant rank; conormal claim only on constant-action strata',
        'physical_completion_boundary': 'native finite-action convergence does not control metric tangent derivatives through a singular stationary projection',
        'parent_terminal': 'OPEN; no unrestricted fixed-smooth-source existence or nonexistence result',
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path)
    ap.add_argument('--expect', type=Path, default=Path(__file__).with_name('a4d_stationary_source_conormal_results.json'))
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    repo = find_repo(args.repo)
    owner_hashes = hashes(repo)
    expected = None
    if args.output is None:
        expected = json.loads(args.expect.read_text())
        assert expected['owner_sha256'] == owner_hashes, 'pinned literal owner SHA-256 mismatch'
    sys.path.insert(0, str(repo / CERT))
    N = importlib.import_module('a4d_identity_quarter_nonlinear_response_check')
    assert Path(N.__file__).resolve() == (repo / CERT / 'a4d_identity_quarter_nonlinear_response_check.py').resolve()
    result = calculate(N, owner_hashes)
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == expected, 'immutable exact ledger mismatch'
    print('PASS_LITERAL_Y_ALL24_EK_ALL10_XI_ALL16_SOLDER_ROWS')
    print('PASS_TRUE_GRAM_NORMAL_RANK4_OPPOSITE_PHASE_MEAN_ZERO')
    print('PASS_ODD_CURVATURE_PAIRING_AND_INDEPENDENT_FULL_EULER')
    print('PASS_POLYNOMIAL_TRACE_FREE_FIXED_SOURCE_NEGATIVE_CONTROL')
    print('PARENT_FIXED_SOURCE_TERMINAL_OPEN')


if __name__ == '__main__':
    main()
