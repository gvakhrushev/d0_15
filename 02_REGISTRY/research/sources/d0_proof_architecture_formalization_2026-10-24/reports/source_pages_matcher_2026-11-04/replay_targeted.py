"""Replay the 17-query diagnostic on the caller's checkout, without overwrites.

This is not the full 50-case acceptance replay. Its observed checkout and
authority digests are recorded; a changed checkout is not the historical run.
"""
import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from tools import proof_architecture as proof
from tools import proof_architecture_cold_start as cold


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(ROOT):
        parser.error("write diagnostic output outside the repository")
    case = next(row for row in cold.CASES if row["id"] == "pr334-native-kappa-owner-delta")
    before = proof.load_dataset(ROOT)
    start = time.monotonic()
    hits = proof.full_text_search_many(ROOT, case["queries"], 18)
    pages = [proof.expand_source_pages(ROOT, query, rows)
             for query, rows in zip(case["queries"], hits)]
    pairs = [(query, cold._query_hits_with_source_pages(query, rows, source_pages))
             for query, rows, source_pages in zip(case["queries"], hits, pages)]
    required = case["required_sources"] + [{"path": path} for path in case["required_refs"]]
    receipts = [cold._required_source_status(pairs, row) for row in required]
    after = proof.load_dataset(ROOT)
    for key in ("snapshot_commit", "worktree_dirty", "source_digests"):
        if before[key] != after[key]:
            raise RuntimeError("checkout changed during diagnostic")
    result = {"case": case["id"], "snapshot_commit": before["snapshot_commit"],
              "worktree_dirty": before["worktree_dirty"],
              "authority_source_digests": before["source_digests"],
              "seconds": time.monotonic() - start,
              "query_results": [{"query": query, "top_candidates": rows, "source_pages": ps}
                                for query, rows, ps in zip(case["queries"], hits, pages)],
              "required_sources": receipts}
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"found": sum(row["found"] for row in receipts), "total": len(receipts)}))
    return 0 if all(row["found"] for row in receipts) else 1


if __name__ == "__main__":
    raise SystemExit(main())
