#!/usr/bin/env python3
"""Validate cold-start metadata for executable D0 task briefs and agent protocol."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import tempfile

REPO = "gvakhrushev/d0_15"
EXEC_CLASSES = {"WORKER": "wrk/", "EXPENSIVE": "exp/"}

META_PATTERNS = {
    "Repository": re.compile(r"(?mi)^Repository:\s*`?([^\n`]+)`?\s*$"),
    "Base": re.compile(r"(?mi)^Base:\s*`?([^\n`]+)`?\s*$"),
    "Branch": re.compile(r"(?mi)^Branch:\s*`?([^\n`]+)`?\s*$"),
    "Primary artifact": re.compile(r"(?mi)^Primary artifact:\s*`?([^\n`]+)`?\s*$"),
    "Execution": re.compile(r"(?mi)^Execution:\s*`?([^\n`]+)`?\s*$"),
}

class ProtocolError(Exception):
    pass


def one(pattern: re.Pattern[str], text: str, label: str) -> str:
    hits = [x.strip() for x in pattern.findall(text)]
    if len(hits) != 1:
        raise ProtocolError(f"brief must contain exactly one '{label}: ...' line")
    return hits[0]


def section_body(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        raise ProtocolError(f"brief missing section '{marker}'")
    start += len(marker)
    rest = text[start:]
    nxt = rest.find("\n## ")
    body = rest if nxt < 0 else rest[:nxt]
    body = body.strip()
    if len(body) < 40:
        raise ProtocolError(f"section '{marker}' is too short to be meaningful")
    return body


def validate_brief(task: dict, text: str) -> None:
    tid = task["id"]
    cls = task["class"]

    first = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    if first != f"# {tid}":
        raise ProtocolError(f"{tid}: first heading must be '# {tid}'")

    repo = one(META_PATTERNS["Repository"], text, "Repository")
    base = one(META_PATTERNS["Base"], text, "Base")
    branch = one(META_PATTERNS["Branch"], text, "Branch")
    artifact = one(META_PATTERNS["Primary artifact"], text, "Primary artifact")
    execution = one(META_PATTERNS["Execution"], text, "Execution")

    if repo != REPO:
        raise ProtocolError(f"{tid}: repository must be {REPO}, got {repo}")
    if base != "main":
        raise ProtocolError(f"{tid}: Base must be main, got {base}")
    prefix = EXEC_CLASSES[cls]
    if not branch.startswith(prefix) or branch == prefix:
        raise ProtocolError(f"{tid}: {cls} branch must start with '{prefix}'")
    if artifact in {"", "N/A", "none", "None"}:
        raise ProtocolError(f"{tid}: executable task requires a primary artifact")
    if artifact.startswith(("http://", "https://")):
        raise ProtocolError(f"{tid}: primary artifact must be a repo-relative path")
    if execution.lower() != "github-first":
        raise ProtocolError(f"{tid}: Execution must be GitHub-first")

    section_body(text, "Why delegated")
    section_body(text, "GitHub execution contract")
    section_body(text, "Chat handoff")


def validate(root: pathlib.Path) -> None:
    agents = root / "AGENTS.md"
    if not agents.is_file():
        raise ProtocolError("AGENTS.md is required at repository root")
    at = agents.read_text(encoding="utf-8")
    required_markers = [
        "Repository: `gvakhrushev/d0_15`",
        "KILL-FIRST",
        "classify once, specialize late",
        "python tools/task_dispatch.py TASK-ID",
    ]
    for marker in required_markers:
        if marker not in at:
            raise ProtocolError(f"AGENTS.md missing required marker: {marker}")

    manifest = json.loads((root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
    for task in manifest.get("tasks", []):
        if task.get("class") not in EXEC_CLASSES:
            continue
        brief = root / task["brief"]
        if not brief.is_file():
            raise ProtocolError(f"{task['id']}: brief missing: {task['brief']}")
        validate_brief(task, brief.read_text(encoding="utf-8"))


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "00_WORK" / "tasks").mkdir(parents=True)
        (root / "AGENTS.md").write_text(
            "Repository: `gvakhrushev/d0_15`\nKILL-FIRST\n"
            "classify once, specialize late\npython tools/task_dispatch.py TASK-ID\n",
            encoding="utf-8",
        )
        task = {
            "id": "WRK-TEST-001",
            "class": "WORKER",
            "brief": "00_WORK/tasks/WRK-TEST-001.md",
        }
        manifest = {"tasks": [task]}
        (root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        good = """# WRK-TEST-001
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/test-001`
Primary artifact: `02_REGISTRY/research/certificates/test.py`
Execution: `GitHub-first`

## Why delegated
This is a bounded independently reviewable exact certificate with several hostile controls.

## GitHub execution contract
Open a Draft PR before implementation, write the artifact there, validate, retire, and mark Ready.

## Chat handoff
Return only the PR number, PASS or FAIL, and one exact blocker if the certificate cannot close.
"""
        bp = root / task["brief"]
        bp.write_text(good, encoding="utf-8")
        validate(root)

        bad = good.replace("gvakhrushev/d0_15", "other/repo", 1)
        bp.write_text(bad, encoding="utf-8")
        try:
            validate(root)
        except ProtocolError as exc:
            assert "repository must be" in str(exc)
        else:
            raise AssertionError("wrong repository was not rejected")

        bad = good.replace("Branch: `wrk/test-001`", "Branch: `exp/test-001`")
        bp.write_text(bad, encoding="utf-8")
        try:
            validate(root)
        except ProtocolError as exc:
            assert "branch must start" in str(exc)
        else:
            raise AssertionError("wrong branch prefix was not rejected")

        bad = good.replace(
            "This is a bounded independently reviewable exact certificate with several hostile controls.",
            "small",
        )
        bp.write_text(bad, encoding="utf-8")
        try:
            validate(root)
        except ProtocolError as exc:
            assert "too short" in str(exc)
        else:
            raise AssertionError("empty delegation rationale was not rejected")

    print("PASS agent_protocol self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=pathlib.Path, default=None)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    root = (args.repo_root or pathlib.Path(__file__).resolve().parents[1]).resolve()
    try:
        validate(root)
    except (ProtocolError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL_AGENT_PROTOCOL: {exc}", file=sys.stderr)
        return 1
    print("PASS agent_protocol: cold-start task metadata enforced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
