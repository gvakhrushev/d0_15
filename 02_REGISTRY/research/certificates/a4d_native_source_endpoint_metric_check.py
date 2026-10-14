#!/usr/bin/env python3
"""Exact endpoint-metric test on the AF/CAR-welded blank source orbit.

This checks one proposed direct join: retain the owned CAR record gate, read
the positive observer pairing from the correlated CAR current at each end,
and require the full exterior Gram to be transported isometrically. A single
exact scalar-column defect rejects that join; no other joint link/gate update
is classified here.
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
BASE = "f1270f63cffa5fcfc27b469ff2517d8398d5362a"
INPUTS = {
    "a4d_native_reference_memory_preparation.py": "67e416c75cc213efca6040cea8cb796efbcff78037e09b31fb6a83acdcfd0e3a",
    "a4d_native_correlated_current_transition.py": "e659733a8ab4fea30f46de56663dc344249420c7e0a3ea65b2aa1a2091b76e0d",
    "a4d_native_record_metric_chronology_check.py": "16929d026206ee69e126484ed2ac7b1dfd2537c1e50c0fc4c4293408caf58527",
}


def load(stem: str):
    path = CERT / (stem + ".py")
    spec = importlib.util.spec_from_file_location(stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"CANNOT_LOAD_PINNED_OWNER:{stem}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


P = load("a4d_native_reference_memory_preparation")
O = load("a4d_native_correlated_current_transition")
C = load("a4d_native_record_metric_chronology_check")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict:
    for name, expected in INPUTS.items():
        actual = digest(CERT / name)
        if actual != expected:
            raise AssertionError(f"PIN_MISMATCH:{name}:{actual}")

    a, p = P.a, P.p
    eta = s.diag(1, -1, -1, -1)
    I4, I16 = s.eye(4), s.eye(16)
    blank = O.blank_code()
    m0 = P.mat(blank * s.Matrix([a, p]))
    U, _, blank_projector = P.full_tuple()
    U = P.mat(U)
    m1 = P.mat(U * m0)

    def require(name: str, proposition: bool, checks: list[str]) -> None:
        if not proposition:
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    checks: list[str] = []
    require("actual_full_blank_projector", P.mat(blank_projector * m0 - m0) == s.zeros(16, 1), checks)
    require("unit_norm_blank_state", P.red((m0.T * m0)[0] - 1) == 0, checks)
    require("literal_gate_isometry_at_initial_pairing", P.mat(U.T * U - I16) == s.zeros(16), checks)

    J0 = P.mat(O.current(I4, m0))
    J1 = P.mat(O.current(I4, m1))
    j1_expected = s.Matrix([1, 2 * a * p, 0, 0])
    require("blank_correlated_current_is_rest", J0 == s.Matrix([1, 0, 0, 0]), checks)
    require("one_literal_tick_gives_owned_source_current", P.mat(J1 - j1_expected) == s.zeros(4, 1), checks)

    h0 = P.mat(O.observer_pairing(eta, J0))
    h1 = P.mat(O.observer_pairing(eta, J1))
    jnorm = P.red((J1.T * eta * J1)[0])
    h1_expected = s.Matrix(
        [
            [2 / p**6 - 1, -4 * a * p / p**6, 0, 0],
            [-4 * a * p / p**6, 2 / p**6 - 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    require("source_current_timelike_norm_is_p6", P.red(jnorm - p**6) == 0, checks)
    require("source_pairing_exact_full_matrix", P.mat(h1 - h1_expected) == s.zeros(4), checks)
    require("initial_pairing_is_identity", h0 == I4, checks)
    require(
        "source_pairing_is_positive",
        P.red(h1[0, 0] - 1 - 8 / p**3) == 0
        and P.red(h1[:2, :2].det() - 1) == 0,
        checks,
    )

    W0 = P.mat(C.ext(h0))
    W1 = P.mat(C.ext(h1))
    require("initial_full_exterior_gram_is_identity", W0 == I16, checks)
    e_scalar = I16[:, 0]
    u_scalar = P.mat(U * e_scalar)
    require("literal_gate_scalar_column", u_scalar == a * I16[:, 0] + p * I16[:, 1], checks)
    defect = P.red((u_scalar.T * W1 * u_scalar)[0] - (e_scalar.T * W0 * e_scalar)[0])
    expected_defect = P.red(8 / p)
    require("exact_endpoint_norm_defect_is_8_over_p", P.red(defect - expected_defect) == 0, checks)
    require("defect_is_strictly_positive", P.red(expected_defect - 8 - 8 * p) == 0, checks)
    require("full_endpoint_isometry_fails", P.red(defect) != 0, checks)

    frozen_defect = P.mat(U.T * W0 * U - W0)
    require("frozen_pairing_control_has_zero_defect", frozen_defect == s.zeros(16), checks)
    reverse = s.Matrix([1, -2 * a * p, 0, 0])
    h_reverse = P.mat(O.observer_pairing(eta, reverse))
    reverse_defect = P.red((u_scalar.T * P.mat(C.ext(h_reverse)) * u_scalar)[0] - 1)
    require("opposite_current_has_same_positive_scalar_defect", P.red(reverse_defect - expected_defect) == 0, checks)

    return {
        "schema": "d0-native-source-endpoint-metric/1",
        "status": "PASS",
        "input_source_head": BASE,
        "input_sha256": INPUTS,
        "checks": checks,
        "exact_controls": len(checks),
        "witness": {
            "initial_current": "(1,0,0,0)",
            "one_tick_current": "(1,2*a*p,0,0)",
            "current_norm_squared": "p^6",
            "source_pairing_00": "2/p^6-1",
            "scalar_column_endpoint_norm_defect": "8/p=8*(1+p)>0",
        },
        "scope": "fixed rest frame, literal owned full-CAR gate, current-defined positive observer pairing",
        "other_joint_link_or_gate_updates_classified": False,
        "physical_admission": False,
        "full_native_q_D_b_m_transition": False,
        "source_Ward_stationarity_GR_closed": False,
        "new_Lean_compilation": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    result["checker_sha256"] = digest(Path(__file__))
    output = CERT / "a4d_native_source_endpoint_metric_results.json"
    if args.write:
        output.write_text(json.dumps(result, indent=2) + "\n")
    elif json.loads(output.read_text()) != result:
        raise AssertionError("IMMUTABLE_RECEIPT_MISMATCH")
    print("PASS_NATIVE_SOURCE_ENDPOINT_METRIC", result["exact_controls"], "exact controls")
    print("SCOPED_OBSTRUCTION: direct current-pairing identification fails endpoint isometry")
    print("PHYSICAL_ADMISSION_AND_OTHER_JOINT_UPDATES_OPEN")


if __name__ == "__main__":
    main()
