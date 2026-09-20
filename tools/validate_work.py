#!/usr/bin/env python3
"""validate_work.py - Validator for active work control plane (d0-work/1).

Enforces:
1. manifest.json parseable.
2. schema == "d0-work/1".
3. Unique task IDs.
4. Valid class and state.
5. Parent rules:
   - CONTROL can have parent ROOT or another CONTROL.
   - EXPENSIVE must have an immediate parent of class CONTROL.
   - WORKER must have an immediate parent of class CONTROL.
   - EXPENSIVE cannot directly parent WORKER.
   - Each task has exactly one parent.
   - Acyclic parent graph.
6. No cycles.
7. No orphan parents.
8. WIP limits enforced on (IN_PROGRESS, BLOCKED, REVIEW).
9. affected_claim rules:
   - Non-empty for EXPENSIVE and WORKER.
   - Every claim must exist in claims.csv or aliases.csv.
   - No 'NEW:...' or unminted IDs allowed.
10. Non-empty exit_condition.
11. Reject placeholder exit conditions ('tbd', 'todo', 'needs work', 'figure out', 'later').
12. brief path starts with '00_WORK/tasks/' and file exists.
13. Exact 00_WORK tree enforcement:
   - Only manifest.json, README.md, STATUS.md, and owned task briefs under 00_WORK/tasks/.
   - No unowned, stray, or nested files permitted anywhere under 00_WORK/.
14. Forbidden completed states rejected (DONE, COMPLETED, CLOSED, ABANDONED, etc.).
15. Frontier Markdown freeze:
   - No regex security boundary: strict whitelist baseline 'legacy_frontier_markdown_paths'.
   - Any new tracked/present .md under 02_REGISTRY/frontier/ is strictly forbidden.
   - Deletion/reduction of legacy baseline files is explicitly permitted.
16. Generated 00_WORK/STATUS.md and README generated block match renderer output.

Self-test (--self-test):
Proves reachability of all mandatory failure modes and permissions using in-memory/temp fixtures.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Set

from render_work_status import generate_views

ALLOWED_CLASSES: Set[str] = {"CONTROL", "EXPENSIVE", "WORKER"}
ALLOWED_STATES: Set[str] = {"PLANNED", "IN_PROGRESS", "BLOCKED", "REVIEW"}
WIP_STATES: Set[str] = {"IN_PROGRESS", "BLOCKED", "REVIEW"}
FORBIDDEN_COMPLETED_STATES: Set[str] = {"DONE", "COMPLETED", "CLOSED", "ABANDONED", "RESOLVED", "FINISHED"}

FORBIDDEN_EXIT_PHRASES: List[str] = ["tbd", "todo", "needs work", "figure out", "later"]

ALLOWED_00_WORK_ROOT_FILES: Set[str] = {"manifest.json", "README.md", "STATUS.md"}


class WorkValidationError(Exception):
    pass


def load_valid_claim_ids(registry_dir: pathlib.Path) -> Set[str]:
    claims_path = registry_dir / "claims.csv"
    aliases_path = registry_dir / "aliases.csv"

    valid_ids: Set[str] = set()

    if claims_path.exists():
        with open(claims_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = row.get("claim_id", "").strip()
                if cid:
                    valid_ids.add(cid)

    if aliases_path.exists():
        with open(aliases_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                legacy = row.get("legacy_id", "").strip()
                if legacy:
                    valid_ids.add(legacy)

    return valid_ids


def get_all_md_files(root: pathlib.Path) -> List[pathlib.Path]:
    try:
        res = subprocess.run(
            ["git", "ls-files", "*.md"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        tracked = [root / line.strip() for line in res.stdout.splitlines() if line.strip()]
        # Also include any actual markdown files under 02_REGISTRY/frontier or 00_WORK that might be untracked
        for sub in ["00_WORK", "02_REGISTRY/frontier"]:
            sub_dir = root / sub
            if sub_dir.exists():
                for p in sub_dir.rglob("*.md"):
                    if p not in tracked:
                        tracked.append(p)
        return tracked
    except Exception:
        # Fallback for non-git environments / temp directories
        mds = []
        for p in root.rglob("*.md"):
            rel_parts = p.relative_to(root).parts
            if any(part.startswith(".") for part in rel_parts):
                continue
            mds.append(p)
        return mds


def validate_work(root: pathlib.Path) -> None:
    manifest_path = root / "00_WORK" / "manifest.json"
    if not manifest_path.exists():
        raise WorkValidationError(f"Missing manifest file: {manifest_path}")

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        raise WorkValidationError(f"manifest.json is not valid JSON: {e}")

    # 1. Schema check
    schema = manifest.get("schema")
    if schema != "d0-work/1":
        raise WorkValidationError(f"Unsupported or missing schema '{schema}', expected 'd0-work/1'")

    limits: Dict[str, int] = manifest.get("limits", {})
    legacy_scaffolds: List[str] = manifest.get("legacy_scaffolds", [])
    legacy_frontier_mds: List[str] = manifest.get("legacy_frontier_markdown_paths", [])
    tasks: List[Dict[str, Any]] = manifest.get("tasks", [])

    # Validate limits definition
    for c in ALLOWED_CLASSES:
        if c not in limits or not isinstance(limits[c], int) or limits[c] < 0:
            raise WorkValidationError(f"manifest limits must specify non-negative integer for class '{c}'")

    valid_claim_ids = load_valid_claim_ids(root / "02_REGISTRY")

    # 2. Unique task IDs & task structure
    task_map: Dict[str, Dict[str, Any]] = {}
    brief_map: Dict[str, str] = {}  # brief_path -> task_id

    for idx, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise WorkValidationError(f"Task at index {idx} is not an object")

        tid = task.get("id")
        if not tid or not isinstance(tid, str) or not tid.strip():
            raise WorkValidationError(f"Task at index {idx} has missing or empty id")
        tid = tid.strip()

        if tid in task_map:
            raise WorkValidationError(f"Duplicate task id '{tid}'")
        task_map[tid] = task

        t_class = task.get("class")
        if t_class not in ALLOWED_CLASSES:
            raise WorkValidationError(f"Task '{tid}' has invalid class '{t_class}', allowed: {sorted(ALLOWED_CLASSES)}")

        t_state = task.get("state")
        if t_state in FORBIDDEN_COMPLETED_STATES:
            raise WorkValidationError(f"Task '{tid}' has forbidden completed state '{t_state}'")
        if t_state not in ALLOWED_STATES:
            raise WorkValidationError(f"Task '{tid}' has invalid state '{t_state}', allowed: {sorted(ALLOWED_STATES)}")

        # exit_condition check
        exit_cond = task.get("exit_condition")
        if not exit_cond or not isinstance(exit_cond, str) or not exit_cond.strip():
            raise WorkValidationError(f"Task '{tid}' has empty exit_condition")
        exit_cond_str = exit_cond.strip()

        for forbidden in FORBIDDEN_EXIT_PHRASES:
            if forbidden in exit_cond_str.lower():
                raise WorkValidationError(
                    f"Task '{tid}' exit_condition contains forbidden placeholder phrase '{forbidden}'"
                )

        # affected_claims check
        aff_claims = task.get("affected_claims")
        if not isinstance(aff_claims, list):
            raise WorkValidationError(f"Task '{tid}' affected_claims must be a list")

        if t_class in ("EXPENSIVE", "WORKER"):
            if len(aff_claims) == 0:
                raise WorkValidationError(f"Task '{tid}' of class '{t_class}' must have non-empty affected_claims")

        for cid in aff_claims:
            if not isinstance(cid, str):
                raise WorkValidationError(f"Task '{tid}' affected_claims contains non-string entry")
            cid_clean = cid.strip()
            if cid_clean.upper().startswith("NEW:"):
                raise WorkValidationError(f"Task '{tid}' contains forbidden unminted claim ID '{cid_clean}'")
            if cid_clean not in valid_claim_ids:
                raise WorkValidationError(f"Task '{tid}' references nonexistent claim ID '{cid_clean}'")

        # brief check
        brief = task.get("brief")
        if brief is not None:
            if not isinstance(brief, str) or not brief.strip():
                raise WorkValidationError(f"Task '{tid}' has invalid brief path '{brief}'")
            brief_clean = brief.strip()
            brief_path_obj = pathlib.Path(brief_clean)
            if brief_path_obj.parent != pathlib.Path("00_WORK/tasks"):
                raise WorkValidationError(
                    f"Task '{tid}' brief '{brief_clean}' must be located directly under '00_WORK/tasks/'"
                )
            if not brief_clean.endswith(".md"):
                raise WorkValidationError(f"Task '{tid}' brief '{brief_clean}' must be a .md file")
            if ".." in brief_path_obj.parts:
                raise WorkValidationError(f"Task '{tid}' brief '{brief_clean}' cannot contain '..'")
            brief_file = root / brief_clean
            if not brief_file.is_file():
                raise WorkValidationError(f"Task '{tid}' brief file does not exist: {brief_clean}")

            if brief_clean in brief_map:
                raise WorkValidationError(
                    f"Brief '{brief_clean}' assigned to multiple tasks: '{brief_map[brief_clean]}' and '{tid}'"
                )
            brief_map[brief_clean] = tid

    # 3. Parent rules & acyclicity
    for tid, task in task_map.items():
        parent = task.get("parent")
        if not parent or not isinstance(parent, str) or not parent.strip():
            raise WorkValidationError(f"Task '{tid}' has missing or empty parent")
        parent = parent.strip()

        t_class = task["class"]
        if parent == "ROOT":
            if t_class != "CONTROL":
                raise WorkValidationError(f"Task '{tid}' of class '{t_class}' cannot have parent 'ROOT'")
        else:
            if parent not in task_map:
                raise WorkValidationError(f"Task '{tid}' has orphan parent '{parent}'")
            parent_task = task_map[parent]
            parent_class = parent_task["class"]

            if t_class in ("EXPENSIVE", "WORKER"):
                if parent_class != "CONTROL":
                    raise WorkValidationError(
                        f"Task '{tid}' of class '{t_class}' must have parent of class 'CONTROL', got '{parent_class}' (parent='{parent}')"
                    )
            elif t_class == "CONTROL":
                if parent_class != "CONTROL":
                    raise WorkValidationError(
                        f"Task '{tid}' of class 'CONTROL' cannot have parent of class '{parent_class}' (parent='{parent}')"
                    )

        # Cycle check via path traversal
        visited = {tid}
        curr = parent
        while curr != "ROOT":
            if curr in visited:
                raise WorkValidationError(f"Cycle detected in task parent hierarchy involving '{tid}' and '{curr}'")
            visited.add(curr)
            if curr not in task_map:
                break
            curr = task_map[curr].get("parent", "")

    # 4. WIP limits enforcement
    wip_counts: Dict[str, int] = {c: 0 for c in ALLOWED_CLASSES}
    for tid, task in task_map.items():
        if task["state"] in WIP_STATES:
            wip_counts[task["class"]] += 1

    for c, count in wip_counts.items():
        lim = limits.get(c, 0)
        if count > lim:
            raise WorkValidationError(
                f"WIP limit exceeded for class '{c}': {count} active tasks in WIP states, limit is {lim}"
            )

    # 5. Exact 00_WORK tree enforcement (R3)
    work_dir = root / "00_WORK"
    if work_dir.exists():
        for p in work_dir.rglob("*"):
            if not p.is_file():
                continue
            rel_work = p.relative_to(work_dir)
            parts = rel_work.parts

            if len(parts) == 1:
                # Top-level file directly in 00_WORK/
                filename = parts[0]
                if filename not in ALLOWED_00_WORK_ROOT_FILES:
                    raise WorkValidationError(
                        f"Stray file directly under 00_WORK/ is forbidden: '00_WORK/{filename}'"
                    )
            elif len(parts) == 2 and parts[0] == "tasks":
                # File in 00_WORK/tasks/
                rel_posix = f"00_WORK/tasks/{parts[1]}"
                if not parts[1].endswith(".md"):
                    raise WorkValidationError(
                        f"Non-markdown file under 00_WORK/tasks/ is forbidden: '{rel_posix}'"
                    )
                if rel_posix not in brief_map:
                    raise WorkValidationError(
                        f"Unowned brief file in 00_WORK/tasks/ is forbidden: '{rel_posix}'"
                    )
            else:
                # Nested directory or invalid structure under 00_WORK/
                rel_posix = f"00_WORK/{rel_work.as_posix()}"
                raise WorkValidationError(
                    f"Nested unowned file under 00_WORK/ is forbidden: '{rel_posix}'"
                )

    # 6. Frontier Markdown freeze (R2) - No filename regex; strict baseline whitelist
    frontier_baseline_set = set(legacy_frontier_mds)
    frontier_dir = root / "02_REGISTRY" / "frontier"

    # Check all existing / tracked markdown files under 02_REGISTRY/frontier/
    if frontier_dir.exists():
        for p in frontier_dir.rglob("*.md"):
            if not p.is_file():
                continue
            rel_posix = p.relative_to(root).as_posix()
            if rel_posix not in frontier_baseline_set:
                raise WorkValidationError(
                    f"New Markdown file under 02_REGISTRY/frontier/ is forbidden: '{rel_posix}' "
                    f"(not in legacy_frontier_markdown_paths baseline)"
                )

    # Also check git tracked files to catch tracked files even if temporarily absent
    all_md_files = get_all_md_files(root)
    for p in all_md_files:
        rel_posix = p.relative_to(root).as_posix()
        if rel_posix.startswith("02_REGISTRY/frontier/"):
            if rel_posix not in frontier_baseline_set:
                raise WorkValidationError(
                    f"New tracked Markdown file under 02_REGISTRY/frontier/ is forbidden: '{rel_posix}'"
                )

    # 7. Check that generated STATUS.md and README block match renderer
    expected_status, expected_readme, status_path, readme_path = generate_views(root)

    if not status_path.exists():
        raise WorkValidationError(f"Generated status file does not exist: {status_path.relative_to(root)}")
    current_status = status_path.read_text(encoding="utf-8")
    if current_status != expected_status:
        raise WorkValidationError(
            f"Generated status view is stale: {status_path.relative_to(root)} does not match renderer output"
        )

    if not readme_path.exists():
        raise WorkValidationError(f"README file does not exist: {readme_path.relative_to(root)}")
    current_readme = readme_path.read_text(encoding="utf-8")
    if current_readme != expected_readme:
        raise WorkValidationError(
            f"README active work status block is stale: does not match renderer output"
        )


def run_self_tests() -> int:
    """Execute in-memory/temp fixtures proving reachability of all mandatory failure modes."""
    print("=== validate_work --self-test ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_root = pathlib.Path(tmpdir)

        def setup_base_fixture() -> None:
            # Clean directory
            for item in tmp_root.iterdir():
                if item.is_dir():
                    import shutil
                    shutil.rmtree(item)
                else:
                    item.unlink()

            (tmp_root / "00_WORK" / "tasks").mkdir(parents=True, exist_ok=True)
            (tmp_root / "02_REGISTRY" / "frontier").mkdir(parents=True, exist_ok=True)

            # Minimal claims.csv
            claims_csv = (
                "claim_id,book,section,lean_module,lean_theorem,lean_status,uses_bridge_assumptions,assumption_ids,python_cert,release_status,notes\n"
                "D0-TEST-CLAIM-001,BOOK_01,01.1,D0.Test,test_thm,LEAN_PROVED,False,,,CORE-FORMALIZED,\n"
            )
            (tmp_root / "02_REGISTRY" / "claims.csv").write_text(claims_csv, encoding="utf-8")

            # Minimal assumptions.csv
            assumptions_csv = "assumption_id,lean_file,claim_id,status\n"
            (tmp_root / "02_REGISTRY" / "assumptions.csv").write_text(assumptions_csv, encoding="utf-8")

            # Minimal aliases.csv
            aliases_csv = "legacy_id,kind,canonical_claim_id,first_reference,note\n"
            (tmp_root / "02_REGISTRY" / "aliases.csv").write_text(aliases_csv, encoding="utf-8")

            # Baseline frontier markdown file
            baseline_md_rel = "02_REGISTRY/frontier/BASELINE_DOC.md"
            (tmp_root / baseline_md_rel).write_text("# Baseline Doc", encoding="utf-8")

            # Task brief
            (tmp_root / "00_WORK" / "tasks" / "CTRL-BASE.md").write_text("# CTRL-BASE", encoding="utf-8")

            # Base manifest
            base_manifest = {
                "schema": "d0-work/1",
                "limits": {"EXPENSIVE": 3, "WORKER": 5, "CONTROL": 2},
                "legacy_scaffolds": ["02_REGISTRY/frontier/BASELINE_DOC.md"],
                "legacy_frontier_markdown_paths": [baseline_md_rel],
                "tasks": [
                    {
                        "id": "CTRL-BASE",
                        "class": "CONTROL",
                        "parent": "ROOT",
                        "state": "PLANNED",
                        "affected_claims": [],
                        "exit_condition": "Valid base acceptance condition.",
                        "brief": "00_WORK/tasks/CTRL-BASE.md",
                    }
                ],
            }
            (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(base_manifest, indent=2), encoding="utf-8")

            # Base README
            readme_text = "# Test Repo\n\n## Citation & Status\n"
            (tmp_root / "README.md").write_text(readme_text, encoding="utf-8")

            # Render status
            from render_work_status import generate_views
            exp_status, exp_readme, status_path, readme_path = generate_views(tmp_root)
            status_path.write_text(exp_status, encoding="utf-8")
            readme_path.write_text(exp_readme, encoding="utf-8")

        # 1. Orphan parent
        setup_base_fixture()
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"][0]["parent"] = "CTRL-NONEXISTENT"
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "orphan_parent test failed to raise"
        except WorkValidationError as e:
            assert "orphan parent" in str(e).lower()
        print("PASS_SELF_TEST: orphan parent rejected")

        # 2. Cycle
        setup_base_fixture()
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"].append(
            {
                "id": "CTRL-CYCLE-2",
                "class": "CONTROL",
                "parent": "CTRL-BASE",
                "state": "PLANNED",
                "affected_claims": [],
                "exit_condition": "Cycle step.",
                "brief": "00_WORK/tasks/CTRL-CYCLE-2.md",
            }
        )
        (tmp_root / "00_WORK" / "tasks" / "CTRL-CYCLE-2.md").write_text("# Cycle 2", encoding="utf-8")
        manifest_data["tasks"][0]["parent"] = "CTRL-CYCLE-2"
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "cycle test failed to raise"
        except WorkValidationError as e:
            assert "cycle detected" in str(e).lower()
        print("PASS_SELF_TEST: cycle rejected")

        # 3. EXPENSIVE parented by WORKER
        setup_base_fixture()
        (tmp_root / "00_WORK" / "tasks" / "WRK-1.md").write_text("# WRK-1", encoding="utf-8")
        (tmp_root / "00_WORK" / "tasks" / "EXP-1.md").write_text("# EXP-1", encoding="utf-8")
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"].append(
            {
                "id": "WRK-1",
                "class": "WORKER",
                "parent": "CTRL-BASE",
                "state": "PLANNED",
                "affected_claims": ["D0-TEST-CLAIM-001"],
                "exit_condition": "Worker step.",
                "brief": "00_WORK/tasks/WRK-1.md",
            }
        )
        manifest_data["tasks"].append(
            {
                "id": "EXP-1",
                "class": "EXPENSIVE",
                "parent": "WRK-1",
                "state": "PLANNED",
                "affected_claims": ["D0-TEST-CLAIM-001"],
                "exit_condition": "Expensive step.",
                "brief": "00_WORK/tasks/EXP-1.md",
            }
        )
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "EXPENSIVE parented by WORKER failed to raise"
        except WorkValidationError as e:
            assert "must have parent of class 'control'" in str(e).lower()
        print("PASS_SELF_TEST: EXPENSIVE parented by WORKER rejected")

        # 4. WORKER parented by EXPENSIVE
        setup_base_fixture()
        (tmp_root / "00_WORK" / "tasks" / "EXP-2.md").write_text("# EXP-2", encoding="utf-8")
        (tmp_root / "00_WORK" / "tasks" / "WRK-2.md").write_text("# WRK-2", encoding="utf-8")
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"].append(
            {
                "id": "EXP-2",
                "class": "EXPENSIVE",
                "parent": "CTRL-BASE",
                "state": "PLANNED",
                "affected_claims": ["D0-TEST-CLAIM-001"],
                "exit_condition": "Expensive step.",
                "brief": "00_WORK/tasks/EXP-2.md",
            }
        )
        manifest_data["tasks"].append(
            {
                "id": "WRK-2",
                "class": "WORKER",
                "parent": "EXP-2",
                "state": "PLANNED",
                "affected_claims": ["D0-TEST-CLAIM-001"],
                "exit_condition": "Worker step.",
                "brief": "00_WORK/tasks/WRK-2.md",
            }
        )
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "WORKER parented by EXPENSIVE failed to raise"
        except WorkValidationError as e:
            assert "must have parent of class 'control'" in str(e).lower()
        print("PASS_SELF_TEST: WORKER parented by EXPENSIVE rejected")

        # 5. Nonexistent affected claim
        setup_base_fixture()
        (tmp_root / "00_WORK" / "tasks" / "WRK-3.md").write_text("# WRK-3", encoding="utf-8")
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"].append(
            {
                "id": "WRK-3",
                "class": "WORKER",
                "parent": "CTRL-BASE",
                "state": "PLANNED",
                "affected_claims": ["D0-NONEXISTENT-999"],
                "exit_condition": "Worker step.",
                "brief": "00_WORK/tasks/WRK-3.md",
            }
        )
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "nonexistent affected claim failed to raise"
        except WorkValidationError as e:
            assert "references nonexistent claim id" in str(e).lower()
        print("PASS_SELF_TEST: nonexistent affected claim rejected")

        # 6. NEW:D0-* claim minting rejected
        setup_base_fixture()
        (tmp_root / "00_WORK" / "tasks" / "WRK-4.md").write_text("# WRK-4", encoding="utf-8")
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"].append(
            {
                "id": "WRK-4",
                "class": "WORKER",
                "parent": "CTRL-BASE",
                "state": "PLANNED",
                "affected_claims": ["NEW:D0-UNMINTED-001"],
                "exit_condition": "Worker step.",
                "brief": "00_WORK/tasks/WRK-4.md",
            }
        )
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "NEW:D0-* claim minting failed to raise"
        except WorkValidationError as e:
            assert "forbidden unminted claim id" in str(e).lower()
        print("PASS_SELF_TEST: NEW:D0-* rejected")

        # 7. Completed state rejected
        setup_base_fixture()
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["tasks"][0]["state"] = "DONE"
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "completed state failed to raise"
        except WorkValidationError as e:
            assert "forbidden completed state" in str(e).lower()
        print("PASS_SELF_TEST: completed state rejected")

        # 8. WIP overflow rejected
        setup_base_fixture()
        manifest_data = json.loads((tmp_root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        manifest_data["limits"]["CONTROL"] = 1
        manifest_data["tasks"][0]["state"] = "IN_PROGRESS"
        (tmp_root / "00_WORK" / "tasks" / "CTRL-EXTRA.md").write_text("# EXTRA", encoding="utf-8")
        manifest_data["tasks"].append(
            {
                "id": "CTRL-EXTRA",
                "class": "CONTROL",
                "parent": "ROOT",
                "state": "REVIEW",
                "affected_claims": [],
                "exit_condition": "Second active task.",
                "brief": "00_WORK/tasks/CTRL-EXTRA.md",
            }
        )
        (tmp_root / "00_WORK" / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "WIP overflow failed to raise"
        except WorkValidationError as e:
            assert "wip limit exceeded" in str(e).lower()
        print("PASS_SELF_TEST: WIP overflow rejected")

        # 9. Orphan brief rejected (under 00_WORK/tasks/)
        setup_base_fixture()
        (tmp_root / "00_WORK" / "tasks" / "unowned.md").write_text("# Unowned Brief", encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "unowned brief under tasks failed to raise"
        except WorkValidationError as e:
            assert "unowned brief file in 00_work/tasks/ is forbidden" in str(e).lower()
        print("PASS_SELF_TEST: unowned task brief rejected (00_WORK/tasks/unowned.md)")

        # 10. Stray file directly under 00_WORK/ rejected (R3)
        setup_base_fixture()
        (tmp_root / "00_WORK" / "OLD_RESULT.md").write_text("# Stray", encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "stray file directly under 00_WORK failed to raise"
        except WorkValidationError as e:
            assert "stray file directly under 00_work/ is forbidden" in str(e).lower()
        print("PASS_SELF_TEST: stray file directly under 00_WORK rejected (00_WORK/OLD_RESULT.md)")

        # 11. Nested unowned file under 00_WORK/ rejected (R3)
        setup_base_fixture()
        (tmp_root / "00_WORK" / "sub").mkdir(parents=True, exist_ok=True)
        (tmp_root / "00_WORK" / "sub" / "nested.txt").write_text("nested", encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "nested file under 00_WORK failed to raise"
        except WorkValidationError as e:
            assert "nested unowned file under 00_work/ is forbidden" in str(e).lower()
        print("PASS_SELF_TEST: nested unowned file under 00_WORK rejected")

        # 12. New frontier markdown with random name rejected (R2)
        setup_base_fixture()
        (tmp_root / "02_REGISTRY" / "frontier" / "RANDOM_NAME.md").write_text("# Random", encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "random frontier markdown failed to raise"
        except WorkValidationError as e:
            assert "new markdown file under 02_registry/frontier/ is forbidden" in str(e).lower()
        print("PASS_SELF_TEST: arbitrary new markdown under 02_REGISTRY/frontier/ rejected (RANDOM_NAME.md)")

        # 13. Removal of legacy scaffold permitted without failure (R2)
        setup_base_fixture()
        # Delete BASELINE_DOC.md from disk
        (tmp_root / "02_REGISTRY" / "frontier" / "BASELINE_DOC.md").unlink()
        try:
            validate_work(tmp_root)
        except WorkValidationError as e:
            assert False, f"removal of baseline scaffold raised unexpectedly: {e}"
        print("PASS_SELF_TEST: removal of baseline legacy scaffold permitted")

        # 14. Stale generated view rejected
        setup_base_fixture()
        (tmp_root / "00_WORK" / "STATUS.md").write_text("# STALE CONTENT\n", encoding="utf-8")
        try:
            validate_work(tmp_root)
            assert False, "stale generated view failed to raise"
        except WorkValidationError as e:
            assert "generated status view is stale" in str(e).lower()
        print("PASS_SELF_TEST: stale generated view rejected")

    print("PASS_SELF_TEST: all mandatory failure modes and permissions verified.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate active work control plane.")
    parser.add_argument("--repo-root", type=pathlib.Path, default=None, help="Root path of repository")
    parser.add_argument("--self-test", action="store_true", help="Run self-tests on temporary fixtures")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_tests()

    root = (args.repo_root or pathlib.Path(__file__).resolve().parents[1]).resolve()

    try:
        validate_work(root)
    except WorkValidationError as e:
        print(f"FAIL_WORK_VALIDATION: {e}", file=sys.stderr)
        return 1

    print("PASS work_validation: active work plane clean and enforced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
