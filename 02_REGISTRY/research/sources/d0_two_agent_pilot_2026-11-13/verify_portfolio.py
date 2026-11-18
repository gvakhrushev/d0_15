"""Replay independent research checks and verify the listed evidence files."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys


def verify_lane(base, lane):
    for filename, digest in lane["evidence"].items():
        path = (base / filename).resolve()
        if not path.is_relative_to(base) or sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Evidence does not match: {filename}")
    script = lane["check"]
    if script not in lane["evidence"] or Path(script).suffix != ".py":
        raise ValueError(f"Missing pinned Python check: {script}")
    # Several scientific checks use assert. Keep them active under parent optimization.
    check_env = dict(os.environ, PYTHONOPTIMIZE="0")
    result = subprocess.run([sys.executable, "-B", str(base / script)], cwd=base,
                            env=check_env, check=True, capture_output=True)
    receipt = lane.get("stdout_matches")
    if receipt and (receipt not in lane["evidence"] or result.stdout != (base / receipt).read_bytes()):
        raise ValueError(f"Output differs from {receipt}")
    return lane["id"]


def main(manifests, workers=4):
    base = Path(__file__).resolve().parent
    lanes = []
    for manifest in manifests:
        portfolio = json.loads(Path(manifest).read_text(encoding="utf-8"))
        lanes.extend(portfolio["lanes"])
    if not lanes or len({lane["id"] for lane in lanes}) != len(lanes):
        raise ValueError("Expected one unique entry per research lane")
    failed = False
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = {pool.submit(verify_lane, base, lane): lane["id"] for lane in lanes}
        for job in as_completed(jobs):
            name = jobs[job]
            try:
                print(f"PASS  {job.result()}", flush=True)
            except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
                print(f"FAIL  {name}: {exc}", file=sys.stderr)
                if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
                    sys.stderr.buffer.write(exc.stderr)
                failed = True
    return int(failed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="+", metavar="portfolio.json")
    parser.add_argument("--jobs", type=int, default=4, help="concurrent checks (default: 4)")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    sys.exit(main(args.manifests, args.jobs))
