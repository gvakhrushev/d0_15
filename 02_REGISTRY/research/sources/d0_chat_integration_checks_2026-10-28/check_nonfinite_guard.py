#!/usr/bin/env python3
"""Mutate each scalar output/error to NaN and require fail-closed behavior.

Only temporary copies are mutated; published original and the independent
checker remain unchanged. Normal and -O refer to the independent checker.
"""
from __future__ import annotations
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np
import scipy

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'independent_frechet_controls.py'
ORIGINAL = ROOT.parent / 'd0_root_moving_cut_2026-10-28' / 'check_root_moving_cut.py'
RAW_FIELDS = ('direct', 'relative', 'bound', 'tangent_error', 'covariant_error',
              'frechet', 'beta_partial', 'beta_fd', 'z_partial', 'z_fd', 'gauge', 'gap')
ERROR_FIELDS = ('source_vs_frechet', 'beta_partial_fd', 'z_partial_fd',
                'co_transport', 'noncommuting_heat_gap')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    original_bytes = ORIGINAL.read_bytes()
    script_bytes = SCRIPT.read_bytes()
    script = script_bytes.decode('utf-8')
    checks = []
    with tempfile.TemporaryDirectory(prefix='d0-nan-guard-') as temp:
        temp_root = Path(temp)
        source = temp_root / 'd0_root_moving_cut_2026-10-28'
        package = temp_root / 'd0_chat_integration_checks_2026-10-28'
        source.mkdir(); package.mkdir()
        (source / ORIGINAL.name).write_bytes(original_bytes)
        mutant = package / SCRIPT.name
        for category, fields in [('numeric_outputs', RAW_FIELDS), ('errors', ERROR_FIELDS)]:
            marker = ('        for name, value in numeric_outputs.items():\n' if category == 'numeric_outputs'
                      else '        for key, value in errors.items():\n')
            require(script.count(marker) == 1, f'Marker not unique: {category}')
            for field in fields:
                altered = script.replace(marker, f"        {category}[{field!r}] = float('nan')\n" + marker)
                mutant.write_text(altered, encoding='utf-8')
                for optimized in (False, True):
                    args = [sys.executable] + (['-O'] if optimized else []) + [str(mutant)]
                    result = subprocess.run(args, capture_output=True, text=True)
                    expected = f'Nonfinite {field} at n=2, rank=0'
                    require(result.returncode != 0 and expected in result.stderr,
                            f'NaN mutation survived: {category}.{field}, optimized={optimized}')
                    checks.append({'category': category, 'field': field,
                                   'optimized': optimized, 'exit_code': result.returncode,
                                   'expected_diagnostic_present': True})
    require(ORIGINAL.read_bytes() == original_bytes and SCRIPT.read_bytes() == script_bytes,
            'Input file mutated by guard test')
    print(json.dumps({'status': 'PASS_NAN_MUTATIONS', 'checks': checks,
        'check_count': len(checks),
        'input_script_sha256': hashlib.sha256(script_bytes).hexdigest(),
        'source_checker_sha256': hashlib.sha256(original_bytes).hexdigest(),
        'versions': {'python': platform.python_version(), 'numpy': np.__version__,
                     'scipy': scipy.__version__, 'platform': platform.platform()},
        'scope': 'Local numerical fail-closed controls; no native full42, Lean or physical acceptance.'},
        indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
