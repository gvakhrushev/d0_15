#!/usr/bin/env python3
"""Replay archived finite mathematics directly from byte-preserved expanded text.

Only two staging/provenance expressions in a TEMPORARY synthesis_check.py copy
are adapted. The complete mathematical body and all four source files are SHA
pinned. No ZIP, compressed capsule, importer, Git command, or patch application
is needed or executed. Inputs are read-only; outputs are new files in --output.
Python 3.11+ and SymPy are required. This does not run full4d interval checks.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

LEAF = '02_REGISTRY/research/sources/d0_joint_lattice_ward_resonance_2026-10-15'
FULL = '02_REGISTRY/research/sources/d0_full_four_dimensional_sheet_2026-10-15'
PINS = {
    'synthesis': 'aaa1d3890377128de7fcdffe3ae68afd2c092a49a222f6b0f239284a541dfbbe',
    'identities': '55cd845e09d62147138b3faf04506895ec7bad75ac1f75a4c528e047dec964bb',
    'linear': '8a25e81936ef10346c41cdc9d9bea899f415cd6c55c847b604d94a4a48d01474',
    'symbol': '37c2b21429c5e703068d2ac398160329e9728ffce480ec86fc57418813e90dab',
    'resonance_reference': 'a9b37737c4b101eb0c84fa224eb98f8d922774ee606a046729651d549be9277c',
    'identities_reference': '2dd9ab48310264a452c2e951cad7d796ae914c62a5e46abc7b1ca27d97081a32',
}
HISTORICAL_ZIP_SHA = '441c5c503737c375600cd119ef5bf0d0c343b0445d425b1e755acd99ddd7b47f'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pinned(path, role):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PINS[role], 'SOURCE_HASH_CHANGED: ' + role)
    return raw


def mathematics(source):
    start = source.index('        R=m.resonance();')
    end = source.index('        receipt={', start)
    return source[start:end]


def adapted_synthesis(source, linear, symbol):
    """Replace archive staging and its archive-only receipt field, nothing else."""
    begin = source.index('        with zipfile.ZipFile(args.input) as z:\n')
    end = source.index('        spec=importlib.util.spec_from_file_location', begin)
    old_staging = source[begin:end]
    require(source.count(old_staging) == 1, 'AMBIGUOUS_STAGING')
    staging = (
        '        # Text adapter: stage unchanged, hash-pinned literal dependencies.\n'
        f'        data=Path({str(linear)!r}).read_bytes()\n'
        "        require(hashlib.sha256(data).hexdigest()==LINEAR_SHA256,'Changed input symbol consumer')\n"
        "        target=root/LEAF/'linear.py';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)\n"
        f'        symbol_data=Path({str(symbol)!r}).read_bytes()\n'
        f"        require(hashlib.sha256(symbol_data).hexdigest()=={PINS['symbol']!r},'Changed literal symbol')\n"
        f"        upstream=root/{FULL!r}/'symbol.py'\n"
        '        upstream.parent.mkdir(parents=True,exist_ok=True);upstream.write_bytes(symbol_data)\n'
    )
    result = source.replace(old_staging, staging, 1)
    old_receipt = "'input_zip_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),"
    new_receipt = f"'historical_input_zip_sha256':{HISTORICAL_ZIP_SHA!r},"
    require(result.count(old_receipt) == 1, 'AMBIGUOUS_PROVENANCE_EXPRESSION')
    result = result.replace(old_receipt, new_receipt, 1)
    require(mathematics(result) == mathematics(source), 'MATHEMATICS_WAS_CHANGED')
    return result


def without_fields(value, keys):
    return {key: item for key, item in value.items() if key not in keys}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--resonant-root', type=Path, required=True,
                    help='Expanded D0_resonant_synthesis_proof_package directory')
    ap.add_argument('--two-syntheses-root', type=Path, required=True,
                    help='Expanded D0_two_syntheses_proof_package directory')
    ap.add_argument('--joint-root', type=Path, required=True,
                    help='Expanded D0_joint_ward_resonance_git_intake directory (contains repo/)')
    ap.add_argument('--full4d-root', type=Path, required=True,
                    help='Expanded PRESERVED_INPUT_full4d_exact_sheet directory (contains repo/)')
    ap.add_argument('--output', type=Path, required=True,
                    help='New or empty output directory; no existing output files are replaced')
    ap.add_argument('--only', choices=('all', 'identities', 'resonance'), default='all')
    ap.add_argument('--optimized', action='store_true', help='Run historical scripts under Python -O')
    ap.add_argument('--timeout', type=int, default=600, help='Timeout in seconds per historical script')
    args = ap.parse_args()
    roots = [args.resonant_root.resolve(), args.two_syntheses_root.resolve(),
             args.joint_root.resolve(), args.full4d_root.resolve()]
    output = args.output.resolve()
    require(not any(output == root or output.is_relative_to(root) for root in roots),
            'OUTPUT_MUST_BE_OUTSIDE_PRESERVED_INPUTS')
    paths = {
        'synthesis': roots[0] / 'synthesis_check.py',
        'identities': roots[1] / 'new_identities.py',
        'linear': roots[2] / 'repo' / LEAF / 'linear.py',
        'symbol': roots[3] / 'repo' / FULL / 'symbol.py',
        'resonance_reference': roots[0] / 'validation.json',
        'identities_reference': roots[1] / 'results.json',
    }
    raw = {role: pinned(path, role) for role, path in paths.items()}
    output.mkdir(parents=True, exist_ok=True)
    names = ['adapter_receipt.json']
    jobs = []
    if args.only in ('all', 'identities'):
        jobs.append(('identities', 'identities_result.json', 'identities.log'))
    if args.only in ('all', 'resonance'):
        jobs.append(('resonance', 'resonance_result.json', 'resonance.log'))
    names += [name for _, result, log in jobs for name in (result, log)]
    require(not any((output / name).exists() for name in names), 'OUTPUT_FILE_ALREADY_EXISTS')
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
           'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1'}
    interpreter = [sys.executable] + (['-O'] if args.optimized else [])
    reports = {}
    with tempfile.TemporaryDirectory(prefix='d0-text-historical-') as directory:
        temp = Path(directory)
        for kind, result_name, log_name in jobs:
            if kind == 'identities':
                script = temp / 'new_identities.py'
                script.write_bytes(raw['identities'])
                reference = json.loads(raw['identities_reference'])
                command = interpreter + [str(script), '--output', str(output / result_name)]
                excluded = {'sympy'}
            else:
                script = temp / 'synthesis_check_text_adapter.py'
                script.write_text(adapted_synthesis(raw['synthesis'].decode('utf-8'),
                                  paths['linear'], paths['symbol']), encoding='utf-8')
                reference = json.loads(raw['resonance_reference'])
                # --input remains syntactically required by the preserved parser;
                # the adapter never reads it as a ZIP or computes an archive hash.
                command = interpreter + [str(script), '--input', str(paths['linear']),
                                         '--output', str(output / result_name)]
                excluded = {'input_zip_sha256', 'historical_input_zip_sha256', 'sympy_version'}
            cp = subprocess.run(command, cwd=temp, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                timeout=args.timeout)
            (output / log_name).write_text(cp.stdout, encoding='utf-8')
            require(cp.returncode == 0, 'REPLAY_FAILED: ' + kind + '; inspect ' + log_name)
            observed = json.loads((output / result_name).read_text(encoding='utf-8'))
            require(without_fields(observed, excluded) == without_fields(reference, excluded),
                    'REFERENCE_MATHEMATICS_DIFFERS: ' + kind)
            reports[kind] = {'status': observed['status'],
                             'matches_historical_math_and_scope': True,
                             'excluded_comparison_fields': sorted(excluded),
                             'result': result_name, 'log': log_name}
            print('PASS_TEXT_REPLAY_' + kind.upper(), flush=True)
    receipt = {
        'schema': 'd0-expanded-text-historical-replay/1',
        'input_sha256': PINS,
        'historical_joint_archive_sha256': HISTORICAL_ZIP_SHA,
        'input_archives_opened': False,
        'compressed_capsules_used': False,
        'importer_or_patch_executed': False,
        'input_files_modified': False,
        'temporary_synthesis_replacements': [
            'ZIP/capsule staging -> plain hash-pinned linear.py and sibling symbol.py',
            'computed input_zip_sha256 -> explicit historical_input_zip_sha256'],
        'complete_synthesis_mathematical_body_unchanged': True,
        'optimized': args.optimized,
        'replays': reports,
        'scope': 'Historical exact identities and fixed four-phase finite cubic compatibility only',
        'full4d_interval_replay': False,
        'native_physical_admission': False,
        'new_GR_closure': False,
        'new_Lean_compilation': False,
    }
    (output / 'adapter_receipt.json').write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
