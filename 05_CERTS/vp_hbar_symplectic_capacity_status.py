#!/usr/bin/env python3
"""vp_hbar_symplectic_capacity_status - guard: physical ħ is NOT a closed CORE theorem.

The commutator obstruction [J,Y] != 0 is rigidity-forced (THE). The identification of its symplectic
capacity with the DIMENSIONFUL physical ħ is a mechanism-limit (MECH-LIMIT): the finite-capacity
mechanism is identified, but the normalization from the finite capacity class to physical ħ is an open
bridge owner (D0-HBAR-SYMPLECTIC-CAPACITY-MECH-LIMIT-001). This guard fails if the books re-assert ħ as a
derived CORE theorem, or use ħ as a core primitive, without a closed finite-capacity-normalization owner.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CID = "D0-HBAR-SYMPLECTIC-CAPACITY-MECH-LIMIT-001"

# phrases that over-claim a CORE/THE derivation of physical ħ (must be ABSENT from the books)
FORBIDDEN = [
    "ħ is derived, not postulated",
    "hbar is derived, not postulated",
    "ħ is a CORE theorem",
    "physical ħ is derived as a core theorem",
    "ħ = c_symp([J,Y]) is THE",
    "the quantum of action is a closed core theorem",
]


def main() -> int:
    print("=== vp_hbar_symplectic_capacity_status  physical ħ is MECH-LIMIT, not a closed CORE theorem ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the forced object is the commutator obstruction [J,Y]!=0 (THE); the "
          "identification with dimensionful physical ħ is a mechanism-limit (capacity mechanism identified, "
          "normalization to physical ħ open) -- fixed before any number")

    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))

    # 1. no over-claim phrase present
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"books over-claim physical ħ as a derived CORE theorem: {hits}"
    print(f"PASS_NO_HBAR_CORE_OVERCLAIM  none of the {len(FORBIDDEN)} 'ħ is a derived CORE theorem' phrases appear")

    # 2. the MECH-LIMIT status note is present and references the owner
    assert CID in prose, f"the ħ MECH-LIMIT status note ({CID}) must appear in the books"
    assert "MECH-LIMIT" in prose and "symplectic" in prose.lower(), "the MECH-LIMIT framing must be stated"
    print(f"PASS_MECH_LIMIT_NOTE_PRESENT  the books carry the MECH-LIMIT status note for {CID}")

    # 3. the registry row, if present, must NOT be a CORE status (firewall: ħ never CORE)
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    r = rows.get(CID)
    if r is not None:
        assert r["release_status"] not in ("CORE-FORMALIZED",), f"{CID} must not be CORE (got {r['release_status']})"
        assert r["release_status"] in ("BRIDGE-ASSUMPTIONS-EXPLICIT", "CORE_BRIDGE_SPLIT", "PROOF-TARGET", "MECH-LIMIT"), \
            f"{CID} must carry a non-core bridge/proof-target status (got {r['release_status']})"
        print(f"PASS_REGISTRY_NOT_CORE  {CID} registered at {r['release_status']} (firewall: ħ never CORE)")
    else:
        print(f"INFO_NO_REGISTRY_ROW  {CID} not yet registered (book-level status note is the owner)")

    # negative control: a planted ħ-CORE over-claim is caught
    planted = "intro: ħ is derived, not postulated, as a closed core theorem."
    assert any(f in planted for f in FORBIDDEN), "control: the ħ-overclaim detector must be reachable"
    print("FAIL_PLANTED_HBAR_CORE_OVERCLAIM_CAUGHT  the detector catches a planted 'ħ is derived (CORE)' phrase (reachable)")

    print("PASS_HBAR_SYMPLECTIC_CAPACITY_STATUS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
