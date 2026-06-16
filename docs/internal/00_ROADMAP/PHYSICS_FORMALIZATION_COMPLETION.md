# Physics-formalization completion — cert-only → machine-checked Lean

## Why / headline (from a 6-agent triage of all cert-only + OPEN physics claims)

Goal: maximize machine-checked (Lean) coverage of the **physics** corpus — the primary track. A
6-agent triage of all `PYTHON_CERTIFIED` + OPEN physics claims (~62 distinct) found the dominant
failure mode is **registry lag, not missing proofs**:

| bucket | count | action |
|---|---|---|
| **ALREADY_LEAN** — finite fact already gap-free in a sibling; row points at nothing | ~12 | registry repoint (verify sibling, flip cert→Lean for the finite leg, keep residual honest) |
| **RIPE_PROMOTE** — genuine new finite theorem, minutes each (`native_decide`/`decide`/`norm_num`/`ring`) | ~8 | write small module, build, promote |
| **REACHABLE_BOUNDED** — real analysis/charpoly proof, hours each | ~12 | as time allows |
| **STAYS_CERT / EXTERNAL** — float-vs-experiment, or owner-edge classical theorem absent from pin | ~30 | correctly NOT promoted (a float-vs-lab check is not a Lean theorem) |

Net: ~20 cert-only rows can flip to machine-checked-finite-leg with well-under-a-day of work, mostly by
reuse. Inflating the ~30 empirical/owner-edge ones would be the exact over-claim the audit prevents.

## DONE (Iter-21 — all committed, build GREEN, demotions 0; strength 3762 → 3962, 78.7%)

**Batch D** (genuine new theorem + clears a dangling pointer 19→18) — `D0-IM-004` (Möbius witness
topological halting) → `D0.Topology.WitnessHalting` (`witness_halting_cert`): the orbit average
`E = (1/8) Σ_k P_k diag(1..8) P_kᵀ` over the 8 cyclic shifts equals the scalar `(9/2)·I` (emission
`36/8=9/2`), and `P_k E P_kᵀ = E` for every shift (`native_decide` on 8×8 ℚ). The cert's described
"orbit-average = (9/2)·I" was accurate; the module was a dangling grandfather pointer, now real.
`native_decide` needed a closed `∀ k` (free-variable goals are rejected). Halting-quotient reading stays cert.
**With Batch D, all flagged genuine-new-theorem batches (B, C, D, E, H) are done.** Remaining = REACHABLE_BOUNDED
(hours-each real-analysis/charpoly proofs) + dangling-pointer cleanup.

**Batch H** (genuine new theorem) — `D0-LAPLACIAN-SPECTRUM-FIX-001` → `D0.Spectral.ZoneMatrixSpectrum`
(`laplacian_3x3_correct`): the 3×3 row-stochastic zone matrix M over ℚ, `e₁=0`/`e₂=−121/160`/`e₃=39/160`
(`native_decide`), charpoly factorization `(λ−1)(λ²+λ+39/160)` (`ring`), the two active roots `−1/2±√10/40`
both as direct quadratic roots AND via the `λ↦1−λ` transport reusing `scene_active_eigenvalue_±` (the
Book-08 S_DE window), and the **error-correction negative control** `p(φ⁻¹)=(199/160)(φ⁻¹−1)≠0` (φ⁻¹ ∉ spec(M)).
Built clean after dropping `Mathlib.Data.Matrix.Notation` (absent in pin; `!![]` is transitive).

Batch C + verified repoints (earlier in Iter-21):
- `D0-HODGE-001` + `D0-NOAXION-001` → `BoundaryBoundary.boundary_boundary_zero` / `FiniteCochainNoAxion.finite_d_d_zero`
  (the d∘d=0 cores already existed — repoint, NOT a new `FiniteHodgeComplex` module; would have duplicated `BoundaryBoundary`).
