#!/usr/bin/env python3
"""Exact q=(0,2,0,0) shell/preparation lift on the full-Lorentz carrier.

Only the pinned literal CAR creator helper is loaded. No root, heat, Hessian
or previous run() is executed. Default execution is read-only; --output opts
into saving the receipt. All ranks below are COMPLEX ranks for one q; the
real field contains its conjugate -q as well.

The actual root frame is F=(a-b)I+b11^T, a>b>0, U=eta F^T. On the unique
ordered shell pair k=-e1,l=+e1, put t=exp(-i*pi/4), z=t-1. The full operator
jet is ell J=z beta(w1)+t Z1(Omega1)+sum_(r!=1) Zr(Omegar), where
Zr(Omega)=C(ur) Gamma(Omega)+Gamma(Omega)^T C(ur)^T. The other twelve
coframe coefficients remain present and are shell-invisible.

Cartan's algebraic inverse identifies the 24 Lorentz-link coefficients with
ALL raising cubics B=sum_(i<j,k) B_ijk Ci Cj Ck^T. Thus the active jet space
is exactly beta(v)+B+B^T, of dimension28. A positive orthogonal CAR basis
change can align the nonzero u1 with e0 for an algebraic rank calculation;
this is not an identification of physical Lorentz gauge. The exact rank22
calculation below, together with the Cartan inverse, applies to every
invertible U. Analytically, writing J in active-occupation blocks gives
Boff+Boff^T=0 and z Ddiag+bar(z) Adiag=0. Of the24 cubics, nine all-spatial
ones vanish, three pair terms vanish, the nine one-body terms reduce to
three skew ones, and three remaining terms are fixed by the three spatial
components of v. The active component of v vanishes. Hence kernel dim6.

For each S^T=-S define Lorentz-skew Cr by
sum C(ur) Gamma(Cr)=C(u1) Gamma(S), using the explicit Cartan inverse.
Then w1=S u1, Omega1=(1-i)C1, Omegar=-i sqrt(2)Cr (r!=1) give
J=Gamma(S) Dk-Dl Gamma(S), so Dl J+J Dk=0. Spatial S give the three
ordinary rotation Ward representatives modulo inactive coframes; S0j
give three further representatives and are not Lorentz generators.

The inactive twelve coframes lift exactly the nine metric entries with
delta q11=0. The S01 representative has delta q11=-4ab!=0, so all ten
physical metric variations have a shell-compatible lift with every24
Lorentz link and observer direction retained. This solves only the linear
preparation/shell condition. No internal Euler equation, thermal Hessian,
nonlinear stationary metric section, physical selection or GR is claimed.
"""
import argparse
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform

import sympy as s
from sympy.polys.matrices import DomainMatrix

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
    check(name, all(s.cancel(s.expand(x)) == 0 for x in entries))


def exact_rank(matrix):
    field = s.QQ.algebraic_field(s.sqrt(2), s.I)
    return DomainMatrix.from_Matrix(matrix).convert_to(field).rank()


for relative, digest in PINS.items():
    check('pin:'+relative,
          hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == digest)
nodes = [node for node in ast.parse((ROOT/HELPER).read_text()).body
         if isinstance(node, ast.FunctionDef) and node.name == '_creators']
check('only_literal_creator_helper_loaded', len(nodes) == 1)
scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
exec(compile(ast.Module(body=nodes, type_ignores=[]), HELPER, 'exec'), scope)
C, order = scope['_creators'](ROOT)
check('actual_ACDB_order', order == (0, 2, 3, 1))
I16, O16, eta = s.eye(16), s.zeros(16), s.diag(1, -1, -1, -1)
vac = I16[:, 0]
for i in range(4):
    for j in range(4):
        eq('actual_CAR_%d%d' % (i, j), C[i]*C[j].T+C[j].T*C[i],
           I16 if i == j else O16)


def creation(v):
    return sum((v[i]*C[i] for i in range(4)), s.zeros(16))


def gamma(omega):
    return sum((omega[i, j]*C[i]*C[j].T for i in range(4) for j in range(4)),
               s.zeros(16))


def cartan_inverse(U, H_inverse, u, S):
    """Unique eta-skew Ar with sum C(ur)Gamma(Ar)=C(u)Gamma(S)."""
    lowered_u, lowered_S = eta*u, eta*S
    L = [[[lowered_u[a]*lowered_S[b, c]-lowered_u[b]*lowered_S[a, c]
           for c in range(4)] for b in range(4)] for a in range(4)]
    G = [[[s.expand((L[a][b][c]-L[b][c][a]+L[c][a][b])/2)
           for c in range(4)] for b in range(4)] for a in range(4)]
    result = []
    for r in range(4):
        lowered_A = s.Matrix(4, 4, lambda b, c:
                             sum(H_inverse[r, a]*G[a][b][c] for a in range(4)))
        result.append((eta*lowered_A).applyfunc(s.cancel))
    return result


