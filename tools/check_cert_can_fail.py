#!/usr/bin/env python3
"""check_cert_can_fail.py — guillotine guard: every registered cert must be able to FAIL.

A certificate that only prints `PASS` tokens with no computation is not a certificate —
the token-matching runner (`run_hard_theorem_closure.py`) rubber-stamps it for free. This
guard closes that blind spot: for every `vp_*.py` referenced in the canonical registry, the
file must contain real failure machinery — at least one `assert`, `raise`, or a conditional
non-zero exit — so a wrong input would actually be rejected.

Exit 0 if every registered cert can fail; exit 1 listing the print-stub offenders.
A small GRANDFATHER set may be passed via --allow to stage a cleanup (e.g. while the
known stubs are being rewritten or demoted); the allow-list is printed so it cannot hide
silently.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CERTS = ROOT / "05_CERTS"

# DEBT RATCHET — registered certs that currently compute-but-don't-gate (print PASS without
# an assert/raise/conditional-exit). This guard's job from now on is to block any NEW such
# cert; the existing debt is grandfathered HERE, printed every run (never hidden), and must
# only SHRINK. Iteration 5 Track-3 rewrites/demotes the 5 pure print-stubs first
# (HODGE, NOAXION, BH-CAPACITY-A4, SPECTRAL-EINSTEIN, HODGE-LINKS); the rest is an owner
# decision (see AUTONOMOUS_SESSION_REPORT). Remove a name the moment its cert really gates.
GRANDFATHER = {
    "vp_archive_pressure_coupling_from_relative_acceleration.py",
    "vp_baryon_40_56_anonymous_poles.py",
    "vp_canonical_operator_search.py",
    "vp_critical_collapse_dss_echo_lattice.py",
    "vp_desi_bao_sde_failure_diagnostics.py",
    "vp_finite_mincut_holographic_entropy.py",
    "vp_fractal_continuum_predictions.py",
    "vp_generation_overlap_response_origin.py",
    "vp_icecube_hese_baseline_comparison.py",
    "vp_meson_positive_defect_transfer.py",
    "vp_nonabelian_seam_gap.py",
    "vp_qnm_delta0_overtone_ladder.py",
    "vp_ramification_edge_ueff_companion.py",
    "vp_relative_archive_acceleration_cosmology_bridge.py",
    "vp_sparc_hull_boundary_response_kernel.py",
    "vp_strong_logdet_pressure_coupling.py",
    "vp_v1132_gauge_matter_ward_anomaly.py",
    "vp_v1143_forced_return_windows_capacity.py",
    "vp_v1145_operator_bridge_triple.py",
}

# evidence that a cert can fail: a real failing branch — an assertion, a non-entry raise,
# a conditional non-zero exit, or the `ok=False ... return 0 if ok else 1` idiom.
FAIL_EVIDENCE = re.compile(
    r"^\s*assert\s"
    r"|^\s*raise\s(?!SystemExit\((?:main|run)\b)"     # a raise that is NOT the entrypoint
    r"|sys\.exit\(1\)"
    r"|\bok\s*=\s*False\b"
    r"|\belse\s+1\b"                                   # `return 0 if ok else 1`
    r"|^\s*return\s+1\b"
)
COMMENT_OR_BLANK = re.compile(r"^\s*(#|$)")


def cert_can_fail(path: Path) -> bool:
    in_doc = False
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        # skip triple-quoted docstring blocks (crude but sufficient: stubs have one docstring)
        if s.startswith('"""') or s.startswith("'''"):
            in_doc = not in_doc if s.count('"""') % 2 == 1 and len(s) > 3 else (not in_doc if s in ('"""', "'''") else in_doc)
            continue
        if in_doc or COMMENT_OR_BLANK.match(ln):
            continue
        if FAIL_EVIDENCE.search(ln):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow", default="", help="extra cert filenames grandfathered on top of GRANDFATHER")
    ap.add_argument("--strict", action="store_true", help="ignore GRANDFATHER (show the full debt)")
    args = ap.parse_args()
    allow = set() if args.strict else set(GRANDFATHER)
    allow |= {a.strip() for a in args.allow.split(",") if a.strip()}

    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    certs = set()
    for r in rows:
        for c in (r.get("python_cert") or "").split(";"):
            c = c.strip()
            if c:
                certs.add(c)

    offenders, missing = [], []
    for c in sorted(certs):
        p = CERTS / c
        if not p.exists():
            # fall back to a recursive search under 05_CERTS — certs may live in
            # ported_legacy_primary/<CLAIM-ID>/ subdirs (same resolution as run_registered_certs).
            hits = list(CERTS.rglob(c))
            if hits:
                p = hits[0]
            else:
                missing.append(c)
                continue
        if not cert_can_fail(p):
            offenders.append(c)

    if allow and not args.strict:
        print(f"check_cert_can_fail: {len(allow)} cert(s) grandfathered (debt ratchet — "
              f"see GRANDFATHER in tools/check_cert_can_fail.py; must only shrink)")
    real = [c for c in offenders if c not in allow]
    print(f"check_cert_can_fail: {len(certs)} registered certs; "
          f"{len(offenders)} print-stub(s), {len(real)} unallowed; {len(missing)} missing-on-disk")
    if real:
        print("!! certs that CANNOT FAIL (pure print-stubs — rewrite with real checks or demote):")
        for c in real:
            print("  - " + c)
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS — every registered cert can fail (or is grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
