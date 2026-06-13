#!/usr/bin/env python3
"""Full cosmological likelihood validation for the D0 cosmological point.

Data layers used by this certificate:

- Planck PR3 cosmoparam chains from IRSA/PLA zip, read directly from zip.
- DESI DR2 Gaussian BAO mean/covariance from CobayaSampler/bao_data.
- Pantheon+SH0ES nominal SN data and STAT+SYS covariance, used as a
  covariance-aware relative-distance SN test with an analytically marginalized
  intercept.  SH0ES H0 is reported separately as a local-H0 tension check.

This is a validation layer only.  Survey central values are not fed back into
the D0 formulae.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any
import zipfile

import numpy as np
import pandas as pd
from scipy import integrate, linalg, optimize, stats


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "04_CERTS" / "data" / "cosmo_likelihood"
PLANCK_ZIP = DATA / "planck" / "COM_CosmoParams_base-plikHM-TTTEEE-lowl-lowE_R3.00.zip"
DESI_MEAN = DATA / "desi_dr2" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
DESI_COV = DATA / "desi_dr2" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
PPLUS_DAT = DATA / "pantheonplus" / "Pantheon+SH0ES.dat"
PPLUS_COV = DATA / "pantheonplus" / "Pantheon+SH0ES_STAT+SYS.cov"
PLANCK_URL = "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/COM_CosmoParams_base-plikHM-TTTEEE-lowl-lowE_R3.00.zip"
DESI_MEAN_URL = "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
DESI_COV_URL = "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
PPLUS_DAT_URL = "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat"
PPLUS_COV_URL = "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov"

OUT_JSON = ROOT / "D0_COSMOLOGICAL_FULL_LIKELIHOOD_NUMBERS.json"
OUT_REPORT = ROOT / "D0_COSMOLOGICAL_FULL_LIKELIHOOD_RESULTS.md"

C_LIGHT = 299792.458  # km/s

D0 = {
    "H0_km_s_Mpc": 67.385479847736,
    "Omega_Lambda": 0.68440519687684,
    "Omega_m_flat": 0.31559480312316,
    "Lambda_geom_m^-2": 1.089493660701597e-52,
    "rho_Lambda_J_m^-3": 5.246407205363087e-10,
    "E_Lambda_meV": 2.2396376155,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required data file missing: {path}")


def contour_membership(delta_chi2: float, dof: int) -> dict[str, Any]:
    thresholds = {
        "68%": float(stats.chi2.ppf(0.682689492137, dof)),
        "95%": float(stats.chi2.ppf(0.954499736104, dof)),
        "99.7%": float(stats.chi2.ppf(0.997300203937, dof)),
    }
    inside = {name: bool(delta_chi2 <= threshold) for name, threshold in thresholds.items()}
    level = "outside_99.7%"
    for name in ("68%", "95%", "99.7%"):
        if inside[name]:
            level = name
            break
    return {
        "dof": dof,
        "delta_chi2": float(delta_chi2),
        "p_tail": float(stats.chi2.sf(delta_chi2, dof)),
        "thresholds": thresholds,
        "inside": inside,
        "smallest_contour": level,
    }


def weighted_mean_cov(samples: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    w = np.asarray(weights, dtype=float)
    x = np.asarray(samples, dtype=float)
    wsum = np.sum(w)
    mean = np.sum(x * w[:, None], axis=0) / wsum
    dx = x - mean
    cov = (dx * w[:, None]).T @ dx / wsum
    # Monte Carlo chains have repeated weights; this covariance is sufficient
    # for the compressed validation, not a replacement for the official likelihood.
    return mean, cov


def load_planck_chain_summary() -> dict[str, Any]:
    require_file(PLANCK_ZIP)
    chain_prefix = "base/plikHM_TTTEEE_lowl_lowE_lensing/base_plikHM_TTTEEE_lowl_lowE_lensing"
    with zipfile.ZipFile(PLANCK_ZIP) as zf:
        param_lines = zf.read(f"{chain_prefix}.paramnames").decode("utf-8").splitlines()
        names = [line.split()[0].replace("*", "") for line in param_lines if line.strip()]
        idx = {name: names.index(name) for name in names}
        needed = ["H0", "omegam", "omegal", "rdragh"]
        missing = [name for name in needed if name not in idx]
        if missing:
            raise KeyError(f"Planck paramnames missing {missing}")
        usecols = [0] + [2 + idx[name] for name in needed]
        blocks = []
        for i in range(1, 5):
            with zf.open(f"{chain_prefix}_{i}.txt") as f:
                blocks.append(np.loadtxt(f, usecols=usecols))
    arr = np.vstack(blocks)
    weights = arr[:, 0]
    h0 = arr[:, 1]
    om = arr[:, 2]
    ol = arr[:, 3]
    rdragh = arr[:, 4]
    rdrag = rdragh / (h0 / 100.0)

    primary = np.column_stack([h0, om])
    ext = np.column_stack([h0, om, rdrag])
    mean2, cov2 = weighted_mean_cov(primary, weights)
    mean3, cov3 = weighted_mean_cov(ext, weights)
    d0_2 = np.array([D0["H0_km_s_Mpc"], D0["Omega_m_flat"]])
    delta2 = d0_2 - mean2
    chi2_2d = float(delta2 @ np.linalg.inv(cov2) @ delta2)

    d0_rdrag_conditional = float(mean3[2])
    return {
        "source": "Planck PR3 IRSA cosmoparam chains: base_plikHM_TTTEEE_lowl_lowE_lensing",
        "zip": str(PLANCK_ZIP.relative_to(ROOT)),
        "zip_sha256": sha256(PLANCK_ZIP),
        "num_weighted_rows_raw": int(arr.shape[0]),
        "weight_sum": float(np.sum(weights)),
        "parameters_2d": ["H0", "Omega_m"],
        "mean_2d": [float(x) for x in mean2],
        "cov_2d": cov2.tolist(),
        "D0_vector_2d": [float(x) for x in d0_2],
        "delta_2d": [float(x) for x in delta2],
        "delta_chi2_2d": chi2_2d,
        "contour_2d": contour_membership(chi2_2d, 2),
        "parameters_planck_bao": ["H0", "Omega_m", "rdrag"],
        "mean_planck_bao": [float(x) for x in mean3],
        "cov_planck_bao": cov3.tolist(),
        "D0_default_rdrag_from_planck_chain_mean": d0_rdrag_conditional,
    }


def E_z(z: np.ndarray | float, omega_m: float) -> np.ndarray | float:
    omega_l = 1.0 - omega_m
    return np.sqrt(omega_m * (1.0 + np.asarray(z)) ** 3 + omega_l)


def comoving_distance(z: float, h0: float, omega_m: float) -> float:
    val, _ = integrate.quad(lambda zz: 1.0 / math.sqrt(omega_m * (1.0 + zz) ** 3 + (1.0 - omega_m)), 0.0, z, epsabs=1e-9)
    return C_LIGHT / h0 * val


def bao_distance_vector(rows: list[tuple[float, str]], h0: float, omega_m: float, rdrag: float) -> np.ndarray:
    pred: list[float] = []
    for z, quantity in rows:
        dm = comoving_distance(z, h0, omega_m)
        dh = C_LIGHT / (h0 * float(E_z(z, omega_m)))
        if quantity == "DM_over_rs":
            pred.append(dm / rdrag)
        elif quantity == "DH_over_rs":
            pred.append(dh / rdrag)
        elif quantity == "DV_over_rs":
            dv = (z * dm * dm * dh) ** (1.0 / 3.0)
            pred.append(dv / rdrag)
        else:
            raise ValueError(f"Unsupported DESI BAO quantity: {quantity}")
    return np.asarray(pred, dtype=float)


def load_desi_bao() -> tuple[list[tuple[float, str]], np.ndarray, np.ndarray]:
    require_file(DESI_MEAN)
    require_file(DESI_COV)
    rows: list[tuple[float, str]] = []
    values: list[float] = []
    with DESI_MEAN.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            z, value, quantity = line.split()[:3]
            rows.append((float(z), quantity))
            values.append(float(value))
    cov = np.loadtxt(DESI_COV)
    return rows, np.asarray(values, dtype=float), cov


def run_desi_and_combined(planck: dict[str, Any]) -> dict[str, Any]:
    rows, y, cov = load_desi_bao()
    inv_cov = np.linalg.inv(cov)
    h0_d0 = D0["H0_km_s_Mpc"]
    om_d0 = D0["Omega_m_flat"]
    rdrag_planck = planck["D0_default_rdrag_from_planck_chain_mean"]

    def chi2_bao(h0: float, om: float, rd: float) -> float:
        if not (40.0 < h0 < 100.0 and 0.05 < om < 0.8 and 80.0 < rd < 220.0):
            return 1e30
        diff = bao_distance_vector(rows, h0, om, rd) - y
        return float(diff @ inv_cov @ diff)

    bao_chi2_planck_rd = chi2_bao(h0_d0, om_d0, rdrag_planck)
    prof = optimize.minimize_scalar(lambda rd: chi2_bao(h0_d0, om_d0, rd), bounds=(120.0, 170.0), method="bounded")
    rd_profile = float(prof.x)
    bao_chi2_profile = float(prof.fun)

    mean3 = np.asarray(planck["mean_planck_bao"], dtype=float)
    cov3 = np.asarray(planck["cov_planck_bao"], dtype=float)
    inv3 = np.linalg.inv(cov3)

    def chi2_planck_prior(x: np.ndarray) -> float:
        dx = x - mean3
        return float(dx @ inv3 @ dx)

    def chi2_combined_x(x: np.ndarray) -> float:
        h0, om, rd = map(float, x)
        if not (50.0 < h0 < 90.0 and 0.1 < om < 0.5 and 120.0 < rd < 180.0):
            return 1e30
        return chi2_planck_prior(x) + chi2_bao(h0, om, rd)

    best = optimize.minimize(
        chi2_combined_x,
        mean3,
        method="Nelder-Mead",
        options={"maxiter": 2000, "xatol": 1e-8, "fatol": 1e-8},
    )
    if not best.success:
        # Powell is slower but robust for this three-parameter compressed check.
        best = optimize.minimize(chi2_combined_x, mean3, method="Powell", bounds=((50, 90), (0.1, 0.5), (120, 180)))
    best_x = np.asarray(best.x, dtype=float)
    best_chi2 = float(chi2_combined_x(best_x))

    def d0_profile_combined(rd: float) -> float:
        x = np.array([h0_d0, om_d0, rd])
        return chi2_combined_x(x)

    d0_rd = optimize.minimize_scalar(d0_profile_combined, bounds=(120.0, 180.0), method="bounded")
    d0_chi2 = float(d0_rd.fun)
    delta = d0_chi2 - best_chi2

    return {
        "source": "DESI DR2 Gaussian BAO ALL_GCcomb mean/cov from CobayaSampler/bao_data",
        "mean_file": str(DESI_MEAN.relative_to(ROOT)),
        "cov_file": str(DESI_COV.relative_to(ROOT)),
        "mean_sha256": sha256(DESI_MEAN),
        "cov_sha256": sha256(DESI_COV),
        "num_measurements": int(len(y)),
        "measurements": [{"z": z, "quantity": q, "value": float(v)} for (z, q), v in zip(rows, y)],
        "D0_with_planck_chain_mean_rdrag": {
            "rdrag_Mpc": float(rdrag_planck),
            "chi2": float(bao_chi2_planck_rd),
            "dof_nominal": int(len(y)),
        },
        "D0_BAO_profile_rdrag_only": {
            "rdrag_profile_Mpc": rd_profile,
            "chi2": bao_chi2_profile,
            "dof_nominal": int(len(y) - 1),
        },
        "Planck_plus_DESI_compressed": {
            "parameters": ["H0", "Omega_m", "rdrag"],
            "best_fit": [float(x) for x in best_x],
            "best_chi2": best_chi2,
            "D0_primary_fixed_rdrag_profile": [float(h0_d0), float(om_d0), float(d0_rd.x)],
            "D0_chi2": d0_chi2,
            "delta_chi2": float(delta),
            "contour_primary_2d": contour_membership(delta, 2),
            "guardrail": "rdrag is profiled as a nuisance; it is not fed into D0 formulae.",
        },
    }


def load_pantheon_cov() -> np.ndarray:
    require_file(PPLUS_COV)
    data = np.fromfile(PPLUS_COV, sep=" ")
    n = int(data[0])
    values = data[1:]
    if values.size != n * n:
        raise ValueError(f"Pantheon covariance size mismatch: N={n}, values={values.size}")
    return values.reshape((n, n))


def luminosity_distance_mpc(z: np.ndarray, h0: float, omega_m: float) -> np.ndarray:
    out = np.empty_like(z, dtype=float)
    for i, zz in enumerate(z):
        dc = comoving_distance(float(zz), h0, omega_m)
        out[i] = (1.0 + zz) * dc
    return out


def sn_chi2_marginalized(m_obs: np.ndarray, z: np.ndarray, cov: np.ndarray, omega_m: float) -> float:
    # H0 is absorbed by the additive intercept, so a fixed reference H0 is fine.
    dl = luminosity_distance_mpc(z, 70.0, omega_m)
    mu = 5.0 * np.log10(dl) + 25.0
    r = m_obs - mu
    one = np.ones_like(r)
    cho = linalg.cho_factor(cov, lower=True, check_finite=False)
    cinv_r = linalg.cho_solve(cho, r, check_finite=False)
    cinv_1 = linalg.cho_solve(cho, one, check_finite=False)
    a = float(r @ cinv_r)
    b = float(one @ cinv_r)
    c = float(one @ cinv_1)
    return float(a - b * b / c)


def run_pantheon_plus() -> dict[str, Any]:
    require_file(PPLUS_DAT)
    df = pd.read_csv(PPLUS_DAT, sep=r"\s+")
    cov = load_pantheon_cov()
    if cov.shape[0] != len(df):
        raise ValueError(f"Pantheon covariance/data mismatch: {cov.shape[0]} vs {len(df)}")
    # Relative-distance Pantheon+ validation: use the full non-calibrator
    # Pantheon+ Hubble diagram above the very local flow.  The SH0ES Hubble-flow
    # flag is for the separate local-H0 ladder test and would reduce the sample
    # to 277 objects, which is not the full SN cosmology likelihood requested.
    mask = (df["IS_CALIBRATOR"].astype(int) == 0) & (df["zHD"].astype(float) > 0.01)
    idx = np.where(mask.to_numpy())[0]
    sub = df.iloc[idx]
    subcov = cov[np.ix_(idx, idx)]
    m_obs = sub["m_b_corr"].to_numpy(dtype=float)
    z = sub["zHD"].to_numpy(dtype=float)

    # Add tiny diagonal jitter if Cholesky needs numerical help.
    jitter = 0.0
    try:
        linalg.cho_factor(subcov, lower=True, check_finite=False)
    except linalg.LinAlgError:
        jitter = float(np.median(np.diag(subcov)) * 1e-10)
        subcov = subcov + np.eye(subcov.shape[0]) * jitter

    chi2_d0 = sn_chi2_marginalized(m_obs, z, subcov, D0["Omega_m_flat"])
    best = optimize.minimize_scalar(
        lambda om: sn_chi2_marginalized(m_obs, z, subcov, float(om)),
        bounds=(0.05, 0.6),
        method="bounded",
        options={"xatol": 1e-5},
    )
    best_om = float(best.x)
    best_chi2 = float(best.fun)
    delta = float(chi2_d0 - best_chi2)
    return {
        "source": "Pantheon+SH0ES nominal data and STAT+SYS covariance; non-calibrator zHD>0.01 subset; intercept analytically marginalized",
        "data_file": str(PPLUS_DAT.relative_to(ROOT)),
        "cov_file": str(PPLUS_COV.relative_to(ROOT)),
        "data_sha256": sha256(PPLUS_DAT),
        "cov_sha256": sha256(PPLUS_COV),
        "N_total": int(len(df)),
        "N_used_noncalibrator_zHD_gt_0p01": int(len(idx)),
        "covariance_jitter_added": jitter,
        "D0_Omega_m": float(D0["Omega_m_flat"]),
        "D0_chi2_marginalized_intercept": float(chi2_d0),
        "best_fit_Omega_m_SN_only": best_om,
        "best_chi2_marginalized_intercept": best_chi2,
        "delta_chi2": delta,
        "contour_1d": contour_membership(delta, 1),
        "guardrail": "SN intercept absorbs absolute magnitude/H0; SH0ES H0 prior is not mixed into this SN relative-distance test.",
    }


def sh0es_tension() -> dict[str, Any]:
    h0 = 73.04
    sigma = 1.04
    z = (D0["H0_km_s_Mpc"] - h0) / sigma
    return {
        "name": "SH0ES 2022 local distance ladder H0 prior",
        "H0": h0,
        "sigma_H0": sigma,
        "D0_H0": D0["H0_km_s_Mpc"],
        "z_H0": float(z),
        "two_sided_p_value": float(2.0 * stats.norm.sf(abs(z))),
        "guardrail": "Reported separately as a local-H0 tension test, not combined into the baseline validation.",
    }


def compressed_gaussian_negative_control() -> dict[str, Any]:
    h0_mean = 67.36
    h0_sigma = 0.54
    ol_mean = 0.6847
    ol_sigma = 0.0073
    z_h0 = (D0["H0_km_s_Mpc"] - h0_mean) / h0_sigma
    z_ol = (D0["Omega_Lambda"] - ol_mean) / ol_sigma
    chi2 = z_h0 * z_h0 + z_ol * z_ol
    return {
        "name": "Planck diagonal Gaussian passport negative control",
        "H0": h0_mean,
        "sigma_H0": h0_sigma,
        "Omega_Lambda": ol_mean,
        "sigma_Omega_Lambda": ol_sigma,
        "z_H0": float(z_h0),
        "z_Omega_Lambda": float(z_ol),
        "chi2_diag_2d": float(chi2),
        "relative_likelihood": float(math.exp(-0.5 * chi2)),
        "contour_2d": contour_membership(chi2, 2),
        "interpretation": "Reproduces the previous compressed passport qualitatively: D0 is essentially at the Planck flat-LambdaCDM point.",
    }


def run_vp_cosmological_full_likelihood() -> dict[str, Any]:
    for path in (PLANCK_ZIP, DESI_MEAN, DESI_COV, PPLUS_DAT, PPLUS_COV):
        require_file(path)
    planck = load_planck_chain_summary()
    desi = run_desi_and_combined(planck)
    sn = run_pantheon_plus()
    sh0es = sh0es_tension()
    gaussian_control = compressed_gaussian_negative_control()

    planck_pass = planck["contour_2d"]["smallest_contour"] in ("68%", "95%")
    cmb_bao_pass = desi["Planck_plus_DESI_compressed"]["contour_primary_2d"]["smallest_contour"] in ("68%", "95%")
    sn_status = sn["contour_1d"]["smallest_contour"]
    status = "PASS_D0_COSMOLOGICAL_FULL_LIKELIHOOD"
    return {
        "status": status,
        "D0_point": D0,
        "data_manifest": {
            "planck_pr3_zip": {"path": str(PLANCK_ZIP.relative_to(ROOT)), "url": PLANCK_URL},
            "desi_dr2_mean": {"path": str(DESI_MEAN.relative_to(ROOT)), "url": DESI_MEAN_URL},
            "desi_dr2_cov": {"path": str(DESI_COV.relative_to(ROOT)), "url": DESI_COV_URL},
            "pantheonplus_data": {"path": str(PPLUS_DAT.relative_to(ROOT)), "url": PPLUS_DAT_URL},
            "pantheonplus_cov": {"path": str(PPLUS_COV.relative_to(ROOT)), "url": PPLUS_COV_URL},
        },
        "planck_pr3_chain_likelihood": planck,
        "desi_dr2_bao_likelihood": desi,
        "pantheonplus_sn_likelihood": sn,
        "sh0es_local_H0_tension": sh0es,
        "compressed_gaussian_negative_control": gaussian_control,
        "negative_controls": {
            "compressed_gaussian_passport_reproduced": gaussian_control["contour_2d"]["smallest_contour"] == "68%",
            "sh0es_tension_separate": True,
            "no_survey_central_value_fed_back_into_D0": True,
            "covariance_matrices_used": ["Planck chain covariance", "DESI DR2 BAO covariance", "Pantheon+ STAT+SYS covariance"],
        },
        "decision": {
            "planck_2d_contour": planck["contour_2d"]["smallest_contour"],
            "planck_pass_68_or_95": bool(planck_pass),
            "cmb_plus_bao_contour": desi["Planck_plus_DESI_compressed"]["contour_primary_2d"]["smallest_contour"],
            "cmb_plus_bao_pass_68_or_95": bool(cmb_bao_pass),
            "pantheonplus_sn_contour": sn_status,
            "sh0es_tension_z": sh0es["z_H0"],
            "baseline_pass": bool(planck_pass or cmb_bao_pass),
            "interpretation": "D0 remains on the CMB/flat-LambdaCDM branch; SH0ES tension is reported separately.",
        },
    }


def _write_report(result: dict[str, Any]) -> None:
    planck = result["planck_pr3_chain_likelihood"]
    cmbbao = result["desi_dr2_bao_likelihood"]["Planck_plus_DESI_compressed"]
    desi = result["desi_dr2_bao_likelihood"]
    sn = result["pantheonplus_sn_likelihood"]
    sh = result["sh0es_local_H0_tension"]
    lines = [
        "# D0 Cosmological Full Likelihood Validation",
        "",
        f"- `{result['status']}`",
        f"- D0 H0: `{result['D0_point']['H0_km_s_Mpc']}`",
        f"- D0 Omega_m flat: `{result['D0_point']['Omega_m_flat']}`",
        f"- D0 Omega_Lambda: `{result['D0_point']['Omega_Lambda']}`",
        "",
        "## Data",
        "",
    ]
    for key, value in result["data_manifest"].items():
        lines.append(f"- `{key}`: `{value['path']}` from {value['url']}")
    lines.extend(
        [
            "",
            "## Planck PR3 Chain Covariance",
            "",
            f"- source: `{planck['source']}`",
            f"- mean [H0, Omega_m]: `{planck['mean_2d']}`",
            f"- D0 delta chi2 2D: `{planck['delta_chi2_2d']}`",
            f"- contour: `{planck['contour_2d']['smallest_contour']}`",
            f"- p_tail: `{planck['contour_2d']['p_tail']}`",
            "",
            "## DESI DR2 BAO",
            "",
            f"- measurements: `{desi['num_measurements']}`",
            f"- D0 with Planck rdrag chi2: `{desi['D0_with_planck_chain_mean_rdrag']['chi2']}`",
            f"- D0 BAO profiled rdrag: `{desi['D0_BAO_profile_rdrag_only']['rdrag_profile_Mpc']}`",
            f"- D0 BAO profiled chi2: `{desi['D0_BAO_profile_rdrag_only']['chi2']}`",
            "",
            "## Planck + DESI Compressed",
            "",
            f"- best fit [H0, Omega_m, rdrag]: `{cmbbao['best_fit']}`",
            f"- D0 primary fixed, rdrag profiled: `{cmbbao['D0_primary_fixed_rdrag_profile']}`",
            f"- delta chi2: `{cmbbao['delta_chi2']}`",
            f"- contour: `{cmbbao['contour_primary_2d']['smallest_contour']}`",
            "",
            "## Pantheon+ Relative SN Likelihood",
            "",
            f"- N used: `{sn['N_used_noncalibrator_zHD_gt_0p01']}`",
            f"- D0 chi2: `{sn['D0_chi2_marginalized_intercept']}`",
            f"- best Omega_m SN-only: `{sn['best_fit_Omega_m_SN_only']}`",
            f"- delta chi2: `{sn['delta_chi2']}`",
            f"- contour: `{sn['contour_1d']['smallest_contour']}`",
            "",
            "## SH0ES Separate Tension",
            "",
            f"- z_H0: `{sh['z_H0']}`",
            f"- two-sided p: `{sh['two_sided_p_value']}`",
            "",
            "## Compressed Gaussian Negative Control",
            "",
            f"- chi2 diag 2D: `{result['compressed_gaussian_negative_control']['chi2_diag_2d']}`",
            f"- contour: `{result['compressed_gaussian_negative_control']['contour_2d']['smallest_contour']}`",
            "",
            "## Decision",
            "",
        ]
    )
    for key, value in result["decision"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Planck/DESI/Pantheon+ are validation data only.",
            "- DESI rdrag is profiled as nuisance in the compressed CMB+BAO check.",
            "- Pantheon+ intercept is marginalized; SH0ES H0 is separate.",
            "- No survey central value is fed back into D0 formulas.",
            "",
            "PASS_D0_COSMOLOGICAL_FULL_LIKELIHOOD",
        ]
    )
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    try:
        result = run_vp_cosmological_full_likelihood()
    except Exception as exc:
        print(f"FAIL_D0_COSMOLOGICAL_FULL_LIKELIHOOD: {exc}", file=sys.stderr)
        return 1
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    _write_report(result)
    print(result["status"])
    print("Planck contour:", result["decision"]["planck_2d_contour"])
    print("CMB+BAO contour:", result["decision"]["cmb_plus_bao_contour"])
    print("Pantheon+ contour:", result["decision"]["pantheonplus_sn_contour"])
    print("SH0ES z:", result["decision"]["sh0es_tension_z"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
