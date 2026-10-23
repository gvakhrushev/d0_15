"""Repeatable cold-start retrieval checks over real D0 cases.

Text matches remain candidates. This runner checks that the expected pinned
owner/application references are surfaced in the bounded result set; it does
not make a semantic acceptance decision.
"""
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import proof_architecture as proof


CASES: list[dict[str, Any]] = [
    {
        "id": "labelled-native-raising-inverse",
        "queries": ["native raising operator inverse null leg"],
        "required_refs": [
            "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md",
            "02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md",
        ],
        "scope_review": "Owner all-jet null-leg inverse and the concrete consumer are distinct; this is not physical price selection.",
    },
    {
        "id": "positive-nonvacuum-recovery",
        "queries": ["exact positive nonvacuum 16+24+2 midpoint recovery"],
        "required_refs": [
            "A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md",
        ],
        "scope_review": "Exact finite recovery and physical native Book selection remain separate.",
    },
    {
        "id": "golden-step-vs-internal-ratio",
        "queries": ["Golden physical metric step internal Perron scale ratio native HJR countercontrol"],
        "required_refs": [
            "A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md",
        ],
        "scope_review": "Physical metric homogeneity and internal Bratteli scale ratio are not interchangeable; native HJR remains a countercontrol.",
    },
    {
        "id": "fixedright-stationary-and-minimum-scopes",
        "queries": [
            "curved fixedRIGHT128 preparation R covector",
            "stationary preparation minimum saddle Fredholm cutoff cusp",
        ],
        "required_refs": [
            "A4D_EXACT_CURVED_NATIVE_DIRAC_FIXED_RIGHT_PREPARATION_AND_SOURCE_2026_10_20.md",
        ],
        "scope_review": "Stationarity, minimum, saddle, Fredholm continuation, and cutoff cusp require separate owners and conclusions.",
    },
    {
        "id": "same-fields-do-not-fix-price-source",
        "queries": [
            "same field coframe different action cut Info clock source equivalence",
            "same-action/source map",
        ],
        "required_refs": [
            "A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md",
        ],
        "scope_review": "Equality of geometric data does not imply action, cut, Info, clock, or source equivalence.",
    },
    {
        "id": "same-prefix-two-ending-prospective-price",
        "queries": [
            "same-prefix two-ending Julia odds equal continuation partition weights absolute Book anchor",
            "actual Julia Born odds native K-weight continuation partition weights",
        ],
        "required_refs": [
            "A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md",
            "A4D_NATIVE_FOUR_COPY_TO_CURVATURE_APPLICATION_2026_10_20.md",
        ],
        "scope_review": "The prospective identity requires equal full continuation partition weights; it supplies neither an absolute normalizer nor physical source selection.",
    },
    {
        "id": "clock-dirac-incidence-curvature",
        "queries": [
            "chronological clock spatial CAR Dirac paired incidence d2 curvature complement modes",
            "native clock pressure complete price synthesis",
            "native weighted Dirac boundary",
            "native pairing refinement source",
        ],
        "required_refs": [
            "A4D_NATIVE_CLOCK_PRESSURE_AND_COMPLETE_PRICE_SYNTHESIS_2026_10_20.md",
            "A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md",
            "A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md",
        ],
        "scope_review": "Chronological clock, spatial CAR Dirac, paired incidence, and d² curvature/complement modes need their explicit maps.",
    },
    {
        "id": "gain-readiness-vs-trace-multiplicity",
        "queries": [
            "source gain readiness trace multiplicity",
            "four copy curvature application readiness derivative gain",
            "AF scene heat comparison trace multiplicity",
        ],
        "required_refs": [
            "A4D_NATIVE_FOUR_COPY_TO_CURVATURE_APPLICATION_2026_10_20.md",
            "A4D_NATIVE_AF_SCENE_HEAT_COMPARISON.md",
        ],
        "scope_review": "Readiness/source gain and trace multiplicity are separate quantities and claims.",
    },
    {
        "id": "conditional-transfer-does-not-select-execution",
        "queries": ["generic verification theory transfer Bellman optimal premise physical execution"],
        "required_refs": [
            "D0_FOUNDATION_THEORY_TRANSFER_COMPOSITION_2026_10_20.md",
            "MEMO_A4D_RESOLVED_AFFINE_PROGRAM.md",
        ],
        "scope_review": "Generic transfer and Bellman consequences with an optimality premise do not choose physical execution.",
    },
    {
        "id": "verification-kernel-transfer-outside-gr",
        "queries": [
            "verification_core representedRecord complete future kernel",
            "Interpretation.transfer_theorem translated regime premise source_proof",
        ],
        "required_refs": [
            "D0_VERIFICATION_CORE_COMPOSITION_2026_10_20.md",
            "03_FORMALIZATION/D0/Foundation/VerificationCore.lean",
            "D0_FOUNDATION_THEORY_TRANSFER_COMPOSITION_2026_10_20.md",
            "03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean",
        ],
        "scope_review": "The verification kernel and generic transfer are reusable mathematical results; an incorrect decoder/operation map must fail, and no physical execution is selected.",
    },
    {
        "id": "scoped-nogo-vs-positive-existence",
        "queries": [
            "native affine probe no-go arbitrary smooth probes physical contrast",
            "native realization closure positive existence physical",
        ],
        "required_refs": [
            "A4D_NATIVE_AFFINE_PROBE_NOGO.md",
            "A4D_NATIVE_REALIZATION_CLOSURE.md",
        ],
        "scope_review": "A scoped negative rules out only its declared route and does not discharge positive existence.",
    },
]


