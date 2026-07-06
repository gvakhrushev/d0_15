# W4_DECOMPOSITION_MEMO — T4 "Missing-object=Decomposition" for the remaining candidates (DRAFT v2, post-skeptic-#1)

> **Post-skeptic banner (2026-07-06, verdict ACCEPTED IN FULL, no defense):** T2A and T4 SURVIVE;
> T1 and T2B were WOUNDED-fixable (ownership mis-attribution; one vacuous check) — all repairs applied
> below; **T3 was KILLED down from DECOMPOSED-CONDITIONAL to HONEST-BLOCKED via the memo's own
> pre-registered ATT-1 tripwire**: the owned branch semantics of THE-A is RETURN-WINDOW-conditional
> (`BOOK_01:1403`: the tick sequence "turns ... into a branch foliation whenever an integer pair (q,m)
> satisfies |q−mτ|≪1") and the downstream windows 20, 8, 4 fail that precondition exactly (best defects
> 8/7, 12/7, 16/7 against τ₀ = 44/7 — check T3.9). Verdict + errors of record at §W4.SKEPTIC.
> **No closure language anywhere in this memo is operative.**

**Status:** DRAFT v2; no registry row edited; no book edited; no `.lean` added; `053040` untouched.
Deliverables: this memo + `_TASKS_CENTER_ATTACK/w4_decomposition_check.py` (**36/36 PASS, rc=0**, exact
int/Fraction arithmetic only; count printed by the script's own counter; **mutation-tested: 11/11 planted
mutations fail** — 7 pre-skeptic + 4 on the repaired checks, identities logged in §W4.SKEPTIC to close the
skeptic's mutation-log gap; one check — T2A.6 — additionally fired organically during authoring on a real
indexing error `F(2n+1)` vs `F(2n+3)` and was repaired against the computation, not the other way round).

**Pre-flight (trap (e)):** `preflight.sh INDUCTIVE-SPECTRAL-TRIPLE` + direct registry greps for all six
claim-ids. Cross-references found and honored — NOT duplicated: the set/kernel-level co-tower of Target 1
is ALREADY owned by `D0-ARCHIVE-TOWER-001` (row 24, CORE-FORMALIZED — module owner of
`D0.Geometry.ArchiveRefinementTower`) and `D0-ARCHIVE-LIGHTPROFINITE-001` (row 271, CORE-FORMALIZED,
LEAN_PROVED). ~~row 412~~ struck by skeptic (EoR-W4-1): `D0-CANONICAL-RENORMALIZATION-SPECTRAL-TOWER-001`
owns the Fibonacci **Bratteli** tower — a DIFFERENT object from the archive co-tower. This memo adds the
expectation-layer computation on top; it does not re-own the co-tower.

