#!/usr/bin/env python3
"""vp_kernel_zone_split.py - D0 certificate (exact integer linear algebra)

CLAIM (THE): the adjacency matrix of the scene K(9,11,13) on N=33 vertices has
rank 3 (= the three transport modes = space) and nullity 30 (= the dark archive),
and the 30-dim kernel splits by zone as 30 = 8 + 10 + 12 (within-zone difference
vectors). Uses exact integer/Fraction arithmetic, no floats.
"""
from fractions import Fraction as F

ZONES = [9, 11, 13]
N = sum(ZONES)                      # 33
assert N == 33

# block boundaries
starts = [0, 9, 20]                 # [0, 9, 9+11]
def zone_of(i):
    if i < 9: return 0
    if i < 20: return 1
    return 2

# complete tripartite adjacency: A[i][j]=1 iff different zones
A = [[1 if zone_of(i) != zone_of(j) else 0 for j in range(N)] for i in range(N)]
edges = sum(sum(row) for row in A) // 2
assert edges == 9 * 11 + 11 * 13 + 13 * 9 == 359
print(f"[1] K(9,11,13): |V|={N}, |E|={edges}=359  PASS")

# exact rational rank via Gaussian elimination
def rank(mat):
    M = [[F(x) for x in row] for row in mat]
    r = 0
    rows, cols = len(M), len(M[0])
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [x / inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

rk = rank(A)
nullity = N - rk
assert rk == 3, rk
assert nullity == 30, nullity
print(f"[2] rank(A)={rk} (space), nullity={nullity} (archive)  PASS")

# zone split: within-zone difference vectors lie in the kernel.
# For zone z of size s, the (s-1) vectors e_{first} - e_{k} are in ker(A) because
# A acts equally on all vertices of a zone (constant row pattern across the zone).
def in_kernel(v):
    return all(sum(A[i][j] * v[j] for j in range(N)) == 0 for i in range(N))

dims = []
ker_vectors = []
for z, s in enumerate(ZONES):
    base = starts[z]
    d = 0
    for k in range(1, s):
        v = [0] * N
        v[base] = 1
        v[base + k] = -1
        assert in_kernel(v), (z, k)
        ker_vectors.append(v)
        d += 1
    dims.append(d)
assert dims == [8, 10, 12], dims
assert sum(dims) == 30
print(f"[3] kernel zone split 30 = {dims[0]}+{dims[1]}+{dims[2]} (within-zone diffs, all in ker)  PASS")

# the 30 zone vectors are independent and therefore span the 30-dim kernel
assert rank(ker_vectors) == 30
print("[4] the 30 zone difference vectors are independent -> span ker(A)  PASS")

print("\n[STATUS] THE: rank 3 / nullity 30 with exact zone split 8+10+12 (exact integer LA).")
print("[CERT-CLOSED] PASS_KERNEL_ZONE_SPLIT")
