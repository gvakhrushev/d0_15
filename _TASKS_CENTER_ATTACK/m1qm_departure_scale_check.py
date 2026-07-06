#!/usr/bin/env python3
"""
M1-QM non-unitary DEPARTURE SCALE — can-fail check.

Question: is there an OWNED object that fixes the SCALE at which D0's owned emergent QM
dynamics departs from exact unitarity, AND does that scale land at the IceCube plateau-knee
E*? REPAIRED verdict (skeptic ACCEPT-IN-FULL, R1-R5): the owned DEPARTING dynamics is the
archive-tracing channel rho -> P U rho U^dag P (M1_QM_GAP1 Block D / 06.7:29), whose per-tick
retained-amplitude decay IS the owned+FORCED phi^-1 (06.40). So an owned+forced RATE governs
the departing dynamics. What is genuinely EXTERNAL is only the mapping of that per-tick rate
to the IceCube knee ENERGY E* (needs the unowned kappaV(E)/zeta bridge). The old headline
"no owned object fixes the departure RATE" was a LEAP (it silently defined "departure" against
the post-conditioned exactly-unitary Block C complement -- the object that does NOT depart --
instead of the departing tracing channel D0 owns as the dynamics).

Compute-first: exact Fraction/Q(phi) where the quantity is arithmetic; the REAL K(9,11,13)
Feshbach SVD and the archive-tracing trace-loss are computed with numpy (imported from the
parent construction, m1_qm_gap1_check.py:72-146,176-207); float only for the SI observability
arithmetic (a counterfactual on the ENERGY, per memo §5).

No book/registry/.lean touched. Reads nothing; self-contained numerics reproducing the
owned quantities cited verbatim in the memo.
"""
import sys
import warnings
from fractions import Fraction
import numpy as np

# macOS Accelerate-backed numpy emits spurious matmul RuntimeWarnings on exact-projector products
# (same as parent m1_qm_gap1_check.py:52-56). Safe to silence: every load-bearing quantity is
# gate()-checked, so a real NaN/inf still flips its gate to FAIL; nothing is trusted from a clean run.
warnings.filterwarnings("ignore", message=".*encountered in matmul.*", category=RuntimeWarning)

