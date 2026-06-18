#!/usr/bin/env python3
"""D0-SMOOTH-MANIFOLD-PASSPORT-001 — smooth manifold as a conditional macro-shadow passport.

The D0-internal object is the finite spectral/metric tower + the phi semigroup envelope
(D0-PHI-LADDER-SEMIGROUP-001 / D0-IM-003 + D0-CONNES-DISTANCE-GEODESIC-001: Connes distance = graph
geodesic, c=1=edge/tick). The smooth compact Riemannian/spin manifold reading is a DOWNSTREAM
macro-shadow, active only CONDITIONAL on the external owners -- Rieffel/GHP convergence
(D0-RIEFFEL-GHP-CONTINUUM-OWNER-001, ASSUMP-RIEFFEL-GHP) and Connes reconstruction
(D0-CONNES-RECONSTRUCTION-OWNER-001, ASSUMP-CONNES-RECONSTRUCTION). It is NOT a primitive D0 input and
NOT a CORE theorem.

Can-FAIL: both external owners must be registered, this row must be PASSPORT-CLOSED with a
conditional-macro-shadow note, and no "smooth manifold is a primitive D0 input" /
"finite tower certificate proves smooth manifold" over-claim may appear in the books.
"""
from __future__ import annotations

import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

OWNERS = ["D0-RIEFFEL-GHP-CONTINUUM-OWNER-001", "D0-CONNES-RECONSTRUCTION-OWNER-001"]
FORBIDDEN = [
    "smooth manifold is a primitive D0 input",
    "finite tower certificate proves smooth manifold",
    "finite tower certificate alone proves smooth manifold",
]


def main() -> int:
    print("=== D0-SMOOTH-MANIFOLD-PASSPORT-001  smooth manifold as a conditional macro-shadow passport ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: internal object = finite spectral/metric tower + phi semigroup envelope; "
          "the smooth-manifold reading is a downstream macro-shadow, conditional on the GHP + Connes owners")

    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    # both external owners registered (the macro-shadow is conditional on them)
    for o in OWNERS:
        assert o in rows, f"external owner {o} must be registered"
    print(f"PASS_OWNERS_DECLARED  {', '.join(OWNERS)} both registered (GHP convergence + Connes reconstruction)")

    me = rows.get("D0-SMOOTH-MANIFOLD-PASSPORT-001")
    assert me is not None and me["release_status"] == "PASSPORT-CLOSED", "this row must be PASSPORT-CLOSED"
    for tok in ("macro-shadow", "conditional", "RIEFFEL-GHP", "CONNES-RECONSTRUCTION", "not a primitive"):
        assert tok in me["notes"], f"passport note must declare {tok!r}"
    print("PASS_PASSPORT_FRAMING  macro-shadow conditional on RIEFFEL-GHP + CONNES owners; not a primitive D0 input, not CORE")

    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden smooth-manifold over-claim present: {hits}"
    print("PASS_NO_SMOOTH_OVERCLAIM  no 'smooth manifold is a primitive D0 input' / 'finite tower proves smooth manifold' in the books")

    assert any(f in "x finite tower certificate proves smooth manifold x" for f in FORBIDDEN), \
        "control: the over-claim detector must be reachable"
    print("FAIL_PLANTED_SMOOTH_OVERCLAIM_CAUGHT  detector catches a planted smooth-manifold over-claim (reachable)")

    print("PASS_SMOOTH_MANIFOLD_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
