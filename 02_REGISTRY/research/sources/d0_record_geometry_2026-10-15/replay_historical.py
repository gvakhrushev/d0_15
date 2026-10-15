#!/usr/bin/env python3
"""Run the historical text adapter with the checked-in publication layout."""
import argparse
from pathlib import Path
import subprocess
import sys

from verify_publication import verify

HERE = Path(__file__).resolve().parent

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--optimized', action='store_true')
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        raise RuntimeError('Python 3.11+ required')
    verify()
    expanded = HERE / 'expanded'
    cmd = [sys.executable, str(HERE / 'replay_historical_text.py'),
           '--resonant-root', str(expanded / 'D0_resonant_synthesis_proof_package_2026-10-15'),
           '--two-syntheses-root', str(expanded / 'D0_two_syntheses_proof_package_2026-10-15'),
           '--joint-root', str(expanded / 'D0_joint_ward_resonance_git_intake_2026-10-15'),
           '--full4d-root', str(expanded / 'PRESERVED_INPUT_full4d_exact_sheet'),
           '--output', str(args.output.resolve())]
    if args.optimized:
        cmd.append('--optimized')
    raise SystemExit(subprocess.run(cmd).returncode)