def ordered_jet(U, w, omega, incoming, outgoing):
    """Complex-linear Fourier jet; adjoint uses OUTGOING momentum."""
    answer = s.zeros(16)
    for r in range(4):
        answer += ((incoming[r]-1)*creation(w[r])
                   +(s.conjugate(outgoing[r])-1)*creation(w[r]).T
                   +incoming[r]*creation(U[:, r])*gamma(omega[r])
                   +s.conjugate(outgoing[r])*gamma(omega[r]).T*creation(U[:, r]).T)
    return answer


a, b = s.symbols('a b', positive=True)  # Actual domain additionally has a>b.
F = (a-b)*s.eye(4)+b*s.ones(4)
F_inverse = s.eye(4)/(a-b)-b*s.ones(4)/((a-b)*(a+3*b))
U = eta*F.T
u = U[:, 1]
eq('actual_frame_inverse', (eta*U)*F_inverse, s.eye(4))
eq('actual_active_spatial_coframe', u, s.Matrix([b, -a, -b, -b]))
tm, tp = (1-s.I)/s.sqrt(2), (1+s.I)/s.sqrt(2)
zm, zp = tm-1, tp-1
eq('phase_difference', zm-zp, -s.I*s.sqrt(2))
eq('active_link_multiplier', -s.I*s.sqrt(2)/tm, 1-s.I)
incoming, outgoing = [1, tm, 1, 1], [1, tp, 1, 1]
Dk, Dl = zm*creation(u)+zp*creation(u).T, zp*creation(u)+zm*creation(u).T
epsilon = (2-s.sqrt(2))*(u.T*u)[0]
eq('actual_shell_Dk_square', Dk**2, epsilon*I16)
eq('actual_shell_Dl_square', Dl**2, epsilon*I16)

representatives = []
for i in range(4):
    for j in range(i+1, 4):
        tag = '%d%d' % (i, j)
        S = s.zeros(4)
        S[i, j], S[j, i] = 1, -1
        eq('positive_skew_S_'+tag, S.T+S, s.zeros(4))
        if i == 0:
            check('extra_S_is_not_Lorentz_'+tag, S.T*eta+eta*S != s.zeros(4))
        else:
            eq('spatial_S_is_Lorentz_'+tag, S.T*eta+eta*S, s.zeros(4))
        A = cartan_inverse(U, F_inverse, u, S)
        for r in range(4):
            eq('Cartan_Lorentz_'+tag+'_'+str(r), A[r].T*eta+eta*A[r], s.zeros(4))
        eq('Cartan_actual_full16_cubic_'+tag,
           sum((creation(U[:, r])*gamma(A[r]) for r in range(4)), s.zeros(16)),
           creation(u)*gamma(S))
        w = [s.zeros(4, 1) for _ in range(4)]
        w[1] = S*u
        omega = [(1-s.I)*A[r] if r == 1 else -s.I*s.sqrt(2)*A[r]
                 for r in range(4)]
        J = ordered_jet(U, w, omega, incoming, outgoing)
        eq('actual_commutator_intertwiner_'+tag, J, gamma(S)*Dk-Dl*gamma(S))
        eq('actual_full16_shell_constraint_'+tag, Dl*J+J*Dk, O16)
        Jminus = ordered_jet(U, [x.conjugate() for x in w],
                            [x.conjugate() for x in omega], outgoing, incoming)
        eq('Fourier_minus_q_reality_'+tag, Jminus, J.H)
        representatives.append((tag, S, w, omega))

# Exact universal rank calculation, NOT a rounded frame/root or matrix scan.
# The Cartan isomorphism and positive orthogonal covariance reduce any u1!=0
# to this one algebraic normal form on the SAME full16 exterior carrier.
canonical_u = s.eye(4)[:, 0]
canonical_Dk = zm*creation(canonical_u)+zp*creation(canonical_u).T
canonical_Dl = zp*creation(canonical_u)+zm*creation(canonical_u).T
J_basis = [C[i]+C[i].T for i in range(4)]
for i in range(4):
    for j in range(i+1, 4):
        for k in range(4):
            B = C[i]*C[j]*C[k].T
            J_basis.append(B+B.T)
