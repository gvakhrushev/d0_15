"""Replay the bundled evidence in a fresh directory, optionally supplying --node."""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from importlib.metadata import version

base = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--node", default=shutil.which("node"))
parser.add_argument("--output",type=Path,default=Path(__file__).with_name("TESTS.json"))
options = parser.parse_args()
digest = lambda data: hashlib.sha256(data).hexdigest()
sources=json.loads((base/"primary/SOURCES.json").read_text())["primary_files"]
for name,item in sources.items():
    assert digest((base/"primary"/name).read_bytes()) == item["sha256"], name
cases=[]
def add(key,relative,expected=None,flags=(),language="python"):
    cases.append((key,relative,expected,flags,language))
for name in ("carry","preseal_review","coframe_response","cq_tail","memory_spectrum","metric","paid_fibres","query_clocks","raw_height","stopped_cq"):
    match="diagnostics/"+name+"_result.json"
    add("diagnostics/"+name,"diagnostics/check_"+name+".py",match if (base/match).exists() else None)
add("diagnostics/B121-portable", "diagnostics/replay_b121.py", "primary/B121/RESULT.json")
for script,receipt in [
    ("check_projective_rigidity.py","expected_projective_rigidity_controls.json"),
    ("check_full128_cq_coframe_residual.py","expected_full128_cq_coframe_residual.json"),
    ("check_actual_stopped_cost.py","expected_actual_stopped_cost.json"),
    ("check_direct_cq_source.py","expected_direct_cq_source.json")]:
    add("checkpoint/"+script,"primary/checkpoint/"+script,"primary/checkpoint/"+receipt,("-Werror",))
    if "residual" in script:
        add("checkpoint/optimized/"+script,"primary/checkpoint/"+script,"primary/checkpoint/"+receipt,("-O","-Werror"))
add("checkpoint/imported-helper-standalone","primary/checkpoint/check_uniform_book_source.py")
add("source/A67","primary/A67/check_scene_reference.py")
add("source/143484","primary/check_complete_143484_stage_clock_cost_selector.mjs",language="node")
def compare(actual,expected):
    differences=[]
    def walk(a,b,p):
        if isinstance(a,float) and isinstance(b,float) and a!=b and math.isfinite(a) and math.isfinite(b):
            differences.append((p,abs(a-b),abs(a-b)<=2e-10+2e-10*abs(b)))
        elif isinstance(a,dict) and isinstance(b,dict) and a.keys()==b.keys():
            for k in a:walk(a[k],b[k],p+"/"+str(k))
        elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
            for i,(x,y) in enumerate(zip(a,b)):walk(x,y,p+"/"+str(i))
        elif type(a)!=type(b) or a!=b:
            differences.append((p,None,False))
    walk(actual,expected,"")
    return {"exact_json_match":not differences,
            "float_only_within_tolerance":bool(differences) and all(t[2] for t in differences),
            "maximum_float_difference":max((t[1] for t in differences if t[1] is not None),default=0),
            "different_json_fields":len(differences),"first_different_fields":[t[0] for t in differences[:12]]}
with tempfile.TemporaryDirectory(prefix="d0-calibration-replay-") as temp:
    workspace=Path(temp)
    for folder in ("primary","diagnostics"):
        shutil.copytree(base/folder,workspace/folder,ignore=shutil.ignore_patterns("__pycache__","TESTS.json"))
    # Run the unchanged A67 primary source at its original relative depth.
    owner_root=workspace/"a67-layout"
    a67=owner_root/"02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round67/valuation/check_scene_reference.py"
    a67.parent.mkdir(parents=True)
    shutil.copy2(workspace/"primary/A67/check_scene_reference.py",a67)
    lean=owner_root/"03_FORMALIZATION/D0/Integration/V15/RawZone.lean"
    lean.parent.mkdir(parents=True);shutil.copy2(workspace/"primary/A67/RawZone.lean",lean)
    def run(case):
        name,relative,expected,flags,language=case
        file=a67 if name=="source/A67" else workspace/relative
        if language=="node" and not options.node:
            return {"check":name,"status":"not_run","reason":"Node.js was not supplied"}
        command=[options.node,str(file)] if language=="node" else [sys.executable,"-B",*flags,str(file)]
        proc=subprocess.run(command,cwd=workspace,capture_output=True,timeout=180)
        output=proc.stdout;notes=proc.stderr.decode(errors="replace")
        result=dict(check=name,status="pass" if proc.returncode==0 else "fail",exit_code=proc.returncode,
                    stdout_sha256=digest(output),stderr=notes[-2400:])
        if proc.returncode:result["stdout_tail"]=output.decode(errors="replace")[-700:]
        if expected and proc.returncode==0:
            result["expected"]=expected
            result.update(compare(json.loads(output),json.loads((workspace/expected).read_bytes())))
            if not (result["exact_json_match"] or result["float_only_within_tolerance"]):result["status"]="fail"
        if expected is None and proc.returncode==0:
            lines=output.decode(errors="replace").splitlines()
            result["output_excerpt"]=(lines[-3:] if len(lines)>3 else lines)
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,cases))
report=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    isolation="Fresh ephemeral copy of only primary/ and diagnostics/. Source paths rebound locally; no Git repository or external absolute paths used by diagnostics.",
    platform=platform.platform(),architecture=platform.machine(),python=sys.version,
    python_executable=sys.executable,libraries={p:version(p) for p in ("sympy","numpy","scipy","mpmath")},
    node_version=(subprocess.check_output([options.node,"--version"],text=True).strip() if options.node else None),
    primary_files_hash_verified=len(sources),numeric_comparison="For frozen primary floating diagnostics, absolute and relative tolerances are both 2e-10. Exact matches are reported separately.",
    checks=results,
    not_reproduced=["A full Lean build, all historical graph/heat/geometry suites, all 42-field dynamics, and an execution on physical hardware.",
        "Equality of microscopic Book03 Cost−Info with the tested entropy or price, universal physical admission, and full GR closure."])
report["all_executed_checks_passed"]=all(x["status"]=="pass" for x in results)
options.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({r["check"]:r["status"] for r in results},indent=2))
sys.exit(0 if report["all_executed_checks_passed"] else 1)
