#!/usr/bin/env python3
from __future__ import annotations
import re, hashlib
from pathlib import Path

MANIFEST = "D0_PUBLICATION_MANIFEST_GOLDEN_PASS30.txt"
RX = re.compile(r"^(?P<path>\S+)\s+sha256=(?P<sha>[0-9a-f]{64})\s+bytes=(?P<bytes>\d+)\s*$")
INCLUDE = ["books", "d0", "cert", "protocols", "tools", "data", ".github", "README.md"]
EXCLUDE_NAMES = {".DS_Store"}


def iter_expected_files(root: Path) -> list[str]:
    files: list[str] = []
    for item in INCLUDE:
        p = root / item
        entries = [p] if p.is_file() else [x for x in p.rglob("*") if x.is_file()]
        for f in entries:
            rel = f.relative_to(root).as_posix()
            if (
                rel.startswith("artifacts/")
                or "/__pycache__/" in rel
                or f.name in EXCLUDE_NAMES
            ):
                continue
            files.append(rel)
    return sorted(files)


def main() -> int:
    root = Path(".").resolve()
    bad = 0
    manifest_entries: dict[str, tuple[str, int]] = {}
    for line in (root / MANIFEST).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        m = RX.match(line)
        if not m:
            print(f"[BAD LINE] {line}")
            bad += 1
            continue
        manifest_entries[m["path"]] = (m["sha"], int(m["bytes"]))

    expected_files = set(iter_expected_files(root))
    manifest_files = set(manifest_entries.keys())
    missing = sorted(expected_files - manifest_files)
    unexpected = sorted(manifest_files - expected_files)
    for path in missing:
        print(f"[MISSING IN MANIFEST] {path}")
        bad += 1
    for path in unexpected:
        print(f"[UNEXPECTED] {path}")
        bad += 1

    for path, (sha_expected, bytes_expected) in manifest_entries.items():
        p = root / path
        if not p.exists():
            print(f"[MISSING] {path}")
            bad += 1
            continue
        b = p.read_bytes()
        sha = hashlib.sha256(b).hexdigest()
        if sha != sha_expected or len(b) != bytes_expected:
            print(f"[MISMATCH] {path}")
            bad += 1
    if bad:
        print(f"[FAIL] {bad} problems")
        return 2
    print("[OK] manifest matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
