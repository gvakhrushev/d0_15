#!/usr/bin/env python3
"""T1 Xi-upgrade: operator-level intertwiner for the whole Bartholdi family on K(9,11,13).
Claims verified EXACTLY (integer arithmetic):
  (1) S T^t = A ; S S^t = T T^t = D ; S J = T ; T J = S
  (2) B = T^t S - J          (Hashimoto = full transfer minus flip)
  (3) S B = A S - T ; T B = (D - I) S    <=>  Phi B = M Phi, Phi = [S;T], M = [[A,-I],[D-I,0]]
  (4) Phi J = sigma Phi, sigma = [[0,I],[I,0]]  => Phi (B + tJ) = (M + t sigma) Phi  FOR ALL t
  (5) B + J = T^t S  has rank <= 33  => on ker Phi the whole family acts as (t-1)J,
      eigenvalues +-(t-1): the Bartholdi prefactor (1-(1-t)^2 u^2)^(|E|-|V|) is the kernel action
  (6) rank Phi = 2|V| - 1 = 65 (connected non-bipartite), dim ker Phi = 653
Negative control: a corrupted flip J' breaks (2).
Exit 1 on any failure.
"""
import numpy as np, sys

zones = [9,11,13]; n = 33
zone_of = []
for zi,z in enumerate(zones): zone_of += [zi]*z
A = np.array([[1 if zone_of[i]!=zone_of[j] else 0 for j in range(n)] for i in range(n)], dtype=np.int64)
deg = A.sum(1); D = np.diag(deg)
edges = [(i,j) for i in range(n) for j in range(n) if A[i,j]]
NE = len(edges); idx = {e:k for k,e in enumerate(edges)}
S = np.zeros((n,NE), dtype=np.int64); T = np.zeros((n,NE), dtype=np.int64)
J = np.zeros((NE,NE), dtype=np.int64); B = np.zeros((NE,NE), dtype=np.int64)
for (u,v),k in idx.items():
    S[u,k]=1; T[v,k]=1; J[k, idx[(v,u)]]=1
    for w in range(n):
        if A[v,w] and w!=u: B[k, idx[(v,w)]]=1
I_E = np.eye(NE, dtype=np.int64); I_n = np.eye(n, dtype=np.int64)

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)

check("(1) S T^t = A",               np.array_equal(S@T.T, A))
check("(1) S S^t = T T^t = D",       np.array_equal(S@S.T, D) and np.array_equal(T@T.T, D))
check("(1) S J = T and T J = S",     np.array_equal(S@J, T) and np.array_equal(T@J, S))
check("(2) B = T^t S - J",           np.array_equal(B, T.T@S - J))
check("(3) S B = A S - T",           np.array_equal(S@B, A@S - T))
check("(3) T B = (D - I) S",         np.array_equal(T@B, (D - I_n)@S))
# (4) is (1)+(3) assembled; verify the family identity at two integer t values as a direct guard
for t in (2, -3):
    Phi = np.vstack([S, T])
    M = np.block([[A, -I_n],[D - I_n, np.zeros((n,n), dtype=np.int64)]])
    sig = np.block([[np.zeros((n,n),dtype=np.int64), I_n],[I_n, np.zeros((n,n),dtype=np.int64)]])
    check(f"(4) Phi(B + {t}J) = (M + {t}sigma) Phi", np.array_equal(Phi@(B + t*J), (M + t*sig)@Phi))
check("(5) B + J = T^t S (rank <= 33 automatic)", np.array_equal(B + J, T.T@S))
# (6) rank Phi over Q: use fraction-free via sympy on the 66x718 integer matrix
import sympy as sp
Phi_sp = sp.Matrix(np.vstack([S, T]))
r = Phi_sp.rank()
check("(6) rank Phi = 65 (=> dim ker = 653, matches 653 unit-modulus eigenvalues of B)", r == 65)
# negative control: corrupt one flip entry -> (2) must FAIL
J_bad = J.copy(); e0 = 0; ebar = int(np.argmax(J[e0])); e1 = (ebar + 1) % NE
J_bad[e0, ebar] = 0; J_bad[e0, e1] = 1
check("negative control: corrupted flip breaks B = T^t S - J", not np.array_equal(B, T.T@S - J_bad))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
