"""Validated12/8 inactive-creator restrictions at shell-transfer q.

All4096 Fourier modes,16 exterior components, occupied reference128,
heat normalizer and signed complement resolvent are retained. Numerical
eigensystems CHOOSE exact finite-decimal square preconditioners only.
Each resulting congruence is independently enclosed on the entire owned
root rectangle. A row-norm distance<1 from diag(+-1) proves its inertia.

J is root-INDEPENDENT on these actual affine inactive-role leg families.
Its only coefficient error comes from converting the fixed decimal B to
binary64. D still moves with both root parameters, and its complete CAR
geometry, phase conversion, assembly and Gram rounding errors remain.

The exact rank-T theorem is an independent consumer premise for identifying
these restrictions with kerT modulo six representation directions. This
file does not prove a nonsingular full19/21 field matrix, solve shell-density
kernel directions, choose physical gauge/admission, or change old outputs.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import time

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
L, N, DIM = 8, 4096, 16
SECTORS = (((2, 0, 0, 0), (1, 2, 3), 3), ((1, 1, 0, 0), (2, 3), 5))


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("full_shell_transfer_interval:"+label)


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE/(name+".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _choose(repo):
    diagnostic = load("full_shell_transfer_diagnostic")
    result, sectors = diagnostic.run(repo, return_data=True)
    choices = []
    for item, data in zip(result["sectors"], sectors):
        values, vectors = np.linalg.eigh(data["H"])
        require(np.min(np.abs(values)) > 1e-5, "numerical_choice_has_no_tiny_pivot")
        matrix = vectors/np.sqrt(np.abs(values))[None, :]
        exact = [[(format(z.real, ".17g"), format(z.imag, ".17g")) for z in row]
                 for row in matrix]
        choices.append({"B": exact, "signs": np.sign(values).astype(int),
                        "q": item["q"], "diagnostic": item})
    return choices


def creator_geometry(B, inactive, repo):
    """Small independent interval geometry, without geometry_bounds()."""
    iv = mp.iv
    owner = load("full_symbol_interval_geometry")
    ordered = load("ordered_operator_check")
    chart = ordered.chart_helper()
    chart.owned_definitions(repo)
    creators, order = ordered.owned_car(repo)
    count = 4*len(inactive)
    require(len(B) == count and all(len(row) == count for row in B), "square_decimal_B_shape")
    require(all(len(pair) == 2 and all(isinstance(value, str) and owner.DECIMAL.fullmatch(value)
                                      for value in pair) for row in B for pair in row),
            "exact_finite_decimal_B_entries")
    patterns = {"C": [owner._pattern(C) for C in creators],
                "I": [owner._pattern(C.T) for C in creators]}
    for family in patterns:
        supports = [{i for i, value in pattern} for pattern in patterns[family]]
        require(all(len(pattern) == 8 and all(abs(value) == 1 for _, value in pattern)
                    for pattern in patterns[family])
                and sum(map(len, supports)) == len(set.union(*supports)),
                "actual_CAR_single_signed_coordinate_entries")
    plus_iv, minus_iv, constant_iv = [], [], []
    plus0, minus0, constant0 = [], [], []
    for direction in range(count):
        p_iv, m_iv, p0, m0, c_iv, c0 = [], [], [], [], [], []
        for r in range(4):
            row = inactive.index(r)*4 if r in inactive else None
            coefficients_iv = ([iv.mpc(*B[row+j][direction]) for j in range(4)]
                               if row is not None else [iv.mpc(0)]*4)
            coefficients0 = ([mp.mpc(*B[row+j][direction]) for j in range(4)]
                              if row is not None else [mp.mpc(0)]*4)
            for family, target_iv, target0 in (("C", p_iv, p0), ("I", m_iv, m0)):
                target_iv.append(owner._matrix([(coefficients_iv[j], patterns[family][j])
                                                for j in range(4)], iv.mpc(0)))
                target0.append(owner._matrix([(coefficients0[j], patterns[family][j])
                                              for j in range(4)], mp.mpc(0)))
                c_iv.extend((-coefficients_iv[j], patterns[family][j]) for j in range(4))
                c0.extend((-coefficients0[j], patterns[family][j]) for j in range(4))
        plus_iv.append(p_iv)
        minus_iv.append(m_iv)
        constant_iv.append(owner._matrix(c_iv, iv.mpc(0)))
        plus0.append(p0)
        minus0.append(m0)
        constant0.append(owner._matrix(c0, mp.mpc(0)))
    plus, minus = (owner._numeric(values, (count, 4, 16, 16)) for values in (plus0, minus0))
    constant = owner._numeric(constant0, (count, 16, 16))
    eJ, coeff_norm = [], []
    for i in range(count):
        error = sum((owner._HS_error(values[i][r], numeric[i, r])
                     for values, numeric in ((plus_iv, plus), (minus_iv, minus))
                     for r in range(4)), iv.mpf(0))
        error += owner._HS_error(constant_iv[i], constant[i])
        eJ.append((L*error).b)
        coeff_norm.append(sum((owner._numeric_HS_upper(matrix)
                               for matrix in [*plus[i], *minus[i], constant[i]]), iv.mpf(0)).b)

    receipt = json.loads((repo/chart.RECEIPT).read_text())
    center = receipt["interval"]["root_center"]
    radius = iv.mpf(receipt["interval"]["root_radius"])
    d, o = [iv.mpf(value)+iv.mpf([-1, 1])*radius for value in center]
    ap, am = iv.sqrt(d+3*o), iv.sqrt(d-o)
    a, b = (ap+3*am)/4, (ap-am)/4
    require(b.a > 0 and (a-b).a > 0, "whole_root_box_regular")
    d0, o0 = map(mp.mpf, center)
    a0 = (mp.sqrt(d0+3*o0)+3*mp.sqrt(d0-o0))/4
    b0 = (mp.sqrt(d0+3*o0)-mp.sqrt(d0-o0))/4
    def legs_at(aa, bb):
        return [[aa if r == 0 else bb]+[-(aa if r == j+1 else bb) for j in range(3)]
                for r in range(4)]
    legs, legs0 = legs_at(a, b), legs_at(a0, b0)
    cu0 = [owner._matrix([(u[j], patterns["C"][j]) for j in range(4)], mp.mpc(0)) for u in legs0]
    iu0 = [owner._matrix([(u[j], patterns["I"][j]) for j in range(4)], mp.mpc(0)) for u in legs0]
    cu, iu = (owner._numeric(values, (4, 16, 16)) for values in (cu0, iu0))
    numeric_legs = np.array([[float(value) for value in row] for row in legs0])
    # Ddiff=C(v)+iota(bar v), so ||Ddiff||op=||v||, ||Ddiff||HS=4||v||.
    # Each phase coefficient |t-1|<=2, and all16 grades remain present.
    deltaD = (2*L*sum((owner._HS_error(u, center_u) for u, center_u in zip(legs, numeric_legs)),
                     iv.mpf(0))).b
    D_coeff = sum((owner._numeric_HS_upper(matrix) for matrix in [*cu, *iu]), iv.mpf(0)).b
    root2, root2_0 = iv.sqrt(2), mp.sqrt(2)
    roots0 = [mp.mpc(1), mp.mpc(1, 1)/root2_0, mp.j, mp.mpc(-1, 1)/root2_0,
              mp.mpc(-1), mp.mpc(-1, -1)/root2_0, -mp.j, mp.mpc(1, -1)/root2_0]
    roots = np.array([complex(value) for value in roots0])
    exact_roots = [iv.mpc(1, 0), iv.mpc(root2/2, root2/2), iv.mpc(0, 1),
                   iv.mpc(-root2/2, root2/2), iv.mpc(-1, 0),
                   iv.mpc(-root2/2, -root2/2), iv.mpc(0, -1), iv.mpc(root2/2, -root2/2)]
    phase_errors = []
    for approximate, exact in zip(roots, exact_roots):
        dr, di = iv.mpf(float(approximate.real))-exact.real, iv.mpf(float(approximate.imag))-exact.imag
        phase_errors.append(iv.sqrt(dr*dr+di*di).b)
    return {"plus": plus, "minus": minus, "constant": constant,
            "cu": cu, "iu": iu, "roots8float": roots,
            "phase_root_error_components": phase_errors,
            "eJ_geom": eJ, "coeff_norm_sum": coeff_norm,
            "deltaD_geom_op": deltaD, "deltaD_geom_F": (4*deltaD).b,
            "D_coeff_norm_sum": D_coeff,
            "metadata": {"J_coefficients_root_independent": True,
                         "D_varies_on_entire_owned_root_box": True,
                         "coefficient_float_conversion_included": True,
                         "all16_exterior_components": True,
                         "owned_exterior_order": list(order), "source_pins": chart.PINS}}


def _validate_sector(choice, weights, geometry, arithmetic):
    iv = mp.iv
    upper, midpoint, gamma = arithmetic.upper, arithmetic.midpoint, arithmetic.gamma
    positive_sum, norm_upper = arithmetic.positive_sum, arithmetic.frobenius_upper
    TINY, INFLATE = arithmetic.TINY, arithmetic.POSITIVE_INFLATION
    signs = np.array(choice["signs"], int)
    count = len(signs)
    modes, outgoing = np.array(weights["modes"], int), np.array(weights["outgoing"], int)
    require(modes.shape == (N, 4) and outgoing.shape == (N,), "all4096_mode_indices")
    tk = geometry["roots8float"][modes]
    plus, minus, constant, cu, iu = (geometry[key] for key in ("plus", "minus", "constant", "cu", "iu"))
    require(plus.shape == minus.shape == (count, 4, 16, 16)
            and constant.shape == (count, 16, 16), "all_restricted_full16_operator_slots")
    for array in (plus, minus, constant, cu, iu, tk):
        require(np.isfinite(array).all() and np.max(np.abs(array)) < 2.0**100,
                "bounded_normal_float_inputs_before_operator_assembly")
    phase_error = max(upper(value) for value in geometry["phase_root_error_components"])
    require(phase_error < 2.0**-50, "explicit_eighth_root_conversion_bound")
    D = L*(np.einsum("kr,rij->kij", tk-1, cu, optimize=False)
           +np.einsum("kr,rij->kij", tk.conj()-1, iu, optimize=False))
    eJ = np.array([upper(geometry["eJ_geom"][i]+phase_error*L*geometry["coeff_norm_sum"][i]
                         +gamma(128)*L*geometry["coeff_norm_sum"][i]+TINY) for i in range(count)])
    d_eval = phase_error*L*geometry["D_coeff_norm_sum"]+gamma(128)*2*L*geometry["D_coeff_norm_sum"]+TINY
    eD_op, eD_F = (upper(geometry[key]+d_eval) for key in ("deltaD_geom_op", "deltaD_geom_F"))
    sqrt_lam = np.array([upper(value) for value in weights["sqrt_lambda"]])
    weight_intervals = (weights["gamma_J"], weights["weight_X"])
    wJ, wX = [np.array([midpoint(value) for value in values]) for values in weight_intervals]
    dwJ, dwX = [np.array([upper(abs(value-iv.mpf(float(w)))) for value, w in zip(values, floats)])
                  for values, floats in zip(weight_intervals, (wJ, wX))]
    WJ, WX = [np.array([upper(abs(value)) for value in values]) for values in weight_intervals]
    require(all(np.isfinite(array).all() and np.max(np.abs(array)) < 2.0**100
                for array in (wJ, wX, dwJ, dwX, WJ, WX, sqrt_lam)),
            "all_spectral_factors_bounded_before_Gram_assembly")
    H = np.zeros((count, count), complex)
    nJ, nX, eX = (np.zeros((count, N)) for _ in range(3))
    for offset in range(0, N, 128):
        sl = slice(offset, offset+128)
        J = L*(np.einsum("kr,arij->akij", tk[sl], plus, optimize=False)
               +np.einsum("kr,arij->akij", tk[sl].conj(), minus, optimize=False)+constant[:, None])
        X = (np.einsum("kij,akjl->akil", D[outgoing[sl]], J, optimize=False)
             +np.einsum("akij,kjl->akil", J, D[sl], optimize=False))
        nj, nx = norm_upper(J), norm_upper(X)
        nJ[:, sl], nX[:, sl] = nj, nx
        sd = sqrt_lam[sl]+sqrt_lam[outgoing[sl]]
        # True D times J-error plus D-error times computed J; no omitted
        # cross term. The remaining budget covers complex16 multiplication.
        error = sd[None, :]*eJ[:, None]+2*eD_op*nj
        error += upper(gamma(512))*(4*sd[None, :]+2*eD_F)*nj
        eX[:, sl] = np.nextafter(error*INFLATE+TINY, np.inf)
        jf, xf = J.reshape(count, -1, 256), X.reshape(count, -1, 256)
        H += np.einsum("akn,bkn,k->ab", jf.conj(), jf, wJ[sl], optimize=False)
        H += np.einsum("akn,bkn,k->ab", xf.conj(), xf, wX[sl], optimize=False)
    absolute_Gram = positive_sum(np.abs(wJ), nJ, nJ)+positive_sum(np.abs(wX), nX, nX)
    roundoff = np.nextafter(upper(2*gamma(2**26))*absolute_Gram*INFLATE+TINY, np.inf)
    coefficient_error = np.zeros_like(roundoff)
    for dw, W, n, e in ((dwJ, WJ, nJ, np.broadcast_to(eJ[:, None], nJ.shape)), (dwX, WX, nX, eX)):
        coefficient_error += (positive_sum(dw, n, n)+positive_sum(W, e, n)
                              +positive_sum(W, n, e)+positive_sum(W, e, e))
    coefficient_error = np.nextafter(coefficient_error*INFLATE+TINY, np.inf)
    residual_rows, variation_rows, arithmetic_rows, total_rows = [], [], [], []
    for i in range(count):
        residual, variation, rounding = iv.mpf(0), iv.mpf(0), iv.mpf(0)
        for j in range(count):
            target = int(signs[i]) if i == j else 0
            residual += arithmetic.interval_complex_abs(iv.mpf(float(H[i, j].real))-target,
                                                         iv.mpf(float(H[i, j].imag)))
            variation += iv.mpf(float(coefficient_error[i, j]))
            rounding += iv.mpf(float(roundoff[i, j]))
        residual_rows.append(upper(residual))
        variation_rows.append(upper(variation))
        arithmetic_rows.append(upper(rounding))
        total_rows.append(upper(residual+variation+rounding))
    distance = max(total_rows)
    require(distance < 1, "whole_rectangle_strict_inertia_congruence")
    return {"q": list(choice["q"]), "restriction_dimension": count,
            "validated_restriction_inertia": {"positive": int(np.sum(signs > 0)),
                                               "negative": int(np.sum(signs < 0)), "zero": 0},
            "exact_decimal_preconditioner": choice["B"], "comparison_signs": signs.tolist(),
            "root_box": weights["root_box"],
            "Hermitian_operator_distance_from_signature_upper": distance,
            "residual_row_sum_bounds": residual_rows,
            "root_variation_and_conversion_row_sum_bounds": variation_rows,
            "Gram_roundoff_row_sum_bounds": arithmetic_rows, "total_row_sum_bounds": total_rows,
            "uniform_J_HS_error_upper": eJ.tolist(), "uniform_D_operator_error_upper": eD_op,
            "maximum_X_HS_error_upper": float(np.max(eX)),
            "phase_root_float_error_upper": phase_error,
            "mode_phase_conversion_error_included": True,
            "floating_operator_assembly_and_Gram_error_included": True,
            "geometry_scope": geometry["metadata"], "scalar_scope": weights.get("metadata", {}),
            "rank_T_theorem_is_an_independent_premise": True,
            "full_unconstrained_19_or_21_field_nonsingularity_claim": False,
            "shell_density_kernel_S_in_kerTadjoint_removed_as_gauge": False}


def run(repo=None):
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    mp.mp.dps, mp.iv.dps = 100, 80
    arithmetic = load("full_symbol_interval")  # helpers only; NEVER its run().
    weights_owner = load("shell_transfer_interval_weights")
    info = np.finfo(np.float64)
    require(info.eps == 2.0**-52 and info.nmant == 52 and info.maxexp == 1024
            and np.dtype(np.complex128).itemsize == 16, "IEEE_binary64_storage")
    choices = _choose(repo)
    require(len(choices) == len(SECTORS) == 2, "both_shell_transfer_sectors_are_present")
    results = []
    for choice, (q, inactive, rank_T) in zip(choices, SECTORS):
        require(tuple(choice["q"]) == q, "preconditioner_sector_order")
        weights = weights_owner.spectral_intervals(repo, q)
        geometry = creator_geometry(choice["B"], inactive, repo)
        result = _validate_sector(choice, weights, geometry, arithmetic)
        result["inactive_roles"] = list(inactive)
        result["independently_required_exact_rank_T"] = rank_T
        results.append(result)
    require([result["restriction_dimension"] for result in results] == [12, 8],
            "complete_twelve_and_eight_dimensional_restrictions")
    return {"status": "VALIDATED_SHELL_TRANSFER_RESTRICTIONS", "seconds": round(time.perf_counter()-start, 4),
            "schema": "d0-native-shell-transfer-restrictions-interval/1",
            "momenta_per_sector": N, "exterior_dimension": DIM, "reference_dimension": 128,
            "sectors": results,
            "source_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                              for name in ("full_shell_transfer_interval.py", "full_shell_transfer_diagnostic.py",
                                           "shell_transfer_interval_weights.py", "full_symbol_interval.py",
                                           "full_symbol_interval_geometry.py", "ordered_operator_check.py")},
            "arithmetic_environment": {"python": platform.python_version(), "numpy": np.__version__,
                                       "mpmath": mp.__version__, "float": "IEEE_binary64_with_outward_budgets"},
            "floating_Gram_real_operation_bound_per_entry": 2**26,
            "complex_Gram_gamma_multiplier": 2,
            "old_checker_runs_root_search_or_receipt_mutations": False,
            "all_Fourier_modes_joint_kernel_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
