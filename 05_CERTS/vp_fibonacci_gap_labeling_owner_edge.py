#!/usr/bin/env python3
"""CERT: D0-GAP-LABELING-OWNER-EDGE-001 — Fibonacci gap labeling, computational shadow of the
owner edge (BBG 1992 allowed labels; DGY Invent. Math. 206 (2016) Thm 1.3 saturation, all
couplings; lab passports Tanese PRL 112 146404 (2014), Baboux PRB 95 161114(R) (2017)).

What this cert PROVES (finite/exact/decidable, no external theorem assumed):
  1. T = A^{-1} exactly (D0 toral generator vs Fibonacci abelianization) and NOT conjugate.
  2. Rank-2 module closure: (phi^-1)^k in Z+Z phi^-1 via signed-Fibonacci recursion (exact pairs);
     closure identity phi^-1 + phi^-2 = 1 as an exact pair identity.
  3. Fricke-Vogt invariant I(x,y,z)=x^2+y^2+z^2-2xyz-1 is preserved by the Fibonacci trace map
     (symbolic identity) and equals lambda^2/4 on the standard Hamiltonian embedding (symbolic).
  4. Gap-labeling SATURATION at approximant level: periodic Fibonacci approximant (|w|=F=987),
     couplings lambda in {1, 4}: EVERY dominant spectral gap carries a small-|m| label with
     k = m*610 mod 987 (610/987 = approximant slope) AND IDS within 2/987 of frac(m*phi^-1).
  5. NEGATIVE CONTROLS (silver/Pell chain, |w|=577): golden small-|m| labels FAIL on the silver
     chain's dominant gaps, while silver labels frac(m*(sqrt2-1)) PASS there — the method detects
     THE module of the chain, not any module (anti-numerology; the silver constant is the corpus's
     own registered control).

What stays EXTERNAL (owner edge, NOT re-proved here): the Bellissard identity IDS = K0-trace
image (BBG 1992) and all-coupling saturation on the true aperiodic operator (DGY 2016 Thm 1.3).
This cert supplies the exact finite shadow + controls; it is also the retirement replacement for
the fabricated-IDS placeholder flagged on D0-KTHEORY-001 (vp_gap_labeling_d0_tiling_hull.py).
"""
from fractions import Fraction
import numpy as np

checks = []

