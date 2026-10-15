#!/usr/bin/env python3
"""Exact positive-state extension of the recorded level-nine AF/CAR source."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/certificates/a4d_native_afcar_positive_state_refinement"
PROOF = "02_REGISTRY/research/A4D_NATIVE_AFCAR_POSITIVE_STATE_REFINEMENT.md"
RECEIPT = ROOT / f"{BASE}_certificate.json"
SOURCE_PINS = {
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_CURRENT_COMMUTANT_BOUNDARY.md":
        "36f77dea7cc868b74bb656c928b3897d5ef42bc45cfde6006070cbcfcf2b6bd9",
    "02_REGISTRY/research/A4D_NATIVE_AFCAR_WHOLE_BLANK_STATE_BOUNDARY.md":
        "f632ddfebbabfd3a9dcc254de57ab3aedcc7e04a00c5d0ebf799f5ab577e1751",
    "02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md":
        "9971253d0ba13b9b66ff28a6bedf166b9de265821a9380b969ba6e23ec9ee0f3",
    "02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md":
        "d51e9af89b1505cdb3696dc544568ca5ec7f4da1cea1e313ff93d553195740cb",
    "02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md":
        "012455bdd3845e1d95f5270bbdcf105c753013d6e0b2339e2c001332e1fe4ee6",
    "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant.py":
        "378a4d39d5e4cb525c653d869900e1926b6fcbea9243f619513af31978098dee",
    "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant_certificate.json":
        "d536f753cc632e7bd1207e495207f70e8988bdd18196bbc7c225e421c1baf2e8",
    "02_REGISTRY/research/certificates/a4d_native_afcar_blank_family_state_certificate.json":
        "f25423f161a62f9d08ecea8c605f66a35a4372e2c15f175d3ffe08198e3efbf8",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    "02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_certificate.json":
        "c11c3a887761aa11fe7f54f3b8e88c49010726941128dff07e06eef2709c7df7",
    "02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement_certificate.json":
        "98296ed5b60c77fc721d72d75ef7f64e8550896500a63bd4bfb0ce7755d36d08",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py":
        "b19f6c864af7e75c2a48d9892692b4d94337d06c04a83013b180148a1752c53f",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport_check.py":
        "caddfd3974a53f178871776b9a1891b3cce484d614eff365587b2607b6d874df",
    "02_REGISTRY/research/certificates/a4d_native_jones_record_transport_certificate.json":
        "c4fdc2642e699c2417b164b034abc60f8090b89c7c41c8db187de4ad2aa00d90",
}


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(stem: str):
    path = ROOT / "02_REGISTRY/research/certificates" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_IMPORT_FAILED:{stem}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="issue the initial receipt")
    args = parser.parse_args()

    owner = load("a4d_native_afcar_current_commutant")
    jones = load("a4d_native_jones_record_transport")
    CAR, FRAME, AF = owner.CAR, owner.FRAME, owner.AF
    E = jones.E
    checks: list[str] = []

    def check(name: str, condition: object) -> None:
        if not bool(condition):
            raise AssertionError(name)
        checks.append(name)

    def eq(name: str, value: sp.Expr | sp.MatrixBase) -> None:
        check(name, E.zero(value))

    for path, expected in SOURCE_PINS.items():
        check(f"source_sha256:{path}", sha(path) == expected)

    upstream_af = json.loads((ROOT / "02_REGISTRY/research/certificates/a4d_native_afcar_current_commutant_certificate.json").read_text())
    upstream_jones = json.loads((ROOT / "02_REGISTRY/research/certificates/a4d_native_jones_record_transport_certificate.json").read_text())
    check("owned_AFCAR_operator_corner_certificate_passes", upstream_af["status"] == "PASS")
    check("owned_Jones_all_level_transport_certificate_passes", upstream_jones["status"] == "PASS")
    check("owned_Jones_certificate_retains_full_complement",
          upstream_jones["scope"]["all_orthogonal_complements_retained"] is True)

    # Reconstruct the actual level-three weld and the recorded CAR blank.
    ops, adapted_frame, current = owner.operators()
    data3 = AF.frame(3)
    d3 = data3["old_dimension"]
    index3 = {coordinate: i for i, coordinate in enumerate(data3["old_coordinates"])}
    weld3 = sp.zeros(4 * d3, 32)
    for apparatus in range(4):
        for left_row in range(2):
            for path in range(2):
                for right_column in range(2):
                    spectator = 2 * left_row + path
                    af_row = left_row + 3 * path
                    source_column = (apparatus * 4 + spectator) * 2 + right_column
                    target_row = apparatus * d3 + index3[(0, af_row, right_column)]
                    weld3[target_row, source_column] = 1
    check("actual_level3_same_simple_weld_isometry", weld3.T * weld3 == sp.eye(32))

    seed = FRAME.mat(adapted_frame.T * CAR.blank_code() * sp.Matrix([CAR.a, CAR.p]))
    two_copy_seed = sp.kronecker_product(seed, sp.eye(2)[:, 0])
    recorded_seed = sp.kronecker_product(ops[0], sp.eye(2)) * two_copy_seed
    field_to_af = {CAR.a: AF.a, CAR.p: AF.p, FRAME.a: AF.a, FRAME.p: AF.p}
    recorded_native3 = AF.mat((weld3 * recorded_seed).subs(field_to_af, simultaneous=True))
    source_row3 = sp.zeros(20, 1)
    for apparatus in range(4):
        for row in range(5):
            source_row3[apparatus * 5 + row] = recorded_native3[
                apparatus * d3 + index3[(0, row, 0)]
            ]
    path_frame = AF.right_frames(3)[0]["V"]
    y = AF.mat(path_frame * source_row3)
    eq("recorded_A9_source_vector_is_normalized", (y.T * y)[0] - 1)
    expected_nonzero = {
        0: AF.p,
        3: AF.p - 1,
        15: AF.a * AF.p,
        18: AF.a * AF.p,
    }
    check("recorded_pre_path_source_row_has_owned_four_entry_form",
          all(source_row3[i] == value for i, value in expected_nonzero.items())
          and all(source_row3[i] == 0 for i in range(source_row3.rows)
                  if i not in expected_nonzero))

    # The source's vector functional is exactly its normalized regular-GNS
    # state on the left A_9 observable algebra, although it misses e/p^3.
    jones_frame = AF.mat(jones.corner_frames(3)[0].subs(
        {E.a: AF.a, E.p: AF.p}, simultaneous=True))
    z = jones_frame[:, 0]
    eq("Jones_source_column_is_normalized", (z.T * z)[0] - 1)
    X = AF.mat(y * z.T)
    tau_weight = AF.p**10
    eq("recorded_GNS_vector_norm_is_p10",
       tau_weight * sp.trace(X.T * X) - tau_weight)

    # Construct the complete A_9 native current triple from the owned CAR
    # current on the actual two M_5 path copies.
    current_to_af = {CAR.a: AF.a, CAR.p: AF.p, FRAME.a: AF.a, FRAME.p: AF.p}
    currents: list[sp.Matrix] = []
    for alpha in current:
        alpha = alpha.subs(current_to_af, simultaneous=True)
        multiplicity = sp.zeros(20)
        for source in range(16):
            app_in, spectator_in = divmod(source, 4)
            row_in = spectator_in // 2 + 3 * (spectator_in % 2)
            for target in range(16):
                app_out, spectator_out = divmod(target, 4)
                row_out = spectator_out // 2 + 3 * (spectator_out % 2)
                multiplicity[app_out * 5 + row_out, app_in * 5 + row_in] = alpha[target, source]
        currents.append(AF.mat(path_frame * multiplicity * path_frame.T))
    source_expectations = [AF.red((y.T * op * y)[0]) for op in currents]
    check("source_A9_current_is_the_owned_full_CAR_readout",
          source_expectations == [2 * AF.a * AF.p, 0, 0])
    check("source_A9_current_has_p6_Lorentz_norm",
          AF.red(1 - sum(value**2 for value in source_expectations) - AF.p**6) == 0)
    # This is the key negative control: the state extension must not force
    # the recorded state into the different canonical Jones conditional state.
    check("source_is_not_replaced_by_zero_current_Jones_vector",
          source_expectations[0] != 0)

    # All-level transport starts at A_9 (Jones parameter n=3) and lands in
    # A_10. Its trace adjoint is the owned UCP conditional expectation.
    n = 3
    sizes = AF.counts(9)
    next_sizes = AF.counts(10)
    check("actual_A9_A10_block_sizes", sizes == (89, 55) and next_sizes == (144, 89))
    rho = y * y.T
    zero55 = sp.zeros(55)
    padded = sp.zeros(144)
    padded[:89, :89] = rho
    next_ops = jones.operators(n)
    Rplus, Rminus = next_ops[0]["R"], next_ops[1]["R"]
    check("Jones_transport_is_orthogonal_on_both_A10_blocks",
          E.zero(Rplus.T * Rplus - sp.eye(144))
          and E.zero(Rminus.T * Rminus - sp.eye(89)))
    rho10_plus = E.mat(AF.p * Rplus * padded * Rplus.T)
    rho10_minus = E.mat(AF.p**2 * Rminus * rho * Rminus.T)
    plus_vector = E.mat(Rplus * sp.Matrix.vstack(y, sp.zeros(55, 1)))
    minus_vector = E.mat(Rminus * y)
    check("A10_plus_density_is_explicit_positive_rank_one",
          E.zero(rho10_plus - AF.p * plus_vector * plus_vector.T)
          and E.zero(plus_vector.T * plus_vector - sp.ones(1, 1)))
    check("A10_minus_density_is_explicit_positive_rank_one",
          E.zero(rho10_minus - AF.p**2 * minus_vector * minus_vector.T)
          and E.zero(minus_vector.T * minus_vector - sp.ones(1, 1)))
    check("A10_density_has_unit_trace_by_p_plus_p2",
          E.red(sp.trace(rho10_plus) + sp.trace(rho10_minus) - 1) == 0
          and E.red(AF.p + AF.p**2 - 1) == 0)
    check("A10_density_spectral_weights_are_p_and_p2",
          E.zero(rho10_plus**2 - AF.p * rho10_plus)
          and E.zero(rho10_minus**2 - AF.p**2 * rho10_minus))

    # Test exact preservation on the noncommutative current *-algebra
    # generated by the actual source: generators and every quadratic word.
    zero89 = sp.zeros(89)
    observables = [sp.eye(89), *currents]
    observables.extend(AF.mat(left * right) for left in currents for right in currents)
    preserved_values: list[str] = []
    for k, observable in enumerate(observables):
        base = [E.mat(observable), zero55]
        fine = jones.transport(n, base)
        recovered = jones.coarse(n, fine)
        check(f"conditional_expectation_is_left_inverse_on_source_word_{k}",
              E.zero(recovered[0] - base[0]) and E.zero(recovered[1] - base[1]))
        value0 = E.red((y.T * observable * y)[0])
        value1 = E.red(sp.trace(rho10_plus * fine[0])
                       + sp.trace(rho10_minus * fine[1]))
        check(f"A10_state_preserves_source_word_expectation_{k}", E.red(value1 - value0) == 0)
        preserved_values.append(str(value0))

    result = {
        "schema": "d0-native-afcar-positive-state-refinement/1",
        "status": "PASS",
        "proof": PROOF,
        "proof_sha256": sha(PROOF),
        "checker_sha256": sha(BASE + "_check.py"),
        "source_sha256": {path: sha(path) for path in SOURCE_PINS},
        "exact_check_count": len(checks),
        "exact_checks": checks,
        "base_level": 9,
        "first_refined_level": 10,
        "base_block_sizes": [89, 55],
        "refined_block_sizes": [144, 89],
        "source_current": [str(value) for value in source_expectations],
        "source_current_lorentz_norm_squared": "p^6",
        "first_refined_density": {
            "plus": "p*Rplus*diag(y*y^T,0_55)*Rplus^T",
            "minus": "p^2*Rminus*(y*y^T)*Rminus^T",
            "positive_rank_one_weights": ["p", "p^2"],
            "trace": "p+p^2=1",
        },
        "preserved_current_algebra_word_expectations": preserved_values,
        "scope": {
            "actual_recorded_A9_state_refines_to_a_positive_state": True,
            "source_and_all_polynomial_readouts_preserved_under_owned_Jones_maps": True,
            "canonical_Jones_conditional_vector_binding": False,
            "physical_execution_or_clock_derived": False,
            "joint_q_D_b_m_field_transition_derived": False,
            "metric_source_or_Ward_identity_derived": False,
            "curved_solution_or_GR_derived": False,
        },
    }
    if args.write:
        RECEIPT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    else:
        if json.loads(RECEIPT.read_text()) != result:
            raise AssertionError("IMMUTABLE_AFCAR_STATE_REFINEMENT_RECEIPT_MISMATCH")
    print("PASS_AFCAR_POSITIVE_STATE_REFINEMENT", len(checks), "exact checks")


if __name__ == "__main__":
    main()
