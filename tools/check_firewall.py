#!/usr/bin/env python3
"""check_firewall.py - anti-promotion guard mirroring the Lean canPromoteTo firewall.

Static checks (HEAD): no CORE-FORMALIZED row carries bridge assumptions; the
bridge-assumption flag and lean_status agree. Diff checks (vs --base, default
base-v14): no claim promotes from {EMPIRICAL_PASSPORT, EXTERNAL_DATA_REQUIRED,
BRIDGE_CALIBRATION} into CORE_CLOSED; DEPRECATED -> anything needs a notes reason.
Exit 0 = pass, 1 = violations, 2 = IO/usage.
"""
from __future__ import annotations

import argparse
import csv
import io
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_theory_status_map as s  # noqa: E402
import d0_status_model as m  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REL_PATH = "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv"
violations: list[str] = []


def d0status(release: str) -> str | None:
    return m.RELEASE_TO_D0STATUS.get(m.canonical_release(release))


def load_base(ref: str) -> dict[str, dict[str, str]] | None:
    try:
        out = subprocess.run(
            ["git", "show", f"{ref}:{REL_PATH}"],
            cwd=str(s.ROOT), capture_output=True, text=True, encoding="utf-8",
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    reader = csv.DictReader(io.StringIO(out.stdout))
    return {r["claim_id"]: r for r in reader}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="base-v14")
    args = ap.parse_args()

    rows = s.read_csv(s.CLAIM_MAP)

    # Static checks
    for r in rows:
        cid = r["claim_id"]
        release = m.canonical_release(r["release_status"])
        aids = s.split_values(r.get("assumption_ids", ""))
        lean_status = r.get("lean_status", "").strip()
        if release == "CORE-FORMALIZED" and aids:
            violations.append(f"[static] {cid}: CORE-FORMALIZED with bridge assumptions {aids} (canPromoteTo forbids)")
        bridge_flag = r.get("uses_bridge_assumptions", "").strip() == "True"
        if bridge_flag and lean_status not in {"LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS", "PYTHON_CERTIFIED"}:
            violations.append(f"[static] {cid}: uses_bridge_assumptions but lean_status={lean_status}")

    # Diff checks vs base
    base = load_base(args.base)
    if base is None:
        print(f"check_firewall: no baseline '{args.base}' (static checks only)")
    else:
        head = {r["claim_id"]: r for r in rows}
        for cid, hr in head.items():
            br = base.get(cid)
            if not br:
                continue
            base_status = d0status(br["release_status"])
            head_status = d0status(hr["release_status"])
            if head_status == "CORE_CLOSED" and base_status in m.FORBIDDEN_PROMOTIONS_TO_CORE:
                violations.append(
                    f"[promote] {cid}: illegal promotion {br['release_status']} -> {hr['release_status']} "
                    f"({base_status} -> CORE_CLOSED forbidden by canPromoteTo)"
                )
            if m.canonical_release(br["release_status"]) == "DEPRECATED" \
                    and m.canonical_release(hr["release_status"]) != "DEPRECATED" \
                    and not hr.get("notes", "").strip():
                violations.append(f"[promote] {cid}: un-deprecated without a notes reason")

    print(f"check_firewall: {len(rows)} rows checked (base={args.base})")
    if violations:
        print(f"\n!! {len(violations)} FIREWALL VIOLATION(S):")
        for v in violations:
            print("  " + v)
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
