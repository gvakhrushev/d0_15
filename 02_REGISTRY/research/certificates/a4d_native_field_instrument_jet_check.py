#!/usr/bin/env python3
"""Exact two-completion witness for the missing field-to-instrument jet.

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
import sys
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "02_REGISTRY" / "research" / "certificates"
SOURCE = ROOT / "02_REGISTRY" / "research" / "sources" / "d0_local_record_to_matter_2026-10-14" / "continuation_v3"
PROOF = ROOT / "02_REGISTRY" / "research" / "A4D_NATIVE_FIELD_TO_INSTRUMENT_JET_BOUNDARY.md"
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
    require("same_base_acceptance_probability", red(first[0] - second[0]) == 0)
    require("same_base_normalized_cost", red(first[2] - second[2]) == 0)
    require("exact_fixed_event_probability", red(first[0] - expected_probability) == 0)
    require("exact_reference_cost", red(first[2] - expected_mean) == 0)
    require("completion_one_exact_source_jet", red(first[3] - unit_response) == 0)
    require("completion_two_exact_source_jet", red(second[3] - 2 * unit_response) == 0)
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
        "schema": "d0-native-field-instrument-jet-boundary/1",
        "status": "PASS_TWO_COMPLETIONS_SAME_BASE_DISTINCT_EXACT_SOURCE_JETS",
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
            "probe_coordinate": "xi(t)=t, same unit calibration in both completions",
            "count_budget": 3,
            "fixed_recorded_event": [1, 2],
            "initial_density": "I/4",
            "kinetic_operator_spectrum": [0, 6, 4, 6],
        },
        "exact_shared_base": {
            "acceptance_probability": str(red(expected_probability)),
            "prepared_cost": str(red(expected_mean)),
        },
        "completions": [
            {"jet_scale": 1, "prepared_source_derivative": str(red(first[3]))},
            {"jet_scale": 2, "prepared_source_derivative": str(red(second[3]))},
        ],
        "checks": checks,
        "exact_controls": len(checks),
        "negative_controls": negatives,
        "missing_datum": "the admitted map from coframe/link field variations to unitary-return tangents (including its scale and constraints)",
        "physical_source_or_stress_claim": False,
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
    print(f"PASS_FIELD_INSTRUMENT_JET_BOUNDARY {result['exact_controls']} exact controls")
    print("same reference event and prepared cost; source derivative doubles under the second allowed field-to-return completion")


if __name__ == "__main__":
    main()
