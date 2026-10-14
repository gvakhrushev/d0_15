#!/usr/bin/env python3
"""Exact finite checks for the Q8/Role x Fibonacci-AF M2 kinematic seed.

This checks an algebraic construction and its stated scope only. It does not
admit a physical operation, infer a metric volume, or prove Einstein dynamics.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = "a4d_native_q8_af_spinor_seed"
PINNED = {
    "03_FORMALIZATION/D0/Representation/Omega8Q8TypedBridge.lean":
        "3bc91c3b1773ce092ebe9559d434cf4bdc92406d50fa376c11dc247608f87354",
    "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean":
        "6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7",
    "03_FORMALIZATION/D0/UnifiedFiniteCore/Q8Terminal.lean":
        "21d12f38c3f34e158bdae228b0fcc01edbafc6d616126c73df66fb144c703af6",
    "02_REGISTRY/research/certificates/a4d_native_q8_af_spinor_seed.lean":
        "d65b67e8b3f21c3db079b7e455d0ce5c1e6a737b49288953de95cd887e9ed67d",
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
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.lean":
        "7445b7c3827a372f4a90eaad5acfbd4523b7852e31778162fe17b155374cd30b",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_check.py":
        "a6d09cc3925b9a5acb415e1bac62a829bcef177f98fc2c0bd29a890cb6bafbf5",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py":
        "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
    "02_REGISTRY/research/A4D_NATIVE_Q8_AF_SPINOR_RECORD_SEED.md":
        "bca4dfa9dc26fb0599ce341f1f33ff003add4104c61848374f4a0eddd3707411",
}


def native_corner_m2_checks() -> dict:
    """Restrict the actual prepared Jones corner to the first M2 AF block."""
    rel = "02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py"
    spec = importlib.util.spec_from_file_location("q8_seed_native_jones_owner", ROOT / rel)
    if spec is None or spec.loader is None:
        raise RuntimeError("NATIVE_JONES_OWNER_IMPORT_FAILED")
    owner = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = owner
    spec.loader.exec_module(owner)
    E = owner.E
    p = E.p
    operations = owner.operators(0)

    def include_n(blocks, count):
        out = blocks
        for _ in range(count):
            out = owner.include(out)
        return out

    # The old A0 types are retained as orthogonal sectors in the full A7
    # carrier. The prepared corner e has exact weights p and p^2 on them.
    type0 = include_n([s.eye(1), s.zeros(1)], 7)
    type1 = include_n([s.zeros(1), s.eye(1)], 7)
    all_types = [s.eye(n) for n in E.counts(7)]
    cases = [
        ("all", all_types, 6, s.diag(p**2, p**2), p**3),
        ("type0", type0, 7, s.diag(p, 0), p**2),
        ("type1", type1, 8, s.diag(0, 1), s.S.Zero),
    ]

    def make_state(projection, rotate):
        prepared = [E.mat(d["e"] * x) for d, x in zip(operations, projection)]
        if rotate:
            return [E.mat(d["R"] * x * d["R"].T)
                    for d, x in zip(operations, prepared)]
        return prepared

    def expectation_matrix(state, normalization_power):
        values = s.zeros(2)
        for i in range(2):
            for j in range(2):
                matrix_unit = s.zeros(2)
                matrix_unit[i, j] = 1
                observable = include_n([matrix_unit, s.zeros(1)], 6)
                raw = owner.native_trace(
                    7, [E.mat(x * y) for x, y in zip(state, observable)])
                values[i, j] = E.red(s.expand(raw * (1 + p) ** normalization_power))
        return values

    def scalar_expectation(state, normalization_power):
        observable = include_n([s.zeros(2), s.eye(1)], 6)
        raw = owner.native_trace(
            7, [E.mat(x * y) for x, y in zip(state, observable)])
        return E.red(s.expand(raw * (1 + p) ** normalization_power))

    if E.red(p * (1 + p) - 1) != 0:
        raise AssertionError("Golden inverse identity for normalized corner failed")

    evaluated = {}
    for name, projection, power, expected_matrix, expected_scalar in cases:
        before = make_state(projection, rotate=False)
        after = make_state(projection, rotate=True)
        before_values = expectation_matrix(before, power)
        after_values = expectation_matrix(after, power)
        before_scalar = scalar_expectation(before, power)
        after_scalar = scalar_expectation(after, power)
        before_total = E.red(s.expand(
            owner.native_trace(7, before) * (1 + p) ** power))
        if before_total != 1:
            raise AssertionError(f"Native {name} corner state failed normalization")
        if E.zero(before_values - expected_matrix) is False:
            raise AssertionError(f"Native {name} M2 state disagrees with exact table")
        if E.zero(after_values - expected_matrix) is False:
            raise AssertionError(f"Jones transition changed native {name} M2 state")
        if E.zero(after_values - before_values) is False:
            raise AssertionError(f"Jones before/after M2 matrix units disagree: {name}")
        if E.red(before_scalar - expected_scalar) != 0:
            raise AssertionError(f"Native {name} scalar record weight mismatch")
        if E.red(after_scalar - expected_scalar) != 0:
            raise AssertionError(f"Jones transition changed native {name} scalar weight")
        evaluated[name] = {
            "expectation_matrix": before_values,
            "scalar_weight": before_scalar,
            "before_state": before,
            "after_state": after,
            "normalization_power": power,
        }

    all_values = evaluated["all"]["expectation_matrix"]
    type0_values = evaluated["type0"]["expectation_matrix"]
    type1_values = evaluated["type1"]["expectation_matrix"]
    if E.zero(all_values - p * type0_values - p**2 * type1_values) is False:
        raise AssertionError("Full M2 restriction failed to decompose over both old types")
    if E.red(evaluated["all"]["scalar_weight"]
             - p * evaluated["type0"]["scalar_weight"]
             - p**2 * evaluated["type1"]["scalar_weight"]) != 0:
        raise AssertionError("Full scalar restriction failed to retain both old types")

    full_m2_mass = E.red(s.trace(all_values))
    full_m2_density = E.mat(all_values.T * (1 + p) ** 2 / 2)
    type0_m2_mass = E.red(s.trace(type0_values))
    type0_m2_density = E.mat(type0_values.T * (1 + p))
    type1_m2_density = E.mat(type1_values.T)
    if full_m2_mass != E.red(2 * p**2):
        raise AssertionError("Full native corner has wrong M2-block mass")
    if type0_m2_mass != E.red(p):
        raise AssertionError("Type-zero corner has wrong M2-block mass")
    if E.zero(full_m2_density - s.eye(2) / 2) is False:
        raise AssertionError("Full native corner M2 density is not maximally mixed")
    if E.zero(type0_m2_density - s.diag(1, 0)) is False:
        raise AssertionError("Type-zero corner does not restrict to the first pure M2 state")
    if E.zero(type1_m2_density - s.diag(0, 1)) is False:
        raise AssertionError("Type-one corner does not restrict to the second pure M2 state")
    if E.zero(full_m2_density - s.diag(p, p**2)) is not False:
        raise AssertionError("M2 tracial state was unexpectedly identified with rho_phi")

    return {
        "level_map": "A1_to_A7_by_six_owned_AF_inclusions",
        "full_corner_m2_unnormalized_density": "p^2*I2",
        "full_corner_m2_block_mass": "2*p^2",
        "full_corner_m2_conditional_density_before_and_after_jones": "I2/2",
        "type0_sector_m2_unnormalized_density": "diag(p,0)",
        "type0_sector_scalar_weight": "p^2",
        "type0_record_distribution": ["p", "p^2"],
        "type1_sector_m2_density": "diag(0,1)",
        "m2_density_equals_rho_phi": False,
        "jones_preserves_all_four_m2_matrix_unit_expectations": True,
        "both_old_type_sectors_retained": True,
    }


def native_activation_spinor_checks() -> dict:
    """Run the owned blank-record gate inside its actual three-bond AF frame."""
    rel = "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py"
    spec = importlib.util.spec_from_file_location("q8_seed_native_af_activation", ROOT / rel)
    if spec is None or spec.loader is None:
        raise RuntimeError("NATIVE_AF_ACTIVATION_OWNER_IMPORT_FAILED")
    owner = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = owner
    spec.loader.exec_module(owner)

    n = 0
    data = owner.frame(n)
    V = data["V"]
    d = data["old_dimension"]
    a, p = owner.a, owner.p

    # The canonical level-zero AF cyclic vector has the forced trace weights
    # p and p^2, represented by their owned positive square-root amplitudes.
    spectator = s.zeros(d, 1)
    for index, (old_type, row, col) in enumerate(data["old_coordinates"]):
        if row == col:
            spectator[index] = owner.root_weight(n + 1 + old_type)
    if owner.red(s.expand((spectator.T * spectator)[0] - 1)) != 0:
        raise AssertionError("Canonical AF spectator vector is not normalized")

    blank = s.Matrix.vstack(spectator, s.zeros(3 * d, 1))
    apparatus_gate = s.kronecker_product(owner.record(), s.eye(d))
    expected_coordinates = owner.mat(apparatus_gate * blank)
    expected = s.Matrix.vstack(a * spectator, s.zeros(d, 1),
                               s.zeros(d, 1), p * spectator)
    if owner.zero(expected_coordinates - expected) is False:
        raise AssertionError("Owned fullStep did not preserve its exact blank output")

    native_gate, _, _, _ = owner.full_operators(V, d)
    complement = owner.mat(s.eye(V.rows) - V * V.T)
    if owner.zero(native_gate.T * native_gate - s.eye(V.rows)) is False:
        raise AssertionError("AF-embedded gate is not unitary on the whole carrier")
    if owner.zero(native_gate * complement - complement) is False:
        raise AssertionError("AF-embedded gate changed its orthogonal complement")
    native_input = owner.mat(V * blank)
    native_output = owner.mat(native_gate * native_input)
    decoded_output = owner.mat(V.T * native_output)
    if owner.zero(native_output - V * expected) is False:
        raise AssertionError("AF-embedded fullStep differs from the owned apparatus gate")
    if owner.zero(decoded_output - expected) is False:
        raise AssertionError("AF frame failed to decode the retained full output")
    if owner.red(s.expand((decoded_output.T * decoded_output)[0] - 1)) != 0:
        raise AssertionError("AF-embedded full output lost norm")

    amplitudes = s.Matrix(4, d, lambda i, j: decoded_output[i * d + j])
    apparatus_density = owner.mat(amplitudes * amplitudes.T)
    system_density = s.zeros(2)
    record_density = s.zeros(2)
    for i in range(2):
        for j in range(2):
            system_density[i, j] = owner.red(sum(
                apparatus_density[2 * i + bit, 2 * j + bit]
                for bit in range(2)))
            record_density[i, j] = owner.red(sum(
                apparatus_density[2 * bit + i, 2 * bit + j]
                for bit in range(2)))
    golden_density = s.diag(p, p**2)
    if owner.zero(system_density - golden_density) is False:
        raise AssertionError("AF-native system partial trace is not diag(p,p^2)")
    if owner.zero(record_density - golden_density) is False:
        raise AssertionError("AF-native record partial trace is not diag(p,p^2)")
    expected_apparatus_density = s.Matrix([
        [p, 0, 0, a * p],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [a * p, 0, 0, p**2],
    ])
    if owner.zero(apparatus_density - expected_apparatus_density) is False:
        raise AssertionError("Full apparatus coherence or retained record was lost")

    pauli_x = s.Matrix([[0, 1], [1, 0]])
    pauli_y = s.Matrix([[0, -s.I], [s.I, 0]])
    pauli_z = s.diag(1, -1)
    spinor_readout = [
        owner.red(s.trace(system_density)),
        owner.red(s.trace(system_density * pauli_x)),
        owner.red(s.trace(system_density * pauli_y)),
        owner.red(s.trace(system_density * pauli_z)),
    ]
    if any(owner.red(value - target) != 0
           for value, target in zip(spinor_readout, [1, 0, 0, p**3])):
        raise AssertionError("AF-native Q8/Pauli spinor readout mismatch")

    return {
        "input": "canonical_A0_cyclic_vector_in_blank_V0_frame",
        "native_embedding": "A0_to_A3_three_inclusions; operator_in_A6_right_module_corner",
        "decoded_full_output": "a*|00>*Omega0 + p*|11>*Omega0",
        "full_apparatus_density_00_11_block": [["p", "a*p"], ["a*p", "p^2"]],
        "system_marginal": "diag(p,p^2)",
        "record_marginal": "diag(p,p^2)",
        "q8_system_expectations_I_X_Y_Z": ["1", "0", "0", "p^3"],
        "norm_and_complement_retained": True,
        "same_as_first_AF_M2_Jones_corner": False,
        "physical_preparation_and_metric_binding_derived": False,
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

    native_corner = native_corner_m2_checks()
    activation_spinor = native_activation_spinor_checks()

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
        "scope": "EXACT_Q8_ROLE_AF_ACTIVATION_SPINOR_SEED_PHYSICAL_ADMISSION_OPEN",
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
        "native_prepared_corner_on_m2": native_corner,
        "native_four_level_activation_spinor": activation_spinor,
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
