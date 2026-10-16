"""Validated full native q3300 symbol, with explicit arithmetic error bounds.

This is a new bounded computation of Eq.(20), not a root search or a replay
of historical certificates.  A numerical eigensystem CHOOSES fixed decimal
constants B only.  The proof below validates the congruence B*H(theta)B on
the complete owned root rectangle, without trusting that eigensystem.

Every Gram sum uses all4096 momenta and all16 exterior components. Three
observer columns have exactly zero operator jet; the other sixteen chart
columns are varied throughout the rectangle. Only a nonsingular13-column
restriction is needed: the independently proved three spatial Ward vectors
then determine the kernel. Separately stored affine-shift rows, shell
reference verticals and other Fourier frequencies are outside this result.

Floating references are exact dyadic constants in the comparison theorem.
Scalar weights and geometry coefficients are enclosed by mpmath.iv. All
complex128 assembly/summation roundoff is included explicitly. No test
depends on Python assert. All output is stdout; no old receipts are written.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

import importlib.util
import hashlib
import json
import math
import platform
from pathlib import Path
import time

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
L, N, DIM, QUOTIENT = 8, 4096, 16, 13
U = mp.iv.mpf(2)**-53
TINY = 2.0**-400
POSITIVE_INFLATION = 1.0+2.0**-30


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("full_symbol_interval:"+label)


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE/(name+".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def upper(interval):
    """Next binary64 above an interval's exact upper endpoint."""
    value = math.nextafter(float(interval.b), math.inf)
    require(math.isfinite(value), "finite_outward_upper")
    return value


def gamma(n):
    return n*U/(1-n*U)


def midpoint(interval):
    # Choice of a dyadic reference need not be an outward bound.
    with mp.workdps(110):
        return float((mp.make_mpf(interval._mpi_[0])
                      +mp.make_mpf(interval._mpi_[1]))/2)


def interval_complex_abs(real, imag):
    return mp.iv.sqrt(real*real+imag*imag)


def positive_sum(weight, left, right):
    """Outward upper matrix for sum_k weight_k left_ik right_jk >=0.

    Each entry has4096 nonnegative triple products and their sum. Fewer
    than2^16 elementary real operations affect an entry, so inflation2^-30
    exceeds gamma_(2^16) by over100. The tiny additive allowance covers
    all possible subnormal contributions (inputs are bounded below/above
    separately wherever they matter). nextafter makes the final conversion
    outward. No cancellation, complex operation, or BLAS is used here.
    """
    require(np.all(weight >= 0) and np.all(left >= 0) and np.all(right >= 0),
            "nonnegative_error_majorants")
    for values in (weight, left, right):
        require(np.all(np.isfinite(values)) and np.max(values) < 2.0**100,
                "positive_sum_factors_finite_and_bounded")
    value = np.einsum("k,ik,jk->ij", weight, left, right, optimize=False)
    require(np.all(np.isfinite(value)) and np.max(value) < 2.0**100,
            "positive_error_sum_normal_range")
    return np.nextafter(value*POSITIVE_INFLATION+TINY, np.inf)


def frobenius_upper(array):
    # At most256 squares per real/imaginary part,512 positive additions
    # and one square root. 2^-35 is >100 gamma_2048. The additive term
    # covers products of components below2^-450 as well as subnormals.
    value = np.sqrt(np.sum(array.real*array.real+array.imag*array.imag, axis=(-2, -1)))
    require(np.all(np.isfinite(value)) and np.max(value) < 2.0**100,
            "norms_normal_finite")
    return np.nextafter(value*(1+2.0**-35)+TINY, np.inf)


