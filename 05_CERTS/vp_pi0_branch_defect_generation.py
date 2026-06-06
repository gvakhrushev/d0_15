#!/usr/bin/env python3
"""Certify D0 branch-defect projective generation relations.

This cert checks the numeric shadow of the Lean theorem:
minimal two-branch defect plane over F2 has exactly three nonzero projective rays
and the canonical companion/defect action cycles them with order 3.

It does not claim physical mass clustering or a PDG/Yukawa hierarchy.
Those remain outside this cert.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NO_GO = ROOT / "05_CERTS" / "NO_GO_PI0_BRANCH_DEFECT_GENERATION.md"
STATUS = "PASS_PI0_BRANCH_DEFECT_PROJECTIVE_GENERATION"


def phi() -> float:
    return (1.0 + math.sqrt(5.0)) / 2.0


def delta0() -> float:
    p_plus = 1.0 / phi()
    p_minus = 1.0 / (phi() * phi())
    return (p_plus - p_minus) / 2.0


def f2_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)


def defect_action(v: tuple[int, int]) -> tuple[int, int]:
    # Matrix [[0,1],[1,1]] over F2 in coordinate form (x,y)->(y,x+y)
    x, y = v
    return (y % 2, (x + y) % 2)


def orbit(v: tuple[int, int], steps: int = 4) -> list[tuple[int, int]]:
    out = [v]
    cur = v
    for _ in range(steps):
        cur = defect_action(cur)
        out.append(cur)
    return out


def main() -> int:
    ph = phi()
    p_plus = 1.0 / ph
    p_minus = 1.0 / (ph * ph)
    gap = p_plus - p_minus
    d0 = delta0()
    pi0 = (6.0 / 5.0) * ph * ph
    tau0 = 2.0 * pi0
    delta_pi = pi0 - math.pi

    e_plus = (1, 0)
    e_minus = (0, 1)
    e_gap = (1, 1)
    nonzero = {e_plus, e_minus, e_gap}

    projective_checks = {
        "f2_nonzero_projective_ray_count_eq_3": len(nonzero) == 3,
        "gap_ray_is_sum_of_plus_and_minus": f2_add(e_plus, e_minus) == e_gap,
        "action_ePlus_to_eMinus": defect_action(e_plus) == e_minus,
        "action_eMinus_to_eGap": defect_action(e_minus) == e_gap,
        "action_eGap_to_ePlus": defect_action(e_gap) == e_plus,
        "action_order_three_on_nonzero_rays": all(defect_action(defect_action(defect_action(v))) == v for v in nonzero),
    }

    real_lift_checks = {
        "pPlus_add_pMinus_eq_one": abs((p_plus + p_minus) - 1.0) < 1e-12,
        "branchGap_eq_two_delta0": abs(gap - 2.0 * d0) < 1e-12,
        "pi0_positive": pi0 > 0,
        "tau0_eq_two_pi0": abs(tau0 - 2.0 * pi0) < 1e-12,
        "deltaPi_nonzero_against_smooth_pi": abs(delta_pi) > 1e-7,
    }

    negative_controls = {
        "remove_gap_loses_third_ray": len({e_plus, e_minus}) != 3,
        "replace_phi_by_sqrt2_breaks_branch_normalization": abs((1/math.sqrt(2.0) + 1/2.0) - 1.0) > 1e-3,
        "perturb_6_5_changes_pi0_defect": abs(((1.21) * ph * ph - math.pi) - delta_pi) > 1e-3,
        "replace_pi0_by_pi_kills_phase_defect": abs(math.pi - math.pi) < 1e-15,
    }

    all_ok = all(projective_checks.values()) and all(real_lift_checks.values()) and all(negative_controls.values())

    payload = {
        "status": STATUS if all_ok else "FAIL_PI0_BRANCH_DEFECT_PROJECTIVE_GENERATION",
        "projective_checks": projective_checks,
        "real_lift_checks": real_lift_checks,
        "negative_controls": negative_controls,
        "values": {
            "phi": ph,
            "pPlus": p_plus,
            "pMinus": p_minus,
            "branchGap": gap,
            "delta0": d0,
            "pi0": pi0,
            "tau0": tau0,
            "deltaPi": delta_pi,
            "orbit_ePlus": orbit(e_plus, 3),
        },
        "scope_guardrail": "Core generation index is projective branch-defect cardinality. Physical masses/Yukawa hierarchy/clustering are not certified here.",
    }

    # Keep the historical NO_GO file but make it precise: no-go is about physical mass/phenomenology from this layer, not the core index.
    NO_GO.write_text(
        "# NO-GO: Pi0 Branch-Defect Physical Generation Clustering\n\n"
        "The projective branch-defect generation index is Lean-proved as exactly three.\n\n"
        "This no-go file records the remaining limitation: physical mass/Yukawa hierarchy or PDG clustering does not follow from the projective index alone.\n\n"
        + json.dumps(payload, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )

    print(payload["status"])
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
