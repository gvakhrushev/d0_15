#!/usr/bin/env python3
"""Outward certificate for the q=(3,3,0,0) mixed-memory crossing.

The floating eigensolver only chooses fixed decimal test bases. Every claimed
sign, complement inverse bound, and memory-direction pairing is rechecked over
the complete owned d/o root box with mpmath interval arithmetic.
No diagnostic midpoint solver or root search is consumed.
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
PINS = {
    "pure_memory_interval.py": "19d4e33f7c74465da9079ec4e3c90e0b20b3b1aad448a0cdb1957a3fc61ef41f",
    "PURE_MEMORY_CHOICES.json":
        "be4facb35ddd2532f137db5a27a4ec6da3b97943980e93f9ddea9a8241390d6a",
    "A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md":
        "a12d151ce659cc2b27ea15d6ddf2f0b8a2973f3b9348d323b32e333c2037ffde",
}


def require(ok, label):
    if not bool(ok):
        raise ArithmeticError("memory_fibre_crossing:" + label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cdec(value, iv):
    """An exact finite-decimal complex number inside the interval context."""
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


def midpoint_complex(value, arithmetic):
    return complex(arithmetic.midpoint(value.real), arithmetic.midpoint(value.imag))


def interval_box(mid, radius, iv):
    """Rectangle enclosure of a complex midpoint with a certified modulus radius."""
    radius = float(radius)
    re = iv.mpf(float(mid.real)) + iv.mpf([-radius, radius])
    im = iv.mpf(float(mid.imag)) + iv.mpf([-radius, radius])
    return iv.mpc(re, im)


def complex_interval_matrix(mid, radius, iv):
    return [[interval_box(mid[i, j], radius[i, j], iv)
             for j in range(mid.shape[1])] for i in range(mid.shape[0])]


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


def load_owner():
    interval_path = PARENT / "pure_memory_interval.py"
    choice_path = PARENT / "PURE_MEMORY_CHOICES.json"
    source_path = ROOT / "02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"
    require(sha(interval_path) == PINS["pure_memory_interval.py"], "pure_interval_source_pin")
    require(sha(source_path) == PINS["A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"],
            "nonlinear_second_jet_source_pin")
    expected_choice_hash = PINS["PURE_MEMORY_CHOICES.json"]
    require(expected_choice_hash and sha(choice_path) == expected_choice_hash,
            "pure_preconditioner_choices_pin")
    spec = importlib.util.spec_from_file_location("pinned_pure_memory_interval", interval_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    choices = json.loads(choice_path.read_text())["choices"]
    # (3,3,0,0) is carried to this spatial-S3 representative by 1<->3;
    # time coordinate 0 is fixed by the owned orbit action.
    choice = next(item for item in choices if item["q"] == [3, 0, 0, 3])
    return module, choice


def evaluate():
    module, choice = load_owner()
    shared = module.prepare_shared()
    arithmetic, iv = shared["arithmetic"], shared["iv"]
    owner = shared["pure_interval_owner"]
    q = tuple(choice["q"])
    _, full, _, _ = module._section(q, choice, shared)
    n = len(choice["B"])

    # H_0 is the complete trace-preparation reduced field Hessian. Delta is
    # its exact derivative along sigma(t)=(1-t)I/16+t|chi><chi|.
    Hraw, Herror, geometry = module._old_symbol(q, full, n, shared)
    finite, finite_error, _ = module._finite_correction(q, geometry, shared)
    scalar = module._scalars(q, full, shared)
    scalar_mid = np.array([[midpoint_complex(scalar[i][j], arithmetic)
                            for j in range(n)] for i in range(n)], dtype=complex)
    H0 = (Hraw + Hraw.conj().T) / 2
    draw = finite + scalar_mid
    Delta = (draw + draw.conj().T) / 2

    eH = np.zeros((n, n), dtype=float)
    eD = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            scalar_error = owner._abs(
                scalar[i][j] - owner._point(scalar_mid[i, j], iv), iv)
            sym_H = abs(Hraw[i, j] - Hraw[j, i].conjugate()) / 2
            sym_D = abs(draw[i, j] - draw[j, i].conjugate()) / 2
            hround = (2 * arithmetic.gamma(32) *
                      (abs(Hraw[i, j]) + abs(Hraw[j, i]) + 1) + arithmetic.TINY)
            dround = (2 * arithmetic.gamma(32) *
                      (abs(finite[i, j]) + abs(finite[j, i]) +
                       abs(scalar_mid[i, j]) + abs(scalar_mid[j, i]) + 1)
                      + arithmetic.TINY)
            # The midpoint matrices below are explicitly Hermitized. Bound
            # both entries before that averaging: the source intervals need
            # not have bitwise-identical widths in positions (i,j)/(j,i).
            h_entry = arithmetic.upper(Herror[i][j])
            h_mirror = arithmetic.upper(Herror[j][i])
            eH[i, j] = max(h_entry, h_mirror) + float(sym_H) + arithmetic.upper(hround)

            scalar_mirror_error = owner._abs(
                scalar[j][i] - owner._point(scalar_mid[j, i], iv), iv)
            d_entry = (arithmetic.upper(finite_error[i][j]) + arithmetic.upper(scalar_error)
                       + arithmetic.upper(dround))
            d_mirror = (arithmetic.upper(finite_error[j][i])
                        + arithmetic.upper(scalar_mirror_error)
                        + arithmetic.upper(dround))
            eD[i, j] = max(d_entry, d_mirror) + float(sym_D)

    H0_iv = complex_interval_matrix(H0, eH, iv)
    Delta_iv = complex_interval_matrix(Delta, eD, iv)

    def pencil_interval(t_text):
        t = iv.mpf(t_text)
        return [[H0_iv[i][j] + t * Delta_iv[i][j]
                 for j in range(n)] for i in range(n)]

    def endpoint(t_text):
        t = float(t_text)
        midpoint = H0 + t * Delta
        values, vectors = la.eigh((midpoint + midpoint.conj().T) / 2)
        basis = [[cdec(vectors[i, j], iv) for j in range(n)] for i in range(n)]
        orth_error = interval_identity_error(
            matmul(adjoint(basis, iv), basis, iv), arithmetic, iv)
        diagonal = [iv.mpf(format(float(value), ".17g")) for value in values]
        residual = congruence_residual(basis, pencil_interval(t_text), diagonal,
                                       arithmetic, iv)
        min_abs = min(abs(float(value)) for value in values) - 1e-12
        require(orth_error < 1, "endpoint_basis_invertible_" + t_text)
        require(residual < min_abs, "endpoint_inertia_interval_" + t_text)
        return {"t": t, "positive": int(sum(value > 0 for value in values)),
                "negative": int(sum(value < 0 for value in values)),
                "min_abs_midpoint_eigenvalue": min_abs,
                "basis_orthogonality_residual_upper": orth_error,
                "congruence_residual_upper": residual}

    left, right = endpoint("0.42"), endpoint("0.44")
    require(left["positive"] == 12 and left["negative"] == 1,
            "left_endpoint_inertia")
    require(right["positive"] == 11 and right["negative"] == 2,
            "right_endpoint_inertia")
    require(0 < left["t"] < right["t"] < 1,
            "crossing_segment_inside_faithful_stationary_memory_fibre")

    # A fixed unit vector close to the crossing eigendirection, normalized
    # exactly through interval sqrt. A Householder map makes its complement an
    # exact orthogonal block; interval arithmetic encloses every entry.
    center_t = 0.43
    center_mid = H0 + center_t * Delta
    center_values, center_vectors = la.eigh((center_mid + center_mid.conj().T) / 2)
    eig_index = 1
    raw = center_vectors[:, eig_index].copy()
    pivot = int(np.argmax(np.abs(raw)))
    raw *= np.exp(-1j * np.angle(raw[pivot]))
    raw[pivot] = abs(raw[pivot]) + 0j
    raw_iv = [cdec(value, iv) for value in raw]
    norm_sq = sum((cconj(value, iv) * value).real for value in raw_iv)
    u0 = [value / iv.sqrt(norm_sq) for value in raw_iv]

    v = [iv.mpc(1 if i == pivot else 0) - u0[i] for i in range(n)]
    vnorm_sq = sum((cconj(value, iv) * value).real for value in v)
    householder = [[iv.mpc(1 if i == j else 0) -
                    2 * v[i] * cconj(v[j], iv) / vnorm_sq
                    for j in range(n)] for i in range(n)]
    columns = [pivot] + [j for j in range(n) if j != pivot]
    permutation = [[iv.mpc(1 if i == columns[j] else 0)
                    for j in range(n)] for i in range(n)]
    Q = matmul(householder, permutation, iv)
    KQ = matmul(matmul(adjoint(Q, iv), pencil_interval("0.43"), iv), Q, iv)
    Cblock = [row[1:] for row in KQ[1:]]
    bblock = [KQ[i][0] for i in range(1, n)]
    bnorm = arithmetic.upper(iv.sqrt(sum((x.real**2 + x.imag**2 for x in bblock), iv.mpf(0))))

    Cmid = np.array([[midpoint_complex(value, arithmetic) for value in row]
                     for row in Cblock])
    mu, Cvectors = la.eigh((Cmid + Cmid.conj().T) / 2)
    Cbasis = [[cdec(Cvectors[i, j], iv) for j in range(n - 1)]
              for i in range(n - 1)]
    Corth = interval_identity_error(matmul(adjoint(Cbasis, iv), Cbasis, iv), arithmetic, iv)
    Cres = congruence_residual(Cbasis, Cblock,
                               [iv.mpf(format(float(value), ".17g")) for value in mu],
                               arithmetic, iv)
    mu_lower = min(abs(float(value)) for value in mu) - 1e-12
    require(Corth < 1, "center_complement_basis_invertible")
    require(Cres < mu_lower, "center_complement_uniform_inverse")
    Cinv_upper = arithmetic.upper((1 + iv.mpf(Corth)) /
                                  (iv.mpf(mu_lower) - iv.mpf(Cres)))

    # The derivative norm is certified by another fixed decimal basis; its
    # eigensolver only proposes the basis and diagonal, while interval residual
    # and near-unitarity prove the norm bound.
    Dvalues, Dvectors = la.eigh(Delta)
    Dbasis = [[cdec(Dvectors[i, j], iv) for j in range(n)] for i in range(n)]
    Dorth = interval_identity_error(matmul(adjoint(Dbasis, iv), Dbasis, iv), arithmetic, iv)
    Dres = congruence_residual(
        Dbasis, Delta_iv, [iv.mpf(format(float(value), ".17g")) for value in Dvalues],
        arithmetic, iv)
    Dnorm_upper = arithmetic.upper(
        (iv.mpf(max(abs(float(value)) for value in Dvalues) + 1e-12) + iv.mpf(Dres)) /
        (1 - iv.mpf(Dorth)))
    require(Dorth < 1, "delta_basis_invertible")

    delta = iv.mpf("0.01") * iv.mpf(Dnorm_upper)
    require(Cinv_upper * delta < 1, "root_neighborhood_preserves_complement_inverse")
    ratio = (iv.mpf(Cinv_upper) * (iv.mpf(bnorm) + delta) /
             (1 - iv.mpf(Cinv_upper) * delta))
    distance = iv.sqrt(2) * ratio
    require(distance < 0.11, "every_crossing_kernel_near_fixed_direction")

    center_slope = matmul(
        matmul([[cconj(value, iv) for value in u0]], Delta_iv, iv),
        [[value] for value in u0], iv)[0][0].real
    slope_upper = arithmetic.upper(center_slope + 2 * iv.mpf(Dnorm_upper) * distance)
    require(slope_upper < -0.8, "strict_negative_memory_fibre_pairing")

    root_box = shared["core"]["root_box"]
    return {
        "schema": "d0-memory-fibre-crossing-transversality/1",
        "checker_sha256": sha(HERE / "check_transversality.py"),
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__, "mpmath": mpmath.__version__},
        "q_original": [3, 3, 0, 0], "q_spatial_s3_representative": list(q),
        "frequency_dimension": n, "memory_path": "sigma(t)=(1-t)I16/16+t|chi><chi|",
        "preparation_rank_on_crossing_segment": 16,
        "root_box_d_o": root_box,
        "endpoint_inertia": [left, right],
        "crossing_interval": [0.42, 0.44],
        "crossing_exists_for_each_root_box_parameter_pair": True,
        "complex_fourier_kernel_dimension": 1,
        "real_q_minus_q_kernel_dimension_before_orbit_quotient": 2,
        "unique_crossing_for_each_root_box_parameter_pair": True,
        "center": {"t": center_t, "simple_eigenvalue_midpoint": float(center_values[eig_index]),
                   "complement_inverse_norm_upper": Cinv_upper,
                   "center_offdiagonal_block_norm_upper": bnorm,
                   "delta_operator_norm_upper": Dnorm_upper,
                   "max_pencil_perturbation_from_center_upper": arithmetic.upper(delta),
                   "kernel_direction_distance_upper": arithmetic.upper(distance),
                   "unit_memory_tangent_pairing_interval": [
                       math.nextafter(float(center_slope.a), -math.inf),
                       math.nextafter(float(center_slope.b), math.inf)],
                   "all_kernel_memory_tangent_pairings_upper": slope_upper},
        "second_order_memory_fibre_compatibility": "Tr((|chi><chi|-I/16) M_v)=0 is necessary",
        "second_order_jet_for_pure_q_minus_q_velocity_with_zero_first_order_memory_velocity_exists": False,
        "scope": "Only the velocity supported on the unique complex q=(3,3,0,0) Fourier crossing and its real q/-q pair, with zero first-order memory velocity, is excluded at second order on this fixed stationary preparation segment; mixed field or memory velocities and other modes are unclassified.",
        "input_sha256": {"pure_memory_interval.py": PINS["pure_memory_interval.py"],
                         "PURE_MEMORY_CHOICES.json": PINS["PURE_MEMORY_CHOICES.json"],
                         "A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md":
                             PINS["A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"]},
    }


def main():
    result = evaluate()
    output = HERE / "RESULT.json"
    output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print("PASS_MEMORY_FIBRE_CROSSING_TRANSVERSALITY")
    print(json.dumps({key: result[key] for key in
                      ("crossing_interval", "endpoint_inertia", "center")},
                     ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
