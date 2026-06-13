#!/usr/bin/env python3
"""D0 nuclear shell-contact SRC certificate.

Synthetic mode checks the frozen Ca-40/Ca-48/Fe-54 shell-contact witness.
Nature source-data mode is passport-only: if a manifest and source data are not
available, it reports SKIP_NATURE2026_SOURCE_DATA_REQUIRED rather than fitting
or inventing external inputs.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PASSPORT_DIR = ROOT / "08_PASSPORTS" / "NuclearSRC"
DEFAULT_MANIFEST = PASSPORT_DIR / "nature2026_src_manifest.json"
RESULTS_CSV = PASSPORT_DIR / "nature2026_src_results.csv"
SUMMARY_JSON = PASSPORT_DIR / "nature2026_src_summary.json"


@dataclass(frozen=True)
class Orbital:
    name: str
    j2: int

    @property
    def degeneracy(self) -> int:
        return self.j2 + 1


F7_2 = Orbital("f7/2", 7)
DELTA0 = ((1.0 + 5.0 ** 0.5) / 2.0) - 1.5


@dataclass(frozen=True)
class Occupancy:
    label: str
    A: int
    Z: int
    N: int
    p_f72: int
    n_f72: int

    @property
    def neutron_excess(self) -> int:
        return self.N - self.Z


CA40 = Occupancy("Ca-40", 40, 20, 20, 0, 0)
CA48 = Occupancy("Ca-48", 48, 20, 28, 0, 8)
FE54 = Occupancy("Fe-54", 54, 26, 28, 6, 8)


def default_manifest() -> dict[str, object]:
    return {
        "dataset_id": "nature2026_src",
        "source_name": "Nature 2026 SRC source-data release",
        "source_url": "",
        "download_url": "",
        "local_path": "",
        "sha256": "",
        "downloaded_at_utc": "",
        "data_fields_required": ["article", "source_data_fig2", "source_data_fig3", "sha256"],
        "data_fields_found": [],
        "license_or_policy_note": "Use only a public source-data release or locally pinned copy.",
        "citation_note": "Pin the exact article/source-data record before external PASS.",
        "status": "MISSING",
    }


def ensure_manifest(path: Path) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default_manifest(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return json.loads(path.read_text(encoding="utf-8"))


def write_summary(mode: str, status: str, missing: list[str] | None = None) -> None:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_JSON.write_text(
        json.dumps(
            {
                "mode": mode,
                "status": status,
                "manifest": str(DEFAULT_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
                "results_csv": str(RESULTS_CSV.relative_to(ROOT)).replace("\\", "/"),
                "missing": missing or [],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def same_shell_contact(o: Occupancy, shell: Orbital = F7_2) -> float:
    return (o.p_f72 * o.n_f72) / shell.degeneracy


def write_synthetic_results() -> None:
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in [CA40, CA48, FE54]:
        rows.append(
            {
                "label": occ.label,
                "A": occ.A,
                "Z": occ.Z,
                "N": occ.N,
                "neutron_excess": occ.neutron_excess,
                "p_f7_2": occ.p_f72,
                "n_f7_2": occ.n_f72,
                "same_shell_contact": same_shell_contact(occ),
            }
        )
    with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def synthetic() -> int:
    ensure_manifest(DEFAULT_MANIFEST)
    ca_jump = same_shell_contact(CA48) - same_shell_contact(CA40)
    fe_jump = same_shell_contact(FE54) - same_shell_contact(CA48)
    mass_ca = CA48.A - CA40.A
    mass_fe = FE54.A - CA48.A
    nex_ca = CA48.neutron_excess - CA40.neutron_excess
    nex_fe = FE54.neutron_excess - CA48.neutron_excess

    assert F7_2.degeneracy == 8
    assert ca_jump == 0.0
    assert fe_jump == 6.0
    assert mass_ca > mass_fe
    assert nex_ca > nex_fe
    assert fe_jump > ca_jump

    leakage_bound = abs(DELTA0) * (CA48.n_f72 / F7_2.degeneracy)
    assert leakage_bound < fe_jump
    write_synthetic_results()
    write_summary("synthetic", "PASS_NUCLEAR_SHELL_CONTACT_SRC_SYNTHETIC")

    print("--- D0 NUCLEAR SHELL-CONTACT SRC: SYNTHETIC ---")
    print(f"[1] f7/2 degeneracy={F7_2.degeneracy}: PASS")
    print(f"[2] Ca48-Ca40 same-shell contact jump={ca_jump:g}: PASS")
    print(f"[3] Fe54-Ca48 same-shell contact jump={fe_jump:g}: PASS")
    print(f"[4] mass-only ordering rejected: dA_Ca={mass_ca} > dA_Fe={mass_fe} but dSCI_Ca < dSCI_Fe: PASS")
    print(f"[5] N/Z-only ordering rejected: d(N-Z)_Ca={nex_ca} > d(N-Z)_Fe={nex_fe} but dSCI_Ca < dSCI_Fe: PASS")
    print(f"[6] cross-shell leakage delta0 bound={leakage_bound:.6g} < matched contact={fe_jump:g}: PASS")
    print("[CORE-CLOSED] PASS_NUCLEAR_SHELL_CONTACT_SRC_SYNTHETIC")
    return 0


def manifest_only(path: Path) -> int:
    data = ensure_manifest(path)
    required = data.get("data_fields_required", ["article", "source_data_fig2", "source_data_fig3", "sha256"])
    found = data.get("data_fields_found", [])
    missing = [str(k) for k in required if k not in found]
    if data.get("status") != "READY":
        missing.append("status_READY")
    if not data.get("sha256") and "sha256" not in missing:
        missing.append("sha256")
    if missing:
        write_summary("manifest_only", "SKIP_NATURE2026_SOURCE_DATA_REQUIRED", missing)
        print("SKIP_NATURE2026_SOURCE_DATA_REQUIRED")
        print("missing:", ",".join(missing))
        return 0
    write_summary("manifest_only", "SKIP_NATURE2026_SOURCE_DATA_REQUIRED")
    print("--- D0 NUCLEAR SHELL-CONTACT SRC: MANIFEST ---")
    print("[1] manifest schema keys present: PASS")
    print("[2] external source-data comparison remains passport-only: PASS")
    print("SKIP_NATURE2026_SOURCE_DATA_REQUIRED")
    return 0


def file_from_manifest(data: dict[str, Any], label: str) -> Path | None:
    for item in data.get("files", []):
        if item.get("label") == label:
            return ROOT / item["local_path"]
    return None


def weighted_mean(values: list[float], errors: list[float]) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    if any(e <= 0 for e in errors) or len(values) != len(errors):
        return sum(values) / len(values), float("nan")
    weights = [1.0 / (e * e) for e in errors]
    mean = sum(v * w for v, w in zip(values, weights)) / sum(weights)
    return mean, math.sqrt(1.0 / sum(weights))


def nature2026_source_data(path: Path) -> int:
    data = ensure_manifest(path)
    found = data.get("data_fields_found", [])
    missing = [k for k in ["article", "source_data_fig2", "source_data_fig3", "sha256"] if k not in found]
    if data.get("status") != "READY":
        missing.append("status_READY")
    fig2 = file_from_manifest(data, "source_data_fig2")
    fig3 = file_from_manifest(data, "source_data_fig3")
    if not fig2 or not fig2.exists():
        missing.append("source_data_fig2_file")
    if not fig3 or not fig3.exists():
        missing.append("source_data_fig3_file")
    if missing:
        write_summary("nature2026_source_data", "SKIP_NATURE2026_SOURCE_DATA_REQUIRED", missing)
        print("SKIP_NATURE2026_SOURCE_DATA_REQUIRED")
        print("missing:", ",".join(missing))
        return 0

    fig2_df = pd.read_excel(fig2)
    fig3_values = pd.read_excel(fig3, sheet_name="Values")
    ca_mean, ca_mean_err = weighted_mean(
        fig2_df["Ca48/Ca40"].astype(float).tolist(),
        fig2_df["Ca48/Ca40 Uncer"].astype(float).tolist(),
    )
    fe_mean, fe_mean_err = weighted_mean(
        fig2_df["Fe54/Ca48"].astype(float).tolist(),
        fig2_df["Fe54/Ca48 Uncer"].astype(float).tolist(),
    )
    values = {str(row["Ratio"]): float(row["Data"]) for _, row in fig3_values.iterrows()}
    ca_integral = values["Ca48/Ca40"]
    fe_integral = values["Fe54/Ca48"]

    d0_ca = same_shell_contact(CA48) - same_shell_contact(CA40)
    d0_fe = same_shell_contact(FE54) - same_shell_contact(CA48)
    observed_order = fe_integral > ca_integral and fe_mean > ca_mean
    d0_order = d0_fe > d0_ca
    a_only_rejected = (CA48.A - CA40.A) > (FE54.A - CA48.A)
    nz_only_rejected = (CA48.neutron_excess - CA40.neutron_excess) > (FE54.neutron_excess - CA48.neutron_excess)
    passed = observed_order and d0_order and a_only_rejected and nz_only_rejected

    with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "comparison",
                "observed_integral_ratio",
                "observed_bin_weighted_mean",
                "observed_bin_weighted_error",
                "d0_shell_contact_increment",
                "a_only_delta",
                "neutron_excess_delta",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "comparison": "Ca48/Ca40",
                "observed_integral_ratio": ca_integral,
                "observed_bin_weighted_mean": ca_mean,
                "observed_bin_weighted_error": ca_mean_err,
                "d0_shell_contact_increment": d0_ca,
                "a_only_delta": CA48.A - CA40.A,
                "neutron_excess_delta": CA48.neutron_excess - CA40.neutron_excess,
            }
        )
        writer.writerow(
            {
                "comparison": "Fe54/Ca48",
                "observed_integral_ratio": fe_integral,
                "observed_bin_weighted_mean": fe_mean,
                "observed_bin_weighted_error": fe_mean_err,
                "d0_shell_contact_increment": d0_fe,
                "a_only_delta": FE54.A - CA48.A,
                "neutron_excess_delta": FE54.neutron_excess - CA48.neutron_excess,
            }
        )

    status = "PASS_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026" if passed else "FAIL_NUCLEAR_SHELL_CONTACT_SRC_NATURE2026"
    SUMMARY_JSON.write_text(
        json.dumps(
            {
                "mode": "nature2026_source_data",
                "status": status,
                "observed_order_fe_gt_ca": observed_order,
                "d0_order_fe_gt_ca": d0_order,
                "a_only_negative_control_rejected": a_only_rejected,
                "nz_only_negative_control_rejected": nz_only_rejected,
                "ca48_ca40_integral": ca_integral,
                "fe54_ca48_integral": fe_integral,
                "ca48_ca40_weighted_mean": ca_mean,
                "fe54_ca48_weighted_mean": fe_mean,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(status)
    print(f"Ca48/Ca40 integral={ca_integral:.6g}, weighted_mean={ca_mean:.6g}")
    print(f"Fe54/Ca48 integral={fe_integral:.6g}, weighted_mean={fe_mean:.6g}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["synthetic", "manifest_only", "nature2026_source_data"], default="synthetic")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = ap.parse_args()
    if args.mode == "synthetic":
        return synthetic()
    if args.mode == "manifest_only":
        return manifest_only(args.manifest)
    return nature2026_source_data(args.manifest)


if __name__ == "__main__":
    raise SystemExit(main())
