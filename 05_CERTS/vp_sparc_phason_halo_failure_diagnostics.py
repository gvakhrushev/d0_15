#!/usr/bin/env python3
"""SPARC failure diagnostics for rejected archive-phason halo kernels."""
from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "SPARC"
MANIFEST = PASSPORT_DIR / "sparc_manifest.json"
DIAG_CSV = PASSPORT_DIR / "sparc_failure_diagnostics.csv"
SUMMARY_JSON = PASSPORT_DIR / "sparc_failure_summary.json"
SUMMARY_MD = PASSPORT_DIR / "sparc_failure_summary.md"
PASS_TOKEN = "PASS_SPARC_PHASON_HALO_FAILURE_DIAGNOSTICS"
FAIL_SHAPE = "FAIL_ARCHIVE_PHASON_HALO_SPARC_SHAPE_ONLY"
FAIL_GLOBAL = "FAIL_ARCHIVE_PHASON_HALO_SPARC_ONE_GLOBAL_SCALE"


def parse_sparc(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) != 10:
            continue
        try:
            vgas = float(parts[5])
            vdisk = float(parts[6])
            vbul = float(parts[7])
            rows.append(
                {
                    "galaxy": parts[0],
                    "radius": float(parts[2]),
                    "v_obs": float(parts[3]),
                    "v_err": float(parts[4]),
                    "v_gas": vgas,
                    "v_disk": vdisk,
                    "v_bulge": vbul,
                    "v_bar": math.sqrt(vgas * vgas + vdisk * vdisk + vbul * vbul),
                    "sb_disk": float(parts[8]),
                    "sb_bulge": float(parts[9]),
                }
            )
        except ValueError:
            continue
    return rows


def rmse(xs: list[float], ys: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(xs, ys)) / len(xs))


def phason_response(rows: list[dict[str, Any]]) -> list[float]:
    phi = (1.0 + 5.0**0.5) / 2.0
    rs = sorted(rows, key=lambda r: r["radius"])
    max_r = max(r["radius"] for r in rs)
    scale = max_r / phi if max_r > 0 else 1.0
    abar = [r["v_bar"] ** 2 / r["radius"] for r in rs]
    response: list[float] = []
    for i, row in enumerate(rs):
        ri = row["radius"]
        s = 0.0
        for j, source in enumerate(rs[: i + 1]):
            prev = abar[j - 1] if j > 0 else 0.0
            d_abar = max(abar[j] - prev, 0.0)
            s += math.exp(-(ri - source["radius"]) / scale) * d_abar
        response.append(s)
    return response


def classify(row: dict[str, Any]) -> str:
    if row["n_points"] < 5:
        return "INSUFFICIENT_POINTS"
    if row["gas_fraction_proxy"] > 0.6:
        return "GAS_DOMINATED"
    if row["disk_fraction_proxy"] > 0.7:
        return "DISK_DOMINATED"
    if row["delta_shape_vs_baryon"] > 0 and row["delta_global_vs_baryon"] > 0:
        return "GLOBAL_SHAPE"
    if row["inner_rmse"] > 1.25 * row["outer_rmse"]:
        return "INNER_SLOPE"
    if row["outer_rmse"] > 1.25 * row["inner_rmse"]:
        return "OUTER_TAIL"
    if abs(row["delta_shape_vs_baryon"]) < 0.05 * max(row["rmse_baryon_only"], 1.0):
        return "AMPLITUDE_ONLY"
    if row["surface_brightness_proxy"] < 1.0:
        return "LSB_CLASS"
    if row["surface_brightness_proxy"] > 20.0:
        return "HSB_CLASS"
    return "GLOBAL_SHAPE"


