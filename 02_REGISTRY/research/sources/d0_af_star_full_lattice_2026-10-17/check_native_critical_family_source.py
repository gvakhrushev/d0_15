#!/usr/bin/env python3
"""New critical-family/source consumer; does not replay the old root suite.

Only stencil definitions are imported. The symbolic null-translation
identity is checked off shell in all eight original pp-wave parameters.
"""
import hashlib
import json
from pathlib import Path

import sympy as s
import star_euler as E


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def mixed_link_rows(backward=True, only=None):
    origin = (0, 0, 0, 0)
    ell = E.I[:, 1]
    def psi(at):
        return int(at == origin)
    direction = 1 if backward else -1
    bases = {origin} | {E.shift(origin, r, direction) for r in range(4)}
    result = {}
    for base in sorted(bases):
        de = s.zeros(4)
        for r in range(4):
            difference = (psi(base)-psi(E.shift(base, r, -1)) if backward
                          else psi(E.shift(base, r))-psi(base))
            de[:, r] = difference*ell
        for r, t in E.PAIRS:
            u, v = [j for j in range(4) if j not in (r, t)]
            dw = [a+b for a, b in zip(E.wedge(de[:, u], E.coframe(base)[:, v]),
                                     E.wedge(E.coframe(base)[:, u], de[:, v]))]
            if not any(dw):
                continue
            edges = E.edges(base, r, t)
            matrices = [E.link(*edge) for edge in edges]
            P = E.I
            for matrix in matrices:
                P = P*matrix
            Pi = E.ETA*P.T*E.ETA
            for pos, (at, axis, inverse) in enumerate(edges):
                left, right = E.I, E.I
                for j in range(pos):
                    left = left*matrices[j]
                for j in range(pos+1, 4):
                    right = right*matrices[j]
                for g, X in enumerate(E.LIE):
                    key = (at, axis, g)
                    if only is not None and key != only:
                        continue
                    du = -matrices[pos]*X if inverse else X*matrices[pos]
                    dp = left*du*right
                    dr = (dp+Pi*dp*Pi)/2
                    value = E.EPS((r, t, u, v))*E.pairing(dw, dr)
                    result[key] = result.get(key, 0)+value
    return {key: s.expand(value) for key, value in result.items()}


def null_translation():
    rows = mixed_link_rows()
    require(rows and all(value == 0 for value in rows.values()),
            'all symbolic mixed link rows vanish')
    require(len(rows) == 150, 'all affected link covectors included')
    wrong_key = ((0, 0, 0, -1), 0, 2)
    wrong = mixed_link_rows(False, wrong_key)[wrong_key]
    require(s.expand(wrong+E.h) == 0 and wrong != 0,
            'forward difference fails the literal mixed row')
    ell = E.I[:, 1]
    for r in range(4):
        for curvature in E.N:
            require(E.pairing(E.wedge(ell, E.I[:, r]), curvature) == 0,
                    'null insertion kills every background curvature pairing')
    tau = s.symbols('tau', real=True)
    xi = s.Matrix(1, 4, s.symbols('xi0:4', real=True))
    V = E.coframe((0, 0, 0, 0))
    changed = V+tau*ell*xi
    require(s.simplify(changed.det()-E.h**4*(1+tau*xi[1]/E.h)) == 0,
            'finite family nondegeneracy condition')
    metric_change = s.expand(changed.T*E.ETA*changed-V.T*E.ETA*V)
    expected = tau*E.h*(E.I[:, 0]*xi+xi.T*E.I[:, 0].T)
    require(metric_change == expected and metric_change != s.zeros(4),
            'raw metric changes; divide by h^2 for the physical metric')
    return {'symbolic_parameters': [str(x) for x in (E.a, E.b, E.d, E.cx, E.cy, E.h, E.x, E.y)],
            'mixed_link_rows': len(rows), 'nonzero_backward_rows': 0,
            'forward_negative_row': str(wrong),
            'finite_tau_euler_identity': 'coframe source linear; quadratic link change zero',
            'physical_metric_variation': '(delta_s0 D_r^-psi + delta_r0 D_s^-psi)/h',
            'continuum_interpretation': 'v-coordinate diffeomorphism; not independent matter',
            'Lorentz_gauge_fix_alone_gives_invertible_Hessian': False}


def whole_frame_source():
    t = s.symbols('t', real=True)
    T = s.Matrix([[1, t], [0, 1]])
    Ti = T.inv()
    G = Ti.T*Ti
    U0 = s.Matrix([[s.Rational(3, 5), -s.Rational(4, 5)],
                    [s.Rational(4, 5), s.Rational(3, 5)]])
    cut0 = s.diag(1, 0)
    U, cut = T*U0*Ti, T*cut0*Ti
    adjoint = G.inv()*U.T*G
    B = s.simplify(cut*adjoint*(s.eye(2)-cut)*U*cut)
    B0 = cut0*U0.T*(s.eye(2)-cut0)*U0*cut0
    require(s.simplify(B-T*B0*Ti) == s.zeros(2), 'whole moving Gram tuple')
    K, dB = T.diff(t)*Ti, B.diff(t)
    require(s.simplify(dB-K*B+B*K) == s.zeros(2), 'actual commutator jet')
    z, lam, I = s.Rational(1, 3), s.Rational(3, 4), s.eye(2)
    H = z*((I-z*B).inv()+(1-lam)*(I-z*(lam*I+(1-lam)*B)).inv())
    require(s.simplify(s.trace(H*dB)) == 0, 'ordinary full-trace scene source zero')
    require(K+K.T != s.zeros(2), 'no false skew-frame hypothesis')
    return {'whole_tuple_Gram_source': '0', 'ordinary_trace': True,
            'skew_frame_generator_required': False,
            'updated_gate_fixed_cut_inferred_equivalent': False}


