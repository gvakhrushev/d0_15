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
# Generic bridge categories (base-v14).
ALLOWED_TYPES = {
    "CONDENSED_BRIDGE",
    "QFT_RG_BRIDGE",
    "EMPIRICAL_DATA",
    "SMOOTH_LIMIT",
    "MACRO_LIMIT",
    "PHYSICS_DICTIONARY",
    "LIE_ALGEBRA_LIBRARY_GAP",
    # Precise external-owner theorem categories (Iter-18/19/20). Each names a real
    # classical theorem absent from the pinned Mathlib, carried as one explicit
    # BridgeAssumption (never an axiom). The descriptive type is deliberate — it records
    # WHICH external owner, information a 7-bucket whitelist would erase.
    "CARTAN_COMPACTNESS_CRITERION",
    "SUBFACTOR_INDEX_QUANTIZATION",
    "LATTICE_GENUS_THEOREM",
    "NONCOMMUTATIVE_GEOMETRY_THEOREM",
    "VON_NEUMANN_MODULAR_THEOREM",
    "QM_FOUNDATIONS_THEOREM",
    "QM_RECONSTRUCTION_THEOREM",
    "EMERGENT_GRAVITY_PROGRAM",
    "DIVISION_ALGEBRA_CLASSIFICATION",
    "LATTICE_GAUGE_RIGOR",
    "NONCOMMUTATIVE_INTEGRAL_THEOREM",
    "QUANTUM_METRIC_CONVERGENCE",
    "SYMBOLIC_DYNAMICS_CLASSIFICATION",
    "TRANSCENDENCE_THEOREM_LINDEMANN_WEIERSTRASS",
}
# D0-internal named forcing targets (Iter-20 M1-reductio hypotheses). NOT external
# classical theorems: decidable obligations the corpus assumes-but-has-not-derived, living
# in their own domain module (Topology/Spectral/Complexity), not under D0/Bridge/. Exempt
# from the external-wrapper convention but still checked: must be EXPLICIT, reference a real
# internal Lean decl, and never be typed CORE/FOUNDATION.
INTERNAL_TARGET_TYPES = {
    "D0_INTERNAL_FORCING_TARGET",
    "COMPLEXITY_NAVIGATION_POTENTIAL",
    "SPECTRAL_PACKAGING_SYMMETRY",
}
FORBIDDEN_TYPES = {"CORE", "FOUNDATION", "UNSPECIFIED", ""}


def strip_comments(text: str) -> str:
    """Return `text` with every Lean comment and string literal blanked out, so
    that forbidden-token scans only see real code.

    Removes:
      * `--` line comments (to end of line),
      * `/- ... -/` block comments — including the `/-!` and `/--` doc-comment
        variants, which all open with `/-` — and they NEST,
      * `"..."` string literals (their contents).

    Without this, the naive `\\bconstant\\b` scan false-positives on the English
    word "constant" (or "axiom", "sorry", ...) inside a docstring even though it
    is not a Lean keyword. Newlines are preserved and removed regions collapse to
    whitespace so adjacent code tokens stay separated.
    """
    out: list[str] = []
    i, n = 0, len(text)
    depth = 0          # block-comment nesting depth
    in_line = False    # inside a `--` line comment
    in_string = False  # inside a "..." string literal
    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if in_line:
            if c == "\n":
                in_line = False
                out.append(c)
            i += 1
        elif depth > 0:
            if two == "/-":
                depth += 1
                i += 2
            elif two == "-/":
                depth -= 1
                i += 2
                if depth == 0:
                    out.append(" ")
            else:
                if c == "\n":
                    out.append(c)
                i += 1
        elif in_string:
            if c == "\\":
                i += 2  # skip escaped char (e.g. \" or \\)
            elif c == '"':
                in_string = False
                out.append(" ")
                i += 1
            else:
                if c == "\n":
                    out.append(c)
                i += 1
        else:
            if two == "--":
                in_line = True
                i += 2
            elif two == "/-":
                depth = 1
                i += 2
            elif c == '"':
                in_string = True
                i += 1
            else:
                out.append(c)
                i += 1
    return "".join(out)


def read_code(path: Path) -> str:
    return strip_comments(path.read_text(encoding="utf-8"))


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
        aid = row.get("assumption_id")
        typ = row.get("assumption_type", "")
        is_internal = typ in INTERNAL_TARGET_TYPES
        if typ in FORBIDDEN_TYPES or typ not in (ALLOWED_TYPES | INTERNAL_TARGET_TYPES):
            failures.append(f"assumption ledger {aid}: bad type {typ!r}")
        if is_internal:
            # Internal forcing target: lives in its own domain module, not D0/Bridge/.
            if row.get("status", "") != "EXPLICIT":
                failures.append(f"assumption ledger {aid}: internal forcing target must be status EXPLICIT")
            if not row.get("lean_name", "") or not row.get("lean_file", ""):
                failures.append(f"assumption ledger {aid}: internal forcing target must reference a real Lean decl (lean_name+lean_file)")
        else:
            if "BridgeAssumption." not in row.get("lean_name", ""):
                failures.append(f"assumption ledger {aid}: lean_name must contain BridgeAssumption.*")
            if not row.get("lean_file", "").replace("\\", "/").startswith("D0/Bridge/"):
                failures.append(f"assumption ledger {aid}: lean_file must be under D0/Bridge/")

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