check('all_active4_plus_link24_columns_retained', len(J_basis) == 28)
J_matrix = s.Matrix.hstack(*(x.reshape(256, 1) for x in J_basis))
T_matrix = s.Matrix.hstack(*((canonical_Dl*x+x*canonical_Dk).reshape(256, 1)
                            for x in J_basis))
eq('exact_complex_active_jet_dimension', exact_rank(J_matrix), 28)
eq('exact_complex_shell_rank', exact_rank(T_matrix), 22)
canonical_kernel = [gamma(S)*canonical_Dk-canonical_Dl*gamma(S)
                    for _, S, _, _ in representatives]
eq('six_representatives_are_independent',
   exact_rank(s.Matrix.hstack(*(x.reshape(256, 1) for x in canonical_kernel))), 6)
for r in (0, 2, 3):
    check('inactive_role_phases_'+str(r), incoming[r] == outgoing[r] == 1)

# Explicit right inverse for ALL ten physical metric entries. For a symmetric
# residual V with V11=0 choose A_s1=0, A_1r=V_1r and A_sr=V_sr/2 otherwise;
# deltaU=(eta U^{-T})A then has delta u1=0 and deltaq=A+A^T=V.
tag, S, extra_w, extra_omega = representatives[0]  # S01
check('chosen_extra_is_S01', tag == '01')
extra_U = s.zeros(4)
extra_U[:, 1] = extra_w[1]
extra_metric = extra_U.T*eta*U+U.T*eta*extra_U
eq('extra_physical_metric_active_entry', extra_metric[1, 1], -4*a*b)
metric_symbols = s.symbols('v00 v01 v02 v03 v11 v12 v13 v22 v23 v33')
V = s.zeros(4)
position = 0
for i in range(4):
    for j in range(i, 4):
        V[i, j] = V[j, i] = metric_symbols[position]
        position += 1
coefficient = -V[1, 1]/(4*a*b)
residual = V-coefficient*extra_metric
eq('metric_residual_has_zero_active_entry', residual[1, 1], 0)
Ametric = s.Matrix(4, 4, lambda row, col:
                   0 if col == 1 else residual[row, col] if row == 1
                   else residual[row, col]/2)
dual_U = F_inverse
eq('metric_dual_frame', U.T*eta*dual_U, s.eye(4))
inactive_U = dual_U*Ametric
eq('metric_lift_inactive_active_column', inactive_U[:, 1], s.zeros(4, 1))
eq('inactive_nine_metric_right_inverse',
   inactive_U.T*eta*U+U.T*eta*inactive_U, residual)
lift_U = inactive_U+coefficient*extra_U
eq('all_ten_physical_metric_right_inverse', lift_U.T*eta*U+U.T*eta*lift_U, V)

result = {
    'status': 'PASS', 'check_count': len(CHECKS), 'checks': CHECKS,
    'frequency_q': [0, 2, 0, 0], 'shell_pair_k_l': [[0, -1, 0, 0], [0, 1, 0, 0]],
    'rank_field': 'C for q; -q is the conjugate real-field partner',
    'actual_frame': 'F=(a-b)I+b11^T, a>b>0; U=eta F^T',
    'full_CAR_dimension': 16, 'full_reference_dimension': 128,
    'active_coframe_plus_all_links_dimension': 28,
    'complex_shell_constraint_rank': 22,
    'active_complex_kernel_dimension': 6,
    'retained_inactive_coframe_dimension': 12,
    'all_field_dimension_with_observer': 43,
    'all_field_kernel_dimension': 21,
    'physical_metric_image_rank_on_shell_kernel': 10,
    'fixed_metric_kernel_including_representation_dimension': 11,
    'representation_dimension': 6,
    'retained_apparatus_dimension_after_representation': 27,
    'retained_apparatus_constraint_rank': 22,
    'neutral_apparatus_dimension_after_representation': 5,
    'complex_shell_density_annihilator_dimension': 256-22,
    'extra_metric_delta_q11': '-4*a*b',
    'shell_constraint_linear_preparation_compatibility_proved': True,
    'all_internal_Euler_equations_solved': False,
    'nonlinear_inhomogeneous_stationary_metric_section_proved': False,
    'physical_GR_proved': False,
    'root_or_thermal_or_old_suite_replayed': False,
    'source_sha256': PINS, 'python': platform.python_version(), 'sympy': s.__version__,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
rendered = json.dumps(result, indent=2)+'\n'
if args.output is not None:
    args.output.write_text(rendered)
print(rendered, end='')
