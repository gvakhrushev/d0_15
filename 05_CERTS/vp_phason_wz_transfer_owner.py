#!/usr/bin/env python3
"""D0-PHASON-WZ-TRANSFER-OWNER-001 (owner manifest) - explicit internal w_D0(u) is PROOF-TARGET.

Verifies the phason-w(z) front is honestly owned: the forced phason mode owner exists, the kernel-only
no-go and the pressure-EOS scaffold are registered-closed, and the explicit-w_D0(u) OWNER is
PROOF-TARGET with the named missing artifact -- no survey datum admitted.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"


def main() -> int:
    print("=== D0-PHASON-WZ-TRANSFER-OWNER-001  owner manifest (explicit w_D0(u) PROOF-TARGET) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: phason owner + 30-dim archive kernel + the EOS form; the explicit w_D0(u) is the named gap")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    def st(c):
        return rows.get(c, {}).get("release_status")

    assert "D0-PHASON-FORCING-001" in rows, "the forced gapless phason mode owner must exist"
    print("PASS_PHASON_OWNER_PRESENT  D0-PHASON-FORCING-001 (forced gapless dark mode) registered")
    assert st("D0-PHASON-WZ-KERNEL-ONLY-NOGO-001") in ("NO-GO", "NO_GO_PROVED"), "kernel-only no-go must be NO-GO"
    assert st("D0-PHASON-PRESSURE-EOS-SCAFFOLD-001") == "CERT-CLOSED", "pressure-EOS scaffold must be CERT-CLOSED"
    print("PASS_NOGO_AND_SCAFFOLD_CLOSED  kernel-only no-go = NO-GO; pressure-EOS scaffold = CERT-CLOSED")

    me = rows.get("D0-PHASON-WZ-TRANSFER-OWNER-001")
    assert me is not None and me["release_status"] == "PROOF-TARGET", "the transfer owner must be PROOF-TARGET"
    assert "w_D0(u)" in me["notes"] and "missing" in me["notes"].lower(), "note must name the missing explicit w_D0(u)"
    print("PASS_OWNER_PROOF_TARGET  D0-PHASON-WZ-TRANSFER-OWNER-001 = PROOF-TARGET; missing = explicit internal w_D0(u)/finite w_N")

    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    for f in ("DESI confirms D0", "D0 predicts DESI w(z)", "30-dimensional kernel proves w(z)"):
        assert f not in prose, f"forbidden survey/kernel over-claim present: {f}"
    print("PASS_NO_SURVEY_OVERCLAIM  no 'DESI confirms D0' / 'D0 predicts DESI w(z)' / 'kernel proves w(z)' in the books")
    print("PASS_PHASON_WZ_TRANSFER_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