- `D0-QUASI008-PHASON-FLIP-ENTROPY-SDE-001` → `PhasonFlipEntropy` (finite SDE polynomial 160λ²−480λ+359 verified real;
  stale "scaffold not proof" Phase-L note superseded after re-reading the module). `D0-IF-KS-FORMULA-FIX-001` →
  `FibonacciIfBridge`/`FibonacciFusionRing` (|λ_max|=φ load-bearing; KS=log|λ_max| Pesin wrapper external).

**VERIFIED-LEAVE-CERT (do NOT re-attempt — verify-then-promote already ruled these out):** `D0-TIME-MODULAR-FLOW-001`
(unique = Sturmian symbolic-word coincidence in the cert; Lean siblings prove the adjacent Beatty-carrier + Pisot-arrow
legs, already owned by other claims), `D0-VACUUM-CUBIC-WINDOW-001` (unique = float discriminator ratios + empirical DESI
fork; both branch polynomials owned by `MIXING-HIERARCHY-INVERSION`/`PhasonFlipEntropy`), `D0-QUASICRYSTAL-CARRIER-FORCING-001`
(unique = 4-external-pillar FORCING argument; inflation backbone owned by `FibonacciFusionRing`), `D0-SDE-K0-001`
(K0/Connes gap-labeling genuinely external). Net: the roadmap's optimistic 6 repoints = 2 genuine + 4 honest leaves.


New finite theorems (machine-checked, `decide`/`native_decide`/`norm_num`/`ring`/`field_simp`):
- `D0-PROTON-001` → `D0.Matter.ProtonReadout306` (306 = 3960/13 + 3960/(13·20·11)); 938 MeV stays cert.
- `D0-BH-CAPACITY-A4-001` → `D0.Gravity.BlackHoleCapacityA4` (S(n)=n/4, S(4)=1, divisor 4).
- `D0-PHASON-THAWING-001` + `D0-IM-COSMO-001` → `D0.Cosmology.ArchiveConvexity` (Δ²(φⁿ−1)=φⁿ(φ−1)²>0; two passports).
- `D0-COMPACTNESS-DEF-FORCING-001` → `D0.Gravity.CompactnessLimit.compactness_def_forcing` (Batch B).
- `D0-CVFT-F3B` → `D0.Matter.BaryonSpinFlavourRanks` (SU(6) 56=40+16: spin 4, decuplet 10, 40, 56, 16) (Batch E).

