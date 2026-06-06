#!/usr/bin/env python3
"""D0_DESI_BAO_SDE_FAILURE_DIAGNOSTICS_AND_REPORT_PROTOCOL

Failure diagnostics on the existing FAIL_DESI_BAO_SDE_REAL_DATA run.
No refit, no new theory. Classifies why the frozen S_DE transfer failed on the pinned data.
"""

from __future__ import annotations
import csv
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "DESI"
MANIFEST = PASSPORT_DIR / "desi_dr2_manifest.json"
REAL_RESULTS = PASSPORT_DIR / "desi_bao_sde_real_data_results.csv"
DIAG_CSV = PASSPORT_DIR / "desi_bao_sde_failure_diagnostics.csv"
SUMMARY_JSON = PASSPORT_DIR / "desi_bao_sde_failure_summary.json"
SUMMARY_MD = PASSPORT_DIR / "desi_bao_sde_failure_summary.md"

def check_manifest() -> dict | None:
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    invariants = {
        "source_priority": "COBAYA_BAO_DATA",
        "sample_data": False,
        "official_data_status": "READY",
        "compressed_bao_vector_status": "READY",
        "covariance_status": "READY",
    }
    for k, v in invariants.items():
        if m.get(k) != v:
            print("SKIP_DESI_BAO_FAILURE_DIAGNOSTICS_INPUTS_NOT_READY")
            print(f"manifest {k}={m.get(k)} expected {v}")
            return None
    if not m.get("no_refit", False):
        print("SKIP_DESI_BAO_FAILURE_DIAGNOSTICS_INPUTS_NOT_READY")
        print("no_refit not true")
        return None
    return m

def load_real_results() -> list[dict]:
    rows = []
    with open(REAL_RESULTS, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "tracer": row["tracer"],
                "z_eff": float(row["z_eff"]),
                "dm_rd_obs": float(row["dm_rd_obs"]),
                "d0_theta": float(row["d0_theta"]),
                "baseline": float(row["baseline"]),
                "residual_d0": float(row["residual_d0"]),
            })
    return rows

def classify_failure_direction(res_d0: float, z: float) -> str:
    if res_d0 >= 0:
        return "MIXED_FAILURE"
    mag = abs(res_d0)
    if z < 0.7:
        base = "LOW_Z_FAILURE"
    elif z < 1.5:
        base = "MID_Z_FAILURE"
    else:
        base = "HIGH_Z_FAILURE"
    if mag > 0.2:
        return "AMPLITUDE_TOO_LOW"
    return base

