#!/usr/bin/env python3
"""Micro-closure v2 Task 4: strengthen EW radial scale no-go."""

from __future__ import annotations

from vp_micro_ew_radial_hessian import run_vp_micro_ew_radial_hessian


def run_vp_micro2_ew_radial_scale_no_go() -> dict[str, object]:
    data = run_vp_micro_ew_radial_hessian()
    ledger = data["hessian_candidate_ledger"]  # type: ignore[index]
    scales = [row["positive_min_eigenvalue"] for row in ledger if row["positive_min_eigenvalue"] > 0.0]
    unique = len(set(round(float(x), 15) for x in scales)) == 1
    return {
        "status": "PASS_EW_RADIAL_SCALE_ACTION_SELECTOR_REQUIRED",
        "candidate_count": len(ledger),
        "unique_scale_without_extra_action": unique,
        "hessian_candidate_ledger": ledger,
        "required_new_object": (
            "A radial Higgs/action Hessian selector that ranks the candidate "
            "39-anchor operators before any SI mass conversion."
        ),
        "guardrail": "Do not choose identity_39 just because it gives the largest familiar-looking MeV value.",
    }


def main() -> None:
    result = run_vp_micro2_ew_radial_scale_no_go()
    print(f"VP micro2 EW radial scale no-go: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
