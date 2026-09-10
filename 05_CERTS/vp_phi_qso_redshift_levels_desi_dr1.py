#!/usr/bin/env python3
"""PHI-P_DESI_01 Leg A: frozen phi-level excess statistic on DESI DR1 QSO redshifts.

Requires Astropy only to read the official FITS table.  The data file lives in the ignored
external cache and is accepted only after SHA-256 verification against the official checksum.
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

try:
    from astropy.io import fits
except ImportError as exc:  # pragma: no cover - environment boundary
    raise SystemExit("SKIP_ASTROPY_REQUIRED: install astropy to read the official DESI FITS catalogue") from exc

ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "08_PASSPORTS" / "DESI"
MANIFEST = PASSPORT / "phi_qso_desi_dr1_manifest.json"
SUMMARY = PASSPORT / "phi_qso_desi_dr1_verdict.json"
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
    """P[Binom(core+side, 1/2) >= core], stable far below double p-value range."""
    total = core + side
    assert total > 0
    if core <= total / 2:
        tail = float(binom.sf(core - 1, total, 0.5))
        assert 0 < tail <= 1
        log10_tail = math.log10(tail)
    else:
        # Sum the decreasing upper tail relative to P(X=core).  This avoids the underflow of
        # scipy's probability value while retaining an exact binomial (not Gaussian) statistic.
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
    per_level = []
    pooled_core = 0
    pooled_side = 0
    pooled_outer = 0
    for level in levels:
        distance = np.abs(x - level)
        core = int(np.count_nonzero(distance <= delta))
        side = int(np.count_nonzero((distance > delta) & (distance <= 2.0 * delta)))
        outer = int(np.count_nonzero((distance > 2.0 * delta) & (distance <= 3.0 * delta)))
        p_value, log10_p = binomial_tail(core, side)
        per_level.append({
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
        "per_level": per_level,
    }


def decode_ascii(column: np.ndarray) -> np.ndarray:
    if column.dtype.kind == "S":
        return np.char.decode(column, "ascii", errors="ignore")
    return column.astype(str)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    path = ROOT / manifest["local_path"]
    if not path.is_file():
        assert SUMMARY.is_file(), "missing both raw external cache and committed verdict"
        recorded = json.loads(SUMMARY.read_text(encoding="utf-8"))
        assert recorded["data_sha256"] == manifest["sha256"]
        assert recorded["hash_verified"] is True and recorded["sample_data"] is False
        print("SKIP_DESI_DR1_QSO_RAW_CACHE_REQUIRED")
        print(f"PASS_RECORDED_VERDICT {recorded['decision']} hash={recorded['data_sha256']}")
        return 0
    actual_hash = file_sha256(path)
    assert actual_hash == manifest["sha256"], f"DESI QSO hash mismatch: {actual_hash}"
    assert path.stat().st_size == manifest["size_bytes"]
    assert manifest["sample_data"] is False and manifest["status"] == "READY"
    assert manifest["protocol_frozen_before_value_access"] is True

    with fits.open(path, memmap=True) as hdul:
        table = hdul["QSO_CAT"].data
        names = set(table.names)
        required = {"TARGETID", "Z", "ZERR", "ZWARN", "SURVEY", "PROGRAM"}
        assert required <= names, f"missing required columns: {sorted(required - names)}"
        targetid = np.asarray(table["TARGETID"])
        final_z = np.asarray(table["Z"], dtype=np.float64)
        zerr = np.asarray(table["ZERR"], dtype=np.float64)
        zwarn = np.asarray(table["ZWARN"])
        survey = decode_ascii(np.asarray(table["SURVEY"]))
        program = decode_ascii(np.asarray(table["PROGRAM"]))
        z_rr = np.asarray(table["Z_RR"], dtype=np.float64) if "Z_RR" in names else None
        z_qn = np.asarray(table["Z_QN"], dtype=np.float64) if "Z_QN" in names else None

        selection = (
            np.isfinite(final_z)
            & (final_z > 0.0)
            & (zwarn == 0)
            & (np.char.lower(survey) == "main")
            & (np.char.lower(program) == "dark")
        )
        selected_indices = np.flatnonzero(selection)
        assert len(selected_indices) > 0
        selected_zerr = zerr[selected_indices]
        selected_zerr = np.where(np.isfinite(selected_zerr), selected_zerr, np.inf)
        order = np.lexsort((selected_indices, selected_zerr, targetid[selected_indices]))
        ranked = selected_indices[order]
        ranked_ids = targetid[ranked]
        first = np.concatenate(([True], ranked_ids[1:] != ranked_ids[:-1]))
        keep = ranked[first]

        z = final_z[keep].copy()
        rr = z_rr[keep].copy() if z_rr is not None else None
        qn = z_qn[keep].copy() if z_qn is not None else None
        total_rows = len(table)

    primary = counts_for_levels(z, LEVELS, PRIMARY_DELTA)
    width_controls = {
        str(delta): counts_for_levels(z, LEVELS, delta) for delta in DIAGNOSTIC_DELTAS
    }
    half_phase = counts_for_levels(z, (1.5, 2.5, 3.5), PRIMARY_DELTA)
    leave_one_out = {
        str(int(omitted)): counts_for_levels(
            z, tuple(level for level in LEVELS if level != omitted), PRIMARY_DELTA
        )
        for omitted in LEVELS
    }
    estimator_controls = {}
    if rr is not None:
        estimator_controls["Z_RR"] = counts_for_levels(rr, LEVELS, PRIMARY_DELTA)
    if qn is not None:
        estimator_controls["Z_QN"] = counts_for_levels(qn, LEVELS, PRIMARY_DELTA)

    same_sign = all(row["core"] > row["adjacent_equal_width_control"] for row in primary["per_level"])
    formally_significant = primary["pooled_log10_p_value"] < math.log10(0.001)
    if formally_significant and same_sign:
        decision = "DESI_ONLY_SIGNAL_REQUIRES_INDEPENDENT_REPLICATION"
    elif formally_significant:
        decision = "DESI_SELECTION_STRUCTURE_NOT_COMMON_PHI_LEVEL_SIGNAL"
    else:
        decision = "NO_DESI_LEVEL_EXCESS_AT_FROZEN_PRIMARY_SCALE"

    # Mutation controls are structural and can fail without prescribing the empirical verdict.
    assert PRIMARY_DELTA not in DIAGNOSTIC_DELTAS
    assert half_phase["levels"] != primary["levels"]
    assert all(len(item["levels"]) == 2 for item in leave_one_out.values())
    assert primary["pooled_core"] + primary["pooled_adjacent_equal_width_control"] > 0

    result = {
        "protocol_id": "PHI-P_DESI_01",
        "leg": "A_DESI_DR1_QSO_LEVEL_EXCESS",
        "decision": decision,
        "scope": "DESI catalogue feature only; not an independent physical confirmation",
        "dataset": manifest["dataset_id"],
        "data_sha256": actual_hash,
        "hash_verified": True,
        "sample_data": False,
        "selection": {
            "total_catalogue_rows": total_rows,
            "rows_after_quality_program_selection_before_deduplication": int(len(selected_indices)),
            "unique_targetids_after_deterministic_min_zerr_deduplication": int(len(z)),
            "cuts": ["finite Z", "Z > 0", "ZWARN == 0", "SURVEY == main", "PROGRAM == dark"],
            "deduplication": "minimum finite ZERR, then first file order",
        },
        "primary": primary,
        "controls": {
            "diagnostic_widths": width_controls,
            "half_phase": half_phase,
            "leave_one_level_out": leave_one_out,
            "redshift_estimators_same_spectra_not_independent": estimator_controls,
        },
        "decision_requirements": {
            "pooled_one_sided_alpha": 0.001,
            "all_three_levels_positive": True,
            "independent_replication_required_for_physical_signal": True,
        },
    }
    SUMMARY.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== PHI-P_DESI_01 Leg A — DESI DR1 QSO phi-level excess ===")
    print(f"HASH_VERIFIED {actual_hash}; SAMPLE_DATA=False")
    print(f"SELECTION rows={total_rows} selected={len(selected_indices)} unique={len(z)}")
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
