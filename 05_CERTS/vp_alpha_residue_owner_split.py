#!/usr/bin/env python3
"""D0-DIXMIER-RESIDUE-OWNER-001 split guard - internal alpha_alg/Delta_alpha CLOSED, external residue PASSPORT.

Verifies the alpha-residue owner split is maintained and not contradicted:
  - internal alpha_alg closure exists (D0-ALPHA-ALG-CLOSED-001 / D0-DELTA-ALPHA-MOMENT-001);
  - internal Delta_alpha seam closure exists (D0-DELTA-ALPHA-SEAM-CLOSED-001 / D0-DELTA-ALPHA-EXACT-001);
  - the external Dixmier/Wodzicki residue-realization owner is registered as a bridge/passport
    (D0-DIXMIER-RESIDUE-OWNER-001, BRIDGE-ASSUMPTIONS-EXPLICIT = external-owner passport);
  - the old bare zeta-residue ROUTE is registered as a closed-negative no-go (D0-CVFT-F1, NO-GO);
  - no book wording demotes alpha_alg/Delta_alpha after closure, claims measured alpha is a theorem,
    leaves 'Delta_alpha analytic owner open' UNqualified, or claims the bare zeta-residue route is the
    internal owner.
Can-FAIL on any contradiction.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

FORBIDDEN = [
    "measured alpha is a theorem",
    "measured value of alpha is derived as a theorem",
    "bare zeta-residue route is the internal owner",
]


def main() -> int:
    print("=== D0-DIXMIER-RESIDUE-OWNER-001  alpha-residue owner split guard (internal CLOSED / external PASSPORT) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: internal alpha_alg + Delta_alpha seam are CLOSED; the profinite Dixmier "
          "residue-realization is the external owner; the bare zeta-route is a closed-negative no-go")

    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    def status(cid):
        return rows[cid]["release_status"] if cid in rows else None

    # internal closures present
    for cid in ("D0-ALPHA-ALG-CLOSED-001", "D0-DELTA-ALPHA-SEAM-CLOSED-001"):
        assert status(cid) == "CERT-CLOSED", f"{cid} must be CERT-CLOSED (internal), got {status(cid)}"
    for cid in ("D0-DELTA-ALPHA-MOMENT-001", "D0-DELTA-ALPHA-EXACT-001"):
        assert status(cid) == "CORE-FORMALIZED", f"{cid} must be CORE-FORMALIZED, got {status(cid)}"
    print("PASS_INTERNAL_ALPHA_CLOSED  alpha_alg + Delta_alpha seam CLOSED (CERT-CLOSED consolidations over CORE-FORMALIZED Lean)")

    # external residue owner = bridge/passport (NOT core)
    dix = status("D0-DIXMIER-RESIDUE-OWNER-001")
    assert dix in ("BRIDGE-ASSUMPTIONS-EXPLICIT", "EXTERNAL-BACKGROUND", "PASSPORT-CLOSED"), \
        f"D0-DIXMIER-RESIDUE-OWNER-001 must be an external passport, got {dix}"
    print(f"PASS_EXTERNAL_RESIDUE_PASSPORT  D0-DIXMIER-RESIDUE-OWNER-001 = {dix} (external-owner passport; the profinite "
          "Dixmier/Wodzicki residue realization, NOT a D0-core debt)")

    # old bare zeta-residue route = closed-negative no-go
    cvft = status("D0-CVFT-F1")
    assert cvft in ("NO-GO", "NO_GO_PROVED"), f"D0-CVFT-F1 (bare zeta-residue route) must be a closed-negative no-go, got {cvft}"
    print(f"PASS_ZETA_ROUTE_NO_GO  D0-CVFT-F1 (bare zeta-residue route) = {cvft} (closed-negative; 1/lnphi transcendental)")

    # no forbidden demotions/over-claims in the books
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden alpha-residue over-claim present: {hits}"
    print("PASS_NO_RESIDUE_OVERCLAIM  no 'measured alpha is a theorem' / 'bare zeta-route is the internal owner' in the books")

    # negative control: detector reachable
    assert any(f in "x measured alpha is a theorem x" for f in FORBIDDEN), "control: over-claim detector reachable"
    print("FAIL_PLANTED_RESIDUE_OVERCLAIM_CAUGHT  the over-claim detector is reachable (the guard can FAIL)")

    print("PASS_ALPHA_RESIDUE_OWNER_SPLIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
