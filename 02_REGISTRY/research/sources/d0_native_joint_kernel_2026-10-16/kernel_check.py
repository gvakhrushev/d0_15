#!/usr/bin/env python3
"""Exact finite fixture for the complete normalized-matter joint kernel.

This is a four-dimensional matrix identity test, not a four-state native D0
preparation, a physical source, a refinement statement, or GR closure. It uses
the fixed v8 price family with m=2=2*n, alpha=1/8, beta=m*alpha, z=1/5,
reference multiplicity b=2. All calculations are rational, including complex
amplitude coordinates. No expected evidence or other files are written.

The field map is the explicit analytic map
 Delta(h,t,u) = exp(A(t)) [Delta0 + sum h_i D_i + u*h_0 E00] exp(-A(t)),
where A is anti-Hermitian. The five D_i and ten orbit directions span the
entire Hermitian hyperplane perpendicular to the actual price-plus-matter
gradient C. Thus the origin is stationary without an added or fitted source.
The extra nonlinear coordinate u has zero first jet and a declared mixed jet;
it independently exercises the nonzero Hermitian shell multiplier eta.
"""

import hashlib
import json
from pathlib import Path

import sympy as s


Q = s.Rational
I = s.I
N = 4
RANK = 2
DELTA = s.diag(1, 2, 2, 4)
EPSILON = s.Integer(2)
U = s.Matrix([[0, 0], [1, 0], [0, 1], [0, 0]])
P = U * U.H
COMPLEMENT = s.eye(N) - P
RESOLVENT = s.diag(-1, 0, 0, Q(1, 2))
ALPHA = Q(1, 8)
M = 2
BETA = M * ALPHA
ZETA = Q(1, 5)
REFERENCE = 2
B = s.eye(N) - ALPHA * DELTA
Z = s.trace(B ** M)
FEEDBACK = (1 - ZETA) * s.eye(N) + ZETA * B ** M
FINV = FEEDBACK.inv()
RHO = P / RANK
KAPPA = -B / Z + REFERENCE * BETA * ZETA * B * FINV
C = RHO + KAPPA
COUNTS = {}
REJECTED = []


