#!/usr/bin/env python3
"""Exact CAR16 phase/source controls. SymPy; no new native action selected.

This checks a variational-source interface. It does not simulate an enacted
two-arm D0 apparatus, solve the full Euler equations or assert GR closure.
"""
from itertools import combinations
import json
import sympy as s


def zero(M):
    return all(s.simplify(v) == 0 for v in M)


def inner(a, b):
    return s.simplify((a.conjugate().T*b)[0])


eta = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
N, B = [s.zeros(4) for _ in range(2)], [s.zeros(4) for _ in range(2)]
for j, a in enumerate((2, 3)):
    N[j][1, a] = N[j][a, 0] = 1
    B[j][0, a] = B[j][a, 1] = 1
X, Y = N[0]-B[0], N[1]-B[1]
J = s.zeros(4)
J[2, 3], J[3, 2] = 1, -1
assert zero(N[0]*B[1]-B[1]*N[0]-J)
assert zero(X*Y-Y*X+2*J)
assert zero(Y*J-J*Y+X)
assert zero(J*X-X*J+Y)
for G in (X, Y, J):
    assert zero(G.T+G)
    assert zero(G.T*eta+eta*G)


basis = [I for k in range(5) for I in combinations(range(4), k)]
where = {I: i for i, I in enumerate(basis)}


def exterior_generator(A):
    """Actual exterior action on every grade, with wedge signs retained."""
    out = s.zeros(16)
    for col, I in enumerate(basis):
        for p, old in enumerate(I):
            for new in range(4):
                if A[new, old] == 0:
                    continue
                word = list(I)
                word[p] = new
                if len(set(word)) != len(word):
                    continue
                inversions = sum(word[i] > word[j] for i in range(len(word))
                                 for j in range(i+1, len(word)))
                out[where[tuple(sorted(word))], col] += (-1)**inversions*A[new, old]
    return out


GX, GY, GJ = [exterior_generator(A) for A in (X, Y, J)]
grade = s.diag(*[len(I) for I in basis])
parity = s.diag(*[(-1)**len(I) for I in basis])
for G in (GX, GY, GJ):
    assert zero(G.T+G)
    assert zero(G*grade-grade*G)
    assert zero(G*parity-parity*G)
assert zero(GX*GY-GY*GX+2*GJ)
assert zero(GY*GJ-GJ*GY+GX)
assert zero(GJ*GX-GX*GJ+GY)
assert zero(GX**3+2*GX) and zero(GY**3+2*GY)

psi4 = s.Matrix([1/s.sqrt(2), 0, s.Rational(1, 2), s.I/2])
psi = s.zeros(16, 1)
for a in range(4):
    psi[where[(a,)]] = psi4[a]
assert inner(psi, psi) == 1
assert parity*psi == -psi
assert inner(psi, GJ*psi) == s.I/2

derivatives = [GX*psi, GY*psi]
second = [[GX*GX*psi, GX*GY*psi], [GX*GY*psi, GY*GY*psi]]
z1 = [inner(psi, d) for d in derivatives]
alpha = s.Matrix([s.simplify(-s.I*z) for z in z1])
jacobian = s.Matrix(2, 2, lambda i, j: s.simplify(-s.I*(
    inner(derivatives[j], derivatives[i])+inner(psi, second[i][j]))))
fixed_ref_hessian = s.Matrix(2, 2, lambda i, j: s.simplify(s.im(
    inner(psi, second[i][j])-z1[i]*z1[j])))
mixed_echo = s.Matrix(2, 2, lambda i, j: s.simplify(
    inner(derivatives[j], derivatives[i])
    -inner(derivatives[j], psi)*inner(psi, derivatives[i])))
assert alpha == s.Matrix([0, -s.sqrt(2)/2])
assert jacobian == s.Matrix([[0, -1], [0, 0]])
assert fixed_ref_hessian == s.Matrix([[0, -s.Rational(1, 2)],
                                      [-s.Rational(1, 2), 0]])
assert mixed_echo == s.Matrix([[1, -s.I/2], [s.I/2, s.Rational(1, 2)]])
assert zero(jacobian-fixed_ref_hessian-mixed_echo.applyfunc(s.im))
assert s.simplify(jacobian[1, 0]-jacobian[0, 1]) == 1

generators = [GX, GY, GJ]
a3 = [s.simplify(-s.I*inner(psi, G*psi)) for G in generators]
curvature = s.Matrix(3, 3, lambda i, j: s.simplify(s.I*inner(
    psi, (generators[i]*generators[j]-generators[j]*generators[i])*psi)))
expected_curvature = s.Matrix([[0, 1, s.sqrt(2)/2], [-1, 0, 0],
                               [-s.sqrt(2)/2, 0, 0]])
assert a3 == [0, -s.sqrt(2)/2, s.Rational(1, 2)]
assert curvature == expected_curvature
contact = s.simplify(a3[0]*curvature[1, 2]-a3[1]*curvature[0, 2]
                     +a3[2]*curvature[0, 1])
assert contact == 1

# The dc wedge alpha terms cancel identically in alpha wedge d(c alpha).
c, cx, cy, cz = s.symbols('c cx cy cz', real=True)
dc = [cx, cy, cz]
scaled_F = s.Matrix(3, 3, lambda i, j:
    c*curvature[i, j]+dc[i]*a3[j]-dc[j]*a3[i])
scaled_contact = s.simplify(c*a3[0]*scaled_F[1, 2]
                          -c*a3[1]*scaled_F[0, 2]+c*a3[2]*scaled_F[0, 1])
assert s.simplify(scaled_contact-c*c) == 0

