#!/usr/bin/env python3
"""One original one-boost alphabet count, consumed by stationary occupation.

Exact finite Walsh coefficients determine the support. The two native checks
confirm those declared sets, rather than estimating a rank or support cutoff.
No preparation certificate or previous source suite is executed.
"""
from __future__ import annotations

import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


CHECKS: list[str] = []


def require(condition: bool, name: str) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def sign(label: int, word: int) -> int:
    return (-1) ** ((label & word).bit_count() % 2)


def add(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def scale(n: int, x: tuple[int, int]) -> tuple[int, int]:
    return n*x[0], n*x[1]


def exact_support() -> tuple[dict, list[int], list[int]]:
    phases = [(0, 1), (0, 1), (-1, 0), (0, -1)]
    odd_coefficients = {}
    even_coefficients = {}
    for label in range(32):
        odd = []
        even = [0]*5  # Coefficients of I,n0,n1,n2,n3; all roots scaled by5.
        for role in range(4):
            ss = [sum(sign(label, 8*role+2*a+d) for d in (0, 1))
                  for a in range(4)]
            phase = phases[role]
            conjugate = phase[0], -phase[1]
            odd.extend((add(scale(ss[0], phase), (-ss[2], 0)),
                        add(scale(ss[1], conjugate), (-ss[3], 0))))
            # L=I-n/5 and R=4I/5+n/5 at the unchanged nu=3/5.
            even[0] += 5*ss[0]+4*ss[1]-5*ss[2]-4*ss[3]
            even[role+1] += -ss[0]+ss[1]+ss[2]-ss[3]
        odd_coefficients[label] = odd
        even_coefficients[label] = even

    odd_active = [lab for lab, row in odd_coefficients.items() if any(v != (0, 0) for v in row)]
    even_active = [lab for lab, row in even_coefficients.items() if any(row)]
    require(odd_active == list(range(0, 32, 2)), 'exact coefficient-zero rows: all16 even Walsh labels')
    require(even_active == [4, 6, 14, 22, 30], 'exact flat coefficient-one rows: five declared Walsh labels')
    require(all(not any(even_coefficients[lab]) and
                not any(v != (0, 0) for v in odd_coefficients[lab])
                for lab in range(1, 32, 2)), 'duplicate-word cancellation for every odd Walsh label')
    require(all(any(v != (0, 0) for v in odd_coefficients[lab][6:8])
                for lab in range(0, 32, 2)), 'unchanged role3 prevents coefficient-zero row cancellation')

    # Only the boosted role1 right defect contains the new 10<->01 entry.
    boost_entry_coefficients = [sign(lab, 10)+sign(lab, 11) for lab in range(32)]
    require(all(abs(boost_entry_coefficients[lab]) == 2 for lab in range(0, 32, 2)),
            'every even Walsh coefficient-one row has nonzero boosted right-root coefficient')
    require(all(boost_entry_coefficients[lab] == 0 for lab in range(1, 32, 2)),
            'the boosted right-root entry still cancels for odd Walsh labels')
    nu, sh, ch = F(3, 5), F(3, 4), F(5, 4)
    cc = sh*sh+ch*ch
    require(ch*ch-sh*sh == 1 and cc == F(17, 8), 'exact nonzero-boost hyperbolic scalar fixture')
    require(0 < 1-nu*nu*cc == F(47, 200) < 1 and ch*sh/cc == F(15, 34),
            'strict Julia defect and nonzero analytic offdiagonal factors')

    flat_rows = [(lab, 0) for lab in odd_active]+[(lab, 1) for lab in even_active]
    boost_rows = [(lab, b) for lab in range(0, 32, 2) for b in (0, 1)]
    flat = sorted(4*lab+2*b+s for lab, b in flat_rows for s in (0, 1))
    boost = sorted(4*lab+2*b+s for lab, b in boost_rows for s in (0, 1))
    extra_flat = [18, 19, 26, 27, 58, 59, 90, 91, 122, 123]
    require(flat == sorted([a for a in range(128) if a & 6 == 0]+extra_flat),
            'exact flat original label list')
    require(boost == [a for a in range(128) if a & 4 == 0], 'exact boosted original label list')
    require(len(flat) == 42 and len(boost) == 64 and set(flat) < set(boost),
            'named active-count factors42 and64 with22 born output labels')
    return {'status': 'EXACT_PASS', 'flat_walsh_coefficient_zero': odd_active,
            'flat_walsh_coefficient_one': even_active,
            'active_labels_flat': flat, 'active_labels_nonzero_boost': boost,
            'new_labels_at_nonzero_boost': sorted(set(boost)-set(flat)),
            'active_count_flat': len(flat), 'active_count_nonzero_boost': len(boost),
            'uncapped_stationary_trial_factor_if_occupation_hypotheses_hold':
                {'flat': len(flat)+1, 'nonzero_boost': len(boost)+1},
            'exact_scalar_fixture': {'nu': str(nu), 'sinh_theta': str(sh),
                                     'cosh_theta': str(ch), 'defect_argument': str(1-nu*nu*cc),
                                     'offdiagonal_prefactor': str(ch*sh/cc)}}, flat, boost


def native_points(flat: list[int], boost: list[int]) -> dict:
    import numpy as np
    import scipy
    from scipy.linalg import expm, solve_sylvester

    source = Path(__file__).resolve().parents[1]/'d0_book_uniform_source_2026-10-21'/'check_uniform_book_source.py'
    raw = source.read_bytes()
    git_blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(git_blob == 'ee8de4635d24c668949ac9a0186616ab7d59f2ed', 'unchanged native constructor input blob')
    names = {'adj', 'herm', 'root', 'creators', 'native'}
    parsed = ast.parse(raw, filename=str(source))
    selected = [node for node in parsed.body if
                (isinstance(node, ast.FunctionDef) and node.name in names) or
                (isinstance(node, ast.Assign) and any(isinstance(v, ast.Name) and v.id in {'P', 'EYE'}
                                                    for v in node.targets))]
    require(len(selected) == 7, 'read only the five unchanged constructor functions and two constants')
    env = {'np': np, 'expm': expm, 'solve_sylvester': solve_sylvester}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(source), 'exec'), env)
    outputs = {}
    for theta, predicted in ((0.0, flat), (0.08, boost)):
        kraus, _ = env['native'](theta, nu=0.6)
        norms = np.linalg.norm(kraus, axis=(1, 2))
        inactive = sorted(set(range(128))-set(predicted))
        minimum = float(min(norms[predicted]))
        maximum = float(max(norms[inactive]))
        eps = float(np.finfo(float).eps)
        require(maximum < 64*eps, f'predicted inactive native columns vanish to floating arithmetic theta={theta}')
        require(minimum > 1000*max(maximum, eps), f'predicted active columns are separated from floating cancellation theta={theta}')
        outputs[str(theta)] = {'formula_predicted_active_count': len(predicted),
                               'minimum_predicted_active_frobenius_norm': minimum,
                               'maximum_predicted_inactive_frobenius_norm': maximum,
                               'nu': 0.6}
    return {'status': 'NUMERICAL_PASS', 'source_git_blob': git_blob,
            'source_sha256': hashlib.sha256(raw).hexdigest(),
            'numpy_version': np.__version__, 'scipy_version': scipy.__version__,
            'scope': 'Only formula-predicted original column supports at theta0 and .08; no rank, fixed-point, geometry or source suite',
            'points': outputs}


def main() -> None:
    exact, flat, boost = exact_support()
    numerical = native_points(flat, boost)
    result = {'status': 'PASS', 'GR_closed': False,
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'exact': exact, 'numerical': numerical,
              'preparation': 'Consumed from d0_native_preparation_closure_2026-10-21/PROOF.md sections1-4; not retested',
              'support_boundary': '42 at theta0;64 at nonzero admissible boost; the uncapped m+1 factor is not differentiable through theta0',
              'checks': CHECKS, 'check_count': len(CHECKS)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
