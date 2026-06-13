from __future__ import annotations

import os
import json
import hashlib
from pathlib import Path
from typing import Any


def get_outdir() -> Path:
    return Path(os.environ.get("D0_OUTDIR", "artifacts")).resolve()


def _ensure(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def ensure_dir(p: Path) -> None:
    _ensure(p)


def save_text(path: Path, text: str) -> None:
    _ensure(path.parent)
    path.write_text(text, encoding="utf-8")
    print(f"[SAVED] {path.as_posix()}")


def save_json(path: Path, obj: Any) -> None:
    save_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def t0_override(default_t0_s: float) -> tuple[float, bool]:
    """
    BRIDGE-only override (allowed input class B).
    Does NOT affect dimensionless CORE PASS/FAIL.
    """
    v = os.environ.get("D0_T0_S", "").strip()
    if not v:
        return default_t0_s, False
    return float(v), True
