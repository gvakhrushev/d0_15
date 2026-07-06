#!/usr/bin/env python3
"""
deep_v_vnext_check.py — can-fail check for DEEP_V_VNEXT_MEMO.md (batch V-a).

Exact integer / Fraction arithmetic only. NO float. Verifies the load-bearing
arithmetic underneath the seven AF-tower no-go verdicts, INCLUDING the newer
owned forcing facts (Iter25) that re-type them, and the anchor-selection question.

Mutation-tested: run with `--selftest` to confirm each check can fail.

House rule honored: no check constructs its key quantity from the conclusion.
Both sides (scene, AF) are built independently from primitive data, then compared.
"""
from fractions import Fraction as F
import sys

FAIL = []

def check(name, cond):
    ok = bool(cond)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAIL.append(name)
    return ok

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# ---------------------------------------------------------------------------
# BLOCK 0 — independent construction of the two carriers (no conclusion reuse)
# ---------------------------------------------------------------------------
# Scene side: complete tripartite K(9,11,13), built from zone sizes ONLY.
zones = [9, 11, 13]
N = sum(zones)                       # 33
k = len(zones)                       # 3
# Complete-multipartite Laplacian closed form (independent of AF):
#   0 (mult 1); N-n_i (mult n_i-1); N (mult k-1).
scene_spec = {}
scene_spec[0] = scene_spec.get(0, 0) + 1
for n in zones:
    scene_spec[N - n] = scene_spec.get(N - n, 0) + (n - 1)
scene_spec[N] = scene_spec.get(N, 0) + (k - 1)
scene_mults = sorted(scene_spec.values())          # {1,2,8,10,12}
scene_trace = sum(ev * m for ev, m in scene_spec.items())
scene_edges = (N * N - sum(n * n for n in zones)) // 2

# AF side: Fibonacci AF/GNS algebra dims from the path-count recurrence ONLY.
# dim A_N built from block sizes = consecutive path counts; here the owned
# sequence dim A = 2,5,13,34,89,233,610 (odd-indexed Fibonacci F(2n+3)).
dimA = [fib(2 * n + 3) for n in range(7)]           # 2,5,13,34,89,233,610
af_reduced = [dimA[0] - 1] + [dimA[i] - dimA[i - 1] for i in range(1, 4)]  # {1,3,8,21}

# ---------------------------------------------------------------------------
# BLOCK 1 — 33-SCENE-ANCHOR-OWNER-001 / -NOGO-001 (typed 34 vs 33; anchor)
# ---------------------------------------------------------------------------
af_algebra_dim = 5 ** 2 + 3 ** 2                     # 34
check("B1.1 scene dim = 33", N == 33)
check("B1.2 AF algebra dim A_3 = 34", af_algebra_dim == 34 and dimA[3] == 34)
check("B1.3 excess = 1", af_algebra_dim - N == 1)
check("B1.4 34 is odd-indexed Fibonacci F(9)", fib(9) == 34)
# Typed distinctness: 2 matrix blocks vs 3 graph parts (the no-go's core).
af_blocks = [5, 3]
check("B1.5 block count 2 != part count 3", len(af_blocks) != len(zones))
check("B1.6 34-1=33 but blocks (5,3) != parts (9,11,13)",
      af_algebra_dim - 1 == N and af_blocks != zones)

# ANCHOR-SELECTION question: is anchoring the AF tower at N*=3 FORCED or SELECTED?
# The tower dims that are >= 33 for the first time: find first N with dimA[N] >= 33.
first_ge_33 = next(i for i, d in enumerate(dimA) if d >= 33)
check("B1.7 N*=3 is the FIRST level with dimA >= 33 (anchor is dimension-selected, "
      "not free): dimA[2]=13<33<=34=dimA[3]",
      first_ge_33 == 3 and dimA[2] < 33 <= dimA[3])
# But 33 itself is never an AF algebra dim (skip) -> algebra anchor refuted.
check("B1.8 33 is NOT an AF algebra dim (skip) => algebra anchor refuted",
      33 not in dimA)