**Calibration honored (GAP_E §SKEPTIC-#1):** every totality scan below quantifies over the claim's ACTUAL
domain and says so inline (T2A.5 closes the Lean row's bounded `N ≤ 3` quantifier by a checked recurrence;
T3.6/T3.7 scan ALL seeds 1..10000 with the bound stated; T4.4 enumerates ALL 8 and ALL 9 maps). No prune
is done via a docstring beyond its scope. Traps (k)-(o) addressed inline where they bite ((m) at T1.10-11
and T3.7; (d) at T3; (o) at T3.3).

---

## Target 1 — D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001 (PROOF-TARGET, nogo_flags)

**T4 candidate under test:** read the tower CONTRAVARIANTLY — the "only downward projections exist"
obstruction becomes: the downward system IS the object (co-tower / projective system).

### Owned pre-facts (verbatim, verified on disk)

- Registry row 414 (`CLAIM_TO_LEAN_MAP.csv:414`): "the corpus realizes the tower as an INVERSE limit of
  downward projections (D0-ARCHIVE-LIGHTPROFINITE-001). EXACT MISSING ARTIFACT: an isometric J_N with
  Dirac compatibility, firewalled to ASSUMP-CONNES-RECONSTRUCTION / Latremoliere propinquity".
- `09_LEAN_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean:96-97`: "The base-level archive kernel is
  the equality kernel. Higher kernels are intentionally defined by pullback, giving exact projective
  compatibility." — and `:121-127` `archive_laplacian_projectively_compatible` closes by `rfl`.
- `ArchiveLightProfinite.lean:25-27`: the tower is a genuine `ℕᵒᵖ ⥤ FintypeCat` functor
  (`Functor.ofOpSequence`, bonding = `archiveProjection`), packaged as a `LightProfinite` (`:57-58`).
- `ArchiveRefinementTower.lean:67-71`: `archiveProjection n : Fin (modes(n+1)) → Fin (modes n)`,
  `x ↦ x % modes(n)`, `modes(n) = (n+2)^4`; surjective (`:73-82`).

### Computed (w4_decomposition_check.py T1.1-T1.12; all exact)

1. **The owned downward maps form a genuine projective system.** Bonding surjectivity re-verified by full
   image scans (T1.2); composition closes by the `ofOpSequence` construction (unique successor path on ℕ,
   no extra coherence obligations); the kernels Δ, G are compatible along COMPOSITES by a full 256²-pair
   scan at level 2 (T1.3). Compatibility is non-vacuous: the rival "direct mod" family
   `A_2 → A_0, x ↦ x mod 16` FAILS it (witness x=100: direct gives 4, composite gives 3 — T1.4).
2. **What the limit-free co-tower content owns (post-skeptic corrected attribution):** surjective bonding
   + nonempty inverse limit are registry-owned by row 24 `D0-ARCHIVE-TOWER-001` (theorem list includes
   `archive_projection_surjective; archive_tower_defines_profinite_object; inverseLimit_nonempty`);
   LightProfinite packaging by row 271. The exact pullback-compatibility theorems
   `archive_covariance_projectively_compatible` / `archive_laplacian_projectively_compatible`
   (`ArchiveRefinementTower.lean:116-127`, rfl-grade) live in row 24's MODULE but **appear in NO row's
   theorem list** (registry grep count: 0) — **registry-unregistered theorems, flagged as a hygiene item
   for integration**. Row 271 carries its own scope caveat, reproduced verbatim: "Nonemptiness is the
   established sibling archive_tower_defines_profinite_object (inverseLimit_nonempty); transferring it
   onto the Mathlib limit point (forget_preservesLimits + nonempty_sections_of_finite_cofiltered_system)
   is a named follow-on theorem-target." — i.e. nonemptiness ON the Mathlib LightProfinite object is a
   named follow-on target, NOT owned.
3. **The conditional-expectation upgrade of the reading is NOT free.** Fibers of `archiveProjection` are
   non-uniform (census: sizes {6×1, 5×15} at n=0, T1.5), hence:
   - the canonical uniform measures are NOT projectively compatible (pushforward = {6/81, 5/81,...} ≠ 1/16,
     T1.6), while the same check PASSES on a divisible control tower (T1.7, T1.9) — the failure is the
     structure's, not the technique's;
   - uniform fiber-average expectations do not compose coherently: `E_0∘E_1 ≠ E_composite` (T1.8);
   - the exact intertwining that DOES hold is `E_n · Δ_{n+1} · U_n = Δ_n · W_n` with `W_n` = the
     fiber-multiplicity diagonal (T1.10-11). **Trap (m) pinned:** this identity holds for any pullback
     kernel along any surjection; its sole content is the ATTRIBUTION — the defect from strict
     compatibility is exactly a fiber-multiplicity (capacity-type) diagonal weight.
   - the covariant candidate is arithmetically dead without external input: `U_n† U_n = W_n ≠ c·I`
     (sizes 5 ≠ 6), and per-fiber normalization would need `|fib|² = |fib|`, i.e. all fibers singletons
     (T1.12) — an exact-integer strengthening of the no-go, not a parametrization artifact (trap (g):
     the regulator here is the owned `modes(n)=(n+2)^4`, and consecutive fourth powers are never
     divisible, `gcd(n+2, n+3)=1`, so NO reparametrization of the owned tower makes fibers uniform).
4. **Is there owned text typing the tower as necessarily-upward?** No. Sweep of BOOK_07: the inductive
   spectral triple is typed EXTERNAL — `BOOK_07:74`: "The frozen Fibonacci AF/GNS tower can be tested
   against an external quantum-metric formalism (Lip-norm, propinquity, inductive spectral triple)";
   `BOOK_07:1057`: "The continuum metric is admissible only if the family is projectively compatible";
   `BOOK_07:1370` THE 07.33.1 works with "a κ-stable inverse system". The upward demand comes only from
   the external Connes/propinquity passport (rows 414/418), never from owned text.

### Verdict: **DECOMPOSED-CONDITIONAL(reading)** — held after repairs, on the corrected ownership base

The co-tower reading is correct and ALREADY owned at the set/kernel level (rows 24+271, with the two
compatibility theorems registry-unregistered as flagged above — the "missing object" was never missing in
that variance). The genuinely new layer this wave adds — the compatibility-FAILURE layer — has a nearest
owned neighbor the pre-skeptic draft missed: row 41 `D0-ARCHIVE-LAPLACIAN-RG` ("Nearest-neighbor phase
Laplacian is not strictly projective; RG residual/curvature obstruction is tracked by scale-fit cert",
Lean `rg_curvature_zero_iff_exact_compatibility`) — this wave's T1.6/T1.8 uniform-weight incoherence is a
sibling of that owned obstruction layer, cross-referenced not re-owned. The conditional-expectation
co-tower exists ONLY conditional on a projectively-compatible weight/measure family, and the canonical
(uniform) family provably fails — the residual missing object, stated exactly, is **a canonical
projectively-compatible weight family on the archive tower (equivalently: a canonical choice among the
non-uniform fiber weights `W_n`)**. Row 414's PROOF-TARGET status is UNCHANGED and stays OPEN: the
isometric Dirac-compatible `J_N` is not dissolved by the reading; it is re-typed as a wrong-variance
demand whose exact defect is the capacity diagonal `W_n`. No promotion proposed.

---

## Target 2 — the two T4-classified cluster-C/E/F/I no-gos

### 2a. D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 — candidate: "AF tower = independent owned layer"

**Ownership citation (verbatim):** row 412: "The present core DOES contain a canonical
renormalization/refinement tower at the ALGEBRA+TRACE+SCALE level ... It does NOT contain a canonical
inductive SPECTRAL-TRIPLE tower". Row 423: "the recovered AF tower is a correct FORMALISM object but NOT
the inductive completion of the D0 Laplacian dynamics". The two-layer decomposition (owned
algebra+trace+scale layer ⊕ external Dirac/isometric layer) is therefore VERBATIM registry-owned already.

