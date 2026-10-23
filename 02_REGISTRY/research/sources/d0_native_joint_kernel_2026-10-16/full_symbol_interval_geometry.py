"""Outward first-jet geometry bounds for the complete q3300 congruence.

The 16 native (non-observer) chart columns MOVE with the owned root a,b.
No coefficient, stabilizer, exterior component, or history is frozen.  A
16x13 preconditioner is instead an arbitrary FIXED matrix of exact finite
decimal complex pairs. Choosing it numerically proves nothing; a later
interval congruence test supplies the proof independently of that choice.

geometry_bounds(B) returns actual full16 phase-coefficient arrays and live
mpmath.iv upper bounds. eJ_geom includes all coefficient conversion errors;
the returned phase-root intervals separately enclose conversion of every
exact eighth root of unity to the binary64 modes used by the assembler.
Coefficient norm sums are UNSCALED, while J and D have the outside factor L=8.

No old run(), root search, receipt generator, or broad suite is executed.
The optional numerical preconditioner choice calls only the new diagnostic.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re

import mpmath as mp
import numpy as np
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
L, FOCK, REDUCED, QUOTIENT = 8, 16, 16, 13
DECIMAL = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("full_symbol_interval_geometry:"+label)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def choose_preconditioner(repo=None):
    """CHOOSE arbitrary finite decimals, without claiming an interval result."""
    repo = ROOT if repo is None else Path(repo).resolve()
    path = HERE/"full_symbol_diagnostic.py"
    diagnostic = _load(path, "interval_geometry_numerical_choice")
    result, data = diagnostic.run(repo, return_data=True)
    complement, H = data["complement"], data["H"]
    reduced = np.einsum("ia,ij,jb->ab", complement.conj(), H, complement)
    eigenvalues, eigenvectors = np.linalg.eigh(reduced)
    require(np.min(np.abs(eigenvalues)) > 1e-5, "numerical_choice_has_no_tiny_pivot")
    B = np.einsum("ia,ab,b->ib", complement, eigenvectors,
                  1/np.sqrt(np.abs(eigenvalues)))
    # These strings, not the binary eigenvectors, are the certificate input.
    exact = [[(format(z.real, ".17g"), format(z.imag, ".17g")) for z in row]
             for row in B]
    return {"B": exact, "signs": [int(np.sign(x)) for x in eigenvalues],
            "diagnostic": result,
            "choice_source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "fixed_preconditioner_is_a_proof": False}


def _cross(x, y):
    return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2],
            x[0]*y[1]-x[1]*y[0]]


def _columns(a, b, kappa):
    """Actual regular_fourier_chart columns, in its original exact order.

    For active r0,r1, the first two columns of I-ww^T/|w|² are independent
    because the third spatial entry is -b !=0.  They are EXACTLY the first
    two columnspace pivots in the owned routine. All other columns are its
    alpha, three beta, and unscaled w stabilizer columns.
    """
    zero = 0*a
    legs = [[a if r == 0 else b]
            +[-(a if r == j+1 else b) for j in range(3)] for r in range(4)]
    columns = []
    for r, u in enumerate(legs):
        w = u[1:]
        rho2 = sum(x*x for x in w)
        def empty():
            return ([[zero for _ in range(4)] for _ in range(4)],
                    [[zero for _ in range(3)] for _ in range(4)])
        if r >= 2:
            av, omega = empty()
            av[r][0] = 1+zero
            columns.append((av, omega))
        for j in range(2 if r < 2 else 3):
            av, omega = empty()
            unit = [int(i == j) for i in range(3)]
            av[r][1:] = ([unit[i]-w[i]*w[j]/rho2 for i in range(3)]
                         if r < 2 else unit)
            omega[r] = [kappa[r]*x/rho2 for x in _cross(w, unit)]
            columns.append((av, omega))
        av, omega = empty()
        omega[r] = list(w)
        columns.append((av, omega))
    require(len(columns) == REDUCED, "all_sixteen_nonobserver_columns")
    return legs, columns


def _validate_B(B):
    require(len(B) == REDUCED and all(len(row) == QUOTIENT for row in B),
            "fixed_preconditioner_shape_16_by_13")
    for row in B:
        for pair in row:
            require(len(pair) == 2 and all(isinstance(x, str) and DECIMAL.fullmatch(x)
                                          for x in pair),
                    "preconditioner_entries_are_exact_finite_decimal_pairs")


def _combine(columns, B, complex_constructor, zero):
    combined = []
    for j in range(QUOTIENT):
        av = [[zero for _ in range(4)] for _ in range(4)]
        omega = [[zero for _ in range(3)] for _ in range(4)]
        for i, (base_a, base_omega) in enumerate(columns):
            coefficient = complex_constructor(*B[i][j])
            for r in range(4):
                for t in range(4):
                    av[r][t] += coefficient*base_a[r][t]
                for t in range(3):
                    omega[r][t] += coefficient*base_omega[r][t]
        combined.append((av, omega))
    return combined


def _pattern(matrix):
    return tuple((16*i+j, int(matrix[i, j])) for i in range(16) for j in range(16)
                 if matrix[i, j] != 0)


def _patterns(creators, operator):
    rotations = [s.diag(0, operator.cross(s.eye(3)[:, j])) for j in range(3)]
    gamma = [operator.Gamma(W, creators) for W in rotations]
    result = {"C": [_pattern(C) for C in creators],
              "I": [_pattern(C.T) for C in creators],
              "CG": [[_pattern(C*G) for G in gamma] for C in creators],
              "IG": [[_pattern(C.T*G) for G in gamma] for C in creators]}
    for family in ("C", "I"):
        supports = [{i for i, value in pattern} for pattern in result[family]]
        require(all(len(pattern) == 8 and all(abs(value) == 1 for _, value in pattern)
                    for pattern in result[family])
                and sum(map(len, supports)) == len(set.union(*supports)),
                "actual_"+family+"_has_disjoint_single_coordinate_entries")
    return result


def _matrix(terms, zero):
    out = [zero for _ in range(FOCK*FOCK)]
    for value, pattern in terms:
        for position, integer in pattern:
            out[position] += value*integer
    return out


def _coefficients(legs, combined, bar_tq, patterns, zero):
    plus, minus, constant = [], [], []
    for av, omega in combined:
        p, m, c = [], [], []
        for r in range(4):
            plus_terms = [(av[r][i], patterns["C"][i]) for i in range(4)]
            minus_terms = [(av[r][i], patterns["I"][i]) for i in range(4)]
            for i in range(4):
                for j in range(3):
                    value = legs[r][i]*omega[r][j]
                    plus_terms.append((value, patterns["CG"][i][j]))
                    minus_terms.append((-bar_tq[r]*value, patterns["IG"][i][j]))
            p.append(_matrix(plus_terms, zero))
            m.append(_matrix(minus_terms, zero))
            c.extend((-av[r][i], patterns[family][i])
                     for i in range(4) for family in ("C", "I"))
        plus.append(p)
        minus.append(m)
        constant.append(_matrix(c, zero))
    cu = [_matrix([(u[i], patterns["C"][i]) for i in range(4)], zero) for u in legs]
    iu = [_matrix([(u[i], patterns["I"][i]) for i in range(4)], zero) for u in legs]
    return plus, minus, constant, cu, iu


def _numeric(values, shape):
    return np.array([complex(value) for value in _flatten(values)],
                    dtype=np.complex128).reshape(shape)


def _flatten(values):
    if isinstance(values, (list, tuple)):
        for value in values:
            yield from _flatten(value)
    else:
        yield values


def _HS_upper(values):
    iv = mp.iv
    squared = iv.mpf(0)
    for value in values:
        squared += (value.real**2+value.imag**2).b
    return iv.sqrt(squared).b


def _HS_error(interval_matrix, numeric_matrix):
    # iv.mpf(float) contains the EXACT binary float. No midpoint or float
    # rounding is silently dropped from the coefficient conversion error.
    flat = np.asarray(numeric_matrix).reshape(-1)
    return _HS_upper([value-mp.iv.mpc(mp.iv.mpf(float(center.real)),
                                    mp.iv.mpf(float(center.imag)))
                      for value, center in zip(interval_matrix, flat)])


def _numeric_HS_upper(matrix):
    return _HS_upper([mp.iv.mpc(mp.iv.mpf(float(z.real)), mp.iv.mpf(float(z.imag)))
                      for z in np.asarray(matrix).reshape(-1)])


def _guard_exact_chart(chart, operator):
    # One symbolic identity, not a new rank census or finite-difference test.
    a, b = s.symbols("geometry_positive_a geometry_positive_b", positive=True)
    q = operator.phases((3, 3, 0, 0))
    kappa = tuple(1-x for x in q)
    F = (a-b)*s.eye(4)+b*s.ones(4)
    actual = chart.regular_fourier_chart(F, kappa)["basis31"][:, :16]
    _, explicit = _columns(a, b, kappa)
    columns = []
    for av, omega in explicit:
        columns.append(s.Matrix([x for row in av for x in row]
                                +[x for row in omega for x in row]+[0, 0, 0]))
    require(all(s.cancel(x) == 0 for x in actual-s.Matrix.hstack(*columns)),
            "symbolic_actual_chart_coefficients_all_a_b_no_frozen_basis")


def geometry_bounds(B, repo=None):
    """Return rigorous uniform geometry errors and independent center arrays.

    eJ_geom[i]=8 sum_9 ||coefficient(root)-coefficient_float||_HS, so it
    bounds J_i at every exact momentum phase, without mode sampling.
    deltaD_geom_op=16 sum_r ||u_r(root)-u_r_float||_2; its Frobenius
    counterpart is4 times larger by the full16 CAR identity. The driver
    separately adds phase and floating-point assembly errors.
    """
    _validate_B(B)
    repo = ROOT if repo is None else Path(repo).resolve()
    chart = _load(HERE/"native_chart_check.py", "interval_geometry_owned_chart")
    operator = _load(HERE/"ordered_operator_check.py", "interval_geometry_owned_operator")
    chart.owned_definitions(repo)  # stable definitions/Lean/receipt pins only.
    creators, exterior_order = operator.owned_car(repo)
    patterns = _patterns(creators, operator)
    _guard_exact_chart(chart, operator)
    receipt = json.loads((repo/chart.RECEIPT).read_text())
    center = receipt["interval"]["root_center"]
    previous_iv = mp.iv.dps
    mp.iv.dps = 80
    try:
        iv = mp.iv
        with mp.workdps(80):
            d0, o0 = map(mp.mpf, center)
            radius = iv.mpf(receipt["interval"]["root_radius"])
            d = iv.mpf(center[0])+iv.mpf([-1, 1])*radius
            o = iv.mpf(center[1])+iv.mpf([-1, 1])*radius
            ap, am = iv.sqrt(d+3*o), iv.sqrt(d-o)
            a, b = (ap+3*am)/4, (ap-am)/4
            require(b.a > 0 and (a-b).a > 0, "whole_root_box_regular_a_greater_b_positive")
            a0 = (mp.sqrt(d0+3*o0)+3*mp.sqrt(d0-o0))/4
            b0 = (mp.sqrt(d0+3*o0)-mp.sqrt(d0-o0))/4
            sqrt2, sqrt2_0 = iv.sqrt(2), mp.sqrt(2)
            qroot, qroot0 = iv.mpc(-sqrt2/2, sqrt2/2), mp.mpc(-sqrt2_0/2, sqrt2_0/2)
            kappa = [1-qroot, 1-qroot, iv.mpf(0), iv.mpf(0)]
            kappa0 = [1-qroot0, 1-qroot0, mp.mpf(0), mp.mpf(0)]
            legs, columns = _columns(a, b, kappa)
            legs0, columns0 = _columns(a0, b0, kappa0)
            combined = _combine(columns, B, iv.mpc, iv.mpc(0))
            combined0 = _combine(columns0, B, mp.mpc, mp.mpc(0))
            barq, barq0 = iv.mpc(-sqrt2/2, -sqrt2/2), mp.mpc(-sqrt2_0/2, -sqrt2_0/2)
            arrays = _coefficients(legs, combined, [barq, barq, 1, 1],
                                   patterns, iv.mpc(0))
            arrays0 = _coefficients(legs0, combined0,
                                    [barq0, barq0, 1, 1],
                                    patterns, mp.mpc(0))
            plus, minus = (_numeric(x, (13, 4, 16, 16)) for x in arrays0[:2])
            constant = _numeric(arrays0[2], (13, 16, 16))
            cu, iu = (_numeric(x, (4, 16, 16)) for x in arrays0[3:])
            require(all(np.isfinite(array).all() for array in (plus, minus, constant, cu, iu)),
                    "all_chosen_float_coefficients_finite")
            errors, norm_sums, center_J = [], [], []
            coefficient_errors = []
            for i in range(13):
                error = sum((_HS_error(arrays[f][i][r], (plus, minus)[f][i, r])
                             for f in range(2) for r in range(4)), iv.mpf(0))
                error += _HS_error(arrays[2][i], constant[i])
                norm_sum = sum((_numeric_HS_upper(matrix)
                                for matrix in [*plus[i], *minus[i], constant[i]]), iv.mpf(0))
                errors.append((L*error).b)
                coefficient_errors.append(error.b)
                norm_sums.append(norm_sum.b)
                center_J.append((L*norm_sum).b)
            # In this occupation basis every nonzero entry of C(u) is a
            # single signed u-coordinate. Its center conversion is exactly
            # represented by the four separately converted u0 coordinates.
            numeric_legs = np.array([[float(x) for x in row] for row in legs0])
            leg_errors = [_HS_error(legs[r], numeric_legs[r]) for r in range(4)]
            delta_D = (2*L*sum(leg_errors, iv.mpf(0))).b
            D_norm_sum = sum((_numeric_HS_upper(matrix) for matrix in [*cu, *iu]),
                             iv.mpf(0)).b
            roots0 = [mp.mpc(1), mp.mpc(1, 1)/sqrt2_0, mp.j,
                      mp.mpc(-1, 1)/sqrt2_0, mp.mpc(-1),
                      mp.mpc(-1, -1)/sqrt2_0, -mp.j, mp.mpc(1, -1)/sqrt2_0]
            roots = np.array([complex(x) for x in roots0])
            roots_iv = [iv.mpc(1, 0), iv.mpc(sqrt2/2, sqrt2/2), iv.mpc(0, 1),
                        iv.mpc(-sqrt2/2, sqrt2/2), iv.mpc(-1, 0),
                        iv.mpc(-sqrt2/2, -sqrt2/2), iv.mpc(0, -1),
                        iv.mpc(sqrt2/2, -sqrt2/2)]
            phase_error_components = []
            for approximate, exact in zip(roots, roots_iv):
                dr = iv.mpf(float(approximate.real))-exact.real
                di = iv.mpf(float(approximate.imag))-exact.imag
                phase_error_components.append(iv.sqrt(dr*dr+di*di).b)
            return {"plus": plus, "minus": minus, "constant": constant,
                    "cu": cu, "iu": iu, "roots8float": roots,
                    "phase_root_error_components": phase_error_components,
                    "eJ_geom": errors, "deltaD_geom_op": delta_D,
                    "deltaD_geom_F": (4*delta_D).b,
                    "coeff_norm_sum": norm_sums, "D_coeff_norm_sum": D_norm_sum,
                    "center_J_HS_uniform": center_J, "coefficient_errors_unscaled": coefficient_errors,
                    "metadata": {"interval_decimal_digits": 80,
                        "root_center_d_o": center,
                        "root_radius": receipt["interval"]["root_radius"],
                        "a_box": str(a), "b_box": str(b),
                        "a_center": mp.nstr(a0, 75), "b_center": mp.nstr(b0, 75),
                        "basis_columns_move_with_entire_root_box": True,
                        "symbolic_actual_chart_identity_checked": True,
                        "fixed_B_complex_decimal_shape": [16, 13],
                        "phase_coefficient_shapes": [[13, 4, 16, 16], [13, 4, 16, 16],
                                                      [13, 16, 16]],
                        "all16_exterior_components": True,
                        "owned_exterior_order": list(exterior_order),
                        "norm_sums_outside_L_factor": L,
                        "coefficient_conversion_error_included": True,
                        "phase_root_error_components_outward": True,
                        "float_assembly_roundoff_in_main_operator": "separate_gamma_bound",
                        "source_pins": chart.PINS,
                        "no_interval_inertia_claim_from_geometry_alone": True}}
    finally:
        mp.iv.dps = previous_iv


def run(repo=None):
    choice = choose_preconditioner(repo)
    result = geometry_bounds(choice["B"], repo)
    return {"status": "GEOMETRY_BOUNDS_ONLY", "signs": choice["signs"],
            "eJ_geom": [str(x) for x in result["eJ_geom"]],
            "deltaD_geom_op": str(result["deltaD_geom_op"]),
            "deltaD_geom_F": str(result["deltaD_geom_F"]),
            "coeff_norm_sum": [str(x) for x in result["coeff_norm_sum"]],
            "D_coeff_norm_sum": str(result["D_coeff_norm_sum"]),
            "metadata": result["metadata"]}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
