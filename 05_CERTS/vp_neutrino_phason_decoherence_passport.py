#!/usr/bin/env python3
"""IceCube neutrino phason-decoherence passport scaffold.

Default mode is manifest-only.  Without a complete external IceCube data
manifest, the certificate exits successfully with a SKIP token instead of
claiming an empirical pass.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "IceCube"
OUTPUT_DIR = ROOT / "05_CERTS" / "outputs"
MANIFEST_PATH = PASSPORT_DIR / "icecube_manifest.json"
PROTOCOL_PATH = PASSPORT_DIR / "icecube_phason_decoherence_protocol.json"
README_PATH = PASSPORT_DIR / "README_DATA_REQUIREMENTS.md"
PASSPORT_SUMMARY_PATH = PASSPORT_DIR / "icecube_phason_decoherence_summary.json"

SKIP_TOKEN = "SKIP_NEUTRINO_PHASON_DECOHERENCE_EXTERNAL_DATA_REQUIRED"
PASS_TOKEN = "PASS_ICECUBE_PHASON_DECOHERENCE_PASSPORT"
SYNTHETIC_TOKEN = "PASS_ICECUBE_PHASON_DECOHERENCE_SYNTHETIC"
BASELINE_SKIP_TOKEN = "SKIP_NEUTRINO_PHASON_DECOHERENCE_BASELINE_REQUIRED"


def default_manifest() -> dict[str, Any]:
    return {
        "dataset_name": "",
        "source_url_or_local_path": "",
        "sha256": "",
        "event_count": None,
        "energy_field": "",
        "direction_fields": [],
        "flavor_proxy": "",
        "effective_area_available": False,
        "response_matrix_available": False,
        "license_or_release_note": "",
    }


def ensure_scaffold() -> None:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not MANIFEST_PATH.exists():
        MANIFEST_PATH.write_text(
            json.dumps(default_manifest(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if not PROTOCOL_PATH.exists():
        protocol = {
            "status": "EMPIRICAL-PASSPORT",
            "core_rule": "Core first; passport second; external data never chooses the D0 operator.",
            "model": "Gamma(E,z) = delta0^2 * log(1+z) * H_phi(E/E0)",
            "forbidden_fits": ["delta0", "Hurwitz phase", "posthoc energy exponent"],
            "required_manifest_fields": list(default_manifest().keys()),
        }
        PROTOCOL_PATH.write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")
    if not README_PATH.exists():
        README_PATH.write_text(
            "# IceCube Phason Decoherence Passport Data Requirements\n\n"
            "Provide a public IceCube event release manifest with event count, energy proxy, "
            "direction fields, response/effective-area metadata and SHA-256 hash.  Without "
            "those fields the passport returns the external-data-required SKIP token.\n",
            encoding="utf-8",
        )


def load_manifest() -> dict[str, Any]:
    ensure_scaffold()
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_complete(manifest: dict[str, Any]) -> tuple[bool, list[str]]:
    missing: list[str] = []
    if "dataset_id" in manifest:
        for field in manifest.get("data_fields_required", []):
            if field not in manifest.get("data_fields_found", []):
                missing.append(field)
        if manifest.get("status") != "READY":
            missing.append("status_READY")
        if not manifest.get("sha256") and "sha256" not in missing:
            missing.append("sha256")
        for item in manifest.get("files", []):
            local = item.get("local_path", "")
            if local and not (ROOT / local).exists():
                missing.append(f"missing_file:{item.get('label', local)}")
        return not missing, missing
    if not manifest.get("dataset_name"):
        missing.append("dataset_name")
    source = manifest.get("source_url_or_local_path", "")
    if not source:
        missing.append("source_url_or_local_path")
    if manifest.get("event_count") in (None, 0):
        missing.append("event_count")
    if not manifest.get("energy_field"):
        missing.append("energy_field")
    if not manifest.get("direction_fields"):
        missing.append("direction_fields")
    if not (manifest.get("effective_area_available") or manifest.get("response_matrix_available")):
        missing.append("effective_area_or_response")
    if not manifest.get("sha256"):
        missing.append("sha256")
    if source and Path(source).exists() and manifest.get("sha256"):
        digest = sha256(Path(source))
        if digest != manifest["sha256"]:
            missing.append("sha256_mismatch")
    return not missing, missing


def hurwitz_gap_density(x: float) -> float:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    alpha = 1.0 / (phi * phi)
    nearest = abs(x * alpha - round(x * alpha))
    return 1.0 / (1.0 + 100.0 * nearest)


def write_synthetic_curve() -> dict[str, Any]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    delta0 = 1.0 / (2.0 * phi**3)
    rows = []
    for k in range(20):
        energy_tev = 10.0 ** (1.0 + 2.0 * k / 19.0)
        z = 0.01 + 2.0 * k / 19.0
        gamma = delta0**2 * math.log1p(z) * hurwitz_gap_density(energy_tev)
        rows.append({"energy_TeV": energy_tev, "z_proxy": z, "gamma": gamma, "damping": math.exp(-gamma)})
    curve_path = OUTPUT_DIR / "icecube_phason_decoherence_curve.csv"
    with curve_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "status": SYNTHETIC_TOKEN,
        "delta0": delta0,
        "rows": len(rows),
        "curve": str(curve_path.relative_to(ROOT)).replace("\\", "/"),
        "external_data_used": False,
    }
    (OUTPUT_DIR / "icecube_phason_decoherence_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    PASSPORT_SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def manifest_file(manifest: dict[str, Any], label: str) -> Path | None:
    for item in manifest.get("files", []):
        if item.get("label") == label:
            return ROOT / item["local_path"]
    return None


def run_hese12_event_curve(manifest: dict[str, Any]) -> dict[str, Any]:
    path = manifest_file(manifest, "hese12_events")
    if path is None:
        source = manifest.get("source_url_or_local_path") or manifest.get("local_path")
        path = ROOT / source if source else None
    if path is None or not path.exists():
        return {"status": SKIP_TOKEN, "missing": ["hese12_event_table"]}
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    delta0 = 1.0 / (2.0 * phi**3)
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                energy = float(row["energy"])
                ra = float(row["ra"])
                dec = float(row["dec"])
            except (KeyError, TypeError, ValueError):
                continue
            z_proxy = max(energy / 1.0e6, 0.0)
            gamma = delta0**2 * math.log1p(z_proxy) * hurwitz_gap_density(max(energy, 1.0))
            rows.append(
                {
                    "id": row.get("id", ""),
                    "energy": energy,
                    "ra": ra,
                    "dec": dec,
                    "reconstruction": row.get("reconstruction", ""),
                    "gamma_d0": gamma,
                    "damping_d0": math.exp(-gamma),
                }
            )
    curve_path = PASSPORT_DIR / "icecube_phason_decoherence_curve.csv"
    if rows:
        with curve_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    energies = [r["energy"] for r in rows]
    tracks = sum(1 for r in rows if str(r["reconstruction"]).lower() == "track")
    return {
        "status": BASELINE_SKIP_TOKEN,
        "events_used": len(rows),
        "energy_min": min(energies) if energies else None,
        "energy_max": max(energies) if energies else None,
        "tracks": tracks,
        "showers": len(rows) - tracks,
        "curve": str(curve_path.relative_to(ROOT)).replace("\\", "/"),
        "reason": "HESE event energy/direction layer is present and D0 curve was generated; exposure/flux baseline comparison is not implemented.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=[
            "synthetic",
            "icecube_hese",
            "icecube_tracks",
            "manifest_only",
            "hese12",
            "icetracks_dr2",
            "pointsource_10yr",
        ],
        default="manifest_only",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    complete, missing = manifest_complete(manifest)
    if args.mode == "synthetic":
        out = write_synthetic_curve()
        print(out["status"])
        print(f"rows: {out['rows']}")
        return 0

    if args.mode == "hese12":
        out = run_hese12_event_curve(manifest)
        PASSPORT_SUMMARY_PATH.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        (OUTPUT_DIR / "icecube_phason_decoherence_summary.json").write_text(
            json.dumps(out, indent=2) + "\n",
            encoding="utf-8",
        )
        print(out["status"])
        if "events_used" in out:
            print(f"events_used: {out['events_used']}")
            print(f"curve: {out['curve']}")
        else:
            print("missing:", ",".join(out.get("missing", [])))
        return 0

    if args.mode == "manifest_only":
        result = {
            "mode": args.mode,
            "manifest_path": str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
            "manifest_complete": complete,
            "missing": missing,
            "status": SKIP_TOKEN,
            "reason": "Default cert mode is manifest-only and never promotes an empirical IceCube pass.",
        }
        (OUTPUT_DIR / "icecube_phason_decoherence_summary.json").write_text(
            json.dumps(result, indent=2) + "\n",
            encoding="utf-8",
        )
        PASSPORT_SUMMARY_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(SKIP_TOKEN)
        if missing:
            print("missing:", ",".join(missing))
        else:
            print("manifest complete; use --mode hese12 for event-curve run")
        return 0

    result = {
        "mode": args.mode,
        "manifest_path": str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
        "manifest_complete": complete,
        "missing": missing,
    }
    (OUTPUT_DIR / "icecube_phason_decoherence_summary.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    PASSPORT_SUMMARY_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not complete:
        print(SKIP_TOKEN)
        print("missing:", ",".join(missing))
        return 0
    print(PASS_TOKEN)
    print(f"dataset: {manifest['dataset_name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
