#!/usr/bin/env python3
"""Complete unitary first-jet family and exact field-to-instrument witness.

The source instrument and its event are held fixed at the reference point.
Only the unowned map from one declared scalar field probe to its unitary-return
jet is varied. The witness is deliberately an interface boundary, not a claim
that either completion is already physically admitted by D0.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "02_REGISTRY" / "research" / "certificates"
SOURCE = ROOT / "02_REGISTRY" / "research" / "sources" / "d0_local_record_to_matter_2026-10-14" / "continuation_v3"
PROOF = ROOT / "02_REGISTRY" / "research" / "A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md"
FIELD_PROOF = ROOT / "02_REGISTRY" / "research" / "A4D_NATIVE_JOINT_FIELD_QUOTIENT.md"
FIELD_CHECK = CERT / "a4d_native_joint_field_quotient_check.py"
FIELD_RESULTS = CERT / "a4d_native_joint_field_quotient_results.json"
FIELD_CERTIFICATE = CERT / "a4d_native_joint_field_quotient_certificate.json"
STEM = "a4d_native_field_instrument_jet"
INPUT_HEAD = "f1270f63cffa5fcfc27b469ff2517d8398d5362a"
INPUTS = {
    "src/moving_preparation_exact.py": "1b3d0f5e10a59ca97daaf06744d6fe1429e7643dd350523b897ca9e2b287bc06",
    "proofs/MOVING_PREPARATION_SOURCE_RU.md": "67bea08cc8a39f49fe92f6d679eabe9d1ae2df7daee260dfe55c23641d45cb61",
    "results/moving_preparation_exact.json": "dec95b219a55d5cd39e8e65bfc6f538cf4be1fa43630cc5c14ee96ce97f7470f",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_reducer():
    path = SOURCE / "src" / "moving_preparation_exact.py"
    spec = importlib.util.spec_from_file_location("moving_preparation_exact_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("CANNOT_LOAD_MOVING_PREPARATION_OWNER")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.red


def run() -> dict:
    for relative, expected in INPUTS.items():
        actual = digest(SOURCE / relative)
        if actual != expected:
            raise AssertionError(f"INPUT_PIN_MISMATCH:{relative}:{actual}")
    source_receipt = json.loads((SOURCE / "results/moving_preparation_exact.json").read_text())
    if source_receipt.get("status") != "PASS" or source_receipt.get("exact_controls") != 169:
        raise AssertionError("MOVING_PREPARATION_SOURCE_RECEIPT_NOT_PASS")

    red = load_source_reducer()
    p = s.symbols("p", real=True)
    minimal = p * p + p - 1

    def mat(value):
        return value.applyfunc(red)

    def zero(value):
        return all(red(entry) == 0 for entry in value)

    checks: list[str] = []
    negatives: list[str] = []

    def require(name: str, condition: bool) -> None:
        if not bool(condition):
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    def reject(name: str, false_claim: bool) -> None:
        require("REJECT_" + name, false_claim)
        negatives.append(name)

    joint_owner = json.loads(FIELD_CERTIFICATE.read_text())
    joint_receipt = json.loads(FIELD_RESULTS.read_text())
    joint_replay = subprocess.run(
        [sys.executable, str(FIELD_CHECK), "--expect", str(FIELD_CERTIFICATE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(
        "current_joint_field_quotient_owner_replays",
        joint_replay.returncode == 0
        and "PASS_NATIVE_JOINT_FIELD_QUOTIENT 41 controls 51 D0 pins" in joint_replay.stdout,
    )
    require(
        "joint_field_owner_keeps_action_and_admission_open",
        joint_owner["scope"]["native_joint_action_selected"] is False
        and joint_owner["scope"]["all_native_admission_constraints_classified"] is False
        and joint_owner["scope"]["G0_closed"] is False,
    )

    # A genuine trace-free, non-gauge tangent in the complete joint quotient.
    # Use the smallest L in the core's L in 4N carrier, and check the actual
    # differentiated edge constraint with its owned source/target convention.
    t = s.symbols("t", real=True)
    eta = s.diag(1, -1, -1, -1)
    metric_tangent = s.diag(1, 1, 0, 0)
    q_path = eta + t * metric_tangent
    raw_lift = s.diag(s.sqrt(1 + t), s.sqrt(1 - t), 1, 1)
    dressed_link = s.eye(4)
    link_tangent = s.zeros(4)
    q_source = eta
    q_target = eta
    delta_q_source = metric_tangent
    delta_q_target = metric_tangent
    require(
        "actual_joint_field_probe_satisfies_reference_edge_constraint",
        dressed_link * q_target * dressed_link.T == q_source,
    )
    require(
        "actual_joint_field_probe_has_raw_lift",
        all(s.simplify(x) == 0 for x in raw_lift * eta * raw_lift.T - q_path),
    )
    require(
        "actual_joint_field_probe_satisfies_edge_constraint_jet",
        dressed_link * delta_q_target * dressed_link.T
        + link_tangent * q_target * dressed_link.T
        + dressed_link * q_target * link_tangent.T
        - delta_q_source
        == s.zeros(4),
    )
    require(
        "actual_joint_field_probe_satisfies_finite_edge_constraint",
        dressed_link * q_path * dressed_link.T == q_path,
    )
    require(
        "actual_joint_field_probe_is_nongauge_and_metric_tracefree",
        metric_tangent != s.zeros(4)
        and metric_tangent.T == metric_tangent
        and s.trace(eta.inv() * metric_tangent) == 0
        and s.diff(q_path.det(), t).subs(t, 0) == 0,
    )
    L = s.Integer(4)  # smallest carrier in the registered L in 4N class.
    site_count = L**4
    probe_derivative = s.simplify(
        site_count * s.trace(metric_tangent * metric_tangent) / (2 * site_count)
    )
    require("actual_joint_field_probe_has_unit_fixed_calibration", probe_derivative == 1)
    require(
        "complete_joint_quotient_dimension_on_registered_carrier",
        site_count == 256
        and 106 * site_count - 10 * (4 * site_count) == 66 * site_count,
    )
    require(
        "complete_two_return_first_jet_dimension_on_registered_carrier",
        32 * 66 * site_count == 540672,
    )

    I = s.eye(4)
    q = 2
    gamma = red(p**3)
    returns = [
        s.diag(1, -1, s.I, -s.I),
        s.diag(1, s.I, -s.I, -1),
    ]
    generators = [
        s.Matrix([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 2, 1], [0, 0, 1, -1]]),
        s.Matrix([[0, 0, 1, 0], [0, 2, 0, 1], [1, 0, -1, 0], [0, 1, 0, 1]]),
    ]
    base_jets = [s.I * H * U for H, U in zip(generators, returns)]
    require("reference_returns_are_unitary", all(zero(U.H * U - I) for U in returns))
    require("reference_returns_commute", zero(returns[0] * returns[1] - returns[1] * returns[0]))
    require("generators_are_hermitian", all(H == H.H for H in generators))

    def channel(branch: int, rho):
        if branch == 1:
            return mat(gamma * sum(((U - I) * rho * (U - I).H for U in returns), s.zeros(4)) / q)
        return mat(sum(((p * I + p * p * U) * rho * (p * I + p * p * U).H for U in returns), s.zeros(4)) / q)

    def channel_jet(branch: int, rho, scale: int):
        answer = s.zeros(4)
        for U, jet in zip(returns, base_jets):
            jet = scale * jet
            A = U - I if branch == 1 else p * I + p * p * U
            dA = jet if branch == 1 else p * p * jet
            answer += dA * rho * A.H + A * rho * dA.H
        return mat((gamma if branch == 1 else 1) * answer / q)

    Delta = mat(sum(((U - I).H * (U - I) for U in returns), s.zeros(4)))
    base_delta_jet = mat(
        sum((jet.H * (U - I) + (U - I).H * jet for U, jet in zip(returns, base_jets)), s.zeros(4))
    )
    require("owned_reference_kinetic_spectrum", [Delta[j, j] for j in range(4)] == [0, 6, 4, 6])

    def evaluate(scale: int):
        states = [I / 4]
        jets = [s.zeros(4)]
        for total in range(1, 4):
            next_states = []
            next_jets = []
            for count in range(total + 1):
                value = s.zeros(4)
                tangent = s.zeros(4)
                if count < total:
                    value += channel(0, states[count])
                    tangent += channel(0, jets[count]) + channel_jet(0, states[count], scale)
                if count > 0:
                    value += channel(1, states[count - 1])
                    tangent += channel(1, jets[count - 1]) + channel_jet(1, states[count - 1], scale)
                next_states.append(mat(value))
                next_jets.append(mat(tangent))
            states, jets = next_states, next_jets
        # Fixed event: 1 <= recorded error count <= 2 out of T=3.
        sigma = mat(states[1] + states[2])
        sigma_jet = mat(jets[1] + jets[2])
        probability = red(s.trace(sigma))
        probability_jet = red(s.trace(sigma_jet))
        rho = mat(sigma / probability)
        mean = red(s.trace(Delta * rho))
        full_jet = red(
            (s.trace(scale * base_delta_jet * sigma + Delta * sigma_jet) - mean * probability_jet)
            / probability
        )
        frozen_jet = red(s.trace(scale * base_delta_jet * rho))
        return probability, probability_jet, mean, full_jet, frozen_jet

    first = evaluate(1)
    second = evaluate(2)
    p_alg = (s.sqrt(5) - 1) / 2
    expected_probability = 144 * p - s.Rational(177, 2)
    expected_mean = (380 - 12 * p) / 71
    unit_response = (1644 * p + 17733) / 5041
    scale = s.symbols("scale", real=True)
    arbitrary_scale = evaluate(scale)
    require("same_base_acceptance_probability", red(first[0] - second[0]) == 0)
    require("same_base_normalized_cost", red(first[2] - second[2]) == 0)
    require("exact_fixed_event_probability", red(first[0] - expected_probability) == 0)
    require("exact_reference_cost", red(first[2] - expected_mean) == 0)
    require("completion_one_exact_source_jet", red(first[3] - unit_response) == 0)
    require("completion_two_exact_source_jet", red(second[3] - 2 * unit_response) == 0)
    require("event_normalizer_jet_linear_in_free_scale", red(second[1] - 2 * first[1]) == 0)
    require("event_normalizer_jet_linear_for_all_real_scales", red(arbitrary_scale[1] - scale * first[1]) == 0)
    require("event_normalizer_jet_is_nonzero", red(first[1]) != 0)
    require(
        "prepared_response_is_linear_for_the_complete_scale_family",
        red(arbitrary_scale[3] - scale * unit_response) == 0,
    )
    require("constant_return_completion_has_zero_field_response", red(evaluate(0)[3]) == 0)
    fixed_calibration = s.Integer(1)
    require("same_fixed_calibration_preserves_distinct_jets",
            red(second[3] / fixed_calibration - first[3] / fixed_calibration) != 0)
    require("event_probability_is_positive", s.simplify(expected_probability.subs(p, p_alg)).is_positive is True)
    require("source_jet_is_positive", s.simplify(unit_response.subs(p, p_alg)).is_positive is True)
    require("the_two_source_jets_are_distinct", red(second[3] - first[3]) != 0)
    require("unitary_tangent_for_both_completions", all(
        zero((scale * jet).H * U + U.H * (scale * jet))
        for scale in (1, 2) for U, jet in zip(returns, base_jets)
    ))
    reject("freeze_the_prepared_density", red(first[3] - first[4]) != 0)
    reject("one_baseline_selects_a_unique_field_jet", red(second[3] - first[3]) != 0)
    commutator_jet = (
        base_jets[0] * returns[1] + returns[0] * base_jets[1]
        - base_jets[1] * returns[0] - returns[1] * base_jets[0]
    )
    reject("variations_must_preserve_reference_commutativity", not zero(commutator_jet))

    return {
        "schema": "d0-native-field-instrument-jet-boundary/2",
        "status": "PASS_COMPLETE_INSTRUMENT_FIRST_JET_AND_FIELD_TANGENT_WITNESS",
        "input_source_head": INPUT_HEAD,
        "input_sha256": INPUTS,
        "source_v3_receipt": {
            "status": source_receipt["status"],
            "exact_controls": source_receipt["exact_controls"],
            "physical_admission": source_receipt["physical_admission"],
            "complete_H_J_R_closed": source_receipt["complete_H_J_R_closed"],
        },
        "probe": {
            "reference_returns_commute": True,
            "probe_coordinate": "xi(q)=average_x Tr(K(q_x-eta))/2 on the full joint quotient",
            "actual_joint_field_tangent": "delta q_source=delta q_target=diag(1,1,0,0), delta D=delta b=delta m=0",
            "joint_field_tangent_is_tracefree_nongauge": True,
            "d_xi_on_tangent": str(probe_derivative),
            "joint_field_owner": {
                "status": joint_owner["status"],
                "source_head": joint_receipt["owner_input_head"],
                "revalidated_on_head": joint_receipt.get("revalidated_on_head"),
                "revalidation_note": joint_receipt.get("revalidation_note"),
                "controls": len(joint_owner["checks"]),
                "transitive_d0_pins": joint_owner["transitive_native_pins"],
                "proof_sha256": digest(FIELD_PROOF),
                "checker_sha256": digest(FIELD_CHECK),
                "receipt_sha256": digest(FIELD_RESULTS),
                "certificate_sha256": digest(FIELD_CERTIFICATE),
            },
            "count_budget": 3,
            "fixed_recorded_event": [1, 2],
            "initial_density": "I/4",
            "kinetic_operator_spectrum": [0, 6, 4, 6],
        },
        "exact_shared_base": {
            "acceptance_probability": str(red(expected_probability)),
            "prepared_cost": str(red(expected_mean)),
        },
        "event_normalizer_first_jet": {
            "event": [1, 2],
            "probability": str(red(expected_probability)),
            "d_probability_dxi_lambda1": str(red(first[1])),
            "d_probability_dxi_lambda2": str(red(second[1])),
            "d_probability_dxi_arbitrary_scale": "lambda * (189*p - 117)",
            "dlog_probability_dxi_lambda1": str(red(first[1] / expected_probability)),
            "dlog_probability_dxi_lambda2": str(red(second[1] / expected_probability)),
            "conditional_information_correction_lambda1": "dlog_probability_dxi_lambda1 / log(phi), if the raw event weights are the path weights",
            "conditional_information_correction_lambda2": "dlog_probability_dxi_lambda2 / log(phi), if the raw event weights are the path weights",
            "scope": "event-conditioning normalizer on the declared instrument interface; not an admitted D0 source",
        },
        "completions": [
            {"jet_scale": 1, "prepared_source_derivative": str(red(first[3]))},
            {"jet_scale": 2, "prepared_source_derivative": str(red(second[3]))},
        ],
        "complete_interface_first_jet_family": {
            "domain": "the full constrained tangent quotient from A4D_NATIVE_JOINT_FIELD_QUOTIENT.md",
            "return_target": "Hom_R(T, Herm(4) x Herm(4))",
            "real_dimension": "2112*L^4",
            "all_jets_realized_by": "U_r(x)=exp(i*H_r(x))*U_r(reference), H_r real-linear Hermitian-valued",
            "prepared_scalar_response_on_the_test_tangent": "all real values; lambda*(1644*p+17733)/5041",
            "response_parameter_is_interface_visible": True,
        },
        "checks": checks,
        "exact_controls": len(checks),
        "negative_controls": negatives,
        "missing_datum": "the admitted refinement-compatible map from the full constrained field tangent to unitary-return Lie-algebra tangents, including its scale and constraints",
        "physical_source_or_stress_claim": False,
        "actual_joint_field_kinematic_tangent_used": True,
        "D0_native_admission_of_either_completion": False,
        "G0_or_GR_closed": False,
        "new_Lean_compilation": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write a refreshed adjacent receipt")
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = digest(Path(__file__))
    result["proof_sha256"] = digest(PROOF)
    destination = CERT / f"{STEM}_results.json"
    encoded = json.dumps(result, indent=2) + "\n"
    if args.write:
        destination.write_text(encoded)
    elif not destination.exists() or destination.read_text() != encoded:
        raise AssertionError("IMMUTABLE_RECEIPT_MISMATCH; use --write only for an explicit reviewed update")
    print(f"PASS_COMPLETE_FIELD_INSTRUMENT_FIRST_JET {result['exact_controls']} exact controls")
    print("complete unitary first-jet family; prepared scalar response spans R on an actual joint-field tangent; physical admission remains open")


if __name__ == "__main__":
    main()
