# ICECUBE-DECOHERENCE-FORM — candidate functional form of neutrino phason-decoherence vs energy: log-damping = (ladder depth) x (owned saturating loop pressure); reading-robust flagship = the bounded/saturating plateau (D1); single-path monomial fine structure reading-conditional (DRAFT v2, post-skeptic-#1)

**Status:** DRAFT candidate FORM, pre-registered BEFORE the HESE cache is pinned. No registry row
edited, no cert minted, no book section touched. Companion script:
`_TASKS_CENTER_ATTACK/icecube_form_check.py` v2 (all PASS + 6 controls; NOT a minted cert).
Skeptic #1 verdict: NO KILL of F1 or the memo; ONE sub-claim KILLED + six forced repairs — all
accepted in full, no defense (repair log §10).
Pre-flight run: `icecube decoherence phason hese` — no existing row owns a functional FORM
derivation; cross-refs: D0-ICECUBE-001 (row 119, EMPIRICAL-PASSPORT), D0-CVFT-F5 (row 138,
PROOF-TARGET), D0-PASSPORT-ICECUBE-HESE-001 (row 202, PROOF-TARGET), D0-FESHBACH-SCHUR-TIME-DELAY-
OWNER-001 (row 368), D0-ARCHIVE-NEUMANN-TICK-OWNER-001 (row 369), D0-CVFT-001A (row 130, feedback
operator core — the RIVAL-reading owner, named by skeptic #1), D0-IM-COSMO-003 (row 160,
kappa = log phi owner), TICK_COUPLING_SCHUR_MEMO.md (DRAFT v2). Nothing here retunes or replaces
the frozen Hurwitz passport curve (§4).

---

## 0. The prediction slot: what the frozen passport actually compares

Pinned from the cert and protocol (so the candidate form is aimed at the REAL observable, not an
imagined one):

