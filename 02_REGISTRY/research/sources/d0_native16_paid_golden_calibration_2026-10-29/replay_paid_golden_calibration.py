#!/usr/bin/env python3
"""Pin and replay the exact #334 §7dv paid Golden calibration calculation."""
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
CHECKER = HERE / "check_paid_golden_calibration.py"
EXPECTED = HERE / "expected_receipt.json"
FIXTURE = HERE / "inputs" / "upstream_receipts.md"
REPLAY = HERE / "replay"
OWNER_COMMIT = "9e80e0c015a8b8dc804ec55a837eda91164201fe"
OWNER_BRANCH = "exp/a4d-joint-response-continuation-2026-10-16"
OWNER_MEMO_PATH = "02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
OWNER_MEMO_BLOB = "3faa2e9e2682a3a1ba1a466d71b2cc45bd85b30f"
OWNER_MEMO_SHA256 = "78e8ea323698755e69fa5cc171b4828078b4d789bb456ad0564a3e34bd1743cb"
OWNER_MEMO_BYTES = 3786534
OWNER_TASK_PATH = "00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md"
OWNER_TASK_BLOB = "3828c33f45b96729ea67fee849849849276ee07a"
OWNER_TASK_SHA256 = "9006861ef8199d6c757a4f8d1196dcec55973f4ee978b39b21af7d42a37f963a"
OWNER_TASK_BYTES = 1202740
SECTION_START = "## 7dv. A real Golden calibration echo and independent controls in one complete paid execution\n".encode()
SECTION_END = b"<!-- END 7dv PAID NATIVE CALIBRATION RECEIPT -->"
SECTION_SHA256 = "825d3773423d5ac8e19a9ace4d198629301b72f5aac4e15593be66c4c1301d2d"
TASK_START = "### 29 October2026 — real paid Golden test, independent calls and one complete price\n".encode()
TASK_EXCERPT_SHA256 = "68bae27744e1c559041a660526ccf65e9a8574ebcd8f4c5280470c59771547fe"
CHECKER_SHA256 = "fa68fa43fa906c8bc5cf5b2fa2bf766910cae19b5c78bebf32ad94decce4b707"
RECEIPT_SHA256 = "d4d24dc76b92377a21a9b40fa19a8fb90e71c2c8c1c33df4a71077060685ed4e"
INPUT_COMMIT = "f23f9149c470051b35acc3fac42f3fecdba084ab"
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
FROZEN_RECEIPTS = {
    "7ds RETURN RECORD COMPILER RECEIPT": "5ca575b88ade09944cdd6af7b1a013620ed7caa6e9ca2628f1773941d8e9f19e",
    "7du RECORD IMPLEMENTATION FIBRE RECEIPT": "b5c6138e8ae5bd1d7cd23bc8cc9e8831448f6b6900f8ef609a84ae4154cf78b6",
    "7do PAID BINARY INPUT RECEIPT": "811bd6eed0cd74ddc3b505a636f3f80796f0d0fb871aa803d90b5d7e4c5211ba",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def artifact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data)}


def owner_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{OWNER_COMMIT}:{path}"], cwd=ROOT)


def embedded(data: bytes, tag: str, language: str) -> bytes:
    opening = f"<!-- BEGIN {tag} -->\n```{language}\n".encode()
    closing = f"```\n<!-- END {tag} -->".encode()
    return data.split(opening, 1)[1].split(closing, 1)[0]


