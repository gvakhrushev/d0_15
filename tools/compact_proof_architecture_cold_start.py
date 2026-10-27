#!/usr/bin/env python3
"""Compact a complete cold-start replay while retaining its source receipts.

Run the existing cold-start runner on a clean commit and write its full JSON
outside the repository. Then, on that same still-clean commit, run this tool::

    python3 tools/compact_proof_architecture_cold_start.py \
        --input /tmp/d0_cold_full.json --output /tmp/d0_cold_summary.json

The compactor does not rerun or authenticate the supplied replay. It checks
its self-reported snapshot, current authority digests, complete case/query
fixture, and pinned source receipts against the clean current checkout. It
does not infer semantic acceptance or carry forward Lean or comparison results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as cold_start

VIEW_PATH = (
    "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
    "claim_source_candidates_current.json"
)
RUNNER_PATH = "tools/proof_architecture_cold_start.py"
SEARCH_PATH = "tools/proof_architecture.py"
TEST_PATH = "tools/test_proof_architecture.py"
COMPACTOR_PATH = "tools/compact_proof_architecture_cold_start.py"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(root: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], stderr=subprocess.PIPE,
        text=True, encoding="utf-8",
    ).strip()


def _validate_snapshot(full: dict[str, Any], head: str, dirty: bool,
                       authority_digests: dict[str, str]) -> None:
    if dirty or full.get("worktree_dirty") is not False:
        raise ValueError("the replay and current checkout must both be clean")
    if not re.fullmatch(r"[0-9a-f]{40}", head) or full.get("snapshot_commit") != head:
        raise ValueError("the replay snapshot must equal the current HEAD")
    if full.get("authority_source_digests") != authority_digests:
        raise ValueError("replay authority source digests differ from the current checkout")


def _expected_requirements(fixture: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Reproduce the runner's keys, including two pins for one path."""
    expected: dict[str, dict[str, Any]] = {}
    for source in fixture.get("required_sources", []):
        key = source["path"]
        if key in expected:
            pin = source.get("commit") or source.get("blob") or str(len(expected))
            key = f"{key}@{pin}"
        if key in expected:
            raise ValueError(f"duplicate required-source key: {key}")
        expected[key] = source
    pinned_paths = {source["path"] for source in fixture.get("required_sources", [])}
    for path in fixture["required_refs"]:
        if path not in pinned_paths:
            expected[path] = {"path": path}
    return expected


