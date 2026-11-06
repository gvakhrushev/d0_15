#!/usr/bin/env python3
"""Read-only, pinned-slice C0 reconciliation view over an immutable Git snapshot.

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
    primary_section_sha256: str
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
    # SHA-256 of the exact selected Markdown section in primary_blob, with only
    # terminal CR/LF separators normalized so adjacent section spacing is not binding.
    primary_section_sha256="3383876849b02f36db8bf71f174cb50d6800ff345c9b30573aebe478acf682cd",
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
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.details = details


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

    def changed_tracked_paths(self, old: str, new: str, path: str) -> list[str]:
        """List byte-path changes under a tracked subtree without external diff tools."""
        raw = self.git("diff", "--no-ext-diff", "--no-renames", "--name-only", "-z",
                       old, new, "--", path)
        try:
            paths = [item.decode("utf-8") for item in raw.split(b"\0") if item]
        except UnicodeError as exc:
            raise MissingEvidence("changed tracked path is not valid UTF-8") from exc
        prefix = path.rstrip("/") + "/"
        if any(not item.startswith(prefix) or "\\" in item or "\x00" in item
               or any(part in ("", ".", "..") for part in item.split("/"))
               for item in paths):
            raise MissingEvidence("Git returned an unsafe changed tracked path")
        return sorted(paths)

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


def primary_section_sha256(section: str) -> str:
    """Hash the exact section text while excluding terminal Markdown separators."""
    return hashlib.sha256(section.rstrip("\r\n").encode("utf-8")).hexdigest()


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
            if isinstance(exc, MissingEvidence) and exc.details is not None:
                checks[name]["details"] = exc.details
            issues.append({"check": name, "reason": str(exc)})

    def read_primary():
        raw = git.data(snapshot, PRIMARY)
        primary_blob = git.blob(snapshot, PRIMARY)
        section = primary_section(raw.decode("utf-8"))
        section_sha256 = primary_section_sha256(section)
        result["authority"]["primary"] = {
            "path": PRIMARY,
            "blob": primary_blob,
            "historical_document_blob": pins.primary_blob,
            "whole_file_matches_historical_blob": primary_blob == pins.primary_blob,
            "section_sha256": section_sha256,
            "pinned_section_sha256": pins.primary_section_sha256,
        }
        if section_sha256 != pins.primary_section_sha256:
            raise MissingEvidence(
                f"primary section digest differs from pinned pilot: {section_sha256}")
        return section

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
        old_tree, old_tree_kind = git.object_at(old, "03_FORMALIZATION")
        current_tree, current_tree_kind = git.object_at(snapshot, "03_FORMALIZATION")
        if old_tree_kind != "tree" or current_tree_kind != "tree":
            raise MissingEvidence("Lean source root is not a tracked tree")
        changed_paths = git.changed_tracked_paths(old, snapshot, "03_FORMALIZATION")
        tracked_inputs_unchanged = git.unchanged_lean_inputs(old, snapshot)
        if (old_blob != pins.module_blob or old_blob != current_blob
                or not tracked_inputs_unchanged):
            raise MissingEvidence(
                "inventory snapshot no longer matches tracked Lean inputs or symlink targets",
                details={
                    "inventory_snapshot": old,
                    "selected_snapshot": snapshot,
                    "module_path": LEAN_PATH,
                    "inventory_module_blob": old_blob,
                    "pinned_module_blob": pins.module_blob,
                    "selected_module_blob": current_blob,
                    "inventory_formalization_tree": old_tree,
                    "selected_formalization_tree": current_tree,
                    "formalization_tree_unchanged": old_tree == current_tree,
                    "changed_formalization_paths": changed_paths,
                    "all_tracked_lean_inputs_unchanged": tracked_inputs_unchanged,
                    "selected_snapshot_declaration_inventory": "not_rebuilt",
                    "diagnostic_only": True,
                },
            )
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


@dataclass(frozen=True)
class KernelSectionPins:
    """Selectors for one existing review section, not accepted C0 membership."""

    section_label: str = "Book02 §02.3b"
    source_anchor: str = "02.3b"
    units_heading: str = "C0 Book02 mathematical-unit candidates"
    require_unit_module: bool = False
    additional_modules: tuple = ()
    primary_heading: str = "C0 source review candidate: Book02 §02.3b"
    units_sha256: str = "206943122c0f0c1f4db2749b31c1f1e79ba250b506f54b3bc7945319af8991a0"
    primary_sha256: str = "325ebf56d196460c71d305c37a7caf849d649db595d683470ee3e4e7164d200b"
    source_commit: str = "a4d0d3919e9c2b8e9f27aeaacaafd6dcf06e6c38"
    source_path: str = "01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md"
    source_blob: str = "00d7c597abb99856719b274bb86b115b17af139f"
    section_range: tuple = (12086, 15801)
    section_sha256: str = "612be4ee853d2f03469e3877a41cb16490a0cb6e5328fead13b2dbcb5346c7c8"
    module: str = "D0.Foundation.TheoryTransfer"
    module_path: str = "03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean"
    module_blob: str = "a882f38aa1caf4d619c6e1f84c73ebe97e4b127a"
    application_id: str = "lean-operational-transfer-to-theory-transfer"
    application_sha256: str = "f9626b7fde77f911bdfef4d7d669dc6ab30cc0cf0c37b6b2fe7a14e6b4779da9"
    historical_inventory_path: str = (
        "02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
        "assembly_result_declaration_crosswalk.json")
    historical_inventory_sha256: str = "a5375df20f1bfc1468ee7fa5813f1f1e876a96328317aaef976bc9be15c47daa"
    historical_inventory_snapshot: str = "fdebdc21a54eafe4fa877e51fdc684e657b4dd03"
    result_id: str = "lean-operational-theory-transfer"


BOOK01_PINS = KernelSectionPins(
    section_label="Book01 §01.1.8", source_anchor="01.1.8",
    units_heading="C0 Book01 mathematical-unit candidates", require_unit_module=True,
    primary_heading="C0 source review candidate: Book01 §01.1.8",
    units_sha256="7e57599211725623450085baa888770950c98ba0523d84d5a71113b3d07959bf",
    primary_sha256="94516f450237cbb7e0cbccd831ffe9e7b9b2542a1ad92b8e04bf89985e796f8e",
    source_path="01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
    source_blob="eb2d8ea779189084cdaaca717326df88589ec918",
    section_range=(14123, 18478),
    section_sha256="bd468ba86fc3eb70004871d2bb5777c40afbfb7f92394d33c52b46759692ea9f",
    module="D0.Foundation.VerificationCore",
    module_path="03_FORMALIZATION/D0/Foundation/VerificationCore.lean",
    module_blob="01b02ebbe81a62464e81d5c397c101fd60fff4f9",
    additional_modules=(
        ("D0.Foundation.FutureExecution", "03_FORMALIZATION/D0/Foundation/FutureExecution.lean",
         "065a8f631e65bda8b9bc85a6ff6217de31bdd1f4"),
        ("D0.Foundation.VerifiabilityNecessity", "03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean",
         "f0dbfcf6e99a24346fa1d9407b4ed49cc784a2e1")),
    application_id="lean-verification-core-to-foundation",
    application_sha256="d53a965e0b258f787078f1e197554f043ae035a5feda7a7b2aca3ad00d71ca8e",
    # This section has no complete historical owner inventory. Do not silently
    # substitute Book02's diagnostic crosswalk for missing Book01 evidence.
    historical_inventory_path="", result_id="lean-verification-core-composition")


# Versioned proof-only owner: historical source pin is never replaced. The
# active snapshot may use only the reviewed historical and exact refactor blobs.
# This verifies provenance, not semantic acceptance or execution of this
# Python helper from the selected snapshot.
VERSIONED_OWNER_BLOBS = {
    ("D0.Foundation.FutureShortlexAdapter",
     "03_FORMALIZATION/D0/Foundation/FutureShortlexAdapter.lean",
     "a4a390673994ecbe7529ebae636ddd3fd6e2db7d"):
        frozenset(("a4a390673994ecbe7529ebae636ddd3fd6e2db7d",
                   "b4ec8b60a52aaa1bb3e5b1fcc40b57ba1087d43b",
                   "4ecbb048faabcdd4b2a5a2b50141e86663d731de")),
}


BOOK01_0116_PINS = KernelSectionPins(
    section_label="Book01 §01.1.6", source_anchor="01.1.6",
    units_heading="C0 Book01 01.1.6 mathematical-unit candidates", require_unit_module=True,
    primary_heading="C0 source review candidate: Book01 §01.1.6",
    units_sha256="ca7095ac7b65fd27d3f44f29686b74705a1f6214d210e7bdef5bcabd5974d896",
    primary_sha256="a9d283028959bbae0045e4c02f90c0697a955ac0878dbb1c00fbd1605e86f2e9",
    source_commit="1eabcccbf7e115c667e9bb8c445ef300107b1493",
    source_path="01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
    source_blob="eb2d8ea779189084cdaaca717326df88589ec918",
    section_range=(11972, 13530),
    section_sha256="ba3fc2c88b388bad890dfcbced2b22343f2019b72d78c927b9488c40ab69afac",
    module="D0.Foundation.VerificationCore",
    module_path="03_FORMALIZATION/D0/Foundation/VerificationCore.lean",
    module_blob="01b02ebbe81a62464e81d5c397c101fd60fff4f9",
    additional_modules=(
        ("D0.Foundation.FutureExecution", "03_FORMALIZATION/D0/Foundation/FutureExecution.lean",
         "065a8f631e65bda8b9bc85a6ff6217de31bdd1f4"),
        ("D0.Foundation.UncoupledCenterRawWitness", "03_FORMALIZATION/D0/Foundation/UncoupledCenterRawWitness.lean",
         "bf1468824fe63fc5f2fed59d74d44d1377923fa6"),
        ("D0.Foundation.FutureShortlexAdapter", "03_FORMALIZATION/D0/Foundation/FutureShortlexAdapter.lean",
         "a4a390673994ecbe7529ebae636ddd3fd6e2db7d")),
    application_id="lean-verification-core-to-foundation",
    application_sha256="d53a965e0b258f787078f1e197554f043ae035a5feda7a7b2aca3ad00d71ca8e",
    historical_inventory_path="", result_id="lean-verification-core-composition")



# Versioned source review: its tracked history activates the correction, so
# querying an earlier snapshot retains its original output. The path and
# digests authenticate bytes, not the review's scientific correctness.
BOOK02_REVIEW_DIR = ("02_REGISTRY/research/sources/d0_proof_architecture_formalization_2026-10-24/"
                     "reports/book02_023b_complete_review_2026-11-06/")
BOOK02_REVIEW = BOOK02_REVIEW_DIR + "SUMMARY_RU.md"
BOOK02_REVIEW_SHA256 = "5163ffef52bf71dfe64820d33c5e94b874fa2e0c2ddba9381eea821718c70e98"
BOOK02_REVIEW_BASE = "a358e91e764655b16082bf7e6161a79df96a24a6"
BOOK02_CONTROL = "d0-book02-represented-emptyword.lean"
BOOK02_CONTROL_SHA256 = "9bb93ff0f4dd5d5a4b194cac1214ea85f19c978fc64d06cb0b773b5d47c67b38"


def book02_reviewed_corrections(git, snapshot, pins, primary, active_version, units):
    """Read proposed corrections from the pinned review; do not accept them.

    Git history is consulted so that an ancestor's published review cannot be
    silently dropped by deleting its current file or pointer. Older snapshots
    without that history keep their byte-for-byte historical presentation.
    """
    if (pins.source_path != KernelSectionPins.source_path or
            pins.units_sha256 != KernelSectionPins.units_sha256):
        return None
    # Search only after the review's recorded base. Besides preserving old
    # outputs this avoids requiring unrelated, possibly pruned historic trees.
    if snapshot == BOOK02_REVIEW_BASE:
        return None
    if git.git("merge-base", BOOK02_REVIEW_BASE, snapshot).decode("ascii").strip() != BOOK02_REVIEW_BASE:
        return None
    history = git.git("log", "--ancestry-path", "--format=%H", "-1",
                      BOOK02_REVIEW_BASE + ".." + snapshot, "--", BOOK02_REVIEW).strip()
    if not history:
        return None
    if active_version is None or active_version["version"] != "corrected":
        raise MissingEvidence("reviewed Book02 correction requires corrected source")
    pointer = "book02_023b_complete_review_2026-11-06/SUMMARY_RU.md"
    if primary.count(pointer) != 1:
        raise MissingEvidence("reviewed Book02 primary pointer missing or ambiguous")
    raw = git.data(snapshot, BOOK02_REVIEW)
    if hashlib.sha256(raw).hexdigest() != BOOK02_REVIEW_SHA256:
        raise MissingEvidence("reviewed Book02 correction digest mismatch")
    control = git.data(snapshot, BOOK02_REVIEW_DIR + BOOK02_CONTROL)
    if hashlib.sha256(control).hexdigest() != BOOK02_CONTROL_SHA256:
        raise MissingEvidence("reviewed Book02 dependency control digest mismatch")
    text = raw.decode("utf-8")
    section = one([x for x in re.split(r"(?m)^## ", text)
                   if x.split("\n", 1)[0].strip() == "Machine-readable proposed corrections"],
                  "reviewed Book02 correction block")
    blocks = re.findall(r"(?s)```json\s*\n(.*?)\n```", section)
    payload = parse_json(one(blocks, "reviewed Book02 correction JSON").encode("utf-8"), "Book02 corrections")
    if payload.get("schema") != "book02-023b-reviewed-corrections/1":
        raise MissingEvidence("unsupported Book02 corrections schema")
    fixes = payload.get("corrections")
    obs = "Interpretation.translate_future_observation"
    run = "Interpretation.verifiedRun_image"
    if not isinstance(fixes, dict) or set(fixes) != {obs, run}:
        raise MissingEvidence("unexpected Book02 correction targets")
    if not isinstance(fixes[obs], dict) or not isinstance(fixes[run], dict):
        raise MissingEvidence("malformed Book02 correction records")
    originals = {u["atom"]: u for u in units}
    if (obs not in originals or run not in originals or
            fixes[obs].get("historical_statement") != originals[obs]["statement"] or
            not isinstance(fixes[obs].get("statement"), str) or not fixes[obs]["statement"] or
            fixes[run].get("proof_dependency") !=
                "D0.Foundation.TheoryTransfer.Interpretation.verifiedStateImageEquiv_representedState" or
            fixes[run].get("control") != BOOK02_CONTROL or
            not isinstance(fixes[run].get("role"), str) or not fixes[run]["role"]):
        raise MissingEvidence("Book02 corrections do not match historical candidates")
    return fixes

def reconcile_kernel_sections(repo: Path, ref: str, *, pins=None,
                              inventory_path=None, inventory_sha256=None) -> dict:
    """Reconcile one pinned kernel slice without inferring scientific acceptance.

    Clean inventory overrides are exact tracked artifacts, not paths to host
    files. The historical crosswalk remains diagnostic: its dirty source tree
    and omitted proof details cannot establish a current compiled theorem.
    """
    pins = pins or KernelSectionPins()
    result = {
        "schema": "d0-c0-kernel-section-view/1", "snapshot": None,
        "scope": {
            "sections": [pins.section_label], "finite_slice_only": True,
            "book01_01_1_8": ("selected_for_reconciliation_not_accepted" if pins.source_anchor == "01.1.8"
                              else "outside_selected_slice_pending_independent_reconciliation"),
            "all_other_c0_candidates": "not_enumerated_unresolved",
            "c0_acceptance_assessment": "not_evaluated", "coverage_reported": False,
            "this_view_does_not_freeze_or_accept": True, "scientific_status_changed": False,
            "running_reconciliation_helper": "current_runtime_not_authenticated_against_selected_snapshot",
        },
        "authority": {}, "checks": {}, "issues": [], "units": [],
    }
    if pins.source_anchor == "01.1.6":
        result["scope"]["book01_01_1_6"] = "selected_for_reconciliation_not_accepted"
    data = {}

    def step(name, callback, dependencies=()):
        missing = [d for d in dependencies if d not in data]
        try:
            if missing:
                raise MissingEvidence("blocked by unresolved checks: " + ", ".join(missing))
            data[name] = callback()
            result["checks"][name] = {"state": "raw_links_consistent_not_semantic_acceptance"}
        except (MissingEvidence, KeyError, TypeError, ValueError, UnicodeError) as exc:
            result["checks"][name] = {"state": "unresolved", "reason": str(exc)}
            result["issues"].append({"check": name, "reason": str(exc)})

    step("snapshot", lambda: GitSnapshot(repo, ref))
    if "snapshot" not in data:
        return result
    git = data["snapshot"]
    snapshot = git.snapshot
    result["snapshot"] = snapshot

    def source_and_primary():
        text = git.data(snapshot, PRIMARY).decode("utf-8")
        try:
            from tools.c0_kernel_units import parse_unit_candidates
        except ModuleNotFoundError:
            from c0_kernel_units import parse_unit_candidates
        units = parse_unit_candidates(text, pins.units_sha256, heading=pins.units_heading)
        module_pins = ((pins.module, pins.module_path, pins.module_blob),) + pins.additional_modules
        if len({m for m, _, _ in module_pins}) != len(module_pins):
            raise MissingEvidence("duplicate pinned owner module")
        historical_owners = {m: (path, blob) for m, path, blob in module_pins}
        owners = dict(historical_owners)
        for u in units:
            if pins.require_unit_module and "module" not in u:
                raise MissingEvidence("mathematical atom lacks explicit owner module")
            if u.get("module", pins.module) not in owners:
                raise MissingEvidence("mathematical atom names unpinned owner module")
        section = one([b for b in re.split(r"(?m)^### ", text)
                       if b.split("\n", 1)[0].strip() == pins.primary_heading],
                      pins.section_label + " primary review section")
        if primary_section_sha256(section) != pins.primary_sha256:
            raise MissingEvidence(pins.section_label + " primary review section digest mismatch")
        for token in (pins.source_commit, pins.source_blob, pins.section_sha256,
                      pins.application_id, *(blob for _, _, blob in module_pins)):
            if token not in section:
                raise MissingEvidence(pins.section_label + " primary review section lacks exact source/application pin")
        if git.blob(pins.source_commit, pins.source_path) != pins.source_blob:
            raise MissingEvidence(pins.section_label + " source blob mismatch at pinned commit")
        raw = git.data(pins.source_commit, pins.source_path)
        current_blob = git.blob(snapshot, pins.source_path)
        active_version = None
        try:
            from tools import c0_book02_version as book02_version
        except ModuleNotFoundError:
            import c0_book02_version as book02_version
        if pins.source_path == book02_version.PATH and pins.source_blob == book02_version.ORIGINAL_BLOB:
            active_version = book02_version.classify(
                raw, pins.source_blob, git.data(snapshot, pins.source_path), current_blob)
        elif current_blob != pins.source_blob:
            raise MissingEvidence(pins.section_label + " source changed in selected snapshot")
        start, end = pins.section_range
        if not 0 <= start < end <= len(raw):
            raise MissingEvidence(pins.section_label + " section range is outside pinned source")
        if hashlib.sha256(raw[start:end]).hexdigest() != pins.section_sha256:
            raise MissingEvidence(pins.section_label + " source section digest mismatch")
        for module, path, blob in module_pins:
            if git.blob(pins.source_commit, path) != blob:
                raise MissingEvidence("historical source differs from pinned reviewed module: " + module)
            active_blob = git.blob(snapshot, path)
            allowed = VERSIONED_OWNER_BLOBS.get((module, path, blob), frozenset((blob,)))
            if active_blob not in allowed:
                raise MissingEvidence("source differs from pinned reviewed module: " + module)
            owners[module] = (path, active_blob)
        if len({u["atom"] for u in units}) != len(units):
            raise MissingEvidence("duplicate mathematical atom key")
        for u in units:
            a, b = u["source_range"]
            if not start <= a < b <= end:
                raise MissingEvidence("mathematical atom range is outside pinned section")
            if not all(isinstance(u[k], str) and u[k] for k in
                       ("atom", "hypotheses", "statement", "disposition", "declaration")):
                raise MissingEvidence("incomplete mathematical atom")
            raw[a:b].decode("utf-8")
        corrections = book02_reviewed_corrections(git, snapshot, pins, text, active_version, units)
        if corrections is not None:
            result["authority"]["active_semantic_review"] = {
                "path": BOOK02_REVIEW, "sha256": BOOK02_REVIEW_SHA256,
                "control": BOOK02_REVIEW_DIR + BOOK02_CONTROL,
                "control_sha256": BOOK02_CONTROL_SHA256,
                "semantic_acceptance": "not_assessed",
            }
        result["authority"]["source"] = {
            "commit": pins.source_commit, "path": pins.source_path, "blob": pins.source_blob,
            "section_range": [start, end], "section_sha256": pins.section_sha256,
            "primary_path": PRIMARY, "primary_section_sha256": pins.primary_sha256,
            "module_path": pins.module_path, "module_blob": pins.module_blob,
            "owner_modules": [{"module": m, "path": p, "blob": b,
                               "historical_blob": b, "active_blob": owners[m][1]}
                              for m, p, b in module_pins],
        }
        if active_version is not None:
            # Units and byte ranges below still refer to the historical source.
            # The corrected version is an exact mapped derivative, not acceptance
            # or a semantic reclassification of either source version.
            result["authority"]["active_source_version"] = active_version
        # Keep context/duplicate/open-obligation dispositions in their existing
        # owning prose instead of copying a second classification into code.
        result["context_dispositions"] = {
            "path": PRIMARY, "section": pins.primary_heading,
            "section_sha256": pins.primary_sha256, "pinned_text": section,
            "acceptance": "not_authenticated_by_this_view",
        }
        return {"raw": raw, "units": units, "owners": owners,
                "corrections": corrections, "active_version": active_version,
                "active_raw": (git.data(snapshot, pins.source_path) if active_version else None)}

    step("source_and_primary", source_and_primary)

    def application():
        path = "02_REGISTRY/gr_assembly/applications.json"
        obj = parse_json(git.data(snapshot, path), "applications")
        app = one([a for a in obj["applications"] if a["id"] == pins.application_id],
                  "existing kernel application")
        digest = hashlib.sha256(json.dumps(app, ensure_ascii=False, sort_keys=True,
                                           separators=(",", ":")).encode()).hexdigest()
        if digest != pins.application_sha256:
            raise MissingEvidence("existing application record differs from pin")
        decision = app["review"]["decision"]
        raw = git.data(decision["ref"], decision["path"])
        if hashlib.sha256(raw).hexdigest() != decision["sha256"]:
            raise MissingEvidence("application review decision digest mismatch")
        result["authority"]["application"] = {
            "id": app["id"], "path": path, "record_sha256": digest,
            "consumer_location": app["consumer_location"], "hypothesis_map": app["hypothesis_map"],
            "recorded_review_state": app["review"]["state"], "decision": decision,
            "interpretation": "existing application only; not acceptance of these C0 atoms",
        }
        return app

    step("existing_application", application)

    def inventory():
        units = data["source_and_primary"]["units"]
        if bool(inventory_path) != bool(inventory_sha256):
            raise MissingEvidence("inventory override requires both tracked path and SHA-256")
        if inventory_path is None and not pins.historical_inventory_path:
            raise MissingEvidence("this section requires a clean tracked inventory override")
        path = inventory_path or pins.historical_inventory_path
        digest = inventory_sha256 or pins.historical_inventory_sha256
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise MissingEvidence("inventory SHA-256 is malformed")
        raw = git.data(snapshot, path)
        if hashlib.sha256(raw).hexdigest() != digest:
            raise MissingEvidence("kernel inventory digest mismatch")
        inv = parse_json(raw, "kernel inventory")
        if not isinstance(inv, dict) or inv.get("public_import_root") != "D0.All":
            raise MissingEvidence("kernel inventory must be an object extracted from D0.All")
        old = inv.get("snapshot_commit", "")
        git.commit_tree(old)
        evidence = {"path": path, "blob": git.blob(snapshot, path), "sha256": digest,
                    "snapshot_commit": old, "source_digest_status": "reported_not_recomputed",
                    "current_build_replayed": False, "semantic_correspondence": "pending_review"}
        if inventory_path is None:
            if old != pins.historical_inventory_snapshot or inv.get("worktree_dirty") is not True:
                raise MissingEvidence("historical kernel inventory provenance differs from pin")
            row = one([r for r in inv["results"] if r["result_id"] == pins.result_id],
                      "historical kernel result")
            declarations = row["compiled_declarations"]
            evidence["state"] = "historical_dirty_snapshot_diagnostic_only"
        else:
            if (inv.get("schema") != "d0-lean-declaration-inventory-v1"
                    or inv.get("inventory_mode") != "owning_module_enumeration"
                    or inv.get("worktree_dirty") is not False):
                raise MissingEvidence("current kernel inventory must be clean owning-module enumeration")
            if (any(git.blob(old, path) != blob
                    for path, blob in data["source_and_primary"]["owners"].values())
                    or not git.unchanged_lean_inputs(old, snapshot)):
                raise MissingEvidence("kernel inventory snapshot no longer matches tracked Lean inputs or symlink targets")
            expected_toolchain = git.data(snapshot, "03_FORMALIZATION/lean-toolchain").decode().strip()
            if inv.get("toolchain") != expected_toolchain:
                raise MissingEvidence("kernel inventory toolchain differs from tracked toolchain")
            collector_path = "tools/lean_declaration_inventory.py"
            if git.blob(old, collector_path) != git.blob(snapshot, collector_path):
                raise MissingEvidence("kernel declaration collector changed since inventory snapshot")
            for field in ("lean_source_digest", "collector_sha256"):
                if not isinstance(inv.get(field), str) or not re.fullmatch(r"[0-9a-f]{64}", inv[field]):
                    raise MissingEvidence("kernel inventory " + field + " is malformed")
            # collector_sha256 authenticates generated Collect.lean, not this
            # Python source file. Recreate only that text, never invoke Lake.
            try:
                from tools import lean_declaration_inventory as collector
            except ModuleNotFoundError:
                import lean_declaration_inventory as collector
            generator_bytes = Path(collector.__file__).read_bytes()
            if generator_bytes != git.data(snapshot, collector_path):
                raise MissingEvidence("running collector generator differs from selected snapshot")
            modules = inv.get("requested_modules")
            if (not isinstance(modules, list) or not modules
                    or any(not isinstance(m, str) for m in modules)
                    or inv.get("module_prefix") is not None
                    or not set(data["source_and_primary"]["owners"]).issubset(modules)):
                raise MissingEvidence("kernel inventory must enumerate every pinned owner explicitly")
            generated = collector.lean_module_collector(modules, "D0.All", include_proof_details=True)
            if inv["collector_sha256"] != hashlib.sha256(generated.encode("utf-8")).hexdigest():
                raise MissingEvidence("kernel inventory collector digest differs from generated Lean collector")
            evidence.update(state="reported_compiled_metadata_consistent_not_replayed",
                            tracked_lean_inputs="unchanged_between_snapshots",
                            toolchain=expected_toolchain, collector_source="unchanged_between_snapshots",
                            collector_script="regenerated_text_matches_digest_not_executed",
                            lean_source_digest=inv["lean_source_digest"],
                            collector_sha256=inv["collector_sha256"])
            declarations = inv["declarations"]
        if not isinstance(declarations, list) or any(not isinstance(d, dict) for d in declarations):
            raise MissingEvidence("kernel declarations must be a list of objects")
        selected = {}
        for u in units:
            dec = one([d for d in declarations if d.get("name") == u["declaration"]],
                      "compiled declaration " + u["declaration"])
            owner = u.get("module", pins.module)
            owner_path, _ = data["source_and_primary"]["owners"][owner]
            if (dec.get("exists") is not True or dec.get("internal_name") is not False
                    or dec.get("module") != owner or dec.get("source_path") != owner_path
                    or dec.get("declaration_kind") != u["declaration_kind"]):
                raise MissingEvidence("kernel declaration metadata mismatch: " + u["declaration"])
            typ = dec.get("elaborated_type")
            if (not isinstance(typ, str) or
                    hashlib.sha256(" ".join(typ.split()).encode()).hexdigest() != u["type_sha256"]):
                raise MissingEvidence("kernel declaration signature mismatch: " + u["declaration"])
            axioms = dec.get("axioms")
            if inventory_path is not None:
                if dec.get("proof_details_status") != "collected" or any(
                        not isinstance(dec.get(field), list) or
                        any(not isinstance(x, str) or not x for x in dec[field])
                        for field in ("proof_dependencies", "type_dependencies")):
                    raise MissingEvidence("kernel declaration lacks complete proof metadata: " + u["declaration"])
                if not isinstance(axioms, list) or any(not isinstance(a, str) or not a for a in axioms):
                    raise MissingEvidence("kernel declaration lacks axiom audit: " + u["declaration"])
                if any(a not in ("propext", "Classical.choice", "Quot.sound") for a in axioms):
                    raise MissingEvidence("kernel declaration has unreviewed axiom: " + u["declaration"])
            selected[u["declaration"]] = {
                "name": dec["name"], "kind": dec["declaration_kind"], "elaborated_type": typ,
                "axioms": axioms, "state": evidence["state"],
                "axiom_audit": "reported_standard_axioms_only" if inventory_path else "not_available",
            }
        result["authority"]["compiled_inventory"] = evidence
        return selected

    step("compiled_inventory", inventory, dependencies=("source_and_primary",))
    if inventory_path is None and "compiled_inventory" in data:
        result["checks"]["current_compiled_evidence"] = {
            "state": "unresolved", "reason": "historical inventory has dirty source and omitted axiom details"}
        result["issues"].append({"check": "current_compiled_evidence",
                                 "reason": "provide a clean tracked inventory with --kernel-inventory and --kernel-inventory-sha256"})
    if "source_and_primary" in data:
        raw = data["source_and_primary"]["raw"]
        for u in data["source_and_primary"]["units"]:
            a, b = u["source_range"]
            row = {k: v for k, v in u.items() if k not in ("declaration_kind", "type_sha256")}
            row.update(source_unit_key=(f"source:{pins.source_commit}:{pins.source_path}"
                                        f"#{pins.source_anchor}/{u['atom']}"),
                       source_excerpt=raw[a:b].decode("utf-8"),
                       source_excerpt_sha256=hashlib.sha256(raw[a:b]).hexdigest(),
                       classification_state="proposed_atomization_of_existing_review_ranges",
                       semantic_acceptance="pending_independent_review",
                       compiled_declaration=data.get("compiled_inventory", {}).get(u["declaration"]),
                       existing_application=(pins.application_id if "existing_application" in data else None),
                       application_scope="shared conditional application; no per-atom semantic acceptance inferred")
            corrections = data["source_and_primary"]["corrections"]
            if corrections and u["atom"] in corrections:
                correction = corrections[u["atom"]]
                if "statement" in correction:
                    row["historical_statement"] = row["statement"]
                    row["statement"] = correction["statement"]
                if "proof_dependency" in correction:
                    row["reviewed_proof_dependency"] = {
                        "declaration": correction["proof_dependency"],
                        "role": correction["role"],
                        "control": BOOK02_REVIEW_DIR + correction["control"],
                    }
                row["active_semantic_correction"] = {
                    "review": BOOK02_REVIEW, "sha256": BOOK02_REVIEW_SHA256,
                    "semantic_acceptance": "not_assessed",
                }
            active = data["source_and_primary"]["active_version"]
            if active is not None:
                row["source_excerpt_version"] = "historical_source_pin"
                if active["version"] == "corrected":
                    try:
                        from tools import c0_book02_version as book02_version
                    except ModuleNotFoundError:
                        import c0_book02_version as book02_version
                    aa, bb = book02_version.translate_offset(a), book02_version.translate_offset(b)
                    excerpt = data["source_and_primary"]["active_raw"][aa:bb]
                    row["active_source_excerpt"] = {
                        "snapshot": snapshot, "blob": active["blob"], "range": [aa, bb],
                        "text": excerpt.decode("utf-8"),
                        "sha256": hashlib.sha256(excerpt).hexdigest(),
                        "mapping": "byte_range_mapped_from_historical_candidate",
                        "semantic_correspondence": "not_assessed",
                        "contains_correction": (a < book02_version.OFFSET + len(book02_version.ORIGINAL)
                                                and b > book02_version.OFFSET),
                    }
            result["units"].append(row)
    result["interpretation"] = (
        f"This is a proposed finite {pins.section_label} atomization, not the C0 denominator. Shared source ranges "
        "are evidence for distinct assertions, not disjoint byte units. Definitions, conditional theorems "
        "and negative controls remain distinct. Existing accepted application metadata does not accept "
        "these source classifications. All unselected slices and full C0 acceptance remain unresolved. Exact reported "
        "compiled signatures do not establish semantic correspondence or replay the build."
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--snapshot", required=True, help="commit or ref to resolve once")
    parser.add_argument("--kernel-sections", action="store_true",
                        help="bounded kernel mathematical-atom view; defaults to Book02")
    parser.add_argument("--kernel-book", choices=("book01", "book01-0116", "book02"),
                        help="select the pinned kernel slice; requires --kernel-sections")
    parser.add_argument("--kernel-inventory", help="tracked clean compiled inventory path")
    parser.add_argument("--kernel-inventory-sha256", help="exact SHA-256 of that inventory")
    args = parser.parse_args()
    if bool(args.kernel_inventory) != bool(args.kernel_inventory_sha256):
        parser.error("--kernel-inventory and --kernel-inventory-sha256 must be supplied together")
    if args.kernel_inventory and not args.kernel_sections:
        parser.error("--kernel-inventory requires --kernel-sections")
    if args.kernel_book and not args.kernel_sections:
        parser.error("--kernel-book requires --kernel-sections")
    result = (reconcile_kernel_sections(
        args.repo, args.snapshot, inventory_path=args.kernel_inventory,
        inventory_sha256=args.kernel_inventory_sha256,
        pins=({"book01": BOOK01_PINS, "book01-0116": BOOK01_0116_PINS}
              .get(args.kernel_book, KernelSectionPins())))
        if args.kernel_sections else reconcile(args.repo, args.snapshot))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not result["issues"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
