#!/usr/bin/env python3
"""Validate or print the D0 strategy handoff. Read-only; never launch agents or Git writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys

PLAN = '02_REGISTRY/research/D0_GR_EXECUTION_PLAN.json'
IDEAS = '02_REGISTRY/research/D0_IDEA_REGISTER.json'
REPO = 'gvakhrushev/d0_15'
ROLES = ('integrator', 'evidence', 'foundations', 'nonlinear')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def safe_path(root: Path, value: str) -> Path:
    p = PurePosixPath(value)
    require(not p.is_absolute() and '..' not in p.parts, 'Unsafe repository path')
    target = (root / value).resolve()
    require(target.is_relative_to(root.resolve()), 'Path escapes repository')
    return target


def load(root: Path) -> tuple[dict, dict, dict]:
    return tuple(json.loads((root / p).read_text(encoding='utf8')) for p in
                 (PLAN, IDEAS, '00_WORK/manifest.json'))


def validate(root: Path) -> dict:
    plan, ideas, manifest = load(root)
    require(plan.get('schema') == 'd0-gr-execution/1', 'Wrong execution schema')
    require(plan.get('repository') == REPO, 'Wrong repository')
    require(plan.get('snapshot_is_live_status') is False, 'Snapshot is not a live heartbeat')
    require(ideas.get('schema') == 'd0-idea-register/1', 'Wrong ideas schema')
    require(set(plan.get('roles', {})) == set(ROLES), 'Missing or unexpected handoff role')
    task_list = manifest['tasks']
    tasks = {t['id']: t for t in task_list}
    require(len(tasks) == len(task_list), 'Duplicate task registration')
    require(manifest['limits'] == {'EXPENSIVE': 3, 'WORKER': 5, 'CONTROL': 2},
            'Handoff must not raise WIP limits')
    for path in (plan['strategy'], plan['ideas'], plan['contract'], 'D0_START_HERE_RU.md',
                 '02_REGISTRY/research/D0_HANDOFF_SOURCE_NOTES_RU.md'):
        require(safe_path(root, path).is_file(), f'Missing handoff input: {path}')
    for role, item in plan['roles'].items():
        task = item.get('task')
        if item.get('registration_state') == 'RETIRED':
            require(isinstance(item.get('retired_pr'), int), 'Retired role requires acceptance PR')
            continue
        require(task in tasks, f'Role {role} has no registered task')
        brief = safe_path(root, tasks[task]['brief'])
        require(brief.is_file(), f'Missing brief: {brief}')
        text = brief.read_text(encoding='utf8')
        require(text.splitlines()[0] == f'# {task}', 'Brief task heading mismatch')
        require('Repository: `gvakhrushev/d0_15`' in text, 'Brief missing repository')
        for heading in ('## Why delegated', '## GitHub execution contract', '## Chat handoff'):
            require(heading in text, f'Missing executable section: {heading}')
        require(item.get('consumer') and item.get('inputs') and item.get('write_fence'),
                'Role must have inputs, write fence and actual consumer')
        for path in item['write_fence']:
            safe_path(root, path)
    nonlinear = plan['roles']['nonlinear']
    require(nonlinear.get('gate', '').startswith('HOLD_') or nonlinear.get('gate_review'),
            'Nonlinear launch needs common-interface and WIP review')
    ids = set()
    for idea in ideas['ideas']:
        require(idea['id'] not in ids, 'Duplicate idea ID')
        ids.add(idea['id'])
        for key in ('origin', 'mechanism', 'current_boundary', 'next_proof_use', 'consumer_role'):
            require(bool(idea.get(key)), f'Idea lacks {key}')
        require(idea.get('proof_status') == 'NO_PROMOTION_BY_HANDOFF',
                'Idea preservation cannot certify a theorem')
    require(len(ids) >= 18, 'Loss of preserved strategic leads')
    for entry in plan['snapshot']['prs']:
        require(re.fullmatch(r'[0-9a-f]{40}', entry['head']) is not None, 'Unpinned source SHA')
    return plan


def dispatch_text(root: Path, role: str) -> str:
    plan = validate(root)
    _, _, manifest = load(root)
    item = plan['roles'][role]
    tid = item['task']
    task = next((t for t in manifest['tasks'] if t['id'] == tid), None)
    require(task is not None, 'Role retired; read its accepted result, do not redispatch')
    lines = [f'Repository: {REPO}', f'Role: {role}', f'Task: {tid}',
             'Start: D0_START_HERE_RU.md', f'Brief: {task["brief"]}',
             f'Launch gate: {item["gate"]}', f'Consumer: {item["consumer"]}',
             'Status: NOT_DISPATCHED; this command performs no remote lookup or write.',
             'Before launch: read live open PRs and search their exact Task: field.',
             'A PLANNED main row is not evidence that no execution exists.',
             f'GitHub search: repo:{REPO} is:pr is:open "{tid}"',
             'If found: resume/review that PR with its current owner; do not create a duplicate.',
             'If absent: resolve the stated gate and main registration before task_lifecycle start.',
             'Snapshot PRs (historical input, not current execution status):']
    lines += [f'  #{p["number"]}: {p["head"]} ({p["branch"]})'
              for p in plan['snapshot']['prs']]
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--role', choices=ROLES)
    group.add_argument('--check', action='store_true')
    args = ap.parse_args()
    try:
        if args.check:
            validate(args.repo_root)
            print('PASS_D0_HANDOFF_STRUCTURE_NOT_SCIENTIFIC_ACCEPTANCE')
        else:
            print(dispatch_text(args.repo_root, args.role))
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        print(f'HANDOFF_BLOCKED: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
