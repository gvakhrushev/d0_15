#!/usr/bin/env python3
"""vp_alpha_seam_form_forced.py — compute layer for D0-ALPHA-SEAM-FORM-FORCED-001 (candidate).

SCOPE (object B ONLY — the dressing/holonomy form; see ALPHA_SEAM_NOGO_V2.md): this cert NEVER
touches the moment-realization front (object A: (mu1,mu2,mu3), alg record, /D_Sigma, rho-family,
zones 11/13, zeta/Dixmier) — that front is CLOSED by D0-ALPHA-SEAM-REALIZATION-NOGO-001 and its
external owner ASSUMP-DIXMIER-TRACE is untouched here.

CLAIM UNDER TEST (candidate, PROOF-TARGET): the dressing tuple
    depth = phi^-17 = xi5 * phi^-12 (SPLIT: seam factor xi5=phi^-5 THE, D0-XI5-TORUS-DEFECT-001;
                     transport factor phi^-12 + composition = OPEN sub-leg, prose 02.13.h:87)
    channel = sin    (off-diagonal, G^2=-I; D0-Q8-SIN-CHANNEL-001, THE)
    angle = 12/5     (D0-PI0-DISCRETE-ANGLE-001, THE)
    form = linear 1+h*sin (N^2=0; D0-ALPHA-HOLONOMY-LINEAR-FORM-001, THE)
    rate h_KS = ln(phi) (identification unowned - near-parents rows 285/243; OPEN leg 5)
is the unique D0-admissible seam dressing of alpha_top^-1 = 359 phi^-2 - phi^-5 = 726 - 364 phi.
"Forced" = unique fixed point of owned constraints, never a fit; the 9-digit agreement is a
CONSEQUENCE (stays CHK, D0-ALPHA-HOLONOMY-002) and the last ~1e-8 stays HYP
(D0-ALPHA-MEASUREMENT-LIMIT-001).

WHAT THIS CERT CHECKS (exact/mpmath, can-fail):
  S1. Assembly: alpha_top^-1 computed EXACTLY in Q(phi) two independent ways (359 phi^-2 - phi^-5
      vs 726 - 364 phi), then dressed: alpha_D0^-1 = alpha_top^-1 + phi^-17*(1 + ln(phi)*sin(12/5));
      digits printed, compared to the FROZEN book value 137.035999151 (section 02.13.h) at 9 digits.
      This check can fail (any leg change breaks it).
  S2. SEPARATION (the falsifier surface F1-F4, each control CAN fail the conclusion): every rival
      tuple — F1 exp-form, F2 cos-channel, F3 wrong depth (phi^-16 and phi^-18 = the TOTAL depths
      of the registry-named seam family phi^-4/phi^-6, vp_xi5_cross_sector.py:60-64), F4 wrong
      rate (h=1, h=ln2, h=phi^-1) — lands >= 1e-6 away from the frozen value: the NAMED-RIVAL
      surface is separated. If any rival landed at <= 1e-6, S2 would FAIL.
      SCOPE (skeptic #19 R4): S2 separates against NAMED rivals only; the CONTINUUM of rates
      (e.g. h = 12/25 lands ~2e-7 from frozen) is NOT excluded by S2 — it is excluded by
      F5/ownership (a free real rate is tuning: "zero free real coefficients", 02.13.h:79) and
      by the row's open exhaustion obligation. Separation != exhaustion.
  S3. HONESTY GUARD: THREE open obligations -> default rc=2 (HONEST-OPEN, the PROOF-TARGET
      state): (i) leg 1b - the phi^-12 transport factor + composition are unowned prose;
      (ii) leg 5 - the cross-scope identification of the registered multiplier rate (row 285)
      with the owned rate value (row 243) is unowned; (iii) joint exhaustion is unowned.
      --grant-ks-rate grants leg 5 + exhaustion as hypotheses -> rc=0 (sufficiency demo: MUT-A
      pattern — IF the open leg is owned, the tuple is unique among the named surface).
  S4. FIREWALL GUARD (F5 redirection clause): asserts this cert makes NO realization claim —
      the moment tuple (1/3, 12288/5, 0) is never computed FROM the dressing; a textual guard
      verifies this file contains no /D_Sigma or rho-normalization of the dressing. If F5 ever
      SUCCEEDS elsewhere (an owned pi0-coefficient derivation with independent content beyond
      the assembled form — hook (iv) verbatim), that does NOT falsify form-forcing — it REOPENS
      the realization no-go via its hook (iv).

rc=2 default (honest open), rc=0 with --grant-ks-rate, rc=1 any check fails.
"""
import sys
from fractions import Fraction

from mpmath import mp, mpf, sqrt, log, sin, power

mp.dps = 40

