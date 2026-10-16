#!/usr/bin/env python3
"""Read-only changed-input closure for research certificates.

Selection is not execution. A skipped scientific step is not a replay.
The existing runner is not modified; certificate_paths is the one-line hook
a later owner can call. Historical receipt paths are never opened for write.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import sysconfig

ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = "02_REGISTRY/research/certificates"
SCIENTIFIC_STEP = "Replay research certificates in isolated worktrees"
SCHEMA = "research-input-closure/1"
LIST_KINDS = {
    "INPUTS": "inputs",
    "VALIDATION": "validation",
    "PINS": "pin",
    "PINNED": "pin",
    "PINNED_INPUTS": "pin",
    "PINNED_PATHS": "pin",
}
PIN_MAPS = {"PINNED_SHA256", "INPUT_SHA256", "PINNED_COMMITS"}
PATH_SUFFIXES = (".py", ".json", ".md", ".txt", ".csv")
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
REQUIREMENT_NAME = re.compile(r"^[A-Za-z0-9_.-]+")


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def git_optional(repo: Path, *args: str) -> bytes | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *args], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None


def resolve_commit(repo: Path, ref: str) -> str:
    try:
        return git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()
    except subprocess.CalledProcessError as error:
        raise ValueError(f"unresolved commit {ref}") from error


def tree_paths(repo: Path, commit: str) -> set[str]:
    raw = git(repo, "ls-tree", "-r", "--name-only", "-z", commit)
    return {os.fsdecode(path) for path in raw.split(b"\0") if path}


def changed_paths(repo: Path, base: str, commit: str) -> list[str]:
    raw = git(repo, "diff", "--name-only", "-z", "--no-renames", base, commit, "--")
    return sorted({os.fsdecode(path) for path in raw.split(b"\0") if path})


def blob(repo: Path, commit: str, path: str) -> bytes | None:
    if not path or path.startswith("/") or ".." in PurePosixPath(path).parts:
        return None
    return git_optional(repo, "show", f"{commit}:{path}")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_rel(text: str) -> str | None:
    if not text or text.startswith("/") or "\\" in text:
        return None
    parts = []
    for part in PurePosixPath(text).parts:
        if part in ("", "."):
            continue
        if part == "..":
            return None
        parts.append(part)
    if not parts:
        return None
    return "/".join(parts)


def parent_path(path: str) -> str:
    parent = PurePosixPath(path).parent.as_posix()
    return "" if parent == "." else parent


def nth_parent(path: str, index: int) -> str | None:
    pure = PurePosixPath(path)
    if index < 0 or index >= len(pure.parents):
        return None
    parent = pure.parents[index].as_posix()
    return "" if parent == "." else parent


def join_path(base: str, child: str) -> str | None:
    norm_child = normalize_rel(child)
    if norm_child is None:
        return None
    if base == "":
        return norm_child
    return normalize_rel(f"{base}/{norm_child}")


def looks_like_path(text: str) -> bool:
    return "/" in text or text.endswith(PATH_SUFFIXES)


def classify_pin(text: str) -> str | None:
    if SHA256_RE.fullmatch(text):
        return "sha256"
    if COMMIT_RE.fullmatch(text):
        return "commit"
    return None


def dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        if base:
            return f"{base}.{node.attr}"
    return None


def slice_value(node: ast.Subscript):
    sl = node.slice
    if isinstance(sl, ast.Constant):
        return sl.value
    index = getattr(ast, "Index", None)
    if index is not None and isinstance(sl, index):
        inner = sl.value
        if isinstance(inner, ast.Constant):
            return inner.value
    return None


def stdlib_roots() -> set[str]:
    roots = set(sys.builtin_module_names)
    if hasattr(sys, "stdlib_module_names"):
        roots.update(sys.stdlib_module_names)
    stdlib = Path(sysconfig.get_path("stdlib"))
    if stdlib.is_dir():
        for entry in stdlib.iterdir():
            name = entry.name
            if name.startswith(".") or name in {"site-packages", "dist-packages"}:
                continue
            if entry.suffix == ".py":
                roots.add(entry.stem)
            elif entry.is_dir() and (entry / "__init__.py").is_file():
                roots.add(name)
        dynload = stdlib / "lib-dynload"
        if dynload.is_dir():
            for entry in dynload.iterdir():
                roots.add(entry.name.split(".", 1)[0])
    return roots


def requirement_roots(text: str) -> set[str]:
    roots = set()
    for line in text.splitlines():
        body = line.split("#", 1)[0].strip()
        if not body or body.startswith(("-", ".")):
            continue
        match = REQUIREMENT_NAME.match(body)
        if not match:
            continue
        name = match.group(0).lower().replace("-", "_")
        roots.add(name)
    return roots


def external_roots(repo: Path, commit: str) -> set[str]:
    roots = stdlib_roots()
    raw = blob(repo, commit, "requirements.txt")
    if raw is not None:
        roots.update(requirement_roots(raw.decode("utf-8", errors="replace")))
    return roots


def eval_expr(node: ast.AST, consts: dict, file_path: str):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return ("string", node.value)
    if isinstance(node, ast.Name):
        if node.id == "__file__" and node.id not in consts:
            return ("path", file_path)
        return consts.get(node.id)
    if isinstance(node, ast.Attribute) and node.attr == "parent":
        inner = eval_expr(node.value, consts, file_path)
        if inner and inner[0] == "path" and inner[1]:
            return ("path", parent_path(inner[1]))
        return None
    if isinstance(node, ast.Subscript):
        return eval_subscript(node, consts, file_path)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = eval_expr(node.left, consts, file_path)
        right = eval_expr(node.right, consts, file_path)
        # compile("owner.py" + ":label") names the same pinned file.
        if (left and right and left[0] in {"path", "string"} and right[0] == "string"
                and (right[1].startswith(":") or not looks_like_path(right[1]))):
            return left
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left = eval_expr(node.left, consts, file_path)
        right = eval_expr(node.right, consts, file_path)
        if not left or not right or right[0] not in {"string", "path"}:
            return None
        if left[0] not in {"string", "path"}:
            return None
        base = left[1] if left[0] == "path" or "/" in left[1] else left[1]
        if left[0] == "string":
            base = normalize_rel(left[1])
            if base is None and left[1] not in {"", "."}:
                return None
            base = "" if left[1] in {"", "."} else base
        joined = join_path(base or "", right[1])
        if joined is None:
            return None
        return ("path", joined)
    if isinstance(node, ast.Call):
        return eval_call(node, consts, file_path)
    return None


def eval_subscript(node: ast.Subscript, consts: dict, file_path: str):
    if not isinstance(node.value, ast.Attribute) or node.value.attr != "parents":
        return None
    base = eval_expr(node.value.value, consts, file_path)
    index = slice_value(node)
    if not base or base[0] != "path" or not isinstance(index, int) or not base[1]:
        return None
    parent = nth_parent(base[1], index)
    if parent is None:
        return None
    return ("path", parent)


def eval_call(node: ast.Call, consts: dict, file_path: str):
    name = dotted(node.func)
    if name == "Path" and node.args:
        arg = eval_expr(node.args[0], consts, file_path)
        if arg and arg[0] == "path":
            return arg
        if arg and arg[0] == "string":
            if isinstance(node.args[0], ast.Name) and node.args[0].id == "__file__":
                return ("path", file_path)
            norm = normalize_rel(arg[1])
            if norm is not None:
                return ("path", norm)
        return None
    if name == "str" and node.args:
        return eval_expr(node.args[0], consts, file_path)
    if name == "os.path.abspath" and node.args:
        arg = eval_expr(node.args[0], consts, file_path)
        if arg and arg[0] == "path":
            return arg
        return None
    if name == "os.path.dirname" and node.args:
        arg = eval_expr(node.args[0], consts, file_path)
        if arg and arg[0] == "path" and arg[1]:
            return ("path", parent_path(arg[1]))
        return None
    if name == "os.path.join" and node.args:
        base = None
        for arg_node in node.args:
            arg = eval_expr(arg_node, consts, file_path)
            if not arg or arg[0] not in {"path", "string"}:
                return None
            if base is None:
                if arg[0] == "path":
                    base = arg[1]
                else:
                    norm = normalize_rel(arg[1])
                    if norm is None:
                        return None
                    base = norm
            else:
                joined = join_path(base, arg[1])
                if joined is None:
                    return None
                base = joined
        return None if base is None else ("path", base)
    if isinstance(node.func, ast.Attribute):
        if node.func.attr == "resolve":
            return eval_expr(node.func.value, consts, file_path)
        if node.func.attr == "with_name" and node.args:
            base = eval_expr(node.func.value, consts, file_path)
            leaf = eval_expr(node.args[0], consts, file_path)
            if not base or not leaf or base[0] != "path" or not base[1] or leaf[0] != "string":
                return None
            joined = join_path(parent_path(base[1]), leaf[1])
            if joined is None:
                return None
            return ("path", joined)
    return None


def call_argument(node: ast.Call, index: int, keyword: str | None):
    if keyword:
        for item in node.keywords:
            if item.arg == keyword:
                return item.value
    if index < len(node.args):
        return node.args[index]
    return None


def loader_slot(node: ast.Call):
    name = dotted(node.func) or ""
    if name == "__import__" or name.endswith(".__import__"):
        return 0, None, "module"
    if name.endswith("import_module"):
        return 0, "name", "module"
    if name.endswith("spec_from_file_location"):
        return 1, "path", "path"
    if name.endswith("run_path"):
        return 0, "path", "path"
    if name == "compile":
        return 1, "filename", "filename"
    if name == "open":
        return 0, "file", "path"
    if isinstance(node.func, ast.Attribute) and node.func.attr in {"read_text", "read_bytes"}:
        return None, None, "read"
    if name in {"exec", "eval"}:
        return 0, None, "exec"
    return None


def module_candidates(module: str, importer: str) -> list[str]:
    parts = [part for part in module.split(".") if part]
    if not parts:
        return []
    rel = "/".join(parts)
    parent = parent_path(importer)
    prefixes = ["", parent] if parent else [""]
    found = []
    for prefix in prefixes:
        base = rel if prefix == "" else f"{prefix}/{rel}"
        found.append(f"{base}.py")
        found.append(f"{base}/__init__.py")
    return found


def relative_candidates(level: int, module: str | None, names: list[str], importer: str) -> list[str]:
    path = PurePosixPath(importer)
    for _ in range(level):
        path = path.parent
    base = "" if path.as_posix() == "." else path.as_posix()
    modules = []
    if module:
        modules.append(module)
    else:
        modules.extend(names)
    found = []
    for name in modules:
        if not name or name == "*":
            continue
        rel = "/".join(part for part in name.split(".") if part)
        prefix = rel if base == "" else f"{base}/{rel}"
        found.append(f"{prefix}.py")
        found.append(f"{prefix}/__init__.py")
    return found


def bind_constants(module: ast.Module, file_path: str) -> dict:
    counts: dict[str, int] = {}
    statements = []
    for stmt in module.body:
        target = None
        value = None
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            target = stmt.targets[0].id
            value = stmt.value
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.value is not None:
            target = stmt.target.id
            value = stmt.value
        if target is None:
            continue
        counts[target] = counts.get(target, 0) + 1
        statements.append((target, value))
    consts = {}
    for name, value in statements:
        if counts[name] != 1:
            continue
        evaluated = eval_expr(value, consts, file_path)
        if evaluated is not None:
            consts[name] = evaluated
    return consts


def add_record(records: list[dict], unknowns: list[dict], path: str, kind: str,
               pin_sha256: str | None = None, pin_commit: str | None = None) -> None:
    if not path or path.startswith("/") or ".." in PurePosixPath(path).parts:
        unknowns.append({"reason": "unresolved-pin", "detail": path or kind, "candidates": []})
        return
    item = {
        "path": path,
        "kind": kind,
        "pin_sha256": pin_sha256.lower() if pin_sha256 else None,
        "pin_commit": pin_commit.lower() if pin_commit else None,
    }
    if item not in records:
        records.append(item)


def path_from_value(value, file_path: str, tree: set[str], allow_missing: bool) -> str | None:
    """Repo-relative path. A missing slash-path may be a deleted input.

    A basename that is not in the tree is a cwd/temp name, not a tracked input.
    """
    if not value or value[0] not in {"path", "string"}:
        return None
    norm = value[1] if value[0] == "path" else normalize_rel(value[1])
    if not norm:
        return None
    if norm in tree:
        return norm
    if "/" not in norm:
        beside = join_path(parent_path(file_path), norm)
        if beside and beside in tree:
            return beside
        return None
    if allow_missing:
        return norm
    return None


def pin_fields(value):
    if not value or value[0] != "string":
        return None, None
    kind = classify_pin(value[1])
    if kind == "sha256":
        return value[1], None
    if kind == "commit":
        return None, value[1]
    return None, None


def dict_items(node: ast.Dict, consts: dict, file_path: str):
    items = []
    for key_node, value_node in zip(node.keys, node.values):
        if key_node is None:
            return None
        items.append((eval_expr(key_node, consts, file_path), eval_expr(value_node, consts, file_path)))
    return items


def dirs_joined_with(loop: ast.For, key: str, consts: dict, file_path: str) -> set[str]:
    found = set()
    for child in ast.walk(loop):
        if isinstance(child, ast.BinOp) and isinstance(child.op, ast.Div):
            if isinstance(child.right, ast.Name) and child.right.id == key:
                left = eval_expr(child.left, consts, file_path)
                if left and left[0] == "path":
                    found.add(left[1])
        if isinstance(child, ast.Call) and dotted(child.func) == "os.path.join":
            for index, arg in enumerate(child.args):
                if not (isinstance(arg, ast.Name) and arg.id == key and index > 0):
                    continue
                base = None
                ok = True
                for prev in child.args[:index]:
                    evaluated = eval_expr(prev, consts, file_path)
                    if not evaluated or evaluated[0] not in {"path", "string"}:
                        ok = False
                        break
                    piece = evaluated[1] if evaluated[0] == "path" else normalize_rel(evaluated[1])
                    if piece is None:
                        ok = False
                        break
                    base = piece if base is None else join_path(base, piece)
                    if base is None:
                        ok = False
                        break
                if ok and base is not None:
                    found.add(base)
    return found


def loop_directories(module: ast.AST, dict_name: str, consts: dict, file_path: str) -> set[str]:
    found = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.For):
            continue
        key = None
        if isinstance(node.iter, ast.Name) and node.iter.id == dict_name and isinstance(node.target, ast.Name):
            key = node.target.id
        elif isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Attribute):
            attr = node.iter.func.attr
            owner = node.iter.func.value
            if isinstance(owner, ast.Name) and owner.id == dict_name and attr in {"items", "keys"}:
                if attr == "keys" and isinstance(node.target, ast.Name):
                    key = node.target.id
                if attr == "items" and isinstance(node.target, ast.Tuple) and node.target.elts:
                    first = node.target.elts[0]
                    key = first.id if isinstance(first, ast.Name) else None
        if key:
            found.update(dirs_joined_with(node, key, consts, file_path))
    return found


def apply_basenames(basenames, directories, file_path: str, tree: set[str],
                    records: list[dict], unknowns: list[dict], *, strict: bool) -> None:
    if len(directories) > 1:
        if strict:
            unknowns.append({
                "reason": "unresolved-pin",
                "detail": "ambiguous-pin-directory",
                "candidates": sorted(directories),
            })
        return
    base = next(iter(directories)) if len(directories) == 1 else None
    for leaf, sha, commit in basenames:
        if base is not None:
            path = join_path(base, leaf)
        else:
            beside = join_path(parent_path(file_path), leaf)
            path = beside if beside in tree else leaf if leaf in tree else None
        if path is None:
            if strict:
                unknowns.append({"reason": "unresolved-pin", "detail": leaf, "candidates": []})
        elif base is not None or path in tree:
            add_record(records, unknowns, path, "pin", sha, commit)


def sequence_paths(node: ast.AST, consts: dict, file_path: str, tree: set[str]):
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    found = []
    for elt in node.elts:
        if isinstance(elt, ast.Dict):
            path_node = None
            sha = None
            commit = None
            for key, value in zip(elt.keys, elt.values):
                key_ev = eval_expr(key, consts, file_path) if key is not None else None
                if not key_ev or key_ev[0] != "string":
                    continue
                if key_ev[1] in {"path", "file", "input"}:
                    path_node = value
                if key_ev[1] in {"sha256", "pin_sha256"}:
                    sha, _commit = pin_fields(eval_expr(value, consts, file_path))
                if key_ev[1] in {"commit", "pin_commit"}:
                    _sha, commit = pin_fields(eval_expr(value, consts, file_path))
            path = path_from_value(eval_expr(path_node, consts, file_path), file_path, tree, True) if path_node else None
            found.append((path, sha, commit))
        else:
            path = path_from_value(eval_expr(elt, consts, file_path), file_path, tree, True)
            found.append((path, None, None))
    return found


def function_table(module: ast.AST) -> dict[str, list[ast.FunctionDef]]:
    found: dict[str, list[ast.FunctionDef]] = {}
    for node in ast.walk(module):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.setdefault(node.name, []).append(node)
    return found


def assignment_counts(fn: ast.AST) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in ast.walk(fn):
        target = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target = node.targets[0].id
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            target = node.target.id
        if target:
            counts[target] = counts.get(target, 0) + 1
    return counts


def function_locals(fn: ast.AST, consts: dict, file_path: str) -> dict:
    """Straight-line assignments that fold from module constants. Not branches."""
    counts = assignment_counts(fn)
    local = {}
    for stmt in fn.body:
        target = None
        value = None
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            target = stmt.targets[0].id
            value = stmt.value
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.value is not None:
            target = stmt.target.id
            value = stmt.value
        if target is None or counts.get(target) != 1:
            continue
        evaluated = eval_expr(value, {**consts, **local}, file_path)
        if evaluated is not None:
            local[target] = evaluated
    return local


def direct_assignments(fn: ast.AST) -> dict[str, ast.AST]:
    counts = assignment_counts(fn)
    found = {}
    for stmt in fn.body:
        target = None
        value = None
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            target = stmt.targets[0].id
            value = stmt.value
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.value is not None:
            target = stmt.target.id
            value = stmt.value
        if target and value is not None and counts.get(target) == 1:
            found[target] = value
    return found


def names_in(node: ast.AST | None) -> set[str]:
    if node is None:
        return set()
    return {item.id for item in ast.walk(node) if isinstance(item, ast.Name)}


def data_names(node: ast.AST | None) -> set[str]:
    """Names used as data. A callee such as ``str`` or ``Path`` is not data."""
    found: set[str] = set()
    if node is None:
        return found

    def walk(item: ast.AST) -> None:
        if isinstance(item, ast.Call):
            if not isinstance(item.func, ast.Name):
                walk(item.func)
            for arg in item.args:
                walk(arg)
            for keyword in item.keywords:
                if keyword.value is not None:
                    walk(keyword.value)
            return
        if isinstance(item, ast.Name):
            found.add(item.id)
            return
        for child in ast.iter_child_nodes(item):
            walk(child)

    walk(node)
    return found


def parameter_names(fn: ast.AST) -> list[str]:
    args = fn.args
    return [item.arg for item in [*args.posonlyargs, *args.args, *args.kwonlyargs]]


def referenced_names(expr: ast.AST | None, scope: dict, params: set[str],
                     assigns: dict[str, ast.AST]) -> tuple[set[str], set[str]]:
    """Parameter names a loader still needs, after straight local assignments."""
    params_hit: set[str] = set()
    unknown_names: set[str] = set()
    if expr is None:
        return params_hit, unknown_names
    pending = list(data_names(expr))
    seen: set[str] = set()
    while pending:
        name = pending.pop()
        if name in seen or name in {"True", "False", "None"}:
            continue
        seen.add(name)
        if name in scope:
            continue
        if name in params:
            params_hit.add(name)
            continue
        assigned = assigns.get(name)
        if assigned is not None:
            pending.extend(data_names(assigned))
            continue
        unknown_names.add(name)
    return params_hit, unknown_names


def _joins_loop_key(value: ast.AST, key: str, scope: dict, file_path: str) -> bool:
    if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Div):
        if isinstance(value.right, ast.Name) and value.right.id == key:
            left = eval_expr(value.left, scope, file_path)
            return bool(left and left[0] == "path")
    if isinstance(value, ast.Call) and dotted(value.func) == "os.path.join":
        for index, arg in enumerate(value.args):
            if not (isinstance(arg, ast.Name) and arg.id == key and index > 0):
                continue
            ok = True
            for prev in value.args[:index]:
                evaluated = eval_expr(prev, scope, file_path)
                if not evaluated or evaluated[0] not in {"path", "string"}:
                    ok = False
                    break
            if ok:
                return True
    return False


def covered_loop_names(module: ast.AST, map_names: set[str], scope: dict, file_path: str) -> set[str]:
    """Names assigned as `path = DIR / key` inside a pin-map loop.

    The map already records those files. A later `path.read_bytes()` is the
    same input, not a second unresolved loader.
    """
    covered: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.For):
            continue
        key = None
        if isinstance(node.iter, ast.Name) and node.iter.id in map_names and isinstance(node.target, ast.Name):
            key = node.target.id
        elif isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Attribute):
            attr = node.iter.func.attr
            owner = node.iter.func.value
            if isinstance(owner, ast.Name) and owner.id in map_names and attr in {"items", "keys"}:
                if attr == "keys" and isinstance(node.target, ast.Name):
                    key = node.target.id
                if attr == "items" and isinstance(node.target, ast.Tuple) and node.target.elts:
                    first = node.target.elts[0]
                    key = first.id if isinstance(first, ast.Name) else None
        if not key:
            continue
        for child in ast.walk(node):
            target = None
            value = None
            if isinstance(child, ast.Assign) and len(child.targets) == 1 and isinstance(child.targets[0], ast.Name):
                target = child.targets[0].id
                value = child.value
            elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name) and child.value is not None:
                target = child.target.id
                value = child.value
            if target and value is not None and _joins_loop_key(value, key, scope, file_path):
                covered.add(target)
    return covered


def record_loaded(value, mode: str, file_path: str, tree: set[str], external: set[str],
                  records: list[dict], unknowns: list[dict]) -> None:
    if mode == "module":
        if not value or value[0] != "string":
            unknowns.append({"reason": "dynamic-import", "detail": "module", "candidates": []})
            return
        root_name = value[1].split(".", 1)[0]
        candidates = module_candidates(value[1], file_path)
        chosen = next((item for item in candidates if item in tree), None)
        if chosen:
            add_record(records, unknowns, chosen, "import")
        elif root_name in external:
            return
        else:
            unknowns.append({"reason": "dynamic-import", "detail": value[1], "candidates": candidates})
        return
    if mode == "filename" and value and value[0] == "string" and not looks_like_path(value[1]):
        return
    # A constant cwd/temp basename is not a tracked repository input.
    if (value is not None and value[0] in {"path", "string"} and "/" not in value[1]
            and value[1] not in tree and path_from_value(value, file_path, tree, False) is None):
        return
    path = path_from_value(value, file_path, tree, allow_missing=True)
    if path is None:
        if value is None:
            unknowns.append({"reason": "dynamic-import", "detail": mode, "candidates": []})
        return
    add_record(records, unknowns, path, "import" if mode != "read" else "read")


def extract(source: str, file_path: str, tree: set[str], external: set[str]) -> dict:
    module = ast.parse(source, filename=file_path)
    consts = bind_constants(module, file_path)
    records: list[dict] = []
    unknowns: list[dict] = []
    pending_basenames = []
    for stmt in module.body:
        target = None
        value = None
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            target = stmt.targets[0].id
            value = stmt.value
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            target = stmt.target.id
            value = stmt.value
        if target is None or value is None:
            continue
        if target in LIST_KINDS and isinstance(value, (ast.List, ast.Tuple)):
            for path, sha, commit in sequence_paths(value, consts, file_path, tree) or []:
                if path is None:
                    unknowns.append({"reason": "unresolved-pin", "detail": target, "candidates": []})
                else:
                    add_record(records, unknowns, path, LIST_KINDS[target], sha, commit)
        if isinstance(value, ast.Dict) and (target in PIN_MAPS or target in LIST_KINDS or target.endswith("_SHA256")):
            items = dict_items(value, consts, file_path)
            basenames = []
            if items is None:
                unknowns.append({"reason": "unresolved-pin", "detail": target, "candidates": []})
            else:
                for key, item_value in items:
                    sha, commit = pin_fields(item_value)
                    # A slash-free filename is joined with the directory used by
                    # `for name in MAP` / `DIR / name`, not guessed beside this file.
                    if key and key[0] == "string" and "/" not in key[1] and looks_like_path(key[1]):
                        basenames.append((key[1], sha, commit))
                        continue
                    path = path_from_value(key, file_path, tree, allow_missing=True)
                    if path:
                        kind = "pin" if target not in LIST_KINDS else LIST_KINDS[target]
                        add_record(records, unknowns, path, kind, sha, commit)
                    else:
                        unknowns.append({"reason": "unresolved-pin", "detail": target, "candidates": []})
            if basenames:
                pending_basenames.append((target, basenames))
        if target.endswith("_SHA256") and target in consts and consts[target][0] == "string":
            sha, _commit = pin_fields(consts[target])
            if sha:
                prefix = target[: -len("_SHA256")]
                for cand in (prefix, f"{prefix}_RELATIVE", f"{prefix}_PATH"):
                    if cand in consts and consts[cand][0] == "path":
                        add_record(records, unknowns, consts[cand][1], "pin", sha, None)
                        break
    hash_maps = {}
    for stmt in module.body:
        target = None
        value = None
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            target = stmt.targets[0].id
            value = stmt.value
        if (target and isinstance(value, ast.Dict) and target not in PIN_MAPS
                and target not in LIST_KINDS and not target.endswith("_SHA256")):
            items = dict_items(value, consts, file_path)
            leaves = []
            if items and all(pin_fields(item_value)[0] for _key, item_value in items):
                for key, item_value in items:
                    sha, _commit = pin_fields(item_value)
                    if key and key[0] == "string" and "/" not in key[1] and looks_like_path(key[1]):
                        leaves.append((key[1], sha, None))
                    else:
                        leaves = []
                        break
            if leaves:
                hash_maps[target] = leaves
    scope_for_maps = dict(consts)
    for fn in [node for nodes in function_table(module).values() for node in nodes]:
        scope_for_maps.update(function_locals(fn, consts, file_path))
    for target, basenames in pending_basenames:
        directories = loop_directories(module, target, scope_for_maps, file_path)
        apply_basenames(basenames, directories, file_path, tree, records, unknowns, strict=True)
    for target, basenames in hash_maps.items():
        directories = loop_directories(module, target, scope_for_maps, file_path)
        apply_basenames(basenames, directories, file_path, tree, records, unknowns, strict=False)

    functions = function_table(module)
    meta = {}
    for fn in [node for nodes in functions.values() for node in nodes]:
        meta[id(fn)] = {
            "scope": {**consts, **function_locals(fn, consts, file_path)},
            "assigns": direct_assignments(fn),
            "params": parameter_names(fn),
            "positional": [item.arg for item in [*fn.args.posonlyargs, *fn.args.args]],
        }
    module_bound = set(consts)
    for stmt in module.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            module_bound.add(stmt.targets[0].id)
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            module_bound.add(stmt.target.id)
    covered = covered_loop_names(module, set(hash_maps) | {name for name, _items in pending_basenames}, scope_for_maps, file_path)
    deferred = []

    def scope_of(stack: list) -> dict:
        return meta[id(stack[-1])]["scope"] if stack else consts

    def note_unresolved(expr: ast.AST | None, mode: str, stack: list) -> None:
        if expr is not None and isinstance(expr, ast.Name) and expr.id in covered:
            return
        if stack:
            info = meta[id(stack[-1])]
            params = set(info["params"])
            hit, missing = referenced_names(expr, info["scope"], params, info["assigns"])
            if not missing and hit:
                deferred.append((stack[-1].name, expr, mode, hit))
                return
        unknowns.append({"reason": "dynamic-import", "detail": mode, "candidates": []})

    def visit(node: ast.AST, stack: list) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stack.append(node)
            for child in node.body:
                visit(child, stack)
            for child in node.decorator_list:
                visit(child, stack)
            stack.pop()
            return
        scope = scope_of(stack)
        if isinstance(node, ast.Import):
            for alias in node.names:
                chosen = next((item for item in module_candidates(alias.name, file_path) if item in tree), None)
                root_name = alias.name.split(".", 1)[0]
                if chosen:
                    add_record(records, unknowns, chosen, "import")
                elif root_name not in external:
                    unknowns.append({
                        "reason": "unresolved-import",
                        "detail": alias.name,
                        "candidates": module_candidates(alias.name, file_path),
                    })
        elif isinstance(node, ast.ImportFrom):
            names = [alias.name for alias in node.names]
            if node.level:
                candidates = relative_candidates(node.level, node.module, names, file_path)
            else:
                candidates = module_candidates(node.module or "", file_path)
            chosen = next((item for item in candidates if item in tree), None)
            root_name = (node.module or names[0]).split(".", 1)[0] if (node.module or names) else ""
            if chosen:
                add_record(records, unknowns, chosen, "import")
            elif node.level or root_name not in external:
                unknowns.append({
                    "reason": "unresolved-import",
                    "detail": node.module or ".",
                    "candidates": candidates,
                })
        elif isinstance(node, ast.Call):
            slot = loader_slot(node)
            if slot is not None:
                index, keyword, mode = slot
                if mode == "read":
                    expr = node.func.value
                    value = eval_expr(expr, scope, file_path)
                    if value is not None:
                        record_loaded(value, "read", file_path, tree, external, records, unknowns)
                    else:
                        note_unresolved(expr, "read", stack)
                elif mode == "exec":
                    arg = node.args[0] if node.args else None
                    compiled = isinstance(arg, ast.Call) and dotted(arg.func) == "compile"
                    if not compiled and not (arg is not None and names_in(arg) <= module_bound):
                        unknowns.append({"reason": "dynamic-import", "detail": "exec", "candidates": []})
                else:
                    arg = call_argument(node, index, keyword)
                    value = eval_expr(arg, scope, file_path) if arg is not None else None
                    if value is not None:
                        record_loaded(value, mode, file_path, tree, external, records, unknowns)
                    else:
                        note_unresolved(arg, mode, stack)
        for child in ast.iter_child_nodes(node):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and child in node.body:
                continue
            visit(child, stack)

    visit(module, [])
    call_sites: list[tuple[ast.Call, ast.AST | None]] = []

    def collect_calls(node: ast.AST, owner: ast.AST | None) -> None:
        current = node if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else owner
        if isinstance(node, ast.Call):
            call_sites.append((node, current))
        for child in ast.iter_child_nodes(node):
            collect_calls(child, current)

    collect_calls(module, None)

    def fold_in_function(expr: ast.AST | None, fn: ast.AST | None, depth: int,
                         stack: set[tuple[str, int]]) -> list | None:
        """Constant values of expr from fn's call sites. None means unresolved."""
        if expr is None or depth < 0:
            return None
        if fn is None:
            value = eval_expr(expr, consts, file_path)
            if value is None:
                value = eval_expr(expr, scope_for_maps, file_path)
            return [value] if value is not None else None
        token = (fn.name, id(expr))
        if token in stack:
            return None
        info = meta[id(fn)]
        direct = eval_expr(expr, info["scope"], file_path)
        if direct is not None:
            return [direct]
        hit, missing = referenced_names(expr, info["scope"], set(info["params"]), info["assigns"])
        if missing or not hit or len(functions.get(fn.name, [])) != 1:
            return None
        sites = [
            pair for pair in call_sites
            if isinstance(pair[0].func, ast.Name) and pair[0].func.id == fn.name
        ]
        if not sites:
            return []
        values = []
        nested_stack = stack | {token}
        for site, caller in sites:
            groups: dict[str, list] = {}
            failed = False
            for name in hit:
                index = info["positional"].index(name) if name in info["positional"] else 10**6
                arg = call_argument(site, index, name)
                nested = fold_in_function(arg, caller, depth - 1, nested_stack)
                if not nested:
                    failed = True
                    break
                groups[name] = nested
            if failed:
                return None
            multi = [name for name, items in groups.items() if len(items) != 1]
            if len(multi) > 1:
                return None
            count = len(groups[multi[0]]) if multi else 1
            for offset in range(count):
                extra = dict(info["scope"])
                for name, items in groups.items():
                    extra[name] = items[offset if name in multi else 0]
                pending = True
                guard = 0
                while pending and guard < 32:
                    pending = False
                    guard += 1
                    for name, assigned in info["assigns"].items():
                        if name in extra:
                            continue
                        evaluated = eval_expr(assigned, extra, file_path)
                        if evaluated is not None:
                            extra[name] = evaluated
                            pending = True
                loaded = eval_expr(expr, extra, file_path)
                if loaded is None:
                    return None
                values.append(loaded)
        return values

    for func_name, expr, mode, _params_hit in deferred:
        owners = functions.get(func_name, [])
        if len(owners) != 1:
            unknowns.append({"reason": "dynamic-import", "detail": func_name, "candidates": []})
            continue
        loaded_values = fold_in_function(expr, owners[0], 4, set())
        if loaded_values is None:
            unknowns.append({"reason": "dynamic-import", "detail": func_name, "candidates": []})
            continue
        for loaded in loaded_values:
            record_loaded(loaded, mode, file_path, tree, external, records, unknowns)
    deduped = []
    for item in records:
        if item["path"] != file_path and item not in deduped:
            deduped.append(item)
    unique_unknowns = []
    for item in unknowns:
        if item not in unique_unknowns:
            unique_unknowns.append(item)
    return {"inputs": deduped, "unknown": unique_unknowns}


