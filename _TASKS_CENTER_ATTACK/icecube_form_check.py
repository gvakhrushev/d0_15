#!/usr/bin/env python3
"""icecube_form_check v2 - companion for ICECUBE_DECOHERENCE_FORM_MEMO.md (DRAFT, candidate;
post-skeptic-#1 repairs applied, all accepted in full).

Computes the CANDIDATE neutrino phason-decoherence envelope FORM from the two owned internal
objects (no IceCube number enters any construction step):

  (i)  the BOOK_08 §08.42 log-det loop-pressure map  P(V) = -ln(1 - zeta*r(V)),
       r(V) = 1 - exp(-kappa V)  (positive, bounded, saturating on 0 < zeta < 1), and
  (ii) the tri-phase tick carrier U3 = diag(mu9; mu11; mu13) on the frozen Feshbach split
       P = proj(range A_scene) (rank 3), Q = proj(ker A_scene) (dim 30), whose archive block
       QUQ is NILPOTENT with per-zone indices (8, 10, 12)  (TICK_COUPLING_SCHUR_MEMO.md).

Everything load-bearing is COMPUTED from the constructed matrices, never assumed:
the single-path ladder theorem (exactly one nonzero Neumann rung per zone, at maximal depth),
the monomial envelope D_n(x) = |x|^(n-1), the geometric-mean law, the plateau, and the
Lindblad-tail discriminator (both bridges, per-bridge numbers printed).

v2 repairs (skeptic #1): (R1) the open-path Schur reading is a SELECTION, not forced -- the
OWNED full-loop object F_N = P U^dag Q U P (D0-CVFT-001A, CLAIM_TO_LEAN_MAP.csv row 130) is
ALIVE on U3: det(I - z F_N) = (1-z)^3 != 1, yielding a RIVAL envelope with uniform depth 3
(same D1 plateau, NO zone splitting) -- now computed in [3c]; (R2) the A1 sub-claim "D1
survives ANY bounded monotone marriage" was KILLED -- counterexample x = e^{-kappa V} gives
exactly Lindblad m=1, computed in control C5; D1's survival class = positive-floor marriages
(inf x = 1 - zeta > 0); (R3) Lindblad tail split now run on BOTH bridges with actual numbers;
(R4) off-by-one in the ladder-bound print fixed; (R5) the zeta x bridge independence grid is
now the FULL product {0.05, 0.3, 0.6} x {b=1, b=1/2}.

Negative controls can fail the CONCLUSION (repeated-phase carrier destroys nilpotency;
equivariant carrier gives NO envelope; free-ratio exponents violate the GM law; the calibrated
Lindblad curve fails the plateau gate; the floorless marriage kills D1 itself).

NOT a minted cert. No registry row edited. DEMO constants (zeta, E_star, L/L0) are flagged
NOT-OWNED and only illustrate the form; every independence claim is checked on the stated grid.
"""
import sys
import warnings

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
# macOS Accelerate-backed numpy emits spurious "... encountered in matmul" RuntimeWarnings on
# exact-projector products. Safe to silence HERE ONLY because every load-bearing quantity below
# is assert-gated (a real NaN/inf fails its assert; nothing is trusted from a warning-free run).
warnings.filterwarnings("ignore", message=".*encountered in matmul.*", category=RuntimeWarning)
TOL = 1e-10
SIZES = [9, 11, 13]
N = 33


def build_scene():
    """K(9,11,13) scene, frozen Feshbach split (owners: rank-3 retained / dim-30 archive)."""
    zone = sum(([i] * s for i, s in enumerate(SIZES)), [])
    A = np.array([[1.0 if zone[i] != zone[j] else 0.0 for j in range(N)] for i in range(N)])
    w, V = np.linalg.eigh(A)
    K = V[:, np.abs(w) < 1e-9]
    Q = K @ K.T
    P = np.eye(N) - Q
    assert round(np.trace(P)) == 3 and round(np.trace(Q)) == 30
    idx = [range(0, 9), range(9, 20), range(20, 33)]
    U = []  # per-zone uniform unit vectors (basis of the rank-3 retained sector)
    for r in idx:
        u = np.zeros(N)
        for i in r:
            u[i] = 1.0
        U.append(u / np.linalg.norm(u))
    return A, P, Q, idx, U


