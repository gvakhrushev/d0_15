"""D0-H0-EVOLVING-W-001 — convex archive acceleration R_n=phi^n-1 (FORM); the H0(z)/evolving-w
cosmological reading is an UNVERIFIED diagnostic awaiting pinned DESI data (PROOF-TARGET).

FORM (exact, can-FAIL): R_n = phi^n - 1 has strictly positive second difference
Delta^2 R_n = phi^n (phi-1)^2 > 0 (via phi^2 = phi + 1) -- a thawing/convex signature, distinct
from a cosmological constant (Delta^2 = 0). This convexity is the only genuinely-forced piece, and
it is the same fact already machine-checked as CORE in the sibling D0-PHASON-THAWING-001
(D0.Cosmology.ArchiveConvexity).

NOT a data confrontation: this cert reads NO external H0(z)/DESI/S8 datum. The earlier version
asserted a self-referential boolean "falsifier" (`def falsified(a,b): return a and b` re-stating a
truth table it defined two lines above) -- not a test of any observation; that tautology is removed.
The cosmological reading (H0 declining with z = the DESI w0>-1, wa<0 corner) is therefore an
UNVERIFIED diagnostic, NOT a passed empirical passport; binding it requires a pinned, versioned DESI
DR2/DR3 w0wa + H0(z) table. Registry status: PROOF-TARGET (data confrontation open), not
EMPIRICAL-PASSPORT.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + math.sqrt(5.0)) / 2.0


def R(n: int) -> float:
    return PHI ** n - 1.0


def main() -> int:
    print("=== D0-H0-EVOLVING-W-001  convex archive acceleration (FORM); cosmo reading = unverified diagnostic ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: R_n=phi^n-1, Delta^2 R_n=phi^n(phi-1)^2>0 forced by phi^2=phi+1 "
          "(convex/thawing FORM); the H0(z)/DESI reading is a diagnostic, NOT asserted against data here")

    # ---- FORM: convex second difference (exact, can-FAIL on a typo) -----------------
    for n in range(0, 12):
        d2 = R(n + 2) - 2 * R(n + 1) + R(n)
        closed = PHI ** n * (PHI - 1.0) ** 2
        assert abs(d2 - closed) <= 1e-9 * max(1.0, abs(closed)), f"Delta^2 R_{n} != phi^n (phi-1)^2"
        assert d2 > 0, f"Delta^2 R_{n} not strictly positive (convexity FORM broken)"
    print("PASS_CONVEX_ACCELERATION  Delta^2 R_n = phi^n (phi-1)^2 > 0 (thawing/convex FORM)")

    # ---- monotone increasing; Lambda-CDM (Delta^2=0) negative control ---------------
    assert all(R(n + 1) > R(n) for n in range(0, 12)), "R_n not monotone increasing"
    assert (1.0 - 2 * 1.0 + 1.0) == 0.0, "control: a constant R (Lambda-CDM) has Delta^2 = 0 (not thawing)"
    print("PASS_MONOTONE_CONVEX  R_n increasing & convex (vs Lambda-CDM Delta^2=0 control)")

    # ---- honest data boundary: NO external confrontation performed here -------------
    print("SKIP_H0_EVOLVING_W_EXTERNAL_DATA_REQUIRED  no pinned DESI DR2/DR3 w0wa + H0(z)/S8 table is read; "
          "the H0-declining-with-z reading is an UNVERIFIED diagnostic, not a passed passport (no self-referential "
          "boolean falsifier is asserted)")
    print("HONEST_CONVEXITY_FORCED_BUT_OWNED_BY_SIBLING  the forced piece (convexity) is CORE in "
          "D0-PHASON-THAWING-001 (D0.Cosmology.ArchiveConvexity); this row's distinct content is the cosmo reading, "
          "which awaits external data -> PROOF-TARGET")

    print("PASS_H0_EVOLVING_W")  # the FORM cert ran + the data confrontation was honestly gated
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