def certificate_paths_at(tree: set[str]) -> list[str]:
    prefix = CERT_DIR + "/"
    return sorted(path for path in tree if path.startswith(prefix) and path.endswith(".py"))


def build_index(repo: Path, commit: str) -> dict:
    """Read blobs at commit. Does not touch the worktree or any receipt."""
    commit = resolve_commit(repo, commit)
    tree = tree_paths(repo, commit)
    external = external_roots(repo, commit)
    certificates = certificate_paths_at(tree)
    extracted = {}
    queue = list(certificates)
    seen = set()
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        raw = blob(repo, commit, path)
        if raw is None or not path.endswith(".py"):
            extracted[path] = {"inputs": [], "unknown": []}
            continue
        try:
            source = raw.decode("utf-8")
            extracted[path] = extract(source, path, tree, external)
        except (SyntaxError, UnicodeError):
            extracted[path] = {"inputs": [], "unknown": [{"reason": "unparsed", "detail": path, "candidates": []}]}
        for item in extracted[path]["inputs"]:
            if item["path"] not in seen:
                queue.append(item["path"])
    by_certificate = {}
    for cert in certificates:
        direct = extracted.get(cert, {"inputs": [], "unknown": []})
        transitive = []
        unknown = list(direct["unknown"])
        stack = [(item, cert) for item in direct["inputs"]]
        visited = {cert}
        while stack:
            item, owner = stack.pop()
            record = dict(item)
            record["declared_by"] = owner
            if record not in transitive:
                transitive.append(record)
            path = item["path"]
            if path in visited:
                continue
            visited.add(path)
            child = extracted.get(path)
            if not child:
                continue
            for reason in child["unknown"]:
                propagated = dict(reason)
                propagated["via"] = path
                unknown.append(propagated)
            for nested in child["inputs"]:
                stack.append((nested, path))
        by_certificate[cert] = {
            "direct": [dict(item, declared_by=cert) for item in direct["inputs"]],
            "transitive": transitive,
            "unknown": unknown,
        }
    return {
        "schema": SCHEMA,
        "commit": commit,
        "certificates": certificates,
        "by_certificate": by_certificate,
    }


