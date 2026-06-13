#!/usr/bin/env python3
"""SPARC archive-phason halo external passport."""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "SPARC"
MANIFEST = PASSPORT_DIR / "sparc_manifest.json"
RESULTS_CSV = PASSPORT_DIR / "sparc_phason_halo_results.csv"
SUMMARY = PASSPORT_DIR / "sparc_phason_halo_summary.json"
SKIP_TOKEN = "SKIP_ARCHIVE_PHASON_HALO_EXTERNAL_DATA_REQUIRED"
PASS_TOKEN = "PASS_ARCHIVE_PHASON_HALO_SPARC"
PASS_INGEST_TOKEN = "PASS_SPARC_DATA_INGEST"
FAIL_SHAPE_TOKEN = "FAIL_ARCHIVE_PHASON_HALO_SPARC_SHAPE_ONLY"
FAIL_GLOBAL_TOKEN = "FAIL_ARCHIVE_PHASON_HALO_SPARC_ONE_GLOBAL_SCALE"
SYNTHETIC_TOKEN = "PASS_SPARC_ARCHIVE_PHASON_HALO_SYNTHETIC"


def default_manifest() -> dict[str, Any]:
    return {
        "dataset_id": "sparc_archive_phason_halo",
        "source_name": "SPARC galaxy rotation-curve database",
        "source_url": "https://astroweb.cwru.edu/SPARC/",
        "download_url": "",
        "local_path": "",
        "sha256": "",
        "downloaded_at_utc": "",
        "data_fields_required": ["galaxy_id", "radius", "v_obs", "v_gas", "v_disk", "v_bulge", "sha256"],
        "data_fields_found": [],
        "license_or_policy_note": "Use the SPARC release policy and citation.",
        "citation_note": "Pin exact SPARC table/version before external PASS.",
        "status": "MISSING",
    }