# Latest two native projective detector lines, integrated at 2a65c4cc.
native_connections = []
native_curvatures = []
for pole in (0, 1):
    native = s.zeros(16, 1)
    native[where[(pole,)]] = 1/s.sqrt(3)
    native[where[(2,)]] = 1/s.sqrt(3)
    native[where[(3,)]] = s.I/s.sqrt(3)
    aa = [s.simplify(-s.I*inner(native, G*native)) for G in generators]
    ff = s.Matrix(3, 3, lambda i, j: s.simplify(s.I*inner(native,
        (generators[i]*generators[j]-generators[j]*generators[i])*native)))
    assert inner(native, native) == 1
    assert s.simplify(aa[0]*ff[1, 2]-aa[1]*ff[0, 2]+aa[2]*ff[0, 1]) == s.Rational(4, 3)
    native_connections.append(s.Matrix(aa))
    native_curvatures.append(ff)
assert native_connections == [s.Matrix([0, -s.Rational(2, 3), s.Rational(2, 3)]),
                              s.Matrix([0, s.Rational(2, 3), s.Rational(2, 3)])]
wa, wb = s.symbols('a b', real=True)
mixed_a = wa*native_connections[0]+wb*native_connections[1]
mixed_f = wa*native_curvatures[0]+wb*native_curvatures[1]
mixed_contact = s.factor(mixed_a[0]*mixed_f[1, 2]-mixed_a[1]*mixed_f[0, 2]
                        +mixed_a[2]*mixed_f[0, 1])
assert s.expand(mixed_contact-s.Rational(4, 9)*(wb-wa)**2-s.Rational(8, 9)*(wa+wb)**2) == 0

# Exact group formula, not a finite-difference source check.
y, r = s.symbols('y r', real=True)
EY = s.eye(16)+s.sin(s.sqrt(2)*y)*GY/s.sqrt(2)+(1-s.cos(s.sqrt(2)*y))*GY**2/2
assert zero(EY.T*EY-s.eye(16))
ax = s.simplify(-s.I*inner(psi, EY.T*GX*EY*psi))
ay = s.simplify(-s.I*inner(psi, GY*psi))
assert s.simplify(ax+s.sin(s.sqrt(2)*y)/s.sqrt(2)) == 0
assert ay == -s.sqrt(2)/2
circulation_square = s.simplify(r*(ax.subs(y, 0)-ax.subs(y, r)))
assert s.simplify(circulation_square-r*s.sin(s.sqrt(2)*r)/s.sqrt(2)) == 0

# Same J23, exact small-face angle, all preparation derivatives included.
beta, theta, mesh = s.symbols('beta theta mesh', real=True)
eplus = s.zeros(16, 1)
eplus[where[(0,)]] = 1
circular = s.zeros(16, 1)
circular[where[(2,)]] = 1/s.sqrt(2)
circular[where[(3,)]] = s.I/s.sqrt(2)
assert GJ*eplus == s.zeros(16, 1)
assert zero(GJ*circular-s.I*circular)
chi = s.cos(beta)*eplus+s.sin(beta)*s.exp(s.I*mesh**2*theta)*circular
assert inner(chi, chi) == 1
aprep = s.simplify(-s.I*inner(chi, chi.diff(beta)))
aphase = s.simplify(-s.I*inner(chi, chi.diff(theta)))
assert aprep == 0
assert s.simplify(aphase-mesh**2*s.sin(beta)**2) == 0
# w=sin(beta)^2, 0<beta<pi/2; divide by dw/dbeta on this domain.
scaled_w_curvature = s.simplify(s.diff(aphase, beta)/(mesh**2*2*s.sin(beta)*s.cos(beta)))
assert scaled_w_curvature == 1
prototype = mesh**2*s.sin(beta)**2*theta
missing_prep = s.simplify(prototype.diff(beta)-aprep)
assert s.simplify(missing_prep-2*mesh**2*theta*s.sin(beta)*s.cos(beta)) == 0

# Exact limiting fixed-input face: nonzero finite curvature is O(mesh^4).
scale = mesh**2
assert zero(scale**2*curvature/mesh**2-mesh**2*curvature)

# A general real normalized factor has zero local phase. This explicit
# curve embeds in two original allowed edge labels; the other 716 remain.
t = s.symbols('t', real=True)
archive = s.zeros(718, 1)
archive[0], archive[1] = s.cos(t), s.sin(t)
assert inner(archive, archive) == 1
assert inner(archive, archive.diff(t)) == 0
assert s.simplify(-s.I*inner(archive, archive.diff(t))) == 0

print(json.dumps({
    'status': 'PASS',
    'input_ref': 'a95927fac939230a8e9d3e124c420fb2e3929a22',
    'carrier_dimension': 16, 'retained_exterior_grades': list(range(5)),
    'fixed_input_phase': [str(v) for v in alpha],
    'moving_reference_source_jacobian': [[str(v) for v in row] for row in jacobian.tolist()],
    'fixed_reference_scalar_hessian': [[str(v) for v in row] for row in fixed_ref_hessian.tolist()],
    'rotation_contact_coefficient': str(contact),
    'arbitrary_scalar_multiplier_contact': str(scaled_contact),
    'latest_two_native_ray_contacts': ['4/3', '4/3'],
    'constant_two_ray_combination_contact': str(mixed_contact),
    'closed_square_circulation': str(circulation_square),
    'moving_preparation_scaled_curvature': str(scaled_w_curvature),
    'missing_preparation_component_beta': str(missing_prep),
    'real_archive_factor_dimension': 718,
    'scope': 'exact source-interface controls, not native apparatus or complete physical action',
    'GR_closed': False, 'raw216_closed': False
}, indent=2))
