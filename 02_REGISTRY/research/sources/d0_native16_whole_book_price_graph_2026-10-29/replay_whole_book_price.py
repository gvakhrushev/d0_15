#!/usr/bin/env python3
"""Verify and replay the exact #334 one-sided record price-graph checker."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKER = HERE / "check_one_sided_price.py"
EXPECTED = HERE / "expected_receipt.json"
FIXTURE = HERE / "inputs" / "upstream_receipts.md"
REPLAY = HERE / "replay"
OWNER_COMMIT = "22b4e3f430ddb7d8dd7af6e734f5e63225edd056"
OWNER_BRANCH = "exp/a4d-joint-response-continuation-2026-10-16"
OWNER_MEMO_PATH = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
OWNER_MEMO_BLOB = "1e81dd0151eea362fedacc008293bcf4f0c7d806"
OWNER_MEMO_SHA256 = "2a1bb4ea2cd694605d09293921bed76f8b9fe5fd237d1aa18a6979c989f292bf"
OWNER_TASK_PATH = "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md"
OWNER_TASK_BLOB = "6f34289104bb71b593e53c6440d827e3182a249f"
OWNER_TASK_SHA256 = "8d8cbc92c2d797d2417c0d254886245ecceff58bc1b72b853d04111329250b0f"
SECTION_START = (
    b"## 7dt. One terminal record layer gives a native finite price graph, "
    b"including independently changed preparation\n"
)
SECTION_END = b"<!-- END 7dt ONE SIDED PRICE GRAPH RECEIPT -->"
TASK_START = b"### 29 October: one terminal record layer binds real code alternatives to the literal full Book price\n"
CHECKER_SHA256 = "0b240fde3cef3e433f598a81e68fb6f32995ce77ae736652f7dd43f6ce28e359"
RECEIPT_SHA256 = "b4e52e9d777135388051c2e5908e99a3110816b256be7d5769315a985dffbfe3"
INPUT_COMMIT = "0f2e421fda2029df92b174c39f594160ce31294f"
INPUTS = {
    "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py": {
        "sha256": "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
        "blob": "9a32a3fa2e594c087d24b9d5dec497c4c5e03f44",
    },
    "02_REGISTRY/research/sources/d0_clock_winding_source_2026-10-28/PROOF_RU.md": {
        "sha256": "ff430c80b070d03b2d6860603575b1898394334775177d9d15feb54179fe4418",
        "blob": "1354b8dadd924b0d96639ba402385e9b734787a9",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_exact(path: Path, data: bytes) -> None:
    if path.exists() and path.read_bytes() != data:
        raise FileExistsError(f"refusing to replace different saved evidence: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _artifact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data)}


def _owner_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{OWNER_COMMIT}:{path}"], cwd=ROOT)


def _check_upstream_snapshot() -> tuple[bytes, bytes]:
    memo = _owner_bytes(OWNER_MEMO_PATH)
    task = _owner_bytes(OWNER_TASK_PATH)
    if sha256(memo) != OWNER_MEMO_SHA256:
        raise AssertionError("owner memo bytes differ from the frozen 22b4 pin")
    if sha256(task) != OWNER_TASK_SHA256:
        raise AssertionError("owner task bytes differ from the frozen 22b4 pin")
    memo_blob = subprocess.check_output(
        ["git", "rev-parse", f"{OWNER_COMMIT}:{OWNER_MEMO_PATH}"], cwd=ROOT, text=True
    ).strip()
    task_blob = subprocess.check_output(
        ["git", "rev-parse", f"{OWNER_COMMIT}:{OWNER_TASK_PATH}"], cwd=ROOT, text=True
    ).strip()
    if (memo_blob, task_blob) != (OWNER_MEMO_BLOB, OWNER_TASK_BLOB):
        raise AssertionError("owner memo/task Git blobs do not match the frozen pins")

    start = memo.index(SECTION_START)
    end = memo.index(SECTION_END, start) + len(SECTION_END)
    if memo[end:end + 1] == b"\n":
        end += 1
    section = memo[start:end]
    if (HERE / "upstream_section_7dt.md").read_bytes() != section:
        raise AssertionError("saved §7dt excerpt is not byte-identical to its owner memo")
    task_start = task.index(TASK_START)
    if (HERE / "upstream_task_7dt.md").read_bytes() != task[task_start:]:
        raise AssertionError("saved task excerpt is not byte-identical to its owner brief")

    def embedded(tag: str, language: str) -> bytes:
        opening = f"<!-- BEGIN {tag} -->\n```{language}\n".encode()
        closing = f"```\n<!-- END {tag} -->".encode()
        return section.split(opening, 1)[1].split(closing, 1)[0]

    if (HERE / "check_one_sided_price.py").read_bytes() != embedded(
        "7dt ONE SIDED PRICE GRAPH CHECKER", "python"
    ):
        raise AssertionError("embedded checker differs from the saved upstream excerpt")
    if EXPECTED.read_bytes() != embedded("7dt ONE SIDED PRICE GRAPH RECEIPT", "json"):
        raise AssertionError("embedded receipt differs from the saved upstream excerpt")
    if sha256(EXPECTED.read_bytes()) != RECEIPT_SHA256:
        raise AssertionError("published result receipt hash mismatch")
    if sha256(CHECKER.read_bytes()) != CHECKER_SHA256:
        raise AssertionError("published checker hash mismatch")
    for rel, pin in INPUTS.items():
        source = ROOT / rel
        if not source.is_file() or sha256(source.read_bytes()) != pin["sha256"]:
            raise AssertionError(f"local checker input changed: {rel}")
        published = _owner_bytes(rel)
        if published != source.read_bytes():
            raise AssertionError(f"checker input is not the pinned owner version: {rel}")
        blob = subprocess.check_output(
            ["git", "rev-parse", f"{INPUT_COMMIT}:{rel}"], cwd=ROOT, text=True
        ).strip()
        if blob != pin["blob"]:
            raise AssertionError(f"checker input Git blob mismatch: {rel}")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", INPUT_COMMIT, OWNER_COMMIT],
        cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    return memo, task


def main() -> None:
    _check_upstream_snapshot()
    expected_bytes = EXPECTED.read_bytes()
    fixture_bytes = FIXTURE.read_bytes()
    REPLAY.mkdir(parents=True, exist_ok=True)
    outputs: list[bytes] = []
    stderrs: list[bytes] = []
    runs: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="d0-native16-whole-book-price-") as temp:
        scratch = Path(temp)
        paper_rel = Path(OWNER_MEMO_PATH)
        paper = scratch / paper_rel
        paper.parent.mkdir(parents=True, exist_ok=True)
        paper.write_bytes(fixture_bytes)
        for rel in INPUTS:
            target = scratch / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)

        for label, flags in (("ordinary", ()), ("optimized", ("-O",)), ("repeat", ())):
            completed = subprocess.run(
                [sys.executable, *flags, "-B", str(CHECKER)],
                cwd=scratch,
                capture_output=True,
                check=False,
            )
            if completed.returncode:
                raise RuntimeError(
                    f"{label} checker exited {completed.returncode}: "
                    f"{completed.stderr.decode('utf-8', errors='replace')}"
                )
            if completed.stderr:
                raise RuntimeError(f"{label} checker wrote to stderr")
            result = json.loads(completed.stdout)
            if result.get("status") != "PASS" or result.get("checks") != 93:
                raise AssertionError(f"{label} checker receipt has unexpected status/count")
            if result.get("scope", {}).get("GR_closed") is not False:
                raise AssertionError("the source must retain GR_closed=false")
            if sha256(completed.stdout) != RECEIPT_SHA256:
                raise AssertionError(f"{label} output differs from the published 7dt receipt")
            if completed.stdout != expected_bytes:
                raise AssertionError(f"{label} output bytes differ from the published 7dt receipt")
            stdout_path = REPLAY / f"{label}_stdout.json"
            stderr_path = REPLAY / f"{label}_stderr.log"
            _write_exact(stdout_path, completed.stdout)
            _write_exact(stderr_path, completed.stderr)
            outputs.append(completed.stdout)
            stderrs.append(completed.stderr)
            runs.append({
                "mode": label,
                "command_flags": list(flags),
                "returncode": completed.returncode,
                "stdout_bytes": len(completed.stdout),
                "stdout_sha256": sha256(completed.stdout),
                "stderr_bytes": len(completed.stderr),
                "stderr_sha256": sha256(completed.stderr),
                "status": result["status"],
                "checks": result["checks"],
                "runtime": result.get("runtime"),
            })

    if not outputs[0] == outputs[1] == outputs[2] == expected_bytes:
        raise AssertionError("ordinary, -O, repeat and published receipt differ")
    if any(stderrs):
        raise AssertionError("all three exact checker runs must leave stderr empty")

    replay_manifest = {
        "schema": "d0-native16-whole-book-price-graph-replay-v1",
        "status": "PASS",
        "checks": 93,
        "checker_sha256": CHECKER_SHA256,
        "published_receipt_sha256": RECEIPT_SHA256,
        "exact_published_receipt_match": True,
        "outputs_byte_identical_across_modes": True,
        "stderr_empty_for_all_runs": True,
        "runtime": {
            "python": sys.version.split()[0],
            "sympy": importlib.metadata.version("sympy"),
            "mpmath": importlib.metadata.version("mpmath"),
        },
        "runs": runs,
        "scope": {
            "one_terminal_record_layer": True,
            "complete_literal_Book_H_plus_J": True,
            "full_physical_X_N_identified": False,
            "finite_stationary_root_proved": False,
            "Lean_or_CI_run": False,
            "physical_selection_proved": False,
            "GR_closed": False,
        },
    }
    replay_bytes = (json.dumps(replay_manifest, indent=2, sort_keys=True) + "\n").encode()
    (HERE / "replay_manifest.json").write_bytes(replay_bytes)

    paths = [
        "PROOF_RU.md", "upstream_section_7dt.md", "upstream_task_7dt.md",
        "check_one_sided_price.py", "expected_receipt.json", "inputs/upstream_receipts.md",
        "replay_whole_book_price.py", "replay_manifest.json",
        *(f"replay/{mode}_{suffix}" for mode in ("ordinary", "optimized", "repeat")
          for suffix in ("stdout.json", "stderr.log")),
    ]
    source_manifest = {
        "schema": "d0-native16-whole-book-price-graph-intake-v1",
        "upstream": {
            "pull_request": 334,
            "branch": OWNER_BRANCH,
            "commit": OWNER_COMMIT,
            "memo_path": OWNER_MEMO_PATH,
            "memo_blob": OWNER_MEMO_BLOB,
            "memo_sha256": OWNER_MEMO_SHA256,
            "memo_bytes": 3712032,
            "task_path": OWNER_TASK_PATH,
            "task_blob": OWNER_TASK_BLOB,
            "task_sha256": OWNER_TASK_SHA256,
            "task_bytes": 1191147,
            "checker_sha256": CHECKER_SHA256,
            "receipt_sha256": RECEIPT_SHA256,
        },
        "checker_inputs": [
            {"path": path, "commit": INPUT_COMMIT, "blob": pin["blob"], "sha256": pin["sha256"]}
            for path, pin in INPUTS.items()
        ],
        "frozen_receipt_inputs": {
            "7ds_return_record_compiler_sha256": "5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e",
            "7do_paid_binary_input_sha256": "811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba",
            "fixture_sha256": sha256(fixture_bytes),
        },
        "integrated_artifacts": {rel: _artifact(HERE / rel) for rel in paths},
        "replay": {
            "manifest": "replay_manifest.json",
            "status": replay_manifest["status"],
            "exact_published_receipt_match": True,
            "GR_closed": False,
        },
        "scope": {
            "phase": "native realization and finite price-graph application",
            "parent_substitution": (
                "For the declared fixed-layout native graph, a single paid terminal record "
                "copy yields exact saturation for every complete original word and its "
                "independent preparation changes; the literal Book H+J price is evaluated "
                "including the positive-gap term and true clock heat."
            ),
            "remaining": [
                "physical admission of the fixed record/reserve layout and initial boundary",
                "identify the actual full physical comparison domain X_N",
                "selected native task/record/Cost-Info and independent clock/boundary equations",
                "large field compiler reserve/width/refinement admission",
                "Lean formalization and CI",
                "physical selection, stationary finite word and GR closure",
            ],
            "GR_closed": False,
        },
    }
    source_bytes = (json.dumps(source_manifest, indent=2, sort_keys=True) + "\n").encode()
    (HERE / "source_manifest.json").write_bytes(source_bytes)
    print(replay_bytes.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
