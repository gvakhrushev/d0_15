#!/usr/bin/env python3
"""Resolve a live task execution before printing a portable dispatch message."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

REPO = "gvakhrushev/d0_15"


def metadata(text: str, name: str) -> list[str]:
    return [m.strip() for m in re.findall(
        rf"^{re.escape(name)}:[ \t]*`?([^`\r\n]+)`?[ \t]*\r?$",
        text, flags=re.MULTILINE | re.IGNORECASE,
    )]


def field(text: str, name: str) -> str:
    values = metadata(text, name)
    if len(values) != 1:
        raise ValueError(f"expected exactly one '{name}: ...' line")
    return values[0]


def open_prs(root: pathlib.Path) -> list[dict]:
    """Fetch every open PR without search-index lag or a fixed result limit."""
    try:
        result = subprocess.run(
            ["gh", "api", "--hostname", "github.com", "--method", "GET",
             "--paginate", "--slurp", f"repos/{REPO}/pulls?state=open&per_page=100"],
            cwd=root, capture_output=True, text=True, check=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        detail = str(exc)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            detail = exc.stderr.strip().splitlines()[0]
        raise ValueError(
            f"GitHub open-PR lookup unavailable: {detail[:200]}. "
            "No launch authorized; --offline only prints unverified brief information."
        ) from exc
    try:
        pages = json.loads(result.stdout)
        if not isinstance(pages, list) or not pages:
            raise ValueError("expected paginated PR arrays")
        prs = []
        for page in pages:
            if not isinstance(page, list):
                raise ValueError("expected a PR array on every page")
            for pr in page:
                if not isinstance(pr, dict) or pr.get("state") != "open":
                    raise ValueError("expected an open PR object")
                if pr.get("body") is not None and not isinstance(pr["body"], str):
                    raise ValueError("expected a PR body string")
                head = pr.get("head")
                if (not isinstance(pr.get("number"), int) or not isinstance(pr.get("html_url"), str)
                        or not pr["html_url"] or not isinstance(pr.get("draft"), bool)
                        or not isinstance(head, dict)
                        or not isinstance(head.get("ref"), str) or not head["ref"]
                        or not isinstance(head.get("sha"), str) or not head["sha"]):
                    raise ValueError("expected complete PR status/head data")
                prs.append(pr)
        return prs
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid GitHub PR response; no launch authorized: {exc}") from exc


def existing_execution(prs: list[dict], task_id: str, branch: str | None) -> tuple[dict | None, str]:
    matches = [pr for pr in prs if task_id in metadata(pr.get("body") or "", "Task")]
    matched_by = "Task metadata"
    if not matches and branch:
        matches = [pr for pr in prs if (pr.get("head") or {}).get("ref") == branch]
        matched_by = "branch fallback; Task metadata missing"
        if any(metadata(pr.get("body") or "", "Task") for pr in matches):
            raise ValueError("queued branch already has an open PR with conflicting Task metadata; no new execution")
    if len(matches) > 1:
        numbers = ", ".join(f"#{pr.get('number', '?')}" for pr in matches)
        raise ValueError(f"ambiguous open execution for {task_id}: {numbers}; no new execution")
    if not matches:
        return None, matched_by
    pr = matches[0]
    if matched_by == "Task metadata" and len(metadata(pr.get("body") or "", "Task")) != 1:
        raise ValueError(f"PR #{pr.get('number', '?')} has ambiguous Task metadata; no new execution")
    return pr, matched_by


def print_execution(pr: dict, matched_by: str) -> None:
    lifecycle = metadata(pr.get("body") or "", "Lifecycle")
    lifecycle = lifecycle[0] if len(lifecycle) == 1 else "UNKNOWN"
    print(f"PR: #{pr['number']} {pr['html_url']}")
    print(f"Status: {'DRAFT' if pr['draft'] else 'READY'}; Lifecycle: {lifecycle}")
    print(f"Head: {pr['head']['ref']} @ {pr['head']['sha']}")
    print(f"Resolved by: {matched_by}")
    if pr["draft"] and lifecycle == "IN_PROGRESS":
        print("Action: Resume this PR at its current head; do not create a new branch or PR.")
    elif pr["draft"] and lifecycle == "BLOCKED":
        print("Action: Resolve the blocker in this PR before resuming; do not create a new execution.")
    elif not pr["draft"] and lifecycle == "REVIEW":
        print("Action: Continue review in this PR; do not launch a new execution or self-merge.")
    else:
        print("Action: Inspect/fix this PR's lifecycle before continuing; do not create a new execution.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_id")
    ap.add_argument("--repo-root", type=pathlib.Path, default=None)
    ap.add_argument("--offline", action="store_true",
                    help="print unverified local brief information; never authorize a new execution")
    args = ap.parse_args(argv)
    root = (args.repo_root or pathlib.Path(__file__).resolve().parents[1]).resolve()

    try:
        manifest = json.loads((root / "00_WORK" / "manifest.json").read_text(encoding="utf-8"))
        tasks = [t for t in manifest.get("tasks", []) if t.get("id") == args.task_id]
        if len(tasks) > 1:
            raise ValueError(f"duplicate local queue entries for {args.task_id}")
        task = tasks[0] if tasks else None
        brief = ""
        if task and (root / task["brief"]).is_file():
            brief = (root / task["brief"]).read_text(encoding="utf-8")
        branches = metadata(brief, "Branch")
        branch = branches[0] if len(branches) == 1 else None

        assembly = None
        if (root / "02_REGISTRY/gr_assembly/contract.json").is_file():
            import gr_assembly
            assembly = gr_assembly.load(root)
            if task:
                gr_assembly.brief_binding(root, task, assembly)
        elif "A4D" in args.task_id:
            raise ValueError("gravity assembly contract missing; use current main before dispatch")

        if not args.offline:
            prs = open_prs(root)
            pr, matched_by = existing_execution(prs, args.task_id, branch)
            if pr:
                print(f"Repository: {REPO}\nTask: {args.task_id}")
                print_execution(pr, matched_by)
                if assembly:
                    print(gr_assembly.context(assembly, args.task_id))
                    actions = gr_assembly.next_actions(assembly, prs)
                    action = next((a for a in actions if a["task"] == args.task_id), None)
                    if action and action["action"] == "resolve-overlap":
                        raise ValueError("conflicting scientific executions: " + "; ".join(action["reasons"]))
                return 0
        if task is None:
            qualifier = " (GitHub status UNVERIFIED in --offline mode)" if args.offline else "; no open execution found"
            raise ValueError(f"{args.task_id} is not in the local queue{qualifier}")

        branch = field(brief, "Branch")
        artifact = field(brief, "Primary artifact")
        print(f"Repository: {REPO}\nTask: {args.task_id}")
        print(f"Class: {task['class']}; Queue state: {task['state']}")
        print(f"Base: {field(brief, 'Base')}")
        print(f"Brief: {task['brief']}\nBranch: {branch}\nPrimary artifact: {artifact}")
        if assembly:
            print(gr_assembly.context(assembly, args.task_id))
        if args.offline:
            print("GitHub status: UNVERIFIED (--offline); no launch authorized.")
            print("Action: Inspect the brief offline; rerun online before starting or resuming execution.")
            return 0
        if task["state"] != "PLANNED":
            raise ValueError(f"queue state is {task['state']} but no open PR exists; reconcile before launching")
        if assembly:
            checked = gr_assembly.launch_check(assembly, args.task_id, prs)
            if not checked["allowed"]:
                raise ValueError("assembly launch gate: " + "; ".join(checked["reasons"]))
        print("Open execution: none (GitHub checked).")
        print("Execute GitHub-first: read the brief, start its lifecycle and open the Draft PR before substantive work.")
        print("Write the durable result in that PR; return only PR + verdict/PASS-FAIL + blocker.")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