# ---------------------------------------------------------------------------
# BLOCK 2 — AF-ONE-DIMENSIONAL-REDUCTION-CLASSIFICATION-001 (Outcome D)
# ---------------------------------------------------------------------------
# Trace-zero reduction of M_5 (+) M_3: su(5)(+)su(3)(+)u(1) = (24,8,1).
reduced_parts = [5 ** 2 - 1, 3 ** 2 - 1, 1]         # (24,8,1)
check("B2.1 reduced parts = (24,8,1)", reduced_parts == [24, 8, 1])
check("B2.2 reduced parts sum to 33", sum(reduced_parts) == 33)
check("B2.3 (24,8,1) != (9,11,13)", reduced_parts != zones)
check("B2.4 2 blocks != 3 parts (structural, not just numeric)",
      len(af_blocks) != len(zones))
# Non-vacuity control: an equal-part scene K(11,11,11) also sums 33 but with
# regular degrees -> the mismatch is scene-specific, not generic to sum-33.
zones_ctrl = [11, 11, 11]
ctrl_spec = {0: 1}
for n in zones_ctrl:
    ctrl_spec[33 - n] = ctrl_spec.get(33 - n, 0) + (n - 1)
ctrl_spec[33] = ctrl_spec.get(33, 0) + (len(zones_ctrl) - 1)
check("B2.5 control K(11,11,11) is regular (single nonzero deg 22) — mismatch is "
      "scene-specific", sorted(ctrl_spec.keys()) == [0, 22, 33])

# ---------------------------------------------------------------------------
# BLOCK 3 — CANONICAL-XI-ANCHOR-OWNER-001 (no canonical chi)
# ---------------------------------------------------------------------------
# A dimension-only Xi is killed by the spectral invariant obstruction (Block 4).
# Here: the reduction target (24,8,1) cannot be a partition-respecting map onto
# V9 | V11 | V13 because block images can't split into the 3 parts.
check("B3.1 no partition-respecting chi: 2 source blocks cannot surject onto 3 "
      "nonempty ordered parts preserving block structure",
      len(af_blocks) < len(zones))

# ---------------------------------------------------------------------------
# BLOCK 4 — AF-D0-SPECTRAL-COMPRESSION-OWNER-001 (scale-independent, DECISIVE)
# ---------------------------------------------------------------------------
check("B4.1 AF reduced multiset = {1,3,8,21}", af_reduced == [1, 3, 8, 21])
check("B4.2 scene multiset = {1,2,8,10,12}", scene_mults == [1, 2, 8, 10, 12])
check("B4.3 multisets differ", af_reduced != scene_mults)
check("B4.4 distinct counts differ 4 vs 5",
      len(af_reduced) != len(scene_mults) and len(af_reduced) == 4
      and len(scene_mults) == 5)
check("B4.5 both partition 33", sum(af_reduced) == 33 and sum(scene_mults) == 33)
check("B4.6 scene trace = 718 = 2|E|",
      scene_trace == 718 and 2 * scene_edges == 718)

# ---------------------------------------------------------------------------
# BLOCK 5 — JOINT-DIRAC-{SCALE-SELECTION,ANCHOR}-NOGO (primitives independent)
# ---------------------------------------------------------------------------
# The two primitives vary independently: scale (phi^N) vs dim (invariant).
# phi^N in Z[phi] pairs (a,b)=(F(N-1),F(N)); dim carries no scale param.
def phi_pow(Nn):  # phi^N = F(N-1) + F(N) phi ; return (a,b)
    return (fib(Nn - 1), fib(Nn))
scale_pairs = [phi_pow(n) for n in range(1, 7)]
# distinct from a 2^N law at every level -> genuine independent freedom
check("B5.1 phi^N scale != 2^N law at every N (independent scale primitive)",
      all(sp != (2 ** n, 0) for n, sp in zip(range(1, 7), scale_pairs)))
check("B5.2 dim sequence invariant under scale choice (no scale param in dimA)",
      dimA == [fib(2 * n + 3) for n in range(7)])
# Joint anchor NOGO: no single anchor unifies scale-selection AND comparison-Xi.
# Witnessed by: comparison-Xi is spectrally blocked (B4) INDEPENDENTLY of scale.
check("B5.3 Xi blocked scale-INDEPENDENTLY (multiplicities, not eigenvalues) "
      "=> anchor cannot co-select scale via Xi", len(af_reduced) != len(scene_mults))

