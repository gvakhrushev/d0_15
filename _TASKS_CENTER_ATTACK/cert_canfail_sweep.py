#!/usr/bin/env python3
"""cert_canfail_sweep.py — Tier-0 can-fail audit of the 05_CERTS/vp_*.py corpus.

Motivation: at least one print-only stub slipped into the cert corpus (SPECTRAL-EINSTEIN
incident). This tool sweeps EVERY top-level 05_CERTS/vp_*.py and answers, per cert, the
only question that matters for a verification certificate: CAN THIS SCRIPT FAIL, i.e. is
there a designed, computation-dependent path to a non-zero exit code?

STATIC layer (AST-based, handles the four corpus failure idioms):
  A. `assert <computed>`                                        (plain asserts)
  B. `def die(msg): ... raise SystemExit(1)` + `if bad: die()`  (die-helper under a guard)
  C. `ok &= emit(...)` / `ok = ok and check(...)`  +  `return 0 if ok else N`
     wired through `raise SystemExit(main())` / `sys.exit(main())`  (accumulator + wiring)
  D. `sys.exit(0 if ok else 1)` / `sys.exit(1)`-under-if at module level (direct gate)

Per-cert metrics:
  - n_asserts, n_constant_asserts (assert on a literal/constant expression = cannot depend
    on computation = suspicious), n_computed_asserts
  - die-like helper functions and guarded call sites
  - conditional raises / conditional nonzero exits / wired-main conditional returns
  - FAKE-GATE detection: exit gate reads a name that is only ever assigned a constant
    (e.g. `ok = True` never updated -> `sys.exit(0 if ok else 1)` can never fail)
  - exit-code discipline (systemexit_main / module_gate / toplevel_checks / none)
  - PASS_/FAIL_ print counts; print-only smell (PASS prints with zero can-fail constructs)
  - negative-control signal: CONTROL_/REJECTED/negative-control/planted-flaw strings in
    code (module-docstring-only mentions are recorded but do NOT count), try/except
    AssertionError|SystemExit control idiom
  - reads_files / writes_files (repo-safety + mutation eligibility)

Classification:
  SOLID        can-fail construct(s) present AND executed negative-control signal in code
  WEAK         can-fail construct(s) present but no in-code negative control, or the
               controls are PRINTED-NOT-EXECUTED ("NEGATIVE_CONTROL_CAUGHT" emitted
               unconditionally on the success path with no control computation)
  STUB-SUSPECT zero designed can-fail constructs (print-only), or all asserts constant,
               or fake gate, or unparseable

Fall-through failure exits ARE recognized: `if ok: ...; return 0` / `sys.exit(0)`
followed by an unconditional `return 1` / `sys.exit(1)` is branch-dependent and counts
as a can-fail construct even though the nonzero exit is not nested under the If.

Cross-reference: 09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv `python_cert` column
(';'-separated); a suspect is LOAD-BEARING if any dependent claim has release_status in
{CERT-CLOSED, NO-GO, NO_GO_PROVED}.

DYNAMIC layer (--dynamic [--mutate]):
  - runs the top-N stub-suspects (load-bearing first) with a 60 s timeout, cwd=05_CERTS
  - SAFETY: certs that statically WRITE files are NOT executed (repo is not a git repo;
    running them would modify tracked outputs) — recorded as SKIPPED-WRITES
  - mutation probe (self-contained certs only, i.e. no file reads/writes): copy the cert
    to a scratch dir, flip ONE computed numeric constant (first int literal with |v|>=2
    outside print/f-string), rerun; a cert that still exits 0 is a confirmed
    MUTATION-SURVIVOR (its checks do not constrain its computation). Originals are never
    modified. File-reading certs are never mutation-tested (documented method limit).

Usage:
  python3 cert_canfail_sweep.py --repo /path/to/d0_15 --json out.json [--dynamic]
      [--mutate] [--top 15] [--scratch DIR] [--timeout 60]

Exit code: 0 on completed sweep (findings are data, not errors); 2 on usage/IO errors.
This auditor deliberately does NOT gate on its own findings — it is a measurement tool.
"""

import argparse
import ast
import csv
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# static analysis
# ---------------------------------------------------------------------------

EXIT_FUNCS = {"exit", "_exit", "quit"}  # sys.exit, os._exit, exit(), quit()

