#!/usr/bin/env python3
"""Resolve a live task execution before printing a portable dispatch message."""
from __future__ import annotations

import argparse
import json
import pathlib
import posixpath
import re
import subprocess
import sys

REPO = "gvakhrushev/d0_15"
MERGE_STATES = {"behind", "blocked", "clean", "dirty", "unstable", "unknown"}


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


def refresh_merge_state(root: pathlib.Path, pr: dict) -> dict:
    """Fetch computed merge state for one registered PR; list responses may leave it null."""
    state = pr.get("mergeable_state")
    if isinstance(state, str) and state in MERGE_STATES and state != "unknown":
        return pr
    number = pr.get("number")
    if not isinstance(number, int):
        raise ValueError("cannot refresh merge state without a PR number; no launch authorized")
    try:
        result = subprocess.run(
            ["gh", "api", "--hostname", "github.com", f"repos/{REPO}/pulls/{number}"],
            cwd=root, capture_output=True, text=True, check=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        detail = str(exc)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            detail = exc.stderr.strip().splitlines()[0]
        raise ValueError(
            f"GitHub merge-state lookup for PR #{number} unavailable: {detail[:200]}. "
            "No resume or launch authorized."
        ) from exc
    try:
        detail = json.loads(result.stdout)
        if (not isinstance(detail, dict) or detail.get("number") != number
                or detail.get("state") != "open"):
            raise ValueError("expected the same open PR")
        state = detail.get("mergeable_state")
        if state is None:
            state = "unknown"
        if not isinstance(state, str) or state not in MERGE_STATES:
            raise ValueError(f"unexpected mergeable_state {state!r}")
        pr["mergeable_state"] = state
        return pr
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid GitHub merge-state response for PR #{number}: {exc}") from exc


def commit_path_blobs(root: pathlib.Path, sha: str, paths: list[str]) -> dict[str, str | None]:
    """Read a bounded set of exact path blobs at one immutable commit via GraphQL."""
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("expected a full commit SHA for path snapshot")
    if (not isinstance(paths, list) or len(paths) > 100
            or any(not isinstance(path, str) for path in paths)
            or len(paths) != len(set(paths))):
        raise ValueError("path snapshot must contain at most 100 unique paths")
    for path in paths:
        if (not isinstance(path, str) or not path or path.startswith("/")
                or "\\" in path or ".." in path.split("/") or posixpath.normpath(path) != path):
            raise ValueError(f"unsafe repository path in path snapshot: {path!r}")
    if not paths:
        return {}

    owner, repository = REPO.split("/", 1)
    fields = " ".join(
        f"p{index}: object(expression:{json.dumps(sha + ':' + path)}) "
        "{ ... on Blob { oid } }"
        for index, path in enumerate(paths)
    )
    query = (f'query {{ repository(owner:{json.dumps(owner)}, name:{json.dumps(repository)}) '
             f'{{ {fields} }} }}')
    try:
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            cwd=root, capture_output=True, text=True, check=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        detail = str(exc)
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            detail = exc.stderr.strip().splitlines()[0]
        raise ValueError(f"GitHub commit-path lookup unavailable: {detail[:200]}") from exc
    try:
        response = json.loads(result.stdout)
        if not isinstance(response, dict) or response.get("errors"):
            raise ValueError("GraphQL returned errors")
        objects = response["data"]["repository"]
        if not isinstance(objects, dict):
            raise ValueError("GraphQL repository result is missing")
        found = {}
        for index, path in enumerate(paths):
            value = objects.get(f"p{index}")
            if value is None:
                found[path] = None
            elif (isinstance(value, dict) and isinstance(value.get("oid"), str)
                  and re.fullmatch(r"[0-9a-f]{40}", value["oid"])):
                found[path] = value["oid"]
            else:
                raise ValueError(f"GraphQL returned a non-blob object for {path}")
        return found
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid GitHub commit-path response: {exc}") from exc


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
    merge_state = pr.get("mergeable_state", "unknown")
    print(f"PR: #{pr['number']} {pr['html_url']}")
    print(f"Status: {'DRAFT' if pr['draft'] else 'READY'}; Lifecycle: {lifecycle}")
    print(f"Merge state: {str(merge_state).upper()}")
    print(f"Head: {pr['head']['ref']} @ {pr['head']['sha']}")
    print(f"Resolved by: {matched_by}")
    if merge_state in {"dirty", "behind"}:
        print("Action: Update this PR against its base and resolve the merge state before resuming; do not create a new execution.")
    elif merge_state not in MERGE_STATES or merge_state == "unknown":
        print("Action: Recheck this PR's merge state before resuming; do not create a new execution.")
    elif pr["draft"] and lifecycle == "IN_PROGRESS":
        print("Action: Resume this PR at its current head; do not create a new branch or PR.")
    elif pr["draft"] and lifecycle == "BLOCKED":
        print("Action: Resolve the blocker in this PR before resuming; do not create a new execution.")
    elif not pr["draft"] and lifecycle == "REVIEW":
        print("Action: Continue review in this PR; do not launch a new execution or self-merge.")
    else:
        print("Action: Inspect/fix this PR's lifecycle before continuing; do not create a new execution.")


def print_programme_focus() -> None:
    print("Read: AGENTS.md; 00_WORK/README.md; "
          "02_REGISTRY/research/MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md"
          "#prospective-minimality-and-physical-execution")
    print("Focus: Reuse pinned proof owners; identify the exact missing parent substitution "
          "and remaining assumptions. Prefer structural certificates before enumerating histories.")
    print("For minimality work: distinguish the generator, full Cost-Info price and physical selection.")
    print("Handoff: PR + exact conclusion + consumed parent premise "
          "(or missing application/changed route), checks, blocker.")


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
                pr = refresh_merge_state(root, pr)
                print(f"Repository: {REPO}\nTask: {args.task_id}")
                print_execution(pr, matched_by)
                print_programme_focus()
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
        print_programme_focus()
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
        print("Write the durable result and its exact parent application or remaining gap in that PR.")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
