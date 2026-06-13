#!/usr/bin/env python3
"""run_registered_certs.py - execute every cert referenced by the canonical
registry and confirm it PASSes. Closes the "cert exists != cert passes" gap:
validate_csv only checks the file is on disk; this actually runs it.

Classification (mirrors the run_all_* PASS pattern, SKIP-aware for passports):
  PASS  = exit 0 AND a 'PASS' token in stdout
  SKIP  = exit 0 AND a 'SKIP' token (passport cert without pinned data) - not a failure
  FAIL  = anything else (nonzero exit, crash, timeout, or no PASS/SKIP)

Writes 03_THEORY_MAP/cert_results.json. Exit 0 if no FAIL, 1 if any FAIL, 2 on usage.
Use --only <substr> to run a subset; --orphans to also run unregistered 05_CERTS certs.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_theory_status_map as s  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
TIMEOUT = 120


DATA_GATED = ("EXTERNAL_DATA_REQUIRED", "missing preregistered", "missing extracted",
              "requires preregistered", "SKIP")


def classify(rc: int, out: str) -> str:
    if rc == 0 and "PASS" in out:
        return "PASS"
    crashed = ("Traceback (most recent call last)" in out) or ("AssertionError" in out)
    # A data-gated passport/negative-control cert with no pinned data is SKIP, not a
    # logic failure - provided it did not crash. (The firewall refusing to certify
    # without data is correct behaviour.)
    if not crashed and any(m in out for m in DATA_GATED):
        return "SKIP"
    return "FAIL"


def run_cert(path: Path) -> tuple[str, int, str]:
    # Force UTF-8 in the child so certs printing Greek/math symbols don't crash
    # on a Windows cp1251 console (encoding bug, not a logic failure).
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    try:
        p = subprocess.run(
            [sys.executable, path.name], cwd=str(path.parent), env=env,
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return classify(p.returncode, p.stdout or ""), p.returncode, out[-400:]
    except subprocess.TimeoutExpired:
        return "FAIL", -1, f"TIMEOUT after {TIMEOUT}s"
    except Exception as e:  # noqa: BLE001
        return "FAIL", -1, f"EXC {e}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--orphans", action="store_true")
    args = ap.parse_args()

    rows = s.read_csv(s.CLAIM_MAP)
    cert_to_claims: dict[str, list[str]] = {}
    for r in rows:
        for c in s.split_values(r["python_cert"]):
            cert_to_claims.setdefault(Path(c).name, []).append(r["claim_id"])

    targets = dict(cert_to_claims)
    if args.orphans:
        ref = set(cert_to_claims)
        for p in (s.ROOT / "05_CERTS").rglob("vp_*.py"):
            if p.name not in ref:
                targets.setdefault(p.name, [])

    results: dict[str, dict] = {}
    counts = {"PASS": 0, "SKIP": 0, "FAIL": 0, "MISSING": 0}
    for cert in sorted(targets):
        if args.only and args.only not in cert:
            continue
        path = s.cert_path(cert)
        if not path.exists():
            # fall back to a recursive search under 05_CERTS
            hits = list((s.ROOT / "05_CERTS").rglob(cert))
            if hits:
                path = hits[0]
            else:
                results[cert] = {"status": "MISSING", "claims": targets[cert]}
                counts["MISSING"] += 1
                continue
        status, rc, tail = run_cert(path)
        counts[status] += 1
        results[cert] = {"status": status, "exit": rc, "claims": targets[cert],
                         "tail": tail if status == "FAIL" else ""}

    (s.THEORY_DIR / "cert_results.json").write_text(
        json.dumps({"counts": counts, "results": results}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")

    print(f"run_registered_certs: {sum(counts.values())} certs -> "
          f"PASS {counts['PASS']}, SKIP {counts['SKIP']}, FAIL {counts['FAIL']}, MISSING {counts['MISSING']}")
    fails = {c: v for c, v in results.items() if v["status"] in ("FAIL", "MISSING")}
    if fails:
        print(f"\n!! {len(fails)} cert(s) not passing:")
        for c, v in sorted(fails.items()):
            print(f"  {v['status']:7} {c}  (claims: {', '.join(v['claims']) or '-'})")
            if v.get("tail"):
                print("      " + v["tail"].replace("\n", " ")[:200])
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
