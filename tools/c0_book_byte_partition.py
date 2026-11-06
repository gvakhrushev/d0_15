#!/usr/bin/env python3
"""Generate unresolved byte-partition candidates for pinned BOOK_* sources.

The output is a reproducible review view, not a list of mathematical units,
an acceptance decision, a C0 freeze, or a scientific status registry. Only
tracked Git objects at the explicitly selected commit are read. The parser
recognizes ATX headings outside fenced code; it is not a full Markdown parser.
Every byte, including preambles and fence lines, remains in exactly one span.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


EXPECTED_BOOKS = (
    "BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md",
    "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
    "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
    "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
    "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
    "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
    "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
    "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
    "BOOK_09_GRAVITATIONAL_WAVES_AND_QUANTUM_INTERFEROMETRY.md",
)
_OID = re.compile(r"[0-9a-f]{40}\Z")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*)|[ \t]*)$")


class EvidenceError(Exception):
    """The requested immutable evidence could not be safely read."""


def _git_env() -> dict[str, str]:
    # In particular, never inherit GIT_DIR, GIT_WORK_TREE, alternates, index,
    # replace-ref bases or command-line Git config injection from the caller.
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
    env.update(GIT_NO_LAZY_FETCH="1", GIT_NO_REPLACE_OBJECTS="1",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT="0")
    return env


def _git(repo: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(["git", "-C", str(repo), *args], env=_git_env(),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=30, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise EvidenceError("git unavailable or timed out") from exc
    if result.returncode:
        raise EvidenceError("git command failed: " + args[0])
    return result.stdout


def _require_repo_root(repo: Path) -> None:
    try:
        top = Path(os.fsdecode(_git(repo, "rev-parse", "--show-toplevel")).strip()).resolve()
    except (ValueError, OSError) as exc:
        raise EvidenceError("invalid worktree root") from exc
    if top != repo.resolve():
        raise EvidenceError("repository path is not the worktree root")
    if _git(repo, "rev-parse", "--show-object-format").strip() != b"sha1":
        raise EvidenceError("only SHA-1 Git repositories are supported")


def _object(repo: Path, oid: str, kind: str) -> bytes:
    if not _OID.fullmatch(oid):
        raise EvidenceError("object id must be a full lowercase SHA-1")
    if _git(repo, "cat-file", "-t", oid).strip() != kind.encode("ascii"):
        raise EvidenceError("Git object type mismatch")
    data = _git(repo, "cat-file", kind, oid)
    actual = hashlib.sha1(f"{kind} {len(data)}\0".encode("ascii") + data).hexdigest()
    if actual != oid:
        raise EvidenceError("Git object bytes do not match object id")
    return data


def _tree_entries(raw: bytes) -> list[tuple[str, bytes, str]]:
    entries: list[tuple[str, bytes, str]] = []
    pos = 0
    while pos < len(raw):
        space = raw.find(b" ", pos)
        nul = raw.find(b"\0", space + 1) if space >= 0 else -1
        if space < 0 or nul < 0 or nul + 21 > len(raw):
            raise EvidenceError("malformed raw tree")
        try:
            mode = raw[pos:space].decode("ascii")
        except UnicodeError as exc:
            raise EvidenceError("invalid tree mode") from exc
        name = raw[space + 1:nul]
        if not name or b"/" in name or name in (b".", b".."):
            raise EvidenceError("invalid tree name")
        entries.append((mode, name, raw[nul + 1:nul + 21].hex()))
        pos = nul + 21
    names = [row[1] for row in entries]
    if len(names) != len(set(names)):
        raise EvidenceError("duplicate tree entry")
    return entries


def _commit_root_tree(repo: Path, commit: str) -> str:
    data = _object(repo, commit, "commit")
    first = data.split(b"\n", 1)[0]
    if not re.fullmatch(rb"tree [0-9a-f]{40}", first):
        raise EvidenceError("invalid commit root tree")
    return first[5:].decode("ascii")


def _book_entries(repo: Path, commit: str) -> list[tuple[str, str]]:
    root_tree = _tree_entries(_object(repo, _commit_root_tree(repo, commit), "tree"))
    selected = [row for row in root_tree if row[1] == b"01_BOOKS"]
    if len(selected) != 1 or selected[0][0] not in ("40000", "040000"):
        raise EvidenceError("tracked 01_BOOKS tree is unavailable")
    directory = _tree_entries(_object(repo, selected[0][2], "tree"))
    books: list[tuple[str, str]] = []
    for mode, name, oid in directory:
        if name.upper().startswith(b"BOOK_") and name.lower().endswith(b".md"):
            if mode not in ("100644", "100755"):
                raise EvidenceError("book candidate is not a regular tracked file")
            try:
                decoded = name.decode("utf-8")
            except UnicodeError as exc:
                raise EvidenceError("book filename is not UTF-8") from exc
            books.append((decoded, oid))
    return sorted(books)


def _fence_transition(line: str, fence: tuple[str, int] | None) -> tuple[tuple[str, int] | None, bool]:
    match = _FENCE.fullmatch(line)
    if not match:
        return fence, False
    marker, tail = match.groups()
    if fence is None:
        if marker[0] == "`" and "`" in tail:
            return None, False
        return (marker[0], len(marker)), True
    if marker[0] == fence[0] and len(marker) >= fence[1] and not tail.strip():
        return None, True
    return fence, True


def partition(data: bytes, commit: str, path: str) -> list[dict[str, Any]]:
    """Split exact UTF-8 bytes at heading starts; never infer mathematical units."""
    try:
        data.decode("utf-8")
    except UnicodeError as exc:
        raise EvidenceError("book bytes are not UTF-8") from exc
    starts: list[tuple[int, int, str, int]] = []
    offset = 0
    fence: tuple[str, int] | None = None
    for line_no, raw_line in enumerate(data.splitlines(keepends=True), 1):
        line = raw_line.decode("utf-8").rstrip("\r\n")
        if offset == 0:
            line = line.removeprefix("\ufeff")
        fence, fence_line = _fence_transition(line, fence)
        if fence is None and not fence_line:
            heading = _HEADING.fullmatch(line)
            if heading:
                title = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(2) or "").strip()
                starts.append((offset, len(heading.group(1)), title, line_no))
        offset += len(raw_line)
    # Always include the preamble, even when its byte range is empty.
    specs: list[tuple[int, int, dict[str, Any]]] = []
    first = starts[0][0] if starts else len(data)
    specs.append((0, first, {"kind": "preamble"}))
    for index, (start, level, title, line_no) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(data)
        specs.append((start, end, {"kind": "heading_section", "heading_level": level,
                                   "heading_text": title, "heading_line": line_no}))
    pieces = [data[start:end] for start, end, _ in specs]
    if b"".join(pieces) != data or any(a > b for a, b, _ in specs):
        raise EvidenceError("byte partition failed reconstruction")
    return [{**metadata, "byte_start": start, "byte_end_exclusive": end,
             "source_key": f"source:{commit}:{path}#bytes={start}:{end}",
             "span_sha256": hashlib.sha256(data[start:end]).hexdigest(),
             "disposition": "unresolved", "mathematical_units": "not_assessed"}
            for start, end, metadata in specs]


def capture(repo: Path, snapshot: str, expected: tuple[str, ...] = EXPECTED_BOOKS) -> dict[str, Any]:
    repo = Path(repo).resolve()
    if not _OID.fullmatch(snapshot):
        raise EvidenceError("snapshot must be a full lowercase commit SHA-1")
    _require_repo_root(repo)
    books = _book_entries(repo, snapshot)
    names = {name for name, _ in books}
    expected_set = set(expected)
    sources = []
    for name, blob in books:
        data = _object(repo, blob, "blob")
        path = "01_BOOKS/" + name
        spans = partition(data, snapshot, path)
        sources.append({"path": path, "blob": blob, "byte_length": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "reconstruction": "verified_from_exact_byte_spans",
                        "spans": spans})
    return {
        "schema": "d0-c0-book-byte-partition-prototype-v1",
        "snapshot_commit": snapshot,
        "capture_status": "expected_book_blob_bytes_reconstructed" if names == expected_set else "unresolved_book_set",
        "missing_expected_books": sorted(expected_set - names),
        "unexpected_book_candidates": sorted(names - expected_set),
        "sources": sources,
        "scope": ("Tracked BOOK_*.md candidates under 01_BOOKS only. Headings use a lexical "
                  "ATX/top-level fence scan, not full Markdown or mathematical parsing; nested "
                  "fences, HTML, math blocks and unclosed fences may alter candidate boundaries. "
                  "Byte reconstruction does not prove heading semantics, mathematical-unit "
                  "completeness, independent review, C0 freeze, or source acceptance. "
                  "All spans are unresolved."),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--snapshot", required=True, help="full 40-character commit SHA")
    args = parser.parse_args()
    try:
        result = capture(args.repo, args.snapshot)
    except EvidenceError as exc:
        print(json.dumps({"schema": "d0-c0-book-byte-partition-prototype-v1",
                          "capture_status": "unresolved", "reason": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["capture_status"] == "expected_book_blob_bytes_reconstructed" else 1


if __name__ == "__main__":
    sys.exit(main())
