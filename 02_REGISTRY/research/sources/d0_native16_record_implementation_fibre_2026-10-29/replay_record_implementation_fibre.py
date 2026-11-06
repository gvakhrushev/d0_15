#!/usr/bin/env python3
"""Verify and replay the exact #334 universal recording-fibre checker."""
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
CHECKER = HERE / "check_record_implementation_fibre.py"
EXPECTED = HERE / "expected_receipt.json"
FIXTURE = HERE / "inputs" / "upstream_receipts.md"
REPLAY = HERE / "replay"
OWNER_COMMIT = "f23f9149c470051b35acc3fac42f3fecdba084ab"
OWNER_BRANCH = "exp/a4d-joint-response-continuation-2026-10-16"
OWNER_MEMO_PATH = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
OWNER_MEMO_BLOB = "21e07fc00279bd897baeefceba8317b1e898107a"
OWNER_MEMO_SHA256 = "ffbaf16b13db8190573db5a8063ce9c53de76698b9e5527693681286d4195c10"
OWNER_MEMO_BYTES = 3747121
OWNER_TASK_PATH = "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md"
OWNER_TASK_BLOB = "8c5b36bbd6fe88ddbb700904204228d1985ca7c1"
OWNER_TASK_SHA256 = "1229452299a859167e15f5d6ed6620bd8c5e1c618c69fbe03705d6a5db4c14a0"
OWNER_TASK_BYTES = 1197383
SECTION_START = b"## 7du. Admit implementations by their full recording map, without fixing the field's output law\n"
SECTION_END = b"<!-- END 7du RECORD IMPLEMENTATION FIBRE RECEIPT -->"
TASK_START = b"### 29 October: a complete recording specification fixes the new control domain without fixing the field response\n"
CHECKER_SHA256 = "66a8f56d93358668c39f357c71c47fed4ad6075c1c40c39b7602adb971b3dc6f"
CHECKER_BODY_SHA256 = "9f99f3e931a080138d1780f4fce48fa4dd6fd7fac70702ef0b32454537369de2"
RECEIPT_SHA256 = "b5c6138e8ae5bd1d7cd23bc8cc9e8831448f6b6900f8ef609a84ae4154cf78b6"
RECEIPT_BODY_SHA256 = "ab58ba5ce72e04eedcda6cade82588d3f2c8a7a876ce91c68f6027ce3769e9fb"
SECTION_SHA256 = "169088d3c4918f1a306cb7ac213b3d4929216f5615c819b53364afd9eadc1627"
TASK_EXCERPT_SHA256 = "cdd1c15bf77d1fa5347517a1491b3818d9bd93d32aac03ae6bef2bd77625de73"
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


def _artifact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data)}


def _owner_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{OWNER_COMMIT}:{path}"], cwd=ROOT)


def _embedded(section: bytes, tag: str, language: str) -> bytes:
    opening = f"<!-- BEGIN {tag} -->\n```{language}\n".encode()
    closing = f"```\n<!-- END {tag} -->".encode()
    return section.split(opening, 1)[1].split(closing, 1)[0]