CONTROL_RE = re.compile(
    r"(NEGATIVE[_ ]?CONTROL"
    r"|negative[ _-]control"
    r"|\bCONTROL\b|CONTROL_|_CONTROL"
    r"|REJECT"          # REJECTED / REJECTS / FAIL_*_REJECTED
    r"|PLANTED|planted"
    r"|MUST[ _]FAIL|must fail"
    r"|MUTANT|mutant"
    r"|TAMPER|tamper"
    r"|COUNTEREXAMPLE|counter-example|counterexample"
    r"|INADMISSIBLE"
    r"|DECOY|decoy"
    r"|\bFLAW|planted[ _-]flaw"
    r")"
)

READ_CALL_NAMES = {"open", "loadtxt", "genfromtxt", "read_csv", "read_json", "read_table",
                   "urlopen", "urlretrieve"}
READ_ATTR_NAMES = {"read_text", "read_bytes", "load", "loadtxt", "genfromtxt", "read_csv",
                   "read_json", "read_table", "reader", "DictReader", "open", "urlopen",
                   "get", "post"}
# .load covers json.load / np.load / pickle.load / tomllib.load (all file-handle based);
# json.loads / np.loads are NOT matched (different attr name).
WRITE_ATTR_NAMES = {"write_text", "write_bytes", "to_csv", "to_json", "dump", "savetxt",
                    "save", "savez", "writerow", "writerows", "mkdir", "makedirs",
                    "replace", "rename", "unlink"}
# 'replace' also matches str.replace -> writes_files is a *safety-first* over-approx for
# the dynamic runner; over-flagging only means we skip a run, never that we break the repo.


def _parents(tree):
    par = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            par[child] = node
    return par


def _ancestors(node, par):
    cur = par.get(node)
    while cur is not None:
        yield cur
        cur = par.get(cur)


def _under(node, par, types):
    return any(isinstance(a, types) for a in _ancestors(node, par))


def _in_print(node, par):
    for a in _ancestors(node, par):
        if isinstance(a, ast.Call):
            f = a.func
            if isinstance(f, ast.Name) and f.id == "print":
                return True
            if isinstance(f, ast.Attribute) and f.attr in {"write", "format"}:
                return True
    return False


def _is_const(node):
    """Expression contains no Name/Call/Attribute/Subscript -> value fixed at parse time."""
    for n in ast.walk(node):
        if isinstance(n, (ast.Name, ast.Call, ast.Attribute, ast.Subscript)):
            return False
    return True


_NOT_CONST = object()  # sentinel: distinguishes "not a Constant node" from Constant(None)


def _const_value(node):
    return node.value if isinstance(node, ast.Constant) else _NOT_CONST


def _is_exit_call(call):
    """Call node is sys.exit(...) / os._exit(...) / exit(...) / quit(...)."""
    f = call.func
    if isinstance(f, ast.Name) and f.id in EXIT_FUNCS:
        return True
    if isinstance(f, ast.Attribute) and f.attr in EXIT_FUNCS:
        return True
    return False


def _exit_arg(call):
    return call.args[0] if call.args else None


def _systemexit_of(raise_node):
    """Return the SystemExit(...) Call/Name of a raise, else None."""
    exc = raise_node.exc
    if exc is None:
        return None
    if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) \
            and exc.func.id == "SystemExit":
        return exc
    if isinstance(exc, ast.Name) and exc.id == "SystemExit":
        return exc
    return None


def _die_like_functions(tree):
    """Functions whose body unconditionally raises / exits nonzero (die/fail helpers)."""
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for stmt in node.body:  # top level of the body only = unconditional
            if isinstance(stmt, ast.Raise):
                out.add(node.name)
                break
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call) \
                    and _is_exit_call(stmt.value):
                a = _exit_arg(stmt.value)
                if a is None or _const_value(a) not in (0, None):
                    out.add(node.name)
                    break
    return out


