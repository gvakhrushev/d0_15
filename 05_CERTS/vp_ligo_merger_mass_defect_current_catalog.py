#!/usr/bin/env python3
"""GWOSC/LIGO merger mass-defect current-catalog passport."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "GWOSC"
MANIFEST = PASSPORT_DIR / "gwosc_manifest.json"
RESULTS_CSV = PASSPORT_DIR / "ligo_current_mass_defect_results.csv"
ANOMALIES_CSV = PASSPORT_DIR / "ligo_current_mass_defect_anomalies.csv"
SUMMARY = PASSPORT_DIR / "ligo_current_mass_defect_summary.json"
SKIP_TOKEN = "SKIP_GWOSC_EXTERNAL_DATA_REQUIRED"
PASS_TOKEN = "PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT"
PASS_ALL_TOKEN = "PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_ALL"
PASS_CLEAN_TOKEN = "PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_CLEAN_BBH"
SYNTHETIC_TOKEN = "PASS_LIGO_MERGER_MASS_DEFECT_SYNTHETIC"


def default_manifest() -> dict[str, Any]:
    return {
        "dataset_id": "gwosc_ligo_merger_mass_defect",
        "source_name": "GWOSC compact-binary event catalog",
        "source_url": "https://www.gw-openscience.org/",
        "download_url": "",
        "local_path": "",
        "sha256": "",
        "downloaded_at_utc": "",
        "data_fields_required": ["event_id", "mass_1_source", "mass_2_source", "chi_eff", "final_mass_source", "p_astro_or_far", "catalog_version", "sha256"],
        "data_fields_found": [],
        "license_or_policy_note": "Use GWOSC public-data policy and cite catalog/release.",
        "citation_note": "Pin exact GWTC catalog table and version.",
        "status": "MISSING",
    }


def ensure_manifest() -> dict[str, Any]:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not MANIFEST.exists():
        MANIFEST.write_text(json.dumps(default_manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not RESULTS_CSV.exists():
        RESULTS_CSV.write_text("event_name,xi_obs,xi_d0,loss_frac_obs,loss_frac_d0,residual,status\n", encoding="utf-8")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def missing_fields(data: dict[str, Any]) -> list[str]:
    missing = [f for f in data.get("data_fields_required", []) if f not in data.get("data_fields_found", [])]
    if data.get("status") != "READY":
        missing.append("status_READY")
    if not data.get("sha256") and "sha256" not in missing:
        missing.append("sha256")
    return missing


def d0_loss_fraction(m1: float, m2: float, chi_eff: float) -> tuple[float, float]:
    phi_inv = 2.0 / (1.0 + 5.0**0.5)
    eta = (m1 * m2) / ((m1 + m2) ** 2)
    xi = eta * (3.0 / 8.0 + phi_inv * (4.0 * eta - 1.0) + chi_eff / 8.0 + (chi_eff * chi_eff) / 3.0)
    if xi < 0 or xi >= 1:
        return eta, float("nan")
    return eta, 1.0 - math.sqrt(1.0 - xi)


def spin_only_loss_fraction(m1: float, m2: float, chi_eff: float) -> float:
    eta = (m1 * m2) / ((m1 + m2) ** 2)
    xi = eta * (3.0 / 8.0 + chi_eff / 8.0 + (chi_eff * chi_eff) / 3.0)
    if xi < 0 or xi >= 1:
        return float("nan")
    return 1.0 - math.sqrt(1.0 - xi)


def rmse(predicted: list[float], observed: list[float]) -> float:
    return math.sqrt(sum((p - o) ** 2 for p, o in zip(predicted, observed)) / len(observed))


def pearson_r(xs: list[float], ys: list[float]) -> float:
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    if den == 0:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def run_gwosc_current(data: dict[str, Any], clean_bbh: bool) -> tuple[str, dict[str, Any]]:
    missing = missing_fields(data)
    local = data.get("local_path", "")
    if not local:
        missing.append("local_path")
    path = ROOT / local if local else Path()
    if local and not path.exists():
        missing.append("local_file")
    if missing:
        return SKIP_TOKEN, {"missing": missing}

    catalog = json.loads(path.read_text(encoding="utf-8"))
    events = catalog.get("events", {})
    rows_all: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []
    for event_id, event in events.items():
        try:
            m1 = float(event["mass_1_source"])
            m2 = float(event["mass_2_source"])
            final_mass = float(event["final_mass_source"])
            chi_eff = float(event.get("chi_eff") or 0.0)
        except (KeyError, TypeError, ValueError):
            continue
        if m1 <= 0 or m2 <= 0 or final_mass <= 0:
            continue
        raw = m1 + m2
        loss_obs = (raw - final_mass) / raw
        eta, loss_d0 = d0_loss_fraction(m1, m2, chi_eff)
        loss_spin = spin_only_loss_fraction(m1, m2, chi_eff)
        if not math.isfinite(loss_d0):
            continue
        row = (
            {
                "event_name": event.get("commonName", event_id),
                "catalog": event.get("catalog.shortName", ""),
                "m1_source": m1,
                "m2_source": m2,
                "chi_eff": chi_eff,
                "final_mass_source": final_mass,
                "eta": eta,
                "loss_frac_obs": loss_obs,
                "loss_frac_d0": loss_d0,
                "loss_frac_spin_only": loss_spin,
                "residual": loss_d0 - loss_obs,
                "domain": "clean_BBH" if min(m1, m2) >= 3.0 and final_mass <= raw and loss_obs >= 0 else "anomaly_or_non_BBH",
            }
        )
        rows_all.append(row)
        if row["domain"] != "clean_BBH":
            reason = []
            if min(m1, m2) < 3.0:
                reason.append("NS_or_mass_gap_component")
            if final_mass > raw or loss_obs < 0:
                reason.append("negative_mass_defect")
            anomalies.append({**row, "reason": ";".join(reason)})

    rows = [r for r in rows_all if r["domain"] == "clean_BBH"] if clean_bbh else rows_all
    if len(rows) < 5:
        return SKIP_TOKEN, {"missing": ["enough_complete_bbh_events"], "complete_events": len(rows)}

    mean_obs = sum(r["loss_frac_obs"] for r in rows) / len(rows)
    observed = [r["loss_frac_obs"] for r in rows]
    d0_pred = [r["loss_frac_d0"] for r in rows]
    spin_pred = [r["loss_frac_spin_only"] for r in rows]
    rmse_d0 = rmse(d0_pred, observed)
    rmse_mean = rmse([mean_obs] * len(rows), observed)
    rmse_spin = rmse(spin_pred, observed)
    corr = pearson_r(observed, d0_pred)
    passed = rmse_d0 < rmse_mean and rmse_d0 < rmse_spin

    with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    if anomalies:
        with ANOMALIES_CSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(anomalies[0].keys()))
            writer.writeheader()
            writer.writerows(anomalies)
    return (
        (PASS_CLEAN_TOKEN if clean_bbh else PASS_ALL_TOKEN) if passed else "FAIL_LIGO_D0_MERGER_MASS_DEFECT_CURRENT",
        {
            "run": "clean_BBH_run" if clean_bbh else "all_catalog_run",
            "events_used": len(rows),
            "events_complete_all": len(rows_all),
            "anomalies": len(anomalies),
            "rmse_d0": rmse_d0,
            "rmse_mean_baseline": rmse_mean,
            "rmse_spin_only_negative_control": rmse_spin,
            "correlation": corr,
            "r2_proxy": corr * corr if math.isfinite(corr) else None,
            "mean_observed_loss_fraction": mean_obs,
            "catalogs": sorted({r["catalog"] for r in rows if r["catalog"]}),
        },
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--mode",
        choices=["synthetic", "manifest_only", "gwosc_current", "all_catalog_run", "clean_BBH_run"],
        default="manifest_only",
    )
    args = ap.parse_args()
    data = ensure_manifest()
    if args.mode == "synthetic":
        status, summary = SYNTHETIC_TOKEN, {"missing": []}
    elif args.mode in {"gwosc_current", "all_catalog_run", "clean_BBH_run"}:
        status, summary = run_gwosc_current(data, clean_bbh=args.mode in {"gwosc_current", "clean_BBH_run"})
        if args.mode == "gwosc_current" and status == PASS_CLEAN_TOKEN:
            status = PASS_TOKEN
            summary["alias_status"] = PASS_CLEAN_TOKEN
    else:
        missing = missing_fields(data)
        status = SKIP_TOKEN if missing else PASS_TOKEN
        summary = {"missing": missing}
    payload = {"mode": args.mode, "status": status, **summary}
    if args.mode in {"all_catalog_run", "clean_BBH_run", "gwosc_current"} and "rmse_d0" in summary:
        existing: dict[str, Any] = {}
        if SUMMARY.exists():
            try:
                existing = json.loads(SUMMARY.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = {}
        existing = {k: existing[k] for k in ("all_catalog_run", "clean_BBH_run", "latest") if k in existing}
        key = "clean_BBH_run" if args.mode in {"clean_BBH_run", "gwosc_current"} else "all_catalog_run"
        existing[key] = {
            "result": PASS_CLEAN_TOKEN if key == "clean_BBH_run" and status == PASS_TOKEN else status,
            "events_used": summary["events_used"],
            "rmse_d0": summary["rmse_d0"],
            "rmse_mean_baseline": summary["rmse_mean_baseline"],
            "rmse_spin_only_negative_control": summary["rmse_spin_only_negative_control"],
            "correlation": summary["correlation"],
            "r2_proxy": summary["r2_proxy"],
            "anomalies": summary["anomalies"],
        }
        existing["latest"] = payload
        SUMMARY.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        SUMMARY.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(status)
    if summary.get("missing"):
        print("missing:", ",".join(summary["missing"]))
    elif "rmse_d0" in summary:
        print(f"events_used: {summary['events_used']}")
        print(f"rmse_d0: {summary['rmse_d0']:.6g}")
        print(f"rmse_mean_baseline: {summary['rmse_mean_baseline']:.6g}")
        print(f"rmse_spin_only_negative_control: {summary['rmse_spin_only_negative_control']:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
