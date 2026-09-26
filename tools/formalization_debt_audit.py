#!/usr/bin/env python3
"""Deterministic formalization debt audit for the D0 Lean library."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT / "03_FORMALIZATION"
SOURCE = FORMALIZATION / "D0"
BASELINE = pathlib.Path(__file__).with_name("formalization_debt_baseline.json")


def mask_lean(text: str) -> str:
    """Blank comments and strings while preserving offsets and line boundaries."""
    out = list(text)
    i = 0
    depth = 0
    state = "code"
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if state == "code":
            if ch == "/" and nxt == "-":
                out[i] = out[i + 1] = " "
                depth = 1
                state = "block"
                i += 2
                continue
            if ch == "-" and nxt == "-":
                out[i] = out[i + 1] = " "
                state = "line"
                i += 2
                continue
            if ch == '"':
                out[i] = " "
                state = "string"
                i += 1
                continue
        elif state == "line":
            if ch == "\n":
                state = "code"
            else:
                out[i] = " "
        elif state == "block":
            if ch == "/" and nxt == "-":
                out[i] = out[i + 1] = " "
                depth += 1
                i += 2
                continue
            if ch == "-" and nxt == "/":
                out[i] = out[i + 1] = " "
                depth -= 1
                i += 2
                if depth == 0:
                    state = "code"
                continue
            if ch != "\n":
                out[i] = " "
        elif state == "string":
            if ch == "\\":
                out[i] = " "
                if i + 1 < len(text):
                    if text[i + 1] != "\n":
                        out[i + 1] = " "
                    i += 2
                    continue
            elif ch == '"':
                out[i] = " "
                state = "code"
            elif ch != "\n":
                out[i] = " "
        i += 1
    return "".join(out)


def finding(path: str, kind: str, line: int, detail: str) -> dict:
    return {"path": path, "kind": kind, "line": line, "detail": detail}


def module_name(path: pathlib.Path) -> str:
    return ".".join(path.relative_to(FORMALIZATION).with_suffix("").parts)


def audit() -> dict:
    files = sorted(list(SOURCE.rglob("*.lean")) + list(FORMALIZATION.glob("*.lean")) )
    findings: List[dict] = []
    modules: Dict[str, dict] = {}
    imports: Dict[str, List[str]] = {}
    line_counts: Dict[str, int] = {}

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        name = module_name(path)
        source = path.read_text(encoding="utf-8")
        code = mask_lean(source)
        lines = source.splitlines()
        line_counts[name] = len(lines)

        for match in re.finditer(r"(?<![\w'])\b(sorry|admit)\b(?![\w'])", code):
            line = code.count("\n", 0, match.start()) + 1
            findings.append(finding(rel, "proof-hole", line, match.group(1)))
        for line_no, line in enumerate(lines, 1):
            for marker in ("TODO", "FIXME"):
                if marker in line:
                    findings.append(finding(rel, marker.lower(), line_no, marker))

        direct_items: List[Tuple[str, int]] = []
        for line_no, line in enumerate(code.splitlines(), 1):
            match = re.match(r"\s*import\s+(.+?)\s*$", line)
            if not match:
                continue
            for imported in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\b", match.group(1)):
                direct_items.append((imported, line_no))
                if imported == name:
                    findings.append(finding(rel, "self-import", line_no, imported))
                if imported == "D0.All" and name not in {"D0.All", "D0"}:
                    findings.append(finding(rel, "umbrella-import", line_no, imported))
        seen = set()
        for imported, line_no in direct_items:
            if imported in seen:
                findings.append(finding(rel, "duplicate-import", line_no, imported))
            seen.add(imported)
        direct = [imported for imported, _ in direct_items]
        imports[name] = direct
        modules[name] = {"path": rel, "loc": len(lines), "imports": direct}

        for match in re.finditer(r"\bset_option\s+maxHeartbeats\s+([0-9]+)", code):
            line = code.count("\n", 0, match.start()) + 1
            findings.append(finding(rel, "heartbeat-override", line, match.group(1)))

    local_names = set(modules)
    graph: Dict[str, List[str]] = {}
    fan_in: Counter = Counter()
    for name, direct in imports.items():
        local = [m for m in direct if m == "D0" or m.startswith("D0.")]
        graph[name] = []
        for imported in local:
            if imported not in local_names:
                findings.append(finding(modules[name]["path"], "missing-local-import", 1, imported))
            else:
                graph[name].append(imported)
                fan_in[imported] += 1

    colors: Dict[str, int] = {}
    stack: List[str] = []
    cycle_keys = set()

    def visit(name: str) -> None:
        colors[name] = 1
        stack.append(name)
        for child in graph.get(name, []):
            if colors.get(child, 0) == 0:
                visit(child)
            elif colors.get(child) == 1:
                at = stack.index(child)
                cycle = stack[at:] + [child]
                key = tuple(cycle)
                if key not in cycle_keys:
                    cycle_keys.add(key)
                    findings.append(finding(modules[name]["path"], "import-cycle", 1, " -> ".join(cycle)))
        stack.pop()
        colors[name] = 2

    for name in sorted(local_names):
        if not colors.get(name):
            visit(name)

    root_module = "D0.All"
    reachable = set()
    pending = [root_module] if root_module in local_names else []
    while pending:
        item = pending.pop()
        if item in reachable:
            continue
        reachable.add(item)
        pending.extend(graph.get(item, []))
    for name in sorted(local_names - reachable):
        # The reachability contract applies to intended library modules, not the
        # top-level compatibility wrapper 03_FORMALIZATION/D0.lean.
        if modules[name]["path"].startswith("03_FORMALIZATION/D0/"):
            findings.append(finding(modules[name]["path"], "unreachable-module", 1, name))

    fan_out = {name: len(set(graph.get(name, []))) for name in modules}
    for name, record in modules.items():
        record["fan_in"] = fan_in[name]
        record["fan_out"] = fan_out[name]

    findings.sort(key=lambda f: (f["path"], f["kind"], f["line"], f["detail"]))
    counts = Counter(f["kind"] for f in findings)
    return {
        "summary": {
            "modules": len(modules),
            "loc": sum(line_counts.values()),
            "findings": len(findings),
            "by_kind": dict(sorted(counts.items())),
        },
        "findings": findings,
        "modules": [modules[name] for name in sorted(modules)],
    }


def key(item: dict) -> Tuple[str, str, str, str]:
    return (item["path"], item["kind"], str(item["line"]), item["detail"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit formalization debt in the local D0 Lean graph.")
    parser.add_argument("--json", action="store_true", help="Print deterministic JSON report.")
    parser.add_argument("--check", action="store_true", help="Reject findings not covered by the path-specific baseline.")
    args = parser.parse_args()
    report = audit()

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        if not args.check:
            return 0
    elif not args.check:
        print("Formalization debt audit")
        print("Lean modules: {modules}; lines: {loc}".format(**report["summary"]))
        print("Findings: {findings}".format(**report["summary"]))
        for kind, count in report["summary"]["by_kind"].items():
            print("  {0}: {1}".format(kind, count))
        for item in report["findings"]:
            print("{path}:{line}: {kind}: {detail}".format(**item))
        return 0

    if not BASELINE.exists():
        print("FAIL: baseline is missing: {0}".format(BASELINE), file=sys.stderr)
        return 1
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    allowed = {(item["path"], item["kind"], str(item["line"]), item["detail"]) for item in baseline.get("entries", [])}
    new = [item for item in report["findings"] if key(item) not in allowed]
    if new:
        print("FAIL: {0} unbaselined formalization debt finding(s)".format(len(new)), file=sys.stderr)
        for item in new[:80]:
            print("{path}:{line}: {kind}: {detail}".format(**item), file=sys.stderr)
        return 1
    print("PASS formalization_debt_non_growth findings={0} baseline={1}".format(
        len(report["findings"]), len(allowed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
