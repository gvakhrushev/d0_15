#!/usr/bin/env python3
"""Bounded diagnostic for the original paired Book source, not D0 closure.

Uses the original full CAR16, strict 32D Julia map, 64D paired leakage,
and literal 128D outer Golden word. The proof is in paired_feedback.md, section9.
The native z=2**-20 source is evaluated without subtracting two logdets:
the exact analytic trace is separated from the resolvent remainder.
"""

import numpy as np


p = (np.sqrt(5.0) - 1.0) / 2.0
a = np.sqrt(p)
mesh_h = p
sigma_native = p
alpha = sigma_native * mesh_h**2  # actual B(v)=h**2*B(e), so alpha=p**3
z = 2.0**-20
I16, I32, I64 = np.eye(16), np.eye(32), np.eye(64)


def positive_root(matrix):
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2)
    assert values.min() > 0
    return (vectors * np.sqrt(values)) @ vectors.T


def creation(index):
    result = np.zeros((16, 16))
    for mask in range(16):
        if not (mask >> index) & 1:
            parity = (mask & ((1 << index) - 1)).bit_count()
            result[mask | (1 << index), mask] = (-1) ** parity
    return result


creators = [creation(index) for index in range(4)]


def derivative_lift(matrix):
    result = np.zeros((16, 16))
    for row in range(4):
        for column in range(4):
            result += matrix[row, column] * creators[row] @ creators[column].T
    return result


def exterior_lift(matrix):
    result = np.zeros((16, 16))
    indices = [[index for index in range(4) if (mask >> index) & 1]
               for mask in range(16)]
    for row, left in enumerate(indices):
        for column, right in enumerate(indices):
            if len(left) == len(right):
                result[row, column] = (
                    np.linalg.det(matrix[np.ix_(left, right)]) if left else 1
                )
    return result


eta = np.array([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]], dtype=float)
N = np.zeros((4, 4))
N[1, 2] = N[2, 0] = 1
assert np.array_equal(N.T @ eta + eta @ N, np.zeros((4, 4)))
assert np.array_equal(N @ N @ N, np.zeros((4, 4)))

# The actual sourced Brinkmann face: B=-N and P=exp(-tN), t=c*h**2>0.
D_B = derivative_lift(-N)
A_B, H_B = (D_B - D_B.T) / 2, (D_B + D_B.T) / 2
S0 = np.block([[A_B, a*p*H_B], [-a*p*H_B, -A_B]]) / 2
K = np.block([[p*p*A_B, a*p*A_B - (p/a)*H_B],
              [a*p*A_B + (p/a)*H_B, -p*p*A_B]])
anticommutator = S0 @ K + K @ S0

# This entry equals p**2/2 analytically; it proves the first matrix jet
# is nonzero even though its full trace and the Palatini value are zero.
assert abs(anticommutator[2, 1] - p*p/2) < 1e-15

S = alpha*S0
D = positive_root(I32 + S @ S)
dD = np.linalg.solve(D, S @ S)  # derivative under B -> rho*B at rho=1
assert np.linalg.norm(D @ dD + dD @ D - 2*S @ S) < 1e-13
R = np.block([[S, D], [-D, -S]])
dR = np.block([[S, dD], [-dD, -S]])
G1 = np.block([[alpha*anticommutator, K @ D - D @ K],
               [K @ D - D @ K, alpha*anticommutator]])
dG1 = np.block([[alpha*anticommutator, K @ dD - dD @ K],
                [K @ dD - dD @ K, alpha*anticommutator]])
c_z = 1 - 2*z*p**3
source_t2 = (z*z*p**6/c_z**2)*np.trace(G1 @ dG1)
strict_lower = (2*z*z*p**6*alpha**2/c_z**2)*np.sum(anticommutator**2)
assert source_t2 > 0
assert source_t2 >= strict_lower*(1 - 1e-12)

J0 = np.block([[p*I16, a*I16], [a*I16, -p*I16]])
golden = np.array([[a, -p], [p, a]])
golden64 = np.kron(golden, I64)

print(f"native h=p={mesh_h:.17g}, sigma_native=p={sigma_native:.17g}")
print(f"effective alpha=sigma_native*h^2={alpha:.17g}, z=2^-20={z:.17g}")
print(f"exact nonzero anticommutator entry p^2/2={p*p/2:.17g}")
print(f"d_rho Book coefficient of t^2={source_t2:.17g}")
print(f"proved strict lower coefficient={strict_lower:.17g}")

for t in (0.03, 0.06, 0.12):
    P = np.eye(4) - t*N + t*t*(N @ N)/2
    L = exterior_lift(P)
    J = np.block([[p*L, positive_root(I16 - p*p*L @ L.T)],
                  [positive_root(I16 - p*p*L.T @ L), -p*L.T]])
    V = J0.T @ J
    zeros = np.zeros((32, 32))
    V_pair = np.block([[V, zeros], [zeros, V.T]])
    zeros64 = np.zeros((64, 64))
    W = golden64.T @ np.block([[R, zeros64], [zeros64, V_pair]]) @ golden64
    leakage = W[64:, :64]
    F = p**3*(2*I64 + R @ V_pair - V_pair.T @ R)
    dF = p**3*(dR @ V_pair - V_pair.T @ dR)
    assert np.linalg.norm(W.T @ W - np.eye(128)) < 1e-12
    assert np.linalg.norm(F - leakage.T @ leakage) < 1e-12

    chi = 2*np.arcsinh(t/(2*np.sqrt(2)))
    r_plus = np.sqrt(1 - p*p*np.exp(2*chi))
    r_minus = np.sqrt(1 - p*p*np.exp(-2*chi))
    delta = p*p*(a*(4 + t*t)/(2*(r_plus + r_minus)) - 1)
    exact_T = 4*p*p*t*delta
    assert delta > 0
    assert abs(np.trace(S0 @ V) - exact_T) < 1e-13
    exact_trace_source = 4*p**3*alpha*exact_T

    E = F - 2*p**3*I64
    # Exact resolvent identity. Only the analytically known trace term
    # would suffer cancellation in the direct z*Tr((I-zF)^-1*dF).
    book_source = ((z/c_z)*exact_trace_source
                   + (z*z/c_z)*np.trace(np.linalg.solve(I64-z*F, E @ dF)))
    assert book_source > 0
    print(f"t={t:.2f}: exact trace dilation={exact_trace_source:.17g}; "
          f"whole Book dilation={book_source:.17g}")

print("PASS: original complete paired outer Book has nonzero sourced-family coframe pressure.")
print("Scope: matrix/source check only; inner programme admission and native Cost-Info remain separate.")
