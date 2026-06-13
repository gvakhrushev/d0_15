#!/usr/bin/env python3
"""PDG meson domain-wall external passport."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "PDG_Meson"
MANIFEST = PASSPORT_DIR / "pdg_meson_manifest.json"
RESULTS_CSV = PASSPORT_DIR / "meson_domain_wall_pdg_results.csv"
SUMMARY = PASSPORT_DIR / "pdg_meson_domain_wall_summary.json"
SKIP_TOKEN = "SKIP_PDG_MESON_EXTERNAL_DATA_REQUIRED"
PASS_TOKEN = "PASS_MESON_DOMAIN_WALL_PDG_PASSPORT"
SYNTHETIC_TOKEN = "PASS_MESON_DOMAIN_WALL_PDG_SYNTHETIC"


def default_manifest() -> dict[str, Any]:
    return {
        "dataset_id": "meson_domain_wall_pdg",
        "source_name": "PDG meson mass/width table",
        "source_url": "https://pdg.lbl.gov/",
        "download_url": "",
        "local_path": "",
        "sha256": "",
        "downloaded_at_utc": "",
        "data_fields_required": ["particle_id", "mass", "width", "quantum_numbers", "sha256"],
        "data_fields_found": [],
        "license_or_policy_note": "Use PDG citation/policy and pinned table year.",
        "citation_note": "Pin exact PDG mass-width table year.",
        "status": "MISSING",
    }


def ensure_manifest() -> dict[str, Any]:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not MANIFEST.exists():
        MANIFEST.write_text(json.dumps(default_manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not RESULTS_CSV.exists():
        RESULTS_CSV.write_text("particle_id,mass,width,k0_label,domain_wall_class,residual,status\n", encoding="utf-8")
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
    ap.add_argument("--mode", choices=["synthetic", "manifest_only", "pdg"], default="manifest_only")
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
