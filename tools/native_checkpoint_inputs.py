"""Historical source and report bindings for the reviewed #322 checkpoint.

The source is restricted to eleven named entrypoints; the report to two of
those entries. Neither binding relaxes checks or removes selected consumers.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re


DIRECTORY = "02_REGISTRY/research/sources/d0_native_variational_checkpoint_2026-10-20"
MANIFEST = DIRECTORY + "/HISTORICAL_INPUT.json"
TARGET = "03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean"
SNAPSHOT = DIRECTORY + "/EndogenousActionQuantum.lean"
SOURCE_HEAD = "64cbac8d17028376ba2e5324da5014ebcfa053b1"
SOURCE_BLOB = "dab5b67300a70768e0211159deb2ac6e53fa7b29"
SOURCE_SHA256 = "692f2b5929b001361a2f22d7dc224fba46a80738036f26a1ff7bdd5175fc80c4"
CERT = "02_REGISTRY/research/certificates/"
NAMES = (
    "a4d_native_addressed_third_role",
    "a4d_native_archive_apparatus_realization",
    "a4d_native_code_price_resolution",
    "a4d_native_dynamical_ownership",
    "a4d_native_history_action",
    "a4d_native_history_field_coupling",
    "a4d_native_prepared_action",
    "a4d_native_scene_payload_action",
    "a4d_native_uniform_memory_actuation",
    "a4d_native_verified_archive_actuation",
    "d0_native_tangent_source_preflight",
)
ENTRYPOINTS = {CERT + name + "_check.py" for name in NAMES}
CAPSULES = {CERT + name + ".lean" for name in NAMES[:-1]}
RECEIPTS = {
    CERT + name + suffix + ".json"
    for name, suffixes in (
        (NAMES[0], ("_certificate", "_results")),
        (NAMES[1], ("_results",)),
        (NAMES[2], ("_certificate", "_results")),
        (NAMES[3], ("_results",)),
        (NAMES[4], ("_results",)),
        (NAMES[5], ("_results",)),
        (NAMES[6], ("_certificate", "_results")),
        ("a4d_native_retained_record_admission", ("_certificate",)),
        (NAMES[7], ("_results",)),
        (NAMES[8], ("_certificate", "_results")),
        (NAMES[9], ("_certificate", "_results")),
        (NAMES[10], ("_certificate",)),
    )
    for suffix in suffixes
}
REPORT_TARGET = "02_REGISTRY/research/APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md"
REPORT_SNAPSHOT = DIRECTORY + "/APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md"
REPORT_BLOB = "dc59c6cdcdd3d2d1d1e4460ec74e456918359abc"
REPORT_SHA256 = "b95d5f631fb9c5936fe61964e73c3f373ea3f9deefb0fae037c7a760d6535ff5"
REPORT_BINDINGS = {
    CERT + name + "_check.py": CERT + name + "_certificate.json"
    for name in ("a4d_native_history_action", "a4d_native_dynamical_ownership")
}
REPORT_ENTRYPOINTS = set(REPORT_BINDINGS)
REPORT_RECEIPTS = set(REPORT_BINDINGS.values())
REPORT_SELECTION_INPUTS = REPORT_RECEIPTS | {REPORT_TARGET, REPORT_SNAPSHOT}
SELECTION_INPUTS = (ENTRYPOINTS | CAPSULES | RECEIPTS | {
    MANIFEST, SNAPSHOT, TARGET, "tools/native_checkpoint_inputs.py",
    "tools/check_native_checkpoint_compatibility.py", "tools/run_research_certs.py",
})


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(root: Path, path: str) -> bytes:
    source = root / path
    if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
        raise ValueError("Historical input path escapes its isolated tree: " + path)
    return source.read_bytes()


def declarations(text: str) -> dict[str, str]:
    """Conservative text compatibility check; actual compilation is separate."""
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    text = re.sub(r"(?m)^@\[[^\]]+\]\s*$", "", text)
    matches = list(re.finditer(r"(?m)^(?:noncomputable )?(?:structure|def|theorem) (\w+)", text))
    result = {}
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = re.split(r"(?m)^end\b", text[match.start():stop], maxsplit=1)[0]
        result[match[1]] = re.sub(r"\s+", " ", block).strip()
    return result


def validate(root: Path) -> tuple[dict, bytes, list[str]]:
    data = json.loads(read(root, MANIFEST))
    required = {
        "schema": "d0-native-checkpoint-historical-input/1",
        "scope": "HISTORICAL_COMPILED_INPUT_REPLAY_NOT_CURRENT_SOURCE_PROOF",
        "source_head": SOURCE_HEAD, "source_blob": SOURCE_BLOB,
        "target_path": TARGET, "snapshot_path": SNAPSHOT,
        "snapshot_sha256": SOURCE_SHA256,
    }
    if any(data.get(key) != value for key, value in required.items()):
        raise ValueError("Unexpected historical input scope, source or path")
    if set(data["entrypoints"]) != ENTRYPOINTS or set(data["receipts"]) != RECEIPTS:
        raise ValueError("Historical binding must retain exactly eleven entries and seventeen receipts")
    if set(data["compatibility_capsules"]) != CAPSULES:
        raise ValueError("Unexpected current compatibility capsule set")
    report = data["report_input"]
    report_required = {
        "scope": "HISTORICAL_REPORT_INPUT_NOT_CURRENT_ROUTE",
        "source_head": SOURCE_HEAD, "source_blob": REPORT_BLOB,
        "target_path": REPORT_TARGET, "snapshot_path": REPORT_SNAPSHOT,
        "snapshot_sha256": REPORT_SHA256, "entrypoints": REPORT_BINDINGS,
    }
    if any(report.get(key) != value for key, value in report_required.items()):
        raise ValueError("Unexpected historical report scope, source, path or entrypoint set")
    if set(report["receipts"]) != REPORT_RECEIPTS:
        raise ValueError("Historical report binding must retain exactly two receipt headers")
    if sha(read(root, REPORT_SNAPSHOT)) != REPORT_SHA256:
        raise ValueError("Historical report snapshot hash mismatch")
    for path, digest in report["receipts"].items():
        receipt = read(root, path)
        if sha(receipt) != digest or json.loads(receipt)["inputs_sha256"].get(REPORT_TARGET) != REPORT_SHA256:
            raise ValueError("Historical report receipt binding mismatch: " + path)
    snapshot = read(root, SNAPSHOT)
    if sha(snapshot) != SOURCE_SHA256:
        raise ValueError("Historical source snapshot hash mismatch")
    for path, digest in {**data["receipts"], **data["compatibility_capsules"]}.items():
        if sha(read(root, path)) != digest:
            raise ValueError("Historical artifact binding mismatch: " + path)
    for entry, binding in data["entrypoints"].items():
        if sha(read(root, entry)) != binding["sha256"]:
            raise ValueError("Historical entrypoint binding mismatch: " + entry)
        prefix = entry.removesuffix("_check.py") + "_"
        expected = sorted(path for path in RECEIPTS if path.startswith(prefix))
        if sorted(binding["receipt_paths"]) != expected:
            raise ValueError("Historical entrypoint receipt binding mismatch: " + entry)
    original = declarations(snapshot.decode("utf-8"))
    maintained = declarations(read(root, TARGET).decode("utf-8"))
    changed = [name for name, body in original.items() if maintained.get(name) != body]
    if changed:
        raise ValueError("Maintained action interface changed; compatibility review required: " + ", ".join(changed))
    return data, snapshot, sorted(original)


@dataclass
class Overlay:
    target: Path
    maintained: bytes
    snapshot: bytes
    provenance: dict
    additional: Overlay | None = None

    def restore(self) -> bool:
        """Restore only an unchanged declared overlay; return mutation status."""
        mutated = self.target.is_symlink() or not self.target.is_file() or self.target.read_bytes() != self.snapshot
        if not mutated:
            self.target.write_bytes(self.maintained)
        if self.additional is not None:
            mutated = self.additional.restore() or mutated
        return mutated


def apply(root: Path, entrypoint: str) -> Overlay | None:
    # Old committed snapshots and every unregistered consumer keep normal replay.
    if entrypoint not in ENTRYPOINTS or not (root / MANIFEST).exists():
        return None
    data, snapshot, preserved = validate(root)
    maintained = read(root, TARGET)
    report_overlay = None
    if entrypoint in REPORT_ENTRYPOINTS:
        report_maintained = read(root, REPORT_TARGET)
        report_snapshot = read(root, REPORT_SNAPSHOT)
        report_provenance = {
            "mode": data["report_input"]["scope"],
            "target_path": REPORT_TARGET, "snapshot_path": REPORT_SNAPSHOT,
            "source_head": SOURCE_HEAD, "source_blob": REPORT_BLOB,
            "historical_sha256": REPORT_SHA256,
            "maintained_sha256": sha(report_maintained),
            "receipt_path": REPORT_BINDINGS[entrypoint],
        }
        report_overlay = Overlay(root / REPORT_TARGET, report_maintained, report_snapshot, report_provenance)
    provenance = {
        "mode": data["scope"], "entrypoint": entrypoint,
        "manifest": MANIFEST, "manifest_sha256": sha(read(root, MANIFEST)),
        "target_path": TARGET, "snapshot_path": SNAPSHOT,
        "source_head": SOURCE_HEAD, "source_blob": SOURCE_BLOB,
        "historical_sha256": SOURCE_SHA256, "maintained_sha256": sha(maintained),
        "original_declarations_preserved": preserved,
        "current_source_compilation": "SEPARATE_REQUIRED_LEAN_COMPATIBILITY_CHECK",
    }
    target = root / TARGET
    if report_overlay is not None:
        provenance["report_input"] = report_overlay.provenance
        report_overlay.target.write_bytes(report_overlay.snapshot)
    target.write_bytes(snapshot)
    return Overlay(target, maintained, snapshot, provenance, report_overlay)
