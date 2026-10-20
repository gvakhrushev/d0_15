"""Read-only targeted checks for the new source-selection application."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/"00_WORK"/"manifest.json").is_file())
parser = argparse.ArgumentParser()
parser.add_argument("--node", default=shutil.which("node"))
parser.add_argument("--output", type=Path)
parser.add_argument("--only", action="append", help="Run only a named changed check")
args = parser.parse_args()
if not args.node:
    raise SystemExit("Node.js is required; pass --node /absolute/path/to/node")
if args.output and args.output.resolve() == (HERE/"VALIDATION.json").resolve():
    raise SystemExit("Refusing to overwrite the preserved validation receipt")

jobs = [
    ("residual_transport", HERE/"check_residual_transport.py"),
    ("record_algebras", HERE/"records/check_record_algebras.py"),
    ("prospective_selection", HERE/"records/check_prospective_selection.py"),
    ("compiler_ticks", HERE/"metric/check_compiler_ticks.py"),
    ("schur_completion", HERE/"metric/check_schur_completion.py"),
    ("refinement_transport", HERE/"metric/check_refinement_schur.py"),
    ("empirical_endpoint", HERE/"history/check_empirical_endpoint.py"),
    ("empirical_source", HERE/"history/check_empirical_c1_source.mjs"),
    ("fisher_horizon", HERE/"history/check_native_fisher_horizon.mjs"),
    ("beatty_law", HERE/"history/check_native_beatty_boundary.mjs"),
    ("owned_beatty_residual", ROOT/"02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/check_phi_beatty_owned_residual.py"),
    ("stopped_source", ROOT/"02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/check_stopped_source_minimum.py"),
]
jobs.append(("adaptive_stopping", HERE/"records/check_adaptive_stopping.py"))
jobs.extend([
    ("adaptive_all_cost", HERE/"records/check_adaptive_all_cost.py"),
    ("stopped_all_cost", ROOT/"02_REGISTRY/research/certificates/a4d_native_stopped_all_cost_source_check.py"),
])
if args.only:
    unknown = set(args.only)-{name for name,_ in jobs}
    if unknown:
        raise SystemExit("Unknown checks: "+", ".join(sorted(unknown)))
    jobs = [(name,path) for name,path in jobs if name in args.only]
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for _,p in jobs}
results = []
for name, path in jobs:
    command = [args.node, str(path)] if path.suffix == ".mjs" else [sys.executable, "-B", str(path)]
    start = time.monotonic()
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    record = {"name": name, "path": str(path.relative_to(ROOT)),
              "exit_code": completed.returncode,
              "seconds": round(time.monotonic()-start,6),
              "stdout": completed.stdout, "stderr": completed.stderr}
    results.append(record)
    print(f"{'PASS' if completed.returncode == 0 else 'FAIL'} {name}", flush=True)
    if completed.returncode:
        print(completed.stdout+completed.stderr)
        break
after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
         for _,p in jobs}
assert before == after, "A checker changed during execution"
receipt = {
    "schema": "d0-source-selection-targeted-checks/1",
    "baseline": subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
    "python": sys.version,
    "node": subprocess.check_output([args.node,"--version"],text=True).strip(),
    "checker_sha256": before,
    "results": results,
    "passed": len(results)==len(jobs) and all(r["exit_code"]==0 for r in results),
    "scope": "Targeted finite checks plus analytical proofs; no physical Book selection or GR closure",
}
if args.output:
    args.output.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
if not receipt["passed"]:
    raise SystemExit(1)
print(f"PASS all {len(results)} targeted checks; no scientific status changed")
