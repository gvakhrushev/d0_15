#!/usr/bin/env python3
"""Generate a book-to-claim mention index from the canonical registry."""
from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "02_REGISTRY" / "claims.csv"
OUTPUT = ROOT / "02_REGISTRY" / "book_claim_coverage.csv"
FIELDS = ("claim_id", "release_status", "lean_status", "declared_book", "lean_module", "book_mentions")


def render() -> tuple[str, int, int]:
    mentions_by_id: dict[str, list[str]] = {}
    token = re.compile(r"(?<![A-Z0-9-])D0-[A-Z0-9-]+")
    for path in sorted((ROOT / "01_BOOKS").glob("BOOK_*.md")):
        for claim_id in set(token.findall(path.read_text(encoding="utf-8"))):
            mentions_by_id.setdefault(claim_id, []).append(path.name[:7])
    with REGISTRY.open(encoding="utf-8", newline="") as source:
        claims = list(csv.DictReader(source))

    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    unmentioned = 0
    for claim in sorted(claims, key=lambda row: row["claim_id"]):
        mentions = mentions_by_id.get(claim["claim_id"], [])
        unmentioned += not mentions
        writer.writerow({
            "claim_id": claim["claim_id"],
            "release_status": claim["release_status"],
            "lean_status": claim["lean_status"],
            "declared_book": claim["book"],
            "lean_module": claim["lean_module"],
            "book_mentions": ";".join(mentions),
        })
    return output.getvalue(), len(claims), unmentioned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the committed index")
    args = parser.parse_args()
    content, total, unmentioned = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            print("FAIL book claim coverage index is stale")
            return 1
    else:
        OUTPUT.write_text(content, encoding="utf-8", newline="")
    print(f"PASS book claim coverage claims={total} without_id_mention={unmentioned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
