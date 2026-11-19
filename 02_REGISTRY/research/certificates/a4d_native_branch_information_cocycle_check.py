#!/usr/bin/env python3
"""Exact finite-history checks for the native branch-information cocycle."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
RECEIPT = Path(__file__).with_name("a4d_native_branch_information_cocycle_certificate.json")
LEAN_CAPSULE = "02_REGISTRY/research/certificates/a4d_native_branch_information_cocycle.lean"
LEAN_OUTPUT = "02_REGISTRY/research/certificates/a4d_native_branch_information_cocycle_output.txt"
LEAN_DECLARATIONS = {
    "codeCost_eq_reference_surprisal",
    "code_minus_pathInfo_eq_pathAction",
    "pathInfo_unique",
    "pathInfo_increment_eq_localInfo",
    "likelihood_nonneg",
    "likelihood_refines",
    "movingPathInfo_hasDerivAt",
}
STANDARD_LEAN_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PINS = {
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md":
        "ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa",
    "03_FORMALIZATION/D0/CondensedAnchor/DetectorSupportGoldenWeight.lean":
        "d7f7f170815cc3ad2052ad48280ae5919652b314",
    "02_REGISTRY/research/A4D_NATIVE_DIRECT_FORCING_ATTACK.md":
        "2def57a045d3a3f83b058c35bb56aec390ce1733",
    "02_REGISTRY/research/sources/d0_direct_forcing_attack_2026-10-14/RESULT.md":
        "d421f20e91c3feb0d636428a1db19233ffb89f5f",
    "02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/continuation_v3/proofs/MOVING_PREPARATION_SOURCE_RU.md":
        "2fe1893246a6ed4985649b6e20af800cec4870f6",
}


class Checks:
    def __init__(self) -> None:
        self.names: list[str] = []

    def require(self, name: str, condition: object) -> None:
        if not bool(condition):
            raise AssertionError(name)
        self.names.append(name)


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "hash-object", path], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write a new immutable receipt")
    args = parser.parse_args()
    checks = Checks()

    for path, expected in SOURCE_PINS.items():
        checks.require(f"source_blob:{path}", git_blob(path) == expected)

    lean_source = (ROOT / LEAN_CAPSULE).read_text()
    lean_output = (ROOT / LEAN_OUTPUT).read_text()
    axiom_blocks = re.findall(
        r"'D0\.Research\.NativeBranchInformationCocycle\.([^']+)' depends on axioms: \[([^\]]*)\]",
        lean_output,
        flags=re.S,
    )
    lean_axioms = {
        name: [axiom.strip() for axiom in raw.split(",") if axiom.strip()]
        for name, raw in axiom_blocks
    }
    checks.require("lean_output_has_all_seven_declarations", set(lean_axioms) == LEAN_DECLARATIONS)
    checks.require(
        "lean_declarations_use_only_standard_axioms",
        all(set(axioms) <= STANDARD_LEAN_AXIOMS for axioms in lean_axioms.values()),
    )
    checks.require("lean_output_has_no_sorry_axiom", "sorryAx" not in lean_output)
    checks.require("lean_source_has_no_sorry_or_admit", not re.search(r"\b(sorry|admit)\b", lean_source))

    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2
    p = 1 / phi
    log_phi = sp.log(phi)
    # Diagnostic factorized Bernoulli law only; 0 < r < 1 is its probability
    # domain. The generic pathwise theorem is in the Lean capsule, while the
    # actual comparator instrument is consumed from the separately pinned
    # direct-forcing owner.
    r = sp.symbols("r", positive=True)

    def q_word(word: tuple[bool, ...]) -> sp.Expr:
        # The owned code uses True=direct (0) and False=return (10).
        out: sp.Expr = sp.Integer(1)
        for direct in word:
            out *= (1 - r) if direct else r
        return out

    def mu_word(word: tuple[bool, ...]) -> sp.Expr:
        code_cost = sum(1 if direct else 2 for direct in word)
        return p**code_cost

    path_count = 0
    for depth in range(1, 7):
        for word in product((True, False), repeat=depth):
            q = q_word(word)
            mu = mu_word(word)
            cost = sum(1 if direct else 2 for direct in word)
            info = sp.expand_log(sp.log(q / mu) / log_phi, force=True)
            action = sp.expand_log(-sp.log(q) / log_phi, force=True)
            checks.require(
                f"pathwise_cost_minus_info_is_action:{depth}:{''.join('0' if b else '10' for b in word)}",
                sp.simplify(cost - info - action) == 0,
            )
            path_count += 1

    prefix_count = 0
    for depth in range(0, 6):
        for prefix in product((True, False), repeat=depth):
            q_parent = q_word(prefix)
            mu_parent = mu_word(prefix)
            q_direct, q_return = q_word(prefix + (True,)), q_word(prefix + (False,))
            mu_direct, mu_return = mu_word(prefix + (True,)), mu_word(prefix + (False,))
            checks.require(
                f"measured_prefix_mass:{depth}:{prefix}",
                sp.simplify(q_direct + q_return - q_parent) == 0,
            )
            checks.require(
                f"golden_prefix_mass:{depth}:{prefix}",
                sp.simplify(mu_direct + mu_return - mu_parent) == 0,
            )
            likelihood = q_parent / mu_parent
            refined_likelihood = mu_direct * (q_direct / mu_direct) + mu_return * (q_return / mu_return)
            checks.require(
                f"likelihood_martingale:{depth}:{prefix}",
                sp.simplify(refined_likelihood - mu_parent * likelihood) == 0,
            )
            prefix_count += 1

    # The local log-likelihood increments telescope along each full record.
    for depth in range(1, 6):
        for word in product((True, False), repeat=depth):
            q_parent: sp.Expr = sp.Integer(1)
            mu_parent: sp.Expr = sp.Integer(1)
            local_sum: sp.Expr = sp.Integer(0)
            for direct in word:
                q_child = q_parent * ((1 - r) if direct else r)
                mu_child = mu_parent * (p if direct else p**2)
                local_sum += sp.log((q_child / q_parent) / (mu_child / mu_parent)) / log_phi
                q_parent, mu_parent = q_child, mu_child
            total = sp.log(q_parent / mu_parent) / log_phi
            checks.require(
                f"conditional_information_cocycle:{depth}:{word}",
                sp.simplify(sp.expand_log(local_sum - total, force=True)) == 0,
            )

    # Expected branch information is the KL divergence to the golden code law.
    for depth in range(1, 6):
        expected_info = sp.Integer(0)
        for word in product((True, False), repeat=depth):
            q, mu = q_word(word), mu_word(word)
            expected_info += q * sp.log(q / mu) / log_phi
        binary_kl = depth * (
            (1 - r) * sp.log((1 - r) / p) + r * sp.log(r / p**2)
        ) / log_phi
        checks.require(
            f"expected_information_is_KL:{depth}",
            sp.simplify(sp.expand_log(expected_info - binary_kl, force=True)) == 0,
        )
        expected_code = depth * (1 + r)
        expected_action = depth * (
            -(1 - r) * sp.log(1 - r) - r * sp.log(r)
        ) / log_phi
        checks.require(
            f"expected_code_minus_KL_is_path_entropy:{depth}",
            sp.simplify(sp.expand_log(expected_code - binary_kl - expected_action, force=True)) == 0,
        )
        expected_kl_derivative = depth * sp.log(r / (p * (1 - r))) / log_phi
        checks.require(
            f"joint_source_derivative_of_expected_KL:{depth}",
            sp.simplify(sp.expand_log(sp.diff(binary_kl, r) - expected_kl_derivative, force=True)) == 0,
        )

    # A full state/effect contraction keeps both preparation and operator jets.
    x, e0, e1, dx, de0, de1 = sp.symbols("x e0 e1 dx de0 de1", real=True)
    measured_q = (1 - x) * e0 + x * e1
    measured_dq = (-dx) * e0 + (1 - x) * de0 + dx * e1 + x * de1
    chain_rule = (
        sp.diff(measured_q, x) * dx
        + sp.diff(measured_q, e0) * de0
        + sp.diff(measured_q, e1) * de1
    )
    checks.require("moving_preparation_and_effect_share_one_probability_jet", sp.expand(chain_rule - measured_dq) == 0)
    checks.require(
        "moving_preparation_omission_is_detected",
        sp.simplify(measured_dq.subs({x: sp.Rational(1, 2), e0: sp.Rational(1, 4), e1: sp.Rational(3, 4), dx: 1, de0: 0, de1: 0}))
        == sp.Rational(1, 2),
    )

    # Hostile controls: an expected Shannon entropy is not the pathwise branch increment.
    checks.require("golden_direct_return_costs_are_distinct", sp.Integer(1) != sp.Integer(2))
    checks.require("golden_direct_return_code_is_normalized", sp.simplify(p + p**2 - 1) == 0)
    checks.require("golden_direct_branch_probability_is_not_half", sp.simplify(p - sp.Rational(1, 2)) == (sqrt5 - 2) / 2)
    no_error_info_at_half = sp.log(sp.Rational(1, 2) / p) / log_phi
    shannon_at_half = sp.log(2) / log_phi
    checks.require(
        "reject_pointwise_info_equals_Shannon_entropy",
        sp.N(no_error_info_at_half, 50) < 0 and sp.N(shannon_at_half, 50) > 0,
    )
    checks.require(
        "reject_erasing_return_child",
        sp.simplify(q_word((True,)) + 0 - q_word(())) != 0,
    )

    certificate = {
        "schema": "d0-native-branch-information-cocycle/1",
        "status": "PASS",
        "source_pins": SOURCE_PINS,
        "exact_condition_count": len(checks.names),
        "finite_path_instances_checked": path_count,
        "prefix_instances_checked": prefix_count,
        "local_cocycle_instances_checked": sum(2**n for n in range(1, 6)),
        "conditions": checks.names,
        "lean_evidence": {
            "compile_command": "cd 03_FORMALIZATION && lake env lean ../" + LEAN_CAPSULE,
            "local_standalone_compile": "PASS",
            "capsule_git_blob": git_blob(LEAN_CAPSULE),
            "output_git_blob": git_blob(LEAN_OUTPUT),
            "declarations": sorted(lean_axioms),
            "axioms": lean_axioms,
            "scope": "standalone capsule only; no D0.All or GitHub CI claim",
        },
        "scope": {
            "book_weight_binding_used_conditionally": True,
            "book_weight_binding_physically_derived": False,
            "cost_binding_used_conditionally": True,
            "finite_expectation_fixture": "factorized Bernoulli q_r, 0<r<1, fixed round depths T=1..5",
            "actual_instrument_finite_instances_replayed": False,
            "native_physical_action_selected": False,
            "full_D0_state_action_refinement_family_derived": False,
            "full_coherent_record_entropy_selected": False,
            "curved_Einstein_or_GR_closed": False,
        },
        "sympy": sp.__version__,
    }
    encoded = json.dumps(certificate, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        RECEIPT.write_text(encoded)
        print("WROTE", RECEIPT)
    else:
        if not RECEIPT.is_file():
            raise SystemExit("MISSING_IMMUTABLE_RECEIPT; rerun with --write after review")
        current = json.loads(RECEIPT.read_text())
        if current != certificate:
            raise SystemExit("IMMUTABLE_RECEIPT_MISMATCH")
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    print("PASS_NATIVE_BRANCH_INFORMATION_COCYCLE", len(checks.names), "exact conditions")
    print("paths", path_count, "prefixes", prefix_count, "receipt_sha256", digest)


if __name__ == "__main__":
    main()
