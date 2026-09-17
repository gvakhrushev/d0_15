"""Runtime-output helpers for D0 certificates.

Certificate code and immutable inputs live in ``04_CERTIFICATES``.  Anything
produced by executing a certificate belongs under ignored ``.build`` so a
certificate run cannot create a second source of truth in the release tree.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def output_dir(script_file: str | Path) -> Path:
    d = ROOT / ".build" / "cert_outputs" / Path(script_file).stem
    d.mkdir(parents=True, exist_ok=True)
    return d


def output_path(script_file: str | Path, name: str) -> Path:
    return output_dir(script_file) / name
