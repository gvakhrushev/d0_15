#!/usr/bin/env python3
"""Exact controls for the fixed-programme preparation source and native clock.

This checks the declared mathematical hypotheses, not physical D0 admission.
Run from any directory; output is deterministic JSON, no files are modified.
"""
import json
import sympy as s

checks = []


def require(label, condition):
    if not bool(condition):
        raise AssertionError(label)
    checks.append(label)


def zero_matrix(m):
    return all(s.simplify(v) == 0 for v in m)


# Complete fixed-jointRIGHT tangent lift, including unused LEFT dimensions.
M = s.Matrix([[1, 0], [0, 2], [0, 0]])
V = s.Matrix([[0, -2], [1, 0], [3, 4]])
Sigma = M.T * M
Sinv = Sigma.inv()
K = V * Sinv * M.T - M * Sinv * V.T - M * Sinv * (M.T * V) * Sinv * M.T
require("rectangular tangent preserves complete RIGHT Gram", zero_matrix(M.T * V + V.T * M))
require("explicit compensating generator is skew real", zero_matrix(K.T + K))
require("explicit generator realizes the encoder tangent", zero_matrix(K * M - V))
Ms = M.row_join(s.zeros(3, 1))
Vs = V.row_join(s.zeros(3, 1))
Sp = s.diag(1, s.Rational(1, 4), 0)
Ks = Vs * Sp * Ms.T - Ms * Sp * Vs.T - Ms * Sp * (Ms.T * Vs) * Sp * Ms.T
require("same lift includes a singular RIGHT support", zero_matrix(Ks - K) and zero_matrix(Ks * Ms - Vs))

# Literal GoldenCoherentMemory.fullStep, not a replacement unitary.
p = (s.sqrt(5) - 1) / 2
a = s.sqrt(p)
G = s.Matrix([[a, -p], [p, a]])
step = s.Matrix([[a, 0, -p, 0], [0, a, 0, -p], [0, p, 0, a], [p, 0, a, 0]])
require("literal original Golden fullStep is orthogonal", zero_matrix(step.T * step - s.eye(4)))
c, d = s.symbols("c d", real=True)
R = s.Matrix([[c, -d], [d, c]])
r = s.Rational(1, 3)
S = s.diag(s.sqrt(r), s.sqrt(1 - r))
encoded = G.T * R * S
output = s.zeros(8, 1)
for right in range(2):
    inp = s.Matrix([encoded[0, right], 0, encoded[1, right], 0])
    out = (step * inp).applyfunc(s.simplify)
    for left_fresh in range(4):
        output[2 * left_fresh + right] = out[left_fresh]
expected = s.Matrix([s.sqrt(r) * c, -s.sqrt(1-r) * d, 0, 0,
                     0, 0, s.sqrt(r) * d, s.sqrt(1-r) * c])
require("all eight coherent output coordinates match original fullStep", zero_matrix(output - expected))
require("RIGHT Gram is constant on rotation circle", zero_matrix(
    (encoded.T * encoded - (c*c+d*d) * S*S).applyfunc(s.simplify)))
require("base input uses Golden constants and fair normalization", zero_matrix(
    (G.T * s.Matrix([1, 1]) / s.sqrt(2) - s.Matrix([a+p, a-p]) / s.sqrt(2))))

# All four nonzero pointer events are retained; other full-basis events are zero.
x, u = s.symbols("x u", real=True)
t = x + u + s.pi/4
q = [r*s.cos(t)**2, (1-r)*s.sin(t)**2,
     r*s.sin(t)**2, (1-r)*s.cos(t)**2]
at0 = {x: 0, u: 0}
q0 = [v.subs(at0) for v in q]
require("full pointer law is normalized and strictly positive at centre",
        s.simplify(sum(q)-1) == 0 and all(v > 0 for v in q0))
variables = (x, u)
dq = s.Matrix([[s.diff(v, z).subs(at0) for z in variables] for v in q])
grad = s.Matrix([sum(dq[j, i]*(s.log(q0[j])+1) for j in range(4)) for i in range(2)])
hess = s.Matrix(2, 2, lambda i, k: s.simplify(sum(
    s.diff(q[j], variables[i], variables[k]).subs(at0)*(s.log(q0[j])+1)
    +dq[j, i]*dq[j, k]/q0[j] for j in range(4))))
require("Cost minus pointer Info has a genuine preparation minimum", zero_matrix(grad) and hess[1, 1] == 4)
require("unreduced native Hessian is nonzero", hess == 4*s.ones(2))
schur = s.simplify(hess[0, 0]-hess[0, 1]**2/hess[1, 1])
require("joint preparation Schur vanishes exactly", schur == 0)
exact_section = expected.subs({c: s.cos(t), d: s.sin(t)}).subs(u, -x)
require("stationary section preserves ENTIRE coherent output", zero_matrix(
    exact_section-expected.subs({c: 1/s.sqrt(2), d: 1/s.sqrt(2)})))
require("faithful reference128 extension keeps its complete Gram",
        s.kronecker_product(S*S, s.eye(64)/64).trace() == 1
        and s.kronecker_product(S*S, s.eye(64)/64).rank() == 128)
kappa = s.symbols("kappa", positive=True)
paid_schur = s.factor(4-16/(4+kappa))
require("real preparation price controls the restored response", paid_schur == 4*kappa/(4+kappa))

