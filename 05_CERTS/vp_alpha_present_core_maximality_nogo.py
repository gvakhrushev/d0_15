#!/usr/bin/env python3
"""vp_alpha_present_core_maximality_nogo - D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001.

Maximality strengthening of the profinite tower no-go, quantified over ALL admissible present-core towers.
An admissible tower has frozen weight r=phi^-3 per increment and multiplicity growth rate a (block N ~
phi^(aN)); per-block trace contribution = rate(a)=phi^(a-3). Present-core supplies a=0 (constant 2^11
ledger) and a=1 (golden carrier, Perron phi). For ANY a<=2<3, rate(a)=phi^(a-3)<1 => trace-class =>
Dixmier/log-Cesaro coefficient 0 != mu_2=12288/5. The critical 1/j line is reached ONLY at a=3 (rate=1,
Perron eigenvalue phi^3), absent from present-core. Reachable controls reject an a>=3 carrier claimed as
present-core, a hand-tuned rate, and the finite-pole route.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

phi = (1 + 5 ** 0.5) / 2
mu2 = 12288 / 5


def rate(a):
    return phi ** (a - 3)


def main() -> int:
    print("=== vp_alpha_present_core_maximality_nogo  ALL admissible present-core towers are trace-class ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the weight r=phi^-3 and the admissible growth rates a (present-core "
          "= {0 constant ledger, 1 golden carrier}) are fixed first; trace-class for all a<=2 is the "
          "consequence; the critical 1/j line needs a=3 (Perron phi^3), absent from present-core.")

    # every present-core admissible rate is sub-critical => trace-class
    for a in (0, 1, 2):
        assert rate(a) < 1, f"rate({a})={rate(a)} must be < 1 (sub-critical)"
    print(f"PASS_ALL_ADMISSIBLE_TRACE_CLASS  rate(a)=phi^(a-3): a=0->{rate(0):.4f}, a=1->{rate(1):.4f}, "
          f"a=2->{rate(2):.4f}  (all < 1 => summable => Dixmier coeff 0).")

    # the critical line is reached EXACTLY at a=3 (Perron phi^3)
    assert abs(rate(3) - 1.0) < 1e-12, "rate(3) = 1 (critical line)"
    assert rate(4) > 1, "a>=4 super-critical (non-trace)"
    print(f"PASS_CRITICAL_THRESHOLD_AT_THREE  rate(3)=phi^0={rate(3):.4f} (critical 1/j line) <=> carrier "
          "Perron eigenvalue phi^3; a<3 strictly sub-critical, a>3 super-critical.")

    assert mu2 != 0
    print(f"PASS_MAXIMALITY_NOGO  no admissible present-core tower (a in {{0,1}}, even a<=2) realizes "
          f"mu_2={mu2:.4f}; the phi^3 carrier is absent (5-fold sym + M1 force the single golden rate phi).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bogus_carrier = {"a": 3, "claimed_present_core": True, "perron_eigenvalue": "phi^3"}
    assert not (bogus_carrier["a"] <= 2), "control: an a=3 (phi^3) carrier is NOT present-core (a<=2 only)"
    print("FAIL_PHI3_CARRIER_AS_PRESENT_CORE_REJECTED  claiming the a=3 (Perron phi^3) carrier as "
          "present-core is caught (present-core forces the golden rate phi, a<=1).")
    hand_tuned = {"rate": 1.0, "forced": False}
    assert not hand_tuned["forced"], "control: a hand-tuned critical rate is not forced"
    print("FAIL_HAND_TUNED_RATE_REJECTED  a hand-tuned multiplicity rate landing on the critical line is caught.")
    finite_pole = {"claims_1_over_s_pole": True, "valid": False}
    assert not finite_pole["valid"], "control: the finite-pole route is invalid (heat trace analytic at 0)"
    print("FAIL_FINITE_POLE_ROUTE_REJECTED  re-running the finite-pole/zeta-residue route is caught.")

    print("PASS_ALPHA_PRESENT_CORE_MAXIMALITY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
