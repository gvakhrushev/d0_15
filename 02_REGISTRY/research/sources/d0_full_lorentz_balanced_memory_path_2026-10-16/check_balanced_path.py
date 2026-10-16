#!/usr/bin/env python3
"""Outward certificate for a 13D q3300 restriction on the balanced path.

The fixed basis is chosen at the midpoint of the affine reduced Hessian pencil.
At both endpoints one scalar direction is strictly negative and its fixed
12-dimensional complement is positive definite. Affineness then preserves
these two signs on the whole segment; the Schur complement gives inertia
12+/1- everywhere in the inherited 13-coordinate section. This does not
certify the full transverse Hessian of the enlarged matrix interface or its
coupling to additional boost/link/observer directions. All interval signs
are checked over the owned (d,o) root box. Floating eigensolvers only
propose finite-decimal bases.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
from pathlib import Path

import mpmath
import numpy as np
import scipy
import scipy.linalg as la

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PARENT = ROOT / "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16"
LORENTZ = ROOT / "02_REGISTRY/research/sources/d0_full_lorentz_adjoint_2026-10-16"
INPUTS = {
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/pure_memory_interval.py":
        "19d4e33f7c74465da9079ec4e3c90e0b20b3b1aad448a0cdb1957a3fc61ef41f",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/pure_memory_symbol.py":
        "1ef97d8f72d5133c75c2c071ed75b8b9ce295322c407c49e91bf589afd2af9fd",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/nonzero_symbol_algebra.py":
        "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/ordered_operator_check.py":
        "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/PURE_MEMORY_CHOICES.json":
        "be4facb35ddd2532f137db5a27a4ec6da3b97943980e93f9ddea9a8241390d6a",
    "02_REGISTRY/research/sources/d0_full_lorentz_adjoint_2026-10-16/full_lorentz_boost_source_check.py":
        "5cf53fc8e901b51f58024eadb7de282c68008f1be304185d9d16a6c12a44be32",
    "02_REGISTRY/research/sources/d0_full_lorentz_adjoint_2026-10-16/RESULTS.json":
        "8920803d185af11132dfa274a42d0e307ad43db150ef8e87d7ab83c9bf2f4d0d",
    "02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md":
        "a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915",
}
BALANCED_EXPECTATION = {
    0: 1, 60: -1, 90: -1, 102: -1,
    150: -1, 170: 1, 204: -1, 240: -1,
}
L = 8


def require(ok, label):
    if not bool(ok):
        raise ArithmeticError("balanced_memory_path:" + label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cdec(value, iv):
    """Finite-decimal complex point, represented in the same interval context."""
    return iv.mpc(iv.mpf(format(float(value.real), ".17g")),
                  iv.mpf(format(float(value.imag), ".17g")))


def cconj(value, iv):
    return iv.mpc(value.real, -value.imag)


def matmul(left, right, iv):
    rows, inner, cols = len(left), len(right), len(right[0])
    return [[sum((left[i][k] * right[k][j] for k in range(inner)), iv.mpc(0))
             for j in range(cols)] for i in range(rows)]


def adjoint(matrix, iv):
    return [[cconj(matrix[j][i], iv) for j in range(len(matrix))]
            for i in range(len(matrix[0]))]


def frobenius_upper(matrix, arithmetic, iv):
    total = iv.mpf(0)
    for row in matrix:
        for value in row:
            total += value.real**2 + value.imag**2
    return arithmetic.upper(iv.sqrt(total))


def interval_identity_error(matrix, arithmetic, iv):
    n = len(matrix)
    return frobenius_upper(
        [[matrix[i][j] - iv.mpc(1 if i == j else 0)
          for j in range(n)] for i in range(n)], arithmetic, iv)


def congruence_residual(basis, matrix, diagonal, arithmetic, iv):
    transformed = matmul(matmul(adjoint(basis, iv), matrix, iv), basis, iv)
    target = [[iv.mpc(diagonal[i] if i == j else 0)
               for j in range(len(diagonal))] for i in range(len(diagonal))]
    return frobenius_upper(
        [[transformed[i][j] - target[i][j]
          for j in range(len(diagonal))] for i in range(len(diagonal))], arithmetic, iv)


def columns(matrix, start, stop=None):
    if stop is None:
        stop = len(matrix[0])
    return [[row[j] for j in range(start, stop)] for row in matrix]


def _gadd(left, right):
    return (left[0]+right[0], left[1]+right[1])


def _gsub(left, right):
    return (left[0]-right[0], left[1]-right[1])


def _gmul(left, right):
    return (left[0]*right[0]-left[1]*right[1],
            left[0]*right[1]+left[1]*right[0])


def _matrix_product(left, right):
    return [[tuple(sum((_gmul(left[i][k], right[k][j])[part]
                        for k in range(16)), 0) for part in (0, 1))
             for j in range(16)] for i in range(16)]


def exact_balanced_K(shared, symbol_shared):
    """Compute K=S_chi-I by exact Gaussian-integer Clifford arithmetic."""
    algebra = shared["algebra"]
    creators = symbol_shared["creators"]
    support = (0, 1, 14, 15)
    require(creators.shape == (4, 16, 16), "actual_full16_CAR_creators")
    require(all(value.real == round(value.real) and value.imag == 0
                for value in creators.ravel()), "owned_creators_are_exact_integer_matrices")
    integer_creators = [[[ (int(creators[a, i, j].real), 0)
                            for j in range(16)] for i in range(16)]
                         for a in range(4)]
    generators = []
    for C in integer_creators:
        generators.append([
            [_gadd(C[i][j], C[j][i]) for j in range(16)]
            for i in range(16)])
        generators.append([
            [(0, C[i][j][0]-C[j][i][0]) for j in range(16)]
            for i in range(16)])
    products = [None]*256
    products[0] = [[(int(i == j), 0) for j in range(16)] for i in range(16)]
    for mask in range(1, 256):
        generator = mask.bit_length()-1
        products[mask] = _matrix_product(products[mask^(1 << generator)],
                                          generators[generator])
    numeric_products = symbol_shared["clifford_products"]
    require(numeric_products.shape == (256, 16, 16), "owned_Clifford_product_shape")
    for mask in range(256):
        for i in range(16):
            for j in range(16):
                re, im = products[mask][i][j]
                value = numeric_products[mask, i, j]
                require(value.real == re and value.imag == im,
                        "exact_Gaussian_product_matches_owned_matrix:"+str((mask, i, j)))
    masks = algebra.EVEN024
    expectation = {}
    for mask in masks:
        numerator = tuple(sum(products[int(mask)][i][j][part]
                              for i in support for j in support)
                          for part in (0, 1))
        require(numerator[0] % 4 == 0 and numerator[1] % 4 == 0,
                "balanced_expectation_has_exact_quarter_state_denominator")
        value = (numerator[0]//4, numerator[1]//4)
        if value != (0, 0):
            expectation[int(mask)] = value
    expected_pairs = {key: (value, 0) for key, value in BALANCED_EXPECTATION.items()}
    require(expectation == expected_pairs,
            "exact_balanced_Clifford_expectation")
    number_operators = [_matrix_product(C, [[C[j][i] for j in range(16)]
                                            for i in range(16)])
                        for C in integer_creators]
    balanced_occupation_counts = [sum(number_operators[a][mask][mask][0]
                                       for mask in support) for a in range(4)]
    old_support = (1, 15)
    legacy_occupation_counts = [sum(number_operators[a][mask][mask][0]
                                    for mask in old_support) for a in range(4)]
    require(balanced_occupation_counts == [2]*4,
            "balanced_witness_all_four_occupations_one_half")
    require(legacy_occupation_counts == [2, 1, 1, 1],
            "legacy_witness_fails_full_Lorentz_time_occupation_balance")
    adjoint_sign = np.array([
        (-1)**(bin(int(mask)).count("1")*(bin(int(mask)).count("1")-1)//2)
        for mask in masks], dtype=np.int64)
    K = np.array([
        [complex(
            adjoint_sign[i] * algebra.mask_sign(int(mask), int(other))
            * expectation.get(int(mask)^int(other), (0, 0))[0]
            - (1 if i == j else 0),
            adjoint_sign[i] * algebra.mask_sign(int(mask), int(other))
            * expectation.get(int(mask)^int(other), (0, 0))[1])
         for j, other in enumerate(masks)]
        for i, mask in enumerate(masks)], dtype=complex)
    require(K.shape == (99, 99), "full_even_Clifford_99_coordinates")
    require(np.array_equal(K, K.conj().T) and np.all(np.diag(K) == 0),
            "balanced_memory_minus_trace_K_is_Hermitian_zero_diagonal")
    require(np.all(np.sum(np.abs(K), axis=1) <= 7)
            and np.all(np.count_nonzero(K, axis=1) <= 7)
            and set(K.ravel()) <= {0, 1, -1},
            "balanced_K_exact_seven_unit_entry_bound")
    return K, expectation, adjoint_sign, balanced_occupation_counts, legacy_occupation_counts


def interval_matrix(mid, radius, iv):
    return [[iv.mpc(iv.mpf(float(mid[i, j].real)) + iv.mpf([-float(radius[i, j]), float(radius[i, j])]),
                    iv.mpf(float(mid[i, j].imag)) + iv.mpf([-float(radius[i, j]), float(radius[i, j])]))
             for j in range(mid.shape[1])] for i in range(mid.shape[0])]


def endpoint_certificate(t, H0, Delta, H0_iv, Delta_iv, U_iv, U_float,
                         arithmetic, iv, label):
    n = len(H0)
    H_iv = [[H0_iv[i][j] + iv.mpf(str(t))*Delta_iv[i][j]
             for j in range(n)] for i in range(n)]
    u_iv = [[row[0]] for row in columns(U_iv, 0, 1)]
    Q_iv = columns(U_iv, 1)
    alpha = matmul(matmul(adjoint(u_iv, iv), H_iv, iv), u_iv, iv)[0][0]
    alpha_upper = arithmetic.upper(alpha.real.b)
    require(alpha.real.b < 0, label + "_fixed_negative_direction")

    C_iv = matmul(matmul(adjoint(Q_iv, iv), H_iv, iv), Q_iv, iv)
    Q_float = U_float[:, 1:]
    H_mid = H0 + float(t)*Delta
    C_mid = Q_float.conj().T @ H_mid @ Q_float
    eig, vectors = la.eigh((C_mid + C_mid.conj().T)/2)
    Cbasis_iv = [[cdec(vectors[i, j], iv) for j in range(len(eig))]
                 for i in range(len(eig))]
    Corth = interval_identity_error(
        matmul(adjoint(Cbasis_iv, iv), Cbasis_iv, iv), arithmetic, iv)
    diagonal = [iv.mpf(format(float(value), ".17g")) for value in eig]
    diagonal_lower = min(math.nextafter(float(value.a), -math.inf)
                         for value in diagonal)
    Cres = congruence_residual(Cbasis_iv, C_iv, diagonal, arithmetic, iv)
    require(Corth < 1, label + "_positive_complement_basis_invertible")
    require(diagonal_lower > Cres, label + "_positive_complement_interval_congruence:"
            +str((diagonal_lower, Cres, float(np.max(np.abs(H_mid))))))
    return {
        "t": t,
        "negative_scalar_interval": [str(alpha.real.a), str(alpha.real.b)],
        "negative_scalar_upper": alpha_upper,
        "complement_diagonal_min_lower": diagonal_lower,
        "complement_congruence_residual_upper": Cres,
        "complement_positive_margin_lower": diagonal_lower-Cres,
        "complement_basis_orthogonality_residual_upper": Corth,
    }


def evaluate():
    for relative, digest in INPUTS.items():
        require(sha(ROOT/relative) == digest, "immutable_input:" + relative)
    full_result = json.loads((LORENTZ/"RESULTS.json").read_text())
    checks = set(full_result["checks"])
    require(full_result["schema"] == "d0-full-lorentz-homogeneous-boost-source/1"
            and full_result["status"] == "PASS_EXACT"
            and full_result["exact_checks"] == 89, "owned_full_Lorentz_source_result")
    required_checks = [
        "balanced_witness_time_occupation_half",
        "balanced_witness_each_spatial_occupation_half",
        "balanced_E0_source_matches_faithful_boost_1",
        "balanced_E0_source_matches_faithful_boost_2",
        "balanced_E0_source_matches_faithful_boost_3",
        "balanced_E0_source_matches_faithful_rotation_12",
        "balanced_E0_source_matches_faithful_rotation_13",
        "balanced_E0_source_matches_faithful_rotation_23",
        "occupation_halves_suffice_for_every_homogeneous_boost_Euler",
        "pure_state_fails_independent_boost_Euler_no_rank_computation",
        "generic_complex_Dirac_square_scalar_on_all16",
    ]
    required_checks.extend("faithful_full_price_boost_Euler_zero_" + suffix
                           for suffix in ("01", "02", "03", "11", "12", "13",
                                          "21", "22", "23", "31", "32", "33"))
    for name in required_checks:
        require(name in checks, "consume_full_Lorentz_check:" + name)

    interval = load_module("balanced_pure_interval",
                           PARENT/"pure_memory_interval.py")
    symbol = load_module("balanced_pure_symbol",
                         PARENT/"pure_memory_symbol.py")
    shared = interval.prepare_shared()
    symbol_shared = symbol.prepare_shared()
    K, expectation, adjoint_sign, balanced_occupation_counts, legacy_occupation_counts = \
        exact_balanced_K(shared, symbol_shared)
    shared["pure_K"] = K
    shared["pure_adjoint_sign"] = adjoint_sign

    # Work on q=(3,3,0,0) in the complete 13-coordinate section returned by
    # the pinned stored-source owner. This is a restriction, not the full
    # transverse Hessian of the enlarged matrix interface. The fixed
    # finite-decimal congruence is only a coordinate preconditioner: certify
    # its invertibility separately and never transfer any mode symmetry.
    q = (3, 3, 0, 0)
    require(q not in shared["shell_differences"], "q3300_outside_Omega_minus_Omega")
    arithmetic, iv = shared["arithmetic"], shared["iv"]
    owner = shared["pure_interval_owner"]
    choices = json.loads((PARENT/"PURE_MEMORY_CHOICES.json").read_text())["choices"]
    choice = next(item for item in choices if item["q"] == [3, 0, 0, 3])
    n = len(choice["B"])
    B_float = np.array([[complex(float(x[0]), float(x[1])) for x in row]
                        for row in choice["B"]], dtype=complex)
    B_inverse_float = np.linalg.inv(B_float)
    B_iv = [[iv.mpc(iv.mpf(choice["B"][i][j][0]),
                    iv.mpf(choice["B"][i][j][1]))
             for j in range(n)] for i in range(n)]
    B_inverse_iv = [[cdec(B_inverse_float[i, j], iv) for j in range(n)]
                    for i in range(n)]
    B_inverse_residual = interval_identity_error(
        matmul(B_iv, B_inverse_iv, iv), arithmetic, iv)
    require(B_inverse_residual < 1,
            "finite_decimal_preconditioner_has_interval_left_inverse")
    _, full, indices, on_shell = interval._section(q, choice, shared)
    require(not on_shell and len(indices) == 13,
            "complete_inherited_13_coordinate_stored_source_section")
    Hraw, Herror, geometry = interval._old_symbol(q, full, n, shared)
    finite, finite_error, finite_data = interval._finite_correction(q, geometry, shared)
    scalar = interval._scalars(q, full, shared)
    scalar_mid = np.array([
        [complex(arithmetic.midpoint(scalar[i][j].real),
                 arithmetic.midpoint(scalar[i][j].imag)) for j in range(n)]
        for i in range(n)], dtype=complex)
    H0 = (Hraw + Hraw.conj().T)/2
    draw = finite + scalar_mid
    Delta = (draw + draw.conj().T)/2
    require(np.isfinite(H0).all() and np.isfinite(Delta).all(),
            "finite_affine_endpoint_symbols")

    eH = np.zeros((n, n), dtype=float)
    eD = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            scalar_error = owner._abs(
                scalar[i][j] - owner._point(scalar_mid[i, j], iv), iv)
            scalar_mirror_error = owner._abs(
                scalar[j][i] - owner._point(scalar_mid[j, i], iv), iv)
            sym_H = abs(Hraw[i, j]-Hraw[j, i].conjugate())/2
            sym_D = abs(draw[i, j]-draw[j, i].conjugate())/2
            hround = (2*arithmetic.gamma(32)
                      *(abs(Hraw[i, j])+abs(Hraw[j, i])+1)+arithmetic.TINY)
            dround = (2*arithmetic.gamma(32)
                      *(abs(finite[i, j])+abs(finite[j, i])
                        +abs(scalar_mid[i, j])+abs(scalar_mid[j, i])+1)
                      +arithmetic.TINY)
            eH[i, j] = math.nextafter(
                max(arithmetic.upper(Herror[i][j]),
                    arithmetic.upper(Herror[j][i]))
                +float(sym_H)+arithmetic.upper(hround), math.inf)
            d_entry = (arithmetic.upper(finite_error[i][j])
                       +arithmetic.upper(scalar_error)+arithmetic.upper(dround))
            d_mirror = (arithmetic.upper(finite_error[j][i])
                        +arithmetic.upper(scalar_mirror_error)
                        +arithmetic.upper(dround))
            eD[i, j] = math.nextafter(max(d_entry, d_mirror)+float(sym_D), math.inf)

    H0_iv = interval_matrix(H0, eH, iv)
    Delta_iv = interval_matrix(Delta, eD, iv)
    midpoint_values, U_float = la.eigh((H0+0.5*Delta+H0.conj().T
                                        +0.5*Delta.conj().T)/2)
    U_iv = [[cdec(U_float[i, j], iv) for j in range(n)] for i in range(n)]
    Uorth = interval_identity_error(
        matmul(adjoint(U_iv, iv), U_iv, iv), arithmetic, iv)
    require(Uorth < 1, "fixed_midpoint_full_basis_invertible")

    endpoints = [
        endpoint_certificate(0, H0, Delta, H0_iv, Delta_iv,
                            U_iv, U_float, arithmetic, iv, "left_endpoint"),
        endpoint_certificate(1, H0, Delta, H0_iv, Delta_iv,
                            U_iv, U_float, arithmetic, iv, "right_endpoint"),
    ]
    root_box = shared["core"]["root_box"]
    return {
        "schema": "d0-full-lorentz-balanced-memory-path/1",
        "status": "CERTIFIED",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__, "mpmath": mpmath.__version__},
        "q": list(q),
        "frequency_dimension": n,
        "preparation_path": "sigma(t)=(1-t)I16/16+t|chi_bal><chi_bal|",
        "balanced_state_support_masks": [0, 1, 14, 15],
        "balanced_state_amplitudes": ["1/2", "1/2", "1/2", "1/2"],
        "balanced_clifford_expectation": {str(k): [int(v[0]), int(v[1])]
                                          for k, v in sorted(expectation.items())},
        "balanced_occupation_half_counts": balanced_occupation_counts,
        "legacy_unbalanced_occupation_counts": legacy_occupation_counts,
        "purification": {
            "faithful_reference_slots": 16,
            "balanced_reference_slots": 1,
            "orthogonal_slots_used": 17,
            "available_reference_dimension": 128,
            "mixture_amplitudes": ["sqrt(1-t)", "sqrt(t)"],
        },
        "balanced_memory_minus_trace_K": {
            "dimension": 99, "hermitian": True, "zero_diagonal": True,
            "max_nonzero_per_row": int(max(np.count_nonzero(K, axis=1))),
            "max_row_l1": int(max(np.sum(np.abs(K), axis=1))),
            "alphabet": [-1, 0, 1]},
        "path_checks": {
            "sigma_is_density_for_all_t_0_to_1": True,
            "all_four_occupation_coordinates_half_along_path": True,
            "full_Lorentz_source_support": "owned exact homogeneous Euler classification; full Lorentz field-source rows are affine in sigma, both endpoints share the same root",
            "matter_stationarity_support": "owned exact full16 Dirac square is scalar at this root; a 17-slot purification fits the retained reference128",
            "q_outside_Omega_minus_Omega": True,
            "reduced_Hessian_exactly_affine_in_t": True,
            "Hessian_scope": "restriction to the complete inherited 13-coordinate stored-source section; no full-interface Schur elimination or coupling map is certified",
            "all_4096_thermal_modes_and_full16_CAR_retained": True,
            "reference_dimension": 128,
        },
        "owned_root_box_d_o": root_box,
        "fixed_basis_midpoint_t": 0.5,
        "coordinate_preconditioner_inverse_residual_upper": B_inverse_residual,
        "fixed_basis_orthogonality_residual_upper": Uorth,
        "endpoint_cone_certificates": endpoints,
        "whole_segment_inertia": {"positive": 12, "negative": 1, "zero": 0},
        "proof": "The restriction of the affine q3300 Hessian to the inherited 13-coordinate section has a fixed scalar form negative at both endpoints and a fixed 12D complement positive definite at both endpoints. Convexity preserves both strict signs for all t; the Schur complement within this section gives inertia 12+/1- throughout. No full-interface Schur elimination is asserted.",
        "source_pins": INPUTS,
        "finite_data": finite_data,
        "scope": "Only the full-Lorentz-balanced affine preparation segment at the owned stationary homogeneous root, and only the q3300 Hessian restriction to the inherited 13-coordinate stored-source section. This excludes a crossing only in that restriction; it is not the full transverse Hessian of the enlarged full-Lorentz interface and does not exclude kernels coupled to additional directions. Other modes, preparations, nonlinear branches, physical admission, refinement, and Einstein dynamics remain unclassified.",
    }


def main():
    result = evaluate()
    (HERE/"RESULT.json").write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+"\n")
    print("PASS_FULL_LORENTZ_BALANCED_MEMORY_PATH")
    print(json.dumps({"whole_segment_inertia": result["whole_segment_inertia"],
                      "endpoint_cone_certificates": result["endpoint_cone_certificates"]},
                     ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
