#!/usr/bin/env python3
"""D0-NEUTRON-002 — neutron lifetime beta/archive unlock-rate closure (can-FAIL).

tau_n is built from the closed D0 primitives (lambda_p, lambda_n, Lambda_act, delta0, q_mass,
the electron full-cycle rest slot 1/38); the measured neutron lifetime is a benchmark, not an
input. Rewritten from a print-stub (hardcoded PASS) to assert the structural chain + the
benchmark agreement, so it can FAIL.

  beta window:   epsilon_beta = sqrt(lambda_n) - sqrt(lambda_p) - 1/38
  rate:          Gamma_n * tau0 = epsilon_beta^5 * delta0^19 * q_mass^14,   q_mass = 1/(1+delta0^3)
  lifetime:      tau_n = tau0 / (Gamma_n * tau0)
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + math.sqrt(5)) / 2
delta0 = (math.sqrt(5) - 2) / 2
LAMBDA_P = 2334.7985901288725
LAMBDA_N = 2341.241179437959
LAMBDA_ACT_MEV = 19.417960126286623
TAU0_S = 2.129815732459607e-22
TAU_N_REF_S = 878.4               # CODATA-class benchmark (s), not input
WEAK_UNLOCK_DEPTH = 19
TERMINAL_SLOT = 14


def main() -> int:
    print("=== D0-NEUTRON-002  neutron lifetime beta/archive unlock rate ===")
    rest_slot = 1.0 / 38
    q_mass = 1.0 / (1 + delta0 ** 3)

    eps = math.sqrt(LAMBDA_N) - math.sqrt(LAMBDA_P) - rest_slot
    assert eps > 0, "the beta window epsilon_beta must be positive"
    Q = LAMBDA_ACT_MEV * eps
    assert 0.7 < Q < 0.85, f"Q_beta = Lambda_act*eps must be in the beta band: {Q}"
    print(f"PASS_BETA_WINDOW  eps_beta = sqrt(ln)-sqrt(lp)-1/38 = {eps:.6f}; Q_beta = {Q:.6f} MeV")

    gamma_tau0 = eps ** 5 * delta0 ** WEAK_UNLOCK_DEPTH * q_mass ** TERMINAL_SLOT
    tau_n = TAU0_S / gamma_tau0
    assert tau_n > 0, "tau_n must be positive"
    rel = tau_n / TAU_N_REF_S - 1
    assert abs(rel) < 2e-3, f"tau_n must match the benchmark within 0.2%: {tau_n:.2f}s rel={rel:.2e}"
    print(f"PASS_TAU_N_BENCHMARK  tau_n(D0) = {tau_n:.2f} s vs ~{TAU_N_REF_S} s (benchmark not input); rel={rel:.2e}")

    # negative control: a wrong unlock depth (delta0^18 instead of ^19) misses by a factor 1/delta0
    tau_wrong = TAU0_S / (eps ** 5 * delta0 ** 18 * q_mass ** TERMINAL_SLOT)
    assert abs(tau_wrong / TAU_N_REF_S - 1) > 0.5, "control: delta0^18 depth must miss the lifetime"
    print("FAIL_WRONG_UNLOCK_DEPTH_18_MISSES_THE_LIFETIME")
    print("HONEST_NEUTRON_LIFETIME_IS_A_BENCHMARK_NOT_AN_INPUT_DOWNSTREAM_OF_CLOSED_PRIMITIVES")
    print("PASS_NEUTRON_LIFETIME_BETA_ARCHIVE_UNLOCK_RATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
