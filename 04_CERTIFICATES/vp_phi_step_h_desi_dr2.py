#!/usr/bin/env python3
"""PHI-P_DESI_01 Leg B: frozen step-H law versus official DESI DR2 BAO.

The tested physical bridge is
    H(z) = H0 * phi^(-floor(log_phi(1+z))).
Because DESI reports DH/rd = c/[H(z) rd], its observable prediction is
    DH/rd = C * phi^floor(log_phi(1+z)),
with one fitted positive normalization C.  No phase, base, boundary, or bin is fitted.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "05_EXPERIMENTS" / "DESI"
MANIFEST = PASSPORT / "phi_step_h_desi_dr2_manifest.json"
SUMMARY = PASSPORT / "phi_step_h_desi_dr2_verdict.json"
PHI = (1.0 + math.sqrt(5.0)) / 2.0
ALPHA_REJECT = 0.001


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> tuple[dict, Path, Path]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mean_path = ROOT / manifest["mean_local_path"]
    cov_path = ROOT / manifest["covariance_local_path"]
    for label, path, expected in (
        ("mean", mean_path, manifest["mean_sha256"]),
        ("covariance", cov_path, manifest["covariance_sha256"]),
    ):
        assert path.is_file(), f"SKIP_EXTERNAL_DATA_REQUIRED: missing {label}: {path}"
        actual = sha256(path)
        assert expected and actual == expected, f"hash mismatch for {label}: {actual} != {expected}"
    assert manifest["sample_data"] is False
    assert manifest["status"] == "READY"
    return manifest, mean_path, cov_path


def read_measurements(path: Path) -> tuple[np.ndarray, np.ndarray, list[str]]:
    z: list[float] = []
    values: list[float] = []
    quantities: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        assert len(fields) == 3, f"unexpected mean row: {line}"
        z.append(float(fields[0]))
        values.append(float(fields[1]))
        quantities.append(fields[2])
    return np.asarray(z), np.asarray(values), quantities


def gls_scale(y: np.ndarray, g: np.ndarray, inv_cov: np.ndarray) -> float:
    return float((g @ inv_cov @ y) / (g @ inv_cov @ g))


def fit_fixed_shape(y: np.ndarray, cov: np.ndarray, g: np.ndarray) -> tuple[float, float, np.ndarray]:
    inv_cov = np.linalg.inv(cov)
    scale = gls_scale(y, g, inv_cov)
    assert scale > 0.0
    residual = y - scale * g
    statistic = float(residual @ inv_cov @ residual)
    return scale, statistic, residual


def fit_power_law(z: np.ndarray, y: np.ndarray, cov: np.ndarray) -> tuple[float, float, float]:
    inv_cov = np.linalg.inv(cov)

    def objective(alpha: float) -> float:
        g = np.power(1.0 + z, alpha)
        _, statistic, _ = fit_fixed_shape(y, cov, g)
        return statistic

    result = minimize_scalar(objective, bounds=(-5.0, 5.0), method="bounded")
    assert result.success
    alpha = float(result.x)
    g = np.power(1.0 + z, alpha)
    scale, statistic, _ = fit_fixed_shape(y, cov, g)
    return scale, alpha, statistic


def chi2_survival(statistic: float, dof: int) -> tuple[str, float]:
    """Return an arbitrary-precision tail string and log10 tail (no double underflow)."""
    mp.mp.dps = 80
    half_dof = mp.mpf(dof) / 2
    tail = mp.gammainc(half_dof, mp.mpf(statistic) / 2, mp.inf) / mp.gamma(half_dof)
    assert tail > 0
    return mp.nstr(tail, 12), float(mp.log10(tail))


def main() -> int:
    manifest_preview = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mean_preview = ROOT / manifest_preview["mean_local_path"]
    cov_preview = ROOT / manifest_preview["covariance_local_path"]
    if not mean_preview.is_file() or not cov_preview.is_file():
        assert SUMMARY.is_file(), "missing both raw external cache and committed verdict"
        recorded = json.loads(SUMMARY.read_text(encoding="utf-8"))
        assert recorded["hashes_verified"] is True and recorded["sample_data"] is False
        assert recorded["dataset"] == manifest_preview["dataset_id"]
        print("SKIP_DESI_DR2_BAO_RAW_CACHE_REQUIRED")
        print(f"PASS_RECORDED_VERDICT {recorded['decision']}")
        return 0
    manifest, mean_path, cov_path = load_manifest()
    all_z, all_y, quantities = read_measurements(mean_path)
    all_cov = np.loadtxt(cov_path)
    assert all_cov.shape == (len(all_y), len(all_y))
    assert np.allclose(all_cov, all_cov.T, rtol=0.0, atol=1e-12)
    assert np.linalg.eigvalsh(all_cov).min() > 0.0

    indices = np.asarray([i for i, quantity in enumerate(quantities) if quantity == "DH_over_rs"])
    z = all_z[indices]
    y = all_y[indices]
    cov = all_cov[np.ix_(indices, indices)]
    assert len(y) == 6, f"expected six DESI DR2 DH/rd points, found {len(y)}"

    k = np.floor(np.log1p(z) / math.log(PHI)).astype(int)
    assert k.tolist() == [0, 1, 1, 1, 1, 2], f"step assignment mutated: {k.tolist()}"
    frozen_shape = np.power(PHI, k)
    scale, statistic, residual = fit_fixed_shape(y, cov, frozen_shape)
    dof = len(y) - 1
    p_value, log10_p_value = chi2_survival(statistic, dof)
    decision = (
        "REJECT_DIRECT_PHYSICAL_STEP_H"
        if log10_p_value < math.log10(ALPHA_REJECT)
        else "NOT_REJECTED_DIRECT_PHYSICAL_STEP_H"
    )

    reverse_shape = np.power(PHI, -k)
    reverse_scale, reverse_statistic, _ = fit_fixed_shape(y, cov, reverse_shape)
    power_scale, power_alpha, power_statistic = fit_power_law(z, y, cov)

    # Can-fail controls: the observable inversion and the frozen step allocation must matter.
    assert not np.allclose(frozen_shape, reverse_shape)
    assert statistic > reverse_statistic, "unexpected: frozen increasing DH ladder beats reverse-ladder control"
    assert statistic > power_statistic, "unexpected: frozen step law beats smooth two-parameter diagnostic"

    sigma = np.sqrt(np.diag(cov))
    rows = []
    for zi, yi, ki, model_i, residual_i, sigma_i in zip(z, y, k, scale * frozen_shape, residual, sigma):
        rows.append({
            "z": float(zi),
            "DH_over_rs_observed": float(yi),
            "step_k": int(ki),
            "DH_over_rs_model": float(model_i),
            "residual": float(residual_i),
            "marginal_sigma": float(sigma_i),
            "pull": float(residual_i / sigma_i),
        })

    result = {
        "protocol_id": "PHI-P_DESI_01",
        "leg": "B_DIRECT_PHYSICAL_STEP_H",
        "decision": decision,
        "scope": "conventional Hubble-rate interpretation only; internal D0 depth/frequency laws are not tested here",
        "dataset": manifest["dataset_id"],
        "hashes_verified": True,
        "sample_data": False,
        "no_refit": {
            "phi": True,
            "phase_origin": True,
            "step_boundaries": True,
            "redshift_bins": True,
        },
        "fitted_nuisance_parameters": 1,
        "best_fit_C": scale,
        "chi2": statistic,
        "dof": dof,
        "p_value": p_value,
        "log10_p_value": log10_p_value,
        "alpha_reject": ALPHA_REJECT,
        "controls": {
            "reverse_ladder": {"best_fit_C": reverse_scale, "chi2": reverse_statistic},
            "smooth_power_law": {"best_fit_C": power_scale, "alpha": power_alpha, "chi2": power_statistic},
        },
        "measurements": rows,
    }
    SUMMARY.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== PHI-P_DESI_01 Leg B — DESI DR2 BAO direct step-H test ===")
    print("HASHES_VERIFIED mean+covariance; SAMPLE_DATA=False")
    print(f"STEP_ASSIGNMENT {k.tolist()}; FITTED_ONLY C={scale:.9g}")
    print(f"PRIMARY chi2={statistic:.6f} dof={dof} p={p_value} log10_p={log10_p_value:.6f}")
    print(f"CONTROL_REVERSE chi2={reverse_statistic:.6f}")
    print(f"CONTROL_POWER_LAW alpha={power_alpha:.6f} chi2={power_statistic:.6f}")
    print(decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