def main() -> int:
    if not MANIFEST.exists():
        print("SKIP_ARCHIVE_PHASON_HALO_EXTERNAL_DATA_REQUIRED")
        print("missing: sparc_manifest.json")
        return 0
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data_path = ROOT / manifest.get("local_path", "")
    if not data_path.exists():
        print("SKIP_ARCHIVE_PHASON_HALO_EXTERNAL_DATA_REQUIRED")
        print("missing: SPARC local data file")
        return 0
    rows = parse_sparc(data_path)
    by_galaxy: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_galaxy[row["galaxy"]].append(row)

    diagnostics: list[dict[str, Any]] = []
    global_pairs: list[tuple[float, float]] = []
    for galaxy, gal_rows in by_galaxy.items():
        rs = sorted(gal_rows, key=lambda r: r["radius"])
        if len(rs) < 2:
            continue
        obs = [r["v_obs"] for r in rs]
        bar = [r["v_bar"] for r in rs]
        response = phason_response(rs)
        target_accel = [max(r["v_obs"] ** 2 - r["v_bar"] ** 2, 0.0) / r["radius"] for r in rs]
        for x, y in zip(response, target_accel):
            global_pairs.append((x, y))
        rms_resp = math.sqrt(sum(x * x for x in response) / len(response)) or 1.0
        rms_obs = math.sqrt(sum(y * y for y in obs) / len(obs)) or 1.0
        shape_velocity = [x / rms_resp * rms_obs for x in response]
        rm_baryon = rmse(bar, obs)
        rm_shape = rmse(shape_velocity, obs)
        mid = max(1, len(rs) // 2)
        gas_power = sum(abs(r["v_gas"]) ** 2 for r in rs)
        disk_power = sum(abs(r["v_disk"]) ** 2 for r in rs)
        bulge_power = sum(abs(r["v_bulge"]) ** 2 for r in rs)
        total_power = gas_power + disk_power + bulge_power or 1.0
        diag = {
            "galaxy": galaxy,
            "n_points": len(rs),
            "quality_flag": "",
            "radius_min": min(r["radius"] for r in rs),
            "radius_max": max(r["radius"] for r in rs),
            "rmse_baryon_only": rm_baryon,
            "rmse_shape_only": rm_shape,
            "rmse_one_global_scale": 0.0,
            "delta_shape_vs_baryon": rm_shape - rm_baryon,
            "delta_global_vs_baryon": 0.0,
            "inner_rmse": rmse(shape_velocity[:mid], obs[:mid]),
            "outer_rmse": rmse(shape_velocity[mid:], obs[mid:]) if len(rs[mid:]) else rmse(shape_velocity[:mid], obs[:mid]),
            "gas_fraction_proxy": gas_power / total_power,
            "disk_fraction_proxy": disk_power / total_power,
            "bulge_present": bulge_power > 0,
            "surface_brightness_proxy": sum(r["sb_disk"] for r in rs) / len(rs),
        }
        diagnostics.append(diag)

    gamma = sum(x * y for x, y in global_pairs) / sum(x * x for x, _ in global_pairs)
    for diag in diagnostics:
        rs = sorted(by_galaxy[diag["galaxy"]], key=lambda r: r["radius"])
        obs = [r["v_obs"] for r in rs]
        response = phason_response(rs)
        global_velocity = [math.sqrt(max(r["v_bar"] ** 2 + gamma * x * r["radius"], 0.0)) for r, x in zip(rs, response)]
        diag["rmse_one_global_scale"] = rmse(global_velocity, obs)
        diag["delta_global_vs_baryon"] = diag["rmse_one_global_scale"] - diag["rmse_baryon_only"]
        diag["failure_class"] = classify(diag)

    with DIAG_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(diagnostics[0].keys()))
        writer.writeheader()
        writer.writerows(diagnostics)
    counts = Counter(d["failure_class"] for d in diagnostics)
    summary = {
        "rows_parsed": len(rows),
        "galaxies": len(by_galaxy),
        "shape_only_result": FAIL_SHAPE,
        "one_global_scale_result": FAIL_GLOBAL,
        "dominant_failure_modes": counts.most_common(),
        "recommendation": "Reject simple radial smoothing kernels. Next operator must include hull-boundary response without per-galaxy halo tuning.",
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    SUMMARY_MD.write_text(
        "# SPARC Failure Diagnostics\n\n"
        f"- rows_parsed: {summary['rows_parsed']}\n"
        f"- galaxies: {summary['galaxies']}\n"
        f"- shape_only_result: {FAIL_SHAPE}\n"
        f"- one_global_scale_result: {FAIL_GLOBAL}\n"
        f"- dominant_failure_modes: {summary['dominant_failure_modes']}\n"
        f"- recommendation: {summary['recommendation']}\n",
        encoding="utf-8",
    )
    print(PASS_TOKEN)
    print(f"rows_parsed: {len(rows)}")
    print(f"galaxies: {len(by_galaxy)}")
    print("dominant_failure_modes:", counts.most_common(5))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
