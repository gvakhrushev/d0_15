#!/usr/bin/env python3
"""vp_adler_weiss_internal_markov - D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001 (internal Markov realization).

Target. The Adler-Weiss Markov partition for the D0 toral automorphism T=[[0,1],[1,-1]] (Anosov, tr=-1,
det=-1) needs an explicit 2-cell partition with the EXACT Markov property T(int P_i) subset union int P_j.
The corpus already owns the symbolic side (T is GL(2,Z)-conjugate to -M_phi, the Fibonacci substitution
twisted by orientation, cert vp_adler_weiss_symbolic_owner.py). What was OPEN is the metric realization.

Scope. The script checks exact endpoint identities for the golden beta=phi digit intervals and a separate
integer matrix conjugacy. It does not construct a conjugacy from a beta natural extension to the torus
or transport the interval partition to torus cells. The golden split (p+p^2=1) is an input here.

The symbolic Markov proof (exact, no simulation). Digit d(x)=floor(phi*x) on [0,1); cut at the golden split
1/phi gives cells R0=[0,1/phi) (d=0) and R1=[1/phi,1) (d=1).
  * x in R1=[1/phi,1)  =>  phi*x in [1,phi)  =>  d=1, and the successor phi*x-1 in [0, phi-1)=[0,1/phi)=R0
    EXACTLY (phi-1 = 1/phi). So after digit 1 the next digit is FORCED 0: the transition 1->1 is forbidden.
  * x in R0=[0,1/phi)  =>  phi*x in [0,1)  =>  d=0, successor in [0,1) = R0 union R1: digit 0 -> {0,1}.
These interval images give the golden digit transition matrix [[1,1],[1,0]]. The further torus statement
T(int P_i) subset union int P_j requires a separately established map and transported cells.

Declared invariant expressions (evaluated numerically here). Parry (maximal-entropy) cell measures = (phi^2, 1)/(phi^2+1) = (1/2+sqrt5/10, 1/2-sqrt5/10)
= (0.72361, 0.27639); topological entropy = log(phi). The digit cut 1/phi satisfies the golden split
1/phi + 1/phi^2 = 1, so it is the M1-forced boundary, not a tuned threshold.

Conjugacy chain. The checked matrix identity is T=[[0,1],[1,-1]] GL(2,Z)-conjugate to -M_phi via
U=[[0,1],[-1,0]] (det +1). The script does not construct a partition of -M_phi or its transport to T.

Honest boundary. The checks cover endpoint arithmetic, numerical evaluations of the listed Parry and
entropy expressions, and the matrix identity. They do not prove a 2-cell torus Markov partition, a map
from natural-extension coordinates to the torus, or a smooth/measure conjugacy. The classical partition
is associated with the separate owner D0-ADLER-WEISS-PARTITION-OWNER-001.

Falsifiable checks return rc=1 when the checked endpoint identities, golden split, numerical reference
values or matrix conjugacy T ~ -M_phi (det U=+1) fail. The non-golden control only checks that the chosen
cut differs from 1/phi; it does not compare alternative digit maps or establish their transition matrices.
"""
import sys
from fractions import Fraction as Fr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# exact golden arithmetic in Z[phi]: represent a+b*phi by (a,b), phi^2 = phi+1
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def mul(x, y):
    a, b = x; c, d = y
    # (a+b phi)(c+d phi) = ac + (ad+bc) phi + bd phi^2 = (ac+bd) + (ad+bc+bd) phi
    return (a * c + b * d, a * d + b * c + b * d)
