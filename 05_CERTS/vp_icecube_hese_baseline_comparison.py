#!/usr/bin/env python3
"""IceCube HESE baseline-comparison gate.

This certificate is intentionally conservative: the HESE event table and D0
curve are sufficient for an observable layer, but this repo does not yet carry a
defensible no-decoherence exposure/flux baseline. The correct result is a
baseline-specific SKIP, not PASS.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "IceCube"
MANIFEST = PASSPORT_DIR / "icecube_manifest.json"
CURVE = PASSPORT_DIR / "icecube_phason_decoherence_curve.csv"
PROTOCOL = PASSPORT_DIR / "icecube_baseline_protocol.md"
SUMMARY = PASSPORT_DIR / "icecube_hese_baseline_summary.json"

PASS_TOKEN = "PASS_ICECUBE_PHASON_DECOHERENCE_HESE12"
FAIL_TOKEN = "FAIL_ICECUBE_PHASON_DECOHERENCE_HESE12"
SKIP_TOKEN = "SKIP_NEUTRINO_PHASON_DECOHERENCE_BASELINE_REQUIRED"


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def hese_event_path(manifest: dict[str, Any]) -> Path | None:
    for item in manifest.get("files", []):
        if item.get("label") == "hese12_events":
            return ROOT / item["local_path"]
    local = manifest.get("local_path") or manifest.get("source_url_or_local_path")
    return ROOT / local if local else None


def count_rows(path: Path | None) -> tuple[int, list[str]]:
    if path is None or not path.exists():
        return 0, []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields = list(reader.fieldnames or [])
        count = sum(1 for _ in reader)
    return count, fields


def curve_rows() -> int:
    if not CURVE.exists():
        return 0
    with CURVE.open("r", encoding="utf-8", newline="") as f:
        return max(sum(1 for _ in f) - 1, 0)


def main() -> int:
    manifest = load_manifest()
    event_count, fields = count_rows(hese_event_path(manifest))
    curve_count = curve_rows()
    baseline_ready = False
    summary = {
        "status": SKIP_TOKEN,
        "allowed_pass_token": PASS_TOKEN,
        "allowed_fail_token": FAIL_TOKEN,
        "dataset": "IceCube HESE 12-year event table",
        "manifest": str(MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "protocol": str(PROTOCOL.relative_to(ROOT)).replace("\\", "/"),
        "events_used": event_count,
        "fields_found": fields,
        "curve_rows": curve_count,
        "observable": "energy-binned event survival / suppression shape",
        "secondary_observable": "track/cascade reconstruction ratio versus energy when topology is present",
        "baseline_ready": baseline_ready,
        "reason": (
            "HESE event layer and D0 damping curve exist, but no published "
            "HESE exposure/flux or no-decoherence null baseline is pinned here."
        ),
        "forbidden": [
            "free damping exponent as core",
            "free threshold tuned after HESE",
            "post-hoc topology selection",
            "discarding events after seeing result",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(SKIP_TOKEN)
    print(f"events_used: {event_count}")
    print(f"curve_rows: {curve_count}")
    print("baseline_ready: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