**Computation (T2A.1-T2A.6):** dims 2,5,13,34,89,233 rebuilt independently from the path-count recurrence;
33 = 9+11+13 = 1+12+10+8+2 both ways; and — the substantive gain — the 33-skip is made **TOTAL**: the Lean
theorem `laplacian_tower_compatibility_no_go` (`AFD0LaplacianComparisonNoGo.lean:40-46`) quantifies only
`∀ N, N ≤ 3`; the script closes ALL N via the checked recurrence identity
`dimA(n+1) − dimA(n) = a(a+2b) > 0` (T2A.3-4) plus `dimA(3)=34>33` (T2A.5), and the typed separator
`dimA(n) = F(2n+3)` (odd-indexed Fibonacci; 33 is not one — T2A.6).

**Verdict: DECOMPOSED-OWNED.** The decomposition needs no new reading — it is printed in rows 412/423; the
wave's contribution is the totality closure of the 33-skip. **Named Lean lift candidate (not forged
here):** `dimA_strictMono` + unbounded `∀ N, dimA N ≠ 33` — a one-lemma upgrade of the `N ≤ 3` quantifier.

### 2b. D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001 — candidate: PRIM-ISOMETRIC-J_N = scale ⊕ comparison layers

**Ownership citation (verbatim):** row 427: "a Dirac-compatible tower requires BOTH a forced scale law
(scale underdetermined, Outcome C) AND a canonical comparison map Xi_N (obstructed, Outcome D). The single
primitive splits into +2 independent primitives." — the split is verbatim registry-owned.

**Computation (T2B.1-3, post-skeptic relabel):** the scale witness pair is genuinely distinct in exact
ℤ[φ] pairs (`φ^N = F(N−1)+F(N)φ ≠ (2^N, 0)` for N=1..20, no float, trap (h) avoided — T2B.1). The
skeptic's repair replaced a vacuous `list == itself` check (EoR-W4-3) with an explicit variation: the
joint object `(scale_N, dim_N)` is varied over the witness pair; dim components are invariant, scale
components differ at every level, and the 33-skip persists under both choices (T2B.2-3). **Honesty
label:** that `dimA` takes no scale input is DEFINITIONAL BOOKKEEPING of the owned formalization
(`FibonacciAFAlgebra.lean:23-28` — `pc`/`dimA` have no scale parameter); the checks EXHIBIT the
variation, they do not prove independence beyond what the owned definitions carry. ~~"independence
verified, not assumed"~~ struck.

