#!/usr/bin/env python3
"""Two exact mixed-sign minors and one real-density source uniqueness control.

Time-flip memory has chi_minus on +/-e0 and chi_plus on the spatial shell.
Its complete first preparation lift follows from these two new cross
minors and the existing same-sign/axial/homogeneous lift. This does not
assert a varied-source solution, nonlinear continuation or GR closure.
The separate real-density control concerns the fixed global chi_plus
carrier and proves its real source-neutral density is uniquely I8/8.
No thermal replay or prior checker main runs. Default is read-only.
"""
import argparse
import hashlib
import json
from pathlib import Path

LOCAL_FILE = Path(__file__).resolve()
PROVIDER = LOCAL_FILE.with_name('check_even_memory_cross_lift.py')
PROVIDER_SHA = '3b5fa93d8740f19ee5bbcaee6fb7bd22774c89f52fa9523d1fc53a23603ca4c6'
if hashlib.sha256(PROVIDER.read_bytes()).hexdigest() != PROVIDER_SHA:
    raise ArithmeticError('pinned cross-lift literal definitions')
# Only literal CAR, arithmetic and Fourier definitions: stop BEFORE its
# determinant loop, rotation checks, result generation or CLI execution.
provider_scope = {'__file__': str(PROVIDER)}
exec(compile(PROVIDER.read_text().split('case_results = []')[0],
             str(PROVIDER), 'exec'), provider_scope)
globals().update(provider_scope)
check('pinned_cross_definition_provider', True)
LOCAL_DATA = LOCAL_FILE.with_name('EVEN_MEMORY_TIMEFLIP_LIFT_DATA.json')
raw_data = LOCAL_DATA.read_bytes()
timeflip_data = json.loads(raw_data)
signs = timeflip_data['memory_sign_by_axis']
check('actual_timeflip_signs', signs == [-1, 1, 1, 1])
check('two_new_cross_orbits', [case['q'] for case in timeflip_data['cases']]
      == [[1, 1, 0, 0], [1, -1, 0, 0]])


def occupied_sign(k):
    return signs[next(j for j in range(4) if k[j])]


def mixed_sign_map(q):
    pairs = [(k, l) for k in SHELL for l in SHELL
             if [l[j]-k[j] for j in range(4)] == q]
    check('two_complete_transfers_'+str(q), len(pairs) == 2)
    columns = []
    for kind, slots in (('coframe', 4), ('link', 6)):
        for role in range(4):
            for slot in range(slots):
                blocks = [shell_jet(kind, role, slot, k, l) for k, l in pairs]
                label = '%s_%s%d%d' % (q, kind, role, slot)
                check('ordered_transpose_'+label, blocks[1] == transpose(blocks[0]))
                for (k, l), X in zip(pairs, blocks):
                    conjugate = [[conjugate_polynomial(z) for z in row] for row in X]
                    check('minus_q_'+label+str(k),
                          shell_jet(kind, role, slot, [-z for z in k], [-z for z in l]) == conjugate)
                    check('actual_adjoint_'+label+str(k),
                          shell_jet(kind, role, slot, l, k) == transpose(conjugate))
                # Each full output uses its ACTUAL incoming cat. Because the
                # second pair reverses the first after momentum reversal and
                # signs(-k)=signs(k), these also impose both full left rows.
                columns.append([row[0]+occupied_sign(k)*row[15]
                                for (k, l), X in zip(pairs, blocks) for row in X])
    T = list(map(list, zip(*columns)))
    check('full32_by40_'+str(q), len(T) == 32 and len(columns) == 40)
    check('even_output_'+str(q),
          all(not any(T[i]) for i in range(32) if i % 16 not in EVEN))
    check('same_vac_'+str(q), T[0] == T[16])
    check('opposite_top_'+str(q), T[15] == [-z for z in T[31]])
    check('links_zero_vac_'+str(q), all(T[0][j] == zero for j in range(16, 40)))
    observers = []
    for j in range(1, 4):
        observers.append([sum((-row[4*role]*u[role][j]-row[4*role+j]*u[role][0]
                               for role in range(4)), zero) for row in T])
    Y = [row[16:]+[observers[j][i] for j in range(3)] for i, row in enumerate(T)]
    return Y, pairs


