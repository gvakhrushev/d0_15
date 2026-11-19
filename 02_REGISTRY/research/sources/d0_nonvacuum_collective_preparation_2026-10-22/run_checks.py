#!/usr/bin/env python3
"""Replay only this packet's four changed finite checks and record provenance."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
MAIN = ROOT.parent.parent / "A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md"
CHECKS = (
    ("check_native_attenuation_gain.py", "RESULT_NATIVE_ATTENUATION_GAIN.json"),
    ("global_audit/check_nonvacuum_whole_tape.py", "global_audit/RESULT_NONVACUUM_WHOLE_TAPE.json"),
    ("joint_source/check_paid_coherent_injection.py", "joint_source/RESULT_PAID_COHERENT_INJECTION.json"),
    ("causal_domain/check_paid_joint_normal.py", "causal_domain/RESULT.json"),
)

def run_one(item):
    script, receipt_path = item
    started = time.perf_counter()
    proc = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT,
                          capture_output=True, text=True, check=False)
    if proc.returncode:
        raise RuntimeError(f"{script}: exit {proc.returncode}\n{proc.stderr}\n{proc.stdout}")
    receipt = json.loads(proc.stdout)
    if receipt.get("status") != "PASS":
        raise RuntimeError(f"{script}: non-PASS receipt")
    (ROOT / receipt_path).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return {"script": script, "script_sha256": sha256((ROOT / script).read_bytes()).hexdigest(),
            "exit_code": proc.returncode, "elapsed_seconds": round(time.perf_counter()-started, 6),
            "stderr": proc.stderr, "receipt": receipt_path, "result": receipt}

def main():
    if sys.flags.optimize:
        raise RuntimeError("Run with Python assertions enabled (no -O / PYTHONOPTIMIZE).")
    started = datetime.now(timezone.utc).isoformat()
    with ThreadPoolExecutor(max_workers=len(CHECKS)) as pool:
        runs = list(pool.map(run_one, CHECKS))
    hashes = {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest()
              for p in sorted(ROOT.rglob("*"))
              if p.is_file() and p.name != "RESULT.json"
              and "__pycache__" not in p.parts}
    # Include the causal receipt, excluding only this integrated RESULT.json.
    hashes["causal_domain/RESULT.json"] = sha256((ROOT / "causal_domain/RESULT.json").read_bytes()).hexdigest()
    if MAIN.is_file():
        hashes["../../" + MAIN.name] = sha256(MAIN.read_bytes()).hexdigest()
    result = {
        "status": "PASS", "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "python_optimization": sys.flags.optimize,
        "scope": "Final frozen four-checker replay for the new collective-preparation source application",
        "runs": runs, "artifact_sha256": hashes,
        "enumerated_exact_assertions": sum(r["result"].get("exact_checks", 0)
            + r["result"].get("exact_rational_checks", 0)
            + r["result"].get("assertions", {}).get("exact", 0) for r in runs),
        "floating_assertions": sum(r["result"].get("assertions", {}).get("floating", 0) for r in runs),
        "paid_normal_depths_and_shells_in_addition": True,
        "source_proof_reviewed_independently": True,
        "historical_full42_replayed": False, "historical_full128_replayed": False,
        "historical_compiler_replayed": False, "Lean_rerun": False, "CI_run_claimed": False,
        "full_D0_price_selected": False, "GR_closed": False,
    }
    (ROOT / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": len(runs),
        "enumerated_exact_assertions": result["enumerated_exact_assertions"],
        "floating_assertions": result["floating_assertions"],
        "runs": [{k: r[k] for k in ("script", "exit_code", "elapsed_seconds")} for r in runs],
        "receipt": str(ROOT / "RESULT.json")}, indent=2))

if __name__ == "__main__":
    main()
