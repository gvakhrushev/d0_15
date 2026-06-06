#!/usr/bin/env python3
"""Guard risky physical interpretations in CLAIM_TO_LEAN_MAP.csv.

This checker does not validate physics. It enforces status discipline:
formal Lean rows may stay formal, bridge rows must remain conditional, and
empirical/SI/continuum promotions must be explicit.
"""

from __future__ import annotations

import sys

from sync_theory_status_map import CLAIM_MAP, claim_domain, claim_text, claim_type, read_csv


RISKY_DOMAINS = {
    "rg",
    "si_calibration",
    "cosmology",
    "spectral_action",
    "smooth_geometry",
    "empirical_passport",
    "gauge_bridge",
    "external_background",
}

COMMON_CORE_GUARDS = {
    "formal",
    "finite",
    "dimensionless",
    "typed",
    "proxy",
    "symbolic",
    "guardrail",
    "not core",
    "external",
    "requires",
    "cannot promote",
}

DOMAIN_GUARDS = {
    "rg": COMMON_CORE_GUARDS | {"interpolation", "certificate", "bounded", "scheme"},
    "si_calibration": {"dimensionless", "external", "externalsicalibration", "requires", "cannot"},
    "cosmology": COMMON_CORE_GUARDS
    | {"shape", "floor", "fixed point", "zero-mean", "mass", "concrete", "formula", "jacobian"},
    "spectral_action": COMMON_CORE_GUARDS
    | {"trace", "heat-trace", "heat trace", "floor", "bounded", "no continuum", "ladder"},
    "smooth_geometry": COMMON_CORE_GUARDS | {"covariance", "continuum", "declared bridge"},
    "empirical_passport": {"passport", "external", "independent", "not core", "data", "certificate"},
    "gauge_bridge": COMMON_CORE_GUARDS | {"algebraic", "positive", "bridge-scoped", "assumption"},
    "external_background": {"external", "background", "not active", "not core"},
}

PHYSICAL_PROMOTION_TERMS = {
    "observed value",
    "physical value",
    "physical constant",
    "matches data",
    "standard model",
    "cosmological constant",
    "continuum limit",
    "einstein-hilbert",
    "h0",
    "g_n",
    "lambda",
    "pdg",
    "bao",
    "desi",
    "pantheon",
}

BOUNDARY_TERMS = {
    "external",
    "passport",
    "certificate",
    "cert",
    "bridge",
    "not core",
    "requires",
    "cannot",
    "finite",
    "dimensionless",
    "no continuum",
}


def has_any(text: str, terms: set[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def bridge_status_ok(release_status: str) -> bool:
    return (
        release_status.startswith("BRIDGE")
        or release_status in {"CERT-CLOSED", "CORE_BRIDGE_SPLIT", "NO-GO", "NO_GO_PROVED"}
        or release_status.startswith("NO-GO")
    )


def main() -> int:
    claims = read_csv(CLAIM_MAP)
    failures: list[str] = []

    for row in claims:
        domain = claim_domain(row)
        ctype = claim_type(row)
        status = row["release_status"]
        text = claim_text(row)
        notes = row["notes"].strip()
        claim_id = row["claim_id"]

        if domain in RISKY_DOMAINS and not notes:
            failures.append(f"{claim_id}: risky domain `{domain}` has empty notes")

        if row["uses_bridge_assumptions"].lower() == "true":
            if not row["assumption_ids"].strip():
                failures.append(f"{claim_id}: uses_bridge_assumptions=True but assumption_ids is empty")
            if not bridge_status_ok(status):
                failures.append(f"{claim_id}: bridge assumptions are present but release_status is `{status}`")

        if domain == "external_background" and status == "CORE-FORMALIZED":
            failures.append(f"{claim_id}: external background cannot be CORE-FORMALIZED")

        if domain == "si_calibration" and status == "CORE-FORMALIZED":
            failures.append(f"{claim_id}: SI calibration must stay bridge/calibration scoped, not CORE-FORMALIZED")

        if status == "CORE-FORMALIZED" and domain in RISKY_DOMAINS:
            guards = DOMAIN_GUARDS[domain]
            if not has_any(text, guards):
                failures.append(f"{claim_id}: CORE-FORMALIZED `{domain}` row lacks a formal scope guard")

        if ctype == "core" and has_any(text, PHYSICAL_PROMOTION_TERMS) and not has_any(text, BOUNDARY_TERMS):
            failures.append(f"{claim_id}: core row contains physical-promotion wording without boundary terms")

    if failures:
        print("FAIL: physical bridge discipline")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"PASS: physical bridge discipline ({len(claims)} claims checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
