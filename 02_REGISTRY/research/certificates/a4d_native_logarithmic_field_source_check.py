#!/usr/bin/env python3
"""Read-only scoped replay; no native support certificate is rerun here."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

INPUTS = ['02_REGISTRY/research/A4D_NATIVE_LOGARITHMIC_FIELD_SOURCE_REDUCTION_2026_10_21.md', '02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/PROOF.md', '02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/README.md', '02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/RESULT.json', '02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/SOURCES.json', '02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/check_source_reduction.py', '02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/SHA256SUMS.json']

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21"

def verify():
    pins = json.loads((PACKET / "SHA256SUMS.json").read_text())
    for name, expected in pins.items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("Input integrity failure: " + name)
    return pins

def main():
    before = verify()
    completed = subprocess.run([sys.executable, "-B", "-O", str(PACKET / "check_source_reduction.py")],
                               check=True, capture_output=True, text=True, timeout=90)
    actual = json.loads(completed.stdout)
    expected = json.loads((PACKET / "RESULT.json").read_text())
    if actual != expected:
        raise RuntimeError("Frozen result mismatch")
    if verify() != before:
        raise RuntimeError("Manifest changed during replay")
    print(json.dumps({"status":"PASS", "checks":actual["checks"],
                      "packet_files_verified":len(before), "native_spectral_replay":False}, sort_keys=True))

if __name__ == "__main__":
    main()
