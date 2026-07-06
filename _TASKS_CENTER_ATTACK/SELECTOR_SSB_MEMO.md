# SELECTOR-SSB — no OWNED action/energy functional on K(9,11,13) has an extremum that spontaneously breaks S₉×S₁₁×S₁₃ and canonically selects a labeling; the four named functionals give (a) symmetric point or (b) degenerate Goldstone orbit; outcome (c) — a unique canonical broken minimizer — is IMPOSSIBLE for any functional built from the invariant adjacency A (class-function no-go). DRAFT candidate v1, pre-skeptic.

**Status:** DRAFT candidate; **no registry row edited, no cert minted, no .lean touched, no 053040 row proposed here.** Companion script `selector_ssb_check.py` — **26/26 PASS**, computed on the actual scene K(9,11,13). Pre-flight run (keywords: spontaneous symmetry breaking / SSB / ground state / vacuum / extremum / selector): **no existing row owns an "SSB selector for the within-zone labeling"**; adjacent owners cross-referenced, not duplicated (TICK_COUPLING_SCHUR_MEMO, M2_PHASE_LABELING_MEMO, D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001, D0-ARCHIVE-CONTRACTION-NOGO-001, the archive-action Lean stack).

**Honest headline:** **NO owned mechanism found.** This is the CORRECT and pre-registered-as-valid outcome for this task. The search is negative and, for the deep reason below, the negative is *structural*: it does not depend on which four functionals were tried.

---

## Claim (DEF-0.2.2 form, candidate language)

Frozen scene K(9,11,13); |V|=33, |E|=359; within-zone symmetry group **G = S₉×S₁₁×S₁₃**, acting by permutation matrices, with the adjacency matrix **A invariant under G** (the C1 vacuum contract). Let 𝓕 be any of the four OWNED functionals named in the task.

**(Y1) Class-function structure (the load-bearing lemma).** Every owned action functional 𝓕 in the corpus is assembled from G-invariant scene data: the adjacency A, the canonical Laplacian L = D−A (equivalently L_sym / L = D²), the Feshbach projectors P = proj(range A) and Q = proj(ker A), and the archive RG Laplacian chain. Consequently 𝓕 is a **G-class function** of its carrier: for any within-zone permutation g∈G and any carrier U, 𝓕(g·U·g⁻¹) = 𝓕(U). *Computed:* P and Q are G-invariant (spectral projectors of the invariant A; script `F2 Feshbach projectors P,Q invariant`), and L's spectrum is G-invariant (conjugation; `F3/F4`).

**(Y2) The trichotomy is forced.** A G-class function on the carrier space has extrema of exactly two shapes: **(a)** a G-**fixed** carrier (within-zone-symmetric — NO breaking), or **(b)** a G-**orbit** of carriers all sharing the extremal value (a degenerate, Nambu–Goldstone manifold). Outcome **(c)** — a *unique* carrier that is *not* G-fixed — is **impossible**: if U is extremal and not fixed, then every g·U·g⁻¹ (g∈G) is a distinct extremal carrier of equal value, so the minimizer is never a single non-symmetric point. This is the SSB deep trap made exact: a broken extremum of an owned action is *always* a Goldstone orbit, and picking a point on it is exactly the catalog M1 forbids.

**(Y3) The four functionals, computed on K(9,11,13).**

| functional | owner (verbatim below) | extremum | symmetry of extremum | verdict |
|---|---|---|---|---|
| **F1** archive curvature action S_N = Σ_n ρ_n | BOOK_07 §07.29; Lean `archiveCurvatureAction` | **flat archive U^flat** (S_N=0 ⟺ all-flat) | G-**fixed**; also lives on the RG phase-index chain, not on the zone-labeled graph at all | **(a)** dead |
| **F2** log-det feedback S_fb = −log det(I−zF_N), F_N=P_N U_N†Q_N U_N P_N | BOOK_03 §03.0/§03.3.2 | (i) equivariant U: S_fb ≡ 0 (flat); (ii) broken U (e.g. U₃): S_fb≠0 but **class-function** | (i) whole equivariant class degenerate; (ii) degenerate G-**orbit** of U | **(a)/(b)** dead / relocates catalog |
| **F3** heat trace Θ(u)=Tr(e^{−uL}) | BOOK_08 §08.32 | spectral invariant | G-**constant** (torsor-blind) | **(a)** dead |
| **F4** A₂ spectral action | BOOK_08 §08.32–34; Lean `HeatTraceA2Decomposition` | spectral invariant | G-**constant** (torsor-blind) | **(a)** dead |