def _name_assignment_kinds(tree, par):
    """name -> kinds of assignments seen anywhere.

    kinds: 'const' (constant at top level), 'condconst' (constant assigned under a
    conditional — e.g. `if bad: ok = False` — which makes a gate LIVE), 'nonconst',
    'aug'. Also 'multiconst' when two different constants are assigned (True/False).
    """
    kinds = {}
    const_vals = {}

    def mark(name, kind):
        kinds.setdefault(name, set()).add(kind)

    def mark_const(name, node, value_node):
        if _under(node, par, COND_TYPES):
            mark(name, "condconst")
        else:
            mark(name, "const")
        if isinstance(value_node, ast.Constant):
            const_vals.setdefault(name, set()).add(repr(value_node.value))
            if len(const_vals[name]) > 1:
                mark(name, "multiconst")

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            const = _is_const(node.value)
            for t in node.targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name):
                        if const:
                            mark_const(n.id, node, node.value)
                        else:
                            mark(n.id, "nonconst")
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            if isinstance(node.target, ast.Name):
                if _is_const(node.value):
                    mark_const(node.target.id, node, node.value)
                else:
                    mark(node.target.id, "nonconst")
        elif isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Name):
                mark(node.target.id, "aug")
        elif isinstance(node, (ast.For, ast.comprehension)):
            tgt = node.target
            for n in ast.walk(tgt):
                if isinstance(n, ast.Name):
                    mark(n.id, "nonconst")
    return kinds


def _gate_is_live(expr, kinds):
    """True if the gate expression can actually vary at runtime.

    Constant -> dead. Name -> live only if it has a nonconst/aug assignment.
    IfExp/Compare/BoolOp/UnaryOp -> live if any contained Name is live, or if it
    contains a Call/Attribute/Subscript (runtime value).
    """
    if expr is None:
        return False
    if isinstance(expr, ast.Constant):
        return False
    names, has_runtime = [], False
    for n in ast.walk(expr):
        if isinstance(n, ast.Name):
            names.append(n.id)
        elif isinstance(n, (ast.Call, ast.Attribute, ast.Subscript)):
            has_runtime = True
    if has_runtime:
        return True
    for nm in names:
        k = kinds.get(nm, set())
        if k & {"nonconst", "aug", "condconst", "multiconst"}:
            return True
    return False  # only top-level single-constant names (or no names) -> fake gate


COND_TYPES = (ast.If, ast.IfExp, ast.While, ast.ExceptHandler)


def _nearest_if(node, par):
    for a in _ancestors(node, par):
        if isinstance(a, ast.If):
            return a
    return None


def _if_has_success_return(if_node):
    for n in ast.walk(if_node):
        if isinstance(n, ast.Return):
            if n.value is None:
                return True
            v = _const_value(n.value)
            if v is not _NOT_CONST and v in (0, None, False):
                return True
    return False


