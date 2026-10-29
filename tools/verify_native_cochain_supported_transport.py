#!/usr/bin/env python3
"""Check definitional transport from the pinned research capsule to D0 owners."""

from __future__ import annotations

import hashlib
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

if __package__:
    from . import lean_task_build
else:
    import lean_task_build


REPO_ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION_ROOT = REPO_ROOT / "03_FORMALIZATION"
CAPSULE = (
    REPO_ROOT
    / "02_REGISTRY/research/certificates/a4d_native_cochain_refinement.lean"
)
CAPSULE_SHA256 = "c07153c478ab7ebafd361107d848a45be47650d93fceaad2c5c67bd052f96515"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AXIOM_REPORT = re.compile(
    r"^'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
    re.MULTILINE,
)

PREFIX = "import D0.Geometry.Archive1DCochainRefinementBinding\n".encode("utf-8")
SUFFIX = """

namespace D0.Research.NativeCochainRefinement

theorem supported_b0_transport (m : ℕ) (f : Fin (m + 1) → ℝ) :
    B0 m f = D0.Geometry.archiveCochainB0 m f := rfl

theorem supported_b1_transport (m : ℕ) (f : Fin (m + 1) → ℝ) :
    B1 m f = D0.Geometry.archiveCochainB1 m f := rfl

theorem supported_incidence_transport (m : ℕ) (f : Fin (m + 1) → ℝ) :
    incidence m f = D0.Geometry.archiveCycleIncidence m f := rfl

theorem supported_scale_ratio_transport (m : ℕ) :
    scaleRatio m = D0.Geometry.archiveCochainScaleRatio m := rfl

#print axioms supported_b0_transport
#print axioms supported_b1_transport
#print axioms supported_incidence_transport
#print axioms supported_scale_ratio_transport
#print axioms D0.Geometry.archive_b1_matrix_gram
#print axioms D0.Geometry.archive_b0_matrix_gram
#print axioms D0.Geometry.intertwining_d_b0_eq_b1_d
#print axioms D0.Geometry.archive_b0_literal_matrix
#print axioms D0.Geometry.archive_lift_operator_gram
#print axioms D0.Geometry.archive_scaled_block_with_owner_scale
#print axioms D0.Geometry.archive_unscaled_chain_fails_owner_scales

end D0.Research.NativeCochainRefinement
""".encode("utf-8")


def read_pinned_capsule(stage: str) -> bytes:
    capsule_bytes = CAPSULE.read_bytes()
    digest = hashlib.sha256(capsule_bytes).hexdigest()
    print(f"capsule_sha256_{stage}={digest}", flush=True)
    if digest != CAPSULE_SHA256:
        raise RuntimeError(f"capsule changed at {stage}; expected {CAPSULE_SHA256}")
    return capsule_bytes


def run_command(command: list[str], stage: str) -> subprocess.CompletedProcess[str]:
    print(f"command={shlex.join(command)} (cwd={FORMALIZATION_ROOT})", flush=True)
    result = subprocess.run(
        command,
        cwd=FORMALIZATION_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    print(f"{stage}_exit={result.returncode}", flush=True)
    return result


def show_failure(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, file=sys.stderr, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")


def audit_axioms(source: bytes, output: str, stderr: str) -> None:
    if any(token in output or token in stderr for token in ("sorryAx", "Lean.trustCompiler")):
        raise RuntimeError("Lean output contains an unaccepted proof dependency")
    requests = re.findall(r"^#print axioms ([A-Za-z0-9_.]+)\s*$", source.decode("utf-8"), re.MULTILINE)
    reports = AXIOM_REPORT.findall(output)
    if len(requests) != len(reports):
        raise RuntimeError(f"expected {len(requests)} axiom reports, got {len(reports)}")
    for requested, (actual, body) in zip(requests, reports):
        if actual != requested and not actual.endswith("." + requested):
            raise RuntimeError(f"unexpected axiom report: {actual} for {requested}")
        dependencies = {item.strip() for item in body.split(",") if item.strip()}
        if not dependencies <= STANDARD_AXIOMS:
            raise RuntimeError(f"nonstandard axioms for {actual}: {sorted(dependencies)}")


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="d0_cochain_transport_") as temp_dir:
            temp_path = Path(temp_dir).resolve()
            if temp_path == REPO_ROOT or REPO_ROOT in temp_path.parents:
                raise RuntimeError("temporary directory is inside the repository")
            combined = temp_path / "NativeCochainSupportedTransport.lean"
            with lean_task_build.build_lock(lean_task_build.LOCK):
                with lean_task_build.materialize_windows_lean_symlinks():
                    before_build = lean_task_build.source_digest()
                    print(f"source_digest_before_build={before_build}", flush=True)
                    capsule_bytes = read_pinned_capsule("before_build")
                    combined.write_bytes(PREFIX + capsule_bytes + SUFFIX)

                    build = run_command(
                        ["lake", "build", "D0.Geometry.Archive1DCochainRefinementBinding"],
                        "build",
                    )
                    after_build = lean_task_build.source_digest()
                    print(f"source_digest_after_build={after_build}", flush=True)
                    read_pinned_capsule("after_build")
                    if before_build != after_build:
                        raise RuntimeError("Lean sources changed during the binding build")
                    if build.returncode:
                        show_failure(build)
                        return build.returncode

                    query = run_command(["lake", "env", "lean", str(combined)], "query")
                    after_query = lean_task_build.source_digest()
                    print(f"source_digest_after_query={after_query}", flush=True)
                    read_pinned_capsule("after_query")
                    if after_build != after_query:
                        raise RuntimeError("Lean sources changed during the compatibility query")
                    if query.returncode:
                        show_failure(query)
                        return query.returncode

                    audit_axioms(capsule_bytes + SUFFIX, query.stdout, query.stderr)
                    print("axiom_output:")
                    print(query.stdout, end="")
                    if query.stderr:
                        print(query.stderr, file=sys.stderr, end="")
                    print("result=PASS")
                    return 0
    except lean_task_build.BuildLockBusy:
        print("FAIL D0 Lean build/cache is busy; retry after it finishes", file=sys.stderr)
        return 1
    except (OSError, RuntimeError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
