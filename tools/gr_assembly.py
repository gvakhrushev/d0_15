#!/usr/bin/env python3
"""Read-only composition, intake and dispatch checks for the D0 gravity route.

The graph checks declared contracts; it cannot prove mathematical applicability.
Only a pinned independent acceptance can discharge an obligation. Historical
research is searchable evidence, never an automatic scientific status upgrade.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

import gr_synthesis

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = "02_REGISTRY/gr_assembly"
INTERFACE_FIELDS = {"carrier", "action", "variations", "source", "normalization", "refinement", "scope"}
OUTCOMES = {"positive", "negative", "classification"}
MODES = {"research", "proof", "verification"}
SHA = re.compile(r"[0-9a-f]{40}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]*\Z")


class AssemblyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssemblyError(message)


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def text_field(value: object, label: str, limit: int = 1200) -> str:
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit,
            f"{label}: expected nonempty text of at most {limit} characters")
    return value


def path_in(root: Path, name: object) -> Path:
    text_field(name, "path", 500)
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in name
            and "\x00" not in name and bool(p.parts), f"unsafe repository path: {name}")
    resolved = (root / name).resolve()
    require(resolved.is_relative_to(root.resolve()), f"path escapes repository: {name}")
    return resolved


def records(rows: object, label: str) -> dict:
    require(isinstance(rows, list), f"{label}: expected an array")
    result = {}
    for row in rows:
        require(isinstance(row, dict), f"{label}: expected objects")
        name = row.get("id")
        require(isinstance(name, str) and ID.fullmatch(name) is not None, f"{label}: invalid id")
        require(name not in result, f"{label}: duplicate id {name}")
        result[name] = row
    return result


def _carrier_edge_matches(edge: dict, slot: str, left: str, right: str) -> bool:
    return (edge.get("slot") == slot and edge.get("type") == "distinct-from"
            and {edge.get("left_interface"), edge.get("right_interface")} == {left, right})


def _has_declared_carrier_edge(model: dict, binding: dict, slot: str, left: str, right: str) -> bool:
    declared = set(binding.get("distinct_from", []))
    edges = model["carrier_distinctions"]
    return any(edge_id in declared and _carrier_edge_matches(edges[edge_id], slot, left, right)
               for edge_id in declared if edge_id in edges)


def string_list(value: object, label: str) -> list[str]:
    require(isinstance(value, list) and all(isinstance(v, str) and v for v in value),
            f"{label}: expected a string array")
    require(len(value) == len(set(value)), f"{label}: duplicate entries")
    return value


def acyclic(edges: dict[str, set[str]], label: str) -> None:
    done, visiting = set(), []

    def visit(node):
        if node in visiting:
            raise AssemblyError(f"{label}: cycle: {' -> '.join(visiting + [node])}")
        if node in done:
            return
        visiting.append(node)
        for dep in sorted(edges.get(node, set())):
            visit(dep)
        visiting.pop()
        done.add(node)

    for node in edges:
        visit(node)


def evidence_bytes(root: Path, evidence: dict) -> bytes:
    """Verify immutable bytes, without fetching, executing or writing evidence."""
    require(isinstance(evidence, dict), "evidence must be an object")
    ref, sha = evidence.get("ref"), evidence.get("sha256")
    require(isinstance(ref, str) and SHA.fullmatch(ref) is not None, "evidence needs a full commit ref")
    require(isinstance(sha, str) and HASH.fullmatch(sha) is not None, "evidence needs SHA-256")
    path_in(root, evidence.get("path"))
    if "snapshot" in evidence:
        snapshot = evidence["snapshot"]
        require(snapshot.startswith(DIRECTORY + "/sources/"), "snapshots must live in assembly sources")
        data = path_in(root, snapshot).read_bytes()
    else:
        try:
            data = subprocess.check_output(
                ["git", "show", f"{evidence['ref']}:{evidence['path']}"],
                cwd=root, stderr=subprocess.PIPE, timeout=15)
        except (OSError, subprocess.SubprocessError) as exc:
            raise AssemblyError(f"unavailable pinned evidence {evidence['ref']}:{evidence['path']}; "
                                "fetch its published source before acceptance") from exc
    require(hashlib.sha256(data).hexdigest() == evidence["sha256"],
            f"evidence SHA-256 mismatch: {evidence['path']}")
    if evidence.get("excerpt"):
        require(evidence["excerpt"].encode() in data, f"evidence excerpt missing: {evidence['path']}")
    return data


def load(root: Path) -> dict:
    root = root.resolve()
    contract = json.loads((root / DIRECTORY / "contract.json").read_text())
    intake = json.loads((root / DIRECTORY / "applications.json").read_text())
    require(contract.get("schema") == "d0-gr-assembly/1", "unsupported assembly schema")
    require(intake.get("schema") == "d0-gr-applications/1", "unsupported applications schema")
    imported = json.loads(evidence_bytes(root, contract["legacy_import"]))
    evidence_bytes(root, contract["route_input"])
    old_nodes = records(imported.get("nodes"), "historical nodes")
    require(len(old_nodes) == contract["legacy_import"]["node_count"], "historical node count changed")
    old_edges = {n: set(string_list(v.get("depends_on"), n)) for n, v in old_nodes.items()}
    require(all(d in old_nodes for deps in old_edges.values() for d in deps), "dangling historical dependency")
    acyclic(old_edges, "historical graph")
    migration = intake.get("migration")
    require(isinstance(migration, dict) and set(migration) == set(old_nodes), "migration must cover every historical id exactly")
    results = records(intake.get("results"), "results")
    for name, node in old_nodes.items():
        rid = "legacy:" + name
        require(migration[name].get("result") == rid and rid not in results, "historical alias collision")
        negative = str(node.get("terminal_class", "")).startswith("NO-GO")
        results[rid] = {
            "id": rid, "statement": node["scope"], "interface": None,
            "outcome": "negative" if negative else "unclassified",
            "hypotheses": {f"h{i + 1}": h for i, h in enumerate(node.get("hypotheses", []))},
            "reported_state": node["status"], "historical": True,
            "owners": node.get("owners", []), "depends_on": node.get("depends_on", []),
        }
    model = {"root": root, "contract": contract, "intake": intake, "results": results,
             "obligations": records(contract.get("obligations"), "obligations"),
             "carrier_distinctions": records(contract.get("carrier_distinctions", []), "carrier_distinctions"),
             "applications": records(intake.get("applications"), "applications"),
             "attempts": records(intake.get("attempts"), "attempts")}
    validate(model)
    return model


def premise_contract(model: dict, name: str) -> dict:
    ob = model["obligations"][name]
    return {k: ob.get(k) for k in ["id", "statement", "interface", "outcome", "scope_level", "hypotheses", "allow_passport"]} | {
        "interface_definition": model["contract"]["interfaces"][ob["interface"]]}


def application_digest(model: dict, app: dict) -> str:
    target = model["obligations"][app["obligation"]]
    result = model["results"][app["result"]]
    interface = model["contract"]["interfaces"]
    method = next(m for m in target["methods"] if m["id"] == app["method"])
    dependencies = set(method["requires"]) | {b["obligation"] for b in app["hypothesis_map"].values() if "obligation" in b}
    return digest({
        "application": {k: v for k, v in app.items() if k != "review" and not k.startswith("_")},
        "target": premise_contract(model, target["id"]), "result": result,
        "method": {"id": method["id"], "requires": sorted(method["requires"])},
        "prerequisite_contracts": {name: premise_contract(model, name) for name in sorted(dependencies)},
        "target_interface": interface[target["interface"]],
        "result_interface": interface.get(result.get("interface")),
    })


def attempt_digest(model: dict, attempt: dict) -> str:
    return digest({"attempt": {k: v for k, v in attempt.items() if k != "review" and not k.startswith("_")},
                   "result": model["results"][attempt["result"]],
                   "interface": model["contract"]["interfaces"][attempt["interface"]]})


def accepted_review(model: dict, record: dict, expected_digest: str) -> bool:
    review = record.get("review", {})
    require(isinstance(review, dict) and review.get("state") in {"proposed", "accepted", "rejected"},
            f"{record['id']}: review state must be proposed, accepted or rejected")
    if review["state"] != "accepted":
        return False
    text_field(review.get("by"), "independent reviewer", 150)
    require(review["by"] != model["results"][record["result"]].get("owner"),
            "acceptance reviewer must differ from the result owner")
    require(review.get("digest") == expected_digest, f"{record['id']}: stale acceptance digest")
    raw = evidence_bytes(model["root"], review.get("decision"))
    marker = f"Assembly-Acceptance: {record['id']} {expected_digest}"
    require(marker.encode() in raw, f"{record['id']}: pinned acceptance marker missing")
    return True


def _validate_fork_pin(pin: object, label: str) -> None:
    require(isinstance(pin, dict)
            and set(pin) == {"number", "head", "base", "task_fields"},
            f"{label}: invalid exact PR pin")
    require(isinstance(pin["number"], int) and not isinstance(pin["number"], bool)
            and pin["number"] > 0, f"{label}: invalid PR number")
    for side in ("head", "base"):
        ref = pin[side]
        require(isinstance(ref, dict) and set(ref) == {"repository", "branch", "sha"},
                f"{label}.{side}: invalid branch pin")
        text_field(ref["repository"], f"{label}.{side}.repository", 200)
        text_field(ref["branch"], f"{label}.{side}.branch", 300)
        require(isinstance(ref["sha"], str) and SHA.fullmatch(ref["sha"]) is not None,
                f"{label}.{side}: invalid Git SHA")
    fields = string_list(pin["task_fields"], f"{label}.task_fields")
    require(len(fields) <= 1, f"{label}: ambiguous Task metadata cannot be reconciled")


def _validate_source_fork_reconciliations(model: dict) -> None:
    rows = model["contract"].get("source_fork_reconciliations", [])
    reconciliations = records(rows, "source_fork_reconciliations")
    for rid, reconciliation in reconciliations.items():
        require(set(reconciliation) == {"id", "parent", "children", "disposition", "reopen_when"},
                f"{rid}: invalid source-fork reconciliation fields")
        _validate_fork_pin(reconciliation["parent"], f"{rid}.parent")
        parent_tasks = reconciliation["parent"]["task_fields"]
        require(len(parent_tasks) == 1 and parent_tasks[0] in model["contract"]["task_bindings"],
                f"{rid}: parent must pin one registered Task")
        children = reconciliation["children"]
        require(isinstance(children, list) and len(children) >= 2,
                f"{rid}: source fork needs at least two children")
        child_numbers = []
        for index, child in enumerate(children):
            label = f"{rid}.children[{index}]"
            require(isinstance(child, dict)
                    and set(child) == {"pin", "merge_base_sha", "child_only_delta", "result_ids"},
                    f"{label}: invalid child reconciliation")
            _validate_fork_pin(child["pin"], f"{label}.pin")
            child_numbers.append(child["pin"]["number"])
            require(child["pin"]["task_fields"] == [],
                    f"{label}: a child with Task metadata needs ownership reconciliation")
            require(isinstance(child["merge_base_sha"], str)
                    and SHA.fullmatch(child["merge_base_sha"]) is not None,
                    f"{label}: invalid merge-base SHA")
            delta = child["child_only_delta"]
            require(isinstance(delta, list) and bool(delta), f"{label}: child delta is required")
            paths = []
            for file in delta:
                require(isinstance(file, dict)
                        and set(file) == {"status", "path", "git_blob", "parent_git_blob"},
                        f"{label}: invalid child delta entry")
                require(file["status"] in {"A", "M", "D", "R"}, f"{label}: invalid delta status")
                path_in(model["root"], file["path"])
                paths.append(file["path"])
                if file["status"] == "D":
                    require(file["git_blob"] is None, f"{label}: deleted path cannot pin a child blob")
                else:
                    require(isinstance(file["git_blob"], str) and SHA.fullmatch(file["git_blob"]) is not None,
                            f"{label}: invalid child Git blob")
                require(file["parent_git_blob"] is None
                        or isinstance(file["parent_git_blob"], str)
                        and SHA.fullmatch(file["parent_git_blob"]) is not None,
                        f"{label}: invalid parent Git blob")
            require(len(paths) == len(set(paths)), f"{label}: duplicate child delta path")
            result_ids = string_list(child["result_ids"], f"{label}.result_ids")
            require(bool(result_ids) and all(result_id in model["results"] for result_id in result_ids),
                    f"{label}: source-fork results must resolve to indexed result-only evidence")
        require(child_numbers == sorted(set(child_numbers)), f"{rid}: children must be unique and sorted by PR number")
        require(reconciliation["disposition"] == "comparison-complete-result-only",
                f"{rid}: source-fork comparison cannot accept child evidence")
        string_list(reconciliation["reopen_when"], f"{rid}.reopen_when")
        require(bool(reconciliation["reopen_when"]), f"{rid}: stale comparison triggers must be explicit")


def _live_fork_pin(pr: dict) -> dict | None:
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    head_repo = head.get("repo") or {}
    base_repo = base.get("repo") or {}
    number = pr.get("number")
    if (not isinstance(number, int) or isinstance(number, bool)
            or not all(isinstance(value, str) and value for value in
                       (head_repo.get("full_name"), head.get("ref"), head.get("sha"),
                        base_repo.get("full_name"), base.get("ref"), base.get("sha")))):
        return None
    return {
        "number": number,
        "head": {"repository": head_repo["full_name"], "branch": head["ref"], "sha": head["sha"]},
        "base": {"repository": base_repo["full_name"], "branch": base["ref"], "sha": base["sha"]},
        "task_fields": metadata(pr.get("body") or "", "Task"),
    }


def matching_source_fork_reconciliation(model: dict, parent: dict, children: list[dict]) -> dict | None:
    """Match a reviewed fork while its exact child-delta paths remain unchanged."""
    parent_pin = _live_fork_pin(parent)
    child_pins = [_live_fork_pin(child) for child in children]
    if parent_pin is None or any(pin is None for pin in child_pins):
        return None
    child_pins = sorted(child_pins, key=lambda pin: pin["number"])
    for reconciliation in model["contract"].get("source_fork_reconciliations", []):
        recorded_parent = reconciliation["parent"]
        same_parent_except_head = (
            recorded_parent["number"] == parent_pin["number"]
            and recorded_parent["head"]["repository"] == parent_pin["head"]["repository"]
            and recorded_parent["head"]["branch"] == parent_pin["head"]["branch"]
            and recorded_parent["base"] == parent_pin["base"]
            and recorded_parent["task_fields"] == parent_pin["task_fields"]
        )
        if not same_parent_except_head:
            continue
        recorded_children = [child["pin"] for child in reconciliation["children"]]
        if recorded_children != child_pins:
            continue
        if recorded_parent["head"]["sha"] != parent_pin["head"]["sha"]:
            if parent.get("_assembly_source_path_blobs_complete") is not True:
                continue
            expected = {
                item["path"]: item["parent_git_blob"]
                for child in reconciliation["children"]
                for item in child["child_only_delta"]
            }
            if parent.get("_assembly_source_path_blobs") != expected:
                continue
        return reconciliation
    return None


def prepare_source_fork_path_snapshots(model: dict, prs: list[dict], root: Path, lookup) -> None:
    """Refresh only child-delta path blobs when a reviewed parent head advances."""
    by_number = {pr.get("number"): pr for pr in prs}
    checked = set()
    for reconciliation in model["contract"].get("source_fork_reconciliations", []):
        recorded_parent = reconciliation["parent"]
        number = recorded_parent["number"]
        parent = by_number.get(number)
        if parent is None or number in checked:
            continue
        checked.add(number)
        live_pin = _live_fork_pin(parent)
        if live_pin is None or live_pin["head"]["sha"] == recorded_parent["head"]["sha"]:
            continue
        same_parent_except_head = (
            recorded_parent["head"]["repository"] == live_pin["head"]["repository"]
            and recorded_parent["head"]["branch"] == live_pin["head"]["branch"]
            and recorded_parent["base"] == live_pin["base"]
            and recorded_parent["task_fields"] == live_pin["task_fields"]
        )
        if not same_parent_except_head:
            continue
        related = stacked_descendants(parent, prs)
        child_pins = [_live_fork_pin(child) for child in related]
        if any(pin is None for pin in child_pins):
            continue
        child_pins = sorted(child_pins, key=lambda pin: pin["number"])
        recorded_children = [child["pin"] for child in reconciliation["children"]]
        if child_pins != recorded_children:
            continue
        paths = sorted({
            item["path"]
            for child in reconciliation["children"]
            for item in child["child_only_delta"]
        })
        try:
            path_blobs = lookup(root, live_pin["head"]["sha"], paths)
            require(isinstance(path_blobs, dict) and set(path_blobs) == set(paths),
                    "incomplete child-delta path snapshot")
            require(all(blob is None or isinstance(blob, str) and SHA.fullmatch(blob) is not None
                        for blob in path_blobs.values()),
                    "invalid child-delta path blob snapshot")
            parent["_assembly_source_path_blobs"] = path_blobs
            parent["_assembly_source_path_blobs_complete"] = True
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            parent["_assembly_source_path_blobs"] = None
            parent["_assembly_source_path_blobs_complete"] = False
            parent["_assembly_source_path_blobs_error"] = str(exc)[:240]


def source_fork_reconciliation_summary(reconciliation: dict, parent: dict,
                                       live_children: list[dict]) -> dict:
    live_by_number = {child["number"]: child for child in live_children}
    live_parent = _live_fork_pin(parent)
    return {
        "id": reconciliation["id"],
        "parent_pr": reconciliation["parent"]["number"],
        "comparison_head_sha": reconciliation["parent"]["head"]["sha"],
        "current_parent_head_sha": live_parent["head"]["sha"] if live_parent else None,
        "parent_head_advanced_with_child_paths_unchanged": bool(
            live_parent
            and live_parent["head"]["sha"] != reconciliation["parent"]["head"]["sha"]
            and parent.get("_assembly_source_path_blobs_complete") is True
        ),
        "disposition": reconciliation["disposition"],
        "children_remain_unaccepted": True,
        "children": [{
            "number": item["pin"]["number"],
            "head_sha": item["pin"]["head"]["sha"],
            "merge_base_sha": item["merge_base_sha"],
            "changed_paths": [entry["path"] for entry in item["child_only_delta"]],
            "result_ids": item["result_ids"],
            "live_state": live_by_number[item["pin"]["number"]]["state"],
            "live_lifecycle": live_by_number[item["pin"]["number"]]["lifecycle"],
            "live_task": live_by_number[item["pin"]["number"]]["task"],
        } for item in reconciliation["children"]],
        "reopen_when": reconciliation["reopen_when"],
    }


def validate(model: dict) -> None:
    c, root = model["contract"], model["root"]
    try:
        gr_synthesis.validate_navigation(c, model["intake"])
    except ValueError as exc:
        raise AssemblyError(str(exc)) from exc
    interfaces, obs = c.get("interfaces"), model["obligations"]
    budget = c.get("registry_budget")
    require(isinstance(budget, dict), "registry_budget is required")
    max_active_results = budget.get("max_active_results")
    require(type(max_active_results) is int and max_active_results > 0,
            "registry_budget.max_active_results must be a positive integer")
    active_results = len(model["intake"].get("results", []))
    require(active_results <= max_active_results,
            f"active result registry budget exceeded: {active_results}/{max_active_results}; strengthen an existing result")
    require(isinstance(interfaces, dict) and bool(interfaces), "interfaces are required")
    for name, value in interfaces.items():
        require(isinstance(value, dict) and set(value) == INTERFACE_FIELDS, f"{name}: incomplete interface")
        for k, v in value.items():
            text_field(v, f"{name}.{k}", 800)
    edges = {name: set() for name in obs}
    for name, ob in obs.items():
        text_field(ob.get("statement"), name)
        require(isinstance(ob.get("hypotheses", {}), dict), f"{name}: target hypotheses must be named")
        require(ob.get("scope_level") in {"finite", "family"}, f"{name}: invalid scope level")
        require(ob.get("interface") in interfaces, f"{name}: unknown interface")
        require(ob.get("outcome") in OUTCOMES, f"{name}: unknown outcome")
        methods = records(ob.get("methods"), f"{name}.methods")
        require(bool(methods), f"{name}: needs at least one proof method")
        for method in methods.values():
            for dep in string_list(method.get("requires"), f"{name}.{method['id']}.requires"):
                require(dep in obs, f"{name}: dangling prerequisite {dep}")
                edges[name].add(dep)
    for goal in records(c.get("goals"), "goals").values():
        deps = string_list(goal.get("requires"), f"goal {goal['id']}")
        require(bool(deps) and all(d in obs for d in deps), f"{goal['id']}: invalid goal requirements")
        require(goal.get("outcome") in {"positive", "classification"}, f"{goal['id']}: invalid goal outcome")
        require(goal["outcome"] != "positive" or all(obs[d]["outcome"] == "positive" for d in deps),
                f"{goal['id']}: a positive goal cannot be supplied by negative/classification terminals")
    require(set(c.get("task_bindings", {})).isdisjoint({"CONTROL-PLANE"}), "CONTROL-PLANE is not a scientific execution")
    for edge in model["carrier_distinctions"].values():
        require(edge.get("type") == "distinct-from", f"{edge['id']}: unsupported carrier edge type")
        require(edge.get("slot") in obs, f"{edge['id']}: unknown slot")
        left, right = edge.get("left_interface"), edge.get("right_interface")
        require(left in interfaces and right in interfaces and left != right,
                f"{edge['id']}: carrier edge needs two distinct typed interfaces")
        text_field(edge.get("reason"), f"{edge['id']}.reason")
    for tid, binding in c.get("task_bindings", {}).items():
        require(binding.get("interface") in interfaces, f"{tid}: unknown interface")
        require(binding.get("carrier") == binding.get("interface"),
                f"{tid}: carrier must name its exact typed interface")
        slot = binding.get("slot")
        require(slot in obs and slot in binding.get("obligations", []),
                f"{tid}: primary slot must be one of its declared obligations")
        declared_edges = string_list(binding.get("distinct_from", []), f"{tid}.distinct_from")
        require(all(edge_id in model["carrier_distinctions"] for edge_id in declared_edges),
                f"{tid}: unknown distinct-from edge")
        require(all(model["carrier_distinctions"][edge_id]["slot"] == slot for edge_id in declared_edges),
                f"{tid}: every distinct-from edge must name the binding's primary slot")
        slot_carrier = obs[slot]["interface"]
        if binding["carrier"] != slot_carrier:
            require(_has_declared_carrier_edge(model, binding, slot, slot_carrier, binding["carrier"]),
                    f"{tid}: a different carrier needs a matching distinct-from edge before dispatch")
        for iface in binding.get("additional_interfaces", []):
            require(iface in interfaces, f"{tid}: unknown additional interface")
        require(binding.get("mode") in MODES, f"{tid}: unknown execution mode")
        text_field(binding.get("work_key"), f"{tid}.work_key", 200)
        text_field(binding.get("statement"), f"{tid}.statement")
        require(binding.get("consumer") in obs, f"{tid}: missing consumer")
        for field in ["obligations", "start_requires", "completion_requires"]:
            names = string_list(binding.get(field), f"{tid}.{field}")
            require(all(n in obs for n in names), f"{tid}: unknown {field}")
            if field in {"obligations", "completion_requires"}:
                require(bool(names), f"{tid}: no obligation")
        string_list(binding.get("assumes"), f"{tid}.assumes")
        for rid in string_list(binding.get("reuse_results", []), f"{tid}.reuse_results"):
            require(rid in model["results"], f"{tid}: unknown reusable result {rid}")
        for path in string_list(binding.get("write_paths"), f"{tid}.write_paths"):
            path_in(root, path)
    for result in model["results"].values():
        if result.get("historical"):
            continue
        text_field(result.get("statement"), f"{result['id']}.statement")
        text_field(result.get("owner"), f"{result['id']}.owner", 150)
        require(result.get("interface") in interfaces, f"{result['id']}: unknown interface")
        require(result.get("outcome") in OUTCOMES, f"{result['id']}: invalid outcome")
        require(result.get("kind") in {"lean", "exact-finite", "analytic", "passport"}, "invalid evidence kind")
        require(result.get("scope_level") in {"finite", "family"}, "result scope level is required")
        require(result["kind"] != "exact-finite" or result["scope_level"] == "finite",
                "a finite certificate cannot assert an infinite/uniform family")
        require(isinstance(result.get("hypotheses"), dict), "result hypotheses must be named")
        for key, value in result["hypotheses"].items():
            text_field(key, "hypothesis id", 100)
            text_field(value, "hypothesis")
        require(isinstance(result.get("evidence"), list) and bool(result["evidence"]), "result evidence is required")
        for ref in result["evidence"]:
            evidence_bytes(root, ref)
    _validate_source_fork_reconciliations(model)
    for app in model["applications"].values():
        aid = app["id"]
        require(app.get("obligation") in obs and app.get("result") in model["results"], f"{aid}: dangling application")
        target, result = obs[app["obligation"]], model["results"][app["result"]]
        distinct_edges = string_list(app.get("distinct_from", []), f"{aid}.distinct_from")
        require(all(edge_id in model["carrier_distinctions"] for edge_id in distinct_edges),
                f"{aid}: unknown distinct-from edge")
        require(all(model["carrier_distinctions"][edge_id]["slot"] == app["obligation"]
                    for edge_id in distinct_edges),
                f"{aid}: every distinct-from edge must name the application's target slot")
        require(not result.get("historical"), f"{aid}: historical results need a typed intake before use")
        require(target["outcome"] == "classification" or target["outcome"] == result["outcome"],
                f"{aid}: a {result['outcome']} result cannot supply a {target['outcome']} premise")
        require(target["scope_level"] != "family" or result["scope_level"] == "family",
                f"{aid}: finite scope cannot discharge a family/uniform premise")
        require(result["kind"] != "passport" or target.get("allow_passport") is True,
                f"{aid}: a passport cannot discharge this internal premise")
        require(app.get("method") in {m["id"] for m in target["methods"]}, f"{aid}: unknown proof method")
        text_field(app.get("consumer_location"), f"{aid}.consumer_location", 600)
        consumer = path_in(root, app["consumer_location"].split("#", 1)[0])
        if not consumer.is_file():
            ref = app.get("consumer_evidence", {})
            require(ref.get("path") == app["consumer_location"].split("#", 1)[0], f"{aid}: consumer location does not exist")
            evidence_bytes(root, ref)
        bindings = app.get("hypothesis_map")
        require(isinstance(bindings, dict) and set(bindings) == set(result["hypotheses"]),
                f"{aid}: hypothesis map must cover every hypothesis exactly")
        for binding in bindings.values():
            require(isinstance(binding, dict) and len(binding) == 1, f"{aid}: invalid hypothesis binding")
            if "obligation" in binding:
                dep = binding["obligation"]
                require(dep in obs, f"{aid}: unknown bound hypothesis")
                edges[app["obligation"]].add(dep)
            elif "evidence" in binding:
                evidence_bytes(root, binding["evidence"])
            elif "target_hypothesis" in binding:
                require(binding["target_hypothesis"] in target.get("hypotheses", {}),
                        f"{aid}: target hypothesis is not part of the exact scoped conclusion")
            else:
                require("assumption" in binding, f"{aid}: unknown hypothesis binding")
                text_field(binding["assumption"], "retained assumption")
        if result["interface"] != target["interface"]:
            require(_has_declared_carrier_edge(model, app, app["obligation"],
                                                target["interface"], result["interface"]),
                    f"{aid}: a different carrier needs an explicit distinct-from edge")
            transport = app.get("transport", {})
            require(set(transport.get("maps", {})) == INTERFACE_FIELDS,
                    f"{aid}: different interfaces require every transport map")
            for field, value in transport["maps"].items():
                text_field(value, f"transport.{field}")
            evidence_bytes(root, transport.get("proof"))
        accepted = accepted_review(model, app, application_digest(model, app))
        app["_accepted"] = accepted
    for attempt in model["attempts"].values():
        require(attempt.get("result") in model["results"], "attempt result is missing")
        require(attempt.get("interface") in interfaces, "attempt interface is missing")
        result = model["results"][attempt["result"]]
        require(not result.get("historical"), "historical attempts need a typed intake before enforcement")
        require(result.get("interface") == attempt["interface"], "attempt must use the negative result's exact interface")
        require(result.get("outcome") == "negative", "attempt needs a negative result")
        require(isinstance(attempt.get("question_digest"), str) and HASH.fullmatch(attempt["question_digest"]) is not None,
                "attempt needs the exact scientific question digest")
        question = attempt.get("question")
        require(isinstance(question, dict) and set(question) <= {"statement", "assumes", "additional_interfaces"},
                "attempt needs its readable exact question")
        text_field(question.get("statement"), "attempt question")
        string_list(question.get("assumes"), "attempt question assumptions")
        require(work_digest(model, {"interface": attempt["interface"], "work_key": attempt["work_key"], **question}) == attempt["question_digest"],
                "attempt question digest does not match its scope/assumptions")
        text_field(attempt.get("work_key"), "attempt work key", 200)
        text_field(attempt.get("scope"), "attempt scope")
        text_field(attempt.get("reopen_when"), "attempt reopen condition")
        attempt["_accepted"] = accepted_review(model, attempt, attempt_digest(model, attempt))
    acyclic(edges, "proof dependencies")


def evaluate(model: dict, additionally_closed=(), *, submission=False) -> dict:
    """OR across proof methods/applications, AND across their actual inputs."""
    closed, witnesses = set(additionally_closed), {}
    changed = True
    while changed:
        changed = False
        for aid, app in model["applications"].items():
            eligible = app.get("_accepted") or (submission and app["review"]["state"] == "proposed")
            if not eligible or app["obligation"] in closed:
                continue
            ob = model["obligations"][app["obligation"]]
            method = next(m for m in ob["methods"] if m["id"] == app["method"])
            required = set(method["requires"])
            assumptions = False
            for binding in app["hypothesis_map"].values():
                if "obligation" in binding:
                    required.add(binding["obligation"])
                assumptions |= "assumption" in binding
            if not assumptions and required <= closed:
                closed.add(app["obligation"])
                witnesses[app["obligation"]] = aid
                changed = True
    return {"closed": closed, "witnesses": witnesses,
            "goals": {g["id"]: set(g["requires"]) <= closed for g in model["contract"]["goals"]}}


def brief_binding(root: Path, task: dict, model: dict | None = None) -> dict | None:
    """A semantic binding is mandatory for queued A4D scientific executions."""
    if task.get("class") not in {"WORKER", "EXPENSIVE"}:
        return None
    tid = task["id"]
    mapped = tid in (model["contract"]["task_bindings"] if model else {})
    gravity = "A4D" in tid
    if not mapped and not gravity:
        return None
    require(model is not None, f"{tid}: gravity assembly contract is missing")
    require(mapped, f"{tid}: register a scientific interface/consumer in the assembly before dispatch")
    body = path_in(root, task["brief"]).read_text()
    matches = re.findall(r"^Assembly:[ \t]*`?([^`\r\n]+)`?[ \t]*\r?$", body, re.MULTILINE)
    require(matches == [tid], f"{tid}: brief must contain exactly one Assembly: `{tid}`")
    binding = model["contract"]["task_bindings"][tid]
    slots = re.findall(r"^Assembly-Slot:[ \t]*`?([^`\r\n]+)`?[ \t]*\r?$", body, re.MULTILINE)
    carriers = re.findall(r"^Assembly-Carrier:[ \t]*`?([^`\r\n]+)`?[ \t]*\r?$", body, re.MULTILINE)
    require(slots == [binding["slot"]], f"{tid}: brief must name exactly its registered Assembly-Slot")
    require(carriers == [binding["carrier"]], f"{tid}: brief must name exactly its registered Assembly-Carrier")
    distinct = re.findall(r"^Assembly-Distinct-From:[ \t]*`?([^`\r\n]+)`?[ \t]*\r?$", body, re.MULTILINE)
    expected = [",".join(binding.get("distinct_from", []))] if binding.get("distinct_from") else []
    require(distinct == expected, f"{tid}: brief distinct-from declaration differs from its typed binding")
    return binding


def validate_queue(root: Path, model: dict) -> None:
    queue = json.loads((root / "00_WORK/manifest.json").read_text())
    for task in queue.get("tasks", []):
        brief_binding(root, task, model)


def metadata(body: str, field: str) -> list[str]:
    from task_dispatch import metadata as canonical_metadata
    return canonical_metadata(body, field)


def task_for_pr(pr: dict) -> str | None:
    fields = metadata(pr.get("body") or "", "Task")
    return fields[0] if len(fields) == 1 else None


def collision_key(binding: dict) -> tuple:
    # The scientific question owns the key; a carrier/interface change alone
    # does not establish that the proposed work is independent.
    return (binding["work_key"],)


def _repo_branch(pr: dict, side: str) -> tuple[str, str] | None:
    value = pr.get(side)
    if not isinstance(value, dict):
        return None
    branch, repo = value.get("ref"), value.get("repo")
    repo_name = repo.get("full_name") if isinstance(repo, dict) else None
    if not isinstance(branch, str) or not branch or not isinstance(repo_name, str) or not repo_name:
        return None
    return repo_name, branch


def stacked_pr_chain(prs: list[dict]) -> list[dict] | None:
    """Return an explicitly ordered same-repository PR stack, if unambiguous.

    A shared Task field alone means duplicate ownership. A child PR whose base
    branch is exactly another live PR's head branch is a different process
    shape: it may be a stacked source, but its current changes still need to
    be reconciled into the parent. We report that relation without accepting
    the child or authorizing another execution.
    """
    if len(prs) < 2:
        return None
    by_head: dict[tuple[str, str], list[dict]] = {}
    for pr in prs:
        identity = _repo_branch(pr, "head")
        if identity is None:
            return None
        by_head.setdefault(identity, []).append(pr)
    if any(len(items) != 1 for items in by_head.values()):
        return None

    parent_for: dict[int, dict] = {}
    for child in prs:
        base = _repo_branch(child, "base")
        candidates = by_head.get(base, []) if base is not None else []
        if len(candidates) == 1 and candidates[0].get("number") != child.get("number"):
            parent_for[child["number"]] = candidates[0]
    if len(parent_for) != len(prs) - 1:
        return None

    # Accept only a single linear chain. Sibling stacks or missing links need
    # ordinary CONTROL reconciliation, not an inferred ordering.
    child_count: dict[int, int] = {}
    for parent in parent_for.values():
        child_count[parent["number"]] = child_count.get(parent["number"], 0) + 1
    if any(count > 1 for count in child_count.values()):
        return None
    # A root is the one PR which is not itself based on another live PR.
    roots = [pr for pr in prs if pr["number"] not in parent_for]
    if len(roots) != 1:
        return None
    root_number = roots[0]["number"]
    for pr in prs:
        seen = set()
        number = pr["number"]
        while number in parent_for:
            if number in seen:
                return None
            seen.add(number)
            number = parent_for[number]["number"]
        if number != root_number:
            return None

    relations = []
    for child_number, parent in parent_for.items():
        child = next(pr for pr in prs if pr["number"] == child_number)
        parent_head = parent.get("head") or {}
        child_base = child.get("base") or {}
        child_head = child.get("head") or {}
        relations.append({
            "parent": parent["number"],
            "child": child_number,
            "parent_branch": parent_head.get("ref"),
            "child_branch": child_head.get("ref"),
            "parent_head_sha": parent_head.get("sha"),
            "child_base_sha": child_base.get("sha"),
            "child_head_sha": child_head.get("sha"),
            "base_matches_parent_head": child_base.get("sha") == parent_head.get("sha"),
        })
    return sorted(relations, key=lambda item: (item["parent"], item["child"]))


def stacked_descendants(root: dict, prs: list[dict]) -> list[dict]:
    """Find open same-repository PRs based transitively on a registered owner.

    A child can be a useful source without repeating the parent's Task metadata.
    Keep that relation visible to route selection instead of silently ignoring
    it or misclassifying the child as an independently registered owner.
    """
    selected = {root["number"]: root}
    changed = True
    while changed:
        changed = False
        parent_heads = {_repo_branch(pr, "head") for pr in selected.values()}
        parent_heads.discard(None)
        for pr in prs:
            if pr.get("number") in selected:
                continue
            if _repo_branch(pr, "base") in parent_heads:
                selected[pr["number"]] = pr
                changed = True
    return [pr for number, pr in selected.items() if number != root["number"]]


def work_digest(model: dict, binding: dict) -> str:
    interfaces = model["contract"]["interfaces"]
    return digest({"work_key": binding["work_key"], "statement": binding["statement"],
                   "assumes": binding["assumes"], "interface": interfaces[binding["interface"]],
                   "additional_interfaces": {n: interfaces[n] for n in binding.get("additional_interfaces", [])}})


def launch_check(model: dict, task_id: str, prs: list[dict]) -> dict:
    bindings = model["contract"]["task_bindings"]
    binding = bindings.get(task_id)
    if binding is None:
        require("A4D" not in task_id, f"{task_id}: missing assembly binding")
        return {"allowed": True, "reasons": [], "binding": None}
    state, reasons = evaluate(model), []
    slot = binding["slot"]
    slot_carrier = model["obligations"][slot]["interface"]
    if binding["carrier"] != slot_carrier and not _has_declared_carrier_edge(
            model, binding, slot, slot_carrier, binding["carrier"]):
        reasons.append(f"slot {slot} uses {slot_carrier}; declare a matching distinct-from edge for {binding['carrier']}")
    filled_carriers = {
        model["results"][app["result"]]["interface"]
        for app in model["applications"].values()
        if app["obligation"] == slot and app.get("_accepted")
    }
    if binding["carrier"] in filled_carriers:
        reasons.append(f"slot {slot} is already filled with the same carrier {binding['carrier']}; do not start duplicate work")
    for filled_carrier in sorted(filled_carriers - {binding["carrier"]}):
        if not _has_declared_carrier_edge(model, binding, slot, filled_carrier, binding["carrier"]):
            reasons.append(f"slot {slot} is filled by {filled_carrier}; a matching distinct-from edge is required")
    for pr in prs:
        fields = metadata(pr.get("body") or "", "Task")
        if len(fields) > 1 and any(t in bindings and collision_key(bindings[t]) == collision_key(binding) for t in fields):
            reasons.append(f"ambiguous scientific ownership in #{pr['number']}; resolve its Task metadata")
        other_id = task_for_pr(pr)
        other = bindings.get(other_id)
        if other and other_id != task_id and collision_key(other) == collision_key(binding):
            if binding["mode"] != "verification" and other["mode"] != "verification":
                reasons.append(f"same scientific work already executes in #{pr['number']} ({other_id})")
    missing = set(binding["start_requires"]) - state["closed"]
    if missing:
        reasons.append("unproved start prerequisites: " + ", ".join(sorted(missing)))
    if (set(binding["obligations"]) <= state["closed"] and binding["mode"] != "verification"
            and not (filled_carriers and binding["carrier"] not in filled_carriers
                     and all(_has_declared_carrier_edge(model, binding, slot, filled, binding["carrier"])
                             for filled in filled_carriers))):
        reasons.append("the exact bound obligations are already discharged; name a genuine new premise")
    for attempt in model["attempts"].values():
        if attempt.get("_accepted") and collision_key(attempt) == collision_key(binding):
            if attempt["question_digest"] == work_digest(model, binding):
                reasons.append(f"scoped no-go {attempt['id']}: {attempt['scope']}; reopen only when {attempt['reopen_when']}")
            else:
                reopen = binding.get("reopens", {})
                if reopen.get("attempt") != attempt["id"] or not isinstance(reopen.get("delta"), str) or not reopen["delta"].strip():
                    reasons.append(f"changed question overlaps {attempt['id']}; record reopens.attempt and the actual hypothesis/scope delta")
    queue = json.loads((model["root"] / "00_WORK/manifest.json").read_text())
    tasks = {t["id"]: t for t in queue.get("tasks", [])}
    cls = tasks.get(task_id, {}).get("class")
    if cls:
        active = {t["id"] for t in tasks.values() if t["class"] == cls and t["state"] in {"IN_PROGRESS", "BLOCKED", "REVIEW"}}
        for pr in prs:
            pid = task_for_pr(pr)
            declared = metadata(pr.get("body") or "", "Class")
            if pid and pid != "CONTROL-PLANE" and (declared == [cls] or tasks.get(pid, {}).get("class") == cls):
                active.add(pid)
        if task_id not in active and len(active) >= queue.get("limits", {}).get(cls, 0):
            reasons.append(f"{cls} WIP is {len(active)}/{queue.get('limits', {}).get(cls, 0)}, including live executions")
    return {"allowed": not reasons, "reasons": reasons, "binding": binding}


def retirement_check(model: dict, task_id: str) -> None:
    binding = model["contract"]["task_bindings"].get(task_id)
    require(binding is not None or "A4D" not in task_id, f"{task_id}: missing assembly binding at retirement")
    if binding:
        missing = set(binding["completion_requires"]) - evaluate(model, submission=True)["closed"]
        require(not missing, "Ready submission requires complete reviewable terminal premises: " + ", ".join(sorted(missing)))


def context(model: dict, task_id: str) -> str:
    binding = model["contract"]["task_bindings"].get(task_id)
    if not binding:
        return ""
    c, state = model["contract"], evaluate(model)
    iface = c["interfaces"][binding["interface"]]
    lines = [f"Assembly: {task_id}", f"Primary slot: {binding['slot']}",
             f"Carrier: {binding['carrier']}", f"Work: {binding['statement']}",
             f"Interface: {binding['interface']} ({digest(iface)[:12]})",
             f"Consumer: {binding['consumer']}", "Obligations: " + ", ".join(binding["obligations"])]
    for assumption in binding["assumes"]:
        lines.append("Retained assumption: " + assumption)
    for key in ["carrier", "action", "variations", "source", "normalization", "refinement", "scope"]:
        lines.append(f"{key.capitalize()}: {iface[key]}")
    for extra in binding.get("additional_interfaces", []):
        lines.append(f"Separate interface retained: {extra}; {c['interfaces'][extra]['normalization']}")
    for rid in binding.get("reuse_results", []):
        result = model["results"][rid]
        lines.append(f"Reuse {rid}: {result['statement']}")
    lines.append("Read: " + c["route"] + "; " + DIRECTORY + "/README.md")
    lines.append("Check intake: python3 tools/gr_assembly.py template " + task_id)
    return "\n".join(lines)


def readiness(model: dict, closed: set) -> set:
    return {n for n, ob in model["obligations"].items() if n not in closed
            and any(set(m["requires"]) <= closed for m in ob["methods"])}


def downstream(model: dict, name: str) -> set:
    found = set()
    while True:
        new = {n for n, ob in model["obligations"].items() if n not in found and n != name
               and any(name in m["requires"] or set(m["requires"]) & found for m in ob["methods"])}
        if not new:
            return found
        found.update(new)


def next_actions(model: dict, prs: list[dict] | None) -> list[dict]:
    state = evaluate(model)
    before = readiness(model, state["closed"])
    queue = json.loads((model["root"] / "00_WORK/manifest.json").read_text())
    queued = {t["id"]: t for t in queue["tasks"]}
    actions = []
    for tid, binding in model["contract"]["task_bindings"].items():
        reconciled_source_forks = []
        live = [p for p in (prs or []) if task_for_pr(p) == tid]
        live_executions = []
        for pr in sorted(live, key=lambda item: item["number"]):
            lifecycle = metadata(pr.get("body") or "", "Lifecycle")
            live_executions.append({
                "number": pr["number"],
                "title": pr.get("title", ""),
                "url": pr.get("html_url", ""),
                "state": "draft" if pr["draft"] else "ready",
                "lifecycle": lifecycle[0] if len(lifecycle) == 1 else "lifecycle-unresolved",
                "head_branch": (pr.get("head") or {}).get("ref"),
                "head_sha": (pr.get("head") or {}).get("sha"),
                "base_branch": (pr.get("base") or {}).get("ref"),
                "base_sha": (pr.get("base") or {}).get("sha"),
            })
        if len(live) > 1:
            stacked = stacked_pr_chain(live)
            if stacked is not None:
                details = []
                for relation in stacked:
                    sha_state = ("child base SHA matches the current parent head" if relation["base_matches_parent_head"]
                                 else "child base SHA differs from the current parent head")
                    details.append(
                        f"#{relation['child']} is based on #{relation['parent']}'s branch "
                        f"({sha_state}; child base {relation['child_base_sha']}, "
                        f"parent head {relation['parent_head_sha']}, child head {relation['child_head_sha']})"
                    )
                affected = set().union(*(downstream(model, n) for n in binding["obligations"]))
                actions.append({
                    "task": tid,
                    "action": "reconcile-stacked-source",
                    "reasons": [
                        "same-task PRs form one explicit same-repository branch stack: "
                        + "; ".join(details)
                        + ". Compare the child-only delta with the parent and pin the consumed child head before resolving; no new execution is authorized"
                    ],
                    "consumer": binding["consumer"],
                    "assumes": binding["assumes"],
                    "reuse_results": binding.get("reuse_results", []),
                    "live_executions": live_executions,
                    "stacked_relations": stacked,
                    "potential_downstream": len(affected),
                    "newly_ready_if_proved": 0,
                })
                continue
            owners = []
            for pr in sorted(live, key=lambda item: item["number"]):
                lifecycle = metadata(pr.get("body") or "", "Lifecycle")
                phase = lifecycle[0] if len(lifecycle) == 1 else "lifecycle-unresolved"
                state_name = "draft" if pr.get("draft") else "ready"
                owners.append(f"#{pr['number']} ({state_name}, {phase})")
            affected = set().union(*(downstream(model, n) for n in binding["obligations"]))
            actions.append({
                "task": tid,
                "action": "resolve-overlap",
                "reasons": [
                    "multiple live PRs claim this task: " + ", ".join(owners)
                    + "; reconcile to one owner before dispatching"
                ],
                "consumer": binding["consumer"],
                "assumes": binding["assumes"],
                "reuse_results": binding.get("reuse_results", []),
                "live_executions": live_executions,
                "potential_downstream": len(affected),
                "newly_ready_if_proved": 0,
            })
            continue
        if not live and tid not in queued:
            continue  # Retired semantic bindings remain provenance, not new work.
        if live:
            p = live[0]
            related = stacked_descendants(p, prs or [])
            if related:
                stack = stacked_pr_chain([p, *related])
                related_prs = []
                for child in sorted(related, key=lambda item: item["number"]):
                    lifecycle = metadata(child.get("body") or "", "Lifecycle")
                    related_prs.append({
                        "number": child["number"],
                        "title": child.get("title", ""),
                        "url": child.get("html_url", ""),
                        "state": "draft" if child.get("draft") else "ready",
                        "lifecycle": lifecycle[0] if len(lifecycle) == 1 else "lifecycle-unresolved",
                        "task": task_for_pr(child),
                        "head_branch": (child.get("head") or {}).get("ref"),
                        "head_sha": (child.get("head") or {}).get("sha"),
                        "base_branch": (child.get("base") or {}).get("ref"),
                        "base_sha": (child.get("base") or {}).get("sha"),
                    })
                affected = set().union(*(downstream(model, n) for n in binding["obligations"]))
                if stack is None and len(related) > 1:
                    reconciliation = matching_source_fork_reconciliation(model, p, related)
                    if reconciliation is None:
                        reason = (
                            "multiple open same-repository PRs descend from the registered owner through separate "
                            "source branches. Compare their exact scientific questions and child-only deltas; do not "
                            "treat branch dependence alone as duplicate ownership or accept a child result"
                        )
                        path_error = p.get("_assembly_source_path_blobs_error")
                        if path_error:
                            reason += "; exact current parent path lookup unavailable, so the prior comparison cannot be reused"
                        elif p.get("_assembly_source_path_blobs_complete") is True:
                            for record in model["contract"].get("source_fork_reconciliations", []):
                                if record["parent"]["number"] != p["number"]:
                                    continue
                                expected = {
                                    item["path"]: item["parent_git_blob"]
                                    for child in record["children"]
                                    for item in child["child_only_delta"]
                                }
                                current = p.get("_assembly_source_path_blobs") or {}
                                changed_paths = sorted(path for path in expected if current.get(path) != expected[path])
                                if changed_paths:
                                    reason += "; parent version changed for child-delta paths: " + ", ".join(changed_paths[:8])
                                break
                        actions.append({
                            "task": tid,
                            "action": "reconcile-source-fork",
                            "reasons": [reason],
                            "consumer": binding["consumer"],
                            "assumes": binding["assumes"],
                            "reuse_results": binding.get("reuse_results", []),
                            "live_executions": live_executions,
                            "related_prs": related_prs,
                            "potential_downstream": len(affected),
                            "newly_ready_if_proved": 0,
                        })
                        continue
                    reconciled_source_forks.append(
                        source_fork_reconciliation_summary(reconciliation, p, related_prs))
                elif stack is None:
                    actions.append({
                        "task": tid,
                        "action": "resolve-overlap",
                        "reasons": [
                            "open PR descendants of the registered owner do not form one unambiguous linear source chain; "
                            "reconcile the related branches before using any child result"
                        ],
                        "consumer": binding["consumer"],
                        "assumes": binding["assumes"],
                        "reuse_results": binding.get("reuse_results", []),
                        "live_executions": live_executions,
                        "related_prs": related_prs,
                        "potential_downstream": len(affected),
                        "newly_ready_if_proved": 0,
                    })
                    continue
                if stack is not None:
                    details = []
                    for relation in stack:
                        sha_state = ("child base SHA matches the current parent head" if relation["base_matches_parent_head"]
                                     else "child base SHA differs from the current parent head")
                        details.append(
                            f"#{relation['child']} is based on #{relation['parent']}'s branch "
                            f"({sha_state}; child base {relation['child_base_sha']}, "
                            f"parent head {relation['parent_head_sha']}, child head {relation['child_head_sha']})"
                        )
                    actions.append({
                        "task": tid,
                        "action": "reconcile-stacked-source",
                        "reasons": [
                            "open PR descendants are surfaced by their exact same-repository branch relation even when "
                            "they omit or differ in Task metadata: " + "; ".join(details)
                            + ". Compare each child-only delta with its parent and pin the consumed child head; "
                            "the relation does not accept the result or authorize another execution"
                        ],
                        "consumer": binding["consumer"],
                        "assumes": binding["assumes"],
                        "reuse_results": binding.get("reuse_results", []),
                        "live_executions": live_executions,
                        "related_prs": related_prs,
                        "stacked_relations": stack,
                        "potential_downstream": len(affected),
                        "newly_ready_if_proved": 0,
                    })
                    continue
            lifecycle = metadata(p.get("body") or "", "Lifecycle")
            action = "resume" if p["draft"] and lifecycle == ["IN_PROGRESS"] else "resolve-blocker" if p["draft"] and lifecycle == ["BLOCKED"] else "review" if not p["draft"] and lifecycle == ["REVIEW"] else "reconcile-lifecycle"
            reasons = [f"existing #{p['number']}"]
            if reconciled_source_forks:
                reasons.append("exact source-fork comparison still matches its pinned PR heads and child set; "
                               "child evidence remains result-only and unaccepted by the parent")
            for other in prs:
                other_id = task_for_pr(other)
                other_binding = model["contract"]["task_bindings"].get(other_id)
                if (other_id != tid and other_binding and binding["mode"] != "verification"
                        and other_binding["mode"] != "verification" and collision_key(binding) == collision_key(other_binding)):
                    action = "resolve-overlap"
                    reasons.append(f"same scientific work also owned by #{other['number']}")
        elif prs is None:
            action, reasons = "unverified-planning", ["GitHub status is unknown; no launch authorized"]
        else:
            checked = launch_check(model, tid, prs)
            task = queued.get(tid)
            if task is None or task["state"] != "PLANNED":
                action, reasons = "reconcile-queue", ["no live execution; queue is absent or not PLANNED"]
            else:
                action = "eligible-for-control" if checked["allowed"] else "blocked"
                reasons = checked["reasons"]
        affected = set().union(*(downstream(model, n) for n in binding["obligations"]))
        after = evaluate(model, set(state["closed"]) | set(binding["obligations"]))["closed"]
        newly_ready = readiness(model, after) - before - set(binding["obligations"])
        row = {"task": tid, "action": action, "slot": binding["slot"], "carrier": binding["carrier"],
               "reasons": reasons,
               "consumer": binding["consumer"], "assumes": binding["assumes"],
               "reuse_results": binding.get("reuse_results", []),
               "live_executions": live_executions,
               "potential_downstream": len(affected), "newly_ready_if_proved": len(newly_ready)}
        if reconciled_source_forks:
            row["reconciled_source_forks"] = reconciled_source_forks
        actions.append(row)
    priority = {"resolve-overlap": 0, "reconcile-stacked-source": 0, "reconcile-source-fork": 0,
                "review": 1, "resolve-blocker": 2,
                "resume": 3, "eligible-for-control": 4}
    return sorted(actions, key=lambda a: (priority.get(a["action"], 4), -a["newly_ready_if_proved"], a["task"]))


def ready_obligations(model: dict, actions: list[dict]) -> list[dict]:
    """Show open obligations whose declared logical inputs are already accepted.

    This is a read-only planning view. An unowned obligation requires ordinary
    CONTROL registration; readiness never authorizes task creation or launch.
    """
    state = evaluate(model)
    closed = set(state["closed"])
    ready = readiness(model, closed)
    action_by_task = {action["task"]: action for action in actions}
    proposed_by_obligation: dict[str, list[str]] = {}
    for app in model["applications"].values():
        if app["review"]["state"] == "proposed":
            proposed_by_obligation.setdefault(app["obligation"], []).append(app["id"])

    rows = []
    for name in ready:
        after = readiness(model, closed | {name})
        newly_ready = sorted(after - ready - {name})
        bindings = []
        for task_id, binding in model["contract"]["task_bindings"].items():
            if name not in binding["obligations"] or task_id not in action_by_task:
                continue
            action = action_by_task[task_id]
            row = {"task": task_id, "action": action["action"],
                   "slot": binding["slot"], "carrier": binding["carrier"],
                   "live_executions": action["live_executions"]}
            if action.get("reconciled_source_forks"):
                row["reconciled_source_forks"] = action["reconciled_source_forks"]
            bindings.append(row)

        proposed = sorted(proposed_by_obligation.get(name, []))
        task_actions = {item["action"] for item in bindings}
        next_step = "register-or-reopen-through-control"
        if proposed:
            next_step = "independent-scoped-review"
        elif any(item.get("reconciled_source_forks") for item in bindings):
            next_step = "resume-parent-after-source-fork-comparison"
        elif "reconcile-stacked-source" in task_actions:
            next_step = "reconcile-stacked-source-through-control"
        elif "reconcile-source-fork" in task_actions:
            next_step = "reconcile-source-fork-through-control"
        elif "resolve-overlap" in task_actions:
            next_step = "resolve-overlap-through-control"
        elif "review" in task_actions:
            next_step = "review-registered-pr"
        elif "resume" in task_actions:
            next_step = "resume-registered-pr"
        elif "resolve-blocker" in task_actions:
            next_step = "clear-blocker-in-current-pr"
        elif "blocked" in task_actions:
            next_step = "resolve-registered-prerequisite"
        elif "eligible-for-control" in task_actions:
            next_step = "control-launch-review"
        elif "unverified-planning" in task_actions:
            next_step = "verify-live-state-first"
        elif task_actions:
            next_step = "reconcile-registered-execution"
        rows.append({"obligation": name, "statement": model["obligations"][name]["statement"],
                     "potential_downstream": len(downstream(model, name)),
                     "newly_ready_if_proved": len(newly_ready), "newly_ready": newly_ready,
                     "registered_tasks": bindings, "proposed_applications": proposed,
                     "next_step": next_step})
    return sorted(rows, key=lambda row: (-row["newly_ready_if_proved"],
                                         -row["potential_downstream"], row["obligation"]))


def result_registry_budget(model: dict) -> dict:
    """Expose the bounded active-result registry capacity in planning output."""
    active = len(model["intake"]["results"])
    limit = model["contract"]["registry_budget"]["max_active_results"]
    remaining = max(0, limit - active)
    return {
        "active_results": active,
        "max_active_results": limit,
        "remaining": remaining,
        "state": "at-capacity" if remaining == 0 else "available",
        "guidance": (
            "Reuse or strengthen an existing result node; consolidate only through CONTROL with provenance, and change the limit only explicitly."
            if remaining == 0 else
            "Reuse an existing result node when it covers the same scoped result."
        ),
    }


def diagram(model: dict) -> str:
    names = {n: "o" + str(i) for i, n in enumerate(model["obligations"])}
    lines = ["flowchart TD"]
    for name, oid in names.items():
        lines.append(f'    {oid}["{name}"]')
    for name, ob in model["obligations"].items():
        for i, method in enumerate(ob["methods"]):
            target = names[name]
            if len(ob["methods"]) > 1:
                mid = f"{target}m{i}"
                lines.append(f'    {mid}{{"AND {method["id"]}"}} --> {target}')
                target = mid
            for dep in method["requires"]:
                lines.append(f"    {names[dep]} --> {target}")
    for i, goal in enumerate(model["contract"]["goals"]):
        lines.append(f'    g{i}[["{goal["id"]}"]]')
        for name in goal["requires"]:
            lines.append(f"    {names[name]} --> g{i}")
    return "\n".join(lines)


def overview(model: dict) -> str:
    state = evaluate(model)
    c = model["contract"]
    lines = ["# D0 to GR assembly overview", "", "Generated by `python3 tools/gr_assembly.py render`. Do not hand-edit.", "",
             "Scientific acceptance and live execution are separate. Historical research does not discharge a premise.", "",
             "| Goal | Composition |", "|---|---|"]
    for goal in c["goals"]:
        lines.append(f"| {goal['id']} | {'DISCHARGED' if state['goals'][goal['id']] else 'OPEN'} |")
    if c.get("synthesis"):
        lines += ["", "For the short working composition and next scientific questions, use [SYNTHESIS.md](SYNTHESIS.md) or `python3 tools/gr_assembly.py puzzle`."]
    lines += ["", "| Obligation | Group | Missing logical inputs | Accepted application |", "|---|---|---|---|"]
    for name, ob in model["obligations"].items():
        missing = [", ".join(d for d in m["requires"] if d not in state["closed"]) or "none; conclusion still needs accepted evidence" for m in ob["methods"]]
        lines.append(f"| {name} | {ob['group']} | {' OR '.join(missing)} | {state['witnesses'].get(name, 'none')} |")
    negatives = sum(r["outcome"] == "negative" for r in model["results"].values())
    lines += ["", "## Declared dependency DAG", "", "Incoming inputs of a method are AND; different methods are alternatives.",
              "The diagram is a proof plan, not evidence that any transition is closed.", "", "```mermaid", diagram(model), "```",
              "", f"Historical catalogue: {c['legacy_import']['node_count']} preserved IDs; {negatives} indexed scoped negative results including typed input.",
              "Use `search` for their exact scope and owners. No historical result is accepted automatically.", "",
              "## Agent entry", "", "```bash", "python3 tools/gr_assembly.py next", "python3 tools/task_dispatch.py TASK-ID",
              "python3 tools/gr_assembly.py why OBLIGATION", "python3 tools/gr_assembly.py search QUERY", "```", "",
              "`next` uses live PRs once. `--offline` means unverified planning and never authorizes launch.",
              "Independent conditional lemmas retain their assumptions. A free slot alone does not prove prerequisites.", "",
              "## Provenance", "", f"Current-route input: `{c['route_input']['ref']}`.",
              f"Historical graph input: `{c['legacy_import']['ref']}`.",
              "The preserved source pin is not a current execution head or an acceptance decision.", ""]
    return "\n".join(lines)


def result_evidence_paths(result: dict) -> set[str]:
    paths = set()
    for evidence in result.get("evidence", []):
        if not isinstance(evidence, dict):
            continue
        for key in ("path", "snapshot"):
            value = evidence.get(key)
            if isinstance(value, str) and value:
                paths.add(value)
    return paths


def query_matches(haystack: str, words: list[str]) -> bool:
    for word in words:
        if len(word) <= 2 and word.isalnum():
            if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", haystack) is None:
                return False
        elif word not in haystack:
            return False
    return True


def attempts(model: dict, query: str) -> list[dict]:
    words = query.casefold().split()
    found, typed = [], set()
    for attempt in model["attempts"].values():
        result = model["results"][attempt["result"]]
        question = attempt.get("question", {})
        fields = [attempt["id"], attempt["scope"], attempt["work_key"], attempt["interface"],
                  attempt["reopen_when"], question.get("statement", ""), *question.get("assumes", []),
                  result["id"], result["statement"], *result.get("owners", []),
                  *result.get("hypotheses", {}).values(), *result_evidence_paths(result)]
        hay = " ".join(fields).casefold()
        if query_matches(hay, words):
            found.append({k: attempt[k] for k in ["id", "scope", "work_key", "interface", "question", "question_digest", "reopen_when"]} |
                         {"evidence_paths": sorted(result_evidence_paths(result)),
                          "enforced": attempt.get("_accepted", False), "review": attempt["review"]["state"]})
        typed.add(attempt["result"])
    for result in model["results"].values():
        fields = [result["id"], result["statement"], *result.get("owners", []),
                  *result.get("hypotheses", {}).values(), *result_evidence_paths(result)]
        hay = " ".join(fields).casefold()
        if result["outcome"] == "negative" and result["id"] not in typed and query_matches(hay, words):
            found.append({"id": result["id"], "scope": result["statement"], "reported_state": result.get("reported_state"),
                          "evidence_paths": sorted(result_evidence_paths(result)),
                          "enforced": False, "acceptance": "historical; typed independent intake required",
                          "owners": result.get("owners", [])[:3]})
    return found


def why(model: dict, name: str) -> dict:
    require(name in model["obligations"], f"unknown obligation {name}")
    ob, state = model["obligations"][name], evaluate(model)
    return {"id": name, "statement": ob["statement"], "interface": ob["interface"],
            "discharged": name in state["closed"], "application": state["witnesses"].get(name),
            "methods": [{"id": m["id"], "missing": sorted(set(m["requires"]) - state["closed"])} for m in ob["methods"]],
            "applications": [{"id": a["id"], "review": a["review"]["state"],
                              "retained_assumptions": [v["assumption"] for v in a["hypothesis_map"].values() if "assumption" in v]}
                             for a in model["applications"].values() if a["obligation"] == name],
            "historical_candidate": "legacy:" + name if "legacy:" + name in model["results"] else None,
            "consumers": sorted(downstream(model, name)),
            "rule": "A candidate or a ready input does not prove this conclusion. Supply a typed, independently accepted application."}


def search(model: dict, query: str) -> list[dict]:
    words = query.casefold().split()
    require(bool(words), "search query cannot be empty")
    found = []
    for name, aliases in gr_synthesis.result_groups(model["results"]).items():
        result = model["results"][name]
        evidence_paths = set().union(*(result_evidence_paths(model["results"][alias]) for alias in aliases))
        fields = []
        for alias in aliases:
            indexed = model["results"][alias]
            fields += [alias, indexed["statement"], indexed.get("owner", ""),
                       *indexed.get("owners", []), *indexed.get("hypotheses", {}).values()]
        fields += sorted(evidence_paths)
        hay = " ".join(fields).casefold()
        if query_matches(hay, words):
            item = {k: result.get(k) for k in ["id", "statement", "outcome", "reported_state"]}
            item["owner"] = result.get("owner")
            item["owners"] = result.get("owners", [])[:5]
            item["evidence_paths"] = sorted(evidence_paths)
            if len(aliases) > 1:
                item["also_indexed_as"] = [alias for alias in aliases if alias != name]
                item["indexed_interfaces"] = sorted({model["results"][alias]["interface"] for alias in aliases})
            found.append(item)
    return found[:20]


def impact(model: dict, base: str, ref: str) -> dict:
    import research_input_closure
    selection = research_input_closure.select(model["root"], ref, base)
    changed = set(selection["changed"])
    affected = []
    for app in model["applications"].values():
        result = model["results"][app["result"]]
        paths = result_evidence_paths(result)
        kinds: dict[str, set[str]] = {}

        def watch(path: object, kind: str) -> None:
            if isinstance(path, str) and path:
                kinds.setdefault(path, set()).add(kind)

        for path in paths:
            watch(path, "pinned result evidence")
        decision = app.get("review", {}).get("decision", {})
        if isinstance(decision, dict) and isinstance(decision.get("path"), str):
            watch(decision["path"], "pinned acceptance decision")
        consumer = app["consumer_location"].split("#", 1)[0]
        watch(consumer, "named parent consumer")
        route_input = model["contract"].get("route_input", {})
        for path in (route_input.get("path"), route_input.get("snapshot")):
            watch(path, "pinned route input")
        watch(DIRECTORY + "/contract.json", "assembly contract")
        hits = sorted(path for path in kinds if path in changed)
        if hits:
            affected.append({"application": app["id"], "obligation": app["obligation"],
                             "changed_paths": hits,
                             "change_kinds": {path: sorted(kinds[path]) for path in hits},
                             "reason": "review compatibility with the proposed new inputs; the pinned old theorem is unchanged"})
    return {"changed": selection["changed"], "applications_to_review": affected,
            "certificate_selection": [{"path": c["certificate"], "reasons": c["reasons"]} for c in selection["selected"]],
            "provenance_ok": selection["provenance_ok"], "ran": False, "scientific_replay": False,
            "rule": "Selection is not replay. Unknown dependencies stay selected. Existing evidence is never rewritten."}


def template(model: dict, tid: str) -> dict:
    binding = model["contract"]["task_bindings"].get(tid)
    require(binding is not None, f"unknown scientific binding {tid}")
    return {"scientific_question_digest": work_digest(model, binding),
            "scientific_question": {k: binding[k] for k in ["statement", "assumes", "additional_interfaces"] if k in binding},
            "result": {"id": "RESULT-ID", "owner": "RESULT-OWNER", "statement": binding["statement"],
                       "interface": binding["interface"], "outcome": "positive", "kind": "analytic", "scope_level": "family",
                       "hypotheses": {"h1": "REMAINING EXACT HYPOTHESIS"},
                       "evidence": [{"ref": "FULL-PUBLISHED-COMMIT", "path": binding["write_paths"][0], "sha256": "SHA256"}]},
            "application": {"id": "APPLICATION-ID", "result": "RESULT-ID", "obligation": binding["slot"],
                            "method": "direct", "consumer_location": model["contract"]["route"] + "#PARENT-STEP",
                            "hypothesis_map": {"h1": {"assumption": "REMAINING EXACT HYPOTHESIS"}},
                            "review": {"state": "proposed"}},
            "instructions": "Replace placeholders with the exact result and parent substitution. Run check and application-digest. "
                            "An independent review pins Assembly-Acceptance: ID DIGEST in the existing parent/intake artifact. "
                            "Then record its full decision ref, SHA-256, reviewer and digest. Retained assumptions never discharge a goal."}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=ROOT)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("show")
    sub.add_parser("dag")
    p = sub.add_parser("puzzle", help="fast local composition reading; no replay or live lookup")
    p.add_argument("query", nargs="*", default=[])
    p = sub.add_parser("render"); p.add_argument("--check", action="store_true")
    p = sub.add_parser("next"); p.add_argument("--offline", action="store_true")
    p = sub.add_parser("why"); p.add_argument("obligation")
    p = sub.add_parser("search"); p.add_argument("query", nargs="+")
    p = sub.add_parser("attempts"); p.add_argument("query", nargs="*", default=[])
    p = sub.add_parser("template"); p.add_argument("task")
    p = sub.add_parser("application-digest"); p.add_argument("application")
    p = sub.add_parser("impact"); p.add_argument("--base", required=True); p.add_argument("--ref", default="HEAD")
    args = ap.parse_args(argv)
    try:
        if args.command == "puzzle":
            data = gr_synthesis.read(args.repo_root, " ".join(args.query))
            print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else gr_synthesis.render(data), end="\n")
            return 0
        model = load(args.repo_root)
        if args.command == "check":
            validate_queue(args.repo_root, model)
            data = {"valid": True, "obligations": len(model["obligations"]), "results": len(model["results"]),
                    "active_results": len(model["intake"]["results"]),
                    "active_result_limit": model["contract"]["registry_budget"]["max_active_results"],
                    "discharged": len(evaluate(model)["closed"]), "scientific_promotion": False}
        elif args.command == "render":
            text = overview(model)
            target = args.repo_root / DIRECTORY / "VIEW.md"
            if args.check:
                require(target.is_file() and target.read_text() == text, "assembly view is stale; run render")
            else:
                target.write_text(text)
            if model["contract"].get("synthesis"):
                synthesis = args.repo_root / DIRECTORY / "SYNTHESIS.md"
                reading = gr_synthesis.render(gr_synthesis.read(args.repo_root))
                if args.check:
                    require(synthesis.is_file() and synthesis.read_text() == reading,
                            "synthesis view is stale; run render")
                else:
                    synthesis.write_text(reading)
            data = {"view": str(target), "checked": args.check}
        elif args.command == "show":
            if not args.json:
                print(overview(model), end=""); return 0
            data = {"goals": evaluate(model)["goals"], "open": sorted(set(model["obligations"]) - evaluate(model)["closed"])}
        elif args.command == "dag":
            print(diagram(model)); return 0
        elif args.command == "next":
            from task_dispatch import commit_path_blobs, open_prs
            prs = None if args.offline else open_prs(args.repo_root)
            if prs is not None:
                prepare_source_fork_path_snapshots(model, prs, args.repo_root, commit_path_blobs)
            actions = next_actions(model, prs)
            data = {"live_verified": prs is not None, "actions": actions,
                    "registry_budget": result_registry_budget(model),
                    "ready_obligations": ready_obligations(model, actions),
                    "readiness_scope": "Declared dependency inputs only; not proof, physical admission, proof success or launch authorization.",
                    "intakes": [{"application": a["id"], "obligation": a["obligation"],
                                 "consumer": a["consumer_location"], "action": "independent-scoped-review"}
                                for a in model["applications"].values() if a["review"]["state"] == "proposed"] +
                               [{"attempt": a["id"], "action": "independent-scoped-review", "scope": a["scope"]}
                                for a in model["attempts"].values() if a["review"]["state"] == "proposed"],
                    "authority": "Recommendations do not reserve execution or bypass CONTROL, prerequisites or WIP."}
        elif args.command == "why":
            data = why(model, args.obligation)
        elif args.command == "search":
            data = search(model, " ".join(args.query))
        elif args.command == "attempts":
            data = attempts(model, " ".join(args.query))
        elif args.command == "template":
            data = template(model, args.task)
        elif args.command == "application-digest":
            record = model["applications"].get(args.application) or model["attempts"].get(args.application)
            require(record is not None, "unknown application or scoped attempt")
            app = {k: v for k, v in record.items() if not k.startswith("_")}
            value = application_digest(model, app) if args.application in model["applications"] else attempt_digest(model, app)
            data = {"id": app["id"], "digest": value,
                    "acceptance_marker": f"Assembly-Acceptance: {app['id']} {value}"}
        else:
            data = impact(model, args.base, args.ref)
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"ASSEMBLY_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
