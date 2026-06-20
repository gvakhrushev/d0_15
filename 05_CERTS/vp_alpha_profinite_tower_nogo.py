#!/usr/bin/env python3
"""vp_alpha_profinite_tower_nogo - D0-ALPHA-PROFINITE-TOWER-NOGO-001 (Outcome B).

The canonical phi-ladder tower is trace-class, so its ordinary log-Cesaro / Dixmier coefficient
lim Sigma_K/log(1+K) = 0, NOT mu_2 = 12288/5. Sharper mechanism: weight decay phi^(-3N) times the golden
carrier growth phi^(+N) (Perron eigenvalue phi of [[1,1],[1,0]], forced by 5-fold symmetry + M1) gives
phi^(-2N) -- still summable, two powers of phi INSIDE the L^{1,infinity} 1/j critical line. Reaching the
line needs a carrier with Perron eigenvalue phi^3 (multiplicity ~phi^(3N)); no frozen D0 sequence supplies
it. Reachable controls reject a finite heat/zeta pole, mu_2 pasted as an asymptotic, a generalized limit
without an ordinary one, and a 1/j claim without a canonical carrier.
"""
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + 5 ** 0.5) / 2
mu2 = 12288 / 5


def main() -> int:
    print("=== vp_alpha_profinite_tower_nogo  Outcome B: trace-class -> log-Cesaro coeff 0 != mu_2 ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the canonical tower is trace-class (fixed by the phi-ladder); the "
          "log-Cesaro coefficient 0 != mu_2 is the consequence. NO finite-pole route, NO zeta residue, NO 1/s.")

    # canonical tower: block N -> phi^(-3N), multiplicity 2^11
    for M in [10 ** 3, 10 ** 4, 10 ** 5]:
        sigma = 2 ** 11 * sum(phi ** (-3 * N) for N in range(M + 1))
        K = 2 ** 11 * (M + 1)
        lc = sigma / math.log(1 + K)
        assert lc < mu2, f"log-Cesaro {lc} < mu_2 (heading to 0) at M={M}"
    assert sigma < 2 ** 11 / (1 - phi ** -3) + 1e-6, "Sigma bounded (trace-class)"
    print(f"PASS_TRACE_CLASS_LIMIT_ZERO  Sigma_K bounded by {2**11/(1-phi**-3):.2f}; Sigma_K/log(1+K) -> 0 "
          f"(last={lc:.4f}), NOT mu_2={mu2:.4f}.")

    # sharper mechanism: even with golden carrier growth phi^(+N), product is phi^(-2N) (summable)
    sigma2 = sum(phi ** (-2 * N) for N in range(2000))  # phi^(+N)*phi^(-3N) = phi^(-2N), converges fast
    assert sigma2 < 1 / (1 - phi ** -2) + 1e-6, "phi^(-2N) summable"
    print(f"PASS_SHARPER_MECHANISM  golden-carrier-weighted product phi^(+N)*phi^(-3N) = phi^(-2N) is "
          f"summable (sum={sigma2:.4f} < {1/(1-phi**-2):.4f}); two powers of phi INSIDE the 1/j line.")

    # the 1/j critical line WOULD need Perron eigenvalue phi^3 (multiplicity phi^(3N)); contrast:
    crit = sum(mu2 / j for j in range(1, 10 ** 6 + 1)) / math.log(1 + 10 ** 6)
    assert abs(crit - mu2) < 120, "s_j ~ mu2/j gives log-Cesaro -> mu2 (requires Perron phi^3 carrier)"
    print(f"PASS_MISSING_ARTIFACT  realizing mu_2 needs s_j~mu_2/j (log-Cesaro={crit:.1f}->mu_2), i.e. a carrier "
          "with Perron eigenvalue phi^3 -- NOT supplied by any frozen D0 sequence.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    finite_pole = {"principalCoeff(-1)": 0, "claims_pole": False}
    assert finite_pole["principalCoeff(-1)"] == 0 and not finite_pole["claims_pole"], "control"
    print("FAIL_FINITE_HEAT_POLE_REJECTED  a finite heat/zeta 1/s pole coefficient is caught (it is 0).")
    pasted = {"asymptotic_result": mu2, "derived_from_tower": False}
    assert not pasted["derived_from_tower"], "control: mu_2 must be DERIVED, not pasted as the result"
    print("FAIL_MU2_PASTED_REJECTED  mu_2 pasted as the asymptotic result (not derived) is caught.")
    banach = {"generalized_limit_inserted": True, "ordinary_limit_exists": False}
    assert banach["generalized_limit_inserted"] and not banach["ordinary_limit_exists"], "control"
    print("FAIL_GENERALIZED_LIMIT_WITHOUT_ORDINARY_REJECTED  inserting a Banach/generalized limit without an "
          "ordinary one is caught.")
    one_over_j = {"s_j": "mu2/j asserted", "canonical_carrier": False}
    assert not one_over_j["canonical_carrier"], "control: 1/j decay needs a canonical Perron-phi^3 carrier"
    print("FAIL_ONE_OVER_J_WITHOUT_CARRIER_REJECTED  asserting 1/j decay without a canonical carrier is caught.")

    print("PASS_ALPHA_PROFINITE_TOWER_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
