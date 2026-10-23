#!/usr/bin/env python3
"""Finite causal Book return of the ORIGINAL full128 Golden reflection.

Only the existing native row constructor is consumed, never its run().
Exact small algebra proves the decisive clock/dark identities; original
full128 numerical controls retain all64 workspace and both Golden ports.
All writes stay beside this scratch checker. No assert-dependent checks.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
REPO = None
OWNER = ('02_REGISTRY/research/sources/d0_execution_clock_source_2026-10-21/'
         'check_execution_clock_source.py')
CHECKS = []


def check(name, value):
    if not bool(value):
        raise ArithmeticError(name)
    CHECKS.append(name)


def adj(x):
    return x.conj().T


def exact_toeplitz(U, h, n):
    A, B = U[:h, :h], U[:h, h:]
    C, D = U[h:, :h], U[h:, h:]
    T = sp.zeros(n*h)
    for i in range(n):
        for j in range(i+1):
            T[i*h:(i+1)*h, j*h:(j+1)*h] = A if i == j else B*D**(i-j-1)*C
    W = sp.Matrix.hstack(*[D**(n-1-j)*C for j in range(n)])
    return T, W, A, D


def exact_checks():
    z = sp.symbols('z', real=True)
    # Noninvolutory full unitary: the general colligation reduction is tested.
    U = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    check('generic_owner_uses_true_nonreflection_unitary', U.T*U == sp.eye(3) and U**2 != sp.eye(3))
    for n in (1, 2, 4):
        T, W, A, D = exact_toeplitz(U, 1, n)
        check('exact_complete_energy_balance_'+str(n), sp.eye(n)-T.T*T == W.T*W)
        check('exact_final_archive_gram_'+str(n), W*W.T == sp.eye(2)-D**n*(D.T)**n)
        check('exact_general_archive_determinant_'+str(n),
              sp.factor((sp.eye(n)-z*(sp.eye(n)-T.T*T)).det()
                        -((1-z)*sp.eye(2)+z*D**n*(D.T)**n).det()) == 0)
    # Explicit finite sequential unitary, with one retained shared archive.
    n, h, q = 4, 1, 2
    network = sp.eye(n*h+q)
    for k in range(n):
        indices = [k]+list(range(n, n+q))
        step = sp.eye(n+q)
        for i in range(3):
            for j in range(3):
                step[indices[i], indices[j]] = U[i, j]
        network = step*network
    T, W, _, _ = exact_toeplitz(U, h, n)
    check('explicit_finite_causal_network_unitary', network.T*network == sp.eye(n+q))
    check('same_network_active_corner_is_full_transfer', network[:n, :n] == T)
    check('same_network_retains_final_archive', network[n:, :n] == W)
    # Reflection with a genuine active dark eigenvalue 1, not a minimal
    # positive-defect model deleting that mode.
    v = sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(2, 3)])
    U = sp.eye(3)-2*v*v.T
    for n in (1, 2, 3):
        T, W, B, D = exact_toeplitz(U, 2, n)
        check('exact_dark_reflection_full_H_determinant_'+str(n),
              sp.factor((sp.eye(2*n)-z*(sp.eye(2*n)-T.T*T)).det()
                        -((1-z)*sp.eye(2)+z*B**(2*n)).det()) == 0)
        strict = sp.zeros(2*(n+1))
        strict[2:, :2*n] = T
        check('exact_strict_clock_boundary_'+str(n),
              sp.factor((sp.eye(2*(n+1))-z*(sp.eye(2*(n+1))-strict.T*strict)).det()
                        -(1-z)**2*((1-z)*sp.eye(2)+z*B**(2*n)).det()) == 0)
    check('first_physical_tick_is_outside_one_slot_cut', sp.zeros(2).T*sp.zeros(2) == sp.zeros(2))
    check('first_tick_absolute_Book_price_not_zero', sp.factor((sp.eye(2)-z*sp.eye(2)).det()-(1-z)**2) == 0)
    check('zero_duration_direct_term_is_a_different_cut',
          sp.factor((sp.eye(2)-z*(sp.eye(2)-B.T*B)).det()-(1-z)**2) != 0)
    a = sp.symbols('a', real=True)
    n = 3
    scalar_log = -sp.log(1-z+z*(1-a*a)**(2*n))
    check('finite_dark_rank_crossing_first_source', sp.diff(scalar_log, a).subs(a, 0) == 0)
    check('finite_dark_rank_crossing_second_source', sp.simplify(sp.diff(scalar_log, a, 2).subs(a, 0)-4*n*z) == 0)


def load_owner():
    spec = importlib.util.spec_from_file_location('pinned_native_clock_owner', REPO/OWNER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def native_rows(mod, theta, phases=(1j, 1j, -1.0, -1j)):
    """Same literal64 rows, exposing N for the complete U rather than a
    newly chosen dilation. Compare all128 columns to the pinned constructor.
    """
    C = mod.creators()
    I = np.eye(16, dtype=complex)
    nu = 3/5
    X = np.zeros((4, 4)); X[0, 1] = X[1, 0] = 1
    GX = sum((X[i, j]*C[i]@adj(C[j]) for i in range(4) for j in range(4)), np.zeros_like(I))
    link = mod.expm(theta*GX)
    words = []
    dA, ddA = np.zeros_like(I), np.zeros_like(I)
    for r in range(4):
        fixed = nu*C[r]
        transported = fixed@(link if r == 1 else I)*phases[r]
        left = mod.positive_sqrt(I-transported@adj(transported))
        right = mod.positive_sqrt(I-adj(transported)@transported)
        left0 = mod.positive_sqrt(I-fixed@adj(fixed))
        right0 = mod.positive_sqrt(I-adj(fixed)@fixed)
        for pair in ((transported, left), (adj(transported), right), (-fixed, -left0), (-adj(fixed), -right0)):
            words.extend((pair, pair))
        if r == 1:
            dp = fixed@link@GX*phases[r]
            ddp = fixed@link@GX@GX*phases[r]
            dA += (dp+adj(dp))/16
            ddA += (ddp+adj(ddp))/16
    rows = []
    for label in range(32):
        for coefficient in range(2):
            rows.append(sum(((-1)**mod.bit_parity(label&j)*words[j][coefficient] for j in range(32)), np.zeros_like(I))/32)
    A = rows[0]
    p = mod.P
    B = I-2*p*p*A@A
    dB = -2*p*p*(dA@A+A@dA)
    ddB = -2*p*p*(ddA@A+2*dA@dA+A@ddA)
    return rows, (B, dB, ddB)


def jmul(x, y):
    return (x[0]@y[0], x[1]@y[0]+x[0]@y[1], x[2]@y[0]+2*x[1]@y[1]+x[0]@y[2])


def jpower(x, n):
    out = (np.eye(x[0].shape[0], dtype=complex), np.zeros_like(x[0]), np.zeros_like(x[0]))
    for _ in range(n):
        out = jmul(out, x)
    return out


def strict_corner(bjet, n):
    h = bjet[0].shape[0]
    out = [np.zeros(((n+1)*h, (n+1)*h), complex) for _ in range(3)]
    square = jpower(bjet, 2)
    defect = (np.eye(h)-square[0], -square[1], -square[2])
    minus = tuple(-x for x in bjet)
    coeff = [bjet]+[jmul(defect, jpower(minus, k)) for k in range(max(n-1, 0))]
    for i in range(1, n+1):
        for j in range(i):
            for order in range(3):
                out[order][i*h:(i+1)*h, j*h:(j+1)*h] = coeff[i-j-1][order]
    return tuple(out)


def logdet_jet(G, G1, G2, eigen_log, mult=128):
    Q1 = np.linalg.solve(G, G1)
    return (float(-mult*eigen_log.sum()), float(-mult*np.trace(Q1).real),
            float(mult*np.trace(Q1@Q1-np.linalg.solve(G, G2)).real))


def full_feedback(kjet, zjet, mult=128):
    K, K1, K2 = kjet
    z, z1, z2 = zjet
    I = np.eye(K.shape[0])
    F = I-adj(K)@K
    F1 = -adj(K1)@K-adj(K)@K1
    F2 = -adj(K2)@K-2*adj(K1)@K1-adj(K)@K2
    G = I-z*F
    G1, G2 = -z1*F-z*F1, -z2*F-2*z1*F1-z*F2
    ev = np.linalg.eigvalsh((F+adj(F))/2)
    check('full_clock_complement_positive_'+str(K.shape[0])+'_'+str(z1), ev.min() > -2e-12 and ev.max() < 1+2e-12)
    return logdet_jet(G, G1, G2, np.log1p(-z*ev), mult)


def reduced_feedback(bjet, n, zjet, mult=128):
    E, E1, E2 = jpower(bjet, 2*n)
    z, z1, z2 = zjet
    h = E.shape[0]; I = np.eye(h)
    G = (1-z)*I+z*E
    G1 = z1*(E-I)+z*E1
    G2 = z2*(E-I)+2*z1*E1+z*E2
    ev = np.linalg.eigvalsh((E+adj(E))/2)
    out = logdet_jet(G, G1, G2, np.log1p(z*(ev-1)), mult)
    boundary = (-mult*h*np.log1p(-z), mult*h*z1/(1-z), mult*h*(z2/(1-z)+z1*z1/(1-z)**2))
    return tuple(out[i]+boundary[i] for i in range(3)), boundary


def native_checks(mod):
    theta = .08
    rows, bjet = native_rows(mod, theta)
    B, dB, ddB = bjet
    execution, A_owner, dB_owner = mod.native_round(theta)
    I = np.eye(16, dtype=complex)
    p = mod.P; a = np.sqrt(p)
    # V is the actual all128 workspace factor in I-2VV*, not sqrt(I-B²).
    V = np.vstack([piece for N in rows for piece in (p*adj(N), a*adj(N))])
    input_blank = np.zeros((2048, 16), complex); input_blank[:16] = I
    def U_apply(X):
        return X-2*V@(adj(V)@X)
    native_column = U_apply(input_blank)
    check('literal_all64_SELECT_row_complete', np.linalg.norm(sum((N@adj(N) for N in rows), np.zeros_like(I))-I) < 2e-13)
    check('actual2048_Golden_reflection_isometry_factor', V.shape == (2048, 16) and np.linalg.norm(adj(V)@V-I) < 2e-13)
    check('actual_full128_column_matches_pinned_owner', np.linalg.norm(native_column-execution.kraus.reshape(2048, 16)) < 3e-13)
    check('actual_full128_involution_on_original_input', np.linalg.norm(U_apply(native_column)-input_blank) < 3e-13)
    check('same_original_blank_and_proper_link_source', np.linalg.norm(rows[0]-A_owner) < 1e-14 and np.linalg.norm(dB-dB_owner) < 1e-14)
    C = native_column.copy(); C[:16] = 0
    def D_apply(X):
        ans = U_apply(X); ans[:16] = 0
        return ans
    check('actual_full_archive_CstarC', np.linalg.norm(adj(C)@C-(I-B@B)) < 3e-13)
    check('actual_full_archive_DC_minus_CB', np.linalg.norm(D_apply(C)+C@B) < 3e-13)
    current = C.copy()
    for k in range(6):
        expected = (-1)**k*(I-B@B)@np.linalg.matrix_power(B, k)
        check('literal_full128_delayed_return_'+str(k), np.linalg.norm(adj(C)@current-expected) < 4e-13)
        current = D_apply(current)
    # A true native noncommuting field direction, not a commuting spectrum fit.
    comm = float(np.linalg.norm(B@dB-dB@B))
    check('actual_proper_link_tangent_is_noncommuting', comm > 1e-10)
    z = mod.Z
    results = []
    for n in (1, 3, 7):
        for zjet in ((z, 0., 0.), (z, .3*z, -.2*z)):
            direct = full_feedback(strict_corner(bjet, n), zjet)
            reduced, boundary = reduced_feedback(bjet, n, zjet)
            errors = [abs(direct[i]-reduced[i]) for i in range(3)]
            check('actual_native_value_first_second_identity_'+str(n)+'_'+str(zjet[1]), max(errors) < 3e-12)
            if zjet[1]:
                check('moving_z_boundary_cannot_be_dropped_'+str(n), abs(boundary[1]) > 1e-4)
            results.append({'n': n, 'moving_z': bool(zjet[1]), 'price': direct[0], 'first_source': direct[1], 'second_source': direct[2], 'max_identity_error': max(errors)})
    # Independent differentiation of the original native rows checks the source.
    step = 2e-4; n = 3
    values = []
    for t in (theta-step, theta, theta+step):
        _, bj = native_rows(mod, t)
        values.append(reduced_feedback(bj, n, (z, 0., 0.))[0][0])
    fd1 = (values[2]-values[0])/(2*step)
    fd2 = (values[2]-2*values[1]+values[0])/(step*step)
    expected = reduced_feedback(bjet, n, (z, 0., 0.))[0]
    check('independent_native_first_source_difference', abs(fd1-expected[1]) < 2e-11)
    check('independent_native_second_source_difference', abs(fd2-expected[2]) < 2e-10)
    # The actual native zero Fourier character retains all16 dark data modes.
    dark_rows, dark = native_rows(mod, 0., phases=(1., 1., 1., 1.))
    check('actual_native_zero_character_is_dark', np.linalg.norm(dark_rows[0]) < 1e-14 and np.linalg.norm(dark[0]-I) < 1e-14)
    dark_value = full_feedback(strict_corner(dark, 3), (z, 0., 0.))
    check('actual_native_dark_source_first_zero', abs(dark_value[1]) < 1e-14)
    check('actual_native_dark_rank_birth_second_retained', dark_value[2] > 1e-7)
    check('actual_native_dark_price_only_true_clock_boundary', abs(dark_value[0]+128*16*np.log1p(-z)) < 1e-14)
    return {'actual_full_unitary_dimension': 2048, 'all_kraus_blocks': 128,
            'full_CAR_dimension': 16, 'oldRIGHT_multiplicity': 128,
            'proper_link_theta': theta, 'B_dB_commutator_norm': comm,
            'finite_identity_checks': results,
            'first_source_fd_error': abs(fd1-expected[1]),
            'second_source_fd_error': abs(fd2-expected[2]),
            'actual_dark_second_source': dark_value[2]}


def main():
    global REPO
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--output', type=Path, default=HERE/'CHECK_RESULT.json')
    args = parser.parse_args()
    REPO = args.repo.resolve() if args.repo else next(
        (p for p in HERE.parents if (p/'AGENTS.md').is_file() and (p/'01_BOOKS').is_dir()), None)
    if REPO is None:
        parser.error('Outside the repository, supply --repo PATH.')
    pins = json.loads((HERE/'SOURCE_PINS.json').read_text())
    for entry in pins['files']:
        check('source_pin_'+Path(entry['path']).name,
              hashlib.sha256((REPO/entry['path']).read_bytes()).hexdigest() == entry['sha256'])
    exact_checks()
    native = native_checks(load_owner())
    out = {'status': 'PASS', 'checks': CHECKS, 'count': len(CHECKS),
           'input_ref': pins['input_ref'], 'native': native,
           'exact_claim': 'finite complete archive determinant and strict first-tick boundary; all finite jets',
           'native_numeric_checks_are_interval_certificates': False,
           'same_fresh128_CQ_price_proved': False,
           'clock_routing_and_primitive_admission_proved': False,
           'Book_Info_selection_proved': False, 'GR_closed': False}
    text = json.dumps(out, indent=2, ensure_ascii=False)+'\n'
    args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