def _path_matches(actual: str, expected: str) -> bool:
    actual = actual.replace("\\", "/").casefold()
    expected = expected.replace("\\", "/").casefold()
    return actual == expected or actual.endswith("/" + expected) or expected.endswith("/" + actual)


def _case10_change_impact_regression() -> dict[str, Any]:
    """Verify exact source changes alter the linked check input, prose does not."""
    with tempfile.TemporaryDirectory(prefix="d0-proof-impact-") as temp:
        root = pathlib.Path(temp)
        source_rel = "02_REGISTRY/research/native_source.md"
        source_path = root / source_rel
        source_path.parent.mkdir(parents=True)
        source_path.write_text("Declared source normalization premise v1.\n", encoding="utf-8")
        unrelated = root / "unrelated-prose.md"
        unrelated.write_text("Independent historical prose.\n", encoding="utf-8")
        dataset = {
            "root": root,
            "claims": [], "assumptions": [], "formal_support": [], "aliases": [],
            "assembly": {
                "results": [{"id": "native-result", "statement": "Native source application",
                             "evidence": [{"path": source_rel}]}],
                "applications": [{"id": "native-result-to-obligation",
                                  "result": "native-result", "obligation": "native-obligation"}],
                "attempts": [],
            },
            "contract": {"obligations": [], "interfaces": [], "goals": [],
                         "anti_substitutions": [], "synthesis": [],
                         "source_fork_reconciliations": []},
            "presuppositions": {"edges": []},
            "snapshot_commit": "fixture", "source_digests": {},
        }
        before = proof.impact_view(dataset, source_rel)
        before_hash = before["source_snapshot"]["source_sha256"]
        linked = before["declared_impact"][0]["declared_applications"][0]["id"]

        source_path.write_text("Declared source normalization premise v2.\n", encoding="utf-8")
        after_source = proof.impact_view(dataset, source_rel)
        changed_hash = after_source["source_snapshot"]["source_sha256"]

        unrelated.write_text("Edited unrelated historical prose.\n", encoding="utf-8")
        after_unrelated = proof.impact_view(dataset, source_rel)
        unrelated_path = proof.impact_view(dataset, "unrelated-prose.md")
        unchanged_hash = after_unrelated["source_snapshot"]["source_sha256"]
        passed = (before_hash != changed_hash == unchanged_hash and
                  linked == "native-result-to-obligation" and
                  unrelated_path["matches"] == [])
        return {"id": "exact-source-vs-unrelated-prose",
                "status": "pass" if passed else "fail",
                "source_hash_changed": before_hash != changed_hash,
                "unrelated_prose_left_source_hash": changed_hash == unchanged_hash,
                "declared_application": linked}


def run(root: pathlib.Path, limit: int = 5) -> dict[str, Any]:
    queries = [query for case in CASES for query in case["queries"]]
    all_hits = proof.full_text_search_many(root, queries, limit)
    offset = 0
    cases = []
    for case in CASES:
        query_hits = []
        for query in case["queries"]:
            query_hits.append(all_hits[offset])
            offset += 1
        required_status = {}
        for required in case["required_refs"]:
            rank = None
            candidate_path = None
            query_match = None
            for query, hits in zip(case["queries"], query_hits):
                for index, hit in enumerate(hits, start=1):
                    referenced = [ref["path"] for ref in hit.get("source_refs", [])]
                    candidates = [hit.get("source", ""), *referenced]
                    if any(_path_matches(str(path), required) for path in candidates):
                        rank, candidate_path, query_match = index, hit.get("source"), query
                        break
                if rank is not None:
                    break
            required_status[required] = {"found": rank is not None,
                                         "candidate_rank": rank,
                                         "citing_candidate": candidate_path,
                                         "query": query_match}
        cases.append({
            "id": case["id"],
            "queries": case["queries"],
            "required_sources": required_status,
            "found_all_required_sources": all(x["found"] for x in required_status.values()),
            "query_results": [
                {"query": query, "top_candidates": [
                    {"path": hit["source"], "matched_terms": hit["matched_terms"],
                     "query_terms": hit["query_terms"], "source_sha256": hit["source_sha256"],
                     "source_refs": [ref["path"] for ref in hit.get("source_refs", [])[:5]]}
                    for hit in hits
                ]}
                for query, hits in zip(case["queries"], query_hits)
            ],
            "scope_review": case["scope_review"],
        })
    dataset = proof.load_dataset(root)
    change_regression = _case10_change_impact_regression()
    return {
        "snapshot_commit": dataset["snapshot_commit"],
        "worktree_dirty": dataset["worktree_dirty"],
        "authority_source_digests": dataset["source_digests"],
        "search_limit": limit,
        "search_cases_found_all_sources": sum(c["found_all_required_sources"] for c in cases),
        "search_cases_total": len(cases),
        "benchmark_cases_total": len(cases) + 1,
        "cases": cases,
        "change_impact_regression": change_regression,
        "semantic_scope_review_is_manual": True,
    }


def main() -> int:
    root = proof.ROOT.resolve()
    print(json.dumps(run(root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

