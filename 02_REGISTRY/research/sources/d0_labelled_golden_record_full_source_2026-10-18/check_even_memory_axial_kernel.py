#!/usr/bin/env python3
"""Pure real-even memory: exact axial preparation kernel, not a Hessian scan.

Only pinned literal CAR definitions are executed. The pinned faithful axial
metric-lift receipt is CONSUMED, never replayed. Default execution is read-only;
--output explicitly saves the receipt. Complex ranks refer to one Q=2e_i;
the conjugate -Q wave is retained for real fields.

Let chi=(vac+top)/sqrt(2), k=-e_i,l=e_i, z=exp(-i*pi/4)-1. After an SO(4)
CAR rotation aligns nonzero u_i with e0, J=J^T has the unique normal form

 A=beta(v)+Z, D=-beta(v)-Z+beta(R),
 B=v0 I+Gamma(M)^T+P, J=[[A,B],[B^T,D]].

Here M is any3x3 matrix; P is a pair creator; Z is a spatial raising cubic
plus its transpose. Full16 outputs X chi=0, X=D_l J+J D_k, are exactly

 v0=0, tr(M)=0, P vac3=Z top3,
 R=-(bar(z)-z)/z*v-bar(z)/z*P^T top3.

Thus the active28 kernel has dimension20: M traceless8, v3, Z9. Its
pure-link part has dimension17 (v=0). The old faithful kernel6 is contained
in it; the fourteen additional directions are pure links, not matter cuts.
SO(4) preserves chi (det=+1), and the invertible native Cartan map identifies
ALL24 Lorentz links with all raising cubics. Therefore the exact normal form
applies to generic actual invertible F, not merely a frame fixture.

The faithful all10 metric lift remains valid since it had X=0 on full16.
With observer3 kept, the field dimension43 has kernel35. The metric-zero
kernel has dimension25; after representation6, INTERNAL dimension is19.
An explicit basis is the17 pure-link jets below and two coframe jets
delta u_r=K_v u_r, where u_i=(c,s), v perpendicular s,
K_v=[[0,v^T],[v,-c(vs^T-sv^T)/|s|^2]]. These K_v fix u_i and preserve eta.

SOURCE BOUNDARY: rho=P_Omega tensor |chi><chi|/8 has rank8, not128.
Reference SPACE128 is retained; its marginal has rank8. Q in the signed
resolvent excludes the ENTIRE128-dimensional epsilon shell, not only rank8.
After eliminating Q amplitudes the true bilinear form is

 Hred(v,w)=Tr[(kappa+rho)({D_v,D_w}+{D,D_vw})]
          +Tr[Dkappa[X_v] X_w]-2 ReTr[rho X_w R_Q X_v].

The second Dirac jet D_vw remains. W=kappa+rho is not scalar on shell;
neither the old scalar-W Gram formula nor its curvature cancellation is
imported. This checker computes no thermal Hessian, internal inverse,
stationary metric section, physical selection or GR result.
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
LIFT = '02_REGISTRY/research/sources/d0_labelled_golden_record_full_source_2026-10-18/check_spatial_shell_lift.py'
LIFT_RESULT = '02_REGISTRY/research/sources/d0_labelled_golden_record_full_source_2026-10-18/SPATIAL_SHELL_LIFT_RESULT.json'
PINS = {
    HELPER: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    LIFT: 'ab86bb69ac5fc9e18fe157e2fa571d2a0093fc272d41dc6bed638ec7679a2b26',
    LIFT_RESULT: '1320eb937b8b9f5066c222bd1b0e86cd1e593002dbb1541d9f202f3faf5419b8',
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


FIELD = s.QQ.algebraic_field(s.sqrt(2), s.I)


def rank(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(FIELD).rank()


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
vac, top = I16[:, 0], I16[:, 15]
cat, phase_cat = (vac+top)/s.sqrt(2), (vac+s.I*top)/s.sqrt(2)
z, zb = (1-s.I)/s.sqrt(2)-1, (1+s.I)/s.sqrt(2)-1
Dk, Dl = z*C[0]+zb*C[0].T, zb*C[0]+z*C[0].T
eq('real_cat_norm', (cat.T*cat)[0], 1)
eq('phase_cat_norm', (phase_cat.H*phase_cat)[0], 1)
eq('opposite_shell_transpose', Dk.T, Dl)


def gamma(matrix, creators):
    return sum((matrix[i, j]*creators[i]*creators[j].T
                for i in range(matrix.rows) for j in range(matrix.cols)),
               s.zeros(creators[0].rows))


for i in range(4):
    for j in range(4):
        eq('actual_CAR_%d%d' % (i, j), C[i]*C[j].T+C[j].T*C[i],
           I16 if i == j else O16)
for i in range(4):
    for j in range(i+1, 4):
        S = s.zeros(4)
        S[i, j], S[j, i] = 1, -1
        eq('SO4_cat_invariance_%d%d' % (i, j), gamma(S, C)*cat, s.zeros(16, 1))
        omega = s.zeros(4)
        omega[i, j], omega[j, i] = 1, -eta[i, i]*eta[j, j]
        eq('Lorentz_cat_invariance_%d%d' % (i, j),
           gamma(omega, C)*cat, s.zeros(16, 1))

# Explicit signed permutation from the actual ACDB matrices to active occupation.
N0 = C[0]*C[0].T
basis0 = s.Matrix.hstack(*(I16[:, j] for j in range(16) if N0[j, j] == 0))
basis1 = C[0]*basis0
T = basis0.row_join(basis1)
eq('actual_ACDB_occupation_intertwiner_orthogonal', T.T*T, I16)
eq('actual_ACDB_active_creator_block', T.T*C[0]*T,
   s.BlockMatrix([[s.zeros(8), s.zeros(8)], [s.eye(8), s.zeros(8)]]).as_explicit())
cs = [basis0.T*C[j]*basis0 for j in (1, 2, 3)]
for j, c in enumerate(cs):
    eq('actual_ACDB_spatial_creator_block_'+str(j), T.T*C[j+1]*T,
       s.diag(c, -c))
vac3, top3 = basis0.T*vac, basis1.T*top
eq('actual_ACDB_cat_occupation_intertwiner',
   T.T*cat, vac3.col_join(top3)/s.sqrt(2))

J_basis = [c+c.T for c in C]
for i in range(4):
    for j in range(i+1, 4):
        for k in range(4):
            cubic = C[i]*C[j]*C[k].T
            J_basis.append(cubic+cubic.T)
eq('active_jet_dimension28',
   rank(s.Matrix.hstack(*(J.reshape(256, 1) for J in J_basis))), 28)
rectangular = s.Matrix.hstack(*((Dl*J+J*Dk)*cat for J in J_basis))
eq('all16_output_rectangular_rank8', rank(rectangular), 8)
eq('all24_link_rectangular_rank7', rank(rectangular[:, 4:]), 7)

# Five extra symmetric trace-zero one-body jets; the skew three are faithful.
symmetric_M = []
for i in range(3):
    for j in range(i+1, 3):
        M = s.zeros(3)
        M[i, j] = M[j, i] = 1
        symmetric_M.append(M)
symmetric_M.extend([s.diag(1, -1, 0), s.diag(1, 1, -2)])
extras = []
extra_names = []
for index, M in enumerate(symmetric_M):
    eq('extra_onebody_trace_'+str(index), s.trace(M), 0)
    B = gamma(M, cs).T
    block = s.BlockMatrix([[s.zeros(8), B], [B.T, s.zeros(8)]]).as_explicit()
    extras.append(T*block*T.T)
    extra_names.append('symmetric_traceless_M_'+str(index))
for i in range(3):
    for j in range(i+1, 3):
        for k in range(3):
            tag = 'spatial_cubic_%d%d%d' % (i, j, k)
            Z = cs[i]*cs[j]*cs[k].T
            Z += Z.T
            P = s.zeros(8)
            for a in range(3):
                for b in range(a+1, 3):
                    e = cs[a]*cs[b]*vac3
                    P += (e.T*Z*top3)[0]*cs[a]*cs[b]
            eq(tag+'_pair_equation', P*vac3, Z*top3)
            target = -(zb/z)*P.T*top3
            R = s.Matrix([((c*vac3).T*target)[0] for c in cs])
            eq(tag+'_remaining_equation',
               sum((R[a]*cs[a]*vac3 for a in range(3)), s.zeros(8, 1)), target)
            beta_R = sum((R[a]*(cs[a]+cs[a].T) for a in range(3)), s.zeros(8))
            block = s.BlockMatrix([[Z, P], [P.T, -Z+beta_R]]).as_explicit()
            extras.append(T*block*T.T)
            extra_names.append(tag)
check('extra_count14', len(extras) == 14)
phase_failures = []
for name, J in zip(extra_names, extras):
    X = Dl*J+J*Dk
    eq(name+'_all16_outputs', X*cat, s.zeros(16, 1))
    eq(name+'_minusQ_all16_outputs', X.H*cat, s.zeros(16, 1))
    eq(name+'_pure_link_no_vacuum_entry', J*vac, s.zeros(16, 1))
    if any(s.cancel(s.expand(x)) != 0 for x in X*phase_cat):
        phase_failures.append(name)
eq('nontrivial_phase_control_count', len(phase_failures), 6)

faithful = []
pure_faithful = []
for i in range(4):
    for j in range(i+1, 4):
        S = s.zeros(4)
        S[i, j], S[j, i] = 1, -1
        G = gamma(S, C)
        J = G*Dk-Dl*G
        eq('faithful_full16_%d%d' % (i, j), Dl*J+J*Dk, O16)
        faithful.append(J)
        if i > 0:
            pure_faithful.append(J)
eq('complete_kernel20_dimension',
   rank(s.Matrix.hstack(*(J.reshape(256, 1) for J in faithful+extras))), 20)
eq('pure_link_kernel17_dimension',
   rank(s.Matrix.hstack(*(J.reshape(256, 1) for J in pure_faithful+extras))), 17)

# Generic actual-frame coframe part of the internal19 basis.
a, b = s.symbols('a b', positive=True)  # Actual domain has a>b>0.
F = (a-b)*s.eye(4)+b*s.ones(4)
U = eta*F.T
for active in range(4):
    u, spatial = U[:, active], U[1:, active]
    v_basis = [s.Matrix([-spatial[1], spatial[0], 0]),
               s.Matrix([-spatial[2], 0, spatial[0]])]
    for index, v in enumerate(v_basis):
        tag = '%d_%d' % (active, index)
        eq('internal_boost_perpendicular_'+tag, (v.T*spatial)[0], 0)
        Rv = -u[0]*(v*spatial.T-spatial*v.T)/(spatial.T*spatial)[0]
        K = s.zeros(4)
        K[0, 1:] = v.T
        K[1:, 0] = v
        K[1:, 1:] = Rv
        eq('internal_coframe_Lorentz_'+tag, K.T*eta+eta*K, s.zeros(4))
        eq('internal_coframe_active_zero_'+tag, K*u, s.zeros(4, 1))
        dU = K*U
        eq('internal_coframe_metric_zero_'+tag,
           dU.T*eta*U+U.T*eta*dU, s.zeros(4))
    eq('two_boost_parts_independent_minor_'+str(active),
       s.Matrix.hstack(*v_basis)[1:, :].det(), spatial[0]**2)

# Consume the existing all10 faithful lift, without executing its checker.
lift = json.loads((ROOT/LIFT_RESULT).read_text())
check('consumed_faithful_lift_pass', lift['status'] == 'PASS')
check('consumed_faithful_all10_metric_image',
      lift['physical_metric_image_rank_on_shell_kernel'] == 10)
check('consumed_faithful_full16_constraint', lift['full_CAR_dimension'] == 16)

# Full reference128 space; only eight Schmidt directions are occupied.
Psi = s.SparseMatrix(128, 128, {})
for k in range(8):
    for j in (0, 15):
        Psi[16*k+j, k] = s.Rational(1, 4)
P_support = s.kronecker_product(s.eye(8), cat*cat.T)
eq('actual_rank8_reference128_realization', Psi*Psi.T, P_support/8)
eq('reference_marginal_rank8_not128',
   Psi.T*Psi, s.diag(*([s.Rational(1, 8)]*8+[0]*120)))
eq('reference128_preparation_normalization', s.trace(Psi.T*Psi), 1)

intertwiner_columns = []
for j in range(16):
    entries = [(i, int(T[i, j])) for i in range(16) if T[i, j] != 0]
    check('signed_permutation_column_'+str(j), len(entries) == 1)
    intertwiner_columns.append(entries[0])
result = {
    'status': 'PASS', 'check_count': len(CHECKS), 'checks': CHECKS,
    'axial_frequency': 'Q=2e_i; -Q conjugate retained',
    'generic_frame_domain': 'invertible U; actual F=(a-b)I+b11^T, a>b>0',
    'memory': '(vac+top)/sqrt(2), real relative phase',
    'full_CAR_dimension': 16, 'full_reference_space_dimension': 128,
    'shell_spectral_dimension': 128, 'preparation_and_reference_rank': 8,
    'active_jet_dimension': 28, 'rectangular_all16_output_rank': 8,
    'active_kernel_dimension': 20, 'pure_link_kernel_dimension': 17,
    'retained_inactive_coframe_dimension': 12,
    'all_field_dimension': 43, 'all_field_kernel_dimension': 35,
    'physical_metric_image_rank': 10,
    'metric_zero_kernel_including_representation_dimension': 25,
    'representation_dimension': 6, 'internal_kernel_dimension': 19,
    'internal_basis': '17 pure-link jets +2 inactive coframe Lorentz-stabilizer jets',
    'actual_ACDB_intertwiner_columns': intertwiner_columns,
    'phase_controls_failed_for_imaginary_cat': phase_failures,
    'consumed_metric_lift_receipt': LIFT_RESULT,
    'thermal_Hessian_computed': False, 'scalar_W_formula_imported': False,
    'second_Dirac_jet_cancelled': False, 'all_internal_Euler_rows_solved': False,
    'nonlinear_metric_section_proved': False, 'physical_GR_proved': False,
    'old_suite_replayed': False, 'source_sha256': PINS,
    'python': platform.python_version(), 'sympy': s.__version__,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
rendered = json.dumps(result, indent=2)+'\n'
if args.output is not None:
    args.output.write_text(rendered)
print(rendered, end='')
