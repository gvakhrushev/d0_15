#!/usr/bin/env python3
"""Narrow exact checks for the native-price/covariant volume-gauge theorem.

The analytical local solution and Jacobi equivalences are in PROOF.md.
This script neither reruns old suites nor changes its expected evidence.
"""
from pathlib import Path
import hashlib
import json
import sympy as s


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
checks = []


def check(name, condition):
    if not bool(condition):
        raise RuntimeError("FAILED: " + name)
    checks.append(name)


def zero(name, expression):
    check(name, s.factor(expression) == 0)


pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
for row in pins["inputs"]:
    data = (REPO / row["path"]).read_bytes()
    check("source-pin:" + row["path"], hashlib.sha256(data).hexdigest() == row["sha256"])

# Actual Golden detector, calculated in Q[p]/(p^2+p-1) without fitting k.
p, z, x, y = s.symbols("p z x y")


def red(expression):
    num, den = s.fraction(s.cancel(expression))
    num = s.rem(s.Poly(num, p), s.Poly(p**2+p-1, p)).as_expr()
    den = s.rem(s.Poly(den, p), s.Poly(p**2+p-1, p)).as_expr()
    return s.cancel(num/den)


ell = 4*p**2*(1+x)*(1-p**2*(1+x))
B = 4*(p+p**2*y)**2*(1-(p+p**2*y)**2)
A = ell + (1-ell)*B
r = 1-(1-z*B)*(1-z*A)
rx = s.diff(r, x)
ry = s.diff(r, y)
rx0 = red(rx.subs({x: 0, y: 0}))
ry0 = red(ry.subs({x: 0, y: 0}))
k0 = ry0/rx0
Q = 1-z*4*p**3
R = 1-z*4*p**3*(1+p**6)
native_k0 = 2*p**-5*(R/Q+p**6)
zero("actual-finite-z-native-source-ratio", red(ry0-native_k0*rx0))
pval = (s.sqrt(5)-1)/2
actual_k0 = s.N(native_k0.subs({p: pval, z: s.Rational(1, 2**20)}), 45)
check("actual-ratio-positive", actual_k0 > 0)
check("finite-z-ratio-not-zero-z-limit", s.Abs(actual_k0-s.N(10+6*s.sqrt(5), 45)) > s.Rational(1, 10**8))

# Source relation for arbitrary field variations, not ansatz variations.
e, eta, Fx, Fy, Lam, q, q0 = s.symbols("e eta Fx Fy Lam q q0", nonzero=True)
de, dR, dq, dLam, RR = s.symbols("de dR dq dLam RR")
k = Fy/Fx
native_source = eta**2*(Fx*(de*RR+e*dR)-Fy*dq)
aux_source = de*(RR-Lam*(q-q0)) + e*dR-e*dLam*(q-q0)-e*Lam*dq
zero("full-ambient-first-source-map", native_source-eta**2*Fx*aux_source.subs({q:q0, Lam:k/e}))
wrong = native_source-eta**2*Fx*aux_source.subs({q:q0, Lam:2*k/e})
zero("wrong-multiplier-factor-two-defect", wrong-eta**2*Fy*dq)
check("wrong-multiplier-factor-two-is-not-equivalence", wrong != 0)

# Trace and volume gauge hold even when the fixed kinetic sector is zero.
kstar, ystar, qstar, estar, Lstar = s.symbols("kstar ystar qstar estar Lstar", nonzero=True)
zero("trace-gauge-radial-compatibility", (-eta**2*kstar*qstar-kstar*ystar).subs(ystar,-eta**2*qstar))
zero("null-sector-no-division", (-eta**2*kstar*qstar).subs(qstar, 0))
de0, dL0, dq0 = s.symbols("de0 dL0 dq0")
linear_gauge = Lstar*de0+estar*dL0
zero("linearized-volume-gauge", linear_gauge.subs(dL0,-Lstar*de0/estar))
trace_delta_eR = -qstar*linear_gauge-estar*Lstar*dq0
zero("linearized-trace-with-fixed-sector-and-gauge", trace_delta_eR.subs({dL0:-Lstar*de0/estar,dq0:0}))
zero("null-linearized-trace", trace_delta_eR.subs({qstar:0,dq0:0}))

