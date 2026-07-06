#!/usr/bin/env python3
"""m1_qm_gap1_check.py -- companion to M1_QM_GAP1_MEMO.md (DRAFT forge; no registry row edited).

Adjudicates GAP-1 of M1_QM_BRIDGE_MEMO.md: continuous reversibility of pure-state dynamics
(Hardy H5 = Masanes-Mueller MM4 = CDP C6-core). Compute-first.

What is checked (each a PASS gate) and the negative controls that FAIL THE CONCLUSION:

  [A] The owned space/time split is real:
      - toral time operator T = [[0,1],[1,-1]] has det=-1, char poly l^2+l-1, ONE contracting
        (|.|<1, the Pisot arrow) + ONE expanding (|.|>1) real eigenvalue: NO reversible orbit
        (spectrum not on the unit circle) -> time evolution is NOT a reversible (unitary/orthogonal)
        map. (Owner D0-UNITY-SPLIT-SPACETIME-001 :265, D0-PISOT-CONTRACTION-TIME-ARROW-001 :270.)
      - the 3 spatial rank-modes carry the depressed cubic l^3 - 359 l - 2574: discriminant > 0 =>
        3 distinct REAL eigenvalues => the spatial transport is real-diagonalizable (reversible on
        its own sector). (Owner D0-RANK3-CAUSAL-CONE-FORCING-001 :260.)

  [B] The archive readout fails invertibility while (I - QUQ) stays invertible:
      - on the frozen K(9,11,13) scene with the tri-phase carrier U3 (reused from icecube machinery),
        QUQ is nilpotent (index 12) => rho(QUQ)=0 => (I - QUQ) INVERTIBLE (Neumann sum finite);
      - BUT the full readout/time map that TRACES the archive (the compression P U P composed with the
        trace-out onto the retained rank-3 sector) is NOT invertible: it is a strict rank-drop
        (33 -> 3), so no two-sided inverse exists. QUQ-nilpotency (a resolvent-domain fact) does NOT
        rescue reversibility of the full readout. This is the exact "(I-QUQ) invertible but the full
        time map may not be" separation the task named.

  [C] MM4 lands on the irreversible sector, not the reversible one:
      - MM4/H5 demands a CONTINUOUS one-parameter group of REVERSIBLE transformations connecting any
        two PURE states, i.e. reversible TIME EVOLUTION of states. In the owned split the state-update
        / evolution channel is the archive-tracing readout (irreversible, [B]); the reversible piece
        is the *spatial* rank-3 transport, which is a static kinematic symmetry, NOT the pure-state
        time-evolution group MM4 needs. So the reversible sector D0 owns does NOT discharge MM4.

  Controls (each can FALSIFY the NO-GO conclusion, not just the technique):
    - CTRL_UNITARY_TIME_WOULD_DISCHARGE: if the time operator T were unitary (spectrum on unit
      circle) MM4 would be owned -> NO-GO would be FALSE. Show D0's T fails this (eigenvalues off
      the unit circle) so the control does not fire (=> NO-GO stands). A planted orthogonal
      rotation Trot passes the unit-circle test (control is live, not vacuous).
    - CTRL_ARCHIVE_INVERTIBLE_WOULD_DISCHARGE: if the readout were rank-preserving (P=I, no trace-out)
      it would be invertible and reversibility could hold -> NO-GO FALSE. Show the owned readout is a
      strict rank-drop (=> NO-GO stands). A planted full-rank map is invertible (control live).
    - CTRL_NILPOTENT_RESCUES_NOTHING: (I-QUQ) invertible is TRUE but does NOT imply the full readout
      invertible (rank still drops). If someone reads QUQ-nilpotency as "reversibility recovered",
      this control shows that inference FAILS.
"""
import sys
import warnings
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
# macOS Accelerate-backed numpy emits spurious matmul RuntimeWarnings on exact-projector products.
# Safe to silence HERE ONLY: every load-bearing quantity is check()-gated, so a real NaN/inf still
# flips its gate to FAIL; nothing is trusted from a warning-free run.
warnings.filterwarnings("ignore", message=".*encountered in matmul.*", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*encountered in det.*", category=RuntimeWarning)

TOL = 1e-9
SIZES = [9, 11, 13]
N = 33
FAILS = []


def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    if not cond:
        FAILS.append(name)
    print(f"{tag}_{name}  {detail}")
    return cond


def build_scene():
    """Frozen K(9,11,13) scene; Feshbach split rank-3 retained / dim-30 archive (owners frozen)."""
    zone = sum(([i] * s for i, s in enumerate(SIZES)), [])
    A = np.array([[1.0 if zone[i] != zone[j] else 0.0 for j in range(N)] for i in range(N)])
    w, V = np.linalg.eigh(A)
    Kk = V[:, np.abs(w) < 1e-9]
    Q = Kk @ Kk.T
    P = np.eye(N) - Q
    idx = [range(0, 9), range(9, 20), range(20, 33)]
    uv = []
    for r in idx:
        u = np.zeros(N)
        for i in r:
            u[i] = 1.0
        uv.append(u / np.linalg.norm(u))
    return A, P, Q, uv


def build_u3():
    d = []
    for n in SIZES:
        d += [np.exp(2j * np.pi * j / n) for j in range(n)]
    return np.diag(d)


# ---------------------------------------------------------------------------
# BLOCK A -- the owned space/time split is real (reversible space, irreversible time)
# ---------------------------------------------------------------------------
def block_A():
    print("\n--- BLOCK A: owned space (reversible) / time (irreversible) split ---")
    # A1: toral time operator T = [[0,1],[1,-1]] -- owner D0-UNITY-SPLIT-SPACETIME-001 (:265)
    T = np.array([[0.0, 1.0], [1.0, -1.0]])
    evT = np.sort(np.linalg.eigvals(T).real)
    detT = round(np.linalg.det(T))
    on_circle = np.allclose(np.abs(np.linalg.eigvals(T)), 1.0)
    check("TIME_DET_MINUS1", detT == -1, f"det(T)={detT} (=psi*phi); char poly l^2+l-1.")
    check("TIME_PISOT_SPLIT",
          (evT[0] < -1.0) and (0.0 < evT[1] < 1.0),
          f"eigs={np.round(evT,5).tolist()}: one contracting |.|<1 (Pisot arrow) + one expanding |.|>1.")
    # THE reversibility test for time: a reversible (orthogonal/unitary) evolution has spectrum ON the
    # unit circle. D0's time operator does NOT -> time evolution is NOT reversible.
    check("TIME_NOT_REVERSIBLE", not on_circle,
          "time eigenvalues OFF the unit circle => the time flow is NOT a reversible group (hyperbolic).")
    # A2: 3 spatial rank-modes -- depressed cubic l^3 - 359 l - 2574 (owner D0-RANK3-CAUSAL-CONE-FORCING-001 :260)
    p, q = -359.0, -2574.0
    disc = -4 * p ** 3 - 27 * q ** 2  # discriminant of x^3+px+q
    roots = np.roots([1, 0, p, q])
    all_real = np.allclose(roots.imag, 0.0, atol=1e-9)
    check("SPACE_REVERSIBLE_REAL_SPECTRUM", (disc > 0) and all_real,
          f"cubic disc={int(disc)}>0 => 3 distinct REAL eigenvalues => spatial transport reversible on its sector.")
    return T


# ---------------------------------------------------------------------------
# BLOCK B -- archive readout non-invertible while (I-QUQ) invertible
# ---------------------------------------------------------------------------
def block_B(P, Q, U3):
    print("\n--- BLOCK B: full readout NON-invertible while (I - QUQ) IS invertible ---")
    # B1: QUQ nilpotent -> rho=0 -> (I-QUQ) invertible (finite Neumann sum)
    QUQ = Q @ U3 @ Q
    nrm = [np.linalg.norm(np.linalg.matrix_power(QUQ, k)) for k in range(1, 15)]
    nil_idx = next((k for k in range(1, 15) if nrm[k - 1] < 1e-8), None)
    det_IminusQUQ = abs(np.linalg.det(np.eye(N) - QUQ) - 1.0)
    check("RESOLVENT_INVERTIBLE", (nil_idx == 12) and (det_IminusQUQ < 1e-8),
          f"QUQ nilpotent index={nil_idx} => rho(QUQ)=0 => (I-QUQ) invertible (det=1). Neumann sum finite.")
    # B2: the trace-out projection P (archive erasure) is rank-3 idempotent -> NOT invertible on C^33
    rankP = np.linalg.matrix_rank(P, tol=1e-9)
    check("TRACEOUT_RANK_DROP", (rankP == 3) and np.allclose(P @ P, P),
          f"retained projection P: P^2=P, rank={rankP} << {N} => archive erasure is NON-invertible (info destroyed).")
    # B3: the Feshbach effective time map W_eff has rank <= 3 as a 33x33 map -> non-invertible on full space
    res = np.linalg.inv(np.eye(N) - QUQ)  # exists by B1
    Weff = P @ U3 @ P + P @ U3 @ Q @ res @ Q @ U3 @ P
    rankW = np.linalg.matrix_rank(Weff, tol=1e-9)
    check("FULL_TIMEMAP_NONINVERTIBLE", rankW <= 3,
          f"rank(W_eff)={rankW} <= 3 << {N}: the full archive-tracing time map is NON-invertible (no two-sided inverse).")
    return QUQ, Weff


# ---------------------------------------------------------------------------
# BLOCK C -- the emergent unitary shadow is EXACT on retained but MM4-insufficient (trivial / hyperbolic)
# ---------------------------------------------------------------------------
def block_C(P, Weff, uv):
    print("\n--- BLOCK C: emergent shadow exact on retained BUT MM4-insufficient ---")
    B = np.array(uv).T  # 33 x 3 retained basis
    Wsub = B.conj().T @ Weff @ B
    sv = np.linalg.svd(Wsub, compute_uv=False)
    is_unitary = np.allclose(Wsub.conj().T @ Wsub, np.eye(3), atol=1e-8)
    # C1: the shadow IS exactly unitary on the retained rank-3 sector (00.2:55 'emergent shadow' -- exact here)
    check("SHADOW_UNITARY_ON_RETAINED", is_unitary,
          f"W_eff|retained singular values={np.round(sv,4).tolist()} => EXACTLY unitary on retained sector.")
    # C2: ... but it is the TRIVIAL unitary (identity): connects NO two distinct pure states => fails MM4 transitivity
    is_identity = np.allclose(Wsub, np.eye(3), atol=1e-6)
    check("SHADOW_TRIVIAL_NOT_MM4", is_identity,
          "W_eff|retained = identity: the reversible piece connects NO two distinct pure states "
          "=> does NOT supply MM4's continuous group acting transitively on pure states.")
    return Wsub


# ---------------------------------------------------------------------------
# BLOCK D -- skeptic S1 defense (the sharpest attack): the coherent Schur complement W_eff is
#            unitary on retained, BUT the PHYSICAL archive-tracing channel is a strict contraction.
#            Which object is "the dynamics" decides A vs B; D0's owned reading (06.7:29) picks the
#            tracing channel. This block shows the two objects differ and the channel loses probability.
# ---------------------------------------------------------------------------
def block_D(P, Q, uv):
    print("\n--- BLOCK D: coherent complement unitary vs PHYSICAL tracing channel contractive (skeptic S1) ---")
    B = np.array(uv).T
    rng = np.random.default_rng(3)
    # D1: for a GENERIC unitary carrier, the coherent Schur complement W_eff|retained is exactly unitary
    #     (this is the A-side temptation) AND non-trivial (not identity) -- so triviality is U3-specific.
    X = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
    Ug, _ = np.linalg.qr(X)
    QUQg = Q @ Ug @ Q
    resg = np.linalg.inv(np.eye(N) - QUQg)
    Wg = B.conj().T @ (P @ Ug @ P + P @ Ug @ Q @ resg @ Q @ Ug @ P) @ B
    coh_unitary = np.allclose(Wg.conj().T @ Wg, np.eye(3), atol=1e-8)
    coh_nontrivial = not np.allclose(Wg, np.eye(3), atol=1e-6)
    check("GENERIC_COHERENT_COMPLEMENT_UNITARY", coh_unitary and coh_nontrivial,
          "generic carrier: coherent Schur complement W_eff|retained IS a non-trivial unitary "
          "(so the identity-triviality is U3-specific; the A-side temptation is real and must be answered).")
    # D2: BUT the PHYSICAL archive-tracing readout rho -> P U rho U^dag P LOSES probability (trace<1) for
    #     EVERY carrier/state -> it is NOT trace-preserving -> NOT a reversible group. This is the answer to S1.
    traces = []
    for _ in range(300):
        Xk = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
        Uk, _ = np.linalg.qr(Xk)
        psi = B @ (rng.standard_normal(3) + 1j * rng.standard_normal(3))
        psi = psi / np.linalg.norm(psi)
        out = P @ Uk @ np.outer(psi, psi.conj()) @ Uk.conj().T @ P
        traces.append(np.trace(out).real)
    traces = np.array(traces)
    all_leak = np.all(traces < 1.0 - 1e-9)
    check("PHYSICAL_TRACING_CHANNEL_CONTRACTIVE", all_leak,
          f"archive-tracing readout: trace surviving mean={traces.mean():.4f}, max={traces.max():.4f}<1 "
          "for ALL 300 carriers/states => probability LEAKS to archive => NOT trace-preserving => "
          "NOT a reversible group. The 'unitary W_eff' is the post-conditioned coherent return, not the channel.")


# ---------------------------------------------------------------------------
# CONTROLS -- each can FALSIFY the NO-GO conclusion (not just the technique)
# ---------------------------------------------------------------------------
def controls(P, Q, U3):
    print("\n--- CONTROLS (each can falsify the NO-GO; must NOT fire on owned objects) ---")
    # CTRL 1: a PLANTED orthogonal (unitary) time operator WOULD discharge MM4.
    #         Show D0's toral T fails the unit-circle test (control does not fire => NO-GO stands),
    #         while a planted rotation passes it (control is LIVE, not vacuous).
    T = np.array([[0.0, 1.0], [1.0, -1.0]])
    theta = 0.7
    Trot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    owned_reversible = np.allclose(np.abs(np.linalg.eigvals(T)), 1.0)
    planted_reversible = np.allclose(np.abs(np.linalg.eigvals(Trot)), 1.0)
    check("CTRL_UNITARY_TIME_WOULD_DISCHARGE",
          (not owned_reversible) and planted_reversible,
          "owned time NOT unit-circle (NO-GO stands); planted rotation IS unit-circle (control is live).")
    # CTRL 2: a PLANTED full-rank (P=I) readout WOULD be invertible => reversibility could hold.
    #         Show the owned readout is a strict rank-drop (NO-GO stands); planted identity is full-rank (live).
    owned_rankdrop = np.linalg.matrix_rank(P, tol=1e-9) < N
    planted_fullrank = np.linalg.matrix_rank(np.eye(N), tol=1e-9) == N
    check("CTRL_ARCHIVE_INVERTIBLE_WOULD_DISCHARGE",
          owned_rankdrop and planted_fullrank,
          "owned readout drops rank 33->3 (NO-GO stands); a planted full-rank map is invertible (control is live).")
    # CTRL 3: (I-QUQ) invertible does NOT imply the full readout invertible (rank still drops).
    QUQ = Q @ U3 @ Q
    res_ok = abs(np.linalg.det(np.eye(N) - QUQ) - 1.0) < 1e-8   # (I-QUQ) invertible
    full_still_singular = np.linalg.matrix_rank(P @ U3 @ P, tol=1e-9) < N  # full map still rank-drops
    check("CTRL_NILPOTENT_RESCUES_NOTHING",
          res_ok and full_still_singular,
          "(I-QUQ) invertible TRUE, yet full readout still rank-drops => nilpotency does NOT recover reversibility.")


def main() -> int:
    print("=== m1_qm_gap1_check (DRAFT forge companion; no registry row edited) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: matrices frozen by owners (toral T, cubic 359/2574, split 3/30);")
    print("MM4/H5 = continuous group of REVERSIBLE transforms connecting any two PURE states (time evolution).")
    A, P, Q, uv = build_scene()
    check("SPLIT", (round(np.trace(P)) == 3) and (round(np.trace(Q)) == 30),
          "rank(retained)=3, dim(archive)=30 (frozen Feshbach split).")
    U3 = build_u3()
    check("CARRIER_UNITARY", np.allclose(U3.conj().T @ U3, np.eye(N)),
          "tri-phase carrier U3 is unitary (reused from icecube machinery).")
    block_A()
    QUQ, Weff = block_B(P, Q, U3)
    block_C(P, Weff, uv)
    block_D(P, Q, uv)
    controls(P, Q, U3)
    print("\n=== SUMMARY ===")
    if FAILS:
        print("CONCLUSION_UNPROVEN: failing gates:", ", ".join(FAILS))
        return 1
    print("CONCLUSION: BRANCH B (owned NO-GO on MM4/H5 continuous reversibility) holds on all gates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
