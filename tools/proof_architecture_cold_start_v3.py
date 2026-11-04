"""Opt-in paged cold-start replay; legacy runner and fixtures are unchanged.

This performs one batched discovery over every CASES query. Snapshot checks
bracket the run and cover visible corpus bytes at two points, not every instant,
external tool binaries, Git object availability, or semantic truth.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as legacy

SCHEMA = "d0-proof-architecture-cold-start-paged-v3"
RANK_SIZE = legacy.COLD_START_MIN_RESULT_WINDOW
RANK_PAGES = 2
SOURCE_PAGES = 12
SOURCE_PAGES_PER_CALL = 4
SOURCE_SIZE = legacy.SOURCE_PAGE_SIZE
WORKSPACE_SOURCE_SIZE = 8
WORKSPACE_SOURCE_PAGES = 8


def corpus_paths(root: pathlib.Path) -> list[str]:
    """Enumerate the same rg-visible files used by batched discovery."""
    roots = [name for name in proof.TEXT_ROOTS if (root / name).is_dir()]
    globs = ["-g", "*.md", "-g", "*.lean", "-g", "*.json", "-g", "*.csv",
             "-g", "*.py", "-g", "*.toml"]
    if not roots:
        names = []
    else:
        proc = subprocess.run(["rg", "--files", *globs, *roots], cwd=root,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if proc.returncode not in (0, 1):
            raise ValueError("cannot enumerate the search corpus")
        names = [os.fsdecode(raw).replace("\\", "/") for raw in proc.stdout.splitlines()]
        names = sorted(name for name in names if name and
                       not name.startswith(proof.DERIVED_TEXT_EXCLUDED_PREFIXES))
    return names


def corpus_snapshot(root: pathlib.Path) -> dict[str, Any]:
    """Hash the current rg-visible corpus, including untracked visible files."""
    proof._search_progress("corpus_enumeration_started")
    names = corpus_paths(root)
    h = hashlib.sha256()
    resolved_root = proof._search_filesystem_path(proof._search_filesystem_path(root).resolve(strict=True))
    proof._search_progress("corpus_snapshot_started", files=len(names))
    for index, name in enumerate(names, 1):
        path = proof._search_filesystem_path(
            proof._search_filesystem_path(root / proof._search_relative_path(name)).resolve(strict=True))
        if not proof._search_contains_file(resolved_root, path) or not path.is_file():
            raise ValueError("invalid search corpus path")
        h.update(name.encode("utf-8")); h.update(b"\0")
        h.update(hashlib.sha256(path.read_bytes()).digest()); h.update(b"\0")
        if index % proof._SEARCH_PROGRESS_INTERVAL == 0:
            proof._search_progress("corpus_snapshot_running", files_hashed=index,
                                   files_total=len(names))
    proof._search_progress("corpus_snapshot_complete", files_hashed=len(names))
    return {"sha256": h.hexdigest(), "file_count": len(names),
            "scope": "rg-visible search roots, checked before and after; no continuous or toolchain attestation"}


def _ranked_pages(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pages = []
    for index in range(RANK_PAGES):
        start = min(index * RANK_SIZE, len(hits))
        end = min((index + 1) * RANK_SIZE, len(hits))
        rows = hits[start:end]
        pages.append({"page_number": index + 1, "start": start, "end_exclusive": end,
                      "may_have_more": len(hits) > end if index + 1 < RANK_PAGES else len(rows) == RANK_SIZE,
                      "candidates": rows})
    return pages


def source_pages(root: pathlib.Path, query: str, hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Continue each ranked locator in bounded four-page calls, at most 12 pages."""
    pages = []
    for rank, hit in enumerate(hits, 1):
        for offset in range(0, SOURCE_PAGES, SOURCE_PAGES_PER_CALL):
            batch = proof.expand_source_pages(
                root, query, [hit], page_size=SOURCE_SIZE,
                pages_per_locator=min(SOURCE_PAGES_PER_CALL, SOURCE_PAGES - offset),
                page_offset=offset, continue_references=True)
            for page in batch:
                page["locator_rank"] = rank
            pages.extend(batch)
            if not batch or batch[-1].get("page_exhausted") or not batch[-1]["remaining_references"]:
                break
    return pages


