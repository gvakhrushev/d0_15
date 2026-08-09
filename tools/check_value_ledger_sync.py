#!/usr/bin/env python3
"""check_value_ledger_sync.py — value is a MAINTAINED registry field, not a one-off report.

A value ranking that is regenerated once and then drifts is worse than none: the reading order and
the attack queue would point at a corpus that no longer exists. This guard enforces that the value
ledger is a live view of the registry, exactly as the status map already is.

Checks:

  1. COVERAGE      every non-deprecated registry claim has a value-ledger row.
  2. FRESHNESS     regenerating the ledger reproduces the committed file byte-for-byte, so a merged
                   claim or a new Lean module cannot silently leave the ranking stale.
  3. SIGNIFICANCE  every row of D0_EXTERNAL_SIGNIFICANCE.csv names a claim that exists, states an
                   external question, and cites a source. This is the model's only hand-assigned
                   component, so it is the only one that can be inflated — it must stay auditable.
  4. NO ORPHAN CLAIM OF EXTERNAL VALUE: a significance weight of 3 on a claim that is neither
                   closed nor in the attack queue is a contradiction (nothing that important can be
                   unranked); it is reported so the reason is written down, not assumed.

Exit 0 = clean, 1 = drift/violation, 2 = IO.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
LEDGER = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "D0_VALUE_LEDGER.csv"
RANKED = ROOT / "03_THEORY_MAP" / "D0_VALUE_RANKED.md"
SIGNIF = ROOT / "03_THEORY_MAP" / "D0_EXTERNAL_SIGNIFICANCE.csv"


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    failures: list[str] = []
    try:
        reg = read_csv(REGISTRY)
        if not LEDGER.exists() or not RANKED.exists():
            print("FAIL: value ledger missing — run `python tools/d0_value_model.py`", file=sys.stderr)
            return 1
        before_csv = LEDGER.read_bytes()
        before_md = RANKED.read_bytes()
        led = read_csv(LEDGER)
        sig = read_csv(SIGNIF) if SIGNIF.exists() else []
    except OSError as exc:
        print(f"IO error: {exc}", file=sys.stderr)
        return 2

    # 1. coverage
    reg_ids = {r["claim_id"].strip() for r in reg
               if r.get("claim_id", "").strip() and r.get("release_status") != "DEPRECATED"}
    led_ids = {r["claim_id"].strip() for r in led if r.get("claim_id", "").strip()}
    missing = sorted(reg_ids - led_ids)
    if missing:
        failures.append(f"COVERAGE: {len(missing)} claims have no value row: {missing[:5]}")

    # 2. freshness — regenerate and compare
    run = subprocess.run([sys.executable, str(ROOT / "tools" / "d0_value_model.py")],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    if run.returncode != 0:
        failures.append(f"FRESHNESS: d0_value_model.py failed: {run.stderr.strip()[:200]}")
    else:
        if LEDGER.read_bytes() != before_csv:
            failures.append("FRESHNESS: D0_VALUE_LEDGER.csv is stale — regenerate and commit")
        if RANKED.read_bytes() != before_md:
            failures.append("FRESHNESS: D0_VALUE_RANKED.md is stale — regenerate and commit")

    # 3. significance rows are auditable
    all_reg_ids = {r["claim_id"].strip() for r in reg if r.get("claim_id", "").strip()}
    for r in sig:
        cid = (r.get("claim_id") or "").strip()
        if cid not in all_reg_ids:
            failures.append(f"SIGNIFICANCE: {cid} is not a registry claim")
        if not (r.get("external_question") or "").strip():
            failures.append(f"SIGNIFICANCE: {cid} declares a weight with no external question")
        if not (r.get("source") or "").strip():
            failures.append(f"SIGNIFICANCE: {cid} declares a weight with no cited source")
        try:
            w = int((r.get("weight") or "0").strip())
        except ValueError:
            failures.append(f"SIGNIFICANCE: {cid} has a non-integer weight")
            continue
        if not 1 <= w <= 3:
            failures.append(f"SIGNIFICANCE: {cid} weight {w} outside 1..3")

    # 4. weight-3 claims must be ranked somewhere visible
    quad = {r["claim_id"].strip(): r.get("quadrant", "") for r in led}
    for r in sig:
        cid = (r.get("claim_id") or "").strip()
        if (r.get("weight") or "").strip() == "3" and quad.get(cid) in ("BALLAST", "DRIFT"):
            failures.append(f"SIGNIFICANCE: {cid} is declared weight-3 but ranks {quad.get(cid)} — "
                            "either the weight is inflated or the claim is under-connected")

    if failures:
        for f in failures:
            print(f"FAIL {f}", file=sys.stderr)
        return 1
    print(f"value ledger sync OK — {len(led_ids)} ranked claims, {len(sig)} declared significance rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