def _check_upstream_snapshot() -> tuple[bytes, bytes]:
    memo = _owner_bytes(OWNER_MEMO_PATH)
    task = _owner_bytes(OWNER_TASK_PATH)
    if len(memo) != OWNER_MEMO_BYTES or sha256(memo) != OWNER_MEMO_SHA256:
        raise AssertionError("owner memo differs from the frozen #334 f23f914 pin")
    if len(task) != OWNER_TASK_BYTES or sha256(task) != OWNER_TASK_SHA256:
        raise AssertionError("owner task differs from the frozen #334 f23f914 pin")
    for path, expected in ((OWNER_MEMO_PATH, OWNER_MEMO_BLOB), (OWNER_TASK_PATH, OWNER_TASK_BLOB)):
        blob = subprocess.check_output(
            ["git", "rev-parse", f"{OWNER_COMMIT}:{path}"], cwd=ROOT, text=True
        ).strip()
        if blob != expected:
            raise AssertionError(f"owner Git blob mismatch: {path}")

    start = memo.index(SECTION_START)
    end = memo.index(SECTION_END, start) + len(SECTION_END)
    if memo[end:end + 1] == b"\n":
        end += 1
    section = memo[start:end]
    if sha256(section) != SECTION_SHA256:
        raise AssertionError("§7du excerpt hash differs from the frozen owner section")
    if (HERE / "upstream_section_7du.md").read_bytes() != section:
        raise AssertionError("saved §7du excerpt is not byte-identical to its owner memo")
    task_start = task.index(TASK_START)
    task_excerpt = task[task_start:]
    if sha256(task_excerpt) != TASK_EXCERPT_SHA256:
        raise AssertionError("saved §7du task excerpt hash mismatch")
    if (HERE / "upstream_task_7du.md").read_bytes() != task_excerpt:
        raise AssertionError("saved task excerpt is not byte-identical to its owner brief")

    checker_body = _embedded(section, "7du RECORD IMPLEMENTATION FIBRE CHECKER", "python")
    receipt_body = _embedded(section, "7du RECORD IMPLEMENTATION FIBRE RECEIPT", "json")
    if sha256(checker_body) != CHECKER_SHA256 or sha256(checker_body[:-1]) != CHECKER_BODY_SHA256:
        raise AssertionError("embedded checker body hash mismatch")
    if sha256(receipt_body) != RECEIPT_SHA256 or sha256(receipt_body[:-1]) != RECEIPT_BODY_SHA256:
        raise AssertionError("embedded receipt body hash mismatch")
    if (HERE / "check_record_implementation_fibre.py").read_bytes() != checker_body:
        raise AssertionError("integrated checker differs from exact owner checker body")
    if EXPECTED.read_bytes() != receipt_body:
        raise AssertionError("expected receipt differs from exact owner receipt bytes")
    if sha256(CHECKER.read_bytes()) != CHECKER_SHA256:
        raise AssertionError("integrated checker SHA-256 mismatch")
    if sha256(EXPECTED.read_bytes()) != RECEIPT_SHA256:
        raise AssertionError("published receipt SHA-256 mismatch")

    fixture = FIXTURE.read_bytes()
    for tag, expected in (
        ("7ds RETURN RECORD COMPILER RECEIPT", "5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e"),
        ("7dt ONE SIDED PRICE GRAPH RECEIPT", "b4e52e9d777135388051c2e5908e99a3110816b256be7d5769315a985dffbfe3"),
        ("7do PAID BINARY INPUT RECEIPT", "811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba"),
    ):
        block = _embedded(fixture, tag, "json")
        if sha256(block) != expected:
            raise AssertionError(f"frozen supporting receipt hash mismatch: {tag}")

    for rel, pin in INPUTS.items():
        source = ROOT / rel
        if not source.is_file() or sha256(source.read_bytes()) != pin["sha256"]:
            raise AssertionError(f"local checker input changed: {rel}")
        if _owner_bytes(rel) != source.read_bytes():
            raise AssertionError(f"checker input differs from frozen owner version: {rel}")
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
    memo, task = _check_upstream_snapshot()
    expected_bytes = EXPECTED.read_bytes()
    fixture_bytes = FIXTURE.read_bytes()
    REPLAY.mkdir(parents=True, exist_ok=True)
    outputs: list[bytes] = []
    stderrs: list[bytes] = []
    runs: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="d0-native16-record-fibre-") as temp:
        scratch = Path(temp)
        paper = scratch / OWNER_MEMO_PATH
        paper.parent.mkdir(parents=True, exist_ok=True)
        paper.write_bytes(fixture_bytes)
        for rel in INPUTS:
            target = scratch / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)

        for label, flags in (("ordinary", ()), ("optimized", ("-O",)), ("repeat", ())):
            completed = subprocess.run(
                [sys.executable, *flags, "-B", str(CHECKER)],
                cwd=scratch, capture_output=True, check=False,
            )
            if completed.returncode:
                raise RuntimeError(
                    f"{label} checker exited {completed.returncode}: "
                    f"{completed.stderr.decode('utf-8', errors='replace')}"
                )
            if completed.stderr:
                raise RuntimeError(f"{label} checker wrote to stderr")
            result = json.loads(completed.stdout)
            if result.get("status") != "PASS" or result.get("checks") != 104:
                raise AssertionError(f"{label} checker receipt has unexpected status/count")
            if result.get("scope", {}).get("GR_closed") is not False:
                raise AssertionError("the source must retain GR_closed=false")
            if sha256(completed.stdout) != RECEIPT_SHA256 or completed.stdout != expected_bytes:
                raise AssertionError(f"{label} output differs from the exact owner receipt")
            (REPLAY / f"{label}_stdout.json").write_bytes(completed.stdout)
            (REPLAY / f"{label}_stderr.log").write_bytes(completed.stderr)
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
        raise AssertionError("ordinary, -O, repeat and owner receipt differ")
    if any(stderrs):
        raise AssertionError("all three exact checker runs must leave stderr empty")

    replay_manifest = {
        "schema": "d0-native16-record-implementation-fibre-replay-v1",
        "status": "PASS",
        "checks": 104,
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
            "all_ready_input_record_map_calibration": True,
            "full_unprepared_operator_completion_freedom": True,
            "complete_literal_Book_price": True,
            "full_physical_X_N_identified": False,
            "physical_record_instrument_selected": False,
            "Lean_or_CI_run": False,
            "physical_selection_proved": False,
            "GR_closed": False,
        },
    }
    (HERE / "replay_manifest.json").write_text(
        json.dumps(replay_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    paths = [
        "PROOF_RU.md", "upstream_section_7du.md", "upstream_task_7du.md",
        "check_record_implementation_fibre.py", "expected_receipt.json",
        "inputs/upstream_receipts.md", "replay_record_implementation_fibre.py",
        "replay_manifest.json",
        *(f"replay/{mode}_{suffix}" for mode in ("ordinary", "optimized", "repeat")
          for suffix in ("stdout.json", "stderr.log")),
    ]
    fixture_hashes = {
        "7ds_return_record_compiler_sha256": "5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e",
        "7dt_one_sided_price_graph_sha256": "b4e52e9d777135388051c2e5908e99a3110816b256be7d5769315a985dffbfe3",
        "7do_paid_binary_input_sha256": "811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba",
        "fixture_sha256": sha256(fixture_bytes),
    }
    source_manifest = {
        "schema": "d0-native16-record-implementation-fibre-intake-v1",
        "upstream": {
            "pull_request": 334,
            "branch": OWNER_BRANCH,
            "commit": OWNER_COMMIT,
            "memo_path": OWNER_MEMO_PATH,
            "memo_blob": OWNER_MEMO_BLOB,
            "memo_sha256": OWNER_MEMO_SHA256,
            "memo_bytes": OWNER_MEMO_BYTES,
            "task_path": OWNER_TASK_PATH,
            "task_blob": OWNER_TASK_BLOB,
            "task_sha256": OWNER_TASK_SHA256,
            "task_bytes": OWNER_TASK_BYTES,
            "section_sha256": SECTION_SHA256,
            "task_excerpt_sha256": TASK_EXCERPT_SHA256,
            "checker_body_sha256": CHECKER_BODY_SHA256,
            "checker_sha256": CHECKER_SHA256,
            "receipt_body_sha256": RECEIPT_BODY_SHA256,
            "receipt_sha256": RECEIPT_SHA256,
        },
        "checker_inputs": [
            {"path": path, "commit": INPUT_COMMIT, "blob": pin["blob"], "sha256": pin["sha256"]}
            for path, pin in INPUTS.items()
        ],
        "frozen_receipt_inputs": fixture_hashes,
        "integrated_artifacts": {rel: _artifact(HERE / rel) for rel in paths},
        "replay": {
            "manifest": "replay_manifest.json",
            "status": replay_manifest["status"],
            "exact_published_receipt_match": True,
            "GR_closed": False,
        },
        "scope": {
            "phase": "native realization and same-operation recorder application",
            "parent_substitution": (
                "For the declared native16 fixed-layout recorder, complete-map equality "
                "D j = C j classifies the same recording operation, including post-state; "
                "the admitted completion fibre has zero feedback derivative while retaining "
                "the complete heat and unchanged horizontal field source."
            ),
            "remaining": [
                "physical admission of the specified recorder and reserve layout",
                "identify the actual full physical comparison domain X_N",
                "bind the finite recorder predicate to the selected physical Book/task",
                "derive the selected Cost-Info and independent clock/boundary equations",
                "larger field/compiler/refinement admission",
                "Lean formalization and CI",
                "physical selection and GR closure",
            ],
            "GR_closed": False,
        },
    }
    (HERE / "source_manifest.json").write_text(
        json.dumps(source_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(replay_manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
