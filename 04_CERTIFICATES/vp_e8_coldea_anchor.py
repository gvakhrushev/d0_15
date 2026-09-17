"""D0-E8-COLDEA-ANCHOR-001 — the leading E8 mass ratio m2/m1 = 2cos(pi/5) = phi (math identity, CERT-CLOSED).

The genuinely-verifiable content is the trig identity m2/m1 = 2cos(pi/5) = phi (Zamolodchikov's E8
S-matrix spectrum), and that this is the SAME phi D0 forces (phi^2 = phi + 1). Both are exact,
can-FAIL checks. The CoNb2O6 quantum-criticality observation (Coldea et al., Science 327 (2010) 177)
that the emergent E8 leading mass ratio sits at ~the golden ratio is recorded as PROSE-CITED external
corroboration -- NOT a pinned measurement with a versioned uncertainty. This cert therefore confronts
no data; it is a FORM/identity cert (CERT-CLOSED), not an EMPIRICAL-PASSPORT.

(Earlier this cert asserted `abs(m2_over_m1 - 1.618) < 0.02` against a hand-typed `1.618`, which only
re-checked phi ~ 1.618 and never touched the Coldea measurement; and it printed a FAIL_ token
unconditionally on the success path. Both are removed.)
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + math.sqrt(5.0)) / 2.0


def main() -> int:
    print("=== D0-E8-COLDEA-ANCHOR-001  E8 m2/m1 = 2cos(pi/5) = phi (math identity + prose-cited corroboration) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the leading E8 mass ratio m2/m1 = 2cos(pi/5) = phi is a fixed trig "
          "identity (Zamolodchikov E8), checked before any external comparison")

    # ---- THE: the leading E8 mass ratio is the golden ratio (exact trig identity, can-FAIL) ----
    m2_over_m1 = 2.0 * math.cos(math.pi / 5.0)
    assert abs(m2_over_m1 - PHI) < 1e-12, "2 cos(pi/5) != phi"
    print(f"PASS_GOLDEN_E8_MASS_RATIO  m2/m1 = 2cos(pi/5) = phi = {m2_over_m1:.6f} (exact trig identity)")

    # ---- THE: it is the SAME phi D0 forces (phi^2 = phi + 1) ----
    assert abs(PHI ** 2 - (PHI + 1.0)) < 1e-12, "phi does not satisfy phi^2 = phi + 1"
    print("PASS_E8_PHI_COINCIDENCE  the E8-critical golden ratio is the D0-forced phi")

    # ---- negative control: phi is rejected against the 3/2 alternative ----
    assert abs(m2_over_m1 - 1.5) > 0.1, "control: phi must differ from the 3/2 alternative"
    print("PASS_E8_RATIO_REJECTS_THREE_HALVES  phi differs from 3/2 by >0.1 (the 3/2 alternative is rejected)")

    # ---- external corroboration: PROSE-CITED, not a pinned measurement ----
    print("CITED_COLDEA_CORROBORATION  CoNb2O6 quantum criticality (Coldea et al., Science 327 (2010) 177) reports "
          "the leading emergent-E8 mass ratio ~ the golden ratio (~1.618) -- PROSE-CITED external corroboration, NOT a "
          "pinned measurement with a versioned uncertainty; this cert asserts the trig identity, not a data confrontation")
    print("HONEST_CORROBORATION_NOT_A_DERIVATION  D0 does not derive CoNb2O6; the icosian->E8 step stays an "
          "EXTERNAL-GAP bridge (Mordell genus-uniqueness not in the kernel)")

    print("PASS_E8_COLDEA_ANCHOR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
