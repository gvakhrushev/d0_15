#!/usr/bin/env python3
"""D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 companion: LOCALIZE the residual B-L freedom.

Strengthens the existing NO-GO (D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001 / §04.11 Front F7),
which proves the anomaly-free set contains the 2-dim span{Y, B-L} and that removing B-L requires
imposing Y_{nu^c}=0 (an input, "question-begging"). This certificate PINS EXACTLY WHERE that
irreducible freedom lives, and proves a charged-fermion-only selector cannot remove it.

RESULT (exact over Q): parametrize the anomaly-free plane as gen = a*Y + b*(B-L). Imposing the
LEFT-HANDED DOUBLET electric charges via the Gell-Mann-Nishijima completion Q = T3 + gen
(T3 = +/-1/2):
    up-quark    Q_u = +1/2 + gen[qL] = 2/3
    down-quark  Q_d = -1/2 + gen[qL] = -1/3
    electron    Q_e = -1/2 + gen[lL] = -1
forces  gen[qL] = 1/6  and  gen[lL] = -1/2  -- i.e. the line a = 1 - 2b -- but DOES NOT fix b.
Along this line the doublet entries gen[qL], gen[lL] are b-INDEPENDENT, while ALL of gen[uc],
gen[dc], gen[ec], gen[nuc] carry b linearly. Hence:

  (i)  the whole B-L residual freedom is carried by the RIGHT-HANDED SINGLET sector;
  (ii) the left-handed doublet electric charges are B-L-BLIND;
  (iii) therefore NO selector using only charged-fermion (doublet) electric charges can remove
        B-L: any selector must assign a right-handed singlet charge. "nu^c uncharged" (b=0) is the
        minimal such input -- confirming and LOCALIZING the corpus's question-begging verdict.

This does NOT overturn the NO-GO; it sharpens it: the obstruction is not fixable by electric-charge
observation on charged fermions, only by a right-handed-singlet input (or a new scene primitive).

Falsifiable: recomputes the anomaly conditions and the b-dependence exactly; breaks (nonzero exit) if
any doublet entry turns out b-dependent, or any singlet entry b-independent, or the anomaly checks fail.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FAIL = 0
def check(tag, cond, detail=""):
    global FAIL
    if not cond:
        FAIL += 1
    print(f"{'PASS' if cond else 'FAIL'}_{tag}  {detail}")
    return cond

# field order (q_L, u^c, d^c, l_L, e^c, nu^c); SM multiplicities
FIELDS = ["qL", "uc", "dc", "lL", "ec", "nuc"]
mult = {"qL": 6, "uc": 3, "dc": 3, "lL": 2, "ec": 1, "nuc": 1}
Y  = {"qL": F(1, 6), "uc": F(-2, 3), "dc": F(1, 3), "lL": F(-1, 2), "ec": F(1), "nuc": F(0)}
BL = {"qL": F(1, 3), "uc": F(-1, 3), "dc": F(-1, 3), "lL": F(-1), "ec": F(1), "nuc": F(1)}

def grav(X):  return sum(mult[f] * X[f] for f in FIELDS)
def su2(X):   return 3 * X["qL"] + X["lL"]
def su3(X):   return 2 * X["qL"] + X["uc"] + X["dc"]
def cubic(X): return sum(mult[f] * X[f] ** 3 for f in FIELDS)
def anomaly_free(X): return grav(X) == 0 and su2(X) == 0 and su3(X) == 0 and cubic(X) == 0

# --- both generators anomaly-free and independent (the 2-dim NO-GO premise) ---
check("Y_ANOMALY_FREE", anomaly_free(Y), "grav,su2,su3,cubic all 0 for Y")
check("BL_ANOMALY_FREE", anomaly_free(BL), "grav,su2,su3,cubic all 0 for B-L")
minor = Y["qL"] * BL["uc"] - Y["uc"] * BL["qL"]
check("INDEPENDENT", minor != 0, f"2x2 minor(Y,B-L)={minor} != 0")

# --- represent gen = a*Y + b*(B-L) as an affine function of (a,b): store (const_in_a, coeff_b) ---
# We work symbolically-by-hand: gen[f](a,b) = a*Y[f] + b*BL[f]. Impose the doublet-charge line a=1-2b
# by substituting a -> 1 - 2b, giving gen[f] = (1-2b)*Y[f] + b*BL[f] = Y[f] + b*(BL[f] - 2*Y[f]).
# Thus the b-coefficient of gen[f] along the line is  c[f] = BL[f] - 2*Y[f], and the b=0 value is Y[f].
c = {f: BL[f] - 2 * Y[f] for f in FIELDS}       # b-coefficient along the doublet-charge line
base = {f: Y[f] for f in FIELDS}                 # value at b=0 (pure hypercharge)

# --- doublet charges pin a=1-2b: check gen[qL],gen[lL] are b-INDEPENDENT (c=0) and equal to SM ---
check("QL_B_BLIND", c["qL"] == 0, f"b-coeff of gen[qL] along line = {c['qL']} (want 0: doublet pinned)")
check("LL_B_BLIND", c["lL"] == 0, f"b-coeff of gen[lL] along line = {c['lL']} (want 0: doublet pinned)")
check("QL_VALUE", base["qL"] == F(1, 6), f"gen[qL]={base['qL']} => Q_u=1/2+1/6=2/3, Q_d=-1/2+1/6=-1/3")
check("LL_VALUE", base["lL"] == F(-1, 2), f"gen[lL]={base['lL']} => Q_e=-1/2-1/2=-1")

# --- ALL singlets carry b (c != 0): the freedom is entirely in the right-handed singlet sector ---
for f in ["uc", "dc", "ec", "nuc"]:
    check(f"{f.upper()}_CARRIES_B", c[f] != 0, f"b-coeff of gen[{f}] along line = {c[f]} (nonzero: carries B-L)")

# --- any single singlet-charge input kills b (=> b=0 => pure Y) ---
# requiring gen[f] = Y[f] (its SM value) means base[f] + b*c[f] = Y[f] => b*c[f]=0 => b=0 (since c[f]!=0)
kills = all(c[f] != 0 for f in ["uc", "dc", "ec", "nuc"])
check("SINGLET_INPUT_KILLS_B", kills,
      "each of uc,dc,ec,nuc has nonzero b-coeff, so fixing ANY ONE to its SM value forces b=0")

# --- the sharpened NO-GO statement ---
check("DOUBLET_ONLY_UNDERDETERMINED", (c["qL"] == 0 and c["lL"] == 0) and any(c[f] != 0 for f in ["uc","dc","ec","nuc"]),
      "charged-fermion (doublet) electric charges are B-L-blind => no doublet-only selector removes B-L")

print()
if FAIL == 0:
    print("PASS_HYPERCHARGE_BL_FREEDOM_LOCALIZED — the B-L residual of the anomaly-free plane lives "
          "ENTIRELY in the right-handed singlet sector; left-handed doublet electric charges are "
          "B-L-blind. Confirms + localizes D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001: any Y-selector "
          "needs a right-handed-singlet input (nu^c uncharged is minimal), not fixable by charged-"
          "fermion charge observation alone.")
    sys.exit(0)
else:
    print(f"FAIL — {FAIL} checks failed.")
    sys.exit(1)
