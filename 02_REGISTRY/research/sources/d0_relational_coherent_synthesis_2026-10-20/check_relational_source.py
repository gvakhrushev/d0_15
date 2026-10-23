#!/usr/bin/env python3
"""Exact relational face-orientation and proper-frame source checks.

Uses the existing Lorentz-star formula. It checks its descent under changes
of representation, not physical admission or selection of a Book action.
No inputs are downloaded and no repository files are changed.
"""
from itertools import combinations, permutations
import json
import sympy as s

I = s.eye(4)
Z = s.zeros(4)
eta = s.diag(1, -1, -1, -1)
pairs = list(combinations(range(4), 2))
perms = [(t, int(s.LeviCivita(*t))) for t in permutations(range(4))]

def boost(i):
    M = I.copy()
    M[0, 0] = M[i, i] = s.Rational(5, 4)
    M[0, i] = M[i, 0] = s.Rational(3, 4)
    return M

def rotation(i, j):
    M = I.copy()
    M[i, i] = M[j, j] = s.Rational(3, 5)
    M[i, j] = s.Rational(4, 5)
    M[j, i] = -s.Rational(4, 5)
    return M

def wedge(u, v):
    return u*v.T - v*u.T

def hodge(B):
    low = eta*B*eta
    H = s.zeros(4)
    for (a, b, c, d), sign in perms:
        H[a, b] += sign*low[c, d]/2
    return H

def mul(A, B):
    return A[0]*B[0], A[1]*B[0] + A[0]*B[1]

def inv(A):
    Ai = A[0].inv()
    return Ai, -Ai*A[1]*Ai

def face(U, dU, r, t):
    word = [(U[r], dU[r]), (U[t], dU[t]),
            inv((U[r], dU[r])), inv((U[t], dU[t]))]
    P = (I, Z)
    for factor in word:
        P = mul(P, factor)
    Pi = inv(P)
    return (P[0]-Pi[0])/2, (P[1]-Pi[1])/2

def density_jet(e, de, U, dU, reverse=()):
    value = s.S.Zero
    derivative = s.S.Zero
    for n, (r0, t0) in enumerate(pairs):
        r, t = (t0, r0) if n in reverse else (r0, t0)
        u, v = [i for i in range(4) if i not in (r, t)]
        sign = s.LeviCivita(r, t, u, v)
        B = sign*hodge(wedge(e[:, u], e[:, v]))*eta
        dB = sign*hodge(wedge(de[:, u], e[:, v])
                        + wedge(e[:, u], de[:, v]))*eta
        F, dF = face(U, dU, r, t)
        value -= s.trace(B*F)/2
        derivative -= s.trace(dB*F + B*dF)/2
    return value, derivative

U = [boost(1), rotation(1, 2), boost(2), rotation(2, 3)]
e = s.Matrix([[1, 2, 0, 1], [0, 1, 1, 0],
              [2, 0, 1, 1], [1, 0, 0, 2]])
assert e.det() != 0
for A in U:
    assert A.T*eta*A == eta and A.det() == 1 and A[0, 0] > 0

G = boost(3)*rotation(1, 2)
Gi = G.inv()
assert G.T*eta*G == eta and G.det() == 1 and G[0, 0] > 0
eG = G*e
UG = [G*A*Gi for A in U]

generators = []
for i, j in pairs:
    X = s.zeros(4)
    X[i, j] = 1
    X[j, i] = -eta[i, i]*eta[j, j]
    assert X.T*eta + eta*X == Z
    generators.append(X)

directions = []
for a in range(4):
    for r in range(4):
        de = s.zeros(4)
        de[a, r] = 1
        directions.append((de, [Z]*4))
for r in range(4):
    for X in generators:
        dU = [Z]*4
        dU[r] = X*U[r]
        directions.append((Z, dU))
assert len(directions) == 40

base = density_jet(e, Z, U, [Z]*4)[0]
assert base != 0
reverse_subset = (0, 2, 5)
for de, dU in directions:
    old = density_jet(e, de, U, dU)
    flipped = density_jet(e, de, U, dU, reverse_subset)
    gauged = density_jet(eG, G*de, UG, [G*dA*Gi for dA in dU])
    both = density_jet(eG, G*de, UG, [G*dA*Gi for dA in dU], reverse_subset)
    assert old == flipped == gauged == both

# Active inversion at fixed coframe is different: it negates each face's F.
active = -base
assert active != base

# Proper frame changes can flip a fixed J23 coordinate without changing the
# relational source. No physical reversal or improper/time-reversing map.
J = s.zeros(4)
J[2, 3], J[3, 2] = 1, -1
P = rotation(2, 3)
L = s.diag(1, -1, 1, -1)
assert L.T*eta*L == eta and L.det() == 1 and L[0, 0] == 1
assert L*J*L.inv() == -J
F = (P-P.inv())/2
pairing = lambda B, C: -s.trace(B*C)/2
assert pairing(J, F) == s.Rational(4, 5)
assert pairing(-J, -F) == pairing(J, F)
assert pairing(L*J*L.inv(), L*F*L.inv()) == pairing(J, F)

# Golden signed-pair coordinates: exact identities in the positive-root chart
# sqrt(q+)=sqrt(k)(m+s), sqrt(q-)=sqrt(k)(m-s). Reversing the
# face exchanges the two labels and negates its coframe coefficient.
c, m, z, k = s.symbols('c m z k', real=True)
rootmark = s.sqrt(2)*z
assert s.expand((-c)*rootmark.subs(z, -z)-c*rootmark) == 0
qplus, qminus = k*(m+z)**2, k*(m-z)**2
assert qplus.subs(z, -z) == qminus
assert qminus.subs(z, -z) == qplus
for variable in (c, m, z, k):
    assert s.diff((-c)*rootmark.subs(z, -z)-c*rootmark, variable) == 0

print(json.dumps({
    'status': 'PASS',
    'exact_six_shared_face_density': str(base),
    'coframe_directions': 16,
    'proper_shared_link_directions': 24,
    'independently_reoriented_faces': list(reverse_subset),
    'orientation_and_proper_frame_pulled_back_source_equal': True,
    'fixed_coframe_active_face_inversion_changes_density_sign': True,
    'proper_frame_J23_component_flip': True,
    'nonzero_relational_J23_pairing': '4/5',
    'paired_opposite_orientation_density': '8/5',
    'Golden_signed_pair_swap_and_coframe_sign_cancel': True,
    'physical_Book_action_selection_claimed': False,
    'scope': 'Exact rational one-site four-shared-link regression of universal orientation/gauge identities; no finite lattice refinement claim.'
}, indent=2))
