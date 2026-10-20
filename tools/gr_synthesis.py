#!/usr/bin/env python3
"""Fast reading view of existing GR composition data; never an acceptance gate.

Navigation reads two local JSON files. It neither resolves Git refs nor opens
evidence, runs certificates, queries GitHub, or changes execution readiness.
Optional synthesis links and display aliases live in the existing assembly.
"""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import re

DIRECTORY = "02_REGISTRY/gr_assembly"
REPOSITORY = "https://github.com/gvakhrushev/d0_15"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def text(value: object, name: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{name}: expected text")
    return value


def rows(value: object, name: str) -> dict:
    require(isinstance(value, list), f"{name}: expected an array")
    result = {}
    for item in value:
        require(isinstance(item, dict), f"{name}: expected objects")
        key = text(item.get("id"), name)
        require(key not in result, f"{name}: duplicate {key}")
        result[key] = item
    return result


def strings(value: object, name: str) -> list[str]:
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value),
            f"{name}: expected strings")
    require(len(set(value)) == len(value), f"{name}: duplicate links")
    return value


def result_groups(results: dict) -> dict[str, list[str]]:
    """Explicit display aliases only; never infer equivalence from shared files."""
    grouped = {}
    for name, result in results.items():
        current, seen = name, set()
        while "navigation_alias_of" in results[current]:
            require(current not in seen, "navigation alias cycle")
            seen.add(current)
            target = results[current]["navigation_alias_of"]
            require(isinstance(target, str) and target in results, "unknown navigation alias")
            require(results[target].get("outcome") == result.get("outcome"),
                    "navigation aliases must preserve outcome")
            current = target
        grouped.setdefault(current, []).append(name)
    return grouped


def validate_navigation(contract: dict, intake: dict) -> None:
    """Optional reading hints: no new scientific fields are required of results."""
    results = rows(intake.get("results"), "results")
    result_groups(results)
    obligations = rows(contract.get("obligations"), "obligations")
    for name, piece in rows(contract.get("synthesis", []), "synthesis").items():
        for key in ("title", "contribution", "next_question"):
            text(piece.get(key), f"{name}.{key}")
        consumers = strings(piece.get("consumers"), name)
        require(bool(consumers) and all(x in obligations for x in consumers),
                f"{name}: unknown synthesis consumer")
        refs = strings(piece.get("results", []), name)
        require(all(x in results for x in refs), f"{name}: unknown synthesis result")
        strings(piece.get("tags", []), name)
        readings = piece.get("readings", [])
        require(isinstance(readings, list), f"{name}: expected readings")
        for reading in readings:
            require(isinstance(reading, dict), f"{name}: expected reading object")
            text(reading.get("label"), name)
            ref = reading.get("ref")
            require(isinstance(ref, str) and re.fullmatch(r"[0-9a-f]{40}", ref) is not None,
                    f"{name}: reading needs a fixed full commit")
            path = text(reading.get("path"), name)
            pure = PurePosixPath(path)
            require(not pure.is_absolute() and ".." not in pure.parts and "\\" not in path
                    and "\x00" not in path and pure.as_posix() == path,
                    f"{name}: unsafe reading path")


def read(root: Path, query: str = "") -> dict:
    directory = root / DIRECTORY
    contract = json.loads((directory / "contract.json").read_text())
    intake = json.loads((directory / "applications.json").read_text())
    require(contract.get("schema") == "d0-gr-assembly/1", "unsupported assembly schema")
    require(intake.get("schema") == "d0-gr-applications/1", "unsupported applications schema")
    validate_navigation(contract, intake)
    results = rows(intake["results"], "results")
    groups = result_groups(results)
    canonical = {alias: name for name, aliases in groups.items() for alias in aliases}
    obligations = rows(contract["obligations"], "obligations")
    pieces = []
    words = query.casefold().split()
    exact_ids = {p["id"] for p in contract.get("synthesis", [])
                 if p["id"].casefold() == query.casefold().strip()}
    for piece in contract.get("synthesis", []):
        if exact_ids and piece["id"] not in exact_ids:
            continue
        ids = list(dict.fromkeys(canonical[x] for x in piece.get("results", [])))
        hay = json.dumps(piece, ensure_ascii=False).casefold() + " " + " ".join(
            json.dumps(results[alias], ensure_ascii=False).casefold()
            for name in ids for alias in groups[name])
        if not exact_ids and not all(word in hay for word in words):
            continue
        uses = []
        for name in ids:
            result = results[name]
            evidence = next(iter(result.get("evidence", [])), {})
            uses.append({"id": name, "also_indexed_as": [x for x in groups[name] if x != name],
                         "statement": result["statement"], "scope_level": result.get("scope_level"),
                         "hypotheses": result.get("hypotheses", {}),
                         "source": evidence})
        pieces.append({**piece, "uses": uses,
                       "consumer_statements": {x: obligations[x]["statement"] for x in piece["consumers"]},
                       "execution_tasks": [tid for tid, binding in contract.get("task_bindings", {}).items()
                                           if set(piece["consumers"]) &
                                           (set(binding.get("obligations", [])) | {binding.get("consumer")})]})
    return {"pieces": pieces, "query": query, "evidence_verified": False,
            "scientific_promotion": False, "live_verified": False,
            "authority": "Reading links propose composition; proof acceptance and live execution use the existing check/review/dispatch commands."}


def source_link(source: dict, label: str) -> str:
    if source.get("ref") and source.get("path"):
        return f"[{label}]({REPOSITORY}/blob/{source['ref']}/{source['path']})"
    return label


def render(data: dict) -> str:
    lines = ["# D0 → ОТО: собрать следующий переход", "",
             "<!-- Generated by gr_assembly.py render from existing assembly metadata. -->", "",
             "Карта чтения и научного синтеза. Связи показывают возможное использование результатов;",
             "приёмка доказательств и живое исполнение остаются в существующем workflow.", ""]
    if not data["pieces"]:
        lines += ["Совпадений нет. Попробуйте `puzzle` без фильтра или `search QUERY`.", ""]
    for piece in data["pieces"]:
        lines += [f"## {piece['id']} — {piece['title']}", "", piece["contribution"], "",
                  "**Следующий переход:** " + piece["next_question"], "",
                  "**Куда подставляется:** " + ", ".join(f"`{x}`" for x in piece["consumers"]), "",
                  "**Взять из уже опубликованного:**"]
        for result in piece["uses"]:
            link = source_link(result["source"], result["id"])
            lines.append(f"- {link}")
        for reading in piece.get("readings", []):
            lines.append(f"- {source_link(reading, reading['label'])} — опубликованный исследовательский вход")
        if piece["execution_tasks"]:
            lines += ["", "**Связанные существующие задачи:** " + ", ".join(f"`{x}`" for x in piece["execution_tasks"])]
        lines.append("")
    lines += ["Узкий вход: `python3 tools/gr_assembly.py puzzle source` (также: `vacuum`, `roots`, `refinement`, `matter`).",
              "Содержимое результата с гипотезами: `python3 tools/gr_assembly.py --json puzzle QUERY`.",
              "Перед запуском работы: `python3 tools/task_dispatch.py TASK-ID`.",
              "Во время синтеза достаточно изменённого расчёта/узкого теста; окончательная проверка — на приёмке.", ""]
    return "\n".join(lines)
