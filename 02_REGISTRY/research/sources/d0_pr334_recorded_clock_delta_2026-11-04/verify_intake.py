#!/usr/bin/env python3
"""Check the pinned #334 delta without running its research checkers."""
import argparse
import gzip
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, description):
    if not condition:
        raise ValueError(description)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-source-objects", action="store_true")
    args = parser.parse_args()
    m = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    require(m["schema"] == "d0-pr334-recorded-clock-intake-v1", "schema")
    archive = (ROOT / "UPSTREAM_SOURCES.zip").read_bytes()
    require(sha(archive) == m["archive_sha256"], "archive digest")
    content = {}
    with zipfile.ZipFile(ROOT / "UPSTREAM_SOURCES.zip") as z:
        require(len(z.namelist()) == len(set(z.namelist())), "duplicate archive member")
        require(set(z.namelist()) == set(m["head_sources"]), "archive paths")
        for path, meta in m["head_sources"].items():
            b = z.read(path)
            require(len(b) == meta["size"] and sha(b) == meta["sha256"], path + " digest")
            blob = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
            require(blob == meta["blob"], path + " Git blob")
            content[path] = b
    diff = gzip.decompress((ROOT / "UPSTREAM.patch.gz").read_bytes())
    require(sha(diff) == m["diff_sha256"], "uncompressed diff digest")
    owner_path = next(p for p in content if p.startswith("02_REGISTRY/research/"))
    task_path = next(p for p in content if p.startswith("00_WORK/tasks/"))
    for name, meta in m["sections"].items():
        lo, hi = meta["byte_range"]
        b = (ROOT / name).read_bytes()
        require(len(b) == meta["size"] and sha(b) == meta["sha256"], name + " digest")
        require(0 <= lo <= hi <= len(content[owner_path]) and content[owner_path][lo:hi] == b, name + " source range")
    lo, hi = m["task_delta"]["byte_range"]
    task_delta = (ROOT / "task_delta.md").read_bytes()
    require(sha(task_delta) == m["task_delta"]["sha256"] and content[task_path][lo:hi] == task_delta, "task delta")
    replay = ROOT / "replay"
    receipt = json.loads((replay / "receipt.json").read_text(encoding="utf-8"))
    require(receipt["owner_head"] == m["head"], "replay owner pin")
    for item in receipt["results"]:
        name = item["script"]
        code = (replay / name).read_bytes()
        require(sha(code) == item["script_sha256"], name + " checker digest")
        section = (ROOT / item["source_section"]).read_bytes()
        marker = item["source_marker"].encode()
        require(section.count(marker) == 1, name + " checker marker")
        block = re.search(rb"```python\n(.*?)```", section[section.index(marker):], re.S)
        require(block is not None and block.group(1) == code, name + " source checker bytes")
        for mode in ("normal", "optimized"):
            out = (replay / (name + "." + mode + ".stdout")).read_bytes()
            err = (replay / (name + "." + mode + ".stderr")).read_bytes()
            require(sha(out) == item["stdout_sha256"] and not err, name + " replay outputs")
            parsed = json.loads(out)
            count = parsed.get("checks") if isinstance(parsed.get("checks"), int) else parsed.get("number_of_checks")
            require(count == item["checks"], name + " check count")
    listed = [line.split("\t", 1)[0] for line in (ROOT / "COMMITS.tsv").read_text(encoding="utf-8").splitlines()]
    require(listed == m["commits"], "commit list")
    if args.verify_source_objects:
        for path, b in content.items():
            require(git("show", m["head"] + ":" + path) == b, path + " published Git object")
        require(git("diff", "--binary", "--full-index", m["base"], m["head"], "--", *m["head_sources"]) == diff, "Git source diff")
        actual = git("log", "--reverse", "--format=%H", m["base"] + ".." + m["head"]).decode().splitlines()
        require(actual == m["commits"], "Git commit range")
        oldtask = git("show", m["base"] + ":" + task_path)
        require(content[task_path] == oldtask + task_delta, "task delta from base")
    print(json.dumps({"status": "PASS", "source_objects_verified": args.verify_source_objects,
                      "head": m["head"], "commits": len(listed), "sections": len(m["sections"]),
                      "scope": "byte integrity and source provenance only; no scientific replay or acceptance",
                      "GR_closed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
