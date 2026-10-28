#!/usr/bin/env python3
"""Exact checks of the unchanged return terminal graph and gauge Schur rule.

These are structural finite-matrix/coordinate checks, not physical admission
of continuous native gate angles or a complete original full42 solve.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

checks = []

def zero(expr, name):
    value = s.simplify(s.cancel(s.expand(expr)))
    if value != 0:
        raise RuntimeError(f"{name}: {value}")
    checks.append(name)

def matrix_zero(expr, name):
    for val in expr:
        if s.simplify(s.cancel(s.expand(val))) != 0:
            raise RuntimeError(f"{name}: nonzero matrix entry {val}")
    checks.append(name)

x, y, px, py = s.symbols("x y px py", real=True)
z = s.symbols("z", positive=True)
t = x-y
U = s.Matrix([[1-t*t, -2*t], [2*t, 1-t*t]])/(1+t*t)
P = s.diag(1, 0)
I = s.eye(2)
matrix_zero(U.T*U-I, "actual_cayley_unitary")
Cescape = (I-P)*U*P
F = Cescape.T*Cescape
f = 4*t*t/(1+t*t)**2
matrix_zero(F-s.diag(f, 0), "original_escape_no_new_action")
B = -s.log(1-z*f)  # fixed isospectral heat adds a constant
coords, momenta = (x, y), (px, py)
constraints = s.Matrix([p-s.diff(B, q) for q, p in zip(coords, momenta)])

def bracket(a, b):
    return sum(s.diff(a,q)*s.diff(b,p)-s.diff(a,p)*s.diff(b,q)
               for q,p in zip(coords,momenta))

zero(bracket(constraints[0], constraints[1]), "terminal_constraints_commute_strongly")
V = s.Matrix([y, x])
W = s.Matrix([x*y, 1])
lie = W.jacobian(coords)*V-V.jacobian(coords)*W
JV = (V.T*constraints)[0]
JW = (W.T*constraints)[0]
zero(bracket(JV, JW)+(lie.T*constraints)[0], "vector_constraints_antihomomorphism")
graph = {px:s.diff(B,x), py:s.diff(B,y)}
zero(JV.subs(graph), "all_vector_constraints_zero_on_graph")
zero(bracket(JV,JW).subs(graph), "weak_bracket_zero_for_arbitrary_price")
omega = s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
embedding = s.eye(2).col_join(s.hessian(B, coords))
matrix_zero(embedding.T*omega*embedding, "terminal_graph_is_lagrangian")

# Genuine reflected unitary with freely varying relative query angle.
w, gauge = s.symbols("w gauge", real=True)
delta = w-x-y
Q = s.Matrix([[s.cos(2*delta),s.sin(2*delta)],
              [s.sin(2*delta),-s.cos(2*delta)]])
matrix_zero(Q*Q-I, "reflection_involution")
Fquery = P*Q*(I-P)*Q*P
matrix_zero(Fquery-s.diag(s.sin(2*delta)**2,0), "reflection_return_original_formula")
J = -s.log(1-z*s.sin(2*delta)**2)
fullcoords = (x,y,w,gauge)
H = s.hessian(J, fullcoords)
reduction_results = []
ga,gb,gc = s.symbols("ga gb gc", real=True)
for name, offset, value, curvature in [
    ("commuting",0,0,8*z),
    ("maximal_escape",s.pi/4,-s.log(1-z),-8*z/(1-z))]:
    at = {w:x+y+offset}
    zero(s.diff(J,w).subs(at), name+"_true_internal_stationarity")
    zero(J.subs(at)-value, name+"_stationary_value_constant")
    h = H.subs(at).applyfunc(s.simplify)
    A = h[2:4,2:4]
    mixed = h[2:4,0:2]
    matrix_zero(A-s.diag(curvature,0), name+"_internal_rank_and_gauge_kernel")
    matrix_zero(s.Matrix([[0,1]])*mixed, name+"_ward_range_compatibility")
    G = s.Matrix([[1/curvature,ga],[gb,gc]])
    matrix_zero(A*G*A-A, name+"_all_allowed_generalized_inverses")
    schur = h[0:2,0:2]-mixed.T*G*mixed
    matrix_zero(schur, name+"_full_boundary_schur_is_zero")
    reduction_results.append({"branch":name,"interior_nonzero_curvature":str(curvature),
                              "reduced_boundary_hessian":"zero"})

# Hostile control: projecting a kernel-incompatible source changes the answer.
A_bad = s.diag(2,0)
G0 = s.diag(s.Rational(1,2),0)
G1 = s.diag(s.Rational(1,2),1)
bad_source = s.Matrix([0,1])
matrix_zero(A_bad*G0*A_bad-A_bad, "bad_source_G0_is_generalized_inverse")
matrix_zero(A_bad*G1*A_bad-A_bad, "bad_source_G1_is_generalized_inverse")
incompatible_shift = (bad_source.T*(G1-G0)*bad_source)[0]
zero(incompatible_shift-1, "incompatible_kernel_source_changes_schur")

print(json.dumps({
    "status":"PASS",
    "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "sympy_version":s.__version__,
    "exact_controls":len(checks),
    "checks":checks,
    "reduction_branches":reduction_results,
    "negative_control_generalized_inverse_ambiguity":str(incompatible_shift),
    "scope":"exact original finite return / canonical algebra; no native continuous-admission, full42, local lapse, refinement or GR closure"
}, indent=2, sort_keys=True))