def analyze_static(path):
    # utf-8-sig: at least one cert ships with a BOM (vp_pdg_strict_passport.py);
    # plain utf-8 would misreport it as unparseable.
    src = path.read_text(encoding="utf-8-sig", errors="replace")
    res = {
        "cert": path.name,
        "loc": src.count("\n") + 1,
        "n_asserts": 0, "n_constant_asserts": 0, "n_computed_asserts": 0,
        "die_like_funcs": [], "n_guarded_die_calls": 0,
        "n_conditional_raises": 0, "n_conditional_exit_nonzero": 0,
        "n_gate_exits": 0, "n_wired_conditional_returns": 0,
        "fake_gates": [],
        "exit_discipline": "none",
        "n_pass_prints": 0, "n_fail_prints": 0,
        "control_in_code": False, "control_in_docstring": False,
        "control_idiom_tryexcept": False,
        "n_control_strings_code": 0, "n_control_success_prints": 0,
        "controls_unbacked": False,
        "reads_files": False, "writes_files": False,
        "can_fail_constructs": 0, "can_fail_reasons": [],
        "parse_error": None,
    }
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        res["parse_error"] = f"{e.__class__.__name__}: {e}"
        res["classification"] = "STUB-SUSPECT"
        res["class_reason"] = "unparseable"
        return res

    par = _parents(tree)
    kinds = _name_assignment_kinds(tree, par)
    die_funcs = _die_like_functions(tree)
    res["die_like_funcs"] = sorted(die_funcs)
    module_doc = ast.get_docstring(tree) or ""

    # ---- string scans (PASS/FAIL prints, negative-control signal) ----
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            s = node.value
            is_module_doc = (s == module_doc and isinstance(par.get(node), ast.Expr)
                             and par.get(par.get(node)) is tree)
            if re.search(r"PASS[_ ]", s):
                res["n_pass_prints"] += 1
            if re.search(r"FAIL[_ ]", s):
                res["n_fail_prints"] += 1
            if CONTROL_RE.search(s):
                if is_module_doc:
                    res["control_in_docstring"] = True
                else:
                    res["control_in_code"] = True
                    res["n_control_strings_code"] += 1
                    # UNBACKED-CONTROL detection: a control string that is merely
                    # PRINTED inside the success branch (an `if` whose subtree
                    # `return`s 0) claims a control ran without executing one —
                    # e.g. `print("NEGATIVE_CONTROL_CAUGHT ...")` next to `return 0`.
                    if _in_print(node, par):
                        nif = _nearest_if(node, par)
                        if nif is not None and _if_has_success_return(nif):
                            res["n_control_success_prints"] += 1
        elif isinstance(node, ast.JoinedStr):
            for v in node.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    s = v.value
                    if re.search(r"PASS[_ ]", s):
                        res["n_pass_prints"] += 1
                    if re.search(r"FAIL[_ ]", s):
                        res["n_fail_prints"] += 1
                    if CONTROL_RE.search(s):
                        res["control_in_code"] = True
                        res["n_control_strings_code"] += 1
                        if _in_print(node, par):
                            nif = _nearest_if(node, par)
                            if nif is not None and _if_has_success_return(nif):
                                res["n_control_success_prints"] += 1

    # ---- reads / writes ----
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in READ_CALL_NAMES:
                res["reads_files"] = True
                if f.id == "open":
                    for a in list(node.args[1:2]) + [k.value for k in node.keywords
                                                     if k.arg == "mode"]:
                        v = _const_value(a)
                        if isinstance(v, str) and any(c in v for c in "wax+"):
                            res["writes_files"] = True
            elif isinstance(f, ast.Attribute):
                if f.attr in READ_ATTR_NAMES:
                    res["reads_files"] = True
                if f.attr in WRITE_ATTR_NAMES:
                    res["writes_files"] = True

    # ---- can-fail constructs ----
    reasons = res["can_fail_reasons"]

    # (A) asserts
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            res["n_asserts"] += 1
            if _is_const(node.test):
                res["n_constant_asserts"] += 1
            else:
                res["n_computed_asserts"] += 1
    if res["n_computed_asserts"]:
        reasons.append(f"computed_asserts x{res['n_computed_asserts']}")

    # (B) guarded die-helper calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in die_funcs and _under(node, par, COND_TYPES):
            res["n_guarded_die_calls"] += 1
    if res["n_guarded_die_calls"]:
        reasons.append(f"guarded_die_calls x{res['n_guarded_die_calls']}")

    # (C/D) conditional raises and exits; module-level gates; wired main
    wired_targets = set()   # function names whose return feeds SystemExit/sys.exit
    success_exit_seen = False        # sys.exit(0) / sys.exit() / raise SystemExit seen
    uncond_nonzero_exits = 0         # sys.exit(1)-style NOT under a conditional
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            se = _systemexit_of(node)
            in_die_body = any(isinstance(a, (ast.FunctionDef, ast.AsyncFunctionDef))
                              and a.name in die_funcs for a in _ancestors(node, par))
            if se is not None and isinstance(se, ast.Call) and se.args:
                arg = se.args[0]
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                    wired_targets.add(arg.func.id)          # raise SystemExit(main())
                    continue
                if _gate_is_live(arg, kinds):
                    res["n_gate_exits"] += 1                 # raise SystemExit(0 if ok..)
                    continue
                v = _const_value(arg)
                if v is not _NOT_CONST and v in (0, None, False):
                    success_exit_seen = True
                    continue
                if v not in (0, None) and _under(node, par, COND_TYPES):
                    res["n_conditional_exit_nonzero"] += 1   # if bad: raise SystemExit(1)
                    continue
                if v not in (0, None) and not _under(node, par, COND_TYPES) \
                        and not in_die_body:
                    uncond_nonzero_exits += 1  # may be a fall-through failure exit
                continue
            if se is not None:  # bare `raise SystemExit` -> exit code 0
                success_exit_seen = True
                continue
            if in_die_body:
                continue        # body of die() itself; call sites counted in (B)
            if _under(node, par, ast.ExceptHandler) and node.exc is None:
                continue        # bare re-raise
            if _under(node, par, COND_TYPES):
                res["n_conditional_raises"] += 1
        elif isinstance(node, ast.Call) and _is_exit_call(node):
            arg = _exit_arg(node)
            if arg is not None and isinstance(arg, ast.Call) \
                    and isinstance(arg.func, ast.Name):
                wired_targets.add(arg.func.id)               # sys.exit(main())
                continue
            if arg is not None and _gate_is_live(arg, kinds):
                res["n_gate_exits"] += 1                     # sys.exit(0 if ok else 1)
                continue
            v = _const_value(arg) if arg is not None else None
            if v is None or (v is not _NOT_CONST and v in (0, None, False)):
                success_exit_seen = True                     # sys.exit() / sys.exit(0)
            elif v not in (0, None) and _under(node, par, COND_TYPES):
                res["n_conditional_exit_nonzero"] += 1
            elif v not in (0, None):
                uncond_nonzero_exits += 1  # may be a fall-through failure exit
            # detect fake gate: sys.exit(<name-only-const-assigned>)
            if arg is not None and not _gate_is_live(arg, kinds) \
                    and not isinstance(arg, ast.Constant):
                res["fake_gates"].append(ast.unparse(arg) if hasattr(ast, "unparse")
                                         else "<gate>")
    # FALL-THROUGH pattern at module level: `if ok: ...; sys.exit(0)` + `sys.exit(1)`
    # at the end. The nonzero exit is not syntactically under the If, but reaching it
    # is branch-dependent, so it IS a designed failure path.
    if uncond_nonzero_exits and success_exit_seen:
        res["n_conditional_exit_nonzero"] += uncond_nonzero_exits
    if res["n_conditional_raises"]:
        reasons.append(f"conditional_raises x{res['n_conditional_raises']}")
    if res["n_conditional_exit_nonzero"]:
        reasons.append(f"conditional_exit_nonzero x{res['n_conditional_exit_nonzero']}")
    if res["n_gate_exits"]:
        reasons.append(f"live_gate_exits x{res['n_gate_exits']}")

    # wired main(): inspect returns of wired target functions
    funcdefs = {n.name: n for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for tgt in sorted(wired_targets):
        fd = funcdefs.get(tgt)
        if fd is None:
            continue
        fd_returns = [n for n in ast.walk(fd) if isinstance(n, ast.Return)]
        # explicit success return anywhere in the function (incl. bare `return`)
        has_success_return = any(
            n.value is None
            or (_const_value(n.value) is not _NOT_CONST
                and _const_value(n.value) in (0, None, False))
            for n in fd_returns)
        for node in fd_returns:
            if node.value is not None:
                val = node.value
                v = _const_value(val)
                if v is not _NOT_CONST and v in (0, None, False):
                    continue
                if isinstance(val, ast.Constant):
                    # `if bad: return 1`  OR the FALL-THROUGH shape
                    # `if ok: ...; return 0` ... `return 1` (nonzero return not
                    # syntactically under the If, but reachable only when the
                    # success branch did not return) — both are branch-dependent.
                    if _under(node, par, COND_TYPES) or has_success_return:
                        res["n_wired_conditional_returns"] += 1
                elif _gate_is_live(val, kinds):
                    res["n_wired_conditional_returns"] += 1       # return 0 if ok else 2
                else:
                    res["fake_gates"].append(f"return {ast.unparse(val)}"
                                             if hasattr(ast, "unparse") else "return <gate>")
    if res["n_wired_conditional_returns"]:
        reasons.append(f"wired_conditional_returns x{res['n_wired_conditional_returns']}")

    # control idiom: try/except AssertionError|SystemExit (planted-flaw harness)
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is not None:
            names = {n.id for n in ast.walk(node.type) if isinstance(n, ast.Name)}
            if names & {"AssertionError", "SystemExit"}:
                res["control_idiom_tryexcept"] = True

    # exit discipline label
    if wired_targets:
        res["exit_discipline"] = "systemexit_main"
    elif res["n_gate_exits"]:
        res["exit_discipline"] = "module_gate"
    elif res["n_computed_asserts"] or res["n_guarded_die_calls"] \
            or res["n_conditional_exit_nonzero"] or res["n_conditional_raises"]:
        res["exit_discipline"] = "toplevel_checks"

    res["can_fail_constructs"] = (
        res["n_computed_asserts"] + res["n_guarded_die_calls"]
        + res["n_conditional_raises"] + res["n_conditional_exit_nonzero"]
        + res["n_gate_exits"] + res["n_wired_conditional_returns"])

    # ---- classification ----
    # controls_unbacked: every in-code control string is a success-path PRINT
    # (claimed in the transcript, never executed) -> does not count as a control.
    res["controls_unbacked"] = bool(
        res["control_in_code"]
        and res["n_control_strings_code"] > 0
        and res["n_control_success_prints"] == res["n_control_strings_code"])
    control = ((res["control_in_code"] and not res["controls_unbacked"])
               or res["control_idiom_tryexcept"])
    if res["can_fail_constructs"] == 0:
        res["classification"] = "STUB-SUSPECT"
        if res["n_asserts"] and res["n_asserts"] == res["n_constant_asserts"]:
            res["class_reason"] = "all_asserts_constant"
        elif res["fake_gates"]:
            res["class_reason"] = "fake_gate:" + ";".join(res["fake_gates"][:2])
        elif res["n_pass_prints"]:
            res["class_reason"] = "print_only_pass_lines"
        else:
            res["class_reason"] = "no_failure_path"
    elif control:
        res["classification"] = "SOLID"
        res["class_reason"] = "computed_checks+negative_control"
    else:
        res["classification"] = "WEAK"
        if res["controls_unbacked"]:
            res["class_reason"] = "controls_printed_not_executed"
        elif res["control_in_docstring"]:
            res["class_reason"] = "checks_but_control_only_in_docstring"
        else:
            res["class_reason"] = "checks_but_no_negative_control"
    return res


# ---------------------------------------------------------------------------
# registry cross-reference
# ---------------------------------------------------------------------------

LOAD_BEARING = {"CERT-CLOSED", "NO-GO", "NO_GO_PROVED"}


def load_registry(csv_path):
    """cert basename -> list of {claim_id, release_status}; also unmatched refs."""
    cert_claims = {}
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    for r in rows:
        for ref in (r.get("python_cert") or "").split(";"):
            ref = ref.strip()
            if not ref:
                continue
            cert_claims.setdefault(Path(ref).name, []).append(
                {"claim_id": r["claim_id"], "release_status": r["release_status"]})
    return cert_claims, rows


# ---------------------------------------------------------------------------
# dynamic layer
# ---------------------------------------------------------------------------

def run_cert(path, cwd, timeout):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, str(path)], cwd=str(cwd),
                           capture_output=True, text=True, timeout=timeout)
        rc, out = p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        rc, out = "TIMEOUT", ""
    dt = round(time.time() - t0, 2)
    tail = "\n".join(out.strip().splitlines()[-3:]) if out else ""
    return {"rc": rc, "secs": dt, "tail": tail[:400]}


