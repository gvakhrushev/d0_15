"""Exact fullStep-only local compiler identities; no numerical rank extrapolation.

This certificate verifies the finite algebra used by FULLSTEP_COMPILATION_RU.md.
Density and effective search termination follow from its proof.  It does not
claim physical actuation from membership in an AF matrix algebra.
"""

from pathlib import Path
import hashlib
import json
import re

import sympy as s


REPO = Path(__file__).resolve().parents[4]
SOURCE = REPO / "03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean"
source_bytes = SOURCE.read_bytes()
source_text = source_bytes.decode("utf-8")
a = s.Symbol("a", real=True)
p = a**2
minimal = a**4 + a**2 - 1
checks = []


def reduce_scalar(x):
    return s.rem(s.expand(x), minimal, a)


def reduced(M):
    return s.Matrix(M).applyfunc(reduce_scalar)


def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    checks.append(label)


def equal(A, B, label):
    require(all(x == 0 for x in reduced(s.Matrix(A) - s.Matrix(B))), label)


def comm(A, B):
    return reduced(A * B - B * A)


def conjugate(U, A):
    return reduced(U * A * U.T)


match = re.search(r"def fullStep\b.*?!!\[(.*?)\]", source_text, re.S)
if match is None:
    raise ArithmeticError("original Lean fullStep definition absent")
rows = match.group(1).split(";")
W = s.Matrix([
    [s.sympify(entry, locals={"a": a, "p": p}) for entry in row.split(",")]
    for row in rows
])
require(W.shape == (4, 4), "original fullStep has all four rows and columns")

I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Z = s.diag(1, -1)
J = s.Matrix([[0, -1], [1, 0]])
G = s.Matrix([[a, -p], [p, a]])
CX = s.Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
               [0, 0, 0, 1], [0, 0, 1, 0]])
kron = s.kronecker_product
equal(W, CX * kron(G, I), "literal fullStep is CX after original G")
equal(W.T * W, s.eye(4), "literal fullStep is orthogonal on all columns")
require(reduce_scalar(W.det()) == -1, "literal fullStep determinant is minus one")

T1, T2 = kron(W, I), kron(I, W)
X3 = kron(s.eye(4), X)
equal(T1 * X3, X3 * T1, "first neighbor copy preserves X on third wire")
equal(T2 * X3, X3 * T2, "second neighbor copy preserves X on third wire")

# Columns first span the X3=+1 block, then the X3=-1 block.  Q^T Q=2I.
Q = s.zeros(8)
for j in range(4):
    Q[2*j, j] = Q[2*j+1, j] = 1
    Q[2*j, 4+j] = 1
    Q[2*j+1, 4+j] = -1
equal(Q.T * Q, 2*s.eye(8), "complete block coordinates retain every column")
equal(Q.T*T1*Q/2, s.diag(W, W), "first neighbor block decomposition")
S = kron(I, Z*G)
equal(Q.T*T2*Q/2, s.diag(kron(I, G), S),
      "second neighbor block decomposition")
equal(S*S, s.eye(4), "minus block of second copy is an involution")
equal(Q.T*T2*T2*Q/2, s.diag(kron(I, G*G), s.eye(4)),
      "positive even powers supply only the plus-block Lie seed")

B = kron(I, J)
C = conjugate(W, B)
E = conjugate(W, C)
F = comm(B, E)
H = conjugate(W, E)
K = comm(C, H)
basis = [kron(J, I), kron(I, J), kron(J, X),
         kron(J, Z), kron(X, J), kron(Z, J)]
equal(s.Matrix([[(u.T*v).trace() for v in basis] for u in basis]),
      4*s.eye(6), "six skew Pauli matrices form an orthogonal so4 basis")
columns = [B, C, E, F, H, K]
coefficients = reduced(s.Matrix([
    [(u.T*v).trace()/4 for v in columns] for u in basis
]))
expected = s.Matrix([
    [0, 0, 0,     0,     0,      4*a*p],
    [1, 0, 2*p-1, 0,     0,      0],
    [0, 0, 0,     4*a*p, 0,      0],
    [0, 0, 2*a*p, 0,     0,      0],
    [0, 0, 0,     0,     2*a*p,  0],
    [0, 1, 0,     0,     2*p-1,  0],
])
equal(coefficients, expected, "displayed exact six-column coefficient matrix")
for j, v in enumerate(columns):
    reconstructed = s.zeros(4)
    for i, u in enumerate(basis):
        reconstructed += coefficients[i, j]*u
    equal(v, reconstructed, "all entries reconstructed for Lie column " + str(j+1))
det = reduce_scalar(coefficients.det())
require(reduce_scalar(det + 64*p**6) == 0,
        "exact determinant is minus 64 p^6, nonzero for p positive")

A = kron(J, I+X)
equal(W*W, s.eye(4) + a*p*A + p**2*A*A/2,
      "W squared is the same-angle A rotation")
Aprime = conjugate(S, A)
equal(Aprime, kron(J, I-(2*p-1)*X-2*a*p*Z),
      "minus-block conjugate has the displayed exact coefficients")
equal(comm(A, Aprime), 4*a*p*B,
      "minus-block commutator gives the same nonzero Lie seed")
require(reduce_scalar(S.det()) == 1,
        "second neighbor lies in the positive determinant component in both blocks")

P = s.diag(1, 0, 0, 0)
equal(P*W*P, a*P, "fresh pair has exact scalar blank corner sqrt(p)")
equal(P*W.T*(s.eye(4)-P)*W*P, p**2*P,
      "fresh pair retains its entire leakage in the true full feedback")

result = {
    "schema": "d0.fullstep-local-compiler-exact-check/1",
    "status": "PASS",
    "source": str(SOURCE.relative_to(REPO)),
    "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "coefficient_field": "Q(a), a^4+a^2-1=0, a>0, p=a^2",
    "lie_basis_dimension": 6,
    "determinant": "-64*p^6",
    "determinant_reduced": str(det),
    "fullstep_only_generators": ["W12", "W23"],
    "positive_word_density_proof": "FULLSTEP_COMPILATION_RU.md sections 1-3",
    "physical_actuation_claimed_from_algebra_membership": False,
    "checks": checks,
    "check_count": len(checks),
}
print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
