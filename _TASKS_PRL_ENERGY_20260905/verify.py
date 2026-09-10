#!/usr/bin/env python3
"""Exact finite D0 calculation, with a numerical collision-limit illustration.

Dependencies: sympy, numpy. No network, no repository mutations.
The source matrices are parsed from the existing Lean owner, not fitted here.
Analytic inequalities are proved in README.md; sampling is not their proof.
"""
from pathlib import Path
import hashlib
import json
import re

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "09_LEAN_FORMALIZATION/D0/Integration/V15/RawZone.lean"
source_text = SOURCE.read_text()
checks = []


def source_matrix(name):
    pattern = rf"def {re.escape(name)}\s*:.*?:=\s*!!\[([^\]]+)\]"
    match = re.search(pattern, source_text)
    if match is None:
        raise RuntimeError(f"Cannot read source matrix {name}")
    return s.Matrix([[s.Rational(v.strip()) for v in row.split(",")]
                     for row in match.group(1).split(";")])


def zero(name, expr):
    entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    remainder = [s.simplify(v) for v in entries]
    if any(v != 0 for v in remainder):
        raise AssertionError((name, remainder))
    checks.append(name)


G, D, A = (source_matrix(name) for name in ("G", "DW", "AW"))
K = D * A - A * D
I = s.eye(3)
lam2 = s.Integer(2840)
lam = s.sqrt(lam2)
P = -K**2 / lam2
P0 = I - P
zero("canonical adjoint", K.T * G + G * K)
zero("annihilator", K**3 + lam2 * K)
zero("projector idempotence", P**2 - P)
zero("complementary projectors", P0 * P)
zero("projector adjoint", P.T * G - G * P)
zero("neutral kernel", K * P0)

q = s.Matrix([0, 1, 2])
r = K * q
X = q.row_join(r)
Q = (q / s.sqrt(63)).row_join(r / (lam * s.sqrt(63)))
J2 = s.Matrix([[0, -1], [1, 0]])
zero("active plane metric", X.T * G * X - s.diag(63, 178920))
zero("orthonormal frame", Q.T * G * Q - s.eye(2))
zero("rotation intertwiner", K * Q - Q * (lam * J2))
zero("intrinsic active plane", Q * Q.T * G - P)

c, b, d, e = s.symbols("c b d e", real=True)


def flow_poly(cosine, sine_over_lambda):
    return P0 + cosine * P + sine_over_lambda * K


U = flow_poly(c, b)
zero("flow metric identity", U.T * G * U - G -
     (c*c + lam2*b*b - 1) * G * P)
zero("flow composition", U * flow_poly(d, e) -
     flow_poly(c*d - lam2*b*e, c*e + b*d))
t = s.symbols("t", real=True)
Ut = flow_poly(s.cos(lam*t), s.sin(lam*t)/lam)
zero("flow differential equation", s.diff(Ut, t) - K * Ut)

H = s.I * K
Pm, Pp = (P - H/lam)/2, (P + H/lam)/2
zero("energy adjoint", H.conjugate().T * G - G * H)
for label, Pi, Ei in (("minus", Pm, -lam), ("neutral", P0, 0), ("plus", Pp, lam)):
    zero(f"energy projector {label}", Pi**2 - Pi)
    zero(f"energy effect adjoint {label}", Pi.conjugate().T * G - G * Pi)
    zero(f"energy eigenvalue {label}", H * Pi - Ei * Pi)
    zero(f"energy conservation {label}", U * Pi - Pi * U)
zero("energy resolution", Pm + P0 + Pp - I)
zero("energy-projector disjointness", Pm * Pp)

p = (s.sqrt(5) - 1)/2
theta = s.asin(p)
zero("golden normalization", p + p*p - 1)
Sphi = flow_poly(s.sqrt(p), p/lam)
Rphi = s.sqrt(p)*s.eye(2) + p*J2
zero("golden gate intertwiner", Sphi * Q - Q * Rphi)
zero("golden gate normalization", Rphi.T * Rphi - s.eye(2))
v = q/s.sqrt(63)
zero("saturating state mean", (v.T * G * H * v)[0])
zero("saturating state variance", (v.T * G * H**2 * v)[0] - lam2)
zero("saturating state overlap", (v.T * G * Ut * v)[0] - s.cos(lam*t))
zero("one-tick transfer response", (Q[:, 1].T * G * Sphi * v)[0]**2 - p*p)

# Full associative algebra: construct matrix units from the two source operators.
degrees = [D[i, i] for i in range(3)]
projectors = []
for i in range(3):
    Ei = I
    for j in range(3):
        if i != j:
            Ei = Ei * (D - degrees[j]*I)/(degrees[i] - degrees[j])
    expected = s.zeros(3)
    expected[i, i] = 1
    zero(f"degree projector {i}", Ei - expected)
    projectors.append(Ei)
