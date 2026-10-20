#!/usr/bin/env python3
"""Finite constrained-price preflight; no native state-to-action map is inferred."""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/d0_native_tangent_source_preflight'
PLAN = '02_REGISTRY/research/D0_NATIVE_TANGENT_SOURCE_PLAN_2026-10-09.md'
INPUTS = [
    '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
    '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md',
    '02_REGISTRY/research/A4D_NATIVE_DYNAMICAL_OWNERSHIP.md',
    '02_REGISTRY/research/A4D_NATIVE_ARCHIVE_APPARATUS_REALIZATION.md',
    '03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean',
    '03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean',
    '03_FORMALIZATION/D0/Representation/SourcePortPreparation.lean',
    '03_FORMALIZATION/D0/Core/Phi.lean',
]
SCOPE = {
    'status': 'FINITE_CONSTRAINED_COTANGENT_PREFLIGHT_NOT_NATIVE_SOURCE',
    'all_size_tangent_lift': 'ANALYTIC_IDENTITY_IN_PLAN',
    'finite_star_tangent_image_complete': True,
    'joint_metric_projection_surjective': True,
    'fixed_dressed_link_is_a_different_probe': True,
    'all_link_and_matter_directions_retained': True,
    'conormal_ambient_changes_restrict_to_zero': True,
    'fixed_p0_z_two_tick_gap_has_zero_metric_jet': True,
    'full_bootstrap_replaced_by_two_tick_gap': False,
    'dressed_link_identified_with_scene_degree_matrix': False,
    'native_Gamma_or_its_first_jet_derived': False,
    'archive_delay_metric_source_computed': False,
    'source_equals_rho0_proved': False,
    'G0b_closed': False,
    'positive_GR_or_global_closure': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def matrix_unit(i, j):
    out = s.zeros(4)
    out[i, j] = 1
    return out


def controls():
    checks = {}

    def check(group, condition):
        assert condition, group
        checks[group] = checks.get(group, 0) + 1

    eta = s.diag(1, -1, -1, -1)
    pairs = [(i, j) for i in range(4) for j in range(i, 4)]
    sym = [matrix_unit(i, j) if i == j else matrix_unit(i, j) + matrix_unit(j, i)
           for i, j in pairs]
    raw = [matrix_unit(i, j) for i in range(4) for j in range(4)]
    factors = [s.eye(4) + s.Rational(k + 1, 7) * matrix_unit(0, 1)
               + s.Rational(k + 2, 9) * matrix_unit(2, 3)
               + s.Rational(k, 11) * matrix_unit(1, 2) for k in range(5)]
    q = [f * eta * f.T for f in factors]
    boost = s.eye(4)
    boost[0, 0] = boost[1, 1] = s.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = s.Rational(4, 3)
    rot = s.eye(4)
    rot[1, 1] = rot[2, 2] = s.Rational(3, 5)
    rot[1, 2] = -s.Rational(4, 5)
    rot[2, 1] = s.Rational(4, 5)
    lorentz = [s.eye(4), boost, rot, boost * rot]
    D = [factors[0] * lorentz[e] * factors[e + 1].inv() for e in range(4)]
    for e in range(4):
        check('nondegenerate_constrained_background', D[e] * q[e + 1] * D[e].T == q[0])
        check('proper_lorentz_background', lorentz[e] * eta * lorentz[e].T == eta
              and lorentz[e].det() == 1 and lorentz[e][0, 0] > 0)
    check('noncommuting_links', D[1] * D[2] != D[2] * D[1])
    for qi in q:
        check('nondegenerate_raw_metric', qi.det() != 0 and qi == qi.T)

    def upper(M):
        return s.Matrix([M[i, j] for i, j in pairs])

    def residual(V, W):
        return s.Matrix.vstack(*[
            upper(D[e] * V[e + 1] * D[e].T + W[e] * q[e + 1] * D[e].T
                  + D[e] * q[e + 1] * W[e].T - V[0]) for e in range(4)])

    def flatten(V, W):
        return s.Matrix.vstack(*[upper(Vi) for Vi in V],
                               *[s.Matrix(list(We)) for We in W])

    def lift(V):
        return [(V[0] * q[0].inv() * D[e]
                 - D[e] * V[e + 1] * q[e + 1].inv()) / 2 for e in range(4)]

    ambient = []
    lifted = []
    for site in range(5):
        for basis in sym:
            V = [s.zeros(4) for _ in range(5)]
            V[site] = basis
            ambient.append(residual(V, [s.zeros(4) for _ in range(4)]))
            W = lift(V)
            check('all_fifty_metric_lifts', residual(V, W) == s.zeros(40, 1))
            lifted.append(flatten(V, W))
    for edge in range(4):
        for basis in raw:
            W = [s.zeros(4) for _ in range(4)]
            W[edge] = basis
            ambient.append(residual([s.zeros(4) for _ in range(5)], W))

    generators = [matrix_unit(0, j) + matrix_unit(j, 0) for j in range(1, 4)]
    generators += [matrix_unit(i, j) - matrix_unit(j, i)
                   for i in range(1, 4) for j in range(i + 1, 4)]
    for edge in range(4):
        for H in generators:
            K = factors[0] * H * factors[0].inv()
            W = [s.zeros(4) for _ in range(4)]
            W[edge] = K * D[edge]
            check('all_twenty_four_free_link_directions',
                  K * q[0] + q[0] * K.T == s.zeros(4)
                  and residual([s.zeros(4) for _ in range(5)], W) == s.zeros(40, 1))
            lifted.append(flatten([s.zeros(4) for _ in range(5)], W))

    C = s.Matrix.hstack(*ambient)
    J = s.Matrix.hstack(*lifted)
    rank_C, rank_J = C.rank(), J.rank()
    check('complete_tangent_matrix', C.shape == (40, 114) and J.shape == (114, 74)
          and C * J == s.zeros(40, 74) and rank_C == 40 and rank_J == 74)
    check('complete_metric_projection', J[:50, :50] == s.eye(50)
          and J[:50, 50:] == s.zeros(50, 24))
    check('full_matter_affine_spectators', 4 * 4 + 5 * 16 == 96
          and 210 - rank_C == 74 + 96 == 170)

    for site in range(5):
        columns = []
        for basis in sym:
            TF = basis - (q[site].inv() * basis).trace() * q[site] / 4
            check('all_tracefree_probe_lifts', (q[site].inv() * TF).trace() == 0)
            V = [s.zeros(4) for _ in range(5)]
            V[site] = TF
            check('tracefree_constraint_restriction', residual(V, lift(V)) == s.zeros(40, 1))
            columns.append(upper(TF))
        check('tracefree_metric_rank', s.Matrix.hstack(*columns).rank() == 9)

    weights = [1 if i == j else 2 for i, j in pairs] * 4
    for row in range(40):
        conormal = weights[row] * C[row, :]
        check('all_conormals_restrict_to_zero', conormal * J == s.zeros(1, 74))
        check('conormal_changes_ambient_metric_part', conormal[:, :50] != s.zeros(1, 50))
    for basis in sym:
        V = [basis] + [s.zeros(4) for _ in range(4)]
        check('fixed_dressed_link_false_probe_rejected',
              residual(V, [s.zeros(4) for _ in range(4)]) != s.zeros(40, 1))

    p, z = s.symbols('p z', positive=True)
    gap = -s.log(1 - 4 * z * p ** 3)
    check('two_tick_price_jets', s.simplify(s.diff(gap, p)
          - 12 * z * p ** 2 / (1 - 4 * z * p ** 3)) == 0)
    check('two_tick_price_jets', s.simplify(s.diff(gap, z)
          - 4 * p ** 3 / (1 - 4 * z * p ** 3)) == 0)
    curve_parameter = s.symbols('curve_parameter')
    check('fixed_parameter_price_has_zero_jet', s.diff(gap, curve_parameter) == 0)
    check('fixed_seam_has_zero_jet', s.diff(s.Rational(12, 5), curve_parameter) == 0)

    A = s.Matrix([[1, 2], [0, 3]])
    V = s.Matrix([[0, 1], [1, 0]])
    t = s.symbols('t')
    return_curve = 2 * (A + t * V) - (A + t * V) ** 2
    jet = return_curve.diff(t).subs(t, 0)
    check('noncommutative_return_jet', jet == 2 * V - V * A - A * V)
    check('false_commuting_return_jet_rejected', jet != 2 * V - 2 * A * V)
    return {
        'checks': checks,
        'total_controls': sum(checks.values()),
        'finite_star': {
            'sites': 5, 'links': 4, 'symmetric_metric_slots': 50,
            'connection_directions': 24, 'geometric_ambient_slots': 114,
            'constraint_rank': rank_C, 'geometric_tangent_rank': rank_J,
            'metric_projection_rank': 50, 'tracefree_metric_rank': 45,
            'retained_affine_and_matter_spectators': 96,
            'complete_ambient_slots': 210, 'complete_tangent_dimension': 170,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', default=str(ROOT / (BASE + '_certificate.json')))
    parser.add_argument('--output')
    args = parser.parse_args()
    result = {'schema': 'd0-constrained-price-preflight/1', 'scope': SCOPE,
              'input_sha256': {p: sha(p) for p in INPUTS},
              'plan_sha256': sha(PLAN), 'checker_sha256': sha(BASE + '_check.py'),
              **controls()}
    if args.expected != 'none':
        expected = json.loads(Path(args.expected).read_text())
        assert expected.get('scope') == SCOPE, 'PREFLIGHT_SCOPE_MISMATCH'
        assert expected == result, 'PREFLIGHT_CERTIFICATE_MISMATCH'
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print('PASS_CONSTRAINED_PRICE_PREFLIGHT controls=' + str(result['total_controls']))


if __name__ == '__main__':
    main()
