#!/usr/bin/env python3
"""Detect registry theorem names absent from Lean source declarations.

This lexical scan is a lower bound: matching short names do not establish a
namespace, type, or proof. Resolve a candidate against Lean before changing an
owner. The non-growth check reports the documented unresolved reference.
Use --strict to fail on every unresolved name, including the known baseline.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
KNOWN_UNRESOLVED = {
    (
        "D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001",
        "archive_naive_weighted_degree_leakage_nogo_owner",
    ),
}
DECLARATION = re.compile(
    r"\b(?:theorem|lemma|def|abbrev|structure|inductive|class|axiom|opaque)"
    r"\s+([^\W\d][\w'?!]*(?:\.[^\W\d][\w'?!]*)*)"
)
CHARACTER = re.compile(r"'(?:\\(?:u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|.)|[^'\\\n])'")


def erase_comments_and_strings(source: str) -> str:
    """Preserve code while masking Lean strings and nested or line comments."""
    result = []
    position = 0
    depth = 0
    in_string = False
    while position < len(source):
        current = source[position]
        pair = source[position:position + 2]
        if depth:
            if pair == "/-":
                depth += 1
                result.append("  ")
                position += 2
            elif pair == "-/":
                depth -= 1
                result.append("  ")
                position += 2
            else:
                result.append("\n" if current == "\n" else " ")
                position += 1
        elif in_string:
            if current == "\\" and position + 1 < len(source):
                result.append("  ")
                position += 2
            elif current == '"':
                in_string = False
                result.append(" ")
                position += 1
            else:
                result.append("\n" if current == "\n" else " ")
                position += 1
        elif pair == "/-":
            depth = 1
            result.append("  ")
            position += 2
        elif pair == "--":
            end = source.find("\n", position)
            if end == -1:
                result.append(" " * (len(source) - position))
                break
            result.append(" " * (end - position))
            position = end
        elif current == "'" and (
            position == 0
            or not (source[position - 1].isalnum() or source[position - 1] in "_'")
        ) and (character := CHARACTER.match(source, position)) is not None:
            length = character.end() - position
            result.append(" " * length)
            position = character.end()
        elif current == '"':
            in_string = True
            result.append(" ")
            position += 1
        else:
            result.append(current)
            position += 1
    if depth or in_string:
        raise ValueError("Unterminated comment or string in Lean source")
    return "".join(result)


def find_unresolved(root: Path) -> tuple[set[tuple[str, str]], int]:
    declarations: set[str] = set()
    for path in (root / "03_FORMALIZATION" / "D0").rglob("*.lean"):
        source = path.read_text(encoding="utf-8")
        declarations.update(
            name.rsplit(".", 1)[-1]
            for name in DECLARATION.findall(erase_comments_and_strings(source))
        )

    unresolved: set[tuple[str, str]] = set()
    checked = 0
    with (root / "02_REGISTRY" / "claims.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        for row in csv.DictReader(source):
            if not row["lean_module"].strip():
                continue
            for entry in row["lean_theorem"].split(";"):
                name = entry.strip()
                if not name:
                    continue
                checked += 1
                if name.rsplit(".", 1)[-1] not in declarations:
                    unresolved.add((row["claim_id"], name))
    return unresolved, checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true", help="fail if any name remains unresolved"
    )
    args = parser.parse_args()
    unresolved, checked = find_unresolved(ROOT)
    for claim, name in sorted(unresolved):
        print(f"UNRESOLVED {claim} {name}")
    unexpected = unresolved - KNOWN_UNRESOLVED
    resolved = KNOWN_UNRESOLVED - unresolved
    if unexpected or resolved:
        print("FAIL: unresolved Lean reference baseline changed; review the declarations")
        return 1
    if args.strict and unresolved:
        print(f"FAIL: {len(unresolved)} unresolved Lean references")
        return 1
    print(
        f"PASS non-growth: {checked} registry references scanned, "
        f"{len(unresolved)} known unresolved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
