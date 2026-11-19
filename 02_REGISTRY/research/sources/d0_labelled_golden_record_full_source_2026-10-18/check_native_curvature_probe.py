#!/usr/bin/env python3
"""Actual finite native H+J+R curvature probe.

Default execution is read-only; --output explicitly saves a receipt.
Only literal helper definitions are loaded; no historical suites run.
The analytic all-size result is in the consuming source owner, section8.9.
This is not a decomposition into EH/observer/torsion or a D0 no-go.
"""
import argparse
import ast
import platform
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HELPER = '02_REGISTRY/research/sources/d0_complete_record_channel_2026-10-17/check_flat_relaxation.py'
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
STAR = '02_REGISTRY/research/sources/d0_af_star_full_lattice_2026-10-17/star_euler.py'
PINS = {
    HELPER: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    STAR: '95de1dca7b7ec738a83ff74a74547a26a6e545d0e55ef601b8c1922d8112f5b5',
}
CHECKS = []


def check(name, condition):
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def eq(name, actual, expected):
    difference = actual-expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    check(name, all(s.cancel(s.expand(x)) == 0 for x in entries))


for path, digest in PINS.items():
    check('pin:'+path, hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest)
nodes = [n for n in ast.parse((ROOT/HELPER).read_text()).body
         if isinstance(n, ast.FunctionDef) and n.name in {'_creators', '_native_rows'}]
check('only_two_pinned_literal_helpers', len(nodes) == 2)
scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, 'exec'), scope)
C, order = scope['_creators'](ROOT)
check('actual_ACDB_order', order == (0, 2, 3, 1))
I16, O16 = s.eye(16), s.zeros(16)
eta = s.diag(1, -1, -1, -1)

# Preserve the real actual64 row/128 port contract at one exact flat fixture.
phases = [s.I, -1, s.Rational(3, 5)+4*s.I/5, 1]
signed_C = [eta[r, r]*C[r] for r in range(4)]
rows, _, _ = scope['_native_rows'](signed_C, s.Rational(3, 5), s.Rational(4, 5), phases)
A = rows[0][2]
D = s.Rational(3, 5)*sum((signed_C[r]*(phases[r]-1)
                         +signed_C[r].H*(s.conjugate(phases[r])-1)
                         for r in range(4)), O16)
eq('actual_blank_block_A_equals_ellD_over16', A, D/16)
p = s.Symbol('p', positive=True)
effect_sum = s.zeros(16)
for label, coefficient, N in rows:
    delta = I16 if (label, coefficient) == (0, 0) else O16
    W = delta-2*N.H*A
    for K in (p*delta+p**2*W, s.sqrt(p)*p*(W-delta)):
        effect_sum += K.H*K
effect_sum = effect_sum.subs(s.conjugate(s.sqrt(p)), s.sqrt(p))
check('all128_outcomes_retained', len(rows)*2 == 128)
check('full128_operator_probability_normalization',
      all(s.rem(s.expand(x), p*p+p-1, p) == 0 for x in effect_sum-I16))

# ALL four momentum phases remain symbolic. No heat/spectrum enumeration.
z = s.symbols('z0:4', nonzero=True)
Q = s.Symbol('Q', nonzero=True)
nu, ell = s.symbols('nu ell', positive=True)
gamma = nu/ell
zl = list(z)
zl[2] = Q*z[2]


def flat_D(ph):
    return gamma*sum((eta[r, r]*(C[r]*(ph[r]-1)+C[r].T*(1/ph[r]-1))
                      for r in range(4)), O16)


Dk, Dl = flat_D(z), flat_D(zl)
G23 = C[2]*C[3].T-C[3]*C[2].T
Js = -gamma*(C[0]*(z[0]-1)+C[0].T*(1/z[0]-1))/2
# This includes the ACTUAL +q sine Fourier coefficient 1/(2i).
Jt_lk = gamma/(2*s.I)*(-C[3]*G23*z[3]+G23*C[3].T/z[3])
Jt_kl = -Jt_lk
N3 = C[3]*C[3].T
eq('actual_connection_variation_simplifies_with_occupation', Jt_lk,
   gamma/(2*s.I)*N3*(C[2]*z[3]+C[2].T/z[3]))