**Verdict: DECOMPOSED-OWNED (with bookkeeping relabel)** — the registry text (row 427) is the owner of
the split; the computation exhibits the two layers varying separately at the strength the owned
definitions support, no more.

---

## Target 3 — sweep-frontier (b): PHASE-TOWER-002 shell-2

**Pre-check demanded by the task:** what do M2 v2 + the registry own about "shell 2"?
- `M2_PHASE_LABELING_MEMO.md:1` — M2's object is "the DETECTOR-LAYER pointed shell V₉ = Ω₈ ⊔ {ω₀}" (a
  9-object pointed set). Registry row 543 same. **This is a DIFFERENT object** from PHASE-TOWER-002's
  `shell` field (a ℕ-valued capacity counter initialized at `V11n = 11`, `PhaseTower.lean:27`). M2 owns
  NOTHING about the capacity shell value 2 (disambiguation check T3.8). No conflation.
- Registry row 23: "Formal tower exists but current terminal recursion stabilizes; direct Einstein tower is
  not derived here." Lean: `current_recursion_stabilizes_at_shell_two` (`InfinitePhaseTower.lean:142-146`),
  `capacity_shell_stable_from_four` (`ArchiveRefinementTower.lean:32-39`) — totality for n ≥ 4 owned.

### Computed (T3.1-T3.9)

- Owned chain, exact: shells `11 → 20 → 8 → 4 → 2 → 2 → …`, windows `44, 20, 8, 4, 4`; stabilization
  depth 4; terminal window `4 = |ABCD|`.
- **The candidate reading (KILLED at the terminal step — see banner and T3.9):** BOOK_01:1615 (THE-A,
  owner): "Terminal window `q_T = ABCD · V11 = 4·11 = 44`; admissible branches form the unit group
  `G = (ℤ/44)*` with `|G| = φ_E(44) = 20 = d13`." The unit-group reading of the totient step is OWNED
  at the 44-instance, and `φ(q) = |(ℤ/q)*|` is theorem-grade arithmetic (trap (o): Mathlib
  `ZMod.card_units_eq_totient`). **BUT the skeptic's trap-(l) read-past found the owned PRECONDITION the
  draft skipped:** `BOOK_01:1403` — the tick sequence "turns the one-dimensional tick sequence into a
  branch foliation whenever an integer pair (q,m) satisfies |q−mτ|≪1. The residue classes modulo q are
  the coherent branches." The branch/unit-group semantics is owned ONLY for RETURN windows. The owned
  returns are 44 (first: `BOOK_01:1393` "first nontrivial stable return 44≈7τ_0"; exact for the
  surrogate τ₀=44/7) and 710 (second: `BOOK_01:1436-1439`). The downstream windows FAIL the
  precondition, exactly (T3.9): best defect `|q − m·τ₀|` = **8/7** at q=20, **12/7** at q=8, **16/7** at
  q=4 — none ≪ 1. The terminal window 4 is NOT an owned return window, so "terminal shell =
  |(ℤ/4)*| = sign dyad" imports branch semantics where the corpus doesn't grant it.
- **Anti-over-read guards (both computed):**
  1. (trap (m)) The VALUE 2 is a **universal totient attractor**: unique fixed point of
     `s ↦ φ(lcm(4,s))` in 1..10000 (T3.6) and EVERY seed 1..10000 reaches it (T3.7). So "stabilizes at
     shell two" carries zero scene-specific information in its terminal value; the scene content lives in
     the owned seed 11 = V11n, the owned weld φ(44) = 20 = d13, and the depth-4 path.
  2. (trap (d)) The numeric echoes `8 = |Ω₈|, 4 = |ABCD|, 2 = |D₂|` along the chain are NOT claimed as
     construction: no owned text identifies `(ℤ/4)*` with the D₂ dyad or the Ω₈ sign bit, and the roles
     as a group are `Q₈/Z ≅ V₄`, not ℤ/4 (GAP_E S-5) — the cyclic structure belongs to the WINDOW
     (owned as a return-window, BOOK_01:1393/1423), not to the roles.

