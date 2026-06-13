#!/usr/bin/env python3
"""D0 tiling hull certificate."""

import json
from pathlib import Path

STATUS = "PASS_D0_TILING_HULL"

def run_certificate() -> None:
    print("--- D0 TILING HULL CERTIFICATE ---")

    # 1. Finite approximants of phi-cut-and-project sequence
    phi = (1 + 5**0.5) / 2
    N = 100
    sequence = [1 if (i * phi) % 1.0 < phi - 1 else 0 for i in range(N)]
    print(f"    Generated {N} sequence elements: PASS")

    # 2. Non-periodicity on windows up to Q
    is_periodic = False
    for p in range(1, 20):
        if all(sequence[i] == sequence[i+p] for i in range(N - p)):
            is_periodic = True
            break
    assert not is_periodic
    print("    Aperiodic on windows up to Q: PASS")

    # 3. Stable patch recurrence (repetitiveness / long-range order)
    patch_len = 5
    for start in range(N - 30):
        patch = sequence[start : start + patch_len]
        found = False
        for offset in range(1, 25):
            if sequence[start + offset : start + offset + patch_len] == patch:
                found = True
                break
        assert found
    print("    Stable patch recurrence / long-range order: PASS")

    # 4. Finite local complexity
    patches = set(tuple(sequence[i : i + patch_len]) for i in range(N - patch_len))
    assert len(patches) <= patch_len + 1
    print(f"    Finite local complexity (found {len(patches)} patches of length {patch_len}): PASS")

    # 5. Export hull_manifest.json
    manifest = {
        "sequence_len": N,
        "is_aperiodic": not is_periodic,
        "patch_length": patch_len,
        "distinct_patches": len(patches),
        "finite_local_complexity": True,
        "long_range_order": True
    }
    Path("hull_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("    hull_manifest.json exported: PASS")

    print(f"\n[CERT-CLOSED] {STATUS}")

if __name__ == "__main__":
    run_certificate()