cases = []
for case in timeflip_data['cases']:
    q, rows, columns = case['q'], case['rows'], case['columns']
    Y, pairs = mixed_sign_map(q)
    check('all14_target_coordinates_'+str(q), rows == TARGET_ROWS)
    check('13_links_plus_observer_'+str(q), len(set(columns)) == 14
          and all(0 <= j < 24 for j in columns[:13]) and 24 <= columns[13] < 27)
    check('observer_supplies_vac_'+str(q), Y[0][columns[13]] != zero)
    A = DomainMatrix([[Y[i][j] for j in columns] for i in rows], (14, 14), K)
    determinant = A.det()
    check('exact_stored_minor_'+str(q), determinant == decode_polynomial(case['determinant_coefficients']))
    check('minor_nonzero_'+str(q), determinant != zero)
    common = determinant.gcd(conjugate_polynomial(determinant)).monic()
    expected = one
    for factor in case['nonvanishing_conjugate_gcd_factors']:
        coefficients = factor['coefficients_low_to_high']
        check('factor_positive_on_r_gt_1_'+str(q), coefficients in ([-1, 1], [1, 1], [1, 0, 1]))
        check('positive_multiplicity_'+str(q), factor['multiplicity'] > 0)
        expected *= sum((cv(c)*rp**j for j, c in enumerate(coefficients)), zero)**factor['multiplicity']
    check('exact_conjugate_gcd_'+str(q), common == expected)
    cases.append({'q': q, 'ordered_pairs': pairs, 'target_dimension': 14,
                  'determinant_degree': determinant.degree(),
                  'conjugate_gcd': str(s.factor(K.to_sympy(common))), 'all_r_gt_1': True})
check('spatial_C3_preserves_sign_pattern', [signs[j] for j in (0, 2, 3, 1)] == signs)

# Separate control: the full field-source moment map on REAL densities of
# the GLOBAL chi_plus shell carrier is injective. A necessary coframe
# subsystem alone proves this, so retaining all link/observer Euler rows
# cannot enlarge its kernel. No link source is dropped or used to cancel
# an independent coframe Euler row. The thermal baseline subtracts out.
chi = (s.eye(16)[:, 0]+s.eye(16)[:, 15])/s.sqrt(2)
for i in range(4):
    for j in range(4):
        check('half_onebody_%d%d' % (i, j),
              (chi.T*C_literal[i]*C_literal[j].T*chi)[0] == s.Rational(int(i == j), 2))
        check('zero_pair_expectation_%d%d' % (i, j),
              (chi.T*C_literal[i]*C_literal[j]*chi)[0] == 0
              and (chi.T*C_literal[i].T*C_literal[j].T*chi)[0] == 0)

zeta, zetabar = tp-one, tm-one
delta = zeta*zetabar
check('positive_phase_gap', delta == cv(2-s.sqrt(2)))
dual_denominator = (rp-one)*(rp+3)
dual_numerators = [[cv(eta[j])*((rp+3)*int(i == j)-one) for j in range(4)] for i in range(4)]
for i in range(4):
    for j in range(4):
        check('actual_Euclidean_dual_%d%d' % (i, j),
              sum((u[j][a]*dual_numerators[i][a] for a in range(4)), zero)
              == (dual_denominator if i == j else zero))


def momentum(axis, sign):
    k = [0]*4
    k[axis] = sign
    return k


def coframe_moment(axis, k, l):
    # Full literal CAR first jet, then its true chi_plus expectation.
    X = summ([scale(shell_jet('coframe', axis, slot, k, l), dual_numerators[axis][slot])
              for slot in range(4)])
    return (X[0][0]+X[0][15]+X[15][0]+X[15][15])/2