### Verdict: **HONEST-BLOCKED** (post-skeptic re-grade; ~~DECOMPOSED-CONDITIONAL~~ killed via ATT-1)

The pre-registered ATT-1 tripwire fired exactly as written: owned text (found by reading past the THE-A
citation, trap (l)) restricts the branch semantics to return windows, and the terminal window 4 fails the
owned `|q−mτ|≪1` precondition by exact arithmetic (16/7). The missing objects, stated exactly (WIDENED
per the skeptic):
1. **an owned clause extending branch/unit-group semantics to non-return lcm-windows** (without it the
   totient step at q ∈ {20, 8, 4} is arithmetic bookkeeping, not branch structure), AND
2. **an owned clause identifying the terminal-window unit action {±1 mod 4} with an owned sign/dyad
   role-object ({±} of Ω₈ or D₂)** — the residue already named pre-skeptic.

**What survives (computed, reusable, NOT closure claims):** the exact chain 11→20→8→4→2 with windows
44,20,8,4,4 (T3.1-2); the owned weld instance φ(44)=20=d13 re-verified by unit census (T3.4); the
anti-over-read guard — the value 2 is a UNIVERSAL totient attractor, unique fixed point and global basin
over all seeds 1..10000 (T3.6-7), so the terminal VALUE carries zero scene-specific content regardless of
any future reading; the M2 disambiguation (capacity shell ≠ V₉ pointed shell, T3.8); and the return-defect
arithmetic itself (T3.9). The T1-flavored "depth-4 = capacity quantity" question is NOT promoted: depth 4
has no owned typing (numerology guard).

---

## Target 4 — sweep-frontier (a): E4+L4 third generation (STRICT CAUTION honored)

**Not attempted:** any derivation of a third generation. The standing 3rd-generation NO-GO stands:
L4 row 491 (NO-GO, Lean `decide`), E4 row 471 (NO-GO), `D0-GENERATION-RAYS-001` row 35 (NO_GO_PROVED),
X5 contract row 498: "HYP primitive contract PRIM-LEPTON-BRANCH-FIXING-OPERATOR (POSTULATED)".

**The T4-hypothesis adjudicated:** "the missing 3rd branch/generation is a LAYER of an owned structure."
Two forms, adjudicated separately:

1. **In-carrier form (third branch = trivial-isotype / fixed layer of the owned branch carrier):
   REFUTED by owned theorem + computation.** The owned carrier is `σ = (0123)(456)` on 7 points
   (`LeptonBranchFixingNoGo.lean:37`). Owned: `shell_no_fixed_point` (`:41`). Computed: exactly 2 orbits,
   no fixed point (T4.1); Burnside over ⟨σ⟩ ≅ C₁₂ gives trivial-isotype multiplicity 24/12 = **2** (T4.2)
   — the trivial-isotype layers of the branch carrier ARE the two branches (one per orbit). There is no
   third in-carrier layer; positing one contradicts an owned Lean theorem. The negative control (T4.6)
   shows the adjudication is not technique-vacuous: a rival carrier `(0123)(45)(6)` WITH a fixed point
   yields 3 layers — the owned carrier is what refuses, not the method.
2. **Cross-carrier form (third generation = layer of the OTHER owned structure, the K(9,11,13)/toral
   side, `Tr(T²) = 3`, T = [[0,1],[1,−1]] owned at BOOK_01:1136; verified exactly, T4.3):** the layer
   count 3 is real but lives on a different owned carrier; connecting it to the 2-orbit branch carrier
   is EXACTLY the operator the corpus already names and forbids from frozen data: pigeonhole totality
   re-verified over ALL 8 maps Fin3→Fin2 and ALL 9 maps Fin2→Fin3 (T4.4, domain = the full map spaces).
   The bridge is `PRIM-LEPTON-BRANCH-FIXING-OPERATOR` — POSTULATED HYP (row 498), proven
   non-constructible (row 491).
