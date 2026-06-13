#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "D0_CANONICAL_FILE_MAP.csv"

SKIP_PARTS = {
    ".git",
    ".codex",
    ".lake",
    ".venv",
    "__pycache__",
    "graphify-out",
}

SKIP_PREFIXES = {
    "tools/graphify/",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    r = rel(path)
    if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
        return True
    if any(r.startswith(prefix) for prefix in SKIP_PREFIXES):
        return True
    if path.suffix == ".pyc":
        return True
    if path.name.endswith("_results.json"):
        return True
    if path.name.endswith("_RESULTS.json") or path.name.endswith("_RESULTS.md"):
        return True
    if path.name.endswith(".zip") or path.name.endswith(".zip.sha256"):
        return True
    if path.name.startswith("D0_v12_") and path.suffix == ".md" and path.parent == ROOT:
        return True
    if path.name.startswith("v") and "patch" in path.name and path.parent.name == "03_THEORY_MAP":
        return True
    if path.name == "D0_v12_42_FOUNDATION_ARCHIVE_INDEX.csv":
        return True
    if path.name == "D0_CANONICAL_FILE_MAP.csv":
        return True
    return False


def category(path: Path) -> str:
    r = rel(path)
    if r.startswith("01_BOOKS/03_COMBINED/"):
        return "book_combined"
    if r.startswith("01_BOOKS/"):
        return "book"
    if r.startswith("09_LEAN_FORMALIZATION/D0/") and path.suffix == ".lean":
        return "lean_module"
    if r.startswith("09_LEAN_FORMALIZATION/docs/"):
        return "lean_doc"
    if r.startswith("09_LEAN_FORMALIZATION/"):
        return "lean_project"
    if r.startswith("05_CERTS/schemas/"):
        return "cert_schema"
    if r.startswith("05_CERTS/ported_legacy_primary/"):
        return "ported_legacy_cert"
    if r.startswith("05_CERTS/") and path.suffix == ".py":
        return "cert_script"
    if r.startswith("05_CERTS/"):
        return "cert_data"
    if r.startswith("03_THEORY_MAP/"):
        return "theory_map"
    if r.startswith("08_PASSPORTS/"):
        return "passport"
    if r.startswith("00_LANGUAGE_NORMALIZATION/"):
        return "language_normalization"
    if r.startswith("D0_LEAN_FULL_TRANSLATION_TZ_"):
        return "lean_translation_spec"
    if r.startswith("docs/"):
        return "docs"
    if r.startswith("tools/"):
        return "tooling"
    if r.startswith(".agents/") or r in {"AGENTS.md", "CLAUDE.md", ".gitignore", ".graphifyignore"}:
        return "agent_config"
    return "project_root"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    rows = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        rows.append(
            {
                "category": category(path),
                "path": rel(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "path", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
