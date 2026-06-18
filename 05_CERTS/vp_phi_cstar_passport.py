#!/usr/bin/env python3
"""D0-PHI-CSTAR-PASSPORT-001 — external operator-algebra passport for the φ-cylinder trace.

The D0-core trace object is the admissible finite/profinite cylinder trace
(D0-PHI-CYLINDER-TRACE-UNIQUE-001, CERT-CLOSED). The EXTERNAL operator-algebra reading — that the
canonical invariant trace on the φ-hull crossed product A_φ = C(X_φ) ⋊_{σ_φ} ℤ is unique under the
standard unique-ergodicity / crossed-product theorem owner — is a PASSPORT, not a D0 theorem. This
cert enforces the passport conditions (can-FAIL): the internal object is frozen + CERT-CLOSED, the
external owner is declared in the passport note, and the corpus does NOT claim a bare scalar
C*(S_φ) has a unique trace 'because φ is unique'.
"""
from __future__ import annotations

import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

FORBIDDEN = [
    "C*(S_phi) has unique trace because phi is unique",
    "bare scalar C* has a unique trace",
]


def main() -> int:
    print("=== D0-PHI-CSTAR-PASSPORT-001  operator-algebra passport for the φ-cylinder trace ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the frozen internal object is the CERT-CLOSED cylinder trace "
          "(D0-PHI-CYLINDER-TRACE-UNIQUE-001); the crossed-product unique trace is the external owner")

    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    # (1) frozen internal object: the cylinder trace exists + is CERT-CLOSED
    inner = rows.get("D0-PHI-CYLINDER-TRACE-UNIQUE-001")
    assert inner is not None, "internal frozen object D0-PHI-CYLINDER-TRACE-UNIQUE-001 must be registered"
    assert inner["release_status"] == "CERT-CLOSED", f"internal object must be CERT-CLOSED, got {inner['release_status']!r}"
    print("PASS_FROZEN_INTERNAL_OBJECT  D0-PHI-CYLINDER-TRACE-UNIQUE-001 registered CERT-CLOSED")

    # (2) this passport row is PASSPORT-CLOSED and declares the external crossed-product owner
    me = rows.get("D0-PHI-CSTAR-PASSPORT-001")
    assert me is not None and me["release_status"] == "PASSPORT-CLOSED", "this row must be PASSPORT-CLOSED"
    note = me["notes"]
    for tok in ("crossed product", "C(X_phi)", "unique-ergodicity", "external"):
        assert tok in note, f"passport note must declare the external-owner token {tok!r}"
    print("PASS_EXTERNAL_OWNER_DECLARED  crossed-product C(X_phi) rtimes Z / unique-ergodicity owner named (external)")

    # (3) forbidden bare-scalar unique-trace claim absent from the books
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden bare-scalar unique-trace over-claim present: {hits}"
    print("PASS_NO_BARE_SCALAR_OVERCLAIM  no 'bare scalar C* has unique trace because phi is unique' claim in the books")

    # negative control: the over-claim detector is reachable
    planted = "x C*(S_phi) has unique trace because phi is unique x"
    assert any(f in planted for f in FORBIDDEN), "control: the bare-scalar over-claim detector must be reachable"
    print("FAIL_PLANTED_BARE_SCALAR_CAUGHT  detector catches a planted bare-scalar unique-trace over-claim (reachable)")

    print("PASS_PHI_CSTAR_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
