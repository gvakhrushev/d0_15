#!/usr/bin/env python3
"""vp_five_front_construction_no_overclaim - guard the five-front construction strike.

Reads the canonical registry AND the books. Fails on grand-closure / front-specific over-claim phrases
unless the corresponding owner is registered at a CLOSED status. The guard reads REGISTRY ROWS (not only
prose): a closure phrase is allowed only if its owner row is actually closed.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CLOSED = {"CORE-FORMALIZED", "CERT-CLOSED", "OPERATOR-SCAFFOLD-CERTIFIED", "NO-GO", "NO_GO_PROVED",
          "PASSPORT-CLOSED", "BRIDGE-ASSUMPTIONS-EXPLICIT", "DEPRECATED"}

# Phrases that are over-claims regardless of registry state (forbidden in the books).
UNCONDITIONAL = [
    "D0 is complete TOE",
    "D0 is a complete TOE",
    "zero theorem debt",
    "Open-joints register is empty",
    "Open-joints register empty",
    "CODATA proves alpha",
    "CODATA validates alpha",
    "PDG proves lepton coefficients",
    "PDG validates lepton coefficients",
    "DESI confirms D0",
    "DESI selects D0",
    "Euclid confirms D0",
    "Rieffel convergence closed",
    "Rieffel/GHP solved",
    "Adler-Weiss closed",
    "Adler-Weiss imported as external theorem and called CORE",
    "Dixmier residue closed",
    "charged-lepton decimals are CORE",
    "w(z) derived from kernel alone",
    "w(z) derived from kernel dimension",
    "smooth manifold primitive",
]

# phrase -> owner claim_id that must be registered-closed for the phrase to be allowed in prose.
CONDITIONAL = {
    "Feshbach finite residue closed": "D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001",
    "D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001 CLOSED": "D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001",
    "neutrino norm-square closed": "D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001",
    "lepton Green-Puiseux operator closed": "D0-LEPTON-GREEN-PUISEUX-OPERATOR-001",
    "Lucas-Voronoi partition closed": "D0-LUCAS-VORONOI-MARKOV-PARTITION-001",
    "phason w_DE sign normalization closed": "D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001",
    "D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001 CLOSED": "D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001",
    "CPL passport closed": "D0-PHASON-WZ-CPL-PASSPORT-001",
    "Connes graph distance closed": "D0-CONNES-GRAPH-DISTANCE-OWNER-001",
    "GHP golden Cauchy bound closed": "D0-GHP-GOLDEN-CAUCHY-BOUND-001",
}

# Owners that this strike registers as still-open: they must NOT be at a CLOSED status.
MUST_STAY_OPEN = [
    "D0-ALPHA-FESHBACH-DIXMIER-OWNER-001",
    "D0-LEPTON-PUISEUX-DECIMAL-SECTION-001",
    "D0-TORAL-TIME-MARKOV-CONJUGACY-001",
    "D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001",
    "D0-PHASON-WZ-LOGDET-WINDOW-OWNER-001",
]


def main() -> int:
    print("=== vp_five_front_construction_no_overclaim  guard the five-front construction strike ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: every closure phrase must be backed by a registered-closed owner row; "
          "the open owners of this strike must stay non-closed; no grand-closure / survey-proves-D0 phrase in the books")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))

    # frontier non-empty (the register is not empty while PROOF-TARGET rows remain)
    proof_targets = [c for c, r in rows.items() if r["release_status"] == "PROOF-TARGET"]
    assert len(proof_targets) > 0, "registry has zero PROOF-TARGET rows -- verify before any closure claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(proof_targets)} PROOF-TARGET rows remain (open-joints register is NOT empty)")

    # unconditional over-claims must be absent from the books
    hits = [p for p in UNCONDITIONAL if p in prose]
    assert not hits, f"forbidden five-front over-claim(s) in books: {hits}"
    print(f"PASS_NO_UNCONDITIONAL_OVERCLAIM  none of the {len(UNCONDITIONAL)} over-claims appear in the books")

    # conditional closure phrases only if the owner is registered-closed (reads REGISTRY ROWS)
    for phrase, cid in CONDITIONAL.items():
        if phrase in prose:
            st = rows.get(cid, {}).get("release_status")
            assert st in CLOSED, f"book claims '{phrase}' but {cid} is not registered-closed (status={st})"
    print("PASS_CONDITIONAL_OWNERS  any closure phrase in the books is backed by a registered-closed owner row")

    # the open owners of this strike must NOT be silently closed
    for cid in MUST_STAY_OPEN:
        r = rows.get(cid)
        if r is not None:
            assert r["release_status"] not in {"CORE-FORMALIZED"}, f"{cid} must stay open, not CORE-FORMALIZED"
            assert r["release_status"] in {"PROOF-TARGET", "OPEN"}, \
                f"{cid} must stay PROOF-TARGET/OPEN (got {r['release_status']})"
    print(f"PASS_OPEN_OWNERS_STAY_OPEN  the {len(MUST_STAY_OPEN)} declared-open front owners are all PROOF-TARGET/OPEN")

    # negative control: the detector is reachable
    planted = "intro: DESI confirms D0 and the Open-joints register is empty."
    assert any(p in planted for p in UNCONDITIONAL), "control: the over-claim detector must be reachable"
    print("FAIL_PLANTED_FIVE_FRONT_OVERCLAIM_CAUGHT  the detector catches a planted grand-closure phrase (reachable)")

    print("PASS_FIVE_FRONT_CONSTRUCTION_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
