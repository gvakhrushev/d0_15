#!/usr/bin/env python3
"""Exact endpoint/order obstruction for a shift-only CAR record functor.

This combines the owned affine path law with the actual sixteen-component
CAR record returns. It proves only that the pure translation endpoint cannot
carry the ordered record product on one fixed carrier; it does not exclude a
stateful, history-retaining, or link-dependent native operation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
GOLDEN_CHECK = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_check.py"
GOLDEN_RESULT = "02_REGISTRY/research/certificates/a4d_native_golden_channel_endogenous_preparation_results.json"
GOLDEN_PROOF = "02_REGISTRY/research/A4D_NATIVE_GOLDEN_CHANNEL_ENDOGENOUS_PREPARATION.md"
PINNED_GOLDEN_CHECK = "d78de07609370a307f30d1daeec9d45dd81de1eb7558654105ef32dc51ba89dd"
PINNED_GOLDEN_RESULT = "13be7f995f36fb53bd837b43aaca51546b124a65aeb81ce840e06d951891c000"
PINNED_GOLDEN_PROOF = "73187cd2a77d3350b01a29f780d939a0a86b2e65c4622b85dc6b18ca283f7df9"


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("affine_translation_record_order:" + label)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None, "load_owned_definition")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compose_affine(left, right):
    D1, b1 = left
    D2, b2 = right
    return (D1 * D2, b1 + D1 * b2)


def run():
    checks = []

    def check(label, condition):
        require(condition, label)
        checks.append(label)

    check("golden_channel_checker_pin", sha(GOLDEN_CHECK) == PINNED_GOLDEN_CHECK)
    check("golden_channel_result_pin", sha(GOLDEN_RESULT) == PINNED_GOLDEN_RESULT)
    check("golden_channel_proof_pin", sha(GOLDEN_PROOF) == PINNED_GOLDEN_PROOF)
    receipt = json.loads((ROOT / GOLDEN_RESULT).read_bytes())
    check("upstream_conditional_record_result_pass",
          receipt.get("status") == "PASS_CONDITIONAL_PRIMITIVE_GOLDEN_RECORD_CHANNEL"
          and receipt.get("exact_controls") == 76
          and receipt.get("channel", {}).get("returns")
          == "U_r=record(I_4,e_r), r=0..3, actual 16-component CAR carrier")
    check("upstream_proof_and_checker_self_consistent",
          receipt.get("checker_sha256") == sha(GOLDEN_CHECK)
          and receipt.get("proof_sha256") == sha(GOLDEN_PROOF))
    for path, expected in receipt["input_sha256"].items():
        check("upstream_transitive_input_pin:" + path, sha(path) == expected)

    source = load(GOLDEN_CHECK, "affine_translation_golden_source")
    chronology = load(source.CHRONOLOGY_CHECK, "affine_translation_chronology_owner")
    owner = chronology.old
    I4, I16 = s.eye(4), s.eye(16)
    basis = [I4[:, r] for r in range(4)]
    returns = [chronology.record(I4, n)[0] for n in basis]
    check("all_four_returns_are_the_owned_orthogonal_full16_records",
          len(returns) == 4 and all(owner.zero(U.T * U - I16) for U in returns))

    # The affine path law (D1,b1)(D2,b2)=(D1D2,b1+D1*b2) makes pure
    # translations an abelian subgroup. Check the exact pair used below.
    t0 = (I4, basis[0])
    t1 = (I4, basis[1])
    t01, t10 = compose_affine(t0, t1), compose_affine(t1, t0)
    check("two_oriented_affine_translations_have_same_endpoint",
          t01[0] == t10[0] == I4 and t01[1] == t10[1] == basis[0] + basis[1])

    commutator = (returns[0] * returns[1] - returns[1] * returns[0]).applyfunc(owner.red)
    witness = owner.red(commutator[0, 3])
    check("full16_CAR_commutator_has_exact_witness_2p_minus_2",
          owner.zero(witness - (2 * owner.p - 2)))
    check("exact_commutator_witness_is_nonzero",
          not owner.zero(witness))
    check("ordered_history_words_have_same_shift_but_distinct_native_products",
          owner.zero((returns[0] * returns[1] - returns[1] * returns[0])[0, 3]
                     - (2 * owner.p - 2)))

    # A homomorphism or anti-homomorphism from the affine translation group
    # into the record unitaries must send commuting inputs to commuting
    # outputs. The exact CAR witness contradicts either convention.
    check("shift_only_path_functor_cannot_match_both_native_basis_returns",
          (t01 == t10) and not owner.zero(witness))

    return {
        "schema": "d0-native-affine-translation-record-order/1",
        "status": "PASS_EXACT_SHIFT_ENDPOINT_LOSES_CAR_ORDER",
        "exact_controls": len(checks),
        "checks": checks,
        "carrier": "all 16 exterior components of the owned CAR record",
        "affine_subgroup": "pure translations (I,b), with (I,b)(I,c)=(I,b+c)",
        "translation_pair": {"first": [1, 0, 0, 0], "second": [0, 1, 0, 0],
                             "common_endpoint_shift": [1, 1, 0, 0]},
        "commutator_entry_0_3": str(witness),
        "commutator_is_nonzero": True,
        "history_pair": "word 01 and word 10 have the same affine endpoint but different full16 return products",
        "necessary_escape": "retain order in an existing state/history or let the operation depend on additional native data",
        "scope": {
            "shift_only_compositional_unitary_readout_excluded": True,
            "stateful_history_readout_excluded": False,
            "link_dependent_readout_excluded": False,
            "full_core_no_go": False,
            "physical_admission_derived": False,
            "own_source_Ward_or_GR_closed": False,
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
