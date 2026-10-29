#!/usr/bin/env python3
"""Independent finite numerical checks of pinned Book03 moving-cut first source.

The exact checker is imported without changes. Independent source evaluation uses
SciPy's full matrix exponential Frechet derivative, not exp(A) times dA.
This is not a native 42-component field replay, Lean proof or physical admission.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm, expm_frechet

root = Path(__file__).resolve().parent
source = root.parent / 'd0_root_moving_cut_2026-10-28' / 'check_root_moving_cut.py'
expected_sha256 = 'da4df4d9c075b9b6cc01a4c74503ea1bb379d062bdbb74e5ddb02703f2f85d2c'
if hashlib.sha256(source.read_bytes()).hexdigest() != expected_sha256:
    raise RuntimeError('Pinned original checker hash mismatch')
spec = importlib.util.spec_from_file_location('original_checker', source)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
seed = 2026102802
rng = np.random.default_rng(seed)
maxes = {'source_vs_frechet': 0., 'beta_partial_fd': 0., 'z_partial_fd': 0.,
         'co_transport': 0., 'noncommuting_heat_gap': 0.}
rows = []
for n in range(2, 7):
    for rank in range(n + 1):
        def hermitian():
            a = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
            return (a + a.conj().T) / (2 * np.sqrt(n))
        P = np.diag([1] * rank + [0] * (n - rank)).astype(complex)
        U = expm(1j * hermitian())
        Delta = hermitian()
        W = 1j * hermitian()
        X = 1j * hermitian()
        extra_Delta = hermitian() / 5
        beta, z = .43, .37
        dP = original.comm(W, P)
        dU = original.comm(W, U) + X @ U
        dDelta = original.comm(W, Delta) + extra_Delta
        direct, relative, bound, tangent_error, covariant_error = original.first_source(
            U, P, Delta, dU, dP, dDelta, beta, z)
        Q = np.eye(n) - P
        C = Q @ U @ P
        dC = -dP @ U @ P + Q @ dU @ P + Q @ U @ dP
        F = C.conj().T @ C
        dF = dC.conj().T @ C + C.conj().T @ dC
        R = np.linalg.inv(np.eye(n) - z * F)
        Zmat = expm(-beta * Delta)
        dZmat = expm_frechet(-beta * Delta, -beta * dDelta, compute_expm=False)
        frechet = float((np.trace(dZmat) / (beta * np.trace(Zmat)) + z * np.trace(R @ dF)).real)
        Z = float(np.trace(Zmat).real)
        rho = Zmat / Z
        beta_partial = float(-np.log(Z) / beta**2 - np.trace(rho @ Delta).real / beta)
        z_partial = float(np.trace(R @ F).real)
        beta_fd = original.fd5(lambda t: original.value(U, P, Delta, beta + t, z))
        z_fd = original.fd5(lambda t: original.value(U, P, Delta, beta, z + t))
        gauge = original.first_source(U, P, Delta, original.comm(W, U), dP,
                                     original.comm(W, Delta), beta, z)[0]
        naive = expm(-beta * Delta) @ (-beta * dDelta)
        gap = float(np.linalg.norm(dZmat - naive))
        # Check every raw numerical output before max(): max(0.0, NaN) can
        # silently return 0.0, including under Python's optimized mode.
        numeric_outputs = {'direct': direct, 'relative': relative, 'bound': bound,
                           'tangent_error': tangent_error, 'covariant_error': covariant_error,
                           'frechet': frechet, 'beta_partial': beta_partial, 'beta_fd': beta_fd,
                           'z_partial': z_partial, 'z_fd': z_fd, 'gauge': gauge, 'gap': gap}
        for name, value in numeric_outputs.items():
            if not np.isfinite(value):
                raise ArithmeticError(f'Nonfinite {name} at n={n}, rank={rank}')
        errors = {'source_vs_frechet': float(max(abs(direct - frechet), abs(relative - frechet))),
                  'beta_partial_fd': float(abs(beta_partial - beta_fd)),
                  'z_partial_fd': float(abs(z_partial - z_fd)),
                  'co_transport': float(abs(gauge)), 'noncommuting_heat_gap': gap}
        for key, value in errors.items():
            if not np.isfinite(value):
                raise ArithmeticError(f'Nonfinite {key} at n={n}, rank={rank}')
        for key in maxes:
            maxes[key] = max(maxes[key], errors[key])
        rows.append({'dimension': n, 'rank': rank, 'direct': direct, 'relative': relative,
                     'frechet_original_derivative': frechet, 'bound': bound,
                     'tangent_error': tangent_error, 'covariant_error': covariant_error,
                     'beta_partial': beta_partial, 'beta_finite_difference': beta_fd,
                     'z_partial': z_partial, 'z_finite_difference': z_fd, **errors})
limits = {'source_vs_frechet': 1e-10, 'beta_partial_fd': 1e-9,
          'z_partial_fd': 1e-9, 'co_transport': 1e-10}
for key, limit in limits.items():
    if not np.isfinite(maxes[key]) or maxes[key] >= limit:
        raise ArithmeticError(f'{key} failed: {maxes[key]} >= {limit}')
if maxes['noncommuting_heat_gap'] <= .01:
    raise ArithmeticError('No noncommuting matrix-exponential negative control')
print(json.dumps({'status': 'PASS_FINITE_NUMERICAL_ONLY',
    'source_commit': 'eebcb5e467742df3e9cf7fa9702042d7294aa742',
    'source_sha256': expected_sha256,
    'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
                 'platform': platform.platform()},
    'inputs': {'seed': seed, 'dimensions': list(range(2, 7)), 'rank_range': '0..n inclusive',
               'beta': .43, 'z': .37, 'five_point_step': 2e-4,
               'data_recipe': 'P=diag(I_rank,0); U=expm(iH1); Delta=H2; W=iH3; X=iH4; extra_Delta=H5/5; H=(A+A*)/(2sqrt(n)); A=normal+i normal',
               'dP': '[W,P]', 'dU': '[W,U]+XU', 'dDelta': '[W,Delta]+extra_Delta'},
    'tolerances': limits, 'required_max_noncommuting_gap_exceeds': .01, 'maxima': maxes,
    'samples': rows, 'scope': 'Finite numerical controls only; no native full42, no Lean, no scientific acceptance or physical source selection.'},
    sort_keys=True, indent=2))