Verified repoints (sibling confirmed to prove the claim's finite content; cert→Lean upgrade):
- `D0-FOUND-004` → `D0.Core.BornQuadraticResponse.unit_phase_blind_quadratic_response_is_norm_sq`.
- `D0-EDGE-ALPHA-001` → `D0.Spectral.ZetaResidueAlpha.zetaEdge_neg_one` (unitary-dilation residual noted).
- `D0-BOOK04-SELECTORS-002` → `D0.Matter.Book04CombinatorialSelectorOrigins`.

**Findings (honesty refinements to the triage):**
1. **3 dangling `lean_module` pointers fixed**, then a **full sweep found 19 more** dangling pointers (rows
   naming Lean modules that never existed). ALL 19 are on `PYTHON_CERTIFIED`/`OPEN` rows — none is
   `LEAN_PROVED`, so none is an over-claim, but they mislead. New guard `tools/check_no_dangling_lean_module.py`
   fails on any NEW dangling pointer, with the 19 GRANDFATHERED (ratchet may only shrink). **Cleanup task:**
   clear the pointer on the ~11 STAYS_CERT/OPEN ones (GRAV-005/006, HORIZON-JET-001, IM-COSMO-002/003/004,
   QUANT-MET-001..004, PUB-001, BARYON-POLES poles) and build the ~8 RIPE/REACHABLE ones (IM-001..005,
   IM-PRED-001, EDGE-RAMIFICATION-001, GRAV-004 finite legs). Each clear = a TARGETED single-row Edit
   (never a DictWriter rewrite — that truncated the CSV once).
2. **Do NOT repoint already-split parents.** `D0-COMPACTNESS-LIMIT-001` (named gap rank-3=cone, deliberately
   bridge-level), `D0-KTHEORY-001` (Bellissard IDS external), `D0-QUASICRYSTAL-PROJECTION-001` (icosahedral
   separation) each have their finite shadow as a SEPARATE CORE claim already (`KTHEORY-GAP-MODULE-001`,
   `CARRIER-NOT-ICOSAHEDRAL-001`, `COMPACTNESS-DEF-FORCING-001`). Repointing the parent would over-claim/duplicate —
   left untouched. The triage's "ALREADY_LEAN" count is therefore smaller in genuine-repoint terms.

## REMAINING (for careful continuation)

New theorems: **Batch C** `FiniteHodgeComplex` (HODGE-001 d∘d=0 + extend `FiniteCochainNoAxion` NOAXION-001 Betti),
**Batch D** `WitnessHalting` (IM-004 orbit-average; matrix `native_decide` — riskier), **Batch H** `ZoneMatrixSpectrum`
(LAPLACIAN-SPECTRUM-FIX charpoly + `SceneActiveEigenvalues` transport). Verified repoints still to verify+do:
`D0-TIME-MODULAR-FLOW-001` (PisotContraction+DeloneInstance), `D0-QUASICRYSTAL-CARRIER-FORCING-001` (FibonacciFusionRing
φ-leg), `D0-VACUUM-CUBIC-WINDOW-001` (SceneActiveEigenvalues+MixingHierarchyInversion), `D0-IF-KS-FORMULA-FIX-001`,
`D0-QUASI008-PHASON-FLIP-ENTROPY-SDE-001` + `D0-SDE-K0-001` (PhasonFlipEntropy finite core; K0 external). Each:
verify the sibling matches, watch for dangling pointers + already-split parents, cert→Lean for the finite leg only.

## REMAINING RIPE batch (new finite theorems, minutes each)

- **Batch C** `D0.Geometry.FiniteHodgeComplex` (HODGE-001: d∘d=0, d1·d1ᵀ diag=3) + extend `D0.Topology.FiniteCochainNoAxion` (NOAXION-001: integer Betti b1=(6−3)−3=0, K4 control 3). `decide` on ℤ `!![…]`; reuse the existing `BoundaryBoundary` d∘d=0 idiom; write the rank helper once.
- **Batch E** `D0.Matter.BaryonSpinFlavourRanks` (CVFT-F3B + BARYON-POLES rank legs): SortedTriple cards — copy the `SortedTriple`/`deriving Fintype`/`decide` idiom from `D0.Matter.BaryonS3Symmetrizer` (flavour 10); add spin-card 4, 6-card 56, 40=10·4, 56−40=16.
- **Batch D** `D0.IM.WitnessHalting` (IM-004): cyclic-orbit-average of diag(1..8) = (9/2)·I commutes with every shift; `native_decide` 8×8 ℚ; reuse `D0.Core.FiniteTypes.card_omega8/card_v9`.
- **Batch B** extend `D0.Gravity.CompactnessLimit` (COMPACTNESS-DEF-FORCING-001): m/(2m)=1/2, 1/(8/3)=3/8, 3/8<1/2≠1/2; `field_simp`/`norm_num`.
- **Batch H** `D0.Spectral.ZoneMatrixSpectrum` (LAPLACIAN-SPECTRUM-FIX-001): row-stochastic + charpoly factorization λ³−(121/160)λ−1287/5280=(λ−1)(λ²+λ+39/160); transport the two eigenvalues as the λ↦1−λ image of `SceneActiveEigenvalues` roots; √5-irrationality separation via `GaloisPhiNontrivial`.

## REMAINING repoints (ALREADY_LEAN — verify sibling, then flip cert→Lean for the finite leg)

| Claim | Repoint to (verify first) | residual kept honest |
|---|---|---|
| D0-COMPACTNESS-LIMIT-001 | `D0.Gravity.CompactnessLimit.compactness_limit` | rank-3=cone prose (bridge) |
| D0-TIME-MODULAR-FLOW-001 | `D0.Dynamics.PisotContraction` + `D0.Topology.DeloneInstance` | topological conjugacy (external) |
| D0-QUASICRYSTAL-CARRIER-FORCING-001 | `D0.Claims.FibonacciFusionRing` (Perron leg) | 5-fold trig + Wilson/Penrose pillars |
| D0-QUASICRYSTAL-PROJECTION-001 | `D0.Claims.CarrierNotIcosahedral.carrier_not_icosahedral` | — |
| D0-KTHEORY-001 | `D0.Claims.KTheoryGapModule.ktheory_gap_module` | Bellissard IDS=K0-trace (external); retire float-IDS cert |
| D0-FOUND-004 | `D0.Core.BornQuadraticOrigin` | — |
| D0-BOOK04-SELECTORS-002 | `D0.Matter.Book04CombinatorialSelectorOrigins` | — |
| D0-EDGE-ALPHA-001 | `D0.Spectral.ZetaResidueAlpha.zetaEdge_neg_one` | unitary dilation (optional) |
| D0-QUASI008-PHASON-FLIP-ENTROPY-SDE-001 | `D0.Cosmology.PhasonFlipEntropy` | K0/holonomy (external) |
| D0-SDE-K0-001 | `D0.Cosmology.PhasonFlipEntropy` (finite core) | K0 gap-labeling (external) |
| D0-VACUUM-CUBIC-WINDOW-001 | `D0.Geometry.SceneActiveEigenvalues` + `D0.Claims.MixingHierarchyInversion` | DESI-DR3 window (empirical) |
| D0-IF-KS-FORMULA-FIX-001 | `D0.Claims.FibonacciIfBridge` + `D0.Claims.FibonacciFusionRing` | log wrapper (optional) |

**Discipline (every promotion):** verify the sibling theorem genuinely proves the claim's finite
content BEFORE flipping cert→Lean (verify-then-promote); a finite leg promotes, an external/empirical
residual stays cert/owner-edge and is named in the note; cert→Lean is an upgrade (firewall-safe,
demotions 0); full `lake build D0.All` green + guard suite per batch.

## REACHABLE_BOUNDED (hours, if pursued) — ranked
CVFT-F4 (Mathlib geometric-series tail bound — the standout), EW-002 (3·13=39 + δ₀ norm), CVFT-F3 (S₃
rep idempotency), EDGE-RAMIFICATION-001 (companion charpoly), GRAVASTAR-FORMATION (seam inequalities),
IM-PRED-001 / IM-001/002/003/005 (φ-recursions; continuum-envelope legs stay cert), MASTER-BOOTSTRAP
(trace ranks), MINCUT-001 (cut=flow witness), GRAV-004/CVFT-F6 (finite ℚ matrix witness only — the
YM-gap / horizon headline rows stay PROOF-TARGET).

## STAYS cert/external (correct, do NOT promote)
Float-vs-experiment: E8-COLDEA, NEUTRON-002 (CODATA), LEPTON-002 (PDG), MODULAR-TIME-FLAVOR (NuFIT),
H0-EVOLVING-W, DSI, GRAVASTAR-GW-FALSIFIER, the PASSPORT-* and IM-COSMO-002/003/004 rows, GRAV-QNM,
GRAV-005, HORIZON-JET. Owner-edge (absent from pin): SOLENOID(-GRAVITY), KTHEORY operator side,
CKM/MESON-K0 + phason-holonomy, DIXMIER (CVFT-F1), Wilson/Clay-YM (LATTICE-FINITENESS, CVFT-F6 gap,
SPECTRAL-ACTION-ADMISS, HST-ARCHIVE), FTHEORY-001/002 (Lin–Weigand), EDGE-002 (Puiseux), HODGE-LINKS,
CVFT-F2/F7/F8/001B.