3. **Central-extension analogy anchor:** the pilot identification {D₂,ABCD} = layers of Q₈'s central
   extension is itself graded fork-open (GAP_E §SKEPTIC-#1 EoR-6: center-reading vs role-pair-reading
   unadjudicated), and it concerns V₉/role material, not the 7-point shell-torus (⟨σ⟩ ≅ C₁₂, whose
   central extensions supply no canonical third orbit). It cannot carry the E4+L4 case.

### Verdict: **HONEST-BLOCKED(exact missing object = PRIM-LEPTON-BRANCH-FIXING-OPERATOR)**

The in-carrier T4 form is refuted by owned theorem; the cross-carrier form reduces to the already-named,
already-postulated external primitive. One genuine structure note recorded WITHOUT promotion: the T4
reading holds within each carrier separately (branches = trivial-isotype layers of the shell-torus, 2 = 2;
generations = trivial-isotype count of the scene side, 3 = 3, both computed) — what is missing is not a
layer but the INTERTWINER between the two owned carriers, which is exactly the registry's named PRIM.
This is consistent with, and sharpens, the standing no-go; nothing here reopens it.

**Minor note (skeptic, accepted):** the trivial-isotype TYPING of the generation count lives in registry
prose only — the Lean definition is a bare literal (`LeptonSelectorExtension.lean:23`:
`def numGenerations : ℕ := 3`), while row 491's prose says "numGenerations=3 (K(9,11,13) trivial-isotype
multiplicity Tr(T^2)=3)". **Candidate one-line Lean lift (not forged here):** a theorem tying
`numGenerations` to the computed `Tr(T²)` of the owned toral operator, closing the prose↔Lean gap.

---

## Named risks & PRE-REGISTERED attack surface

- **ATT-1 (strongest self-attack, Target 3) — FIRED, kill accepted:** the unit-group reading is owned at
  ONE instance (q=44); claiming it at the terminal step (q=4) is an instance→rule lift of exactly the
  kind GAP-E's skeptic punished. The pre-registered tripwire condition ("if the skeptic finds owned text
  restricting THE-A's reading... the verdict drops to HONEST-BLOCKED") was met by `BOOK_01:1403`
  (return-window precondition `|q−mτ|≪1`); the drop to HONEST-BLOCKED is applied in the Target 3 verdict
  and the banner.
- **ATT-2 (Target 1):** "the co-tower is the object" could be read as claiming closure of row 414.
  Pre-registered: it is NOT — the PROOF-TARGET stands; the memo only re-types the missing artifact and
  names the residual weight-family object. Any closure reading of this memo is an over-read.
- **ATT-3 (Target 1, trap (f)):** does T1.10-11 construct its key quantity from the conclusion? The
  weight `W_n` is built from fiber censuses computed independently of the intertwining check, and the
  identity is verified on TWO kernels; the trap-(m) caveat is printed in the script itself.
- **ATT-4 (Target 4):** Burnside over ⟨σ⟩ uses the cyclic group generated by the owned permutation; if
  the owned symmetry object is larger (e.g. the full centralizer), the trivial-isotype count could
  differ. Pre-registered check: for the PERMUTATION representation the multiplicity of the trivial
  rep equals the number of orbits of the acting group; any group with the same orbits {4-cycle set,
  3-cycle set} gives the same count 2, and any larger group can only MERGE orbits (count ≤ 2), never
  reach 3. The refutation is robust in the direction that matters.
- **ATT-5 (Target 2a):** the totality closure relies on my recurrence identity, not on Lean. It is
  checked exactly at 41 points plus the positivity induction (T2A.3-4); the Lean lift is named but not
  claimed.

## What this does NOT show

- No registry row changes status; no PROOF-TARGET is closed; no third generation exists or is hinted.
- Target 1's residual object (canonical compatible weight family) and Target 3's TWO residual objects
  (non-return-window branch-semantics clause; window-units ↔ sign-dyad clause) are NAMED GAPS, not
  constructions — Target 3 is HONEST-BLOCKED, not conditional.
- The chain echoes 8/4/2 vs Ω₈/ABCD/D₂ remain unexplained cardinality coincidences.
- Nothing here touches the α-seam, the M2 torsor, or any 053040 material.

---

## §W4.SKEPTIC — verdict + repair log (INDEPENDENT pass, 2026-07-06, ACCEPTED IN FULL, no defense)

