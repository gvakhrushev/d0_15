#!/usr/bin/env python3
"""Bounded, read-only search and composition view over existing D0 authorities.

This is a generated view. Claims, assembly contracts, result evidence, and
Lean declaration facts continue to be owned by their existing source files.
Text search returns candidates only; it never accepts a mathematical edge.
"""
from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLAIMS = pathlib.Path("02_REGISTRY/claims.csv")
ASSUMPTIONS = pathlib.Path("02_REGISTRY/assumptions.csv")
FORMAL_SUPPORT = pathlib.Path("02_REGISTRY/formal_support.csv")
ALIASES = pathlib.Path("02_REGISTRY/aliases.csv")
APPLICATIONS = pathlib.Path("02_REGISTRY/gr_assembly/applications.json")
CONTRACT = pathlib.Path("02_REGISTRY/gr_assembly/contract.json")
PRESUPPOSITIONS = pathlib.Path("02_REGISTRY/presupposition_edges.json")
TEXT_ROOTS = ("01_BOOKS", "02_REGISTRY", "03_FORMALIZATION",
              "04_CERTIFICATES", "05_EXPERIMENTS", "tools")
# Deterministic outputs from this search workflow live beside its source pins
# for provenance, but must not rank themselves as source evidence.
DERIVED_TEXT_EXCLUDED_PREFIXES = (
    "02_REGISTRY/research/sources/"
    "d0_proof_architecture_formalization_2026-10-24/reports/",
)
MAX_STRUCTURED_SEARCH_RESULTS = 5
MAX_SEARCH_RESULTS = 5
MIN_PIN_VERIFICATION_WINDOW = 18
VERIFIED_PINNED_SOURCE_BONUS = 0.18
MAX_SNIPPET = 650
MAX_FIELD_CHARS = 8000
MAX_SEARCH_EVIDENCE = 3
MAX_SEARCH_SOURCE_REFS = 3
MAX_SEARCH_DETAIL_CHARS = 160
MAX_DECLARED_SOURCE_RESULTS = 3
MAX_DECLARED_SOURCE_APPLICATIONS = 3
MAX_DECLARED_SOURCE_ATTEMPTS = 3
MAX_FORMAL_SUPPORT_LOCATORS = 5
SOURCE_LOCATOR_STOPWORDS = frozenset("""
a an and are as at be been by can do does for from has have if in into is it its
of on or our that the their then this to under was were what when where which
with without would you all any every fixed actual stated declared specified
theorem result source section field proof claim mathematical unit
для или над при без из из-за как где когда который которая которые это этот
эта эти был была были есть для по от до как что если уже настоящий заданный
указанный исходный полный точный точная точное результат источник раздел
математический утверждение доказательство
""".split())


