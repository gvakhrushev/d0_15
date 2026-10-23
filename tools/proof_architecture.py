#!/usr/bin/env python3
"""Bounded, read-only search and composition view over existing D0 authorities.

This is a generated view. Claims, assembly contracts, result evidence, and
Lean declaration facts continue to be owned by their existing source files.
Text search returns candidates only; it never accepts a mathematical edge.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
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
MAX_SEARCH_RESULTS = 5
MAX_SNIPPET = 650
MAX_FIELD_CHARS = 8000


def read_json(root: pathlib.Path, relative: pathlib.Path) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8-sig"))


def read_csv(root: pathlib.Path, relative: pathlib.Path) -> list[dict[str, str]]:
    with (root / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


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


def structured_search(dataset: dict[str, Any], query: str, limit: int = MAX_SEARCH_RESULTS) -> list[dict[str, Any]]:
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


def _query_terms(query: str) -> list[str]:
    return [t.casefold() for t in re.findall(r"[\w.-]+", query, flags=re.UNICODE) if len(t) > 1]


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


def _filename_bonus(rel: str, terms: list[str]) -> float:
    """Prefer a source whose own title names the queried mathematical topic."""
    stem = pathlib.PurePosixPath(rel).stem.casefold()
    filename_terms = set(re.findall(r"[\w]+", stem.replace("_", " ").replace("-", " "),
                                    flags=re.UNICODE))
    if not terms:
        return 0.0
    return 0.40 * sum(term in filename_terms for term in terms) / len(terms)


def _source_references(lines: list[str]) -> list[dict[str, Any]]:
    """Expose exact path/hash pins present in the lines that matched the query."""
    path_pattern = re.compile(
        r"(?<![\w])(?:[\w.-]+[\\/])*[\w.-]+\.(?:md|lean|json|csv|py)(?:#[^\s,;]*)?",
        flags=re.IGNORECASE,
    )
    hash_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", flags=re.IGNORECASE)
    found: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}
    for line in lines:
        hashes = tuple(dict.fromkeys(hash_pattern.findall(line)))
        for path in path_pattern.findall(line):
            normalized = path.replace("\\", "/")
            key = (normalized, hashes)
            found[key] = {"path": normalized, "hashes": list(hashes),
                          "context": line[:MAX_SNIPPET]}
    return list(found.values())[:12]


def full_text_search_many(root: pathlib.Path, queries: list[str],
                          limit: int = MAX_SEARCH_RESULTS) -> list[list[dict[str, Any]]]:
    """Search several cold-start questions in one corpus pass."""
    terms_by_query = [_query_terms(query) for query in queries]
    unique_terms = sorted({term for terms in terms_by_query for term in terms})
    if not unique_terms:
        return [[] for _ in queries]
    roots = [name for name in TEXT_ROOTS if (root / name).is_dir()]
    if not roots:
        return [[] for _ in queries]
    text_globs = ["-g", "*.md", "-g", "*.lean", "-g", "*.json", "-g", "*.csv",
                  "-g", "*.py", "-g", "*.toml"]
    rg_query = ["rg", "--files-with-matches", "--ignore-case", "--fixed-strings",
                *text_globs]
    for term in unique_terms:
        rg_query.extend(["-e", term])
    file_list = subprocess.run(
        [*rg_query, *roots], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if file_list.returncode not in (0, 1):
        raise RuntimeError(f"rg text search failed ({file_list.returncode}): {file_list.stderr}")
    candidate_paths = set(filter(None, file_list.stdout.splitlines()))
    all_files = subprocess.run(["rg", "--files", *text_globs, *roots], cwd=root,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
    if all_files.returncode not in (0, 1):
        raise RuntimeError(f"rg file listing failed ({all_files.returncode}): {all_files.stderr}")
    for raw_rel in filter(None, all_files.stdout.splitlines()):
        stem = pathlib.PurePosixPath(raw_rel.replace("\\", "/")).stem.casefold()
        if any(term in stem for term in unique_terms):
            candidate_paths.add(raw_rel)

    candidates_by_query: list[list[tuple[float, str, dict[str, Any]]]] = [
        [] for _ in queries
    ]
    for raw_rel in sorted(candidate_paths):
        rel = raw_rel.replace("\\", "/")
        if (rel in {"tools/proof_architecture.py", "tools/proof_architecture_cold_start.py"}
                or rel.startswith("tools/test_")):
            continue
        path = root / pathlib.Path(raw_rel)
        try:
            if path.stat().st_size > 4_000_000:
                continue
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        file_title = path.stem
        folded = (file_title + "\n" + content).casefold()
        content_lines = content.splitlines()
        folded_lines = [line.casefold() for line in content_lines]
        title_line = f"Filename: {file_title}"
        title_folded = title_line.casefold()
        term_present = {term: term in folded for term in unique_terms}
        for index, terms in enumerate(terms_by_query):
            if not terms:
                continue
            hits = sum(term_present[term] for term in terms)
            min_hits = 1 if len(terms) <= 3 else max(2, (len(terms) + 3) // 4)
            if hits < min_hits:
                continue
            matching_lines = ([title_line] if any(term in title_folded for term in terms) else [])
            matching_lines.extend(line.strip() for line, folded_line in zip(content_lines, folded_lines)
                                  if any(term in folded_line for term in terms))
            matching_lines.sort(key=lambda line: (
                -sum(term in line.casefold() for term in terms), len(line), line
            ))
            snippet = " | ".join(matching_lines[:3])[:MAX_SNIPPET]
            score = hits / len(terms) + _owner_bonus(rel) + _filename_bonus(rel, terms)
            record = {"kind": "text-candidate", "key": rel, "label": snippet,
                      "source": rel, "source_sha256": sha256(path),
                      "source_refs": _source_references(matching_lines[:12]),
                      "matched_terms": hits, "query_terms": len(terms)}
            candidates_by_query[index].append((score, rel, record))
    results = []
    for candidates in candidates_by_query:
        candidates.sort(key=lambda row: (-row[0], row[1]))
        results.append([record for _, _, record in candidates[:limit]])
    return results


def full_text_search(root: pathlib.Path, query: str,
                     limit: int = MAX_SEARCH_RESULTS) -> list[dict[str, Any]]:
    """Return bounded text candidates from books, registry, and Lean sources."""
    return full_text_search_many(root, [query], limit)[0]


def _search_summary(item: dict[str, Any]) -> dict[str, Any]:
    """Keep the search response small; use `show` for the full source record."""
    return {"kind": item.get("kind"), "key": item.get("key"),
            "label": str(item.get("label", ""))[:MAX_SNIPPET],
            "source": item.get("source")}


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


def relation_view(dataset: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    """Return declared application links; never infer missing semantic edges."""
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
                if a.get("result") == result_id or a.get("obligation") == obligation_id]
    claim_id = record.get("claim_id") if item["kind"] == "claim-metadata" else None
    registered_assumptions = [assumption for assumption in dataset["assumptions"]
                              if claim_id and assumption.get("claim_id") == claim_id]
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
        "scoped_attempts": attempts,
        "conceptual_presupposition_edges": conceptual_edges,
        "warning": "Declared metadata links are not Lean type-checking or independent scientific acceptance.",
    }


def why_view(dataset: dict[str, Any], key: str) -> dict[str, Any]:
    obligation = next((x for x in records(dataset) if x["kind"] == "obligation" and x["key"] == key), None)
    if obligation:
        view = relation_view(dataset, obligation)
        interface_id = obligation["record"].get("interface")
        interface = next((x["record"] for x in records(dataset)
                          if x["kind"] == "interface" and x["key"] == interface_id), None)
        expected = set(obligation["record"].get("hypotheses", {}))
        for application in view["declared_applications"]:
            mapping = application.get("hypothesis_map", {})
            mapped_targets = set()
            if isinstance(mapping, dict):
                for value in mapping.values():
                    if isinstance(value, dict) and value.get("target_hypothesis"):
                        mapped_targets.add(value["target_hypothesis"])
                    elif isinstance(value, str):
                        mapped_targets.add(value)
            application["hypothesis_mapping_gaps"] = sorted(expected - mapped_targets)
        return {"key": key, "obligation": obligation["record"],
                "interface": interface,
                **view,
                "hypotheses": obligation["record"].get("hypotheses", {}),
                "snapshot_commit": dataset["snapshot_commit"],
                "interpretation": "Mapping coverage is reported mechanically; its correctness requires review. A declared method and accepted review still do not replace typed Lean/application evidence."}
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


def _render_text(value: Any) -> str:
    def bound(item: Any) -> Any:
        if isinstance(item, str) and len(item) > MAX_FIELD_CHARS:
            digest = hashlib.sha256(item.encode("utf-8")).hexdigest()
            return item[:MAX_FIELD_CHARS] + f"… [truncated {len(item) - MAX_FIELD_CHARS} chars; sha256={digest}]"
        if isinstance(item, list):
            values = [bound(value) for value in item[:32]]
            if len(item) > 32:
                values.append({"_omitted_items": len(item) - 32})
            return values
        if isinstance(item, dict):
            return {key: bound(value) for key, value in item.items()}
        return item
    return json.dumps(bound(value), ensure_ascii=False, indent=2, sort_keys=False)


def main() -> int:
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
    reuse = sub.add_parser("reuse", help="show declared applications and scoped attempts for a key")
    reuse.add_argument("key")
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
                      "text_candidates": [x for x in text_hits if (x["kind"], x["key"]) not in seen],
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
            hits = find_exact(data, args.key)
            result = {"key": args.key, "matches": [
                {"item": item, **relation_view(data, item)} for item in hits
            ], "snapshot_commit": data["snapshot_commit"], "source_digests": data["source_digests"]}
        else:
            if not args.key:
                parser.error("impact requires KEY unless --base is supplied")
            result = impact_view(data, args.key)
    if "data" in locals():
        result.setdefault("snapshot_commit", data["snapshot_commit"])
        result.setdefault("worktree_dirty", data["worktree_dirty"])
    print(_render_text(result) if args.json else _render_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
