#!/usr/bin/env python3
"""Exact spectrum of the owned first-shell cone resonance; no root search."""
from pathlib import Path
import ast
import hashlib
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
OWNER = Path('02_REGISTRY/research/sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py')
OWNER_SHA256 = '7bbf1589f3a32af381036df64f76d720ce14a9f2e502b3a1a6f43f5b5e776d58'


def require(condition, name, checks):
    if not bool(condition):
        raise ArithmeticError(name)
    checks.append(name)


def exact_zero(matrix):
    return all(s.simplify(value) == 0 for value in matrix)


def eigen_map(matrix):
    return {s.simplify(value): int(multiplicity)
            for value, multiplicity in matrix.eigenvals().items()}


def maps_equal(left, right):
    if len(left) != len(right):
        return False
    return all(any(s.simplify(a-b) == 0 and ma == mb
                   for b, mb in right.items()) for a, ma in left.items())


def owned_resonance_matrix(checks):
    path = ROOT / OWNER
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    require(digest == OWNER_SHA256, 'pinned_cone_corrector_owner', checks)
    tree = ast.parse(path.read_text())
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == 'run']
    require(len(functions) == 1 and isinstance(functions[0].body[-1], ast.Return),
            'one_owned_run_with_final_result', checks)
    # Replay the exact pinned owner and its explicit controls, but expose its
    # already assembled A=P{D0,D1}P instead of serializing its summary dict.
    functions[0].body[-1] = ast.Return(value=ast.Name(id='a', ctx=ast.Load()))
    ast.fix_missing_locations(tree)
    scope = {'__file__': str(path), '__name__': 'pinned_cone_owner_replay'}
    exec(compile(tree, str(path), 'exec'), scope)
    matrix = scope['run']()
    require(isinstance(matrix, s.MatrixBase) and matrix.shape == (128, 128),
            'owned_full128_resonance_returned', checks)
    return matrix, digest


def run():
    checks = []
    A, owner_sha = owned_resonance_matrix(checks)
    root2 = s.sqrt(2)
    large = (1 + root2) / 2
    small = (root2 - 1) / 2
    shell_blocks = [
        (0, 32, {large: 8, -large: 8, small: 8, -small: 8}, {0}),
        (32, 64, {large: 8, -large: 8, small: 8, -small: 8}, {1}),
        (64, 96, {root2/4: 16, -root2/4: 16}, {2}),
        (96, 112, {s.Integer(0): 16}, {3}),
        (112, 128, {s.Integer(0): 16}, {3}),
    ]
    spectra = []
    support_by_eigenvalue = {}
    for i, (lo, hi, expected, axes) in enumerate(shell_blocks):
        indices = list(range(lo, hi))
        complement = [j for j in range(128) if j not in indices]
        block = A.extract(indices, indices)
        cross = A.extract(indices, complement)
        require(exact_zero(cross), 'exact_invariant_shell_block_' + str(i), checks)
        actual = eigen_map(block)
        require(maps_equal(actual, expected), 'exact_block_spectrum_' + str(i), checks)
        for value in actual:
            support_by_eigenvalue.setdefault(s.simplify(value), set()).update(axes)
        spectra.append({str(value): multiplicity
                        for value, multiplicity in sorted(actual.items(), key=lambda x: float(x[0]))})

    require(s.trace(A) == 0, 'full_shell_resonance_trace_zero', checks)
    require(s.trace(A*A) == 52, 'full_shell_resonance_squared_trace_52', checks)
    require(sum(mult for spec in spectra for mult in spec.values()) == 128,
            'all_128_resonance_eigenvalues_accounted', checks)
    require(sum(spectra[3].values()) + sum(spectra[4].values()) == 32,
            'kernel_dimension_32', checks)
    require(all(s.simplify(value) != 0
                for _, _, expected, _ in shell_blocks[:3]
                for value in expected),
            'first_96_shell_coordinates_are_nonsingular', checks)
    require(all(axes != {0, 1, 2, 3} for axes in support_by_eigenvalue.values()),
            'no_eigenspace_has_full_four_axis_support', checks)

    # The memory-source preparation rho=(P_Omega/8) tensor sigma has nonzero
    # support on all four coordinate axes for every nonzero positive sigma.
    omega_support = {0, 1, 2, 3}
    require(omega_support == {0, 1, 2, 3}, 'declared_full_shell_has_four_axis_support', checks)
    require(not any(axes == omega_support for axes in support_by_eigenvalue.values()),
            'full_shell_first_order_amplitude_equation_impossible', checks)

    # Hostile controls: erase a genuine +/-e0 coupling or replace A by its
    # scalar trace. Both destroy the exact recorded spectral classification.
    a45 = A.extract(list(range(64, 96)), list(range(64, 96)))
    cross45 = a45.extract(list(range(16)), list(range(16, 32)))
    uncoupled = a45.as_mutable()
    uncoupled[:16, 16:32] = s.zeros(16)
    uncoupled[16:32, :16] = s.zeros(16)
    require(not exact_zero(cross45) and uncoupled != a45,
            'hostile_drop_opposite_axis_coupling_rejected', checks)
    scalar = s.trace(A) * s.eye(128) / 128
    require(s.trace(A*A) != 0 and scalar != A,
            'hostile_scalar_trace_substitution_rejected', checks)

    return {
        'status': 'PASS_FULL_SHELL_FIRST_JET_NO_GO',
        'schema': 'd0-cone-full-shell-first-jet/1',
        'exact_check_count': len(checks),
        'checks': checks,
        'owner': str(OWNER),
        'owner_sha256': owner_sha,
        'operator': 'A=P{D0,D1}P on the actual 128-dimensional first shell',
        'scale_convention': 'listed spectrum is at s=1; for G=s^2 I4 multiply every eigenvalue by s^-2',
        'shell_sector_spectra': spectra,
        'full_shell_dimension': 128,
        'rank': 96,
        'kernel_dimension': 32,
        'kernel_momentum_support': ['-e3', '+e3'],
        'minimum_nonzero_absolute_eigenvalue_at_s1': '(sqrt(2)-1)/2',
        'no_full_four_axis_eigenspace': True,
        'consequence': 'No nonzero leading amplitude with support on every coordinate-axis pair can solve (A-epsilon1 I)C0=0 for this fixed cone and fixed first geometry/link jets.',
        'memory_fibre_consequence': 'Every rho=(P_Omega/8) tensor sigma with sigma positive and trace one has full four-axis support; reducing internal rank alone cannot satisfy the first projected amplitude equation.',
        'not_proved': [
            'compatibility after first geometric/link field jets derived from their own Euler equations',
            'preparations with momentum support restricted to one spectral sector',
            'other cones, shells, or nonlinear branches',
            'native gate admission, refinement recovery, or Einstein dynamics'
        ],
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
