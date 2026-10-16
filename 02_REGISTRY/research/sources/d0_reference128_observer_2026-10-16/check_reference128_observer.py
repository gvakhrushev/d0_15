#!/usr/bin/env python3
"""Bounded full16/reference128 observer-reading boundary; no old entrypoints.

The right-reference K below is a CONDITIONAL retained tensor, not an owned
native observer law. All tests are exact small matrix identities. They neither
replay a stationary root nor prove physical preparation or GR admission.
"""
from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
SOURCE_REF = "a4f4d4e86ae63336841337e1a93cd5296eb43792"
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
FOCK = "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py"
PINS = {
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    FOCK: "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md":
        "f7ea30d997a58fa4e608d4403acae5f5e3d7e5da45116f9a7c3f62be5e99115c",
    "02_REGISTRY/research/A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md":
        "04d38a6a126830fa857f4f7a06bf74789f21e283ed540d676ba8ea1de50e9184",
    "02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md":
        "040f26ba81a25959add549d01fb592c19bf102e6081e32e5b64a7102ab6fdc0c",
}


def require(condition, name):
    if not bool(condition):
        raise ArithmeticError("reference128_observer:" + name)


def owned_definitions(repo):
    """Only creator/order, record_basis, and three literal matrix assignments."""
    parsed = {}
    for path, expected in PINS.items():
        raw = (repo / path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, "source_pin:" + path)
        if path in (CURVED, FOCK):
            parsed[path] = ast.parse(raw)
    nodes = [node for node in parsed[CURVED].body
             if (isinstance(node, ast.FunctionDef) and node.name == "creator")
             or (isinstance(node, ast.Assign) and any(
                 isinstance(t, ast.Name) and t.id == "EXTERIOR_ORDER"
                 for t in node.targets))]
    require(len(nodes) == 2, "only_creator_and_order")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, "exec"), scope)
    creators = tuple(scope["creator"](i) for i in range(4))
    gate_tree = parsed[FOCK]
    basis = next(n for n in gate_tree.body
                 if isinstance(n, ast.FunctionDef) and n.name == "record_basis")
    controls = next(n for n in gate_tree.body
                    if isinstance(n, ast.FunctionDef) and n.name == "controls")
    literals = [n for n in controls.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id in ("U", "P", "T") for t in n.targets)]
    require(len(literals) == 3, "only_literal_gate_cut_and_chart_assignments")
    a, p = s.symbols("golden_a golden_p", real=True)
    gate_scope = {"s": s, "a": a, "p": p}
    exec(compile(ast.Module(body=[basis] + literals, type_ignores=[]), FOCK, "exec"),
         gate_scope)
    return creators, scope["EXTERIOR_ORDER"], gate_scope, a, p


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    cs, order, gate, ga, gp = owned_definitions(repo)
    checks = []
    c, z = s.symbols("boost_c boost_s", real=True)
    x, y = s.symbols("rotation_c rotation_s", real=True)
    a, b = s.symbols("amplitude_a amplitude_b", real=True)

    def red(value):
        value = s.expand(value)
        if value == 0:
            return value
        value = s.rem(value, c*c-z*z-1, c)
        return s.expand(s.rem(value, x*x+y*y-1, x))

    def eq(actual, expected, name, reducer=red):
        difference = actual - expected
        entries = difference if isinstance(difference, s.MatrixBase) else (difference,)
        require(all(reducer(v) == 0 for v in entries if v != 0), name)
        checks.append(name)

    def yes(condition, name):
        require(condition, name)
        checks.append(name)

    I = s.eye(16)
    beta = tuple(k + k.T for k in cs)
    H = tuple(cs[0]*cs[j].T + cs[j]*cs[0].T for j in range(1, 4))
    chi = s.zeros(16, 1)
    for mask in (0, 1, 14, 15):
        chi[mask] = s.Rational(1, 2)
    P = chi*chi.T
    C = a*I + (b-a)*P
    rho = a*a*I + (b*b-a*a)*P
    norm = 15*a*a+b*b
    yes(order == (0, 2, 3, 1), "actual_ACDB_order")
    eq(chi.dot(chi), 1, "balanced_chi_normalized")
    eq(C*C, rho, "whole_rank_path_density_no_extra_slot")
    eq(s.trace(rho), norm, "full_path_HS_normalizer")
    eq(beta[0]*chi, chi, "balanced_chi_beta0_eigenvector")
    eq(C*beta[0], beta[0]*C, "path_commutes_with_reference_K")
    for i in range(4):
        for j in range(4):
            eq(cs[i]*cs[j].T+cs[j].T*cs[i], int(i == j)*I,
               f"owned_full16_CAR_{i}_{j}")
            eq(beta[i]*beta[j]+beta[j]*beta[i], 2*int(i == j)*I,
               f"full16_beta_Clifford_{i}_{j}")
        eq(s.trace(C.T*beta[i]*C*beta[0]), int(i == 0)*norm,
           f"conditional_reference_correlation_at_center_{i}")
    tangent = [beta[i]*C*beta[0]-int(i == 0)*C for i in range(4)]
    for i in range(4):
        for j in range(4):
            eq(s.trace(tangent[i].T*tangent[j]),
               (int(i == j)-int(i == 0)*int(j == 0))*norm,
               f"conditional_correlation_matter_tangent_Gram_{i}_{j}")
    for j, h in enumerate(H):
        eq(h.T, h, f"Hermitian_exterior_boost_{j}")
        eq(h*h*h, h, f"exterior_boost_minimal_polynomial_{j}")
        eq(s.trace(rho*h), 0, f"centering_value_all_path_{j}")
        for k, h2 in enumerate(H):
            eq(s.trace(rho*(h*h2+h2*h)), int(j == k)*norm,
               f"centering_jacobian_minus_identity_{j}_{k}")
        lift = I + (c-1)*h*h-z*h
        inverse = I + (c-1)*h*h+z*h
        eq(lift*inverse, I, f"true_full16_boost_lift_inverse_{j}")
        eq(lift.T, lift, f"positive_symmetric_boost_lift_{j}")
        w = lift*C
        eq(s.trace(w.T*w), c*c*norm, f"raw_fixed_norm_cosh_squared_{j}")
        for i in range(4):
            eq(s.trace(w.T*beta[i]*w*beta[0]), int(i == 0)*c*norm,
               f"raw_fixed_correlation_sech_no_direction_inverse_{j}_{i}")
        for sign in (-1, 1):
            projector = (h*h+sign*h)/2
            eq(s.trace(rho*projector), norm/4,
               f"geodesic_boost_spectral_weight_{j}_{sign}")

    # O(4) changes causal g while G and coordinate-form C remain fixed.
    J4 = s.zeros(4)
    J4[0, 1], J4[1, 0] = 1, -1
    J = cs[0]*cs[1].T-cs[1]*cs[0].T
    O = s.eye(4)+y*J4+(1-x)*J4*J4
    rotation = I+y*J+(1-x)*J*J
    eta = s.diag(1, -1, -1, -1)
    eta_ext = s.diag(*[(-1)**bin(mask & 14).count("1") for mask in range(16)])
    U = rotation.T*eta_ext
    eq(rotation.T*rotation, I, "all_grade_rotation_isometry")
    eq(U.T*U, I, "coordinate_form_B_e_isometry_at_G_identity")
    for i in range(4):
        expected = sum((O[k, i]*cs[k] for k in range(4)), s.zeros(16))
        eq(rotation*cs[i]*rotation.T, expected,
           f"actual_exterior_rotation_creator_intertwiner_{i}")
    native_rho = U.T*rho*U
    eq(s.trace(native_rho), norm, "same_coordinate_state_native_norm")
    faithful = U.T*(I/16)*U
    eq(faithful, I/16, "faithful_cone_fibre_density_identical")
    for j, h in enumerate(H):
        eq(s.trace(native_rho*h), 0, f"cone_fibre_centering_still_zero_{j}")
        for k, h2 in enumerate(H):
            diagonal = norm if j == 0 else 16*a*a+(b*b-a*a)*x*x
            eq(s.trace(native_rho*(h*h2+h2*h)),
               diagonal if j == k else 0,
               f"cone_fibre_centering_regular_near_identity_{j}_{k}")
    eq(O.T*O, s.eye(4), "cone_family_positive_G_fixed")
    changed_g = (O.T*eta*O).subs({x: s.Rational(4, 5), y: s.Rational(3, 5)})
    yes(changed_g != eta and changed_g.det() == -1,
        "centered_cone_family_changes_nongauge_Lorentz_metric")
    eq(changed_g[0, 1], s.Rational(24, 25), "explicit_changed_causal_cross_slot")

    # A literal eight-block, 128-reference witness; all columns are retained.
    fixture = (I+6*P)/8  # a=1/8,b=7/8: density=I/64+3P/4.
    C128 = s.SparseMatrix(s.kronecker_product(s.eye(8), fixture)/s.sqrt(8))
    K128 = s.SparseMatrix(s.kronecker_product(s.eye(8), beta[0].T))
    yes(C128.shape == (128, 128) and K128.shape == (128, 128),
        "eight_by_sixteen_reference_exactly128_not136")
    eq(s.trace(C128.T*C128), 1, "literal_reference128_normalizer")
    for i in range(4):
        B128 = s.SparseMatrix(s.kronecker_product(s.eye(8), beta[i]))
        eq(s.trace(C128.T*B128*C128*K128), int(i == 0),
           f"literal_reference128_full_correlation_{i}")

    # Signed Choi metric is necessarily rank-one on the balanced endpoint.
    first = s.zeros(4, 16)
    for i in range(4):
        first[i, 1 << i] = 1
    signed_ref = first.T*eta*first
    eq((first*(I/4))*signed_ref*(first*(I/4)).T, eta/16,
       "signed_Choi_faithful_reconstructs_reference_eta")
    endpoint = first*P
    endpoint_metric = endpoint*signed_ref*endpoint.T
    yes(endpoint.rank() == 1 and endpoint_metric.rank() == 1,
        "signed_Choi_balanced_rank_one_cannot_reconstruct_metric")
    noncentered = s.zeros(16, 1)
    noncentered[1] = noncentered[2] = 1/s.sqrt(2)
    eq(H[0]*noncentered, noncentered,
       "prep_critical_scalar_shell_does_not_force_norm_centering")

    # Pin the actual golden gate/cut pointer without executing its old controls.
    def golden_red(v):
        return s.expand(s.rem(s.rem(s.expand(v), ga*ga-gp, ga), gp*gp+gp-1, gp))
    T = gate["T"]
    U4, P4 = T.T*gate["U"]*T, T.T*gate["P"]*T
    B0 = gate["record_basis"]()
    native_gate = B0*s.kronecker_product(U4, s.eye(4))*B0.T
    native_cut = B0*s.kronecker_product(P4, s.eye(4))*B0.T
    Z = 2*native_cut-I
    eq(native_gate.T*native_gate, I, "literal_owned_golden_gate_unitarity", golden_red)
    eq(Z, I-2*cs[0]*cs[0].T, "literal_owned_price_cut_is_time_occupation", golden_red)
    eq(native_gate.T*Z*native_gate, gp**3*Z-2*ga*gp*beta[0],
       "owned_gate_price_pointer_beta0_identity", golden_red)

    return {
        "status": "PASS",
        "source_ref": SOURCE_REF,
        "source_pins": PINS,
        "exact_checks": checks,
        "exact_check_count": len(checks),
        "carrier": {"Fock_dimension": 16, "momentum_blocks": 8,
                    "purifying_reference_dimension": 128,
                    "retained_workspace_deleted": False},
        "correlation": {
            "K": "I8 tensor beta0^T; conditional retained reference tensor",
            "same128_rank_path": "128 to8; C_theta uses no seventeenth per-mode slot",
            "raw_fixed_boost_q": "(sech(r),0,0,0)",
            "observer_alignment_Jacobian_rank": 0,
            "conditional_joint_constraint_matter_rank": 3},
        "centering": {
            "at_path": "<H_i>=0; Re<H_i H_j>=delta_ij/2",
            "observer_Jacobian": "-I3", "observer_Jacobian_rank": 3,
            "exact_norm": "N0 cosh(r)^2",
            "log_norm_second_derivative_radial": "2 sech(r)^2 >0",
            "unique_center_line_for_path": True,
            "coercive_for_path": True,
            "faithful_fixed_G_coordinate_state_cone_fibre_survives": True},
        "scope": {
            "native_reference_K_selection_derived": False,
            "centering_forced_by_native_price": False,
            "observer_law_or_causal_source_closed": False,
            "old_scientific_entrypoints_executed": False,
            "physical_admission_or_GR_claim": False},
        "gate_pointer": {
            "identity": "U_n^* Z_n U_n=p^3 Z_n-2 a p beta_n; Z_n=2P_n-I",
            "source": FOCK,
            "executed_old_definitions_only": ["record_basis", "literal U/P/T assignments"],
            "reference128_copy_initialization_or_measurement_derived": False},
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
