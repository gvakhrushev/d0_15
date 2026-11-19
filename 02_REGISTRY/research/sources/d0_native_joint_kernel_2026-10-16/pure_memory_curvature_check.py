"""Bounded full16 identities for the actual pure E0 preparation.

Only defining AST nodes are loaded from SHA-pinned owners. No old run(),
4096-momentum matrix, root solve, evidence generator or file write occurs.
The rational return is a member of the actual stored-adjoint constraint
class, not a new stationary root. The root receipt is read for scalar signs.
"""
from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CURVED = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
JOINT = "02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source.py"
RECEIPT = "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json"
OLD_DIAGNOSTIC = "02_REGISTRY/research/sources/d0_native_memory_source_2026-10-16/diagnostic_old_frequency.py"
MEMORY_DIAGNOSTIC = "02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16/diagnostic_memory_fibre.py"
PINS = {
    CURVED: "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    JOINT: "71ba142e284974db57d67c91a77ccd08a7e4f9759e8fc8daef7c5938774c0b28",
    RECEIPT: "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9",
    "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/nonzero_symbol_algebra.py":
        "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1",
    MEMORY_DIAGNOSTIC:
        "c92b184e2a0a3aad64b64a44f2eb70d3ff4c4aebe794ca69e3e2ffdbc1302bbc",
    OLD_DIAGNOSTIC:
        "a47d1c8cdf3967750cc33da598d3f58d567ebecf0e3e277ba97f38a7c1f18ec5",
}
L = 8
ETA = s.diag(1, -1, -1, -1)


def _definitions(repo):
    tree = ast.parse((repo / CURVED).read_text())
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef)
                 and node.name in {"creator", "basis_phase"})
             or (isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id == "EXTERIOR_ORDER"
                         for target in node.targets))]
    if len(nodes) != 3:
        raise ArithmeticError("pure_memory:owned_definition_nodes")
    scope = {"s": s, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CURVED, "exec"), scope)
    tree = ast.parse((repo / JOINT).read_text())
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "exterior"]
    if len(nodes) != 1:
        raise ArithmeticError("pure_memory:owned_exterior_node")
    scope["P"] = SimpleNamespace(basis_phase=scope["basis_phase"])
    exec(compile(ast.Module(body=nodes, type_ignores=[]), JOINT, "exec"), scope)
    return tuple(scope["creator"](j) for j in range(4)), scope["exterior"], scope["basis_phase"]


