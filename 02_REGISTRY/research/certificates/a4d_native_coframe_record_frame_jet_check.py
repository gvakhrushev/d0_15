#!/usr/bin/env python3
"""Exact first-jet boundary for a native CAR record in its moving frame.

The result is carrier-level. It does not declare the composed instrument
physically admitted or infer a stress tensor.
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
STEM = "a4d_native_coframe_record_frame_jet"
PROOF = "02_REGISTRY/research/A4D_NATIVE_COFRAME_RECORD_FRAME_JET_BOUNDARY.md"
CHRONOLOGY = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
CHRONOLOGY_CERT = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json"
INPUTS = {
    "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py": "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
    "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json": "0b91e13d823568898a006dd468f9963ffbbc1949f0976a21e8530af465ecfbbe",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py": "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json": "8cba34862bf6af48c8c49d75c5e3a5a2a80948f9f0bf2e1818c42f43b370a238",
    "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_results.json": "4c28dd449b844e5a8332d56d457c2bbcd83853069563542dc12f0238439510a8",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean": "5dc96be9c2ee5c874a617f3ebe80f0da9803973c1656112fe24f31e90c2f5eb1",
    "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean": "69e7a9a0290ee08c748db03c62d5e331e23efdeb84fb6ffefe4165267b14c967",
}


def sha(path: str | Path) -> str:
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    return hashlib.sha256(target.read_bytes()).hexdigest()


def load_chronology():
    path = ROOT / CHRONOLOGY
    spec = importlib.util.spec_from_file_location("d0_native_record_chronology_owner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("NATIVE_RECORD_CHRONOLOGY_OWNER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run() -> dict:
    for path, expected in INPUTS.items():
        actual = sha(path)
        if expected and actual != expected:
            raise AssertionError(f"INPUT_PIN_MISMATCH:{path}:{actual}")

    chronology_cert = json.loads((ROOT / CHRONOLOGY_CERT).read_text())
    if chronology_cert.get("status") != "PASS" or chronology_cert.get("full_native_fibre") != 16:
        raise AssertionError("NATIVE_RECORD_CHRONOLOGY_RECEIPT_NOT_PASS")
    for path, expected in chronology_cert["input_sha256"].items():
        if sha(path) != expected:
            raise AssertionError(f"CHRONOLOGY_TRANSITIVE_PIN_MISMATCH:{path}")
    fock_receipt_path = "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_results.json"
    fock_receipt = json.loads((ROOT / fock_receipt_path).read_text())
    fock_certificate_path = "02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json"
    fock_certificate = json.loads((ROOT / fock_certificate_path).read_text())
    if (fock_receipt.get("status") != "PASS" or fock_receipt.get("compiler_exit_code") != 0
            or fock_certificate.get("status") != "PASS" or fock_certificate.get("exact_controls") != 169):
        raise AssertionError("NATIVE_FOCK_RECORD_RECEIPT_NOT_PASS")

    owner = load_chronology()
    old = owner.old
    record = owner.record
    dcompound = owner.dcompound
    red = owner.red
    zero = old.zero
    eye4 = s.eye(4)
    eye16 = s.eye(16)
    G = eye4
    observers = [eye4[:, r] for r in range(4)]
    returns = [record(G, n)[0] for n in observers]

    checks: list[str] = []
    negatives: list[str] = []

    def check(name: str, condition: bool) -> None:
        if not bool(condition):
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    def reject(name: str, false_claim: bool) -> None:
        check("REJECT_" + name, false_claim)
        negatives.append(name)

    check("FOUR_FULL_FOCK_RETURNS_ARE_REAL_ORTHOGONAL",
          all(zero(U.T * U - eye16) for U in returns))
    noncommuting_pairs = [
        (i, j) for i in range(4) for j in range(i)
        if not zero(returns[i] * returns[j] - returns[j] * returns[i])
    ]
    check("REFERENCE_RETURNS_INCLUDE_NONCOMMUTING_PAIR", bool(noncommuting_pairs))

    directions: list[s.Matrix] = []
    labels: list[str] = []
    for i in range(4):
        for j in range(i, 4):
            V = s.zeros(4)
            V[i, j] = V[j, i] = 1
            directions.append(V)
            labels.append(f"{i}{j}")

    zero_jets = 0
    first_nonzero_raw = None
    first_nonzero_wrong_sign = None
    for label, V in zip(labels, directions):
        dS = dcompound(G, V)
        dE = dcompound(eye4, -V / 2)
        check(f"FRAME_ISOMETRY_JET_{label}", zero(dE + dS / 2)
              and zero(dE.T + dS + dE))
        for r, (n, U) in enumerate(zip(observers, returns)):
            _, _, dU, _ = record(G, n, V, -V * n / 2)
            moving_isometry = dU.T * U + U.T * dS * U + U.T * dU - dS
            check(f"MOVING_PAIRING_RECORD_JET_{label}_{r}", zero(moving_isometry))
            fixed_jet = dU + (dS * U - U * dS) / 2
            check(f"FIXED_FRAME_RETURN_JET_ZERO_{label}_{r}", zero(fixed_jet))
            zero_jets += 1
            if first_nonzero_raw is None and not zero(dU):
                first_nonzero_raw = dU
            wrong_sign = dU - (dS * U - U * dS) / 2
            if first_nonzero_wrong_sign is None and not zero(wrong_sign):
                first_nonzero_wrong_sign = wrong_sign

    check("ALL_40_SYMMETRIC_METRIC_RETURN_JETS_CLASSIFIED", zero_jets == 40)
    reject("FREEZE_THE_MOVING_PAIRING", first_nonzero_raw is not None)
    reject("REVERSE_THE_FRAME_ISOMETRY_SIGN", first_nonzero_wrong_sign is not None)

    # With every fixed-frame return jet zero, both the return-derived kinetic
    # operator and every channel branch have zero first variation.
    for V in directions:
        dS = dcompound(G, V)
        fixed_jets = []
        for n, U in zip(observers, returns):
            _, _, dU, _ = record(G, n, V, -V * n / 2)
            fixed_jets.append(dU + (dS * U - U * dS) / 2)
        delta_jet = sum((dU.T * (U - eye16) + (U - eye16).T * dU
                         for dU, U in zip(fixed_jets, returns)), s.zeros(16))
        check("RETURN_COST_METRIC_JET_ZERO_" + labels[directions.index(V)], zero(delta_jet))

    n0 = observers[0]
    relative_dn = observers[1]
    _, _, relative_jet, _ = record(G, n0, s.zeros(4), relative_dn)
    check("RELATIVE_OBSERVER_TANGENT_IS_NORMALIZED", (n0.T * G * relative_dn)[0] == 0)
    check("RELATIVE_OBSERVER_JET_IS_UNITARY_TANGENT",
          zero(relative_jet.T * returns[0] + returns[0].T * relative_jet))
    reject("RELATIVE_OBSERVER_JET_IS_NOT_AUTOMATICALLY_ZERO", not zero(relative_jet))

    return {
        "schema": "d0-native-coframe-record-frame-jet/1",
        "status": "PASS_PURE_FRAME_METRIC_JETS_NULL_RELATIVE_OBSERVER_OPEN",
        "input_sha256": {path: sha(path) for path in INPUTS},
        "proof_sha256": sha(PROOF),
        "checker_sha256": sha(Path(__file__)),
        "reference": {
            "pairing": "G=I_4",
            "observer_frame": "n_r=e_r, r=0..3",
            "record_carrier_dimension": 16,
            "return_family": "actual full-Fock record(G,n_r)",
            "noncommuting_reference_pairs": noncommuting_pairs,
        },
        "metric_tangent_basis": labels,
        "fixed_frame": "E=ext(A), A(t)=I-tV/2, G(t)=A(t)^(-T)A(t)^(-1)",
        "fixed_frame_jet": "dU + (dS*U-U*dS)/2 = 0 for all 40 return/tangent pairs",
        "exact_controls": len(checks),
        "checks": checks,
        "negative_controls": negatives,
        "scope": {
            "candidate_native_record_to_instrument_composition_tested": True,
            "physical_admission_of_four_return_identification": False,
            "pure_common_frame_metric_source_for_return_derived_cost": "ZERO_FIRST_JET",
            "relative_observer_or_matter_source": "OPEN_NONZERO_OPERATOR_JET_WITNESS_ONLY",
            "v3_commuting_reference_derivative_theorem_used": False,
            "local_coframe_field_or_link_map_constructed": False,
            "native_source_Ward_or_Einstein_tensor_derived": False,
            "new_Lean_declarations": 0,
            "G0_closed": False,
            "positive_GR_or_original_terminals_closed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    destination = ROOT / "02_REGISTRY/research/certificates" / f"{STEM}_results.json"
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        destination.write_text(encoded)
    elif not destination.exists() or destination.read_text() != encoded:
        raise AssertionError("IMMUTABLE_RECEIPT_MISMATCH; use --write only after reviewing the exact result")
    print(f"PASS_NATIVE_COFRAME_RECORD_FRAME_JET controls={result['exact_controls']} fixed_frame_jets=40")
    print("pure common-frame metric source is zero; relative observer/matter response remains open")


if __name__ == "__main__":
    main()