def workspace_source_pages(root: pathlib.Path, query: str, hits: list[dict[str, Any]],
                           allowed_paths: set[str]) -> list[dict[str, Any]]:
    """Open observed workspace links, bounded independently of Git-pin pages.

    The only allowed-path input is the enumerated corpus, never expected
    benchmark sources; its bytes are covered by the caller's endpoint hashes.
    """
    return proof.expand_workspace_source_pages(
        root, query, hits, page_size=WORKSPACE_SOURCE_SIZE,
        pages_per_locator=WORKSPACE_SOURCE_PAGES, allowed_paths=allowed_paths,
    )


def verified_query(root: pathlib.Path, query: str, result: dict[str, Any],
                   allowed_paths: set[str] | None = None) -> list[dict[str, Any]]:
    """Recheck returned evidence and exact source pages; never use expected paths."""
    ranked = result.get("ranked_pages")
    if not isinstance(ranked, list) or len(ranked) != RANK_PAGES:
        raise ValueError("missing ranked pages")
    hits: list[dict[str, Any]] = []
    empty = False
    for i, page in enumerate(ranked):
        if not isinstance(page, dict) or page.get("page_number") != i + 1 or page.get("start") != len(hits):
            raise ValueError("ranked pages out of order")
        rows = page.get("candidates")
        if not isinstance(rows, list) or len(rows) > RANK_SIZE or (empty and rows):
            raise ValueError("invalid ranked page size")
        if page.get("end_exclusive") != len(hits) + len(rows):
            raise ValueError("invalid ranked page span")
        if len(rows) < RANK_SIZE:
            empty = True
        hits.extend(rows)
    for i, page in enumerate(ranked):
        more = (len(hits) > page["end_exclusive"] if i + 1 < RANK_PAGES
                else len(page["candidates"]) == RANK_SIZE)
        if page.get("may_have_more") is not more:
            raise ValueError("invalid ranked continuation indicator")
    if result.get("query") != query or len(hits) > 64:
        raise ValueError("query or ranked budget mismatch")
    if allowed_paths is None:
        allowed_paths = set(corpus_paths(root))

    terms = proof._query_terms(query)
    pattern = proof._term_pattern(terms)
    variants: dict[str, list[tuple[int, str]]] = {}
    for name, values in terms:
        for value in values:
            variants.setdefault(value, []).append((0, name))
    matcher = proof._build_multi_pattern_matcher(variants)
    pin_cache: dict = {}
    workspace_cache: dict[str, tuple[bytes, str, list[str], float, str]] = {}

    def workspace(rel: str) -> tuple[bytes, str, list[str], float, str]:
        if rel in workspace_cache:
            return workspace_cache[rel]
        if (rel not in allowed_paths or rel in {"tools/proof_architecture.py",
                "tools/proof_architecture_cold_start.py", "tools/proof_architecture_cold_start_v3.py",
                "tools/compact_proof_architecture_cold_start_v3.py"} or rel.startswith("tools/test_")):
            raise ValueError("candidate was not in the searchable workspace corpus")
        path = proof._search_filesystem_path(
            proof._search_filesystem_path(root / proof._search_relative_path(rel)).resolve(strict=True))
        resolved_root = proof._search_filesystem_path(proof._search_filesystem_path(root).resolve(strict=True))
        if not proof._search_contains_file(resolved_root, path) or not path.is_file():
            raise ValueError("invalid workspace candidate")
        data = path.read_bytes()
        text = data.decode("utf-8-sig", errors="replace")
        title = pathlib.PurePosixPath(rel).stem.replace("_", " ").replace("-", " ")
        content_names = proof._multi_pattern_matches(proof._fold(text), matcher).get(0, set())
        names = content_names | proof._matched_term_names(proof._fold(title), pattern, terms)
        ordered_names = [name for name, _ in terms if name in names]
        if not terms:
            raise ValueError("empty query cannot produce a ranked candidate")
        score = len(names) / len(terms) + proof._owner_bonus(rel) + proof._filename_bonus(rel, terms)
        origin = "workspace" if content_names else "filename_only"
        workspace_cache[rel] = (data, text, ordered_names, score, origin)
        return workspace_cache[rel]

    def pin_trace(hit: dict[str, Any]) -> tuple[dict[str, Any], float]:
        trace = hit.get("pin_discovery")
        if not isinstance(trace, dict):
            raise ValueError("ranked pin has no observed locator trace")
        loc, digest = trace.get("locator_source"), trace.get("locator_sha256")
        rank, ref_rank = trace.get("pin_window_rank"), trace.get("reference_rank")
        if (not isinstance(loc, str) or type(rank) is not int or not 1 <= rank <= RANK_SIZE or
                type(ref_rank) is not int or not 1 <= ref_rank <= 8):
            raise ValueError("invalid observed locator trace")
        data, text, names, locator_score, _ = workspace(loc)
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError("observed locator bytes do not match digest")
        minimum = 1 if len(terms) <= 3 else max(2, (len(terms) + 3) // 4)
        if len(names) < minimum or len(data) > 4_000_000:
            raise ValueError("observed locator is outside the bounded pin window")
        lines = [line for line in text.splitlines() if pattern.search(proof._fold(line))]
        refs = proof._source_references(lines, terms, pattern)
        refs.sort(key=lambda item: (
            -len(proof._matched_term_names(proof._fold(str(item.get("context", ""))), pattern, terms)),
            -sum(any(variant in proof._fold(str(item.get("path", ""))) for variant in values)
                 for _, values in terms),
            -bool(item.get("pin_complete")), str(item.get("path", "")),
        ))
        refs = [ref for ref in refs if ref.get("pin_complete")][:8]
        if ref_rank > len(refs):
            raise ValueError("pin reference lies outside the locator budget")
        ref = refs[ref_rank - 1]
        if (ref.get("path") != hit.get("source") or ref.get("commit") != hit.get("source_commit") or
                (ref.get("blob") is not None and ref["blob"] != hit.get("source_blob"))):
            raise ValueError("ranked pin is not the observed locator reference")
        return dict(ref), locator_score

    combined = []
    previous_rank = None
    seen_keys = set()
    for i, hit in enumerate(hits):
        if not isinstance(hit, dict) or not isinstance(hit.get("source"), str):
            raise ValueError("invalid ranked candidate")
        rel = hit["source"]
        score, sort_key = hit.get("rank_score"), hit.get("rank_sort_key")
        if (type(score) not in (float, int) or not math.isfinite(score) or
                not isinstance(sort_key, str) or sort_key != hit.get("key") or
                hit.get("kind") != "text-candidate" or hit.get("query_terms") != len(terms)):
            raise ValueError("rank score or key missing")
        identity = (hit["kind"], sort_key)
        if identity in seen_keys:
            raise ValueError("duplicate ranked candidate")
        seen_keys.add(identity)
        rank = (-score, sort_key)
        if previous_rank is not None and rank < previous_rank:
            raise ValueError("ranked candidates are out of order")
        previous_rank = rank
        direct = hit.get("direct_content")
        if type(direct) is not bool:
            raise ValueError("invalid direct-content flag")
        origin = hit.get("source_origin")
        if origin in {"workspace", "filename_only"}:
            data, text, names, expected_score, actual_origin = workspace(rel)
            if origin != actual_origin or sort_key != rel:
                raise ValueError("workspace origin or key does not match source")
            if hit.get("source_sha256") is not None and hit["source_sha256"] != hashlib.sha256(data).hexdigest():
                raise ValueError("candidate bytes do not match digest")
            if (hit.get("matched_term_names") != names or hit.get("matched_terms") != len(names) or
                    hit.get("query_terms") != len(terms)):
                raise ValueError("candidate terms do not match source and query")
            if direct:
                candidate = proof._candidate_record(rel, text, terms, origin="workspace", pattern=pattern)
                if (hit.get("source_sha256") != hashlib.sha256(data).hexdigest() or candidate is None or
                        candidate[1].get("direct_content") is not True or not hit.get("evidence_lines") or
                        hit["evidence_lines"] != candidate[1]["evidence_lines"]):
                    raise ValueError("workspace direct evidence does not match source")
        elif origin in {"pinned_snapshot", "citation_only"}:
            ref, locator_score = pin_trace(hit)
            status, data = proof._read_pinned_source(root, ref, pin_cache)
            if origin == "citation_only":
                if (direct or data is not None or status != hit.get("pin_status") or
                        hit.get("matched_terms") != 0 or hit.get("matched_term_names") != []):
                    raise ValueError("invalid unresolved ranked pin")
                expected_score = locator_score - 0.50
            else:
                if (status != "pinned_snapshot" or data is None or
                        hit.get("source_sha256") != hashlib.sha256(data).hexdigest() or
                        ref.get("blob") != hit.get("source_blob")):
                    raise ValueError("ranked pin does not match exact bytes")
                text = data.decode("utf-8-sig", errors="replace")
                candidate = proof._candidate_record(rel, text, terms, origin="pinned_snapshot", pattern=pattern)
                if candidate is None:
                    if (direct or hit.get("pin_status") != "verified_no_content_match" or
                            hit.get("matched_terms") != 0 or hit.get("matched_term_names") != [] or
                            hit.get("evidence_lines") != []):
                        raise ValueError("ranked pin lacks content match")
                    expected_score = locator_score - 0.50
                else:
                    expected_score, checked = candidate
                    if (hit.get("pin_status") != "verified" or direct != checked["direct_content"] or
                            hit.get("matched_term_names") != checked["matched_term_names"] or
                            hit.get("matched_terms") != checked["matched_terms"] or
                            hit.get("evidence_lines") != checked["evidence_lines"]):
                        raise ValueError("ranked pin content does not match source")
        else:
            raise ValueError("unknown ranked candidate origin")
        if not math.isclose(score, expected_score, rel_tol=0, abs_tol=1e-12):
            raise ValueError("candidate score does not match source and query")
        combined.append({**hit, "candidate_rank": i % RANK_SIZE + 1,
                         "candidate_stage": "top_candidates" if i < RANK_SIZE else "ranked_page",
                         "candidate_page_number": None if i < RANK_SIZE else i // RANK_SIZE + 1,
                         "candidate_locator_source": None})

    # Reconstruct the exact pages from the same locator bytes, including all
    # observed references, alias budgets, actual spans, pin status and content.
    actual = source_pages(root, query, hits)
    pages = result.get("source_pages")
    if actual != pages:
        raise ValueError("source pages do not reproduce from locator bytes and pins")
    for page in pages:
        for rank, candidate in enumerate(page["candidates"], 1):
            combined.append({**candidate, "candidate_stage": "source_page", "candidate_rank": rank,
                             "candidate_locator_source": page["locator_source"],
                             "candidate_page_number": page["page_number"]})
    # Old v3 receipts have no workspace-page field. Do not silently expand
    # their historical search; new receipts explicitly opt into this surface.
    if "workspace_source_pages" in result:
        actual_workspace = workspace_source_pages(root, query, hits, allowed_paths)
        workspace_pages = result["workspace_source_pages"]
        if (not isinstance(workspace_pages, list) or
                len(workspace_pages) > len(hits) * WORKSPACE_SOURCE_PAGES or
                workspace_pages != actual_workspace):
            raise ValueError("workspace source pages do not reproduce from locator bytes")
        seen_workspace_pages = set()
        observed_links: dict[str, set[tuple[int, str]]] = {}
        for page in workspace_pages:
            if not isinstance(page, dict):
                raise ValueError("invalid workspace source page")
            locator_rank = page.get("locator_rank")
            if type(locator_rank) is not int or not 1 <= locator_rank <= len(hits):
                raise ValueError("workspace page locator is not a returned candidate")
            number, total, remaining = (page.get(k) for k in
                                         ("page_number", "total_references", "remaining_references"))
            if (page.get("query") != query or type(number) is not int or
                    not 1 <= number <= WORKSPACE_SOURCE_PAGES or
                    page.get("page_size") != WORKSPACE_SOURCE_SIZE or
                    type(total) is not int or not 1 <= total <= 64 or
                    type(remaining) is not int or remaining < 0 or
                    page.get("reference_scan_limit") != 64 or
                    type(page.get("reference_set_may_be_truncated")) is not bool or
                    (locator_rank, number) in seen_workspace_pages):
                raise ValueError("invalid workspace page bounds")
            seen_workspace_pages.add((locator_rank, number))
            locator = hits[locator_rank - 1]
            if (locator.get("source_origin") != "workspace" or
                    locator.get("direct_content") is not True or
                    locator.get("source") != page.get("locator_source") or
                    locator.get("source_sha256") != page.get("locator_sha256")):
                raise ValueError("workspace page has no observed direct locator")
            locator_bytes, locator_text, _, _, _ = workspace(page["locator_source"])
            if hashlib.sha256(locator_bytes).hexdigest() != page["locator_sha256"]:
                raise ValueError("workspace locator changed after discovery")
            locator_lines = locator_text.splitlines()
            if page["locator_source"] not in observed_links:
                links: set[tuple[int, str]] = set()
                fence_char, fence_length = None, 0
                markdown = re.compile(r"(?<!!)(?<!\\)\[[^\]\n]*\]\(([^\s)]+)\)")
                for line_number, line_text in enumerate(locator_lines, 1):
                    fence_char, fence_length, fence_line = proof._markdown_fence_transition(
                        line_text, fence_char, fence_length)
                    if (fence_line or fence_char is not None or len(line_text) > 4096 or
                            not pattern.search(proof._fold(line_text))):
                        continue
                    for match in markdown.finditer(line_text):
                        if line_text[:match.start()].count("`") % 2 == 0:
                            links.add((line_number, match.group(1)))
                observed_links[page["locator_source"]] = links
            statuses = page.get("reference_statuses")
            candidates = page.get("candidates")
            expected_count = min(WORKSPACE_SOURCE_SIZE,
                                 max(0, total - (number - 1) * WORKSPACE_SOURCE_SIZE))
            if (not isinstance(statuses, list) or not isinstance(candidates, list) or
                    len(statuses) != expected_count or len(candidates) > len(statuses) or
                    remaining != max(0, total - number * WORKSPACE_SOURCE_SIZE)):
                raise ValueError("invalid workspace page records")
            matched_statuses = set()
            for status in statuses:
                if not isinstance(status, dict):
                    raise ValueError("invalid workspace reference status")
                line, literal, text = (status.get("citation_line"), status.get("citation_path"),
                                       status.get("citation_text"))
                if (type(line) is not int or not 1 <= line <= len(locator_lines) or
                        not isinstance(literal, str) or not literal or
                        text != locator_lines[line - 1] or
                        (line, literal) not in observed_links[page["locator_source"]]):
                    raise ValueError("workspace reference is not in the observed locator line")
                if status.get("content_status") == "direct_content_match":
                    matched_statuses.add((line, literal, status.get("source")))
            seen_candidates = set()
            for rank, candidate in enumerate(candidates, 1):
                if not isinstance(candidate, dict):
                    raise ValueError("invalid workspace candidate")
                rel = candidate.get("source")
                if not isinstance(rel, str):
                    raise ValueError("workspace candidate source is not a path")
                key = (candidate.get("citation_line"), candidate.get("citation_path"), rel)
                if (key not in matched_statuses or key in seen_candidates or
                        candidate.get("locator_source") != page["locator_source"] or
                        candidate.get("source_commit") is not None or
                        candidate.get("source_blob") is not None or
                        candidate.get("source_origin") != "workspace" or
                        candidate.get("direct_content") is not True or
                        candidate.get("citation_text") != locator_lines[key[0] - 1]):
                    raise ValueError("invalid workspace source provenance")
                literal = candidate["citation_path"]
                parts = literal.split("/")
                if (not literal or any(part in {"", ".", ".."} for part in parts) or
                        any(char in literal for char in ("%", "?", "#", ":", "\\")) or
                        any(ord(char) < 32 or ord(char) == 127 for char in literal) or
                        f"]({literal})" not in candidate["citation_text"] or
                        (pathlib.PurePosixPath(page["locator_source"]).parent / literal).as_posix() != rel):
                    raise ValueError("workspace candidate does not resolve from its observed link")
                target_bytes, target_text, _, _, _ = workspace(rel)
                checked = proof._candidate_record(rel, target_text, terms, origin="workspace",
                                                  pattern=pattern,
                                                  content_sha256=hashlib.sha256(target_bytes).hexdigest())
                if (checked is None or not checked[1].get("direct_content") or
                        any(candidate.get(k) != value for k, value in checked[1].items())):
                    raise ValueError("workspace source content evidence does not match bytes")
                seen_candidates.add(key)
                combined.append({**candidate, "candidate_stage": "workspace_source_page",
                                 "candidate_rank": rank,
                                 "candidate_locator_source": page["locator_source"],
                                 "candidate_page_number": page["page_number"]})
            if seen_candidates != matched_statuses:
                raise ValueError("workspace reference status lacks returned direct evidence")
    return combined


def _requirements(case: dict[str, Any], pairs: list[tuple[str, list[dict[str, Any]]]], *,
                  discovery_attested: bool = False) -> dict[str, Any]:
    statuses = {}
    for item in case.get("required_sources", []):
        key = item["path"]
        if key in statuses:
            key = f"{key}@{item.get('commit') or item.get('blob') or str(len(statuses))}"
        statuses[key] = legacy._required_source_status(pairs, item)
    for path in case["required_refs"]:
        if not any(row["path"] == path for row in case.get("required_sources", [])):
            statuses[path] = legacy._required_source_status(pairs, {"path": path})
    if not discovery_attested:
        for receipt in statuses.values():
            if receipt["found"]:
                receipt["found"] = False
                receipt["status"] = "evidence_verified_discovery_unattested"
            for scoped in receipt["scoped_queries"]:
                if scoped["found"]:
                    scoped["found"] = False
                    scoped["status"] = "evidence_verified_discovery_unattested"
    return statuses


def run(root: pathlib.Path) -> dict[str, Any]:
    root = proof._search_run_root(root)
    before = proof.load_dataset(root)
    if before["worktree_dirty"]:
        raise ValueError("paged replay requires a clean checkout")
    corpus_before = corpus_snapshot(root)
    allowed_paths = set(corpus_paths(root))
    queries = [query for case in legacy.CASES for query in case["queries"]]
    all_hits = proof.full_text_search_many(root, queries, RANK_SIZE, ranked_pages=RANK_PAGES)
    if len(all_hits) != len(queries):
        raise ValueError("incomplete batched discovery")
    results = []
    for index, (query, hits) in enumerate(zip(queries, all_hits)):
        result = {"query": query, "ranked_pages": _ranked_pages(hits),
                  "source_pages": source_pages(root, query, hits),
                  "workspace_source_pages": workspace_source_pages(root, query, hits, allowed_paths)}
        results.append((result, verified_query(root, query, result, allowed_paths)))
        proof._search_progress("verified_paged_query_ready", query_index=index,
                               query_count=len(queries),
                               source_pages=len(result["source_pages"]),
                               workspace_pages=len(result["workspace_source_pages"]))
    cases = []
    offset = 0
    for fixture in legacy.CASES:
        count = len(fixture["queries"])
        subset = results[offset:offset + count]
        offset += count
        pairs = [(query, rows[1]) for query, rows in zip(fixture["queries"], subset)]
        requirements = _requirements(fixture, pairs)
        cases.append({"id": fixture["id"], "queries": fixture["queries"],
                      "query_results": [row[0] for row in subset], "required_sources": requirements,
                      "found_all_required_sources": all(row["found"] for row in requirements.values()),
                      "scope_review": fixture["scope_review"]})
    impact = legacy._case10_change_impact_regression()
    after = proof.load_dataset(root)
    corpus_after = corpus_snapshot(root)
    for key in ("snapshot_commit", "worktree_dirty", "source_digests"):
        if before[key] != after[key]:
            raise ValueError("checkout changed during replay")
    if corpus_before != corpus_after:
        raise ValueError("search corpus changed during replay")
    return {"schema": SCHEMA, "snapshot_commit": before["snapshot_commit"], "worktree_dirty": False,
            "authority_source_digests": before["source_digests"], "corpus_snapshot": corpus_before,
            "ranking": {"window": RANK_SIZE, "pages": RANK_PAGES, "batched_scan_count": 1},
            "source_page_budget": {"size": SOURCE_SIZE, "pages_per_locator": SOURCE_PAGES,
                                   "pages_per_call": SOURCE_PAGES_PER_CALL},
            "workspace_source_page_budget": {"size": WORKSPACE_SOURCE_SIZE,
                                              "pages_per_locator": WORKSPACE_SOURCE_PAGES},
            "cases": cases, "search_cases_total": len(cases),
            "search_cases_found_all_sources": None,
            "benchmark_cases_total": len(cases) + 1, "change_impact_regression": impact,
            "semantic_scope_review_is_manual": True,
            "discovery_validation": "unattested",
            "provenance_boundary": "point-in-time corpus checks; no continuous immutability or toolchain attestation"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    proof._configure_stdout_utf8()
    print(json.dumps(run(ROOT), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