def pick_mutation_target(src):
    """First int constant |v|>=2 not inside print()/f-string. -> (node, None) or (None, why)."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None, "unparseable"
    par = _parents(tree)
    cands = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, int) \
                and not isinstance(node.value, bool) and abs(node.value) >= 2:
            if _under(node, par, ast.JoinedStr):
                continue  # f-string offsets unreliable pre-3.12
            if _in_print(node, par):
                continue
            if getattr(node, "end_col_offset", None) is None:
                continue
            cands.append(node)
    if not cands:
        return None, "no_int_constant_>=2"
    cands.sort(key=lambda n: (n.lineno, n.col_offset))
    return cands[0], None


def mutate_copy(orig, scratch_dir):
    """Copy cert to scratch, flip one computed int constant. -> (mutpath, note)."""
    src = orig.read_text(encoding="utf-8-sig", errors="replace")
    node, why = pick_mutation_target(src)
    if node is None:
        return None, why
    starts, off = [], 0
    for line in src.splitlines(keepends=True):
        starts.append(off)
        off += len(line)
    a = starts[node.lineno - 1] + node.col_offset
    b = starts[node.end_lineno - 1] + node.end_col_offset
    old_txt = src[a:b]
    new_val = node.value + 1
    mut = src[:a] + repr(new_val) + src[b:]
    mutpath = scratch_dir / orig.name
    mutpath.write_text(mut, encoding="utf-8")
    return mutpath, f"line {node.lineno}: {old_txt} -> {new_val}"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--json", default=None, help="write full results JSON here")
    ap.add_argument("--dynamic", action="store_true", help="run top suspects")
    ap.add_argument("--mutate", action="store_true", help="mutation-probe self-contained suspects")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--timeout", type=int, default=60)
    ap.add_argument("--scratch", default=None, help="scratch dir for mutated copies")
    args = ap.parse_args()

    repo = Path(args.repo)
    certs_dir = repo / "05_CERTS"
    csv_path = repo / "09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv"
    if not certs_dir.is_dir() or not csv_path.is_file():
        print(f"FATAL: bad repo layout under {repo}", file=sys.stderr)
        return 2

    certs = sorted(certs_dir.glob("vp_*.py"))          # top level only, per task scope
    cert_claims, _rows = load_registry(csv_path)

    results = []
    for p in certs:
        r = analyze_static(p)
        claims = cert_claims.get(p.name, [])
        r["claims"] = claims
        r["n_claims"] = len(claims)
        r["loadbearing_claims"] = [c for c in claims if c["release_status"] in LOAD_BEARING]
        r["n_loadbearing"] = len(r["loadbearing_claims"])
        results.append(r)

    unmatched_refs = sorted(set(cert_claims) - {p.name for p in certs})

    by_class = {}
    for r in results:
        by_class.setdefault(r["classification"], []).append(r)

    print(f"# cert_canfail_sweep — {len(certs)} certs, "
          f"{sum(len(v) for v in cert_claims.values())} registry cert-references")
    for cls in ("SOLID", "WEAK", "STUB-SUSPECT"):
        rs = by_class.get(cls, [])
        lb = sum(1 for r in rs if r["n_loadbearing"])
        print(f"{cls:13s} {len(rs):4d}   ({lb} of them back CERT-CLOSED/NO-GO claims)")
    print(f"registry cert refs with no file in 05_CERTS top level: {len(unmatched_refs)}")

    suspects = sorted(by_class.get("STUB-SUSPECT", []),
                      key=lambda r: (-r["n_loadbearing"], -r["n_claims"], r["cert"]))
    print("\n## STUB-SUSPECTS (sorted by load-bearing claim count)")
    for r in suspects:
        cl = ",".join(f"{c['claim_id']}[{c['release_status']}]"
                      for c in r["loadbearing_claims"]) or "-"
        print(f"  {r['cert']:60s} reason={r['class_reason']:28s} "
              f"lb={r['n_loadbearing']} claims={r['n_claims']} {cl}")

    dyn = []
    if args.dynamic:
        scratch = Path(args.scratch) if args.scratch else Path("/tmp/cert_canfail_scratch")
        (scratch / "mut").mkdir(parents=True, exist_ok=True)
        top = suspects[:args.top]
        print(f"\n## DYNAMIC — running top {len(top)} stub-suspects (timeout {args.timeout}s)")
        for r in top:
            p = certs_dir / r["cert"]
            entry = {"cert": r["cert"], "n_loadbearing": r["n_loadbearing"]}
            if r["writes_files"]:
                entry["run"] = "SKIPPED-WRITES (would modify repo outputs)"
            else:
                entry["run"] = run_cert(p, certs_dir, args.timeout)
            if args.mutate:
                if r["reads_files"] or r["writes_files"]:
                    entry["mutation"] = "SKIPPED (file-reading/writing cert — method limit)"
                else:
                    mp, note = mutate_copy(p, scratch / "mut")
                    if mp is None:
                        entry["mutation"] = f"SKIPPED ({note})"
                    else:
                        mres = run_cert(mp, scratch / "mut", args.timeout)
                        survived = (mres["rc"] == 0)
                        entry["mutation"] = {"flip": note, "rc": mres["rc"],
                                             "survived_exit0": survived}
            dyn.append(entry)
            print(f"  {r['cert']:55s} run={entry['run'] if isinstance(entry['run'], str) else entry['run']['rc']}"
                  f"  mut={entry.get('mutation', '-') if isinstance(entry.get('mutation'), str) else entry.get('mutation', {}).get('survived_exit0', '-')}")

    if args.json:
        payload = {
            "n_certs": len(certs),
            "counts": {k: len(v) for k, v in by_class.items()},
            "unmatched_registry_refs": unmatched_refs,
            "results": results,
            "dynamic": dyn,
        }
        Path(args.json).write_text(json.dumps(payload, indent=1), encoding="utf-8")
        print(f"\nJSON written: {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
