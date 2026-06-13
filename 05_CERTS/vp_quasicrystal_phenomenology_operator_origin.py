#!/usr/bin/env python3
"""One-command bundle for D0-QUASI-002 phenomenology operator origin."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PASS_TOKEN = "PASS_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN"

CERTS = [
    ("vp_quasi_generation_inflation.py", "PASS_QUASI_GENERATION_INFLATION_ORBIT"),
    ("vp_archive_phason_dark_matter.py", "PASS_DARK_PHASON_STRAIN"),
    ("vp_window_offset_chirality.py", "PASS_CHIRAL_WINDOW_OFFSET"),
    ("vp_phason_flip_inertia.py", "PASS_INERTIA_PHASON_FLIP_DRAG"),
    ("vp_window_fractional_charge.py", "PASS_FRACTIONAL_CHARGE_WINDOW_WEIGHT"),
]


def main() -> dict:
    here = Path(__file__).resolve().parent
    results = []
    for script, token in CERTS:
        proc = subprocess.run(
            [sys.executable, str(here / script)],
            cwd=str(here.parent),
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        ok = proc.returncode == 0 and token in proc.stdout
        results.append(
            {
                "script": script,
                "expected_token": token,
                "ok": ok,
                "output": proc.stdout,
            }
        )
    checks = {row["script"]: row["ok"] for row in results}
    status = PASS_TOKEN if all(checks.values()) else "FAIL"
    return {"status": status, "checks": checks, "results": results}


if __name__ == "__main__":
    out = main()
    here = Path(__file__).resolve().parent
    (here / "vp_quasicrystal_phenomenology_operator_origin_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out["status"])
    for name, ok in out["checks"].items():
        print(f"{name}: {ok}")
    if out["status"] != PASS_TOKEN:
        raise SystemExit(1)
