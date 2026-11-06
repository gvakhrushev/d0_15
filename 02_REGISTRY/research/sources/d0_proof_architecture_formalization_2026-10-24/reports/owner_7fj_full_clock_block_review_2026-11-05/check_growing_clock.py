#!/usr/bin/env python3
"""Exact two-stage GROWING/CX control; not a physical admission proof."""
import json
import itertools
import sympy as s

a, p, z = s.symbols('a p z', real=True)
# a > 0, p > 0, a²=p and p²+p=1; positivity is explained separately.
ideal = s.groebner([a*a-p, p*p+p-1], a, p, z)

def reduce_poly(expr):
    return s.factor(ideal.reduce(s.expand(expr))[1])

def check_matrix(lhs, rhs, label):
    delta = lhs-rhs
    failures = [(i, j, reduce_poly(delta[i, j]))
                for i in range(delta.rows) for j in range(delta.cols)
                if reduce_poly(delta[i, j]) != 0]
    if failures:
        raise ArithmeticError(label + ': ' + str(failures))

def check_scalar(lhs, rhs, label):
    if reduce_poly(lhs-rhs) != 0:
        raise ArithmeticError(label + ': ' + str(reduce_poly(lhs-rhs)))

def determinant_mod(matrix):
    """Leibniz determinant with exact reduction after every product."""
    if matrix.rows != matrix.cols:
        raise ValueError('determinant needs a square matrix')
    entries = matrix.applyfunc(reduce_poly)
    total = 0
    for perm in itertools.permutations(range(matrix.rows)):
        inversions = sum(perm[i] > perm[j] for i in range(len(perm))
                         for j in range(i + 1, len(perm)))
        term = s.Integer((-1) ** inversions)
        for i, j in enumerate(perm):
            term = reduce_poly(term * entries[i, j])
        total = reduce_poly(total + term)
    return total

I2, I4, I6 = s.eye(2), s.eye(4), s.eye(6)
v = s.Matrix([a, p])
B = s.kronecker_product(I2, v)  # H0=2 -> Hf=4, canonical birth
A = B
P0 = v*v.T  # the active H0 bit itself is in its canonical born state
control_one = s.diag(0, 1)
X = s.Matrix([[0, 1], [1, 0]])
g = s.diag(1, 1, 0, 0) + s.kronecker_product(control_one, X)  # live bit controls born bit
D = I4-B*B.T
U = B.T*g*A
C = P0*U*P0
L = (I2-P0)*U*P0
E = P0*A.T*g.T*D*g*A*P0
P = s.diag(P0, A*P0*A.T)
T = s.zeros(6)
T[:2, 2:] = B.T*g
T[2:, :2] = A
T[2:, 2:] = D*g
jf = s.zeros(6, 1)
jf[2:, 0] = A*v
F = P*T.T*(I6-P)*T*P
c = (v.T*U*v)[0]

check_matrix(B.T*B, I2, 'birth isometry')
check_matrix(g.T*g, I4, 'final CX is unitary')
check_matrix(P.T, P, 'generated P self-adjoint')
check_matrix(P*P, P, 'generated P projector')
check_matrix(T.T*T, I6, 'full T isometry')
check_matrix(T*T.T, I6, 'full T coisometry')
check_matrix(U, s.diag(1, 2*a*p), 'compressed return')
check_matrix(C.T*C+L.T*L, P0-E, 'full defect identity')
check_matrix(E, p**8*P0, 'birth complement is nonzero')
check_matrix(F, (1-c*c)*jf*jf.T, 'full clock leakage retains complement')
check_matrix(F[:2, :], s.zeros(2, 6), 'first stage feedback rows vanish')
check_matrix(F[:, :2], s.zeros(6, 2), 'first stage feedback columns vanish')
check_scalar(determinant_mod((I6-z*F)[2:, 2:]), 1-z+z*c*c, 'full clock determinant')
check_scalar(determinant_mod(I2-z*L.T*L), 1-z+z*c*c+z*p**8, 'naive compressed determinant')

# Exact real parameter, rather than a floating approximation.
p_exact = (s.sqrt(5)-1)/2
if not bool(p_exact > 0 and p_exact < 1):
    raise ArithmeticError('golden p is not in (0,1)')
print(json.dumps({'status':'PASS','method':'polynomial reduction modulo a^2=p, p^2+p=1',
                  'stage_dimensions':[2,4],'actual_word':['canonical birth','CX'],
                  'cut':'P0=|v><v|, v=(a,p)','effective_U':'diag(1,2*a*p)',
                  'birth_complement':'p^8 P0',
                  'owner_feedback_det':'1-z+z*(v.T*U*v)^2',
                  'naive_feedback_det':'owner_feedback_det+z*p^8',
                  'scientific_promotion':False,'GR_closed':False},sort_keys=True,indent=2))
