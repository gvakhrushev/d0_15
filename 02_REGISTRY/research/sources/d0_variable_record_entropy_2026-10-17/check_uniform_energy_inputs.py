#!/usr/bin/env python3
"""Bounded exact global-Julia inputs for a lattice energy proof.

The two-site ring retains the literal full16 CAR module and all four roles.
It checks actual defect roots, the paired global recycling map and its fixed
Hermitian-Kraus double-commutator identity.  It is not a four-dimensional
solution, a uniform lattice estimate, an entropy/source limit or a physical
action/admission law.  Only the pinned creator definition is executed; no
previous entrypoint, grid census, rank or eigenspectrum is used.
"""

from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}


def _creators(repo):
    tree = ast.parse((repo / CURVED).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator')
             or (isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name)
                         and target.id == 'EXTERIOR_ORDER'
                         for target in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('uniform_energy_inputs:creator_definition_nodes')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, 'exec'), scope)
    return ([s.SparseMatrix(scope['creator'](r)) for r in range(4)],
            scope['EXTERIOR_ORDER'])


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('uniform_energy_inputs:' + name)
        checks.append(name)

    def zero(value):
        return s.simplify(s.expand(value)) == 0

    def eq(actual, expected, name):
        difference = actual - expected
        if isinstance(difference, s.MatrixBase):
            entries = s.SparseMatrix(difference).todok().values()
        else:
            entries = [difference]
        require(all(zero(entry) for entry in entries), name)

    def nonzero(matrix):
        return any(not zero(value)
                   for value in s.SparseMatrix(matrix).todok().values())

    def commutator(left, right):
        return left * right - right * left

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    c, order = _creators(repo)
    I16 = s.SparseMatrix(s.eye(16))
    O16 = s.SparseMatrix(16, 16, {})
    I2 = s.SparseMatrix(s.eye(2))
    I = s.SparseMatrix(s.eye(32))
    O = s.SparseMatrix(32, 32, {})
    require(order == (0, 2, 3, 1), 'literal_ACDB_full16_exterior_order')
    require(all(c[r] * c[t].H + c[t].H * c[r]
                == (I16 if r == t else O16)
                and c[r] * c[t] + c[t] * c[r] == O16
                for r in range(4) for t in range(4)),
            'all16_literal_CAR_all_four_roles')

    def kron(left, right):
        return s.SparseMatrix(s.kronecker_product(left, right))

    amplitudes = (s.Rational(3, 5), s.Rational(5, 13))
    defects = (s.Rational(4, 5), s.Rational(12, 13))
    require(all(0 < a < 1 and 0 < b < 1 and a*a+b*b == 1
                for a, b in zip(amplitudes, defects)),
            'strict_rational_345_and_5_12_13_Julia_margins')
    site_amplitudes = s.diag(*amplitudes)
    flip = s.SparseMatrix([[0, 1], [1, 0]])
    shifts = [kron(flip, I16)] + [I for _ in range(3)]
    C = [kron(site_amplitudes, c[0])]
    C.extend(kron(I2, amplitudes[0] * c[r]) for r in range(1, 4))
    P = [C[r] * shifts[r] for r in range(4)]
    require(len(C) == len(P) == len(shifts) == 4,
            'two_sites_full16_and_all_four_native_roles')
    require(all(shift.H * shift == I and shift * shift.H == I
                for shift in shifts),
            'actual_two_site_flip_and_three_identity_shifts_unitary')

    def positive_diagonal_root(matrix, name):
        require(matrix.is_diagonal(), name + '_diagonal_defect')
        diagonal = [matrix[i, i] for i in range(32)]
        require(all(entry.is_Rational and entry > 0 for entry in diagonal),
                name + '_strict_positive_rational_squares')
        root = s.SparseMatrix(s.diag(*(s.sqrt(entry) for entry in diagonal)))
        require(all(root[i, i].is_Rational and root[i, i] > 0
                    for i in range(32)), name + '_actual_positive_rational_root')
        eq(root * root, matrix, name + '_root_square')
        return root

    words = []
    hermitian_kraus = []
    roots = {}
    for role in range(4):
        for family, X in (('P', P[role]), ('C', C[role])):
            name = family + str(role)
            left = positive_diagonal_root(I-X*X.H, name + '_left')
            right = positive_diagonal_root(I-X.H*X, name + '_right')
            eq(X*right, left*X, name + '_true_Julia_intertwining')
            words.append((X, left, right))
            roots[(family, role)] = (left, right)
            hermitian_kraus.extend(((X+X.H)/s.sqrt(32),
                                    s.I*(X-X.H)/s.sqrt(32),
                                    left/4, right/4))
    require(len(words) == 8 and len(hermitian_kraus) == 32,
            'actual_eight_PC_pairs_give_32_fixed_Hermitian_Kraus')
    require(all(B.H == B for B in hermitian_kraus),
            'all_global_Kraus_have_fixed_Hermitian_phase')
    eq(sum((B*B for B in hermitian_kraus), O.copy()), I,
       'global_sum_B_squared_identity_not_only_pointwise')
    eq(roots[('P', 0)][0], roots[('C', 0)][0],
       'forward_left_root_unchanged_by_unitary_site_shift')
    eq(roots[('P', 0)][1], shifts[0].H*roots[('C', 0)][1]*shifts[0],
       'forward_right_root_is_shifted_to_its_actual_site')
    require(nonzero(roots[('P', 0)][1]-roots[('C', 0)][1]),
            'hostile_unshifted_right_root_would_change_the_programme')
    bad_unital = (sum((B*B for B in hermitian_kraus), O.copy())
                  +(roots[('C', 0)][1]**2-roots[('P', 0)][1]**2)/16-I)
    require(nonzero(bad_unital),
            'hostile_erasing_right_root_shift_breaks_global_unitality')

    def paired_T(X):
        return sum((Y.H*X*Y+Y*X*Y.H+left*X*left+right*X*right
                    for Y, left, right in words), O.copy())/16

    def hermitian_T(X):
        return sum((B*X*B for B in hermitian_kraus), O.copy())

    h = s.Rational(1, 2)
    forward = sum((P[r]-C[r] for r in range(4)), O.copy())/h
    D = forward+forward.H
    Delta = D*D
    eq(D.H, D, 'true_forward_plus_positive_adjoint_D_Hermitian')
    eq(Delta.H, Delta, 'actual_full32_D_square_Hermitian')
    require(nonzero(D), 'actual_two_site_D_not_zero')
    Xprobe = (kron(s.diag(1, 2), I16)
              +kron(flip, c[1]+c[1].H)/7)
    eq(Xprobe.H, Xprobe, 'site_and_CAR_probe_Hermitian')
    require(nonzero(commutator(Delta, Xprobe)),
            'probe_really_noncommutes_with_native_Delta')

    drift = None
    for name, X in (('Delta', Delta), ('site_CAR_probe', Xprobe)):
        paired = paired_T(X)
        global_value = hermitian_T(X)
        eq(paired, global_value, name + '_paired_Julia_equals_fixed_global_Hermitian_T')
        eq(s.trace(global_value), s.trace(X), name + '_global_trace_preserved')
        double = sum((commutator(B, commutator(X, B))
                      for B in hermitian_kraus), O.copy())/2
        eq(global_value-X, double, name + '_exact_ordered_double_commutator_identity')
        if name == 'Delta':
            drift = global_value-X
    require(nonzero(drift), 'actual_global_recycling_Delta_drift_nonzero')
    eq(drift.H, drift, 'actual_Delta_drift_Hermitian')
    eq(s.trace(drift), 0, 'actual_Delta_drift_trace_zero')
    wrong_sign = sum((commutator(B, commutator(B, Delta))
                      for B in hermitian_kraus), O.copy())/2
    require(nonzero(drift-wrong_sign),
            'hostile_reversed_inner_commutator_sign_rejected')

    # A universal noncommutative polynomial check, independent of this
    # fixture, shows the pairing identity for an arbitrary operator input.
    Y, Ya, X = s.symbols('Y Ya X', commutative=False)
    eq(((Y+Ya)*X*(Y+Ya)-(Y-Ya)*X*(Y-Ya))/32,
       (Ya*X*Y+Y*X*Ya)/16,
       'universal_PC_to_Hermitian_pairing_polynomial')

    # Scalar linearity of the principal cell map only.  If a separate
    # calculus proof identifies F5=2*lambda*F3, then b2=2*lambda*b1
    # cancels it.  This check does NOT assert that higher-order PDE input.
    lam = s.Symbol('lambda', positive=True)
    principal, b1, Tb1 = s.symbols('principal b1 Tb1', commutative=False)
    eq(principal*(2*lam*Tb1)*principal-lam*(2*lam*b1),
       2*lam*(principal*Tb1*principal-lam*b1),
       's2_scalar_cell_scaling_b2_equals_two_lambda_b1')

    witness = next(({'row': row, 'column': column, 'value': str(s.simplify(value))}
                    for (row, column), value in sorted(s.SparseMatrix(drift).todok().items())
                    if not zero(value)), None)
    require(witness is not None, 'exact_nonzero_drift_entry_recorded')
    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks,
        'source_pins': PINS,
        'fixture': {'sites': 2, 'forms': 16, 'roles': 4, 'system_dimension': 32,
                    'h': str(h), 'role0_amplitudes': [str(x) for x in amplitudes],
                    'role0_defect_factors': [str(x) for x in defects],
                    'other_role_amplitude': str(amplitudes[0]),
                    'shifts': ['two_site_flip', 'identity', 'identity', 'identity'],
                    'Hermitian_Kraus_count': len(hermitian_kraus)},
        'exact_formulae': {
            'D': '(sum_r(P_r-C_r)+(sum_r(P_r-C_r))^*)/h',
            'paired_T': '(1/16)*sum_(Y=P_r,C_r)(Y^* X Y+Y X Y^*+L_Y X L_Y+R_Y X R_Y)',
            'global_T': 'sum_a B_a X B_a, sum_a B_a^2=I',
            'B_each_Y': ['(Y+Y^*)/sqrt(32)', 'i*(Y-Y^*)/sqrt(32)', 'L_Y/4', 'R_Y/4'],
            'drift': 'T(Delta)-Delta=(1/2)*sum_a[B_a,[Delta,B_a]]',
            's2_cell_only': 'M(2*lambda*b1)=2*lambda*M(b1); F5=2*lambda*F3 is a separate premise',
        },
        'nonzero_Delta_drift_entry': witness,
        'scope': (
            'Exact two-site global operator input identities with the full16 CAR '
            'module and all four roles. The paired Julia and fixed Hermitian '
            'representations are mathematical expressions of the same recycling '
            'map, not a new physical record basis. No old run, spectral/rank '
            'census, four-dimensional solution, uniform lattice pseudodifferential '
            'calculus, energy/entropy/source convergence, changed action, '
            'preparation restriction or native physical admission is proved.'
        ),
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