**(Y4) The one place a break appears — and why it is (b), not (c).** Only F2 admits a symmetry-broken carrier that makes the action nontrivial: the tri-phase diagonal U₃ = diag(μ₉;μ₁₁;μ₁₃) of TICK_COUPLING_SCHUR_MEMO. On the real scene, **‖P U₃ Q‖_F = √3 ≠ 0** (feedback fires) and **S_fb(U₃) = 2.079442 ≠ 0** (computed). But conjugating U₃ by any g∈G leaves S_fb **exactly invariant** (`orbit spread = 8.9×10⁻¹⁶`) while producing a **distinct** carrier (`orbit is nondegenerate as a SET`). So the broken "minimizer" is a full G-orbit — a Goldstone manifold — and selecting a point on it is picking a labeling: **the M1 catalog, relocated, not escaped.** Moreover U₃ is not even owned (TICK S2: "μ_n-as-diagonal-operator is not a greppable owned object").

**(Y5) Is the orbit owned-quotiented? (the only escape hatch — it is not.)** A legal SSB would survive (b) if the degenerate manifold were *itself* an owned quotient — e.g. if the G-orbit coincided with the M2 Q₈-typed torsor and the residual freedom were the owned G_res. It does not, for two computed reasons: (i) the F2 orbit is the *full* S₉×S₁₁×S₁₃ within-zone relabeling torsor (the graph-slot torsor), which M2 X4 identifies as *exactly the un-owned datum* C1 forbids resolving; (ii) the M2 owned quotient lives on the **detector-layer pointed shell V₉ = Ω₈⊔{ω₀}, not on the graph slots** (M2 W2a), and it is **Q₈-typed with exponent 4 — it has no order-9 (μ₉) element** (M2 X2), whereas the F2 break that fires the action is exactly the μ₉/μ₁₁/μ₁₃ *cyclic* pattern that M2 X2 proves is **impossible** from owned data. The action-firing break and the owned quotient are *disjoint objects*: the break the action can see is not owned; the labeling that is owned does not fire the action. Owned-quotienting the orbit therefore fails.

---

## The deep trap, confronted head-on (the crux)

Physics SSB replaces "symmetric, no selector" with a **degenerate vacuum manifold**. The task's warning is that picking a point on that manifold is the *same* catalog problem M1 forbids (Nambu–Goldstone). **Result: every owned functional falls into exactly this trap, and it is unavoidable — not an accident of the four choices.** The reason is Y1+Y2: an owned action is a *class function* of G because it is built from the G-invariant A. A class function cannot have a unique non-symmetric minimizer. So the two live outcomes are:

- **(a)** the extremum is G-fixed → no breaking → no selection (F1, F3, F4, and F2's equivariant class);
- **(b)** the extremum is a G-orbit → breaking, but degenerate → the catalog is *relocated to the choice of point on the orbit* (F2's broken carrier).

Outcome **(c)** — a unique canonical broken minimizer — would require an action that is *not* a class function of G, i.e. an action built from data that is *not* G-invariant. But any such datum is a privileged within-zone vertex/labeling, which is precisely the exogenous parameter C1/M1 forbid. **The SSB route to a selector is closed by the same contract (C1) that made the labeling un-owned in the first place.** SSB does not add a new escape; it re-expresses the M1 obstruction as the degeneracy of the vacuum manifold.

---

## Owned pre-facts (verbatim, file:line — each VERIFIED to exist on disk this session)

1. **Archive action definition** — `01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md:1093-1094`: "and the finite archive action / `S_N = sum_{n < N} rho_n.`" With `:1088` "`rho_n = sum_{i,j} C_n(i,j)^2,`" and `:1082` "`C_n = L_{n+1} B_n - B_n L_n.`"
2. **Archive-action minimum = flat, Lean-proved** — `:1097`: "The proved Lean facts are: `rho_n >= 0`, `rho_n = 0` iff operator transport is flat, `S_N >= 0`, and `S_N = 0` iff every included refinement step is flat." Confirmed in source (not build artifact): `09_LEAN_FORMALIZATION/D0/Geometry/ArchiveActionFunctional.lean:18-20` `theorem archiveCurvatureAction_zero_iff_all_flat (N : Nat) : archiveCurvatureAction N = 0 ↔ ∀ n < N, OperatorTransportFlat n`, and `:11` `theorem archiveCurvatureAction_nonnegative`. `OperatorTransportFlat` = `seamCommutator n = 0` (`ArchiveSeamCurvature.lean:29-30`).
3. **Flat is the cycle-free minimum / vacuum = stationarity** — `BOOK_07:1116-1117`: "The vacuum equation is stationarity of the seam action against all admissible finite Laplacian variations"; `:1140-1145`: "the flat reference `U^flat` is the cycle-free minimum … the seam-action vacuum equation is exactly the discrete `K=0 ⟺ ϱ=0` statement (`b=0`, no closures ⇒ flat)."
4. **The archive action lives on the RG phase-index chain, not the zone-labeled graph** — `ArchiveSeamCurvature.lean:13-27`: seam transport built from `archiveCanonicalLaplacian` on `archivePhaseIndex n` (the coarse-graining chain), no S₉×S₁₁×S₁₃ carrier appears.
5. **Log-det feedback action + variation** — `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md:27` "`S_fb = -log det(I - z F_N)`"; `:34` "`delta S_fb = Tr[(I - z F_N)^(-1) z delta F_N]`"; `:221` "`F_N=P_N U_N^dagger Q_N U_N P_N` is feedback-return"; `:1116-1117` the bootstrap "`\delta\mathcal B_N=0` locks finite spectral geometry to feedback-return thermodynamics."
6. **Heat trace / spectral action use the graph-canonical (G-invariant) Laplacian** — `01_BOOKS/BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md:678`: "The dynamic survey transfer, Weyl dimension scaling, and spectral action stability certificates use the phase-canonical Laplacian operator derived from the cyclic phase-distance metric"; `:758` "`heat-trace A2 decomposition / EH proxy | CORE-CLOSED | D0.Geometry.HeatTraceA2Decomposition.heat_trace_sq_exact_decomposition`."
7. **C1 vacuum contract (the class-function root)** — `01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md:1570` (verified verbatim on disk): "**(C1) Exchangeability.** No permutation inside a part may change the physics, i.e. the adjacency matrix `A` is invariant under `S9 × S11 × S13`. A part-internal exception would name a privileged vertex — an exogenous parameter — violating M1." Strengthened at `:1576`: "From **(C1)**, `A` is constant on the orbits of `S9 × S11 × S13`" — i.e. A is literally a G-invariant, the root of the class-function lemma Y1.
8. **R1 commutant (equivariant carriers cannot couple P↔Q)** — `05_CERTS/vp_root_r1_representation_reconstruction.py:2` (verified on disk): "Aut(K(9,11,13))=S9xS11xS13 perm rep on C^33: isotypes 3 trivial + std9/11/13 (8,10,12); commutant dim=3^2+1+1+1=12". No trivial↔std cross-block ⇒ every equivariant U has PUQ=0.
9. **Staticity of the carrier under U_N** — `01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:425` (verified): "The global state of the finite holographic carrier is static under the unitary `U_N`." (Feshbach split is rank-3/nullity-30, same line.)
10. **The break that fires the action is un-owned** — `TICK_COUPLING_SCHUR_MEMO.md:93-94`: "**mu_n-as-diagonal-operator is not a greppable owned object**"; and `:38-46` U₃ fires with nilpotent index 12. Cross-owned: M2_PHASE_LABELING_MEMO X2 (`:53-68`) — canonical μ₉ labeling of V₉ IMPOSSIBLE (Q₈ exponent 4); X4 (`:79-83`) — graph-slot transport is exactly the un-owned torsor datum C1 forbids.

---

## The construction (every load-bearing quantity computed, script `selector_ssb_check.py`)

- Scene rebuilt exactly: |V|=33, |E|=359, degrees {24,22,20} by zone; C1 verified (A invariant under 200 random within-zone relabelings).
- **F3/F4 (spectral invariants):** spectrum of L identical after a random G-relabeling; Tr L = 718, Tr L² = 16426 identical after relabel; Θ(u) torsor-constant. ⇒ **(a)**, computed.
- **F1 (archive action):** flat step gives ρ=0 (the minimum), any bend gives ρ>0 (strict min, `NC4`); minimizer is the flat reference, G-fixed. ⇒ **(a)**.
- **F2 (log-det feedback), real scene:** Feshbach split rank(A)=3, dim ker=30 (exact). (i) equivariant U (polynomial in L): **‖PUQ‖ = 2.5×10⁻¹⁵ ≈ 0** ⇒ F_N=0 ⇒ S_fb ≡ 0 across the whole equivariant class (swept, `NC2`). (ii) broken U₃: **‖P U₃ Q‖_F = √3**, **S_fb = 2.079442 ≠ 0**; conjugation by 30 random g∈G leaves S_fb invariant to 8.9×10⁻¹⁶ (**degenerate orbit**) while the carrier changes (**nondegenerate set**). ⇒ **(a)** on the equivariant class, **(b)** on the broken carrier.
- **Cross-links confirmed computationally:** U₃ = the TICK memo's tri-phase carrier (fires the tick, breaks all three zone symmetries); its zone-9 μ₉ factor is exactly M2 X2's forbidden cyclic labeling.
- **Negative controls (each can fail the CONCLUSION):** NC1 — a per-slot (C1-forbidden) readout DOES vary over the orbit (proves the *technique* can see breaking; the *owned action* cannot — the class-function property is a fact about the action, not a blindness of the test). NC2 — PUQ=0 across a sweep of equivariant U (regime-(i) vacuity not a fluke). NC3 — a non-conjugation perturbation DOES change the spectrum (F3/F4 invariance is genuine, conjugation-specific). NC4 — every bend raises S_N (flat is a strict minimum, so F1's (a) is not vacuous).

---

## Cross-links (adjudicated)

- **TICK_COUPLING_SCHUR_MEMO (U₃, within-zone breaking required).** This memo *confirms and generalizes* the tick memo's finding: the tick fires only on within-zone-broken carriers, and the log-det action is *identically flat* on the equivariant class. New content here: the break is a **degenerate G-orbit** (outcome b) for the action too, so "carrier selection" is not resolved by extremizing the owned action — it is exactly the un-selected orbit. Consistent with TICK's own "selection ≠ forcing."
- **M2_PHASE_LABELING_MEMO (Q₈ torsor).** The degenerate F2 orbit does **not** coincide with the M2 owned quotient: M2's quotient is on the detector-layer shell V₉ (not graph slots), is Q₈-typed (exponent 4, no μ₉), and is forced up to G_res; the F2 action-firing break is the graph-slot μ₉/μ₁₁/μ₁₃ pattern M2 proves un-owned/impossible. **The owned quotient and the action-visible break are disjoint objects** — so the "owned-quotiented manifold" escape from (b) fails (Y5).
- **D0-ARCHIVE-CONTRACTION-NOGO-001 / R2.** F1's flat-minimum result is consistent (the archive vacuum is flat, U^flat); no contradiction, no demotion.

---

## What this does NOT show / limitations

- Does **not** claim SSB selectors are impossible for an *external* owner (a passport catalog can always name a point on the orbit — that is the M1 catalog, stated as such).
- Does **not** prove the class-function lemma (Y1) as a formal theorem over *all conceivable* owned functionals — it proves it for the four named and gives the C1-based structural argument for why *any* A-derived functional inherits it. A functional built from genuinely non-G-invariant owned data would evade Y1 — but no such datum exists per C1 (that is the whole point; the reopening hook is exactly "produce an owned G-non-invariant datum").
- Does **not** adjudicate BOOK_06 §06.8.F staticity binding (TICK S1'); F2's U₃ is a candidate carrier, not a typed theorem, and its un-ownedness (pre-fact 10) is independent of that.
- Does **not** edit/demote any CERT-CLOSED row, any .lean, any 053040 row, or the two cross-linked memos.

---

## Falsification / reopening hooks

1. **Produce an owned functional NOT built from the G-invariant A** (or an owned G-non-invariant per-vertex datum). Y1 fails for it and (c) becomes possible. Script control: `NC1` shows what a G-non-invariant readout looks like — the task is to find one that is *owned*. (C1 says none exists; this is the load-bearing bet.)
2. **Show the F2 broken orbit coincides with the M2 Q₈ torsor** (owned-quotient the manifold). Refuted here by Y5 (disjoint objects, computed), but a reading that transports the detector-shell quotient onto graph slots *and* survives M2 X4's non-invariance would reopen (b)→legal. This is the same graph-bridge C1 forbids; reopening it means overturning C1.
3. **An owned selector inside the degeneracy** (a super-selection rule from owned data that picks one point of the G-orbit). None found; this is definitionally the catalog M1 forbids, but a genuinely internal owned tie-breaker would be outcome (c) in disguise — the hook is to exhibit one.

---

## Named risks & PRE-REGISTERED attack surface (strongest self-attacks first)

- **R1 (strongest): is Y1 (class-function) really forced, or did I only test four functionals?** The four are class functions by direct computation. The *generalization* rests on C1 (pre-fact 7): any owned action is A-derived, A is G-invariant, so the action is G-equivariant in its carrier, hence a class function. The attack surface is precisely "an owned functional whose construction inputs a G-non-invariant object." I claim none exists (C1); if the skeptic names one that is genuinely owned, Y2 collapses and (c) reopens. Pre-registered concession: Y1 is a structural argument, not a Lean theorem over all functionals — its strength is exactly C1's strength.
- **R2: the F2 regime-(i) PUQ=0 relies on U being in the commutant.** For a *unitary* equivariant U this is R1-cert + BOOK_06 staticity (pre-facts 8,9). My equivariant witnesses are polynomials in L (self-adjoint, commutant), giving PUQ=0 exactly (2.5e-15). A non-normal equivariant U still has no trivial↔std block, so PUQ=0 holds for the whole commutant (dim 12, no cross-block) — swept in NC2. Attack: a G-equivariant U *outside* the polynomial-in-L family but still in the commutant — covered, since the commutant has no P↔Q cross-block by R1.
- **R3: could a DIFFERENT owned functional (not among the four) break the pattern?** E.g. the CVFT statistical sum Z_D, the partition Z_N, the diagram sum 𝒵_k. Each is either (i) a spectral/class function of the same invariant operators (Z_N = Tr e^{−βΔ} det(I−zF)⁻¹ — both factors class functions), or (ii) a diagram/geometry code-length sum A(G,J) that scores *geometries up to iso*, hence G-invariant by construction. Pre-registered: I did not exhaustively enumerate every action symbol in the corpus; the class-function argument (Y1) is the claim that covers them, and its single failure mode is R1.
- **R4: the "degenerate orbit" reading of (b) assumes G acts freely enough that the orbit is nontrivial.** If U₃ were G-*fixed* the break would be spurious. Computed against: the orbit is a nondegenerate SET (distinct carriers), and U₃ is manifestly not G-fixed (its per-slot phase pattern is permuted by g). So (b) is genuine, not (a) in disguise.
- **R5: F1's minimizer uniqueness.** S_N=0 ⟺ all-flat gives a unique *action value* (0) but the flat *carrier* could be non-unique. It does not matter for this memo: any flat carrier is G-fixed (built from the canonical chain), so even a non-unique flat set is within outcome (a) — no within-zone breaking. The claim is "(a), no selection," which is robust to flat-set multiplicity.
- **R6: model-completeness of the "owned functionals" sweep** — same shape as M2 A6. If the corpus owns an action functional I did not locate that is NOT A-derived, R1/R3 reopen. The three cited symbols (S_N, S_fb, Θ/A₂) plus the CVFT bootstrap 𝓑_N are the greppable action layer; a missed one is the reopening hook.
