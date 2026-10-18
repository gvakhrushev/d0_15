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


def validate(model: dict) -> None:
    c, root = model["contract"], model["root"]
    interfaces, obs = c.get("interfaces"), model["obligations"]
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
    for tid, binding in c.get("task_bindings", {}).items():
        require(binding.get("interface") in interfaces, f"{tid}: unknown interface")
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
    for app in model["applications"].values():
        aid = app["id"]
        require(app.get("obligation") in obs and app.get("result") in model["results"], f"{aid}: dangling application")
        target, result = obs[app["obligation"]], model["results"][app["result"]]
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
    return model["contract"]["task_bindings"][tid]


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
    return binding["interface"], binding["work_key"]


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
    if set(binding["obligations"]) <= state["closed"] and binding["mode"] != "verification":
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
    lines = [f"Assembly: {task_id}", f"Work: {binding['statement']}",
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
    lines.append("Check intake: python tools/gr_assembly.py template " + task_id)
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
        live = [p for p in (prs or []) if task_for_pr(p) == tid]
        require(len(live) <= 1, f"ambiguous live execution for {tid}")
        if not live and tid not in queued:
            continue  # Retired semantic bindings remain provenance, not new work.
        if live:
            p = live[0]
            lifecycle = metadata(p.get("body") or "", "Lifecycle")
            action = "resume" if p["draft"] and lifecycle == ["IN_PROGRESS"] else "resolve-blocker" if p["draft"] and lifecycle == ["BLOCKED"] else "review" if not p["draft"] and lifecycle == ["REVIEW"] else "reconcile-lifecycle"
            reasons = [f"existing #{p['number']}"]
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
        actions.append({"task": tid, "action": action, "reasons": reasons,
                        "consumer": binding["consumer"], "assumes": binding["assumes"],
                        "reuse_results": binding.get("reuse_results", []),
                        "potential_downstream": len(affected), "newly_ready_if_proved": len(newly_ready)})
    priority = {"review": 0, "resume": 1, "resolve-blocker": 2, "eligible-for-control": 3}
    return sorted(actions, key=lambda a: (priority.get(a["action"], 4), -a["newly_ready_if_proved"], a["task"]))


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
    lines = ["# D0 to GR assembly overview", "", "Generated by `python tools/gr_assembly.py render`. Do not hand-edit.", "",
             "Scientific acceptance and live execution are separate. Historical research does not discharge a premise.", "",
             "| Goal | Composition |", "|---|---|"]
    for goal in c["goals"]:
        lines.append(f"| {goal['id']} | {'DISCHARGED' if state['goals'][goal['id']] else 'OPEN'} |")
    lines += ["", "| Obligation | Group | Missing logical inputs | Accepted application |", "|---|---|---|---|"]
    for name, ob in model["obligations"].items():
        missing = [", ".join(d for d in m["requires"] if d not in state["closed"]) or "none; conclusion still needs accepted evidence" for m in ob["methods"]]
        lines.append(f"| {name} | {ob['group']} | {' OR '.join(missing)} | {state['witnesses'].get(name, 'none')} |")
    negatives = sum(r["outcome"] == "negative" for r in model["results"].values())
    lines += ["", "## Declared dependency DAG", "", "Incoming inputs of a method are AND; different methods are alternatives.",
              "The diagram is a proof plan, not evidence that any transition is closed.", "", "```mermaid", diagram(model), "```",
              "", f"Historical catalogue: {c['legacy_import']['node_count']} preserved IDs; {negatives} indexed scoped negative results including typed input.",
              "Use `search` for their exact scope and owners. No historical result is accepted automatically.", "",
              "## Agent entry", "", "```bash", "python tools/gr_assembly.py next", "python tools/task_dispatch.py TASK-ID",
              "python tools/gr_assembly.py why OBLIGATION", "python tools/gr_assembly.py search QUERY", "```", "",
              "`next` uses live PRs once. `--offline` means unverified planning and never authorizes launch.",
              "Independent conditional lemmas retain their assumptions. A free slot alone does not prove prerequisites.", "",
              "## Provenance", "", f"Current-route input: `{c['route_input']['ref']}`.",
              f"Historical graph input: `{c['legacy_import']['ref']}`.",
              "The preserved source pin is not a current execution head or an acceptance decision.", ""]
    return "\n".join(lines)


def attempts(model: dict, query: str) -> list[dict]:
    words = query.casefold().split()
    found, typed = [], set()
    for attempt in model["attempts"].values():
        hay = (attempt["id"] + " " + attempt["scope"] + " " + attempt["work_key"]).casefold()
        if all(w in hay for w in words):
            found.append({k: attempt[k] for k in ["id", "scope", "work_key", "interface", "question", "question_digest", "reopen_when"]} |
                         {"enforced": attempt.get("_accepted", False), "review": attempt["review"]["state"]})
        typed.add(attempt["result"])
    for result in model["results"].values():
        hay = (result["id"] + " " + result["statement"]).casefold()
        if result["outcome"] == "negative" and result["id"] not in typed and all(w in hay for w in words):
            found.append({"id": result["id"], "scope": result["statement"], "reported_state": result.get("reported_state"),
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
    for result in model["results"].values():
        fields = [result["id"], result["statement"], *result.get("owners", []), *result.get("hypotheses", {}).values()]
        hay = " ".join(fields).casefold()
        if all(word in hay for word in words):
            item = {k: result.get(k) for k in ["id", "statement", "outcome", "reported_state"]}
            item["owners"] = result.get("owners", [])[:5]
            found.append(item)
    return found[:20]


def impact(model: dict, base: str, ref: str) -> dict:
    import research_input_closure
    selection = research_input_closure.select(model["root"], ref, base)
    changed = set(selection["changed"])
    affected = []
    for app in model["applications"].values():
        result = model["results"][app["result"]]
        paths = {r["path"] for r in result.get("evidence", [])}
        if paths & changed or DIRECTORY + "/contract.json" in changed:
            affected.append({"application": app["id"], "obligation": app["obligation"],
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
            "application": {"id": "APPLICATION-ID", "result": "RESULT-ID", "obligation": binding["obligations"][0],
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
        model = load(args.repo_root)
        if args.command == "check":
            validate_queue(args.repo_root, model)
            data = {"valid": True, "obligations": len(model["obligations"]), "results": len(model["results"]),
                    "discharged": len(evaluate(model)["closed"]), "scientific_promotion": False}
        elif args.command == "render":
            text = overview(model)
            target = args.repo_root / DIRECTORY / "VIEW.md"
            if args.check:
                require(target.is_file() and target.read_text() == text, "assembly view is stale; run render")
            else:
                target.write_text(text)
            data = {"view": str(target), "checked": args.check}
        elif args.command == "show":
            if not args.json:
                print(overview(model), end=""); return 0
            data = {"goals": evaluate(model)["goals"], "open": sorted(set(model["obligations"]) - evaluate(model)["closed"])}
        elif args.command == "dag":
            print(diagram(model)); return 0
        elif args.command == "next":
            from task_dispatch import open_prs
            prs = None if args.offline else open_prs(args.repo_root)
            data = {"live_verified": prs is not None, "actions": next_actions(model, prs),
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