def provenance_status(repo: Path, commit: str, item: dict) -> dict:
    path = item["path"]
    data = blob(repo, commit, path)
    actual = sha256_hex(data) if data is not None else None
    status = "unpinned"
    if data is None:
        status = "deleted-input"
    elif item.get("pin_sha256") and actual != item["pin_sha256"]:
        status = "sha-mismatch"
    elif item.get("pin_commit"):
        pinned = blob(repo, item["pin_commit"], path)
        if pinned is None:
            status = "deleted-input"
        elif pinned != data:
            status = "sha-mismatch"
        else:
            status = "match"
    elif item.get("pin_sha256"):
        status = "match"
    return {
        "path": path,
        "declared_by": item.get("declared_by"),
        "kind": item.get("kind"),
        "pin_sha256": item.get("pin_sha256"),
        "pin_commit": item.get("pin_commit"),
        "actual_sha256": actual,
        "status": status,
    }


def select(repo: Path, commit: str, base: str | None) -> dict:
    """Conservative consumer selection. Does not execute certificates."""
    repo = Path(repo)
    commit = resolve_commit(repo, commit)
    base_commit = resolve_commit(repo, base) if base is not None else None
    index = build_index(repo, commit)
    changed = changed_paths(repo, base_commit, commit) if base_commit is not None else []
    changed_set = set(changed)
    tree = tree_paths(repo, commit)
    selected = []
    provenance = []
    for cert in index["certificates"]:
        info = index["by_certificate"][cert]
        reasons = []
        if base_commit is None:
            reasons.append("full-snapshot")
        elif cert in changed_set:
            reasons.append("changed-entrypoint")
        inputs = info["transitive"]
        if any(item["path"] in changed_set for item in inputs):
            reasons.append("changed-input")
        unknown_hit = False
        for reason in info["unknown"]:
            unknown_hit = True
            candidates = reason.get("candidates") or []
            if any(candidate in changed_set and candidate not in tree for candidate in candidates):
                if "deleted-input" not in reasons:
                    reasons.append("deleted-input")
        if unknown_hit and "unknown-dependency" not in reasons:
            reasons.append("unknown-dependency")
        rows = []
        for item in inputs:
            row = provenance_status(repo, commit, item)
            row["certificate"] = cert
            rows.append(row)
            if row["status"] == "deleted-input" and "deleted-input" not in reasons:
                reasons.append("deleted-input")
            if row["status"] == "sha-mismatch" and "sha-mismatch" not in reasons:
                reasons.append("sha-mismatch")
        provenance.extend(rows)
        if reasons:
            selected.append({
                "certificate": cert,
                "reasons": reasons,
                "unknown": info["unknown"],
                "inputs": inputs,
            })
    selected_paths = {item["certificate"] for item in selected}
    import run_research_certs as runner
    runner_paths = set(runner.select_certificates(repo, commit, base_commit))
    missing = sorted(runner_paths - selected_paths)
    if missing:
        raise RuntimeError("selector weakened existing certificate diff: " + ", ".join(missing))
    failures = [row for row in provenance if row["status"] in {"deleted-input", "sha-mismatch"}]
    return {
        "schema": SCHEMA,
        "commit": commit,
        "base": base_commit,
        "changed": changed,
        "selected": selected,
        "unselected": [cert for cert in index["certificates"] if cert not in selected_paths],
        "provenance": provenance,
        "provenance_ok": not failures,
        "superset_of_runner": True,
        "ran": False,
        "scientific_replay": False,
    }


