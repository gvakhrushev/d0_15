#!/usr/bin/env python3
"""render_work_status.py - Deterministic renderer for active work status views.

Inputs (deterministic tracked only):
- 00_WORK/manifest.json
- 02_REGISTRY/claims.csv
- 02_REGISTRY/assumptions.csv
- README.md (for status block replacement)

Outputs:
- 00_WORK/STATUS.md
- README.md (bounded block between <!-- D0-WORK-STATUS:BEGIN --> and <!-- D0-WORK-STATUS:END -->)

Strict discipline:
- No git SHAs, dates, timestamps, hostnames, usernames, branches, or absolute paths.
- Standalone check mode: `--check` exits 1 if tracked views are stale without modifying disk.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
from collections import Counter
from typing import Any, Dict, List, Tuple

CLASSES: List[str] = ["CONTROL", "EXPENSIVE", "WORKER"]
STATES: List[str] = ["PLANNED", "IN_PROGRESS", "BLOCKED", "REVIEW"]
WIP_STATES: set[str] = {"IN_PROGRESS", "BLOCKED", "REVIEW"}

README_BEGIN_MARKER = "<!-- D0-WORK-STATUS:BEGIN -->"
README_END_MARKER = "<!-- D0-WORK-STATUS:END -->"


def load_manifest(manifest_path: pathlib.Path) -> Dict[str, Any]:
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_claims_release_status_counts(claims_path: pathlib.Path) -> List[Tuple[str, int]]:
    counts: Counter[str] = Counter()
    with open(claims_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row.get("release_status", "").strip()
            if status:
                counts[status] += 1
    return sorted(counts.items(), key=lambda item: item[0])


def count_assumptions(assumptions_path: pathlib.Path) -> int:
    with open(assumptions_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return sum(1 for _ in reader)


def render_status_markdown(
    manifest: Dict[str, Any],
    release_status_counts: List[Tuple[str, int]],
    assumptions_count: int,
) -> str:
    limits: Dict[str, int] = manifest.get("limits", {})
    tasks: List[Dict[str, Any]] = manifest.get("tasks", [])
    legacy_scaffolds: List[str] = manifest.get("legacy_scaffolds", [])

    # Metrics aggregation
    counts: Dict[str, Dict[str, int]] = {c: {s: 0 for s in STATES} for c in CLASSES}
    for task in tasks:
        t_class = task.get("class", "")
        t_state = task.get("state", "")
        if t_class in counts and t_state in counts[t_class]:
            counts[t_class][t_state] += 1

    lines: List[str] = [
        "# Work Queue & Control Status",
        "",
        "Runtime execution status lives in GitHub pull requests; the PR number is the execution ID.",
        "",
        "## Repository Task Summary",
        "",
        "| Class | PLANNED | IN_PROGRESS | BLOCKED | REVIEW | Total Tracked | WIP (Active / Limit) |",
        "|---|---|---|---|---|---|---|",
    ]

    total_planned = 0
    total_in_prog = 0
    total_blocked = 0
    total_review = 0
    total_active = 0
    total_wip = 0
    total_limit = 0

    for c in CLASSES:
        pl = counts[c]["PLANNED"]
        ip = counts[c]["IN_PROGRESS"]
        bl = counts[c]["BLOCKED"]
        rv = counts[c]["REVIEW"]
        tot = pl + ip + bl + rv
        wip = ip + bl + rv
        lim = limits.get(c, 0)

        total_planned += pl
        total_in_prog += ip
        total_blocked += bl
        total_review += rv
        total_active += tot
        total_wip += wip
        total_limit += lim

        lines.append(f"| {c} | {pl} | {ip} | {bl} | {rv} | {tot} | {wip} / {lim} |")

    lines.append(
        f"| **Total** | **{total_planned}** | **{total_in_prog}** | **{total_blocked}** | "
        f"**{total_review}** | **{total_active}** | **{total_wip} / {total_limit}** |"
    )
    lines.append("")

    lines.append("## Repository Queue / Control Tasks")
    lines.append("")
    lines.append("| ID | Class | State | Parent | Affected Claims |")
    lines.append("|---|---|---|---|---|")

    if not tasks:
        lines.append("| *(none)* | - | - | - | - |")
    else:
        for task in tasks:
            tid = task.get("id", "")
            t_class = task.get("class", "")
            t_state = task.get("state", "")
            t_parent = task.get("parent", "")
            aff = task.get("affected_claims", [])
            aff_str = ", ".join(aff) if aff else "-"
            lines.append(f"| {tid} | {t_class} | {t_state} | {t_parent} | {aff_str} |")

    lines.append("")
    lines.append("## Registry Health & Metrics")
    lines.append("")
    lines.append(f"- **Assumptions**: {assumptions_count}")
    lines.append(f"- **Legacy Scaffolds Remaining**: {len(legacy_scaffolds)}")
    lines.append("")
    lines.append("### Claims by Exact `release_status`")
    lines.append("")
    lines.append("| Exact `release_status` | Count |")
    lines.append("|---|---|")

    total_claims = 0
    for st, cnt in release_status_counts:
        total_claims += cnt
        lines.append(f"| {st} | {cnt} |")
    lines.append(f"| **Total** | **{total_claims}** |")
    lines.append("")

    return "\n".join(lines)


def render_readme_block(manifest: Dict[str, Any]) -> str:
    limits: Dict[str, int] = manifest.get("limits", {})
    tasks: List[Dict[str, Any]] = manifest.get("tasks", [])
    legacy_scaffolds: List[str] = manifest.get("legacy_scaffolds", [])

    class_counts: Dict[str, int] = {c: 0 for c in CLASSES}
    wip_counts: Dict[str, int] = {c: 0 for c in CLASSES}

    for task in tasks:
        c = task.get("class", "")
        s = task.get("state", "")
        if c in class_counts:
            class_counts[c] += 1
            if s in WIP_STATES:
                wip_counts[c] += 1

    ctrl_cnt = class_counts["CONTROL"]
    exp_cnt = class_counts["EXPENSIVE"]
    wrk_cnt = class_counts["WORKER"]
    tot_active = ctrl_cnt + exp_cnt + wrk_cnt

    ctrl_wip = f"{wip_counts['CONTROL']}/{limits.get('CONTROL', 0)}"
    exp_wip = f"{wip_counts['EXPENSIVE']}/{limits.get('EXPENSIVE', 0)}"
    wrk_wip = f"{wip_counts['WORKER']}/{limits.get('WORKER', 0)}"

    lines = [
        README_BEGIN_MARKER,
        "### Work Queue & Control Plane",
        "",
        f"- **Tracked Queue/Control Tasks**: CONTROL: {ctrl_cnt}, EXPENSIVE: {exp_cnt}, WORKER: {wrk_cnt} (Total: {tot_active})",
        "- **Runtime Execution**: see open GitHub pull requests; PR number = execution ID",
        f"- **WIP Utilization**: CONTROL: {ctrl_wip}, EXPENSIVE: {exp_wip}, WORKER: {wrk_wip}",
        f"- **Legacy Scaffolds Remaining**: {len(legacy_scaffolds)}",
        "- **Detailed Status Report**: [00_WORK/STATUS.md](00_WORK/STATUS.md)",
        README_END_MARKER,
    ]
    return "\n".join(lines)


def update_readme_content(original_readme: str, new_block: str) -> str:
    if README_BEGIN_MARKER in original_readme and README_END_MARKER in original_readme:
        prefix, rest = original_readme.split(README_BEGIN_MARKER, 1)
        _, suffix = rest.split(README_END_MARKER, 1)
        return prefix + new_block + suffix
    else:
        # Insert before "## Citation & Status" if present, or at the end
        target_heading = "## Citation & Status"
        if target_heading in original_readme:
            parts = original_readme.split(target_heading, 1)
            return parts[0] + target_heading + "\n\n" + new_block + "\n\n" + parts[1].lstrip("\n")
        else:
            return original_readme.rstrip() + "\n\n" + new_block + "\n"


def generate_views(
    root: pathlib.Path,
) -> Tuple[str, str, pathlib.Path, pathlib.Path]:
    manifest_path = root / "00_WORK" / "manifest.json"
    claims_path = root / "02_REGISTRY" / "claims.csv"
    assumptions_path = root / "02_REGISTRY" / "assumptions.csv"
    status_md_path = root / "00_WORK" / "STATUS.md"
    readme_path = root / "README.md"

    manifest = load_manifest(manifest_path)
    release_counts = load_claims_release_status_counts(claims_path)
    assumptions_cnt = count_assumptions(assumptions_path)

    expected_status_content = render_status_markdown(manifest, release_counts, assumptions_cnt)

    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    readme_block = render_readme_block(manifest)
    expected_readme_content = update_readme_content(readme_text, readme_block)

    return expected_status_content, expected_readme_content, status_md_path, readme_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render deterministic active work status views.")
    parser.add_argument("--repo-root", type=pathlib.Path, default=None, help="Root path of repository")
    parser.add_argument("--check", action="store_true", help="Check that tracked views match rendered output")
    args = parser.parse_args(argv)

    root = (args.repo_root or pathlib.Path(__file__).resolve().parents[1]).resolve()

    expected_status, expected_readme, status_path, readme_path = generate_views(root)

    if args.check:
        stale = False
        if not status_path.exists():
            print(f"STALE: {status_path} does not exist", file=sys.stderr)
            stale = True
        else:
            current_status = status_path.read_text(encoding="utf-8")
            if current_status != expected_status:
                print(f"STALE: {status_path} is out of date", file=sys.stderr)
                stale = True

        if not readme_path.exists():
            print(f"STALE: {readme_path} does not exist", file=sys.stderr)
            stale = True
        else:
            current_readme = readme_path.read_text(encoding="utf-8")
            if current_readme != expected_readme:
                print(f"STALE: {readme_path} active work status block is out of date", file=sys.stderr)
                stale = True

        if stale:
            print("Run 'python tools/render_work_status.py' to update views.", file=sys.stderr)
            return 1
        print("PASS work_views stale=0")
        return 0

    # Regenerate mode
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(expected_status, encoding="utf-8")
    readme_path.write_text(expected_readme, encoding="utf-8")
    print(f"Rendered {status_path} and updated {readme_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
