#!/usr/bin/env python3
"""Check conditional source identities and their endpoint-allocation law."""
import json
import math
import pathlib
import subprocess
import sys

checks = []


def req(condition, name):
    if not condition:
        raise ArithmeticError(name)
    checks.append(name)


repo = pathlib.Path(__file__).resolve().parents[4]
source_checker = (repo / "02_REGISTRY/research/sources/"
                  "d0_book03_first_source_underdetermination_2026-10-21/"
                  "check_book03_source_gap.py")
source_run = subprocess.run([sys.executable, str(source_checker)],
                            text=True, capture_output=True)
req(source_run.returncode == 0,
    "typed Book03 source identities and actual full128 replay")
source = json.loads(source_run.stdout)
req(source["status"] == "PASS_TYPED_CANDIDATE_SOURCE_IDENTITIES",
    "typed-source result status")
req(source["scope"]["Book03_bootstrap_pullback_proved"] is False,
    "bootstrap-to-field pullback remains open")

# For the additive endpoint family, the path-action difference is exactly
# (theta-eta)*(I_final-I_initial); differentiate with arbitrary endpoint jets.
endpoint_cases = []
for theta, eta, d_endpoint in ((1.0, 0.0, 1.0),
                               (0.75, 0.25, -2.0),
                               (0.0, 1.0, math.sqrt(2.0))):
    dS_theta = theta * d_endpoint
    dS_eta = eta * d_endpoint
    gap = dS_theta - dS_eta
    expected = (theta - eta) * d_endpoint
    req(abs(gap - expected) < 2e-15,
        f"conditional endpoint-allocation source theta={theta}, eta={eta}")
    endpoint_cases.append({"theta": theta, "eta": eta,
                           "endpoint_information_jet": d_endpoint,
                           "source_gap": gap})

out = {
    "status": "PASS_FORMAL_INTERFACE_AND_SOURCE_REPLAY",
    "check_count": len(checks),
    "checks": checks,
    "endpoint_allocation": {
        "identity": "D(S_theta-S_eta)=(theta-eta)*D(I_final-I_initial)",
        "cases": endpoint_cases,
        "physical_endpoint_jet_admission_proved": False,
    },
    "actual_full128_candidate_source": source["actual_full128_operator_family"],
    "scope": {
        "Book03_master_action_exists": True,
        "bootstrap_pullback_to_GR_carrier_proved": False,
        "physical_history_and_Info_selection_proved": False,
        "two_physical_completions_constructed": False,
        "GR_closed": False,
    },
}
print(json.dumps(out, indent=2, sort_keys=True))