def invariant_control_macro():
    J = s.Matrix([[0, -1], [1, 0]])
    R = s.Matrix([[s.Rational(3, 5), -s.Rational(4, 5)],
                  [s.Rational(4, 5), s.Rational(3, 5)]])
    swap = s.Matrix(4, 4, lambda i, j: int(i == (j % 2)*2+j//2))
    gauge = s.kronecker_product(s.eye(2), s.kronecker_product(R, R))
    JI, JQ = s.kronecker_product(J, s.eye(4)), s.kronecker_product(J, swap)
    c, q = s.Rational(5, 13), s.Rational(12, 13)
    macro = (c*s.eye(8)+q*JI)*(c*s.eye(8)-q*JQ)
    require(macro.T*macro == s.eye(8), 'orthogonal completed macro')
    require(macro*gauge == gauge*macro, 'exact covariance at nonzero finite error')
    require(macro != s.kronecker_product(s.eye(2), swap), 'spectator leakage is retained')
    return {'completed_invariant_macro_covariant': True,
            'finite_spectator_return_asserted': False,
            'forward_gate_inverse_requires_declared_resource': True,
            'physical_gate_admission_inferred': False}


def full_car_scalarization():
    creators = []
    for i in range(4):
        C = s.zeros(16)
        for mask in range(16):
            if not ((mask >> i) & 1):
                C[mask | (1 << i), mask] = (-1)**bin(mask & ((1 << i)-1)).count('1')
        creators.append(C)
    vacuum = s.diag(1, *([0]*15))
    columns = []
    for mask in range(16):
        column = vacuum
        for i in reversed(range(4)):
            if (mask >> i) & 1:
                column = creators[i]*column
        columns.append(column)
    def unit(i, j):
        return columns[i]*columns[j].T
    A = s.eye(4)
    A[:2, :2] = s.Matrix([[s.Rational(5, 4), s.Rational(3, 4)],
                          [s.Rational(3, 4), s.Rational(5, 4)]])
    eta = s.diag(1, -1, -1, -1)
    require(A.T*eta*A == eta and A.det() == 1, 'actual proper Lorentz edge')
    indices = [[i for i in range(4) if (mask >> i) & 1] for mask in range(16)]
    exterior = s.Matrix(16, 16, lambda i, j:
        (A.extract(indices[i], indices[j]).det() if indices[i] else 1)
        if len(indices[i]) == len(indices[j]) else 0)
    edge = creators[0]*exterior/4
    transporter = unit(0, 1)*edge*unit(0, 0)
    amplitude = unit(0, 3)*edge*unit(2, 0)
    require(transporter == vacuum/4, 'positive vacuum transporter derived from edge')
    require(amplitude == s.Rational(5, 16)*vacuum, 'nontrivial moving matrix amplitude')
    centered = s.zeros(16)
    for k in range(16):
        centered += unit(k, 0)*amplitude*transporter.T*unit(0, k)*4
    require(centered == s.Rational(5, 16)*s.eye(16),
            'scalar acts on ALL CAR columns without preparing vacuum')
    return {'input_columns': 16, 'central_scalar': '5/16',
            'vacuum_transporter': 'derived from actual proper-Lorentz edge query',
            'physical_vacuum_state_or_postselection_used': False,
            'supplied_controlled_query_interface_required': False}


def scalar_controlled_square():
    O = s.Matrix([[s.Rational(4, 5), -s.Rational(3, 5)],
                  [s.Rational(3, 5), s.Rational(4, 5)]])
    Z = s.diag(1, -1)
    require(Z*O*Z == O.T, 'actual Julia rotation has scalar echo adjoint')
    full = s.kronecker_product(s.eye(2), O)
    CZ = s.diag(1, 1, 1, -1)
    echo = full*CZ*full.T*CZ
    require(echo == s.diag(s.eye(2), O*O), 'controlled O^2 without a CAR bank')
    W = O*O
    def K(A):
        return s.BlockMatrix([[s.zeros(2), -A], [A.T, s.zeros(2)]]).as_explicit()
    X = s.Matrix([[0, 1], [1, 0]])
    require(K(W)-K(W.T) == -s.kronecker_product(X, W-W.T),
            'skew Laurent Hamiltonian synthesis, not polynomial-oracle assumption')
    return {'controlled_square_echo': 'exact',
            'analytic_branch_gap_required': True,
            'unitary_Laurent_polynomial_assumed_primitive': False,
            'scalar_return_and_leakage_budget_required': True}


if __name__ == '__main__':
    result = {'status': 'PASS',
              'stencil_sha256': hashlib.sha256(Path(E.__file__).read_bytes()).hexdigest(),
              'null_translation': null_translation(),
              'whole_frame': whole_frame_source(),
              'invariant_macro': invariant_control_macro(),
              'full_car_scalarization': full_car_scalarization(),
              'scalar_controlled_square': scalar_controlled_square(),
              'exact_compiled_joint_roots_proved': False,
              'physical_D0_GR_proved': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
