"""Validate and compact the opt-in paged cold-start v3 report.

Returned source evidence and bounded pages are rechecked against current bytes.
By default discovery and ranks are unattested. An explicit optional rerun
compares all ranked pages with a fresh batched run of the same implementation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as legacy
from tools import proof_architecture_cold_start_v3 as paged
from tools import compact_proof_architecture_cold_start as old_compactor

SUMMARY_SCHEMA = "d0-proof-architecture-cold-start-paged-summary-v3"


def compact(full_bytes: bytes, root: pathlib.Path = ROOT, *,
            verify_discovery: bool = False) -> dict[str, Any]:
    root = root.resolve()
    full = json.loads(full_bytes)
    if not isinstance(full, dict) or full.get("schema") != paged.SCHEMA:
        raise ValueError("not a paged v3 replay")
    head = old_compactor._git(root, "rev-parse", "HEAD")
    dirty = bool(old_compactor._git(root, "status", "--porcelain=v1", "--untracked-files=all"))
    dataset = proof.load_dataset(root)
    old_compactor._validate_snapshot(full, head, dirty, dataset["source_digests"])
    if dataset["snapshot_commit"] != head or dataset["worktree_dirty"]:
        raise ValueError("checkout changed during snapshot verification")
    if (full.get("ranking") != {"window": paged.RANK_SIZE, "pages": paged.RANK_PAGES,
                               "batched_scan_count": 1} or
            full.get("source_page_budget") != {"size": paged.SOURCE_SIZE,
                                               "pages_per_locator": paged.SOURCE_PAGES,
                                               "pages_per_call": paged.SOURCE_PAGES_PER_CALL}):
        raise ValueError("paged replay budgets do not match the v3 contract")
    corpus = paged.corpus_snapshot(root)
    if full.get("corpus_snapshot") != corpus:
        raise ValueError("paged replay corpus differs from current checkout")
    allowed_paths = set(paged.corpus_paths(root))
    cases = full.get("cases")
    if not isinstance(cases, list) or len(cases) != len(legacy.CASES):
        raise ValueError("incomplete paged case set")
    replayed = None
    if verify_discovery:
        queries = [query for fixture in legacy.CASES for query in fixture["queries"]]
        replayed = proof.full_text_search_many(root, queries, paged.RANK_SIZE,
                                              ranked_pages=paged.RANK_PAGES)
        if len(replayed) != len(queries):
            raise ValueError("incomplete batched discovery rerun")
    replay_offset = 0
    summary_cases = []
    for case, fixture in zip(cases, legacy.CASES):
        if (not isinstance(case, dict) or case.get("id") != fixture["id"] or
                case.get("queries") != fixture["queries"] or
                case.get("scope_review") != fixture["scope_review"]):
            raise ValueError("paged case or scope differs from the fixture")
        query_results = case.get("query_results")
        if not isinstance(query_results, list) or len(query_results) != len(fixture["queries"]):
            raise ValueError("incomplete paged query set")
        if replayed is not None:
            for result, hits in zip(query_results, replayed[replay_offset:replay_offset + len(query_results)]):
                if not isinstance(result, dict) or result.get("ranked_pages") != paged._ranked_pages(hits):
                    raise ValueError("ranked pages disagree with batched discovery rerun")
            replay_offset += len(query_results)
        pairs = [(query, paged.verified_query(root, query, result, allowed_paths))
                 for query, result in zip(fixture["queries"], query_results)]
        required = paged._requirements(fixture, pairs)
        if case.get("required_sources") != required:
            raise ValueError("paged source receipts disagree with verified query evidence")
        found_all = all(row["found"] for row in required.values())
        if case.get("found_all_required_sources") is not found_all:
            raise ValueError("paged case result disagrees with receipts")
        if verify_discovery:
            required = paged._requirements(fixture, pairs, discovery_attested=True)
            found_all = all(row["found"] for row in required.values())
        summary_cases.append({"id": fixture["id"], "query_count": len(query_results),
                              "required_source_count": len(required),
                              "all_required_sources_found": found_all,
                              "missing_paths": ([row["path"] for row in required.values() if not row["found"]]
                                                if verify_discovery else None),
                              "discovery_unattested_paths": ([] if verify_discovery else list(required)),
                              "scope_review": fixture["scope_review"], "required_sources": required,
                              "source_page_count": sum(len(row["source_pages"]) for row in query_results)})
    if (full.get("search_cases_total") != len(cases) or
            full.get("benchmark_cases_total") != len(cases) + 1 or
            full.get("search_cases_found_all_sources") is not None or
            full.get("discovery_validation") != "unattested" or
            full.get("semantic_scope_review_is_manual") is not True):
        raise ValueError("paged totals or manual-review boundary disagree")
    impact = full.get("change_impact_regression")
    if (not isinstance(impact, dict) or impact.get("id") != "exact-source-vs-unrelated-prose" or
            impact.get("status") not in {"pass", "fail"} or
            type(impact.get("source_hash_changed")) is not bool or
            type(impact.get("unrelated_prose_left_source_hash")) is not bool or
            not isinstance(impact.get("declared_application"), str) or
            (impact["status"] == "pass" and not
             (impact["source_hash_changed"] and impact["unrelated_prose_left_source_hash"] and
              impact["declared_application"] == "native-result-to-obligation"))):
        raise ValueError("invalid change-impact receipt")
    after = proof.load_dataset(root)
    if (after["snapshot_commit"] != head or after["worktree_dirty"] or
            after["source_digests"] != dataset["source_digests"] or
            paged.corpus_snapshot(root) != corpus):
        raise ValueError("checkout changed during paged compaction")
    return {"schema": SUMMARY_SCHEMA, "snapshot_commit": head, "worktree_dirty": False,
            "authority_source_digests": dataset["source_digests"], "corpus_snapshot": corpus,
            "ranking": full["ranking"], "source_page_budget": full["source_page_budget"],
            "cases": summary_cases, "search_cases_total": len(cases),
            "search_cases_found_all_sources": (sum(row["all_required_sources_found"] for row in summary_cases)
                                                if verify_discovery else None),
            "discovery_validation": ("batched_rerun_same_implementation" if verify_discovery else
                                     "unattested"),
            "benchmark_cases_total": len(cases) + 1, "change_impact_regression": impact,
            "semantic_scope_review_is_manual": True,
            "full_output_sha256": hashlib.sha256(full_bytes).hexdigest(),
            "provenance_boundary": ("bounded evidence rechecked; batched discovery rerun with same implementation; "
                                    "corpus checked only at endpoints; no independent implementation or continuous snapshot attestation"
                                    if verify_discovery else
                                    "bounded evidence rechecked; discovery and ranks unattested; corpus checked only at endpoints")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--verify-discovery", action="store_true",
                        help="rerun one full batched search before accepting discovery")
    args = parser.parse_args()
    try:
        proof._configure_stdout_utf8()
        result = compact(args.input.read_bytes(), verify_discovery=args.verify_discovery)
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
        else:
            sys.stdout.write(rendered)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"paged cold-start compaction failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