def build_u3():
    d = []
    for n in SIZES:
        d += [np.exp(2j * np.pi * j / n) for j in range(n)]
    return np.diag(d)


def ladder_coefficients(U3, P, Q, uvecs):
    """Per zone n: direct term p_n = <u|PUP|u> and Neumann rungs t_k = <u|PUQ (QUQ)^k QUP|u>.
    Computed by raw matrix powers -- the sparsity pattern is an OUTPUT, not an input."""
    QUQ = Q @ U3 @ Q
    PUQ = P @ U3 @ Q
    QUP = Q @ U3 @ P
    out = []
    for n, u in zip(SIZES, uvecs):
        p_direct = complex(u @ (P @ U3 @ P) @ u)
        rungs = []
        M = np.eye(N, dtype=complex)
        for k in range(n):  # k = 0..n-1 (one past the last possibly-nonzero rung)
            rungs.append(complex(u @ (PUQ @ M @ QUP) @ u))
            M = M @ QUQ
        out.append((n, p_direct, rungs))
    return out, QUQ, PUQ, QUP


def envelope_from_rungs(rungs, p_direct, x):
    """CONV-1: weight x per archive-resident U-step => rung k carries x^(k+1); direct term x^0."""
    w = p_direct + sum(t * x ** (k + 1) for k, t in enumerate(rungs))
    return abs(w)


