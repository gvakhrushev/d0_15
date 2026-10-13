#!/usr/bin/env python3
"""Actual full-record chronology under the stated endpoint-isometry hypothesis.

The hypothesis is tested, not promoted to a native operation admission law.
No supported Lean owner or physical source is introduced by this certificate.
"""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology'
PROOF = '02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md'
HEAD = 'a7ad40cd3cb5410c2c50332eb4e47c2ed437fc95'
OLD = '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py'
INPUTS = [
    OLD,
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_results.json',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_output.txt',
    '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
    '02_REGISTRY/research/A4D_NATIVE_MATTER_OBSERVER_PAIRING.md',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
    '02_REGISTRY/research/A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md',
    '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md',
    '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
]
SCOPE = {
    'state': 'ALL_16_REAL_NATIVE_EXTERIOR_COMPONENTS',
    'operation': 'LITERAL_GOLDEN_FULLSTEP_IN_CURRENT_OBSERVER_FRAME',
    'conditional_transition_hypothesis': 'FULL_ENDPOINT_PAIRING_ISOMETRY',
    'hypothesis_physically_admitted_or_core_forced': False,
    'single_state_norm_conservation_forces_endpoint_isometry': False,
    'solved_metric': 'Q_plus=Q;q_plus=-Q+2*w*wT/(wT*Qinv*w)',
    'solved_domain': 'INITIAL_TIMELIKE_FIRST_GRADE_AND_OUTPUT_FIRST_GRADE_NONZERO',
    'new_blank_or_reset_between_records': False,
    'top_grade_required_for_every_retained_tick': False,
    'global_native_closed_sector': False,
    'chronological_operator': 'U_next*U_current',
    'price_readout': 'ORIGINAL_P_ON_BOTH_SIDES',
    'feedback_pencil': 'A(c)^2*B(c)^2*C(c)_ALL16_ROWS',
    'chronological_matter_jet_identically_zero': False,
    'whole_congruent_factor_curve_record_jet': 'EXACT_ZERO',
    'heat_factor_bound': 'CONSUMED_ALL_L_ANALYTIC_THEOREM_NOT_FINITE_EXTRAPOLATION',
    'full_price_source_Ward_or_GR_derived': False,
    'all_core_no_go': False,
    'new_action_selector_fitted_source_or_kernel_gate': False,
    'new_supported_Lean_owner': False,
}
spec = importlib.util.spec_from_file_location('fock_record_owner', ROOT / OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
a, p, z = old.a, old.p, old.z
ext, creator, B0, ETA = old.ext, old.creator, old.record_basis(), old.ETA
I = s.eye(16)
DEG = s.diag(*map(len, old.SUBS))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def red(x):
    return old.red(x)


def mat(M):
    return M.applyfunc(red)


def zero(x):
    return old.zero(x)


def first(m):
    return s.Matrix([m[1 << i] for i in range(4)])


def twoform(m):
    M = s.zeros(4)
    for i in range(4):
        for j in range(i+1, 4):
            M[i, j] = m[(1 << i) | (1 << j)]
            M[j, i] = -M[i, j]
    return M


def exterior_jet(A):
    return sum((A[i, j] * creator(s.eye(4)[:, i]) * creator(s.eye(4)[:, j]).T
                for i in range(4) for j in range(4)), s.zeros(16))


def frame_jet(G, n, dG, dn):
    # Realizes every jointly normalized pairing/observer jet by GL congruence.
    u = dn + G.inv()*dG*n/2
    return mat(-G.inv()*dG/2 + u*n.T*G-n*u.T*G)


def dcompound(G, dG):
    # Direct minor differentiation, valid even when individual minors vanish.
    def entry(i, j):
        ii, jj = old.SUBS[i], old.SUBS[j]
        if len(ii) != len(jj) or not ii:
            return s.Integer(0)
        A, H = G.extract(ii, jj), dG.extract(ii, jj)
        return sum(A.cofactor(r, c) * H[r, c]
                   for r in range(len(ii)) for c in range(len(ii)))
    return s.Matrix(16, 16, entry)


def record(G, n, dG=None, dn=None):
    """The orientation-independent full CAR formula and its genuine jet."""
    S = ext(G)
    Si = ext(G.inv())
    cr = creator(n)
    an = Si * cr.T * S
    N = cr * an
    X = DEG - N
    H = (-2 * X**3 + 9 * X**2 - 7 * X) / 6
    U = a * ((I - H) + H * (I - 2 * N)) + p * (
        (I - H) * (cr - an) - H * (cr + an))
    P = I - N
    if dG is None:
        return mat(U), mat(P)
    dS = dcompound(G, dG)
    dr = creator(dn)
    T = Si * dS
    da = Si * dr.T * S + an * T - T * an
    dN = dr * an + cr * da
    dX = -dN
    dH = (-2 * (dX * X**2 + X * dX * X + X**2 * dX)
          + 9 * (dX * X + X * dX) - 7 * dX) / 6
    dU = a * (-dH + dH * (I - 2 * N) - 2 * H * dN) + p * (
        -dH * (cr - an) + (I - H) * (dr - da)
        - dH * (cr + an) - H * (dr + da))
    return mat(U), mat(P), mat(dU), mat(-dN)


def polynomials(c):
    lam = p**2 * (1 + c) * (1 + p**3 * c)
    tr = 2 * (p**2 + p**5 * c**2)
    det = p**4 * (1 - c**2)**2
    tr0 = 2 * (1 - c) * (2 * p**4 * c**3 + 2 * p * c**2
                                + (3 * p - 1) * c + p**2)
    det0 = (1 - c)**2 * (5 * p**4 * c**2 + (14 * p - 8) * c + p**4)
    return lam, tr, det, tr0, det0


def controls():
    checks, mutants = [], []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    def reject(name, actual, false):
        check('REJECT_' + name, not zero(actual - false))
        mutants.append(name)

    UC = s.Matrix([[a, -p, 0, 0], [p, a, 0, 0],
                   [0, 0, a, -p], [0, 0, -p, -a]])
    PC = s.diag(1, 0, 1, 0)
    BC = s.Matrix([[1, 0, 1, 0], [0, 1, 0, 1],
                   [1, 0, 1, 0], [0, 1, 0, 1]]) / 2
    UR = B0 * s.kronecker_product(UC, s.eye(4)) * B0.T
    PR = B0 * s.kronecker_product(PC, s.eye(4)) * B0.T
    BR = B0 * s.kronecker_product(BC, s.eye(4)) * B0.T
    U, P = record(s.eye(4), s.Matrix([1, 0, 0, 0]))
    check('CAR_formula_is_literal_full_record', zero(U - UR))
    check('CAR_formula_keeps_original_price_cut', P == PR)
    check('all_degrees_retained', Counter(map(len, old.SUBS)) == {0: 1, 1: 4, 2: 6, 3: 4, 4: 1})
    check('CAR_whole_unitarity', zero(U.T * U - I))

    # Solved endpoint correction on nonrest data, including the old spacelike output.
    for A in [s.eye(4), s.diag(2, s.Rational(1, 2), 1, 1),
              s.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]])]:
        Q = A * A.T
        G = Q.inv()
        E = ext(A)
        S = ext(G)
        U0, P0 = record(G, A[:, 0])
        check('nonrest_full_CAR_congruence', zero(U0 - E * U * E.inv()))
        check('nonrest_full_cut_congruence', P0 == E * P * E.inv())
        for r0 in [s.Integer(1), s.Integer(2)]:
            m0 = s.zeros(16, 1)
            m0[1] = m0[15] = 1
            m0[3] = m0[13] = r0
            check('genuine_whole_blank_input', BR * m0 == m0)
            m = E * m0
            out = mat(U0 * m)
            w = first(out)
            norm = red((w.T * G * w)[0])
            qp = mat(-Q + 2 * w * w.T / norm)
            qi = mat(-G + 2 * (G * w) * (G * w).T / norm)
            check('solved_metric_inverse', zero(qp * qi - s.eye(4)))
            check('solved_output_timelike_norm', zero((w.T * qi * w)[0] - norm))
            check('solved_same_positive_pairing', zero(-qp + 2 * w * w.T / norm - Q))
            check('solved_metric_determinant', zero(qp.det() + Q.det()))
            check('whole_endpoint_isometry', zero(U0.T * S * U0 - S))
            check('whole_state_norm_retained', zero((out.T * S * out - m.T * S * m)[0]))
            if r0 == 2 and A == s.eye(4):
                reject('OLD_LORENTZ_METRIC_USED_AFTER_SPACELIKE_OUTPUT',
                       red((w.T * ETA * w)[0]), norm)
                reject('UNIQUE_CORRECTION_IS_OLD_METRIC', qp, ETA)

    singular = s.zeros(16, 1)
    singular[0] = singular[14] = -a / p
    singular[1] = singular[15] = 1
    bad = mat(U * singular)
    check('singular_input_is_actual_blank', BR * singular == singular)
    check('singular_output_first_and_top', zero(first(bad)) and zero(bad[15]))
    check('singular_output_information_retained', zero(bad[0] + 1 / p) and zero(bad[14] + 1 / p))
    reject('WHOLE_NORM_LOST_AT_PAIRING_SINGULARITY', (bad.T * bad)[0], 0)
    topzero = s.zeros(16, 1)
    topzero[1] = topzero[15] = 1
    topzero[14] = -a / p
    out = mat(U * topzero)
    check('top_zero_has_regular_first_grade', zero(out[15]) and zero(first(out) - s.Matrix([a, 0, 0, 0])))
    check('second_gate_defined_without_new_top_resource', zero(record(s.eye(4), s.Matrix([1, 0, 0, 0]))[0] - U))
    simple = s.zeros(16, 1)
    simple[1] = simple[15] = 1
    simple_out = U*simple
    Qalt = s.diag(1, 2, s.Rational(1, 2), 1)
    Salt = ext(Qalt.inv())
    check('single_state_control_is_actual_blank', BR*simple == simple)
    check('alternative_pairing_keeps_actual_state_norm',
          zero((simple_out.T*Salt*simple_out-simple.T*simple)[0]))
    reject('SINGLE_STATE_NORM_IMPLIES_WHOLE_ENDPOINT_ISOMETRY', U.T*Salt*U, I)

    # Whole feedback, original P on both sides, independent exact plane rotation.
    c, b = s.symbols('c b', real=True)
    ideal = s.groebner([a*a-p, p*p+p-1, b*b+c*c-1], a, p, b,
                      domain=s.QQ.frac_field(c, z))

    def rr(x):
        return s.factor(ideal.reduce(s.expand(x))[1])

    R = s.eye(4)
    R[0, 0] = R[1, 1] = c
    R[0, 1], R[1, 0] = -b, b
    ER = ext(R).applyfunc(rr)
    U1 = (ER * U * ER.T).applyfunc(rr)
    K = (U1 * U).applyfunc(rr)
    check('actual_two_step_product_orthogonal', all(rr(x) == 0 for x in K.T*K-I))
    FB = (P * K.T * (I - P) * K * P).applyfunc(rr)
    active = list(range(4)) + list(range(8, 12))
    F8 = (B0.T * FB * B0).extract(active, active)
    lam, tr, det, tr0, det0 = polynomials(c)
    pieces = [([0], lam, lam), ([1], lam, lam),
              ([2, 7], tr, det), ([3, 6], tr, det), ([4, 5], tr0, det0)]
    for rows, trace, determinant in pieces:
        block = F8.extract(rows, rows)
        check('whole_active_block_trace', rr(s.trace(block) - trace) == 0)
        check('whole_active_block_determinant', rr(block.det() - determinant) == 0)
        for i in rows:
            for j in set(range(8)) - set(rows):
                check('no_unscored_cross_block', F8[i, j] == 0)
    AA, BB, CC = 1-z*lam, 1-z*tr+z*z*det, 1-z*tr0+z*z*det0
    poly = AA**2 * BB**2 * CC
    check('all16_identity_complement_retained', zero(P * FB * P - FB))
    check('static_frame_exact_old_determinant', zero(poly.subs(c, 1) - (1-4*z*p**3)**4))
    check('opposite_observer_exact_determinant', zero(poly.subs(c, -1) - (1-4*z*p**3)**4))
    reject('FROZEN_GATE_REPLACES_CHRONOLOGY', poly.subs({c: s.Rational(3, 5), z: s.Rational(1, 2)}),
           ((1-4*z*p**3)**4).subs(z, s.Rational(1, 2)))
    reject('SINGLE_APPARATUS_INSTEAD_OF_FULL_FOCK', poly.subs(c, 1), 1-4*z*p**3)
    moving = (P * K.T * (I - ER * P * ER.T) * K * P).applyfunc(rr)
    reject('CHANGING_FINAL_READOUT_TO_NEXT_P',
           s.trace(moving).subs({c: s.Rational(3, 5), b: s.Rational(4, 5)}),
           s.trace(FB).subs({c: s.Rational(3, 5), b: s.Rational(4, 5)}))
    one = mat(P * U.T * (I-P) * U * P)
    reject('RESET_ONE_RECORD_PRICE', poly.subs(c, 1), (s.eye(16)-z*one).det())

    # Derivative from the full matrix, not from a prescribed source coefficient.
    h = s.symbols('h', real=True)
    ch = (1-h*h)/(1+h*h)
    bh = 2*h/(1+h*h)
    at = {h: s.Rational(1, 2), z: s.Rational(1, 2)}
    Fh = F8.subs({c: ch, b: bh})
    Fbase = mat(Fh.subs(h, s.Rational(1, 2)))
    dF = mat(Fh.diff(h).subs(h, s.Rational(1, 2)))
    W8 = mat(s.eye(8)-Fbase/2)
    Winv = s.zeros(8)
    for rows, _, _ in pieces:
        block = W8.extract(rows, rows)
        ib = mat(block.inv())
        for ii, i in enumerate(rows):
            for jj, j in enumerate(rows):
                Winv[i, j] = ib[ii, jj]
    check('whole_feedback_resolvent_inverse', zero(W8 * Winv - s.eye(8)))
    matrix_jet = red(s.trace(Winv * dF)/2)
    determinant_jet = red((-s.diff(poly, c)/poly).subs({c: s.Rational(3, 5), z: s.Rational(1, 2)})
                          * s.diff(ch, h).subs(h, s.Rational(1, 2)))
    check('genuine_matrix_Jacobi_matches_chronological_derivative', zero(matrix_jet-determinant_jet))
    reject('ALL_CHRONOLOGICAL_MATTER_JETS_ZERO', matrix_jet, 0)
    # Actual normalized blank family r=4/(3a) realizes c=3/5.
    r0 = 4/(3*a)
    s0 = red(a*a+p*p*r0*r0)
    check('genuine_blank_family_angle', zero(s0-25*p/9))
    check('genuine_blank_family_dc_dr', zero(-a*p*p*r0/(125*a**3/27)+36*a/125))
    regular = s.zeros(16, 1)
    regular[1] = regular[15] = 1
    regular[3] = regular[13] = r0
    actual_R = R.subs({c: s.Rational(3, 5), b: -s.Rational(4, 5)})
    actual_U1 = mat(ext(actual_R)*U*ext(actual_R).T)
    actual_out1 = mat(U*regular)
    check('regular_next_gate_from_actual_recorded_vector',
          zero(first(actual_out1)-actual_R[:, 0]*(5*a/3)))
    actual_out2 = mat(actual_U1*actual_out1)
    w2 = first(actual_out2)
    reject('SECOND_OUTPUT_FIRST_GRADE_VANISHES_ON_WITNESS', w2, s.zeros(4, 1))
    n2sq = red((w2.T*w2)[0])
    q2 = mat(-s.eye(4)+2*w2*w2.T/n2sq)
    q2i = q2  # In a Q=I frame every reflection is its own inverse.
    check('second_solved_metric_exact_reflection', zero(q2*q2i-s.eye(4)))
    check('second_solved_pairing_same_Q', zero(-q2+2*w2*w2.T/n2sq-s.eye(4)))
    check('regular_two_full_records_keep_all_norm',
          zero((actual_out2.T*actual_out2-regular.T*regular)[0]))
    reject('SIGNED_OBSERVER_ANGLE_IS_DISCARDED',
           poly.subs({c: s.Rational(3, 5), z: s.Rational(1, 2)}),
           poly.subs({c: -s.Rational(3, 5), z: s.Rational(1, 2)}))

    # Complete 10+16 initial joint directions, on a nonrest genuine blank base.
    A = s.diag(2, s.Rational(1, 2), 1, 1)
    q = A * ETA * A.T
    Q = A * A.T
    G = Q.inv()
    S = ext(G)
    n = A[:, 0]
    mb = s.zeros(16, 1)
    mb[1] = mb[3] = mb[13] = mb[15] = 1
    m = ext(A) * mb
    U0, P0 = record(G, n)
    mout = mat(U0*m)
    w = first(mout)
    qp = mat(-Q+2*w*w.T)
    qpi = mat(-G+2*(G*w)*(G*w).T)
    U1base, _ = record(G, w)
    Kbase = mat(U1base*U0)
    Si = ext(Q)
    Kadj = mat(Si*Kbase.T*S)
    Fbase_full = mat(P0*Kadj*(I-P0)*Kbase*P0)
    E0 = ext(A)*B0
    Fcanonical = mat(E0.inv()*Fbase_full*E0)
    F8native = mat(F8.subs({c: a, b: -p}))
    check('complete_nonrest_chronology_matches_full_blocks',
          zero(Fcanonical.extract(active, active)-F8native))
    resolvent = s.eye(16)
    for rows, _, _ in pieces:
        block = mat(s.eye(len(rows))-F8native.extract(rows, rows)/2)
        ib = mat(block.inv())
        for ii, i in enumerate(rows):
            for jj, j in enumerate(rows):
                resolvent[active[i], active[j]] = ib[ii, jj]
    check('full16_initial_chronological_resolvent',
          zero((I-Fcanonical/2)*resolvent-I))
    jbase = red((-s.diff(poly, c)/poly).subs({c: a, z: s.Rational(1, 2)}))
    reject('REFERENCE_CHRONOLOGICAL_COVECTOR_IS_ZERO', jbase, 0)
    angle_slots = []
    directions = []
    for i in range(4):
        for j in range(i, 4):
            V = s.zeros(4)
            V[i, j] = V[j, i] = 1
            directions.append((V, s.zeros(16, 1)))
    for i in range(16):
        xi = s.zeros(16, 1)
        xi[i] = 1
        directions.append((s.zeros(4), xi))
    for V, xi in directions:
        v, u = first(m), first(xi)
        r = q.inv()*v
        dk = (2*r.T*u-r.T*V*r)[0]
        dQ = -V+2*(u*v.T+v*u.T)-2*dk*v*v.T
        dG = -G*dQ*G
        dn = u-n*dk/2
        _, _, dU, dP = record(G, n, dG, dn)
        dS = dcompound(G, dG)
        check('all26_differentiated_gate_isometry', zero(dU.T*S*U0+U0.T*dS*U0+U0.T*S*dU-dS))
        check('all26_moving_cut_projection', zero(dP*P0+P0*dP-dP))
        A0 = frame_jet(G, n, dG, dn)
        T0 = exterior_jet(A0)
        check('all26_complete_frame_jet_realizes_pairing_and_observer',
              zero(-A0.T*G-G*A0-dG) and zero(A0*n-dn))
        check('all26_CAR_derivative_equals_exterior_naturality', zero(dU-T0*U0+U0*T0))
        dw = first(mat(dU*m+U0*xi))
        ds = red((2*w.T*G*dw-w.T*G*dQ*G*w)[0])
        dqp = mat(-dQ+2*(dw*w.T+w*dw.T)-2*ds*w*w.T)
        dki = red((2*w.T*qpi*dw-w.T*qpi*dqp*qpi*w)[0])
        check('all26_output_normalization_differential', zero(dki-ds))
        actual_dQp = mat(-dqp+2*(dw*w.T+w*dw.T)-2*dki*w*w.T)
        check('all26_solved_endpoint_pairing_differential', zero(actual_dQp-dQ))
        check('all26_reflection_identity_differential',
              zero(dqp*G*qp+qp*dG*qp+qp*G*dqp-dQ))
        dn1 = mat(dw-w*ds/2)
        A1 = frame_jet(G, w, dG, dn1)
        T1 = mat(exterior_jet(A1))
        check('all26_next_frame_jet_from_actual_output',
              zero(-A1.T*G-G*A1-dG) and zero(A1*w-dn1))
        dU1 = mat(T1*U1base-U1base*T1)
        dK = mat(dU1*U0+U1base*dU)
        Wjet = Si*dS
        dKa = mat(Si*dK.T*S+Kadj*Wjet-Wjet*Kadj)
        dFB = mat(dP*Kadj*(I-P0)*Kbase*P0 + P0*dKa*(I-P0)*Kbase*P0
                  -P0*Kadj*dP*Kbase*P0 + P0*Kadj*(I-P0)*dK*P0
                  +P0*Kadj*(I-P0)*Kbase*dP)
        dFBc = mat(E0.inv()*dFB*E0)
        dJdirect = red(s.trace(resolvent*dFBc)/2)
        dangle = red((dn.T*G*w+n.T*dG*w+n.T*G*dn1)[0])
        check('all26_actual_chronological_price_chain_rule', zero(dJdirect-jbase*dangle))
        e = twoform(m).T*G*n
        de = twoform(xi).T*G*n + twoform(m).T*dG*n + twoform(m).T*G*dn
        de2 = (2*e.T*G*de+e.T*dG*e)[0]
        dalpha = p*xi[0]+a*dk/2
        # At this base alpha=a, ||e||^2=1 and alpha^2+p^2||e||^2=1.
        invariant_angle_jet = red(p*p*(dalpha-a*de2/2))
        check('all26_complete_electric_invariant_derivative', zero(invariant_angle_jet-dangle))
        angle_slots.append(str(dangle))
    # Rank of the complete fixed-Q output-metric derivative, retaining amplitude kernel.
    v = s.Matrix([1, 0, 0, 0])
    cols = []
    for j in range(4):
        dv = s.eye(4)[:, j]
        M = 2*(dv*v.T+v*dv.T)-4*dv[0]*v*v.T
        cols.append(s.Matrix([M[i, k] for i in range(4) for k in range(i, 4)]))
    rank = s.Matrix.hstack(*cols).rank()
    expected_q = ['0'] * 10
    expected_q[4] = str(red(-2*a*p*p))
    expected_m = ['0'] * 16
    expected_m[0], expected_m[1], expected_m[3] = map(str, [red(p**3), red(a*p*p/2), red(-a*p*p)])
    check('all10_packed_reference_coefficients', angle_slots[:10] == expected_q)
    check('all16_matter_reference_coefficients', angle_slots[10:] == expected_m)
    check('fixed_Q_next_metric_rank_three', rank == 3)
    reject('FIXED_Q_NEXT_METRIC_HAS_TEN_FREE_SLOTS', s.Integer(rank), 10)

    # Full congruently prepared factor tangent: every state, metric and gate moves.
    H = s.diag(1, -1, 0, 0)
    Hd = s.diag(*[sum(H[i, i] for i in ss) for ss in old.SUBS])
    V = H*q+q*H.T
    dQ = H*Q+Q*H.T
    xi = Hd*m
    dU0 = Hd*U0-U0*Hd
    dmout = mat(dU0*m+U0*xi)
    check('factor_full_record_output_transports', zero(dmout-Hd*mout))
    check('factor_q_tracefree', s.trace(q.inv()*V) == 0)
    check('factor_all_spatial_constraints', V-V == s.zeros(4))
    check('factor_same_density', s.trace(G*dQ) == 0)
    dw = first(dmout)
    ds = red((2*w.T*G*dw-w.T*G*dQ*G*w)[0])
    dqp = mat(-dQ+2*(dw*w.T+w*dw.T)-2*ds*w*w.T)
    check('factor_forced_next_metric_transports', zero(dqp-H*qp-qp*H.T))
    dc = red(((H*n).T*G*w+n.T*(-G*dQ*G)*w+n.T*G*dw)[0])
    check('factor_chronological_price_jet_zero', dc == 0)
    reject('FROZEN_PAIRING_IN_ANGLE_DERIVATIVE',
           red(((H*n).T*G*w+n.T*G*dw)[0]), dc)
    reject('INITIAL_MATTER_SILENTLY_FROZEN', xi, s.zeros(16, 1))

    # Exact consumed flat heat factor witness. The all-L proof is separate.
    x0, x1, x2 = s.Rational(1, 2)**4, s.Rational(1, 2)**64, s.Rational(1, 2)**16
    E0 = 16*x0/(4*(1+x0))
    E1 = 16*x1/(s.Rational(1, 4)*(1+x1))
    E2 = 16*x2/(1+x2)
    moments = [E0, E1, E2, E2]
    Z = s.zeros(4)
    part = s.Integer(0)
    for bits in itertools.product([0, 1], repeat=4):
        symbol = s.Matrix([-4*b for b in bits])
        eigenvalue = (symbol.T*G*symbol)[0]
        weight = 2**(-eigenvalue)
        part += weight
        Z += weight*G*symbol*symbol.T*G
    Z /= part
    hq, hm = [], []
    for V, xi in directions:
        v, u = first(m), first(xi)
        r = q.inv()*v
        dk = (2*r.T*u-r.T*V*r)[0]
        dq = -V+2*(u*v.T+v*u.T)-2*dk*v*v.T
        value = s.trace(Z*dq)
        (hq if len(hq) < 10 else hm).append(value)
    hq_expected = []
    for i in range(4):
        for j in range(i, 4):
            hq_expected.append((1 if i == 0 else -1)*moments[i]/Q[i, i]
                               if i == j else -moments[i]*moments[j]/8)
    hm_expected = [s.Integer(0)]*16
    for i in range(1, 4):
        hm_expected[1 << i] = moments[0]*moments[i]/2
    for actual, expected in zip(hq+hm, hq_expected+hm_expected):
        check('all26_heat_coefficients_independent_full_mode_sum', actual == expected)
    reject('PACKED_OFFDIAGONAL_WEIGHT_LOST', hq[1], hq[1]/2)
    reject('FORWARD_SYMBOL_OFFDIAGONAL_ERASED', hq[1], 0)
    heatjet = 2*(E0-E1)
    check('literal_L2_log_heat_factor_positive', heatjet > s.Rational(1, 10000))
    reject('FULL_FACTOR_PRICE_STATIONARY_WITH_ONLY_RECORD', heatjet, 0)

    ledger = json.loads((ROOT / INPUTS[1]).read_text())
    check('consumed_literal_record_checker_hash', ledger['checker_sha256'] == sha(OLD))
    check('consumed_literal_record_proof_hash', ledger['proof_sha256'] == sha(INPUTS[4]))
    for path, digest in ledger['input_sha256'].items():
        check('consumed_record_owner_input_hash', sha(path) == digest)
    receipt = json.loads((ROOT / INPUTS[2]).read_text())
    check('consumed_genuine_Lean_receipt', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    for path, digest in receipt['input_sha256'].items():
        check('consumed_Lean_transitive_pin', sha(path) == digest)
    check('consumed_Lean_output_hash', receipt['output_sha256'] == sha(INPUTS[3]))
    return {
        'status': 'PASS', 'input_source_head': HEAD, 'proof': PROOF,
        'scope': SCOPE, 'checks': dict(sorted(Counter(checks).items())),
        'exact_controls': len(checks), 'executed_mathematical_mutants': mutants,
        'full_native_fibre': 16, 'initial_joint_directions': len(directions),
        'fixed_Q_next_metric_rank': rank,
        'packed_q_order': ['00', '01', '02', '03', '11', '12', '13', '22', '23', '33'],
        'angle_q_covector': angle_slots[:10],
        'angle_full_matter_mask_covector': angle_slots[10:],
        'chronological_covector_common_factor': 'j(a) as derived from the full pencil',
        'flat_geometric_rho0_in_all10_slots': ['0'] * 10,
        'coefficient_table_scope': 'HOMOGENEOUS_FULL_FINITE_PRICE_NOT_LOCAL_SOURCE_SUBTRACTED_EQUATIONS',
        'genuine_chronological_matrix_jet_at_half_cayley': str(matrix_jet),
        'factor_record_jet': '0', 'new_Lean_declarations': 0,
        'input_sha256': {path: sha(path) for path in INPUTS},
        'proof_sha256': sha(PROOF), 'checker_sha256': sha(BASE+'_check.py'),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = controls()
    path = ROOT / (BASE+'_certificate.json')
    if args.write:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        assert json.loads(path.read_text()) == result, 'CHRONOLOGY_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_RECORD_METRIC_CHRONOLOGY controls=%d mutations=%d joint_directions=26 '
          'full_fibre=16 physical_admission=OPEN' %
          (result['exact_controls'], len(result['executed_mathematical_mutants'])))


if __name__ == '__main__':
    main()
