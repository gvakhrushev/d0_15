#!/usr/bin/env python3
"""Read-only authored replay; inherited native support is not rerun."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

INPUTS = ['02_REGISTRY/research/A4D_EXACT_COHERENT_PREPARATION_STATIONARITY_2026_10_21.md', '02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21/PROOF.md', '02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21/README.md', '02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21/RESULT.json', '02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21/SOURCES.json', '02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21/check_balanced_stationarity.py', '02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21/SHA256SUMS.json']
ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_balanced_preparation_stationarity_2026-10-21"

def verify():
    raw = (PACKET / "SHA256SUMS.json").read_bytes()
    pins = json.loads(raw)
    for name, expected in pins.items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("Input integrity failure: " + name)
    return raw

def main():
    before = verify()
    run = subprocess.run([sys.executable, "-B", "-O", str(PACKET / "check_balanced_stationarity.py")],
                         check=True, capture_output=True, timeout=90)
    if run.stdout != (PACKET / "RESULT.json").read_bytes():
        raise RuntimeError("Frozen result byte mismatch")
    if verify() != before:
        raise RuntimeError("Manifest changed during replay")
    actual = json.loads(run.stdout)
    print(json.dumps({"status":"PASS", "checks":actual["checks"],
                      "packet_files_verified":len(json.loads(before)),
                      "native_support_replayed":False, "independent_review":False}, sort_keys=True))

if __name__ == "__main__":
    main()
