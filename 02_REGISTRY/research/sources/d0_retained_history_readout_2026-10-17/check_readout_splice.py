#!/usr/bin/env python3
"""Exact golden/registration readout splice; no imported certificate execution."""
import hashlib
import json
from pathlib import Path

import sympy as sp


SOURCE_PINS = {
    "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean":
        "76c7082b4f600f7b178579b8a2a859d6f692c96ce5a769920fb3ff427532292c",
    "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean":
        "6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7",
    "03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean":
        "955bcffc5b927faf039cb15aae13e250b71c5e7b26fa811c30c61df423c005cc",
    "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md":
        "f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c",
}


def run(repo=None):
    root = Path(repo) if repo is not None else Path(__file__).resolve().parents[4]
    checks = []

    def require(name, condition):
        if not condition:
            raise ValueError(name)
        checks.append(name)

    texts = {}
    for relative, expected in SOURCE_PINS.items():
        body = (root / relative).read_bytes()
        require("source_pin:" + relative, hashlib.sha256(body).hexdigest() == expected)
        texts[relative] = body.decode("utf-8")
    require("literal_owned_golden_gate", "def gate (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a,-p; p,a]" in texts[next(iter(SOURCE_PINS))])
    require("literal_owned_full_step", "!![a,0,-p,0; 0,a,0,-p; 0,p,0,a; p,0,a,0]" in texts["03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean"])
    register_text = texts["03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean"]
    require("literal_owned_registration", "toFun x := (x.1, Bool.xor x.1 x.2)" in register_text and "invFun x := (x.1, Bool.xor x.1 x.2)" in register_text)
    require("actual_v8_fresh_workspace_scope", "n rounds use fresh workspace without resetting old records." in texts["02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md"])

    # Q(a), a>0, a^4+a^2=1; p=a^2. No floating-point decisions.
    a, x = sp.symbols("a x", real=True)
    p = a ** 2
    modulus = a ** 4 + a ** 2 - 1

    def red(value):
        numerator, denominator = sp.fraction(sp.cancel(value))
        numerator = sp.rem(numerator, modulus, a)
        denominator = sp.rem(denominator, modulus, a)
        return sp.cancel(numerator / denominator)

    def zero(value):
        return red(value) == 0

    def matrix_zero(matrix):
        return all(zero(value) for value in matrix)

    def involution_zero(value):
        return zero(sp.rem(sp.expand(value), x ** 2 - 1, x))

    G = sp.Matrix([[a, -p], [p, a]])
    require("golden_gate_orthogonal", matrix_zero(G.T * G - sp.eye(2)))
    require("golden_port_weight", zero(p + p ** 2 - 1))
    require("golden_amplitude_nonzero", sp.rem(a ** 6, modulus, a) != 0)
    formal = G * sp.diag(1, x) * G
    k0, k1 = p - p ** 2 * x, a * p * (1 + x)
    require("general_involution_forward_word_blocks", zero(formal[0, 0] - k0) and zero(formal[1, 0] - k1))
    require("general_involution_complete_effect", involution_zero(k0 ** 2 + k1 ** 2 - 1))
    require("general_involution_exit_effect", involution_zero(k1 ** 2 - 2 * p ** 3 * (1 + x)))
    require("general_involution_charge_preserved", all(involution_zero(x * entry - entry * x) for entry in formal))

    # Literal register(a,r)=(a,r xor a), in fullStep's 00,01,10,11 order.
    C = sp.zeros(4)
    for active in range(2):
        for record in range(2):
            C[2 * active + (record ^ active), 2 * active + record] = 1
    GA = sp.kronecker_product(G, sp.eye(2))
    W_literal = sp.Matrix([[a, 0, -p, 0], [0, a, 0, -p], [0, p, 0, a], [p, 0, a, 0]])
    require("full_step_is_literal_registration_after_G", matrix_zero(C * GA - W_literal))
    require("registration_complete_involution", C.T * C == sp.eye(4) and C * C == sp.eye(4))
    V = GA * C * GA
    require("three_forward_operations_complete", matrix_zero(V.T * V - sp.eye(4)))
    X = sp.Matrix([[0, 1], [1, 0]])
    K0, K1 = V[:2, :2], V[2:, :2]
    require("actual_K0", matrix_zero(K0 - (p * sp.eye(2) - p ** 2 * X)))
    require("actual_K1", matrix_zero(K1 - a * p * (sp.eye(2) + X)))
    require("actual_charge_commutator_zero", matrix_zero(V * sp.kronecker_product(sp.eye(2), X) - sp.kronecker_product(sp.eye(2), X) * V))
    P0, P1 = sp.diag(1, 0), sp.diag(0, 1)
    effects = [K.T * P * K for K in (K0, K1) for P in (P0, P1)]
    require("all_four_joint_outcomes_complete", matrix_zero(sum(effects, sp.zeros(2)) - sp.eye(2)))
    Epair = K1.T * P0 * K1
    require("pair_effect_matrix_units", matrix_zero(Epair - p ** 3 * sp.ones(2)))
    require("pair_effect_positive_Gram", Epair == (P0 * K1).T * (P0 * K1))
    require("pair_effect_is_not_diagonal", not zero(Epair[0, 1]))
    require("no_old_address_is_a_distinct_word", not matrix_zero(C * sp.kronecker_product(sp.eye(2), P0) - sp.kronecker_product(sp.eye(2), P0) * C))

    plus = sp.ones(2) / 2
    mixed = sp.eye(2) / 2
    port1 = K1.T * K1
    require("hostile_pointer_dephasing_keeps_diagonal", plus.diagonal() == mixed.diagonal())
    require("coherence_changes_actual_port_probability", zero(sp.trace(port1 * plus) - 4 * p ** 3) and zero(sp.trace(port1 * mixed) - 2 * p ** 3))
    require("hostile_drop_coherence_is_detected", not zero(sp.trace(port1 * (plus - mixed))))

    # Arbitrary pair i!=j is a two-dimensional block of every tape size.
    # This checks the symbolic matrix-unit identity, not sampled rank growth.
    di, dj, cij = sp.symbols("d_i d_j c_ij", real=True)
    qij = p ** 3 * (di + dj + 2 * cij)
    require("all_dimensions_pair_left_inverse", zero(qij / (2 * p ** 3) - (di + dj) / 2 - cij))
    ddi, ddj, dcij = sp.symbols("dd_i dd_j dc_ij", real=True)
    dqij = p ** 3 * (ddi + ddj + 2 * dcij)
    require("all_dimensions_tangent_left_inverse", zero(dqij / (2 * p ** 3) - (ddi + ddj) / 2 - dcij))
    Aii, Ajj, Aij = sp.symbols("A_ii A_jj A_ij", real=True)
    source = (Aii - Aij) * ddi + (Ajj - Aij) * ddj + Aij * dqij / p ** 3
    require("all_dimensions_dual_source_pair_identity", zero(source - Aii * ddi - Ajj * ddj - 2 * Aij * dcij))
    require("independent_matrix_unit_coefficients", sp.diff(qij, cij) == 2 * p ** 3 and sp.diff(di, cij) == 0 and sp.diff(dj, cij) == 0)

    # Moving normalization of a genuine unnormalized real density.
    u, v, w, du, dv, dw = sp.symbols("u v w du dv dw", real=True)
    N, dN = u + w, du + dw
    raw = sp.Matrix([[u, v], [v, w]])
    draw = sp.Matrix([[du, dv], [dv, dw]])
    rho = raw / N
    drho = draw / N - raw * dN / N ** 2
    q = sp.trace(Epair * rho)
    dq_direct = sum(sp.diff(q, variable) * tangent for variable, tangent in ((u, du), (v, dv), (w, dw)))
    dq_normalized = sp.trace(Epair * draw) / N - q * dN / N
    require("moving_normalizer_full_source", zero(dq_direct - dq_normalized) and zero(dq_direct - sp.trace(Epair * drho)))
    require("normalized_density_jet_trace_zero", sp.simplify(sp.trace(drho)) == 0)
    require("left_inverse_with_moving_normalizer", zero(dq_direct / (2 * p ** 3) - (drho[0, 0] + drho[1, 1]) / 2 - drho[0, 1]))
    wrong = sp.trace(Epair * draw) / N
    witness = {u: 2, v: 1, w: 3, du: 1, dv: 0, dw: 1}
    require("hostile_frozen_normalizer_detected", not zero((dq_direct - wrong).subs(witness)))
    require("hostile_missing_factor_two_detected", not zero((dqij / p ** 3 - (ddi + ddj) - dcij).subs({ddi: 0, ddj: 0, dcij: 1})))

    # The word and the pointer effects are real; no imaginary quadrature gate.
    imaginary_pure = sp.Matrix([[sp.Rational(1, 2), -sp.I / 2], [sp.I / 2, sp.Rational(1, 2)]])
    require("imaginary_quadrature_not_read_by_this_family", all(zero(sp.trace(effect * (imaginary_pure - mixed))) for effect in effects))
    require("imaginary_blindness_is_not_equal_state", imaginary_pure != mixed and sp.trace(imaginary_pure ** 2) == 1 and sp.trace(mixed ** 2) == sp.Rational(1, 2))

    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "checks": checks,
        "source_pins": SOURCE_PINS,
        "carrier": {"old_tape_dimension": "128^n=2^(7n)", "fresh_test_port": 2, "original_data_grades": 16, "original_reference": 128},
        "word": "G_A (product_{j:t_j=1} register_{A,R_j}) G_A; 2+Hamming(t) forward operations",
        "effect": "p^3(P_i+P_j+|i><j|+|j><i|)",
        "left_inverse": "Re rho_ij=q_ij/(2p^3)-(rho_ii+rho_jj)/2",
        "scopes": {
            "all_real_symmetric_matrix_units_proved": True,
            "arbitrary_complex_POVM_generation": False,
            "old_bit_address_placement_derived": False,
            "literal_v8_fresh_schedule_extended_for_free": False,
            "test_programme_cost_or_physical_Info_selected": False,
            "old_suites_imported_or_executed": False,
            "all_native_physical_admission_or_GR_closed": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, ensure_ascii=False, indent=2))