def check_owner_snapshot() -> tuple[bytes, bytes]:
    memo = owner_bytes(OWNER_MEMO_PATH)
    task = owner_bytes(OWNER_TASK_PATH)
    if len(memo) != OWNER_MEMO_BYTES or sha256(memo) != OWNER_MEMO_SHA256:
        raise AssertionError("owner memo differs from the exact #334 §7dv snapshot")
    if len(task) != OWNER_TASK_BYTES or sha256(task) != OWNER_TASK_SHA256:
        raise AssertionError("owner task differs from the exact #334 §7dv snapshot")
    for path, expected in ((OWNER_MEMO_PATH, OWNER_MEMO_BLOB), (OWNER_TASK_PATH, OWNER_TASK_BLOB)):
        blob = subprocess.check_output(["git", "rev-parse", f"{OWNER_COMMIT}:{path}"], cwd=ROOT, text=True).strip()
        if blob != expected:
            raise AssertionError(f"owner Git blob mismatch: {path}")

    start = memo.index(SECTION_START)
    end = memo.index(SECTION_END, start) + len(SECTION_END)
    if memo[end:end + 1] == b"\n":
        end += 1
    section = memo[start:end]
    if sha256(section) != SECTION_SHA256:
        raise AssertionError("§7dv section differs from its frozen owner bytes")
    if (HERE / "upstream_section_7dv.md").read_bytes() != section:
        raise AssertionError("saved §7dv is not byte-identical to the owner memo")
    task_start = task.index(TASK_START)
    task_excerpt = task[task_start:]
    if sha256(task_excerpt) != TASK_EXCERPT_SHA256:
        raise AssertionError("saved §7dv task excerpt hash mismatch")
    if (HERE / "upstream_task_7dv.md").read_bytes() != task_excerpt:
        raise AssertionError("saved task excerpt is not byte-identical to its owner brief")

    checker = embedded(section, "7dv PAID NATIVE CALIBRATION CHECKER", "python")
    receipt = embedded(section, "7dv PAID NATIVE CALIBRATION RECEIPT", "json")
    if sha256(checker) != CHECKER_SHA256 or CHECKER.read_bytes() != checker:
        raise AssertionError("integrated checker differs from the exact owner block")
    if sha256(receipt) != RECEIPT_SHA256 or EXPECTED.read_bytes() != receipt:
        raise AssertionError("expected receipt differs from the exact owner block")

    fixture = FIXTURE.read_bytes()
    if sha256(fixture) != "ca97beea61912cd3f47c298190010c0a58e9b4eed04a232e89efe304f870e044":
        raise AssertionError("receipt fixture changed")
    for tag, expected in FROZEN_RECEIPTS.items():
        if sha256(embedded(fixture, tag, "json")) != expected:
            raise AssertionError(f"prior receipt is not exact: {tag}")

    for rel, pin in INPUTS.items():
        source = ROOT / rel
        if not source.is_file() or sha256(source.read_bytes()) != pin["sha256"]:
            raise AssertionError(f"local checker input changed: {rel}")
        if owner_bytes(rel) != source.read_bytes():
            raise AssertionError(f"checker input differs from its pinned owner version: {rel}")
        blob = subprocess.check_output(["git", "rev-parse", f"{INPUT_COMMIT}:{rel}"], cwd=ROOT, text=True).strip()
        if blob != pin["blob"]:
            raise AssertionError(f"input Git blob mismatch: {rel}")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", INPUT_COMMIT, OWNER_COMMIT],
        cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    return memo, task


