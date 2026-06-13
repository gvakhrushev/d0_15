#!/usr/bin/env python3
"""Run all D0 v15 closure certificates.

Parallelized with bounded workers so the release check stays fast while each cert
still executes as an independent subprocess. No .lake/Lean cache is touched.
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import pathlib
import subprocess
import sys
import time

here = pathlib.Path(__file__).resolve().parent
scripts = [
    'vp_self_substrate_trace_principle.py',
    'vp_fractal_tick_informational_mechanics.py',
    'vp_continuum_from_fractal_tick.py',
    'vp_mobius_witness_topological_halting.py',
    'vp_quadratic_peel_born_holography.py',
    'vp_measurement_horizon_equivalence.py',
    'vp_optical_jet_backreaction.py',
    'vp_master_bootstrap_and_volume_derivative.py',
    'vp_gauge_boundary_commutator_obstruction.py',
    'vp_horizon_emission_conjugate_feedback.py',
    'vp_edge_sector_alpha_trace_target.py',
    'vp_cvft_baryon_40_56_decomposition.py',
    'vp_higgs_scalar_projector_constructive.py',
    'vp_higgs_yukawa_section_transfer.py',
    'vp_meson_defect_transfer_algebra.py',
    'vp_horizon_jet_axis_observable.py',
    'vp_baryon_40_56_anonymous_poles.py',
    'vp_quantum_metrology_limits.py',
    'vp_edge_alpha_trace_constructive.py',
    'vp_edge_alpha_ramification_puiseux.py',
    'vp_ramification_edge_ueff_companion.py',
    'vp_fractal_continuum_predictions.py',
    'vp_relative_archive_acceleration_cosmology_bridge.py',
    'vp_archive_pressure_coupling_from_relative_acceleration.py',
    'vp_strong_logdet_pressure_coupling.py',
    'vp_logdet_second_response_and_stability.py',
]

def run_one(script: str) -> dict:
    p = here / script
    if not p.exists():
        return {'script': script, 'status': 'MISSING'}
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    env['OMP_NUM_THREADS'] = '1'
    env['OPENBLAS_NUM_THREADS'] = '1'
    env['MKL_NUM_THREADS'] = '1'
    t = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(p)],
            cwd=here,
            text=True,
            capture_output=True,
            timeout=90,
            env=env,
            encoding='utf-8',
            errors='replace',
        )
        out = proc.stdout.strip()
        status = 'PASS' if proc.returncode == 0 and 'PASS' in out else 'FAIL'
        return {
            'script': script,
            'returncode': proc.returncode,
            'last_stdout': out.splitlines()[-1:] if out else [],
            'stderr_tail': proc.stderr.strip().splitlines()[-2:],
            'seconds': round(time.time() - t, 3),
            'status': status,
        }
    except subprocess.TimeoutExpired as e:
        return {
            'script': script,
            'status': 'TIMEOUT',
            'seconds': round(time.time() - t, 3),
            'stderr_tail': [str(e)],
        }

def main() -> int:
    max_workers = min(4, os.cpu_count() or 1)
    results = []
    with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
        future_map = {ex.submit(run_one, s): s for s in scripts}
        by_script = {}
        for fut in cf.as_completed(future_map):
            r = fut.result()
            by_script[r['script']] = r
    results = [by_script[s] for s in scripts]
    pass_all = all(r.get('status') == 'PASS' for r in results)
    (here / 'run_all_v15_closure_certs_results.json').write_text(
        json.dumps({'pass': pass_all, 'results': results}, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )
    print('PASS_RUN_ALL_V15_CLOSURE_CERTS' if pass_all else 'FAIL_RUN_ALL_V15_CLOSURE_CERTS')
    return 0 if pass_all else 1

if __name__ == '__main__':
    raise SystemExit(main())
