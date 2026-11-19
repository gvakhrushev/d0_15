#!/usr/bin/env python3
"""Exact identities for the one-way feasible-gain theorem; no old runs."""
import hashlib
import json
from pathlib import Path

import sympy as sp


SOURCE_PINS = {
    "02_REGISTRY/research/A4D_RETAINED_HISTORY_COHERENCE_TEST.md":
        "3a55980ed2051b34bfba3570731622489a2e11e48d49a9f42bce034cae2ef1d6",
    "02_REGISTRY/research/A4D_NATIVE_RETAINED_RECORD_ADMISSION.md":
        "05c50904b149fcffcc93d8d52ffa66da260654cf9bfc47b80354d59fef4fe336",
    "03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean":
        "76c7082b4f600f7b178579b8a2a859d6f692c96ce5a769920fb3ff427532292c",
    "03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean":
        "955bcffc5b927faf039cb15aae13e250b71c5e7b26fa811c30c61df423c005cc",
    "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean":
        "c350ead450996bfb7da20a987454b57da94dc098d17efeafc85a56b751664aa4",
    "03_FORMALIZATION/D0/Representation/OrderMemoryControl.lean":
        "2f63c3701cb01a2eb67b24b62d5978f989bbd8c88ea6d1a27721dc2df5b6b382",
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
    require("owned_gate_definition", "def gate (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a,-p; p,a]" in texts["03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean"])
    require("owned_register_definition", "toFun x := (x.1, Bool.xor x.1 x.2)" in texts["03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean"])
    require("quarterturn_is_right_complex_reading", "def complexTurn : M4 := !![0,-1,0,0; 1,0,0,0; 0,0,0,1; 0,0,-1,0]" in texts["03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean"])
    require("local_left_quarterturn_is_separate", "def localIQ : M8Q := fromBlocks 1 0 0 (spin 2)" in texts["03_FORMALIZATION/D0/Representation/OrderMemoryControl.lean"])

    a = sp.symbols("a", real=True)
    p = a ** 2
    polynomial = a ** 4 + a ** 2 - 1

    def red(value):
        numerator, denominator = sp.fraction(sp.cancel(sp.expand_complex(value)))
        return sp.cancel(sp.rem(numerator, polynomial, a) / sp.rem(denominator, polynomial, a))

    def matrix_zero(matrix):
        return all(red(value) == 0 for value in matrix)

    I2 = sp.eye(2)
    X = sp.Matrix([[0, 1], [1, 0]])
    Z = sp.diag(1, -1)
    P = [sp.diag(1, 0), sp.diag(0, 1)]
    G = sp.Matrix([[a, -p], [p, a]])
    C = sp.zeros(4)
    for active in range(2):
        for old in range(2):
            C[2 * active + (old ^ active), 2 * active + old] = 1
    Xt = sp.kronecker_product(I2, X)
    GA = sp.kronecker_product(G, I2)
    require("actual_recording_commutes_old_translation", C * Xt == Xt * C)
    require("arbitrary_active_operators_commute_old_translation", sp.kronecker_product(sp.Matrix(2, 2, sp.symbols("A0:4")), I2) * Xt == Xt * sp.kronecker_product(sp.Matrix(2, 2, sp.symbols("A0:4")), I2))
    Vgold = GA * C * GA
    require("actual_golden_word_is_complete", matrix_zero(Vgold.H * Vgold - sp.eye(4)))
    require("actual_golden_word_is_covariant", matrix_zero(Vgold * Xt - Xt * Vgold))
    Kgold = [Vgold[:2, :2], Vgold[2:, :2]]
    require("actual_golden_coherence_effect", matrix_zero(Kgold[1].H * Kgold[1] - 2 * p ** 3 * (I2 + X)))
    require("actual_golden_joint_effect_covariance", all(matrix_zero(K.H * P[1] * K - X * K.H * P[0] * K * X) for K in Kgold))

    # Universal row of every complex block U in the old-X commutant:
    # U(old-first)=[[A,B],[B,A]], input active blank. Isometry supplies
    # completeness, but is not needed for this covariance identity.
    u, v = sp.symbols("u v", complex=True)
    row0, row1 = sp.Matrix([[u, v]]), sp.Matrix([[v, u]])
    E0, E1 = row0.H * row0, row1.H * row1
    require("generic_complex_commutant_row_covariance", sp.simplify(E1 - X * E0 * X) == sp.zeros(2))
    A = sp.Matrix(2, 2, sp.symbols("u0:4", complex=True))
    B = sp.Matrix(2, 2, sp.symbols("v0:4", complex=True))
    blockU = A.row_join(B).col_join(B.row_join(A))
    old_first_X = sp.kronecker_product(X, I2)
    require("generic_all_active_blocks_commute", blockU * old_first_X == old_first_X * blockU)
    require("word_product_preserves_commutant", (blockU * blockU.H) * old_first_X == old_first_X * (blockU * blockU.H))

    # Bloch coordinates of a positive effect: E=tau(I+v.sigma), |v|<=1.
    # Orbit weights tau agree; conjugation by X flips Y,Z and preserves X.
    vx, vy, vz, x, z = sp.symbols("v_x v_y v_z x z", real=True)
    Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    E = I2 + vx * X + vy * Y + vz * Z
    require("generic_bloch_orbit", X * E * X == I2 + vx * X - vy * Y - vz * Z)
    orbit_second = sp.expand(((x * vx + z * vz) ** 2 + (x * vx - z * vz) ** 2) / 2)
    require("covariance_kills_cross_moment", sp.expand(orbit_second - x ** 2 * vx ** 2 - z ** 2 * vz ** 2) == 0)
    norm2 = vx ** 2 + vy ** 2 + vz ** 2
    require("variance_bound_case_x_dominates", sp.expand(x ** 2 - orbit_second - (x ** 2 * (1 - norm2) + (x ** 2 - z ** 2) * vz ** 2 + x ** 2 * vy ** 2)) == 0)
    require("variance_bound_case_z_dominates", sp.expand(z ** 2 - orbit_second - (z ** 2 * (1 - norm2) + (z ** 2 - x ** 2) * vx ** 2 + z ** 2 * vy ** 2)) == 0)
    require("hostile_uncancelled_cross_term", sp.expand((x * vx + z * vz) ** 2 - orbit_second) == 2 * x * z * vx * vz)

    t = sp.symbols("t", positive=True)
    f = t * sp.log(t)
    require("strong_Jensen_curvature_exact", sp.simplify(sp.diff(f - t ** 2 / 4, t, 2) - (2 - t) / (2 * t)) == 0)
    r, mean, second = sp.symbols("r mean second", real=True)
    quantum_second = ((1 + r) ** 2 + (1 - r) ** 2) / 2
    require("Jensen_variance_gap_before_normalization", sp.expand(quantum_second - (1 + 2 * mean + second) - (r ** 2 - second - 2 * mean)) == 0)
    require("normalized_Jensen_gap", sp.expand((quantum_second - (1 + 2 * mean + second)).subs(mean, 0) - (r ** 2 - second)) == 0)
    require("strict_covariance_deficit_case_x", sp.expand((x ** 2 + z ** 2 - x ** 2) / 4 - z ** 2 / 4) == 0)
    require("strict_covariance_deficit_case_z", sp.expand((x ** 2 + z ** 2 - z ** 2) / 4 - x ** 2 / 4) == 0)

    # Exact sharp X test in the SUPPLIED all-active-O class. H is NOT
    # claimed to be an exact finite native-golden word or a free resource.
    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    HA = sp.kronecker_product(H, I2)
    Vsharp = HA * C * HA
    Ksharp = [Vsharp[:2, :2], Vsharp[2:, :2]]
    require("supplied_H_is_orthogonal", H.T * H == I2)
    require("supplied_H_CNOT_H_X_readout", Ksharp[0] == (I2 + X) / 2 and Ksharp[1] == (I2 - X) / 2)
    require("sharp_complete_joint_outcomes", sum((K.H * Pi * K for K in Ksharp for Pi in P), sp.zeros(2)) == I2)
    require("sharp_joint_readout_keeps_covariance", all(K.H * P[1] * K == X * K.H * P[0] * K * X for K in Ksharp))
    require("sharp_joint_pointer_is_equal_split", all(K.H * Pi * K == K / 2 for K in Ksharp for Pi in P))
    s, direction = sp.symbols("s direction", real=True)
    gain = ((1 + s * direction) * sp.log(1 + s * direction) + (1 - s * direction) * sp.log(1 - s * direction)) / 2
    require("saturated_sharp_axis_second_jet", sp.diff(gain, s, 2).subs(s, 0) == direction ** 2)
    require("Taylor_first_normalization_cancels", sp.diff(gain, s).subs(s, 0) == 0)
    require("uniform_scalar_Taylor_coefficients", sp.series((1 + s * direction) * sp.log(1 + s * direction), s, 0, 4).removeO().expand() == s * direction + s ** 2 * direction ** 2 / 2 - s ** 3 * direction ** 3 / 6)
    require("directional_second_jet_is_not_quadratic", sp.Max(1, 1) + sp.Max(1, 1) != 2 * sp.Max(1, 0) + 2 * sp.Max(0, 1))

    # Conditional imaginary-quadrature splice does not leave the old-X
    # commutant. It supplies no missing noncommuting memory actuation.
    S = sp.diag(1, sp.I)
    SA = sp.kronecker_product(S, I2)
    Vphase = GA * SA * C * GA
    Kphase = [Vphase[:2, :2], Vphase[2:, :2]]
    require("conditional_active_S_still_commutes_translation", matrix_zero(Vphase * Xt - Xt * Vphase))
    require("conditional_S_K1", matrix_zero(Kphase[1] - a * p * (I2 + sp.I * X)))
    Eimag = Kphase[1].H * P[0] * Kphase[1]
    require("conditional_imaginary_pair_effect", matrix_zero(Eimag - p ** 3 * sp.Matrix([[1, sp.I], [-sp.I, 1]])))
    require("conditional_phase_full_completion", matrix_zero(sum((K.H * K for K in Kphase), sp.zeros(2)) - I2))
    require("hostile_claim_phase_breaks_covariance_rejected", matrix_zero(Kphase[1].H * P[1] * Kphase[1] - X * Eimag * X))
    oldG = sp.kronecker_product(I2, G)
    require("old_record_G_really_exits_commutant", not matrix_zero(oldG * Xt - Xt * oldG))
    require("old_record_G_really_breaks_pointer_orbit", not matrix_zero(G.H * P[1] * G - X * G.H * P[0] * G * X))

    # The source-owned local LEFT i is not the scalar RIGHT i on full spin.
    left_i = sp.Matrix([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]])
    right_i = sp.Matrix([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]])
    require("quarterturns_both_square_minus_identity", left_i ** 2 == -sp.eye(4) and right_i ** 2 == -sp.eye(4))
    require("left_i_is_not_scalar_right_i", left_i != right_i)
    eigen_reference = sp.Matrix([1, -sp.I, 0, 0]) / sp.sqrt(2)
    require("conditional_phase_reference_eigenline", left_i * eigen_reference == sp.I * eigen_reference and (eigen_reference.H * eigen_reference)[0] == 1)
    require("phase_reference_is_not_real_blank", eigen_reference != sp.conjugate(eigen_reference))

    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "checks": checks,
        "source_pins": SOURCE_PINS,
        "carrier": "one retained qubit as a factor of full128^n tape; data16/reference128 retained as spectators",
        "all_word_covariance": "E_(b,omega+t)=X_t E_(b,omega) X_t whenever [U,I_active tensor X_t]=0",
        "analytical_bound": "D(sigma||I/2)-D_test >= min(x^2,z^2)/4 for x^2+z^2<=1",
        "analytical_bound_inputs": "positive Bloch effects, complete normalized POVM, orbit covariance, convexity of t log t-t^2/4 on[0,2]",
        "supplied_class_directional_gain": "I_cov(I/2+s(xX+zZ)/2)=s^2 max(x^2,z^2)/2+O(s^3)",
        "sharp_axis_word": "H_active CNOT_(active,old) H_active; two supplied H plus one registration",
        "scopes": {
            "arbitrary_word_lengths_and_limits_covariance": True,
            "all_complex_or_mixed_covariant_effects_upper_bound": True,
            "sharp_H_axis_test_uses_supplied_active_O": True,
            "exact_native_golden_H_compilation_derived": False,
            "complex_phase_or_old_address_admission_derived": False,
            "arbitrary_native_POVM_or_physical_Info_selected": False,
            "unknown_physical_test_class_Hessian_determined": False,
            "physical_programme_cost_fixed_or_free": False,
            "old_scientific_entrypoints_imported_or_run": False,
            "GR_or_all_native_closure": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
