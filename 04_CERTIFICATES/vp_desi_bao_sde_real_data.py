#!/usr/bin/env python3
"""
D0_DESI_BAO_SDE_REAL_DATA_HARD_RUN

Historical D0 S_DE demo, not a real-data confrontation.
The executable entrypoint returns SKIP until a verified data, covariance and baseline pipeline exists.
It does not create synthetic inputs or overwrite the manifest/results.

Frozen polynomial: 160λ² - 480λ + 359
Roots:
  λ_c = 1.4209430584957905
  λ_r = 1.5790569415042095

No refit of roots, windows, H0, Ωm, rd, etc.
"""

from __future__ import annotations

import json
import math
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "05_EXPERIMENTS" / "DESI"
MANIFEST = PASSPORT_DIR / "desi_dr2_manifest.json"
RESULTS_CSV = PASSPORT_DIR / "desi_bao_sde_real_data_results.csv"
SUMMARY_JSON = PASSPORT_DIR / "desi_bao_sde_real_data_summary.json"
SUMMARY_MD = PASSPORT_DIR / "desi_bao_sde_real_data_summary.md"
CACHE_DIR = ROOT / "05_EXPERIMENTS" / "_EXTERNAL_DATA_CACHE" / "desi_bao"

# Frozen D0 S_DE
POLY_A = 160.0
POLY_B = -480.0
POLY_C = 359.0
LAMBDA_C_FROZEN = 1.4209430584957905
LAMBDA_R_FROZEN = 1.5790569415042095

# Sample frozen transfer params (from internal certs; do not refit)
Z_C = 0.5
Z_R = 2.0
SIGMA_C = 0.5
SIGMA_R = 1.0
A_C = 0.03
A_R = 0.025
THETA_0 = 0.01
XI_5 = 3.0

def G_log(z: float, z0: float, sigma: float) -> float:
    """Log-Gaussian window."""
    if sigma <= 0:
        return 0.0
    arg = (math.log(1 + z) - math.log(1 + z0)) / sigma
    return math.exp(-0.5 * arg * arg)

def theta_d0(z: float) -> float:
    """Frozen S_DE transfer shape (no tail refit)."""
    term_c = A_C * G_log(z, Z_C, SIGMA_C)
    term_r = A_R * G_log(z, Z_R, SIGMA_R)
    tail = THETA_0 * math.exp(- (z / XI_5)**2 )
    return term_c - term_r - tail

def load_or_create_manifest() -> dict[str, Any]:
    """Read the historical manifest without creating or modifying any inputs."""
    if not MANIFEST.is_file():
        return {"status": "MISSING", "sample_data": True}
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {"status": "INVALID", "sample_data": True}
    if not isinstance(manifest, dict):
        return {"status": "INVALID", "sample_data": True}
    return manifest

def load_data(manifest: dict[str, Any]) -> list[dict[str, float]]:
    """Read the declared legacy row format; never replace bad input with samples."""
    raw_path = manifest.get("local_path")
    if not isinstance(raw_path, str) or not raw_path:
        return []
    p = Path(raw_path)
    if not p.is_absolute():
        p = ROOT / p
    rows = []
    try:
        with p.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append({
                    "tracer": row["tracer"],
                    "z_eff": float(row["z_eff"]),
                    "dm_rd": float(row["dm_rd"]),
                    "dh_rd": float(row["dh_rd"]),
                    "cov_diag": float(row["cov_diag"]),
                })
    except (OSError, UnicodeError, csv.Error, KeyError, TypeError, ValueError):
        return []
    return rows

def compute_d0_values(rows: list[dict[str, float]]) -> list[float]:
    return [theta_d0(r["z_eff"]) for r in rows]

def compute_metrics(rows: list[dict[str, float]], d0_vals: list[float]) -> dict[str, Any]:
    """Historical demo arithmetic only; its placeholder baseline is not an observation test."""
    # Simple baselines
    # ΛCDM baseline: use observed as "baseline" for demo (in real, load published)
    baseline_vals = [r["dm_rd"] * 0.01 for r in rows]  # placeholder scaled residual shape
    flat_residual = [0.0 for _ in rows]

    # Assume diagonal cov for metric (real would use full cov)
    chi2_d0 = sum( ((d0 - r["dm_rd"]*0.01) / r["cov_diag"] )**2 for d0, r in zip(d0_vals, rows) )
    chi2_lcdm = sum( ((b - r["dm_rd"]*0.01) / r["cov_diag"] )**2 for b, r in zip(baseline_vals, rows) )
    delta_chi2 = chi2_d0 - chi2_lcdm

    rmse_d0 = math.sqrt( sum( (d0 - r["dm_rd"]*0.01)**2 for d0,r in zip(d0_vals, rows) ) / max(1, len(rows)) )
    rmse_lcdm = math.sqrt( sum( (b - r["dm_rd"]*0.01)**2 for b,r in zip(baseline_vals, rows) ) / max(1, len(rows)) )

    return {
        "chi2_d0": round(chi2_d0, 4),
        "chi2_lcdm_baseline": round(chi2_lcdm, 4),
        "delta_chi2": round(delta_chi2, 4),
        "rmse_d0": round(rmse_d0, 6),
        "rmse_lcdm_baseline": round(rmse_lcdm, 6),
        "n_bins": len(rows),
    }

def main() -> int:
    # No verified covariance/baseline pipeline is implemented here. In particular,
    # manifest READY flags cannot turn the historical demo into a physical test.
    print("SKIP_DESI_BAO_SDE_VALUE_PIPELINE_NOT_IMPLEMENTED")
    print("physical_result: SKIP_DESI_BAO_SDE_VALUE_PIPELINE_NOT_IMPLEMENTED")
    print("No synthetic data generated, no inputs or tracked results overwritten, "
          "and no observational PASS/FAIL asserted.")
    return 0

def parse_args():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="desi_dr2", choices=["desi_dr2", "desi_dr2_official"])
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # Both modes remain SKIP until an actual data-confrontation pipeline is implemented.
    raise SystemExit(main())
