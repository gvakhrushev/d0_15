#!/usr/bin/env python3
"""PHI-P_DESI_01 independent-survey replication on SDSS DR16Q.

Uses the same levels, coordinate, primary width, statistic and decision threshold frozen for DESI.
Only the catalogue-specific reader differs.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.special import gammaln
from scipy.stats import binom

ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "05_EXPERIMENTS" / "DESI"
MANIFEST = PASSPORT / "phi_qso_sdss_dr16q_manifest.json"
SUMMARY = PASSPORT / "phi_qso_sdss_dr16q_verdict.json"
PHI = (1.0 + math.sqrt(5.0)) / 2.0
LEVELS = (1.0, 2.0, 3.0)
PRIMARY_DELTA = 0.01
DIAGNOSTIC_DELTAS = (0.005, 0.02)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def binomial_tail(core: int, side: int) -> tuple[str, float]:
    total = core + side
    assert total > 0
    if core <= total / 2:
        tail = float(binom.sf(core - 1, total, 0.5))
        assert 0 < tail <= 1
        log10_tail = math.log10(tail)
    else:
        log_pmf = (
            gammaln(total + 1)
            - gammaln(core + 1)
            - gammaln(total - core + 1)
            - total * math.log(2.0)
        )
        relative_sum = 1.0
        term = 1.0
        for value in range(core, total):
            term *= (total - value) / (value + 1)
            relative_sum += term
            if term < 1e-16 * relative_sum:
                break
        log10_tail = (log_pmf + math.log(relative_sum)) / math.log(10.0)
    exponent = math.floor(log10_tail)
    mantissa = 10.0 ** (log10_tail - exponent)
    return f"{mantissa:.11f}e{exponent:+d}", log10_tail


def counts_for_levels(z: np.ndarray, levels: tuple[float, ...], delta: float) -> dict[str, Any]:
    good = np.isfinite(z) & (z > 0.0)
    x = np.log1p(z[good]) / math.log(PHI)
    rows = []
    pooled_core = 0
    pooled_side = 0
    pooled_outer = 0
    for level in levels:
        distance = np.abs(x - level)
        core = int(np.count_nonzero(distance <= delta))
        side = int(np.count_nonzero((distance > delta) & (distance <= 2.0 * delta)))
        outer = int(np.count_nonzero((distance > 2.0 * delta) & (distance <= 3.0 * delta)))
        p_value, log10_p = binomial_tail(core, side)
        rows.append({
            "level": level,
            "z_level": PHI ** level - 1.0,
            "core": core,
            "adjacent_equal_width_control": side,
            "outer_equal_width_control": outer,
            "core_fraction": core / (core + side),
            "one_sided_p_value": p_value,
            "log10_p_value": log10_p,
        })
        pooled_core += core
        pooled_side += side
        pooled_outer += outer
    pooled_p, pooled_log10_p = binomial_tail(pooled_core, pooled_side)
    return {
        "levels": list(levels),
        "delta": delta,
        "finite_positive_redshifts": int(good.sum()),
        "pooled_core": pooled_core,
        "pooled_adjacent_equal_width_control": pooled_side,
        "pooled_outer_equal_width_control": pooled_outer,
        "pooled_core_fraction": pooled_core / (pooled_core + pooled_side),
        "pooled_one_sided_p_value": pooled_p,
        "pooled_log10_p_value": pooled_log10_p,
        "per_level": rows,
    }


def read_vizier_tsv(path: Path) -> tuple[list[str], np.ndarray]:
    identifiers: list[str] = []
    redshifts: list[float] = []
    in_data = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not in_data:
            if raw.startswith("------------------"):
                in_data = True
            continue
        if not raw.strip() or raw.startswith("#"):
            continue
        fields = raw.split("\t")
        assert len(fields) == 2, f"unexpected VizieR row: {raw[:120]}"
        identifiers.append(fields[0].strip())
        redshift = fields[1].strip()
        redshifts.append(float(redshift) if redshift else math.nan)
    return identifiers, np.asarray(redshifts, dtype=np.float64)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    path = ROOT / manifest["local_path"]
    if not path.is_file():
        assert SUMMARY.is_file(), "missing both raw external cache and committed verdict"
        recorded = json.loads(SUMMARY.read_text(encoding="utf-8"))
        assert recorded["data_sha256"] == manifest["sha256"]
        assert recorded["hash_verified"] is True and recorded["sample_data"] is False
        print("SKIP_SDSS_DR16Q_RAW_CACHE_REQUIRED")
        print(f"PASS_RECORDED_VERDICT {recorded['decision']} hash={recorded['data_sha256']}")
        return 0
    actual_hash = file_sha256(path)
    assert actual_hash == manifest["sha256"]
    assert manifest["sample_data"] is False and manifest["status"] == "READY"
    assert manifest["same_frozen_levels_and_statistic_as_desi"] is True

    identifiers, z = read_vizier_tsv(path)
    assert len(z) == manifest["expected_rows"], f"row count {len(z)} != {manifest['expected_rows']}"
    assert len(set(identifiers)) == len(identifiers), "SDSS quasar-only identifiers must be unique"

    primary = counts_for_levels(z, LEVELS, PRIMARY_DELTA)
    width_controls = {
        str(delta): counts_for_levels(z, LEVELS, delta) for delta in DIAGNOSTIC_DELTAS
    }
    half_phase = counts_for_levels(z, (1.5, 2.5, 3.5), PRIMARY_DELTA)
    same_sign = all(row["core"] > row["adjacent_equal_width_control"] for row in primary["per_level"])
    significant = primary["pooled_log10_p_value"] < math.log10(0.001)
    decision = (
        "INDEPENDENT_SDSS_LEVEL_EXCESS_REPLICATION"
        if significant and same_sign
        else "NO_INDEPENDENT_SDSS_LEVEL_EXCESS_REPLICATION"
    )

    assert PRIMARY_DELTA not in DIAGNOSTIC_DELTAS
    assert half_phase["levels"] != primary["levels"]
    result = {
        "protocol_id": "PHI-P_DESI_01",
        "leg": "A2_SDSS_DR16Q_INDEPENDENT_SURVEY_REPLICATION",
        "decision": decision,
        "scope": "independent survey/instrument/pipeline replication; exact object overlap with DESI not removed",
        "dataset": manifest["dataset_id"],
        "data_sha256": actual_hash,
        "hash_verified": True,
        "sample_data": False,
        "rows": len(z),
        "primary": primary,
        "controls": {"diagnostic_widths": width_controls, "half_phase": half_phase},
        "decision_requirements": {
            "same_frozen_statistic_as_desi": True,
            "pooled_one_sided_alpha": 0.001,
            "all_three_levels_positive": True,
        },
    }
    SUMMARY.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== PHI-P_DESI_01 Leg A2 — SDSS DR16Q independent-survey replication ===")
    print(f"HASH_VERIFIED {actual_hash}; SAMPLE_DATA=False; rows={len(z)}")
    print(
        "PRIMARY "
        f"core={primary['pooled_core']} side={primary['pooled_adjacent_equal_width_control']} "
        f"fraction={primary['pooled_core_fraction']:.9f} "
        f"p={primary['pooled_one_sided_p_value']} log10_p={primary['pooled_log10_p_value']:.6f}"
    )
    for row in primary["per_level"]:
        print(
            f"LEVEL n={row['level']:.0f} z={row['z_level']:.9f} "
            f"core={row['core']} side={row['adjacent_equal_width_control']} "
            f"fraction={row['core_fraction']:.9f} log10_p={row['log10_p_value']:.6f}"
        )
    print(decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
