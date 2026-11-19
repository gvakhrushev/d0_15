#!/usr/bin/env python3
"""One exact native control for the proposed six-link coercivity.

Load only the pinned CAR creator definition. No historical run(), spectral
census, root solver or full-lattice replay executes. The algebraic parameter
is located by exact endpoint signs, not a numerical near-zero eigenvalue.
Default is read-only; --output explicitly saves the bounded result.
"""
import argparse
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform

import sympy as s


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
SHA = 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da'


def run():
    checks = []

    def require(name, condition):
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    def eq(name, left, right):
        difference = left-right
        values = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(name, all(s.expand(value) == 0 for value in values))

    source = ROOT/SOURCE
    require('literal_source_sha256', hashlib.sha256(source.read_bytes()).hexdigest() == SHA)
    nodes = [node for node in ast.parse(source.read_text()).body
             if (isinstance(node, ast.FunctionDef) and node.name == 'creator')
             or (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
                 and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    require('only_literal_creator_definition_loaded', len(nodes) == 2)
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), SOURCE, 'exec'), scope)
    require('actual_full16_ACDB_order', scope['EXTERIOR_ORDER'] == (0, 2, 3, 1))
    C = [scope['creator'](j) for j in range(4)]
    I, O = s.eye(16), s.zeros(16)
    eta = s.diag(1, -1, -1, -1)

    def char(i, j):
        return (-1)**bin(int(i) & int(j)).count('1')

    H = s.Matrix(4, 4, lambda i, j: s.Rational(char(i, j), 2))
    eq('normalized_four_role_Walsh', H.T*H, s.eye(4))
    creators = [sum((H[j, r]*C[j] for j in range(4)), O.copy()) for r in range(4)]
    x = s.Symbol('x', real=True)
    K = s.zeros(4)
    K[0, 2] = K[2, 0] = K[0, 3] = K[3, 0] = 1
    K[1, 2] = K[1, 3] = x
    K[2, 1] = K[3, 1] = -x
    eq('all_parameter_values_are_true_Lorentz_jets', K.T*eta+eta*K, s.zeros(4))

    # Actual +axis0 on L=4: shifted phase i on role0 and1 elsewhere.
    Z = (s.I-1)*creators[0]+(-s.I-1)*creators[0].T  # 16 A_0
    eq('actual_scalar_energy_shell', Z*Z, 2*I)
    X = O.copy()  # 16 delta A_0, forward-only genuine link jet
    for r in range(4):
        signs = s.diag(*[char(j, r) for j in range(4)])
        omega = signs*K*signs
        eq('Lorentz_role_%d' % r, omega.T*eta+eta*omega, s.zeros(4))
        generator = sum((omega[i, j]*C[i]*C[j].T
                         for i in range(4) for j in range(4)), O.copy())
        phase = s.I if r == 0 else s.S.One
        X += phase*creators[r]*generator + s.conjugate(phase)*generator.T*creators[r].T
    T = s.expand((Z*X+X*Z)/2)  # sqrt(2) times the projected splitting S
    eq('Hermitian_projected_native_splitting', T, T.H)
    eq('same_sign_energy_projection', T*Z, Z*T)
    parity = s.diag(*[(-1)**bin(j).count('1') for j in range(16)])
    eq('retains_both_CAR_parities', T*parity, parity*T)
    eq('zero_full16_trace', s.trace(T), 0)

    F = parity
    for c in C:
        F = F*(c+c.T)
    eq('full_particle_hole_unitary', F*F.T, I)
    for j, c in enumerate(C):
        eq('particle_hole_creator_%d' % j, F*c*F.T, c.T)
    eq('antiunitary_flips_actual_splitting', F*s.conjugate(T)*F.T, -T)

    even = [j for j in range(16) if bin(j).count('1') % 2 == 0]
    polynomial = x**4+10*x**3-10*x**2-2*x+5
    determinant = s.factor(T.extract(even, even).det(method='domain-ge'))
    eq('exact_native_even_determinant', s.expand(determinant), s.expand(polynomial**2/16))
    require('exact_root_interval_left', polynomial.subs(x, -1) == -12)
    require('exact_root_interval_right', polynomial.subs(x, -s.Rational(1, 2)) == s.Rational(37, 16))
    require('nonsingular_control_at_x_zero', determinant.subs(x, 0) == s.Rational(25, 16))
    return {
        'status': 'PASS', 'checks': checks,
        'input_sha256': {SOURCE: SHA},
        'grid': 'L=4, all8 first-shell momenta, CAR16, reference128',
        'positive_axis0_parameter': 'K02+K03+x(R12+R13)',
        'even_determinant': str(determinant),
        'kernel_parameter_interval': ['-1', '-1/2'],
        'scope': 'Refutes state-independent six-link splitting coercivity; not finite-root or GR no-go.',
        'full_joint_root_proved': False, 'physical_GR_proved': False,
        'python': platform.python_version(), 'sympy': s.__version__,
        'old_research_or_Lean_suite_replayed': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, ensure_ascii=False)+'\n'
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end='')
