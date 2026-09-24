#!/usr/bin/env python3
"""Prune remote branches whose work is already safely represented elsewhere.

Automatic class:
- exact current heads of merged pull requests.

Explicit legacy-safe class:
- stale duplicate/closed branches whose payload was audited as superseded or
  already present on main during the 2026-09-24 GitHub-first migration.

Never delete:
- default/main;
- archive anchor;
- any branch that currently backs an open PR;
- explicitly protected candidate branches.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
REPO = os.environ.get("GITHUB_REPOSITORY", "gvakhrushev/d0_15")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

PROTECTED = {
    "main",
    "archive-d0v15-main",
    "wrk/a4d-observer-frame-car-lift",
    "draft/a4d-primal-dual-parent-algebra",
    "work/geo-car-dirac-parity",
}

LEGACY_SAFE = {
    "codex/a4d-second-order-cell-energy-ward",  # stale duplicate PR #89
    "work/acap-riesz-mismatch-lean",            # module already identical on main
    "work/c1-common-carrier",                   # superseded by v2 / PR #47
    "work/c1-common-carrier-v2",                # payload already on main / PR #47
    "draft/a4d-cubical-differential-cartan",    # superseded by merged PR #57
    "draft/public-claim-strength-lint",          # superseded by merged PR #73
    "research/post-c1-rho1-truth-repair",       # superseded by merged PR #36
    "wrk-a4d-observer-frame-car-lift",           # golden memo copied exactly into PR #86
}


def request(path: str, method: str = "GET") -> object | None:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is required")
    req = urllib.request.Request(
        API + path,
        method=method,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "d0-branch-hygiene",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            return json.loads(data) if data else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {method} {path} failed: {exc.code} {body}") from exc


def paged(path: str) -> list[dict]:
    out: list[dict] = []
    page = 1
    sep = "&" if "?" in path else "?"
    while True:
        batch = request(f"{path}{sep}per_page=100&page={page}")
        assert isinstance(batch, list)
        out.extend(batch)
        if len(batch) < 100:
            return out
        page += 1


def delete_branch(name: str, dry_run: bool) -> None:
    print(("WOULD_DELETE" if dry_run else "DELETE"), name)
    if dry_run:
        return
    encoded = urllib.parse.quote(name, safe="")
    request(f"/repos/{REPO}/git/refs/heads/{encoded}", method="DELETE")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    branches = {
        b["name"]: b["commit"]["sha"]
        for b in paged(f"/repos/{REPO}/branches")
    }
    open_prs = paged(f"/repos/{REPO}/pulls?state=open")
    closed_prs = paged(f"/repos/{REPO}/pulls?state=closed")

    open_heads = {
        pr["head"]["ref"]
        for pr in open_prs
        if pr.get("head", {}).get("repo")
        and pr["head"]["repo"].get("full_name") == REPO
    }

    exact_merged: set[str] = set()
    for pr in closed_prs:
        if not pr.get("merged_at"):
            continue
        head = pr.get("head") or {}
        repo = head.get("repo") or {}
        name = head.get("ref")
        sha = head.get("sha")
        if repo.get("full_name") != REPO or not name or not sha:
            continue
        if branches.get(name) == sha:
            exact_merged.add(name)

    candidates = (exact_merged | LEGACY_SAFE) & branches.keys()
    candidates -= PROTECTED
    candidates -= open_heads

    for name in sorted(candidates):
        delete_branch(name, args.dry_run)

    print(
        json.dumps(
            {
                "branch_count_before": len(branches),
                "open_pr_heads": sorted(open_heads),
                "exact_merged_candidates": len(exact_merged),
                "legacy_safe_present": sorted(LEGACY_SAFE & branches.keys()),
                "deleted_or_would_delete": sorted(candidates),
                "protected_present": sorted(PROTECTED & branches.keys()),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