def ensure_manifest() -> dict[str, Any]:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    if not MANIFEST.exists():
        MANIFEST.write_text(json.dumps(default_manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not RESULTS_CSV.exists():
        RESULTS_CSV.write_text("galaxy_id,rmse_d0,rmse_baryon_only,chi2_d0,chi2_baryon_only,status\n", encoding="utf-8")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def missing_fields(data: dict[str, Any]) -> list[str]:
    missing = [f for f in data.get("data_fields_required", []) if f not in data.get("data_fields_found", [])]
    if data.get("status") != "READY":
        missing.append("status_READY")
    if not data.get("sha256") and "sha256" not in missing:
        missing.append("sha256")
    return missing


def write_summary(mode: str, status: str, missing: list[str]) -> None:
    SUMMARY.write_text(
        json.dumps({"mode": mode, "status": status, "manifest": str(MANIFEST.relative_to(ROOT)).replace("\\", "/"), "missing": missing}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_sparc_mass_models(path: Path) -> list[dict[str, float | str]]:
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) != 10:
            continue
        try:
            row = {
                "galaxy_id": parts[0],
                "distance_mpc": float(parts[1]),
                "radius_kpc": float(parts[2]),
                "v_obs": float(parts[3]),
                "v_obs_err": float(parts[4]),
                "v_gas": float(parts[5]),
                "v_disk": float(parts[6]),
                "v_bulge": float(parts[7]),
                "v_baryon_ml1": (float(parts[5]) ** 2 + float(parts[6]) ** 2 + float(parts[7]) ** 2) ** 0.5,
            }
        except ValueError:
            continue
        rows.append(row)
    return rows


def write_sparc_rows(rows: list[dict[str, float | str]]) -> None:
    if rows:
        with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def pearson(xs: list[float], ys: list[float]) -> float | None:
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    if den == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def sparc_shape_run(rows: list[dict[str, float | str]], one_global_scale: bool) -> tuple[str, dict[str, object]]:
    phi = (1.0 + 5.0**0.5) / 2.0
    by_galaxy: dict[str, list[dict[str, float | str]]] = {}
    for row in rows:
        by_galaxy.setdefault(str(row["galaxy_id"]), []).append(row)
    all_x: list[float] = []
    all_y: list[float] = []
    correlations: list[float] = []
    out_rows: list[dict[str, object]] = []
    for galaxy, galaxy_rows in by_galaxy.items():
        rs = sorted(galaxy_rows, key=lambda r: float(r["radius_kpc"]))
        if len(rs) < 5:
            continue
        max_r = max(float(r["radius_kpc"]) for r in rs)
        scale = max_r / phi if max_r > 0 else 1.0
        abar = [float(r["v_baryon_ml1"]) ** 2 / float(r["radius_kpc"]) for r in rs]
        target = [max(float(r["v_obs"]) ** 2 - float(r["v_baryon_ml1"]) ** 2, 0.0) / float(r["radius_kpc"]) for r in rs]
        response: list[float] = []
        for i, row in enumerate(rs):
            ri = float(row["radius_kpc"])
            s = 0.0
            for j, source in enumerate(rs[: i + 1]):
                rj = float(source["radius_kpc"])
                prev = abar[j - 1] if j > 0 else 0.0
                d_abar = max(abar[j] - prev, 0.0)
                s += math.exp(-(ri - rj) / scale) * d_abar
            response.append(s)
        if max(response) > 0 and max(target) > 0:
            xr = math.sqrt(sum(x * x for x in response) / len(response))
            yr = math.sqrt(sum(y * y for y in target) / len(target))
            corr = pearson([x / xr for x in response], [y / yr for y in target])
            if corr is not None:
                correlations.append(corr)
        all_x.extend(response)
        all_y.extend(target)
        for source, x, y in zip(rs, response, target):
            out_rows.append({**source, "target_archive_accel": y, "d0_shape_response": x})
    if not all_x or not all_y:
        return SKIP_TOKEN, {"missing": ["shape_rows"]}
    gamma = sum(x * y for x, y in zip(all_x, all_y)) / sum(x * x for x in all_x) if sum(x * x for x in all_x) else 0.0
    pred = [gamma * x for x in all_x] if one_global_scale else all_x
    if not one_global_scale:
        # Shape-only is judged by per-galaxy normalized correlation, not amplitude.
        passed = bool(correlations) and statistics.median(correlations) > 0.0 and sum(c > 0 for c in correlations) > len(correlations) / 2
        status = PASS_TOKEN if passed else FAIL_SHAPE_TOKEN
    else:
        rmse_d0 = math.sqrt(sum((p - y) ** 2 for p, y in zip(pred, all_y)) / len(all_y))
        rmse_zero = math.sqrt(sum(y * y for y in all_y) / len(all_y))
        passed = rmse_d0 < 0.98 * rmse_zero
        status = PASS_TOKEN if passed else FAIL_GLOBAL_TOKEN
    write_sparc_rows(out_rows)
    return status, {
        "rows_used": len(all_y),
        "galaxies_used": len({str(r["galaxy_id"]) for r in rows}),
        "median_shape_correlation": statistics.median(correlations) if correlations else None,
        "positive_shape_correlations": sum(c > 0 for c in correlations),
        "shape_correlations_count": len(correlations),
        "global_gamma": gamma,
        "rmse_d0_global_scale": math.sqrt(sum((gamma * x - y) ** 2 for x, y in zip(all_x, all_y)) / len(all_y)),
        "rmse_baryon_only_residual": math.sqrt(sum(y * y for y in all_y) / len(all_y)),
        "forbidden": ["per-galaxy halo tuning", "per-galaxy scale radius", "post-hoc MOND-like acceleration fitting"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["synthetic", "manifest_only", "sparc", "shape_only", "one_global_scale"], default="manifest_only")
    args = ap.parse_args()
    data = ensure_manifest()
    if args.mode == "synthetic":
        write_summary(args.mode, SYNTHETIC_TOKEN, [])
        print(SYNTHETIC_TOKEN)
        return 0
    missing = missing_fields(data)
    local_path = data.get("local_path", "")
    if local_path and not (ROOT / local_path).exists():
        missing.append("local_file")
    if missing:
        write_summary(args.mode, SKIP_TOKEN, missing)
        print(SKIP_TOKEN)
        print("missing:", ",".join(missing))
        return 0
    rows = parse_sparc_mass_models(ROOT / local_path)
    if args.mode in {"shape_only", "one_global_scale"}:
        status, summary = sparc_shape_run(rows, one_global_scale=args.mode == "one_global_scale")
        SUMMARY.write_text(json.dumps({"mode": args.mode, "status": status, **summary}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(status)
        print(f"rows_used: {summary['rows_used']}")
        print(f"median_shape_correlation: {summary['median_shape_correlation']}")
        print(f"rmse_d0_global_scale: {summary['rmse_d0_global_scale']:.6g}")
        print(f"rmse_baryon_only_residual: {summary['rmse_baryon_only_residual']:.6g}")
        return 0
    write_sparc_rows(rows)
    status = PASS_INGEST_TOKEN
    SUMMARY.write_text(
        json.dumps(
            {
                "mode": args.mode,
                "status": status,
                "manifest": str(MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "rows_parsed": len(rows),
                "galaxies_parsed": len({str(r["galaxy_id"]) for r in rows}),
                "meaning": "Data-ingest PASS only. This is not a dark-sector physics PASS.",
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(status)
    print(f"rows_parsed: {len(rows)}")
    print(f"galaxies_parsed: {len({str(r['galaxy_id']) for r in rows})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
