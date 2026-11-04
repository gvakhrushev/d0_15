#!/usr/bin/env python3
"""Verify pinned C0 review candidate byte partitions.

The primary artifact and both books are read from Git objects through the
existing c0_book_byte_partition reader supplied via --reader. This verifies
byte provenance and coverage only, not mathematical classification, review,
acceptance or completeness of C0.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any

PRIMARY = "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md"
TITLES = ("Book01 §01.1.8", "Book02 §02.3b")
BOOK01_0116 = "Book01 §01.1.6"
OID = re.compile(r"[0-9a-f]{40}\Z")
SHA = re.compile(r"[0-9a-f]{64}\Z")
RANGE = r"`\[(\d+),(\d+)\)`"


class VerificationError(Exception):
    pass


def load_reader(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("c0_book_git_reader", path)
    if spec is None or spec.loader is None:
        raise VerificationError("cannot load Git reader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    methods = ("_require_repo_root", "_commit_root_tree", "_tree_entries", "_object", "partition")
    if (any(not callable(getattr(module, name, None)) for name in methods)
            or not isinstance(getattr(module, "EvidenceError", None), type)
            or not issubclass(module.EvidenceError, Exception)):
        raise VerificationError("Git reader API is incomplete")
    return module


def object_at(reader: Any, repo: Path, commit: str, path: str) -> tuple[str, bytes]:
    if not OID.fullmatch(commit):
        raise VerificationError("snapshot must be a full lowercase Git commit SHA-1")
    parts = path.split("/")
    if any(part in ("", ".", "..") or "\\" in part or ":" in part for part in parts):
        raise VerificationError("unsafe repository path")
    oid = reader._commit_root_tree(repo, commit)
    for index, part in enumerate(parts):
        entries = reader._tree_entries(reader._object(repo, oid, "tree"))
        selected = [(mode, value) for mode, name, value in entries if name == part.encode("utf-8")]
        if len(selected) != 1:
            raise VerificationError("tracked path is missing or ambiguous: " + path)
        mode, oid = selected[0]
        if index + 1 < len(parts):
            if mode not in ("40000", "040000"):
                raise VerificationError("path component is not a tracked tree")
        elif mode not in ("100644", "100755"):
            raise VerificationError("tracked path is not a regular file")
    return oid, reader._object(repo, oid, "blob")


def exactly(pattern: str, text: str, label: str) -> tuple[str, ...]:
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    if len(matches) != 1:
        raise VerificationError(f"{label}: expected one match, found {len(matches)}")
    value = matches[0]
    return (value,) if isinstance(value, str) else tuple(value)


def parse_primary(raw: bytes, *, include_book01_0116: bool = False) -> list[dict[str, Any]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise VerificationError("primary artifact is not UTF-8") from exc
    header = re.compile(r"(?m)^### C0 source review candidate: ([^\r\n]+)\r?$")
    headings = list(header.finditer(text))
    names = [m.group(1) for m in headings]
    expected = set(TITLES)
    allowed = expected | {BOOK01_0116}
    if (len(names) != len(set(names)) or not expected.issubset(names)
            or not set(names).issubset(allowed)):
        raise VerificationError("expected the specified candidate sections without duplicates")
    if include_book01_0116 and BOOK01_0116 not in names:
        raise VerificationError("the requested Book01 §01.1.6 candidate section is missing")
    candidates = []
    for match in headings:
        if match.group(1) == BOOK01_0116 and not include_book01_0116:
            continue
        rest = text[match.end():]
        next_heading = re.search(r"(?m)^#{1,3} ", rest)
        section = rest[:next_heading.start()] if next_heading else rest
        title = match.group(1)
        commit, = exactly(r"\bsnapshot\s+`([0-9a-f]{40})`", section, "source snapshot")
        path, blob = exactly(r"`(01_BOOKS/BOOK_[^`\r\n]+\.md)`\s+has\s+Git\s+blob\s+`([0-9a-f]{40})`",
                             section, "source path and blob")
        expected_prefix = "01_BOOKS/BOOK_01_" if title.startswith("Book01 ") else "01_BOOKS/BOOK_02_"
        if not path.startswith(expected_prefix):
            raise VerificationError("candidate title and book path disagree")
        start, end, checksum = exactly(
            r"complete section is\s+(?:the half-open byte range\s+)?" + RANGE +
            r",\s*SHA-256\s*`([0-9a-f]{64})`", section, "section range and digest")
        lines = section.splitlines()
        table_headers = [i for i, line in enumerate(lines)
                         if line.strip() == "| Byte range | Candidate disposition and existing support |"]
        if len(table_headers) != 1:
            raise VerificationError("candidate range table header missing or ambiguous")
        i = table_headers[0] + 1
        if i >= len(lines) or not re.fullmatch(r"\|\s*-+\s*\|\s*-+\s*\|\s*", lines[i]):
            raise VerificationError("candidate table separator missing")
        i += 1
        tables = []
        while i < len(lines) and lines[i].startswith("|"):
            tables.append(lines[i])
            i += 1
        if not tables:
            raise VerificationError("candidate range table missing")
        if any(line.startswith("|") for line in lines[i:]):
            raise VerificationError("additional or detached table rows are ambiguous")
        rows = []
        for line in tables:
            m = re.fullmatch(r"\|\s*" + RANGE + r"\s*\|\s*(.*?)\s*\|\s*", line)
            if not m or not m.group(3):
                raise VerificationError("malformed candidate range row")
            rows.append((int(m.group(1)), int(m.group(2)), m.group(3)))
        candidate: dict[str, Any] = {"title": title, "commit": commit, "path": path,
            "blob": blob, "start": int(start), "end": int(end), "sha256": checksum,
            "rows": rows}
        if title == "Book02 §02.3b":
            hs, he = exactly(r"heading\s+" + RANGE, section, "structural heading")
            if "one-byte LF separators" not in section or "final separator is included" not in section:
                raise VerificationError("Book02 structural LF declarations missing")
            candidate["heading"] = (int(hs), int(he))
        else:
            if "Heading and separator, structural context." not in rows[0][2]:
                raise VerificationError("Book01 structural heading row missing")
        candidates.append(candidate)
    return candidates


def verify_candidate(reader: Any, repo: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    oid, data = object_at(reader, repo, candidate["commit"], candidate["path"])
    if oid != candidate["blob"]:
        raise VerificationError("source blob does not match declared Git blob")
    start, end = candidate["start"], candidate["end"]
    if not 0 <= start < end <= len(data):
        raise VerificationError("section bounds are invalid")
    if not SHA.fullmatch(candidate["sha256"]) or hashlib.sha256(data[start:end]).hexdigest() != candidate["sha256"]:
        raise VerificationError("section SHA-256 mismatch")
    spans = reader.partition(data, candidate["commit"], candidate["path"])
    if not any(span.get("kind") == "heading_section" and span.get("byte_start") == start
               and span.get("byte_end_exclusive") == end for span in spans):
        raise VerificationError("declared range is not one complete lexical heading section")
    rows = candidate["rows"]
    if not rows:
        raise VerificationError("candidate range table missing")
    if candidate["title"] in ("Book01 §01.1.8", BOOK01_0116):
        hs, he, _ = rows[0]
        body = data[hs:he]
        anchor = b"01.1.6" if candidate["title"] == BOOK01_0116 else b"01.1.8"
        if hs != start or not re.fullmatch(rb"#{1,6} " + re.escape(anchor) + rb"[ \t]+[^\r\n]+\n\n", body):
            raise VerificationError("Book01 structural heading and LF are invalid")
        cursor = start
        for a, b, _ in rows:
            if a != cursor or b <= a or b > end:
                raise VerificationError("Book01 ranges have a gap, overlap or invalid end")
            cursor = b
        if cursor != end:
            raise VerificationError("Book01 ranges do not cover the section")
        structural = [{"kind": "heading_and_separator", "start": hs, "end": he}]
    else:
        hs, he = candidate["heading"]
        body = data[hs:he]
        if hs != start or not re.fullmatch(rb"#{1,6} 02\.3b[ \t]+[^\r\n]+\n", body):
            raise VerificationError("Book02 structural heading is invalid")
        cursor = he
        structural = [{"kind": "heading", "start": hs, "end": he}]
        for a, b, _ in rows:
            if a != cursor + 1 or data[cursor:a] != b"\n" or b <= a or b > end:
                raise VerificationError("Book02 ranges require exactly one LF without gap or overlap")
            structural.append({"kind": "LF_separator", "start": cursor, "end": a})
            cursor = b
        if cursor + 1 != end or data[cursor:end] != b"\n":
            raise VerificationError("Book02 final LF separator is missing or invalid")
        structural.append({"kind": "LF_separator", "start": cursor, "end": end})
    # A numerically complete partition may still split a multi-byte character.
    # Decode every claimed row and each separately declared structural range.
    for a, b in ([(a, b) for a, b, _ in rows] +
                 [(item["start"], item["end"]) for item in structural]):
        try:
            data[a:b].decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise VerificationError("range boundary splits UTF-8 text") from exc
    return {"title": candidate["title"], "source_commit": candidate["commit"],
            "source_path": candidate["path"], "source_blob": oid,
            "section": {"start": start, "end": end, "sha256": candidate["sha256"]},
            "table_ranges": [{"start": a, "end": b,
                              "role": "structural" if candidate["title"] in ("Book01 §01.1.8", BOOK01_0116) and i == 0 else "candidate"}
                             for i, (a, b, _) in enumerate(rows)],
            "structural_ranges": structural, "byte_coverage": "verified",
            "text_boundaries": "utf8_decodable",
            "semantic_classification": "not_assessed", "acceptance": "not_assessed"}


def verify(reader: Any, repo: Path, snapshot: str, *, include_book01_0116: bool = False) -> dict[str, Any]:
    repo = Path(repo).resolve()
    reader._require_repo_root(repo)
    primary_blob, primary = object_at(reader, repo, snapshot, PRIMARY)
    candidates = parse_primary(primary, include_book01_0116=include_book01_0116)
    result = [verify_candidate(reader, repo, item) for item in candidates]
    return {"schema": "d0-c0-candidate-range-v1", "snapshot_commit": snapshot,
            "primary_path": PRIMARY, "primary_blob": primary_blob,
            "status": "candidate_byte_coverage_verified", "candidates": result,
            "scope": "Only source bytes, UTF-8 boundaries, lexical heading-section boundaries and declared "
                     "range coverage were checked; the heading scanner is not a full Markdown parser. "
                     "Merged or split rows do not establish a mathematical-unit count. No semantic "
                     "classification, scientific acceptance, C0 coverage or freeze is inferred."}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--include-book01-0116", action="store_true",
                        help="also verify the separately declared Book01 §01.1.6 candidate range")
    parser.add_argument("--reader", type=Path, required=True,
                        help="path to the existing c0_book_byte_partition.py")
    args = parser.parse_args()
    try:
        reader = load_reader(args.reader)
        result = verify(reader, args.repo, args.snapshot, include_book01_0116=args.include_book01_0116)
    except (VerificationError, OSError, ImportError, ValueError, SyntaxError, AttributeError) as exc:
        result = {"schema": "d0-c0-candidate-range-v1", "status": "unresolved", "reason": str(exc)}
    except Exception as exc:
        # The existing Git reader owns its EvidenceError class, loaded at runtime.
        if "reader" not in locals() or not isinstance(exc, reader.EvidenceError):
            raise
        result = {"schema": "d0-c0-candidate-range-v1", "status": "unresolved", "reason": str(exc)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "candidate_byte_coverage_verified" else 1


if __name__ == "__main__":
    sys.exit(main())
