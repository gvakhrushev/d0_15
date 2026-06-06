#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path

INCLUDE = ["books", "d0", "cert", "protocols", "tools", "data", ".github", "README.md"]
OUT = "D0_PUBLICATION_MANIFEST_GOLDEN_PASS30.txt"
EXCLUDE_NAMES = {".DS_Store"}


def main() -> int:
    root = Path(".").resolve()
    lines = []
    for item in INCLUDE:
        p = root / item
        files = [p] if p.is_file() else [x for x in p.rglob("*") if x.is_file()]
        for f in sorted(files):
            rel = f.relative_to(root).as_posix()
            if (
                rel.startswith("artifacts/")
                or "/__pycache__/" in rel
                or f.name in EXCLUDE_NAMES
            ):
                continue
            b = f.read_bytes()
            sha = hashlib.sha256(b).hexdigest()
            lines.append(f"{rel}  sha256={sha}  bytes={len(b)}")
    (root / OUT).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[WROTE] {OUT} ({len(lines)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