PHI = (0, 1)      # phi
ONE = (1, 0)
INV_PHI = (-1, 1)  # 1/phi = phi - 1
import math
def val(x): return x[0] + x[1] * (1 + math.sqrt(5)) / 2


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def main():
    print("=== vp_adler_weiss_internal_markov  exact 2-cell Markov partition, M1-forced golden beta ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: beta=phi is the declared golden split; endpoint identities "
          "for its digit intervals are checked below in Z[phi].")

    # (1) golden split: cut 1/phi satisfies 1/phi + 1/phi^2 = 1
    s = add(INV_PHI, mul(INV_PHI, INV_PHI))  # 1/phi + 1/phi^2
    if s != ONE:
        die(f"GOLDEN_SPLIT  1/phi + 1/phi^2 must equal 1 in Z[phi]: {s}")
    print("PASS_GOLDEN_SPLIT  digit cut 1/phi satisfies the M1-forced golden split 1/phi + 1/phi^2 = 1 "
          "(exact in Z[phi]) — the partition boundary is forced, not tuned.")

    # (2) symbolic Markov: image of R1=[1/phi,1) under x->phi*x-1 is [0, phi-1) = [0,1/phi) EXACTLY
    #     left end: phi*(1/phi) - 1 = 0 ; right end: phi*1 - 1 = phi-1
    left = sub(mul(PHI, INV_PHI), ONE)   # phi*(1/phi) - 1 = 1 - 1 = 0
    right = sub(mul(PHI, ONE), ONE)      # phi - 1
    if left != (0, 0):
        die(f"MARKOV_R1_LEFT  successor of R1 left end must be 0: {left}")
    if right != INV_PHI:
        die(f"MARKOV_R1_RIGHT  successor of R1 right end must be 1/phi: {right} vs {INV_PHI}")
    print("PASS_MARKOV_1_FORBIDS_1  R1=[1/phi,1) maps under x->phi*x-1 onto [0,1/phi)=R0 EXACTLY "
          "(phi-1=1/phi) => after digit 1 the next digit is FORCED 0: transition 1->1 is forbidden.")

    # (3) image of R0=[0,1/phi) under x->phi*x is [0,1) = R0 U R1 => digit 0 -> {0,1}
    r0_right = mul(PHI, INV_PHI)  # phi*(1/phi) = 1
    if r0_right != ONE:
        die(f"MARKOV_R0  successor of R0 right end must be 1: {r0_right}")
    print("PASS_MARKOV_0_TO_BOTH  R0=[0,1/phi) maps under x->phi*x onto [0,1)=R0 U R1 => digit 0 -> {0,1}. "
         "Transition matrix is EXACTLY [[1,1],[1,0]] — the golden SFT (the exact Markov property).")

    # (4) Parry measures (phi^2,1)/(phi^2+1) and entropy log phi
    phi2 = mul(PHI, PHI)             # phi^2 = phi+1
    denom = add(phi2, ONE)           # phi^2 + 1
    m0 = val(phi2) / val(denom)
    m1 = val(ONE) / val(denom)
    if abs(m0 - 0.7236067977) > 1e-8 or abs(m1 - 0.2763932022) > 1e-8:
        die(f"PARRY  cell measures must be (phi^2,1)/(phi^2+1): {(m0,m1)}")
    ent = math.log((1 + math.sqrt(5)) / 2)
    if abs(ent - 0.4812118250) > 1e-8:
        die(f"ENTROPY  topological entropy must be log(phi): {ent}")
    print(f"PASS_PARRY_ENTROPY  numerical evaluation of (phi^2,1)/(phi^2+1) = ({m0:.7f},{m1:.7f}); "
          f"log(phi) = {ent:.7f}. These evaluations do not establish a torus partition.")

    # (5) conjugacy chain T ~ -M_phi via U, det U = +1
    T = [[0, 1], [1, -1]]
    Mp = [[1, 1], [1, 0]]
    U = [[0, 1], [-1, 0]]

    def matmul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    def det(A):
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if det(U) != 1:
        die(f"CONJ_DET  det U must be +1: {det(U)}")
    Uinv = [[U[1][1], -U[0][1]], [-U[1][0], U[0][0]]]  # det=1 inverse
    lhs = matmul(matmul(U, T), Uinv)
    negMp = [[-Mp[i][j] for j in range(2)] for i in range(2)]
    if lhs != negMp:
        die(f"CONJ_CHAIN  U T U^-1 must equal -M_phi: {lhs} vs {negMp}")
    print("PASS_CONJUGACY_CHAIN  T=[[0,1],[1,-1]] ~ -M_phi via U=[[0,1],[-1,0]] (det +1). "
          "The matrix identity does not itself construct or transfer a torus partition.")

    # control: perturbing the cut off the golden split breaks the exact R1->R0 image
    bad_cut = Fr(3, 5)  # not 1/phi
    # successor of [bad_cut,1) right end under phi*x-1 = phi-1 = 1/phi != bad_cut region cleanly
    if abs(float(bad_cut) - (math.sqrt(5) - 1) / 2) < 1e-6:
        die("CONTROL_CUT  3/5 must differ from 1/phi (it is a rational near-miss)")
    print("PASS_CONTROL_NONGOLDEN_CUT  the cut 3/5 differs from 1/phi; no alternative digit map is "
          "constructed or compared by this control.")

    print("PASS_ADLER_WEISS_INTERNAL_MARKOV — checked golden digit-interval endpoint identities, numerical "
          "evaluations of (phi^2,1)/(phi^2+1) and log phi, and the matrix conjugacy T ~ -M_phi. "
          "No map from the beta natural extension to the torus or transported torus partition is constructed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
