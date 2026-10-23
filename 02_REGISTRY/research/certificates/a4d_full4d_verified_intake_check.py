#!/usr/bin/env python3
"""Replay the complete byte-preserved full-4D local-sheet submission."""
# D0_CI_TIMEOUT_SECONDS=480
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[3]
script=root/'02_REGISTRY/research/sources/d0_full4d_intake_2026-10-15/restore.py'
subprocess.run([sys.executable,str(script)],check=True,timeout=450)
