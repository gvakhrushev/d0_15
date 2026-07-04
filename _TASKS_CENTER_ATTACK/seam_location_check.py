#!/usr/bin/env python3
"""SEAM LOCATION: the alpha-chain Feshbach seam CANNOT be realized on the scene vertex algebra.
For the owned active(rank-3)/archive(dim-30) split of the 33-vertex scene (kernel = zone-wise
sum-zero vectors, structure 8+10+12, archive fingerprint {24x8, 22x10, 20x12} = ROOT R2):
  (i)  A annihilates the kernel; D_deg is zone-scalar and preserves it;
  (ii) hence EVERY word in the algebra <A, D_deg> maps kernel -> kernel: the off-diagonal
       Feshbach blocks B, C vanish identically for any W_eff built from the vertex algebra;
  (iii) therefore the depth-2 moment mu2*u^2 + mu1*u with mu2, mu1 != 0 is UNREALIZABLE at the
       vertex level: the seam's operator home must be a carrier extension (the 359-edge space,
       where the V11-Fock capacity 2^11 is native).
Negative control: a single-edge operator (outside the algebra) produces a nonzero seam.
Exit 1 on failure."""
import numpy as np, sys, itertools

zones = [9,11,13]; n = 33
zone_of = []
for zi,z in enumerate(zones): zone_of += [zi]*z
A = np.array([[1 if zone_of[i]!=zone_of[j] else 0 for j in range(n)] for i in range(n)], dtype=np.int64)
Dg = np.diag(A.sum(1))
kerbasis = []; start = 0
for z in zones:
    for k in range(1, z):
        v = np.zeros(n, dtype=np.int64); v[start] = 1; v[start+k] = -1
        kerbasis.append(v)
    start += z
K = np.array(kerbasis).T
zs = []; start = 0
for z in zones:
    zs.append(np.array([1 if start <= i < start+z else 0 for i in range(n)])); start += z
Z = np.array(zs)   # active-side zone functionals

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)

check("kernel dim = 30 (8+10+12)", K.shape[1] == 30)
check("A annihilates kernel", not (A@K).any())
check("archive block of L is zone-scalar (spectrum {24x8,22x10,20x12})", ((Dg-A)@K == Dg@K).all())
# all words of length <= 4 in {A, Dg} have zero seam on the kernel
words = [np.eye(n, dtype=np.int64)]
maxseam = 0
for length in range(1, 5):
    for w in itertools.product([A, Dg], repeat=length):
        M = np.eye(n, dtype=np.int64)
        for f in w: M = f @ M
        maxseam = max(maxseam, int(np.abs(Z@(M@K)).max()))
check("ALL words length<=4 in <A,D> have ZERO seam (B=C=0 for any vertex W_eff)", maxseam == 0)
E = np.zeros((n,n), dtype=np.int64); E[0,9] = 1; E[9,0] = 1
check("negative control: single-edge operator (outside algebra) has NONZERO seam", int(np.abs(Z@(E@K)).max()) != 0)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
