#!/usr/bin/env python3
"""check_book_cert_references.py - prose<->registry phantom-cert guard.

Scans 01_BOOKS/*.md (and 00_*/03_THEORY_MAP narrative) for vp_*.py cert tokens.
A cited cert is a PHANTOM violation if it is absent on disk AND not present in the
canonical registry as an OPEN/PROOF-TARGET placeholder row. Per
D0_CLAIM_CLOSURE_CONTRACT.md ("a cert that can't FAIL is not a cert"), prose may
not cite a cert that does not exist and is not even a declared work item.

Exit 0 = pass, 1 = phantom citations found, 2 = IO/usage.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_theory_status_map as s  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CERT_RE = re.compile(r"vp_[A-Za-z0-9_]+\.py")
SCAN_GLOBS = ["01_BOOKS/*.md"]
CERT_DIRS = [s.ROOT / "05_CERTS", s.ROOT / "05_CERTS" / "ported_legacy_primary"]


def cert_on_disk(name: str) -> bool:
    if s.cert_path(name).exists():
        return True
    # also accept ported_legacy_primary/**/<name>
    for hit in (s.ROOT / "05_CERTS").rglob(name):
        if hit.is_file():
            return True
    return False


def main() -> int:
    rows = s.read_csv(s.CLAIM_MAP)
    # certs that are legitimately declared but not-yet-written (OPEN/PROOF-TARGET placeholders)
    declared_open: set[str] = set()
    registry_certs: set[str] = set()
    for r in rows:
        for c in s.split_values(r.get("python_cert", "")):
            registry_certs.add(Path(c).name)
            if r.get("lean_status", "").strip() == "OPEN" or r.get("release_status", "").strip() == "PROOF-TARGET":
                declared_open.add(Path(c).name)

    phantoms: dict[str, list[str]] = {}
    cited: set[str] = set()
    for pattern in SCAN_GLOBS:
        for md in sorted(s.ROOT.glob(pattern)):
            text = md.read_text(encoding="utf-8", errors="ignore")
            for ln, line in enumerate(text.splitlines(), 1):
                for tok in CERT_RE.findall(line):
                    cited.add(tok)
                    if not cert_on_disk(tok) and tok not in declared_open:
                        phantoms.setdefault(tok, []).append(f"{md.relative_to(s.ROOT).as_posix()}:{ln}")

    print(f"check_book_cert_references: {len(cited)} distinct cert tokens cited in prose")
    if phantoms:
        print(f"\n!! {len(phantoms)} PHANTOM cert(s) cited in prose (absent on disk, not a declared OPEN/PROOF-TARGET):")
        for tok, locs in sorted(phantoms.items()):
            in_reg = " (in registry as non-open!)" if tok in registry_certs else ""
            print(f"  {tok}{in_reg}")
            for loc in locs[:6]:
                print(f"      {loc}")
            if len(locs) > 6:
                print(f"      ... +{len(locs) - 6} more")
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