**Per-target verdicts (skeptic):** T2A SURVIVES; T4 SURVIVES; T1 WOUNDED-fixable; T2B WOUNDED-fixable;
**T3 KILLED** (DECOMPOSED-CONDITIONAL → HONEST-BLOCKED) — the kill route was the memo's own
pre-registered ATT-1 tripwire, discharged by the skeptic's trap-(l) read-past of the THE-A citation.

### Errors of record (enumerated, no defense; all repairs applied inline at the cited sites)

- **EoR-W4-1 (T1, ownership mis-attribution):** the pre-skeptic draft credited the co-tower kernel level
  to "rows 271+412". Row 412 owns the Fibonacci **Bratteli** tower — a different object; the module owner
  is row 24 `D0-ARCHIVE-TOWER-001`. *Fix:* row 412 struck from Target 1 ownership (it remains correctly
  cited in Target 2a, where the Bratteli tower IS the object); rows 24+271 substituted; row 271's
  follow-on caveat reproduced verbatim (nonemptiness on the Mathlib LightProfinite object = named
  follow-on target, not owned).
- **EoR-W4-2 (T1, registry hygiene find):** `archive_covariance_projectively_compatible` and
  `archive_laplacian_projectively_compatible` (`ArchiveRefinementTower.lean:116-127`) appear in NO
  registry row's theorem list (grep count 0). *Fix:* flagged as an integration hygiene item; also added
  row 41 `D0-ARCHIVE-LAPLACIAN-RG` as the nearest owned neighbor of the compatibility-failure layer.
- **EoR-W4-3 (T2B, vacuous check):** T2B.2 compared a list to itself; "independence verified, not
  assumed" over-claimed. *Fix:* replaced with an explicit variation of the joint `(scale, dim)` object
  over the witness pair + honesty label "definitional bookkeeping of the owned formalization"; the
  over-claim struck; check count 35→36 (T3.9 added, T2B rebuilt).
- **EoR-W4-4 (T3, THE KILL):** the draft lifted THE-A's unit-group/branch semantics from the owned
  return window q=44 to the non-return windows 20/8/4. Owned precondition `BOOK_01:1403` (`|q−mτ|≪1`,
  "residue classes modulo q are the coherent branches") is FAILED by all three (exact defects 8/7, 12/7,
  16/7 vs τ₀=44/7 — new check T3.9). *Fix:* verdict re-graded HONEST-BLOCKED; banner added; residual
  missing-object spec WIDENED to two clauses; survivors listed explicitly.
- **EoR-W4-5 (T2A, cosmetic):** stale script comment `F(2n+1)` (line 178) survived the organic T2A.6
  repair. *Fix:* comment corrected to `F(2n+3)`.
- **EoR-W4-6 (T4, minor):** trivial-isotype typing of `numGenerations = 3` exists in registry prose
  only, not in Lean (`LeptonSelectorExtension.lean:23` is a bare literal). *Fix:* noted in Target 4 with
  a candidate one-line Lean lift (not forged).

### Mutation log (closing the skeptic's mutation-log gap)

11/11 planted mutations fail the script (rc=1), each caught by the intended check: m1 pushforward
6/81→1/16 (T1.6); m2 skip-target 33→34 (T2A.5); m3 fixed-point [2]→[4] (T3.6); m4 Burnside 24→21 (T4.2);
m5 coherence `!=`→`==` (T1.8); m6 orbit sizes {3,4}→{3,5} (T4.1); m7 chain 8→10 (T3.1); post-repair:
m8 joint-object scale equality flip (T2B.2); m9 defect 8/7→9/7 (T3.9); m10 τ₀ 44/7→45/7 (T3.9);
m11 Burnside re-check (T4.2). Plus one organic firing: T2A.6 on the author's real `F(2n+1)` indexing
error during authoring.

### Hygiene items handed to integration (no registry motion made here)

1. Register `archive_covariance_projectively_compatible; archive_laplacian_projectively_compatible` in a
   row's theorem list (natural home: row 24 `D0-ARCHIVE-TOWER-001`).
2. Row 414 `D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001` STAYS OPEN/PROOF-TARGET — this wave re-types its
   missing artifact (wrong-variance demand; defect = fiber-multiplicity diagonal `W_n`) but closes
   nothing.
3. Candidate Lean lifts (owner decision): `dimA_strictMono` + unbounded 33-skip (T2A);
   `numGenerations = Tr(T²)` typing (T4).
