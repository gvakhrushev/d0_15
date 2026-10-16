#!/usr/bin/env python3
"""Exact test whether the literal full CAR return induces a CAR-mode link.

This tests the standard Bogoliubov/one-particle-hole lift only. It does not
exclude a separate native link variable or a state-dependent nonlinear law.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
BASE = "02_REGISTRY/research/certificates/a4d_native_record_non_gaussian_link"
PROOF = "02_REGISTRY/research/A4D_NATIVE_RECORD_NOT_A_BOGOLIUBOV_LINK.md"
CHRON_CHECK = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
CHRON_CERT = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json"
CLOSED_ENGINE = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py"
CLOSED_CHECK = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine_check.py"
CLOSED_CERT = "02_REGISTRY/research/certificates/a4d_native_closed_record_engine_certificate.json"
PINS = {
    CHRON_CHECK: "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    CHRON_CERT: "0b91e13d823568898a006dd468f9963ffbbc1949f0976a21e8530af465ecfbbe",
    CLOSED_ENGINE: "7aead2716c7bf7899a134eedbf4b87dbe1ef9c85900189b5afc8cdfeed13f0f9",
    CLOSED_CHECK: "7d4cd83521729b780758c8559b9168668f6aac8437f89c9b8652b1141f2692f8",
    CLOSED_CERT: "2c6060cc856083c4dc60ee67b8b2bfca1a9a4967f4992bcfdc3b5ef6c604d5ce",
    "02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md":
        "36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py":
        "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_results.json":
        "4c28dd449b844e5a8332d56d457c2bbcd83853069563542dc12f0238439510a8",
    "02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md":
        "d85e57979a61972e641eae24442a776133c429c8696d0948590f6d290a60b045",
    "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean":
        "6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean":
        "5dc96be9c2ee5c874a617f3ebe80f0da9803973c1656112fe24f31e90c2f5eb1",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean":
        "846fddef981b82357bab5b1a4de72d7f27bdfc6321ed41bfdc26e410cbd0178d",
    "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean":
        "69e7a9a0290ee08c748db03c62d5e331e23efdeb84fb6ffefe4165267b14c967",
}
PINNED_9X9_ROWS = [0, 1, 2, 4, 8, 16, 32, 64, 128]


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    if spec is None or spec.loader is None:
        raise ArithmeticError("CANNOT_LOAD_OWNED_DEFINITION:" + path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run() -> dict:
    checks: list[str] = []

    def need(label: str, condition) -> None:
        if not bool(condition):
            raise ArithmeticError("record_non_gaussian_link:" + label)
        checks.append(label)

    for path, expected in PINS.items():
        need("source_pin:" + path, sha(path) == expected)

    chronology_receipt = json.loads((ROOT / CHRON_CERT).read_bytes())
    need("owned_chronology_receipt_pass",
         chronology_receipt.get("status") == "PASS"
         and chronology_receipt.get("exact_controls") == 469)
    for path, expected in chronology_receipt["input_sha256"].items():
        need("chronology_transitive_pin:" + path, sha(path) == expected)
    need("chronology_checker_pin_matches_receipt",
         chronology_receipt.get("checker_sha256") == sha(CHRON_CHECK))

    closed_receipt = json.loads((ROOT / CLOSED_CERT).read_bytes())
    need("actual_seed_engine_receipt_pass",
         closed_receipt.get("status") == "PASS"
         and closed_receipt.get("exact_controls") == 24745)
    need("closed_engine_checker_pin_matches_receipt",
         closed_receipt.get("checker_sha256") == sha(CLOSED_CHECK))
    need("closed_engine_implementation_pin_matches_receipt",
         closed_receipt.get("engine_sha256") == sha(CLOSED_ENGINE))
    need("closed_engine_proof_pin_matches_receipt",
         closed_receipt.get("proof_sha256") == sha(
             "02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md"))
    for path, expected in closed_receipt["input_sha256"].items():
        need("closed_engine_transitive_pin:" + path, sha(path) == expected)

    chronology = load(CHRON_CHECK, "record_non_gaussian_chronology")
    engine = load(CLOSED_ENGINE, "record_non_gaussian_actual_engine")
    old = chronology.old
    I4, I16 = s.eye(4), s.eye(16)
    e0 = I4[:, 0]

    # This is the actual first transition of the owned autonomous seed orbit:
    # the current seed selects +e0, and the literal CAR record returns U_0.
    U, _ = chronology.record(I4, e0)
    U = chronology.mat(U)
    need("literal_return_is_orthogonal", old.zero(U.T * U - I16))

    def from_golden(value):
        u, r, v, t = value.coefficients
        return u + r * old.a + v * old.p + t * old.a * old.p

    seed = engine.seed()
    need("actual_seed_is_all16_role0_plus_top",
         len(seed.matter) == 16
         and seed.matter[1] == seed.matter[15] == engine.ONE
         and all(not seed.matter[i] for i in range(16) if i not in (1, 15)))
    seed_vec = s.Matrix([from_golden(x) for x in seed.matter])
    returned = U * seed_vec
    actual_next = engine.step(seed)
    actual_next_vec = s.Matrix([from_golden(x) for x in actual_next.matter])
    need("record_is_the_actual_first_autonomous_seed_return",
         all(old.zero(returned[i] - actual_next_vec[i]) for i in range(16)))
    need("actual_seed_selects_positive_role0_observer",
         seed.matter[1].sign() == 1)

    creators = [old.creator(I4[:, i]) for i in range(4)]
    annihilators = [C.T for C in creators]
    mode_columns = [M.reshape(256, 1) for M in creators + annihilators]
    B = s.Matrix.hstack(*mode_columns)
    c0 = creators[0]
    transformed = (U * c0 * U.T).applyfunc(old.red)
    augmented = B.row_join(transformed.reshape(256, 1))

    # Exact row-rank elimination over the quotient field Q[a,p]/(a^2-p,p^2+p-1).
    # Pivot columns of M^T are coordinate rows of M and certify a square minor.
    def pivot_rows(M):
        A = [[old.red(M[r, c]) for r in range(M.rows)] for c in range(M.cols)]
        pivots: list[int] = []
        row = 0
        for col in range(M.rows):
            pivot = next((r for r in range(row, M.cols)
                          if not old.zero(A[r][col])), None)
            if pivot is None:
                continue
            A[row], A[pivot] = A[pivot], A[row]
            scale = A[row][col]
            A[row] = [old.red(x / scale) for x in A[row]]
            for r in range(M.cols):
                if r != row and not old.zero(A[r][col]):
                    scale = A[r][col]
                    A[r] = [old.red(A[r][j] - scale * A[row][j])
                            for j in range(M.rows)]
            pivots.append(col)
            row += 1
            if row == M.cols:
                break
        return pivots

    mode_rows = pivot_rows(B)
    augmented_rows = pivot_rows(augmented)
    need("four_creation_and_four_annihilation_modes_have_rank_8",
         len(mode_rows) == 8)
    need("conjugated_c0_increases_mode_span_rank_to_9",
         len(augmented_rows) == 9)
    need("rank_witness_rows_match_exact_receipt",
         augmented_rows == PINNED_9X9_ROWS)
    determinant = old.red(augmented.extract(augmented_rows, range(9)).det())
    need("exact_nonzero_minor_is_minus_a_p",
         old.zero(determinant + old.a * old.p)
         and not old.zero(determinant))
    native_p = (s.sqrt(5) - 1) / 2
    native_a = s.sqrt(native_p)
    need("minor_nonzero_from_owned_positive_golden_roots",
         native_p.is_positive is True and native_a.is_positive is True)

    return {
        "schema": "d0-native-record-nongaussian-link/1",
        "status": "PASS_FULL_RECORD_NOT_A_BOGOLIUBOV_CAR_LIFT",
        "exact_controls": len(checks),
        "checks": checks,
        "actual_transition": "first autonomous return from the owned whole-blank seed",
        "operator": "literal full16 CAR record U(I,e0)",
        "tested_mode_space": "span{c_0,...,c_3,c_0^T,...,c_3^T}",
        "mode_space_rank": len(mode_rows),
        "augmented_rank_after_Ad_U(c0)": len(augmented_rows),
        "flattening": "row-major 16x16 operator coordinates",
        "minor_row_indices_zero_based": augmented_rows,
        "minor_determinant": str(determinant),
        "nonzero_reason": "a>0 and p>0 with a^2=p and p+p^2=1",
        "scope": {
            "standard_car_mode_lift_exists_for_U0": False,
            "separate_native_D_variable_or_nonlinear_joint_law_excluded": False,
            "all_possible_record_to_link_maps_excluded": False,
            "physical_affine_shift_to_record_admission_proved": False,
            "metric_source_Ward_refinement_or_GR_closed": False,
            "new_supported_Lean_owner": False,
        },
        "input_sha256": {path: sha(path) for path in PINS},
        "proof_sha256": sha(PROOF),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    output = ROOT / (BASE + "_results.json")
    if args.write:
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        if json.loads(output.read_bytes()) != result:
            raise ArithmeticError("NON_GAUSSIAN_LINK_RECEIPT_MISMATCH")
    print("PASS_RECORD_NOT_BOGOLIUBOV controls=%d minor=%s" %
          (result["exact_controls"], result["minor_determinant"]))


if __name__ == "__main__":
    main()