PHI = (1 + sqrt(5)) / 2
FROZEN_BOOK_VALUE = mpf("137.035999151")   # section 02.13.h frozen value (object B)
CODATA_2018 = mpf("137.035999084")          # printed for context only; NEVER a pass/fail input


def q_phi_eval(a: Fraction, b: Fraction):
    """Evaluate a + b*phi exactly-symbolically then numerically (exact Q(phi) pair)."""
    return mpf(a.numerator) / a.denominator + (mpf(b.numerator) / b.denominator) * PHI


def main() -> int:
    grant = "--grant-ks-rate" in sys.argv
    failures = []

    # S1 — assembly, two independent exact routes to alpha_top^-1.
    #   Route 1: 359*phi^-2 - phi^-5 ; Route 2: exact Q(phi) pair (726, -364).
    r1 = 359 * power(PHI, -2) - power(PHI, -5)
    r2 = q_phi_eval(Fraction(726), Fraction(-364))
    ok_top = abs(r1 - r2) < mpf("1e-35")
    h_ks = log(PHI)
    dressing = power(PHI, -17) * (1 + h_ks * sin(mpf(12) / 5))
    alpha_d0 = r1 + dressing
    ok_nine = abs(alpha_d0 - FROZEN_BOOK_VALUE) < mpf("5e-10")
    print(f"S1 assembly: alpha_top^-1 two-route agree={ok_top}; "
          f"alpha_D0^-1={mp.nstr(alpha_d0, 12)} vs frozen {mp.nstr(FROZEN_BOOK_VALUE, 12)} "
          f"(CODATA context {mp.nstr(CODATA_2018, 12)}): {'PASS' if ok_top and ok_nine else 'FAIL'}")
    if not (ok_top and ok_nine):
        failures.append("S1")

    # S2 — separation controls (each rival CAN fail the conclusion; all must land far).
    rivals = {
        "F1-exp-form":      r1 + power(PHI, -17) * (mp.e ** (h_ks * sin(mpf(12) / 5))),
        "F2-cos-channel":   r1 + power(PHI, -17) * (1 + h_ks * mp.cos(mpf(12) / 5)),
        "F3-depth-16":      r1 + power(PHI, -16) * (1 + h_ks * sin(mpf(12) / 5)),
        "F3-depth-18":      r1 + power(PHI, -18) * (1 + h_ks * sin(mpf(12) / 5)),
        "F4-rate-1":        r1 + power(PHI, -17) * (1 + 1 * sin(mpf(12) / 5)),
        "F4-rate-ln2":      r1 + power(PHI, -17) * (1 + log(2) * sin(mpf(12) / 5)),
        "F4-rate-phiinv":   r1 + power(PHI, -17) * (1 + (1 / PHI) * sin(mpf(12) / 5)),
    }
    sep_ok = True
    for name, val in rivals.items():
        dist = abs(val - FROZEN_BOOK_VALUE)
        good = dist > mpf("1e-6")
        sep_ok &= good
        print(f"  S2 {name}: |delta|={mp.nstr(dist, 3)} {'SEPARATED' if good else 'COLLIDES'}")
    print(f"S2 separation: {'PASS' if sep_ok else 'FAIL'}")
    if not sep_ok:
        failures.append("S2")

    # S4 — firewall guard (textual, self-referential): no realization language in this cert.
    src = open(__file__, encoding="utf-8").read()
    banned = ["D_Sigma-normal" + "ized dressing", "rho-normal" + "ized dressing",
              "real" + "izes mu2", "der" + "ives (1/3, 12288/5"]
    ok_fw = not any(b in src for b in banned)
    print(f"S4 firewall-guard (object B only, no realization claim): {'PASS' if ok_fw else 'FAIL'}")
    if not ok_fw:
        failures.append("S4")

    if failures:
        print(f"RESULT: FAIL {','.join(failures)} rc=1")
        return 1

    # S3 — honesty: leg 5 + joint exhaustion are not owned.
    if grant:
        print("RESULT: PASS (sufficiency demo under --grant-ks-rate: granted leg-5 h_KS=ln(phi) "
              "ownership + named-surface exhaustion => tuple unique on the surface) rc=0")
        return 0
    print("RESULT: HONEST-OPEN rc=2 — assembly + separation PASS; ONE open obligation: "
          "(i) leg 1b phi^-12 transport factor + composition unowned (four-door fork post "
          "TransportTwelveForkCollapse). (ii) ADOPTED at assembly grade [post-skeptic #22, "
          "SEAM_RATE_ADOPTION_MEMO.md; Lean D0.Spectral.SeamRateImport wired] — ceiling: "
          "entropy reading stays the named external wrapper. (iii) DECOMPOSED "
          "[EXHAUSTION_DECOMPOSITION_MEMO.md] — reduces to (i). The FORCED claim stays "
          "PROOF-TARGET. This rc=2 is the registered state of D0-ALPHA-SEAM-FORM-FORCED-001.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
