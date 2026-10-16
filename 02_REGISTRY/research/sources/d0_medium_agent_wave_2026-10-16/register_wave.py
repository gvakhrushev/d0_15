#!/usr/bin/env python3
"""Install this one approved wave into the EXISTING work manifest; never launch agents.
--check is read-only. --apply is a rollback-safe local CONTROL transaction, not a Git push.
This is an intake helper, not another queue, dispatcher, or scientific verifier.
"""
from __future__ import annotations
import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
EXPECTED_BRANCH="control/gr-research-flow"

TASK_IDS=(
 "WRK-A4D-CERTIFICATE-INPUT-CLOSURE",
 "WRK-A4D-LEAN-GOLDEN-CURVATURE-KERNEL",
 "WRK-A4D-LEAN-SOURCE-REFLECTION",
 "WRK-A4D-TRANSVERSE-MATCHING-RESIDUAL",
 "WRK-A4D-PF-MEASURE-SOURCE-TRANSPORT",
 "WRK-A4D-ANISOTROPIC-NORMAL-SOURCE",
 "WRK-A4D-MOVING-SCALE-VARIATION",
 "WRK-A4D-PREPARATION-SECOND-VARIATION",
 "WRK-A4D-FLAT-SHEAR-COMMON-SOURCE")

def load_rows():
    rows=[]
    for task_id in TASK_IDS:
        text=(HERE/(task_id+".md")).read_text(encoding="utf8")
        prefix="Parent: `"
        lines=[line for line in text.splitlines() if line.startswith(prefix)]
        if len(lines)!=1 or not lines[0].endswith("`"):
            raise ValueError("ambiguous parent in brief: "+task_id)
        parent=lines[0][len(prefix):-1]
        heading="## Точное обязательство\n"
        if text.count(heading)!=1:
            raise ValueError("one terminal statement required: "+task_id)
        goal=text.split(heading,1)[1].split("\n\n",1)[0].strip()
        if not goal:
            raise ValueError("empty terminal: "+task_id)
        rows.append({"id":task_id,"class":"WORKER","parent":parent,
          "state":"PLANNED","affected_claims":["D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001"],
          "exit_condition":goal,"brief":"00_WORK/tasks/"+task_id+".md"})
    return rows

ROWS=load_rows()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def plan(root: Path):
    root=root.resolve()
    manifest_path=root/"00_WORK/manifest.json"
    manifest=json.loads(manifest_path.read_text(encoding="utf8"))
    require(manifest.get("schema")=="d0-work/1", "wrong manifest schema")
    require(manifest.get("limits")=={"EXPENSIVE":3,"WORKER":5,"CONTROL":2},
            "WIP differs: obtain a new CONTROL decision instead of silently changing it")
    old=manifest["tasks"]
    by_id={t["id"]:t for t in old}
    require(len(by_id)==len(old), "duplicate current task IDs")
    with (root/"02_REGISTRY/claims.csv").open(encoding="utf8",newline="") as stream:
        valid={row["claim_id"] for row in csv.DictReader(stream)}
    changes={}
    added=[]
    for row in ROWS:
        require(row["parent"] in by_id and by_id[row["parent"]]["class"]=="CONTROL",
                "missing actual CONTROL parent")
        require(set(row["affected_claims"])<=valid, "unregistered affected claim")
        source=HERE/(row["id"]+".md")
        text=source.read_text(encoding="utf8")
        require(text.startswith("# "+row["id"]+"\n"), "brief ID mismatch")
        for token in ("Repository: `gvakhrushev/d0_15`",
                      "## Why delegated","## GitHub execution contract","## Chat handoff"):
            require(token in text, "incomplete brief: "+token)
        target=root/row["brief"]
        require(target.resolve().is_relative_to(root), "brief path/symlink escapes repository")
        if row["id"] in by_id:
            existing=by_id[row["id"]]
            require({k:v for k,v in existing.items() if k!="state"} ==
                    {k:v for k,v in row.items() if k!="state"}, "existing registration conflicts")
            require(target.is_file() and target.read_text(encoding="utf8")==text,
                    "existing task brief changed: preserve it and resolve manually")
        else:
            require(not target.exists(), "unowned task file exists")
            added.append(row)
            changes[row["brief"]]=text.encode("utf8")
    if added:
        manifest["tasks"]=old+added
        changes["00_WORK/manifest.json"]=(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode()
    return changes, [x["id"] for x in added]

def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(prefix=".d0-wave-",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as out:
            out.write(data)
        os.replace(temp,path)
    finally:
        if os.path.exists(temp): os.unlink(temp)

def apply(root: Path):
    root=root.resolve()
    changes,added=plan(root)
    branch=subprocess.run(["git","branch","--show-current"],cwd=root,
                          check=True,capture_output=True,text=True).stdout.strip()
    require(branch==EXPECTED_BRANCH, "apply only in assigned #324 CONTROL branch")
    watched=set(changes)|{"README.md","00_WORK/STATUS.md"}
    # Do not overwrite another agent's uncommitted work.
    status=subprocess.run(["git","status","--porcelain","--",*sorted(watched)],cwd=root,
                          check=True,capture_output=True,text=True)
    require(not status.stdout.strip(), "owned paths have local changes; coordinate first")
    for row in ROWS:
        if row["id"] in added:
            history=subprocess.run(["git","log","--all","-1","--format=%H","--",row["brief"]],
                                   cwd=root,check=True,capture_output=True,text=True).stdout.strip()
            require(not history, "task existed in Git history: do not resurrect retired work")
    saved={p:((root/p).read_bytes() if (root/p).exists() else None) for p in watched}
    try:
        for path,data in changes.items(): atomic_write(root/path,data)
        commands=[["tools/render_work_status.py"],
                  ["tools/validate_work.py"],
                  ["tools/validate_agent_protocol.py"],
                  ["tools/render_work_status.py","--check"]]
        for args in commands:
            subprocess.run([sys.executable,*args],cwd=root,check=True,timeout=180)
    except Exception:
        for path,data in saved.items():
            if data is None:
                (root/path).unlink(missing_ok=True)
            else:
                atomic_write(root/path,data)
        raise
    return added

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root",type=Path,default=HERE.parents[3])
    modes=ap.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check",action="store_true")
    modes.add_argument("--apply",action="store_true")
    args=ap.parse_args()
    try:
        added=apply(args.repo_root) if args.apply else plan(args.repo_root)[1]
        print(json.dumps({"mode":"APPLIED_LOCALLY_NOT_COMMITTED" if args.apply else "READ_ONLY",
              "new_task_ids":added,"agents_launched":False,
              "main_updated":False,"scientific_acceptance":False},ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as exc:
        print("REGISTRATION_BLOCKED: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
