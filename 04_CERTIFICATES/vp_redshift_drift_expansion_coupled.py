#!/usr/bin/env python3
"""D0-RDEC-01: coupled redshift-drift / expansion real-data passport.

The primary test eliminates the constant tick rate and tests the resulting radial-BAO shape.
It also tests the tempting microscopic single-section tick identification and keeps the absent
independent dark-response representation explicit.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2
from cert_runtime import assert_json_artifact_matches


ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "05_EXPERIMENTS" / "COUPLED_REDSHIFT_EXPANSION"
MANIFEST = PASSPORT / "d0_rdec_01_manifest.json"
VERDICT = PASSPORT / "d0_rdec_01_verdict.json"
SECONDS_PER_YEAR = 365.25 * 86400.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verified_path(spec: dict, path_key: str, hash_key: str) -> Path:
    path = ROOT / spec[path_key]
    assert path.is_file(), f"missing pinned input: {path}"
    assert sha256(path) == spec[hash_key], f"hash mismatch: {path}"
    return path


def load_radial_bao(mean_path: Path, covariance_path: Path):
    rows: list[tuple[float, float, str]] = []
    for line in mean_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        z, value, quantity = line.split()
        rows.append((float(z), float(value), quantity))
    covariance = np.loadtxt(covariance_path)
    assert covariance.shape == (len(rows), len(rows)) == (13, 13)
    indices = [i for i, row in enumerate(rows) if row[2] == "DH_over_rs"]
    assert len(indices) == 6
    z = np.asarray([rows[i][0] for i in indices], dtype=float)
    y = np.asarray([rows[i][1] for i in indices], dtype=float)
    cov = covariance[np.ix_(indices, indices)]
    assert np.all(np.linalg.eigvalsh(cov) > 0.0)
    return z, y, cov


def gls_amplitude(y: np.ndarray, cov: np.ndarray, shape: np.ndarray):
    precision = np.linalg.inv(cov)
    denominator = float(shape @ precision @ shape)
    amplitude = float(shape @ precision @ y) / denominator
    sigma_amplitude = 1.0 / math.sqrt(denominator)
    residual = y - amplitude * shape
    statistic = float(residual @ precision @ residual)
    return amplitude, sigma_amplitude, statistic, residual


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["protocol_id"] == "D0-RDEC-01"
    assert manifest["status"] == "READY"
    assert manifest["prospective_preregistration"] is False
    assert manifest["sample_data"] is False
    assert manifest["dark_response_representation_supplied"] is False
    assert manifest["primary_model"] == "DH_over_rd=C/(1+z)"
    assert manifest["fitted_primary_parameters"] == ["C"]
    assert set(manifest["forbidden_primary_refits"]) == {
        "phi", "rho", "exponent", "redshift bins", "covariance"
    }

    drift_path = verified_path(
        manifest["direct_drift_verdict"], "local_path", "sha256"
    )
    drift = json.loads(drift_path.read_text(encoding="utf-8"))
    continuous = drift["leg_b_continuous_si_bridge"]
    assert continuous["bridge"] == "1+z(t)=(1+z0)*phi^(rho*t), rho>=0 ticks/year"
    assert continuous["decision"] == (
        "NO_POSITIVE_DRIFT_DETECTION_CONTINUOUS_RATE_NOT_REJECTED_AT_FROZEN_ALPHA"
    )

    desi = manifest["desi_dr2_radial_bao"]
    mean_path = verified_path(desi, "mean_local_path", "mean_sha256")
    covariance_path = verified_path(
        desi, "covariance_local_path", "covariance_sha256"
    )
    z, observed, covariance = load_radial_bao(mean_path, covariance_path)

    # Primary: constant rho + FLRW drift identity => H/(1+z)=const => DH/rd=C/(1+z).
    primary_shape = 1.0 / (1.0 + z)
    C, sigma_C, statistic, residual = gls_amplitude(
        observed, covariance, primary_shape
    )
    assert C > 0.0
    dof = len(z) - 1
    p_value = float(chi2.sf(statistic, dof))
    alpha = float(manifest["alpha"])
    decision = (
        "REJECT_CONSTANT_RATE_D0_FLRW_COUPLED_BRIDGE"
        if p_value < alpha
        else "DO_NOT_REJECT_CONSTANT_RATE_D0_FLRW_COUPLED_BRIDGE"
    )

    # Nested control: let the exponent carry one additional real datum.
    def profiled_statistic(exponent: float) -> float:
        return gls_amplitude(
            observed, covariance, (1.0 + z) ** exponent
        )[2]

    power = minimize_scalar(
        profiled_statistic, bounds=(-4.0, 2.0), method="bounded",
        options={"xatol": 1.0e-13},
    )
    assert power.success
    free_exponent = float(power.x)
    free_C, free_sigma_C, free_statistic, _ = gls_amplitude(
        observed, covariance, (1.0 + z) ** free_exponent
    )
    free_dof = len(z) - 2
    free_p = float(chi2.sf(free_statistic, free_dof))
    delta_chi2 = statistic - free_statistic
    fixed_exponent_p = float(chi2.sf(delta_chi2, 1))
    assert delta_chi2 > 0.0

    reverse_C, _, reverse_statistic, _ = gls_amplitude(
        observed, covariance, 1.0 + z
    )
    assert reverse_statistic > statistic

    # DESI internal diagnostic: galaxy-tracer calibration, z=2.33 Ly-alpha holdout.
    galaxy = np.arange(5)
    lyalpha = 5
    galaxy_C, galaxy_sigma_C, galaxy_statistic, _ = gls_amplitude(
        observed[galaxy], covariance[np.ix_(galaxy, galaxy)],
        primary_shape[galaxy],
    )
    galaxy_dof = len(galaxy) - 1
    galaxy_p = float(chi2.sf(galaxy_statistic, galaxy_dof))
    holdout_prediction = galaxy_C * primary_shape[lyalpha]
    holdout_prediction_sigma = galaxy_sigma_C * primary_shape[lyalpha]
    holdout_total_sigma = math.hypot(
        holdout_prediction_sigma, math.sqrt(float(covariance[lyalpha, lyalpha]))
    )
    holdout_pull = (observed[lyalpha] - holdout_prediction) / holdout_total_sigma

    leave_one_out = []
    for omitted in range(len(z)):
        kept = np.asarray([i for i in range(len(z)) if i != omitted])
        loo_C, _, loo_statistic, _ = gls_amplitude(
            observed[kept], covariance[np.ix_(kept, kept)], primary_shape[kept]
        )
        loo_dof = len(kept) - 1
        leave_one_out.append({
            "omitted_z": float(z[omitted]),
            "best_fit_C": loo_C,
            "chi2": loo_statistic,
            "dof": loo_dof,
            "p_value": float(chi2.sf(loo_statistic, loo_dof)),
        })

    # Candidate collision: one cosmological tick = the existing electron action-section tick.
    section = manifest["electron_action_section"]
    h = float(section["h_J_s_exact"])
    c = float(section["c_m_per_s_exact"])
    electron_mass = float(section["electron_mass_kg_codata_2022"])
    tau_e_seconds = h / (38.0 * electron_mass * c**2)
    rho_e_per_year = SECONDS_PER_YEAR / tau_e_seconds
    rho_upper = float(continuous["upper_rho_ticks_per_year"])
    scale_separation_lower = rho_e_per_year / rho_upper
    tick_time_lower_seconds = (
        float(continuous["lower_time_per_phi_tick_years"]) * SECONDS_PER_YEAR
    )
    assert scale_separation_lower > 1.0
    electron_tick_decision = (
        "REJECT_ELECTRON_ACTION_SECTION_TICK_AS_COSMOLOGICAL_REFINEMENT_TICK"
    )

    measurements = []
    marginal_sigma = np.sqrt(np.diag(covariance))
    prediction = C * primary_shape
    for zz, yy, ss, pp, rr in zip(z, observed, marginal_sigma, prediction, residual):
        measurements.append({
            "z": float(zz),
            "DH_over_rd_observed": float(yy),
            "marginal_sigma": float(ss),
            "DH_over_rd_model": float(pp),
            "residual": float(rr),
            "marginal_pull": float(rr / ss),
            "transformed_one_plus_z_times_DH_over_rd": float((1.0 + zz) * yy),
        })

    result = {
        "protocol_id": manifest["protocol_id"],
        "hashes_verified": True,
        "sample_data": False,
        "prospective_preregistration": False,
        "independent_observable_blocks": [
            "GBT_HI_plus_ESPRESSO_redshift_drift",
            "DESI_DR2_radial_BAO_expansion",
        ],
        "derivation": {
            "d0_continuous": "dot(z)=rho*ln(phi)*(1+z)",
            "external_flrw_kinematics": "dot(z)=(1+z)*H0-H(z)",
            "rho_eliminated_shape": "H(z)/(1+z)=constant",
            "tested_radial_bao_shape": "DH(z)/rd=C/(1+z)",
            "phi_cancels_from_shape": True,
        },
        "direct_drift_cross_block": {
            "decision": continuous["decision"],
            "constant_shape_p_value": continuous["constant_shape_p_value"],
            "upper_rho_ticks_per_year_99_9pct": rho_upper,
        },
        "desi_radial_bao_primary": {
            "decision": decision,
            "alpha": alpha,
            "fitted_parameters": 1,
            "best_fit_C": C,
            "sigma_C": sigma_C,
            "chi2": statistic,
            "dof": dof,
            "p_value": p_value,
            "measurements": measurements,
        },
        "controls": {
            "free_power_law": {
                "model": "C*(1+z)^alpha",
                "best_fit_C": free_C,
                "sigma_C_conditional_on_alpha": free_sigma_C,
                "best_fit_alpha": free_exponent,
                "chi2": free_statistic,
                "dof": free_dof,
                "p_value": free_p,
                "delta_chi2_fixed_alpha_minus1": delta_chi2,
                "fixed_alpha_minus1_nested_p_value": fixed_exponent_p,
                "interpretation": "rescue requires at least one additional shape datum; even the best exact power law fails the frozen 0.001 goodness-of-fit threshold",
            },
            "reverse_shape": {
                "model": "C*(1+z)",
                "best_fit_C": reverse_C,
                "chi2": reverse_statistic,
            },
            "galaxy_calibration_lyalpha_holdout": {
                "galaxy_best_fit_C": galaxy_C,
                "galaxy_sigma_C": galaxy_sigma_C,
                "galaxy_chi2": galaxy_statistic,
                "galaxy_dof": galaxy_dof,
                "galaxy_p_value": galaxy_p,
                "lyalpha_z": float(z[lyalpha]),
                "lyalpha_observed": float(observed[lyalpha]),
                "lyalpha_prediction": holdout_prediction,
                "lyalpha_total_sigma": holdout_total_sigma,
                "lyalpha_holdout_pull": holdout_pull,
                "same_survey_not_claimed_independent": True,
            },
            "leave_one_out": leave_one_out,
            "rejection_without_z_2_33": leave_one_out[lyalpha]["p_value"] < alpha,
        },
        "single_section_tick_collision": {
            "candidate": "one cosmological refinement tick = h/(38*m_e*c^2)",
            "tau_e_seconds": tau_e_seconds,
            "rho_e_ticks_per_year": rho_e_per_year,
            "rho_upper_ticks_per_year_99_9pct": rho_upper,
            "minimum_dimensionless_scale_separation": scale_separation_lower,
            "cosmological_tick_time_lower_seconds": tick_time_lower_seconds,
            "decision": electron_tick_decision,
            "scope": "rejects the cross-scale tick identification, not the dimensionless coefficient 38 or the electron terminal section",
        },
        "dark_response_leg": {
            "internal_candidate_relation": "f_archive=z/(1+z); therefore DH/rd=C*(1-f_archive)",
            "independent_measured_representation_supplied": False,
            "decision": "NOT_TESTED_NO_INDEPENDENT_DARK_RESPONSE_REPRESENTATION",
            "forbidden_promotion": "BAO residuals are not relabelled as dark response",
        },
        "structural_reopening": {
            "constant_rho_rejected": decision.startswith("REJECT_"),
            "minimal_shape_repair": "rho must become a nonconstant function rho(z), or the FLRW/physical-redshift bridge must be abandoned",
            "information_cost": "at least one additional outcome-affecting shape degree of freedom; a free exponent is itself rejected in absolute goodness-of-fit",
        },
    }
    assert_json_artifact_matches(VERDICT, result)

    print("=== D0-RDEC-01 coupled redshift-drift / expansion passport ===")
    print("HASHES_VERIFIED direct-drift verdict + DESI DR2 mean/cov; SAMPLE_DATA=False")
    print(
        f"PRIMARY C={C:.8g} +/- {sigma_C:.8g}; "
        f"chi2={statistic:.8g}/{dof}; p={p_value:.8g}"
    )
    print(f"PRIMARY_DECISION {decision}")
    print(
        f"FREE_POWER alpha={free_exponent:.8g}; chi2={free_statistic:.8g}/{free_dof}; "
        f"DeltaChi2(alpha=-1)={delta_chi2:.8g}; nested_p={fixed_exponent_p:.8g}"
    )
    print(
        f"GALAXY_CALIBRATION p={galaxy_p:.8g}; "
        f"LYALPHA_HOLDOUT_PULL={holdout_pull:.8g} sigma"
    )
    print(
        f"ELECTRON_TICK tau={tau_e_seconds:.8g} s; rho={rho_e_per_year:.8g}/yr; "
        f"required_scale_separation>{scale_separation_lower:.8g}"
    )
    print(f"ELECTRON_TICK_DECISION {electron_tick_decision}")
    print("DARK_RESPONSE NOT_TESTED_NO_INDEPENDENT_DARK_RESPONSE_REPRESENTATION")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

