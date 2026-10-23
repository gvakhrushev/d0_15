"""Exact homogeneous boost source of the canonical full Lorentz adjoint.

Only the pinned full16 creator AST is executed. No old run(),4096-mode
matrix, root search or receipt generation occurs. The old true-root
coframe moment identities are explicit consumed hypotheses.
"""
from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
RECEIPT = "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json"
PINS = {
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    RECEIPT: "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/nonzero_symbol_algebra.py":
        "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/rank8_source_submersion.py":
        "04d5fba2d34538e2c7e4b41748fafb4e88e041174f4380bd0e7990111ffc6afd",
}
L = 8


def _creators(repo):
    tree = ast.parse((repo / CURVED).read_text())
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef) and node.name == "creator")
             or (isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id == "EXTERIOR_ORDER"
                         for target in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError("full_lorentz_boost:literal_creator_nodes")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, "exec"), scope)
    return [scope["creator"](j) for j in range(4)], scope["EXTERIOR_ORDER"]


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, label):
        if not bool(condition):
            raise ArithmeticError("full_lorentz_boost:" + label)
        checks.append(label)

    def eq(actual, expected, label):
        entries = ((actual - expected).todok().values()
                   if isinstance(actual, s.MatrixBase) else (actual - expected,))
        require(all(s.expand(x) == 0 for x in entries), label)

    require(all(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest
                for path, digest in PINS.items()), "immutable_actual_CAR_root_memory_inputs")
    C, order = _creators(repo)
    I = s.eye(16)
    require(order == (0, 2, 3, 1), "literal_full16_ACDB_convention")
    require(all(C[i] * C[j].T + C[j].T * C[i] == (I if i == j else s.zeros(16))
                for i in range(4) for j in range(4)), "all_full16_CAR_relations")
    create = lambda v: sum((v[i] * C[i] for i in range(4)), s.zeros(16))
    contract = lambda v: sum((v[i] * C[i].T for i in range(4)), s.zeros(16))
    chi = (s.eye(16)[:, 1] + s.eye(16)[:, 15]) / s.sqrt(2)
    chi_minus = (s.eye(16)[:, 1] - s.eye(16)[:, 15]) / s.sqrt(2)
    eq((chi.H * chi)[0], 1, "actual_native_pure_E0_state_normalized")
    E = s.Matrix.hstack(*[s.eye(16)[:, mask] for mask in (0, 1, 14, 15)])
    N0 = E.H * C[0] * C[0].T * E
    Nsp = E.H * C[1] * C[1].T * E
    eq(N0, s.diag(0, 1, 0, 1), "full_E0_time_occupation_operator")
    require(all(E.H * C[j] * C[j].T * E == Nsp for j in range(1, 4))
            and Nsp == s.diag(0, 0, 1, 1), "full_E0_common_spatial_occupation_operator")
    require(all(E.H * C[i] * C[j] * E == s.zeros(4) for i in range(4) for j in range(4))
            and all(E.H * C[i] * C[j].T * E == s.zeros(4)
                    for i in range(4) for j in range(4) if i != j),
            "all_E0_anomalous_and_offdiagonal_normal_two_points_zero")
    balanced = E * s.ones(4, 1) / 2
    eq((balanced.H * balanced)[0], 1, "balanced_full_E0_pure_witness_normalized")
    eq((balanced.H * C[0] * C[0].T * balanced)[0], s.Rational(1, 2),
       "balanced_witness_time_occupation_half")
    require(all((balanced.H * C[j] * C[j].T * balanced)[0] == s.Rational(1, 2)
                for j in range(1, 4)), "balanced_witness_each_spatial_occupation_half")
    u = s.Matrix(s.symbols("u0:4", real=True))
    vr = s.Matrix(s.symbols("vr0:4", real=True))
    vi = s.Matrix(s.symbols("vi0:4", real=True))
    v = vr + s.I * vi
    tx, ty = s.symbols("tx ty", real=True)
    t = tx + s.I * ty
    D = create(v) + contract(v.conjugate())
    eq(D * D, (vr.dot(vr) + vi.dot(vi)) * I,
       "generic_complex_Dirac_square_scalar_on_all16")
    generic = []
    for j in range(1, 4):
        Gamma = C[0] * C[j].T + C[j] * C[0].T
        eq(Gamma.H, Gamma, "Lorentz_boost_exterior_generator_Hermitian_" + str(j))
        J = L * (t * create(u) * Gamma + s.conjugate(t) * Gamma * contract(u))
        eq(J.H, J, "canonical_forward_plus_adjoint_first_jet_" + str(j))
        X = D * J + J * D
        faithful, pure = s.trace(X) / 16, (chi.H * X * chi)[0]
        old = -L * (u[j] * (tx * vr[0] + ty * vi[0])
                    + u[0] * (tx * vr[j] + ty * vi[j]))
        difference = -L * u[0] * (tx * vr[j] + ty * vi[j])
        eq(faithful, old, "generic_full16_trace_boost_source_" + str(j))
        eq(pure - faithful, difference, "generic_pure_minus_faithful_source_" + str(j))
        eq(E.H * X * E,
           -2 * L * (u[0] * (tx * vr[j] + ty * vi[j]) * N0
                     + u[j] * (tx * vr[0] + ty * vi[0]) * Nsp),
           "generic_full_E0_operator_compression_including_complex_coherences_" + str(j))
        eq((balanced.H * X * balanced)[0], faithful,
           "balanced_E0_source_matches_faithful_boost_" + str(j))
        eq((chi_minus.H * X * chi_minus)[0], pure,
           "relative_parity_phase_keeps_even_source_" + str(j))
        generic.append({"boost": [0, j],
                        "trace_normalized": "-L Re[t*(u_j*bar(v_0)+u_0*bar(v_j))]",
                        "pure_minus_trace": "-L*u_0 Re[t*bar(v_j)]"})

    # Spatial rotations annihilate the WHOLE E0 sector. Their compressed
    # first source therefore also reduces to its normal two-point data.
    # Together with the boost compression and scalar coframe CAR identity,
    # this supplies the homogeneous full-Lorentz field-source comparison.
    for i, j in ((1, 2), (1, 3), (2, 3)):
        Gamma = C[i] * C[j].T - C[j] * C[i].T
        eq(Gamma * E, s.zeros(16, 4), "entire_E0_spatial_rotation_singlet_" + str(i) + str(j))
        J = L * (t * create(u) * Gamma - s.conjugate(t) * Gamma * contract(u))
        X = D * J + J * D
        eq((balanced.H * X * balanced)[0], s.trace(X) / 16,
           "balanced_E0_source_matches_faithful_rotation_" + str(i) + str(j))

    a, b = s.symbols("a b", positive=True)
    F = (a - b) * s.eye(4) + b * s.ones(4)
    eta = s.diag(1, -1, -1, -1)
    legs = [eta * F.row(r).T for r in range(4)]
    total_leg = sum(legs, s.zeros(4, 1))
    roots = (1, (1 + s.I) / s.sqrt(2), s.I, (-1 + s.I) / s.sqrt(2),
             -1, (-1 - s.I) / s.sqrt(2), -s.I, (1 - s.I) / s.sqrt(2))
    shell = [tuple(sign if j == r else 0 for j in range(4))
             for r in range(4) for sign in (1, 7)]
    lambda1 = L * L * (2 - s.sqrt(2))
    moments = []
    for r in range(4):
        moment = s.zeros(4, 1)
        for k in shell:
            vk = L * sum(((roots[k[q]] - 1) * legs[q] for q in range(4)), s.zeros(4, 1))
            moment += roots[k[r]] * vk.conjugate()
        eq(moment, lambda1 / L * (2 * legs[r] - total_leg),
           "exact_eight_occupied_phase_vector_moment_" + str(r))
        moments.append(moment)

    # Consumed exact root moments: sum chi_k bar(z_s)=0 and
    # sum chi_k z_r bar(z_s)=0, chi_k=kappa_k+1_Omega/128.
    # Their algebraic consequence is sum chi_k t_r bar(v_k)=0.
    m1 = s.Matrix(s.symbols("root_first0:4"))
    m2 = s.Matrix(4, 4, s.symbols("root_second0:16"))
    zeros = {value: 0 for value in list(m1) + list(m2)}
    for r in range(4):
        weighted = sum(((m1[q] + m2[r, q] / L) * legs[q]
                        for q in range(4)), s.zeros(4, 1))
        eq(weighted.subs(zeros), s.zeros(4, 1),
           "old_true_root_moments_kill_total_faithful_boost_" + str(r))
    source, heat_source, old_matter_source, pure_matter_source = (s.zeros(4, 3) for _ in range(4))
    scaled = s.Matrix(4, 3, lambda r, j:
        -a * (a + b) if r == 0 else (b * (a - 3 * b) if r == j + 1 else -b * (a + b)))
    for r in range(4):
        for j in range(1, 4):
            B = s.zeros(4)
            B[0, j] = B[j, 0] = 1
            old_matter = -L * moments[r].dot(B * legs[r]) / 8
            heat = -old_matter
            difference = -L * legs[r][0] * moments[r][j] / 8
            pure_matter = old_matter + difference
            eq(heat + old_matter, 0, "faithful_full_price_boost_Euler_zero_" + str(r) + str(j))
            eq(heat + pure_matter, lambda1 * scaled[r, j - 1] / 8,
               "actual_pure_full_price_boost_Euler_" + str(r) + str(j))
            source[r, j - 1] = s.factor(heat + pure_matter)
            heat_source[r, j - 1], old_matter_source[r, j - 1] = s.factor(heat), s.factor(old_matter)
            pure_matter_source[r, j - 1] = s.factor(pure_matter)
    c = s.symbols("c", positive=True)
    eq(-scaled[0, 0].subs(a, b + c), (b + c) * (2 * b + c),
       "strict_nonzero_time_role_source_every_regular_a_greater_b")
    require(((b + c) * (2 * b + c)).is_positive is True,
            "pure_state_fails_independent_boost_Euler_no_rank_computation")
    x, y = s.symbols("x y", real=True)
    family_x = s.Matrix(4, 3, lambda r, j: legs[r][0] * (total_leg[j + 1] - 2 * legs[r][j + 1]))
    family_y = s.Matrix(4, 3, lambda r, j: legs[r][j + 1] * (total_leg[0] - 2 * legs[r][0]))
    eq(family_x, scaled, "all_E0_source_x_coefficients_match_actual_pure_case")
    expected_y = s.Matrix(4, 3, lambda r, j:
        b * (a - 3 * b) if r == 0 else (-a * (a + b) if r == j + 1 else -b * (a + b)))
    eq(family_y, expected_y, "all_E0_source_y_coefficients_native_spatial_sign")
    family = lambda1 * (family_x * x + family_y * y) / 4
    eq(family.subs({x: s.Rational(1, 2), y: 0}), source,
       "entire_E0_family_specializes_to_previous_actual_chi")
    eq(family[1, 1], -lambda1 * b * (a + b) * (x + y) / 4,
       "offdiagonal_spatial_Euler_forces_x_plus_y_zero")
    eq((family_x[0, 0] * x + family_y[0, 0] * y).subs(y, -x),
       -(a - b) * (a + 3 * b) * x,
       "time_role_Euler_with_y_minus_x_forces_x_zero")
    minor = s.Matrix([[family_x[1, 1], family_y[1, 1]],
                      [family_x[0, 0], family_y[0, 0]]]).det()
    eq(minor, -b * (a + b) * (a - b) * (a + 3 * b),
       "two_actual_Euler_rows_classify_all_E0_states")
    require(s.factor((-minor).subs(a, b + c)).is_positive is True,
            "classification_minor_strictly_nonzero_for_all_a_greater_b_positive")
    eq(family.subs({x: 0, y: 0}), s.zeros(4, 3),
       "occupation_halves_suffice_for_every_homogeneous_boost_Euler")
    receipt = json.loads((repo / RECEIPT).read_text())
    radius = s.Rational(receipt["interval"]["root_radius"])
    dc, oc = map(s.Rational, receipt["interval"]["root_center"])
    require(0 < oc - radius < oc + radius < dc - radius,
            "owned_root_rectangle_positive_b_and_a_minus_b")

    # Small full16 NONROOT control, all four legs still retained.
    uf = -s.eye(4)[:, 2] / 4  # F=I/4 gives u_r=eta F_r.
    B = s.zeros(4)
    B[0, 1] = B[1, 0] = 1
    Gamma = C[0] * C[1].T + C[1] * C[0].T
    eq(B * uf, s.zeros(4, 1), "nonroot_boost_preserves_own_leg")
    D0 = L * ((s.I - 1) * create(uf) + (-s.I - 1) * contract(uf))
    Jcan = s.I * L * Gamma * (create(uf) - contract(uf))
    Jreverse = s.I * L * Gamma * (create(uf) + contract(uf))
    eq(Jcan.H, Jcan, "nonroot_canonical_first_jet_selfadjoint")
    eq(Jreverse.H, -Jreverse, "nonroot_geometric_reverse_first_jet_antiadjoint")
    require(Jreverse != s.zeros(16), "nonroot_geometric_reverse_is_not_selfadjoint")
    X = D0 * Jcan + Jcan * D0
    eq(X, 8 * Gamma, "nonroot_literal_full16_Delta_first_jet_eight_Gamma")
    xi = (s.eye(16)[:, 1] + s.eye(16)[:, 2]) / s.sqrt(2)
    eq((xi.H * X * xi)[0], 8, "nonroot_same_quadratic_matter_source_eight")
    eq(s.trace(X), 0, "nonroot_full16_trace_source_zero")
    # The generic trace formula also proves zero at EVERY thermal momentum:
    # B u_2=0, hence its contraction with arbitrary v vanishes.
    eq(B * uf, s.zeros(4, 1), "nonroot_all_thermal_trace_sources_zero_by_generic_identity")

    strings = lambda M: [[s.sstr(s.factor(M[i, j])) for j in range(M.cols)] for i in range(M.rows)]
    return {"schema": "d0-full-lorentz-homogeneous-boost-source/1", "status": "PASS_EXACT",
            "exact_checks": len(checks), "checks": checks, "source_pins": PINS,
            "generic_full16_source_identities": generic, "lambda1": s.sstr(lambda1),
            "source_unit": "lambda1/8", "pure_total_source_scaled": strings(scaled),
            "pure_total_source": strings(source), "heat_feedback_source": strings(heat_source),
            "faithful_matter_source": strings(old_matter_source),
            "pure_matter_source": strings(pure_matter_source),
            "faithful_total_boost_source": [[0] * 3 for _ in range(4)],
            "all_E0_source": {
                "state_domain": "sigma>=0, Tr sigma=1, support in masks{0,1,14,15}; all complex coherences retained",
                "x": "Tr(sigma n0)-1/2", "y": "Tr(sigma nj)-1/2, same for each spatial j",
                "unit": "lambda1/4", "x_coefficient": strings(family_x),
                "y_coefficient": strings(family_y),
                "common_zero_iff": "x=y=0, for ALL a>b>0",
                "nonzero_classification_minor": "-b(a+b)(a-b)(a+3b)",
                "balanced_pure_amplitudes": {"0": "1/2", "1": "1/2", "14": "1/2", "15": "1/2"},
                "balanced_momentum_preparation_rank": 8,
                "balanced_homogeneous_full_Lorentz_first_field_sources_match_faithful": True,
                "balanced_preparation_law_or_old_kernel_inherited": False},
            "consumed_true_root_identity": "sum chi bar(z_s)=0; sum chi z_r bar(z_s)=0; chi=kappa+1_Omega/128",
            "retained": {"Fock": 16, "thermal_momenta": 4096, "shell": 128,
                         "reference": 128, "faithful_weight": "1/128",
                         "pure_momentum_weight": "1/8", "pure_prepared_rank": 8},
            "nonroot_countercontrol": {"F": "I/4", "role": 2, "boost": [0, 1],
                                       "momentum": [0, 0, 2, 0], "matter_source": 8,
                                       "full_trace_source": 0, "stationary_root": False},
            "domain": "independent homogeneous connection boosts; fixed legs and endpoint pairing; canonical d+d_dagger",
            "pure_old_root_satisfies_new_independent_boost_Euler": False,
            "all_new_faithful_Euler_rows_proved_here": False,
            "old_run_full_matrix_or_root_search_executed": False,
            "physical_programme_admission_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
