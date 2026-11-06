#!/usr/bin/env python3
"""Replay the pinned nine-package intake in disposable copies, not in place.

A successful replay is a scoped computational check, not physical or Lean
acceptance. The independent member-byte verifier runs before any archived code.
"""
from __future__ import annotations

import argparse
import ast
from decimal import Decimal, InvalidOperation
import hashlib
import importlib.metadata
import json
import math
import os
import platform
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / '02_REGISTRY/research/sources/d0_chat_intake_2026-10-28'
SOURCE_COMMIT = 'eebcb5e467742df3e9cf7fa9702042d7294aa742'
# Checker name, its explicit success status, and (when present) exact check count.
CASES = [
    ('D0_closed_source_cone_2026-10-27/check_closed_source_cone.py', 'PASS_CLOSED_SOURCE_CONE_AND_UNARY_ENSEMBLE', 12423),
    ('D0_complete_source_application_2026-10-27/complete_book_source_application_check.py', 'PASS_COMPLETE_CUT_SOURCE_AND_FIXED_INITIAL_LIFT', None),
    ('D0_complete_source_application_2026-10-27/check_original_car.py', 'CAR_DIAGNOSTIC', None),
    ('D0_density_and_full_price_bridge_2026-10-27/check_density_price_bridge.py', 'PASS_DENSITY_INVOLUTION_AND_FULL_PRICE_C1_CONTROL', 57),
    ('D0_final_selection_check_2026-10-27/check_arithmetic.py', 'PASS_EXACT_GOLDEN_ARITHMETIC_SCOPE', 14),
    ('D0_final_selection_check_2026-10-27/check_selection.py', 'PASS_EXACT_SAME_INVENTORY_CLOSED_SELECTION_TEST', 59),
    ('D0_global_geometric_source_2026-10-27/check_parity_bridge.py', 'PASS_EXACT_CAR_PARITY_GEOMETRIC_SOURCE', 305),
    ('D0_internal_clock_bridge_2026-10-27/check_internal_clock_bridge.py', 'PASS_INTERNAL_CLOCK_REFLECTION_SOURCE_APPLICATION', 26),
    ('D0_internal_clock_bridge_2026-10-27/check_finite_golden_secants.py', 'PASS_NATIVE_GOLDEN_ECHO_SECANTS', 21),
    ('D0_intrinsic_metric_and_exact_stationarity_2026-10-27/check_intrinsic_metric_heat_recovery.py', 'PASS_INTRINSIC_METRIC_HEAT_EQUIVALENCE_AND_C2_CONTROL', 59),
    ('D0_root_source_test_2026-10-27/check_root_source_universality.py', 'PASS_FIXED_INTERFACE_POLYNOMIAL_SOURCE_REALIZATION', 4217),
    ('D0_source_class_synthesis_2026-10-27/check_source_class.py', 'PASS_COMPLETE_HERALD_SOURCE_CLASS', 10370),
]

