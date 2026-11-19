#!/usr/bin/env python3
"""Check typed source identities and replay the actual full128 operator family."""
import json
import math
import pathlib
import subprocess
import sys

p = (math.sqrt(5.0) - 1.0) / 2.0
checks = []


def req(condition, name):
    if not condition:
        raise ArithmeticError(name)
    checks.append(name)


# Original nonblank Kraus pairs have q0=p^2*x, q1=p*x. Their conditional
# Golden ratio is fixed, so its derivative is zero for every x, dx.
for x, dx in ((0.2, 0.3), (0.7, -0.4), (1.0, 1.0)):
    q0, q1 = p * p * x, p * x
    dq0, dq1 = p * p * dx, p * dx
    total, dtotal = q0 + q1, dq0 + dq1
    ratio0, ratio1 = q0 / total, q1 / total
    dratio0 = (dq0 * total - q0 * dtotal) / total**2
    dratio1 = (dq1 * total - q1 * dtotal) / total**2
    req(abs(ratio0 - p * p) < 2e-15 and abs(ratio1 - p) < 2e-15,
        f"fixed native conditional Golden pair x={x}")
    req(abs(dratio0) < 2e-15 and abs(dratio1) < 2e-15,
        f"zero conditional-pair source x={x}")

bad_pair = (-1.0, 1.0)
ratio_constraint_jet = bad_pair[0] - p * bad_pair[1]
req(abs(ratio_constraint_jet + 1.0 + p) < 2e-15,
    "withdrawn (-1,+1) direction violates the native ratio")

# Under complete amplitude binding, M=H/2-J and P=-J. The source gap is
# exactly H'/2 for arbitrary record and common-mode derivatives.
source_cases = []
for dH, dJ, dCbar in ((0.0, 0.0, 1.0), (0.7, -1.2, 0.4),
                      (-1.4, 0.3, 2.0), (math.sqrt(2), 2.0, -0.5)):
    dM, dP = 0.5 * dH - dJ, -dJ
    req(abs((dM - dP) - 0.5 * dH) < 2e-15,
        f"amplitude-bound source gap for dH={dH}, dJ={dJ}")
    dCQ = dCbar - dH
    dJ_mean = 1.5 * dH - dCbar
    dP_mean = -dJ_mean
    req(abs((dP_mean - dCQ) + 0.5 * dH) < 2e-15,
        f"mean-to-CQ pressure gap formula for dH={dH}")
    dJ_pressure = dH - dCbar
    dM_pressure = 0.5 * dH - dJ_pressure
    req(abs((dM_pressure - dCQ) - 0.5 * dH) < 2e-15,
        f"pressure-to-CQ mean gap formula for dH={dH}")
    source_cases.append({"dH": dH, "dJ": dJ, "dCbar": dCbar,
                         "dM_minus_dP": dM - dP,
                         "pressure_minus_CQ_if_mean_matches": dP_mean - dCQ,
                         "mean_minus_CQ_if_pressure_matches": dM_pressure - dCQ})

# Replay the independent exact-sign theorem on the actual 128 Kraus labels.
repo = pathlib.Path(__file__).resolve().parents[4]
native_checker = (repo / "02_REGISTRY/research/sources/"
                  "d0_variational_selection_synthesis_2026-10-21/"
                  "aggregation_audit/check_native_entropy_tangent.py")
replay = subprocess.run([sys.executable, str(native_checker)],
                        text=True, capture_output=True)
req(replay.returncode == 0, "actual full128 entropy-tangent replay exits 0")
native = json.loads(replay.stdout)
req(native["status"] == "PASS_LITERAL_NATIVE128_MEASURED_ENTROPY_TANGENT",
    "actual full128 entropy-tangent status")
req(native["check_count"] == 100, "actual full128 entropy-tangent controls")
nu_half = next(f for f in native["fixtures"] if f["nu"] == 0.5)
req(nu_half["positive_outcome_count"] == 42 and
    nu_half["dark_outcome_count"] == 86,
    "full128 fixture retains 42 positive and 86 dark outcomes")
req(nu_half["entropy_nu_derivative_exact_formula"] > 0,
    "positive numeric nu witness agrees with the strict analytic sign proof")
req(native["scope"]["physical_writer_or_controller_admission"] is False and
    native["scope"]["GR_closed"] is False,
    "nu-family witness is not physical admission or GR closure")

out = {
    "status": "PASS_TYPED_CANDIDATE_SOURCE_IDENTITIES",
    "check_count": len(checks),
    "checks": checks,
    "native_conditional_pair": {
        "q0": "p^2*x", "q1": "p*x", "conditional_derivative": [0, 0],
        "withdrawn_trial": list(bad_pair),
        "withdrawn_trial_ratio_constraint_derivative": ratio_constraint_jet,
    },
    "amplitude_binding": {
        "exact_identity": "D(mean)-D(pressure)=DH_phi/2",
        "sampled_derivatives": source_cases,
    },
    "actual_full128_operator_family": {
        "parameter": "nu",
        "nu": 0.5,
        "DH_phi_dnu": nu_half["entropy_nu_derivative_exact_formula"],
        "exact_sign_domain": "0<nu<sqrt(3)/2; see aggregation_audit/PROOF.md",
        "controller_admission": False,
        "physical_Book03_selection": False,
        "local_replay_runtime_warning_lines": len(replay.stderr.splitlines()),
    },
    "scope": {
        "old_pairwise_native_tangent_claim": False,
        "Book03_bootstrap_pullback_proved": False,
        "GR_closed": False,
    },
}
print(json.dumps(out, indent=2, sort_keys=True))
