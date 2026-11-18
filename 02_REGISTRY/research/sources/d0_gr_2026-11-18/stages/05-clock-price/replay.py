"""Check the archive hashes, replay the three main calculations and ten supporting ones."""
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parent
TESTS = {
    "check_master_mark.py": "master_mark_result.json",
    "check_all_leaves.py": "all_leaves_result.json",
    "check_mean_price.py": "mean_price_result.json",
}
ATTACHMENT_TESTS = {
    "check_projective_rigidity.py": "projective_rigidity_controls.json",
    "doob_actual_mark.py": "doob_actual_mark.json",
}


def compare(actual, expected):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and expected.keys() == actual.keys()
                and all(compare(actual[key], value) for key, value in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(compare(x, y) for x, y in zip(actual, expected)))
    if type(expected) is float:
        return type(actual) in (float, int) and math.isclose(
            actual, expected, rel_tol=1e-11, abs_tol=2e-14)
    return type(actual) is type(expected) and actual == expected


def main():
    for filename, saved in json.loads((ROOT / "SHA256SUMS.json").read_text()).items():
        observed = hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
        if observed != saved:
            raise ValueError(f"SHA-256 differs for {filename}")
    env = dict(os.environ, PYTHONPATH="", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    with tempfile.TemporaryDirectory(prefix="d0-book03-") as working_dir:
        work = Path(working_dir)
        bundle = work / "copy"
        shutil.copytree(ROOT, bundle)
        for script, receipt in TESTS.items():
            call = [sys.executable, "-I", "-B", str(bundle / script)]
            output = subprocess.check_output(call, env=env, cwd=work, text=True)
            if not compare(json.loads(output), json.loads((bundle / receipt).read_text())):
                raise ValueError(f"Replayed numbers differ for {script}")
            print("PASS", script, flush=True)
        subprocess.run([sys.executable, "-I", "-B", str(bundle / "proofs/replay.py")],
                       env=env, cwd=work, check=True)
        attachment = work / "original_attachment_checks"
        attachment.mkdir()
        source = json.loads((bundle / "primary/SOURCES.json").read_text())["original_attachment"]
        with zipfile.ZipFile(bundle / "primary" / source["file"]) as archive:
            for script, receipt in ATTACHMENT_TESTS.items():
                (attachment / script).write_bytes(archive.read(script))
                command = [sys.executable, "-I", "-B", str(attachment / script)]
                subprocess.check_output(command, env=env, cwd=attachment, text=True)
                if json.loads((attachment / receipt).read_text()) != json.loads(archive.read(receipt)):
                    raise ValueError(f"Original archive calculation differs for {script}")
                print("PASS", "original/" + script, flush=True)


if __name__ == "__main__":
    main()
