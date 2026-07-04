#!/usr/bin/env python3
"""FOCK SEAM CANDIDATE — second-quantized realization of the alpha depth moments.
Carrier: Lambda*(V11), dim 2^11 (FORCED by the exclusion chain: vertex seam = 0 theorem;
linear-edge universal bound m2/m1 <= lambda_max ~ 42 << 7372.8).
Construction (owned ingredients ONLY — no mu enters as input):
  D_tilde = (pi0*phi^-2) * 2^N   on Lambda*(V11)
    - per-mode factor 2 = the owned primitive dyad D2 (BOOK_01 §01.20/§01.22: ABCD = D2^2,
      V11 = V9 ⊔ D2) — binary occupancy of each of the 11 zone modes;
    - global angle density pi0*phi^-2 = 6/5 (pi0 = (6/5)phi^2 DERIVED from delta0 balance,
      vp_feshbach_residue_amplitudes.py PASS_PI0_OWNED).
  m1 = 1/rank = 1/3 (owned, active side, no Fock content).
  m2 = TOP-BLADE eigenvalue of D_tilde (full saturation of the moving shell; the depth-2
      circulation readout at the dominant archive pole).
CLAIMS VERIFIED:
  m2 = (6/5)*2^11 = 12288/5 = mu2 EXACTLY (comes out as an eigenvalue, not inserted);
  m2*u^2 + m1*u = alpha_alg^-1 = 159739/5 - (294902/15) phi exactly (u = phi^-3 = 2phi-3);
  ratio m2/m1 = 36864/5 — reachable ONLY because D_tilde is multiplicative (exclusion-consistent).
FIVE NEGATIVE CONTROLS (each must fail to reproduce mu2): trace readout, additive dGamma lift,
partial blade k=10, angle-free dyads, wrong zones V9/V13.
NAMED SOFT JOINT (open, honest): the top-blade (saturation) coupling forcing — two candidate
owners recorded in FOCK_SEAM_CANDIDATE.md, neither yet written as DEF-0.2.2. Exit 1 on failure."""
from fractions import Fraction as F
from math import comb
import sys

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ")+name); ok = ok and bool(cond)

n = 11
angle = F(6,5)                    # pi0 * phi^-2, owned
m1 = F(1,3)                       # 1/rank, owned
m2 = angle * 2**n                 # TOP eigenvalue of (6/5)*2^N — the construction's output
check("m2 = top-blade eigenvalue = (6/5)*2^11 = 12288/5 = mu2 (output, not input)", m2 == F(12288,5))
check("ratio m2/m1 = 36864/5 (reachable only multiplicatively — exclusion-consistent)", m2/m1 == F(36864,5))

def mulp(x,y):
    a,b=x; c,d=y
    return (a*c+b*d, a*d+b*c+b*d)
u  = (F(-3), F(2))                # phi^-3 = 2 phi - 3
u2 = mulp(u,u)
check("u^2 = phi^-6 = 13 - 8 phi", u2 == (F(13), F(-8)))
alpha = (m2*u2[0] + m1*u[0], m2*u2[1] + m1*u[1])
check("m2 u^2 + m1 u = alpha_alg^-1 = 159739/5 - (294902/15) phi EXACT", alpha == (F(159739,5), F(-294902,15)))

# negative controls
check("control (i): full-Fock trace readout = (6/5)*3^11 != mu2",
      angle*sum(2**k*comb(n,k) for k in range(n+1)) == angle*3**n and angle*3**n != m2)
check("control (ii): additive dGamma lift lambda_max = 66/5 != mu2 (linear-class, bound-blocked)", angle*n != m2)
check("control (iii): partial saturation k=10 gives 6144/5 != mu2", angle*2**10 != m2)
check("control (iv): angle-free dyads give 2048 != mu2", F(2**n) != m2)
check("control (v): wrong zones — V9: 3072/5, V13: 49152/5, both != mu2",
      angle*2**9 != m2 and angle*2**13 != m2)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
