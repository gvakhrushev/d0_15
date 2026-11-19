#!/usr/bin/env python3
"""Bounded exact checks for the full-Lorentz homogeneous stationary reduction.

Only literal CAR definitions are loaded; no old root/thermal suite is run.
The general rank27 and nonlinear IFT arguments are in the source owner §8.10.
Default execution is read-only; --output opts into saving the receipt.
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
HELPER = '02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py'
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    HELPER: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}
CHECKS = []


def check(name, condition):
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def eq(name, actual, expected):
    difference = actual-expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    check(name, all(s.expand(x).simplify() == 0 for x in entries))


for path, digest in PINS.items():
    check('pin:'+path, hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest)
nodes = [node for node in ast.parse((ROOT/HELPER).read_text()).body
         if isinstance(node, ast.FunctionDef) and node.name == '_creators']
check('only_literal_creator_loader', len(nodes) == 1)
scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, 'exec'), scope)
C, order = scope['_creators'](ROOT)
check('actual_ACDB_order', order == (0, 2, 3, 1))
eta, zero = s.diag(1, -1, -1, -1), s.zeros(16)
vac = s.eye(16)[:, 0]


def creation(v):
    return sum((v[j]*C[j] for j in range(4)), s.zeros(16))


def exterior_generator(omega):
    return sum((omega[i, j]*C[i]*C[j].T for i in range(4) for j in range(4)),
               s.zeros(16))


# Verify the actual vacuum/one-particle identity for ALL six Lorentz directions.
v = s.Matrix(s.symbols('v0:4', real=True))
generators = []
for i in range(4):
    for j in range(i+1, 4):
        omega = s.zeros(4)
        omega[i, j], omega[j, i] = 1, -eta[i, i]*eta[j, j]
        generators.append(omega)
        G = exterior_generator(omega)
        eq('Lorentz_metric_compatibility_%d%d' % (i, j), omega.T*eta+eta*omega, s.zeros(4))
        eq('vacuum_annihilation_%d%d' % (i, j), G*vac, s.zeros(16, 1))
        eq('actual_one_particle_generator_%d%d' % (i, j),
           G*creation(v)*vac, creation(omega*v)*vac)

# The tensor used in the analytic injectivity proof has no nonzero solution.
tensor = s.symbols('t0:64')
def t(a, b, c):
    return tensor[16*a+4*b+c]
equations = []
for a in range(4):
    for b in range(4):
        for c in range(4):
            equations.extend([t(a, b, c)-t(b, a, c), t(a, b, c)+t(a, c, b)])
matrix, rhs = s.linear_eq_to_matrix(equations, tensor)
eq('symmetric_ab_antisymmetric_bc_only_zero', matrix.rank(), 64)

# Independent actual CAR obstruction to retaining an arbitrary connection.
a, b, ell = s.symbols('a b ell', positive=True)
F = (a-b)*s.eye(4)+b*s.ones(4)
u = [eta*F.row(r).T for r in range(4)]
phase = (1+s.I)/s.sqrt(2)
zeta = phase-1
D = (zeta*creation(u[3])+s.conjugate(zeta)*creation(u[3]).T)/ell
G = exterior_generator(generators[0])  # B01 on the independent role2 link
dD = (creation(u[2])*G+G.T*creation(u[2]).T)/ell
X = D*dD+dD*D
eq('independent_boost_scalar_vacuum_entry', (vac.T*X*vac)[0], 0)
eq('independent_boost_nonscalar_full16_trace', s.trace(X)/16,
   b*b*(s.sqrt(2)-2)/ell**2)
check('trace_vacuum_mismatch_nonzero', s.sqrt(2)-2 != 0)

# All three observer components, with the physical inverse-frame convention.
nu = s.Matrix([0, *s.symbols('nu1:4', real=True)])
e0 = s.eye(4)[:, 0]
dGram = 2*F*(e0*nu.T+nu*e0.T)*F.T
diffs = s.Matrix([dGram[i, i]-dGram[0, 0] for i in range(1, 4)])
J = diffs.jacobian(list(nu)[1:])
expected = 4*b*(a-b)*(s.eye(3)-s.ones(3))
eq('actual_observer_equal_diagonal_jacobian', J, expected)
eq('observer_jacobian_determinant', J.det(), -128*b**3*(a-b)**3)
eq('observer_jacobian_inverse', J*(s.eye(3)-s.ones(3)/2)/(4*b*(a-b)), s.eye(3))

result = {
    'status': 'PASS', 'check_count': len(CHECKS), 'checks': CHECKS,
    'homogeneous_retained_rank': '27, analytic proof in owner section8.10',
    'translation_invariant_density_coordinates': 8*16**2-1,
    'neutral_density_parameters': 8*16**2-1-27,
    'full16_boost_trace_over16': str(b*b*(s.sqrt(2)-2)/ell**2),
    'physical_GR_proved': False, 'inhomogeneous_metric_section_proved': False,
    'root_or_thermal_suite_replayed': False,
    'source_sha256': PINS, 'python': platform.python_version(), 'sympy': s.__version__,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
rendered = json.dumps(result, indent=2)+'\n'
if args.output is not None:
    args.output.write_text(rendered)
print(rendered, end='')