def _direct_candidates(result: dict[str, Any], required: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    return [(rank, hit) for rank, hit in enumerate(result["top_candidates"], 1)
            if cold_start._path_matches(str(hit.get("path", "")), required["path"]) and
            hit.get("direct_content") is True and
            (required.get("commit") is None or hit.get("source_commit") == required["commit"]) and
            (required.get("blob") is None or hit.get("source_blob") == required["blob"])]


def _summarize_case(case: dict[str, Any], fixture: dict[str, Any], limit: int) -> dict[str, Any]:
    case_id = fixture["id"]
    if case.get("id") != case_id or case.get("queries") != fixture["queries"]:
        raise ValueError(f"case or query fixture mismatch: {case_id}")
    if case.get("scope_review") != fixture["scope_review"]:
        raise ValueError(f"manual scope review mismatch: {case_id}")
    results = case.get("query_results")
    if not isinstance(results, list) or len(results) != len(fixture["queries"]):
        raise ValueError(f"incomplete query results: {case_id}")
    for query, result in zip(fixture["queries"], results):
        if (not isinstance(result, dict) or result.get("query") != query or
                not isinstance(result.get("top_candidates"), list) or
                len(result["top_candidates"]) > limit):
            raise ValueError(f"malformed query results: {case_id}")
        hit_fields = {"path", "matched_terms", "matched_term_names", "query_terms",
                      "source_sha256", "source_origin", "direct_content", "source_commit",
                      "source_blob", "pin_status", "evidence_lines", "source_refs"}
        if any(not isinstance(hit, dict) or not hit_fields <= set(hit) or
               not isinstance(hit.get("direct_content"), bool) or
               not isinstance(hit.get("evidence_lines"), list) or
               not isinstance(hit.get("source_refs"), list)
               for hit in result["top_candidates"]):
            raise ValueError(f"incomplete candidate records: {case_id}")
    requirements = _expected_requirements(fixture)
    receipts = case.get("required_sources")
    if not isinstance(receipts, dict) or set(receipts) != set(requirements):
        raise ValueError(f"incomplete required-source receipts: {case_id}")
    for key, required in requirements.items():
        receipt = receipts[key]
        receipt_fields = {"path", "status", "found", "source_origin", "expected_commit",
                          "expected_blob", "required_sections", "sections_found",
                          "missing_sections", "scoped_queries", "candidate_rank", "query",
                          "evidence_lines", "citation_only_refs"}
        if (not isinstance(receipt, dict) or receipt.get("path") != required["path"] or
                not receipt_fields <= set(receipt) or
                receipt.get("expected_commit") != required.get("commit") or
                receipt.get("expected_blob") != required.get("blob") or
                receipt.get("required_sections") != [str(value) for value in required.get("sections", [])] or
                not isinstance(receipt.get("sections_found"), list) or
                receipt.get("missing_sections") != sorted(
                    set(receipt.get("required_sections", [])) - set(receipt.get("sections_found", []))) or
                not isinstance(receipt.get("evidence_lines"), list) or
                not isinstance(receipt.get("citation_only_refs"), list) or
                not isinstance(receipt.get("found"), bool) or
                not isinstance(receipt.get("status"), str)):
            raise ValueError(f"invalid required-source receipt: {case_id}: {key}")
        scoped = receipt.get("scoped_queries")
        indexes = required.get("scope_query_indexes") or []
        if not isinstance(scoped, list) or [row.get("query_index") for row in scoped] != indexes:
            raise ValueError(f"incomplete scoped-query receipts: {case_id}: {key}")
        for index, row in zip(indexes, scoped):
            expected_query = fixture["queries"][index] if index < len(fixture["queries"]) else None
            expected_sections = [str(value) for value in required.get("scope_query_sections", {}).get(
                str(index), required.get("scope_query_sections", {}).get(index, []))]
            if (row.get("query") != expected_query or not isinstance(row.get("found"), bool) or
                    not isinstance(row.get("status"), str) or
                    not isinstance(row.get("evidence_lines"), list) or
                    row.get("required_sections") != expected_sections or
                    not isinstance(row.get("sections_found"), list) or
                    row.get("missing_sections") != sorted(
                        set(expected_sections) - set(row.get("sections_found", [])))):
                raise ValueError(f"invalid scoped-query receipt: {case_id}: {key}")
            if row["found"]:
                hits = _direct_candidates(results[index], required)
                if not hits or row.get("candidate_rank") != hits[0][0]:
                    raise ValueError(f"scoped success has no matching direct hit: {case_id}: {key}")
        if receipt["found"] and (receipt["status"] != "found_direct_content" or
                                 receipt.get("missing_sections") or
                                 any(not row["found"] for row in scoped)):
            raise ValueError(f"inconsistent successful source receipt: {case_id}: {key}")
        if receipt["found"]:
            matched = [(rank, hit) for result in results if result["query"] == receipt["query"]
                       for rank, hit in _direct_candidates(result, required)
                       if rank == receipt["candidate_rank"]]
            if not matched or matched[0][1].get("source_origin") != receipt["source_origin"]:
                raise ValueError(f"source success has no matching direct hit: {case_id}: {key}")
    found_all = all(row["found"] for row in receipts.values())
    if case.get("found_all_required_sources") is not found_all:
        raise ValueError(f"inconsistent case result: {case_id}")
    return {
        "id": case_id,
        "query_count": len(results),
        "required_source_count": len(receipts),
        "all_required_sources_found": found_all,
        "missing_paths": [row["path"] for row in receipts.values() if not row["found"]],
        "scope_review": case["scope_review"],
        # Keep the runner's full per-source receipts, including pin, section,
        # scoped-query, rank, evidence and negative/citation-only statuses.
        "required_sources": receipts,
    }


def _exact_retrieval(case: dict[str, Any], fixture: dict[str, Any],
                     suffix: str, query_index: int) -> dict[str, Any]:
    requirements = [row for row in fixture.get("required_sources", [])
                    if row["path"].endswith(suffix) and
                    query_index in row.get("scope_query_indexes", [])]
    if len(requirements) != 1:
        raise ValueError(f"expected one pinned source for {suffix} at query {query_index}")
    required = requirements[0]
    records = [row for row in case["required_sources"].values()
               if row["path"] == required["path"] and
               row.get("expected_commit") == required.get("commit") and
               row.get("expected_blob") == required.get("blob")]
    if len(records) != 1:
        raise ValueError(f"missing unique pinned receipt for {suffix}")
    record = records[0]
    scoped = [row for row in record["scoped_queries"] if row["query_index"] == query_index]
    if len(scoped) != 1:
        raise ValueError(f"missing scoped receipt for {suffix}")
    scoped = scoped[0]
    query_result = case["query_results"][query_index]
    matches = _direct_candidates(query_result, required)
    if scoped["found"] and not matches:
        raise ValueError(f"scoped success has no exact pinned hit: {suffix}")
    if matches and scoped.get("candidate_rank") != matches[0][0]:
        raise ValueError(f"scoped candidate rank disagrees with the full replay: {suffix}")
    return {
        "path": required["path"], "commit": required.get("commit"),
        "blob": required.get("blob"), "query_index": query_index,
        "query": query_result["query"], "found": scoped["found"],
        "status": scoped["status"],
        "source_origin": matches[0][1].get("source_origin") if matches else None,
        "candidate_rank": scoped.get("candidate_rank"),
        "required_sections": scoped.get("required_sections", []),
        "sections_found": scoped.get("sections_found", []),
        "missing_sections": scoped.get("missing_sections", []),
    }


def _compact_cases(full: dict[str, Any], fixtures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cases = full.get("cases")
    limit = full.get("search_limit")
    if (not isinstance(cases, list) or len(cases) != len(fixtures) or
            not isinstance(limit, int) or limit != cold_start.COLD_START_MIN_RESULT_WINDOW):
        raise ValueError("incomplete cold-start case set or unexpected search window")
    result = [_summarize_case(case, fixture, limit) for case, fixture in zip(cases, fixtures)]
    if (full.get("search_cases_total") != len(result) or
            full.get("benchmark_cases_total") != len(result) + 1 or
            full.get("search_cases_found_all_sources") !=
            sum(row["all_required_sources_found"] for row in result)):
        raise ValueError("cold-start totals disagree with their case receipts")
    if full.get("semantic_scope_review_is_manual") is not True:
        raise ValueError("manual semantic-review boundary is missing")
    impact = full.get("change_impact_regression")
    if (not isinstance(impact, dict) or impact.get("id") != "exact-source-vs-unrelated-prose" or
            impact.get("status") not in {"pass", "fail"} or
            not isinstance(impact.get("source_hash_changed"), bool) or
            not isinstance(impact.get("unrelated_prose_left_source_hash"), bool) or
            not isinstance(impact.get("declared_application"), str)):
        raise ValueError("change-impact regression receipt is incomplete")
    if impact["status"] == "pass" and not (impact["source_hash_changed"] and
                                           impact["unrelated_prose_left_source_hash"] and
                                           impact["declared_application"] == "native-result-to-obligation"):
        raise ValueError("change-impact pass conflicts with its controls")
    return result


def _candidate_view(root: pathlib.Path, authority_digests: dict[str, str]) -> dict[str, Any]:
    path = root / VIEW_PATH
    raw = path.read_bytes()
    view = json.loads(raw)
    pin = view.get("snapshot_commit")
    if (view.get("schema") != "d0-claim-source-candidate-view-v3" or
            view.get("worktree_dirty") is not False or
            not isinstance(pin, str) or not re.fullmatch(r"[0-9a-f]{40}", pin) or
            view.get("claim_registry_sha256") != authority_digests["02_REGISTRY/claims.csv"] or
            not isinstance(view.get("counts"), dict) or
            not isinstance(view.get("book_sources"), dict)):
        raise ValueError("claim-source candidate view has stale or incomplete provenance")
    _git(root, "cat-file", "-e", f"{pin}^{{commit}}")
    for source, entry in view["book_sources"].items():
        source_path = (root / source).resolve()
        if not source_path.is_relative_to(root.resolve()) or not isinstance(entry, dict):
            raise ValueError(f"invalid candidate-view book source: {source}")
        if _sha(source_path.read_bytes()) != entry.get("source_sha256"):
            raise ValueError(f"candidate-view book source is stale: {source}")
    return {"path": VIEW_PATH, "snapshot_commit": pin, "worktree_dirty": False,
            "claim_registry_sha256": view["claim_registry_sha256"],
            "view_sha256": _sha(raw), "counts": view["counts"],
            "book_sources": view["book_sources"]}


def compact(full_bytes: bytes, root: pathlib.Path = ROOT) -> dict[str, Any]:
    """Validate and compact one full replay against a clean current checkout."""
    root = root.resolve()
    full = json.loads(full_bytes)
    if not isinstance(full, dict):
        raise ValueError("full replay must be a JSON object")
    head = _git(root, "rev-parse", "HEAD")
    dirty = bool(_git(root, "status", "--porcelain=v1", "--untracked-files=all"))
    if dirty:
        raise ValueError("current checkout must be clean before compaction")
    dataset = proof.load_dataset(root)
    if dataset["snapshot_commit"] != head or dataset["worktree_dirty"]:
        raise ValueError("checkout changed while reading authority sources")
    _validate_snapshot(full, head, dirty, dataset["source_digests"])
    cases = _compact_cases(full, cold_start.CASES)
    candidate_view = _candidate_view(root, dataset["source_digests"])

    index = next(i for i, case in enumerate(cold_start.CASES)
                 if case["id"] == "positive-nonvacuum-recovery")
    raw_case, fixture, summary_case = full["cases"][index], cold_start.CASES[index], cases[index]
    summary_case["exact_application_retrieval"] = _exact_retrieval(
        raw_case, fixture, "nonvacuum_compact_pointwise_margin_2026-10-27.json", 17)
    summary_case["cubic_family_retrieval"] = _exact_retrieval(
        raw_case, fixture, "nonvacuum_cubic_profile_car_margin_2026-10-27.json", 18)
    summary_case["cubic_lean_source_retrieval"] = _exact_retrieval(
        raw_case, fixture, "NonvacuumBrinkmannStencil.lean", 18)
    lean = _exact_retrieval(raw_case, fixture, "NonvacuumBrinkmannStencil.lean", 19)
    inventory = _exact_retrieval(
        raw_case, fixture, "nonvacuum_cubic_profile_same_record_euclidean_refinement_2026-10-27.json", 19)
    summary_case["same_record_euclidean_refinement_retrieval"] = {
        "query_index": 19, "query": lean["query"],
        "found": lean["found"] and inventory["found"],
        "status": "found_direct_content" if lean["found"] and inventory["found"] else "missing_pinned_source",
        "source_origin": lean["source_origin"] if lean["source_origin"] == inventory["source_origin"] else "mixed",
        "lean_source_path": lean["path"], "lean_source_commit": lean["commit"],
        "lean_source_blob": lean["blob"], "lean_candidate_rank": lean["candidate_rank"],
        "inventory_path": inventory["path"], "inventory_commit": inventory["commit"],
        "inventory_blob": inventory["blob"], "inventory_candidate_rank": inventory["candidate_rank"],
    }
    eq24 = _exact_retrieval(
        raw_case, fixture, "A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md", 14)
    eq24["required_section"] = "7.2"
    if "7.2" not in eq24["required_sections"]:
        raise ValueError("Eq. (24) receipt does not require section 7.2")

    replay = {"source_commit": head, "command": "python3 tools/proof_architecture_cold_start.py"}
    for label, path in (("runner", RUNNER_PATH), ("search_engine", SEARCH_PATH),
                        ("test", TEST_PATH), ("compactor", COMPACTOR_PATH)):
        replay[label + "_sha256"] = _sha((root / path).read_bytes())
        replay[label + "_git_blob"] = _git(root, "rev-parse", f"{head}:{path}")
    replay["full_output_sha256"] = _sha(full_bytes)
    replay["full_output_bytes"] = len(full_bytes)
    if _git(root, "rev-parse", "HEAD") != head or _git(
            root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise ValueError("checkout changed while compacting the replay")
    return {
        "schema": "d0-proof-architecture-cold-start-summary-v2",
        "snapshot_commit": head, "worktree_dirty": False,
        "authority_source_digests": full["authority_source_digests"],
        "search_limit": full["search_limit"],
        "search_cases_found_all_sources": full["search_cases_found_all_sources"],
        "search_cases_total": full["search_cases_total"],
        "benchmark_cases_total": full["benchmark_cases_total"], "cases": cases,
        "change_impact_regression": full["change_impact_regression"],
        "semantic_scope_review_is_manual": True,
        "required_source_ref_count": sum(row["required_source_count"] for row in cases),
        "claim_source_candidate_view": candidate_view, "replay": replay,
        "eq24_owner_source_retrieval": eq24,
        "report_compaction": {
            "reason": "Retains every required-source receipt and exact application retrieval; omits full candidate arrays.",
            "full_output_bytes": len(full_bytes), "full_output_sha256": _sha(full_bytes),
            "provenance_limit": "The supplied full replay is not rerun or authenticated by the compactor.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=pathlib.Path,
                        help="complete JSON from proof_architecture_cold_start.py")
    parser.add_argument("--output", type=pathlib.Path,
                        help="new output path; omit to write JSON to stdout")
    args = parser.parse_args()
    try:
        proof._configure_stdout_utf8()
        result = compact(args.input.read_bytes())
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(rendered)
    except (OSError, ValueError, KeyError, IndexError, TypeError, subprocess.CalledProcessError) as error:
        print(f"cold-start compaction failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
