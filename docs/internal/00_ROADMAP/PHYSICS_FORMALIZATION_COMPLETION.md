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

## DONE (Iter-21 so far — all committed, build GREEN, demotions 0)

- `D0-PROTON-001` → `D0.Matter.ProtonReadout306` (306 = 3960/13 + 3960/(13·20·11), `norm_num`); 938 MeV stays cert.
- `D0-BH-CAPACITY-A4-001` → `D0.Gravity.BlackHoleCapacityA4` (S(n)=n/4, S(4)=1, divisor 4; `ring`/`norm_num`).
- `D0-PHASON-THAWING-001` + `D0-IM-COSMO-001` → `D0.Cosmology.ArchiveConvexity` (Δ²(φⁿ−1)=φⁿ(φ−1)²>0; one theorem, two passports; fixed a dangling lean_module pointer).

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
