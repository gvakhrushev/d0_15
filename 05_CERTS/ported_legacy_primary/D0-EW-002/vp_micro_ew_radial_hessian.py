#!/usr/bin/env python3
"""Final micro-closure Task 3: EW radial/Higgs Hessian scale audit."""

from __future__ import annotations

import math

import numpy as np

from d0_graph import delta_0, phi
from vp_qmass_ew_full_mass_spectrum import run_vp_qmass_ew_full_mass_spectrum


def run_vp_micro_ew_radial_hessian() -> dict[str, object]:
    ew = run_vp_qmass_ew_full_mass_spectrum()
    e0 = float(ew["E0_MeV"])
    runtime = ew["dimensionless_runtime"]  # type: ignore[assignment]
    t_z = float(runtime["T_Z"])  # type: ignore[index]
    t_w = float(runtime["T_W"])  # type: ignore[index]
    n_anchor = 39
    v_h = delta_0 / math.sqrt(n_anchor)

    # Candidate 39-anchor Hessians.  They are all internal, but the current
    # action does not pick one uniquely.
    candidates = {}
    candidates["identity_39"] = np.eye(n_anchor)
    candidates["single_anchor_radial"] = np.diag([n_anchor] + [0.0] * (n_anchor - 1))
    candidates["uniform_vH_curvature"] = (v_h**2) * np.eye(n_anchor)
    candidates["cycle_leakage_curvature"] = (delta_0**3) * np.eye(n_anchor)
    candidates["golden_depth_curvature"] = (phi**-8) * np.eye(n_anchor)

    ledger = []
    for name, mat in candidates.items():
        eigs = np.linalg.eigvalsh(mat)
        positive = eigs[eigs > 1e-14]
        scale = float(np.min(positive)) if len(positive) else 0.0
        ledger.append(
            {
                "candidate": name,
                "rank": int(np.linalg.matrix_rank(mat)),
                "positive_min_eigenvalue": scale,
                "positive_max_eigenvalue": float(np.max(positive)) if len(positive) else 0.0,
                "MZ_MeV_if_used_as_scale": e0 * math.sqrt(t_z * scale) if scale > 0.0 else 0.0,
                "MW_MeV_if_used_as_scale": e0 * math.sqrt(t_w * scale) if scale > 0.0 else 0.0,
            }
        )

    return {
        "status": "PASS_EW_RADIAL_HESSIAN_SINGLE_GAUGE_FALSE_OPEN_CLOSURE",
        "E0_MeV": e0,
        "v_H": v_h,
        "runtime": {"T_Z": t_z, "T_W": t_w},
        "hessian_candidate_ledger": ledger,
        "single_gauge_statement": (
            "A 39-anchor radial Hessian can be constructed in several internal ways, "
            "but Single Action-Gauge forbids using any of them as a second independent "
            "SI mass dictionary.  The only closed EW observable here is the runtime ratio."
        ),
    }


def main() -> None:
    result = run_vp_micro_ew_radial_hessian()
    print(f"VP micro EW radial Hessian: [{result['status']}]")
    for key, value in result.items():
        if key != "status":
            print(f"{key}= {value}")


if __name__ == "__main__":
    main()
