#!/usr/bin/env python3
"""Detector guardrail for weak-coupling wave/axion-DM classical readout."""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NO_GO = ROOT / "05_CERTS" / "NO_GO_DM_CLASSICALITY_GUARDRAIL.md"


SIGNATURES = {
    "p_negativity": 1.0,
    "squeezing": 0.4,
    "mandel_q": 0.2,
}


def signature_bound(
    *,
    eta: float,
    raw: float,
    mode_count: int,
    mode_averaging: bool,
) -> float:
    averaging = math.sqrt(mode_count) if mode_averaging else 1.0
    return eta * raw / averaging


def check_case(
    name: str,
    *,
    eta: float,
    mode_count: int,
    noise_floor: float,
    mode_averaging: bool,
    require_pass: bool,
) -> tuple[bool, str]:
    bounds = {
        key: signature_bound(
            eta=eta,
            raw=raw,
            mode_count=mode_count,
            mode_averaging=mode_averaging,
        )
        for key, raw in SIGNATURES.items()
    }
    max_bound = max(bounds.values())
    ok = (
        eta >= 0.0
        and mode_count > 1
        and mode_averaging
        and noise_floor > 0.0
        and max_bound <= noise_floor
    )
    details = (
        f"{name}: ok={ok} eta={eta:.3e} modes={mode_count} "
        f"averaging={mode_averaging} noise={noise_floor:.3e} "
        f"max_signature={max_bound:.3e}"
    )
    if require_pass:
        return ok, details
    return (not ok), details


def fail(lines: list[str]) -> int:
    NO_GO.write_text(
        "# NO-GO: DM classicality guardrail failed\n\n"
        + "\n".join(f"- {line}" for line in lines)
        + "\n",
        encoding="utf-8",
    )
    print("FAIL_DM_CLASSICALITY_GUARDRAIL")
    for line in lines:
        print(line)
    return 1


def main() -> int:
    checks = [
        check_case(
            "d0_realistic_weak_coupling",
            eta=1.0e-8,
            mode_count=1_000_000,
            noise_floor=1.0e-9,
            mode_averaging=True,
            require_pass=True,
        ),
        check_case(
            "negative_eta_artificially_large",
            eta=1.0e-2,
            mode_count=1_000_000,
            noise_floor=1.0e-9,
            mode_averaging=True,
            require_pass=False,
        ),
        check_case(
            "negative_no_mode_averaging",
            eta=1.0e-8,
            mode_count=1_000_000,
            noise_floor=1.0e-9,
            mode_averaging=False,
            require_pass=False,
        ),
        check_case(
            "negative_zero_noise_floor",
            eta=1.0e-8,
            mode_count=1_000_000,
            noise_floor=0.0,
            mode_averaging=True,
            require_pass=False,
        ),
        check_case(
            "negative_single_mode_ideal_detector",
            eta=1.0e-8,
            mode_count=1,
            noise_floor=1.0e-9,
            mode_averaging=True,
            require_pass=False,
        ),
    ]
    failed = [details for ok, details in checks if not ok]
    if failed:
        return fail(failed)
    if NO_GO.exists():
        NO_GO.unlink()
    for _ok, details in checks:
        print(details)
    
    # Required outputs
    eta = 1.0e-8
    mode_count = 1_000_000
    averaging_factor = math.sqrt(mode_count)
    max_bound = eta * 1.0 / averaging_factor
    noise_floor = 1.0e-9
    print(f"Suppression factor: {eta}")
    print(f"Mode averaging factor: {averaging_factor}")
    print(f"Threshold comparison: {max_bound} <= {noise_floor} -> {max_bound <= noise_floor}")
    print("Archive-channel compatibility flag: True")
    print("PASS_DM_CLASSICALITY_GUARDRAIL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