def run(repo=None):
    start = time.perf_counter()
    mp.mp.dps = 100
    mp.iv.dps = 80
    info = np.finfo(np.float64)
    require(info.eps == 2.0**-52 and info.nmant == 52 and info.maxexp == 1024
            and np.dtype(np.complex128).itemsize == 16, "IEEE_binary64_storage")
    repo = ROOT if repo is None else Path(repo).resolve()
    weights_owner = load("full_symbol_interval_weights")
    geometry_owner = load("full_symbol_interval_geometry")
    choice = geometry_owner.choose_preconditioner(repo)
    signs = np.array(choice["signs"], dtype=int)
    require(signs.shape == (QUOTIENT,) and set(signs) == {-1, 1},
            "fixed_sign_comparison_has_both_signs")
    weights = weights_owner.spectral_intervals(repo)
    geometry = geometry_owner.geometry_bounds(choice["B"], repo)

    modes = np.array(weights["modes"], dtype=int)
    outgoing = np.array(weights["outgoing"], dtype=int)
    require(modes.shape == (N, 4) and outgoing.shape == (N,), "all4096_modes")
    roots = np.array(geometry["roots8float"], dtype=complex)
    tk = roots[modes]
    plus, minus, constant = (np.array(geometry[key], dtype=complex)
                             for key in ("plus", "minus", "constant"))
    cu, iu = (np.array(geometry[key], dtype=complex) for key in ("cu", "iu"))
    require(plus.shape == minus.shape == (QUOTIENT, 4, DIM, DIM)
            and constant.shape == (QUOTIENT, DIM, DIM), "all13_full16_jets")
    for values in (roots, plus, minus, constant, cu, iu):
        require(np.all(np.isfinite(values)) and np.max(np.abs(values)) < 2.0**100,
                "finite_coefficient_range")
    phase_root_error = max(upper(value)
                           for value in geometry["phase_root_error_components"])
    require(phase_root_error < 2.0**-50, "eighth_root_binary64_conversion_bound")
    D = L*(np.einsum("kr,rij->kij", tk-1, cu, optimize=False)
           +np.einsum("kr,rij->kij", tk.conj()-1, iu, optimize=False))

    # The nine-phase J evaluation and the D evaluation each have <128
    # elementary real operations per entry, including exact eighth-root
    # conversion error <=2u. Extra factors cover that phase error and the
    # |t-1|<=2 coefficients in D. All coefficient conversion is in geometry.
    g128, g512 = gamma(128), gamma(512)
    eJ = np.array([upper(geometry["eJ_geom"][i]
                         +phase_root_error*L*geometry["coeff_norm_sum"][i]
                         +g128*L*geometry["coeff_norm_sum"][i]+TINY)
                   for i in range(QUOTIENT)])
    d_eval = (phase_root_error*L*geometry["D_coeff_norm_sum"]
              +g128*2*L*geometry["D_coeff_norm_sum"]+TINY)
    eD_op = upper(geometry["deltaD_geom_op"]+d_eval)
    eD_F = upper(geometry["deltaD_geom_F"]+d_eval)
    sqrt_lam = np.array([upper(x) for x in weights["sqrt_lambda"]])

    wJ_iv, wX_iv = weights["gamma_J"], weights["weight_X"]
    wJ, wX = (np.array([midpoint(x) for x in values]) for values in (wJ_iv, wX_iv))
    dwJ, dwX = (np.array([upper(abs(v-mp.iv.mpf(float(w))))
                          for v, w in zip(values, floats)])
                 for values, floats in ((wJ_iv, wJ), (wX_iv, wX)))
    WJ, WX = (np.array([upper(abs(v)) for v in values]) for values in (wJ_iv, wX_iv))

    H = np.zeros((QUOTIENT, QUOTIENT), complex)
    nJ, nX, eX = (np.zeros((QUOTIENT, N)) for _ in range(3))
    for offset in range(0, N, 128):
        sl = slice(offset, offset+128)
        J = L*(np.einsum("kr,arij->akij", tk[sl], plus, optimize=False)
               +np.einsum("kr,arij->akij", tk[sl].conj(), minus, optimize=False)
               +constant[:, None, :, :])
        X = (np.einsum("kij,akjl->akil", D[outgoing[sl]], J, optimize=False)
             +np.einsum("akij,kjl->akil", J, D[sl], optimize=False))
        nj, nx = frobenius_upper(J), frobenius_upper(X)
        nJ[:, sl], nX[:, sl] = nj, nx
        sd = sqrt_lam[sl]+sqrt_lam[outgoing[sl]]
        # Split Dtrue*(Jtrue-Jfloat)+(Dtrue-Dfloat)*Jfloat.
        # Hence no missing eD*eJ term. Complex16 products and their sum
        # need <512 real operations per entry. F(Dtrue)=4sqrt(lambda).
        xerr = (sd[None, :]*eJ[:, None]+2*eD_op*nj
                +upper(g512)*(4*sd[None, :]+2*eD_F)*nj)
        eX[:, sl] = np.nextafter(xerr*POSITIVE_INFLATION+TINY, np.inf)
        jf, xf = J.reshape(QUOTIENT, -1, DIM*DIM), X.reshape(QUOTIENT, -1, DIM*DIM)
        H += np.einsum("akn,bkn,k->ab", jf.conj(), jf, wJ[sl], optimize=False)
        H += np.einsum("akn,bkn,k->ab", xf.conj(), xf, wX[sl], optimize=False)

    # <2^26 real operations per entry in the entire complex Gram sums,
    # including all128-mode partial sums and the final additions. This is
    # conservative even counting each complex multiply as6 real operations.
    abs_gram = (positive_sum(np.abs(wJ), nJ, nJ)
                +positive_sum(np.abs(wX), nX, nX))
    # Factor2 covers real/imaginary error bounds in complex absolute value.
    roundoff = np.nextafter(upper(2*gamma(2**26))*abs_gram*POSITIVE_INFLATION+TINY,
                           np.inf)
    coefficient_error = np.zeros_like(roundoff)
    for dw, W, n, e in ((dwJ, WJ, nJ, np.broadcast_to(eJ[:, None], nJ.shape)),
                        (dwX, WX, nX, eX)):
        coefficient_error += (positive_sum(dw, n, n)+positive_sum(W, e, n)
                              +positive_sum(W, n, e)+positive_sum(W, e, e))
    coefficient_error = np.nextafter(coefficient_error*POSITIVE_INFLATION+TINY,
                                      np.inf)

    residual_rows, variation_rows, arithmetic_rows, total_rows = [], [], [], []
    for i in range(QUOTIENT):
        residual = mp.iv.mpf(0)
        variation = mp.iv.mpf(0)
        arithmetic = mp.iv.mpf(0)
        for j in range(QUOTIENT):
            delta = int(signs[i]) if i == j else 0
            residual += interval_complex_abs(mp.iv.mpf(float(H[i, j].real))-delta,
                                              mp.iv.mpf(float(H[i, j].imag)))
            variation += mp.iv.mpf(float(coefficient_error[i, j]))
            arithmetic += mp.iv.mpf(float(roundoff[i, j]))
        residual_rows.append(upper(residual))
        variation_rows.append(upper(variation))
        arithmetic_rows.append(upper(arithmetic))
        total_rows.append(upper(residual+variation+arithmetic))
    norm_bound = max(total_rows)
    require(norm_bound < 1, "entire_root_box_congruence_within_one_of_signature")
    elapsed = time.perf_counter()-start
    return {"status": "VALIDATED_FULL_Q3300_SYMBOL",
            "schema": "d0-native-full-q3300-interval-symbol/1",
            "seconds": round(elapsed, 4), "q": [3, 3, 0, 0],
            "momenta": N, "exterior_dimension": DIM, "reference_dimension": 128,
            "all19_native_field_columns": 19, "restriction_dimension": QUOTIENT,
            "proved_observer_zero_columns": 3, "proved_spatial_Ward_columns": 3,
            "exact_decimal_preconditioner": choice["B"],
            "comparison_signs": signs.tolist(),
            "root_box": weights["root_box"],
            "phase_root_float_error_upper": phase_root_error,
            "mode_phase_conversion_error_included": True,
            "floating_operator_assembly_error_included": True,
            "residual_row_sum_bounds": residual_rows,
            "root_variation_and_coefficient_row_sum_bounds": variation_rows,
            "Gram_roundoff_row_sum_bounds": arithmetic_rows,
            "total_row_sum_bounds": total_rows,
            "Hermitian_operator_distance_from_signature_upper": norm_bound,
            "complex_full19_inertia_at_owned_stationary_root": {
                "positive": int(np.sum(signs > 0)), "negative": int(np.sum(signs < 0)),
                "representation_zero": 6},
            "uniform_J_HS_error_upper": eJ.tolist(),
            "uniform_D_operator_error_upper": eD_op,
            "maximum_X_HS_error_upper": float(np.max(eX)),
            "geometry_scope": geometry.get("metadata", {}),
            "scalar_scope": weights.get("metadata", {}),
            "source_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                              for name in ("full_symbol_interval.py", "full_symbol_interval_geometry.py",
                                           "full_symbol_interval_weights.py", "full_symbol_diagnostic.py",
                                           "native_chart_check.py", "ordered_operator_check.py")},
            "arithmetic_environment": {"python": platform.python_version(),
                                       "numpy": np.__version__, "mpmath": mp.__version__,
                                       "float": "IEEE binary64 round-to-nearest; explicit outward budgets"},
            "floating_Gram_real_operation_bound_per_entry": 2**26,
            "complex_Gram_gamma_multiplier": 2,
            "physical_gauge_quotient_asserted": False,
            "other_Fourier_frequencies_solved": False,
            "separate_affine_shift_rows_included": False,
            "nonflat_root_constructed": False, "physical_admission_or_GR_claim": False,
            "old_runs_or_receipt_regeneration": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
