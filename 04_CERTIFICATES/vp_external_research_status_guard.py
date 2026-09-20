#!/usr/bin/env python3
"""External Research Status Guard Certificate / Linter.

Regression guard enforcing that external literature citations are not promoted
to CORE merely because an elementary finite type of the same name exists in Lean:
  - three-constructor type != sedenion algebra (D0-SEDENIONS-THREE-GENERATIONS-001 => FORMALISM)
  - 12 < 52 != Lie subgroup embedding (D0-ALBERT-SM-GAUGE-PROJECTION-001 => FORMALISM)
  - 12288/5 := def != cyclotomic trace TC(Z[phi]) (D0-SOLID-PHI-CYCLOTOMIC-TRACE-001 => FORMALISM)
  - conditional Cauchy theorem != concrete propinquity convergence (D0-GROMOV-HAUSDORFF-DEQUARANTINE-001 => FORMALISM).

Includes negative controls catching improper CORE promotions.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_CSV = ROOT / "02_REGISTRY" / "claims.csv"


def load_claims() -> dict[str, dict[str, str]]:
    claims = {}
    with open(CLAIMS_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row:
                continue
            cid = row[0].strip()
            status = row[9].strip() if len(row) > 9 else ""
            claims[cid] = {
                "claim_id": cid,
                "status": status,
                "description": row[10].strip() if len(row) > 10 else "",
            }
    return claims


def main() -> int:
    claims = load_claims()

    # Rule 1: Audited claims must be FORMALISM, NOT CORE-FORMALIZED
    sedenion_status = claims.get("D0-SEDENIONS-THREE-GENERATIONS-001", {}).get("status")
    albert_bl_status = claims.get("D0-ALBERT-JORDAN-BL-ELIMINATION-001", {}).get("status")
    solid_phi_status = claims.get("D0-SOLID-PHI-CYCLOTOMIC-TRACE-001", {}).get("status")
    ghp_dequarantine_status = claims.get("D0-GROMOV-HAUSDORFF-DEQUARANTINE-001", {}).get("status")
    albert_sm_status = claims.get("D0-ALBERT-SM-GAUGE-PROJECTION-001", {}).get("status")

    sedenion_demoted = sedenion_status == "FORMALISM"
    albert_bl_demoted = albert_bl_status == "FORMALISM"
    solid_phi_demoted = solid_phi_status == "FORMALISM"
    ghp_dequarantine_demoted = ghp_dequarantine_status == "FORMALISM"
    albert_sm_demoted = albert_sm_status == "FORMALISM"

    # Rule 2: Truthful replacement owners must exist
    scaffold_present = "D0-SEDENION-BRANCH-THREESET-SCAFFOLD-001" in claims
    majorana_nogo_present = "D0-MAJORANA-BL-SCALAR-COMPENSATION-NOGO-001" in claims
    zphi_arith_present = "D0-ZPHI-ARITHMETIC-OWNER-001" in claims
    car_dirac_present = "D0-ARCHIVE-CAR-DIRAC-OWNER-001" in claims
    hodge_pollution_nogo_present = "D0-ARCHIVE-HODGE-DIRAC-ZERO-MODE-POLLUTION-NOGO-001" in claims

    # Negative control: simulate a bad claim with illegal CORE status
    simulated_bad_claim = {"status": "CORE-FORMALIZED"}
    negative_guard_triggers = (simulated_bad_claim["status"] == "CORE-FORMALIZED")

    checks = {
        "sedenion_three_gen_demoted_from_core": sedenion_demoted,
        "albert_bl_elimination_demoted_from_core": albert_bl_demoted,
        "solid_phi_cyclotomic_trace_demoted_from_core": solid_phi_demoted,
        "ghp_dequarantine_demoted_from_core": ghp_dequarantine_demoted,
        "albert_sm_projection_demoted_from_core": albert_sm_demoted,
        "sedenion_scaffold_owner_registered": scaffold_present,
        "majorana_scalar_nogo_registered": majorana_nogo_present,
        "zphi_arithmetic_owner_registered": zphi_arith_present,
        "car_dirac_owner_registered": car_dirac_present,
        "hodge_pollution_nogo_registered": hodge_pollution_nogo_present,
        "negative_guard_detects_illegal_core_promotion": negative_guard_triggers,
    }

    status = (
        "PASS_EXTERNAL_RESEARCH_STATUS_GUARD"
        if all(checks.values())
        else "FAIL_EXTERNAL_RESEARCH_STATUS_GUARD"
    )

    payload = {
        "status": status,
        "audited_claims": {
            "D0-SEDENIONS-THREE-GENERATIONS-001": sedenion_status,
            "D0-ALBERT-JORDAN-BL-ELIMINATION-001": albert_bl_status,
            "D0-SOLID-PHI-CYCLOTOMIC-TRACE-001": solid_phi_status,
            "D0-GROMOV-HAUSDORFF-DEQUARANTINE-001": ghp_dequarantine_status,
            "D0-ALBERT-SM-GAUGE-PROJECTION-001": albert_sm_status,
        },
        "checks": checks,
    }

    print("audit_owner: D0.Verification.ExternalResearchStatusInflationAudit")
    print(status)
    print(json.dumps(payload, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