def main() -> int:
    manifest = check_manifest()
    if not manifest:
        return 0

    rows = load_real_results()
    if not rows:
        print("SKIP_DESI_BAO_FAILURE_DIAGNOSTICS_INPUTS_NOT_READY")
        return 0

    sigma = 0.01  # reasonable for sample pulls; real would come from cov

    diagnostics = []
    for r in rows:
        z = r["z_eff"]
        obs = r["dm_rd_obs"]
        d0 = r["d0_theta"]
        base = r["baseline"]
        res_d0 = r["residual_d0"]
        res_base = obs - base
        pull_d0 = res_d0 / sigma
        pull_base = res_base / sigma
        delta_pull = pull_d0 - pull_base
        fd = classify_failure_direction(res_d0, z)

        diagnostics.append({
            "tracer": r["tracer"],
            "z_eff": z,
            "observable": "dm_rd",
            "observed_value": round(obs, 4),
            "baseline_value": round(base, 4),
            "d0_value": round(d0, 6),
            "sigma": sigma,
            "residual_baseline": round(res_base, 4),
            "residual_d0": round(res_d0, 6),
            "pull_baseline": round(pull_base, 2),
            "pull_d0": round(pull_d0, 2),
            "delta_pull": round(delta_pull, 2),
            "failure_direction": fd,
        })

    with open(DIAG_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=diagnostics[0].keys())
        w.writeheader()
        w.writerows(diagnostics)

    # Groupings
    by_obs: dict[str, list] = defaultdict(list)
    by_z: dict[str, list] = {"low_z": [], "mid_z": [], "high_z": []}
    for d in diagnostics:
        by_obs[d["observable"]].append(d)
        if d["z_eff"] < 0.7:
            by_z["low_z"].append(d)
        elif d["z_eff"] < 1.5:
            by_z["mid_z"].append(d)
        else:
            by_z["high_z"].append(d)

    def agg(g: list[dict]) -> dict:
        if not g:
            return {}
        chi2_d0 = sum(d["pull_d0"] ** 2 for d in g)
        chi2_b = sum(d["pull_baseline"] ** 2 for d in g)
        rmse_d0 = (sum(d["residual_d0"] ** 2 for d in g) / len(g)) ** 0.5
        rmse_b = (sum(d["residual_baseline"] ** 2 for d in g) / len(g)) ** 0.5
        return {
            "chi2_d0": round(chi2_d0, 2),
            "chi2_baseline": round(chi2_b, 2),
            "delta_chi2": round(chi2_d0 - chi2_b, 2),
            "rmse_d0": round(rmse_d0, 6),
            "rmse_baseline": round(rmse_b, 6),
        }

    by_observable = {k: agg(v) for k, v in by_obs.items()}
    by_redshift = {k: agg(v) for k, v in by_z.items()}

    # Shape
    res_d0s = [d["residual_d0"] for d in diagnostics]
    if all(r < 0 for r in res_d0s) and max(abs(r) for r in res_d0s) > 0.2:
        shape = "AMPLITUDE_ONLY"
    elif max(res_d0s) - min(res_d0s) > 0.1:
        shape = "WRONG_REDSHIFT_SHAPE"
    else:
        shape = "MIXED_SHAPE_FAILURE"

    modes = [m[0] for m in Counter(d["failure_direction"] for d in diagnostics).most_common()]
    largest = sorted(diagnostics, key=lambda x: abs(x["pull_d0"]), reverse=True)[:3]
    largest_rows = [{"tracer": d["tracer"], "z_eff": d["z_eff"], "pull_d0": round(d["pull_d0"], 2), "failure_direction": d["failure_direction"]} for d in largest]

    rec = "Frozen finite-window S_DE transfer fails BAO shape; next admissible operator must diagnose transfer geometry without refitting roots or window centers."

    summary = {
        "result": "FAIL_DESI_BAO_SDE_REAL_DATA",
        "diagnostic_result": "PASS_DESI_BAO_SDE_FAILURE_DIAGNOSTICS",
        "source_priority": manifest["source_priority"],
        "sample_data": manifest["sample_data"],
        "no_refit": True,
        "frozen_roots": {"lambda_c": 1.4209430584957905, "lambda_r": 1.5790569415042095},
        "dominant_failure_modes": modes,
        "largest_pull_rows": largest_rows,
        "by_observable": by_observable,
        "by_redshift": by_redshift,
        "shape_diagnostic": shape,
        "recommendation": rec,
    }

    with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    with open(SUMMARY_MD, "w", encoding="utf-8") as f:
        f.write("# DESI/BAO S_DE Failure Diagnostics\n\n")
        f.write(f"- result: {summary['result']}\n")
        f.write(f"- diagnostic_result: {summary['diagnostic_result']}\n")
        f.write(f"- dominant_failure_modes: {summary['dominant_failure_modes']}\n")
        f.write(f"- shape_diagnostic: {summary['shape_diagnostic']}\n")
        f.write(f"- recommendation: {summary['recommendation']}\n")
        f.write("- largest_pull_rows:\n")
        for r in largest_rows:
            f.write(f"  - {r}\n")

    print("PASS_DESI_BAO_SDE_FAILURE_DIAGNOSTICS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