for i in range(3):
    for j in range(3):
        expected = s.zeros(3)
        expected[i, j] = 1
        Mij = projectors[i] if i == j else projectors[i] * A * projectors[j] / A[i, j]
        zero(f"constructed matrix unit {i}{j}", Mij - expected)

# Conditional control algebra: if these two continuous generators are admissible,
# their Lie algebra is the full traceless G-skew-Hermitian algebra.
L = [s.I*(D - s.trace(D)/3*I), s.I*A]
L.extend([L[0]*L[1]-L[1]*L[0]])
L.extend([L[0]*L[2]-L[2]*L[0]])
L.extend([L[1]*L[2]-L[2]*L[1]])
L.extend([L[0]*L[3]-L[3]*L[0]])
L.extend([L[1]*L[3]-L[3]*L[1]])
L.extend([L[2]*L[3]-L[3]*L[2]])
rank = s.Matrix.hstack(*(Li.reshape(9, 1) for Li in L)).rank()
if rank != 8:
    raise AssertionError(("control Lie rank", rank))
checks.append("conditional control Lie rank 8")
for i, Li in enumerate(L):
    zero(f"control adjoint {i}", Li.conjugate().T * G + G * Li)
    zero(f"control trace {i}", s.trace(Li))

# Negative controls: metric, lost coupling, insufficient single-generator group.
if K.T + K == s.zeros(3):
    raise AssertionError("ordinary metric must fail")
zero("negative control: diagonal adjacency", D*s.diag(1,2,3)-s.diag(1,2,3)*D)
zero("single-flow invariant state 1", K*P0-P0*K)
zero("single-flow invariant state 2", K*(P/2)-(P/2)*K)
if P0 == P/2:
    raise AssertionError("the two invariant density operators must differ")
checks.append("single flow has multiple invariant states")

# Independent check of the partial-SWAP reduction in a two-level complex example.
rho2 = s.Matrix([[s.Rational(2,3), s.I/6],[-s.I/6,s.Rational(1,3)]])
sig2 = s.Matrix([[s.Rational(3,5),s.Rational(1,10)],[s.Rational(1,10),s.Rational(2,5)]])
swap = s.zeros(4)
for i in range(2):
    for j in range(2):
        swap[2*j+i, 2*i+j] = 1
joint = s.kronecker_product(rho2, sig2)
V = c*s.eye(4)-s.I*b*swap
joint_after = V*joint*V.conjugate().T
reduced = s.Matrix(2, 2, lambda i,j: sum(joint_after[2*i+k,2*j+k] for k in range(2)))
zero("partial-SWAP finite reduction", reduced -
     (c*c*rho2+b*b*sig2-s.I*c*b*(sig2*rho2-rho2*sig2)))

# Numerical illustration only. These matrices are in the energy eigenbasis.
theta_num = float(theta)
energies = np.array([-theta_num, 0., theta_num])
sigma_diag = np.array([0., 1/3, 2/3])
psi = np.array([1., 0., 1.])/np.sqrt(2)
rho = np.outer(psi, psi)
target = np.exp(-1j*(energies[:, None]-energies[None, :])) * rho
collision_time = 3*theta_num
collision_rows = []
for n in (16, 64, 256, 1024):
    delta = collision_time/n
    co, si = np.cos(delta), np.sin(delta)
    factor = co*co-1j*co*si*(sigma_diag[:,None]-sigma_diag[None,:])
    reduced_n = factor**n*rho
    np.fill_diagonal(reduced_n, sigma_diag + (co*co)**n*(np.diag(rho)-sigma_diag))
    error = float(np.sum(np.abs(np.linalg.eigvalsh(reduced_n-target))))
    bound = min(2., 4*collision_time**2/n)
    if not (0 <= error <= bound + 1e-12):
        raise AssertionError((n, error, bound))
    if np.linalg.eigvalsh(reduced_n).min() < -1e-12 or abs(np.trace(reduced_n)-1) > 1e-12:
        raise AssertionError("invalid reduced state")
    collision_rows.append({"n": n, "trace_norm_error": error, "proved_bound": bound})

print(json.dumps({
    "status": "PASS",
    "scope": "finite algebra; analytic proofs in README; no physical clock identification",
    "source": str(SOURCE.relative_to(ROOT)),
    "source_sha256": hashlib.sha256(source_text.encode()).hexdigest(),
    "exact_checks": len(checks),
    "checks": checks,
    "lambda": float(lam),
    "theta": theta_num,
    "matching_flow_parameter": float(theta/lam),
    "orthogonal_time_in_interpolated_ticks": float(s.pi/(2*theta)),
    "conditional_control_lie_rank": rank,
    "collision_limit": collision_rows,
}, indent=2, ensure_ascii=False))