def _configure_stdout_utf8(stream: Any | None = None) -> None:
    """Keep JSON CLI output usable on Windows consoles with legacy code pages."""
    target = sys.stdout if stream is None else stream
    reconfigure = getattr(target, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")


def read_json(root: pathlib.Path, relative: pathlib.Path) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8-sig"))


def read_csv(root: pathlib.Path, relative: pathlib.Path) -> list[dict[str, str]]:
    with (root / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


_BOOK_HEADING_RE = re.compile(r"^BOOK_(\d+)(?:_|\.|$)", re.IGNORECASE)
_BOOK_TOKEN_RE = re.compile(r"^BOOK[_ -]?(\d+)$", re.IGNORECASE)
_SECTION_ID_RE = re.compile(
    r"^(?:§\s*)?\d+(?:\.\d+)*(?:[a-z])?(?:\s*[-–]\s*\d+(?:\.\d+)*(?:[a-z])?)?$",
    re.IGNORECASE,
)
_HEADING_SECTION_RE = re.compile(
    r"^(?:§\s*)?(\d+(?:\.\d+)*(?:[a-z])?(?:[-–]\d+(?:\.\d+)*(?:[a-z])?)?)(?=$|[\s:：—–])",
    re.IGNORECASE,
)


def _parse_claim_book_tokens(value: str) -> tuple[list[str], str | None]:
    """Expand BOOK_01/02 shorthand without guessing at other source names."""
    parts = [part.strip() for part in value.split("/") if part.strip()]
    if not parts:
        return [], "missing_book_locator"
    numbers: list[str] = []
    current: str | None = None
    for part in parts:
        full = _BOOK_TOKEN_RE.fullmatch(part)
        if full:
            current = f"{int(full.group(1)):02d}"
            numbers.append(current)
            continue
        if part.isdecimal() and current is not None:
            current = f"{int(part):02d}"
            numbers.append(current)
            continue
        return [], "malformed_book_locator"
    return [f"BOOK_{number}" for number in numbers], None


def _claim_section_tokens(value: str) -> list[str]:
    """Split slash-separated section IDs, preserving prose labels verbatim."""
    value = value.strip()
    if not value:
        return []
    parts = [part.strip() for part in value.split("/")]
    if len(parts) > 1 and all(_SECTION_ID_RE.fullmatch(part) for part in parts):
        return parts
    return [value]


def _claim_heading_candidates(
    section: str,
    headings: list[dict[str, Any]],
    heading_texts: dict[tuple[str, int], str],
) -> list[dict[str, Any]]:
    """Return exact or lexical heading candidates without accepting a source map."""
    exact = [dict(heading) for heading in headings
             if _section_matches_heading(section, heading["heading"])]
    if exact:
        for candidate in exact:
            candidate["match_kind"] = "exact_heading"
            candidate["review_status"] = "unreviewed_exact_heading_candidate"
        return exact

    # Numeric section labels already make a precise claim. If that heading is
    # absent, lexical matches would only obscure the actual locator failure.
    if _SECTION_ID_RE.fullmatch(section):
        return []

    query_terms = _locator_terms(section)
    if not query_terms:
        return []
    # A single title anchor is enough when the section body matches at least
    # three quarters of the locator. This preserves strong topical candidates
    # whose locator describes the result more precisely than the heading does.
    minimum_title_matches = min(1, len(query_terms))
    minimum_matches = min(len(query_terms), max(minimum_title_matches,
                                                 (len(query_terms) + 1) // 2))
    ranked: list[tuple[int, int, dict[str, Any]]] = []
    for heading in headings:
        text = heading_texts.get((heading["path"], heading["line"]), heading["heading"])
        title_shared = query_terms & _locator_terms(heading["heading"])
        shared = query_terms & _locator_terms(text)
        body_only_minimum = max(minimum_matches, (3 * len(query_terms) + 3) // 4)
        if (len(title_shared) < minimum_title_matches or len(shared) < minimum_matches
                or len(shared) < body_only_minimum):
            continue
        candidate = dict(heading)
        candidate.update({
            "match_kind": "lexical_heading_candidate",
            "title_matched_terms": sorted(title_shared),
            "matched_terms": sorted(shared),
            "query_term_count": len(query_terms),
            "overlap_fraction": round(len(shared) / len(query_terms), 4),
            "review_status": "unreviewed_lexical_candidate",
        })
        ranked.append((len(title_shared), len(shared), candidate))
    ranked.sort(key=lambda item: (-item[0], -item[1], item[2]["line"], item[2]["path"]))
    return [candidate for _title_count, _count, candidate in ranked[:3]]


def _normalize_heading_label(value: str) -> str:
    value = re.sub(r"^§\s*", "", value.strip(), flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value)
    return value.casefold()


def _section_matches_heading(section: str, heading: str) -> bool:
    """Match a section ID at the beginning of a Markdown heading, never body text."""
    section_id = _normalize_heading_label(section).replace("–", "-")
    if _SECTION_ID_RE.fullmatch(section):
        match = _HEADING_SECTION_RE.match(heading)
        return bool(match and match.group(1).casefold().replace("–", "-") == section_id)
    return _normalize_heading_label(heading) == _normalize_heading_label(section)


def _book_source_pin(root: pathlib.Path, path: pathlib.Path) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    blob_sha1: str | None = None
    head_blob_sha1: str | None = None
    try:
        blob_sha1 = subprocess.check_output(
            ["git", "hash-object", "--", str(path)], cwd=root,
            text=True, encoding="utf-8", stderr=subprocess.DEVNULL,
        ).strip()
        head_blob_sha1 = subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{relative}"], cwd=root,
            text=True, encoding="utf-8", stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return {
        "path": relative,
        "source_sha256": sha256(path),
        "source_blob_sha1": blob_sha1,
        "snapshot_blob_sha1": head_blob_sha1,
        "matches_snapshot_commit": bool(blob_sha1 and blob_sha1 == head_blob_sha1),
    }


def claim_source_candidate_view(dataset: dict[str, Any]) -> dict[str, Any]:
    """Resolve existing claim book/section locators to exact heading candidates.

    This generated view reports source-location candidates only. It does not
    accept claim semantics, application edges, or any C0 disposition.
    """
    root: pathlib.Path = dataset["root"]
    book_paths: dict[str, list[pathlib.Path]] = {}
    book_sources: dict[str, dict[str, Any]] = {}
    book_headings: dict[str, list[dict[str, Any]]] = {}
    book_heading_texts: dict[str, dict[tuple[str, int], str]] = {}
    claim_id_pattern = _claim_id_pattern(
        claim.get("claim_id", "") for claim in dataset["claims"]
    )
    claim_id_mentions: dict[str, list[dict[str, Any]]] = {}
    for path in sorted((root / "01_BOOKS").glob("BOOK_*.md")):
        match = _BOOK_HEADING_RE.match(path.name)
        if not match:
            continue
        key = f"BOOK_{int(match.group(1)):02d}"
        book_paths.setdefault(key, []).append(path)
        pin = _book_source_pin(root, path)
        book_sources[pin["path"]] = pin
        book_text = path.read_text(encoding="utf-8-sig")
        sections = _markdown_sections(book_text)
        for line_number, heading, body in sections:
            book_headings.setdefault(key, []).append({
                "path": pin["path"],
                "line": line_number,
                "heading": heading,
                "source_sha256": pin["source_sha256"],
                "source_blob_sha1": pin["source_blob_sha1"],
                "snapshot_blob_sha1": pin["snapshot_blob_sha1"],
                "matches_snapshot_commit": pin["matches_snapshot_commit"],
            })
            book_heading_texts.setdefault(key, {})[(pin["path"], line_number)] = (
                heading + "\n" + body
            )
        headings_by_line = sorted(
            (line, heading) for line, heading, _body in sections
        )
        heading_index = 0
        nearest_heading: str | None = None
        nearest_heading_line: int | None = None
        fence_char: str | None = None
        fence_length = 0
        for line_number, line in enumerate(book_text.splitlines(), start=1):
            fence_char, fence_length, is_fence_line = _markdown_fence_transition(
                line, fence_char, fence_length
            )
            if is_fence_line:
                continue
            if fence_char is not None:
                continue
            while (heading_index < len(headings_by_line)
                   and headings_by_line[heading_index][0] == line_number):
                nearest_heading_line, nearest_heading = headings_by_line[heading_index]
                heading_index += 1
            for mention in claim_id_pattern.finditer(line):
                claim_id = mention.group("claim_id")
                column_start = mention.start()
                column_end = mention.end()
                excerpt_start = max(0, column_start - MAX_SNIPPET // 2)
                excerpt_end = min(len(line), max(column_end, excerpt_start + MAX_SNIPPET))
                if excerpt_end - excerpt_start < MAX_SNIPPET:
                    excerpt_start = max(0, excerpt_end - MAX_SNIPPET)
                occurrence = {
                    "book_locator": key,
                    "path": pin["path"],
                    "line": line_number,
                    "start_offset_0based": column_start,
                    "end_offset_0based_exclusive": column_end,
                    "claim_id_text": claim_id,
                    "nearest_heading": nearest_heading,
                    "nearest_heading_line": nearest_heading_line,
                    "literal_text_excerpt": line[
                        excerpt_start:excerpt_end
                    ].strip(),
                    "matches_snapshot_commit": pin["matches_snapshot_commit"],
                    "candidate_coordinate_key": (
                        f"source:{dataset['snapshot_commit']}:{pin['path']}"
                        f"#L{line_number}:O[{column_start},{column_end})"
                        if pin["matches_snapshot_commit"] else None
                    ),
                    "match_kind": "literal_claim_id_mention",
                    "review_status": "unreviewed_literal_claim_id_mention_candidate",
                }
                claim_id_mentions.setdefault(claim_id, []).append(occurrence)

    rows: list[dict[str, Any]] = []
    counts = {
        "claim_rows": len(dataset["claims"]),
        "fully_unique_claim_rows": 0,
        "partially_resolved_claim_rows": 0,
        "ambiguous_claim_rows": 0,
        "unresolved_claim_rows": 0,
        "non_book_claim_rows": 0,
        "malformed_claim_rows": 0,
        "locator_pairs": 0,
        "unique_locator_pairs": 0,
        "ambiguous_locator_pairs": 0,
        "unresolved_locator_pairs": 0,
        "unpaired_multi_book_claim_rows": 0,
        "claim_rows_with_ranked_heading_candidates": 0,
        "ranked_heading_candidate_count": 0,
        "literal_claim_id_mention_count": 0,
        "claim_rows_with_literal_claim_id_mentions": 0,
        "book_source_files_with_literal_claim_id_mentions": 0,
    }

    for claim in dataset["claims"]:
        claim_id = claim.get("claim_id", "")
        book_field = claim.get("book", "").strip()
        section_field = claim.get("section", "").strip()
        recognized_book = bool(re.search(r"\bBOOK[_ -]?\d+", book_field, re.IGNORECASE))
        if not recognized_book:
            counts["non_book_claim_rows"] += 1
            rows.append({
                "claim_id": claim_id,
                "book_locator": book_field,
                "section_locator": section_field,
                "resolution_status": "non_book_locator",
                "locator_pairs": [],
                "literal_claim_id_mentions": claim_id_mentions.get(claim_id, []),
                "interpretation": "The declared source is not a BOOK_XX locator; no book heading was inferred.",
            })
            continue

        book_tokens, book_error = _parse_claim_book_tokens(book_field)
        section_tokens = _claim_section_tokens(section_field)
        parse_error = book_error
        if not section_tokens:
            parse_error = parse_error or "missing_section_locator"
        elif book_tokens and len(book_tokens) > 1 and len(section_tokens) == 1:
            counts["unpaired_multi_book_claim_rows"] += 1
            book_candidates = []
            row_has_ranked_candidates = False
            for book_key in book_tokens:
                candidates = _claim_heading_candidates(
                    section_tokens[0], book_headings.get(book_key, []),
                    book_heading_texts.get(book_key, {}),
                )
                for candidate in candidates:
                    candidate["candidate_source_unit_key"] = (
                        f"source:{dataset['snapshot_commit']}:{candidate['path']}"
                        f"#L{candidate['line']}: {candidate['heading']}"
                        if candidate["matches_snapshot_commit"] else None
                    )
                    if candidate["match_kind"] == "lexical_heading_candidate":
                        row_has_ranked_candidates = True
                        counts["ranked_heading_candidate_count"] += 1
                book_candidates.append({
                    "book_locator": book_key,
                    "candidate_count": len(candidates),
                    "candidates": candidates,
                })
            if row_has_ranked_candidates:
                counts["claim_rows_with_ranked_heading_candidates"] += 1
            counts["unresolved_claim_rows"] += 1
            rows.append({
                "claim_id": claim_id,
                "book_locator": book_field,
                "section_locator": section_field,
                "resolution_status": "unresolved",
                "resolution_reason": "multiple_books_share_one_unpaired_section_locator",
                "locator_pairs": [],
                "book_heading_candidates": book_candidates,
                "literal_claim_id_mentions": claim_id_mentions.get(claim_id, []),
                "interpretation": (
                    "Multiple books share one section locator, so no book/section pairing was inferred. "
                    "Heading matches are retrieval candidates requiring source-unit review."
                ),
            })
            continue
        elif book_tokens and len(book_tokens) != 1 and len(book_tokens) != len(section_tokens):
            parse_error = "book_section_count_mismatch"

        if parse_error:
            counts["malformed_claim_rows"] += 1
            rows.append({
                "claim_id": claim_id,
                "book_locator": book_field,
                "section_locator": section_field,
                "resolution_status": "malformed_locator",
                "parse_error": parse_error,
                "locator_pairs": [],
                "literal_claim_id_mentions": claim_id_mentions.get(claim_id, []),
                "interpretation": "The locator could not be paired conservatively; no source was selected.",
            })
            continue

        pairs = ([(book_tokens[0], section) for section in section_tokens]
                 if len(book_tokens) == 1 else list(zip(book_tokens, section_tokens)))
        pair_rows: list[dict[str, Any]] = []
        for book_key, section in pairs:
            paths = book_paths.get(book_key, [])
            heading_candidates = _claim_heading_candidates(
                section, book_headings.get(book_key, []),
                book_heading_texts.get(book_key, {}),
            )
            candidates = [candidate for candidate in heading_candidates
                          if candidate["match_kind"] == "exact_heading"]
            ranked_candidates = [candidate for candidate in heading_candidates
                                 if candidate["match_kind"] == "lexical_heading_candidate"]
            for candidate in candidates:
                candidate["candidate_source_unit_key"] = (
                    f"source:{dataset['snapshot_commit']}:{candidate['path']}"
                    f"#L{candidate['line']}: {candidate['heading']}"
                    if candidate["matches_snapshot_commit"] else None
                )
            if len(paths) == 0:
                status = "unresolved"
                reason = "book_file_missing"
            elif len(candidates) == 1 and len(paths) == 1:
                status = "unique"
                reason = None
            elif candidates:
                status = "ambiguous"
                reason = "multiple_exact_heading_candidates"
            else:
                status = "unresolved"
                reason = "no_exact_heading_match"
            counts["locator_pairs"] += 1
            counts[f"{status}_locator_pairs"] += 1
            pair_row: dict[str, Any] = {
                "book_locator": book_key,
                "section_locator": section,
                "resolution_status": status,
                "candidates": candidates,
            }
            if ranked_candidates:
                for candidate in ranked_candidates:
                    candidate["candidate_source_unit_key"] = (
                        f"source:{dataset['snapshot_commit']}:{candidate['path']}"
                        f"#L{candidate['line']}: {candidate['heading']}"
                        if candidate["matches_snapshot_commit"] else None
                    )
                pair_row["ranked_heading_candidates"] = ranked_candidates
                counts["ranked_heading_candidate_count"] += len(ranked_candidates)
            if reason:
                pair_row["reason"] = reason
            pair_rows.append(pair_row)

        statuses = [row["resolution_status"] for row in pair_rows]
        if all(status == "unique" for status in statuses):
            overall = "unique"
            counts["fully_unique_claim_rows"] += 1
        elif "ambiguous" in statuses:
            overall = "ambiguous"
            counts["ambiguous_claim_rows"] += 1
        elif "unique" in statuses:
            overall = "partial"
            counts["partially_resolved_claim_rows"] += 1
        else:
            overall = "unresolved"
            counts["unresolved_claim_rows"] += 1
        if any(pair.get("ranked_heading_candidates") for pair in pair_rows):
            counts["claim_rows_with_ranked_heading_candidates"] += 1
        mentions = claim_id_mentions.get(claim_id, [])
        rows.append({
            "claim_id": claim_id,
            "book_locator": book_field,
            "section_locator": section_field,
            "resolution_status": overall,
            "locator_pairs": pair_rows,
            "literal_claim_id_mentions": mentions,
            "interpretation": "Exact heading coordinates are source candidates, not semantic claim acceptance or C0 disposition.",
        })

    heading_claim_links: dict[tuple[str, int], dict[str, set[str]]] = {}
    for claim_row in rows:
        claim_id = claim_row.get("claim_id", "")
        candidate_lists: list[list[dict[str, Any]]] = []
        for pair in claim_row.get("locator_pairs", []):
            candidate_lists.append(pair.get("candidates", []))
            candidate_lists.append(pair.get("ranked_heading_candidates", []))
        for group in claim_row.get("book_heading_candidates", []):
            candidate_lists.append(group.get("candidates", []))
        for candidates in candidate_lists:
            for candidate in candidates:
                if not candidate.get("path") or not isinstance(candidate.get("line"), int):
                    continue
                link = heading_claim_links.setdefault(
                    (candidate["path"], candidate["line"]),
                    {"exact_claim_ids": set(), "ranked_claim_ids": set()},
                )
                relation = (
                    "exact_claim_ids"
                    if candidate.get("match_kind") == "exact_heading"
                    else "ranked_claim_ids"
                )
                link[relation].add(claim_id)

    book_heading_source_candidates: list[dict[str, Any]] = []
    for book_key, headings in sorted(book_headings.items()):
        for heading in headings:
            link = heading_claim_links.get(
                (heading["path"], heading["line"]),
                {"exact_claim_ids": set(), "ranked_claim_ids": set()},
            )
            source_unit_key = (
                f"source:{dataset['snapshot_commit']}:{heading['path']}"
                f"#L{heading['line']}: {heading['heading']}"
                if heading["matches_snapshot_commit"] else None
            )
            book_heading_source_candidates.append({
                "book_locator": book_key,
                "path": heading["path"],
                "line": heading["line"],
                "heading": heading["heading"],
                "candidate_source_unit_key": source_unit_key,
                "matches_snapshot_commit": heading["matches_snapshot_commit"],
                "exact_heading_candidate_claim_ids": sorted(link["exact_claim_ids"]),
                "ranked_heading_candidate_claim_ids": sorted(link["ranked_claim_ids"]),
            })

    counts.update({
        "literal_claim_id_mention_count": sum(
            len(mentions) for mentions in claim_id_mentions.values()
        ),
        "claim_rows_with_literal_claim_id_mentions": sum(
            bool(claim_id_mentions.get(claim.get("claim_id", "")))
            for claim in dataset["claims"]
        ),
        "book_source_files_with_literal_claim_id_mentions": len({
            mention["path"]
            for mentions in claim_id_mentions.values()
            for mention in mentions
        }),
        "book_heading_count": len(book_heading_source_candidates),
        "book_headings_with_exact_heading_candidate": sum(
            bool(row["exact_heading_candidate_claim_ids"])
            for row in book_heading_source_candidates
        ),
        "book_headings_with_ranked_heading_candidate": sum(
            bool(row["ranked_heading_candidate_claim_ids"])
            for row in book_heading_source_candidates
        ),
        "book_headings_with_both_exact_and_ranked_heading_candidates": sum(
            bool(row["exact_heading_candidate_claim_ids"]
                 and row["ranked_heading_candidate_claim_ids"])
            for row in book_heading_source_candidates
        ),
        "book_headings_without_claim_heading_candidate": sum(
            not row["exact_heading_candidate_claim_ids"]
            and not row["ranked_heading_candidate_claim_ids"]
            for row in book_heading_source_candidates
        ),
    })

    return {
        "schema": "d0-claim-source-candidate-view-v3",
        "snapshot_commit": dataset["snapshot_commit"],
        "worktree_dirty": dataset.get("worktree_dirty"),
        "collector_sha256": sha256(pathlib.Path(__file__).resolve()),
        "claim_registry_sha256": dataset["source_digests"].get(CLAIMS.as_posix()),
        "book_sources": book_sources,
        "book_source_count": len(book_sources),
        "counts": counts,
        "rows": rows,
        "book_heading_source_candidates": book_heading_source_candidates,
        "interpretation": (
            "Derived locator view only. Exact heading matches identify candidate source coordinates; "
            "ranked headings are retrieval candidates, not exact source links. The exhaustive heading list "
            "contains source coordinates, while literal claim-ID mentions identify textual coordinates that may "
            "be citations or cross-references. Neither kind identifies accepted mathematical units or C0 "
            "dispositions. None of these fields accepts a claim statement, proves semantic coverage, freezes C0, "
            "or changes owner/status."
        ),
    }


def alias_source_candidate_view(dataset: dict[str, Any]) -> dict[str, Any]:
    """Inspect alias targets and legacy book locators without accepting semantics."""
    root: pathlib.Path = dataset["root"]
    claim_rows = {row.get("claim_id", ""): row for row in dataset["claims"]}
    rows: list[dict[str, Any]] = []
    counts: dict[str, int] = {
        "alias_count": len(dataset["aliases"]),
        "legacy_book_label_count": 0,
        "canonical_target_alias_count": 0,
        "legacy_id_in_claim_registry_count": 0,
        "legacy_ids_with_existing_book_locator_count": 0,
        "legacy_ids_with_label_in_designated_book_count": 0,
        "legacy_locator_line_with_label_count": 0,
        "legacy_locator_is_first_label_line_count": 0,
        "legacy_ids_without_designated_book_occurrence_count": 0,
        "canonical_targets_found_count": 0,
        "canonical_targets_missing_count": 0,
    }
    book_lines: dict[str, list[str]] = {}
    book_pins: dict[str, dict[str, Any]] = {}

    for alias in dataset["aliases"]:
        alias_id = alias.get("legacy_id", "")
        kind = alias.get("kind", "")
        item: dict[str, Any] = {
            "alias_id": alias_id,
            "kind": kind,
            "first_reference": alias.get("first_reference", ""),
            "note": alias.get("note", ""),
            "interpretation": "Lookup/source candidate only; no semantic merge or C0 disposition is inferred.",
        }

        if kind == "CANONICAL_TARGET":
            counts["canonical_target_alias_count"] += 1
            target_id = alias.get("canonical_claim_id", "")
            target = claim_rows.get(target_id)
            item.update({
                "canonical_claim_id": target_id,
                "target_claim_found": target is not None,
            })
            if target is None:
                counts["canonical_targets_missing_count"] += 1
            else:
                counts["canonical_targets_found_count"] += 1
                item["canonical_claim"] = {
                    field: target.get(field)
                    for field in (
                        "claim_id", "book", "section", "lean_module", "lean_theorem",
                        "lean_status", "uses_bridge_assumptions", "assumption_ids",
                        "release_status",
                    )
                }
            book_name = alias.get("first_reference", "")
            valid_book_name = bool(re.fullmatch(r"BOOK_[A-Za-z0-9_.-]+\.md", book_name))
            book_path = root / "01_BOOKS" / book_name if valid_book_name else None
            item["book_source_path"] = (
                book_path.relative_to(root).as_posix() if book_path is not None else None
            )
            item["book_source_exists"] = bool(book_path and book_path.is_file())
            if book_path and book_path.is_file():
                pin = _book_source_pin(root, book_path)
                item["book_source_pin"] = pin
                book_pins[pin["path"]] = pin
            item["resolution_status"] = (
                "canonical_target_found" if target is not None else "canonical_target_missing"
            )
            rows.append(item)
            continue

        if kind != "LEGACY_BOOK_LABEL":
            item["resolution_status"] = "unrecognized_alias_kind"
            rows.append(item)
            continue

        counts["legacy_book_label_count"] += 1
        item["claim_registry_contains_legacy_id"] = alias_id in claim_rows
        counts["legacy_id_in_claim_registry_count"] += alias_id in claim_rows
        match = re.fullmatch(r"(BOOK_[A-Za-z0-9_.-]+\.md):([1-9][0-9]*)",
                             alias.get("first_reference", ""))
        if match is None:
            item["resolution_status"] = "invalid_book_line_reference"
            rows.append(item)
            continue

        book_name, line_text = match.groups()
        line_number = int(line_text)
        book_path = root / "01_BOOKS" / book_name
        item["locator_source_path"] = book_path.relative_to(root).as_posix()
        item["locator_line"] = line_number
        if not book_path.is_file():
            item["resolution_status"] = "book_source_missing"
            rows.append(item)
            continue

        relative_path = book_path.relative_to(root).as_posix()
        if relative_path not in book_lines:
            book_lines[relative_path] = book_path.read_text(encoding="utf-8-sig").splitlines()
            book_pins[relative_path] = _book_source_pin(root, book_path)
        lines = book_lines[relative_path]
        item["book_source_pin"] = book_pins[relative_path]
        if line_number > len(lines):
            item["resolution_status"] = "line_out_of_range"
            rows.append(item)
            continue

        counts["legacy_ids_with_existing_book_locator_count"] += 1
        label_pattern = _claim_id_pattern([alias_id])
        occurrence_lines = [index for index, line in enumerate(lines, start=1)
                            if label_pattern.search(line)]
        line_text_value = lines[line_number - 1]
        line_has_label = bool(label_pattern.search(line_text_value))
        if line_has_label:
            counts["legacy_locator_line_with_label_count"] += 1
        if occurrence_lines:
            counts["legacy_ids_with_label_in_designated_book_count"] += 1
            if occurrence_lines[0] == line_number:
                counts["legacy_locator_is_first_label_line_count"] += 1
        else:
            counts["legacy_ids_without_designated_book_occurrence_count"] += 1

        item.update({
            "resolution_status": "existing_line_anchor_with_label"
            if line_has_label else "existing_line_anchor_without_label_text",
            "locator_line_contains_alias_id": line_has_label,
            "first_alias_occurrence_line_in_designated_book": (
                occurrence_lines[0] if occurrence_lines else None
            ),
            "alias_occurrence_count_in_designated_book": len(occurrence_lines),
            "locator_is_first_alias_occurrence_in_designated_book": (
                bool(occurrence_lines) and occurrence_lines[0] == line_number
            ),
            "locator_line_text": line_text_value,
        })
        rows.append(item)

    return {
        "schema": "d0-alias-source-candidate-view-v1",
        "snapshot_commit": dataset["snapshot_commit"],
        "worktree_dirty": dataset.get("worktree_dirty"),
        "alias_registry_sha256": dataset["source_digests"].get(ALIASES.as_posix()),
        "claim_registry_sha256": dataset["source_digests"].get(CLAIMS.as_posix()),
        "counts": counts,
        "rows": rows,
        "book_sources": book_pins,
        "interpretation": (
            "Existing line anchors, literal labels, and canonical-target lookups are source candidates only. "
            "They do not establish semantic equivalence, a mathematical-unit identity, a Lean application, "
            "release status, or independent C0 acceptance."
        ),
    }


def _claim_id_pattern(claim_ids: Any) -> re.Pattern[str]:
    """Match exact claim-ID tokens without matching them inside longer IDs."""
    identifiers = sorted({str(value) for value in claim_ids if str(value)},
                         key=lambda value: (-len(value), value))
    if not identifiers:
        return re.compile(r"(?!)")
    alternatives = "|".join(re.escape(value) for value in identifiers)
    return re.compile(
        rf"(?<![A-Za-z0-9_-])(?P<claim_id>{alternatives})(?![A-Za-z0-9_-])"
    )


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dataset(root: pathlib.Path = ROOT) -> dict[str, Any]:
    """Load the existing authorities and their source digests; create no registry."""
    paths = (CLAIMS, ASSUMPTIONS, FORMAL_SUPPORT, ALIASES, APPLICATIONS, CONTRACT, PRESUPPOSITIONS)
    missing = [path.as_posix() for path in paths if not (root / path).is_file()]
    if missing:
        raise FileNotFoundError(f"required D0 authority files are missing: {missing}")
    applications = read_json(root, APPLICATIONS)
    contract = read_json(root, CONTRACT)
    return {
        "root": root,
        "claims": read_csv(root, CLAIMS),
        "assumptions": read_csv(root, ASSUMPTIONS),
        "formal_support": read_csv(root, FORMAL_SUPPORT),
        "aliases": read_csv(root, ALIASES),
        "assembly": applications,
        "contract": contract,
        "presuppositions": read_json(root, PRESUPPOSITIONS),
        "snapshot_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
        ).strip(),
        "worktree_dirty": bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=root, text=True, encoding="utf-8"
        ).strip()),
        "source_digests": {p.as_posix(): sha256(root / p) for p in paths},
    }


def _lean_atoms(row: dict[str, Any]) -> list[str]:
    return [part.strip() for part in str(row.get("lean_theorem", "")).split(";") if part.strip()]


def _as_rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        rows = []
        for key, item in value.items():
            if isinstance(item, dict):
                rows.append({**item, "id": item.get("id", key)})
            else:
                rows.append({"id": key, "value": item})
        return rows
    return []


def records(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize authorities into read-only display records without merging units."""
    out: list[dict[str, Any]] = []
    for row in dataset["claims"]:
        key = row.get("claim_id", "")
        out.append({
            "kind": "claim-metadata", "key": key,
            "label": f"{row.get('book', '')} §{row.get('section', '')}".strip(),
            "source": CLAIMS.as_posix(), "record": row,
            "search_terms": [key, row.get("book", ""), row.get("section", ""),
                             row.get("lean_module", ""), *_lean_atoms(row), row.get("notes", "")],
        })
    for row in dataset["assumptions"]:
        key = row.get("assumption_id", "")
        out.append({
            "kind": "assumption-metadata", "key": key,
            "label": row.get("justification", ""),
            "source": ASSUMPTIONS.as_posix(), "record": row,
            "search_terms": [key, row.get("lean_name", ""), row.get("lean_file", ""),
                             row.get("used_by_theorem", ""), row.get("claim_id", ""),
                             row.get("assumption_type", ""), row.get("status", ""),
                             row.get("justification", ""),
                             row.get("external_source_or_cert", ""),
                             row.get("failure_meaning", "")],
        })
    for row in dataset["formal_support"]:
        key = row.get("lean_module", "")
        out.append({
            "kind": "formal-support-metadata", "key": key,
            "label": row.get("role", ""), "source": FORMAL_SUPPORT.as_posix(),
            "record": row,
            "search_terms": [key, row.get("lean_file", ""), row.get("role", ""),
                             row.get("referenced_by", "")],
        })
    for row in dataset["aliases"]:
        key = row.get("legacy_id", "")
        out.append({
            "kind": "alias-lookup", "key": key,
            "label": row.get("canonical_claim_id") or row.get("first_reference", ""),
            "source": ALIASES.as_posix(), "record": row,
            "search_terms": [key, row.get("kind", ""), row.get("canonical_claim_id", ""),
                             row.get("first_reference", ""), row.get("note", "")],
        })
    for row in dataset["presuppositions"].get("edges", []):
        key = f"{row.get('claim', '')}->{row.get('presupposes', '')}"
        out.append({
            "kind": "conceptual-presupposition", "key": key,
            "label": row.get("evidence", ""),
            "source": PRESUPPOSITIONS.as_posix(), "record": row,
            "search_terms": [key, row.get("claim", ""), row.get("presupposes", ""),
                             row.get("evidence", "")],
        })
    assembly = dataset["assembly"]
    for collection, kind in (("results", "assembly-result"), ("applications", "application"),
                             ("attempts", "scoped-attempt")):
        for row in assembly.get(collection, []):
            key = row.get("id", "")
            out.append({
                "kind": kind, "key": key, "label": row.get("statement", row.get("title", "")),
                "source": APPLICATIONS.as_posix(), "record": row,
                "search_terms": [key, row.get("statement", ""), row.get("title", ""),
                                 row.get("owner", ""), row.get("interface", ""),
                                 row.get("work_key", ""), row.get("scope", "")],
            })
    contract = dataset["contract"]
    for collection, kind in (("obligations", "obligation"), ("interfaces", "interface"),
                             ("goals", "assembly-goal"), ("anti_substitutions", "countercontrol"),
                             ("synthesis", "composition"),
                             ("source_fork_reconciliations", "source-fork-reconciliation")):
        for row in _as_rows(contract.get(collection, [])):
            key = row.get("id", "")
            out.append({
                "kind": kind, "key": key, "label": row.get("statement", row.get("title", "")),
                "source": CONTRACT.as_posix(), "record": row,
                "search_terms": [key, row.get("statement", ""), row.get("title", ""),
                                 row.get("contribution", ""), row.get("consumer", ""),
                                 row.get("interface", ""), row.get("next_question", ""),
                                 row.get("carrier", ""), row.get("action", ""),
                                 row.get("variations", ""), row.get("source", ""),
                                 row.get("normalization", ""), row.get("refinement", ""),
                                 row.get("scope", ""), row.get("owner", ""),
                                 row.get("work_key", ""), row.get("hypothesis_map", ""),
                                 row.get("evidence", ""), row.get("method", ""),
                                 row.get("conclusion", ""), row.get("path", "")],
            })
    return out


def _item_text(item: dict[str, Any]) -> str:
    return " ".join(str(value) for value in item.get("search_terms", []) if value).casefold()


def structured_search(dataset: dict[str, Any], query: str,
                      limit: int = MAX_STRUCTURED_SEARCH_RESULTS) -> list[dict[str, Any]]:
    exact = " ".join(query.casefold().split())
    if not exact:
        return []
    found: list[tuple[tuple[int, int, int], dict[str, Any]]] = []
    for item in records(dataset):
        key = str(item.get("key", "")).casefold()
        exact_key = key == exact
        exact_name = bool(exact and exact in key)
        exact_field = bool(exact and any(
            exact in " ".join(str(value).casefold().split())
            for value in item.get("search_terms", []) if value
        ))
        if not (exact_key or exact_name or exact_field):
            continue
        # Registry matches are exact authority lookups. Approximate matching
        # belongs in full-text candidates and cannot manufacture a declared
        # result, alias, dependency, or application relation.
        rank = (0 if exact_key else 1 if exact_name else 2, len(key), len(item["kind"]))
        found.append((rank, item))
    found.sort(key=lambda pair: (pair[0], pair[1]["kind"], pair[1]["key"]))
    return [item for _, item in found[:limit]]


_QUERY_SYNONYMS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("all", ("all", "every", "все", "всех", "всем", "все16")),
    ("exact", ("exact", "exactly", "precise", "точн")),
    ("raising", ("raising", "creator", "creation", "подъем", "подъём", "создател", "создан")),
    ("operator", ("operator", "оператор")),
    ("inverse", ("inverse", "invert", "reconstruct", "reconstruction", "обратн", "восстанов")),
    ("null", ("null", "lightlike", "isotropic", "нул", "светоподоб", "изотроп", "pp-wave")),
    ("leg", ("leg", "component", "компонент", "ножк")),
    ("coframe", ("coframe", "solder", "тетрад", "кофрейм")),
    ("link", ("link", "links", "connection", "связь", "связи", "звено", "ребро")),
    ("direction", ("direction", "directions", "направлен")),
    ("row", ("row", "rows", "строк", "строка", "строки")),
    ("node", ("node", "site", "узел", "узла", "узле")),
    ("observer", ("observer", "наблюдател")),
    ("tangent", ("tangent", "касательн")),
    ("jet", ("jet", "jets", "джет", "джеты", "джетов")),
    ("lorentz", ("lorentz", "лоренц")),
    ("transverse", ("transverse", "попереч")),
    ("nonvacuum", ("nonvacuum", "non-vacuum", "невакуум", "не-вакуум")),
    ("midpoint", ("midpoint", "середин")),
    ("radial", ("radial", "радиальн")),
    ("equivalence", ("equivalence", "equivalent", "эквивалент")),
)

# Broad words still contribute to matching and ranking, but should not cause
# the first corpus pass to load every document that mentions them. Queries
# made only from broad words retain the ordinary exhaustive fallback.
_LOW_INFORMATION_TERMS = frozenset({
    "all", "first", "full", "complete", "second", "jet", "derivative",
    "variation", "native", "actual", "operator", "source", "positive",
    "recovery", "источник", "полный", "полн", "перв", "втор",
    "производн", "вариац", "оператор", "положител", "восстанов",
    "настоящ", "исходн", "касательн", "окрестност", "вектор",
})


def _fold(text: str) -> str:
    return text.casefold().replace("ё", "е")


def _query_terms(query: str) -> list[tuple[str, tuple[str, ...]]]:
    """Return deduplicated bilingual concept groups for deterministic search."""
    groups: list[tuple[str, tuple[str, ...]]] = []
    seen: set[str] = set()
    for raw in re.findall(r"[\w.-]+", query, flags=re.UNICODE):
        token = _fold(raw.strip(".-_"))
        if len(token) <= 1:
            continue
        match = next((item for item in _QUERY_SYNONYMS
                      if any(token == alias or (len(alias) >= 4 and token.startswith(alias))
                             for alias in item[1])), None)
        name, variants = match if match else (token, (token,))
        if name not in seen:
            groups.append((name, tuple(_fold(value) for value in variants)))
            seen.add(name)
    return groups


def _owner_bonus(rel: str) -> float:
    # Prefer current research owners over copied historical snapshots when
    # textual evidence is otherwise tied. The architecture artifact is not a
    # scientific result owner and receives no special boost.
    if rel.casefold().endswith(".csv"):
        return -0.25
    if rel.startswith("02_REGISTRY/research/sources/") or "/inputs/" in rel:
        return -0.10
    if rel.startswith("02_REGISTRY/research/"):
        return 0.05
    return 0.0


def _filename_bonus(rel: str, terms: list[tuple[str, tuple[str, ...]]]) -> float:
    """Prefer a source whose own title names the queried mathematical topic."""
    stem = _fold(pathlib.PurePosixPath(rel).stem.replace("_", " ").replace("-", " "))
    if not terms:
        return 0.0
    return 0.40 * sum(any(variant in stem for variant in variants)
                      for _, variants in terms) / len(terms)


def _source_references(lines: list[str],
                       terms: list[tuple[str, tuple[str, ...]]] | None = None,
                       pattern: re.Pattern[str] | None = None) -> list[dict[str, Any]]:
    """Expose exact path/commit/blob pins present in matched source lines."""
    path_pattern = re.compile(
        r"(?<![\w])(?:[\w.-]+[\\/])*[\w.-]+\.(?:md|lean|json|csv|py)(?:#[^\s,;]*)?",
        flags=re.IGNORECASE,
    )
    hash_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", flags=re.IGNORECASE)
    commit_pattern = re.compile(r"\bcommit\s*[`:=]?\s*([0-9a-f]{40})\b", flags=re.IGNORECASE)
    blob_pattern = re.compile(r"\bblob\s*[`:=]?\s*([0-9a-f]{40})\b", flags=re.IGNORECASE)
    github_blob_pattern = re.compile(
        r"https?://github\.com/[^/\s)]+/[^/\s)]+/blob/([0-9a-f]{40})/([^\s)#)]+)",
        flags=re.IGNORECASE,
    )
    section_pattern = re.compile(r"§{1,2}\s*([0-9]+(?:\.[0-9a-z]+)?)(?:\s*[–-]\s*([0-9]+(?:\.[0-9a-z]+)?))?",
                                 flags=re.IGNORECASE)
    found: dict[tuple[str, str | None, str | None], dict[str, Any]] = {}
    for line in lines:
        for link in github_blob_pattern.finditer(line):
            normalized = link.group(2).replace("\\", "/")
            commit = link.group(1).lower()
            sections = [part for match in section_pattern.finditer(line)
                        for part in match.groups() if part]
            key = (normalized, commit, None)
            reference = {"path": normalized, "hashes": list(dict.fromkeys(hash_pattern.findall(line))),
                         "commit": commit, "blob": None,
                         "section_refs": list(dict.fromkeys(sections)),
                         "pin_complete": True, "context": line[:MAX_SNIPPET]}
            previous = found.get(key)
            if (previous is None or terms is None or pattern is None or
                    len(_matched_term_names(_fold(line[:MAX_SNIPPET]), pattern, terms)) >
                    len(_matched_term_names(_fold(previous["context"]), pattern, terms))):
                found[key] = reference
        paths = list(path_pattern.finditer(line))
        commits = list(commit_pattern.finditer(line))
        blobs = list(blob_pattern.finditer(line))
        for index, path_match in enumerate(paths):
            next_path_start = paths[index + 1].start() if index + 1 < len(paths) else len(line)
            local_blobs = [match for match in blobs
                           if path_match.end() <= match.start() < next_path_start]
            blob = local_blobs[0].group(1).lower() if local_blobs else None
            preceding_commits = [match for match in commits if match.start() < path_match.start()]
            commit = (preceding_commits[-1].group(1).lower() if preceding_commits else
                      commits[0].group(1).lower() if len(commits) == 1 else None)
            section_text = line[path_match.end():next_path_start]
            section_refs: list[str] = []
            for section in section_pattern.finditer(section_text):
                section_refs.append(section.group(1))
                if section.group(2):
                    section_refs.append(section.group(2))
            if not section_refs:
                section_refs = [part for match in section_pattern.finditer(line)
                                for part in match.groups() if part]
            normalized = path_match.group(0).replace("\\", "/")
            if "/blob/" in normalized or normalized.casefold().startswith("github.com/"):
                continue
            key = (normalized, commit, blob)
            reference = {"path": normalized, "hashes": list(dict.fromkeys(hash_pattern.findall(line))),
                         "commit": commit, "blob": blob,
                         "section_refs": list(dict.fromkeys(section_refs)),
                         "pin_complete": bool(commit and normalized),
                         "context": line[:MAX_SNIPPET]}
            previous = found.get(key)
            if (previous is None or terms is None or pattern is None or
                    len(_matched_term_names(_fold(line[:MAX_SNIPPET]), pattern, terms)) >
                    len(_matched_term_names(_fold(previous["context"]), pattern, terms))):
                found[key] = reference
    references = list(found.values())
    if terms is not None and pattern is not None:
        references.sort(key=lambda item: (
            -len(_matched_term_names(_fold(item.get("context", "")), pattern, terms)),
            -bool(item.get("pin_complete")), str(item.get("path", "")),
        ))
        return references[:64]
    return references[:12]


def _read_pinned_source(root: pathlib.Path, reference: dict[str, Any],
                        cache: dict[tuple[str, str, str], tuple[str, bytes | None, str | None]]) -> tuple[str, bytes | None]:
    """Read only a safely typed, exact same-repository commit/path/blob pin."""
    commit, path, blob = (reference.get("commit"), reference.get("path"), reference.get("blob"))
    key = (str(commit or ""), str(path or ""), str(blob or ""))
    if key in cache:
        status, cached_bytes, derived_blob = cache[key]
        if derived_blob and blob is None:
            reference["blob"] = derived_blob
            reference["pin_complete"] = True
        return status, cached_bytes
    if (not re.fullmatch(r"[0-9a-f]{40}", str(commit or ""))
            or (blob is not None and not re.fullmatch(r"[0-9a-f]{40}", str(blob)))
            or not isinstance(path, str) or not path or "\\" in path or ":" in path
            or pathlib.PurePosixPath(path).is_absolute()
            or ".." in pathlib.PurePosixPath(path).parts
            or pathlib.PurePosixPath(path).as_posix() != path
            or pathlib.PurePosixPath(path).suffix.casefold() not in {".md", ".lean", ".json", ".csv", ".py", ".txt", ".toml"}):
        cache[key] = ("citation_only", None, None)
        return "citation_only", None
    try:
        git_env = os.environ.copy()
        git_env["GIT_NO_LAZY_FETCH"] = "1"
        oid = subprocess.run(["git", "rev-parse", f"{commit}:{path}"], cwd=root,
                             capture_output=True, text=True, encoding="utf-8", timeout=5,
                             env=git_env)
        if oid.returncode:
            cache[key] = ("external_reference_only", None, None)
            return "external_reference_only", None
        resolved_blob = oid.stdout.strip().lower()
        if blob is not None and resolved_blob != blob.lower():
            cache[key] = ("pin_mismatch", None, resolved_blob)
            return "pin_mismatch", None
        if blob is None:
            reference["blob"] = resolved_blob
            reference["pin_complete"] = True
        data = subprocess.run(["git", "cat-file", "blob", f"{commit}:{path}"], cwd=root,
                              capture_output=True, timeout=5, env=git_env)
        if data.returncode or len(data.stdout) > 4_000_000:
            cache[key] = ("external_reference_only", None, None)
            return "external_reference_only", None
        cache[key] = ("pinned_snapshot", data.stdout, resolved_blob)
    except (OSError, subprocess.SubprocessError):
        cache[key] = ("external_reference_only", None, None)
    status, cached_bytes, derived_blob = cache[key]
    if derived_blob and blob is None:
        reference["blob"] = derived_blob
        reference["pin_complete"] = True
    return status, cached_bytes


def _term_pattern(terms: list[tuple[str, tuple[str, ...]]]) -> re.Pattern[str]:
    alternatives = []
    for index, (_, variants) in enumerate(terms):
        values = sorted(set(variants), key=lambda value: (-len(value), value))
        alternatives.append(f"(?P<t{index}>" + "|".join(re.escape(value) for value in values) + ")")
    return re.compile("|".join(alternatives)) if alternatives else re.compile(r"(?!)")


def _build_multi_pattern_matcher(
        variant_queries: dict[str, list[tuple[int, str]]]
) -> tuple[list[dict[str, int]], list[int], list[list[tuple[int, str]]]]:
    """Build an Aho-Corasick matcher for all folded query variants."""
    transitions: list[dict[str, int]] = [{}]
    failures = [0]
    outputs: list[list[tuple[int, str]]] = [[]]
    for variant, query_names in variant_queries.items():
        state = 0
        for character in variant:
            target = transitions[state].get(character)
            if target is None:
                target = len(transitions)
                transitions[state][character] = target
                transitions.append({})
                failures.append(0)
                outputs.append([])
            state = target
        outputs[state].extend(query_names)

    queue = list(transitions[0].values())
    offset = 0
    while offset < len(queue):
        state = queue[offset]
        offset += 1
        for character, target in transitions[state].items():
            failure = failures[state]
            while failure and character not in transitions[failure]:
                failure = failures[failure]
            failures[target] = transitions[failure].get(character, 0)
            outputs[target].extend(outputs[failures[target]])
            outputs[target] = list(dict.fromkeys(outputs[target]))
            queue.append(target)
    return transitions, failures, outputs


def _multi_pattern_matches(
        text: str,
        matcher: tuple[list[dict[str, int]], list[int], list[list[tuple[int, str]]]],
) -> dict[int, set[str]]:
    """Return every query term present, including overlapping variants."""
    transitions, failures, outputs = matcher
    state = 0
    matched: dict[int, set[str]] = {}
    for character in text:
        while state and character not in transitions[state]:
            state = failures[state]
        state = transitions[state].get(character, 0)
        for query_index, name in outputs[state]:
            matched.setdefault(query_index, set()).add(name)
    return matched


def _matched_term_names(text: str, pattern: re.Pattern[str],
                        terms: list[tuple[str, tuple[str, ...]]]) -> set[str]:
    group_names = {f"t{index}": name for index, (name, _) in enumerate(terms)}
    return {group_names[match.lastgroup] for match in pattern.finditer(text)
            if match.lastgroup in group_names}


def _line_evidence(content: str, terms: list[tuple[str, tuple[str, ...]]],
                   pattern: re.Pattern[str]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    heading = ""
    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+", stripped):
            heading = stripped
        folded_line = _fold(line)
        matched_names = _matched_term_names(folded_line, pattern, terms)
        matched = [name for name, _ in terms if name in matched_names]
        if matched:
            evidence.append({"line": line_number, "heading": heading,
                             "matched_terms": matched,
                             "text": stripped[:MAX_SNIPPET],
                             "kind": "direct_content"})
    evidence.sort(key=lambda row: (-len(row["matched_terms"]), len(row["text"]), row["line"]))
    return evidence[:20]


def _source_header_owner_declarations(content: str) -> list[dict[str, Any]]:
    """Return only explicitly labelled owner fields from the document header.

    These source-authored statements are useful provenance, but are not
    assembly ownership records or independent owner validation.
    """
    pattern = re.compile(r"^\s*\*\*Existing owner:\*\*\s*(.+?)\s*$", re.IGNORECASE)
    declarations = []
    for line_number, line in enumerate(content.splitlines()[:40], start=1):
        match = pattern.match(line)
        if match:
            declarations.append({
                "line": line_number,
                "field": "Existing owner",
                "value": match.group(1),
                "status": "source_document_declaration_only",
            })
    return declarations


def _candidate_record(rel: str, content: str, terms: list[tuple[str, tuple[str, ...]]],
                      *, origin: str, source_refs: list[dict[str, Any]] | None = None,
                      commit: str | None = None, blob: str | None = None,
                      content_sha256: str | None = None,
                      pattern: re.Pattern[str] | None = None,
                      include_evidence: bool = True,
                      prioritize_verified_pin: bool = False,
                      ) -> tuple[float, dict[str, Any]] | None:
    file_title = pathlib.PurePosixPath(rel).stem
    pattern = pattern or _term_pattern(terms)
    content_matches = _matched_term_names(_fold(content), pattern, terms)
    title_matches = _matched_term_names(_fold(file_title.replace("_", " ").replace("-", " ")),
                                        pattern, terms)
    matched_names = content_matches | title_matches
    term_present = {name: name in matched_names for name, _ in terms}
    hits = sum(term_present.values())
    min_hits = 1 if len(terms) <= 3 else max(2, (len(terms) + 3) // 4)
    if hits < min_hits:
        return None
    evidence = _line_evidence(content, terms, pattern) if include_evidence else []
    if not evidence and title_matches:
        evidence = [{"line": None, "heading": "", "matched_terms": [
            name for name, _ in terms if name in title_matches],
            "text": f"Filename: {file_title}", "kind": "filename_only"}]
    direct = bool(content_matches)
    record = {"kind": "text-candidate", "key": rel if origin == "workspace" else f"{rel}@{commit}",
              "label": " | ".join(row["text"] for row in evidence[:3])[:MAX_SNIPPET],
              "source": rel, "source_sha256": content_sha256 or hashlib.sha256(content.encode("utf-8")).hexdigest(),
              "source_refs": source_refs or [], "matched_terms": hits,
              "matched_term_names": [name for name, present in term_present.items() if present],
              "query_terms": len(terms), "source_origin": origin if direct else "filename_only",
              "direct_content": direct, "evidence_lines": evidence}
    header_owner_declarations = _source_header_owner_declarations(content)
    if header_owner_declarations:
        record["source_header_owner_declarations"] = header_owner_declarations
    if commit:
        record["source_commit"] = commit
    if blob:
        record["source_blob"] = blob
    score = hits / len(terms) + _owner_bonus(rel) + _filename_bonus(rel, terms)
    if origin == "pinned_snapshot" and prioritize_verified_pin:
        # A verified commit/path/blob with direct matching content is a
        # primary source surface. Prioritize it in the narrow user-facing
        # card window, without treating the pin as owner validation or
        # semantic acceptance. Expanded searches keep lexical evidence order.
        score += VERIFIED_PINNED_SOURCE_BONUS
    return score, record


def full_text_search_many(root: pathlib.Path, queries: list[str],
                          limit: int = MAX_SEARCH_RESULTS) -> list[list[dict[str, Any]]]:
    """Search bilingual text once, then verify exact pins for ranked candidates."""
    raw_terms_by_query = [_query_terms(query) for query in queries]
    terms_by_query = []
    for terms in raw_terms_by_query:
        informative = [item for item in terms
                       if not any(item[0].startswith(broad) for broad in _LOW_INFORMATION_TERMS)]
        min_hits = 1 if len(terms) <= 3 else max(2, (len(terms) + 3) // 4)
        terms_by_query.append(informative if len(informative) >= min_hits else terms)
    patterns_by_query = [_term_pattern(terms) for terms in terms_by_query]
    variant_queries: dict[str, list[tuple[int, str]]] = {}
    for index, terms in enumerate(terms_by_query):
        for name, variants in terms:
            for variant in variants:
                variant_queries.setdefault(variant, []).append((index, name))
    unique_variants = sorted(variant_queries)
    if not unique_variants:
        return [[] for _ in queries]
    matcher = _build_multi_pattern_matcher(variant_queries)
    roots = [name for name in TEXT_ROOTS if (root / name).is_dir()]
    if not roots:
        return [[] for _ in queries]
    text_globs = ["-g", "*.md", "-g", "*.lean", "-g", "*.json", "-g", "*.csv",
                  "-g", "*.py", "-g", "*.toml"]
    rg_query = ["rg", "--json", "--ignore-case", "--fixed-strings", *text_globs]
    for term in unique_variants:
        rg_query.extend(["-e", term])
    text_matches = subprocess.run(
        [*rg_query, *roots], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if text_matches.returncode not in (0, 1):
        raise RuntimeError(f"rg text search failed ({text_matches.returncode}): {text_matches.stderr}")

    content_groups_by_query: list[dict[str, set[str]]] = [{} for _ in queries]
    for event_text in text_matches.stdout.splitlines():
        try:
            event = json.loads(event_text)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "match":
            continue
        data = event.get("data", {})
        raw_path = data.get("path", {}).get("text")
        if not raw_path:
            continue
        if raw_path.replace("\\", "/").startswith(DERIVED_TEXT_EXCLUDED_PREFIXES):
            continue
        # ripgrep reports non-overlapping submatches. In a batched search, a
        # shorter term from another query can hide an overlapping declaration
        # name, so recover each query's terms from the whole matching line.
        # Match every query variant in one pass over this line. This retains
        # overlapping terms without rescanning the line for every query.
        line_text = _fold(data.get("lines", {}).get("text", ""))
        if not line_text:
            continue
        for index, matched_names in _multi_pattern_matches(line_text, matcher).items():
            content_groups_by_query[index].setdefault(raw_path, set()).update(matched_names)

    all_files = subprocess.run(["rg", "--files", *text_globs, *roots], cwd=root,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
    if all_files.returncode not in (0, 1):
        raise RuntimeError(f"rg file listing failed ({all_files.returncode}): {all_files.stderr}")
    all_text_paths = [
        path for path in all_files.stdout.splitlines()
        if path and not path.replace("\\", "/").startswith(
            DERIVED_TEXT_EXCLUDED_PREFIXES
        )
    ]
    candidates_by_query: list[list[tuple[float, str, dict[str, Any]]]] = [[] for _ in queries]
    for index, terms in enumerate(terms_by_query):
        if not terms:
            continue
        pattern = patterns_by_query[index]
        content_groups = content_groups_by_query[index]
        candidate_paths = set(content_groups)
        for raw_rel in all_text_paths:
            stem = pathlib.PurePosixPath(raw_rel.replace("\\", "/")).stem
            title_groups = _matched_term_names(
                _fold(stem.replace("_", " ").replace("-", " ")), pattern, terms,
            )
            if title_groups:
                candidate_paths.add(raw_rel)
        min_hits = 1 if len(terms) <= 3 else max(2, (len(terms) + 3) // 4)
        for raw_rel in sorted(candidate_paths):
            rel = raw_rel.replace("\\", "/")
            if (rel in {"tools/proof_architecture.py", "tools/proof_architecture_cold_start.py"}
                    or rel.startswith("tools/test_")):
                continue
            content_groups_here = content_groups.get(raw_rel, set())
            file_title = pathlib.PurePosixPath(rel).stem.replace("_", " ").replace("-", " ")
            title_groups = _matched_term_names(_fold(file_title), pattern, terms)
            present = content_groups_here | title_groups
            if len(present) < min_hits:
                continue
            hits = len(present)
            record = {
                "kind": "text-candidate", "key": rel, "label": "",
                "source": rel, "source_sha256": None, "source_refs": [],
                "matched_terms": hits,
                "matched_term_names": [name for name, _ in terms if name in present],
                "query_terms": len(terms),
                "source_origin": "workspace" if content_groups_here else "filename_only",
                "direct_content": bool(content_groups_here), "evidence_lines": [],
            }
            score = hits / len(terms) + _owner_bonus(rel) + _filename_bonus(rel, terms)
            candidates_by_query[index].append((score, rel, record))

    pinned_cache: dict[tuple[str, str, str], tuple[str, bytes | None, str | None]] = {}
    pinned_seen: list[set[tuple[str, str, str]]] = [set() for _ in queries]
    results = []
    for index, candidates in enumerate(candidates_by_query):
        candidates.sort(key=lambda row: (-row[0], row[1]))
        terms = terms_by_query[index]
        pattern = patterns_by_query[index]
        # Reading pins is expensive. Only inspect references in the bounded
        # top-ranked candidate window; the returned source itself must still
        # pass its exact commit/path/blob and direct-content checks.
        pin_window = candidates[:max(MIN_PIN_VERIFICATION_WINDOW, limit)]
        pinned_candidates: list[tuple[float, str, dict[str, Any]]] = []
        for score, rel, record in pin_window:
            path = root / pathlib.Path(rel)
            try:
                if path.stat().st_size > 4_000_000:
                    continue
                source_bytes = path.read_bytes()
                content = source_bytes.decode("utf-8-sig", errors="replace")
            except OSError:
                continue
            record["source_sha256"] = hashlib.sha256(source_bytes).hexdigest()
            header_owner_declarations = _source_header_owner_declarations(content)
            if header_owner_declarations:
                record["source_header_owner_declarations"] = header_owner_declarations
            evidence = _line_evidence(content, terms, pattern)
            if evidence:
                record["evidence_lines"] = evidence
                record["label"] = " | ".join(row["text"] for row in evidence[:3])[:MAX_SNIPPET]
            elif not record["direct_content"]:
                evidence = [{"line": None, "heading": "",
                             "matched_terms": record["matched_term_names"],
                             "text": f"Filename: {pathlib.PurePosixPath(rel).stem}",
                             "kind": "filename_only"}]
                record["evidence_lines"] = evidence
                record["label"] = evidence[0]["text"]
            matching_lines = [line for line in content.splitlines()
                              if pattern.search(_fold(line))]
            refs = _source_references(matching_lines, terms, pattern)
            refs.sort(key=lambda item: (
                -len(_matched_term_names(_fold(str(item.get("context", ""))), pattern, terms)),
                -sum(any(variant in _fold(str(item.get("path", ""))) for variant in variants)
                     for _, variants in terms),
                -bool(item.get("pin_complete")), str(item.get("path", "")),
            ))
            for reference in refs:
                reference["pin_status"] = "not_followed_bounded_search"
            record["source_refs"] = refs

            # Follow only exact same-repository commit/path/blob pins found in
            # matching source lines. A citation alone is retained as such and
            # never counts as direct source content.
            followed = 0
            for reference in refs:
                if not reference.get("pin_complete") or followed >= 8:
                    continue
                followed += 1
                pin_key = (str(reference.get("commit") or ""),
                           str(reference.get("path") or ""),
                           str(reference.get("blob") or ""))
                if pin_key in pinned_seen[index]:
                    continue
                pinned_seen[index].add(pin_key)
                pin_status, pinned_bytes = _read_pinned_source(root, reference, pinned_cache)
                reference["pin_status"] = pin_status
                pinned_rel = str(reference.get("path") or "")
                if pinned_bytes is not None:
                    pinned_text = pinned_bytes.decode("utf-8-sig", errors="replace")
                    pinned_match = _candidate_record(
                        pinned_rel, pinned_text, terms, origin="pinned_snapshot",
                        commit=reference["commit"], blob=reference["blob"],
                        content_sha256=hashlib.sha256(pinned_bytes).hexdigest(),
                        pattern=pattern, include_evidence=True,
                        prioritize_verified_pin=limit <= MAX_SEARCH_RESULTS,
                    )
                    if pinned_match is not None:
                        pinned_score, pinned_record = pinned_match
                        pinned_record["pin_status"] = "verified"
                        pinned_lines = [pinned_text.splitlines()[row["line"] - 1]
                                        for row in pinned_record["evidence_lines"]
                                        if row.get("line") is not None]
                        pinned_record["source_refs"] = _source_references(pinned_lines)
                        pinned_candidates.append(
                            (pinned_score, pinned_record["key"], pinned_record)
                        )
                    else:
                        pinned_candidates.append((
                            score - 0.50, f"{pinned_rel}@{reference['commit']}",
                            {"kind": "text-candidate", "key": f"{pinned_rel}@{reference['commit']}",
                             "label": "Exact pinned source loaded; its content did not match this query.",
                             "source": pinned_rel, "source_sha256": hashlib.sha256(pinned_bytes).hexdigest(),
                             "source_refs": [reference], "matched_terms": 0,
                             "matched_term_names": [], "query_terms": len(terms),
                             "source_origin": "pinned_snapshot", "direct_content": False,
                             "pin_status": "verified_no_content_match", "source_commit": reference["commit"],
                             "source_blob": reference["blob"], "evidence_lines": []}
                        ))
                else:
                    pinned_candidates.append((
                        score - 0.50, f"{pinned_rel}@{reference.get('commit') or 'unversioned'}",
                        {"kind": "text-candidate",
                         "key": f"{pinned_rel}@{reference.get('commit') or 'unversioned'}",
                         "label": f"Reference only; pinned source status: {pin_status}.",
                         "source": pinned_rel, "source_refs": [reference],
                         "matched_terms": 0, "matched_term_names": [],
                         "query_terms": len(terms), "source_origin": "citation_only",
                         "direct_content": False, "pin_status": pin_status,
                         "source_commit": reference.get("commit"),
                         "source_blob": reference.get("blob"), "evidence_lines": []}
                    ))
        combined = list(candidates)
        combined.extend(pinned_candidates)
        combined.sort(key=lambda row: (-row[0], row[1]))
        results.append([record for _, _, record in combined[:limit]])
    return results


def full_text_search(root: pathlib.Path, query: str,
                     limit: int = MAX_SEARCH_RESULTS) -> list[dict[str, Any]]:
    """Return bounded text candidates from books, registry, and Lean sources."""
    return full_text_search_many(root, [query], limit)[0]


def _search_summary(item: dict[str, Any]) -> dict[str, Any]:
    """Expose typed fields from exact authority matches; use `show` for detail."""
    record = item.get("record", {})
    summary = {"kind": item.get("kind"), "key": item.get("key"),
               "label": str(item.get("label", ""))[:MAX_SNIPPET],
               "source": item.get("source")}
    for key in (
        "owner", "statement", "interface", "outcome", "scope_level", "scope",
        "hypotheses", "hypothesis_map", "consumer", "consumer_location",
        "result", "obligation", "method", "review", "carrier", "action",
        "variations", "normalization", "refinement", "role", "lean_file",
        "referenced_by", "status", "failure_meaning",
    ):
        if key in record:
            summary[key] = record[key]
    evidence = record.get("evidence")
    if isinstance(evidence, list):
        summary["evidence"] = evidence[:MAX_SEARCH_SOURCE_REFS]
        summary["evidence_omitted"] = max(0, len(evidence) - MAX_SEARCH_SOURCE_REFS)
    return summary


def _normalized_source_path(value: Any) -> str:
    path = pathlib.PurePosixPath(str(value or "").replace("\\", "/")).as_posix()
    return path[2:] if path.startswith("./") else path


def _declared_source_links(dataset: dict[str, Any], source_path: str) -> dict[str, Any]:
    """Join only exact source-path fields to their existing typed records.

    These are registry links, not semantic validation of the source or its
    owner. Missing links stay explicit instead of being inferred from prose.
    """
    source_path = _normalized_source_path(source_path)
    results = dataset.get("assembly", {}).get("results", [])
    applications = dataset.get("assembly", {}).get("applications", [])
    attempts = dataset.get("assembly", {}).get("attempts", [])
    interface_rows = _as_rows(dataset.get("contract", {}).get("interfaces", []))
    obligation_rows = _as_rows(dataset.get("contract", {}).get("obligations", []))
    declared_results = []

    for result in results:
        evidence = [
            item for item in result.get("evidence", [])
            if isinstance(item, dict)
            and _normalized_source_path(item.get("path")) == source_path
        ]
        if not evidence:
            continue
        result_id = str(result.get("id", ""))
        interface_id = result.get("interface")
        interface_contract = next(
            (row for row in interface_rows if row.get("id") == interface_id), None
        )
        linked_applications = [
            row for row in applications if row.get("result") == result_id
        ]
        linked_attempts = [
            row for row in attempts if row.get("result") == result_id
        ]
        compact_applications = []
        for application in linked_applications[:MAX_DECLARED_SOURCE_APPLICATIONS]:
            obligation_id = application.get("obligation")
            obligation = next(
                (row for row in obligation_rows if row.get("id") == obligation_id), None
            )
            compact_applications.append({
                "id": application.get("id"),
                "obligation": obligation_id,
                "method": application.get("method"),
                "consumer_location": application.get("consumer_location"),
                "hypothesis_map": application.get("hypothesis_map"),
                "review": application.get("review"),
                "target_hypotheses": obligation.get("hypotheses") if obligation else None,
            })
        compact_attempts = [
            {key: row.get(key) for key in ("id", "work_key", "scope", "reopen_when", "review")
             if key in row}
            for row in linked_attempts[:MAX_DECLARED_SOURCE_ATTEMPTS]
        ]
        declared_results.append({
            "result_id": result_id,
            "owner": result.get("owner"),
            "statement": result.get("statement"),
            "interface": interface_id,
            "interface_contract": interface_contract,
            "outcome": result.get("outcome"),
            "scope_level": result.get("scope_level"),
            "hypotheses": result.get("hypotheses"),
            "reported_state": result.get("reported_state"),
            "evidence": evidence[:MAX_SEARCH_SOURCE_REFS],
            "evidence_omitted": max(0, len(evidence) - MAX_SEARCH_SOURCE_REFS),
            "declared_applications": compact_applications,
            "applications_omitted": max(
                0, len(linked_applications) - len(compact_applications)
            ),
            "scoped_attempts": compact_attempts,
            "attempts_omitted": max(0, len(linked_attempts) - len(compact_attempts)),
        })

    formal_support = []
    for row in dataset.get("formal_support", []):
        referenced = {
            _normalized_source_path(item)
            for item in str(row.get("referenced_by", "")).split(";")
            if item.strip()
        }
        if source_path in referenced:
            formal_support.append({
                "lean_module": row.get("lean_module"),
                "lean_file": row.get("lean_file"),
                "role": row.get("role"),
                "link_basis": "exact member of formal_support.referenced_by",
                "status": "metadata_locator_only",
            })

    owners = sorted({str(row["owner"]) for row in declared_results if row.get("owner")})
    if owners:
        owner_status = "declared_by_exact_assembly_evidence_link"
    elif declared_results:
        owner_status = "exact_assembly_evidence_link_without_owner"
    else:
        owner_status = "no_exact_assembly_owner_link"
    return {
        "source_path": source_path,
        "link_basis": "exact source-path field match only",
        "owner_status": owner_status,
        "owners": owners,
        "assembly_results": declared_results[:MAX_DECLARED_SOURCE_RESULTS],
        "assembly_results_omitted": max(
            0, len(declared_results) - MAX_DECLARED_SOURCE_RESULTS
        ),
        "formal_support_locators": formal_support[:MAX_FORMAL_SUPPORT_LOCATORS],
        "formal_support_locators_omitted": max(
            0, len(formal_support) - MAX_FORMAL_SUPPORT_LOCATORS
        ),
    }


def _search_candidate_summary(item: dict[str, Any],
                              dataset: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a compact search card while preserving exact pin coordinates."""
    references = item.get("source_refs", [])
    evidence = item.get("evidence_lines", [])
    compact_refs = []
    for reference in references[:MAX_SEARCH_SOURCE_REFS]:
        hashes = reference.get("hashes", [])
        compact = {key: reference.get(key) for key in
                   ("path", "commit", "blob", "section_refs", "pin_complete")}
        compact["hashes"] = hashes[:4]
        if len(hashes) > 4:
            compact["hashes_omitted"] = len(hashes) - 4
        context = reference.get("context")
        if context:
            compact["context"] = str(context)[:MAX_SEARCH_DETAIL_CHARS]
        compact_refs.append(compact)
    compact_evidence = [
        {"line": row.get("line"), "heading": str(row.get("heading", ""))[:MAX_SEARCH_DETAIL_CHARS],
         "matched_terms": row.get("matched_terms", []),
         "text": str(row.get("text", ""))[:MAX_SEARCH_DETAIL_CHARS],
         "kind": row.get("kind")}
        for row in evidence[:MAX_SEARCH_EVIDENCE]
    ]
    summary = {
        "kind": item.get("kind"), "key": item.get("key"),
        "label": str(item.get("label", ""))[:MAX_SEARCH_DETAIL_CHARS],
        "source": item.get("source"), "source_sha256": item.get("source_sha256"),
        "source_origin": item.get("source_origin"),
        "direct_content": item.get("direct_content"),
        "matched_terms": item.get("matched_terms"),
        "matched_term_names": item.get("matched_term_names", []),
        "query_terms": item.get("query_terms"),
        "evidence_lines": compact_evidence,
        "evidence_lines_omitted": max(0, len(evidence) - len(compact_evidence)),
        "source_refs": compact_refs,
        "source_refs_omitted": max(0, len(references) - len(compact_refs)),
    }
    for key in ("source_commit", "source_blob"):
        if item.get(key):
            summary[key] = item[key]
    if item.get("pin_status"):
        summary["pin_status"] = item["pin_status"]
    if item.get("source_header_owner_declarations"):
        summary["source_header_owner_declarations"] = item[
            "source_header_owner_declarations"
        ]
    if dataset is not None and item.get("source"):
        summary["declared_source_links"] = _declared_source_links(
            dataset, str(item["source"])
        )
    return summary


def find_exact(dataset: dict[str, Any], key: str) -> list[dict[str, Any]]:
    needle = key.casefold()

    def exact_value(value: Any) -> bool:
        if isinstance(value, str):
            return value.casefold() == needle
        if isinstance(value, dict):
            return any(exact_value(child) for child in value.values())
        if isinstance(value, list):
            return any(exact_value(child) for child in value)
        return False

    hits = []
    for item in records(dataset):
        candidates = [str(item.get("key", "")), *item.get("search_terms", [])]
        if (any(str(value).casefold() == needle for value in candidates if value)
                or exact_value(item["record"])):
            hits.append(item)
    return hits


def source_file_view(root: pathlib.Path, key: str) -> dict[str, Any] | None:
    """Show an exact in-repository source path without treating it as a registry unit."""
    root_path = root.resolve()
    candidate = (root_path / key).resolve()
    try:
        candidate.relative_to(root_path)
    except ValueError:
        return None
    if not candidate.is_file() or candidate.suffix.casefold() not in {
        ".md", ".lean", ".json", ".csv", ".txt", ".py"
    }:
        return None
    data = candidate.read_bytes()
    return {"kind": "source-file", "path": candidate.relative_to(root_path).as_posix(),
            "size_bytes": len(data), "source_sha256": hashlib.sha256(data).hexdigest(),
            "content": data.decode("utf-8-sig", errors="replace")}


def _registry_assumption_ids(value: Any) -> list[str]:
    """Parse the existing claim-row assumption links without changing their authority."""
    return [part.strip() for part in re.split(r"[;,]", str(value or "")) if part.strip()]


def relation_view(dataset: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    """Return declared application and registry links without inferring semantic edges."""
    record = item["record"]
    result_id = record.get("id") if item["kind"] == "assembly-result" else None
    obligation_id = record.get("id") if item["kind"] == "obligation" else None
    applications = dataset["assembly"].get("applications", [])
    if item["kind"] == "application":
        related = [record]
        result_id = record.get("result")
        obligation_id = record.get("obligation")
    elif result_id:
        related = [a for a in applications if a.get("result") == result_id]
    elif obligation_id:
        related = [a for a in applications if a.get("obligation") == obligation_id]
    else:
        related = []
    attempts = [a for a in dataset["assembly"].get("attempts", [])
                if (result_id and a.get("result") == result_id)
                or (obligation_id and a.get("obligation") == obligation_id)]
    claim_id = record.get("claim_id") if item["kind"] == "claim-metadata" else None
    registered_assumptions = [assumption for assumption in dataset["assumptions"]
                              if claim_id and assumption.get("claim_id") == claim_id]
    assumptions_by_id = {
        str(assumption.get("assumption_id", "")): assumption
        for assumption in dataset["assumptions"]
        if assumption.get("assumption_id")
    }
    claim_assumption_links = [
        {
            "assumption_id": assumption_id,
            "resolution_status": "resolved" if assumption_id in assumptions_by_id else "unresolved",
            "assumption": assumptions_by_id.get(assumption_id),
            "assumption_owner_claim_id": (
                assumptions_by_id[assumption_id].get("claim_id")
                if assumption_id in assumptions_by_id else None
            ),
        }
        for assumption_id in _registry_assumption_ids(record.get("assumption_ids", ""))
    ] if claim_id else []
    conceptual_edges = [edge for edge in dataset["presuppositions"].get("edges", [])
                        if claim_id and (edge.get("claim") == claim_id or edge.get("presupposes") == claim_id)]
    result_record = next((result for result in dataset["assembly"].get("results", [])
                          if result.get("id") == result_id), None)
    obligation_record = next((obligation for obligation in _as_rows(
        dataset["contract"].get("obligations", []))
        if obligation.get("id") == obligation_id), None)
    target_interface_id = obligation_record.get("interface") if obligation_record else None
    target_interface = next((x["record"] for x in records(dataset)
                             if x["kind"] == "interface" and x["key"] == target_interface_id), None)
    return {
        "declared_applications": related,
        "declared_result": result_record,
        "target_obligation": obligation_record,
        "target_interface": target_interface,
        "registered_assumptions": registered_assumptions,
        "claim_assumption_links": claim_assumption_links,
        "scoped_attempts": attempts,
        "conceptual_presupposition_edges": conceptual_edges,
        "warning": (
            "Claim assumption IDs resolve to registry rows; this is separate from owner-claim "
            "links and does not type-check Lean propositions or establish independent scientific acceptance."
        ),
    }


def compiled_claim_reuse_view(dataset: dict[str, Any], item: dict[str, Any],
                             lean_inventory: Any, import_root: str) -> dict[str, Any]:
    """Join one claim's exact name locators to compiled declarations and proof dependencies."""
    record = item["record"]
    claim_id = str(record.get("claim_id", ""))
    module = str(record.get("lean_module", ""))
    mappings: list[dict[str, Any]] = []
    names: list[str] = []
    for atom in _lean_atoms(record):
        candidates = lean_inventory.candidate_names(module, atom)
        mappings.append({"claim_id": claim_id, "module_locator": module,
                         "theorem_atom": atom, "candidate_names": candidates})
        names.extend(candidates)
    if not mappings:
        mappings.append({"claim_id": claim_id, "module_locator": module,
                         "theorem_atom": None, "candidate_names": []})
    names = list(dict.fromkeys(names))
    rows, collector_sha, lean_digest = (
        lean_inventory.run_inventory(names, import_root) if names else ([], None, None)
    )
    by_name = {str(row.get("name", "")): row for row in rows}
    resolved_rows: dict[str, dict[str, Any]] = {}
    locator_results = []
    for locator in mappings:
        resolved = []
        for candidate in locator["candidate_names"]:
            row = by_name.get(candidate)
            if row and row.get("exists"):
                row.setdefault("source_path", lean_inventory.module_source_path(row.get("module")))
                resolved_rows[candidate] = row
                resolved.append(row)
        locator_results.append({
            **locator,
            "resolution_status": "resolved" if resolved else "unresolved",
            "resolved_declarations": resolved,
        })
    # Keep the historical name-presence result and full declaration rows, but
    # classify owner matches separately using the shared inventory crosswalk.
    # The same declaration may occur under different locators, so owner flags
    # belong to the locator, not to the shared declaration object.
    owner_crosswalk = lean_inventory.claim_locator_crosswalk(mappings, rows)
    for locator_result, owner_result in zip(locator_results, owner_crosswalk["mappings"]):
        locator_result["owner_resolution_status"] = owner_result["resolution_status"]
        locator_result["declared_modules"] = owner_result["declared_modules"]
        locator_result["owner_resolution_matches"] = owner_result["matches"]
    declared_claim_locators: dict[str, list[dict[str, str]]] = {}
    for claim in dataset["claims"]:
        target_claim = str(claim.get("claim_id", ""))
        target_module = str(claim.get("lean_module", ""))
        for atom in _lean_atoms(claim):
            for candidate in lean_inventory.candidate_names(target_module, atom):
                target = {"claim_id": target_claim, "theorem_atom": atom,
                          "module_locator": target_module}
                values = declared_claim_locators.setdefault(candidate, [])
                if target not in values:
                    values.append(target)
    dependency_claim_links = []
    for name, row in resolved_rows.items():
        for dependency in row.get("proof_dependencies", []):
            targets = declared_claim_locators.get(dependency, [])
            if targets:
                dependency_claim_links.append({
                    "source_claim_id": claim_id,
                    "source_declaration": name,
                    "dependency_declaration": dependency,
                    "target_claim_locators": targets,
                    "relation": "compiled-proof-dependency-to-claim-locator",
                })
    return {
        "claim_id": claim_id,
        "claim_locator_mappings": locator_results,
        "compiled_declarations": list(resolved_rows.values()),
        "compiled_dependency_claim_links": dependency_claim_links,
        "declared_metadata_relations": relation_view(dataset, item),
        "collector_sha256": collector_sha,
        "lean_source_digest": lean_digest,
        "public_import_root": import_root,
        "interpretation": (
            "Claim theorem strings are candidate-name locators. Compiled declaration presence and "
            "reported Lean proof dependencies are separate evidence. Name presence does not imply "
            "that a declaration is owned by a listed module; see owner_resolution_status and "
            "owner_resolution_matches. A dependency joined to another "
            "claim locator is a candidate crosswalk only; registry application links, conceptual "
            "edges, and semantic claim acceptance are not inferred from name matches."
        ),
    }


def reuse_view(dataset: dict[str, Any], key: str, *,
               lean_inventory: Any | None = None,
               import_root: str = "D0.All") -> dict[str, Any]:
    """Show declared reuse relations and optionally join claim locators to compiled Lean evidence."""
    hits = find_exact(dataset, key)
    result = {"key": key, "matches": [
        {"item": item, **relation_view(dataset, item)} for item in hits
    ], "snapshot_commit": dataset["snapshot_commit"],
        "source_digests": dataset["source_digests"]}
    if lean_inventory is not None:
        claims = [item for item in hits
                  if item["kind"] == "claim-metadata" and item["key"] == key]
        result["compiled_claim_reuse"] = [
            compiled_claim_reuse_view(dataset, item, lean_inventory, import_root)
            for item in claims
        ]
        alias_reuse = []
        claim_items = {item["key"]: item for item in records(dataset)
                       if item["kind"] == "claim-metadata"}
        for alias in hits:
            if alias["kind"] != "alias-lookup" or alias["key"] != key:
                continue
            alias_record = alias["record"]
            target_id = str(alias_record.get("canonical_claim_id", ""))
            if alias_record.get("kind") != "CANONICAL_TARGET" or not target_id:
                continue
            target = claim_items.get(target_id)
            alias_item = {
                "alias_id": alias["key"],
                "alias_kind": alias_record.get("kind"),
                "canonical_claim_id": target_id,
                "target_claim_found": target is not None,
            }
            if target is not None:
                claim_record = target["record"]
                alias_item["canonical_claim"] = {
                    field: claim_record.get(field)
                    for field in (
                        "claim_id", "book", "section", "lean_module", "lean_theorem",
                        "lean_status", "uses_bridge_assumptions", "assumption_ids",
                        "release_status",
                    )
                }
                alias_item["compiled_claim_reuse"] = compiled_claim_reuse_view(
                    dataset, target, lean_inventory, import_root
                )
            alias_reuse.append(alias_item)
        result["compiled_claim_alias_reuse"] = alias_reuse
        if alias_reuse:
            targets_found = all(row["target_claim_found"] for row in alias_reuse)
            if targets_found:
                alias_status = "controlled_alias_candidate"
                alias_interpretation = (
                    "The alias registry explicitly points this key to a canonical claim ID. "
                    "The target's compiled declarations remain locator evidence; no semantic "
                    "equivalence, application, or claim acceptance is inferred."
                )
            else:
                alias_status = "controlled_alias_target_missing"
                alias_interpretation = (
                    "The alias registry points to a canonical claim ID that is absent from "
                    "claims.csv. No Lean query is made for the unresolved alias target."
                )
            result["compiled_claim_alias_reuse_status"] = (
                "exact_claim_and_controlled_alias" if claims and targets_found
                else "exact_claim_and_alias_target_missing" if claims
                else alias_status
            )
            result["compiled_claim_alias_reuse_interpretation"] = (
                "The exact claim and the explicit alias target are reported separately; "
                "the alias does not replace or merge the exact claim. " + alias_interpretation
                if claims else alias_interpretation
            )
            if not claims:
                result["compiled_claim_reuse_status"] = alias_status
                result["compiled_claim_reuse_interpretation"] = alias_interpretation
        elif not claims:
            result["compiled_claim_reuse_status"] = "key_is_not_an_exact_claim_id"
            result["compiled_claim_reuse_interpretation"] = (
                "Use a claims.csv claim ID or an explicit CANONICAL_TARGET alias for "
                "the joined claim-to-declaration view. Lookup-only aliases, assembly "
                "results, and applications retain their separate relation views."
            )
    return result


def _safe_repository_path(root: pathlib.Path, relative: str) -> pathlib.Path | None:
    """Resolve a repository-relative evidence path without allowing traversal."""
    pure = pathlib.PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        return None
    candidate = (root / pathlib.Path(*pure.parts)).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _pinned_evidence_view(root: pathlib.Path, evidence: dict[str, Any]) -> dict[str, Any]:
    """Verify immutable Git bytes and compare them with the current working source."""
    relative = str(evidence.get("path", ""))
    ref = str(evidence.get("ref", ""))
    expected = str(evidence.get("sha256", "")).lower()
    candidate = _safe_repository_path(root, relative)
    path_is_safe = candidate is not None
    expected_is_sha = bool(re.fullmatch(r"[0-9a-f]{64}", expected))
    pinned_digest = None
    pin_status = "unverified"
    if not path_is_safe:
        pin_status = "unsafe_or_missing_path"
    elif not re.fullmatch(r"[0-9a-fA-F]{40}", ref):
        pin_status = "missing_or_noncommit_ref"
    elif not expected_is_sha:
        pin_status = "missing_or_invalid_sha256"
    else:
        proc = subprocess.run(
            ["git", "cat-file", "blob", f"{ref}:{relative}"], cwd=root,
            capture_output=True,
        )
        if proc.returncode:
            pin_status = "pinned_blob_unavailable"
        else:
            pinned_digest = hashlib.sha256(proc.stdout).hexdigest()
            pin_status = "verified" if pinned_digest == expected else "pinned_sha256_mismatch"
    current_digest = None
    if candidate is not None and candidate.is_file():
        current_digest = sha256(candidate)
    current_status = (
        "matches_pin" if pin_status == "verified" and current_digest == expected
        else "changed_since_pin" if pin_status == "verified" and current_digest is not None
        else "source_missing" if current_digest is None
        else "unverified_pin"
    )
    module = None
    prefix = "03_FORMALIZATION/D0/"
    normalized = pathlib.PurePosixPath(relative).as_posix()
    if normalized.startswith(prefix) and normalized.endswith(".lean"):
        module = "D0." + normalized[len(prefix):-len(".lean")].replace("/", ".")
    return {
        "ref": ref or None,
        "path": relative or None,
        "expected_sha256": expected or None,
        "pinned_blob_sha256": pinned_digest,
        "pin_status": pin_status,
        "current_source_sha256": current_digest,
        "current_source_status": current_status,
        "current_module_locator": module,
        "direct_formal_module_source": module is not None,
    }


@functools.lru_cache(maxsize=512)
def _pinned_markdown_text(root: str, ref: str, path: str) -> str:
    return subprocess.check_output(
        ["git", "cat-file", "blob", f"{ref}:{path}"], cwd=root
    ).decode("utf-8", errors="replace")


def _markdown_sections(text: str) -> list[tuple[int, str, str]]:
    """Return pinned ATX heading sections as (line, title, body) tuples."""
    sections: list[tuple[int, str, str]] = []
    current_line: int | None = None
    current_title = ""
    current_body: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        fence_char, fence_length, is_fence_line = _markdown_fence_transition(
            line, fence_char, fence_length
        )
        if is_fence_line:
            if current_line is not None:
                current_body.append(line)
            continue
        heading = None if fence_char is not None else re.match(
            r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line
        )
        if heading:
            if current_line is not None:
                sections.append((current_line, current_title, "\n".join(current_body)))
            current_line = line_number
            current_title = heading.group(2).strip()
            current_body = []
        elif current_line is not None:
            current_body.append(line)
    if current_line is not None:
        sections.append((current_line, current_title, "\n".join(current_body)))
    return sections


def _markdown_fence_transition(
    line: str, fence_char: str | None, fence_length: int
) -> tuple[str | None, int, bool]:
    """Track Markdown fences; a closing marker may have trailing whitespace only."""
    marker_match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
    if not marker_match:
        return fence_char, fence_length, False
    marker, suffix = marker_match.groups()
    if fence_char is None:
        if marker[0] == "`" and "`" in suffix:
            return None, 0, False
        return marker[0], len(marker), True
    if (marker[0] == fence_char and len(marker) >= fence_length
            and not suffix.strip()):
        return None, 0, True
    return fence_char, fence_length, True


def _locator_terms(text: str) -> set[str]:
    tokens = re.findall(r"(?u)[^\W_]{3,}|(?<!\w)\d{2,}(?!\w)", text.casefold())
    return {token for token in tokens if token not in SOURCE_LOCATOR_STOPWORDS}


def _ranked_section_candidates(root: pathlib.Path, evidence: dict[str, Any],
                                pin: dict[str, Any], source_file_key: str | None,
                                statement: str) -> list[dict[str, Any]]:
    path = pin.get("path")
    ref = pin.get("ref")
    if (not source_file_key or pin.get("pin_status") != "verified"
            or not isinstance(path, str) or not path.lower().endswith((".md", ".markdown"))):
        return []
    query_terms = _locator_terms(statement)
    if not query_terms:
        return []
    text = _pinned_markdown_text(str(root), str(ref), path)
    minimum_matches = min(len(query_terms), max(3, (len(query_terms) + 4) // 5))
    candidates = []
    for line, title, body in _markdown_sections(text):
        shared = query_terms & _locator_terms(title + "\n" + body)
        if len(shared) < minimum_matches:
            continue
        section_ref = f"L{line}: {title}"
        candidates.append({
            "candidate_source_unit_key": f"{source_file_key}#{section_ref}",
            "section_ref": section_ref,
            "heading": title,
            "heading_line": line,
            "matched_terms": sorted(shared),
            "query_term_count": len(query_terms),
            "overlap_fraction": round(len(shared) / len(query_terms), 4),
            "review_status": "unreviewed_lexical_candidate",
        })
    candidates.sort(key=lambda item: (
        -item["overlap_fraction"], -len(item["matched_terms"]), item["heading_line"]
    ))
    return candidates[:3]


def _source_locator_crosswalk(root: pathlib.Path, evidence: dict[str, Any],
                              pin: dict[str, Any], statement: str) -> dict[str, Any]:
    """Expose a pinned file key without treating a file as a mathematical unit."""
    ref = pin.get("ref")
    path = pin.get("path")
    valid_commit = isinstance(ref, str) and bool(re.fullmatch(r"[0-9a-fA-F]{40}", ref))
    safe_path = isinstance(path, str) and pin.get("pin_status") != "unsafe_or_missing_path"
    verified_pin = pin.get("pin_status") == "verified"
    # A locator is exact only when the immutable bytes behind the commit/path
    # pair have been checked against the recorded digest. The current checkout
    # may be missing or newer; that does not invalidate a verified historical
    # pin, but an unavailable or mismatched blob cannot name an exact source.
    source_file_key = (
        f"source:{ref}:{path}"
        if valid_commit and safe_path and verified_pin else None
    )
    raw_sections: list[Any] = []
    for field in ("section", "section_ref", "sections", "section_refs"):
        value = evidence.get(field)
        if isinstance(value, str):
            raw_sections.append(value)
        elif isinstance(value, list):
            raw_sections.extend(value)
    sections = []
    for value in raw_sections:
        if isinstance(value, str):
            section = value.strip().lstrip("#").strip()
            if section and section not in sections:
                sections.append(section)
    exact_unit_keys = (
        [f"{source_file_key}#{section}" for section in sections]
        if source_file_key else []
    )
    section_candidates = (
        [] if sections else _ranked_section_candidates(
            root, evidence, pin, source_file_key, statement
        )
    )
    return {
        "source_file_key": source_file_key,
        "exact_unit_key_candidates": exact_unit_keys,
        "section_refs": sections,
        "ranked_section_candidates": section_candidates,
        "unit_locator_status": (
            "candidate_section_keys_need_review" if exact_unit_keys
            else "section_reference_without_verified_source_pin" if sections
            else "ranked_heading_candidates_need_review" if section_candidates
            else "section_locator_not_recorded" if source_file_key
            else "source_pin_unverified"
        ),
        "pin_status": pin.get("pin_status"),
        "current_source_status": pin.get("current_source_status"),
        "snapshot_path": evidence.get("snapshot"),
    }


def _module_source_path(module: str) -> str:
    return "03_FORMALIZATION/" + module.replace(".", "/") + ".lean"


def _formal_support_candidates(dataset: dict[str, Any], module: str,
                               evidence_path: str) -> list[dict[str, str]]:
    evidence_suffix = evidence_path.removeprefix("03_FORMALIZATION/")
    matches = []
    for row in dataset["formal_support"]:
        modules = [part.strip() for part in str(row.get("lean_module", "")).split(";")
                   if part.strip()]
        files = [part.strip().replace("\\", "/")
                 for part in str(row.get("lean_file", "")).split(";") if part.strip()]
        if module in modules or evidence_path in files or evidence_suffix in files:
            matches.append({**row, "relation": "module_or_source_co-location_candidate"})
    return matches


def _claim_locator_candidates(dataset: dict[str, Any], declaration_names: set[str],
                              lean_inventory: Any) -> list[dict[str, str]]:
    matches = []
    for claim in dataset["claims"]:
        module = str(claim.get("lean_module", ""))
        for atom in _lean_atoms(claim):
            candidates = lean_inventory.candidate_names(module, atom)
            matched = sorted(declaration_names.intersection(candidates))
            for declaration in matched:
                matches.append({
                    "declaration": declaration,
                    "claim_id": str(claim.get("claim_id", "")),
                    "module_locator": module,
                    "theorem_atom": atom,
                    "relation": "exact_declaration_name_locator_candidate",
                })
    return matches


def result_declaration_crosswalk_view(dataset: dict[str, Any],
                                      lean_inventory: Any,
                                      result_id: str | None = None,
                                      import_root: str = "D0.All",
                                      all_current: bool = False) -> dict[str, Any]:
    """Crosswalk pinned assembly evidence to compiled declaration candidates.

    Exact declaration names supplied with pinned evidence are elaborated against
    that source module. Source co-location and other inferred matches remain
    candidates; no semantic application, claim coverage, or independent
    acceptance is inferred.
    """
    root = pathlib.Path(dataset.get("root", ROOT)).resolve()
    results = list(dataset["assembly"].get("results", []))
    if result_id is not None:
        results = [row for row in results if row.get("id") == result_id]
        if not results:
            return {"key": result_id, "status": "no_exact_assembly_result"}

    per_result: dict[str, dict[str, Any]] = {}
    modules: set[str] = set()
    for row in results:
        key = str(row.get("id", ""))
        evidence_views = []
        source_locator_views = []
        for evidence in row.get("evidence", []):
            if not isinstance(evidence, dict) or not evidence.get("path"):
                continue
            pin = _pinned_evidence_view(root, evidence)
            source_locator_views.append({
                "locator": _source_locator_crosswalk(
                    root, evidence, pin, str(row.get("statement", ""))
                ),
                "pin": pin,
            })
            if not str(evidence.get("path", "")).endswith(".lean"):
                continue
            module = pin["current_module_locator"]
            if pin["pin_status"] == "verified" and pin["current_source_status"] == "matches_pin" and module:
                expected_source = _module_source_path(module)
                if expected_source == pin["path"]:
                    modules.add(module)
                else:
                    module = None
            else:
                module = None
            requested_declaration_names = evidence.get("declaration_names")
            if requested_declaration_names is None:
                declaration_name_locators = []
            elif (not isinstance(requested_declaration_names, list)
                  or any(not isinstance(name, str) or not name.strip()
                         for name in requested_declaration_names)):
                declaration_name_locators = [{
                    "requested": requested_declaration_names,
                    "resolution_status": "invalid_declaration_name_metadata",
                }]
            else:
                initial_status = (
                    "not_enumerated" if module
                    else "pinned_source_not_current_or_not_lean"
                )
                declaration_name_locators = [{
                    "name": name.strip(),
                    "resolution_status": initial_status,
                } for name in dict.fromkeys(requested_declaration_names)]
            evidence_views.append({
                "pin": pin,
                "inventory_module": module,
                "declarations": [],
                "declaration_name_locators": declaration_name_locators,
                "formal_support_candidates": [],
                "requested_declaration_names": requested_declaration_names,
            })
        per_result[key] = {"record": row, "evidence": evidence_views}
        per_result[key]["source_locators"] = source_locator_views

    inventory_rows: list[dict[str, Any]] = []
    collector_sha = None
    proof_detail_collector_sha = None
    lean_digest = None
    if modules and (result_id is not None or all_current):
        inventory_rows, collector_sha, lean_digest = lean_inventory.run_module_inventory(
            sorted(modules), import_root, include_proof_details=False
        )
        by_module: dict[str, list[dict[str, Any]]] = {}
        for declaration in inventory_rows:
            owner = str(declaration.get("module", ""))
            source_path = declaration.get("source_path") or _module_source_path(owner)
            if source_path == _module_source_path(owner):
                by_module.setdefault(owner, []).append(declaration)
        for item in per_result.values():
            for evidence_view in item["evidence"]:
                module = evidence_view["inventory_module"]
                requested_names = evidence_view["requested_declaration_names"]
                path = str(evidence_view["pin"].get("path", ""))
                declarations = [row for row in by_module.get(module, [])
                                if row.get("source_path") == path] if module else []
                evidence_view["declarations"] = declarations
                if module:
                    evidence_view["formal_support_candidates"] = _formal_support_candidates(
                        dataset, module, path
                    )
                if requested_names is None:
                    continue
                if (not isinstance(requested_names, list)
                        or any(not isinstance(name, str) or not name.strip()
                               for name in requested_names)):
                    evidence_view["declaration_name_locators"] = [{
                        "requested": requested_names,
                        "resolution_status": "invalid_declaration_name_metadata",
                    }]
                    continue
                names = list(dict.fromkeys(name.strip() for name in requested_names))
                if not module:
                    evidence_view["declaration_name_locators"] = [{
                        "name": name,
                        "resolution_status": "pinned_source_not_current_or_not_lean",
                    } for name in names]
                    continue
                available_names = {str(row.get("name", "")) for row in declarations}
                evidence_view["declaration_name_locators"] = [{
                    "name": name,
                    "module": module,
                    "source_path": path,
                    "resolution_status": (
                        "resolved" if name in available_names
                        else "not_found_in_pinned_module"
                    ),
                } for name in names]
        declaration_names = {str(row.get("name", "")) for row in inventory_rows}
        locator_candidates = _claim_locator_candidates(dataset, declaration_names, lean_inventory)
        explicit_declaration_names = {
            locator["name"]
            for item in per_result.values()
            for evidence_view in item["evidence"]
            for locator in evidence_view["declaration_name_locators"]
            if locator.get("resolution_status") == "resolved"
        }
        claim_declaration_names = {row["declaration"] for row in locator_candidates}
        detailed_names = sorted(explicit_declaration_names | claim_declaration_names)
        if detailed_names:
            detailed_rows, proof_detail_collector_sha, detailed_source_digest = (
                lean_inventory.run_inventory(detailed_names, import_root)
            )
            if detailed_source_digest != lean_digest:
                raise RuntimeError(
                    "Lean source digest changed between module enumeration and exact declaration extraction."
                )
            detailed_by_name = {
                str(row.get("name", "")): row for row in detailed_rows if row.get("exists")
            }
            for declaration in inventory_rows:
                name = str(declaration.get("name", ""))
                if name in detailed_by_name:
                    declaration.update(detailed_by_name[name])
                    declaration["source_path"] = lean_inventory.module_source_path(
                        declaration.get("module")
                    )
                    declaration["proof_details_status"] = (
                        "collected_for_explicit_declaration_locator"
                        if name in explicit_declaration_names
                        else "collected_for_exact_claim_locator"
                    )
            for item in per_result.values():
                for evidence_view in item["evidence"]:
                    for locator in evidence_view["declaration_name_locators"]:
                        if locator.get("resolution_status") != "resolved":
                            continue
                        declaration = detailed_by_name.get(locator["name"])
                        if declaration is None:
                            locator["resolution_status"] = (
                                "not_found_in_elaborated_environment"
                            )
                        elif declaration.get("module") != locator.get("module"):
                            locator["resolution_status"] = "declaration_owner_module_mismatch"
                        else:
                            source_path = lean_inventory.module_source_path(
                                declaration.get("module")
                            )
                            if source_path != locator.get("source_path"):
                                locator["resolution_status"] = (
                                    "declaration_owner_source_path_mismatch"
                                )
                            else:
                                locator["compiled_declaration"] = {
                                    **declaration,
                                    "source_path": source_path,
                                }

    detailed_rows = []
    summary_rows = []
    for key, item in per_result.items():
        row = item["record"]
        evidence = item["evidence"]
        source_locators = item["source_locators"]
        declarations_by_name: dict[str, dict[str, Any]] = {}
        for evidence_view in evidence:
            for declaration in evidence_view["declarations"]:
                declarations_by_name[str(declaration.get("name", ""))] = declaration
        declarations = [declarations_by_name[name] for name in sorted(declarations_by_name) if name]
        declaration_names = set(declarations_by_name)
        claim_candidates = _claim_locator_candidates(dataset, declaration_names, lean_inventory)
        support_candidates = []
        for evidence_view in evidence:
            support_candidates.extend(evidence_view["formal_support_candidates"])
        unique_support = {}
        for support in support_candidates:
            identity = (support.get("lean_module", ""), support.get("lean_file", ""),
                        support.get("role", ""), support.get("referenced_by", ""))
            unique_support[identity] = support
        pin_verified_count = sum(e["pin"]["pin_status"] == "verified" for e in evidence)
        current_match_count = sum(e["pin"]["current_source_status"] == "matches_pin" for e in evidence)
        has_current_module_source = any(e.get("inventory_module") for e in evidence)
        if not declarations and result_id is None and has_current_module_source and not all_current:
            disposition = "not_enumerated"
        elif not declarations:
            disposition = "unresolved"
        elif len(declarations) == 1:
            disposition = "candidate"
        else:
            disposition = "ambiguous"
        matched_claim_declarations = sorted({
            candidate["declaration"] for candidate in claim_candidates
        })
        if not matched_claim_declarations:
            claim_locator_disposition = "unresolved"
        elif len(matched_claim_declarations) == 1:
            claim_locator_disposition = "candidate"
        else:
            claim_locator_disposition = "ambiguous"
        applications = [
            {"id": app.get("id"), "result": app.get("result"),
             "obligation": app.get("obligation"),
             "review_state": (app.get("review") or {}).get("state")}
            for app in dataset["assembly"].get("applications", [])
            if app.get("result") == key
        ]
        explicit_locators = [
            {
                "source": {
                    "ref": evidence_view["pin"].get("ref"),
                    "path": evidence_view["pin"].get("path"),
                    "sha256": evidence_view["pin"].get("expected_sha256"),
                },
                **locator,
            }
            for evidence_view in evidence
            for locator in evidence_view["declaration_name_locators"]
        ]
        explicit_statuses = [locator.get("resolution_status")
                             for locator in explicit_locators]
        if not explicit_locators:
            explicit_locator_disposition = "not_recorded"
        elif all(status == "resolved" for status in explicit_statuses):
            explicit_locator_disposition = "all_resolved"
        elif any(status == "resolved" for status in explicit_statuses):
            explicit_locator_disposition = "partially_resolved"
        else:
            explicit_locator_disposition = "unresolved"
        summary_rows.append({
            "result_id": key,
            "owner": row.get("owner"),
            "lean_evidence_count": len(evidence),
            "verified_pin_count": pin_verified_count,
            "current_source_match_count": current_match_count,
            "source_evidence_count": len(source_locators),
            "source_pin_verified_count": sum(
                x["pin"]["pin_status"] == "verified" for x in source_locators
            ),
            "section_locator_count": sum(
                bool(x["locator"]["exact_unit_key_candidates"]) for x in source_locators
            ),
            "source_unit_locator_disposition": (
                "section_keys_need_review"
                if source_locators and any(
                    x["locator"]["exact_unit_key_candidates"] for x in source_locators
                )
                else "section_mapping_incomplete" if source_locators
                else "no_pinned_source_evidence"
            ),
            "compiled_declaration_count": (
                len(declarations) if result_id is not None or all_current else None
            ),
            "declaration_disposition": disposition,
            "explicit_declaration_locator_disposition": explicit_locator_disposition,
            "explicit_declaration_locator_count": len(explicit_locators),
            "claim_locator_disposition": claim_locator_disposition,
            "semantic_relation_status": "unresolved",
            "declared_application_count": len(applications),
            "evidence": [{
                "path": e["pin"].get("path"),
                "ref": e["pin"].get("ref"),
                "pin_status": e["pin"].get("pin_status"),
                "current_source_status": e["pin"].get("current_source_status"),
                "module": e.get("inventory_module"),
                "declaration_count": (
                    len(e.get("declarations", [])) if result_id is not None or all_current else None
                ),
            } for e in evidence],
        })
        if result_id is not None or all_current:
            result_item = {"kind": "assembly-result", "key": key, "record": row}
            detailed_rows.append({
                "result_id": key,
                "owner": row.get("owner"),
                "statement": row.get("statement"),
                "reported_state": row.get("reported_state"),
                "evidence_crosswalks": evidence,
                "source_locator_crosswalks": source_locators,
                "compiled_declarations": declarations,
                "explicit_declaration_locators": explicit_locators,
                "claim_locator_candidates": claim_candidates,
                "formal_support_candidates": list(unique_support.values()),
                "declared_relations": relation_view(dataset, result_item),
                "declaration_disposition": disposition,
                "explicit_declaration_locator_disposition": explicit_locator_disposition,
                "claim_locator_disposition": claim_locator_disposition,
                "semantic_relation_status": "unresolved",
                "acceptance_inferred": False,
                "collector_sha256": collector_sha,
                "lean_source_digest": lean_digest,
                "public_import_root": import_root,
                "proof_detail_collector_sha256": proof_detail_collector_sha,
                "interpretation": (
                    "Pinned source bytes, compiled declarations, exact claim-name locators, and "
                    "formal-support module locators are displayed as separate evidence. Explicit "
                    "declaration names are checked against their pinned current module and elaborated "
                    "environment, but do not establish semantic scope, an application edge, or review "
                    "acceptance. Co-location and inferred exact-name matches remain candidates only."
                ),
            })

    common = {
        "snapshot_commit": dataset["snapshot_commit"],
        "worktree_dirty": dataset.get("worktree_dirty", False),
        "source_digests": dataset.get("source_digests", {}),
        "tool_source_digests": {
            "tools/proof_architecture.py": sha256(pathlib.Path(__file__)),
            "tools/lean_declaration_inventory.py": sha256(
                ROOT / "tools" / "lean_declaration_inventory.py"
            ),
        },
        "public_import_root": import_root,
        "enumerated_current_modules": sorted(modules) if result_id is not None or all_current else None,
        "collector_sha256": collector_sha,
        "proof_detail_collector_sha256": proof_detail_collector_sha,
        "lean_source_digest": lean_digest,
        "interpretation": (
            "This generated crosswalk is retrieval and review evidence. It does not infer a semantic "
            "application, mathematical coverage, or independent acceptance."
        ),
        "source_locator_interpretation": (
            "A source:<commit>:<path> key is emitted only after the immutable commit:path blob "
            "matches its recorded SHA-256; the current checkout may be missing or changed. Only "
            "explicit section metadata yields exact section-key candidates. When it is absent, "
            "ranked headings from verified pinned Markdown may be shown as lexical candidates; "
            "all section candidates require review and none is accepted by this view."
        ),
    }
    if result_id is not None:
        return {**common, **detailed_rows[0]}
    if all_current:
        all_source_locators = [
            source_locator
            for item in per_result.values()
            for source_locator in item["source_locators"]
        ]
        pin_status_counts: dict[str, int] = {}
        current_source_status_counts: dict[str, int] = {}
        for source_locator in all_source_locators:
            pin_status = str(source_locator["pin"].get("pin_status", "unknown"))
            current_status = str(
                source_locator["pin"].get("current_source_status", "unknown")
            )
            pin_status_counts[pin_status] = pin_status_counts.get(pin_status, 0) + 1
            current_source_status_counts[current_status] = (
                current_source_status_counts.get(current_status, 0) + 1
            )
        return {
            **common,
            "result_count": len(detailed_rows),
            "source_locator_summary": {
                "evidence_count": sum(r["source_evidence_count"] for r in summary_rows),
                "verified_pin_count": sum(r["source_pin_verified_count"] for r in summary_rows),
                "pin_status_counts": pin_status_counts,
                "current_source_status_counts": current_source_status_counts,
                "section_locator_count": sum(r["section_locator_count"] for r in summary_rows),
                "ranked_section_candidate_count": sum(
                    len(source_locator["locator"]["ranked_section_candidates"])
                    for source_locator in all_source_locators
                ),
                "results_with_ranked_section_candidates": sum(
                    any(source_locator["locator"]["ranked_section_candidates"]
                        for source_locator in item["source_locators"])
                    for item in per_result.values()
                ),
                "results_with_incomplete_section_mapping": sum(
                    r["source_unit_locator_disposition"] == "section_mapping_incomplete"
                    for r in summary_rows
                ),
                "interpretation": (
                    "Counts describe source pins and recorded section locators, not accepted C0 "
                    "units or semantic result-to-source relations."
                ),
            },
            "results": detailed_rows,
        }
    return {**common, "result_count": len(summary_rows), "results": summary_rows}


def why_view(dataset: dict[str, Any], key: str) -> dict[str, Any]:
    obligation = next((x for x in records(dataset) if x["kind"] == "obligation" and x["key"] == key), None)
    if obligation:
        view = relation_view(dataset, obligation)
        interface_id = obligation["record"].get("interface")
        interface = next((x["record"] for x in records(dataset)
                          if x["kind"] == "interface" and x["key"] == interface_id), None)
        raw_hypotheses = obligation["record"].get("hypotheses")
        hypotheses_known = isinstance(raw_hypotheses, dict)
        expected = set(raw_hypotheses) if hypotheses_known else set()
        hypotheses_status = ("declared_empty" if not expected else "declared") if hypotheses_known else "unknown"
        for application in view["declared_applications"]:
            mapping_present = "hypothesis_map" in application
            mapping = application.get("hypothesis_map")
            mapped_targets = set()
            invalid_entries = []
            if isinstance(mapping, dict):
                for value in mapping.values():
                    target = (value.get("target_hypothesis") if isinstance(value, dict)
                              else value if isinstance(value, str) else None)
                    if isinstance(target, str) and target:
                        mapped_targets.add(target)
                    else:
                        invalid_entries.append(value)
            unknown_targets = sorted(mapped_targets - expected) if hypotheses_known else []
            gaps = sorted(expected - mapped_targets) if hypotheses_known else []
            if not hypotheses_known or not mapping_present or not isinstance(mapping, dict):
                mapping_status = "unknown"
            elif invalid_entries:
                mapping_status = "unknown"
            elif unknown_targets:
                mapping_status = "unknown_target"
            elif not expected and not mapped_targets:
                mapping_status = "declared_empty"
            elif gaps:
                mapping_status = "unmapped"
            else:
                mapping_status = "mapped"
            application["hypothesis_mapping_gaps"] = gaps
            application["hypothesis_mapping_status"] = mapping_status
            application["unknown_hypothesis_targets"] = unknown_targets
            application["invalid_hypothesis_map_entries"] = invalid_entries
        return {"key": key, "obligation": obligation["record"],
                "interface": interface,
                **view,
                "hypotheses": raw_hypotheses,
                "hypotheses_status": hypotheses_status,
                "snapshot_commit": dataset["snapshot_commit"],
                "interpretation": "Mapping coverage is reported mechanically; unknown, empty, unmapped, and unknown-target states remain distinct. Correctness requires review; a declared method and accepted review still do not replace typed Lean/application evidence."}
    hits = find_exact(dataset, key)
    if hits:
        return {"key": key, "matches": [
                    {"item": item, **relation_view(dataset, item)} for item in hits
                ], "snapshot_commit": dataset["snapshot_commit"],
                "interpretation": "Conceptual presupposition edges and lookup aliases do not establish proof dependencies; no obligation substitution is inferred without a separately reviewed application edge."}
    return {"key": key, "matches": [],
            "snapshot_commit": dataset["snapshot_commit"],
            "interpretation": "No exact authority match. Search candidates are not evidence of nonexistence."}


def impact_view(dataset: dict[str, Any], key: str) -> dict[str, Any]:
    source = source_file_view(dataset["root"], key)
    source_snapshot = ({"path": source["path"], "size_bytes": source["size_bytes"],
                       "source_sha256": source["source_sha256"]}
                      if source else None)
    hits = find_exact(dataset, key)
    if not hits:
        return {"key": key, "matches": [], "snapshot_commit": dataset["snapshot_commit"],
                "source_snapshot": source_snapshot,
                "interpretation": "No declared impact edge found; this is not a proof of independence."}
    impacts = []
    for item in hits:
        impacts.append({"item": item, **relation_view(dataset, item)})
    return {"key": key, "declared_impact": impacts,
            "snapshot_commit": dataset["snapshot_commit"],
            "source_snapshot": source_snapshot,
            "source_digests": dataset["source_digests"],
            "interpretation": "This is impact through currently declared registry links. Lean dependency impact requires elaborated declaration data."}


def run_assembly_impact(root: pathlib.Path, base: str, ref: str | None) -> dict[str, Any]:
    cmd = [sys.executable, str(root / "tools" / "gr_assembly.py"), "--json", "impact", "--base", base]
    if ref:
        cmd.extend(["--ref", ref])
    proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def _render_text(value: Any, *, complete_arrays: bool = False) -> str:
    def bound(item: Any) -> Any:
        if isinstance(item, str) and len(item) > MAX_FIELD_CHARS:
            digest = hashlib.sha256(item.encode("utf-8")).hexdigest()
            return item[:MAX_FIELD_CHARS] + f"… [truncated {len(item) - MAX_FIELD_CHARS} chars; sha256={digest}]"
        if isinstance(item, list):
            values = [bound(value) for value in (item if complete_arrays else item[:32])]
            if len(item) > 32 and not complete_arrays:
                values.append({"_omitted_items": len(item) - 32})
            return values
        if isinstance(item, dict):
            return {key: bound(value) for key, value in item.items()}
        return item
    return json.dumps(bound(value), ensure_ascii=False, indent=2, sort_keys=False)


def main() -> int:
    _configure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search", help="search structured authorities and bounded full-text candidates")
    search.add_argument("query", nargs="+")
    show = sub.add_parser("show", help="show an exact claim/result/application/obligation key")
    show.add_argument("key")
    show.add_argument("--lean", action="store_true",
                      help="resolve the key as an exact Lean name or claims.csv ID in elaborated Lean")
    show.add_argument("--import-root", default="D0.All",
                      help="compiled public import used by --lean (default: D0.All)")
    why = sub.add_parser("why", help="show declared route, hypotheses, and missing application edges")
    why.add_argument("key")
    reuse = sub.add_parser("reuse", help="show declared reuse links and optional compiled claim dependencies")
    reuse.add_argument("key")
    reuse.add_argument("--lean", action="store_true",
                       help="compile exact theorem-name locators for a claims.csv ID")
    reuse.add_argument("--import-root", default="D0.All",
                       help="compiled public import used by --lean (default: D0.All)")
    crosswalk = sub.add_parser(
        "crosswalk", help="show pinned assembly Lean evidence and compiled declaration candidates"
    )
    crosswalk.add_argument("key", nargs="?",
                           help="exact assembly result ID; omit for a bounded all-result summary")
    crosswalk.add_argument("--import-root", default="D0.All",
                           help="compiled public import used for declaration enumeration")
    crosswalk.add_argument("--all-current", action="store_true",
                           help="enumerate all verified current pinned Lean evidence sources in one pass")
    sub.add_parser("claim-sources",
                   help="resolve claims.csv book/section locators to exact heading candidates")
    sub.add_parser("alias-sources",
                   help="inspect alias target rows and legacy book line locators as candidates")
    impact = sub.add_parser("impact", help="show declared impact, or assembly impact since a Git base")
    impact.add_argument("key", nargs="?")
    impact.add_argument("--base")
    impact.add_argument("--ref")
    parser.add_argument("--repo-root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    if args.command == "impact" and args.base:
        result = run_assembly_impact(root, args.base, args.ref)
    else:
        data = load_dataset(root)
        if args.command == "search":
            query = " ".join(args.query)
            structured = structured_search(data, query)
            text_hits = full_text_search(root, query)
            seen = {(x["kind"], x["key"]) for x in structured}
            result = {"query": query, "structured_matches": [_search_summary(x) for x in structured],
                      "text_candidates": [_search_candidate_summary(x, data) for x in text_hits
                                          if (x["kind"], x["key"]) not in seen],
                      "snapshot_commit": data["snapshot_commit"],
                      "source_digests": data["source_digests"],
                      "warning": "Text matches are retrieval candidates, not accepted mathematical relations."}
        elif args.command == "show":
            if args.lean:
                import lean_declaration_inventory as lean_inventory
                if args.key.startswith("D0."):
                    mapping, names = {"full_name": args.key}, [args.key]
                else:
                    mapping, names = lean_inventory.claim_requests(args.key)
                rows, collector_sha, lean_digest = lean_inventory.run_inventory(names, args.import_root)
                for row in rows:
                    row["source_path"] = lean_inventory.module_source_path(row.get("module"))
                result = {"key": args.key, "claim_mapping": mapping,
                          "elaborated_declarations": rows,
                          "collector_sha256": collector_sha,
                          "lean_source_digest": lean_digest,
                          "snapshot_commit": data["snapshot_commit"],
                          "public_import_root": args.import_root}
            else:
                hits = find_exact(data, args.key)
                source_view = source_file_view(root, args.key) if not hits else None
                result = {"key": args.key, "matches": hits,
                          "source_file": source_view,
                          "snapshot_commit": data["snapshot_commit"],
                          "source_digests": data["source_digests"]}
        elif args.command == "why":
            result = why_view(data, args.key)
        elif args.command == "reuse":
            if args.lean:
                import lean_declaration_inventory
                inventory = lean_declaration_inventory
            else:
                inventory = None
            result = reuse_view(data, args.key, lean_inventory=inventory,
                                import_root=args.import_root)
        elif args.command == "crosswalk":
            if args.key and args.all_current:
                parser.error("crosswalk accepts either RESULT-ID or --all-current, not both")
            import lean_declaration_inventory
            result = result_declaration_crosswalk_view(
                data, lean_declaration_inventory, result_id=args.key,
                import_root=args.import_root, all_current=args.all_current,
            )
        elif args.command == "claim-sources":
            result = claim_source_candidate_view(data)
        elif args.command == "alias-sources":
            result = alias_source_candidate_view(data)
        else:
            if not args.key:
                parser.error("impact requires KEY unless --base is supplied")
            result = impact_view(data, args.key)
    if "data" in locals():
        result.setdefault("snapshot_commit", data["snapshot_commit"])
        result.setdefault("worktree_dirty", data["worktree_dirty"])
    print(_render_text(
        result,
        complete_arrays=(args.command == "crosswalk" and args.all_current)
        or args.command in {"claim-sources", "alias-sources"},
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