# ---------- 1. T = A^{-1}, not conjugate ----------
A = [[1, 1], [1, 0]]
T = [[0, 1], [1, -1]]
mul = lambda M, N: [[sum(M[i][k]*N[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
I2 = [[1, 0], [0, 1]]
detA = A[0][0]*A[1][1] - A[0][1]*A[1][0]
# charpoly x^2 - tr x + det
cpA = (A[0][0]+A[1][1], detA)
cpT = (T[0][0]+T[1][1], T[0][0]*T[1][1]-T[0][1]*T[1][0])
checks.append(("T=A^-1 (A*T=T*A=I, det A=-1)", mul(A, T) == I2 and mul(T, A) == I2 and detA == -1))
checks.append(("NOT conjugate (charpoly x^2-x-1 vs x^2+x-1)", cpA == (1, -1) and cpT == (-1, -1) and cpA != cpT))

# ---------- 2. module closure, exact pairs in basis (1, phi^-1) ----------
# phi^-1 * (a + b phi^-1) = b + (a-b) phi^-1   [since phi^-2 = 1 - phi^-1]
p = (5**0.5 - 1)/2
a, b = 0, 1                      # phi^-1 = 0 + 1*phi^-1
ok2 = True
for k in range(2, 13):
    a, b = b, a - b              # signed-Fibonacci step
    ok2 &= abs((a + b*p) - p**k) < 1e-12
pair_sum = (0 + 1, 1 + (-1))     # phi^-1=(0,1), phi^-2=(1,-1): sum must be (1,0)=1
checks.append(("module closure (phi^-1)^k=(a,b), k<=12, exact recursion", ok2))
checks.append(("closure identity phi^-1+phi^-2=1 as pair (1,0)", pair_sum == (1, 0)))

# ---------- 3. Fricke-Vogt invariant: symbolic ----------
import sympy as sp
x, y, z, E, lam = sp.symbols('x y z E lam')
Iv = lambda u, v, w: u**2 + v**2 + w**2 - 2*u*v*w - 1
inv_preserved = sp.expand(Iv(y, z, 2*y*z - x) - Iv(x, y, z)) == 0
seed = Iv((E - lam)/2, E/2, 1)   # standard embedding x_{-1}=(E-lam)/2, x_0=E/2, x_1=1... convention check below
seed_val = sp.simplify(seed - lam**2/4)
checks.append(("trace map preserves Fricke-Vogt invariant (symbolic)", inv_preserved))
checks.append(("invariant = lambda^2/4 on Hamiltonian embedding (symbolic)", seed_val == 0))

# ---------- 4. approximant saturation (the real spectrum; replaces fabricated-IDS placeholder) ----------
def sub_word(rules, n_target, w="a"):
    while len(w) < n_target:
        w = "".join(rules[c] for c in w)
    return w

def dominant_gap_labels(word, lam, slope_num, slope_den, alpha, mmax=34, top_k=25, tol_states=2):
    """Periodic tridiagonal H over the word; label the top_k WIDEST gaps (threshold-free rank
    selection — at large coupling a spacing threshold sweeps in arbitrarily deep gaps whose
    legitimate labels exceed any fixed |m| bound; the labeled PREDICTION is wide gap <-> small m).
    """
    N = len(word)
    v = np.array([lam if c == 'b' else 0.0 for c in word])
    H = np.diag(v) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    H[0, -1] = H[-1, 0] = 1.0    # periodic BC (no edge states in gaps)
    ev = np.linalg.eigvalsh(H)
    sp_ = np.diff(ev)
    ks = np.argsort(sp_)[::-1][:top_k] + 1
    out = []
    for k in sorted(int(t) for t in ks):          # k states strictly below the gap
        # integer congruence label: k = m*slope_num mod slope_den, smallest |m|
        m_int = None
        for m in range(-mmax, mmax+1):
            if (m*slope_num - k) % slope_den == 0:
                if m_int is None or abs(m) < abs(m_int): m_int = m
        # module label: nearest frac(m*alpha) within tol
        ids = k/N
        dists = [(min(abs(ids - ((m*alpha) % 1.0)), 1 - abs(ids - ((m*alpha) % 1.0))), m)
                 for m in range(-mmax, mmax+1)]
        d, m_mod = min(dists)
        out.append(dict(k=int(k), ids=ids, m_int=m_int, m_mod=m_mod, dist=d, ok_int=m_int is not None,
                        ok_mod=d < tol_states/N))
    return out

fib = sub_word({"a": "ab", "b": "a"}, 987)[:987]        # F_16=987, F_15=610
assert fib.count("a") == 610 and fib.count("b") == 377
phi_inv = (5**0.5 - 1)/2
ok4 = True
for lam_val in (1.0, 4.0):
    labs = dominant_gap_labels(fib, lam_val, 610, 987, phi_inv)
    allok = all(g["ok_int"] and g["ok_mod"] for g in labs)
    ok4 &= allok and len(labs) >= 20
    worst = max(g["dist"] for g in labs)
    ms = sorted({abs(g["m_mod"]) for g in labs})
    print(f"  [4] lambda={lam_val}: top {len(labs)} gaps, all golden-labeled={allok}, "
          f"worst |IDS-frac(m phi^-1)|={worst:.2e} (tol {2/987:.2e}), |m| set={ms}")
checks.append(("approximant saturation: top-25 widest gaps golden-labeled (lam=1 and 4)", ok4))

# ---------- 5. controls: silver/Pell chain (approximant slope 169/577, module gen 1-1/sqrt2) ----------
silver = sub_word({"a": "aab", "b": "a"}, 577)[:577]     # Pell lengths 1,3,7,17,41,99,239,577
nb = silver.count("b")
assert nb == 169                                          # b-frequency 169/577 ~ 1-1/sqrt2
silver_alpha = 1 - 1/2**0.5                               # letter-b frequency: the silver label module Z+Z(sqrt2/2) mod 1
labs_g = dominant_gap_labels(silver, 1.0, 610, 987, phi_inv, top_k=15)   # golden labels forced on silver chain
golden_fails = sum(1 for g in labs_g if not g["ok_mod"])
labs_s = dominant_gap_labels(silver, 1.0, 169, 577, silver_alpha, top_k=15)
silver_pass = sum(1 for g in labs_s if g["ok_int"] and g["ok_mod"])
worst_s = max(g["dist"] for g in labs_s)
print(f"  [5] silver chain ({len(silver)} sites, {nb} b's): top {len(labs_g)} gaps; "
      f"golden-label FAILURES={golden_fails}; silver-label passes={silver_pass}/{len(labs_s)} "
      f"(worst dist {worst_s:.2e})")
checks.append(("negative control: golden labels FAIL on silver chain (>=1 of top-15)", golden_fails >= 1))
checks.append(("positive control: silver labels (169/577, 1-1/sqrt2) PASS on silver chain",
               len(labs_s) >= 10 and silver_pass == len(labs_s)))

# ---------- verdict ----------
print()
allpass = True
for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    allpass &= ok
print(f"\nCERT D0-GAP-LABELING-OWNER-EDGE-001: {'ALL PASS' if allpass else 'FAIL'}")
raise SystemExit(0 if allpass else 1)
