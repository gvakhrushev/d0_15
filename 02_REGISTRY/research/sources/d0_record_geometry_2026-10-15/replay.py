#!/usr/bin/env python3
"""Replay only the new packet's checks, without ZIPs or changes to original files."""
import json
import platform
from pathlib import Path
import subprocess
import sys

from verify_publication import verify

HERE = Path(__file__).resolve().parent


def run(script, optimized=False):
    args = [sys.executable] + (['-O'] if optimized else []) + [str(HERE / 'original' / script)]
    cp = subprocess.run(args, cwd=HERE / 'original', capture_output=True, text=True, timeout=180)
    if cp.returncode:
        raise RuntimeError(script + ': ' + cp.stderr[-3000:])
    return json.loads(cp.stdout)


def main():
    if sys.version_info < (3, 11):
        raise RuntimeError('Python 3.11+ required')
    import sympy
    import numpy
    verify()
    exact, exact_o = run('check_record_2jet.py'), run('check_record_2jet.py', True)
    stored = json.loads((HERE / 'original/exact_result.json').read_text())
    if exact != exact_o or exact != stored:
        raise RuntimeError('Exact replay differs from default, optimized or preserved result')
    mutants = run('check_mutations.py')
    if mutants != json.loads((HERE / 'original/mutation_result.json').read_text()):
        raise RuntimeError('Mutation outcomes differ from preserved result')
    heat, heat_o = run('check_heat_window.py'), run('check_heat_window.py', True)
    if heat != heat_o:
        raise RuntimeError('Default and optimized heat diagnostics differ')
    stored_heat = json.loads((HERE / 'original/heat_diagnostic.json').read_text())
    if heat['coefficient'] != stored_heat['coefficient'] or len(heat['rows']) != len(stored_heat['rows']):
        raise RuntimeError('Heat fixture differs')
    max_gap = max(abs(a['shape_source'] - b['shape_source'])
                  for a, b in zip(heat['rows'], stored_heat['rows']))
    if max_gap > 1e-9:
        raise RuntimeError('Heat diagnostic changed beyond floating tolerance')
    print(json.dumps({
        'status': 'PASS_NEW_PACKET_REPLAY', 'python': platform.python_version(),
        'sympy': sympy.__version__, 'numpy': numpy.__version__,
        'exact_default_optimized_and_preserved_equal': True,
        'heat_default_optimized_equal': True, 'heat_preserved_max_absolute_gap': max_gap,
        'heat_comparison_tolerance': 1e-9, 'mutations': mutants,
        'exact_result': exact, 'heat_diagnostic': heat,
        'scope': 'new exact kinematic fixture, mathematical mutations, floating heat diagnostic',
        'historical_full_replay': False, 'native_admission': False,
        'native_action_binding': False, 'GR_closed': False, 'Lean_build': False,
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
