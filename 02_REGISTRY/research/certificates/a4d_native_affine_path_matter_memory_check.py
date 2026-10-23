#!/usr/bin/env python3
"""Exact full-state memory witness for equal-endpoint affine path orders."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
ORDER_CHECK = "02_REGISTRY/research/certificates/a4d_native_affine_translation_record_order_check.py"
ORDER_RESULT = "02_REGISTRY/research/certificates/a4d_native_affine_translation_record_order_results.json"
ORDER_PROOF = "02_REGISTRY/research/A4D_NATIVE_AFFINE_TRANSLATION_CAR_ORDER.md"
ORDER_PINS = {
    ORDER_CHECK: "fa9cc590c069955462ceb29e36358ced02077e9a86b9a018c720104d7ae22918",
    ORDER_RESULT: "0c9466fae49f0018a76381d5e8d71617a34e401ef1b23e2d53430d8af5c595ba",
    ORDER_PROOF: "e0cb43d110d468225b54be37c9ebc26c709d7c68f9b045924c73369c2e1d318e",
}
CLOSED_CHECK = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine_check.py"
CLOSED_CERT = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine_certificate.json"
CLOSED_PROOF = "02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md"
CLOSED_PINS = {
    CLOSED_CHECK: "7d4cd83521729b780758c8559b9168668f6aac8437f89c9b8652b1141f2692f8",
    CLOSED_CERT: "2c6060cc856083c4dc60ee67b8b2bfca1a9a4967f4992bcfdc3b5ef6c604d5ce",
    CLOSED_PROOF: "36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a",
}
GOLDEN_CHECK = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_check.py"
GOLDEN_RESULT = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_results.json"


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("affine_path_matter_memory:" + label)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None, "load_owned_definition")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    checks = []

    def check(label, condition):
        require(condition, label)
        checks.append(label)

    for path, expected in ORDER_PINS.items():
        check("ordered_translation_owner_pin:" + path, sha(path) == expected)
    for path, expected in CLOSED_PINS.items():
        check("closed_record_engine_pin:" + path, sha(path) == expected)

    order_result = json.loads((ROOT / ORDER_RESULT).read_bytes())
    check("equal_endpoint_order_obstruction_pass",
          order_result.get("status") == "PASS_EXACT_SHIFT_ENDPOINT_LOSES_CAR_ORDER"
          and order_result.get("commutator_is_nonzero") is True)
    closed = json.loads((ROOT / CLOSED_CERT).read_bytes())
    check("native_closed_record_engine_certificate_pass",
          closed.get("status") == "PASS" and closed.get("exact_controls") == 24745
          and closed.get("scope", {}).get("state")
          == "ALL_16_REAL_EXTERIOR_COMPONENTS_EXACT_INTEGER_GOLDEN_COEFFICIENTS")
    check("closed_engine_checker_and_proof_self_consistent",
          closed.get("checker_sha256") == sha(CLOSED_CHECK)
          and closed.get("proof_sha256") == sha(CLOSED_PROOF))
    for path, expected in closed["input_sha256"].items():
        check("closed_engine_transitive_input_pin:" + path, sha(path) == expected)

    engine = load("02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py",
                  "affine_path_existing_native_matter_seed")
    seed = engine.seed()
    check("seed_is_the_existing_whole_blank_on_all_16_slots",
          len(seed.matter) == 16
          and seed.matter[1] == seed.matter[15] == engine.ONE
          and all(not seed.matter[i] for i in range(16) if i not in (1, 15)))
    seed_vec = s.Matrix([int(bool(value)) for value in seed.matter])
    check("seed_vector_is_e0_plus_volume", seed_vec[1] == seed_vec[15] == 1
          and sum(seed_vec) == 2)

    golden = load(GOLDEN_CHECK, "affine_path_existing_native_record")
    chronology = golden.load(golden.CHRONOLOGY_CHECK, "affine_path_chronology")
    owner = chronology.old
    I4, I16 = s.eye(4), s.eye(16)
    e = [I4[:, r] for r in range(4)]
    U = [chronology.record(I4, e[r])[0] for r in range(4)]
    check("records_are_actual_full16_orthogonal_native_operators",
          all(owner.zero(U[r].T * U[r] - I16) for r in range(4)))

    # Left action m -> U_r m: chronological 0,1 is U_1 U_0 m; 1,0 is
    # U_0 U_1 m. Their affine translation endpoint is identical by the
    # already checked affine path owner.
    state_01 = (U[1] * U[0] * seed_vec).applyfunc(owner.red)
    state_10 = (U[0] * U[1] * seed_vec).applyfunc(owner.red)
    delta = (state_10 - state_01).applyfunc(owner.red)
    support = [(i, owner.red(delta[i])) for i in range(16) if not owner.zero(delta[i])]
    expected = {2: owner.red(2 - 2 * owner.p),
                12: owner.red(2 * owner.p - 2)}
    check("full_state_difference_has_exact_two_slot_support",
          len(support) == 2 and {i for i, _ in support} == set(expected))
    check("full_state_difference_is_signed_2_minus_2p_pair",
          all(owner.zero(delta[i] - expected[i]) for i in expected))
    norm_squared = owner.red(sum((delta[i] * delta[i] for i in range(16)), s.Integer(0)))
    check("whole_blank_euclidean_memory_distance_is_16_minus_24p",
          owner.zero(norm_squared - (16 - 24 * owner.p))
          and not owner.zero(norm_squared))
    check("both_history_states_are_distinct_native_full_vectors",
          state_01 != state_10 and len(state_01) == len(state_10) == 16)

    return {
        "schema": "d0-native-affine-path-matter-memory/1",
        "status": "PASS_EXACT_EXISTING_MATTER_DISTINGUISHES_PATH_ORDER_PAIR",
        "exact_controls": len(checks), "checks": checks,
        "initial_state": "actual whole blank e0+volume, all sixteen coordinates retained",
        "ordered_paths": ["0 then 1", "1 then 0"],
        "affine_endpoint_for_both": "(I,e0+e1)",
        "state_difference_nonzero_slots_zero_based": {
            "2": str(expected[2]), "12": str(expected[12])},
        "euclidean_norm_squared": str(norm_squared),
        "exact_positivity_reason": "p>0 and p+p^2=1 imply p<2/3, hence 16-24p>0",
        "scope": {
            "existing_16_component_state_can_store_this_order_bit": True,
            "all_possible_path_histories_injective": False,
            "affine_shift_to_record_transition_physically_admitted": False,
            "refinement_compatibility_proved": False,
            "finite_physical_bit_capacity_derived": False,
            "native_source_Ward_or_GR_closed": False,
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
