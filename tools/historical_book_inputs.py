"""Bind explicitly identified research replays to their historical book inputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

DIRECTORY = "02_REGISTRY/research/sources/d0_editorial_book_inputs_2026-11-25"
MANIFEST = DIRECTORY + "/MANIFEST.json"
MANIFEST_SHA256 = "7a6827e88598946a1c45fc743db38e5bfa013e094192b2a850180536bced2f67"
SOURCE_COMMIT = "2270d3eb238e0c078c7696548ee3968106adf272"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(root: Path, path: str) -> bytes:
    target = root / path
    if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError("Historical book input escapes isolated tree: " + path)
    return target.read_bytes()


class Overlay:
    def __init__(self, entries: list[tuple[Path, bytes, bytes]], provenance: dict):
        self.entries = entries
        self.provenance = provenance

    def restore(self) -> bool:
        mutated = False
        for target, maintained, historical in reversed(self.entries):
            if target.is_symlink() or not target.is_file() or target.read_bytes() != historical:
                mutated = True
            else:
                target.write_bytes(maintained)
        return mutated


def apply(root: Path, entrypoint: str) -> Overlay | None:
    if not (root / MANIFEST).exists():
        return None
    manifest_bytes = read(root, MANIFEST)
    if digest(manifest_bytes) != MANIFEST_SHA256:
        raise ValueError("Historical book manifest hash mismatch")
    data = json.loads(manifest_bytes)
    if data["source_commit"] != SOURCE_COMMIT or data["schema"] != "historical-editorial-book-inputs/1":
        raise ValueError("Unexpected historical book binding")
    expected = data["entrypoints_sha256"].get(entrypoint)
    if expected is None:
        return None
    if digest(read(root, entrypoint)) != expected:
        raise ValueError("Historical book checker hash mismatch: " + entrypoint)
    entries = []
    book_provenance = []
    for target, spec in data["books"].items():
        historical = read(root, spec["snapshot"])
        git_blob = hashlib.sha1(b"blob " + str(len(historical)).encode() + b"\0" + historical).hexdigest()
        if digest(historical) != spec["sha256"] or git_blob != spec["git_blob"]:
            raise ValueError("Historical book snapshot hash mismatch: " + target)
        maintained = read(root, target)
        entries.append((root / target, maintained, historical))
        book_provenance.append({
            "path": target, "historical_sha256": spec["sha256"],
            "historical_git_blob": spec["git_blob"], "maintained_sha256": digest(maintained),
        })
    provenance = {
        "mode": data["scope"], "entrypoint": entrypoint, "checker_sha256": expected,
        "manifest": MANIFEST, "manifest_sha256": MANIFEST_SHA256,
        "source_commit": SOURCE_COMMIT, "books": book_provenance,
    }
    overlay = Overlay(entries, provenance)
    written = []
    try:
        for entry in entries:
            entry[0].write_bytes(entry[2])
            written.append(entry)
    except Exception:
        Overlay(written, provenance).restore()
        raise
    return overlay
