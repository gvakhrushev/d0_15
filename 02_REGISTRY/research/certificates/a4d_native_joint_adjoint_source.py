#!/usr/bin/env python3
"""Exact kernels for the stored joint adjoint class and conditional source.

No heat binding, stationary equation, physical gauge, or native preparation
map is selected. Universal statements are proved in the companion research text.
"""
from functools import lru_cache
import importlib.util
from pathlib import Path
import sys
import sympy as s

spec = importlib.util.spec_from_file_location('joint_curved_input',
    Path(__file__).with_name('a4d_native_curved_soldered_heat.py'))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
ETA = s.diag(1, -1, -1, -1)
SLOTS = [(i, j) for i in range(4) for j in range(i, 4)]


def comm(A, B):
    return A*B-B*A


def dagger(A, G):
    return G.inv()*A.conjugate().T*G


def creator(v):
    return sum((v[r]*P.creator(r) for r in range(4)), s.zeros(16))


def exterior(A):
    """Full exterior lift in the actual A,C,D,B occupation basis."""
    subsets = [[i for i in range(4) if mask & (1 << i)] for mask in range(16)]
    out = s.zeros(16)
    for i, rows in enumerate(subsets):
        for j, cols in enumerate(subsets):
            if len(rows) == len(cols):
                out[i, j] = A.extract(rows, cols).det() if rows else 1
    J = P.basis_phase()
    return J*out*J


def observer(n):
    return -ETA+2*ETA*n*n.T*ETA


def exterior_gram(h):
    J = P.basis_phase()
    return J*P.H.exterior_gram(h)*J


def edge(A, nx, ny, vx, vy):
    hx, hy = observer(nx), observer(ny)
    Gx, Gy = exterior_gram(hx), exterior_gram(hy)
    U, Ui = exterior(A), exterior(A.inv())
    forward = creator(vx)*U
    stored = creator(hy*vy).T*Ui
    adjoint = exterior(hy.inv())*forward.T*Gx
    T = hy.inv()*A.T*hx*A
    return {'hx': hx, 'hy': hy, 'Gx': Gx, 'Gy': Gy, 'U': U,
            'forward': forward, 'stored': stored, 'adjoint': adjoint,
            'defect': stored-adjoint, 'T': T,
            'b': hy*vy, 'c': A.T*hx*vx}


def lorentz_jet(values):
    b1, b2, b3, r12, r13, r23 = values
    return s.Matrix([[0, b1, b2, b3], [b1, 0, r12, r13],
                     [b2, -r12, 0, r23], [b3, -r13, -r23, 0]])


@lru_cache(None)
def tangent_system(flags):
    """43-variable linearization; flags mark nonzero Fourier differences.

    Actual nonzero Fourier factors can be divided out independently in each
    edge equation. Replacing them by one preserves these dimensions.
    """
    variables = s.symbols('x:43')
    dF = s.Matrix(4, 4, variables[:16])
    u = s.Matrix([0, *variables[16:19]])
    equations = []
    for r, difference in enumerate(flags):
        W = lorentz_jet(variables[19+6*r:25+6*r])
        equations.extend(W[:, 0]-difference*u)
        equations.extend(W[:, r]-difference*ETA*dF.row(r).T)
    constraints = s.Matrix(equations).jacobian(variables)
    metric = s.Matrix([dF[i, j]+dF[j, i] for i, j in SLOTS]).jacobian(variables)
    return constraints, metric


def minimal_rotation(source, target):
    """Unit vectors, nonantipodal: maps source to target exactly."""
    K = target*source.T-source*target.T
    return s.eye(source.rows)+K+K*K/(1+(source.T*target)[0])


def metric_lift_legs(eps, diagonal, time_A, time_B, spatial_cross):
    """Pointwise part of the nonlinear metric lift.

    H_rr is independent of coordinate r; A_i is independent of coordinate i;
    B_i is independent of time; H_0i=A_i+B_i. Links are minimal rotations of
    adjacent normalized spatial legs, with identity time links.
    """
    legs = [s.Matrix([1+eps*diagonal[0]/2,
                      *[-eps*time_B[i] for i in range(3)]])]
    for i in range(3):
        direction = s.eye(3)[:, i]-eps*spatial_cross[:, i]/2
        direction = direction/s.sqrt((direction.T*direction)[0])
        legs.append(s.Matrix([eps*time_A[i],
                              *list((1-eps*diagonal[i+1]/2)*direction)]))
    return legs


def raw_frame(legs):
    return s.Matrix.vstack(*[(ETA*v).T for v in legs])


def commutant_weight(D):
    """Positive exact commuting surrogate for algebraic trace-kernel tests.

    This is not called a Gibbs density. Actual Gibbs behavior is separately
    checked on a full16 scalar-square family where the Gibbs weight is exact.
    """
    W = (s.eye(D.rows)+D*D).inv()
    return W/s.trace(W)


def joint_covector(d, G, projection, U, z, rho):
    adjd, adjU = dagger(d, G), dagger(U, G)
    D = d+adjd
    N = adjU*(s.eye(G.rows)-projection)*U
    feedback = projection*N*projection
    resolvent = z*(s.eye(G.rows)-z*feedback).inv()
    RP = projection*resolvent*projection
    C = N*RP+RP*N-U*RP*adjU
    J = comm(RP, N)
    CG = -2*comm(rho*D, adjd)
    return {'D': D, 'N': N, 'F': feedback, 'R': resolvent,
            'RP': RP, 'C': C, 'J': J, 'CG': CG}


def covector_fixture():
    """Nonorthonormal exact4 prototype, not a physical state preparation."""
    T = s.Matrix([[1, 1, 0, 0], [0, 2, 1, 0], [0, 0, 1, 1], [0, 0, 0, 3]])
    G = T.inv().T*T.inv()
    hat = lambda M: T*M*T.inv()
    projection = hat(s.diag(1, 1, 0, 0))
    U = hat(s.Matrix([[s.Rational(3,5), 0, s.Rational(-4,5), 0],
                     [0, s.Rational(5,13), 0, s.Rational(-12,13)],
                     [s.Rational(4,5), 0, s.Rational(3,5), 0],
                     [0, s.Rational(12,13), 0, s.Rational(5,13)]]))
    d = hat(s.Matrix([[0, 1, 2, 0], [0, 0, 1, 3], [0, 0, 0, 2], [0, 0, 0, 0]]))
    K = hat(s.Matrix([[2, 1, 0, 1], [1, 3, 1, 0], [0, 1, 4, 2], [1, 0, 2, 5]]))
    B = hat(s.Matrix([[0, 0, 0, 0], [0, 0, 0, 0], [1, 2, 0, 0], [3, 4, 0, 0]]))
    A = hat(s.Matrix([[0, 1, 2, 3], [-1, 0, 4, 5], [-2, -4, 0, 6], [-3, -5, -6, 0]]))
    Z = hat(s.Matrix(4, 4, range(16)))
    X = B+dagger(B, G)
    D = d+dagger(d, G)
    return {'T': T, 'G': G, 'P': projection, 'U': U, 'd': d,
            'K': K, 'B': B, 'A': A, 'Z': Z, 'X': X,
            'rho': commutant_weight(D), 'z': s.Rational(1,3)}


if __name__ == '__main__':
    A, H = tangent_system((1, 1, 1, 1))
    print('Generic full-joint metric image:', A.col_join(H).rank()-A.rank())
    print('Stored adjoint admission / general Gram completion are distinct.')
    print('Native heat / coupled source / GR: OPEN')