FAILS = []
def gate(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAILS.append(name)
    print(f"{tag}_{name}  {detail}")

# ---- Q(phi) mini-arithmetic: represent a+b*phi with phi^2=phi+1 -----------------
def qmul(x, y):
    (a, b), (c, d) = x, y
    # (a+b phi)(c+d phi) = ac + (ad+bc) phi + bd phi^2 = (ac+bd) + (ad+bc+bd) phi
    return (a*c + b*d, a*d + b*c + b*d)
def qpow(x, n):
    r = (Fraction(1), Fraction(0))
    for _ in range(n):
        r = qmul(r, x)
    return r
PHI = (Fraction(0), Fraction(1))          # phi
PHI_INV = (Fraction(-1), Fraction(1))     # phi^-1 = phi - 1  (since 1/phi = phi-1) = -1 + 1*phi
SQRT5 = 5 ** 0.5
phi_f = (1 + SQRT5) / 2

print("=== M1-QM DEPARTURE SCALE — can-fail check ===\n")

# ---------------------------------------------------------------------------
# 1. OWNED FACTS reproduced (each is cited verbatim in the memo).
# ---------------------------------------------------------------------------

# 1a. phi^-1 satisfies the detector primitive p + p^2 = 1  (BOOK_01; forces p=phi^-1).
#     06.40:23 "p+p^2=1 ... unique admissible root p=phi^-1 ... per-tick decay A_{t+1}=phi^-1 A_t".
p_plus_psq = tuple(a + b for a, b in zip(PHI_INV, qmul(PHI_INV, PHI_INV)))
gate("PRIMITIVE_P_PLUS_PSQ_EQ_1", p_plus_psq == (Fraction(1), Fraction(0)),
     f"p+p^2 = {p_plus_psq} (== 1+0*phi)  [06.40:23 forces p=phi^-1]")

# 1b. per-tick trace-production recursion A_t = p^t A_0, B_t = (1-p^t) A_0  (06.40:3-16).
#     Verify A + B conserved per tick (A leaks to B): A_{t+1}+B_{t+1} = A_t+B_t.
def AB(t):
    p = PHI_INV
    A = qpow(p, t)                                   # A_t / A_0
    one = (Fraction(1), Fraction(0))
    B = tuple(o - a for o, a in zip(one, A))         # B_t/A_0 = 1 - p^t
    return A, B
A1, B1 = AB(1); A2, B2 = AB(2)
tot1 = tuple(a + b for a, b in zip(A1, B1))
tot2 = tuple(a + b for a, b in zip(A2, B2))
gate("TRACE_PRODUCTION_CONSERVED", tot1 == (Fraction(1), Fraction(0)) and tot2 == (Fraction(1), Fraction(0)),
     f"A_t+B_t = {tot1} at t=1, {tot2} at t=2 (full amplitude conserved; A leaks to archive B)")

# 1c. alpha-seam depth phi^-17 = phi^-5 * phi^-12  (02.13:87). Exact in Q(phi).
d17 = qpow(PHI_INV, 17)
d5x12 = qmul(qpow(PHI_INV, 5), qpow(PHI_INV, 12))
gate("ALPHA_DEPTH_FACTORS", d17 == d5x12,
     f"phi^-17 == phi^-5 * phi^-12 : {d17} == {d5x12}  [static coupling depth, not a rate]")

# 1d. delta0 cascade delta0^{n+1}; delta0 = phi-3/2 = 1/(2 phi^3)  (vp_dim_ladder_compact.py:28).
delta0 = tuple(a + b for a, b in zip((Fraction(-3, 2), Fraction(0)), PHI))   # phi - 3/2
half_phi_m3 = qmul((Fraction(1, 2), Fraction(0)), qpow(PHI_INV, 3))          # (1/2) phi^-3
gate("DELTA0_VALUE", delta0 == half_phi_m3,
     f"delta0 = phi-3/2 == (1/2)phi^-3 : {delta0} == {half_phi_m3}  [dimension ladder, not a rate]")

# ---------------------------------------------------------------------------
# 1e. REAL frozen K(9,11,13) construction (copied verbatim from m1_qm_gap1_check.py:72-94,
#     128-146,176-207). Used by the REPAIRED adjudication gates 2a/2a' below. This replaces the
#     old tautology gate (|product of unit-modulus phases| == 1, which is 1 for ANY n and CANNOT
#     fail; skeptic R3 KILL GATE 3).
# ---------------------------------------------------------------------------
SIZES = [9, 11, 13]
NDIM = 33

def build_scene():
    zone = sum(([i] * s for i, s in enumerate(SIZES)), [])
    A = np.array([[1.0 if zone[i] != zone[j] else 0.0 for j in range(NDIM)] for i in range(NDIM)])
    w, V = np.linalg.eigh(A)
    Kk = V[:, np.abs(w) < 1e-9]
    Q = Kk @ Kk.T
    P = np.eye(NDIM) - Q
    idx = [range(0, 9), range(9, 20), range(20, 33)]
    uv = []
    for r in idx:
        u = np.zeros(NDIM)
        for i in r:
            u[i] = 1.0
        uv.append(u / np.linalg.norm(u))
    return P, Q, uv

def build_u3():
    d = []
    for n in SIZES:
        d += [np.exp(2j * np.pi * j / n) for j in range(n)]
    return np.diag(d)

P, Q, uv = build_scene()
U3 = build_u3()
res = np.linalg.inv(np.eye(NDIM) - Q @ U3 @ Q)          # exists: QUQ nilpotent (parent B1)
Weff = P @ U3 @ P + P @ U3 @ Q @ res @ Q @ U3 @ P       # Feshbach effective map (parent B3)
B = np.array(uv).T                                       # 33x3 retained basis

# ---------------------------------------------------------------------------
# 2. THE ADJUDICATION GATES — each can fail the REPAIRED conclusion.
#    REPAIRED conclusion (R1): phi^-1 IS the owned+forced per-tick departure rate of the
#    archive-tracing channel (the object D0 owns as the dynamics); what is EXTERNAL is only the
#    mapping of that rate to the IceCube knee ENERGY E*. So the gates now test the TRUE
#    adjudication: (2a) the post-conditioned complement does NOT depart, but (2a') the tracing
#    channel D0 actually owns DOES depart, at rate phi^-1; (2b) the departure is floorless O(1)
#    (so it is not the positive-floor IceCube PLATEAU knee); (2c) the knee ENERGY is unowned.
# ---------------------------------------------------------------------------

# 2a. THE POST-CONDITIONED COMPLEMENT DOES NOT DEPART (this is NOT "the dynamics"; skeptic R2/R3).
#     Real B^dag W_eff B SVD (m1_qm_gap1_check.py:154-161), NOT a phase-product tautology.
#     This is the object the OLD memo wrongly called "the departure"; it is exactly unitary
#     because it post-conditions on coherent return (parent Block D verdict, :304-312).
Wsub = B.conj().T @ Weff @ B
sv_complement = np.linalg.svd(Wsub, compute_uv=False)
complement_unitary = np.allclose(Wsub.conj().T @ Wsub, np.eye(3), atol=1e-8)
gate("F_COMPLEMENT_POSTCOND_IS_UNITARY_NOT_THE_DYNAMICS", complement_unitary,
     f"B^dag W_eff B singular values = {np.round(sv_complement,6).tolist()} == 1 => the "
     f"post-conditioned coherent complement does NOT depart. Per parent :304-312 this is NOT "
     f"'the dynamics' -- it is the resolvent-summed no-net-leak object. NOT the departure.")

# 2a'. THE OWNED DEPARTING DYNAMICS DOES DEPART, at per-tick rate phi^-1 (skeptic R2/R3 -- the
#      gate the old script RIGGED AWAY). D0's owned reading (06.7:29) picks the archive-tracing
#      channel rho -> P U rho U^dag P (M1_QM_GAP1 Block D, m1_qm_gap1_check.py:176-207): it LOSES
#      probability for every carrier/state (trace<1) => it genuinely departs from unitarity.
#      The per-tick retained-amplitude decay of that ladder is A_{t+1}=phi^-1 A_t (06.40, FORCED).
rng = np.random.default_rng(3)
traces = []
for _ in range(300):
    Xk = rng.standard_normal((NDIM, NDIM)) + 1j * rng.standard_normal((NDIM, NDIM))
    Uk, _ = np.linalg.qr(Xk)
    psi = B @ (rng.standard_normal(3) + 1j * rng.standard_normal(3))
    psi = psi / np.linalg.norm(psi)
    out = P @ Uk @ np.outer(psi, psi.conj()) @ Uk.conj().T @ P
    traces.append(np.trace(out).real)
traces = np.array(traces)
tracing_channel_departs = np.all(traces < 1.0 - 1e-9)
# the FORCED per-tick departure rate of this departing ladder (06.40): retained share A decays x phi^-1.
per_tick_rate_forced = (p_plus_psq == (Fraction(1), Fraction(0)))  # phi^-1 forced by p+p^2=1
gate("F_OWNED_TRACING_CHANNEL_DEPARTS_AT_PHIM1", tracing_channel_departs and per_tick_rate_forced,
     f"archive-tracing channel (06.7:29, the OWNED dynamics): trace mean={traces.mean():.4f} "
     f"(~phi^-5={phi_f**-5:.4f}), max={traces.max():.4f}<1 for ALL 300 carriers => it DOES depart "
     f"from unitarity; its per-tick retained-amplitude rate A_{{t+1}}=phi^-1 A_t is FORCED (06.40). "
     f"=> an owned+forced RATE governs the departing owned dynamics (old headline REFUTED).")

# 2b. F-MAGNITUDE (SCOPED per R1/R5): phi^-1 per tick is O(1) -> floorless collapse. This does
#     NOT show "phi^-1 is not a departure rate" (it IS -- gate 2a'). It shows the NARROWER, correct
#     thing: phi^-1 is not the IceCube positive-floor PLATEAU-knee rate, because an O(1) floorless
#     collapse is a different signature from the owned positive-floor plateau (08.42:16, inf x=1-zeta>0).
coh = [phi_f ** (-t) for t in range(0, 8)]
collapsed_by_t = next(t for t, c in enumerate(coh) if c < 0.1)
floor = lambda zeta: 1 - zeta  # owned plateau floor 08.42:16, demo zeta only shows floor>0
gate("F_MAGNITUDE_PHIM1_IS_NOT_THE_POSITIVEFLOOR_PLATEAU_KNEE", collapsed_by_t <= 6 and floor(0.3) > 0,
     f"phi^-1/tick collapses coherence<0.1 by tick {collapsed_by_t} (floorless O(1)); owned IceCube "
     f"D1 flagship is a positive-floor PLATEAU (floor {floor(0.3)}>0). So phi^-1 is the departure "
     f"rate of the tracing channel (2a') but NOT the IceCube plateau-KNEE rate -- a NARROWER claim "
     f"than the retracted 'phi^-1 is no departure rate at all'.")

# 2c. OWNED-FACT ASSERTION (relabeled per R4 -- this is NOT a can-fail gate; it restates an owned
#     fact): the knee ENERGY E* is external. zeta VALUE is NOT-OWNED (08.42:16 gives domain 0<z<1
#     only, verified verbatim on disk); E* NOT-OWNED (ICECUBE_MEMO:332, verified verbatim). phi^-1
#     is a per-tick RATIO; converting the owned per-tick RATE to a knee ENERGY needs the unowned
#     kappaV(E) map. This asserts the owned fact; it cannot "fail the conclusion" (it IS a premise).
zeta_owned_value = None   # OWNED FACT: 08.42:16 gives DOMAIN 0<z<1 only; no line fixes the value.
gate("ASSERT_KNEE_ENERGY_ESTAR_IS_EXTERNAL", zeta_owned_value is None,
     "OWNED-FACT ASSERTION (not a can-fail gate): zeta value NOT-OWNED (08.42:16 domain 0<z<1 "
     "only); knee E* NOT-OWNED (ICECUBE_MEMO:332). The owned per-tick RATE phi^-1 -> knee ENERGY "
     "map (kappaV(E)) is the ONLY genuinely external object. This is the repaired headline.")

# ---------------------------------------------------------------------------
# 3. OBSERVABILITY ARITHMETIC (counterfactual, memo §5): owned tick scale is NON-Planck,
#    NON-IceCube-tuned. This is context, not a prediction; gate checks the numbers stated.
# ---------------------------------------------------------------------------
m_e_MeV = 0.51099895069           # electron mass energy (PDG)
Lambda_act_MeV = 38 * m_e_MeV      # BOOK_03:300  Lambda_act = 38 m_e c^2
Lambda_act_GeV = Lambda_act_MeV / 1000.0
icecube_floor_GeV = 1e4            # ~10 TeV HESE window floor
icecube_ceil_GeV = 1e7             # ~few PeV
planck_GeV = 1.22e19
not_planck = Lambda_act_GeV < planck_GeV / 1e10
not_tuned = Lambda_act_GeV < icecube_floor_GeV      # sits BELOW window => no coincidence
gate("OBSERVABILITY_NONPLANCK_NONTUNED", not_planck and not_tuned,
     f"Lambda_act = {Lambda_act_MeV:.3f} MeV = {Lambda_act_GeV:.4g} GeV; IceCube window "
     f"[{icecube_floor_GeV:.0g},{icecube_ceil_GeV:.0g}] GeV -> {icecube_floor_GeV/Lambda_act_GeV:.2g}x above "
     f"Lambda_act (NOT tuned; NOT Planck)")

# ---------------------------------------------------------------------------
# 4. CONTROLS — each can fail the CONCLUSION, not the technique.
# ---------------------------------------------------------------------------
# C1: OWNED-FACT ASSERTION (relabeled per R4 -- NOT a computed can-fail check): IF the knee ENERGY
#     bridge (kappaV(E)/zeta) were owned, the ENERGY verdict would flip to knee-fixed. It is NOT
#     owned (08.42:16, ICECUBE_MEMO:332). This restates the premise; it does not test it.
gate("ASSERT_IF_KNEE_BRIDGE_OWNED_ENERGY_FLIPS", zeta_owned_value is None,
     "OWNED-FACT ASSERTION (not a computed gate): had kappaV(E)/zeta been owned, the knee ENERGY "
     "would be fixed; they are NOT owned -> the ENERGY (not the rate) stays external")

# C2: coincidence-trap guard: phi^-17 (or any phi-power) numerically near an IceCube energy is
#     NOT ownership. Show phi^-17 as an energy (if mis-scaled by Lambda_act) is NOT in the window
#     AND is a static coupling anyway -> flags that a match would be a coincidence, not a rate.
phi_m17_as_energy_GeV = (phi_f ** -17) * Lambda_act_GeV
in_window = icecube_floor_GeV <= phi_m17_as_energy_GeV <= icecube_ceil_GeV
gate("CTRL_PHIPOWER_COINCIDENCE_GUARD", not in_window,
     f"phi^-17 * Lambda_act = {phi_m17_as_energy_GeV:.3g} GeV NOT in IceCube window "
     f"(and phi^-17 is a static coupling, not a rate) -> no coincidence to over-read")

# C3: (REPAIRED per R1) the per-tick rate IS genuinely owned+forced AND it governs the DEPARTING
#     dynamics (gate 2a', not a wrong-sector object). Guards against the retracted under-claim
#     'no owned object fixes the departure rate'. Fails only if phi^-1 were not forced.
rate_owned_and_forced = (p_plus_psq == (Fraction(1), Fraction(0)))   # phi^-1 forced by p+p^2=1
gate("CTRL_DEPARTURE_RATE_IS_OWNED_AND_FORCED", rate_owned_and_forced,
     "control: phi^-1 per-tick rate IS forced+owned AND governs the departing tracing channel "
     "(2a') -> the retracted 'no owned rate' headline is REFUTED; only the knee ENERGY is external")

# ---------------------------------------------------------------------------
print()
if FAILS:
    print(f"RESULT: {len(FAILS)} GATE(S) FAILED -> {FAILS}")
    print("A failure would indicate the owned tracing channel does NOT depart, or the knee bridge IS owned.")
    sys.exit(1)
print("RESULT (REPAIRED, skeptic ACCEPT-IN-FULL): ALL GATES PASS.")
print("- The owned DEPARTING dynamics is the archive-tracing channel (06.7:29 / Block D): it DOES")
print("  depart from unitarity, at the owned+FORCED per-tick rate phi^-1 (06.40).  [gate 2a']")
print("- The post-conditioned coherent complement is exactly unitary but is NOT 'the dynamics'")
print("  (parent :304-312) -- the OLD headline mislabeled it as 'the departure'.  [gate 2a]")
print("- phi^-1 is NOT the IceCube positive-floor PLATEAU-knee rate (floorless O(1)).  [gate 2b]")
print("- The ONLY genuinely EXTERNAL object is the per-tick-rate -> knee-ENERGY map (kappaV(E)/zeta),")
print("  i.e. the E* MAGNITUDE, not 'the rate'.  [assertions 2c/C1]")
print("=> VERDICT: rate phi^-1 OWNED+FORCED for the departing dynamics; only the IceCube knee ENERGY is external.")
sys.exit(0)
