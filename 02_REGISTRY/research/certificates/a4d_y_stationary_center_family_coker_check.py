#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Exact parameter-family check for the curved stationary Y cokernel."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

import a4d_y_curved_normaljet_degree2_obstruction_check as owner

RESULT_PATH = Path(__file__).with_name("a4d_y_stationary_center_family_coker_results.json")


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def run(write: bool = False) -> dict:
    result = owner.run(
        write=False,
        first_center_shift=sp.Symbol("s"),
        joint_coker_family=True,
    )
    expected = {
        "schema": "a4d-y-stationary-center-family-coker-v1",
        "first_order_y_center_parameter": "s",
        "stationary_connection_coker_C2": [
            "351402359/2108160",
            "21506403637/154949760",
        ],
        "joint_phase_common_xi3_squared_witness_pairing": "-22209",
        "exact_parameter_dependence": "both outputs are independent of s",
        "scope": "normalized surviving Y-curvature germ at z=1; exact order-delta^2 normal jet; phase-common metric readout and arbitrary degree-three center corrections",
        "nonclaim": "does not rule out spatially varying center corrections, other curvature germs, h-dependent nonanalytic branches, or establish the global response theorem",
    }
    check("PARAMETRIC_CONNECTION_COKER_MATCHES", result["stationary_connection_coker"] ==
          expected["stationary_connection_coker_C2"])
    check("PARAMETRIC_JOINT_WITNESS_MATCHES", result["joint_phase_common_witness"] ==
          expected["joint_phase_common_xi3_squared_witness_pairing"])
    if write:
        RESULT_PATH.write_text(json.dumps(expected, indent=2) + "\n")
        print("WROTE", RESULT_PATH, flush=True)
    else:
        check("RESULTS_MATCH_PINNED_JSON", expected == json.loads(RESULT_PATH.read_text()))
    print("TERMINAL A4D-Y-STATIONARY-CENTER-C2-INVARIANT-UNDER-CONSTANT-RETUNING", flush=True)
    return expected


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