- Observable: "energy-binned event survival / suppression shape using the HESE `energy` field"
  (`08_PASSPORTS/IceCube/icecube_baseline_protocol.md`); statistic scored on the TOP log10(E) bin
  only, `delta_loglik` / `delta_chi2` vs a no-decoherence null
  (`05_CERTS/vp_icecube_hese_baseline_comparison.py:22-38`, window "edges 1.97e4 .. 4.80e6,
  high_bin_obs = 4").
- The D0 side of the comparison is a per-event DAMPING ENVELOPE: `damping_d0 = exp(-gamma)`
  multiplying expected counts (`05_CERTS/vp_neutrino_phason_decoherence_passport.py:198`), with
  the FROZEN kernel `"Gamma(E,z) = delta0^2 * log(1+z) * H_phi(E/E0)"` and
  `forbidden_fits = ["delta0", "Hurwitz phase", "posthoc energy exponent"]`
  (`08_PASSPORTS/IceCube/icecube_phason_decoherence_protocol.json:4-9`), `delta0 = 1/(2*phi^3)`
  (`vp_neutrino_phason_decoherence_passport.py:176-177`).
- So the D0 prediction slot IS the functional family of the damping envelope D(E) (equivalently
  the shape of -ln D vs E), NOT a fitted exponent and NOT an event selection. That is the slot
  this memo fills with a candidate derived from internal objects only.
- Naming guard: the §08.42 loop fugacity is written `zeta` throughout this memo; `z` in the
  passport code is a REDSHIFT proxy (`z_proxy = energy/1e6`,
  `vp_neutrino_phason_decoherence_passport.py:188`). Two different symbols, kept apart on purpose.

## 1. Claim F1 (DEF-0.2.2 form; CANDIDATE, not forced)

> **F1 (candidate envelope form).** On the frozen scene K(9,11,13) with the frozen Feshbach split
> P = proj(range A_scene) (rank 3), Q = proj(ker A_scene) (dim 30), take the tri-phase unitary
> carrier U3 = diag(mu9; mu11; mu13) (TICK_COUPLING_SCHUR_MEMO candidate) and give each
> archive-resident step the §08.42 resolvent retention weight x = 1 - zeta*r(V),
> r(V) = 1 - e^{-kappa V} (CONV-1, CONV-2 below). Then the retained-sector coherence envelope is,
> per zone n in {9,11,13}, EXACTLY the monomial
>
>     D_n(x) = |x|^(n-1),    i.e.    -ln D_n(E, L) = N_n * (L/L0) * P0842(E),
>
> with N_n in {8, 10, 12} fixed integers (no free exponent) and
> P0842(E) = -ln(1 - zeta*(1 - e^{-kappa V(E)})) the owned §08.42 log-det loop pressure evaluated
> on a bridge V(E) (BR-1, not owned). The candidate IceCube-facing prediction is this envelope
> family: bounded, saturating energy damping with fixed integer log-damping ratios 8:10:12 —
> against the standard Lindblad family exp[-(E/E0)^m * L/L0], which is unbounded in E.

**F1 is READING-CONDITIONAL even at fixed carrier (skeptic #1 strongest finding, adopted).**
On the SAME carrier U3 the OWNED full-loop feedback object F_N = P U^dag Q U P (D0-CVFT-001A,
row 130: `feedback_determinant_return_cycles`, `feedback_pressure_trace_log`, LEAN_PROVED) is
ALIVE: F_N = P exactly (computed — per zone ||Q U3 u_n||^2 = 1 because PUP = 0), so
det(I - z F_N) = (1-z)^3 != 1, and the owned log-det pressure route yields a RIVAL envelope

    F0 (rival, STRICTLY BETTER ownership pedigree):  -ln D(E, L) = 3 * (L/L0) * P0842(E)

— uniform depth 3, NO zone splitting, no 8:10:12, GM law degenerate, SAME bounded/saturating
plateau. The open-path Schur reading behind F1 is a SELECTION among live readings, not forced.
What is COMMON to both live readings — the honest flagship of this memo — is D1:
-ln D(E) = (fixed depth) x (L/L0) x P0842(E) with P0842 bounded and saturating (owned shape).
The fine structure (which depth; whether zones split) is reading-conditional.

Status language: candidate/DRAFT. "Fixed integers" refers to the computed ladder structure on the
candidate carrier under the open-path reading; F1 is conditional on gaps G1-G4 plus the reading
selection G2' (§6) and is NOT promotable past them.

## 2. Owned pre-facts (verbatim, file:line)

1. Loop pressure map (the energy-shape owner). BOOK_08 §08.42
   (`01_BOOKS/BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER/0032__08.42__icecube-neutrino-phason-decoherence-passport.md`):
   - :8 "R(V)=e^{\kappa V}-1, \qquad r(V)=1-e^{-\kappa V}"
   - :12-13 "\partial_V[-d_\tau\log(1-zr(V))] = d_\tau\frac{z\kappa e^{-\kappa V}}{1-z(1-e^{-\kappa V})}>0"
   - :16 "positive but bounded and saturating: \(L(V)\to -d_\tau\log(1-z)\) and \(L'(V)\to0\)"
   - :5 "This is an internal dimensionless pressure-response theorem. Survey comparison remains passport-layer."
   - :26 "Active contraction and archive expansion are the stable and unstable eigen-branches of one determinant-balanced time automorphism, not two independent fitted forces."
   - :29 "active localization x archive expansion = 1"
2. Neutrino identification (why a phason/archive object is the right carrier CLASS).
   - `09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` row D0-ICECUBE-001, notes: "Neutrino is a
     neutral bulk phason leakage mode internally; IceCube decoherence comparison is skipped until
     a complete external event energy direction response and hash manifest is supplied."
   - `01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY/0011__04.9__neutrino-leakage-sector.md:19-23`:
     "Neutrino is interpreted as neutral bulk phason wave / neutral leakage mode in the theorem
     owner `D0.Matter.NeutrinoPhasonWaves`. ... any IceCube decoherence comparison belongs to the
     downstream passport layer (a manifest-only scaffold cert that does not verify the beat law below)."
   - `.../0006__04.4__matter-as-defects-and-gap-labeled-spectra-over-t.md:102`: "The neutrino is
     represented as a neutral bulk phason wave with zero active EM coupling."
3. The FORM slot is open in Lean (nothing is being re-derived or contradicted).
   `09_LEAN_FORMALIZATION/D0/Matter/NeutrinoPhasonWaves.lean:7-10`: "The module states the
   internal finite object only. IceCube comparison is a passport layer and must carry an external
   manifest." The kernel objects there are marker-level witnesses
   (`HurwitzGapScatteringKernel ... strength := 1 ... admissible := True`, :54-64;
   `PhasonDecoherenceKernel ... energy_dependence := 1`, :72-87): no functional form of
   Gamma(E) is Lean-owned. F1 competes for an OPEN slot.
4. Tick ladder (the circulation-count owner). `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:487`:
   "the active evolution is the Feshbach–Schur complement `W_eff = P U P + P U Q (I - Q U Q)^{-1}
   Q U P`; expanding the archive resolvent `(I - Q U Q)^{-1} = Σ_k (Q U Q)^k`, the order-`k` term
   carries exactly `k` internal archive circulations before observable return. The Neumann index
   `k` IS the discrete time tick (`D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001`,
   `D0-ARCHIVE-NEUMANN-TICK-OWNER-001`). Honest residual: the tick identity is closed on the
   resolvent/convergence domain (spectral radius of `Q U Q < 1`)."
   (Registry: row 369 theorem `neumann_term_k_has_k_archive_circulations`.)
5. Nilpotent carrier (the finite-ladder fact; DRAFT-owned, computed).
   `_TASKS_CENTER_ATTACK/TICK_COUPLING_SCHUR_MEMO.md:39-46`: U3 "is UNITARY, breaks all three
   within-zone symmetries, and satisfies: (QUQ)^12 = 0 EXACTLY (nilpotent; true rho = 0), so the
   Neumann ladder is a FINITE SUM — no convergence hypothesis at all; ... Nilpotency index exactly
   12 ... destroyed by a single repeated phase (the full phase lattice is exactly load-bearing)."
   Note rho(QUQ) = 0 < 1: the finite ladder sits INSIDE the tick owners' declared convergence
   domain (pre-fact 4), so using their k-counting here needs no domain extension.
6. Passport discipline this memo must respect. §08.45
   (`.../0035__08.45__icecube-neutrino-phason-decoherence-external-com.md`):
   - :6 frozen object = "neutral bulk phason-wave kernel with finite decoherence window"
   - :21-23 "High-energy neutrino decoherence is a falsification hook for the frozen neutral bulk
     phason-wave kernel, not a license to retune the kernel from IceCube data."
   - :27-29 "no energy-window retuning after event selection; no detector-response tuning inside
     the D0 kernel; no IceCube residual may select a new neutrino operator."

## 3. Construction (compute-first; every quantity from `icecube_form_check.py`)

**Step 1 — reading selection (REPAIRED v2: selection, NOT forcing — error of record E1).**
det(I - x*QUQ) = 1 identically (all eigenvalues of a nilpotent block are 0; verified at
x = 0.3, 0.7, 0.99): the closed-loop log-det pressure vanishes on the archive block ITSELF
(tr((QUQ)^m) = 0 for all m >= 1). v1 concluded from this that the open-path Schur ladder was the
"only surviving" circulation object — WRONG: the OWNED full-loop object F_N = P U^dag Q U P
(D0-CVFT-001A) is alive on U3 with det(I - z F_N) = (1-z)^3 (computed, script [3c]) and carries
the owned pressure route directly, giving the rival F0 of §1 with uniform depth 3. The QUQ-det
computation kills only the QUQ-closed-loop reading. F1's open-path reading is a SELECTION among
(at least) two live readings; adjudication between them (G2', §6) is an ownership question, not
settled here. What both readings share: depth x P0842(E) structure, hence D1.

**Step 2 — single-path theorem on U3 (computed, the memo's core fact).**
Per zone n in {9,11,13} (everything block-diagonal per zone; retained basis = per-zone uniform
vectors u_n):
- direct channel: <u_n| P U3 P |u_n> = (1/n) * sum of all n-th roots of unity = 0 EXACTLY;
- Neumann rungs t_k = <u_n| P U3 Q (Q U3 Q)^k Q U3 P |u_n>: EXACTLY ONE nonzero rung, at the
  MAXIMAL depth k = n-2, with |t_{n-2}| = 1.
DFT reading: in the zone Fourier basis U3 acts as the cyclic mode-shift, Q deletes the DC mode,
so QUQ is the truncated shift (Jordan chain of length n-1; per-zone nilpotency indices 8/10/12,
verified). The unique coherent return path is the FULL traversal DC -> mode 1 -> ... -> mode n-1
-> DC. Cross-check against the skeptic-#2 recorded value: ||sum_k P U3 Q (QUQ)^k Q U3 P||_F =
sqrt(3) reproduced to 1e-12 (= one unit-amplitude return per zone).
Consequence: the retained-sector amplitude per tick is the PURE MONOMIAL w_n(x) = t * x^(n-1)
once each archive-resident step carries a retention weight x (CONV-1). At x = 1 (lossless),
|w_n| = 1 — consistent with unitarity.

**Step 3 — marriage with the owned pressure map (CONV-2; the load-bearing unowned step).**
Identify the per-step retention weight with the §08.42 resolvent factor: x = 1 - zeta*r(V),
0 < zeta < 1, r(V) = 1 - e^{-kappa V} (pre-fact 1). Then
    -ln D_n = (n-1) * [-ln(1 - zeta*r(V))] = N_n * P0842(V):
log-damping = (integer ladder depth) x (owned log-det loop pressure). All shape properties are
INHERITED from the §08.42 theorem: positive, monotone (:12-13), bounded and saturating (:16).
Interpretive gloss (candidate language only): a strictly positive coherence floor is the
determinant-balance residue — total erasure of the active branch would violate
"active localization x archive expansion = 1" (:29, :26).

**Step 4 — distance/tick iteration and conventions (declared, not owned).**
- CONV-1: weight x per archive-resident U-step => exponents N_n = n-1 in {8,10,12}.
  CONV-1': weight per internal circulation only => {7,9,11}. Both are arithmetic progressions
  with gap 2; every discriminator below is checked under both.
- CONV-3: probability = |amplitude|^2 and T = L/L_tick tick iterations multiply -ln D by
  2T — absorbed into (L/L0). Ratios, GM law, plateau-existence are invariant.
- BR-1: V(E) monotone non-decreasing (script demonstrates kappaV = E/E* and sqrt(E/E*); all
  claimed discriminators are verified identical under both bridge shapes).
- Ensemble: HESE has no per-event baseline L; averaging over a non-degenerate L-distribution
  turns the GM EQUALITY into the strict Cauchy-Schwarz INEQUALITY <D_11>^2 <= <D_9><D_13>
  (computed). Pre-registered as a limitation, not discovered later.

## 4. Relation to the frozen Hurwitz passport curve (no retuning)

The frozen curve Gamma = delta0^2*log(1+z_r)*H_phi(E/E0) stays the frozen passport object. F1 is
a SECOND, independently-derived candidate for the same envelope slot, registered while the HESE
cache is UNPINNED (live verdict SKIP, `vp_icecube_hese_baseline_comparison.py:55-63`). Selection
between the two candidates must be INTERNAL (adjudicating G2/G3 ownership), never by IceCube
residuals (§08.45:27-29 — "no IceCube residual may select a new neutrino operator"). Zero IceCube
numbers enter F1's construction (the only quoted data-adjacent numbers — window edges, stale
avg_damping_high = 0.99934 — appear in §0/§6 as context and in no construction step).
Context-consistency, not evidence: for small zeta*r in the recorded window, D_n ~ 1 - N_n*zeta*r
is near unity, compatible with the stale near-no-damping context; F1 separates from both the
frozen curve and Lindblad in the tail and in the flavor split.

## 5. The candidate law, its properties, and the discriminators

**F1:**  -ln D_n(E, L) = N_n * (L/L0) * P0842(E),  N_n in {8,10,12} (CONV-1; {7,9,11} under
CONV-1'),  P0842(E) = -ln(1 - zeta*(1 - e^{-kappa V(E)})).

Computed properties (all verified in the script; reading-conditionality per skeptic #1):
- P1 (plateau) — READING-ROBUST (shared by F1 and the rival F0): -ln D increases monotonically
  in E and saturates at depth*(L/L0)*(-ln(1-zeta)): a strictly positive coherence floor.
  Same knee E* for all zones. CONDITIONAL on the positive-floor marriage class (see D1).
- P2 (maximal sparsity) — READING-CONDITIONAL (open-path only): the envelope is a SINGLE
  monomial in x — not merely a finite polynomial (the a-priori finite ladder, <= 11
  circulations, collapses to its deepest rung). Absent on the F_N route.
- P3 (factorization) — READING-CONDITIONAL: energy enters ONLY through the common scalar
  P0842(E); zones/distance enter only through the integer x (L/L0) prefactor. (The F0 rival
  also factorizes but with a single uniform depth — no zone structure to factor.)
- P4 (fixed triple) — READING-CONDITIONAL (open-path only): log-damping ratios
  ln D_9 : ln D_11 : ln D_13 = 8 : 10 : 12 = 4 : 5 : 6 at EVERY energy, independent of zeta,
  kappa, bridge shape, L (verified on the FULL grid zeta in {0.05,0.3,0.6} x both bridges);
  geometric-mean law D_11^2 = D_9 * D_13 per baseline (deviation < 1e-12); after L-averaging:
  <D_11>^2 <= <D_9><D_13> (strict CS, computed). On the F0 rival all three coincide (degenerate).

**Discriminators vs standard Lindblad decoherence exp[-(E/E0)^m L/L0]** (flagship first):
- D1 (bounded vs unbounded energy damping) — the READING-ROBUST flagship: shared by F1 and the
  rival F0; independent of CONV-1/1', of G4, and of the depth integer. CONDITIONAL on the
  marriage class: it holds for marriages with a strictly positive retention floor
  (inf x = 1 - zeta > 0, inherited from the §08.42 resolvent factor); a floorless marriage
  x = e^{-kappa V} reproduces Lindblad m = 1 exactly and KILLS D1 (computed control C5 — the v1
  "any bounded monotone marriage" sub-claim is retracted, §10/E2). Numbers (demo zeta = 0.3,
  L/L0 = 1, from the script): bridge kappaV = E/E*: calibrated Lindblad (m = 0.973) tracks F1
  to <15% below the knee, log-dampings differ 2x by E = 2.44 E*, and at 1000 E* F1 damping =
  0.0138 (plateau, -lnD = 4.28) vs Lindblad 0.00e+00 at float precision (-lnD = 2675.9);
  bridge kappaV = sqrt(E/E*): m = 0.454, 2x split by E = 10.0 E*, at 1000 E* Lindblad 1.99e-29
  (-lnD = 66.1) vs the same F1 plateau. Exposure-free two-bin shape statistic:
  rho(E) = lnD(2E)/lnD(E) -> 1.000 above the knee for F1/F0 vs 2^m (still falling) for Lindblad.
  Relation to the frozen HESE statistic: INDIRECT and one-sided — the frozen primary is a single
  top-bin count, which constrains D1 only parameter-conditionally (if the knee sits below the
  top bin, F1/F0 predict energy-flat suppression there while Lindblad predicts deepening); the
  rho(E) statistic needs two energies and is a PROPOSED secondary, outside the frozen primary.
- D2 (geometric-mean law) — READING-CONDITIONAL (open-path only), convention- and bridge-robust;
  needs flavor-resolved damping: D_11^2 = D_9*D_13 per baseline; ensemble version one-sided.
- D3 (integer triple) — READING-CONDITIONAL and convention-dependent: 8:10:12 (= 4:5:6) under
  CONV-1, 7:9:11 under CONV-1'; the AP gap 2 is convention-invariant. Also distinguishes F1
  from the rival F0 (uniform depth): any observed zone/flavor SPLITTING kills F0 but not F1.

**Falsifier (pre-stated).** When the HESE cache is pinned: if the binned suppression keeps
deepening compatibly with (E/E0)^m (m > 0) across the top decade with NO flattening, the whole
positive-floor family (F1 AND the rival F0) is killed (no parameter rescue: zeta and E* move the
knee and floor but cannot unbound the energy damping). If flavor-resolved damping shows a
non-degenerate triple violating the GM/CS relation of P4, the open-path F1 is killed
specifically (and a degenerate triple kills nothing between F1-with-one-zone-selected and F0 —
stated to avoid a false dichotomy). Conversely, F1/F0 CANNOT explain any observed unbounded
suppression — this family is not a universal fit family.

## 6. Named gaps (what is owned vs bridge-assumed)

- G1 (bridge): the zeta <-> E map. §08.42 owns the SHAPE P0842(V) in the internal variable V and
  the domain 0 < zeta < 1; kappa = log phi > 0 itself IS owned (D0-IM-COSMO-003, row 160,
  CORE-FORMALIZED — v2 correction, error of record E6); what is NOT owned: the composite bridge
  kappaV(E) (BR-1), the CONV-2 marriage, and the values of zeta, E*, L0. Without BR-1
  monotonicity, D1's "plateau IN ENERGY" is not implied.
- G2 (carrier identification — the exact missing link): NO owned object identifies the neutrino
  phason kernel's propagation with the open-path archive ladder of the tick carrier. The needed
  (nonexistent) statement has the shape: "the neutral bulk phason leakage mode of
  `D0.Matter.NeutrinoPhasonWaves` propagates through ker A_scene, and its per-tick coherence
  transfer is the Feshbach open-path ladder P U Q (QUQ)^k Q U P of
  D0-ARCHIVE-NEUMANN-TICK-OWNER-001 on the selected carrier U." Until such an owner exists, F1's
  carrier premise is a candidate, not a fact.
- G2' (reading selection — v2, skeptic #1): even granting the carrier, the choice between the
  open-path Schur reading (F1) and the OWNED F_N = P U^dag Q U P loop reading (F0, D0-CVFT-001A)
  is NOT adjudicated; F0 currently has the better ownership pedigree. Only D1 is
  reading-invariant.
- G3 (carrier pedigree): U3 itself is DRAFT-candidate; inherits TICK_COUPLING_SCHUR_MEMO S1'
  (staticity-clause reading unresolved) and S2 (mu_n-as-operator not a greppable owned object).
- G4 (zone <-> flavor): no owned map assigns zones {9,11,13} to neutrino flavors/generations;
  only the SET of exponents (and the AP-2/GM structure) is pre-registered, not the assignment
  (6 permutations open).
- G5 (contact honesty): the recorded stale FAIL (`avg_damping_high = 0.99934`) was visible before
  this memo. Pre-registration here is pre-PINNING, not pre-any-contact. Mitigation: F1's every
  structural ingredient carries an owned/computed citation independent of IceCube, and F1's free
  content beyond the bridge constants is zero.
- G6 (statistical reach — demoted v2, error of record E7): the frozen primary statistic is a
  SINGLE top-bin count. NONE of D1-D3 is directly decided by it: D1 is testable only indirectly,
  one-sidedly and parameter-conditionally through it (knee below the top bin => flat vs deepening
  suppression); the rho(E) two-bin statistic and the D2/D3 flavor-resolved observables are
  PROPOSED secondaries outside the frozen primary and must never alter the primary event set
  (icecube_baseline_protocol.md discipline).

## 7. PRE-REGISTERED attack surface (strongest first; built against ourselves)

- A0 (STRONGEST — v2, the F_N rival route; skeptic #1's construction, adopted with credit): the
  owned F_N = P U^dag Q U P object (D0-CVFT-001A) + the §08.42 pressure produce the F0 envelope
  on the SAME carrier with STRICTLY BETTER ownership pedigree and NONE of F1's fine structure
  (uniform depth 3, no 8:10:12, degenerate GM). Attack: adjudicate G2' toward F0 and F1's
  P2/P3/P4/D2/D3 all evaporate, leaving only D1 — which F0 also predicts. The defense F1 can
  ever mount is an ownership pedigree for the open-path reading (e.g. a minted owner tying
  neutrino coherence transfer to W_eff rather than to the feedback trace); no such owner exists.
- A1 (the CONV-2 marriage; v2-restated after the E2 kill): identifying the §08.42 resolvent
  factor 1 - zeta*r(V) as a PER-STEP retention weight is unowned; §08.42 is a pressure statement,
  not a per-step channel weight. Alternative marriages change the g(E) shape, and the v1
  sub-claim "D1 survives ANY bounded monotone marriage" is FALSE — the floorless marriage
  x = e^{-kappa V} gives exactly Lindblad m = 1 (computed control C5): D1's survival class is
  exactly the positive-floor marriages (inf x = 1 - zeta > 0). Attack: argue the physical
  marriage is floorless; then the entire memo reduces to zero discriminating content against
  Lindblad. This is now the sharpest single-point attack after A0.
- A2 (carrier applies to neutrinos at all): G2 verbatim. If the neutrino kernel lives on the
  ACTIVE branch instead (or on a different completion carrier), the entire ladder reading
  collapses; then F1's only surviving content is the generic §08.42 boundedness — which the
  frozen Hurwitz curve also respects. Attack: produce an owned quote placing neutrino propagation
  outside ker A_scene.
- A3 (iteration washing): if physical propagation composes MANY ticks with dephasing BETWEEN
  ticks, the single-monomial structure could wash into an effective exponential in L (that is
  what CONV-3 absorbs) — but if it also mixes zones per tick, the FIXED RATIOS P4 could wash too.
  Attack: exhibit an owned inter-zone mixing object; the ratio claim is the casualty.
- A4 (contamination): G5; an attacker may claim the plateau was reverse-engineered from the
  stale near-unity damping. Defense on record: the plateau is forced by owned :16 saturation +
  nilpotency, both predating; and the stale context is near-NO-damping in-window, which
  constrains nothing about tail flattening vs tail deepening.
- A5 (fragility of exactness): PUP = 0 and the single-path collapse hold on the EXACT phase
  lattice; one duplicated phase gives rho(QUQ) = 1 and destroys the finite ladder (computed
  control). If the physical carrier is only approximately U3, exact monomiality degrades —
  P2/P4 sharp claims soften into "dominant-rung" claims. The script's repeated-phase control is
  the attacker's entry point.
- A6 (convention slack): D3's specific integers move under CONV-1 vs CONV-1' ({8,10,12} vs
  {7,9,11}). Only the AP gap 2 and the GM relation are convention-free. Any presentation quoting
  4:5:6 without the convention caveat is over-claiming.

## 8. Verification

`_TASKS_CENTER_ATTACK/icecube_form_check.py` v2 — 13 PASS gates + 6 controls + the rival-route
computation, all green (exit 0):
PASS_SPLIT, PASS_NILPOTENT_LADDER (per-zone indices exactly (8,10,12); rungs k <= n-2 = (7,9,11)),
PASS_LADDER_SUM_CROSSCHECK (sqrt(3), skeptic-#2 value), PASS_SINGLE_PATH x3 (PUP = 0; unique rung
k = n-2; |t| = 1), PASS_EXPONENT_TRIPLE, RIVAL_ROUTE_ALIVE_FN (F_N = P; det(I - z F_N) = (1-z)^3;
the F0 envelope), PASS_MONOMIAL_ENVELOPE, PASS_FORM_PROPERTIES x2 bridges, PASS_DEMO_INDEPENDENCE
(FULL grid: zeta {0.05,0.3,0.6} x both bridges, 6/6), PASS_ENSEMBLE_CS,
PASS_LINDBLAD_TAIL_SPLIT x2 bridges (per-bridge numbers as quoted in D1), PASS_BIN_RATIO_DISCRIMINATOR.
Controls (each can fail the CONCLUSION, not the technique): CONTROL_ARCHIVE_BLOCK_LOOP_EMPTY
(det(I-xQUQ) = 1 — kills only the QUQ-closed-loop reading; renamed in v2, no forcing language),
CONTROL_REPEATED_PHASE_KILLS_LADDER (rho = 1.0 — the finite-ladder premise CAN fail),
CONTROL_EQUIVARIANT_VACUOUS (PUQ = 0 — the form CAN be vacuous), CONTROL_GM_GATE_CAN_FAIL
(free-ratio triple flagged at 0.18), CONTROL_PLATEAU_GATE_CAN_FAIL (calibrated Lindblad flagged),
CONTROL_FLOORLESS_MARRIAGE_KILLS_D1 (x = e^{-kappa V} => Lindblad m = 1.000000 exactly — D1
itself CAN fail; defines its survival class).
Demo constants zeta = 0.3, E*, L/L0 = 1 are NOT-OWNED and marked; every independence claim
(zeta, bridge shape, convention) is checked on the exact grid stated, not asserted.

## 9. What this does NOT show

- Does NOT derive neutrino decoherence from D0 core; F1 is a candidate FORM conditional on
  G1-G4 (two of which are inherited DRAFT-level, none Lean-owned).
- Does NOT replace, retune, or grade the frozen Hurwitz passport curve; does NOT touch the
  frozen statistic, window, or event discipline; does NOT move any registry row.
- Does NOT claim the HESE top-bin data can currently distinguish F1 from no-decoherence (in the
  recorded stale window both are near-unity); the discriminating regime is the tail above the
  (unowned) knee E*.
- Does NOT assign zones to flavors, does NOT fix zeta, E*, L0, and does NOT assert that
  U3 is THE tick carrier (selection != forcing; TICK_COUPLING_SCHUR_MEMO discipline inherited).
- Does NOT adjudicate the reading selection G2' (open-path F1 vs owned-loop F0); does NOT claim
  the open-path reading is forced (v1 did; retracted, E1); the flagship D1 is the only content
  robust to that selection.

## 10. Repair log (skeptic #1 — all accepted in full, no defense)

Verdict: NO KILL of F1 or the memo; citations verbatim-clean; independent math reproduction of
(8,10,12) indices, PUP = 0, single-path, det(I - xQUQ) = 1, GM law. One sub-claim KILLED, six
forced repairs. Errors of record:
- E1 ("forcing-of-reading"): v1 §3 Step 1 + the script's "forced reading" print claimed the
  open-path ladder was the only surviving circulation object. FALSE — the owned
  F_N = P U^dag Q U P (D0-CVFT-001A, row 130) is alive on U3, det(I - z F_N) = (1-z)^3.
  Repaired: selection language throughout; rival F0 presented with its better pedigree (§1, §3,
  A0); P2/P3/P4/D2/D3 marked reading-conditional; D1 promoted to sole flagship; G2' added.
- E2 (A1 sub-claim KILLED): "D1 survives ANY bounded monotone marriage" — counterexample
  x = e^{-kappa V} yields exactly Lindblad m = 1 (adopted as script control C5). Repaired:
  survival class restated as positive-floor marriages (inf x = 1 - zeta > 0) in §5 D1 and A1.
- E3 (fabricated-precision number): v1 D1 quoted "3e-46" — not a script output. Repaired: actual
  per-bridge outputs quoted (b=1: 0.00e+00 at float precision, -lnD = 2675.9, E_sep = 2.44 E*;
  b=1/2: 1.99e-29, -lnD = 66.1, E_sep = 10.0 E*).
- E4 (script off-by-one): "k <= (6,8,10)" in the ladder-bound print; correct bound k <= n-2 =
  (7,9,11). Fixed in script v2.
- E5 (scope over-statement): v1 PASS_DEMO_INDEPENDENCE claimed zeta x bridge coverage that was
  not the grid actually run. Repaired: full 6/6 product grid now run and stated exactly.
- E6 (ownership misstatement): v1 G1 said kappa is not owned; kappa = log phi > 0 is
  CORE-FORMALIZED (D0-IM-COSMO-003, row 160). Corrected; the COMPOSITE kappaV(E) stays unowned.
- E7 (over-claim on the frozen statistic): v1 D1 said the discriminator "maps directly onto the
  frozen HESE statistic". The frozen primary is a single top-bin count; the mapping is indirect,
  one-sided, parameter-conditional; rho(E) is a proposed secondary. Repaired in §5 D1 and G6.
- E8 (cross-ref typo): §4 pointed the stale-FAIL context note at §0/§7; correct home §0/§6 (G5).
