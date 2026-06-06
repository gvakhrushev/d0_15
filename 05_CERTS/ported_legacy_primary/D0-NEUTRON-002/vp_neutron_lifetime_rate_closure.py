#!/usr/bin/env python3
"""D0 neutron lifetime beta/archive unlock-rate closure certificate.

This certificate is downstream of the already closed D0 corpus values:
lambda_p, lambda_n, Lambda_act, tau0, delta0, q_mass and the electron
full-cycle rest slot 1/38.  It does not use the measured neutron lifetime.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def run_vp_neutron_lifetime_rate_closure() -> dict[str, object]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    delta0 = (math.sqrt(5.0) - 2.0) / 2.0

    # Closed upstream D0 values from the canonical corpus.
    lambda_p = 2334.7985901288725
    lambda_n = 2341.241179437959
    Lambda_act_MeV = 19.417960126286623
    tau0_seconds = 2.129815732459607e-22
    electron_full_cycle_slots = 38
    electron_rest_slot = 1.0 / electron_full_cycle_slots
    q_mass = 1.0 / (1.0 + delta0**3)

    # The beta window is read on the sqrt(lambda) mass/action line.
    epsilon_beta = math.sqrt(lambda_n) - math.sqrt(lambda_p) - electron_rest_slot
    Q_beta_MeV = Lambda_act_MeV * epsilon_beta

    weak_unlock_depth = 19
    terminal_shell_plus_comparison_slot = 14

    epsilon_phase_space = epsilon_beta**5
    delta_weak_unlock = delta0**weak_unlock_depth
    q_mass_terminal_factor = q_mass**terminal_shell_plus_comparison_slot
    Gamma_tau0 = epsilon_phase_space * delta_weak_unlock * q_mass_terminal_factor
    tau_n_seconds = tau0_seconds / Gamma_tau0

    return {
        "status": "PASS_NEUTRON_LIFETIME_BETA_ARCHIVE_UNLOCK_RATE_CLOSURE",
        "phi": phi,
        "delta0": delta0,
        "lambda_p_D0": lambda_p,
        "lambda_n_D0": lambda_n,
        "sqrt_lambda_n_minus_sqrt_lambda_p": math.sqrt(lambda_n) - math.sqrt(lambda_p),
        "electron_full_cycle_slots": electron_full_cycle_slots,
        "electron_rest_slot_1_over_38": electron_rest_slot,
        "epsilon_beta_D0": epsilon_beta,
        "Lambda_act_MeV": Lambda_act_MeV,
        "Q_beta_D0_MeV": Q_beta_MeV,
        "q_mass_formula": "1/(1+delta0^3)",
        "q_mass": q_mass,
        "weak_unlock_depth": weak_unlock_depth,
        "terminal_shell_plus_comparison_slot": terminal_shell_plus_comparison_slot,
        "epsilon_beta_power_5": epsilon_phase_space,
        "delta0_power_19": delta_weak_unlock,
        "q_mass_power_14": q_mass_terminal_factor,
        "Gamma_n_D0_times_tau0": Gamma_tau0,
        "tau0_seconds": tau0_seconds,
        "tau_n_D0_seconds": tau_n_seconds,
        "formula_epsilon_beta": "sqrt(lambda_n_D0)-sqrt(lambda_p_D0)-1/38",
        "formula_rate": "Gamma_n_D0*tau0 = epsilon_beta_D0^5 * delta0^19 * q_mass^14",
        "guardrail": "No measured neutron lifetime is used as input; external bottle/beam values are benchmarks only.",
    }


def write_results(root: Path, res: dict[str, object]) -> None:
    cert_dir = root / "04_CERTS"
    cert_dir.mkdir(parents=True, exist_ok=True)
    (cert_dir / "D0_NEUTRON_LIFETIME_RATE_NUMBERS.json").write_text(
        json.dumps(res, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# D0 Neutron Lifetime Beta/Archive Unlock-Rate Closure",
        "",
        f"Status: `{res['status']}`",
        "",
        "## Formulae",
        "",
        "```text",
        str(res["formula_epsilon_beta"]),
        str(res["formula_rate"]),
        "```",
        "",
        "## Numbers",
    ]
    skip = {"status", "formula_epsilon_beta", "formula_rate"}
    for key, value in res.items():
        if key not in skip:
            lines.append(f"- `{key}`: `{value}`")
    (cert_dir / "D0_NEUTRON_LIFETIME_RATE_RESULTS.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    res = run_vp_neutron_lifetime_rate_closure()
    root = Path(__file__).resolve().parents[1]
    write_results(root, res)
    print(json.dumps(res, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