def certificate_paths(repo: Path, commit: str, base: str | None) -> list[str]:
    """Sorted selected entrypoints. This is the unapplied runner hook."""
    return [item["certificate"] for item in select(repo, commit, base)["selected"]]


def workflow_replay(job: dict) -> dict:
    """Job SUCCESS does not count when the scientific step did not succeed."""
    conclusion = job.get("conclusion") if isinstance(job, dict) else None
    steps = job.get("steps") if isinstance(job, dict) else None
    if not isinstance(steps, list):
        steps = []
    matched = [step for step in steps if isinstance(step, dict) and step.get("name") == SCIENTIFIC_STEP]
    step = matched[0] if len(matched) == 1 else None
    step_conclusion = None if step is None else step.get("conclusion")
    replay = (
        conclusion == "success"
        and step is not None
        and step.get("status") == "completed"
        and step_conclusion == "success"
    )
    if conclusion == "success" and not replay:
        reason = "workflow SUCCESS skipped scientific step"
    elif replay:
        reason = "scientific step completed successfully"
    else:
        reason = "scientific step did not succeed"
    return {
        "replay": replay,
        "reason": reason,
        "job_conclusion": conclusion,
        "step_conclusion": step_conclusion,
    }


def scientific_replay(execution: list[dict] | None, workflow: dict | None = None, *, ran: bool = False) -> bool:
    if workflow is not None and not workflow_replay(workflow)["replay"]:
        return False
    if not ran or execution is None:
        return False
    return all(item.get("status") == "PASS" for item in execution)


