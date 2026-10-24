#!/usr/bin/env python3
"""Extract actual Lean declaration metadata from the compiled D0.All environment."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import re
import subprocess
import tempfile
from typing import Any

import lean_task_build

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORMAL = ROOT / "03_FORMALIZATION"
CLAIMS = ROOT / "02_REGISTRY" / "claims.csv"
PREFIX = "D0_DECLARATION_JSON="
COLLECTOR_BATCH_SIZE = 128


def name_expr(full_name: str) -> str:
    """Build a Lean Name from string components without source interpolation."""
    parts = full_name.split(".")
    if not parts or any(not part for part in parts):
        raise ValueError(f"invalid dotted Lean name: {full_name!r}")
    expr = "Lean.Name.anonymous"
    for part in parts:
        expr = f"Lean.Name.str ({expr}) {json.dumps(part, ensure_ascii=False)}"
    return expr


def name_batches(names: list[str], batch_size: int = COLLECTOR_BATCH_SIZE) -> list[list[str]]:
    if batch_size <= 0:
        raise ValueError("collector batch size must be positive")
    return [names[start:start + batch_size] for start in range(0, len(names), batch_size)]


def validate_collector_records(names: list[str], records: list[dict[str, Any]]) -> None:
    if len(records) != len(names):
        raise RuntimeError(
            f"Lean collector returned {len(records)} rows for {len(names)} requests"
        )
    for index, (requested, row) in enumerate(zip(names, records)):
        returned = row.get("name")
        if returned != requested:
            raise RuntimeError(
                f"Lean collector name mismatch at row {index}: "
                f"requested {requested!r}, returned {returned!r}"
            )


def candidate_names(module: str, atom: str) -> list[str]:
    """Return plausible exact names; the elaborated environment resolves them."""
    names = []
    if atom.startswith("D0."):
        names.append(atom)
    else:
        modules = list(dict.fromkeys(part.strip() for part in module.split(";") if part.strip()))
        for module_name in modules:
            names.append(f"{module_name}.{atom}")
        # A Lean source module can declare into a parent namespace, as is common
        # when several files contribute to one namespace. Keep those candidates
        # explicit and let the elaborated environment resolve exact names.
        for module_name in modules:
            parts = module_name.split(".")
            for end in range(len(parts) - 1, 1, -1):
                names.append(f"{'.'.join(parts[:end])}.{atom}")
        names.append(f"D0.{atom}")
        if not modules:
            names.append(atom)
    return list(dict.fromkeys(names))


def claim_requests(claim_id: str) -> tuple[dict[str, Any], list[str]]:
    with CLAIMS.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    matches = [row for row in rows if row["claim_id"] == claim_id]
    if len(matches) != 1:
        raise ValueError(f"expected one claim row for {claim_id}, found {len(matches)}")
    mapping, names = _claim_row_request(matches[0])
    return {"claim_id": claim_id, "mappings": mapping}, names


def _claim_row_request(row: dict[str, str]) -> tuple[list[dict[str, Any]], list[str]]:
    module = row.get("lean_module", "").strip()
    mapping = []
    names: list[str] = []
    for atom in filter(None, (part.strip() for part in row.get("lean_theorem", "").split(";"))):
        candidates = candidate_names(module, atom)
        names.extend(candidates)
        mapping.append({"claim_id": row.get("claim_id", ""), "module_locator": module, "theorem_atom": atom,
                        "candidate_names": candidates})
    if not mapping:
        mapping.append({"claim_id": row.get("claim_id", ""), "module_locator": module,
                        "theorem_atom": None, "candidate_names": []})
    return mapping, list(dict.fromkeys(names))


def all_claim_requests(rows: list[dict[str, str]] | None = None) -> tuple[dict[str, Any], list[str]]:
    """Resolve every current claims.csv locator without assigning semantic coverage."""
    if rows is None:
        with CLAIMS.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
    mappings: list[dict[str, Any]] = []
    names: list[str] = []
    for row in rows:
        row_mappings, row_names = _claim_row_request(row)
        mappings.extend(row_mappings)
        names.extend(row_names)
    return {"claim_rows": len(rows), "mappings": mappings}, list(dict.fromkeys(names))


def module_source_path(module_name: str | None) -> str | None:
    if not module_name:
        return None
    rel = pathlib.Path(*module_name.split(".")).with_suffix(".lean")
    roots = [FORMAL]
    package_root = FORMAL / ".lake" / "packages"
    if package_root.is_dir():
        roots.extend(p for p in package_root.iterdir() if p.is_dir())
    for root in roots:
        source = root / rel
        if source.is_file():
            try:
                return source.relative_to(ROOT).as_posix()
            except ValueError:
                return str(source.resolve())
    return None


def lean_collector(names: list[str], import_root: str, resolution_only: bool = False) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*", import_root):
        raise ValueError(f"invalid Lean import root: {import_root!r}")
    if resolution_only:
        declaration_lines = [
            "        let owner ← findModuleOf? target",
            "        pure <| Json.mkObj [",
            '          ("name", toJson target.toString),',
            '          ("exists", toJson true),',
            '          ("module", toJson (owner.map Name.toString))',
            "        ]",
        ]
    else:
        declaration_lines = [
            "        let typeText ← liftTermElabM do",
            "          let fmt ← PrettyPrinter.ppExpr info.type",
            "          pure fmt.pretty",
            "        let (binders, conclusionWhnf) ← liftTermElabM <| forallTelescope info.type fun xs target => do",
            "          let binders ← xs.mapM fun fvar => do",
            "            let localDecl ← getFVarLocalDecl fvar",
            "            let binderTypeExpr ← withTransparency .default (whnf localDecl.type)",
            "            let binderType ← PrettyPrinter.ppExpr binderTypeExpr",
            "            let isProposition ← Meta.isProp localDecl.type",
            "            pure <| Json.mkObj [",
            '              ("name", toJson localDecl.userName.toString),',
            '              ("binder_info", toJson (reprStr (LocalDecl.binderInfoEx localDecl))),',
            '              ("type", toJson binderType.pretty),',
            '              ("is_proposition", toJson isProposition)',
            "            ]",
            "          let targetExpr ← withTransparency .default (whnf target)",
            "          let targetFormat ← PrettyPrinter.ppExpr targetExpr",
            "          pure (binders, targetFormat.pretty)",
            "        let typeDependencies := info.type.getUsedConstantsAsSet.toList.map Name.toString",
            "        let proofDependencies := match info.value? (allowOpaque := true) with",
            "          | none => []",
            "          | some value => value.getUsedConstantsAsSet.toList.map Name.toString",
            "        let owner ← findModuleOf? target",
            "        let declarationKind := match info with",
            '          | .axiomInfo _ => "axiom"',
            '          | .defnInfo _ => "definition"',
            '          | .thmInfo _ => "theorem"',
            '          | .opaqueInfo _ => "opaque"',
            '          | .quotInfo _ => "quotient"',
            '          | .inductInfo _ => "inductive"',
            '          | .ctorInfo _ => "constructor"',
            '          | .recInfo _ => "recursor"',
            "        let ranges ← findDeclarationRanges? target",
            "        let axioms ← collectAxioms target",
            "        let rangeJson := match ranges with",
            "          | none => Json.null",
            "          | some rs => Json.mkObj [",
            '              ("declaration", d0RangeJson rs.range),',
            '              ("selection", d0RangeJson rs.selectionRange)',
            "            ]",
            "        pure <| Json.mkObj [",
            '          ("name", toJson target.toString),',
            '          ("exists", toJson true),',
            '          ("elaborated_type", toJson typeText),',
            '          ("binders", toJson binders),',
            '          ("conclusion_whnf", toJson conclusionWhnf),',
            '          ("type_dependencies", toJson typeDependencies),',
            '          ("proof_dependencies", toJson proofDependencies),',
            '          ("axioms", toJson (axioms.toList.map Name.toString)),',
            '          ("declaration_kind", toJson declarationKind),',
            '          ("internal_name", toJson target.isInternal),',
            '          ("module", toJson (owner.map Name.toString)),',
            '          ("declaration_ranges", rangeJson)',
            "        ]",
        ]
    declaration_payload = "\n".join(declaration_lines)
    commands = []
    for batch in name_batches(names):
        targets = ",\n    ".join(name_expr(name) for name in batch)
        commands.append(f'''run_cmd do
  let targets : Array Name := #[
    {targets}
  ]
  let env ← getEnv
  for target in targets do
    let payload ← match env.find? target with
      | none => pure <| Json.mkObj [
          ("name", toJson target.toString), ("exists", toJson false)
        ]
      | some info => do
{declaration_payload}
    liftIO <| IO.println s!"{PREFIX}{{payload.compress}}"
''')
    return f'''import Lean
import {import_root}

open Lean Meta Elab Command

def d0PositionJson (p : Position) : Json := Json.mkObj [
  ("line", toJson p.line), ("column", toJson p.column)
]

def d0RangeJson (r : DeclarationRange) : Json := Json.mkObj [
  ("start", d0PositionJson r.pos), ("end", d0PositionJson r.endPos)
]

{''.join(commands)}
'''


def run_inventory(names: list[str], import_root: str, resolution_only: bool = False) -> tuple[list[dict[str, Any]], str, str]:
    if not names:
        raise ValueError("no declaration names were requested")
    with tempfile.TemporaryDirectory(prefix="d0-lean-inventory-") as directory:
        script = pathlib.Path(directory) / "Collect.lean"
        script_text = lean_collector(names, import_root, resolution_only)
        script_bytes = script_text.encode("utf-8")
        script_sha256 = hashlib.sha256(script_bytes).hexdigest()
        script.write_bytes(script_bytes)
        try:
            with lean_task_build.build_lock(lean_task_build.LOCK):
                source_digest_before_build = lean_task_build.source_digest()
                build = subprocess.run(
                    ["lake", "build", import_root], cwd=FORMAL,
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                )
                source_digest_after_build = lean_task_build.source_digest()
                if build.returncode:
                    raise RuntimeError(
                        f"Lean import root is not current/buildable ({build.returncode}):\n"
                        f"{build.stderr}\n{build.stdout}"
                    )
                if source_digest_before_build != source_digest_after_build:
                    raise RuntimeError(
                        "Lean sources changed while the import root was being built; "
                        "discard this result and rerun."
                    )
                proc = subprocess.run(
                    ["lake", "env", "lean", str(script)], cwd=FORMAL,
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                )
                source_digest_after = lean_task_build.source_digest()
        except lean_task_build.BuildLockBusy as exc:
            raise RuntimeError(
                "D0 Lean build/cache is busy; retry declaration extraction after it finishes."
            ) from exc
    if source_digest_after_build != source_digest_after:
        raise RuntimeError(
            "Lean sources changed during declaration extraction; discard this result and rerun."
        )
    if proc.returncode:
        raise RuntimeError(f"Lean collector failed ({proc.returncode}):\n{proc.stderr}\n{proc.stdout}")
    records = []
    for line in proc.stdout.splitlines():
        if line.startswith(PREFIX):
            records.append(json.loads(line[len(PREFIX):]))
    try:
        validate_collector_records(names, records)
    except RuntimeError as exc:
        raise RuntimeError(f"{exc}; stdout was:\n{proc.stdout}\nstderr was:\n{proc.stderr}") from exc
    for row in records:
        for key in ("type_dependencies", "proof_dependencies", "axioms"):
            if isinstance(row.get(key), list):
                row[key] = sorted(row[key])
    return records, script_sha256, source_digest_after_build


def lean_module_collector(modules: list[str], import_root: str,
                          module_prefix: str | None = None,
                          include_proof_details: bool = True) -> str:
    """Enumerate declarations owned by selected modules in a compiled import."""
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*", import_root):
        raise ValueError(f"invalid Lean import root: {import_root!r}")
    if module_prefix is None and not modules:
        raise ValueError("select at least one owning module or a module prefix")
    if module_prefix is not None and not re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*\.?", module_prefix):
        raise ValueError(f"invalid Lean module prefix: {module_prefix!r}")
    for module in modules:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*", module):
            raise ValueError(f"invalid Lean module name: {module!r}")
    owner_names = ",\n    ".join(name_expr(module) for module in modules)
    owner_clause = (f"  let ownerModules : Array Name := #[\n    {owner_names}\n  ]\n"
                    if module_prefix is None else "")
    if module_prefix is None:
        owner_test = "ownerModules.contains owner"
    else:
        prefix_expr = json.dumps(module_prefix, ensure_ascii=False)
        owner_test = f'owner.toString.startsWith {prefix_expr}'
    if include_proof_details:
        proof_details = '''          let proofDependenciesJson := toJson <| match info.value? (allowOpaque := true) with
            | none => []
            | some value => value.getUsedConstantsAsSet.toList.map Name.toString
          let axioms ← collectAxioms target
          let axiomsJson := toJson (axioms.toList.map Name.toString)
          let proofDetailsStatus := "collected"
'''
    else:
        proof_details = '''          let proofDependenciesJson := Json.null
          let axiomsJson := Json.null
          let proofDetailsStatus := "omitted_by_bulk_mode"
'''
    return f'''import Lean
import {import_root}

open Lean Meta Elab Command

def d0PositionJson (p : Position) : Json := Json.mkObj [
  ("line", toJson p.line), ("column", toJson p.column)
]

def d0RangeJson (r : DeclarationRange) : Json := Json.mkObj [
  ("start", d0PositionJson r.pos), ("end", d0PositionJson r.endPos)
]

run_cmd do
{owner_clause}  let env ← getEnv
  for h : moduleIdx in *...env.header.modules.size do
    let owner := env.header.modules[moduleIdx].module
    if {owner_test} then
      let moduleData := env.header.moduleData[moduleIdx]!
      for target in moduleData.constNames do
        match env.find? target with
        | none => pure ()
        | some info =>
          let typeText ← liftTermElabM do
            let fmt ← PrettyPrinter.ppExpr info.type
            pure fmt.pretty
          let (binders, conclusionWhnf) ← liftTermElabM <| forallTelescope info.type fun xs targetType => do
            let binders ← xs.mapM fun fvar => do
              let localDecl ← getFVarLocalDecl fvar
              let binderTypeExpr ← withTransparency .default (whnf localDecl.type)
              let binderType ← PrettyPrinter.ppExpr binderTypeExpr
              let isProposition ← Meta.isProp localDecl.type
              pure <| Json.mkObj [
                ("name", toJson localDecl.userName.toString),
                ("binder_info", toJson (reprStr (LocalDecl.binderInfoEx localDecl))),
                ("type", toJson binderType.pretty),
                ("is_proposition", toJson isProposition)
              ]
            let targetExpr ← withTransparency .default (whnf targetType)
            let targetFormat ← PrettyPrinter.ppExpr targetExpr
            pure (binders, targetFormat.pretty)
          let typeDependencies := info.type.getUsedConstantsAsSet.toList.map Name.toString
{proof_details}          let ranges ← findDeclarationRanges? target
          let declarationKind := match info with
            | .axiomInfo _ => "axiom"
            | .defnInfo _ => "definition"
            | .thmInfo _ => "theorem"
            | .opaqueInfo _ => "opaque"
            | .quotInfo _ => "quotient"
            | .inductInfo _ => "inductive"
            | .ctorInfo _ => "constructor"
            | .recInfo _ => "recursor"
          let rangeJson := match ranges with
            | none => Json.null
            | some rs => Json.mkObj [
                ("declaration", d0RangeJson rs.range),
                ("selection", d0RangeJson rs.selectionRange)
              ]
          let payload := Json.mkObj [
            ("name", toJson target.toString),
            ("exists", toJson true),
            ("elaborated_type", toJson typeText),
            ("binders", toJson binders),
            ("conclusion_whnf", toJson conclusionWhnf),
            ("type_dependencies", toJson typeDependencies),
            ("proof_dependencies", proofDependenciesJson),
            ("axioms", axiomsJson),
            ("proof_details_status", toJson proofDetailsStatus),
            ("declaration_kind", toJson declarationKind),
            ("internal_name", toJson target.isInternal),
            ("module", toJson owner.toString),
            ("declaration_ranges", rangeJson)
          ]
          liftIO <| IO.println s!"{PREFIX}{{payload.compress}}"
'''


def run_module_inventory(modules: list[str], import_root: str,
                         module_prefix: str | None = None,
                         include_proof_details: bool = True) -> tuple[list[dict[str, Any]], str, str]:
    """Build an import and enumerate its declarations by owning module."""
    if module_prefix is None and not modules:
        raise ValueError("select at least one owning module or a module prefix")
    script_text = lean_module_collector(
        modules, import_root, module_prefix, include_proof_details=include_proof_details
    )
    script_bytes = script_text.encode("utf-8")
    script_sha256 = hashlib.sha256(script_bytes).hexdigest()
    with tempfile.TemporaryDirectory(prefix="d0-lean-module-inventory-") as directory:
        script = pathlib.Path(directory) / "Collect.lean"
        script.write_bytes(script_bytes)
        try:
            with lean_task_build.build_lock(lean_task_build.LOCK):
                source_digest_before_build = lean_task_build.source_digest()
                build = subprocess.run(
                    ["lake", "build", import_root], cwd=FORMAL,
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                )
                source_digest_after_build = lean_task_build.source_digest()
                if build.returncode:
                    raise RuntimeError(
                        f"Lean import root is not current/buildable ({build.returncode}):\n"
                        f"{build.stderr}\n{build.stdout}"
                    )
                if source_digest_before_build != source_digest_after_build:
                    raise RuntimeError(
                        "Lean sources changed while the import root was being built; "
                        "discard this result and rerun."
                    )
                proc = subprocess.run(
                    ["lake", "env", "lean", str(script)], cwd=FORMAL,
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                )
                source_digest_after = lean_task_build.source_digest()
        except lean_task_build.BuildLockBusy as exc:
            raise RuntimeError(
                "D0 Lean build/cache is busy; retry declaration extraction after it finishes."
            ) from exc
    if source_digest_after_build != source_digest_after:
        raise RuntimeError(
            "Lean sources changed during declaration extraction; discard this result and rerun."
        )
    if proc.returncode:
        raise RuntimeError(f"Lean module collector failed ({proc.returncode}):\n{proc.stderr}\n{proc.stdout}")
    rows = []
    for line in proc.stdout.splitlines():
        if line.startswith(PREFIX):
            rows.append(json.loads(line[len(PREFIX):]))
    names = [str(row.get("name", "")) for row in rows]
    if any(not name for name in names) or len(names) != len(set(names)):
        raise RuntimeError("Lean module collector returned an empty or duplicate declaration name")
    allowed_modules = set(modules)
    for row in rows:
        owner = str(row.get("module", ""))
        if module_prefix is None and owner not in allowed_modules:
            raise RuntimeError(f"Lean module collector returned unexpected owner {owner!r}")
        if module_prefix is not None and not (
                owner == module_prefix.rstrip(".")
                or owner.startswith(module_prefix.rstrip(".") + ".")):
            raise RuntimeError(f"Lean module collector returned unexpected owner {owner!r}")
        row["source_path"] = module_source_path(owner)
        for key in ("type_dependencies", "proof_dependencies", "axioms"):
            if isinstance(row.get(key), list):
                row[key] = sorted(row[key])
    rows.sort(key=lambda row: str(row.get("name", "")))
    return rows, script_sha256, source_digest_after_build


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--name", help="exact full Lean declaration name")
    select.add_argument("--claim-id", help="resolve theorem-name candidates for one claims.csv row")
    select.add_argument("--all-claims", action="store_true",
                        help="resolve all theorem-name candidates in claims.csv")
    select.add_argument("--module", action="append", dest="modules",
                        help="enumerate every declaration owned by a module in the compiled import; repeatable")
    select.add_argument("--all-d0", action="store_true",
                        help="enumerate every declaration owned by a D0 module in the compiled import")
    parser.add_argument("--resolution-only", action="store_true",
                        help="return exact availability and owner module without signatures or proof dependencies")
    parser.add_argument("--omit-proof-details", action="store_true",
                        help="for module enumeration, skip proof-term dependencies and axiom closures")
    parser.add_argument("--output", type=pathlib.Path, help="write JSON to this path; default is stdout")
    parser.add_argument("--import-root", default="D0.All", help="compiled public Lean import (default: D0.All)")
    args = parser.parse_args()

    mapping = None
    if args.name:
        mapping = {"full_name": args.name}
        names = [args.name]
    elif args.claim_id:
        mapping, names = claim_requests(args.claim_id)
    elif args.modules or args.all_d0:
        modules = args.modules or []
        module_prefix = "D0." if args.all_d0 else None
        rows, collector_sha256, lean_source_digest = run_module_inventory(
            modules, args.import_root, module_prefix=module_prefix,
            include_proof_details=not args.omit_proof_details,
        )
        output = {
            "schema": "d0-lean-declaration-inventory-v1",
            "snapshot_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8"
            ).strip(),
            "worktree_dirty": bool(subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True, encoding="utf-8"
            ).strip()),
            "lean_source_digest": lean_source_digest,
            "collector_sha256": collector_sha256,
            "toolchain": (FORMAL / "lean-toolchain").read_text(encoding="utf-8").strip(),
            "public_import_root": args.import_root,
            "inventory_mode": "owning_module_enumeration",
            "requested_modules": modules,
            "module_prefix": module_prefix,
            "declarations": rows,
        }
        rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("w", encoding="utf-8", newline="\n") as inventory_file:
                inventory_file.write(rendered)
        else:
            print(rendered, end="")
        return 0
    else:
        mapping, names = all_claim_requests()
    rows, collector_sha256, lean_source_digest = run_inventory(names, args.import_root, args.resolution_only)
    for row in rows:
        row["source_path"] = module_source_path(row.get("module"))
    output = {
        "schema": "d0-lean-declaration-inventory-v1",
        "snapshot_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8"
        ).strip(),
        "worktree_dirty": bool(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True, encoding="utf-8"
        ).strip()),
        "claim_registry_sha256": (
            hashlib.sha256(CLAIMS.read_bytes()).hexdigest()
            if args.claim_id or args.all_claims else None
        ),
        "lean_source_digest": lean_source_digest,
        "collector_sha256": collector_sha256,
        "toolchain": (FORMAL / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "public_import_root": args.import_root,
        "resolution_only": args.resolution_only,
        "request": mapping,
        "declarations": rows,
    }
    rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