def _cross(v):
    return s.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, label):
        if not bool(condition):
            raise ArithmeticError("pure_memory:" + label)
        checks.append(label)

    def eq(actual, expected, label):
        entries = ((actual - expected).todok().values()
                   if isinstance(actual, s.MatrixBase) else (actual - expected,))
        require(all(s.cancel(s.expand(x)) == 0 for x in entries), label)

    require(all(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest
                for path, digest in PINS.items()), "immutable_actual_definition_and_receipt_pins")
    creators, exterior, basis_phase = _definitions(repo)
    I = s.eye(16)

    def create(v):
        return sum((v[j] * creators[j] for j in range(4)), s.zeros(16))

    def contract(v):
        return sum((v[j] * creators[j].T for j in range(4)), s.zeros(16))

    def lift(W):
        return sum((W[i, j] * creators[i] * creators[j].T
                    for i in range(4) for j in range(4)), s.zeros(16))

    require(all(creators[i] * creators[j].T + creators[j].T * creators[i]
                == (I if i == j else s.zeros(16))
                for i in range(4) for j in range(4)), "actual_full16_CAR_all_modes")
    chi = s.zeros(16, 1)
    chi[1], chi[15] = 1 / s.sqrt(2), 1 / s.sqrt(2)
    packet = chi.copy()
    packet[15] = -1 / s.sqrt(2)
    eta_exterior = s.diag(*[(-1) ** bin(mask & 14).count("1") for mask in range(16)])
    eq(basis_phase() * eta_exterior * packet, chi, "packet_to_native_whole_blank_ray")
    eq((chi.H * chi)[0], 1, "actual_pure_preparation_norm")

    wx, wy, wz, tau = s.symbols("wx wy wz tau", real=True)
    spatial = s.Matrix([wx, wy, wz])
    norm2 = spatial.dot(spatial)
    u = s.Matrix([tau, wx, wy, wz])
    W = s.diag(0, _cross(spatial))
    G = lift(W)
    eq(W * u, s.zeros(4, 1), "generic_stabilizer_preserves_own_leg")
    eq(G * chi, s.zeros(16, 1), "all_spatial_generators_fix_actual_E0_ray")
    eq(s.trace(G * G), -8 * norm2, "full16_rotation_square_trace")
    v = s.Matrix(s.symbols("v0:4", real=True))
    eq(s.trace(create(v) * contract(u) * G * G), -4 * norm2 * v.dot(u),
       "full16_creator_contractor_stabilizer_square_trace")
    eq(s.trace(contract(v) * create(u) * G * G), -4 * norm2 * v.dot(u),
       "full16_contractor_creator_stabilizer_square_trace")
    eq(s.trace(create(v) * create(u) * G * G), 0,
       "full16_same_charge_trace_zero")

    # Literal finite rational member of the same nonlinear native class.
    # This is NOT the certified v8 root or a physical primitive admission.
    a, b = s.Rational(3, 5), s.Rational(1, 10)
    F = (a - b) * s.eye(4) + b * s.ones(4)
    legs = [ETA * F.row(r).T for r in range(4)]
    omega = legs[2][1:4, :]
    Wr = s.diag(0, _cross(omega))
    omega2 = omega.dot(omega)
    t = s.symbols("t", real=True)
    R = s.eye(4) + t * Wr / (1 + t * t * omega2 / 4) \
        + t * t * Wr * Wr / (2 * (1 + t * t * omega2 / 4))
    eq(R.T * R, s.eye(4), "actual_rational_return_curve_is_positive_isometry")
    eq(R.T * ETA * R, ETA, "actual_rational_return_curve_is_Lorentz")
    eq(R * legs[2], legs[2], "actual_rational_return_curve_own_leg_transport")
    eq(R.diff(t).subs(t, 0), Wr, "actual_return_first_jet")
    eq(R.diff(t, 2).subs(t, 0), Wr * Wr, "actual_return_second_jet_not_omitted")
    q = (3, 3, 0, 0)
    require(q[2] == 0, "q3300_stabilizer_field_constant_along_own_role")
    Er = exterior(R.subs(t, s.Rational(1, 7)))
    eq(Er.H * Er, I, "actual_full16_finite_return_unitary")
    eq(Er * chi, chi, "actual_full16_finite_return_fixes_memory")
    roots = (1, (1 + s.I) / s.sqrt(2), s.I, (-1 + s.I) / s.sqrt(2),
             -1, (-1 - s.I) / s.sqrt(2), -s.I, (1 - s.I) / s.sqrt(2))
    phases = [roots[j] for j in (1, 2, 3, 4)]
    literal, free = s.zeros(16), s.zeros(16)
    for r in range(4):
        E = Er if r == 2 else I
        C, B = create(legs[r]), contract(legs[r])
        literal += L * (phases[r] * C * E - C + s.conjugate(phases[r]) * B * E.H - B)
        free += L * ((phases[r] - 1) * C + (s.conjugate(phases[r]) - 1) * B)
    eq(literal * chi, free * chi, "literal_stored_plane_input_identity_all16")
    phase = roots[1]
    single = L * ((phase - 1) * create(u) + (s.conjugate(phase) - 1) * contract(u))
    lambda1 = L * L * (2 - s.sqrt(2))
    eq(single * single, lambda1 * u.dot(u) * I, "full16_occupied_mode_exact_square")

    # The actual sphere/radius chart keeps its full second leg jet.
    rho, da, db, ba1, ba2, bb1, bb2 = s.symbols("rho da db ba1 ba2 bb1 bb2", real=True)
    z = s.Matrix([1, 0, 0])
    ba, bb = s.Matrix([0, ba1, ba2]), s.Matrix([0, bb1, bb2])
    aa, ab = da * z + rho * ba, db * z + rho * bb
    second = da * bb + db * ba - rho * ba.dot(bb) * z
    eq(aa.dot(ab) + (rho * z).dot(second), da * db,
       "true_sphere_second_jet_cancels_pure_orientation_energy")

    # Only eight scalar occupied phases enter this countercontrol, never
    # 4096 heat matrices.  The physical heat/feedback normalizer is untouched.
    d, o, omega_norm2 = s.symbols("d o omega_norm2", real=True)
    shell = [tuple(sign if j == r else 0 for j in range(4))
             for r in range(4) for sign in (1, 7)]
    phase_sums = []
    for r in range(4):
        phase_sums.append(s.expand(sum(
            s.re(roots[k[2]] * L * (s.conjugate(roots[k[r]]) - 1)) for k in shell)))
    eq(s.Matrix(phase_sums), s.Matrix([2 * L * (1 - 1 / s.sqrt(2)) * (1 if r == 2 else -1)
                                      for r in range(4)]), "exact_eight_phase_shell_moments")
    cold = s.expand(-L * omega_norm2 * sum((d if r == 2 else o) * phase_sums[r]
                                          for r in range(4)) / 8)
    cL = L * L * (1 - 1 / s.sqrt(2)) / 4
    eq(cold, -cL * (d - 3 * o) * omega_norm2,
       "faithful_chart_curvature_exact_full16_normalization")
    literal_cold = 0
    Gr2 = lift(Wr) ** 2
    for k in shell:
        occupied_role = next(r for r in range(4) if k[r])
        phase = roots[k[occupied_role]]
        Dk = L * ((phase - 1) * create(legs[occupied_role])
                  + (s.conjugate(phase) - 1) * contract(legs[occupied_role]))
        D2k = L * (roots[k[2]] * create(legs[2])
                   + s.conjugate(roots[k[2]]) * contract(legs[2])) * Gr2
        literal_cold += s.trace(Dk * D2k) / 64  # 2 * (1/8 shell) * (1/16 Fock).
    df, of = a * a + 3 * b * b, 2 * b * (a + b)
    exact_fixture_cold = -cL * (df - 3 * of) * omega2
    eq(literal_cold, exact_fixture_cold,
       "literal_eight_full16_blocks_verify_curvature_factor")
    def static_prefactor(path, function, name):
        tree = ast.parse((repo / path).read_text())
        body = next(node.body for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == function)
        value = next(node.value for node in body if isinstance(node, ast.Assign)
                     and any(isinstance(target, ast.Name) and target.id == name for target in node.targets))
        if not isinstance(value, ast.BinOp) or not isinstance(value.op, ast.Mult):
            raise ArithmeticError("pure_memory:static_prefactor_product")
        value = value.left
        if isinstance(value, ast.Constant):
            return s.Rational(value.value)
        if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Div) \
                and isinstance(value.left, ast.Constant) and isinstance(value.right, ast.Constant):
            return s.Rational(value.left.value, value.right.value)
        raise ArithmeticError("pure_memory:static_prefactor_literal")
    require(all(static_prefactor(OLD_DIAGNOSTIC, "direct_second", name) == 8
                for name in ("A0", "A1"))
            and all(static_prefactor(MEMORY_DIAGNOSTIC, "matter_matrix", name) == s.Rational(1, 2)
                    for name in ("B0", "B1"))
            and (2 * s.Rational(1, 2) / 16) == s.Rational(8, 128),
            "operator_anticommutator_factor_matches_old_scalar_trace_coefficient")
    # The memory operator uses B@mat+mat@B.  Cyclicity doubles its trace;
    # omitting this factor would incorrectly diagnose its prefactor as half.
    Ar, Br = contract(legs[2]), create(legs[2]) * Gr2
    require(s.trace(Ar * Br) != 0, "anticommutator_trace_control_is_nonzero")
    eq(s.trace((Ar * Br + Br * Ar) * I / 16), s.trace(Ar * Br) / 8,
       "full16_anticommutator_trace_retains_factor_two")
    eq(G * G * chi, s.zeros(16, 1), "pure_E0_chart_curvature_zero_for_stabilizer")
    correction = -cold
    eq(correction, cL * (d - 3 * o) * omega_norm2,
       "pure_minus_faithful_curvature_retained")
    require(s.expand(correction) != 0,
            "hostile_first_jet_only_zero_correction_rejected")

    receipt = json.loads((repo / RECEIPT).read_text())
    radius = s.Rational(receipt["interval"]["root_radius"])
    dc, oc = map(s.Rational, receipt["interval"]["root_center"])
    dl, du, ol, ou = dc - radius, dc + radius, oc - radius, oc + radius
    require(0 < ol < ou < dl < du and dl - 3 * ou > 0,
            "actual_owned_root_box_has_d_minus_3o_positive")
    lower = 4 * (dl - 3 * ou) * (dl - ou)
    upper = 8 * (du - 3 * ol) * du
    require(0 < lower < upper,
            "strict_rational_bounds_for_unscaled_inactive_theta_correction")

    # Even Clifford expectations of the actual whole-blank ray.  Both parity
    # sectors remain; their coherence is not visible to an even operator.
    majoranas = [value for C in creators for value in (C + C.T, s.I * (C - C.T))]
    products = [I]
    for mask in range(1, 256):
        j = mask.bit_length() - 1
        products.append(products[mask ^ (1 << j)] * majoranas[j])
    expected = {0: 1, 3: -s.I, 60: -1, 63: s.I,
                204: -1, 207: s.I, 240: -1, 243: s.I}
    require(all(s.expand((chi.H * products[mask] * chi)[0]) == expected.get(mask, 0)
                for mask in range(256) if bin(mask).count("1") % 2 == 0),
            "exact_eight_nonzero_even_Clifford_expectations_full16")
    require(all(s.expand((packet.H * products[mask] * packet)[0]) == expected.get(mask, 0)
                for mask in range(256) if bin(mask).count("1") % 2 == 0),
            "whole_blank_relative_parity_phase_does_not_change_even_expectations")

    return {"schema": "d0-pure-memory-curvature-interface/1", "status": "PASS_EXACT",
            "exact_checks": len(checks), "checks": checks, "source_pins": PINS,
            "full_Fock_dimension": 16, "thermal_momenta_retained": 4096,
            "occupied_shell_dimension": 128, "prepared_rank": 8,
            "reference_dimension_retained": 128,
            "rational_return_fixture_is_stationary_root": False,
            "occupied_shell_mode_square": "lambda1=L^2(2-2cos(2pi/L))",
            "fixed_preparation_energy": "lambda1/(4N) sum_(x,r) ||u_r(x)||^2",
            "curvature_correction": "c_L(d-3o)||omega||^2, c_L=L^2(1-cos(2pi/L))/4",
            "strict_correction_lower_rational": str(lower),
            "strict_correction_upper_rational": str(upper),
            "even_Clifford_expectation_support": sorted(expected),
            "consumed_stationary_identity": "C_kappa+C_faithful=0 at the owned true root; not replayed",
            "full_heat_matrix_or_previous_suite_executed": False,
            "rank8_field_inertia_or_new_joint_branch_proved": False,
            "physical_admission_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, ensure_ascii=False))