def ck(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1


def reduced(value):
    if isinstance(value, s.MatrixBase):
        return value.applyfunc(lambda x: s.cancel(s.expand(x)))
    return s.cancel(s.expand(value))


def zero(value):
    value = reduced(value)
    return value == (s.zeros(*value.shape) if isinstance(value, s.MatrixBase) else 0)


def reject(name, condition):
    ck('reject_' + name, not condition)
    REJECTED.append(name)


def unit(i, j, size=N):
    result = s.zeros(size)
    result[i, j] = 1
    return result


def comm(a, b):
    return a * b - b * a


def real_coordinates(matrix):
    return s.Matrix([part for item in matrix for part in (s.re(item), s.im(item))])


PAULI = [s.diag(1, -1), s.Matrix([[0, 1], [1, 0]]),
         s.Matrix([[0, I], [-I, 0]])]
VERTICAL = [I * s.eye(RANK)] + [I * item for item in PAULI]


def dkappa(x, omit_normalizer=False):
    """Spectral divided differences, with the full rank-one Z response."""
    eigenvalues = list(DELTA.diagonal())
    t = s.Symbol('t', real=True)
    bt = 1 - ALPHA * t
    fixed_z = -bt / Z + REFERENCE * BETA * ZETA * bt / (1 - ZETA + ZETA * bt ** M)
    result = s.zeros(N)
    for i in range(N):
        for j in range(N):
            if eigenvalues[i] == eigenvalues[j]:
                coefficient = s.diff(fixed_z, t).subs(t, eigenvalues[i])
            else:
                coefficient = (KAPPA[i, i] - KAPPA[j, j]) / (eigenvalues[i] - eigenvalues[j])
            result[i, j] = coefficient * x[i, j]
    if not omit_normalizer:
        dz = -BETA * s.trace(B * x)
        result += B * dz / Z ** 2
    return reduced(result)


def direct_price_hessian(x, w, y):
    """Differentiate log Z and log det M directly; no divided differences."""
    zx, zw = -2 * ALPHA * s.trace(B * x), -2 * ALPHA * s.trace(B * w)
    zxw = 2 * ALPHA ** 2 * s.trace(x * w) - 2 * ALPHA * s.trace(B * y)
    mx = -ZETA * ALPHA * (x * B + B * x)
    mw = -ZETA * ALPHA * (w * B + B * w)
    mxw = ZETA * (ALPHA ** 2 * (x * w + w * x) - ALPHA * (y * B + B * y))
    return reduced((zxw / Z - zx * zw / Z ** 2) / BETA
                   - REFERENCE * s.trace(FINV * mxw - FINV * mw * FINV * mx))


def field_jets():
    e00 = unit(0, 0)
    diagonal = [unit(1, 1) - unit(2, 2),
                unit(1, 2) + unit(2, 1),
                I * unit(1, 2) - I * unit(2, 1),
                unit(1, 1) + unit(2, 2) - (2 * C[1, 1] / C[0, 0]) * e00,
                unit(3, 3) - (C[3, 3] / C[0, 0]) * e00]
    names = ['shell_z', 'shell_x', 'shell_y', 'shell_mean', 'upper_balance']
    generators = []
    for i in range(N):
        for j in range(i + 1, N):
            gap = DELTA[j, j] - DELTA[i, i]
            if gap == 0:
                continue
            generators.extend([(unit(i, j) - unit(j, i)) / gap,
                               I * (unit(i, j) + unit(j, i)) / gap])
            names.extend([f'orbit_{i}{j}_real', f'orbit_{i}{j}_imag'])
    first = diagonal + [comm(a, DELTA) for a in generators] + [s.zeros(N)]
    names.append('nonlinear_u')
    count = len(first)
    second = [[s.zeros(N) for _ in range(count)] for _ in range(count)]
    for i, a in enumerate(generators, 5):
        for j, d in enumerate(diagonal):
            second[i][j] = second[j][i] = comm(a, d)
        for j, a2 in enumerate(generators, 5):
            second[i][j] = (comm(a, comm(a2, DELTA)) + comm(a2, comm(a, DELTA))) / 2
    second[-1][0] = second[0][-1] = e00
    return names, first, second


def amplitude_basis():
    result = []
    for i in range(N):
        for j in range(RANK):
            for scalar in (1, I):
                item = s.zeros(N, RANK)
                item[i, j] = scalar
                result.append(item)
    return result


def full_jacobian(first, fixed_hessian):
    """All field, complex amplitude/eigenvalue and normalization rows."""
    nf = len(first)
    amplitudes = amplitude_basis()
    jac = s.zeros(nf + 2 * N * RANK + 1)
    jac[:nf, :nf] = fixed_hessian
    for a, x in enumerate(first):
        jac[nf:nf + 2 * N * RANK, a] = real_coordinates(x * U)
        for b, amplitude in enumerate(amplitudes, nf):
            jac[a, b] = reduced(s.trace((amplitude * U.H + U * amplitude.H) * x) / RANK)
    for b, amplitude in enumerate(amplitudes, nf):
        jac[nf:nf + 2 * N * RANK, b] = real_coordinates((DELTA - EPSILON * s.eye(N)) * amplitude)
        jac[-1, b] = reduced(s.trace(U.H * amplitude + amplitude.H * U) / RANK)
    jac[nf:nf + 2 * N * RANK, -1] = real_coordinates(-U)
    return reduced(jac)


def lift(first, field, eta, vertical):
    x = sum((coefficient * item for coefficient, item in zip(field, first)), s.zeros(N))
    amplitude = -RESOLVENT * x * U + U * (RANK * eta / 2 + vertical)
    depsilon = s.trace(P * x) / RANK
    return s.Matrix(list(field) + list(real_coordinates(amplitude)) + [depsilon])


def kernel_fixture():
    names, first, second = field_jets()
    nf = len(first)
    ck('positive_Delta_and_B_in_open_neighborhood', all(x > 0 for x in DELTA.diagonal())
       and all(x > 0 for x in B.diagonal()))
    ck('full_rank_normalized_purification', U.rank() == RANK and s.trace(U.H * U) == RANK)
    ck('shell_eigen_equation', DELTA * U == EPSILON * U)
    ck('lower_and_upper_complement', RESOLVENT[0, 0] < 0 < RESOLVENT[3, 3])
    ck('Q_resolvent_identity', (DELTA - EPSILON * s.eye(N)) * RESOLVENT == COMPLEMENT)
    ck('no_fitted_source_actual_stationary_variation_image', all(zero(s.trace(C * x)) for x in first))
    ck('entire_Hermitian_gradient_annihilator_not_diagonal_fields',
       s.Matrix.hstack(*(real_coordinates(x) for x in first)).rank() == N ** 2 - 1)
    ck('all_Hermitian_first_and_second_jets', all(x == x.H for x in first)
       and all(y == y.H for row in second for y in row))
    ck('nonzero_direct_CY_term', s.trace(C * second[-1][0]) != 0)
    fixed = s.zeros(nf)
    no_y = s.zeros(nf)
    reduced_hessian = s.zeros(nf)
    for a, x in enumerate(first):
        dx = dkappa(x)
        for b, w in enumerate(first):
            y = second[a][b]
            fixed[a, b] = direct_price_hessian(x, w, y) + s.trace(RHO * y)
            no_y[a, b] = direct_price_hessian(x, w, s.zeros(N))
            ck('independent_logdet_Z_jet_equals_spectral_formula',
               zero(fixed[a, b] - s.trace(C * y) - s.trace(dx * w)))
            response = 2 * s.re(s.trace(P * x * RESOLVENT * w * P)) / RANK
            reduced_hessian[a, b] = reduced(fixed[a, b] - response)
    fixed, reduced_hessian = reduced(fixed), reduced(reduced_hessian)
    ck('symmetric_full_and_reduced_field_Hessians', fixed == fixed.T
       and reduced_hessian == reduced_hessian.T)
    tangent = [U.H * x * U - s.trace(P * x) * s.eye(RANK) / RANK for x in first]
    constraints = s.Matrix([[s.trace(e * t) / 2 for t in tangent] for e in PAULI])
    eta_pairing = s.Matrix([[s.trace(e * t) for e in PAULI] for t in tangent])
    reduced_kkt = constraints.row_join(s.zeros(3)).col_join(reduced_hessian.row_join(eta_pairing))
    full = full_jacobian(first, fixed)
    lift_columns = []
    for i in range(nf + 3):
        v = s.zeros(nf, 1)
        eta = s.zeros(RANK)
        if i < nf:
            v[i] = 1
        else:
            eta = PAULI[i - nf]
        lift_columns.append(lift(first, v, eta, s.zeros(RANK)))
    lifting = s.Matrix.hstack(*lift_columns)
    vertical = s.Matrix.hstack(*(lift(first, s.zeros(nf, 1), s.zeros(RANK), k) for k in VERTICAL))
    reduced_null = s.Matrix.hstack(*reduced_kkt.nullspace())
    reconstructed = (lifting * reduced_null).row_join(vertical)
    full_nullity = full.cols - full.rank()
    ck('all_normalized_complex_amplitude_rows_vanish', zero(full * reconstructed))
    ck('full_kernel_equality_by_inclusion_and_exact_dimension', reconstructed.rank() == full_nullity)
    ck('all_four_antiHermitian_vertical_nulls_retained', vertical.rank() == RANK ** 2
       and zero(full * vertical))
    ck('shell_traceless_constraint_is_surjective', constraints.rank() == 3)

    # An actual orbit direction mixes a shell state with the lower Q mode.
    orbit_v = s.zeros(nf, 1)
    orbit_v[5] = 1
    orbit_solution = lift(first, orbit_v, s.zeros(RANK), s.zeros(RANK))
    ck('joint_orbit_kernel_has_moving_matter', zero(full * orbit_solution)
       and not zero(orbit_solution[nf:nf + 2 * N * RANK, :]))
    frozen = orbit_solution.copy()
    frozen[nf:nf + 2 * N * RANK, :] = s.zeros(2 * N * RANK, 1)
    reject('FROZEN_MATTER', zero(full * frozen))
    reject('DROPPED_SECOND_FIELD_JET_Y', zero(full_jacobian(first, no_y) * orbit_solution))

    # u couples only through its genuine mixed second jet u*h_0*E00.
    u_v = s.zeros(nf, 1)
    u_v[-1] = 1
    eta = -C[0, 0] * PAULI[0] / 2
    ck('nonzero_Hermitian_shell_eta_required', eta != s.zeros(RANK)
       and zero(full * lift(first, u_v, eta, s.zeros(RANK))))
    reject('FORCED_ETA_ZERO', zero(full * lift(first, u_v, s.zeros(RANK), s.zeros(RANK))))

    # The price's Z term is tested against independently differentiated log Z,
    # including diagonal field variations even when a particular null is orbital.
    diagonal_x = first[3]
    lost = s.trace((dkappa(diagonal_x) - dkappa(diagonal_x, True)) * diagonal_x)
    ck('normalizer_rank_one_response_is_nonzero', lost != 0)
    reject('DROPPED_NORMALIZER_RESPONSE', zero(direct_price_hessian(diagonal_x, diagonal_x, s.zeros(N))
           - s.trace(dkappa(diagonal_x, True) * diagonal_x)))
    lower = s.re(s.trace(P * first[5] * RESOLVENT * first[5] * P))
    upper_index = names.index('orbit_13_real')
    upper = s.re(s.trace(P * first[upper_index] * RESOLVENT * first[upper_index] * P))
    ck('opposite_signed_lower_and_upper_shell_feedback', lower < 0 < upper)
    positive_only = orbit_solution.copy()
    wrong_amplitude = -s.diag(1, 0, 0, Q(1, 2)) * first[5] * U
    positive_only[nf:nf + 2 * N * RANK, :] = real_coordinates(wrong_amplitude)
    reject('POSITIVE_ONLY_Q_RESOLVENT', zero(full * positive_only))
    return {'field_dimension': nf, 'Hermitian_tangent_image_rank': 15,
            'full_real_Jacobian_shape': list(full.shape), 'reduced_KKT_shape': list(reduced_kkt.shape),
            'full_kernel_dimension': full_nullity, 'reduced_kernel_dimension': reduced_null.cols,
            'antiHermitian_vertical_dimension': vertical.cols,
            'normalizer_diagonal_witness': str(lost), 'stationary_gradient_C': [str(x) for x in C.diagonal()]}


def nonlinear_schur_fixture():
    """Independent block identities; no stationary physical source is fitted."""
    qembed = s.Matrix([[1, 0], [0, 0], [0, 0], [0, 1]])
    d = s.diag(-1, 2)
    gq = d.inv()
    coupling = s.Matrix([[Q(1, 7), I / 11], [(1 + I) / 13, Q(1, 17)]])
    shell = coupling.H * gq * coupling
    delta = EPSILON * s.eye(N) + qembed * d * qembed.H + qembed * coupling * U.H \
        + U * coupling.H * qembed.H + U * shell * U.H
    j = U - qembed * gq * coupling
    e = U.H * (delta - EPSILON * s.eye(N)) * U - coupling.H * gq * coupling
    gram = reduced(j.H * j)
    ck('nonlinear_Q_elimination_all_complex_rows', zero(qembed.H * (delta - EPSILON * s.eye(N)) * j))
    ck('nonlinear_Schur_E_equals_Jstar_residual_J', zero(e - j.H * (delta - EPSILON * s.eye(N)) * j))
    ck('nonlinear_Schur_G_is_moving_Gram', gram != s.eye(RANK) and gram == gram.H)
    x = unit(0, 1) + unit(1, 0) + I * unit(2, 3) - I * unit(3, 2) + unit(0, 0) / 3
    depsilon = Q(2, 7)
    dq = qembed.H * x * qembed - depsilon * s.eye(RANK)
    dv = qembed.H * x * U
    dgq = -gq * dq * gq
    de = U.H * x * U - depsilon * s.eye(RANK) \
        - dv.H * gq * coupling - coupling.H * dgq * coupling - coupling.H * gq * dv
    ck('nonlinear_exact_dE_including_epsilon_Gram', zero(de - j.H * x * j + depsilon * gram))
    tau = s.eye(RANK) / s.trace(gram)
    ck('nonlinear_positive_tau_exact_normalization', tau[0, 0] > 0 and zero(s.trace(tau * gram) - 1))
    reject('FROZEN_GRAM_IN_EPSILON_NORMALIZATION', s.trace(tau) == 1)
    reject('FROZEN_GRAM_IN_dE', zero(de - j.H * x * j + depsilon * s.eye(RANK)))
    return {'Q_resolvent_signature': [-1, 1], 'E_zero': zero(e),
            'Gram_trace': str(s.trace(gram)), 'tau_trace': str(s.trace(tau)),
            'scope': 'exact nonlinear block/elimination identities only; no claim of all field stationarity'}


def main():
    fixture = kernel_fixture()
    schur = nonlinear_schur_fixture()
    result = {'schema': 'd0-native-joint-kernel-finite-fixture/1',
              'status': 'PASS_EXACT_FINITE_IDENTITIES',
              'price': {'m': M, 'n': 1, 'alpha': str(ALPHA), 'beta': str(BETA),
                        'z': str(ZETA), 'reference_multiplicity': REFERENCE, 'Z': str(Z)},
              'fixture': fixture, 'nonlinear_schur': schur,
              'checks': sum(COUNTS.values()), 'check_names': COUNTS, 'rejected_shortcuts': REJECTED,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'boundary': 'finite exact matrix fixture only; native preparation, L8 application, refinement and GR remain outside this certificate'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
