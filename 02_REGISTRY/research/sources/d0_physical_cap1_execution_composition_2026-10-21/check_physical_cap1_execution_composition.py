#!/usr/bin/env python3
"""Integrity and narrow replay for the same-execution physical composition."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
PKG=Path(__file__).resolve().parent
INPUT="92c00ccbf39e6e21e4383f7a7b573ab7c7c6f1be"
GROUPS={
    "moving_query":("SOURCE_PINS.json","files","VERIFICATION.json","check_native_query_value_and_jet.py",17),
    "book_binding":("SOURCE_PINS.json","sources","VERIFICATION.json","check_exact_cq_book_binding.py",17),
    "independent_input":("SOURCE_PINS.json","sources","VERIFICATION.json","check_upstream_reaction.py",21),
    "car_effect":("SOURCE_PINS.json","sources","VERIFICATION.json","check_same_effect_spectrum.py",50),
    "restricted_car":("SOURCE_PINS.json","sources",None,None,None),
}

def git(*args):
    result=subprocess.run(["git",f"--work-tree={ROOT}",*args],cwd=ROOT,check=True,capture_output=True)
    return result.stdout

def sha(data): return hashlib.sha256(data).hexdigest()

def run():
    manifest=json.loads((PKG/"MANIFEST.json").read_text())
    assert manifest["input_commit"]==INPUT
    for item in manifest["files"]:
        data=(PKG/item["path"]).read_bytes()
        assert sha(data)==item["sha256"], f"artifact hash mismatch: {item['path']}"
    pinned={}
    pin_counts={}
    for name,(pin_name,field,_,_,_) in GROUPS.items():
        directory=PKG/name
        record=json.loads((directory/pin_name).read_text())
        commit=record.get("input_commit",record.get("repository_head"))
        assert commit==INPUT, f"wrong input commit in {name}"
        rows=record[field]
        pin_counts[name]=len(rows)
        for row in rows:
            path=row["path"]
            content=git("show",f"{INPUT}:{path}")
            assert sha(content)==row["sha256"], f"source SHA mismatch: {path}"
            blob=git("rev-parse",f"{INPUT}:{path}").decode().strip()
            assert blob==row["git_blob"], f"source Git blob mismatch: {path}"
            assert (ROOT/path).read_bytes()==content, f"working source differs from pin: {path}"
            if path in pinned:
                assert pinned[path]==(row["sha256"],row["git_blob"]), f"conflicting duplicate pin: {path}"
            pinned[path]=(row["sha256"],row["git_blob"])
    controls={}
    for name,(_,_,expected_name,script,expected_count) in GROUPS.items():
        directory=PKG/name
        if script is None:
            recorded=json.loads((ROOT/"02_REGISTRY/research/certificates/a4d_native_field_instrument_jet_results.json").read_text())
            assert recorded["status"]=="PASS_COMPLETE_INSTRUMENT_FIRST_JET_AND_FIELD_TANGENT_WITNESS"
            assert recorded["source_v3_receipt"]["physical_admission"] is False
            assert recorded["source_v3_receipt"]["complete_H_J_R_closed"] is False
            assert recorded["G0_or_GR_closed"] is False
            controls[name]={"status":"PINNED_SCOPE_ONLY","recorded_exact_controls":recorded["exact_controls"],"replayed":False}
            continue
        expected=json.loads((directory/expected_name).read_text())
        assert expected["status"]=="PASS"
        check_proc=subprocess.run([sys.executable,str(directory/script)],cwd=ROOT,check=True,capture_output=True,text=True)
        result=json.loads(check_proc.stdout)
        assert result["status"]=="PASS", f"narrow checker failed: {name}"
        if name in ("moving_query","car_effect"): count=len(result["checks"])
        elif name=="book_binding": count=result["checks"]
        else: count=result["check_count"]
        assert count==expected_count, f"wrong check count from {name}: {count}"
        controls[name]={"status":"PASS","checks":count}
    return {
      "status":"PASS",
      "input_commit":INPUT,
      "source_files_pinned":pin_counts,
      "unique_source_files":len(pinned),
      "frozen_artifact_files":len(manifest["files"]),
      "narrow_controls":controls,
      "scope":"same cap-one algebra/source composition, narrow CAR effect-spectrum exclusion, and a source-pinned existing restricted CAR result; no physical admission or GR closure",
    }

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--write-receipt",action="store_true")
    args=parser.parse_args()
    result=run()
    payload=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.write_receipt:
        (PKG/"INTEGRATION_VERIFICATION.json").write_text(payload,encoding="utf-8")
    print(payload,end="")
