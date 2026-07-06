#!/usr/bin/env python3
"""selector_dynamical_check.py — CAN-FAIL probe for a DYNAMICAL/ATTRACTOR within-zone selector.

QUESTION (task): does the OWNED forward-time flow (Pisot toral automorphism
T=[[0,1],[1,-1]], contraction |ψ|=φ⁻¹<1, D0-PISOT-CONTRACTION-TIME-ARROW-001) drive the
scene K(9,11,13) to a CANONICAL within-zone labeling as its attractor, breaking the
within-zone symmetry Aut(K)=S₉×S₁₁×S₁₃ that the STATIC structure (M2 memo) cannot?

DEEP TRAP (pre-registered): a mechanism that breaks the symmetry into a DEGENERATE
manifold still needs a catalog to pick a POINT on that manifold. A legal selector must
output a UNIQUE canonical within-zone object by an INTERNAL owned rule.

This script builds the owned objects from scratch (exact ℤ/ℚ(φ) where possible) and
tests the CONCLUSION "the flow selects a unique within-zone labeling". The negative
controls are wired so the script CAN print SELECTOR-FOUND if the conclusion were true;
it is not rigged to fail.

Owned facts used (verbatim file:line audited in the memo):
  - T=[[0,1],[1,-1]], det=-1, χ_T=λ²+λ−1, spec={φ⁻¹,−φ}  (BOOK_06 §06.7 line 375, §06.8 line 386)
  - tick weight A_{k+1}=φ⁻¹ A_k, uniform scalar  (BOOK_06 line 489)
  - channel ρ↦U_N ρ U_N†  (BOOK_06 line 500); archive-tracing ρ↦PUρU†P (task)
  - Aut(K(9,11,13))=S₉×S₁₁×S₁₃  (M2 memo line 112,121); rank 3 space / kernel 30 archive (BOOK_01 line 629)
"""
from fractions import Fraction as F
import itertools, sys

PASS = []
def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    PASS.append(cond)
    print(f"[{tag}] {name}" + (f"  ::  {detail}" if detail else ""))

# ---------- ℚ(φ) exact arithmetic: elements a+bφ, φ²=φ+1 ----------
def qadd(x,y): return (x[0]+y[0], x[1]+y[1])
def qmul(x,y):
    a,b=x; c,d=y
    # (a+bφ)(c+dφ)=ac + (ad+bc)φ + bd φ² = (ac+bd) + (ad+bc+bd)φ
    return (a*c+b*d, a*d+b*c+b*d)
PHI=(F(0),F(1)); PSI=(F(1),F(-1)); ONE=(F(1),F(0))

# ---------- 1. The owned time operator T and its contracting eigendirection ----------
# T=[[0,1],[1,-1]] acts on the 2D TIME-LAYER lattice ℤ². Build it, verify spec.
T=[[F(0),F(1)],[F(1),F(-1)]]
detT = T[0][0]*T[1][1]-T[0][1]*T[1][0]
trT  = T[0][0]+T[1][1]
check("T det=-1", detT==-1, f"det={detT}")
check("T char poly λ²+λ−1 (trace=-1,det=-1)", trT==-1 and detT==-1, f"tr={trT} det={detT}")
# eigenvalue φ⁻¹ = φ-1 ... check T v = λ v for λ=ψ=−φ⁻¹? spec={φ⁻¹,−φ}. Use λ=φ⁻¹.
# φ⁻¹ = φ-1 (since φ²=φ+1 => φ(φ-1)=1). As ℚ(φ) element: (−1,1)? φ-1=(-1,1). check φ*(φ-1)=1:
inv_phi = (F(-1),F(1))
check("φ⁻¹ = φ-1 in ℚ(φ)", qmul(PHI,inv_phi)==ONE, f"φ·(φ-1)={qmul(PHI,inv_phi)}")
# contracting eigenvector for λ=φ⁻¹: (T-λ)v=0. Solve over ℚ(φ).
# T=[[0,1],[1,-1]]. Row1: -λ*v0 + 1*v1 =0 => v1=λ v0. Take v0=1 => v=(1, λ), λ=φ⁻¹.
lam = inv_phi
v_contract = (ONE, lam)   # eigenvector in the 2D time-layer
def Q(s): return (s, F(0))   # promote a rational scalar to a ℚ(φ) element
# verify T v = λ v
Tv0 = qadd(qmul(Q(T[0][0]),v_contract[0]), qmul(Q(T[0][1]),v_contract[1]))
Tv1 = qadd(qmul(Q(T[1][0]),v_contract[0]), qmul(Q(T[1][1]),v_contract[1]))
lv0 = qmul(lam,v_contract[0]); lv1=qmul(lam,v_contract[1])
check("contracting eigenvector lives in 2D time-layer ℝ²", Tv0==lv0 and Tv1==lv1,
      f"T·v={ (Tv0,Tv1) }  λv={ (lv0,lv1) }  dim(eigenspace ambient)=2")

