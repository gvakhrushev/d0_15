# TASK W6 — T2′: the E₀-block restriction and what the X5 lepton contract actually postulates

**Goal:** T2 (witness-extension) failed its scope gate (W3 report) but exposed the correct object:
the 7-point no-go carrier is the **restriction of the (1,4,3) Q₈-Fourier system with the rank-1
trivial-rep block E₀ removed**, and E₀ *is* the unramified electron entry, already declared
"exact and THE" elsewhere in the corpus. This task pins down: (a) where and why the restriction
(1,4,3) → (4,3) enters the no-go chain, (b) what exactly `D0-X5-LEPTON-CONTRACT-001` still
postulates once the full (1,4,3) system is used, and (c) whether the residual gap reduces to the
block↔generation identification.

**Repo:** `/Users/grigorijvahrusev/Downloads/d0_15/`
Prior work to read first: `_TASKS_CENTER_ATTACK/TASK_W3_REPORT.md` (provenance + prior-art sections),
`TASK_W2_REPORT.md` (the 8-point construction and its honest OPEN list).

## Context (self-contained)

- `ℂ[Q₈] ≅ ℂ⁴ ⊕ M₂(ℂ)` gives three orthogonal idempotents E₀,E₄,E₃ with ranks (1,4,3);
  `Q8Terminal.lean` fixes `Q₉ ↔ E₀ (rank 1, unramified)` = electron; `UnifiedTheorem.lean:31–36`
  says the branch orders (1,4,3) appear simultaneously in the Q₈ Fourier ranks and the return orders;
  `LeptonPuiseuxUniquenessObstruction.lean:73` declares the row (electron 0, muon 1/4, tau 1/3)
  "exact and THE".
- Yet the pigeonhole no-go (`LeptonBranchFixingNoGo.lean`) freezes the carrier as the 4+3=7
  *nontrivial return cycles* only, proves 2 orbits < 3 generations, and posts the third branch as an
  external postulate (`D0-X5-LEPTON-CONTRACT-001`).
- Tension to resolve: if the (1,4,3) row is already THE, what is the X5 postulate FOR? Hypothesis
  (T2′): the true residual gap is not the *existence* of the third branch (it exists internally as
  E₀) but the *identification* of the Q₈-side triple (1,4,3) with the scene-side generation triple
  (Tr(T²)=3, `D0.Matter.PhasonStrainGenerations`) — two independent "3"s needing a forced map.

## Steps

1. **Exact content of the X5 contract:** read `09_LEAN_FORMALIZATION/D0/Extensions/X5/Lepton.lean`
   (and any `D0-X5-LEPTON-CONTRACT-001` prose in `01_BOOKS/BOOK_04*` / `04_VERIFICATION/`). Write out
   verbatim: what is postulated (an object? a map? a number?), its stated non-vacuous model, and its
   axiom-deletion minimality argument. Determine: does the postulate assert the *existence* of an
   electron branch, or the *assignment* of branches to generations, or both?
2. **Where the restriction enters:** trace the chain `Q8Terminal.lean` → `UnifiedTheorem.lean` →
   `Representation/TypedRepresentationFunctor.lean` → `LeptonClosure/BranchRowMinimalExtension.lean`
   (`blockRanks := [1,4,3]`, `exponentRow := [0,1/4,1/3]`) → `LeptonSelectorExtension.lean`
   (`orbitSizes = [4,3]`) → `LeptonBranchFixingNoGo.lean`. Identify the exact file/line where the
   rank-1 block is dropped and the stated reason (if any). Classify the reason: FORCED (a derivation
   is cited) / CONVENTION (a choice with no derivation) / SILENT (no reason recorded).
3. **Does the no-go still bite the full system?** Restate the no-go's three pigeonhole questions for
   Branch(3) = {E₀,E₄,E₃} vs Gen(3): cardinality now admits a bijection, and sizes (1,4,3) are
   pairwise distinct so the size-keyed map {1↦gen_e, 4↦gen_μ, 3↦gen_τ}-style assignment is label-free
   on the Q₈ side. What survives: is there any *scene-side* structure that distinguishes the three
   generations of `PhasonStrainGenerations` (beyond count 3)? If the scene-side triple is
   rank-only/S₃-symmetric (`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001` says the 3
   generations carry GL(3)/S₃ label-freedom), then the residual gap is exactly: **no canonical map
   between an intrinsically-ordered triple (1,4,3) and an unordered triple (3 generations)** — which
   is a *naming* freedom, not an existence gap. Verify or refute this reading with citations.
4. **Minimality re-test:** if step 3 confirms the reading, assess (do not enact): would the X5
   contract's content reduce from "postulate the third branch" to "postulate the Q₈-triple ↔
   scene-triple identification" — a strictly weaker postulate? List which Lean files/claims would be
   touched by such a re-scope, as a plan only.
5. Write `TASK_W6_REPORT.md`: (a) verbatim X5 content; (b) restriction locus + classification
   (FORCED/CONVENTION/SILENT); (c) what survives of the no-go against Branch(3); (d) the residual-gap
   statement in one sentence; (e) skeptic's paragraph: strongest reason T2′ is still wrong.

## Acceptance criteria

- Every verdict carries file:line citations; the FORCED/CONVENTION/SILENT call is explicit.
- No edits outside `_TASKS_CENTER_ATTACK/`; no status/claim language ("derived", "confirmed") in the report.
- The report ends with the skeptic's paragraph even if the overall reading favors T2′.