class ReplayFailure(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_constant(value: str) -> None:
    raise ReplayFailure('non-finite JSON constant: ' + value)


INTERVAL_NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'
INTERVAL = re.compile(r'\[\s*(' + INTERVAL_NUMBER + r')\s*,\s*(' + INTERVAL_NUMBER + r')\s*\]')


def check_interval(value: Any) -> None:
    if not isinstance(value, str) or len(value) > 4096:
        raise ReplayFailure('invalid numeric interval')
    match = INTERVAL.fullmatch(value)
    if match is None:
        raise ReplayFailure('invalid numeric interval')
    try:
        lower, upper = (Decimal(part) for part in match.groups())
        if not lower.is_finite() or not upper.is_finite() or lower > upper:
            raise ReplayFailure('non-finite or reversed numeric interval')
    except InvalidOperation as exc:
        raise ReplayFailure('invalid numeric interval') from exc


def finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ReplayFailure('non-finite numeric result')
    if isinstance(value, str) and value.strip().lower() in {
            'nan', '+nan', '-nan', 'inf', '+inf', '-inf',
            'infinity', '+infinity', '-infinity'}:
        raise ReplayFailure('non-finite numeric string')
    if isinstance(value, dict):
        for key, item in value.items():
            name = key.lower()
            if name in {'operator_error_plus_interval', 'operator_error_minus_interval'}:
                check_interval(item)
            if name == 'status' or name.endswith('_status'):
                if not isinstance(item, str) or not (item == 'PASS' or item.startswith('PASS_')):
                    raise ReplayFailure('non-passing status: ' + key)
            if name in {'fail', 'failed', 'failure', 'failures', 'error', 'errors',
                        'fail_count', 'failed_count', 'failure_count', 'error_count',
                        'failed_checks', 'failed_tests'}:
                if not (item is False or (type(item) is int and item == 0)
                        or item == [] or item == {}):
                    raise ReplayFailure('checker reports failure: ' + key)
            if (name.endswith('_gr_closed') or name == 'universal_gr_closed') and item is not False:
                raise ReplayFailure('GR closure nonclaim missing or changed')
            finite(item)
    elif isinstance(value, list):
        for item in value:
            finite(item)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ReplayFailure('duplicate JSON key: ' + key)
        result[key] = value
    return result


def parse_json(data: bytes, status: str, count: int | None) -> dict[str, Any]:
    try:
        result = json.loads(data.decode('utf-8'), parse_constant=reject_constant,
                            object_pairs_hook=unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReplayFailure('invalid JSON output: ' + str(exc)) from exc
    if not isinstance(result, dict) or result.get('status') != status:
        raise ReplayFailure('unexpected or missing checker status')
    finite(result)
    if count is not None and (type(result.get('checks')) is not int or result['checks'] != count):
        raise ReplayFailure('unexpected or missing check count')
    if count is None:
        required = ('thermal_bound_exact', 'ready_probability', 'strict_native_cut_vs_tensor_heat_source')
        if any(not isinstance(result.get(key), str) or not result[key] for key in required):
            raise ReplayFailure('missing complete-source evidence')
    return result


def parse_car(data: bytes) -> dict[str, Any]:
    try:
        lines = data.decode('utf-8').splitlines()
    except UnicodeError as exc:
        raise ReplayFailure('invalid CAR diagnostic encoding') from exc
    values: dict[str, str] = {}
    for line in lines:
        key, sep, value = line.partition(' ')
        if not sep or key in values:
            raise ReplayFailure('malformed or duplicate CAR diagnostic line')
        values[key] = value.strip()
    if (values.get('quadratic_bad_count') != '0' or
            values.get('trace_difference') != '0' or values.get('first_bad') != '[]'):
        raise ReplayFailure('CAR diagnostic reports failure or is incomplete')
    if not values.get('eigenvals') or not values.get('elapsed'):
        raise ReplayFailure('incomplete CAR diagnostic')
    if len(values['eigenvals']) > 4096:
        raise ReplayFailure('CAR eigenvalue expression too large')
    try:
        eigenvalues = ast.parse(values['eigenvals'], mode='eval').body
    except (SyntaxError, ValueError, RecursionError) as exc:
        raise ReplayFailure('malformed CAR eigenvalue dictionary') from exc
    if not isinstance(eigenvalues, ast.Dict) or len(eigenvalues.keys) != 2:
        raise ReplayFailure('CAR eigenvalue diagnostic must contain two entries')
    if any(not isinstance(value, ast.Constant) or type(value.value) is not int or value.value != 8
           for value in eigenvalues.values):
        raise ReplayFailure('CAR eigenvalue multiplicities must be integer 8')
    keys = eigenvalues.keys
    if len(list(ast.walk(eigenvalues))) > 100:
        raise ReplayFailure('CAR eigenvalue expression too complex')
    if any(key is None for key in keys) or ast.dump(keys[0]) == ast.dump(keys[1]):
        raise ReplayFailure('CAR eigenvalue expressions must be structurally distinct')
    def numeric_expression(node: ast.AST) -> bool:
        if isinstance(node, ast.Constant):
            return type(node.value) is int
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return numeric_expression(node.operand)
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            return numeric_expression(node.left) and numeric_expression(node.right)
        return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == 'sqrt' and len(node.args) == 1 and not node.keywords
                and numeric_expression(node.args[0]))
    if not all(numeric_expression(key) for key in keys):
        raise ReplayFailure('CAR eigenvalue expressions contain unsupported or nonnumeric syntax')
    try:
        elapsed = float(values['elapsed'])
    except ValueError as exc:
        raise ReplayFailure('invalid CAR elapsed value') from exc
    if not math.isfinite(elapsed) or elapsed < 0:
        raise ReplayFailure('non-finite CAR elapsed value')
    return {'quadratic_bad_count': 0, 'trace_difference': 0,
            'first_bad': [], 'eigenvals': values['eigenvals'],
            'structurally_distinct_eigenvalue_expressions': 2,
            'reported_integer_multiplicities': [8, 8]}


def invoke(command: list[str], cwd: Path, timeout: int) -> dict[str, Any]:
    try:
        process = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, timeout=timeout,
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        out, err, code, timed_out = process.stdout, process.stderr, process.returncode, False
    except subprocess.TimeoutExpired as exc:
        out, err, code, timed_out = exc.stdout or b'', exc.stderr or b'', None, True
    return {'command': command, 'exit_code': code, 'timed_out': timed_out,
            'stdout_sha256': digest(out), 'stderr_sha256': digest(err),
            'stderr': err.decode('utf-8', errors='replace'), '_stdout': out}


def verifier(intake: Path, timeout: int) -> dict[str, Any]:
    result = invoke([sys.executable, '-B', str(intake / 'verify_intake.py'), str(intake)], intake, timeout)
    raw = result.pop('_stdout')
    if result['exit_code'] != 0 or result['timed_out']:
        raise ReplayFailure('read-only intake verifier failed: ' + result['stderr'])
    try:
        data = json.loads(raw.decode('utf-8'), parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReplayFailure('invalid intake verifier output') from exc
    if (not isinstance(data, dict) or data.get('status') != 'PASS_MEMBER_BYTES_ONLY'
            or data.get('source_commit') != SOURCE_COMMIT
            or data.get('member_files') != 74 or data.get('packages') != 9
            or data.get('member_bytes') != 650121
            or data.get('archived_code_executed') is not False):
        raise ReplayFailure('unexpected intake verifier contract')
    result['result'] = data
    return result


def run_case(intake: Path, case: tuple[str, str, int | None], optimized: bool,
             timeout: int, warnings_as_errors: bool) -> dict[str, Any]:
    relative, status, count = case
    source = intake / 'packages' / relative
    temp_root = Path(tempfile.gettempdir()).resolve()
    repo = ROOT.resolve()
    if temp_root == repo or repo in temp_root.parents:
        raise ReplayFailure('temporary directory must be outside the checkout')
    with tempfile.TemporaryDirectory(prefix='d0-intake-replay-') as temp:
        copy = Path(temp) / source.parent.name
        shutil.copytree(source.parent, copy)
        script = copy / source.name
        def inventory(directory: Path) -> dict[str, str]:
            return {p.relative_to(directory).as_posix(): digest(p.read_bytes())
                    for p in directory.rglob('*') if p.is_file()}
        if inventory(copy) != inventory(source.parent):
            raise ReplayFailure('copied package differs from verified source')
        command = [sys.executable, '-B']
        if warnings_as_errors:
            command += ['-W', 'error']
        if optimized:
            command.append('-O')
        command.append(str(script))
        result = invoke(command, copy, timeout)
        raw = result.pop('_stdout')
        result.update({'checker': relative, 'checker_sha256': digest(source.read_bytes()),
                       'mode': 'optimized' if optimized else 'normal'})
        if result['exit_code'] != 0 or result['timed_out']:
            result['error'] = 'checker failed or timed out'
        else:
            try:
                result['parsed'] = parse_car(raw) if status == 'CAR_DIAGNOSTIC' else parse_json(raw, status, count)
            except ReplayFailure as exc:
                result['error'] = str(exc)
        return result


def safe_output(path: Path, repo: Path) -> Path:
    path = path.expanduser().resolve()
    repo = repo.resolve()
    if path == repo or repo in path.parents:
        raise ReplayFailure('receipt must be outside the checkout')
    if path.exists():
        raise ReplayFailure('receipt already exists; choose a new path')
    return path


def environment() -> dict[str, Any]:
    versions = {}
    for package in ('numpy', 'scipy', 'sympy', 'mpmath'):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return {'python_executable': sys.executable, 'python_version': sys.version,
            'platform': platform.platform(), 'packages': versions,
            'python_warnings': os.environ.get('PYTHONWARNINGS'),
            'python_hash_seed': os.environ.get('PYTHONHASHSEED')}


def replay(intake: Path, cases: list[tuple[str, str, int | None]], timeout: int,
           warnings_as_errors: bool) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        'status': 'FAIL', 'source_commit': SOURCE_COMMIT, 'environment': environment(),
        'warnings_as_errors': warnings_as_errors, 'runs': [],
        'scope': ['Pinned member bytes only; original ZIP bytes are not verified.',
                  'Computational controls only; no Lean proof or scientific acceptance.',
                  'Native source admission, full physical selection and GR closure remain open.'],
    }
    try:
        receipt['verification_before'] = verifier(intake, timeout)
        for case in cases:
            runs = []
            for optimized in (False, True):
                item = run_case(intake, case, optimized, timeout, warnings_as_errors)
                receipt['runs'].append(item)
                runs.append(item)
                if 'error' in item:
                    raise ReplayFailure(case[0] + ': ' + item['error'])
            if runs[0]['parsed'] != runs[1]['parsed']:
                raise ReplayFailure(case[0] + ': normal and optimized results differ')
        receipt['verification_after'] = verifier(intake, timeout)
        receipt['status'] = 'PASS_SCOPED_REPLAY'
    except (ReplayFailure, OSError, ValueError) as exc:
        receipt['error'] = str(exc)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='new receipt path outside checkout')
    parser.add_argument('--timeout', type=int, default=600, help='seconds per process')
    parser.add_argument('--warnings-as-errors', action='store_true')
    args = parser.parse_args()
    try:
        if args.timeout <= 0:
            raise ReplayFailure('timeout must be positive')
        output = safe_output(args.output, ROOT.resolve())
        receipt = replay(INTAKE, CASES, args.timeout, args.warnings_as_errors)
        # Exclusive creation avoids overwriting an existing artifact or symlink.
        with output.open('x', encoding='utf-8') as stream:
            json.dump(receipt, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
        print(f"{receipt['status']}: {output}")
        if receipt.get('error'):
            print(receipt['error'], file=sys.stderr)
        for item in receipt['runs']:
            if item['stderr']:
                print(f"{item['checker']} ({item['mode']}) stderr:\n{item['stderr']}", file=sys.stderr)
        return 0 if receipt['status'] == 'PASS_SCOPED_REPLAY' else 1
    except (ReplayFailure, OSError, ValueError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
