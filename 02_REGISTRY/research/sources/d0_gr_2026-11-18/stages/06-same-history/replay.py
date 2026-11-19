"""Verify all files, replay the new checks and repeat the attachment's symbolic controls."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parent


def close_json(actual, expected):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys()==expected.keys()
                and all(close_json(actual[k],v) for k,v in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual)==len(expected)
                and all(close_json(x,y) for x,y in zip(actual,expected)))
    if type(expected) is float:
        return type(actual) in (int,float) and math.isclose(
            actual, expected, rel_tol=3e-12, abs_tol=2e-14)
    return type(actual) is type(expected) and actual==expected


def main():
    for name, wanted in json.loads((ROOT/"SHA256SUMS.json").read_text()).items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=wanted:
            raise ValueError(f"Fingerprint differs: {name}")
    settings=json.loads((ROOT/"CHECKS.json").read_text())
    with tempfile.TemporaryDirectory(prefix="d0-same-history-") as tmp:
        work=Path(tmp)
        bundle=work/"source"
        shutil.copytree(ROOT,bundle)
        env=dict(os.environ, PYTHONPATH="", OPENBLAS_NUM_THREADS="1",
                 OMP_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONOPTIMIZE="")
        def run(pair):
            name,receipt=pair
            command=[sys.executable,"-I","-B",str(bundle/name)]
            actual=json.loads(subprocess.check_output(command,cwd=work,env=env,text=True))
            expected=json.loads((bundle/receipt).read_text())
            if not close_json(actual,expected):
                raise ValueError(f"Calculation differs: {name}")
            print("PASS",name,flush=True)
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(run,settings["checks"].items()))
        original=work/"user_attachment"
        original.mkdir()
        with zipfile.ZipFile(bundle/"frozen"/settings["attachment"]) as archive:
            for name,receipt in settings["attachment_checks"].items():
                (original/name).write_bytes(archive.read(name))
                subprocess.check_output([sys.executable,"-I","-B",str(original/name)],
                                        env=env,cwd=original,text=True)
                if json.loads((original/receipt).read_text())!=json.loads(archive.read(receipt)):
                    raise ValueError(f"Attachment control differs: {name}")
                print("PASS","attachment/"+name,flush=True)


if __name__=="__main__":
    main()
