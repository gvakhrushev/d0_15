#!/usr/bin/env python3
"""D0-LEPTON-INDIRECT-GREEN-PUISEUX-SCOUT-001 - scout closure: what exists vs what is missing.

The scout precisely identifies the existing finite assets for the lepton indirect route and names the
minimal next owner. It is CERT-CLOSED as a scout (a documentation closure), NOT a theorem closure: the
indirect coefficient owner stays PROOF-TARGET.

EXISTING (registered): shell-torus / edge carrier (D0-EDGE-002 torus-ramification target, D0-EDGE-ALPHA-001
zetaEdge, D0-EDGE-RAMIFICATION-001 RamificationFromUeEffCompanion); Feshbach-Schur transfer
(D0-GENERATIVE-DYNAMICS-001 W_eff on rank-3/kernel-30, cert vp_feshbach_residue_amplitudes.py); exact
exponent row (0,1/4,1/3) THE (04.8).
MISSING (the minimal next owner): a finite Green function over the shell torus whose Puiseux/ramification
branch indices are PROVED to equal (0,1/4,1/3), with a branch-index uniqueness certificate; + the EFT/IR
matching functor for the decimal bridge.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
EXISTING = ["D0-EDGE-002", "D0-EDGE-ALPHA-001", "D0-EDGE-RAMIFICATION-001", "D0-GENERATIVE-DYNAMICS-001"]


def main() -> int:
    print("=== D0-LEPTON-INDIRECT-GREEN-PUISEUX-SCOUT-001  scout closure (existing vs missing) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the scout records the existing finite shell-torus/Feshbach/ramification assets "
          "and names the minimal missing owner; it does NOT close the coefficient owner")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    for c in EXISTING:
        assert c in rows, f"scouted existing asset must be registered: {c}"
    print(f"PASS_EXISTING_ASSETS_RECORDED  shell-torus/edge (D0-EDGE-002/-ALPHA-001/-RAMIFICATION-001) + Feshbach "
          "(D0-GENERATIVE-DYNAMICS-001) registered")
    assert (ROOT / "05_CERTS" / "vp_feshbach_residue_amplitudes.py").exists(), "Feshbach cert must exist"
    print("PASS_FESHBACH_TRANSFER_PRESENT  vp_feshbach_residue_amplitudes.py present (Feshbach-Schur transfer)")
    # the exponent row is exact (THE 04.8) but has NO proved operator source yet
    owner = rows.get("D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001")
    assert owner is not None and owner["release_status"] == "PROOF-TARGET", "the coefficient owner stays PROOF-TARGET"
    print("PASS_OWNER_STAYS_PROOF_TARGET  the exponent row (0,1/4,1/3) is exact (THE) but has NO proved Green/Puiseux operator "
          "source -> D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 stays PROOF-TARGET")
    print("SCOUT_CONCLUSION  minimal next owner = a finite Green function over the shell torus whose Puiseux/ramification "
          "branch indices PROVABLY equal (0,1/4,1/3) + a branch-index uniqueness cert; D0-EDGE-RAMIFICATION-001 (companion "
          "cover) + the Feshbach transfer are the nearest existing scaffolds to build it on.")
    print("PASS_LEPTON_GREEN_PUISEUX_SCOUT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
