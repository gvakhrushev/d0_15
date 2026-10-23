#!/usr/bin/env python3
"""Exact faithful preparation obstruction at Fourier q=e0+e1.

Verify one explicit polynomial separating functional, not a rank census.
Only pinned literal CAR16 definitions execute. The actual positive-adjoint
Fourier jet keeps all16 coframe and24 independent Lorentz-link columns,
both ordered occupied-shell blocks and the conjugate real-field mode.
No old thermal/root suite runs. Default is read-only; --output saves a receipt.
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


for path, digest in PINS.items():
    check('pin:'+path, hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest)
nodes = [node for node in ast.parse((ROOT/HELPER).read_text()).body
         if isinstance(node, ast.FunctionDef) and node.name == '_creators']
check('only_literal_creator_loader', len(nodes) == 1)
scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, 'exec'), scope)
C_actual, order = scope['_creators'](ROOT)
check('actual_ACDB_order', order == (0, 2, 3, 1))

# The stored functional uses role-ordered wedges. This is an explicit full16
# signed-permutation intertwiner, not a restriction or change of CAR roles.
vac = s.eye(16)[:, 0]
columns = []
for mask in range(16):
    v = vac
    for j in reversed(range(4)):
        if mask & (1 << j):
            v = C_actual[j]*v
    columns.append(v)
S = s.Matrix.hstack(*columns)
check('full16_exterior_basis_isometry', S.T*S == s.eye(16))
C_literal = [S.T*c*S for c in C_actual]
for a in range(4):
    standard = s.zeros(16)
    for mask in range(16):
        if not (mask & (1 << a)):
            standard[mask | (1 << a), mask] = (-1)**bin(mask & ((1 << a)-1)).count('1')
    check('literal_role_intertwiner_%d' % a, C_literal[a] == standard)
    for b in range(4):
        check('full_CAR_%d%d' % (a, b),
              C_literal[a]*C_literal[b].T+C_literal[b].T*C_literal[a]
              == (s.eye(16) if a == b else s.zeros(16)))

# Polynomial arithmetic is exact. No interpolation, numerical tolerance,
# rank computation, fitted a/b or optional acceleration package is required.
r = s.Symbol('r', real=True)
phase_expression = (1+s.I)/s.sqrt(2)
K0 = s.QQ.algebraic_field(phase_expression)
K = K0.poly_ring(r)
zero, one = K.zero, K.one
cv = lambda e: K.from_sympy(s.sympify(e))
rp, tp, tm = cv(r), cv(phase_expression), cv(s.conjugate(phase_expression))
C = [[[cv(x) for x in row] for row in c.tolist()] for c in C_literal]
eta = (1, -1, -1, -1)


def add(A, B):
    return [[x+y for x, y in zip(a, b)] for a, b in zip(A, B)]


def scale(A, z):
    return [[x*z for x in row] for row in A]


def transpose(A):
    return list(map(list, zip(*A)))


def mm(A, B):
    return [[sum((x*y for x, y in zip(a, b) if x and y), zero)
             for b in zip(*B)] for a in A]


def summ(matrices):
    out = [[zero]*16 for _ in range(16)]
    for matrix in matrices:
        out = add(out, matrix)
    return out


def conjugate_polynomial(value):
    result = zero
    for (degree,), coefficient in value.items():
        # ANP.to_list is descending order in zeta8.
        cbar = zero
        for power, rational in enumerate(reversed(coefficient.to_list())):
            cbar += cv(s.Rational(str(rational)))*tm**power
        result += cbar*rp**degree
    return result


u = [[(rp if a == b else one)*eta[b] for b in range(4)] for a in range(4)]
creation = lambda v: summ([scale(C[j], v[j]) for j in range(4)])
cr = [creation(v) for v in u]
generators, exterior = [], []
for a in range(4):
    for b in range(a+1, 4):
        omega = s.zeros(4)
        omega[a, b], omega[b, a] = 1, -eta[a]*eta[b]
        check('proper_Lorentz_tangent_%d%d' % (a, b),
              omega.T*s.diag(*eta)+s.diag(*eta)*omega == s.zeros(4))
        generators.append(omega)
        exterior.append(summ([scale(mm(C[i], transpose(C[j])), cv(omega[i, j]))
                              for i in range(4) for j in range(4) if omega[i, j]]))

separator_path = HERE/'SPATIAL_SHELL_SEPARATOR.json'
separator_bytes = separator_path.read_bytes()
separator = json.loads(separator_bytes)
weights = {}
for entry in separator['entries']:
    index = entry['row_major_entry']
    check('unique_separator_entry_%d' % index, index not in weights and 0 <= index < 256)
    polynomial = zero
    check('separator_degree_bound_%d' % index, len(entry['r_coefficients_zeta8_basis']) == 5)
    for degree, coefficients in enumerate(entry['r_coefficients_zeta8_basis']):
        check('separator_field_basis_%d_%d' % (index, degree), len(coefficients) == 4)
        polynomial += rp**degree*sum((cv(s.Rational(c))*tp**j
                                     for j, c in enumerate(coefficients)), zero)
    weights[index] = polynomial


def functional(matrix):
    return sum((weight*matrix[index//16][index % 16]
                for index, weight in weights.items()), zero)


def dirac(axis, sign):
    phase = tp if sign == 1 else tm
    inverse = tm if sign == 1 else tp
    return add(scale(cr[axis], phase-one), scale(transpose(cr[axis]), inverse-one))


def block(kind, role, slot, incoming, outgoing, qsign=1, wrong_adjoint=False):
    """k=-qsign*e_incoming, l=qsign*e_outgoing, ell=b=1.

    Coefficients of the q Fourier mode are complex-linear: only fixed real
    CAR/Lorentz matrices are transposed in the incoming adjoint. The phase
    is evaluated at l there; evaluating it at k is a different stencil.
    """
    phase = tm if qsign == 1 else tp
    tk = phase if role == incoming else one
    tl_bar = phase if role == outgoing else one
    if kind == 'coframe':
        derivative = add(scale(C[slot], tk-one), scale(transpose(C[slot]), tl_bar-one))
    else:
        G = exterior[slot]
        incoming_adjoint = (mm(transpose(cr[role]), transpose(G)) if wrong_adjoint
                            else mm(transpose(G), transpose(cr[role])))
        derivative = add(scale(mm(cr[role], G), tk), scale(incoming_adjoint, tl_bar))
    Dk, Dl = dirac(incoming, -qsign), dirac(outgoing, qsign)
    return add(mm(Dl, derivative), mm(derivative, Dk))


# f = 2*dq01 + t*(dq00+dq11), with PHYSICAL q=u eta u^T.
f = [zero]*40
for j in range(4):
    f[j] = 2*(u[1][j]+tp*u[0][j])*eta[j]
    f[4+j] = 2*(u[0][j]+tp*u[1][j])*eta[j]
checked_columns = 0
wrong_adjoint_rejected = False
for kind, slots in (('coframe', 4), ('link', 6)):
    for role in range(4):
        for slot in range(slots):
            column = role*4+slot if kind == 'coframe' else 16+role*6+slot
            # Both occupied ordered pairs are retained, with full16 outputs.
            ordered_blocks = {}
            for incoming, outgoing in ((0, 1), (1, 0)):
                plus = block(kind, role, slot, incoming, outgoing)
                minus = block(kind, role, slot, incoming, outgoing, qsign=-1)
                ordered_blocks[incoming, outgoing] = (plus, minus)
                check('real_Fourier_pair_%d_%d%d' % (column, incoming, outgoing),
                      all(conjugate_polynomial(plus[i][j]) == minus[i][j]
                          for i in range(16) for j in range(16)))
                if incoming == 0:
                    check('polynomial_separator_column_%d' % column,
                          functional(plus) == (rp**2-one)*f[column])
            forward = ordered_blocks[0, 1][0]
            reversed_conjugate_mode = ordered_blocks[1, 0][1]
            check('actual_Hermitian_reversed_pair_%d' % column,
                  all(conjugate_polynomial(forward[j][i]) == reversed_conjugate_mode[i][j]
                      for i in range(16) for j in range(16)))
            if kind == 'link' and not wrong_adjoint_rejected:
                wrong_adjoint_rejected = bool(functional(
                    block(kind, role, slot, 0, 1, wrong_adjoint=True)))
            checked_columns += 1
check('all16_coframe_and24_link_columns', checked_columns == 40)
check('wrong_incoming_adjoint_order_rejected', wrong_adjoint_rejected)

# All three observer columns are included modulo independent Lorentz links:
# du_r=-B_j u_r, dM_r=(exp(i q_r)-1) B_j. Links already annihilate the
# functional individually, so these are exact retained-variable identities.
for j in range(1, 4):
    du = [[zero]*4 for _ in range(4)]
    for role in range(4):
        du[role][0], du[role][j] = -u[role][j], -u[role][0]
    check('observer_%d_annihilation' % j,
          sum((f[role*4+i]*du[role][i] for role in range(4) for i in range(4)), zero) == zero)

# A true physical-metric lift of dq00=1 exists as a field variation; it is
# its PREPARATION lift that is obstructed. Here F^-1 is explicit for r>1.
Finv = (s.eye(4)-s.ones(4)/(r+3))/(r-1)
U = ((r-1)*s.eye(4)+s.ones(4))*s.diag(*eta)
dq = s.zeros(4)
dq[0, 0] = 1
du = dq*Finv/2
metric_jet = du*s.diag(*eta)*U.T+U*s.diag(*eta)*du.T
check('actual_deltaq00_coframe_lift', all(s.cancel(x) == 0 for x in metric_jet-dq))
evaluated = sum(K.to_sympy(f[role*4+i])*du[role, i]
                for role in range(4) for i in range(4))
check('physical_deltaq00_separator_nonzero', s.simplify(evaluated-phase_expression) == 0)
check('positive_Gram_substitution_rejected', f[1] != 2*(u[1][1]+tp*u[0][1]))

b, ell = s.symbols('b ell', positive=True)
x00, x01, x11 = s.symbols('dq00 dq01 dq11')
physical_covector = 2*x01+phase_expression*(x00+x11)
rescaled = b**2/ell**2*(r**2-1)*(2*x01/b**2+phase_expression*(x00+x11)/b**2)
check('restore_actual_b_and_ell', s.simplify(rescaled-(r**2-1)*physical_covector/ell**2) == 0)

result = {
    'status': 'PASS', 'check_count': len(CHECKS), 'checks': CHECKS,
    'coframe_columns': 16, 'independent_Lorentz_link_columns': 24,
    'retained_observer_columns': 3, 'ordered_shell_blocks': 2,
    'each_block_shape': [16, 16], 'reference_dimension': 128,
    'faithful_support_rank': 8*16, 'Fourier_q': [1, 1, 0, 0],
    'physical_metric': 'q=u eta u^T, eta=diag(1,-1,-1,-1)',
    'necessary_preparation_condition': '2 deltaq01+exp(i*pi/4)*(deltaq00+deltaq11)=0',
    'separator_identity': 'sum L_ij(a/b)*deltaDelta_ij=((a/b)^2-1)/ell^2*(2 deltaq01+exp(i*pi/4)*(deltaq00+deltaq11))',
    'parameter_scope': 'all real a>b>0, ell>0; both real Fourier conjugates retained',
    'full_rank_classification_claimed': False, 'balanced_rank8_classification_claimed': False,
    'physical_GR_proved': False, 'root_or_thermal_suite_replayed': False,
    'source_sha256': PINS,
    'separator_sha256': hashlib.sha256(separator_bytes).hexdigest(),
    'python': platform.python_version(), 'sympy': s.__version__,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
rendered = json.dumps(result, indent=2)+'\n'
if args.output is not None:
    args.output.write_text(rendered)
print(rendered, end='')
