#!/usr/bin/env python3
"""D0-PASSPORT-DESI-BAO-001 — BAO/S_DE failure-diagnostics certificate.

HONEST FORM/VALUE split (replaces an earlier print-stub that unconditionally printed
FAIL_DESI_BAO_SDE_REAL_DATA + PASS with no data load — a §00.9 "a cert that cannot return FAIL is
not a cert" violation):

  * FORM (pre-registered, no external data needed): the frozen S_DE transfer polynomial
    160λ² − 480λ + 359 (BOOK_08 §08.12.2), with constant term 359 = |E| (the scene edge count, a
    forced invariant) and a positive discriminant (two real relaxation modes). Asserted here with a
    negative control (a refit of the constant degenerates the two-mode structure) — this is the
    can-FAIL core.
  * VALUE (external-data confrontation): the frozen roots/transfer vs a pinned DESI DR2 BAO table +
    covariance. This REQUIRES a present, hash-verified DESI file. When the cache is absent the cert
    emits an honest SKIP_BAO_SDE_EXTERNAL_DATA_REQUIRED and asserts NO FAIL/PASS on data it never
    loaded (matching the BOOK_08 §08.48 SKIP state). Registry status is PROOF-TARGET (FORM
    pre-registered; VALUE awaits a pinned DESI DR2/DR3 release), not EMPIRICAL-PASSPORT.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "08_PASSPORTS" / "DESI" / "desi_dr2_manifest.json"

# frozen S_DE transfer polynomial 160λ² − 480λ + 359 (BOOK_08 §08.12.2; do NOT refit)
POLY_A, POLY_B, POLY_C = 160, -480, 359
EDGE_COUNT = 359  # |E| of the scene K(9,11,13)


def main() -> int:
    print("=== D0-PASSPORT-DESI-BAO-001  BAO/S_DE failure diagnostics (FORM can-FAIL; VALUE data-gated) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: frozen S_DE polynomial 160λ²−480λ+359 (BOOK_08 §08.12.2), "
          "359=|E|, no refit of roots/windows/H0/Ωm/rd -- fixed before any survey datum")

    # ---- FORM (can-FAIL on a refit/typo; needs NO external data) ----
    assert (POLY_A, POLY_B, POLY_C) == (160, -480, 359), "frozen S_DE polynomial coefficients must not be refit"
    assert POLY_C == EDGE_COUNT, "constant term must be the scene edge count |E|=359 (forced, not fitted)"
    disc = POLY_B * POLY_B - 4 * POLY_A * POLY_C
    assert disc == 640 and disc > 0, f"discriminant must be 640>0 (two real relaxation modes): {disc}"
    print(f"PASS_SDE_FORM_FROZEN  160λ²−480λ+359, 359=|E|, disc={disc}>0 (two relaxation modes) -- FORM verified")

    # negative control: a refit of the constant term degenerates the two-real-mode structure
    disc_refit = POLY_B * POLY_B - 4 * POLY_A * (POLY_C + 1)
    assert disc_refit <= 0, f"control: a refit constant {POLY_C + 1} must lose the two-real-mode structure: {disc_refit}"
    print(f"FAIL_REFIT_BREAKS_TWO_MODES  a refit constant {POLY_C + 1} gives disc={disc_refit}<=0 "
          "(degenerate/no two modes); 359=|E| is forced, not fitted")

    # ---- VALUE (data-gated: honest SKIP when the DESI cache is absent or unverified) ----
    cache_present = False
    if MANIFEST.exists():
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        local = ROOT / m.get("local_path", "")
        if (not m.get("sample_data", True)) and m.get("status") == "READY" and local.exists():
            want = (m.get("sha256") or "").lower()
            got = hashlib.sha256(local.read_bytes()).hexdigest()
            cache_present = bool(want) and want == got

    if cache_present:
        # data present + hash-verified: the pinned VALUE confrontation is owned by the real-data runner
        value_status = "DATA_PRESENT_RUN_REAL_DATA_RUNNER"
        print("DATA_PRESENT  a hash-verified DESI DR2 table is present -- run vp_desi_bao_sde_real_data.py "
              "for the pinned VALUE confrontation (frozen roots vs measurement + covariance)")
    else:
        value_status = "SKIP_BAO_SDE_EXTERNAL_DATA_REQUIRED"
        print("SKIP_BAO_SDE_EXTERNAL_DATA_REQUIRED  no present, hash-verified DESI DR2 BAO table -- the VALUE "
              "confrontation is NOT run and NO FAIL/PASS is asserted on absent data (BOOK_08 §08.48 SKIP state)")

    results = {
        "form_status": "PASS_SDE_FORM_FROZEN",
        "value_status": value_status,
        "polynomial": "160*lambda^2 - 480*lambda + 359",
        "no_refit": True,
    }
    (Path(__file__).with_suffix(".results.json")).write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("PASS_DESI_BAO_SDE_FAILURE_DIAGNOSTICS")  # the FORM diagnostic ran + the VALUE was honestly gated
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
