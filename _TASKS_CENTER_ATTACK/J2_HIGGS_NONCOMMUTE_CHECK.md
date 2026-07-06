# J2 PIECE-TO-HOLE CHECK — Higgs condensation hole vs TorusCore13 noncommuting pair

**Date:** 2026-07-04 · **Status:** VERIFICATION MEMO (no registry/status edits; owner to bless)
**Hypothesis under test (J2):** the owned Lean noncommutation `radial_hopping_phase_drift_noncommute`
(D0-TORUS-CORE13-GEOMETRY-001) satisfies the completion class demanded by
D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001 ("a frozen non-commuting (U,Q0,Pi_H), [T,Q0]!=0").

## VERDICT: CATEGORY MISMATCH — J2 KILLED as a direct fit

The piece and the hole live on different carriers, over different rings, against different operators,
with different object types, and the piece fails the hole's frozen/forcing condition. Five independent
mismatch axes; any one alone is disqualifying. One narrow salvage lead survives (§4).

---

## 1. The hole, typed precisely (sources read)

Sources: `05_CERTS/vp_higgs_condensation_present_core_maximality_nogo.py`,
`09_LEAN_FORMALIZATION/D0/Matter/HiggsCondensationPresentCoreMaximalityNoGo.lean`,
`09_LEAN_FORMALIZATION/D0/Matter/HiggsReturnQuotientAction.lean` (T definition),
`04_VERIFICATION/HIGGS_PHASON_ORBIT_BLOCKERS.csv`, `04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv`
(PRIM-NONCOMMUTING-TRIPLE row), registry row in `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv`.

| Slot | Typed requirement | Source |
|---|---|---|
| Operator space | `Matrix (Fin 2) (Fin 2) (ZMod 44)` — the Higgs **return-quotient scalar/archive sector**. NOT the 33-dim scene (ℂ³³/commutant-M₃ is the E1 rep behind the operator-type firewall; the condensation hole is typed downstream of the return quotient, not on ℂ³³). | Lean no-go module, lines 27–46; blocker atlas `exact_finite_object: T=[[0,1],[1,-1]] over ZMod 44` |
| T | The **return operator** `T = !![0,1; 1,-1]` over ZMod 44, order 30 ("no period-44 toral return exists"; cert control `FAIL_T_POW_44_EQ_I_REJECTED`). The present-core class is *defined* as polynomials in this T (`tPoly_commutes`: all `a•1 + b•T`). | HiggsReturnQuotientAction.lean:20; cert lines 17, 55–56 |
| Q0 | A **projector** (archive projector; the orbit `Q_n = T^n Q0 T^-n` / `Q_n = Wbar(n) Q0 Wbar(n)^dag` and the double-well need idempotency), **FROZEN / independently forced** — "derived not chosen"; "not a chosen rank-1 projector"; cert control `FAIL_CHOSEN_PROJECTOR_AS_PRESENT_CORE_REJECTED` explicitly rejects hand-picked Qnc. Must satisfy `[T, Q0] ≠ 0` against the T above. | blocker atlas rows D0-HIGGS-ARCHIVE-PROJECTOR-ORBIT-OWNER-001, D0-HIGGS-FINITE-CONDENSATION-OWNER-001; cert lines 52–54 |
| U | A **concrete orbit unitary** `Wbar(n)` driving `Q_n = Wbar(n) Q0 Wbar(n)^dag`. | blocker atlas row D0-HIGGS-ARCHIVE-PROJECTOR-ORBIT-OWNER-001 |
| Pi_H | Rank-2 scalar projector — **already owned** (D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001, CORE-FORMALIZED); the triple must bind to it. | HIGGS_PHASON_ORBIT_BLOCKERS.csv |
| Extra conditions | PRIM-NONCOMMUTING-TRIPLE catalog: mathematical_type "frozen noncommuting (U,Q0,Pi_H)"; minimal_input "**isolated spectral cluster + Riesz projector**"; necessary "non-commuting, **log-det stationary**"; admissible class "noncommuting spectral triples with finite flow". | TOTAL_EXTENSION_PRIMITIVES.csv |

Downstream chain the filled hole must feed (all PROOF-TARGET, is_global_blocker=True):
CANONICAL-PHASON-ORBIT → DISCRETE-LOGDET-EOM → DISCRETE-HESSIAN → FINITE-CONDENSATION
(stable stationary index n≠0 with Δ²S_n>0).

## 2. The piece, typed precisely (source read)

Source: `09_LEAN_FORMALIZATION/D0/Geometry/TorusCore13GeometryOrigin.lean` (full read).

| Slot | What the module owns |
|---|---|
| Space | `ShellMat = Matrix (Fin 3) (Fin 3) ℚ` — 3-shell carrier (`Shell3 = Fin 3`; inner/core/outer memory-torus shell boundaries). Rational entries, char 0. |
| Pair | `radialAdjacency` — symmetric 0/1 **tridiagonal hopping** (zero diagonal) — vs `phaseDrift T` — **diagonal radius readout** diag(1, (a+1)/2, a). |
| Theorem | `radial_hopping_phase_drift_commutator_01`: commutator entry (0,1) = `T.minor = (a−1)/2`; `radial_hopping_phase_drift_noncommute`: ≠ 0 since a > 1. |
| Parameter | `TorusParameter`: **free** rational a with only `1 < a`; docstring: "the concrete passport may instantiate a = phi^5" — instantiation is explicitly passport-level, not scene-forced. |
| Absent | No unitary, no projector, no Pi_H binding, no log-det functional, no ZMod structure, no import relation to any D0.Matter module (imports Mathlib only). |

