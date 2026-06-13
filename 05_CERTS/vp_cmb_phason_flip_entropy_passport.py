#!/usr/bin/env python3
"""Planck CMB phason-flip entropy external passport."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "PlanckCMB"
MANIFEST = PASSPORT_DIR / "planck_manifest.json"
RESULTS_CSV = PASSPORT_DIR / "planck_phason_flip_results.csv"
SUMMARY = PASSPORT_DIR / "planck_phason_flip_summary.json"
SKIP_TOKEN = "SKIP_CMB_PHASON_FLIP_EXTERNAL_DATA_REQUIRED"
PASS_TOKEN = "PASS_CMB_PHASON_FLIP_ENTROPY_PASSPORT"
SYNTHETIC_TOKEN = "PASS_CMB_PHASON_FLIP_ENTROPY_SYNTHETIC"


def default_manifest() -> dict[str, Any]:
    return {
        "dataset_id": "planck_cmb_phason_flip_entropy",
        "source_name": "Planck PR3/legacy CMB likelihood products",
        "source_url": "https://pla.esac.esa.int/",
        "download_url": "",
        "local_path": "",
        "sha256": "",
        "downloaded_at_utc": "",
        "data_fields_required": ["cl_spectrum", "mask_or_likelihood", "multipole_range", "sha256"],
        "data_fields_found": [],
        "license_or_policy_note": "Use Planck Legacy Archive policy and citation.",
        "citation_note": "Pin exact Planck product IDs and likelihood version.",
        "status": "MISSING",
    }


def ensure_manifest() -> dict[str, Any]:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not MANIFEST.exists():
        MANIFEST.write_text(json.dumps(default_manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not RESULTS_CSV.exists():
        RESULTS_CSV.write_text("ell,cl_obs,cl_baseline,d0_template,residual,status\n", encoding="utf-8")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def missing_fields(data: dict[str, Any]) -> list[str]:
    missing = [f for f in data.get("data_fields_required", []) if f not in data.get("data_fields_found", [])]
    if data.get("status") != "READY":
        missing.append("status_READY")
    if not data.get("sha256") and "sha256" not in missing:
        missing.append("sha256")
    return missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["synthetic", "manifest_only", "planck_pr3"], default="manifest_only")
    args = ap.parse_args()
    data = ensure_manifest()
    if args.mode == "synthetic":
        status, missing = SYNTHETIC_TOKEN, []
    else:
        missing = missing_fields(data)
        status = SKIP_TOKEN if missing else PASS_TOKEN
    SUMMARY.write_text(json.dumps({"mode": args.mode, "status": status, "missing": missing}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(status)
    if missing:
        print("missing:", ",".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
