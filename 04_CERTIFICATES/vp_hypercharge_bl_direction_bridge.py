#!/usr/bin/env python3
"""vp_hypercharge_bl_direction_bridge.py - D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 certificate.
Closes the hypercharge-direction obligation as a minimal bridge (NOT a THE): the bridge Xi_Y =
'nu^c uncharged' (= nu_R in ker A, the R2 graph->physics localization, a MECH-LIMIT) is proven
NECESSARY + SUFFICIENT + MINIMAL to collapse the 2-dim anomaly-free family span{Y,B-L} to span{Y}.
Mirrors D0.Matter.HyperchargeBLDirectionBridge. Exact Fraction arithmetic.
"""
from fractions import Fraction as F
import sys
sys.stdout.reconfigure(encoding="utf-8")
ok = True
def check(name, cond):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    ok = ok and bool(cond)

# field order (q_L, u^c, d^c, l_L, e^c, nu^c)
Y   = [F(1,6), F(-2,3), F(1,3), F(-1,2), F(1), F(0)]
BmL = [F(1,3), F(-1,3), F(-1,3), F(-1), F(1), F(1)]
mult = [6, 3, 3, 2, 1, 1]
def combo(a, b): return [a*Y[i] + b*BmL[i] for i in range(6)]

def grav(X):  return sum(mult[i]*X[i] for i in range(6))
def su2(X):   return 3*X[0] + X[3]
def su3(X):   return 2*X[0] + X[1] + X[2]
def cubic(X): return sum(mult[i]*X[i]**3 for i in range(6))
def anomaly_free(X): return grav(X)==0 and su2(X)==0 and su3(X)==0 and cubic(X)==0

# --- both generators anomaly-free ---
check("Y anomaly-free (grav,su2,su3,cubic all 0)", anomaly_free(Y))
check("B-L anomaly-free (with charged nu^c)", anomaly_free(BmL))

# --- bridge functional reads b ---
check("combo(a,b)[nu^c] = b for sampled a,b", all(combo(a,b)[5]==b for a in range(-2,3) for b in range(-2,3)))

# --- necessity: 2 independent anomaly-free directions; B-L charges nu^c ---
minor = Y[0]*BmL[1] - Y[1]*BmL[0]
check("necessity: Y,B-L independent (2x2 minor != 0)", minor != 0)
check("necessity: B-L charges nu^c (combo(0,1)[nu^c]=1)", combo(0,1)[5]==1)

# --- sufficiency: nu^c uncharged => b=0 => span{Y} ---
check("sufficiency: combo(a,b)[nu^c]=0 <=> b=0 <=> pure Y",
      all((combo(a,b)[5]==0)==(b==0) for a in range(-3,4) for b in range(-3,4)))

# --- minimality: nu^c is the UNIQUE coordinate reading b alone ---
clean = [i for i in range(6) if Y[i]==0 and BmL[i]!=0]
check("minimality: unique bridge coordinate (Y=0, B-L!=0) is nu^c", clean == [5])

# --- negative control: anomaly cancellation ALONE must NOT fix the direction (B-L also anomaly-free) ---
def _neg_control():
    # if B-L were anomalous, anomalies alone would pick Y; it is NOT -> control must hold (assert not)
    return not anomaly_free(BmL)
assert not _neg_control(), "negative control breached: B-L must be anomaly-free, so anomalies alone do NOT fix Y"
# guillotine
assert ok, "RESULT: SOME FAIL - a claimed identity did not hold"
print("\n[STATUS] BRIDGE-ASSUMPTIONS-EXPLICIT: Xi_Y (nu^c uncharged = nu_R in ker A) necessary+sufficient+minimal;")
print("         collapses span{Y,B-L} -> span{Y}. NOT a present-core THE (rests on the R2 MECH-LIMIT localization).")
print("[CERT-CLOSED] PASS_HYPERCHARGE_BL_DIRECTION_BRIDGE")
sys.exit(0)
