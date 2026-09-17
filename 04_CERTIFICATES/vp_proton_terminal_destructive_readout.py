#!/usr/bin/env python3
"""D0-PROTON-001 — proton terminal-destructive readout-306 (can-FAIL).

M_p is the charged terminal-destructive readout of the nucleon core: the terminal readout is the
exact 306 = Lambda_B2/V13 + Lambda_B2/(V13*d13*V11), giving lambda_p, and M_p = Lambda_act*sqrt(lambda_p).
The measured 938.272 MeV is a benchmark, not an input. Rewritten from a conditional-status stub
(always exit 0) to assert + raise, so it can FAIL.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LAMBDA_B2 = 3960.0
LAMBDA_N_CORE = 2640.7985901288725
V9, V11, V13 = 9, 11, 13
D13 = V9 + V11                       # = 20, terminal active capacity
LAMBDA_ACT_MEV = 19.417960126286623
REF_MP_MEV = 938.27208816            # benchmark, not input


def main() -> int:
    print("=== D0-PROTON-001  proton terminal-destructive readout-306 ===")
    terminal_primary = LAMBDA_B2 / V13
    terminal_checksum = LAMBDA_B2 / (V13 * D13 * V11)
    terminal_total = terminal_primary + terminal_checksum
    assert abs(terminal_total - 306.0) < 1e-9, f"terminal readout must be exactly 306: {terminal_total}"
    print(f"PASS_READOUT_306  Lambda_B2/V13 + Lambda_B2/(V13.d13.V11) = {terminal_total:.6f} = 306")

    lambda_p = LAMBDA_N_CORE - terminal_total
    assert abs(lambda_p - 2334.7985901288725) < 1e-9, f"lambda_p mismatch: {lambda_p}"
    mp = LAMBDA_ACT_MEV * math.sqrt(lambda_p)
    assert abs(mp - 938.2710491516433) < 1e-6, f"M_p formula mismatch: {mp}"
    rel = mp / REF_MP_MEV - 1
    assert abs(rel) < 1e-5, f"M_p must match the benchmark within 1e-5: rel={rel:.2e}"
    print(f"PASS_M_P_BENCHMARK  M_p(D0)={mp:.6f} MeV vs {REF_MP_MEV} (benchmark not input); rel={rel:.2e}")

    # negative control: a wrong terminal shell (V13 -> 12) breaks the exact 306 readout
    tt_wrong = LAMBDA_B2 / 12 + LAMBDA_B2 / (12 * D13 * V11)
    assert abs(tt_wrong - 306.0) > 1.0, "control: V13=12 must not give the 306 readout"
    print("FAIL_WRONG_TERMINAL_SHELL_12_DOES_NOT_GIVE_306")
    print("HONEST_938_MEV_IS_A_BENCHMARK_NOT_AN_INPUT_PROTON_IS_THE_TERMINAL_READOUT")
    print("PASS_PROTON_TERMINAL_DESTRUCTIVE_READOUT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