# ORIGINAL K(9,11,13), all 33 vertices and all 718 directed edges.
zones = [0]*9 + [1]*11 + [2]*13
A = s.Matrix(33, 33, lambda i,j: int(zones[i] != zones[j]))
require("original graph contains all 718 directed edges", sum(A) == 718)
require("original complete depths are 718 and 7722", s.trace(A*A) == 718 and s.trace(A*A*A) == 7722)
require("rooted original depths are 24 and 286", (A*A)[0,0] == 24 and (A*A*A)[0,0] == 286)
# Symbolic aggregate compression of symmetric K=p D A D.
aa, bb, cc, lam = s.symbols("a b c lambda", positive=True)
Q = s.Matrix([[0, bb, cc], [aa, 0, cc], [aa, bb, 0]])
ss = aa*bb+aa*cc+bb*cc
rr = aa*bb*cc
require("three aggregate Perron polynomial is exact",
        s.expand((lam*s.eye(3)-Q).det()-(lam**3-ss*lam-2*rr)) == 0)
require("full native clock ratio is fixed by exact traces",
        s.trace(Q**2) == 2*ss and s.trace(Q**3) == 6*rr)
root_ratio = 2*p*bb*cc/(bb+cc)
require("rooted clock cancels every A-zone Info derivative", s.diff(root_ratio, aa) == 0)
# In log(a),log(b),log(c), differentiate the SAME Perron equation implicitly.
agg = (aa, bb, cc)
base = {aa: 1, bb: 1, cc: 1, lam: 2}
poly = lam**3-ss*lam-2*rr
Ei = lambda f,i: s.expand(agg[i]*s.diff(f, agg[i]))
lambda_i = [-Ei(poly,i).subs(base)/s.diff(poly,lam).subs(base) for i in range(3)]
lambda_ij = s.Matrix(3,3,lambda i,j: s.simplify(-(
    Ei(Ei(poly,i),j).subs(base)
    +Ei(s.diff(poly,lam),i).subs(base)*lambda_i[j]
    +Ei(s.diff(poly,lam),j).subs(base)*lambda_i[i]
    +s.diff(poly,lam,lam).subs(base)*lambda_i[i]*lambda_i[j]
    )/s.diff(poly,lam).subs(base)))
clock_hess = s.Matrix(3,3,lambda i,j: s.simplify(
    Ei(Ei(s.log(rr)-s.log(ss),i),j).subs(base)
    -(lambda_ij[i,j]/2-lambda_i[i]*lambda_i[j]/4)))
target = -s.Rational(4,9)*(s.eye(3)-s.ones(3)/3)
require("full clock completion is a strict shape MAXIMUM", clock_hess == target and clock_hess.eigenvals() == {-s.Rational(4,9):2, s.Integer(0):1})
shape_grad = [1-Ei(ss,i)/ss+(Ei(poly,i)/s.diff(poly,lam))/lam for i in range(3)]
require("balanced aggregates are the ONLY stationary shapes", s.factor(
    shape_grad[0]-shape_grad[1]+3*lam**2*cc*(aa-bb)/(ss*(3*lam**2-ss))) == 0)
# AMGM s^3>=27r^2 implies polynomial(6r/s)<=0, hence lambda>=6r/s.
require("global maximum follows from the original Perron cubic", s.factor(poly.subs(lam,6*rr/ss) - 8*rr*(27*rr**2-ss**3)/ss**3) == 0)
# Original unmodified Info=0 aggregates (9,11,13); PF isolated symbolically.
orig = {aa:9, bb:11, cc:13}
numeric_lambda = s.nsolve(poly.subs(orig), 22, prec=50)
pi_zone = [s.N((-Ei(poly,i)/s.diff(poly,lam)/lam).subs(orig).subs(lam,numeric_lambda),25) for i in range(3)]
clock_zone = [s.simplify(Ei(s.log(rr)-s.log(ss),i).subs(orig)) for i in range(3)]
residual = [s.N(clock_zone[i]-pi_zone[i],20) for i in range(3)]
require("original Perron zone masses are strictly positive", all(v > 0 for v in pi_zone))
require("uniform clock Ward cancellation leaves nonzero shape source", abs(float(sum(residual))) < 1e-18 and all(abs(float(v)) > 0.001 for v in residual))

result = {
    "status":"PASS", "groups":len(checks), "checks":checks,
    "native_golden":{"pointer_centre":[str(v) for v in q0],
        "cost_minus_info_hessian_natural_units":[list(hess.row(i)) for i in range(2)],
        "joint_schur":str(schur), "paid_preparation_schur":str(paid_schur)},
    "native_clock":{"original_aggregate_Perron":str(numeric_lambda),
        "original_zone_Perron_masses":[str(v) for v in pi_zone],
        "original_zone_clock_covector":[str(v) for v in clock_zone],
        "original_zone_residual":[str(v) for v in residual],
        "balanced_log_aggregate_hessian_natural_units":[[str(v) for v in clock_hess.row(i)] for i in range(3)]},
    "scope":{"physical_full_price_selected":False,"all_LEFT_prep_tangents_physically_admitted":False,
        "original_full128_Kraus_replayed":False,"GR_closed":False}
}
print(json.dumps(result, indent=2, default=str)+"\n", end="")
