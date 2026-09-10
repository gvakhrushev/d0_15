#!/usr/bin/env python3
"""D0-RD-01: direct redshift-drift confrontation on two observing technologies.

Leg A tests the literal discrete one-tick jump without fitting an SI scale.
Leg B explicitly adds one continuous tick-rate bridge and fits its single common amplitude.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import tarfile
from pathlib import Path

import numpy as np
from scipy.stats import chi2, norm


ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "08_PASSPORTS" / "REDSHIFT_DRIFT"
MANIFEST = PASSPORT / "d0_rd_01_manifest.json"
VERDICT = PASSPORT / "d0_rd_01_verdict.json"
PHI = (1.0 + math.sqrt(5.0)) / 2.0
C_MPS = 299_792_458.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_and_verify_manifest() -> tuple[dict, Path, list[Path]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["protocol_id"] == "D0-RD-01"
    assert manifest["status"] == "READY"
    assert manifest["sample_data"] is False
    assert manifest["measurement_level_only"] is True
    assert manifest["prospective_preregistration"] is False
    data_path = ROOT / manifest["data_local_path"]
    assert data_path.is_file()
    assert sha256(data_path) == manifest["data_sha256"]
    source_paths = []
    for source in manifest["sources"]:
        path = ROOT / source["local_path"]
        assert path.is_file(), f"missing source archive: {path}"
        assert sha256(path) == source["sha256"], f"source hash mismatch: {path}"
        source_paths.append(path)
    return manifest, data_path, source_paths


def verify_primary_source_tokens(source_paths: list[Path]) -> None:
    with tarfile.open(source_paths[0], "r:gz") as archive:
        darling = archive.extractfile("ms-emulapj.tex")
        assert darling is not None
        darling_text = darling.read().decode("utf-8")
    for token in (
        "{\\bf 0738+313 A}", "{\\bf 0738+313 B}", "{\\bf PKS 1413+135}",
        "{\\bf PKS 1127$-$145}", "{\\bf 0248+430}", "{\\bf PKS 1229$-$021}",
        "{\\bf 0235+164}", "{\\bf B3 1504+377}", "{\\bf B0218+357}",
        "{\\bf 3C286}",
        "\\langle\\dot{z}\\rangle = (-2.3\\,\\pm\\,0.8)\\times10^{-8}",
        "\\langle\\dot{v}\\rangle = -5.5\\,\\pm\\,2.2",
    ):
        assert token in darling_text, f"missing pinned Darling token: {token}"

    with tarfile.open(source_paths[1], "r:gz") as archive:
        trost = archive.extractfile("ESPRESSO_DRIFT_3.tex")
        assert trost is not None
        trost_text = trost.read().decode("utf-8")
    for token in (
        "\\dot{v} = -3.43 \\pm 3.56",
        "-5.23 \\pm 5.43",
        "\\dot{v} = -3.63\\pm3.65",
        "-5.53 \\pm 5.56",
        "z=3.57",
    ):
        assert token in trost_text, f"missing pinned Trost token: {token}"


def load_rows(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            for key in (
                "z", "baseline_days", "dotz_per_year", "sigma_dotz_per_year",
                "dv_mps_per_year", "sigma_dv_mps_per_year",
            ):
                row[key] = float(row[key])
            rows.append(row)
    assert len(rows) == 12
    gbt = [row for row in rows if row["group"] == "GBT_HI" and row["role"] == "primary"]
    espresso_primary = [
        row for row in rows if row["group"] == "ESPRESSO_LYA" and row["role"] == "primary"
    ]
    espresso_controls = [
        row for row in rows
        if row["group"] == "ESPRESSO_LYA" and row["role"] == "correlated_control"
    ]
    assert len(gbt) == 10
    assert [row["object"] for row in espresso_primary] == ["SB2_pixel"]
    assert [row["object"] for row in espresso_controls] == ["SB2_likelihood"]
    for row in rows:
        assert row["z"] > 0.0 and row["baseline_days"] > 0.0
        assert row["sigma_dotz_per_year"] > 0.0 and row["sigma_dv_mps_per_year"] > 0.0
        derived_dv = C_MPS * row["dotz_per_year"] / (1.0 + row["z"])
        # Published table entries are rounded independently.
        assert abs(derived_dv - row["dv_mps_per_year"]) < 1.2
    return rows


def weighted_constant(rows: list[dict]) -> tuple[float, float, float, int, float]:
    values = np.asarray([row["dv_mps_per_year"] for row in rows], dtype=float)
    sigmas = np.asarray([row["sigma_dv_mps_per_year"] for row in rows], dtype=float)
    weights = 1.0 / sigmas**2
    estimate = float(np.sum(weights * values) / np.sum(weights))
    uncertainty = float(1.0 / math.sqrt(float(np.sum(weights))))
    statistic = float(np.sum(((values - estimate) / sigmas) ** 2))
    dof = len(rows) - 1
    p_value = float(chi2.sf(statistic, dof))
    return estimate, uncertainty, statistic, dof, p_value


def main() -> int:
    manifest, data_path, source_paths = load_and_verify_manifest()
    verify_primary_source_tokens(source_paths)
    rows = load_rows(data_path)
    primary = [row for row in rows if row["role"] == "primary"]
    gbt = [row for row in primary if row["group"] == "GBT_HI"]
    espresso = [row for row in primary if row["group"] == "ESPRESSO_LYA"]
    assert len(primary) == 11 and len(espresso) == 1

    discrete_rows = []
    for row in primary:
        years = row["baseline_days"] / 365.25
        observed_delta = row["dotz_per_year"] * years
        sigma_delta = row["sigma_dotz_per_year"] * years
        envelope_5sigma = abs(observed_delta) + 5.0 * sigma_delta
        one_tick_delta = (PHI - 1.0) * (1.0 + row["z"])
        factor = one_tick_delta / envelope_5sigma
        assert factor > 1.0
        discrete_rows.append({
            "object": row["object"],
            "group": row["group"],
            "baseline_years": years,
            "observed_delta_z": observed_delta,
            "sigma_delta_z": sigma_delta,
            "five_sigma_envelope": envelope_5sigma,
            "minimum_one_tick_delta_z": one_tick_delta,
            "separation_factor": factor,
        })
    min_separation = min(item["separation_factor"] for item in discrete_rows)
    leg_a_decision = "REJECT_LITERAL_NONZERO_D0_TICK_IN_EACH_REGISTERED_BASELINE"

    gbt_A, gbt_sigma, gbt_chi2, gbt_dof, gbt_p = weighted_constant(gbt)
    holdout = espresso[0]
    holdout_residual = holdout["dv_mps_per_year"] - gbt_A
    holdout_sigma = math.hypot(holdout["sigma_dv_mps_per_year"], gbt_sigma)
    holdout_pull = holdout_residual / holdout_sigma

    A, sigma_A, constant_chi2, constant_dof, constant_p = weighted_constant(primary)
    z_score = A / sigma_A
    positive_detection_p = float(norm.sf(z_score))
    nonnegative_family_exclusion_p = float(norm.cdf(z_score))
    confidence = float(manifest["confidence_level"])
    alpha = float(manifest["alpha"])
    upper_A = A + float(norm.ppf(confidence)) * sigma_A
    assert upper_A > 0.0
    upper_rho = upper_A / (C_MPS * math.log(PHI))
    tick_time_lower_years = 1.0 / upper_rho
    leg_b_decision = (
        "REJECT_NONNEGATIVE_CONTINUOUS_RATE_AT_FROZEN_ALPHA"
        if nonnegative_family_exclusion_p < alpha
        else "NO_POSITIVE_DRIFT_DETECTION_CONTINUOUS_RATE_NOT_REJECTED_AT_FROZEN_ALPHA"
    )

    # Independence mutation: pooling the correlated ESPRESSO control must be observably different
    # and is prohibited from becoming the primary result.
    correlated_control = [row for row in rows if row["role"] == "correlated_control"]
    assert len(correlated_control) == 1
    invalid_A, invalid_sigma, _, _, _ = weighted_constant(primary + correlated_control)
    assert invalid_sigma < sigma_A
    assert abs(invalid_A - A) > 1e-4

    result = {
        "protocol_id": manifest["protocol_id"],
        "hashes_verified": True,
        "sample_data": False,
        "measurement_level_only": True,
        "prospective_preregistration": False,
        "independent_blocks": ["GBT_HI", "ESPRESSO_LYA"],
        "leg_a_literal_discrete_tick": {
            "decision": leg_a_decision,
            "test": "minimum one-tick jump versus absolute observed change plus five sigma",
            "minimum_separation_factor": min_separation,
            "rows": discrete_rows,
            "scope": "rejects only a physical bridge assigning one or more forward D0 ticks to a registered observing baseline",
        },
        "leg_b_continuous_si_bridge": {
            "bridge": "1+z(t)=(1+z0)*phi^(rho*t), rho>=0 ticks/year",
            "eliminated_relation": "dv/dt=c*dot(z)/(1+z)=c*rho*ln(phi)=constant",
            "decision": leg_b_decision,
            "alpha": alpha,
            "joint_unrestricted_A_mps_per_year": A,
            "joint_sigma_A_mps_per_year": sigma_A,
            "joint_z_score": z_score,
            "constant_shape_chi2": constant_chi2,
            "constant_shape_dof": constant_dof,
            "constant_shape_p_value": constant_p,
            "positive_detection_p_value": positive_detection_p,
            "nonnegative_family_exclusion_p_value": nonnegative_family_exclusion_p,
            "gbt_only_A_mps_per_year": gbt_A,
            "gbt_only_sigma_A_mps_per_year": gbt_sigma,
            "gbt_only_chi2": gbt_chi2,
            "gbt_only_dof": gbt_dof,
            "gbt_only_p_value": gbt_p,
            "espresso_holdout_observed_mps_per_year": holdout["dv_mps_per_year"],
            "espresso_holdout_sigma_mps_per_year": holdout["sigma_dv_mps_per_year"],
            "espresso_holdout_prediction_residual_mps_per_year": holdout_residual,
            "espresso_holdout_pull": holdout_pull,
            "upper_limit_confidence": confidence,
            "upper_A_mps_per_year": upper_A,
            "upper_rho_ticks_per_year": upper_rho,
            "lower_time_per_phi_tick_years": tick_time_lower_years,
            "scope": "external one-parameter SI interpolation; null/sensitivity result, never Lean core",
        },
        "correlated_control": {
            "object": correlated_control[0]["object"],
            "not_pooled": True,
            "invalid_double_count_A_mps_per_year": invalid_A,
            "invalid_double_count_sigma_A_mps_per_year": invalid_sigma,
        },
    }
    VERDICT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== D0-RD-01 direct redshift-drift passport ===")
    print("HASHES_VERIFIED arXiv:1211.4585 + arXiv:2603.02318; SAMPLE_DATA=False")
    print(f"LEG_A {leg_a_decision}")
    print(f"LEG_A_MIN_SEPARATION_FACTOR {min_separation:.6g}")
    print(
        f"GBT_CALIBRATION A={gbt_A:.6g} +/- {gbt_sigma:.6g} m/s/yr; "
        f"ESPRESSO_HOLDOUT_PULL={holdout_pull:.6g}"
    )
    print(
        f"JOINT_CONSTANT A={A:.6g} +/- {sigma_A:.6g} m/s/yr; "
        f"chi2={constant_chi2:.6g}/{constant_dof}; p={constant_p:.6g}"
    )
    print(
        f"POSITIVE_DETECTION_P={positive_detection_p:.6g}; "
        f"NONNEGATIVE_EXCLUSION_P={nonnegative_family_exclusion_p:.6g}"
    )
    print(
        f"UPPER_{100*confidence:.1f}% A={upper_A:.6g} m/s/yr; "
        f"rho={upper_rho:.6g} tick/yr; time_per_phi_tick>{tick_time_lower_years:.6g} yr"
    )
    print(f"LEG_B {leg_b_decision}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
