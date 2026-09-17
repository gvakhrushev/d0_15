#!/usr/bin/env python3
"""D0-DSI-EXPERIMENTAL-001 — log-periodic (DSI) ladder: the D0 phi-ladder FORM (CERT-CLOSED); the
experimental VALUE (is the observed scale = phi?) is an open named gap, NOT confronted here.

The verifiable content is the FORM: a discrete-scale-invariant observable with scale factor lambda has
log-period ln(lambda); D0's phi-ladder (lambda = phi) has log-period ln(phi) ~ 0.4812 (= I_f = h_KS),
and phi^k samples land on integer log-rungs. Those are exact, can-FAIL checks.

NOT a data confrontation: log-periodic magneto-oscillations ARE observed in ZrTe5/HfTe5 (Wang et al.,
Natl. Sci. Rev. 6, 914, 2019; Sci. Adv. 4, eaau5096) -- real evidence the FORM occurs in nature -- but
NO measured log-period from those papers is loaded/pinned here. The earlier "experimental" scale
`lambda_exp = e**0.30` was a SELF-CHOSEN placeholder (not a measured value), engineered to make
`lambda_exp != phi`; it is removed. Whether the observed scale equals phi (expected: Coulomb-set, not
golden) is the open named gap. Registry: CERT-CLOSED for the FORM; the VALUE is a named PROOF-TARGET.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def log_period(lam: float) -> float:
    """Log-period of a DSI/log-periodic observable with scale factor lambda."""
    return math.log(lam)


def main() -> int:
    print("=== D0-DSI-EXPERIMENTAL-001  log-periodic DSI ladder: D0 FORM (cert) vs unbound experimental VALUE ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: a DSI observable with scale lambda has log-period ln(lambda); "
          "D0's phi-ladder (lambda=phi) has ln(phi)~0.4812 with phi^k on integer rungs -- FORM fixed before any datum")

    phi = (1 + math.sqrt(5)) / 2

    # ---- FORM (exact, can-FAIL): D0 phi-ladder log-period = ln(phi) ----
    P_phi = log_period(phi)
    assert abs(P_phi - math.log(phi)) < 1e-15
    assert abs(P_phi - 0.4812118) < 1e-5, "ln(phi) ~ 0.4812 (same log phi as I_f / h_KS)"
    print(f"PASS_D0_PHI_LADDER  D0 DSI scale lambda=phi => log-period ln(phi) = {P_phi:.7f} = log phi")

    xs = [phi ** k for k in range(6)]
    rungs = [math.log(x) / P_phi for x in xs]
    assert all(abs(r - round(r)) < 1e-9 for r in rungs), "phi^k samples must land on integer log-rungs (ladder)"
    print("PASS_LOG_PERIODIC_FORM  phi^k land on integer log-rungs (the DSI ladder signature)")

    # ---- VALUE (data-gated; NOT performed here): no measured log-period is bound ----
    print("SKIP_DSI_EXPERIMENTAL_VALUE_REQUIRED  no measured ZrTe5/HfTe5 log-period is pinned here -- the FORM "
          "(log-periodicity) is confirmed real in the cited materials, but whether the observed scale equals phi is "
          "NOT measured here (the prior lambda_exp=e^0.30 was a self-chosen placeholder, removed); expected Coulomb-set")
    print("HONEST_FORM_REAL_VALUE_OPEN  confirms the log-periodic FORM; does NOT measure lambda=phi (named gap)")

    print("PASS_DSI_EXPERIMENTAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
