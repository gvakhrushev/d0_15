#!/usr/bin/env python3
"""Actual recorded A3->A9 archive occupation in the owned residual heat family.

The record, frames, PF trace, and ordinary-GNS inclusion are source pinned.
Only their definitions are imported; no earlier certificate is replayed.
L=nu*(I-J J*) is the v7 comparison family, not a derived native field action.
The full 10946-dimensional carrier and its heat trace remain in the formulas.
"""
from __future__ import annotations

import hashlib
import importlib.util
from itertools import combinations
import json
from math import isqrt
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CERT = "02_REGISTRY/research/certificates/"
SOURCE_PINS = {
    CERT + "a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    CERT + "a4d_native_jones_record_transport.py":
        "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
    CERT + "a4d_native_afcar_positive_state_refinement_check.py":
        "bf82cb2555a8ae5d832fe06dc0b4fbea11f0135eb75c011d50556f3c8a61d341",
    CERT + "a4d_native_golden_cost_refinement.lean":
        "3e47588629ce3ed51ff165643090a697ecc5d39e64be2019bfa856e024014bd4",
    "02_REGISTRY/research/sources/d0_native_af_heat_transfer_v7_2026-10-14/af_heat_check.py":
        "b9b491ac34db33a7e5091dda0ac03297fab64b17594f535235daa0ceabf23b65",
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_POSITIVE_STATE_REFINEMENT.md":
        "1b50e1ca0cdc555ac26d0a3091cebdfefc68bd0ae2c284b9f037239bbc7fe7cc",
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def _load(repo: Path, name: str):
    spec = importlib.util.spec_from_file_location(
        "archive_occupation_" + name, repo / CERT / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("source_definition_import_failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def occupation_jet(sigma: s.MatrixBase, dsigma: s.MatrixBase,
                   J: s.MatrixBase, dJ: s.MatrixBase) -> tuple[s.Expr, s.Expr]:
    """q,dq for normalized density sigma and a moving isometry J.

    All entries of sigma/dsigma are retained. The caller supplies a genuine
    normalized-state and isometry jet; in particular Tr(dsigma)=0. For Hermitian
    sigma the second term is -2 Re Tr(sigma dJ J*). No unitary-state ansatz is used.
    """
    if sigma.rows != sigma.cols or dsigma.shape != sigma.shape:
        raise ValueError("square_density_and_same_shape_tangent_required")
    if J.rows != sigma.rows or dJ.shape != J.shape:
        raise ValueError("compatible_inclusion_and_tangent_required")
    Q = s.eye(J.rows) - J * J.H
    q = s.trace(sigma * Q)
    dq = s.trace(dsigma * Q) - s.trace(sigma * (dJ * J.H + J * dJ.H))
    return s.simplify(q), s.simplify(dq)


def residual_source(q: s.Expr, dq: s.Expr, nu: s.Expr, dnu: s.Expr,
                    beta: s.Expr, rank: int, dimension: int) -> s.Expr:
    """d(H+R)=(q-p_th)dnu+nu*dq; beta and both full ranks are fixed."""
    if not 0 < rank < dimension:
        raise ValueError("strict_retained_rank_required")
    m = dimension - rank
    p_th = m * s.exp(-beta * nu) / (rank + m * s.exp(-beta * nu))
    return (q - p_th) * dnu + nu * dq


def scalar_stationary_gap(q: s.Expr, beta: s.Expr,
                          rank: int, dimension: int) -> s.Expr:
    """Conditional nu*: requires beta>0 and 0<q<(dimension-rank)/dimension.

    This solves the fixed-q scalar comparison only. It neither selects a
    physical gap nor removes the moving-preparation/J source nu* dq.
    """
    if not 0 < rank < dimension:
        raise ValueError("strict_retained_rank_required")
    return s.log((dimension - rank) * (1 - q) / (rank * q)) / beta


def transported_refinement(q: s.Expr, level: int, beta: s.Expr,
                           nu: s.Expr) -> dict:
    """Fixed-record source along the explicitly transported pure GNS lift.

    Write K=hatJ_(9->N), J_N=K J_(3->9), psi_N=K psi_9. The owned PF/Jones
    maps give K* K=I, hence J_N* psi_N=J_(3->9)* psi_9 and ||psi_N||=1.
    Thus q_N=q exactly for every N>=9. At the first step its left densities
    are p R+ diag(yy*,0) R+* and p^2 R- yy* R-*, precisely the positive-state
    owner's extension. The fixed right-column pure lift is constructive;
    uniqueness across all GNS density fibers is not asserted.

    The transported composite J_N includes the owned Jones conjugations
    after A9; it is not silently replaced by unrotated ordinary AF inclusion.
    """
    if not isinstance(level, int) or level < 9:
        raise ValueError("transported_record_level_at_least_nine_required")
    A, B = 1, 1
    for _ in range(level):
        A, B = A+B, A
    D = A*A+B*B
    return {"dimension": D, "rank": 34, "occupation": q,
            "source": residual_source(q, 0, nu, 1, beta, 34, D),
            "conditional_nu_star": scalar_stationary_gap(q, beta, 34, D)}


def recorded_archive(repo: Path | None = None) -> dict:
    """Reconstruct the pinned positive-state owner's actual y,z,X=y z*.

    The four-entry source row is the owner's explicitly checked recorded CAR
    row, not an arbitrary Gibbs vector. z is its actual Jones right column.
    """
    repo = ROOT if repo is None else Path(repo)
    for path, digest in SOURCE_PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                "source_pin:" + path)
    AF = _load(repo, "a4d_native_fibonacci_record_activation")
    Jones = _load(repo, "a4d_native_jones_record_transport")
    a, p = AF.a, AF.p
    row = s.zeros(20, 1)
    for i, value in {0: p, 3: p - 1, 15: a*p, 18: a*p}.items():
        row[i] = value
    y = AF.mat(AF.right_frames(3)[0]["V"] * row)
    G = AF.mat(Jones.corner_frames(3)[0].subs(
        {Jones.E.a: a, Jones.E.p: p}, simultaneous=True))
    z = G[:, 0]
    X = AF.mat(y * z.H)
    q_left = AF.red(1 - (y.H * G * G.H * y)[0])
    q_full = AF.red(1 - p**6 * (1 - q_left))
    return {"AF": AF, "a": a, "p": p, "y": y, "G": G, "z": z,
            "X": X, "q_left": q_left, "q_full": q_full}


def _field_reduce(expr: s.Expr, a: s.Symbol, p: s.Symbol) -> s.Expr:
    """Exact Q(sqrt(2))[a]/(a^4+a^2-1), including nonconstant denominators."""
    field = s.QQ.algebraic_field(s.sqrt(2))
    poly = a**4 + a**2 - 1
    num, den = s.cancel(expr.subs(p, a*a)).as_numer_denom()
    num = s.rem(num, poly, a, domain=field)
    den = s.rem(den, poly, a, domain=field)
    return s.expand(s.rem(num * s.invert(den, poly, a, domain=field),
                          poly, a, domain=field))


def _positive_root_boxes() -> tuple[tuple[s.Rational, s.Rational], ...]:
    """Rational isolators for positive a^4+a^2=1 and sqrt(2), no floats."""
    D = 10**12
    lo, hi = 0, D
    def sign(k: int) -> int:
        return k**4 + k*k*D*D - D**4
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sign(mid) < 0:
            lo = mid
        else:
            hi = mid
    require(sign(lo) < 0 < sign(hi), "a_rational_root_isolation")
    b = isqrt(2*D*D)
    require(b*b < 2*D*D < (b+1)**2, "sqrt2_rational_root_isolation")
    # Both defining polynomials are strictly increasing on the positive axis.
    return ((s.Rational(lo, D), s.Rational(hi, D)),
            (s.Rational(b, D), s.Rational(b+1, D)))


def _bound(expr: s.Expr, a: s.Symbol, p: s.Symbol,
           boxes: tuple[tuple[s.Rational, s.Rational], ...]) -> tuple[s.Expr, s.Expr]:
    """Termwise rational enclosure after exact golden-field reduction."""
    b = s.Symbol("sqrt2_root", positive=True)
    poly = s.Poly(_field_reduce(expr, a, p).subs(s.sqrt(2), b), a, b, domain=s.QQ)
    low = high = s.S.Zero
    for (i, j), coefficient in poly.terms():
        left = boxes[0][0]**i * boxes[1][0]**j
        right = boxes[0][1]**i * boxes[1][1]**j
        if coefficient >= 0:
            low += coefficient*left
            high += coefficient*right
        else:
            low += coefficient*right
            high += coefficient*left
    return low, high


def run_checks(repo: Path | None = None) -> dict:
    data = recorded_archive(repo)
    AF, a, p = data["AF"], data["a"], data["p"]
    y, G, z, X = (data[k] for k in ("y", "G", "z", "X"))
    q_left, q_full = data["q_left"], data["q_full"]
    def eq(value: s.Expr | s.MatrixBase, name: str) -> None:
        values = list(value) if isinstance(value, s.MatrixBase) else [value]
        require(all(_field_reduce(v, a, p) == 0 for v in values), name)

    require(AF.counts(3) == (5, 3) and AF.counts(9) == (89, 55), "actual_levels")
    eq((y.H*y)[0] - 1, "recorded_y_normalized")
    eq(G.H*G - s.eye(5), "literal_Jones_frame_isometry")
    eq((z.H*z)[0] - 1, "actual_right_column_normalized")
    eq(p**10*s.trace(X.H*X) - p**10, "full_record_PF_norm")

    # Independent route: SIX literal conditional expectations, not a projection
    # onto the 610-dimensional left Jones corner. Every intervening block is kept.
    coarse = (X, s.zeros(55))
    for n in range(8, 2, -1):
        A, B = AF.counts(n)
        Z, W = coarse
        require(Z.shape == (A+B, A+B) and W.shape == (A, A), "literal_C_shape")
        coarse = (AF.mat(p*Z[:A, :A] + p*p*W),
                  AF.mat(Z[A:A+B, A:A+B]))
    coarse_expected = p**6*(G.H*y)*s.eye(5)[:, 0].T
    eq(coarse[0] - coarse_expected, "six_conditional_expectations_actual_X")
    eq(coarse[1], "six_conditional_expectations_second_block_zero")
    coarse_norm = p**4*s.trace(coarse[0].H*coarse[0]) + p**5*s.trace(coarse[1].H*coarse[1])
    eq(1 - coarse_norm/p**10 - q_full, "full_GNS_occupation_from_PF_norm_ratio")

    # A second adjoint construction sums the literal six-step inclusion copies
    # in normalized-HS coordinates. No huge dense full-GNS matrix is needed.
    adjoint = [s.zeros(5), s.zeros(3)]
    copies = [0, 0]
    for kind, _path, offset in AF.segments(5, 3, 6)[0]:
        d = (5, 3)[kind]
        copies[kind] += 1
        adjoint[kind] += AF.root_weight(6-kind)*X[offset:offset+d, offset:offset+d]
    require(copies == [13, 8], "literal_old_copy_multiplicities_in_M89")
    eq(adjoint[0] - p**3*(G.H*y)*s.eye(5)[:, 0].T, "normalized_Jstar_X")
    eq(adjoint[1], "normalized_Jstar_X_second_block")
    eq(1 - sum(s.trace(v.H*v) for v in adjoint) - q_full,
       "normalized_adjoint_agrees_with_six_C_maps")
    expected_left = (-94*a*p - 34*s.sqrt(2)*a*p + 21*s.sqrt(2)*a + 58*a
                     - 86*p + 21*s.sqrt(2)*p - 13*s.sqrt(2) + 54)
    eq(q_left - expected_left, "actual_left_corner_polynomial")
    eq(q_full - (1 - p**6*(1-q_left)), "full_vs_left_corner_compression")

    # Actual old-A1 M2 congruence, not a freely selected density. Both orbit
    # Grams are calculated before using the finite-orbit normalization proof.
    # In normalized PF coordinates x_ij is represented by vec(X_ij), whereas
    # its physical algebra representative is X_ij/p**5.
    def old_m2(matrix: s.MatrixBase) -> s.MatrixBase:
        pair = (matrix, s.zeros(1))
        for _ in range(8):  # literal A1 -> A9, with the old scalar retained
            pair = (s.diag(*pair), pair[0])
        return pair[0]

    P0 = old_m2(s.diag(1, 0))
    F10 = old_m2(s.Matrix([[0, 0], [1, 0]]))
    eq(P0*y-y, "actual_y_old_M2_highest_weight")
    eq(P0*z-z, "actual_z_old_M2_highest_weight")
    ys = (y, AF.mat(F10*y))
    zs = (z, AF.mat(F10*z))
    for vectors, label in ((ys, "y"), (zs, "z")):
        eq(F10*vectors[1], label+"_lowering_square_zero")
        eq(F10.H*vectors[0], label+"_raising_annihilates_highest")
        eq(F10.H*vectors[1]-vectors[0], label+"_matrix_unit_returns_highest")
    orbit = [AF.mat(u*v.H) for u in ys for v in zs]

    def six_C(matrix: s.MatrixBase) -> tuple[s.MatrixBase, s.MatrixBase]:
        blocks = (matrix, s.zeros(55))
        for n in range(8, 2, -1):
            A, B = AF.counts(n)
            Z, W = blocks
            blocks = (AF.mat(p*Z[:A, :A] + p*p*W),
                      AF.mat(Z[A:A+B, A:A+B]))
        return blocks

    coarse_orbit = [six_C(matrix) for matrix in orbit]
    orbit_gram = AF.mat(s.Matrix(4, 4, lambda i, j:
        s.trace(orbit[i].H*orbit[j])))
    coarse_gram = AF.mat(s.Matrix(4, 4, lambda i, j:
        p**4*s.trace(coarse_orbit[i][0].H*coarse_orbit[j][0])
        + p**5*s.trace(coarse_orbit[i][1].H*coarse_orbit[j][1])))
    eq(orbit_gram-s.eye(4), "actual_SL2_orbit_HS_Gram")
    eq(coarse_gram-p**10*(1-q_full)*s.eye(4),
       "actual_SL2_orbit_six_C_PF_Gram")
    ur, ui, vr, vi = s.symbols("ur ui vr vi", real=True)
    column = (ur+s.I*ui, vr+s.I*vi)
    coefficients = s.Matrix([u*s.conjugate(v) for u in column for v in column])
    f = sum(s.conjugate(v)*v for v in column)
    require(s.expand((coefficients.H*coefficients)[0]-f**2) == 0,
            "whole_complex_first_column_norm_not_finite_boost_sampling")
    require(AF.red((coefficients.H*coarse_gram*coefficients)[0]
                   - p**10*(1-q_full)*f**2) == 0,
            "whole_normalized_orbit_occupation_constant")
    Kz = old_m2(s.diag(s.Rational(1, 2), -s.Rational(1, 2)))
    Xdot = AF.mat(Kz*X + X*Kz.H)
    norm_jet = AF.red(s.trace(Xdot.H*X + X.H*Xdot))
    eq(norm_jet-2, "actual_nonzero_raw_z_boost_normalizer")
    Cdot = six_C(Xdot)
    coarse_norm_jet = AF.red(sum(weight*s.trace(D.H*C + C.H*D)
                               for weight, C, D in zip((p**4, p**5),
                                                       coarse, Cdot)))
    eq(coarse_norm_jet-p**10*(1-q_full)*norm_jet,
       "actual_z_boost_quotient_rule_cancels_normalizer")

    # The new #322 tuple bridge does NOT claim Lorentz equivariance. Test the
    # additional spectator-only continuation separately: character mismatch
    # rules out every fixed intertwiner, without changing the valid tuple map.
    A_spin = s.diag(-2*s.I, s.I/2)
    pauli = (s.eye(2), s.Matrix([[0, 1], [1, 0]]),
             s.Matrix([[0, -s.I], [s.I, 0]]), s.diag(1, -1))
    Lambda = s.Matrix(4, 4, lambda i, j:
        s.trace(pauli[i]*A_spin*pauli[j]*A_spin.H)/2)
    require(A_spin.det() == 1, "mixed_boost_rotation_is_in_SL2")
    require(Lambda == s.Matrix([[s.Rational(17, 8), 0, 0, s.Rational(15, 8)],
                               [0, -1, 0, 0], [0, 0, -1, 0],
                               [s.Rational(15, 8), 0, 0, s.Rational(17, 8)]]),
            "actual_Pauli_congruence_mixed_element")
    eta = s.diag(1, -1, -1, -1)
    require(Lambda.T*eta*Lambda == eta, "full_Lorentz_witness")
    exterior_characters = [sum(Lambda.extract(indices, indices).det()
                              for indices in combinations(range(4), k))
                           for k in range(5)]
    require(exterior_characters == [1, s.Rational(9, 4), -s.Rational(13, 2),
                                   s.Rational(9, 4), 1],
            "all_five_exterior_grades_retained")
    require(4*s.trace(Lambda) == 9 and sum(exterior_characters) == 0
            and (s.eye(4)+Lambda).det() == 0,
            "spectator_congruence_not_exterior_representation")

    rank, dimension = 34, 10946
    m = dimension - rank
    require(rank == 5**2+3**2 and dimension == 89**2+55**2 and m == 10912,
            "full_GNS_ranks_retained")
    require(5*89+3*55 == 610 and 610 != rank, "left_corner_not_full_GNS_inclusion")
    thermal = s.Rational(m, 2*rank+m)
    require(thermal == s.Rational(2728, 2745), "actual_full_thermal_occupation")
    gap = AF.red(q_full-thermal)
    eq(residual_source(q_full, 0, 1, 1, s.log(2), rank, dimension)-gap,
       "same_fixed_L_full_source")

    # Actual v7 ordinary-trace reduction: R(I)_i=m_i/n_i, R(JJ*)=I.
    # Determine both central sectors by literal inclusions of (I5,0), rather
    # than assume the recorded y has a chosen central distribution.
    central = (s.eye(5), s.zeros(3))
    for _n in range(3, 9):
        central = (s.diag(*central), central[0])
    u_A = AF.red((y.H*central[0]*y)[0])
    u_B = AF.red(1-u_A)
    require((s.Matrix([[1, 1], [1, 0]])**12*s.Matrix([5, 3])) == s.Matrix([1597, 987]),
            "ordinary_regular_multiplicities")
    require(5*1597+3*987 == dimension, "ordinary_reduced_trace_retains_full_dimension")
    beta, nu = s.symbols("beta nu", positive=True)
    x = s.exp(-beta*nu)
    ratios = (s.Rational(1597, 5), s.Rational(987, 3))
    prices = tuple(-s.log(1+x*(ratio-1))/beta for ratio in ratios)
    dprices = tuple(s.diff(v, nu).subs({beta: s.log(2), nu: 1}) for v in prices)
    require(dprices == (s.Rational(796, 801), s.Rational(164, 165)),
            "actual_v7_reduced_price_derivatives")
    eq(u_A-1, "recorded_source_central_weight_from_literal_inclusion")
    weighted_price_jet = AF.red(u_A*dprices[0]+u_B*dprices[1])
    reduced_source = AF.red(weighted_price_jet-thermal)
    archive_jet = AF.red(q_full-weighted_price_jet)
    eq(reduced_source+s.Rational(4, 81435), "actual_reduced_source_exact")
    eq(reduced_source+archive_jet-gap, "actual_archive_source_restores_full_source")

    # Nonzero signs use exact Q(a,sqrt(2)) arithmetic and rational root brackets.
    # sqrt(2) is present in the OWNED diagonal-difference path frame.
    boxes = _positive_root_boxes()
    gap_bounds = _bound(gap, a, p, boxes)
    archive_bounds = _bound(archive_jet, a, p, boxes)
    q_bounds = _bound(q_full, a, p, boxes)
    left_bounds = _bound(q_left, a, p, boxes)
    require(gap_bounds[1] < -s.Rational(1, 160), "fixed_gap_source_rigorously_negative")
    require(archive_bounds[1] < 0, "actual_archive_jet_cannot_be_dropped")
    require(0 < q_bounds[0] < q_bounds[1] < s.Rational(m, dimension),
            "actual_q_admits_conditional_positive_scalar_stationary_gap")
    require(left_bounds[1] < q_bounds[0], "left_and_full_corner_readouts_differ")

    # The all-level statement follows from K*K=I as proved above, not from
    # finite samples. These few dimensions check its exact indexing and signs.
    levels = [transported_refinement(q_full, N, s.log(2), s.S.One)
              for N in range(9, 13)]
    require([v["dimension"] for v in levels] == [10946, 28657, 75025, 196418],
            "full_GNS_refinement_dimensions")
    eq(levels[0]["source"]-gap, "refinement_starts_at_actual_A9_source")
    for before, after in zip(levels, levels[1:]):
        delta = s.simplify(after["source"]-before["source"])
        require(delta.is_Rational and delta < 0, "refinement_source_strictly_decreases")
    require(q_bounds[1] < s.Rational(79, 80), "refinement_limit_source_below_minus_one_over_80")
    limit_source = AF.red(q_full-1)
    eq(limit_source+p**6*(1-q_left), "exact_uniform_refinement_limit")

    # A small diagnostic jet tests the reusable evaluator, including the moving
    # normalization, a nonunitary state motion, and a moving inclusion. This
    # two-level fixture is not a replacement for the actual 10946-level source.
    t = s.symbols("t", real=True)
    psi = s.Matrix([1+t, 2])
    sigma_t = psi*psi.H/(psi.H*psi)[0]
    Jt = s.Matrix([s.cos(t), s.sin(t)])
    sigma0, dsigma0 = sigma_t.subs(t, 0), s.diff(sigma_t, t).subs(t, 0)
    J0, dJ0 = Jt.subs(t, 0), s.diff(Jt, t).subs(t, 0)
    q0, dq0 = occupation_jet(sigma0, dsigma0, J0, dJ0)
    require(q0 == s.Rational(4, 5) and dq0 == -s.Rational(28, 25), "moving_full_source_jet")
    direct_q = 1-(Jt.H*psi)[0]**2/(psi.H*psi)[0]
    require(s.simplify(s.diff(direct_q, t).subs(t, 0)-dq0) == 0,
            "independent_normalized_vector_derivative")
    require(occupation_jet(sigma0, s.zeros(2), J0, dJ0)[1] != dq0,
            "reject_frozen_preparation")
    require(occupation_jet(sigma0, dsigma0, J0, s.zeros(2, 1))[1] != dq0,
            "reject_frozen_inclusion")

    # Scalar closure is conditional on holding q fixed. Its envelope still has
    # nu* dq, so it supplies neither full stationarity nor a thermal state law.
    q = s.symbols("q", positive=True)
    nu_star = scalar_stationary_gap(q, beta, rank, dimension)
    x_star = rank*q/(m*(1-q))
    require(s.simplify(m*x_star/(rank+m*x_star)-q) == 0, "conditional_scalar_stationarity")
    require(s.simplify(beta*m*x/(rank+m*x)*(1-m*x/(rank+m*x))
                       - s.diff(s.log(rank+m*x)/beta+nu*q, nu, 2)) == 0,
            "strict_scalar_curvature_beta_pth_one_minus_pth")
    envelope = s.log(rank+m*x_star)/beta+nu_star*q
    require(s.simplify(s.diff(envelope, q)-nu_star) == 0, "conditional_envelope_retains_source")
    actual_p = (s.sqrt(5)-1)/2
    actual_sub = {p: actual_p, a: s.sqrt(actual_p)}
    approx = lambda value: str(s.N(value.subs(actual_sub, simultaneous=True), 18))
    return {
        "status": "PASS_NATIVE_ARCHIVE_OCCUPATION",
        "carrier": {"A3": [5, 3], "A9": [89, 55], "full_dimension": dimension,
                    "GNS_inclusion_rank": rank, "archive_rank": m, "left_corner_rank": 610},
        "exact": {"q_left": str(q_left), "q_full": str(q_full),
                  "fixed_gap_source": str(gap), "u_A": str(u_A),
                  "reduced_source": str(reduced_source), "archive_jet": str(archive_jet)},
        "diagnostic": {"q_full": approx(q_full), "fixed_gap_source": approx(gap),
                       "archive_jet": approx(archive_jet),
                       "conditional_nu_star": approx(scalar_stationary_gap(q_full, s.log(2), rank, dimension))},
        "rigorous_bounds": {"fixed_gap_source": [str(v) for v in gap_bounds],
                            "archive_jet": [str(v) for v in archive_bounds]},
        "transported_refinement": {
            "occupation": "q_N=q_full by K* K=I, for every N>=9",
            "fixed_rank": 34,
            "dimension": "D_N=F_(2N+3)",
            "source_at_beta_log2_nu1": "q_full-(D_N-34)/(D_N+34)",
            "uniform_source_upper_bound": "source_N<=source_9<-1/160",
            "limit_source": str(limit_source),
            "limit_source_upper_bound": "<-1/80",
            "conditional_nu_star_asymptotic": "(2 log(phi)/beta) N+O(1)",
            "full_GNS_lift_uniquely_forced_by_left_state": False,
        },
        "old_SL2_pullback": {
            "actual_orbit_GNS_Gram": "I4",
            "actual_six_C_Gram": "(1-q_full) I4",
            "raw_PF_squared_norm": "p^10 ||A e0||^4",
            "normalized_occupation": "q_archive(A)=q_full for every invertible A",
            "source_at_fixed_nu_beta_J": "nu dq_archive=0",
            "scope": "this pinned X9 state; not every preparation or full Cost-Info",
            "AF_tuple_bridge_input": "PR322 ce255de831f1e42a9429a5e767f1a9121a4ae2f3",
            "spectator_only_Lorentz_continuation": {
                "witness": "A=diag(-2i,i/2)",
                "four_vector_character": 9,
                "full_exterior_character": 0,
                "fixed_intertwiner_exists": False,
                "owner_tuple_bridge_remains_valid": True,
            },
        },
        "scope": {"actual_owned_AF_record": True, "six_literal_PF_adjoint_steps": True,
                  "full_heat_trace_and_archive_retained": True,
                  "one_occupation_plus_its_jet_suffices_for_this_family": True,
                  "diagnostic_state_jet_dimension": 2,
                  "physical_native_field_action_identified": False,
                  "physical_gap_variation_or_state_law_derived": False,
                  "full_variational_stationarity_proved": False},
        "source_pins": SOURCE_PINS,
    }


if __name__ == "__main__":
    result = run_checks()
    # Keep ordinary execution concise; callers can inspect the reusable dict.
    print(json.dumps({"status": result["status"], "carrier": result["carrier"],
                      **result["diagnostic"], "physical_native_action": "OPEN"}, sort_keys=True))
