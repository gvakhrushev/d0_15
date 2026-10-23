#!/usr/bin/env python3
"""Bounded literal-native128 entropy tangent; no conditional-pair fiction.

The all-interval sign proof is in PROOF.md. This checker tests the literal
indices and moving-nu implementation, using the original frozen source.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
import sys

import numpy as np


SOURCE_PINS = {
    '02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py':
        'ee8de4635d24c668949ac9a0186616ab7d59f2ed',
    '02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md':
        'df8611c7fa37fa71e883831b3f01f434532d99ce',
}
CHECKS: list[str] = []


def require(ok: bool, label: str) -> None:
    if not bool(ok):
        raise ArithmeticError(label)
    CHECKS.append(label)


def main() -> None:
    source_root = (Path(sys.argv[1]) if len(sys.argv) > 1 else
                   Path(__file__).resolve().parent.parent / 'inputs')
    source_hashes = {}
    for relative, expected in SOURCE_PINS.items():
        data = (source_root / relative).read_bytes()
        actual = hashlib.sha1(
            ('blob ' + str(len(data)) + '\0').encode() + data).hexdigest()
        require(actual == expected, 'pinned source ' + relative)
        source_hashes[relative] = {
            'git_blob': actual, 'sha256': hashlib.sha256(data).hexdigest()}

    native_path = source_root / next(iter(SOURCE_PINS))
    spec = importlib.util.spec_from_file_location('entropy_native_input', native_path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load pinned native constructor')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)

    p = native.P
    phi = 1 / p
    ell = math.log(phi)
    phases = (1j, 1j, -1.0, -1j)
    cs = native.creators()
    eye = np.eye(16, dtype=complex)
    purification = np.zeros((16, 128), dtype=complex)
    purification[:, :16] = eye / 4
    require(np.linalg.norm(purification @ purification.conj().T - eye / 16) < 1e-15,
            'fixed normalized DATA16/oldRIGHT128 purification')
    require(Fraction(59, 64)**2 > Fraction(1, 2),
            'exact rational blank-dominance bound')

    def formula(nu: float):
        lam, dlam = 5 * nu * nu / 128, 10 * nu / 128
        b = math.sqrt(1 - nu * nu)
        db = -nu / b
        t, dt = np.zeros(64), np.zeros(64)
        for s in range(16):
            coefficient = (5 if (s & 2) == 0 else 3) / 128
            t[4*s], dt[4*s] = coefficient * nu * nu, 2 * coefficient * nu
        t[9], dt[9] = (1+b)**2/4, (1+b)*db/2
        for j in (13, 29, 45, 61):
            t[j], dt[j] = (1-b)**2/16, -(1-b)*db/8
        q, dq = np.zeros(128), np.zeros(128)
        for j in range(64):
            q[2*j] = 4*p**4*lam*t[j]
            q[2*j+1] = 4*p**3*lam*t[j]
            dq[2*j] = 4*p**4*(dlam*t[j]+lam*dt[j])
            dq[2*j+1] = 4*p**3*(dlam*t[j]+lam*dt[j])
        q[0] = (1-2*p*p*lam)**2
        dq[0] = -4*p*p*dlam*(1-2*p*p*lam)
        return lam, t, dt, q, dq

    def actual(nu: float):
        # The returned source is d/dtheta, not d/dnu. Do not use it here.
        kraus, _theta_jet = native.native(0.0, nu=nu, phases=phases)
        amplitudes = np.einsum('kij,jr->kir', kraus, purification)
        q = np.einsum('kir,kir->k', amplitudes.conj(), amplitudes).real
        return kraus, q

    def entropy(q: np.ndarray) -> float:
        active = q > 0
        return float(-np.dot(q[active], np.log(q[active])) / ell)

    fixtures = []
    for nu in (0.5, 0.6, 0.8):
        lam, t, dt, q, dq = formula(nu)
        kraus, actual_q = actual(nu)
        a = (nu/16) * sum(
            (c*(zeta-1)+c.conj().T*(np.conjugate(zeta)-1)
             for c, zeta in zip(cs, phases)), np.zeros_like(eye))
        require(np.linalg.norm(a@a-lam*eye) < 2e-14,
                'native scalar CAR identity at nu=' + str(nu))
        # From K_(1j)=-2p sqrt(p) N_j* A and A^-1=A/lambda.
        recovered_adj = -np.matmul(kraus[1::2], a)/(2*p*math.sqrt(p)*lam)
        recovered_t = np.einsum('kij,kij->k', recovered_adj.conj(), recovered_adj).real/16
        row_error = float(np.max(np.abs(recovered_t-t)))
        probability_error = float(np.max(np.abs(actual_q-q)))
        require(row_error < 2e-13, 'literal64 row norms and indices at nu=' + str(nu))
        require(probability_error < 2e-13,
                'literal128 full measured probabilities at nu=' + str(nu))
        active_rows = np.flatnonzero(t > 0)
        active = q > 0
        require(len(active_rows) == 21 and int(active.sum()) == 42,
                '21 positive rows and42 positive labels at nu=' + str(nu))
        require(float(np.max(np.abs(actual_q[~active]))) < 2e-26,
                'all86 identically dark outcomes retained at nu=' + str(nu))
        require(abs(t.sum()-1) < 2e-14 and abs(dt.sum()) < 2e-14,
                'complete row normalization and nu derivative at nu=' + str(nu))
        require(abs(q.sum()-1) < 2e-14 and abs(dq.sum()) < 2e-14,
                'complete outcome normalization and nu derivative at nu=' + str(nu))
        nonblank = active.copy()
        nonblank[0] = False
        require(np.all(dq[nonblank] > 0) and q[0] > 0.5,
                'strict all-positive-outcome entropy sign at nu=' + str(nu))
        derivative = float(np.dot(dq[nonblank], np.log(q[0]/q[nonblank]))/ell)
        direct_derivative = float(-np.dot(dq[active], np.log(q[active]))/ell)
        require(abs(derivative-direct_derivative) < 1e-13 and derivative > 0,
                'normalized full-entropy derivative identity at nu=' + str(nu))
        require(abs(actual_q[1::2].sum()-4*p**3*lam) < 2e-14,
                'unchanged native port-one cost mean at nu=' + str(nu))

        maximum_conditional_derivative = 0.0
        for j in active_rows:
            if j == 0:
                continue
            pair, pair_jet = q[2*j:2*j+2], dq[2*j:2*j+2]
            total, total_jet = pair.sum(), pair_jet.sum()
            conditional = pair/total
            conditional_jet = (pair_jet*total-pair*total_jet)/(total*total)
            maximum_conditional_derivative = max(maximum_conditional_derivative,
                                                 float(np.max(np.abs(conditional_jet))))
            require(np.max(np.abs(conditional-np.array([p*p, p]))) < 2e-14,
                    'fixed Golden conditional pair row=' + str(j) + ' nu=' + str(nu))
        require(maximum_conditional_derivative < 2e-13,
                'zero actual conditional-pair entropy tangent at nu=' + str(nu))
        fixtures.append({
            'nu': nu, 'lambda': lam,
            'positive_row_indices': active_rows.tolist(),
            'positive_outcome_count': int(active.sum()),
            'dark_outcome_count': int((~active).sum()),
            'max_row_norm_error': row_error,
            'max_literal_probability_error': probability_error,
            'entropy_base_phi': entropy(actual_q),
            'entropy_nu_derivative_exact_formula': derivative,
            'half_entropy_nu_derivative': derivative/2,
            'native_port_one_mean': float(actual_q[1::2].sum()),
            'maximum_conditional_pair_derivative': maximum_conditional_derivative,
        })

    nu, step = 0.5, 1e-5
    values = [entropy(actual(nu+factor*step)[1]) for factor in (-2, -1, 1, 2)]
    finite_difference = (values[0]-8*values[1]+8*values[2]-values[3])/(12*step)
    derivative = fixtures[0]['entropy_nu_derivative_exact_formula']
    require(abs(finite_difference-derivative) < 2e-8,
            'independent five-point actual-nu full128 entropy derivative')

    # The hypothetical vector conserves normalization but not the native ratio.
    bad_pair = np.array([-1.0, 1.0])
    ratio_constraint_derivative = float(bad_pair[0]-p*bad_pair[1])
    require(ratio_constraint_derivative < -1,
            'hostile (-1,+1) violates fixed native Golden pair ratio')
    require(abs(-float(np.dot(bad_pair, np.log([p*p, p])))/ell + 1) < 1e-13,
            'hypothetical pair entropy source is explicitly inadmissible')

    result = {
        'status': 'PASS_LITERAL_NATIVE128_MEASURED_ENTROPY_TANGENT',
        'source_hashes': source_hashes,
        'source_root_contract': 'frozen ../inputs by default; optional first argument overrides root',
        'checks': CHECKS, 'check_count': len(CHECKS),
        'fixed_input': {'DATA_dimension': 16, 'oldRIGHT_dimension': 128,
                        'active_Schmidt_columns': 16, 'density': 'I16/16',
                        'whole_RIGHT_Gram_fixed': True},
        'literal_family': {'theta': 0, 'phases': ['i', 'i', '-1', '-i'],
                           'varied_parameter': 'nu', 'Golden_p_fixed': True},
        'analytical_sign_domain': '0 < nu < sqrt(3)/2; proof in PROOF.md',
        'fixtures': fixtures,
        'independent_native_derivative': {'nu': nu, 'step': step,
            'five_point_derivative': finite_difference,
            'absolute_error': abs(finite_difference-derivative)},
        'hostile_conditional_pair': {'trial': [-1, 1],
            'native_ratio_constraint_derivative': ratio_constraint_derivative,
            'actual_conditional_pair_derivative': [0, 0], 'trial_is_native_tangent': False},
        'scope': {'all128_measured_labels_retained': True, 'postselection': False,
            'coherent_entropy_identification': False, 'full_spatial_DATA128_claim': False,
            'compulsory_Book03_Info_binding': False, 'physical_writer_or_controller_admission': False,
            'whole_D0_model_no_go': False, 'GR_closed': False},
    }
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
