#!/usr/bin/env python3
from pathlib import Path
import argparse
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
D0 = ROOT / "D0"
ASSUMPTION_LEDGER = ROOT / "docs" / "LEAN_ASSUMPTION_LEDGER.csv"

CORE_FORBIDDEN = ["sorry", "admit", "axiom", "unsafe", "Float", "constant", "opaque"]
CORE_DIRS = {"Core", "Combinatorics", "Topology", "Algebra", "Gauge"}
ALLOWED_TYPES = {
    "CONDENSED_BRIDGE",
    "QFT_RG_BRIDGE",
    "EMPIRICAL_DATA",
    "SMOOTH_LIMIT",
    "MACRO_LIMIT",
    "PHYSICS_DICTIONARY",
    "LIE_ALGEBRA_LIBRARY_GAP",
}
FORBIDDEN_TYPES = {"CORE", "FOUNDATION", "UNSPECIFIED", ""}


def strip_line_comment(line: str) -> str:
    return line.split("--", 1)[0]


def read_code(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return "\n".join(strip_line_comment(line) for line in text.splitlines())


def load_assumptions():
    with ASSUMPTION_LEDGER.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    by_name = {row["lean_name"]: row for row in rows}
    by_file = {}
    for row in rows:
        by_file.setdefault(row["lean_file"].replace("\\", "/"), []).append(row)
    return rows, by_name, by_file


def is_core_file(rel: Path) -> bool:
    return rel.parts and rel.parts[0] in CORE_DIRS


def check_core() -> list[str]:
    failures = []
    for path in D0.rglob("*.lean"):
        rel = path.relative_to(D0)
        if not is_core_file(rel):
            continue
        code = read_code(path)
        for token in CORE_FORBIDDEN:
            if re.search(rf"\b{re.escape(token)}\b", code):
                failures.append(f"{rel}: forbidden core token {token!r}")
        if re.search(r"\bset_option\s+autoImplicit\s+true\b", code):
            failures.append(f"{rel}: set_option autoImplicit true is forbidden")
    return failures


def check_bridge() -> list[str]:
    failures = []
    rows, by_name, by_file = load_assumptions()
    for row in rows:
        typ = row.get("assumption_type", "")
        if typ in FORBIDDEN_TYPES or typ not in ALLOWED_TYPES:
            failures.append(f"assumption ledger {row.get('assumption_id')}: bad type {typ!r}")
        if "BridgeAssumption." not in row.get("lean_name", ""):
            failures.append(f"assumption ledger {row.get('assumption_id')}: lean_name must contain BridgeAssumption.*")
        if not row.get("lean_file", "").replace("\\", "/").startswith("D0/Bridge/"):
            failures.append(f"assumption ledger {row.get('assumption_id')}: lean_file must be under D0/Bridge/")

    for path in (D0 / "Bridge").rglob("*.lean"):
        rel = path.relative_to(ROOT).as_posix()
        code = read_code(path)
        if re.search(r"\bset_option\s+autoImplicit\s+true\b", code):
            failures.append(f"{rel}: set_option autoImplicit true is forbidden")
        if re.search(r"\b(axiom|constant|opaque|unsafe|sorry|admit|Float)\b", code):
            failures.append(f"{rel}: forbidden bridge proof shortcut")
        if "structure " in code and "BridgeAssumption" in code:
            ledger_rows = by_file.get(rel, [])
            if not ledger_rows:
                failures.append(f"{rel}: BridgeAssumption structure missing from ledger")
    return failures



def check_all_modules() -> list[str]:
    failures = []
    for path in D0.rglob("*.lean"):
        rel = path.relative_to(D0)
        code = read_code(path)
        for token in CORE_FORBIDDEN:
            if re.search(rf"\b{re.escape(token)}\b", code):
                failures.append(f"{rel}: forbidden all-module token {token!r}")
        if re.search(r"\bset_option\s+autoImplicit\s+true\b", code):
            failures.append(f"{rel}: set_option autoImplicit true is forbidden")
    return failures

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", action="store_true")
    parser.add_argument("--bridge", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--all-modules", action="store_true")
    args = parser.parse_args()

    if not (args.core or args.bridge or args.all or args.all_modules):
        args.all = True

    failures = []
    if args.core or args.all:
        failures.extend(check_core())
    if args.bridge or args.all:
        failures.extend(check_bridge())
    if args.all or args.all_modules:
        failures.extend(check_all_modules())

    if failures:
        print("FAIL")
        for failure in failures:
            print(failure)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
