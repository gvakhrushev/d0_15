"""Compare the legacy assembly search and proof-architecture search on the
same real cold-start questions.

This is a retrieval-surface comparison only. It does not judge semantic owner
selection, hypothesis preservation, or whether a result requires new
mathematics; those require reviewing the complete bounded answer/application.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from tools import gr_assembly, proof_architecture as proof
from tools.proof_architecture_cold_start import CASES, _path_matches


def expected_sources(case: dict[str, Any], query_index: int) -> list[str]:
    """Return only sources explicitly scoped to this question in the fixture."""
    return sorted({
        str(source["path"])
        for source in case.get("required_sources", [])
        if query_index in source.get("scope_query_indexes", [])
    })


def selected_query(case: dict[str, Any]) -> tuple[int, str]:
    """Choose one existing query with an explicit source target, if available."""
    scoped_indexes = sorted({
        int(index)
        for source in case.get("required_sources", [])
        for index in source.get("scope_query_indexes", [])
        if 0 <= int(index) < len(case["queries"])
    })
    index = scoped_indexes[0] if scoped_indexes else 0
    return index, str(case["queries"][index])


def _old_paths(hits: list[dict[str, Any]]) -> list[list[str]]:
    return [sorted({str(path) for path in hit.get("evidence_paths", [])})
            for hit in hits]


def _matches_expected(paths: list[str], expected: list[str]) -> bool:
    return any(_path_matches(path, source) for path in paths for source in expected)


def _new_cli_answer(dataset: dict[str, Any], query: str,
                    text_hits: list[dict[str, Any]]) -> dict[str, Any]:
    structured = proof.structured_search(dataset, query)
    seen = {(item["kind"], item["key"]) for item in structured}
    return {
        "query": query,
        "structured_matches": [proof._search_summary(item) for item in structured],
        "text_candidates": [
            proof._search_candidate_summary(item, dataset)
            for item in text_hits
            if (item["kind"], item["key"]) not in seen
        ],
    }


def run(root: pathlib.Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    selected = [(case, *selected_query(case)) for case in CASES]
    queries = [query for _case, _index, query in selected]
    legacy_model = gr_assembly.load(root)
    dataset = proof.load_dataset(root)
    new_text_hits = proof.full_text_search_many(
        root, queries, proof.MAX_SEARCH_RESULTS
    )

    rows: list[dict[str, Any]] = []
    offset = 0
    for case, query_index, query in selected:
        old_hits = gr_assembly.search(legacy_model, query)
        text_hits = new_text_hits[offset]
        new_answer = _new_cli_answer(dataset, query, text_hits)
        old_paths = _old_paths(old_hits)
        new_structured = new_answer["structured_matches"]
        new_text = new_answer["text_candidates"]
        new_owner_values = set()
        for item in [*new_structured, *new_text]:
            new_owner_values.update(
                str(owner) for owner in
                ([item.get("owner")] + list(item.get("owners", []))) if owner
            )
            source_links = item.get("declared_source_links", {})
            new_owner_values.update(
                str(owner) for owner in source_links.get("owners", []) if owner
            )
        new_owner_values = sorted(new_owner_values)
        expected = expected_sources(case, query_index)

        old_relevant_candidates = sum(
            _matches_expected(paths, expected) for paths in old_paths
        )
        old_source_hits = [source for source in expected
                           if any(_path_matches(path, source)
                                  for paths in old_paths for path in paths)]
        new_text_paths = [str(item.get("source", "")) for item in new_text]
        new_relevant_candidates = sum(
            _matches_expected([path], expected) for path in new_text_paths
        )
        new_source_hits = [
            source for source in expected
            if any(_path_matches(path, source) for path in new_text_paths)
        ]
        expected_owner_links: dict[tuple[str, str, str], dict[str, Any]] = {}
        for item in new_text:
            candidate_path = str(item.get("source", ""))
            source_links = item.get("declared_source_links", {})
            for expected_source in expected:
                if (proof._normalized_source_path(candidate_path)
                        != proof._normalized_source_path(expected_source)):
                    continue
                for result in source_links.get("assembly_results", []):
                    owner = result.get("owner")
                    result_id = str(result.get("result_id", ""))
                    if not owner:
                        continue
                    key = (expected_source, result_id, str(owner))
                    expected_owner_links[key] = {
                        "source": expected_source,
                        "result_id": result_id,
                        "owner": str(owner),
                        "interface": result.get("interface"),
                        "evidence": result.get("evidence", []),
                    }
        expected_owner_links_list = [
            expected_owner_links[key] for key in sorted(expected_owner_links)
        ]
        expected_source_link_details = []
        for expected_source in expected:
            candidate = next((
                item for item in new_text
                if proof._normalized_source_path(item.get("source"))
                == proof._normalized_source_path(expected_source)
            ), None)
            if candidate is None:
                expected_source_link_details.append({
                    "source": expected_source,
                    "candidate_surfaced": False,
                    "owner_status": "candidate_not_surfaced",
                    "owners": [],
                    "assembly_results": [],
                    "formal_support_locators": [],
                    "source_header_owner_declarations": [],
                    "source_refs": [],
                })
                continue
            source_links = candidate.get("declared_source_links", {})
            expected_source_link_details.append({
                "source": expected_source,
                "candidate_surfaced": True,
                "owner_status": source_links.get("owner_status"),
                "owners": source_links.get("owners", []),
                "assembly_results": source_links.get("assembly_results", []),
                "formal_support_locators": source_links.get("formal_support_locators", []),
                "source_header_owner_declarations": candidate.get(
                    "source_header_owner_declarations", []
                ),
                "source_origin": candidate.get("source_origin"),
                "source_sha256": candidate.get("source_sha256"),
                "source_commit": candidate.get("source_commit"),
                "source_blob": candidate.get("source_blob"),
                "pin_status": candidate.get("pin_status"),
                "direct_content": candidate.get("direct_content"),
                "source_refs": candidate.get("source_refs", []),
            })
        expected_sources_without_owner_link = sorted(
            source for source in expected if not any(
                link["source"] == source for link in expected_owner_links_list
            )
        )
        old_serialized = json.dumps(old_hits, ensure_ascii=False, indent=2)
        new_serialized = json.dumps(new_answer, ensure_ascii=False, indent=2)
        rows.append({
            "case_id": case["id"],
            "query_index": query_index,
            "query": query,
            "query_sha256": hashlib.sha256(query.encode("utf-8")).hexdigest(),
            "expected_sources": expected,
            "legacy": {
                "result_ids": [str(item.get("id", "")) for item in old_hits],
                "owners": sorted({str(owner) for item in old_hits
                                  for owner in ([item.get("owner")] +
                                                list(item.get("owners", [])))
                                  if owner}),
                "candidate_count": len(old_hits),
                "expected_source_hits": old_source_hits,
                "relevant_candidate_count": old_relevant_candidates,
                "candidate_count_not_in_scoped_source_set": (
                    len(old_hits) - old_relevant_candidates if expected else None
                ),
                "serialized_answer_bytes": len(old_serialized.encode("utf-8")),
            },
            "current": {
                "structured_matches": [f"{item.get('kind')}:{item.get('key')}"
                                        for item in new_structured],
                "owners": new_owner_values,
                "text_candidate_paths": new_text_paths,
                "structured_match_count": len(new_structured),
                "text_candidate_count": len(new_text),
                "expected_source_hits": new_source_hits,
                "expected_source_owner_links": expected_owner_links_list,
                "expected_source_link_details": expected_source_link_details,
                "expected_sources_without_direct_owner_link": expected_sources_without_owner_link,
                "relevant_text_candidate_count": new_relevant_candidates,
                "text_candidate_count_not_in_scoped_source_set": (
                    len(new_text) - new_relevant_candidates if expected else None
                ),
                "serialized_answer_bytes": len(new_serialized.encode("utf-8")),
            },
            "semantic_review": {
                "owner_correctness": (
                    "exact registered links are shown; independent owner correctness "
                    "is not assessed by search output"
                ),
                "hypothesis_preservation": "not_assessed_by_search_output",
                "new_mathematics_required": "not_assessed_by_search_output",
            },
        })
        offset += 1

    scoped = [row for row in rows if row["expected_sources"]]
    old_hits = sum(bool(row["legacy"]["expected_source_hits"]) for row in scoped)
    new_hits = sum(bool(row["current"]["expected_source_hits"]) for row in scoped)
    legacy_bytes = sum(row["legacy"]["serialized_answer_bytes"] for row in rows)
    current_bytes = sum(row["current"]["serialized_answer_bytes"] for row in rows)
    return {
        "schema": "d0-proof-architecture-search-comparison-v1",
        "snapshot_commit": dataset["snapshot_commit"],
        "worktree_dirty": dataset["worktree_dirty"],
        "authority_source_digests": dataset["source_digests"],
        "runner_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        "query_fixture_sha256": hashlib.sha256(
            pathlib.Path(__file__).with_name("proof_architecture_cold_start.py").read_bytes()
        ).hexdigest(),
        "comparison_scope": {
            "legacy": "gr_assembly.search over the existing assembly result records",
            "current": (
                "proof_architecture search over structured authorities, five "
                "bounded text candidates, and exact-path links to existing "
                "assembly/formal-support records"
            ),
            "questions": (
                "one identical existing query per real cold-start case, chosen "
                "from an explicitly source-scoped query where available"
            ),
            "context_measure": "serialized UTF-8 JSON answer bytes; a response-size proxy, not model-token or file-read accounting",
            "semantic_limit": "search output alone does not establish owner correctness, hypothesis preservation, or whether new mathematics is required",
        },
        "metrics": {
            "query_count": len(rows),
            "query_count_with_explicit_source_scope": len(scoped),
            "legacy_scoped_queries_with_expected_source": old_hits,
            "current_scoped_queries_with_expected_source": new_hits,
            "legacy_serialized_answer_bytes_total": legacy_bytes,
            "current_serialized_answer_bytes_total": current_bytes,
            "legacy_average_answer_bytes": round(legacy_bytes / len(rows), 1) if rows else 0,
            "current_average_answer_bytes": round(current_bytes / len(rows), 1) if rows else 0,
            "legacy_owner_bearing_queries": sum(
                bool(row["legacy"]["owners"]) for row in rows
            ),
            "current_owner_bearing_queries": sum(
                bool(row["current"]["owners"]) for row in rows
            ),
            "current_scoped_queries_with_expected_source_owner_link": sum(
                bool(row["current"]["expected_source_owner_links"])
                for row in scoped
            ),
            "current_expected_source_owner_link_count": sum(
                len(row["current"]["expected_source_owner_links"])
                for row in scoped
            ),
            "current_scoped_queries_with_expected_source_header_owner_declaration": sum(
                any(detail.get("source_header_owner_declarations")
                    for detail in row["current"]["expected_source_link_details"])
                for row in scoped
            ),
            "current_expected_source_header_owner_declaration_count": sum(
                len(detail.get("source_header_owner_declarations", []))
                for row in scoped
                for detail in row["current"]["expected_source_link_details"]
            ),
            "current_scoped_expected_sources_without_direct_owner_link": sum(
                len(row["current"]["expected_sources_without_direct_owner_link"])
                for row in scoped
            ),
            "semantic_review_required_for_all_queries": True,
        },
        "cases": rows,
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