## 3. Mismatch axes (each independently disqualifying)

1. **Carrier/ring mismatch.** `Fin 3 / ℚ` vs `Fin 2 / ZMod 44`. No typed map exists anywhere in the repo
   between the two; none can be canonical without a *new forced* reduction choice (char-0 rationals →
   composite modulus 44 = 4·11; e.g. the minor radius (a−1)/2 has no forced ZMod-44 image — the
   denominator-clearing is a choice).
2. **Wrong T.** The hole's commutator must be against the return operator `!![0,1;1,-1]` — the operator
   whose polynomial algebra *defines* present-core. `radialAdjacency` is a different operator on a
   different space: 3-dim, symmetric, zero trace/diagonal, vs 2-dim, non-symmetric, trace −1, order 30.
   "Noncommutes with an adjacency" certifies nothing about "noncommutes with the return operator".
   Note the attraction rides on a **name collision**: TorusCore13's torus is the *memory-torus solid
   geometry* (shell radii); the Higgs hole's torus is the *toral automorphism* T on (ZMod 44)² (the same
   matrix as the toral-Markov sector, cf. D0-LUCAS-VORONOI-MARKOV-PARTITION-001). Two different toruses.
3. **Q0 typing fails.** The hole demands a projector (idempotent). `phaseDrift` = diag(1,(a+1)/2,a) is
   **not idempotent** for a > 1 (it is a radius readout); `radialAdjacency` is not idempotent either.
   Neither operand of the owned commutator is even the right kind of object for the Q0 slot.
4. **Triple structure missing.** The hole is a *triple* (U, Q0, Pi_H) + log-det stationarity + finite
   flow. The piece owns exactly one commutator inequality: no `Wbar(n)`, no Pi_H binding (Pi_H is owned
   elsewhere and unreferenced here), no stationarity, no flow.
5. **Frozen/forcing condition fails.** `TorusParameter` is free; the φ⁵ instantiation is marked
   passport-level in the module's own docstring. Supplying (radialAdjacency, phaseDrift) as the hole's
   (T,Q0) is precisely the move the cert's reachable control rejects
   (`FAIL_CHOSEN_PROJECTOR_AS_PRESENT_CORE_REJECTED`: a chosen, non-independently-forced object).

Cross-check: repo-wide grep shows `radial_hopping_phase_drift_noncommute` is consumed only by ledger/
index modules (TheoremLedger/ClaimMap, HardClosureTheoremIndex, FinalBridgeIndex) and by
CKMPhasonHolonomy / GenerationSelectorOrigin — no Higgs-sector consumer, no bridge in either direction.

## 4. Exact lift that would be needed (named, in dependency order)

If the owner still wants to prosecute J2, ALL of the following are required — each is a new forced
artifact, none currently exists:

- **L1 Carrier registration.** A frozen-input-registered typed map
  `Matrix (Fin 3) (Fin 3) ℚ → Matrix (Fin 2) (Fin 2) (ZMod 44)` (or a common parent carrier), including
  a *forced* char-0 → ZMod 44 reduction. This is a new primitive by itself (nothing in the frontier
  primitives catalog covers it).
- **L2 Return-operator identification.** A forced 3→2 compression (Feshbach/Schur-type, cf. the repo's
  Feshbach lift machinery) under which the image of `radialAdjacency` *is* (or canonically intertwines
  with) `T = !![0,1;1,-1]`, with proof the compression carries the commutator. Structurally obstructed:
  symmetric-vs-nonsymmetric, dimension 3 vs 2, different spectra — expect a NO-GO here rather than a lift.
- **L3 Projector extraction (the one genuine seed).** Replace `phaseDrift` by its **Riesz/spectral
  projector onto one shell radius**. The shell spectrum {1, (a+1)/2, a} IS a set of isolated clusters for
  a > 1 — this literally matches PRIM-NONCOMMUTING-TRIPLE's `minimal_input: isolated spectral cluster +
  Riesz projector`. But the resulting projector must then be (a) frozen (needs frozen-input registration
  of the instantiation, currently passport-level) and (b) shown noncommuting with the *return* T after
  L1+L2 — neither exists.
- **L4 Triple completion.** Concrete forced `U = Wbar(n)`, binding to the owned rank-2 Pi_H
  (D0-HIGGS-SCALAR-PROJECTOR-CONSTRUCTIVE-001), plus log-det stationarity (necessary condition in the
  primitive catalog) feeding the DISCRETE-LOGDET-EOM → HESSIAN → CONDENSATION chain.
- **L5 Forcing certificate.** Independent forcing of the TorusParameter instantiation (a = φ⁵ or
  otherwise) — without it, the object is "chosen", which the completion class forbids by name.

## 5. Bottom line

- **J2 as stated: KILLED.** The owned pair is a 3×3/ℚ shell-geometry fact about an adjacency and a radius
  readout; the hole demands a frozen projector noncommuting with the 2×2/ZMod-44 return operator inside a
  full (U,Q0,Pi_H) log-det-stationary triple. Wrong space, wrong T, wrong object type, missing triple,
  not frozen.
- **Salvage lead (do not over-claim):** L3's observation — the 3-shell radii are isolated spectral
  clusters, matching the primitive's minimal_input shape — is a *lead for a new forcing chain*
  (Riesz projector on a forced carrier), not evidence the existing piece fits. If pursued, run it through
  the adversarial forcing loop as a NEW candidate with L1/L2 as pre-registered attack surface.