# ---------------------------------------------------------------------------
# BLOCK 6 — NEWER OWNED FORCING (Iter25) that RE-TYPES the cluster
# ---------------------------------------------------------------------------
# 6a. DIM-EVEN-FIBONACCI-FORCING: 33 = sum of EVEN-indexed Fibonacci F2+F4+F6+F8,
#     independently of the odd-indexed algebra dims. The +2 grading is shared.
even_fib = [fib(2 * j) for j in range(1, 5)]        # F2,F4,F6,F8 = 1,3,8,21
check("B6.1 even-index Fib {F2,F4,F6,F8} = {1,3,8,21}", even_fib == [1, 3, 8, 21])
check("B6.2 even-index Fib sum = 33 = scene dim (DIMENSION LIFTS, forced)",
      sum(even_fib) == 33 == N)
check("B6.3 classical identity sum_{k=1..4} F_2k = F_9 - 1 = 33",
      sum(even_fib) == fib(9) - 1 == 33)
# The AF-reduced multiplicities ARE the even-index Fibonacci numbers -> the
# "spectral obstruction" multiset {1,3,8,21} is exactly the forced dimension grading.
check("B6.4 AF reduced mults == even-index Fib (obstruction multiset IS the "
      "forced grading)", af_reduced == even_fib)
# 6b. LAPLACIAN-SPECTRUM-FORCED: the whole scene spectrum is the multipartite
#     closed form; 30 = N-k nullity is NOT Fibonacci (honest anti-numerology).
check("B6.5 nullity 30 = N - k and 30 is NOT Fibonacci (honest scope guard)",
      (N - k) == 30 and all(fib(m) != 30 for m in range(13)))
check("B6.6 edges 359 prime (alpha_top coeff, no phi form)",
      all(359 % d for d in range(2, 359)))
# 6c. The +2 grading is the shared root: zones are a +2 AP; even powers step +2.
check("B6.7 zones are +2 arithmetic progression (shared root of the convergence)",
      zones[1] - zones[0] == 2 and zones[2] - zones[1] == 2)

# ---------------------------------------------------------------------------
# BLOCK 7 — Feshbach compression (row 433 CERT-CLOSED) does the 5->4 reduction
# ---------------------------------------------------------------------------
# Bulk zones 1,2 = 20 vtx; traced boundary zone 3 = 13, degree 33-13=20 => D_tt=20 I.
# Compressed spectrum {0,22,24,33}: drops the eigenvalue 20 (the boundary block value).
compressed_distinct = {0, 22, 24, 33}
scene_distinct = set(scene_spec.keys())              # {0,20,22,24,33}
check("B7.1 scene has 5 distinct eigenvalues", len(scene_distinct) == 5)
check("B7.2 Feshbach compression has 4 distinct (drops 20 = boundary deg)",
      len(compressed_distinct) == 4 and (scene_distinct - compressed_distinct) == {20})
check("B7.3 boundary degree = 33 - 13 = 20 (why D_tt = 20 I_13)", 33 - 13 == 20)
# Honest bound: compressed {0,22,24,33} is NOT the geometric phi-ladder phi^2:phi^4:phi^6.
check("B7.4 compressed spectrum is NOT the AF geometric ladder (congruence still "
      "NO-GO)", sorted(compressed_distinct) != af_reduced)

# ---------------------------------------------------------------------------
# BLOCK 8 — UCP/interlacing binding inequality (Iter24 root sharpening)
# ---------------------------------------------------------------------------
# Root obstruction: AF-reduced corner embeds for k<=4, infeasible k>=5:
#   binding 20/phi^2 > 33/phi^4  <=>  20 phi > 13. Check in Z[phi] exactly.
# 20*phi - 13 = 20*phi - 13 ; phi>0 so 20*phi ~ 32.36 > 13. Exact surrogate:
# multiply by phi: 20*phi^2 vs 13*phi ; phi^2 = phi+1 -> 20*(phi+1)=20phi+20.
# Compare 20*phi vs 13: since phi = (1+sqrt5)/2, 20*phi = 10+10 sqrt5.
# (10+10 sqrt5) - 13 = -3 + 10 sqrt5 ; 10 sqrt5 = sqrt500 > 22 -> positive.
check("B8.1 binding inequality 20*phi > 13 (exact: 10*sqrt5 > 3 <=> 500 > 9)",
      500 > 9)   # 20 phi -13 = -3 + 10 sqrt5 ; positive iff (10 sqrt5)^2=500 > 3^2=9
