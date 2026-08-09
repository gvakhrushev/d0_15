#!/usr/bin/env python3
"""d0_prune_process_residue.py — delete campaign memos that no result points at.

A memo is a report about an attempt. The result of an attempt lives in the registry, in Lean and
in a certificate; the memo that produced it is scaffolding. Scaffolding that nothing cites is
storage cost with no reader — and it makes the corpus look like it is made of reports.

The rule is mechanical. A memo is LIVE if its filename appears anywhere in the corpus proper — the
books, theory map, certificates, verification tables, publication set, registry/ledger docs, tools,
quarantine ledger, CI, root entry documents, **or a Lean module docstring** (modules cite their
forge memo by name, and those are live references).

Liveness then propagates by **transitive closure**: a memo cited by a live memo is itself live.
This is not caution, it is correctness — the evidence the epistemic-engine README stands on is a
*chain* (the GAP-E campaign is twelve recorded passes, each citing the last), and deleting an
intermediate pass destroys the audit trail the corpus claims as its distinctive value. Residue is
what remains unreachable from any live citation: files nothing at all points at, directly or
indirectly.

  default      link-preserving: delete only the unreachable set. Guarantees zero dangling
               references anywhere, including inside the memos that survive.
  --aggressive delete every memo not cited from the corpus proper, ignoring memo-to-memo edges.
               Reclaims more, but leaves dangling references inside kept memos; the count of
               references it would break is reported before anything is removed.

Dry-run by default: prints the list and the reclaimed size, changes nothing. Pass `--apply` to
delete (via `git rm` when the file is tracked, so the content stays recoverable from history).

Exit 0 = ok, 2 = IO/usage.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "_TASKS_CENTER_ATTACK"

# Where a live reference to a memo could legitimately live.
SCAN_DIRS = ("01_BOOKS", "03_THEORY_MAP", "05_CERTS", "04_VERIFICATION", "00_PUBLICATION",
             "docs", "06_AUDIT", "tools", "00_LANGUAGE_NORMALIZATION", "08_PASSPORTS",
             "_QUARANTINE", ".github")
SCAN_ROOT_FILES = ("README.md", "D0_EPISTEMIC_ENGINE_README.md", "D0_CLAIM_CLOSURE_CONTRACT.md",
                   "AGENTS.md", "CLAUDE.md")
SCAN_SUFFIXES = {".md", ".csv", ".py", ".json", ".txt", ".yml", ".yaml", ".dot"}


def corpus_text() -> str:
    parts: list[str] = []
    for d in SCAN_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in SCAN_SUFFIXES:
                try:
                    parts.append(p.read_text(errors="ignore"))
                except OSError:
                    pass
    # the registry and assumption ledger live under the Lean package's docs/
    ldocs = ROOT / "09_LEAN_FORMALIZATION" / "docs"
    if ldocs.exists():
        for p in ldocs.rglob("*"):
            if p.is_file():
                try:
                    parts.append(p.read_text(errors="ignore"))
                except OSError:
                    pass

    # Lean module docstrings cite their forge memo by name ("Forge memo: _TASKS_CENTER_ATTACK/…").
    # Those are live references and must keep the memo alive. Scan only the D0 source subtree —
    # never the whole package, whose .lake/mathlib tree is gigabytes and contains no D0 references.
    lsrc = ROOT / "09_LEAN_FORMALIZATION" / "D0"
    if lsrc.exists():
        for p in lsrc.rglob("*.lean"):
            try:
                parts.append(p.read_text(errors="ignore"))
            except OSError:
                pass
    for f in SCAN_ROOT_FILES:
        p = ROOT / f
        if p.exists():
            parts.append(p.read_text(errors="ignore"))
    return "\n".join(parts)


def residue(transitive: bool = True) -> tuple[list[Path], list[Path], int]:
    """Return (kept, residue, broken_refs).

    `broken_refs` counts references from KEPT memos into the residue set — zero by construction
    when `transitive` is on, and the cost of the aggressive mode when it is off.
    """
    if not TASKS.exists():
        return [], [], 0
    files = [p for p in TASKS.iterdir() if p.is_file() and not p.name.startswith(".")]
    text = corpus_text()
    body: dict[str, str] = {}
    for p in files:
        try:
            body[p.name] = p.read_text(errors="ignore")
        except OSError:
            body[p.name] = ""

    live = {p.name for p in files if p.name in text}
    if transitive:
        # a memo cited by a live memo is itself live — iterate to fixpoint
        while True:
            grown = {f.name for f in files
                     if f.name not in live and any(f.name in body[k] for k in live)}
            if not grown:
                break
            live |= grown

    kept = [p for p in files if p.name in live]
    gone = [p for p in files if p.name not in live]
    gone_names = {p.name for p in gone}
    broken = sum(1 for k in kept for n in gone_names if n in body[k.name])
    return sorted(kept), sorted(gone), broken


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="actually delete (default: dry run)")
    ap.add_argument("--aggressive", action="store_true",
                    help="ignore memo-to-memo citations; deletes more but breaks references "
                         "inside the memos that survive")
    args = ap.parse_args()

    try:
        kept, gone, broken = residue(transitive=not args.aggressive)
    except OSError as exc:
        print(f"IO error: {exc}", file=sys.stderr)
        return 2

    size = sum(p.stat().st_size for p in gone if p.exists())
    mode = "aggressive (corpus citations only)" if args.aggressive else "link-preserving (transitive closure)"
    print(f"_TASKS_CENTER_ATTACK: {len(kept) + len(gone)} files | mode: {mode}")
    print(f"  live {len(kept)} (kept) | residue {len(gone)} ({size/1e6:.2f} MB)")
    for p in gone:
        print(f"  residue  {p.relative_to(ROOT)}")

    if broken:
        print(f"\nWARNING: deleting this set breaks {broken} reference(s) from kept memos into the "
              f"residue. Drop --aggressive to keep the evidence chains intact.", file=sys.stderr)

    if not args.apply:
        print("\ndry run — nothing deleted. Re-run with --apply to remove the residue.")
        return 0

    tracked = set()
    try:
        out = subprocess.run(["git", "ls-files", "_TASKS_CENTER_ATTACK"], cwd=ROOT,
                             capture_output=True, text=True, check=False).stdout
        tracked = {(ROOT / ln).resolve() for ln in out.splitlines() if ln.strip()}
    except OSError:
        pass

    git_batch = [str(p.relative_to(ROOT)) for p in gone if p.resolve() in tracked]
    if git_batch:
        subprocess.run(["git", "rm", "-q", "--"] + git_batch, cwd=ROOT, check=False)
    for p in gone:
        if p.exists():
            p.unlink()
    print(f"\ndeleted {len(gone)} files ({size/1e6:.2f} MB); "
          f"{len(git_batch)} were tracked and remain recoverable from git history.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