# Genuine positive, nonconstant spacetime volume density; its full Jacobian.
t, u, v, w, c = s.symbols("t u v w c", real=True)
f = (2+t**2)*(1+u**2)*s.exp(v)
T = (2*t+t**3/3)*(1+u**2)*s.exp(v)/c
coords = s.Matrix([T,u,v,w])
J = coords.jacobian([t,u,v,w]).det()
zero("nonconstant-four-dimensional-volume-Jacobian", J-f/c)
zero("volume-gauge-is-exact", f/J-c)
check("volume-map-does-not-preserve-arbitrary-old-collar", s.diff(T,u) != 0)

# All components of div(Lambda K)=sum current_A*dpsi_A+Lambda*dq/2.
# Normal coordinates at a point are enough to check this tensor identity.
metric_inverse = s.diag(1,-1,-1,-1)
ka = [s.Matrix(s.symbols("a0:4")), s.Matrix(s.symbols("b0:4"))]
ha = []
for letter in ("a", "b"):
    h = s.zeros(4)
    for i in range(4):
        for j in range(i,4):
            h[i,j] = h[j,i] = s.Symbol("H"+letter+str(i)+str(j))
    ha.append(h)
L = s.Symbol("L")
dL = s.Matrix(s.symbols("L0:4"))
K = sum((u0*u0.T for u0 in ka), s.zeros(4))
for n in range(4):
    lhs = sum(metric_inverse[m,m]*dL[m]*K[m,n] for m in range(4))
    for u0,H in zip(ka,ha):
        lhs += L*sum(metric_inverse[m,m]*(H[m,m]*u0[n]+u0[m]*H[m,n]) for m in range(4))
    rhs = 0
    for u0,H in zip(ka,ha):
        current = (dL.T*metric_inverse*u0)[0]+L*s.trace(metric_inverse*H)
        dq_n = 2*(u0.T*metric_inverse*H[:,n])[0]
        rhs += current*u0[n]+L*dq_n/2
    zero("complete-two-scalar-conservation-component-"+str(n), lhs-rhs)

# Total-null does not mean rank-one or VSI. This is only an algebraic
# stress fixture; CROSSING_STREAMS.md supplies the actual curved solution.
null_total_K = s.diag(1,1,0,0)
zero("two-scalar-total-null", s.trace(metric_inverse*null_total_K))
check("two-scalar-total-null-rank-two", null_total_K.rank()==2)
check("two-scalar-total-null-tensor-square-positive", s.trace(metric_inverse*null_total_K*metric_inverse*null_total_K)==2)

# Dropping the multiplier equation leaves an actual independent equation.
zero("multiplier-equation-before-gauge", s.diff(-e*Lam*(q-q0),Lam)+e*(q-q0))
check("early-gauge-drops-multiplier-variable", s.diff((-e*Lam*(q-q0)).subs(Lam,c/e),Lam)==0)
check("early-gauge-does-not-imply-kinetic-constraint", (-e*(q-q0)).subs({e:1,q:2,q0:1}) != 0)

result = {
    "status": "PASS",
    "scope": "Exact native coefficient, full source normalization, local volume-gauge/Jacobi identities, both scalar currents, and negative controls; analytical theorem in PROOF.md",
    "checks": len(checks),
    "source_pins": len(pins["inputs"]),
    "native_finite_z_k0": str(actual_k0),
    "two_scalar_total_null_rank": 2,
    "two_scalar_total_null_tensor_square": 2,
    "physical_native_admission": False,
    "off_shell_native_diff_naturality": False,
    "GR_closed": False,
}
print(json.dumps(result, indent=2, ensure_ascii=False))
