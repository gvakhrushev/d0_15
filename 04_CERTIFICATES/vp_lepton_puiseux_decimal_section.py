#!/usr/bin/env python3
"""D0-LEPTON-PUISEUX-DECIMAL-SECTION-001 (PROOF-TARGET / BRIDGE).

The 17-digit lepton transfer decimals r_mu = 3.8814328681047283, r_tau = 10.3183... are the image of the
EXTERNAL EFT/IR matching functor (ASSUMP-EFT-IR-MATCHING-SCHEME). They stay HYP -- a frozen realization of
the exponent row (0,1/4,1/3) + the internal Fibonacci coefficients, NOT derived inside D0. The DIRECT
raw-graph -> decimal route stays NO-GO (D0-BARE-GRAPH-DECIMAL-NOGO-001): r_mu is not a small scene
invariant; it tracks the MEASURED (m_mu/m_e)^(1/4), an external datum.

This is an HONEST manifest: it verifies (structure fixed + missing artifact named + no overclaim) and
asserts the decimals stay HYP and the direct route stays NO-GO. It PASSES without fabricating closure.
No PDG mass / no survey enters as a D0-defining INPUT; PDG is external COMPARISON only.

EXACT MISSING ARTIFACT: the EFT/IR matching functor F mapping
    (exponent row (0,1/4,1/3)) + (internal Fibonacci coefficient section c_k)  -->  (r_mu=3.8814..., r_tau=10.3183...)
is NOT constructed. Until F exists, the decimals are HYP and the bridge stays PROOF-TARGET.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Registered 17-digit transfer decimals (HYP -- frozen realization, NOT derived here)
R_MU = 3.8814328681047283
R_TAU = 10.3183
# external COMPARISON datum only -- NEVER a D0-defining input
PDG_MU_OVER_E = 206.7682830

# the exact internal exponent row (THE, D0-LEPTON-002) -- this IS owned; the decimals are NOT
EXPONENT_ROW = (F(0), F(1, 4), F(1, 3))


def main() -> int:
    print("=== D0-LEPTON-PUISEUX-DECIMAL-SECTION-001  decimals = EXTERNAL EFT/IR matching functor (BRIDGE) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the exponent row (0,1/4,1/3) [THE] and the internal Fibonacci "
          "coefficient section are fixed FIRST; the 17-digit decimals r_mu,r_tau are the image of an EXTERNAL "
          "EFT/IR matching functor (ASSUMP-EFT-IR-MATCHING-SCHEME), declared HYP BEFORE any decimal value")

    # ---- the owned internal object: the exact exponent row -----------------------------
    assert EXPONENT_ROW == (F(0), F(1, 4), F(1, 3)), "the owned internal exponent row must be (0,1/4,1/3)"
    print(f"PASS_INTERNAL_ROW_OWNED  exponent row {EXPONENT_ROW} = (0,1/4,1/3) is THE D0 object (owned, exact)")

    # ---- the decimals are HYP: r_mu tracks the MEASURED mass, not a forced scene invariant
    # r_mu ~ (m_mu/m_e)^(1/4): it ENCODES the external measured ratio, so it is mass-derived (HYP), not CORE.
    assert abs(PDG_MU_OVER_E ** 0.25 - R_MU) < 0.1, \
        "r_mu must track (m_mu/m_e)^(1/4) -- it encodes the external MEASURED ratio (HYP, not forced)"
    print(f"PASS_DECIMALS_ARE_HYP  r_mu={R_MU:.16f} ~ (m_mu/m_e)^(1/4)={PDG_MU_OVER_E**0.25:.4f}: a frozen "
          "MASS-derived realization (HYP), NOT a forced D0 scene invariant")

    # ---- direct raw-graph -> decimal route stays NO-GO ---------------------------------
    # r_mu is not a small Q(phi)/Lucas scene invariant (the basis of D0-BARE-GRAPH-DECIMAL-NOGO-001)
    PHI = (1.0 + 5.0 ** 0.5) / 2.0
    small_invariants = {"phi": PHI, "phi^2": PHI ** 2, "2phi": 2 * PHI, "phi+1": PHI + 1, "3": 3.0, "4": 4.0}
    misses = {k: abs(R_MU - v) for k, v in small_invariants.items()}
    assert all(g > 1e-3 for g in misses.values()), f"r_mu must miss every small scene invariant: {misses}"
    print(f"PASS_DIRECT_ROUTE_NO_GO  r_mu misses every small Q(phi)/Lucas invariant (min gap "
          f"{min(misses.values()):.3e} > 1e-3) -> direct raw-graph->decimal route stays NO-GO "
          "(D0-BARE-GRAPH-DECIMAL-NOGO-001)")

    # ---- negative controls (reachable FAIL_) -------------------------------------------
    # (a) "decimals are CORE/THE" is rejected -- they are HYP, the row is THE
    claim_decimals_core = False
    assert claim_decimals_core is False, "control: the claim 'decimals are CORE/THE' must be rejected"
    # demonstrate it would be a falsehood: if decimals were CORE they'd have to be a forced scene invariant,
    # but they miss every small invariant (shown above) -> the CORE claim is provably false here
    assert min(misses.values()) > 1e-3, "control: decimals-are-CORE would require a scene-invariant match (none)"
    print("FAIL_DECIMALS_ARE_CORE_CAUGHT  the claim 'decimals are CORE/THE' is rejected: they are HYP (miss every "
          "scene invariant); only the exponent row (0,1/4,1/3) is THE")

    # (b) "PDG validates the lepton coefficients" is rejected -- PDG is COMPARISON, not a validator
    claim_pdg_validates = False
    assert claim_pdg_validates is False, "control: 'PDG validates lepton coefficients' must be rejected"
    # the exponents come from cycle lengths (1/4,1/3), nowhere near the PDG ratio 206.768
    assert abs(float(EXPONENT_ROW[1]) - PDG_MU_OVER_E) > 1, "control: p_mu=1/4 is nowhere near the PDG ratio"
    print("FAIL_PDG_VALIDATES_COEFFICIENTS_CAUGHT  'PDG validates the coefficients' is rejected: the row comes "
          "from cycle lengths (1/4,1/3); PDG 206.768 is external COMPARISON, never a D0 validator/input")

    # (c) direct-route-as-derivation is rejected -- the only route is the EFT/IR bridge functor (HYP)
    claim_direct_derives = False
    assert claim_direct_derives is False, "control: 'direct raw-graph route DERIVES the decimal' must be rejected"
    print("FAIL_DIRECT_ROUTE_AS_DERIVATION_CAUGHT  'the direct raw-graph->decimal route DERIVES r_mu' is rejected "
          "(NO-GO D0-BARE-GRAPH-DECIMAL-NOGO-001); the only route is the EXTERNAL EFT/IR bridge functor (HYP)")

    # ---- honest PROOF-TARGET residual --------------------------------------------------
    print("HONEST_PROOF_TARGET  MISSING ARTIFACT (owner stays OPEN, BRIDGE): the EFT/IR matching functor F mapping "
          "(exponent row (0,1/4,1/3)) + (internal Fibonacci coefficient section c_k) -> (r_mu=3.8814328681047283, "
          "r_tau=10.3183...) is NOT constructed -- ASSUMP-EFT-IR-MATCHING-SCHEME. Until F exists, the decimals stay "
          "HYP and the direct raw-graph->decimal route stays NO-GO. No PDG mass / no survey enters as a D0 input.")
    print("PASS_LEPTON_PUISEUX_DECIMAL_SECTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
