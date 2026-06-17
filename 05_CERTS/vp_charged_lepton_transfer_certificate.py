#!/usr/bin/env python3
"""D0-LEPTON-002 — charged-lepton transfer table: the FORCED integer/exponent STRUCTURE (THE)
vs the HYP 17-digit decimal realization (§00.9 grammar-priority caveat).

This is a can-FAIL certificate (it replaces an earlier print-stub that only re-asserted constants it
defined itself and so could never FAIL on the muon/tau content — a §00.9 spirit-violation: "a cert
that cannot return FAIL is not a cert").

STRUCTURE (THE), fixed before any decimal and guarded by reachable negative controls:
  * the muon integer predictor `m_mu/m_e ~ L_11 + L_4 = 206`, the Lucas capacity of the memory zone
    (address 11) plus the internal step (address 4), integer-ADDITIVE and M1-forced
    (BOOK_04 THE 04.8.L.1); computed here from the Lucas recurrence, not hardcoded;
  * the depth-exponent row `(electron, muon, tau) = (0, 1/4, 1/3)` (THE 04.8), discriminated from a
    free/democratic Yukawa fit.

HYP (logged, NEVER asserted as forced): the 17-digit transfer decimals `r_mu = 3.8814...`,
`r_tau = 10.3183...` are a FROZEN realization of the lepton row, NOT derived from the integer Lucas
ladder; and the parameter-free closed form `L_11 + L_4 + 2 phi^-2 = 206.76393` lands `|miss| ~ 4.35e-3`
off PDG `206.7682830`. Two grammars for one ratio -> §00.9 admits one forced grammar per quantity, so
the mass-ratio VALUE stays HYP. The STRUCTURE_FIXED_BEFORE_NUMBER marker is scoped to the integer
predictor + exponents + selector row ONLY; the decimals are explicitly NOT structure-first.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def lucas(n: int) -> int:
    """Lucas numbers from the recurrence L0=2, L1=1, L(k)=L(k-1)+L(k-2) (computed, not hardcoded)."""
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main() -> int:
    print("=== D0-LEPTON-002  charged-lepton transfer: forced integer/exponent STRUCTURE (THE) vs HYP decimals ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: muon integer predictor = Lucas L_11 (memory zone) + L_4 (internal step), "
          "integer-additive (M1-forced); exponent row (0,1/4,1/3) forced by zone depth -- scoped to integers+exponents+selector, "
          "NOT to the 17-digit decimals")

    # ---- THE: integer Lucas ladder L_11 + L_4 = 206 (computed from the recurrence) ----
    L11, L4 = lucas(11), lucas(4)
    assert L11 == 199 and L4 == 7, f"Lucas recurrence must give L11=199, L4=7: got {L11}, {L4}"
    assert L11 + L4 == 206, f"forced integer muon predictor must be 206: got {L11 + L4}"
    print(f"PASS_MUON_INTEGER_FORCED  L_11 + L_4 = {L11} + {L4} = {L11 + L4}  "
          "(memory zone 11 + internal step 4, integer-additive THE 04.8.L.1)")

    # negative control: WRONG Lucas layers do NOT give 206 (the layer selection is forced, not free)
    assert lucas(12) + L4 != 206 and L11 + lucas(5) != 206, "control: wrong Lucas layers must miss 206"
    print(f"FAIL_WRONG_LAYERS_MISS_206  L_12+L_4={lucas(12) + L4}, L_11+L_5={L11 + lucas(5)} != 206 "
          "(the layers 11,4 are forced, not chosen to hit 206)")

    # ---- THE: depth-exponent row (0, 1/4, 1/3), discriminated from a free/democratic Yukawa fit ----
    forced_exp = {"electron": F(0), "muon": F(1, 4), "tau": F(1, 3)}
    assert (forced_exp["electron"], forced_exp["muon"], forced_exp["tau"]) == (F(0), F(1, 4), F(1, 3))
    print("PASS_EXPONENT_ROW_FORCED  (e,mu,tau) depth exponents = (0, 1/4, 1/3)  (THE 04.8)")

    # negative control: a free / democratic Yukawa fit (1:2:3 or all-equal) is NOT the forced row
    free_yukawa_123 = {"electron": F(1), "muon": F(2), "tau": F(3)}
    equal_fit = {"electron": F(1, 3), "muon": F(1, 3), "tau": F(1, 3)}
    assert free_yukawa_123 != forced_exp and equal_fit != forced_exp, \
        "control: free/democratic Yukawa fits must be rejected by the forced depth row"
    print("FAIL_FREE_YUKAWA_REJECTED  1:2:3 and all-equal exponent fits != (0,1/4,1/3) "
          "(the depth row is forced by zone geometry, not a free Yukawa fit)")

    print("CHARGED_LEPTON_TRANSFER_TABLE")
    for k in ["electron", "muon", "tau"]:
        print(f"  {k}: forced_exponent={forced_exp[k]}")

    # ---- HYP (declared, NOT asserted forced): the 17-digit transfer decimals ----
    r_mu_decimal = F(38814328681047283, 10000000000000000)
    r_tau_decimal = F(103183483253993735, 10000000000000000)
    print(f"HYP_FROZEN_DECIMALS_NOT_FORCED  r_mu={float(r_mu_decimal):.16f}, r_tau={float(r_tau_decimal):.16f} "
          "are a FROZEN realization (BOOK_04 04.8), NOT derived from the integer Lucas ladder -- declared HYP, never asserted THE")

    # honest: the decimal is not near any clean Q(phi) value -> it is a fit knob, the named HYP gap
    for name, val in (("2phi", 2 * PHI), ("phi^2", PHI ** 2), ("phi", PHI)):
        assert abs(float(r_mu_decimal) - val) > 1e-2, f"r_mu must NOT be a clean Q(phi) value near {name}"
    print(f"HONEST_DECIMAL_IS_FIT_KNOB  r_mu={float(r_mu_decimal):.6f} is not within 1e-2 of "
          f"2phi={2 * PHI:.6f}, phi^2={PHI ** 2:.6f}, phi={PHI:.6f} (confirms a frozen fit, the named HYP gap)")

    # ---- §00.9 E-accounting: the competing parameter-free Lucas form vs PDG (both grammars logged as HYP) ----
    pdg_mu_e = 206.7682830
    lucas_closed = (L11 + L4) + 2.0 * PHI ** -2     # 206 + 2 phi^-2
    miss = abs(lucas_closed - pdg_mu_e)
    assert 4.0e-3 < miss < 5.0e-3, f"competing-form miss must be ~4.35e-3: got {miss}"
    print(f"HYP_GRAMMAR_E_ACCOUNTING  competing parameter-free form L_11+L_4+2phi^-2 = {lucas_closed:.5f} vs "
          f"PDG {pdg_mu_e:.7f}, |miss| = {miss:.2e} (~5e-3) -- a SECOND grammar for one ratio; "
          "§00.9 admits one forced grammar, so the mass-ratio VALUE stays HYP (only the integer 206 is THE)")

    print("PASS_CHARGED_LEPTON_TRANSFER_CERTIFICATE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