def main() -> None:
    check_owner_snapshot()
    expected = EXPECTED.read_bytes()
    fixture = FIXTURE.read_bytes()
    REPLAY.mkdir(parents=True, exist_ok=True)
    outputs: list[bytes] = []
    stderrs: list[bytes] = []
    runs: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="d0-native16-paid-golden-") as temp:
        scratch = Path(temp)
        paper = scratch / OWNER_MEMO_PATH
        paper.parent.mkdir(parents=True, exist_ok=True)
        paper.write_bytes(fixture)
        for rel in INPUTS:
            target = scratch / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)
        for label, flags in (("ordinary", ()), ("optimized", ("-O",)), ("repeat", ())):
            completed = subprocess.run(
                [sys.executable, *flags, "-B", str(CHECKER)], cwd=scratch,
                capture_output=True, check=False,
            )
            if completed.returncode:
                raise RuntimeError(
                    f"{label} checker exited {completed.returncode}: "
                    f"{completed.stderr.decode('utf-8', errors='replace')}"
                )
            if completed.stderr:
                raise RuntimeError(f"{label} checker wrote to stderr")
            result = json.loads(completed.stdout)
            if result.get("status") != "PASS" or result.get("checks") != 109:
                raise AssertionError(f"{label} returned an unexpected status or check count")
            if result.get("scope", {}).get("GR_closed") is not False:
                raise AssertionError("the source must retain GR_closed=false")
            if sha256(completed.stdout) != RECEIPT_SHA256 or completed.stdout != expected:
                raise AssertionError(f"{label} output differs from the exact #334 receipt")
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
    if not outputs[0] == outputs[1] == outputs[2] == expected or any(stderrs):
        raise AssertionError("ordinary, -O, repeat and owner receipt must match byte-for-byte")

    replay_manifest = {
        "schema": "d0-native16-paid-golden-calibration-replay-v1",
        "status": "PASS",
        "checks": 109,
        "owner_commit": OWNER_COMMIT,
        "owner_branch": OWNER_BRANCH,
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
            "actual_21_call_golden_test": True,
            "actual_59_call_one_book_price": True,
            "test_and_use_control_positions_independent": True,
            "unconstrained_price_selects_correct_recorder": False,
            "physical_X_N_identified": False,
            "Lean_or_CI_run": False,
            "GR_closed": False,
        },
    }
    (HERE / "replay_manifest.json").write_text(json.dumps(replay_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    integrated = {}
    for path in sorted(HERE.rglob("*")):
        if path.is_file() and path.name != "source_manifest.json":
            integrated[path.relative_to(HERE).as_posix()] = artifact(path)
    source_manifest = {
        "schema": "d0-native16-paid-golden-calibration-intake-v1",
        "upstream": {
            "pull_request": 334,
            "branch": OWNER_BRANCH,
            "commit": OWNER_COMMIT,
            "memo_path": OWNER_MEMO_PATH,
            "memo_blob": OWNER_MEMO_BLOB,
            "memo_bytes": OWNER_MEMO_BYTES,
            "memo_sha256": OWNER_MEMO_SHA256,
            "section_sha256": SECTION_SHA256,
            "task_path": OWNER_TASK_PATH,
            "task_blob": OWNER_TASK_BLOB,
            "task_bytes": OWNER_TASK_BYTES,
            "task_sha256": OWNER_TASK_SHA256,
            "task_excerpt_sha256": TASK_EXCERPT_SHA256,
        },
        "checker_inputs": [
            {"path": rel, "commit": INPUT_COMMIT, **pin}
            for rel, pin in INPUTS.items()
        ],
        "frozen_receipts": {
            "fixture_sha256": sha256(fixture),
            "receipt_sha256_by_tag": FROZEN_RECEIPTS,
        },
        "integrated_artifacts": integrated,
        "replay": replay_manifest,
        "scope": {
            "phase": "native realization and complete-price application",
            "parent_substitution": "An exact paid Golden return calibration is implemented in the fixed native16 alphabet and linked to its own independent test/use positions under one original Book price; the unconstrained price argument is shown unable to derive correct recording.",
            "remaining": [
                "derive the native task or continuation law requiring faithful recording and independently binding its later use",
                "identify and admit the physical comparison domain X_N and SourceI availability",
                "retain upstream preparation, clock, boundary and complete original GR transport/refinement obligations",
                "Lean formalization, CI, physical selection and GR closure",
            ],
            "GR_closed": False,
        },
    }
    (HERE / "source_manifest.json").write_text(json.dumps(source_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checks": 109, "owner_commit": OWNER_COMMIT, "receipt_sha256": RECEIPT_SHA256, "replay_manifest": str(HERE / "replay_manifest.json")}, sort_keys=True))


if __name__ == "__main__":
    main()