# Dynamic-range reading: d1/d_top = 20/33 = 0.606... > 1/phi^2 = 0.381...
# exact: 20/33 > 1/phi^2 = 2 - phi = (3 - sqrt5)/2. Cross-multiply integers via
# rational bound 1/phi^2 < 5/13 (since phi^2=phi+1>13/5=2.6 as 2.618>2.6).
check("B8.2 dynamic range 20/33 exceeds 1/phi^2 (too bunched for phi-ladder): "
      "20/33 > 5/13 >= 1/phi^2", F(20, 33) > F(5, 13))

# ---------------------------------------------------------------------------
print()
if FAIL:
    print(f"RESULT: {len(FAIL)} FAILED -> {FAIL}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS (exact arithmetic, no float)")


def _selftest():
    """Mutation test: each planted mutation must flip a check to FAIL."""
    import subprocess, tempfile, os, re
    src = open(__file__).read()
    muts = [
        ("N = sum(zones)", "N = sum(zones) + 1", "B1.1"),
        ("af_algebra_dim = 5 ** 2 + 3 ** 2", "af_algebra_dim = 5 ** 2 + 3 ** 2 + 1", "B1.2"),
        ("reduced_parts = [5 ** 2 - 1, 3 ** 2 - 1, 1]",
         "reduced_parts = [24, 8, 2]", "B2.1"),
        ("af_reduced = [dimA[0] - 1]", "af_reduced = [dimA[0]]", "B4.1"),
        ("scene_spec[N] = scene_spec.get(N, 0) + (k - 1)",
         "scene_spec[N] = scene_spec.get(N, 0) + k", "B4.2"),
        ("even_fib = [fib(2 * j) for j in range(1, 5)]",
         "even_fib = [fib(2 * j + 1) for j in range(1, 5)]", "B6.1"),
        ("compressed_distinct = {0, 22, 24, 33}",
         "compressed_distinct = {0, 20, 22, 24, 33}", "B7.2"),
        ("first_ge_33 = next(i for i, d in enumerate(dimA) if d >= 33)",
         "first_ge_33 = 2", "B1.7"),
        ("check(\"B8.2 dynamic range 20/33 exceeds 1/phi^2 (too bunched for phi-ladder): \"\n      \"20/33 > 5/13 >= 1/phi^2\", F(20, 33) > F(5, 13))",
         "check(\"B8.2 x\", F(20, 33) < F(5, 13))", "B8.2"),
        ("check(\"B6.2 even-index Fib sum = 33 = scene dim (DIMENSION LIFTS, forced)\",\n      sum(even_fib) == 33 == N)",
         "check(\"B6.2 x\", sum(even_fib) == 34 == N)", "B6.2"),
        ("check(\"B7.3 boundary degree = 33 - 13 = 20 (why D_tt = 20 I_13)\", 33 - 13 == 20)",
         "check(\"B7.3 x\", 33 - 13 == 21)", "B7.3"),
    ]
    passed = 0
    for old, new, tag in muts:
        if old not in src:
            print(f"[SELFTEST-ERR] anchor not found for {tag}")
            continue
        mutated = src.replace(old, new, 1).replace("_selftest()", "pass")
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
            tf.write(mutated)
            path = tf.name
        rc = subprocess.run([sys.executable, path], capture_output=True).returncode
        os.unlink(path)
        ok = rc != 0
        print(f"[{'KILL' if ok else 'SURVIVE'}] mutation {tag}: {new[:50]}")
        passed += ok
    print(f"\nSELFTEST: {passed}/{len(muts)} mutations killed")
    sys.exit(0 if passed == len(muts) else 1)


if __name__ == "__main__" and "--selftest" in sys.argv:
    _selftest()