for i in range(4):
    for sign in (-1, 1):
        k = momentum(i, sign)
        check('homogeneous_density_moment_%d_%d' % (i, sign),
              coframe_moment(i, k, k) == 2*delta*dual_denominator)
    check('axial_density_moment_%d' % i,
          coframe_moment(i, momentum(i, -1), momentum(i, 1))
          == zetabar*(zeta+zetabar)*dual_denominator)
    for j in range(i+1, 4):
        for sign in (-1, 1):
            k, l = momentum(i, -1), momentum(j, sign)
            expected = delta*dual_denominator/2
            check('cross_density_moment_%d%d_%d' % (i, j, sign),
                  coframe_moment(i, k, l) == expected
                  and coframe_moment(i, [-z for z in l], [-z for z in k]) == expected)
check('axial_density_coefficient_nonzero', zetabar*(zeta+zetabar) != zero)

# Fourier order (-ei,+ei); real position columns (cos_i,sin_i).
FT = s.zeros(8)
REV = s.zeros(8)
for i in range(4):
    FT[2*i, 2*i] = FT[2*i+1, 2*i] = 1/s.sqrt(2)
    FT[2*i, 2*i+1], FT[2*i+1, 2*i+1] = s.I/s.sqrt(2), -s.I/s.sqrt(2)
for i in range(8):
    REV[i, i ^ 1] = 1
check('real_position_Fourier_isometry', FT.H*FT == s.eye(8))
slots = [(i, j) for i in range(8) for j in range(i, 8)]
moment_columns = []
for a, b in slots:
    density = s.zeros(8)
    density[a, b] = density[b, a] = 1
    R = s.simplify(FT*density*FT.H)
    check('density_Hermitian_and_real_%d%d' % (a, b), R.H == R and REV*R.conjugate()*REV == R)
    values = [R[2*i, 2*i]+R[2*i+1, 2*i+1] for i in range(4)]
    for i in range(4):
        values.extend([s.re(R[2*i, 2*i+1]), s.im(R[2*i, 2*i+1])])
    for i in range(4):
        for j in range(i+1, 4):
            for sign in (-1, 1):
                k, l = 2*i, 2*j+int(sign == 1)
                check('real_density_equal_cross_pairs_%d%d_%d%d%d' % (a, b, i, j, sign), R[k, l] == R[l ^ 1, k ^ 1])
                values.extend([s.re(R[k, l]), s.im(R[k, l])])
    moment_columns.append(s.Matrix(values))
moment_matrix = s.Matrix.hstack(*moment_columns)
moment_det = moment_matrix.det()
check('exact36_real_moments_injective', moment_matrix.shape == (36, 36)
      and moment_det == s.Rational(timeflip_data['real_density_control']['moment_matrix_determinant'])
      and moment_det != 0)

receipt = {
    'status': 'PASS', 'memory_sign_by_axis': signs, 'parameter_domain': 'a>b>0, ell>0',
    'new_cross_cases': cases,
    'complete_first_lift_consumer': 'time-spatial C3 orbits plus owned same-sign spatial, faithful axial, equal-diagonal Q0 and non-difference signed-resolvent lifts',
    'carrier': 'full16 outputs, both ordered/left constraints, real +/-Q, reference128 retained',
    'scaling': 'u=b*u_tilde and delta u=b*delta u_tilde give common X factor b^2/ell^2',
    'real_density_control': {
        'carrier': 'fixed global real chi_plus on all8 occupied momenta',
        'dimension': 36, 'moment_matrix_determinant': str(moment_det),
        'source_preserving_real_density': 'uniquely I8/8, even without a PSD assumption',
        'argument': '4 diagonal-pair moments, 4 complex axial coherences and12 complex cross coherences are determined by the actual coframe Euler subsystem; all other field rows remain',
        'rank_lowering_candidate_exists': False,
    },
    'not_asserted': ['timeflip varied-source solution', 'nonlinear timeflip branch', 'GR closure', 'classification beyond the fixed chi_plus real-density carrier'],
    'provider_sha256': PROVIDER_SHA, 'data_sha256': hashlib.sha256(raw_data).hexdigest(),
    'literal_provider_sha256': CORE_SHA, 'pinned_inputs': PINS,
    'python': platform.python_version(), 'sympy': s.__version__, 'checks': len(CHECKS),
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
rendered = json.dumps(receipt, ensure_ascii=False, indent=2)+'\n'
if args.output:
    args.output.write_text(rendered)
print(rendered, end='')