eq('internal_Js_Jt_anticommutator', Js*Jt_lk+Jt_lk*Js, O16)
Ds_kl = Dk*Js+Js*Dl
Ds_lk = Dl*Js+Js*Dk
Dt_lk = Dl*Jt_lk+Jt_lk*Dk
Dt_kl = Dk*Jt_kl+Jt_kl*Dl
Tf = s.factor(s.trace(Ds_kl*Dt_lk))
Tr = s.factor(s.trace(Ds_lk*Dt_kl))
a0 = (z[0]-1)*(1/z[0]-1)
bracket = (zl[2]+z[2]-2)/z[3]+(1/zl[2]+1/z[2]-2)*z[3]
expected = 2*gamma**4/s.I*a0*bracket
eq('full16_forward_edge_trace_including_sine_i', Tf, expected)
eq('actual_reverse_edge_cancellation', Tf+Tr, 0)


def adjoint_unit_phase(M):
    # Phases have unit modulus; all physical coefficient parameters are real.
    mapping = {s.I: -s.I, Q: 1/Q, **{v: 1/v for v in z}}
    return M.T.xreplace(mapping)


eq('Ds_is_actual_Hermitian_Fourier_tangent', Ds_lk, adjoint_unit_phase(Ds_kl))
eq('Dt_is_actual_Hermitian_Fourier_tangent', Dt_kl, adjoint_unit_phase(Dt_lk))
eq('forward_trace_pure_imaginary_after_actual_amplitudes', Tf+adjoint_unit_phase(s.Matrix([Tf]))[0], 0)

# Evaluate the EXISTING star_euler density, not a replacement contraction.
# Constant orientation-preserving orthogonal change diag(+---)->null basis.
T = s.Matrix([[1/s.sqrt(2), 1/s.sqrt(2), 0, 0],
              [1/s.sqrt(2), -1/s.sqrt(2), 0, 0],
              [0, 0, -1, 0], [0, 0, 0, 1]])
eta_null = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
eq('proper_constant_metric_basis_change', T.T*eta*T, eta_null)
eq('proper_constant_orientation', T.det(), 1)
ss, tt, h = s.symbols('ss tt h', real=True)
B23 = s.zeros(4)
B23[2, 3], B23[3, 2] = 1, -1
Bnull = T.T*B23*T


def coframe(site):
    c = s.cos(s.pi*site[2]/2)
    return h/nu*T.T*s.diag(1+ss*c, 1, 1, 1)


def link(site, axis, inv=False):
    if axis != 3:
        return s.eye(4)
    angle = tt*s.sin(s.pi*site[2]/2)*(-1 if inv else 1)
    return s.eye(4)+s.sin(angle)*Bnull+(1-s.cos(angle))*Bnull**2


names = {'shift', 'edges', 'plaquette', 'wedge', 'pairing', 'density'}
star_nodes = [node for node in ast.parse((ROOT/STAR).read_text()).body
              if isinstance(node, ast.FunctionDef) and node.name in names]
check('only_generic_star_density_helpers', len(star_nodes) == len(names))
star_scope = {'s': s, 'lru_cache': lru_cache, 'I': s.eye(4), 'ETA': eta_null,
              'PAIRS': list(combinations(range(4), 2)), 'EPS': lambda x: s.LeviCivita(*x),
              'coframe': coframe, 'link': link}
exec(compile(ast.Module(body=star_nodes, type_ignores=[]), STAR, 'exec'), star_scope)
star_cycle = s.simplify(sum(s.diff(star_scope['density']((0, 0, j, 0)), ss, tt)
                          .subs({ss: 0, tt: 0}) for j in range(4)))
eq('actual_star_density_transverse_L4_cycle_nonzero', star_cycle, -2*h*h/nu**2)
result = {'status': 'PASS', 'checks': CHECKS, 'check_count': len(CHECKS),
          'trace_forward_full16': str(Tf), 'trace_reverse_plus_forward': str(s.simplify(Tf+Tr)),
          'full_HJR_mixed_source': '0: analytic divided-difference proof in paired edges',
          'actual_star_mixed_L4_transverse_cycle': str(star_cycle),
          'full_L4_four_torus_star_mixed': str(4**3*star_cycle),
          'all128_probability_normalization_checked': True,
          'complete128_Shannon_mixed_source_evaluated': False,
          'native_action_no_go': False, 'D0_to_GR_proved': False,
          'physical_native_palatini_coefficient': None,
          'python': platform.python_version(), 'sympy': s.__version__,
          'source_sha256': PINS}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, help='Opt-in receipt destination')
args = parser.parse_args()
rendered = json.dumps(result, indent=2) + '\n'
if args.output is not None:
    args.output.write_text(rendered)
print(rendered, end='')
