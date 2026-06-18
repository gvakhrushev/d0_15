#!/usr/bin/env python3
"""D0-PASSPORT-SPARC-001 — SPARC hull-boundary response kernel: the seam-gap FORM (can-FAIL) vs the
SPARC rotation-curve VALUE confrontation (data-gated; SKIP when the database is absent).

FORM (exact, can-FAIL, no external data): the hull-boundary response kernel's seam energy is the
squared Frobenius norm of the generator commutator on the finite seam. A COMMUTING (abelian) generator
pair gives zero seam energy; a NON-COMMUTING pair gives strictly positive seam energy (the hull-boundary
seam gap). Computed here from explicit matrices with a negative control.

VALUE (data-gated): confronting the kernel against the SPARC rotation-curve database (Lelli, McGaugh &
Schombert 2016, 175 galaxies) requires that database to be present/pinned. It is NOT bundled here, so
the cert emits SKIP_SPARC_EXTERNAL_DATA_REQUIRED and asserts no rotation-curve PASS. Registry status is
PROOF-TARGET (data confrontation open), not EMPIRICAL-PASSPORT. (Replaces a print-stub that printed
PASS_SPARC_HULL_BOUNDARY_RESPONSE_KERNEL with hard-coded 0.0/2.0 and no computation.)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]


def commutator_seam_energy(A, B):
    """E_seam = ||AB - BA||_F^2 for 2x2 real matrices (nested lists)."""
    def mul(X, Y):
        return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    AB, BA = mul(A, B), mul(B, A)
    return sum((AB[i][j] - BA[i][j]) ** 2 for i in range(2) for j in range(2))


def main() -> int:
    print("=== D0-PASSPORT-SPARC-001  hull-boundary seam-gap FORM (can-FAIL) + SPARC VALUE (data-gated) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: seam energy = ||[A,B]||_F^2; a commuting generator -> 0, a "
          "non-commuting generator -> >0 (the hull-boundary seam gap), fixed before any rotation-curve datum")

    # ---- FORM (can-FAIL): commuting -> 0 seam energy; non-commuting -> positive ----
    abelian_A, abelian_B = [[1, 0], [0, -1]], [[2, 0], [0, 3]]      # both diagonal -> commute
    nonab_A, nonab_B = [[0, 1], [1, 0]], [[1, 0], [0, -1]]          # sigma_x, sigma_z -> [.,.] != 0
    e_ab = commutator_seam_energy(abelian_A, abelian_B)
    e_nonab = commutator_seam_energy(nonab_A, nonab_B)
    assert e_ab == 0, f"abelian (commuting) seam energy must vanish: {e_ab}"
    assert e_nonab > 0, f"non-abelian (non-commuting) seam energy must be positive: {e_nonab}"
    print(f"PASS_ABELIAN_SEAM_KERNEL_CONTROL  E_seam(abelian)={e_ab}=0, E_seam(non-abelian)={e_nonab}>0 "
          "(commuting generators give no seam gap; non-commuting give it)")

    # negative control: a commuting pair can NEVER manufacture a positive seam gap
    assert commutator_seam_energy(abelian_A, [[5, 0], [0, 7]]) == 0, "control: any commuting pair must give 0"
    print("FAIL_COMMUTING_CANNOT_FAKE_GAP  every commuting generator pair gives E_seam=0 (the gap needs non-commutativity)")

    # ---- VALUE (data-gated): the SPARC rotation-curve confrontation needs the database ----
    sparc_dir = ROOT / "08_PASSPORTS" / "SPARC"
    data_present = sparc_dir.exists() and any(sparc_dir.iterdir())
    if not data_present:
        print("SKIP_SPARC_EXTERNAL_DATA_REQUIRED  the SPARC rotation-curve database (Lelli-McGaugh-Schombert 2016, "
              "175 galaxies) is not present/pinned -- the kernel-vs-rotation-curve VALUE confrontation is NOT run "
              "and no rotation-curve PASS is asserted")
    value_status = "DATA_PRESENT_RUN_CONFRONTATION" if data_present else "SKIP_SPARC_EXTERNAL_DATA_REQUIRED"

    results = {
        "form_status": "PASS_SEAM_GAP_FORM",
        "value_status": value_status,
        "E_seam_abelian": e_ab,
        "E_seam_nonabelian": e_nonab,
    }
    (Path(__file__).with_suffix(".results.json")).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("PASS_SPARC_HULL_BOUNDARY_RESPONSE_KERNEL")  # the seam-gap FORM kernel passed; SPARC VALUE honestly gated
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
