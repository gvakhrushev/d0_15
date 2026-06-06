#!/usr/bin/env python3
"""
Optional helper: download DESI DR2 BAO data and update manifest.

In production: point to official DESI DR2 cosmology products / BAO measurements + covariance.
For this run the main cert creates a minimal pinned sample if data is absent.
"""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
import hashlib

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "08_PASSPORTS" / "DESI" / "desi_dr2_manifest.json"
CACHE = ROOT / "08_PASSPORTS" / "_EXTERNAL_DATA_CACHE" / "desi_bao"

def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    m = {
        "dataset_id": "DESI_DR2_BAO",
        "source_name": "DESI DR2 BAO public data release (official)",
        "source_url": "https://data.desi.lbl.gov/public/dr2/",
        "download_url": "Replace with exact official DESI DR2 BAO table + full covariance release",
        "local_path": str(CACHE / "desi_dr2_bao_sample.csv"),
        "sha256": "",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_fields_required": ["z_eff", "dm_rd", "dh_rd", "covariance"],
        "data_fields_found": ["z_eff", "dm_rd", "dh_rd", "cov_diag"],
        "license_or_policy_note": "Use DESI public-data policy and cite the release.",
        "citation_note": "Pin exact DESI DR2 BAO table/covariance release.",
        "status": "PARTIAL",
        "note": "Sample data created for hard-run demo. Replace with official pinned files for production."
    }
    MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Manifest updated. For real run: download official DESI DR2 BAO data to the local_path and set status=READY with full cov.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
