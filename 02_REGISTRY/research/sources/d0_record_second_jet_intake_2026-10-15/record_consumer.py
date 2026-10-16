#!/usr/bin/env python3
"""Consume the archived U(4) fixture; check actual normal metric variations.

The imported script was inspected before intake: it performs finite SymPy
algebra and prints JSON, without file or network writes. Its definitions and
checks are reused, not copied. This consumer adds the normal-field condition,
unitary deformation jets, dual packing, nonzero Christoffel normalization,
and the distinction between ambient and unitary-graph normal directions.
No native operation/action/observer/admission law is selected.
"""
from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
ORIGINAL = (
    "02_REGISTRY/research/sources/d0_record_second_jet_intake_2026-10-15/"
    "INPUT_check_record_2jet.py"
)
ORIGINAL_SHA256 = "2b99efc7c09df0aad2b3c8df25600d423582d203031c19c98af71d293931c3a3"


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    original_path = repo / ORIGINAL
    if hashlib.sha256(original_path.read_bytes()).hexdigest() != ORIGINAL_SHA256:
        raise RuntimeError("archived_2jet_source_pin")
    captured = io.StringIO()
    with redirect_stdout(captured):
        fixture = runpy.run_path(str(original_path))
    original_result = json.loads(captured.getvalue())
    checks: list[str] = []

    def require(condition: object, name: str) -> None:
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    def eq(actual, expected, name: str) -> None:
        delta = actual - expected
        entries = list(delta) if isinstance(delta, s.MatrixBase) else [delta]
        require(all(s.simplify(v) == 0 for v in entries), name)

    E = fixture["P1"]
    Z = fixture["P2"]
    normals = fixture["Normals"]
    pairs = fixture["pairs"]
    generators = fixture["B"]
    first_u = fixture["U1"]
    ip = fixture["ip"]  # Re Tr(X*Y)/(2d), d=4; fixture matrices are Hermitian.
    block = fixture["block"]
    p = fixture["p"]
    d = 4
    scale2 = p**3
    ap = s.sqrt(p) * p

    require(original_result["second_source_map_rank"] == 10,
            "original_finite_fixture_completed")
    eq(s.Matrix([[ip(u, v) for v in normals] for u in normals]), s.eye(10),
       "chosen_normal_Gram_before_p3_scaling")

    # The actual projector, rather than only an unconstrained Hermitian map.
    P0 = (p*s.eye(d)).row_join(ap*s.eye(d)).col_join(
        (ap*s.eye(d)).row_join(p**2*s.eye(d)))
    eq(P0*P0, P0, "actual_golden_record_projector")
    for k, N in enumerate(normals):
        eq(P0*(ap*N)+(ap*N)*P0, ap*N,
           "chosen_normal_is_projector_tangent_"+str(k))

    # Extend each point normal WITHIN the unitary graph. Start from the field
    # Y_A=dP_U[i B_A U] and subtract its tangent projection at every x.
    # At zero projection coefficients vanish. Their derivatives are
    # c_(nu,mu)=<Z_(mu,nu),N_A>+<E_nu,partial_mu Y_A>, since G(0)=I.
    # This produces a genuine normal field near zero; using i B_A U alone
    # would instead be an ambient-isometric left translation, with dq=0.
    metric_columns = []
    raw_metric_columns = []
    for k, (pair, N) in enumerate(zip(pairs, normals)):
        B = generators[pair]
        raw_u = [s.I*B*first_u[mu] for mu in range(4)]
        raw_y = [block(v.conjugate().T, v) for v in raw_u]
        coefficients = s.Matrix(4, 4, lambda nu, mu:
            ip(Z[mu, nu], N) + ip(E[nu], raw_y[mu]))
        normal_y = [raw_y[mu] - sum(
            (coefficients[nu, mu]*E[nu] for nu in range(4)), s.zeros(8))
            for mu in range(4)]
        normal_u = [raw_u[mu] - sum(
            (coefficients[nu, mu]*first_u[nu] for nu in range(4)), s.zeros(4))
            for mu in range(4)]
        du0 = s.I*B
        eq(du0+du0.conjugate().T, s.zeros(4),
           "unitary_normal_value_"+str(k))
        for mu in range(4):
            eq(normal_u[mu]+normal_u[mu].conjugate().T
               +du0*first_u[mu].conjugate().T
               +first_u[mu]*du0.conjugate().T, s.zeros(4),
               "actual_linearized_unitarity_"+str((k, mu)))
            for nu in range(4):
                eq(ip(E[nu], normal_y[mu])+ip(Z[mu, nu], N), 0,
                   "derivative_of_normal_field_"+str((k, mu, nu)))
        metric_columns.append(s.Matrix([
            scale2*(ip(E[mu], normal_y[nu])+ip(normal_y[mu], E[nu]))
            for mu, nu in pairs]))
        raw_metric_columns.append(s.Matrix([
            ip(E[mu], raw_y[nu])+ip(raw_y[mu], E[nu]) for mu, nu in pairs]))
    metric_map = s.Matrix.hstack(*metric_columns)
    eq(metric_map, -2*scale2*s.eye(10), "actual_normal_field_metric_map")
    eq(s.Matrix.hstack(*raw_metric_columns), s.zeros(10),
       "point_normal_left_translation_alone_has_zero_metric_variation")
    eq(metric_map*(-s.eye(10)/(2*scale2)), s.eye(10),
       "ten_slot_coefficient_right_inverse")

    # Full symmetric-tensor contraction has weight two off diagonal.
    weights = [1 if mu == nu else 2 for mu, nu in pairs]
    packing = s.diag(*weights)
    covector_map = metric_map.T*packing
    off = pairs.index((0, 1))
    eq(covector_map[off, off], -4*scale2,
       "offdiagonal_tensor_contraction_counts_both_entries")
    require(covector_map[off, off] != metric_map[off, off],
            "reject_unweighted_offdiagonal_covector")
    # In the packed DUAL coordinates e=(E00,2E01,...), the pullback is M^T e.
    eq(metric_map.T, -2*scale2*s.eye(10), "packed_dual_pullback")

    # The origin has Gamma=0 and cannot detect an omitted 1/(2d). A true
    # reparametrization x0=y0+kappa*y0^2/2 yields Gamma^0_00=kappa.
    kappa = s.Rational(3, 2)
    reparam_second = Z[0, 0]+kappa*E[0]
    gamma = s.Matrix([ip(v, reparam_second) for v in E])
    eq(gamma, s.Matrix([kappa, 0, 0, 0]),
       "Christoffel_with_actual_normalized_inner_product")
    eq(reparam_second-sum((gamma[mu]*E[mu] for mu in range(4)), s.zeros(8)),
       Z[0, 0], "second_fundamental_form_reparametrization")
    wrong_gamma = s.Matrix([s.re(s.trace(v*reparam_second)) for v in E])
    eq(wrong_gamma, 2*d*gamma, "missing_normalization_multiplies_Gamma_by_2d")
    require(wrong_gamma != gamma, "reject_unnormalized_Christoffel")

    # The zero in the input's linear control is a restriction of its normal
    # probes. Ambient Hermitian normals also contain the quadratic term.
    linear = fixture["P2linear"]
    linear_gram = s.Matrix([[ip(linear[u], linear[v]) for v in pairs] for u in pairs])
    full_gram = s.Matrix([[ip(Z[u], Z[v]) for v in pairs] for u in pairs])
    require(linear_gram.rank() == 4, "linear_H_ambient_second_normal_span_rank4")
    require(full_gram.rank() == 10, "full_fixture_ambient_second_normal_span_rank10")
    require(fixture["Clinear"] == s.zeros(10),
            "linear_H_selected_unitary_graph_normal_map_rank0")
    require(linear_gram.rank() != fixture["Clinear"].rank(),
            "reject_rank0_for_all_ambient_normals")
    # A nonzero Hermitian lower block is not an infinitesimal U(4) return.
    require(linear[(0, 0)][4:8, 0:4]
            +linear[(0, 0)][4:8, 0:4].conjugate().T != s.zeros(4),
            "ambient_quadratic_normal_is_not_unitary_graph_tangent")

    sectional = {str((mu, nu)):
                 ip(Z[mu, mu], Z[nu, nu])-ip(Z[mu, nu], Z[mu, nu])
                 for mu, nu in pairs if mu < nu}
    eq(2*sum(sectional.values()), -6, "full_ambient_Gauss_scalar_times_p3")
    require(sorted(sectional.values()) == [-1, -1, -1, 0, 0, 0],
            "full_sectional_curvatures_times_p3")

    # Inspecting labels rather than reconstructing another Pauli fixture.
    require(len(pairs) == 10 and len(fixture["A"]) == 4,
            "original_four_parameter_ten_symmetric_slots")
    return {
        "status": "PASS_RECORD_SECOND_JET_CONSUMER",
        "exact_check_count": len(checks),
        "source": {"path": ORIGINAL, "sha256": ORIGINAL_SHA256,
                   "original_script_executed_once": True,
                   "old_repository_suites_executed": False},
        "metric": "p^3 I4",
        "normal_metric_map": "-2 p^3 I10 in upper-coordinate / normal-coefficient norms",
        "packed_covector": "(E00,2E01,2E02,2E03,E11,2E12,2E13,E22,2E23,E33)",
        "Christoffel_reparametrization": "Gamma^0_00=3/2; raw trace would give12",
        "linear_control": {"selected_unitary_graph_normal_rank": 0,
                           "ambient_second_normal_span_rank": 4,
                           "full_fixture_second_normal_span_rank": 10},
        "curvature": {"p3_times_scalar": -6,
                      "p3_times_sectional": {k: str(v) for k, v in sectional.items()}},
        "scope": {"actual_unitary_normal_fields_constructed": True,
                  "varying_quadratic_coefficients_alone_is_metric_variation": False,
                  "native_field_action_or_operation_admission_derived": False,
                  "Lorentz_observer_or_beta_law_selected": False,
                  "physical_GR_source_closure": False},
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), ensure_ascii=False, sort_keys=True, indent=2))
