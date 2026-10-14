#!/usr/bin/env python3
"""Exact finite checks for the Q8/Role x Fibonacci-AF M2 kinematic seed.

This checks an algebraic construction and its stated scope only. It does not
admit a physical operation, infer a metric volume, or prove Einstein dynamics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = "a4d_native_q8_af_spinor_seed"
PINNED = {
    "03_FORMALIZATION/D0/Representation/Omega8Q8TypedBridge.lean":
        "3bc91c3b1773ce092ebe9559d434cf4bdc92406d50fa376c11dc247608f87354",
    "03_FORMALIZATION/D0/UnifiedFiniteCore/Q8Terminal.lean":
        "21d12f38c3f34e158bdae228b0fcc01edbafc6d616126c73df66fb144c703af6",
    "03_FORMALIZATION/D0/Research/Q8AFSpinorSeed.lean":
        "569b0cb724f7dee7e143d062b7882cc642013d45a17b698cb968093e32796abf",
    "03_FORMALIZATION/D0/Core/RoleAlternatingPairing.lean":
        "2f5cccba34e02b0173ca30c9d59b83dca55e2116d2456098f35deafcc77e117f",
    "03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean":
        "b923882386bc66998f4f3cf2ba7d73b0acf30938859d26680458420bafbd1db7",
    "03_FORMALIZATION/D0/Algebra/RoleSignature.lean":
        "5dfb03dc839b4c81d199ff053e57d4b9d54cd61812577078e6302bc710c4ffcf",
    "03_FORMALIZATION/D0/Geometry/ArchiveRoleEquivalence.lean":
        "215d9081e23e1e84c51a7b36f252c1540302317db0945d75431cc4f97e1c7920",
    "02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md":
        "012455bdd3845e1d95f5270bbdcf105c753013d6e0b2339e2c001332e1fe4ee6",
    "02_REGISTRY/research/A4D_NATIVE_FOUR_LEVEL_SELF_SIMILAR_TAIL.md":
        "927e6735edc5fb2cdaa5fea8d43b29fd507e91c2f9636189ca6330edb40b2ef0",
    "02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md":
        "d51e9af89b1505cdb3696dc544568ca5ec7f4da1cea1e313ff93d553195740cb",
    "02_REGISTRY/research/A4D_NATIVE_RECORDED_OBSERVER_PREPARATION.md":
        "d045c5980c99539e647eff71ff792fe20ae2c98931fb6f012de998a3c538ca12",
    "02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md":
        "5f121dc43aa9ea701fe055f72070f95339f607f267d411b1b9ae5e93c1c20ffc",
    "02_REGISTRY/research/A4D_NATIVE_FULL_PREPARATION_FIBER.md":
        "cf363734f8433d3a3315a0487ddb311a68c852d906e2f19915b2ffb3d9ee16e5",
    "02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md":
        "9c7e4d582d5627bf5b926a6f8ad15743ff473e9bcc22e741c42309dabb854299",
    "02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md":
        "9971253d0ba13b9b66ff28a6bedf166b9de265821a9380b969ba6e23ec9ee0f3",
    "02_REGISTRY/research/A4D_NATIVE_Q8_AF_SPINOR_RECORD_SEED.md":
        "3dd223dc09775ac02b29c3dee850522d6a12072b6a29e936ba9a0dfb638f2f26",
}


def exact_checks() -> dict:
    actual = {}
    for rel, expected in PINNED.items():
        digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if digest != expected:
            raise RuntimeError(f"SOURCE_HASH_MISMATCH {rel}: {digest} != {expected}")
        actual[rel] = digest

    I = s.I
    identity = s.eye(2)
    pauli_x = s.Matrix([[0, 1], [1, 0]])
    pauli_y = s.Matrix([[0, -I], [I, 0]])
    pauli_z = s.Matrix([[1, 0], [0, -1]])
    # The cocycle basis: role bit 1 -> i sigma_z, bit 2 -> i sigma_y.
    gen_1, gen_2 = I * pauli_z, I * pauli_y

    def role_matrix(u: tuple[int, int]) -> s.Matrix:
        return gen_1**u[0] * gen_2**u[1]

    def role_add(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
        return ((u[0] + v[0]) % 2, (u[1] + v[1]) % 2)

    def cocycle(u: tuple[int, int], v: tuple[int, int]) -> int:
        return (u[0] * v[0] + u[1] * v[1] + u[1] * v[0]) % 2

    def omega(u: tuple[int, int], v: tuple[int, int]) -> int:
        return (u[0] * v[1] + u[1] * v[0]) % 2

    roles = [(0, 0), (1, 1), (0, 1), (1, 0)]  # A, B, C, D
    product_count = 0
    for u in roles:
        U = role_matrix(u)
        if s.simplify(U.conjugate().T * U - identity) != s.zeros(2):
            raise AssertionError(f"Q8 generator is not unitary: {u}")
        for v in roles:
            V = role_matrix(v)
            if s.simplify(U * V - (-1) ** cocycle(u, v) * role_matrix(role_add(u, v))) != s.zeros(2):
                raise AssertionError(f"Q8 cocycle product mismatch: {u}, {v}")
            if s.simplify(U * V - (-1) ** omega(u, v) * V * U) != s.zeros(2):
                raise AssertionError(f"Role alternating commutator mismatch: {u}, {v}")
            product_count += 1

    role_paulis = {
        (1, 1): -I * role_matrix((1, 1)),  # B -> sigma_x
        (0, 1): -I * role_matrix((0, 1)),  # C -> sigma_y
        (1, 0): -I * role_matrix((1, 0)),  # D -> sigma_z
    }
    expected_paulis = {
        (1, 1): pauli_x,
        (0, 1): pauli_y,
        (1, 0): pauli_z,
    }
    for role, matrix in role_paulis.items():
        if s.simplify(matrix - expected_paulis[role]) != s.zeros(2):
            raise AssertionError(f"Role/Pauli axis mismatch: {role}")
        if s.simplify(matrix.conjugate().T - matrix) != s.zeros(2):
            raise AssertionError(f"Hermitian Pauli axis failure: {role}")
        if s.simplify(matrix * matrix - identity) != s.zeros(2):
            raise AssertionError(f"Pauli square failure: {role}")

    t, x, y, z = s.symbols("t x y z", real=True)
    H = t * identity + x * pauli_x + y * pauli_y + z * pauli_z
    determinant = s.factor(H.det())
    if determinant != t**2 - x**2 - y**2 - z**2:
        raise AssertionError(f"Wrong Hermitian M2 determinant: {determinant}")
    characteristic = s.factor(H.charpoly(s.Symbol("lambda")).as_expr())
    lam = s.Symbol("lambda")
    if s.simplify(characteristic - ((lam - t) ** 2 - (x**2 + y**2 + z**2))) != 0:
        raise AssertionError(f"Wrong Hermitian M2 characteristic polynomial: {characteristic}")

    # AF path count A_0=C (+) C; A_1=M_2(C) (+) C; d_n=dim_C A_n.
    sizes = [(1, 1)]
    for _ in range(5):
        a, b = sizes[-1]
        sizes.append((a + b, a))
    dimensions = [a * a + b * b for a, b in sizes]
    if sizes[:5] != [(1, 1), (2, 1), (3, 2), (5, 3), (8, 5)]:
        raise AssertionError(f"AF path count mismatch: {sizes[:5]}")
    if dimensions[:5] != [2, 5, 13, 34, 89]:
        raise AssertionError(f"AF algebra dimensions mismatch: {dimensions[:5]}")
    if any(dimensions[n + 2] != 3 * dimensions[n + 1] - dimensions[n] for n in range(4)):
        raise AssertionError("AF algebra dimension recurrence mismatch")

    p = (s.sqrt(5) - 1) / 2
    if s.simplify(p + p**2 - 1) != 0:
        raise AssertionError("Golden trace weights fail normalization")
    phi = 1 / p
    rho = s.diag(p, p**2)
    delta = (p - p**2) / 2
    split_a, split_b = phi - 1, 2 - phi
    if s.simplify(split_a - p) != 0 or s.simplify(split_b - p**2) != 0:
        raise AssertionError("Golden scalar split mismatch")
    if s.simplify(split_a + split_b - 1) != 0:
        raise AssertionError("Golden scalar split is not normalized")
    if s.simplify(s.trace(rho) - 1) != 0:
        raise AssertionError("Ancestor diagonal state is not normalized")
    if s.simplify(rho.det() - p**3) != 0:
        raise AssertionError("Golden qubit determinant mismatch")
    if s.simplify(delta - p**3 / 2) != 0:
        raise AssertionError("Golden half-difference mismatch")
    scalar_q_values = []
    for dimension in range(1, 6):
        q_value = s.simplify(2 * delta * phi ** (dimension - 1))
        if s.simplify(q_value - phi ** (dimension - 4)) != 0:
            raise AssertionError(f"Scalar Q(D) identity failed at D={dimension}")
        scalar_q_values.append(s.sstr(q_value))
    scalar_next_delta = delta * (split_a - split_b) / 2
    if s.simplify(scalar_next_delta - delta**2) != 0:
        raise AssertionError("Repeated scalar half-difference recursion mismatch")
    if s.simplify(delta * delta - p**6 / 4) != 0:
        raise AssertionError("Repeated scalar half-difference mismatch")
    if s.simplify(4 * rho.det() - 8 * delta) != 0:
        raise AssertionError("Lorentz norm / AF feedback scalar mismatch")
    if s.simplify(p**6 - 4 * delta**2) != 0:
        raise AssertionError("Prepared corner / delta-square mismatch")
    if s.simplify(8 * delta + p**6 - 1) != 0:
        raise AssertionError("Feedback / corner complementary weights mismatch")

    initial_table = s.Matrix([[p**2, p**3], [p**3, p**4]])
    recorded_table = s.Matrix([[p, 0], [0, p**2]])
    initial_marginals = [s.simplify(sum(initial_table[i, j] for j in range(2))) for i in range(2)]
    recorded_marginals = [s.simplify(sum(recorded_table[i, j] for j in range(2))) for i in range(2)]
    initial_columns = [s.simplify(sum(initial_table[i, j] for i in range(2))) for j in range(2)]
    recorded_columns = [s.simplify(sum(recorded_table[i, j] for i in range(2))) for j in range(2)]
    if any(s.simplify(v - w) != 0 for v, w in zip(initial_marginals, recorded_marginals)):
        raise AssertionError("Jones record changed a row marginal")
    if any(s.simplify(v - w) != 0 for v, w in zip(initial_columns, recorded_columns)):
        raise AssertionError("Jones record changed a column marginal")
    if s.simplify(sum(initial_table) - 1) != 0 or s.simplify(sum(recorded_table) - 1) != 0:
        raise AssertionError("Jones record table is not normalized")
    if s.simplify(initial_table.det()) != 0 or s.simplify(recorded_table.det() - p**3) != 0:
        raise AssertionError("Jones record correlation control failed")

    # Hostile control: the full AF tracial state restricted conditionally to M2
    # has density I/2, not rho. Ancestor-diagonal rho is a separate preparation.
    af_conditional_density = identity / 2
    if s.simplify(af_conditional_density - rho) == s.zeros(2):
        raise AssertionError("Conditional AF trace was conflated with ancestor density")
    c_re, c_im = s.symbols("c_re c_im", real=True)
    rho_extension = s.Matrix([[p, c_re + I * c_im], [c_re - I * c_im, p**2]])
    if s.simplify(rho_extension.det() - (p**3 - c_re**2 - c_im**2)) != 0:
        raise AssertionError("Off-diagonal state-extension control failed")
    coherent_state = rho_extension.subs({c_re: p**3 / 2, c_im: 0})
    if not s.simplify(coherent_state.det()).is_positive:
        raise AssertionError("Nonzero coherent extension failed positivity")
    if any(s.simplify(coherent_state[i, i] - rho[i, i]) != 0 for i in range(2)):
        raise AssertionError("Coherent extension changed the fixed diagonal data")
    if s.simplify(s.trace(coherent_state * pauli_x) - s.trace(rho * pauli_x) - p**3) != 0:
        raise AssertionError("Fixed diagonal did not leave a distinct Pauli-X readout")

    # Hostile control: every SU(2) adjoint fixes I and preserves the Pauli inner
    # product; a determinant-one spin boost is not such a conjugation.
    ua, ub, uc, ud = s.symbols("u_a u_b u_c u_d", real=True)
    norm2 = ua**2 + ub**2 + uc**2 + ud**2
    unitary = s.Matrix([[ua + I * ub, uc + I * ud],
                        [-uc + I * ud, ua - I * ub]])
    if s.simplify(unitary * unitary.conjugate().T - norm2 * identity) != s.zeros(2):
        raise AssertionError("Generic SU(2) parameterization failed")
    adjoint_paulis = [unitary * sigma * unitary.conjugate().T
                      for sigma in (pauli_x, pauli_y, pauli_z)]
    for i, left in enumerate(adjoint_paulis):
        for j, right in enumerate(adjoint_paulis):
            target = 2 * norm2**2 if i == j else 0
            if s.simplify(s.trace(left * right) - target) != 0:
                raise AssertionError("SU(2) Pauli action failed to preserve Euclidean form")
    q = s.symbols("q", positive=True)
    boost = s.diag(q, 1 / q)
    boost_identity = s.simplify(boost * identity * boost.conjugate().T)
    if boost.det() != 1 or boost_identity == identity:
        raise AssertionError("Noncompact boost control failed")
    if s.simplify(unitary * identity * unitary.conjugate().T - norm2 * identity) != s.zeros(2):
        raise AssertionError("SU(2) identity-fixing control failed")

    return {
        "scope": "EXACT_Q8_ROLE_AF_M2_KINEMATIC_SEED_PHYSICAL_ADMISSION_OPEN",
        "status": "PASS",
        "source_sha256": actual,
        "q8_role_products_and_commutators": product_count,
        "hermitian_m2_determinant": "t^2-x^2-y^2-z^2",
        "hermitian_m2_cone_signature": [1, 3],
        "af_path_counts": [list(v) for v in sizes[:5]],
        "af_algebra_dimensions": dimensions[:5],
        "golden_state": "rho=diag(p,p^2); det(rho)=p^3; tr(rho)=1",
        "old_scalar_split": {
            "a0": "phi-1=p",
            "b0": "2-phi=p^2",
            "Q_D_for_D_1_to_5": scalar_q_values,
            "Q_4": "1",
            "next_scalar_half_difference": "delta0^2",
            "physical_dimension_inference": "NOT_ESTABLISHED",
        },
        "feedback_corner_identity": "4 det(rho)=8 delta0; p^6=4 delta0^2; 8 delta0+p^6=1",
        "jones_record_tables": {
            "initial": [["p^2", "p^3"], ["p^3", "p^4"]],
            "after": [["p", "0"], ["0", "p^2"]],
            "both_marginals_preserved": True,
            "correlation_changes": True,
        },
        "hostile_controls": {
            "full_af_trace_is_not_ancestor_density": True,
            "fixed_diagonal_does_not_fix_nondiagonal_observables": True,
            "generic_su2_action_fixes_identity_and_preserves_pauli_form": True,
            "noncompact_boost_is_not_fixed_block_unitary_conjugation": True,
        },
        "physical_operation_source_metric_volume_and_gr": "OPEN",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the pinned JSON result")
    args = parser.parse_args()
    result = exact_checks()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (Path(__file__).with_name(BASE + "_results.json")).write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