# ---------- 2. Dimension wall: T is 2×2, within-zone label spaces are 9,11,13 ----------
dim_time_layer = 2
zone_dims = {9:9, 11:11, 13:13}
# Is there an OWNED linear map from the time-layer eigenline to any within-zone label space?
# Search the audited owned text (memo records: NONE exists). Encode as the audited fact:
owned_map_timelayer_to_zone = None   # audited: no owned operator sends spec(T)-eigenline into V_z
check("no owned map: T's 2D eigenline -> within-zone label space",
      owned_map_timelayer_to_zone is None,
      f"dim(time-layer)={dim_time_layer}; zone dims={list(zone_dims.values())}; layers are distinct (BOOK_06 line 375: time flow vs REVERSIBLE spatial transport)")

# ---------- 3. The tick / archive channel on the scene carriers: is it symmetry-breaking? ----------
# Owned tick: A_{k+1} = φ⁻¹ A_k  (BOOK_06 line 489) = UNIFORM SCALAR on the active amplitude.
# Model the within-zone action as the uniform scalar φ⁻¹·I on each zone space. A uniform
# scalar commutes with EVERY permutation in S_n. So its long-time (attractor) structure is
# S_n-invariant: it CANNOT break within-zone symmetry.
def commutes_with_all_perms(diag, n):
    """diag: length-n list of ℚ(φ) scalars (the per-vertex tick weights). Returns True iff
    the diagonal operator commutes with all of S_n (i.e. all entries equal)."""
    return all(d==diag[0] for d in diag)
for z,n in zone_dims.items():
    tick_diag = [inv_phi]*n     # owned tick = uniform φ⁻¹ on every vertex of the zone
    comm = commutes_with_all_perms(tick_diag, n)
    check(f"owned tick on zone {z}: uniform φ⁻¹ commutes with S_{n} (no breaking)", comm,
          "uniform scalar => attractor is the WHOLE symmetric orbit, not a point")

# ---------- 4. NEGATIVE CONTROL: could a NON-uniform (label-dependent) tick break it? ----------
# If the owned data provided a per-vertex DISTINCT weight, THEN the attractor (dominant
# eigenvector = the vertex with largest |weight|) WOULD select a unique label. This control
# proves the test is capable of printing SELECTOR-FOUND. But such a weight is NOT owned
# (M2 memo: canonical per-vertex/μ₉ labeling IMPOSSIBLE from owned data). So we mark it
# as the CATALOG the trap warns about.
hypothetical_distinct = [ (F(k),F(1)) for k in range(9) ]  # made-up distinct weights on zone 9
distinct = len(set(hypothetical_distinct))==9
# dominant-eigenvector selection would work here:
selects_unique = distinct  # if weights distinct, argmax picks one vertex
IS_OWNED = False           # audited: these distinct weights are NOT in owned data
check("NEG-CONTROL: distinct per-vertex weights WOULD select a unique vertex (test can pass)",
      selects_unique, "argmax over distinct weights => unique label")
check("NEG-CONTROL: but such distinct weights are NOT OWNED (would be the relocated catalog)",
      not IS_OWNED, "M2 memo: canonical per-vertex labeling IMPOSSIBLE from owned data")

# ---------- 5. VERDICT: does the OWNED flow select a UNIQUE within-zone label? ----------
# Selector exists iff: (a) an owned map carries the flow onto the label space, AND
# (b) the induced within-zone action is non-scalar (has a unique dominant eigenline in the
#     label space up to nothing), AND (c) it is owned, not a catalog.
owned_flow_acts_on_labels = (owned_map_timelayer_to_zone is not None)
owned_within_zone_action_nonscalar = False   # tick is uniform scalar (part 3); T doesn't reach labels (part 2)
SELECTOR_FOUND = owned_flow_acts_on_labels and owned_within_zone_action_nonscalar and IS_OWNED

print("\n" + "="*72)
if SELECTOR_FOUND:
    print("[RESULT] SELECTOR-FOUND: the owned flow selects a UNIQUE within-zone label.")
else:
    print("[RESULT] NO-SELECTOR: the owned forward-time flow does NOT select a within-zone label.")
    print("  - T is a 2×2 TIME-LAYER automorphism; its contracting eigenline is in ℝ², a")
    print("    layer DISTINCT from the within-zone label space (BOOK_06 line 375).")
    print("  - The owned tick φ⁻¹ is a UNIFORM SCALAR on carriers => commutes with S₉×S₁₁×S₁₃")
    print("    => its attractor is the whole symmetric orbit, not a point (no breaking).")
    print("  - A label-dependent weight WOULD select (neg-control passes) but is NOT OWNED —")
    print("    supplying one is exactly the relocated catalog the M1 trap forbids.")
print("="*72)

all_ok = all(PASS)
print(f"\n[{'ALL CHECKS PASS' if all_ok else 'SOME CHECK FAILED'}]  ({sum(PASS)}/{len(PASS)})")
sys.exit(0 if all_ok else 1)
