#!/usr/bin/env python3
"""Read-only, single-pilot C0 reconciliation view over an immutable Git snapshot.

No source decisions or scientific statuses are created here. The tool reads the
existing architecture artifact, scientific owner, support registry, dependency
graph and a previously generated compiled inventory. It does not call Lake,
read untracked files, assert semantic coverage or establish C0 completeness.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import hashlib
import io
import json
import os
import re
import subprocess
from pathlib import Path

PRIMARY = "02_REGISTRY/research/D0_PROOF_ARCHITECTURE_AND_FORMALIZATION.md"
SUPPORT = "02_REGISTRY/formal_support.csv"
GRAPH = "02_REGISTRY/gr_assembly/sources/native_gravity_dependencies.json"
TARGET_HEADING = "Weak smooth test for the composed frozen refinement"
MODULE = "D0.Geometry.ArchiveGradedRefinementWeakTest"
DECLARATION = "D0.Geometry.archive_doubling_sine_weak_pairing_tendsto"
LEAN_PATH = "03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementWeakTest.lean"
SOURCE_DIR = "02_REGISTRY/research/"
CONSUMER = "composed_frozen_readout"
SOURCE_ANCHOR = "5-one-step-estimates-and-composed-fixed-torus-failure"
# Exact elaborated type in the pinned public inventory. This tests spelling and
# shape, not the semantic equivalence of definitions to the research prose.
EXPECTED_TYPE = " ".join("""∀ (r : D0.Role), Filter.Tendsto
  (fun N => D0.Geometry.archiveSineWeakPairing (N + (N + 2))
    (D0.Geometry.archiveRepeatedGradedPullback N (D0.Geometry.archiveUnitSingletonCochain N r) (N + 2)) r)
  Filter.atTop (nhds (2 / Real.pi))""".split())


@dataclass(frozen=True)
class PilotPins:
    """Immutable pilot selectors, not an additional scientific status registry."""

    primary_blob: str
    source_commit: str
    source_path: str
    source_blob: str
    source_owner: str
    source_heading: str
    consumer_graph_blob: str
    consumer_scope: str
    consumer_status: str
    inventory_path: str
    inventory_blob: str
    inventory_sha256: str
    inventory_snapshot: str
    module_blob: str


DEFAULT_PINS = PilotPins(
    primary_blob="d7d9aa2479e2d97c1ebf047bab39a932a14527ef",
    source_commit="75527846bf3603a1c51acf445f8354e3254341be",
    source_path="02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md",
    source_blob="c216f19daebc9a6b2a9e732d277350dd2d69f88c",
    source_owner="310",
    source_heading="5. One-step estimates and composed fixed-torus failure",
    consumer_graph_blob="fdb180cb19c8beb3c9ba96a9b439a1e483d0f68a",
    consumer_scope=("Actual composition of adjacent frozen cochain maps with scale-corrected "
                    "component readout on a fixed unit torus, including L to 2L."),
    consumer_status="PROVED_SCOPED_ANALYTIC_OBSTRUCTION",
    inventory_path="02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/reports/weak_test_declarations_2026-10-28.json",
    inventory_blob="27a3cc53ad304fe629fa43acd617e87f55e915f7",
    inventory_sha256="25e7f5af68dfab9d28123720d735a169f8754d465f97218acb35ae42c3d6a407",
    inventory_snapshot="d2bf764d210cb377387db1bcdb007b88c99f69d3",
    module_blob="4e6b5419f46a542091cec0d4f82d3b693f99cd26",
)


class MissingEvidence(Exception):
    pass


class GitSnapshot:
    def __init__(self, repo: Path, ref: str):
        self.repo = Path(repo).resolve()
        self._objects: dict[tuple[str, str], bytes] = {}
        self.verify_worktree()
        if self.git("rev-parse", "--show-object-format").decode().strip() != "sha1":
            raise MissingEvidence("only SHA-1 Git repositories are supported by this pilot")
        self.snapshot = self.git("rev-parse", "--verify", "--end-of-options",
                                 f"{ref}^{{commit}}").decode().strip()
        self.commit_tree(self.snapshot)

    def git(self, *args: str) -> bytes:
        # Eliminate all inherited Git redirection and configuration injection,
        # then set only our own no-replace/no-network/read-only controls.
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1",
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"})
        try:
            p = subprocess.run(["git", "-C", str(self.repo), *args],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               check=False, timeout=30, env=env)
        except FileNotFoundError as exc:
            raise MissingEvidence("Git executable unavailable") from exc
        except subprocess.TimeoutExpired as exc:
            raise MissingEvidence("Git command timed out") from exc
        except OSError as exc:
            raise MissingEvidence(f"Git could not be executed: {exc}") from exc
        if p.returncode:
            raise MissingEvidence(f"git {' '.join(args)}: {p.stderr.decode(errors='replace').strip()}")
        return p.stdout

    def verify_worktree(self) -> None:
        """Require the declared root and its .git directory or worktree file."""
        dotgit = self.repo / ".git"
        try:
            if dotgit.is_dir():
                expected_gitdir = dotgit.resolve()
            elif dotgit.is_file():
                data = dotgit.read_text(encoding="utf-8").strip()
                if not data.startswith("gitdir: ") or "\n" in data:
                    raise MissingEvidence("invalid .git worktree file")
                gitdir = Path(data[len("gitdir: "):])
                expected_gitdir = (gitdir if gitdir.is_absolute() else self.repo / gitdir).resolve()
            else:
                raise MissingEvidence("declared repo has no .git directory or worktree file")
            top = Path(os.fsdecode(self.git("rev-parse", "--show-toplevel").strip())).resolve()
            actual_gitdir = Path(os.fsdecode(self.git("rev-parse", "--absolute-git-dir").strip())).resolve()
            bare = self.git("rev-parse", "--is-bare-repository").decode().strip()
        except (OSError, UnicodeError) as exc:
            raise MissingEvidence(f"cannot verify worktree identity: {exc}") from exc
        if top != self.repo or actual_gitdir != expected_gitdir or bare != "false":
            raise MissingEvidence("declared repo does not match Git worktree root and git-dir")

    def raw(self, oid: str, kind: str) -> bytes:
        if not re.fullmatch(r"[0-9a-f]{40}", oid):
            raise MissingEvidence(f"invalid SHA-1 object id: {oid!r}")
        key = (oid, kind)
        if key not in self._objects:
            actual_kind = self.git("cat-file", "-t", oid).decode().strip()
            if actual_kind != kind:
                raise MissingEvidence(f"object {oid} has type {actual_kind}, expected {kind}")
            raw = self.git("cat-file", kind, oid)
            header = f"{kind} {len(raw)}\0".encode("ascii")
            if hashlib.sha1(header + raw).hexdigest() != oid:
                raise MissingEvidence(f"raw {kind} object hash mismatch: {oid}")
            self._objects[key] = raw
        return self._objects[key]

    def commit_tree(self, commit: str) -> str:
        raw = self.raw(commit, "commit")
        first = raw.split(b"\n", 1)[0]
        if not re.fullmatch(rb"tree [0-9a-f]{40}", first):
            raise MissingEvidence(f"invalid root tree in commit {commit}")
        return first[5:].decode("ascii")

    def tree_entries(self, oid: str) -> list[tuple[str, str, str]]:
        raw = self.raw(oid, "tree")
        entries = []
        pos = 0
        while pos < len(raw):
            space = raw.find(b" ", pos)
            nul = raw.find(b"\0", space + 1) if space >= 0 else -1
            if space < 0 or nul < 0 or nul + 21 > len(raw):
                raise MissingEvidence(f"invalid raw tree object {oid}")
            try:
                mode = raw[pos:space].decode("ascii")
                name = raw[space + 1:nul].decode("utf-8")
            except UnicodeError as exc:
                raise MissingEvidence(f"invalid tree entry in {oid}") from exc
            if not name or name in (".", "..") or "/" in name or "\\" in name:
                raise MissingEvidence(f"unsafe tree entry in {oid}")
            entries.append((mode, name, raw[nul + 1:nul + 21].hex()))
            pos = nul + 21
        if len({name for _, name, _ in entries}) != len(entries):
            raise MissingEvidence(f"duplicate names in tree {oid}")
        return entries

    def entry_at(self, commit: str, path: str) -> tuple[str, str]:
        parts = path.split("/")
        if not parts or any(p in ("", ".", "..") or "\x00" in p or "\\" in p for p in parts):
            raise MissingEvidence(f"invalid repository path: {path!r}")
        oid = self.commit_tree(commit)
        for index, part in enumerate(parts):
            mode, oid = one([(m, o) for m, n, o in self.tree_entries(oid) if n == part],
                            f"tracked path {path} component {part}")
            if index < len(parts) - 1 and mode not in ("40000", "040000"):
                # Symlinked path components need a separate, complete resolver;
                # never infer their targets from the host filesystem.
                raise MissingEvidence(f"non-tree path component in {path}")
        return mode, oid

    def object_at(self, commit: str, path: str) -> tuple[str, str]:
        mode, oid = self.entry_at(commit, path)
        kind = "tree" if mode in ("40000", "040000") else "blob"
        if kind == "blob" and mode not in ("100644", "100755"):
            raise MissingEvidence(f"path {path} is not a regular tracked file")
        self.raw(oid, kind)
        return oid, kind

    def data(self, commit: str, path: str) -> bytes:
        oid, kind = self.object_at(commit, path)
        if kind != "blob":
            raise MissingEvidence(f"path {path} is not a blob")
        return self.raw(oid, "blob")

    def blob(self, commit: str, path: str) -> str:
        oid, kind = self.object_at(commit, path)
        if kind != "blob":
            raise MissingEvidence(f"path {path} is not a blob")
        return oid

    def unchanged_lean_inputs(self, old: str, new: str) -> bool:
        # Include tracked symlink targets outside the Lean tree. This is a
        # snapshot consistency check, not proof of the full build closure.
        old_oid, old_kind = self.object_at(old, "03_FORMALIZATION")
        new_oid, new_kind = self.object_at(new, "03_FORMALIZATION")
        if old_kind != "tree" or new_kind != "tree" or old_oid != new_oid:
            return False

        links = []
        def walk(tree: str, prefix: str) -> None:
            for mode, name, oid in self.tree_entries(tree):
                path = prefix + "/" + name
                if mode in ("40000", "040000"):
                    walk(oid, path)
                elif mode == "120000":
                    links.append(path)
                elif mode not in ("100644", "100755"):
                    raise MissingEvidence(f"unsupported tracked mode {mode} at {path}")
        walk(old_oid, "03_FORMALIZATION")

        for link in links:
            path = link
            seen = set()
            while True:
                if path in seen:
                    raise MissingEvidence(f"cyclic tracked symlink: {path}")
                seen.add(path)
                mode, oid = self.entry_at(old, path)
                new_mode, new_target_oid = self.entry_at(new, path)
                if (mode, oid) != (new_mode, new_target_oid):
                    return False
                if mode in ("100644", "100755"):
                    self.raw(oid, "blob")
                    break
                if mode != "120000":
                    raise MissingEvidence(f"unsupported symlink target mode {mode} at {path}")
                try:
                    target = self.raw(oid, "blob").decode("utf-8")
                except UnicodeError as exc:
                    raise MissingEvidence(f"non-UTF-8 symlink target at {path}") from exc
                if not target or target.startswith("/") or "\\" in target or "\x00" in target:
                    raise MissingEvidence(f"unsafe symlink target at {path}")
                target_parts = target.split("/")
                if any(part in ("", ".") for part in target_parts):
                    raise MissingEvidence(f"noncanonical symlink target at {path}")
                parts = path.split("/")[:-1]
                named_component_seen = False
                for part in target_parts:
                    if part == "..":
                        # A preceding component could itself be a symlink, so
                        # lexical cancellation would not model OS resolution.
                        if named_component_seen:
                            raise MissingEvidence(f"ambiguous symlink target at {path}")
                        if not parts:
                            raise MissingEvidence(f"symlink escapes repository at {path}")
                        parts.pop()
                    else:
                        named_component_seen = True
                        parts.append(part)
                if not parts or ":" in parts[0]:
                    raise MissingEvidence(f"unsafe symlink target at {path}")
                path = "/".join(parts)
        return True



def one(items: list, label: str):
    if len(items) != 1:
        raise MissingEvidence(f"{label}: expected one, found {len(items)}")
    return items[0]


def parse_json(raw: bytes, label: str):
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise MissingEvidence(f"{label}: invalid UTF-8/JSON: {exc}") from exc


def primary_section(text: str) -> str:
    blocks = re.split(r"(?m)^### ", text)
    matches = [b for b in blocks if b.split("\n", 1)[0].strip() == TARGET_HEADING]
    return one(matches, "primary section")


def reconcile(repo: Path, ref: str, *, pins: PilotPins = DEFAULT_PINS) -> dict:
    """Return independent evidence dimensions; any missing dimension stays unresolved."""
    result = {
        "schema": "d0-c0-reconciliation-pilot-view/1",
        "snapshot": None,
        "scope": {
            "pilot_only": True,
            "all_other_c0_candidates": "not_enumerated_unresolved",
            "c0_freeze_assessment": "not_evaluated",
            "c0_acceptance_assessment": "not_evaluated",
            "this_view_does_not_freeze_or_accept": True,
            "coverage_reported": False,
            "scientific_status_changed": False,
        },
        "authority": {},
        "pilot": {"state": "unresolved", "independent_review": "not_authenticated",
                  "semantic_correspondence": "not_automatically_checked",
                  "consumer_binding_semantics": "unresolved",
                  "provenance": "reported_metadata_links_not_recomputed_or_replayed"},
        "checks": {},
        "issues": [],
    }
    try:
        git = GitSnapshot(repo, ref)
    except MissingEvidence as exc:
        result["checks"]["snapshot"] = {"state": "unresolved", "reason": str(exc)}
        result["issues"].append({"check": "snapshot", "reason": str(exc)})
        result["interpretation"] = "Declared Git worktree or snapshot could not be verified."
        return result
    snapshot = git.snapshot
    result["snapshot"] = snapshot
    checks = result["checks"]
    issues = result["issues"]
    data: dict = {}

    def step(name, callback, state="verified_raw_link", dependencies=()):
        missing = [dep for dep in dependencies if dep not in data]
        if missing:
            reason = "blocked by unresolved checks: " + ", ".join(missing)
            checks[name] = {"state": "blocked_by_dependency", "dependencies": missing}
            issues.append({"check": name, "reason": reason})
            return
        try:
            value = callback()
            checks[name] = {"state": state}
            data[name] = value
        except (MissingEvidence, KeyError, TypeError, ValueError) as exc:
            checks[name] = {"state": "unresolved", "reason": str(exc)}
            issues.append({"check": name, "reason": str(exc)})

    def read_primary():
        raw = git.data(snapshot, PRIMARY)
        primary_blob = git.blob(snapshot, PRIMARY)
        if primary_blob != pins.primary_blob:
            raise MissingEvidence(f"primary blob differs from pinned pilot: {primary_blob}")
        result["authority"]["primary"] = {"path": PRIMARY, "blob": primary_blob}
        return primary_section(raw.decode("utf-8"))

    step("primary_section", read_primary)

    def source_pin():
        owner, commit, path, expected_blob = (pins.source_owner, pins.source_commit,
                                               pins.source_path, pins.source_blob)
        git.commit_tree(commit)
        actual_blob = git.blob(commit, path)
        if actual_blob != expected_blob:
            raise MissingEvidence(f"source blob mismatch: {expected_blob} != {actual_blob}")
        snapshot_blob = git.blob(snapshot, path)
        if snapshot_blob != actual_blob:
            raise MissingEvidence(f"source owner changed in selected snapshot: {snapshot_blob} != {actual_blob}")
        source = git.data(commit, path).decode("utf-8")
        heading = one(re.findall(r"(?m)^## (5\. [^\r\n]+)\s*$", source), "source section 5")
        if heading != pins.source_heading:
            raise MissingEvidence("source heading differs from exact pinned pilot")
        if not re.search(rf"\bDraft #{re.escape(owner)}\b", source):
            raise MissingEvidence("source scientific owner not present")
        pin = {"commit": commit, "path": path, "blob": actual_blob,
               "snapshot_blob": snapshot_blob,
               "section": heading, "owner": f"#{owner}"}
        result["pilot"]["source"] = pin
        result["pilot"]["source_unit_key"] = f"source:{commit}:{path}#{heading}/fixed-sine-weak-test"
        result["pilot"]["unit_scope"] = (
            "Normalized four-role counting pairing of the doubled adjacent-map "
            "unit one-form error with the fixed sampled sine tends to 2/pi."
        )
        return pin

    step("source_pin_and_owner", source_pin)

    def source_primary_link():
        section, pin = data["primary_section"], data["source_pin_and_owner"]
        pattern = (r"§5 of #(\d+)'s\s+`([^`]+)` at commit\s+"
                   r"`([0-9a-f]{40})`, blob\s+`([0-9a-f]{40})`")
        owner, filename, commit, blob = one(re.findall(pattern, section), "source locator")
        if (owner, filename, commit, blob) != (pins.source_owner, Path(pin["path"]).name,
                                               pins.source_commit, pins.source_blob):
            raise MissingEvidence("source locator differs from exact pinned pilot")
        return True

    step("source_primary_link", source_primary_link,
         dependencies=("primary_section", "source_pin_and_owner"))

    def review_report():
        section = data["primary_section"]
        # No free-text interpretation is performed. The exact pinned primary
        # section is returned for a person to assess. Its wording is not an
        # independently authenticated review or semantic approval.
        result["pilot"]["primary_section_text"] = section
        return True

    step("primary_review_text", review_report, "pinned_text_only_not_review_verification",
         dependencies=("primary_section",))

    def support():
        pin = data["source_pin_and_owner"]
        reader = csv.DictReader(io.StringIO(git.data(snapshot, SUPPORT).decode("utf-8")))
        if reader.fieldnames != ["lean_module", "lean_file", "role", "referenced_by"]:
            raise MissingEvidence("formal-support CSV has unexpected schema")
        rows = list(reader)
        if any(None in r or any(not isinstance(v, str) for v in r.values()) for r in rows):
            raise MissingEvidence("formal-support CSV contains malformed rows")
        row = one([r for r in rows if r.get("lean_module") == MODULE], "formal-support locator")
        if row.get("role") != "EXPLICIT_SUPPORT":
            raise MissingEvidence("formal-support role is not EXPLICIT_SUPPORT")
        if row.get("lean_file") != LEAN_PATH.removeprefix("03_FORMALIZATION/"):
            raise MissingEvidence("formal-support Lean path mismatch")
        if pin["path"] not in row.get("referenced_by", "").split(";"):
            raise MissingEvidence("formal-support source locator missing")
        result["authority"]["formal_support"] = {"path": SUPPORT, "blob": git.blob(snapshot, SUPPORT)}
        return row

    step("formal_support", support, dependencies=("source_pin_and_owner",))

    def consumer():
        pin = data["source_pin_and_owner"]
        consumer_id = CONSUMER
        graph_raw = git.data(snapshot, GRAPH)
        graph_blob = git.blob(snapshot, GRAPH)
        if graph_blob != pins.consumer_graph_blob:
            raise MissingEvidence("consumer graph blob differs from pinned pilot snapshot")
        graph = parse_json(graph_raw, "dependency graph")
        if not isinstance(graph, dict) or graph.get("schema") != "d0-native-gravity-dependencies/1":
            raise MissingEvidence("unexpected dependency graph schema")
        if not isinstance(graph.get("nodes"), list):
            raise MissingEvidence("dependency graph nodes must be a list")
        nodes = graph["nodes"]
        if any(not isinstance(n, dict) for n in nodes):
            raise MissingEvidence("dependency graph node must be an object")
        if any(not isinstance(n.get("id"), str) or not n["id"] for n in nodes):
            raise MissingEvidence("dependency graph node ids must be nonempty strings")
        node = one([n for n in nodes if n.get("id") == consumer_id], "consumer node")
        owners = node.get("owners")
        if not isinstance(owners, list) or any(not isinstance(x, str) for x in owners):
            raise MissingEvidence("consumer owners must be a list of strings")
        source_refs = [x for x in owners if x.split("#", 1)[0] == pin["path"]]
        source_ref = one(source_refs, "consumer source owner")
        if source_ref != f"{pin['path']}#{SOURCE_ANCHOR}":
            raise MissingEvidence("consumer source section locator is not exact")
        if any(not isinstance(node.get(k), str) or not node[k] for k in ("scope", "status")):
            raise MissingEvidence("consumer scope and status must be nonempty strings")
        if node["scope"] != pins.consumer_scope or node["status"] != pins.consumer_status:
            raise MissingEvidence("consumer scope or status differs from pinned pilot node")
        result["authority"]["consumer_graph"] = {"path": GRAPH, "blob": graph_blob}
        result["pilot"]["consumer"] = {"id": consumer_id, "source_ref": source_ref,
                                      "scope": node.get("scope"), "status": node.get("status")}
        return node

    step("consumer_and_source_owner", consumer, dependencies=("source_pin_and_owner",))

    def consumer_primary_link():
        ids = re.findall(r"Its consumer is the existing `([^`]+)`", data["primary_section"])
        if one(ids, "primary consumer locator") != CONSUMER:
            raise MissingEvidence("primary consumer locator differs from pinned pilot")
        return True

    step("consumer_primary_link", consumer_primary_link,
         dependencies=("primary_section", "consumer_and_source_owner"))

    def inventory():
        path, expected_sha = pins.inventory_path, pins.inventory_sha256
        raw = git.data(snapshot, path)
        inventory_blob = git.blob(snapshot, path)
        if inventory_blob != pins.inventory_blob:
            raise MissingEvidence("compiled inventory blob differs from pinned pilot")
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != expected_sha:
            raise MissingEvidence(f"inventory digest mismatch: {expected_sha} != {actual_sha}")
        inv = parse_json(raw, "compiled inventory")
        if not isinstance(inv, dict):
            raise MissingEvidence("compiled inventory must be an object")
        if inv.get("schema") != "d0-lean-declaration-inventory-v1":
            raise MissingEvidence("unexpected inventory schema")
        if inv.get("worktree_dirty") is not False or inv.get("public_import_root") != "D0.All":
            raise MissingEvidence("inventory not clean or not extracted from D0.All")
        if inv.get("inventory_mode") != "owning_module_enumeration":
            raise MissingEvidence("inventory mode is not compiled owning-module enumeration")
        if not isinstance(inv.get("toolchain"), str) or not inv["toolchain"]:
            raise MissingEvidence("reported inventory toolchain must be a nonempty string")
        old = inv.get("snapshot_commit", "")
        if not re.fullmatch(r"[0-9a-f]{40}", old):
            raise MissingEvidence("inventory snapshot is missing or not an exact commit")
        # Check object type before equality so a tree used as a snapshot is
        # reported as a malformed provenance claim, not accepted as a commit.
        git.commit_tree(old)
        if old != pins.inventory_snapshot:
            raise MissingEvidence("inventory snapshot differs from pinned pilot")
        old_blob = git.blob(old, LEAN_PATH)
        current_blob = git.blob(snapshot, LEAN_PATH)
        if old_blob != pins.module_blob or old_blob != current_blob or not git.unchanged_lean_inputs(old, snapshot):
            raise MissingEvidence("inventory snapshot no longer matches tracked Lean inputs or symlink targets")
        reported_digest = inv.get("lean_source_digest")
        if not isinstance(reported_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", reported_digest):
            raise MissingEvidence("compiled inventory source digest is malformed")
        declarations = inv.get("declarations")
        if not isinstance(declarations, list) or any(not isinstance(d, dict) for d in declarations):
            raise MissingEvidence("compiled declarations must be a list of objects")
        if any(not isinstance(d.get("name"), str) or not d["name"] for d in declarations):
            raise MissingEvidence("compiled declaration names must be nonempty strings")
        decl = one([d for d in declarations if d.get("name") == DECLARATION],
                   "compiled declaration")
        if (decl.get("exists") is not True or decl.get("internal_name") is not False
                or decl.get("declaration_kind") != "theorem" or decl.get("module") != MODULE
                or decl.get("source_path") != LEAN_PATH):
            raise MissingEvidence("compiled declaration metadata mismatch")
        dtype = decl.get("elaborated_type")
        if not isinstance(dtype, str) or " ".join(dtype.split()) != EXPECTED_TYPE:
            raise MissingEvidence("compiled declaration type differs from the expected exact signature")
        if (not isinstance(decl.get("axioms"), list)
                or any(not isinstance(a, str) or not a for a in decl["axioms"])):
            raise MissingEvidence("compiled declaration axioms must be a list of nonempty strings")
        if any(a == "sorryAx" or a.endswith(".sorryAx") for a in decl["axioms"]):
            raise MissingEvidence("compiled declaration depends on sorryAx")
        evidence = {"path": path, "blob": inventory_blob, "sha256": actual_sha,
                    "inventory_snapshot": old, "lean_source_digest": reported_digest,
                    "source_digest_status": "reported_not_recomputed",
                    "source_closure_status": "not_verified",
                    "tracked_lean_tree_and_symlink_targets": "unchanged_between_snapshots",
                    "toolchain_status": "reported_not_verified",
                    "module_blob": current_blob, "public_import_root": "D0.All",
                    "toolchain": inv.get("toolchain"), "declaration": DECLARATION,
                    "elaborated_type": decl["elaborated_type"], "axioms": decl["axioms"]}
        result["pilot"]["compiled_inventory"] = evidence
        return evidence

    step("compiled_declaration_inventory", inventory, "reported_metadata_links_consistent_not_replayed")

    def inventory_primary_link():
        section, inv = data["primary_section"], data["compiled_declaration_inventory"]
        link = one(re.findall(r"\[compiled declaration inventory\]\(([^)]+)\)", section),
                   "compiled inventory locator")
        path = str((Path(PRIMARY).parent / link).as_posix())
        if ".." in Path(path).parts or path != pins.inventory_path:
            raise MissingEvidence("compiled inventory locator differs from pinned pilot")
        sha = one(re.findall(r"Its SHA-256 is `([0-9a-f]{64})`", section), "inventory digest")
        if sha != pins.inventory_sha256:
            raise MissingEvidence("compiled inventory SHA differs from pinned pilot")
        digest = one(re.findall(r"Lake jobs at Lean source digest\s+`([0-9a-f]{64})`", section),
                     "build source digest")
        if digest != inv["lean_source_digest"]:
            raise MissingEvidence("compiled inventory and reported build digest differ")
        return True

    step("inventory_primary_link", inventory_primary_link,
         "reported_metadata_links_consistent_not_replayed",
         dependencies=("primary_section", "compiled_declaration_inventory"))
    if not issues:
        result["pilot"]["state"] = "reported_metadata_links_consistent_not_c0_acceptance"
    result["interpretation"] = (
        "Consult each check state; unresolved or blocked checks are not verified. Other C0 "
        "candidates are not enumerated. If available, pinned primary text is not authenticated "
        "review. Any matching node is only a locator, and source digest/toolchain are reported, "
        "not recomputed or replayed; complete build closure is unverified. "
        "Type shape does not establish semantic equivalence."
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--snapshot", required=True, help="commit or ref to resolve once")
    args = parser.parse_args()
    result = reconcile(args.repo, args.snapshot)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not result["issues"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
