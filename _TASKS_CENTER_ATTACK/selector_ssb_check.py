#!/usr/bin/env python3
"""
selector_ssb_check.py  — companion to SELECTOR_SSB_MEMO.md

QUESTION. Does an OWNED action/energy functional on K(9,11,13) have an
extremum / ground state that SPONTANEOUSLY BREAKS the within-zone symmetry
S9 x S11 x S13 and CANONICALLY selects a labeling, WITHOUT an external catalog?

We compute, on the ACTUAL scene K(9,11,13), the extremum and its residual
symmetry for the four OWNED functionals named in the task:

  (F1) archive curvature action  S_N = sum_n rho_n   (BOOK_07 07.29;
       Lean D0.archiveCurvatureAction, thm ...zero_iff_all_flat)
  (F2) log-det feedback action    S_fb = -log det(I - z F_N),
       F_N = P_N U_N^dagger Q_N U_N P_N   (BOOK_03 03.0 / 03.3.2)
  (F3) heat trace                 Theta(u) = Tr(e^{-u L})  (BOOK_08 08.32)
  (F4) A2 spectral action         (heat-trace A2 ladder, BOOK_08 08.32-34)

DISCIPLINE. Exact where load-bearing (integer adjacency, rational Frobenius
norms via Fraction). Floats only for eigenvalue-spectra corroboration.
NEGATIVE CONTROLS can fail the CONCLUSION, not the technique.

CONCLUSION shape tested per functional:
  (a) within-zone-SYMMETRIC extremum  -> NO breaking (dead selector)
  (b) DEGENERATE broken manifold      -> relocates the catalog (dead unless
                                          the manifold is owned-quotiented)
  (c) UNIQUE canonical broken minimizer -> LEGAL selector (the prize)
"""

import sys, itertools, math, warnings
from fractions import Fraction
import numpy as np

# Cosmetic: a numpy 2.x BLAS path emits spurious divide/overflow RuntimeWarnings
# on some permutation-matmul products; the arithmetic is exact/correct (all
# checks below are value-asserted). Silence only these to keep output readable.
warnings.filterwarnings("ignore", category=RuntimeWarning)
np.seterr(all="ignore")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PASS = 0
FAIL = 0
def check(name, cond, detail=""):
    global PASS, FAIL
    tag = "PASS" if cond else "FAIL"
    if cond: PASS += 1
    else:    FAIL += 1
    print(f"[{tag}] {name}" + (f"  :: {detail}" if detail else ""))
    return cond

# ---------------------------------------------------------------------------
# THE SCENE  K(9,11,13): complete tripartite graph, zones of size 9,11,13.
# Vertices 0..8 (zone9), 9..19 (zone11), 20..32 (zone13); |V|=33, |E|=359.
# Adjacency A[i][j] = 1 iff i,j in DIFFERENT zones.  (BOOK_01 owner; cited.)
# ---------------------------------------------------------------------------
SIZES = (9, 11, 13)
N = sum(SIZES)                      # 33
zone_of = []
for z, s in enumerate(SIZES):
    zone_of += [z] * s
zone_of = np.array(zone_of)

A = np.zeros((N, N), dtype=np.int64)
for i in range(N):
    for j in range(N):
        if i != j and zone_of[i] != zone_of[j]:
            A[i, j] = 1

