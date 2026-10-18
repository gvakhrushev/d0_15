#!/usr/bin/env python3
"""Exact complete preparation first lift for the real even memory cat.

At q=e_i +/- e_j, i!=j, every coframe tangent admits retained link/observer
compensation, for every a>b>0. Four orientation-preserving spatial orbits
are checked. The full16 CAR output, both ordered shell blocks, their left
constraints and the real -q mode remain present. No source/Hessian or
nonlinear field-equation conclusion is asserted. No old suite runs.
Default is read-only; --output writes the optional small receipt.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import platform

from sympy.polys.matrices import DomainMatrix

SELF = Path(__file__).resolve()
CORE = SELF.with_name('check_spatial_shell_obstruction.py')
CORE_SHA = 'c1c0e05e479549d7097da5343359d5271cea3326825efaa752f62e8d989bb8a9'
if hashlib.sha256(CORE.read_bytes()).hexdigest() != CORE_SHA:
    raise ArithmeticError('pinned literal CAR/Fourier arithmetic provider')
# Execute only its pinned literal CAR16/algebra definitions, ending BEFORE
# any separator load or historical obstruction calculation.
core_source = CORE.read_text().split('separator_path =')[0]
core_scope = {'__file__': str(CORE)}
exec(compile(core_source, str(CORE), 'exec'), core_scope)
globals().update(core_scope)
check('pinned_literal_provider', True)

DATA_PATH = SELF.with_name('EVEN_MEMORY_CROSS_LIFT_DATA.json')
data_bytes = DATA_PATH.read_bytes()
data = json.loads(data_bytes)
check('four_cross_orbits', [case['q'] for case in data['cases']] ==
      [[1, 1, 0, 0], [1, -1, 0, 0], [0, 1, 1, 0], [0, 1, -1, 0]])
CHI = s.eye(16)[:, 0] + s.eye(16)[:, 15]
check('actual_even_cat_basis', S*CHI == CHI)
for j, G in enumerate(exterior):
    check('proper_exterior_link_fixes_even_cat_%d' % j,
          all(row[0]+row[15] == zero for row in G))
    check('transpose_link_fixes_even_cat_%d' % j,
          all(row[0]+row[15] == zero for row in transpose(G)))


def dirac_at(k):
    return summ([add(scale(cr[j], tp**(k[j] % 8)-one),
                     scale(transpose(cr[j]), tp**((-k[j]) % 8)-one))
                 for j in range(4)])


def shell_jet(kind, role, slot, k, l):
    tk = tp**(k[role] % 8)
    tl_bar = tp**((-l[role]) % 8)
    if kind == 'coframe':
        J = add(scale(C[slot], tk-one),
                scale(transpose(C[slot]), tl_bar-one))
    else:
        G = exterior[slot]
        J = add(scale(mm(cr[role], G), tk),
                scale(mm(transpose(G), transpose(cr[role])), tl_bar))
    return add(mm(dirac_at(l), J), mm(J, dirac_at(k)))


SHELL = []
for axis in range(4):
    for sign in (-1, 1):
        k = [0]*4
        k[axis] = sign
        SHELL.append(k)
EVEN = (0, 3, 5, 6, 9, 10, 12, 15)
TARGET_ROWS = [0, 3, 5, 6, 9, 10, 12, 15, 19, 21, 22, 25, 26, 28]


def build_complete_map(q):
    pairs = [(k, l) for k in SHELL for l in SHELL
             if [l[j]-k[j] for j in range(4)] == q]
    check('two_ordered_pairs_%s' % q, len(pairs) == 2)
    columns = []
    for kind, slots in (('coframe', 4), ('link', 6)):
        for role in range(4):
            for slot in range(slots):
                blocks = [shell_jet(kind, role, slot, k, l) for k, l in pairs]
                label = '%s_%s%d%d' % (q, kind, role, slot)
                # This is the full left constraint, not chi compression.
                check('ordered_transpose_'+label, blocks[1] == transpose(blocks[0]))
                for (k, l), X in zip(pairs, blocks):
                    negative = shell_jet(kind, role, slot,
                                         [-z for z in k], [-z for z in l])
                    conjugate = [[conjugate_polynomial(z) for z in row] for row in X]
                    check('real_minus_q_'+label+str(k), negative == conjugate)
                    # Self-adjoint operator, actual adjoint incoming phase/order.
                    reverse = shell_jet(kind, role, slot, l, k)
                    check('Hermitian_reversed_pair_'+label+str(k),
                          reverse == transpose(conjugate))
                    check('no_vac_top_shortcut_'+label+str(k),
                          X[0][15] == zero and X[15][0] == zero)
                columns.append([row[0]+row[15] for X in blocks for row in X])
    T = list(map(list, zip(*columns)))
    check('all40_columns_'+str(q), len(columns) == 40)
    check('all16_outputs_per_pair_'+str(q), len(T) == 32)
    check('even_output_'+str(q),
          all(not any(T[i]) for i in range(32) if i % 16 not in EVEN))
    check('common_vac_scalar_'+str(q), T[0] == T[16])
    check('common_top_scalar_'+str(q), T[15] == T[31])
    check('links_have_zero_vac_row_'+str(q),
          all(T[i][j] == zero for i in (0, 16) for j in range(16, 40)))
    observers = []
    for j in range(1, 4):
        observers.append([sum((-row[4*role]*u[role][j]
                               -row[4*role+j]*u[role][0]
                               for role in range(4)), zero) for row in T])
    Y = [row[16:]+[observers[j][i] for j in range(3)] for i, row in enumerate(T)]
    return T, Y, pairs


def decode_polynomial(coefficients):
    value = zero
    for degree, coeffs in coefficients.items():
        check('scalar_degree_nonnegative', int(degree) >= 0)
        check('zeta8_field_basis', len(coeffs) <= 4)
        value += rp**int(degree)*sum((cv(s.Rational(c))*tp**j
                                     for j, c in enumerate(coeffs)), zero)
    return value


case_results = []
for case in data['cases']:
    q = case['q']
    T, Y, pairs = build_complete_map(q)
    rows, columns = case['rows'], case['columns']
    check('complete14_target_coordinates_'+str(q), rows == TARGET_ROWS)
    check('13_links_and_one_observer_'+str(q),
          len(set(columns)) == 14 and all(0 <= j < 24 for j in columns[:13])
          and 24 <= columns[13] < 27)
    check('observer_supplies_vac_scalar_'+str(q), Y[0][columns[13]] != zero)
    A = DomainMatrix([[Y[i][j] for j in columns] for i in rows], (14, 14), K)
    determinant = A.det()
    check('exact_minor_'+str(q),
          determinant == decode_polynomial(case['determinant_coefficients']))
    check('nonzero_minor_'+str(q), determinant != zero)
    common = determinant.gcd(conjugate_polynomial(determinant)).monic()
    factors = one
    for factor in case['nonvanishing_conjugate_gcd_factors']:
        coefficients = factor['coefficients_low_to_high']
        # Every listed factor is strictly positive on real r>1. A real zero
        # of det would also zero its coefficient conjugate and hence this gcd.
        check('positive_factor_on_r_gt_1_'+str(q),
              coefficients in ([-1, 1], [1, 1], [1, 0, 1]))
        check('factor_multiplicity_positive_'+str(q), factor['multiplicity'] > 0)
        factors *= sum((cv(c)*rp**j for j, c in enumerate(coefficients)), zero)**factor['multiplicity']
    check('exact_conjugate_gcd_'+str(q), common == factors)
    # Constructive right inverse: for any coframe z in C^16, set the selected
    # retained variables to -A(r)^(-1) [T_u(r) z]_TARGET_ROWS, all others zero.
    # The checked 14-dimensional common target makes all32 equations hold.
    case_results.append({'q': q, 'ordered_pairs': pairs,
                         'target_dimension': 14, 'links_used': 13,
                         'observer_used': columns[13]-24+1,
                         'determinant_degree': determinant.degree(),
                         'conjugate_gcd': str(s.factor(K.to_sympy(common))),
                         'all_r_gt_1': True})

# Every symmetric physical delta q has a coframe representative: U=F eta,
# F=(r-1)I+11^T and delta U=delta q F^(-1)/2.
F = s.Matrix(4, 4, lambda i, j: r if i == j else 1)
Finv_numerator = (r+3)*s.eye(4)-s.ones(4)
check('all_physical_metric_tangents_have_coframe_lift',
      s.simplify(F*Finv_numerator-(r-1)*(r+3)*s.eye(4)) == s.zeros(4))
# Only the orientation-preserving spatial 3-cycle is needed. Odd spatial
# permutations would send vac+top to vac-top and are not used here.
permutation = (0, 2, 3, 1)
P_columns = []
for mask in range(16):
    v = s.eye(16)[:, 0]
    for j in reversed(range(4)):
        if mask & (1 << j):
            v = C_literal[permutation[j]]*v
    P_columns.append(v)
P = s.Matrix.hstack(*P_columns)
check('spatial_cycle_preserves_even_cat', P*CHI == CHI and P.T*P == s.eye(16))
for j in range(4):
    check('spatial_cycle_CAR_%d' % j, P*C_literal[j]*P.T == C_literal[permutation[j]])

receipt = {
    'status': 'PASS', 'scope': 'full rectangular preparation first lift at cross shell modes',
    'carrier': 'full16 CAR output and shell reference128; real even cat occupied support',
    'parameter_domain': 'all a>b>0 and ell>0',
    'scaling': 'u=b*u_tilde; delta u=b*delta u_tilde; every column scales b^2/ell^2',
    'right_inverse': '-A(r)^(-1) times the selected14 coframe-forcing rows; other retained coordinates zero',
    'coverage': 'all q=+/-e_i+/-e_j, i!=j, by spatial3-cycle and real conjugation',
    'not_asserted': ['q=0', 'q=2e_i', 'full source stationarity', 'nonlinear branch', 'GR closure'],
    'data_sha256': hashlib.sha256(data_bytes).hexdigest(),
    'literal_provider_sha256': CORE_SHA,
    'pinned_inputs': PINS,
    'python': platform.python_version(), 'sympy': s.__version__,
    'checks': len(CHECKS), 'cases': case_results,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, help='optional receipt destination')
args = parser.parse_args()
if args.output:
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
