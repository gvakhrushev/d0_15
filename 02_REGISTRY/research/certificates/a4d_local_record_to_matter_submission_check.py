#!/usr/bin/env python3
"""Verify original delivery and all 106 imported bytes; integrity, not physics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
DELIVERY = ROOT / "02_REGISTRY/research/sources/d0_complete_intake_submission_2026-10-14"
PREFIX = "D0_git_intake_v1_v2_v3/"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    manifest = json.loads((DELIVERY / "MANIFEST.json").read_text())
    expected = {item["path"] for item in manifest["files"]}
    actual = {p.name for p in DELIVERY.iterdir() if p.is_file() and p.name != "MANIFEST.json"}
    require(actual == expected, "Original submission file set changed")
    for item in manifest["files"]:
        file = DELIVERY / item["path"]
        require(not file.is_symlink(), "Original submission is a symlink")
        data = file.read_bytes()
        require(len(data) == item["bytes"], "Original submission length changed")
        require(hashlib.sha256(data).hexdigest() == item["sha256"], "Original submission hash changed")

    archive = DELIVERY / "D0_complete_git_intake_v1_v2_v3_2026-10-14.zip"
    with ZipFile(archive) as bundle:
        names = bundle.namelist()
        require(len(names) == len(set(names)), "Duplicate archive paths")
        for name in names:
            path = PurePosixPath(name)
            require(not path.is_absolute() and ".." not in path.parts, "Unsafe archive path")
            require(name.startswith(PREFIX), "Unexpected archive root")
        transfer = json.loads(bundle.read(PREFIX + "TRANSFER.json"))
        patch = bundle.read(PREFIX + "D0_v1_v2_v3_complete_intake.patch")
        require(hashlib.sha256(patch).hexdigest() == transfer["patch_sha256"], "Original patch changed")
        rows = bundle.read(PREFIX + "PACKAGE_SHA256SUMS.txt").decode().splitlines()
        for row in rows:
            digest, relative = row.split("  ", 1)
            require(hashlib.sha256(bundle.read(PREFIX + relative)).hexdigest() == digest,
                    "Internal package checksum changed: " + relative)
        payload = [name for name in names if name.startswith(PREFIX + "payload/") and not name.endswith("/")]
        require(len(payload) == transfer["added_files"] == 106, "Payload file count changed")
        for name in payload:
            relative = name.removeprefix(PREFIX + "payload/")
            file = ROOT / relative
            require(file.is_file() and not file.is_symlink(), "Missing imported file: " + relative)
            require(file.read_bytes() == bundle.read(name), "Imported byte mismatch: " + relative)
        proof = "02_REGISTRY/research/sources/d0_local_record_to_matter_2026-10-14/continuation_v3/proofs/MOVING_PREPARATION_SOURCE_RU.md"
        require((DELIVERY / "MOVING_PREPARATION_SOURCE_RU.md").read_bytes() == (ROOT / proof).read_bytes(),
                "Standalone proof differs from the supplied package")
    print("PASS_ORIGINAL_SUBMISSION 3 original files; 110 internal hashes; 106 imported files")
    print("SCOPE: byte preservation and reproducible intake only; no physical or Lean claim")


if __name__ == "__main__":
    main()