def write_exclusive(path: Path, text: str) -> None:
    """Create a new receipt. Refuse to rewrite an existing one."""
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


def execute_isolated(repo: Path, commit: str, certificates: list[str], log_dir: Path,
                     preserve: list[Path] | None = None) -> dict:
    """Run already selected certificates. Selection itself performs no execution."""
    repo = Path(repo)
    log_dir = Path(log_dir)
    commit = resolve_commit(repo, commit)
    if log_dir.exists():
        raise FileExistsError(f"refusing to reuse execution directory {log_dir}")
    preserved = [(path, path.read_bytes()) for path in (preserve or [])]
    import run_research_certs as runner
    log_dir.mkdir(parents=True)
    results = []
    try:
        for cert in certificates:
            results.append(runner.run_certificate(repo, commit, cert, log_dir))
    finally:
        for path, prior in preserved:
            if path.read_bytes() != prior:
                raise RuntimeError(f"historical receipt changed: {path}")
    payload = {
        "schema": SCHEMA,
        "commit": commit,
        "execution": results,
        "ran": True,
        "scientific_replay": scientific_replay(results, ran=True),
    }
    write_exclusive(log_dir / "execution.json", json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def close_inputs(repo: Path, commit: str, base: str | None, log_dir: Path | None = None,
                 workflow: dict | None = None, preserve: list[Path] | None = None) -> dict:
    selection = select(repo, commit, base)
    execution = None
    ran = False
    if log_dir is not None:
        execution = execute_isolated(
            repo, selection["commit"],
            [item["certificate"] for item in selection["selected"]],
            log_dir, preserve)
        ran = True
    report = {
        "schema": SCHEMA,
        "selection": selection,
        "execution": None if execution is None else execution["execution"],
        "ran": ran,
        "workflow": None if workflow is None else workflow_replay(workflow),
        "scientific_replay": scientific_replay(
            None if execution is None else execution["execution"], workflow, ran=ran),
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--base", default=None)
    parser.add_argument("--report", type=Path, help="new report path; existing files are left untouched")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--log-dir", type=Path)
    args = parser.parse_args(argv)
    if args.execute and args.log_dir is None:
        parser.error("--execute requires a new --log-dir")
    try:
        report = close_inputs(
            args.repo, args.ref, args.base,
            args.log_dir if args.execute else None)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Research input closure error: {error}", file=sys.stderr)
        return 1
    if args.report is not None:
        try:
            write_exclusive(args.report, json.dumps(report, indent=2, sort_keys=True) + "\n")
        except FileExistsError:
            print(f"refusing to rewrite existing receipt {args.report}", file=sys.stderr)
            return 1
    selection = report["selection"]
    print(f"commit={selection['commit']}")
    print(f"base={selection['base'] or ''}")
    print(f"selected={len(selection['selected'])}")
    print(f"provenance_ok={str(selection['provenance_ok']).lower()}")
    print(f"scientific_replay={str(report['scientific_replay']).lower()}")
    for item in selection["selected"]:
        print(f"{item['certificate']} {' '.join(item['reasons'])}")
    if not selection["provenance_ok"] or (report["ran"] and not report["scientific_replay"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
