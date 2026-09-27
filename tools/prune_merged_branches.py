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
    "wrk/a4d-observer-frame-car-lift",           # pre-flow PR #87; canonical task relaunched from current main
    "draft/a4d-primal-dual-parent-algebra",       # theorem surface fully subsumed by main
    "work/geo-car-dirac-parity",                  # theorem surface subsumed; main has extra Dirac aliases

    # Audited A4D relaunch/squash tails; canonical payloads are landed on main.
    "work/a4d-pure-gauge-dressing-torsor-passport",  # lifecycle-only draft superseded by merged PR #159
    "wrk/a4d-crossed-dressing-mismatch",              # memo/certificate exact on main via merged PR #146
    "wrk/a4d-quotient-saturation-canonical",          # exact canonical modules landed via merged PR #158
    "wrk/a4d-quotient-saturation-passport",           # exact canonical modules landed via merged PR #158
    "wrk/a4d-quotient-saturation-passport-r2",        # older implementation superseded by merged PR #158
    "wrk/a4d-quotient-saturation-passport-v3",        # exact canonical modules landed via merged PR #158
    "wrk/a4d-relative-ae-graphification-closure",     # modules exact on main via merged PR #156
    "wrk/a4d-relative-ae-graphification-closure-v2",  # modules exact on main via merged PR #156
    "wrk/a4d-relative-ae-graphification-closure-v3",  # modules exact on main via merged PR #156
    "wrk/a4d-relative-ae-graphification-closure-v4",  # modules exact on main via merged PR #156
    "wrk/a4d-resolved-correlated-action-passport",    # module exact on main via merged PR #153
    "wrk/a4d-resolved-correlated-action-passport-v2", # module exact on main via merged PR #153
    "wrk/a4d-resolved-correlated-action-passport-v3", # module exact on main via merged PR #153
    "wrk/a4d-sourced-mismatch-factor-passport",       # module exact on main via merged PR #147
    "wrk/a4d-sourced-mismatch-factor-passport-v2",    # module exact on main via merged PR #147
    # Audited 2026-09-27 post-wave tails. These are either exact ancestors of
    # accepted heads, closed superseded attempts, or temporary sync branches
    # whose durable payload is already on main. Open PR heads are still
    # excluded independently below, so this list cannot prune active work.
    "tmp/rebuild-pr246-contract",                           # exact ancestor of accepted #246 head
    "tmp/sync-pr246-moving-sign",                          # #246 cert byte-identical; memo superseded by accepted #246
    "control/a4d-star-density-lorentz-nonlinear-quotient", # closed #179; superseded by merged #180 r2
    "control/register-j2-smooth-resonance-closure",        # closed #214; superseded by merged #215 v2
    "exp/a4d-joint-holonomy-quotient-completeness",        # closed #186; superseded by merged #196 r3
    "exp/a4d-joint-holonomy-quotient-completeness-r2",     # closed #194; superseded by merged #196 r3
    "wrk/a4d-joint-diagonal-invisible-germ",               # closed #235; task remains PLANNED for fresh relaunch
    "wrk/a4d-joint-resonance-linear-kernel",                # closed #231; superseded by clean replay #252
    "wrk/a4d-joint-one-d-residual-germs",                   # closed #234; superseded by clean replay #253
    "wrk/a4d-affine-curvature-cert",                       # closed #166; superseded by merged clean #168
    "wrk/a4d-formalize-affine-relative-solder",               # closed #210; superseded by merged #218 r2
    "wrk/a4d-formalize-cartan-hodge-translation-nogo",         # merged #192; safe retained payload on main
    "wrk/a4d-formalize-checkerboard-nonlinear-obstruction",    # closed #211; superseded by merged #221 r2
    "wrk/a4d-formalize-gauge-image-seam-resolution",           # closed #212; superseded by merged #220 r2
    "wrk/a4d-formalize-nonlinear-lorentz-quotient",            # closed #191; superseded by merged #195 r2
    "wrk/a4d-formalize-star-einstein-seed",                    # closed #206; superseded by merged #217 r2
    "exp/a4d-role-bivector-insertion-spatial-selector",   # #169 explicitly superseded; result moved unchanged to merged #170
    "exp/a4d-oriented-spatial-role-selector",             # #172 explicitly closed as duplicate of merged #170
    "control/a4d-role-bivector-oriented-density-selector",# #173 explicitly closed as duplicate of merged #170
    "exp/a4d-star-translation-invariant-action-completion",# stale source #182 replaced by clean packet #198
    "exp/a4d-star-nonlinear-stationary-rigidity-r2",       # #198 exact science byte-identical on main
    "exp/a4d-curved-stationary-sector-after-affine-completion", # stale source #187 replaced by clean packet #197
    "exp/a4d-curved-stationary-sector-r2",                 # #197 exact science byte-identical on main
    "wrk/a4d-diagonal-microstructure-connection-stationary-slow-lift", # closed stale #243; task remains PLANNED for fresh relaunch
    "control/strengthen-role-weld-scout",                  # no unique commits; main is strict descendant

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
