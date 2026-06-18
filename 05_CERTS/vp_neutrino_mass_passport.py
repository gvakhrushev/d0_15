#!/usr/bin/env python3
"""D0-NEUTRINO-MASS-PASSPORT-001 — neutrino mass as a closed passport over the frozen seam Delta_alpha.

The D0-internal object is the dimensionless sterile-seam channel P_sterile := Delta_alpha^2, where
Delta_alpha is the CORE-FORMALIZED exact gluing anomaly (D0-DELTA-ALPHA-EXACT-001, exact in Q(phi)).
The external neutrino-mass reading m_nu/m_e ~ P_sterile is PACKAGING, not a CORE theorem: external
neutrino data may compare against the passport but may NOT tune Delta_alpha, mu1, mu2, or alpha.

This cert (can-FAIL) checks the passport conditions: the internal seam object is frozen + CORE, the
P_sterile = Delta_alpha^2 map is concrete in Q(phi), this row is PASSPORT-CLOSED, and no
"neutrino data tunes Delta_alpha" over-claim appears in the books.
"""
from __future__ import annotations

import csv
import pathlib
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def val(x):
    return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-NEUTRINO-MASS-PASSPORT-001  neutrino mass as a closed passport over the frozen Delta_alpha ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: internal object = P_sterile := Delta_alpha^2, Delta_alpha CORE-exact "
          "(D0-DELTA-ALPHA-EXACT-001); the external m_nu packaging is fixed AFTER the seam, never tuned by data")

    # frozen internal object: Delta_alpha exact in Q(phi) (D0-DELTA-ALPHA-EXACT-001) -> P_sterile = Delta_alpha^2 concrete
    delta_alpha = (F(-156109, 5), F(289442, 15))      # -156109/5 + (289442/15) phi  (D0-DELTA-ALPHA-EXACT-001)
    p_sterile = mul(delta_alpha, delta_alpha)
    assert abs(val(delta_alpha) - (-4.1522e-4)) < 1e-7, f"Delta_alpha must match the CORE exact value: {val(delta_alpha)}"
    assert val(p_sterile) > 0, "P_sterile = Delta_alpha^2 must be a positive frozen Q(phi) value"
    print(f"PASS_FROZEN_SEAM_OBJECT  Delta_alpha={val(delta_alpha):.3e} (exact Q(phi)); P_sterile=Delta_alpha^2={val(p_sterile):.3e} (frozen)")

    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    src = rows.get("D0-DELTA-ALPHA-EXACT-001")
    assert src is not None and src["release_status"] == "CORE-FORMALIZED", "Delta_alpha must be CORE-FORMALIZED (frozen)"
    print("PASS_INTERNAL_OWNER_CORE  D0-DELTA-ALPHA-EXACT-001 is CORE-FORMALIZED (the seam is a real owner, not a fit)")

    me = rows.get("D0-NEUTRINO-MASS-PASSPORT-001")
    assert me is not None and me["release_status"] == "PASSPORT-CLOSED", "this row must be PASSPORT-CLOSED"
    for tok in ("P_sterile", "Delta_alpha^2", "external", "not tune"):
        assert tok in me["notes"], f"passport note must declare {tok!r}"
    print("PASS_PASSPORT_FRAMING  P_sterile=Delta_alpha^2 internal; m_nu external packaging; data may not tune Delta_alpha")

    # forbidden over-claims absent from the books
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    forbidden = ["neutrino data tunes Delta_alpha", "neutrino mass is a CORE theorem", "KATRIN confirms D0"]
    hits = [f for f in forbidden if f in prose]
    assert not hits, f"forbidden neutrino over-claim present: {hits}"
    print("PASS_NO_NEUTRINO_OVERCLAIM  no 'neutrino data tunes Delta_alpha' / 'neutrino mass is CORE' / 'KATRIN confirms D0' in the books")

    # negative control: detector reachable
    assert any(f in "x neutrino data tunes Delta_alpha x" for f in forbidden), "control: over-claim detector reachable"
    print("FAIL_PLANTED_NEUTRINO_OVERCLAIM_CAUGHT  detector catches a planted neutrino over-claim (reachable)")

    print("PASS_NEUTRINO_MASS_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