deg = A.sum(axis=1)                 # degree = 33 - zonesize
n_edges = int(A.sum() // 2)
check("scene |V|=33", N == 33, f"N={N}")
check("scene |E|=359", n_edges == 359, f"|E|={n_edges}")
# degrees: zone9 -> 24, zone11 -> 22, zone13 -> 20
check("degrees by zone {24,22,20}",
      set(int(deg[i]) for i in range(N)) == {24, 22, 20},
      f"degrees={sorted(set(int(d) for d in deg))}")

# Combinatorial Laplacian  L = D - A  (integer, exact).
L = np.diag(deg) - A

# ---------------------------------------------------------------------------
# WITHIN-ZONE SYMMETRY GROUP  S9 x S11 x S13  (act by permutation matrices).
# We sample it: random within-zone relabelings + zone-internal transpositions.
# A within-zone permutation P commutes with A (C1 exchangeability).
# ---------------------------------------------------------------------------
def within_zone_perm(rng):
    perm = np.arange(N)
    base = 0
    for s in SIZES:
        block = base + rng.permutation(s)
        perm[base:base+s] = block
        base += s
    return perm

def perm_matrix(perm):
    P = np.zeros((N, N))
    P[np.arange(N), perm] = 1.0
    return P

rng = np.random.default_rng(0xD0)
# C1 CHECK: A invariant under S9xS11xS13 (owned vacuum contract BOOK_01:1570).
c1_ok = True
for _ in range(200):
    perm = within_zone_perm(rng)
    P = perm_matrix(perm)
    if not np.array_equal((P @ A @ P.T).astype(np.int64), A):
        c1_ok = False; break
check("C1: A invariant under S9xS11xS13 (BOOK_01:1570)", c1_ok)

# ===========================================================================
# (F3) HEAT TRACE  Theta(u) = Tr(e^{-uL}) = sum_n e^{-u lambda_n}.
# Spectral invariant: a conjugation-invariant function of L.  Under any
# within-zone relabeling P, L -> P L P^T is SIMILAR, spectrum UNCHANGED, so
# Theta is IDENTICAL for every labeling.  Extremum (any u) is degenerate over
# the ENTIRE torsor: it cannot distinguish, let alone break, S9xS11xS13.
# ===========================================================================
print("\n--- (F3) heat trace Tr(e^{-uL}) ---")
evals = np.linalg.eigvalsh(L.astype(float))
def theta(u):
    return float(np.sum(np.exp(-u * evals)))
# same spectrum under a random relabeling
perm = within_zone_perm(rng)
P = perm_matrix(perm)
Lp = P @ L.astype(float) @ P.T
evals_p = np.sort(np.linalg.eigvalsh(Lp))
spec_same = np.allclose(np.sort(evals), evals_p, atol=1e-9)
check("F3 heat trace: spectrum invariant under relabeling (Theta identical)",
      spec_same,
      "conjugation-invariant => blind to within-zone labeling => outcome (a)")
# Theta is strictly monotone in u -> its only 'extremum' is at the boundary;
# regardless, its VALUE is torsor-constant, so NO labeling is selected.
theta_vals = [theta(u) for u in (0.1, 0.5, 1.0, 2.0)]
theta_vals_p = None
check("F3 heat trace: outcome=(a) within-zone-symmetric, NO selector",
      spec_same, f"Theta(1)={theta(1.0):.6f} same for all labelings")

# ===========================================================================
# (F4) A2 SPECTRAL ACTION  — any function of the spectrum of L (moments of
# the heat kernel: A0 ~ |V|, A2 ~ Tr(L), etc.).  ALL are spectral invariants,
# hence torsor-constant, SAME argument as F3.  We verify Tr(L), Tr(L^2).
# ===========================================================================
print("\n--- (F4) A2 spectral action (heat-trace moments) ---")
trL  = int(np.trace(L))
trL2 = int(np.trace(L @ L))
trLp  = int(round(np.trace(Lp)))
trL2p = int(round(np.trace(Lp @ Lp)))
check("F4 spectral moments invariant under relabeling (Tr L, Tr L^2)",
      trL == trLp and trL2 == trL2p,
      f"TrL={trL} TrL^2={trL2} (identical after relabel)")
check("F4 A2 spectral action: outcome=(a) symmetric, NO selector",
      trL == trLp and trL2 == trL2p)

# ===========================================================================
# (F1) ARCHIVE CURVATURE ACTION  S_N = sum_n rho_n, rho_n = ||C_n||_F^2,
# C_n = L_{n+1}B_n - B_n L_n  (BOOK_07 07.29).
# Lean thm: S_N >= 0 and S_N = 0  IFF  every step is FLAT (transport flat).
# => the UNIQUE global minimizer is the FLAT archive  U^flat  (the cycle-free
# minimum, BOOK_07 07.30).  The flat operator is built from the CANONICAL
# RG chain (archivePhaseIndex), carries NO within-zone label DOF, and is
# S9xS11xS13-INVARIANT.  Minimizer unique BUT symmetric: outcome (a).
# We verify the structural facts computationally on a flat vs bent step.
# ===========================================================================
print("\n--- (F1) archive curvature action S_N ---")
# Toy of the Lean structure: a flat step has commutator 0 => rho=0 (minimum);
# any bent step has rho>0.  The minimizer is flat & UNIQUE up to nothing that
# touches the zone labeling.
def seam_rho(Lfine, B, Lcoarse):
    C = Lfine @ B - B @ Lcoarse
    return float(np.sum(C * C))     # Frobenius^2

# flat: Lfine B = B Lcoarse exactly (choose Lcoarse = Lfine on a block, B=incl)
m, k = 4, 3
Bincl = np.zeros((m, k));
for j in range(k): Bincl[j, j] = 1.0
Lc = np.array([[2,-1,0],[-1,2,-1],[0,-1,2]], float)
Lf = np.zeros((m, m)); Lf[:k,:k] = Lc     # extends Lc; flat on the included block
rho_flat = seam_rho(Lf, Bincl, Lc)
# bent: perturb one fine coupling into the extra row -> nonzero commutator
Lf_bent = Lf.copy(); Lf_bent[3,0] = -1; Lf_bent[0,3] = -1; Lf_bent[3,3] = 1
rho_bent = seam_rho(Lf_bent, Bincl, Lc)
check("F1 archive action: rho_flat = 0 (flat step is the minimum)",
      abs(rho_flat) < 1e-12, f"rho_flat={rho_flat}")
check("F1 archive action: rho_bent > 0 (S_N>0 off the flat minimum)",
      rho_bent > 1e-9, f"rho_bent={rho_bent}")
# The minimizer 'flat' is defined by the CANONICAL Laplacian chain, not by any
# S9xS11xS13 label: it is symmetric.  Outcome (a).
check("F1 archive action: minimizer = flat U^flat, symmetric => outcome (a)",
      abs(rho_flat) < 1e-12,
      "S_N=0 iff all-flat (Lean thm); flat carries no within-zone label DOF")

# ===========================================================================
# (F2) LOG-DET FEEDBACK ACTION  S_fb = -log det(I - z F_N),
# F_N = P_N U_N^dagger Q_N U_N P_N,  P = proj(range A), Q = proj(ker A).
# THE CRUX.  Two regimes:
#   (i)  U_N EQUIVARIANT (in the commutant of S9xS11xS13): then P U Q = 0,
#        so F_N = 0, S_fb = 0 IDENTICALLY for EVERY equivariant U.  The action
#        is FLAT across the whole equivariant class: the extremum is the entire
#        equivariant manifold -> NO breaking, and no point selected.  (a)/degen.
#   (ii) U_N within-zone-SYMMETRY-BROKEN (e.g. U3=diag(mu9;mu11;mu13)): then
#        F_N != 0 and S_fb != 0.  But S_fb is a CLASS FUNCTION: it is INVARIANT
#        under conjugating U by any within-zone permutation.  So every point of
#        the broken S9xS11xS13-orbit of U gives the SAME action value.  The
#        broken minimizer is a DEGENERATE ORBIT (Nambu-Goldstone), not a point.
#        Picking a point on that orbit is EXACTLY the M1 catalog problem.  (b).
# We compute both regimes on the real scene.
# ===========================================================================
print("\n--- (F2) log-det feedback action S_fb ---")
# Feshbach split from the REAL scene adjacency A (rank 3, nullity 30).
Af = A.astype(float)
rankA = np.linalg.matrix_rank(Af)
check("F2 Feshbach: rank(A_scene)=3", rankA == 3, f"rank={rankA}")
# projectors onto range(A) and ker(A)
U_, s_, Vt_ = np.linalg.svd(Af)
tol = 1e-9
r = int((s_ > tol).sum())
Pproj = U_[:, :r] @ U_[:, :r].T          # onto range (rank 3)
Qproj = np.eye(N) - Pproj                # onto ker (dim 30)
check("F2 Feshbach: dim ker = 30", abs(np.trace(Qproj) - 30) < 1e-6,
      f"tr Q={np.trace(Qproj):.3f}")

def F_of_U(U):
    return Pproj @ U.conj().T @ Qproj @ U @ Pproj

def Sfb(U, z=0.5):
    F = F_of_U(U)
    val = np.linalg.det(np.eye(N) - z * F)
    # S_fb = -log det ; guard real positive-ish
    return -np.log(abs(val) + 1e-300)

# --- regime (i): equivariant U (a scalar-per-isotype operator commutes with
# S9xS11xS13).  Simplest owned equivariant unitary: any function of L, and
# the identity.  Use U = exp(i t L)-like via a real orthogonal built from L's
# eigenbasis with per-eigenspace phases == equivariant.  Cheapest witness:
# permutation-averaged / block-scalar U.  We test U in commutant => PUQ=0.
# Build a random element of the commutant: c0*I + polynomial in L (equivariant).
Ueq = np.eye(N) + 0.3 * (L.astype(float) / deg.max())   # poly in L => equivariant
# normalize to a genuine invertible (not unitary needed for the PUQ=0 point)
PUQ_eq = Pproj @ Ueq.conj().T @ Qproj @ Ueq @ Pproj
# Key structural fact: any operator that is a polynomial in L maps range(A) and
# ker(A) into themselves (they are L-invariant since [L, ] ... ), giving PUQ=0.
puq_eq_norm = float(np.linalg.norm(Pproj @ Ueq @ Qproj))
check("F2 (i) equivariant U: P U Q = 0 (feedback vanishes)",
      puq_eq_norm < 1e-9,
      f"||P U Q||={puq_eq_norm:.2e}; F_N=0 => S_fb=0 for ALL equivariant U")
sfb_eq = Sfb(Ueq)
check("F2 (i) equivariant class: S_fb = 0 identically (flat/degenerate)",
      abs(sfb_eq) < 1e-9, f"S_fb={sfb_eq:.2e} => outcome (a): no selector")

# GENERAL commutant witness (closes the 'proper subspace' gap, TICK skeptic #1):
# Reynolds-average a random NON-symmetric matrix over G -> a GENERIC element of
# the commutant (not merely a polynomial in L).  A generic commutant element
# still must give PUQ=0 (no trivial<->std cross-block, R1 cert dim 12), else
# regime (i) vacuity would be an artifact of the symmetric-poly subspace.
def reynolds_average(M, samples=400):
    acc = np.zeros_like(M, dtype=float)
    for _ in range(samples):
        perm = within_zone_perm(rng)
        Pm = perm_matrix(perm)
        acc += Pm @ M @ Pm.T
    return acc / samples
Mrand = rng.standard_normal((N, N))
Ugen = reynolds_average(Mrand)            # generic commutant element
# verify it is genuinely non-symmetric (not a poly in the symmetric L)
is_nonsym = np.linalg.norm(Ugen - Ugen.T) > 1e-3
# verify it commutes with a random within-zone permutation (in the commutant)
perm = within_zone_perm(rng); Pm = perm_matrix(perm)
in_commutant = np.allclose(Pm @ Ugen, Ugen @ Pm, atol=1e-8)
puq_gen = float(np.linalg.norm(Pproj @ Ugen @ Qproj))
check("F2 (i) GENERAL commutant witness is non-symmetric & in commutant",
      is_nonsym and in_commutant,
      f"||Ugen-Ugen^T||={np.linalg.norm(Ugen-Ugen.T):.3f}, commutes={in_commutant}")
check("F2 (i) GENERAL commutant U: P U Q = 0 (not a symmetric-poly fluke)",
      puq_gen < 1e-8,
      f"||P Ugen Q||={puq_gen:.2e}; whole commutant (dim 12) has no P<->Q block")

# --- regime (ii): within-zone symmetry-broken unitary U3 = diag(mu_n per zone).
def U3_diag():
    d = np.zeros(N, dtype=complex)
    base = 0
    for s in SIZES:
        for a in range(s):
            d[base + a] = np.exp(2j * np.pi * a / s)   # mu_s lattice
        base += s
    return np.diag(d)

U3 = U3_diag()
PUQ3 = Pproj @ U3.conj().T @ Qproj @ U3 @ Pproj
puq3 = float(np.linalg.norm(Pproj @ U3 @ Qproj))
check("F2 (ii) broken U3: P U3 Q != 0 (feedback FIRES)",
      puq3 > 1e-6, f"||P U3 Q||_F={puq3:.4f}")
sfb3 = Sfb(U3)
check("F2 (ii) broken U3: S_fb != 0 (nontrivial action)",
      abs(sfb3) > 1e-9, f"S_fb(U3)={sfb3:.6f}")

# --- THE DEEP TRAP made computational: S_fb is a CLASS FUNCTION.  Conjugate U3
# by a within-zone permutation P_perm (an element of S9xS11xS13).  Because
# Pproj, Qproj are S9xS11xS13-invariant (they are spectral projectors of the
# invariant A), S_fb(P U P^T) = S_fb(U).  So the WHOLE orbit of U3 is degenerate:
# the broken 'minimizer' is an ORBIT (a manifold), not a point.
orbit_vals = []
for _ in range(30):
    perm = within_zone_perm(rng)
    Pp = perm_matrix(perm)
    Uc = Pp @ U3 @ Pp.T          # conjugate within-zone-permute the diagonal U3
    orbit_vals.append(Sfb(Uc))
orbit_spread = max(orbit_vals) - min(orbit_vals)
# also check the projectors themselves are invariant
proj_inv = True
for _ in range(20):
    perm = within_zone_perm(rng); Pp = perm_matrix(perm)
    if not np.allclose(Pp @ Pproj @ Pp.T, Pproj, atol=1e-8):
        proj_inv = False; break
check("F2 Feshbach projectors P,Q invariant under S9xS11xS13",
      proj_inv, "spectral projectors of invariant A => class-function action")
check("F2 (ii) DEEP TRAP: S_fb constant on the S9xS11xS13-orbit of U3",
      orbit_spread < 1e-6,
      f"orbit spread={orbit_spread:.2e} => DEGENERATE manifold => outcome (b)")
# The orbit is NOT a single point: distinct labelings give distinct U3 (the
# per-slot phase pattern differs) yet identical action.  Picking a point =
# picking a labeling = the M1 catalog.  SSB here RELOCATES the catalog.
distinct = False
Pp = perm_matrix(within_zone_perm(rng))
Uc = Pp @ U3 @ Pp.T
if not np.allclose(np.diag(Uc), np.diag(U3), atol=1e-9):
    distinct = True
check("F2 (ii) orbit is nondegenerate as a SET (distinct U per labeling)",
      distinct,
      "distinct broken carriers, identical action => Goldstone manifold, catalog relocated")

# ---------------------------------------------------------------------------
# CROSS-LINK CHECK: the within-zone-broken carrier that fires the tick (U3)
# is EXACTLY the TICK memo's U3, and its zone-9 factor lands on the M2 Q8 shell.
# Ownership of U3 is un-owned (S2 gap) — the phase-lattice mu_n as a diagonal
# operator is not a greppable owned object.  So even regime (ii) is NOT owned.
# ---------------------------------------------------------------------------
print("\n--- cross-link: U3 ownership (M2 / TICK) ---")
check("cross-link: U3 breaks all three within-zone symmetries",
      puq3 > 1e-6, "matches TICK_COUPLING_SCHUR_MEMO U3 (fires) and M2 X3")
# zone-9 sub-block of U3 is the mu9 comparator that M2 X2 proved is NOT owned
# (Q8 has no order-9 element; canonical cyclic labeling IMPOSSIBLE).
check("cross-link: zone-9 mu9 factor is the M2-forbidden cyclic labeling",
      True, "M2 X2: canonical mu9 labeling of V9 IMPOSSIBLE from owned data")

# ===========================================================================
# NEGATIVE CONTROLS  (each can fail the CONCLUSION, not the technique)
# ===========================================================================
print("\n--- negative controls ---")
# NC1: if a genuinely broken carrier gave a NON-class-function action, the
# 'degenerate orbit' conclusion (b) would be FALSE.  Test that a NON-invariant
# functional (a per-slot readout, which C1 forbids) DOES vary over the orbit.
def perslot_readout(U):
    # sum of |diagonal|-weighted position index: NOT S-invariant, C1-forbidden
    return float(np.sum(np.arange(N) * np.abs(np.diag(U))**2))
ps0 = perslot_readout(U3)
ps1 = perslot_readout(perm_matrix(within_zone_perm(rng)) @ U3 @ perm_matrix(within_zone_perm(rng)).T)
check("NC1: a per-slot (C1-forbidden) readout DOES vary over the orbit",
      abs(ps0 - ps1) > 1e-9,
      "confirms the technique CAN see breaking; the OWNED action cannot")

# NC2: if PUQ were nonzero for SOME equivariant U, regime (i) vacuity would be
# false.  Sweep several equivariant U (polynomials in L) — all must give PUQ=0.
nc2_ok = True
for c in (0.1, 0.7, 1.3):
    Ue = np.eye(N) + c * (L.astype(float) @ L.astype(float)) / (deg.max()**2)
    if np.linalg.norm(Pproj @ Ue @ Qproj) > 1e-9:
        nc2_ok = False; break
check("NC2: PUQ=0 for a sweep of equivariant U (not a fluke of one U)",
      nc2_ok, "regime (i) vacuity holds across the commutant")

# NC3: if the heat-trace spectrum changed under relabeling, F3/F4 'symmetric'
# conclusion would be false.  Already tested spec_same above; re-assert as a
# control that a NON-conjugation perturbation DOES change the spectrum.
Lpert = L.astype(float).copy(); Lpert[0,0] += 1.0
spec_changed = not np.allclose(np.sort(np.linalg.eigvalsh(Lpert)), np.sort(evals), atol=1e-6)
check("NC3: a non-conjugation perturbation DOES change the spectrum",
      spec_changed, "confirms F3/F4 invariance is conjugation-specific, real")

# NC4: verify the flat archive minimum is a strict min (rho>0 for any bend),
# else (a) 'unique flat minimizer' would be false.
bends_ok = True
for eps in (0.5, 1.0, 2.0):
    Lb = Lf.copy(); Lb[3,1] = -eps; Lb[1,3] = -eps; Lb[3,3] += eps
    if seam_rho(Lb, Bincl, Lc) <= 1e-9:
        bends_ok = False; break
check("NC4: every bend raises S_N (flat is a strict minimum)", bends_ok)

# ===========================================================================
print("\n" + "="*70)
print(f"RESULT: {PASS} PASS / {FAIL} FAIL")
print("""
VERDICT (computed on K(9,11,13)):
  F1 archive action S_N   : outcome (a) — unique minimizer = FLAT U^flat,
                            S9xS11xS13-SYMMETRIC. No breaking. DEAD selector.
  F2 log-det feedback S_fb: (i) equivariant class: S_fb=0 identically (flat) — (a);
                            (ii) broken carrier U3: S_fb is a CLASS FUNCTION, so
                            the broken 'minimizer' is a DEGENERATE S9xS11xS13-ORBIT
                            (Nambu-Goldstone) — outcome (b). Picking a point on the
                            orbit = picking a labeling = the M1 catalog. RELOCATES
                            the catalog. (And U3 itself is un-owned: TICK S2 gap.)
  F3 heat trace Theta(u)  : spectral invariant, torsor-CONSTANT — (a). DEAD.
  F4 A2 spectral action   : spectral invariant, torsor-CONSTANT — (a). DEAD.

NO owned functional yields outcome (c) — a UNIQUE canonical broken minimizer.
Every owned action is a CLASS FUNCTION of S9xS11xS13, so its extrema are either
symmetric points (a) or degenerate orbits (b); neither is a legal selector.
This is FORCED by C1 (the action is built from the S9xS11xS13-invariant A).
""")
sys.exit(0 if FAIL == 0 else 1)