def main() -> int:
    print("=== icecube_form_check v2 (DRAFT companion; no registry row edited; post-skeptic-#1) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: split=(range A, ker A) frozen by owners (3/30);")
    print("carrier=U3 tri-phase (TICK_COUPLING_SCHUR_MEMO candidate); pressure map = BOOK_08 08.42;")
    print("no IceCube number is used in any construction step below.")

    A, P, Q, idx, uvecs = build_scene()
    print("PASS_SPLIT  rank(retained)=3, dim(archive)=30.")

    # [2] carrier: unitarity + per-zone nilpotency indices EXACTLY (8, 10, 12)
    U3 = build_u3()
    assert np.allclose(U3.conj().T @ U3, np.eye(N))
    QUQ = Q @ U3 @ Q
    for zi, (n, r) in enumerate(zip(SIZES, idx)):
        sub = QUQ[np.ix_(list(r), list(r))]
        M_idx = np.linalg.matrix_power(sub, n - 1)
        M_pre = np.linalg.matrix_power(sub, n - 2)
        assert np.linalg.norm(M_idx) < 1e-8, f"zone {n}: (QUQ)^{n-1} != 0"
        assert np.linalg.norm(M_pre) > 1e-6, f"zone {n}: (QUQ)^{n-2} == 0 (index too small)"
    assert np.linalg.norm(np.linalg.matrix_power(QUQ, 12)) < 1e-8
    print("PASS_NILPOTENT_LADDER  per-zone nilpotency indices exactly (8,10,12); global (QUQ)^12=0.")
    print("  => the Neumann ladder P U Q (QUQ)^k Q U P terminates: nonzero rungs bounded by")
    print("     k <= n-2 = (7,9,11) per zone; <= 11 globally (finite, convergence-free).")

    # [3] ladder coefficients: computed, not assumed
    coeffs, QUQ, PUQ, QUP = ladder_coefficients(U3, P, Q, uvecs)
    ladder_sum = np.zeros((N, N), dtype=complex)
    M = np.eye(N, dtype=complex)
    for k in range(12):
        ladder_sum = ladder_sum + PUQ @ M @ QUP
        M = M @ QUQ
    frob = np.linalg.norm(ladder_sum)
    assert abs(frob - np.sqrt(3)) < 1e-9, f"ladder-sum Frobenius {frob} != sqrt(3)"
    print(f"PASS_LADDER_SUM_CROSSCHECK  ||sum_k PUQ(QUQ)^k QUP||_F = {frob:.12f} = sqrt(3) (skeptic #2 value).")

    exponents_conv1 = []
    for n, p_direct, rungs in coeffs:
        assert abs(p_direct) < TOL, f"zone {n}: direct channel PUP != 0 ({p_direct})"
        nz = [k for k, t in enumerate(rungs) if abs(t) > TOL]
        assert nz == [n - 2], f"zone {n}: nonzero rungs at {nz}, expected single rung k={n - 2}"
        assert abs(abs(rungs[n - 2]) - 1.0) < TOL, f"zone {n}: |t_(n-2)| = {abs(rungs[n-2])} != 1"
        exponents_conv1.append((n - 2) + 1)  # CONV-1 weight: rung k carries x^(k+1)
        print(f"PASS_SINGLE_PATH  zone {n}: PUP=0 exactly; unique nonzero rung k={n - 2} with |t|=1;")
        print(f"                  retained amplitude w_{n}(x) = t * x^{n - 1} (pure monomial, computed).")
    assert exponents_conv1 == [8, 10, 12]
    print("PASS_EXPONENT_TRIPLE  CONV-1 exponents (8,10,12); CONV-1' (per-circulation) gives (7,9,11);")
    print("  arithmetic-progression gap = 2 under BOTH conventions (convention-robust).")

    # [3b] closed-loop control on the ARCHIVE BLOCK: det(I - x QUQ) == 1 identically.
    for x in (0.3, 0.7, 0.99):
        det = np.linalg.det(np.eye(N) - x * QUQ)
        assert abs(det - 1.0) < 1e-8, f"det(I - {x} QUQ) = {det} != 1"
    print("CONTROL_ARCHIVE_BLOCK_LOOP_EMPTY  det(I - x*QUQ) = 1 exactly: the closed-loop log-det")
    print("  pressure vanishes on the nilpotent archive block ITSELF. This kills only the")
    print("  QUQ-closed-loop reading -- NOT every loop reading (see [3c]); the open-path Schur")
    print("  ladder used above is therefore a SELECTION among live readings, not forced (v2 repair R1).")

    # [3c] RIVAL OWNED ROUTE (skeptic #1 strongest finding, adopted): the owned full-loop
    # feedback object F_N = P U^dag Q U P (D0-CVFT-001A, row 130) is ALIVE on U3.
    FN = P @ U3.conj().T @ Q @ U3 @ P
    assert np.linalg.norm(FN - P) < 1e-9, "F_N != P on the retained sector"
    for z in (0.3, 0.7, 0.99):
        detF = np.linalg.det(np.eye(N) - z * FN)
        assert abs(detF - (1.0 - z) ** 3) < 1e-8, f"det(I - {z} F_N) = {detF} != (1-z)^3"
    print("RIVAL_ROUTE_ALIVE_FN  F_N = P U^dag Q U P equals P on U3 (each zone: ||Q U u_n||^2 = 1");
    print("  since PUP = 0); det(I - z F_N) = (1-z)^3 != 1 (computed). The owned log-det pressure")
    print("  route (D0-CVFT-001A + 08.42) therefore yields a RIVAL envelope on the SAME carrier:")
    print("    -ln D = 3 * (L/L0) * P0842(E)   (uniform depth 3; NO zone splitting; no 8:10:12;")
    print("  GM law degenerate; SAME bounded/saturating D1 plateau). Better ownership pedigree")
    print("  than the open-path reading; P2/P3/P4/D2/D3 below are READING-CONDITIONAL.")

    # [4] envelope structure D_n(x) = |x|^(n-1): from computed rungs, checked against monomial
    xs = np.linspace(0.0, 1.0, 21)
    for (n, p_direct, rungs) in coeffs:
        for x in xs:
            d_computed = envelope_from_rungs(rungs, p_direct, x)
            assert abs(d_computed - x ** (n - 1)) < 1e-9
    print("PASS_MONOMIAL_ENVELOPE  D_n(x) = |x|^(n-1) on [0,1] from the computed rungs (n=9,11,13).")

    # [5] candidate physical form via BR-1 bridge (DEMO constants; flagged NOT-OWNED):
    #     x(E) = 1 - zeta*r(V(E)), r = 1 - exp(-kappa V), kappa V = (E/E_star)^b  (b=1 and b=1/2)
    #     => -ln D_n(E, L) = N_n * (L/L0) * [-ln(1 - zeta*r(V(E)))]  =  N_n * (L/L0) * P_0842(E)
    zeta_demo = 0.3       # NOT-OWNED demo loop coupling (0<zeta<1 owned as a DOMAIN, not a value)
    Egrid = np.logspace(-2, 3, 401)  # in units of E_star (E_star NOT OWNED)
    for bridge_pow, bridge_name in ((1.0, "kappaV=E/E*"), (0.5, "kappaV=sqrt(E/E*)")):
        r = 1.0 - np.exp(-(Egrid ** bridge_pow))
        x = 1.0 - zeta_demo * r
        lnD = {n: (n - 1) * np.log(x) for n in SIZES}
        # plateau: -ln D -> (n-1)*(-ln(1-zeta)) as E -> inf (bounded energy damping)
        plateau = {n: (n - 1) * (-np.log1p(-zeta_demo)) for n in SIZES}
        for n in SIZES:
            assert abs(-lnD[n][-1] - plateau[n]) < 1e-3 * plateau[n]
            assert np.all(np.diff(-lnD[n]) >= -1e-12)  # monotone deepening, then flat
        # geometric-mean law (per-baseline): D_11^2 = D_9 * D_13 at EVERY energy
        gm_dev = np.max(np.abs(2 * lnD[11] - (lnD[9] + lnD[13])))
        assert gm_dev < 1e-12, f"GM law violated: {gm_dev}"
        # fixed log-damping ratios 8:10:12 at every energy (bridge- and zeta-independent)
        mask = -lnD[9] > 1e-12
        ratios = lnD[13][mask] / lnD[9][mask]
        assert np.max(np.abs(ratios - 12.0 / 8.0)) < 1e-9
        print(f"PASS_FORM_PROPERTIES[{bridge_name}]  plateau=(n-1)*(-ln(1-zeta)) reached; GM law "
              f"max|2lnD11-(lnD9+lnD13)|={gm_dev:.1e}; lnD13/lnD9 = 3/2 exactly on the whole grid.")

    # zeta x bridge independence: FULL product grid (v2 repair R5 -- scope now exactly as run)
    for z2 in (0.05, 0.3, 0.6):
        for bp in (1.0, 0.5):
            r = 1.0 - np.exp(-(Egrid ** bp))
            x = 1.0 - z2 * r
            lnD = {n: (n - 1) * np.log(x) for n in SIZES}
            assert np.max(np.abs(2 * lnD[11] - (lnD[9] + lnD[13]))) < 1e-12
            mask = -lnD[9] > 1e-12
            assert np.max(np.abs(lnD[13][mask] / lnD[9][mask] - 1.5)) < 1e-9
    print("PASS_DEMO_INDEPENDENCE  GM law and 8:10:12 ratios hold on the FULL grid")
    print("  zeta in {0.05, 0.3, 0.6} x bridge in {E/E*, sqrt(E/E*)} (6/6 combinations run).")

    # [5b] ensemble (baseline-averaged) version: GM equality degrades to a ONE-SIDED
    # Cauchy-Schwarz inequality  <D_11>^2 <= <D_9><D_13>, strict for non-degenerate L.
    rng = np.random.default_rng(20260704)
    Ls = np.exp(rng.normal(0.0, 0.7, size=2000))  # toy non-degenerate baseline distribution
    xE = 1.0 - zeta_demo * (1.0 - np.exp(-1.0))   # fixed evaluation energy E = E_star
    Dbar = {n: np.mean(xE ** ((n - 1) * Ls)) for n in SIZES}
    assert Dbar[11] ** 2 < Dbar[9] * Dbar[13]
    print("PASS_ENSEMBLE_CS  baseline-averaged: <D11>^2 < <D9><D13> (strict CS inequality; the GM")
    print("  EQUALITY is per-baseline only -- pre-registered limitation, not a surprise).")

    # [6] discriminator vs standard Lindblad exp-damping, calibrated to agree at low E.
    # Lindblad: -ln D_L = (E/E0)^m * (L/L0); calibrate (m, E0) on the LOW window to the D0 zone-13
    # curve, then compare tails. v2 repair R3: run on BOTH bridges, print per-bridge numbers.
    tail_results = {}
    for bridge_pow, bridge_name in ((1.0, "kappaV=E/E*"), (0.5, "kappaV=sqrt(E/E*)")):
        r = 1.0 - np.exp(-(Egrid ** bridge_pow))
        x = 1.0 - zeta_demo * r
        g13 = -12.0 * np.log(x)                      # D0: -ln D_13(E)
        low = (Egrid >= 0.01) & (Egrid <= 0.33)      # calibration window: E << E_star (knee)
        m_fit, c_fit = np.polyfit(np.log(Egrid[low]), np.log(g13[low]), 1)
        gL = np.exp(c_fit) * Egrid ** m_fit          # calibrated Lindblad -ln D
        cal_dev = np.max(np.abs(gL[low] / g13[low] - 1.0))
        assert cal_dev < 0.15, f"[{bridge_name}] calibration mismatch {cal_dev}"
        sep = np.abs(np.log(gL / g13))
        i_sep = int(np.argmax(sep > np.log(2.0)))
        assert i_sep > 0, f"[{bridge_name}] no separation found"
        E_sep = Egrid[i_sep]
        D0_tail = np.exp(-g13[-1])
        L_tail = np.exp(-gL[-1])
        assert D0_tail > 0.01 and L_tail < 1e-6
        print(f"PASS_LINDBLAD_TAIL_SPLIT[{bridge_name}]  calibrated m={m_fit:.3f}, tracks D0 <15% below")
        print(f"  the knee; log-dampings differ 2x by E = {E_sep:.2f} E*; at E = 1000 E*: D0 damping =")
        print(f"  {D0_tail:.4f} (PLATEAU, -lnD = {g13[-1]:.2f}), Lindblad damping = {L_tail:.2e}"
              f" (-lnD = {gL[-1]:.1f}).")
        tail_results[bridge_pow] = (g13, gL, m_fit)
    g13, gL, m_fit = tail_results[1.0]               # b=1 numbers for the bin-ratio gates below
    # bin-ratio statistic (shape-only, exposure-free): rho(E) = lnD(2E)/lnD(E)
    for Eprobe, regime in ((0.02, "below knee"), (50.0, "above knee")):
        i1 = int(np.argmin(np.abs(Egrid - Eprobe)))
        i2 = int(np.argmin(np.abs(Egrid - 2 * Eprobe)))
        rho_d0 = g13[i2] / g13[i1]
        rho_L = gL[i2] / gL[i1]
        print(f"  bin-ratio rho(E)=lnD(2E)/lnD(E) at {regime} [b=1]: D0 {rho_d0:.3f} vs Lindblad {rho_L:.3f}")
    i1 = int(np.argmin(np.abs(Egrid - 50.0)))
    i2 = int(np.argmin(np.abs(Egrid - 100.0)))
    assert abs(g13[i2] / g13[i1] - 1.0) < 0.02          # D0: ratio -> 1 above knee
    assert abs(gL[i2] / gL[i1] - 2.0 ** m_fit) < 0.02   # Lindblad: ratio -> 2^m != 1
    print("PASS_BIN_RATIO_DISCRIMINATOR  above the knee: D0 ratio -> 1 (flat), Lindblad -> 2^m (falling).")

    # [7] negative controls -- each can fail the CONCLUSION.
    # C1: single repeated phase (zone 13) destroys nilpotency => finite-ladder premise fails.
    d_bad = []
    for n in SIZES:
        col = [np.exp(2j * np.pi * j / n) for j in range(n)]
        d_bad += col
    d_bad[20 + 12] = d_bad[20 + 0]  # duplicate one phase inside zone 13
    U_bad = np.diag(d_bad)
    QUQ_bad = Q @ U_bad @ Q
    rho_bad = max(abs(np.linalg.eigvals(QUQ_bad)))
    assert rho_bad > 0.9, f"repeated-phase carrier still near-nilpotent (rho={rho_bad})"
    print(f"CONTROL_REPEATED_PHASE_KILLS_LADDER  one duplicated phase: rho(QUQ) = {rho_bad:.3f} (not")
    print("  nilpotent; infinite ladder; NO finite-monomial form). Full phase lattice is load-bearing.")
    # C2: equivariant carrier => coupling zero => NO envelope at all (form vacuous there).
    U_eq = np.zeros((N, N))
    for r_ in idx:
        for i in r_:
            for j in r_:
                U_eq[i, j] = 1.0 / len(list(r_))
    assert np.linalg.norm(P @ U_eq @ Q) < TOL
    print("CONTROL_EQUIVARIANT_VACUOUS  equivariant carrier: PUQ = 0, no ladder, no envelope --")
    print("  the form REQUIRES the within-zone symmetry-broken carrier (carrier-selection dependency).")
    # C3: a free-ratio exponent triple violates the GM law (the GM gate can fail).
    lnx = np.log(1.0 - zeta_demo * (1.0 - np.exp(-Egrid)))
    lnD_free = {9: 8.0 * lnx, 11: 10.7 * lnx, 13: 12.9 * lnx}
    gm_free = np.max(np.abs(2 * lnD_free[11] - (lnD_free[9] + lnD_free[13])))
    assert gm_free > 1e-3, "free-ratio triple slipped through the GM gate"
    print(f"CONTROL_GM_GATE_CAN_FAIL  exponents (8,10.7,12.9): GM deviation {gm_free:.2f} >> 0 -- flagged.")
    # C4: the calibrated Lindblad curve fails the plateau gate.
    assert gL[-1] / gL[i1] > 5.0
    print("CONTROL_PLATEAU_GATE_CAN_FAIL  calibrated Lindblad keeps deepening above the knee -- flagged.")
    # C5 (v2 repair R2, skeptic counterexample adopted): a FLOORLESS marriage kills D1 itself.
    # Marriage x = e^{-kappa V} with kappaV = E/E*: -lnD_13 = 12*(E/E*) == Lindblad m=1 exactly.
    # (Grid capped at E = 500 E*: exp(-E) underflows to 0.0 beyond ~708, log(0) = -inf.)
    Efl = Egrid[Egrid <= 500.0]
    g_fl = -12.0 * np.log(np.exp(-Efl))              # = 12*Efl, computed via the marriage itself
    m_fl = np.polyfit(np.log(Efl), np.log(g_fl), 1)[0]
    assert abs(m_fl - 1.0) < 1e-9, f"floorless marriage slope {m_fl} != 1"
    assert g_fl[-1] / g_fl[i1] > 5.0                  # no plateau: keeps deepening above E*
    print(f"CONTROL_FLOORLESS_MARRIAGE_KILLS_D1  x = e^(-kappa V), kappaV = E/E*: -lnD = 12*(E/E*),")
    print(f"  log-log slope = {m_fl:.6f} == Lindblad m=1 EXACTLY; no plateau. D1 is NOT marriage-free:")
    print("  its survival class is marriages with a strictly positive retention floor")
    print("  (inf x = 1 - zeta > 0, inherited from the 08.42 resolvent factor). The v1 sub-claim")
    print("  'survives ANY bounded monotone marriage' was KILLED (accepted; error of record).")

    # [8] summary
    print()
    print("CANDIDATE_FORM (READING-CONDITIONAL)  -ln D_n(E, L) = N_n * (L/L0) * P0842(E),")
    print("  N_n in {8,10,12} (CONV-1; {7,9,11} under CONV-1'),  P0842(E) = -ln(1 - zeta*(1 -")
    print("  exp(-kappa V(E)))) = the owned BOOK_08 08.42 log-det loop pressure on the bridge V(E).")
    print("  OPEN-PATH Schur reading = a SELECTION; rival OWNED F_N route (D0-CVFT-001A) on the")
    print("  same carrier gives -ln D = 3*(L/L0)*P0842(E): uniform depth, same D1, no zone split.")
    print("DISCRIMINATORS  D1 bounded energy-damping (plateau; bin-ratio -> 1) vs Lindblad unbounded")
    print("  -- READING-ROBUST (shared by both live readings) within the positive-floor marriage")
    print("  class; the honest flagship. D2 GM law D11^2 = D9*D13 per baseline (CS inequality after")
    print("  ensemble averaging) and D3 integer triple 8:10:12 = 4:5:6 (AP gap 2 convention-robust)")
    print("  -- READING-CONDITIONAL (open-path only; absent on the F_N route).")
    print("NAMED_GAPS  G1 the composite bridge kappaV(E) + the CONV-2 marriage NOT owned (BR-1")
    print("  declared; kappa = log phi itself IS owned, D0-IM-COSMO-003 row 160); G2 carrier")
    print("  identification (neutrino phason kernel = tick archive ladder) NOT owned; G2' reading")
    print("  selection (open-path vs owned F_N loop) NOT adjudicated; G3 U3 pedigree gaps inherited")
    print("  (S1' staticity, S2 phase-lattice ownership); G4 zone<->flavor map NOT owned; G5 stale-FAIL")
    print("  context predates this memo (pre-registration is pre-PINNING, not pre-contact).")
    print("PASS_ICECUBE_FORM_CHECK_V2  (DRAFT companion; candidate language only; post-skeptic-#1)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
