# M1 ⇒ QM BRIDGE MEMO — the deepest cement made explicit

**Status:** DRAFT / bridge-made-explicit (NOT a closure).
**Date:** 2026-07-05 (external-source hardening pass 2026-07-05: axiom lists verified against primary/author sources;
Masanes–Müller corrected 4→5 requirements; all D0 file:line anchors verified verbatim).
**Citation-defect LOCATION (corrected per Skeptic #1; re-verified by full-repo grep 2026-07-05):** the wrong
Masanes–Müller-2011 article number — the string `13, 053040, 2011` — occurs in **THREE** built artifacts, NOT
"exactly one" as an earlier draft of this memo (and Skeptic #1's own finding) asserted:
(1) `09_LEAN_FORMALIZATION/D0/Bridge/M1InfoReconstructionBridge.lean:8` ("*New J. Phys.* 13, 053040, 2011");
(2) `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:473`;
(3) `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/0012__00.9__anti-numerology-firewall.md:39`.
The two registry rows named below (`CLAIM_TO_LEAN_MAP.csv:247`, `LEAN_ASSUMPTION_LEDGER.csv:14`) ALREADY read
`063001` on disk and need no correction. **Do NOT confuse this with the string `15, 053040, 2013`** in
`BOOK_02...SPINE...md:1892` and `0033__02.28__born-epr-assumption-split.md:16`: that is a *different, correctly
numbered* paper (Müller–Masanes, *New J. Phys.* **15**, 053040, 2013) and must not be touched. See §2 flag for the
verified-on-disk grep.
**Owner row (existing):** `D0-M1-INFO-RECONSTRUCTION-001` (CLAIM_TO_LEAN_MAP.csv:247)
**Ledger row (existing):** `ASSUMP-M1-INFO-RECONSTRUCTION` (LEAN_ASSUMPTION_LEDGER.csv:14)
**Proposed refinement:** `ASSUMP-M1-QM-RECONSTRUCTION` (per-hypothesis decomposition; see §6).

---

## 0. What this memo is, and is NOT

This memo answers ONE question, honestly: **does D0's M1 finite-observability axiom
yield complex-Hilbert-space quantum mechanics — and if not internally, what exactly must
be imported to bridge the gap?**

- It is a **bridge-ledger entry**, not a derivation. The correct outcome here is
  *bridge-made-explicit*: naming the minimal import and its failure-meaning IS the deliverable.
- The pre-existing `ASSUMP-M1-INFO-RECONSTRUCTION` lumps the entire reconstruction into one
  opaque `reconstructsComplexQM : Prop` (see Lean `M1InfoReconstructionBridge.lean:17`). That is
  honest that a bridge exists, but it is **not minimal**: it hides *which* reconstruction axioms
  D0 already owns and *which* it must still import. This memo decomposes that single Prop into the
  exact per-axiom hypothesis list and grades each.
- NO edits are made here to CLAIM_TO_LEAN_MAP.csv, the LEAN_ASSUMPTION_LEDGER, or any built
  `.lean`. All registry/ledger changes below are **proposals**; Lean appears as code blocks only.

---

## 1. What D0 actually owns (verbatim, file:line)

### 1.1 The M1 axiom itself (the premise the reconstructions start from)

`01_BOOKS/BOOK_00.../0004__00.2__primitive-thesis.md:3`
> "D0 is a finite-observability framework over a condensed/profinite φ-quasicrystalline tiling hull."

`…:12` (the M1 law, verbatim):
> "**M1** — no exogenous parameters: no background dependence, no external catalog. Physics is
> *what survives the requirement to distinguish itself without outside help.* … the world is the
> fixed point of 'describe yourself, borrowing nothing from outside' … **which structure is uniquely
> compatible with its own existence as a record.**"

`…:21–22` (the two readings of M1):
> "- **Algebraically** — minimality (MDL/Kolmogorov): the shortest record, empty catalog.
> - **Operationally** — no hidden degrees of freedom: it is forbidden to keep a side-register 'which one of.'"

The formal predicate form: `CLAIM_TO_LEAN_MAP.csv:277` `D0-M1-PREDICATE-001`
(`D0.Foundation.M1Predicate`, `m1_forced_unique`, LEAN_PROVED, CORE-FORMALIZED):
> "M1 formalized as a reusable proof-theoretic predicate (NOT a new axiom): `M1Forced (Forced:a->Prop) a`
> = a satisfies the canonical finite constraint AND is its unique witness; `RequiresExternalCatalogue Forced b`
> = not (Forced b) (b needs data beyond the finite code = an unprovable input)."

**Load-bearing reading:** M1's *primitive* is **finite distinguishability of a self-reading record with no
external catalogue.** This is a statement about a single elementary system's information content — it maps
directly onto the "finite information capacity of an elementary system" premise the reconstructions open from.

### 1.2 QM-flavoured structure D0 already owns

**(a) Born / quadratic response — OWNED as CORE.**
`01_BOOKS/BOOK_04.../0008__04.6__finite-born-2-0-in-matter-language.md:3`
> "A finite channel amplitude `(x,y)` is first reduced to the forced phase-blind quadratic response `x^2+y^2`;
> matter effects then aggregate these squared norms over the finite support; only then is the response normalized.
> Thus a matter-sector probability cannot introduce either a new response functional or a new probability functional."

`…:29–33` (Lean owners): `D0.finite_effect_born_readout_unique`, `finite_effect_born_no_hidden_response`,
`finite_coarse_born_readout_unique`, `finite_tensor_born_readout_unique`, `finite_power_readout_no_alternative`.

**(b) Symplectic / 2D-Gleason / Fibonacci-fusion routes — OWNED as principle.**
`0004__00.2__primitive-thesis.md:46` (Finite Holographic Self-Reading Principle):
> "Physical information is realized exclusively through a finite holographic readout whose response preserves a
> symplectic (area-preserving) form across the cut between the retained (active) sector and the archive (traced)
> sector. The detector must read itself autonomously — hidden states and external memory backgrounds are strictly forbidden."

`…:50` (route 1):
> "**2D Gleason closure.** A non-degenerate symplectic form requires a minimal 2D phase space; enforcing
> area-preservation there topologically forces the quadratic Born response."

`…:55` (a NO-GO to respect):
> "the readout operation `τ` has no algebraic inverse: the fundamental symmetry is a **non-invertible categorical
> symmetry**, so structural time-irreversibility is an algebraic inevitability rather than a statistical artifact,
> and **unitarity is recovered only as an emergent low-energy shadow.**"

**(c) Phase / angle carrier and its microquantum — OWNED as CORE.**
`0008__04.6...:46`:
> "The Born readout above lives on phases, and a phase is an *angle*."
`…:70` (LEM 04.6.π.2): the angular microquantum is pinned to the owned `δ₀`, "so no new constant enters when the
angle is introduced."

**(d) ℂ⊕ℍ electroweak division-algebra structure — OWNED (memory: d0-matter-sector map).**
Per MEMORY.md `d0-matter-sector-scene-vs-terminal-map`: the electroweak ℂ⊕ℍ structure is derived-core.
This is *downstream* of the QM scaffold, not a substitute for it (see skeptic §5).

**(e) Q₈ / spinor bit — OWNED as forcing.**
`0004__00.2...:36`:
> "*Why Q₈?* A non-normal subgroup yields conjugate copies, hence a 'which copy' catalog, hence ⊥M1; what
> survives is the Hamiltonian non-abelian group ⇒ Q₈ (Dedekind-1897 minimality)."

### 1.3 The existing bridge (what it says today)

`LEAN_ASSUMPTION_LEDGER.csv:14` `ASSUMP-M1-INFO-RECONSTRUCTION`, type `QM_RECONSTRUCTION_THEOREM`, status EXPLICIT:
> "Finite info capacity + continuity + tomographic locality => complex Hilbert QM; an external forcing of the M1
> finite-capacity premise." Failure-meaning: "M1 => QM structure is a cited reconstruction-theorem family not a
> D0-internal derivation."

Lean `D0/Bridge/M1InfoReconstructionBridge.lean:13–19`: a single structure with two opaque `Prop` fields
(`m1FiniteCapacity`, `reconstructsComplexQM`) and `d0Witness`/`cited`. **The entire reconstruction is one Prop.**
That is the imprecision this memo removes.

## 2. The three reconstruction theorems — exact axiom lists

Sources (external, cited for their axiom content; NOT D0-owned facts):
Hardy, *Quantum Theory From Five Reasonable Axioms*, arXiv:quant-ph/0101012 (2001);
Masanes–Müller, *A derivation of quantum theory from physical requirements*, New J. Phys. 13, **063001** (2011)
(arXiv:1004.1483); Chiribella–D'Ariano–Perinotti, *Informational derivation of quantum theory*,
Phys. Rev. A 84, 012311 (2011) (arXiv:1011.6451).

> **Citation-defect flag (verified 2026-07-05 against IOPscience DOI 10.1088/1367-2630/13/6/063001 and the
> author's own publications page mpmueller.net; full-repo grep re-run per Skeptic #1 AND its residual undercount):**
> the correct Masanes–Müller-2011 article number is **063001** (New J. Phys. **13** (2011) 063001, arXiv:1004.1483),
> NOT 053040.
> **LOCATION OF THE DEFECT (corrected, verified count = THREE):** the wrong string `13, 053040, 2011` occurs in
> THREE built artifacts:
> (1) `09_LEAN_FORMALIZATION/D0/Bridge/M1InfoReconstructionBridge.lean:8` — "*New J. Phys.* 13, **053040**, 2011";
> (2) `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:473`;
> (3) `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/0012__00.9__anti-numerology-firewall.md:39`.
> `grep -c "13, 053040, 2011"` on disk = 1 in each of those three files. Skeptic #1's finding said "exactly ONE
> built artifact (the .lean)"; that undercount is itself CORRECTED here — the two BOOK_00 markdown files carry the
> same wrong number and are equally in scope for the proposed correction.
> **NOT a defect (do not touch):** the string `15, 053040, 2013` in `BOOK_02...SPINE...md:1892` and
> `0033__02.28__born-epr-assumption-split.md:16` is a *different, correctly numbered* paper (Müller–Masanes,
> *New J. Phys.* **15**, 053040, 2013). `grep` for the bare token `053040` alone conflates the two; always match on
> the full `13, 053040, 2011` string.
> The two registry rows — `ASSUMP-M1-INFO-RECONSTRUCTION` (LEAN_ASSUMPTION_LEDGER.csv:14) and
> `D0-M1-INFO-RECONSTRUCTION-001` (CLAIM_TO_LEAN_MAP.csv:247) — **ALREADY read 063001 on disk**
> (`grep -c "13, 053040, 2011"` = 0, `grep -c "063001"` = 1 in each). They require NO correction; the earlier draft
> of this memo wrongly claimed both rows "still say 053040" — that claim is RETRACTED (Skeptic #1, strongest finding).
> Proposed correction (do not apply here): fix the article number `053040`→`063001` in all THREE built artifacts
> (the `.lean:8` docstring and the two BOOK_00 markdown lines) when the child assumption is registered. This memo
> uses 063001 throughout.

### 2.1 Hardy 2001 — five axioms
Setup primitives: `N` = max number of distinguishable states in one measurement (a *capacity*);
`K` = number of degrees of freedom (real parameters) fixing a state.
- **H1 Probabilities** — relative frequencies converge for a fixed preparation+measurement on an infinite ensemble.
- **H2 Simplicity** — `K` is a function of `N` taking the *minimum* value consistent with the axioms, for each `N`.
- **H3 Subspaces** — a system constrained to an `M`-dim subspace behaves like a system of dimension `M`.
- **H4 Composite systems** — for subsystems A,B: `N = N_A N_B` **and** `K = K_A K_B` (this is *tomographic locality*).
- **H5 Continuity** — there is a continuous reversible transformation between any two pure states.
(H1–H4 hold for classical probability too; **H5 alone excludes classical theory** and forces `K = N²` ⇒ complex QM.)

### 2.2 Masanes–Müller 2011 — FIVE requirements (verified 2026-07-05; earlier draft said "four")
The published abstract (arXiv:1004.1483 / NJP 13 063001) states quantum theory follows from **"five simple
physical requirements."** The Müller-group summary page (iqoqi-vienna.at, verified 2026-07-05) presents the same
content as **three core postulates** (Tomographic Locality, Subspace, Continuous Reversibility) with two items
— finite-dimensionality and no-restriction — as background assumptions. Both framings are the same theorem at
different granularity; the memo uses the five-requirement enumeration and flags the three-core reading.
Frame: a generalized probabilistic theory (the requirements themselves supply finite-dimensionality).
- **MM1 Finiteness** — a system carrying one bit of information has each state fixed by a *finite* set of
  outcome probabilities (i.e. finite-dimensional state space). *This is the finite-capacity premise itself* —
  in the earlier draft it was mislabelled an "implicit frame"; it is a NAMED requirement. (In the 3-core reading
  it is a background assumption, not a numbered postulate.)
- **MM2 Local tomography** — states of composite AB are uniquely characterized by the statistics and correlations
  of local measurements on A and on B. (Müller-group verbatim.)
- **MM3 Equivalence of subspaces (Subspace axiom)** — a system with `n` perfectly distinguishable states, restricted
  to the face where the `n`-th outcome has probability zero, is equivalent to a system with `(n−1)` distinguishable
  states. (Müller-group verbatim.)
- **MM4 Symmetry / Continuous reversibility** — for every pair of pure states there is a one-parameter group of
  *reversible* transformations mapping one to the other. (Müller-group verbatim.) **This is the classical-excluding
  axiom, exactly as Hardy's H5.**
- **MM5 All measurements allowed (no-restriction hypothesis)** — every mathematically-consistent probability rule on
  the 2-state system is a physical measurement. (In the 3-core reading this is a background assumption.)

### 2.3 Chiribella–D'Ariano–Perinotti 2011 — five axioms + one postulate
Frame: operational-probabilistic theory (circuits of tests), finite systems.
- **C1 Causality** — the probability of a preparation is independent of the choice of *later* measurement (no signalling from the future). *This is the informational form of "no external catalogue / self-contained record."*
- **C2 Perfect distinguishability** — every state not on the boundary of the state space is perfectly distinguishable from some other state.
- **C3 Ideal compression** — every source of information can be encoded into a minimal system that is both lossless and maximally efficient.
- **C4 Local distinguishability** (= local tomography) — states of composites are distinguished by local measurements.
- **C5 Pure conditioning** — a pure bipartite state conditioned on a pure effect leaves a pure state.
- **C6 Purification (the single postulate)** — every mixed state arises as the marginal of a pure state of a larger
  system, *uniquely up to reversible transformation on the purifying system.* **C6 is what singles out QM** inside
  the "standard" class C1–C5.

## 3. Per-axiom ownership ledger

Grades: **OWNED** = D0 has a CORE/principle owner that entails the axiom; **PARTIAL** = D0 owns a
same-shaped statement but with a gap (weaker form, or a downstream-not-foundational owner); **UNOWNED** =
no D0 owner, must be imported. Every OWNED/PARTIAL claim carries its file:line from §1.

### 3.1 Hardy

| Axiom | Grade | D0 anchor / why |
|---|---|---|
| **H1 Probabilities** (frequentist limit) | PARTIAL | D0's Born readout `x²+y²` normalized *only after* the finite frame (04.6:3) gives the *probability functional*, but the frequentist *ensemble-limit* semantics is an infinite-`n` idealization; D0 is finite-observability (00.2:3). D0 owns the probability *rule*, not the ∞-ensemble limit. |
| **H2 Simplicity** (`K` minimal in `N`) | PARTIAL (object-mismatch, per Skeptic #1) | M1 read algebraically is "minimality (MDL/Kolmogorov): the shortest record, empty catalog" (00.2:21). BUT the objects differ: Hardy H2 minimizes `K` **as a function of `N`** — i.e. it minimizes the *state-parameter (real-dimension) count* of the state space (H2 def, §2.1) — whereas M1 minimizes **description length** (MDL/Kolmogorov complexity of the record). These are *analogous* minimality principles over *different* objects (dimensional counting vs. code length), not the same statement; the entailment M1-MDL ⇒ H2-dimensional-minimality is a *reading*, not a theorem — the SAME "pun-not-identity" caveat skeptic A1 applies to finiteness. Downgraded from OWNED to PARTIAL; it remains the *closest* informational match but "strongest single match" must not be read as identity. |
| **H3 Subspaces** | PARTIAL | D0 owns a rank-3/nullity-30 retained/traced *subspace split* (BOOK_04 04.2:39) and subspace-restricted spectra, but "an `M`-dim subspace behaves like a full `M`-system" as a *universal closure* is not separately proved; the scene's subspaces are specific, not a free `M`. |
| **H4 Composite / tomographic locality** | PARTIAL | D0 owns a *tensor* Born owner `finite_tensor_born_readout_unique` (04.6:32) and the S3 phason-triple tensor carrier (04.4). That gives `K=K_AK_B`-flavoured multiplicativity on the owned sector. But *tomographic locality as a universal axiom* (every composite state fixed by local statistics) is NOT proved for arbitrary composites — D0's composites are the specific scene tensor, not a general GPT tensor. |
| **H5 Continuity** (continuous reversible pure-state transf.) | **UNOWNED — and in tension** | D0's owned readout `τ` is **non-invertible** ("τ has no algebraic inverse … unitarity recovered only as an emergent low-energy shadow," 00.2:55). Continuous *reversibility* between pure states is the classical-excluding axiom in Hardy — and D0 does NOT own it at the foundational layer; it owns only an *emergent* unitary shadow. **This is the load-bearing residual gap.** |

### 3.2 Masanes–Müller

| Requirement | Grade | D0 anchor / why |
|---|---|---|
| **MM1 Finiteness** (one bit ⇒ finite outcome-prob set) | PARTIAL | This is the *finite-capacity premise* the whole bridge rests on. M1's "finite distinguishability, no external catalogue" (00.2:12) is the D0-side reading, but the map M1↦finite-`N`-capacity is a *reading*, not a theorem (skeptic A1). D0 owns finiteness of observation (00.2:3), not the precise GPT "one-bit ⇒ finite outcome set" statement. |
| **MM2 Local tomography** | PARTIAL | Same as H4: owned on the scene tensor sector (04.6:32), not as a universal composite axiom. |
| **MM3 Equivalence of subspaces** | PARTIAL | Same as H3: retained/traced split owned (04.2:39), universal subspace-equivalence not separately proved. |
| **MM4 Symmetry / continuous reversibility** | **UNOWNED — and in tension** | Same obstruction as H5: D0's foundational symmetry is non-invertible (00.2:55). Reversible pure-to-pure transitivity is imported, not owned. **The load-bearing gap, identical across all three theorems.** |
| **MM5 All measurements allowed** | PARTIAL / in mild tension | D0's `finite_effect_born_no_hidden_response` (04.6:30) *restricts* admissible readouts to Born; MM5 says *every* consistent probability rule is realizable. D0 is more restrictive by design — a modelling mismatch, resolvable but not free. |

### 3.3 Chiribella–D'Ariano–Perinotti

| Axiom | Grade | D0 anchor / why |
|---|---|---|
| **C1 Causality** (no signalling from future / self-contained record) | **OWNED** | Best match in the whole memo. M1: "no external catalog … describe yourself, borrowing nothing from outside" (00.2:12); operationally "no outside to escape to, hence no external catalog to escape into" (00.2:68). D0's closed-vacuum `external_mirror_model_forbidden` IS operational causality/self-containment. |
| **C2 Perfect distinguishability** | PARTIAL | D0 owns *finite distinguishability* with a quantum-of-distinguishability `δ₀` (04.6:70) and the `359` address-space distinguishability ceiling (04.5:41). But CDP's C2 is a *geometric* claim about the state-space boundary; D0 owns finite distinguishability, not the boundary-perfect-distinguishability geometry. |
| **C3 Ideal compression** | OWNED | This is M1+ read as MDL: canonicalize to the minimal record `Can(S)` (00.2:13), "the shortest record, empty catalog" (00.2:21). Lossless minimal encoding = M1+ stop rule. |
| **C4 Local distinguishability** (local tomography) | PARTIAL | Same as H4/MM2: owned on scene tensor (04.6:32), not universal. |
| **C5 Pure conditioning** | PARTIAL / uncertain | D0's retained/traced split with the feedback resolvent `F_N` (00.2:60–66) conditions a sector on a projector; whether the *pure→pure* preservation holds is not established. Owned structure is present but the purity-preservation is unverified. |
| **C6 Purification** (the QM-selecting postulate) | **UNOWNED** | No D0 owner. D0's foundational readout is *irreversible/dissipative* (traced archive, non-invertible τ, 00.2:55). Purification demands every mixed state be the reversible marginal of a pure global state, unique up to reversible transf. on the purifier — a *reversibility* structure D0 does not own foundationally. **Second load-bearing residual gap, and it is the same reversibility obstruction as H5/MM4.** |

## 4. The precise residual gap

Aggregating §3, the three reconstructions converge on the *same* structural axiom that D0 does **not**
own foundationally, plus a cluster of composite/subspace axioms D0 owns only on its specific scene:

**GAP-1 (load-bearing, single point of failure): Continuous reversibility of pure-state dynamics.**
This is Hardy H5 = Masanes–Müller MM4 = the reversibility core of CDP C6-purification. All three theorems use
*exactly this axiom* to (a) exclude classical probability and (b) select the complex field. D0's owned
foundational readout is explicitly **non-invertible** — "τ has no algebraic inverse … unitarity recovered only
as an emergent low-energy shadow" (`00.2:55`). So D0 does not merely *lack* reversibility; its stated core is in
*tension* with it, holding reversibility only as an emergent shadow. **To claim "M1 ⇒ complex-Hilbert QM," D0 must
prove that the emergent-unitary shadow satisfies continuous reversibility on pure states at the reconstruction's
input layer.** This is the single missing lemma. It is currently unproven and NOT trivially available.

**GAP-2 (moderate): Universal tomographic locality / subspace equivalence.**
D0 owns H4/MM2/C4 and H3/MM3 only on its *specific* scene tensor (`finite_tensor_born_readout_unique`, 04.6:32;
retained/traced split, 04.2:39), not as *universal* GPT axioms over arbitrary composites/subspaces. The
reconstructions need the universal form. Either D0 restricts the reconstruction to its scene (weakening the
theorem's generality — acceptable) or it must prove the universal axioms (unowned).

**GAP-3 (minor / modelling): Measurement closure vs. Born restriction.**
MM5 ("all measurements allowed") and C2 (perfect distinguishability geometry) are in mild tension with D0's
*restrictive* Born-only readout (`finite_effect_born_no_hidden_response`, 04.6:30). D0 is deliberately more
restrictive; this narrows but does not block the bridge.

**What IS cleanly owned** (so the bridge is genuinely minimal, not vacuous): C1-causality and
C3-ideal-compression are OWNED — these are literally M1/M1+ restated. H2-simplicity is the *closest*
informational match but is downgraded to PARTIAL (Skeptic #1 object-mismatch: H2 minimizes state-parameter
dimension `K(N)`, M1 minimizes description length — analogous minimality over different objects; see §3.1).
And the *complex* (not real, not
quaternionic) field selection has independent downstream corroboration in the owned ℂ⊕ℍ electroweak structure
(MEMORY d0-matter-sector map) and the Q₈/spinor forcing (00.2:36) — but note (skeptic §5) this is downstream,
not a foundational proof of the field.

**Residual gap in one sentence:** *D0 owns the informational/minimality/self-containment half of every
reconstruction (H2, C1, C3), but does NOT own the continuous-reversibility axiom (H5=MM4=C6-core) that each
theorem uses to reach complex Hilbert space — and D0's stated non-invertible core is in tension with it.*

## 5. Adversarial skeptic pass

Pre-registered attack surface (attacks I committed to run before grading), then verdicts.

**A1 — "M1 = finite capacity is a pun, not an identity."**
The reconstructions' "finite information capacity" is a *precise* GPT notion: `N` = number of perfectly
distinguishable states, `K` = real dimension of the state space. M1's "finite distinguishability, no external
catalogue" (00.2:12) is a *proof-theoretic* / MDL notion (00.2:21). These are cousins, not synonyms.
**Verdict: SUSTAINED, partial.** The map M1↦finite-capacity is a *reading*, not a theorem. This is precisely why
the honest grade for H1 is PARTIAL and why the whole thing must stay a BRIDGE. The memo does not claim identity;
it claims the informational half (H2/C1/C3) is entailed and the capacity-frame is imported. Keep as bridge.

**A2 — "The reversibility gap (GAP-1) is fatal, not moderate: D0 forbids exactly what QM needs."**
D0's core is non-invertible (00.2:55); QM's reconstruction needs continuous reversibility. If D0's foundational
dynamics is *genuinely* irreversible, then M1 ⇏ QM — it would yield a *different* (dissipative, non-unitary)
theory, and the emergent-unitary "shadow" might be only approximate, never the exact complex-Hilbert structure.
**Verdict: SUSTAINED — this is the real risk and the memo must not soften it.** Consequence: the bridge assumption
must carry an explicit *reversibility-recovery obligation*, and its failure-meaning must state that failure =
"D0's emergent unitarity is not exact ⇒ M1 yields a post-quantum / dissipative theory, not textbook QM." I have
strengthened §4 GAP-1 and §6 accordingly. This attack *changes the failure-meaning* — it is not cosmetic.

**A3 — "The complex-field win is double-counted."**
The memo notes owned ℂ⊕ℍ / Q₈ as corroborating the *complex* (vs real/quaternionic) selection. But per MEMORY
`colour-su3-not-derived-in-d0` and the matter-sector map, ℂ⊕ℍ is *derived-core downstream of the QM scaffold*, so
using it to support the field choice *inside* the M1⇒QM bridge is circular if QM is what we're trying to reach.
**Verdict: SUSTAINED.** Demoted: ℂ⊕ℍ/Q₈ is listed as *downstream corroboration only*, explicitly flagged
non-foundational in §4, and MUST NOT be counted toward closing GAP-1. Removed any implication that it proves the field.

**A4 — "This duplicates ASSUMP-M1-INFO-RECONSTRUCTION; you're re-opening a closed bridge."**
Respecting the discipline: the existing row/ledger stays. This memo does **not** re-open or contradict it; it
*refines* it from one opaque Prop into a per-axiom decomposition. Per MEMORY `d0-registry-source-of-truth`,
CLAIM_TO_LEAN_MAP.csv is canonical and I propose (not perform) an edit. **Verdict: no violation** — the proposal
is a strict refinement (adds granularity + a reversibility obligation), and I keep the old assumption id as the
parent.

**A5 — "Naming a bridge is not progress; it's just relabeling ignorance."**
Counter: the deliverable's value is *minimality* — before this memo the import was "all of QM reconstruction";
after it, the import is *precisely GAP-1 (continuous reversibility) + GAP-2 (universal locality) + GAP-3
(measurement closure)*, with H2/C1/C3 discharged onto owned M1. That is a strictly smaller, auditable import.
**Verdict: the bridge-made-explicit outcome is the correct and honest result** — not a closure, and not nothing.

**Net skeptic outcome:** the honest grade is **bridge-made-explicit, NOT closed.** The single most important
correction the skeptic forced: GAP-1 is not "moderate," it is the *decisive* obstruction, and the failure-meaning
must name the post-quantum/dissipative alternative. No grade in §3 was upgraded; A3 forced a demotion.

## 6. Proposed bridge assumption ASSUMP-M1-QM-RECONSTRUCTION

**Proposal (NOT applied — registry/ledger edits are proposals only).**
Refine the parent `ASSUMP-M1-INFO-RECONSTRUCTION` into a per-hypothesis child that isolates the *actual* import.

**Proposed ledger row (LEAN_ASSUMPTION_LEDGER.csv — PROPOSED, do not apply here):**

```
assumption_id: ASSUMP-M1-QM-RECONSTRUCTION
lean_symbol:   D0.Bridge.BridgeAssumption.M1QMReconstruction
lean_file:     D0/Bridge/M1QMReconstructionBridge.lean
lean_thm:      m1_qm_reconstruction_conditional
owner_row:     D0-M1-INFO-RECONSTRUCTION-001   (parent; this is a refinement, not a new owner)
type:          QM_RECONSTRUCTION_THEOREM
status:        EXPLICIT
parent:        ASSUMP-M1-INFO-RECONSTRUCTION
citations:     Hardy quant-ph/0101012; Masanes-Mueller NJP 13 063001 (2011) / arXiv:1004.1483;
               Chiribella-DAriano-Perinotti PRA 84 012311 (2011) / arXiv:1011.6451
               [NOTE: 063001 is correct. The stale "13, 053040, 2011" lives in THREE built artifacts —
               M1InfoReconstructionBridge.lean:8, BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:473, and
               0012__00.9__anti-numerology-firewall.md:39 — fix all THREE on registration. The two registry
               rows (CLAIM_TO_LEAN_MAP.csv:247, LEAN_ASSUMPTION_LEDGER.csv:14) already read 063001, no edit
               needed. Do NOT touch "15, 053040, 2013" (Müller–Masanes 2013, a different, correctly numbered paper)]
what_is_owned_by_M1:   H2-simplicity, C1-causality, C3-ideal-compression (= M1/M1+ restated; OWNED)
what_is_imported:      GAP-1 continuous reversibility of pure-state dynamics (Hardy H5 = MM4 = CDP C6-core);
                       GAP-2 universal tomographic locality + subspace equivalence (owned only on scene tensor);
                       GAP-3 measurement closure (in mild tension with D0's Born-only restriction)
failure_meaning:       If continuous reversibility (GAP-1) is NOT recoverable from D0's emergent-unitary shadow
                       (00.2:55 says unitarity is only an emergent low-energy shadow of a non-invertible core),
                       then M1 does NOT yield textbook complex-Hilbert QM: it yields a DISSIPATIVE / POST-QUANTUM
                       operational theory whose unitary regime is approximate, not exact. Failure is therefore
                       physically meaningful and testable in principle (exact vs approximate unitarity), not a
                       mere labelling loss.
```

**Discharge obligation to promote this from BRIDGE toward CORE (the single missing lemma):**
> Prove that D0's emergent-unitary shadow (the low-energy limit of the non-invertible readout `τ`, 00.2:55)
> satisfies **continuous reversibility between pure states at the reconstruction input layer**, on the scene
> tensor sector. If that lemma is proved, GAP-1 closes and the reconstruction theorems fire on owned inputs,
> leaving only GAP-2/GAP-3 (both restrictable-to-scene, hence honest partials, not obstructions).

**Why this is a valid G2-gate closure:** per §00.12 bridge-austerity and the D0 discipline, a cement that must be
imported is legitimately closed by making it an EXPLICIT, minimal, honestly-labelled bridge assumption. This memo
does exactly that: it shrinks the import from "all of QM" to "GAP-1 reversibility (+ two restrictable partials)"
and attaches a concrete failure-meaning and a single discharge lemma.

## 7. Proposed Lean draft (code block only — NOT built)

```lean
namespace D0.Bridge
namespace BridgeAssumption

/-- Refinement of `M1InfoReconstruction`: the per-axiom decomposition of the M1 ⇒ complex-Hilbert-QM bridge.
    The informational half (Hardy H2 simplicity, CDP C1 causality, CDP C3 ideal compression) is DISCHARGED onto
    owned M1/M1+ (`D0.Foundation.M1Predicate`, Born/MDL owners). The remaining fields are the honest IMPORT:
    `continuousReversibility` (Hardy H5 = Masanes–Müller MM4 = CDP C6-core) is the single load-bearing gap;
    `universalLocality` and `measurementClosure` are restrictable-to-scene partials. -/
structure M1QMReconstruction where
  -- OWNED by M1 (D0 witnesses these):
  m1Simplicity          : Prop   -- Hardy H2 = M1 algebraic minimality (00.2:21)
  m1Causality           : Prop   -- CDP C1 = M1 no-external-catalogue (00.2:12, 00.2:68)
  m1IdealCompression    : Prop   -- CDP C3 = M1+ canonical minimal record (00.2:13)
  ownedSimplicity       : m1Simplicity
  ownedCausality        : m1Causality
  ownedCompression      : m1IdealCompression
  -- IMPORTED (the residual gap; assumed, not proved):
  continuousReversibility : Prop -- GAP-1: Hardy H5 = MM4 = CDP C6-core. NOT owned; in tension with 00.2:55.
  universalLocality       : Prop -- GAP-2: tomographic locality + subspace equivalence beyond scene tensor.
  measurementClosure      : Prop -- GAP-3: all-measurements-allowed, vs D0 Born-only (04.6:30).
  importedReversibility   : continuousReversibility
  importedLocality        : universalLocality
  importedClosure         : measurementClosure
  -- Conclusion of the reconstruction theorems, conditional on the imports:
  yieldsComplexHilbertQM  : Prop
  reconstructs            : yieldsComplexHilbertQM

/-- Conditional bridge: M1's owned informational half PLUS the three imported axioms yield complex-Hilbert QM.
    Proved only relative to `ASSUMP-M1-QM-RECONSTRUCTION`. Discharging `continuousReversibility` from D0's
    emergent-unitary shadow is the single lemma that would move this from BRIDGE toward CORE. -/
theorem m1_qm_reconstruction_conditional (h : M1QMReconstruction) :
    (h.m1Simplicity ∧ h.m1Causality ∧ h.m1IdealCompression) ∧
    (h.continuousReversibility ∧ h.universalLocality ∧ h.measurementClosure) ∧
    h.yieldsComplexHilbertQM :=
  ⟨⟨h.ownedSimplicity, h.ownedCausality, h.ownedCompression⟩,
   ⟨h.importedReversibility, h.importedLocality, h.importedClosure⟩,
   h.reconstructs⟩

end BridgeAssumption
end D0.Bridge
```

---

## 8. Bottom line

- **Outcome: bridge-made-explicit (NOT closed).** Correct and honest per D0 discipline.
- The import shrinks from "the entire QM reconstruction" (opaque single Prop today) to a **named, minimal
  three-part gap**, with H2/C1/C3 discharged onto owned M1/M1+.
- **The decisive residual is GAP-1: continuous reversibility of pure-state dynamics** — used identically by
  Hardy (H5), Masanes–Müller (MM4), and CDP (C6-purification) to reach complex Hilbert space, and in **explicit
  tension** with D0's stated non-invertible core (00.2:55).
- **Single discharge lemma** to promote toward CORE: prove D0's emergent-unitary shadow satisfies continuous
  pure-state reversibility on the scene tensor sector.
- **Failure-meaning is physical, not cosmetic:** if GAP-1 cannot be discharged, M1 yields a dissipative /
  post-quantum theory whose unitarity is approximate, not exact — a distinction with, in principle, empirical teeth.
- All registry/ledger/Lean changes above are **proposals**; nothing built was edited.

---

## 9. Skeptic #1 verdict + repair log (accepted in full)

**Verdict: WOUNDED** (accepted in full, no defense). The memo's central bridge-ledger content survives — the
per-axiom ownership grades, the load-bearing GAP-1 reversibility obstruction, and the bridge-made-explicit outcome
are all correct — but the memo carried a **mislocated-citation-correction integrity defect** in the exact claim it
most loudly said it had verified verbatim. All repairs below are applied; every load-bearing fact carries an
on-disk-verified file:line citation. No registry, ledger, or built-`.lean` file was edited; all corrections are to
this memo, and all Lean/registry changes remain proposals.

### 9.1 Errors of record

- **EOR-1 (strongest finding, accepted).** The earlier draft asserted that the built rows
  `CLAIM_TO_LEAN_MAP.csv:247` and `LEAN_ASSUMPTION_LEDGER.csv:14` "still say 053040" and must be corrected to
  063001. That is **FALSE**: both rows ALREADY read `063001` on disk. Verified verbatim —
  `CLAIM_TO_LEAN_MAP.csv:247` reads "Masanes-Mueller NJP 13 063001 (2011)"; `LEAN_ASSUMPTION_LEDGER.csv:14` reads
  "Masanes-Mueller NJP 13 063001 (2011)". `grep -c "13, 053040, 2011"` = 0 in each. The false claim is **RETRACTED**
  (header block; §2 flag). No correction is needed to either registry row.
- **EOR-2 (residual undercount inside the skeptic's own finding, corrected here).** Skeptic #1's finding stated the
  wrong `053040` string exists "in exactly ONE built artifact ... `M1InfoReconstructionBridge.lean:8`." That is also
  an **undercount**. A full-repo grep (2026-07-05) shows the wrong Masanes–Müller-2011 string `13, 053040, 2011`
  lives in **THREE** built artifacts: `09_LEAN_FORMALIZATION/D0/Bridge/M1InfoReconstructionBridge.lean:8`,
  `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:473`, and
  `01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/0012__00.9__anti-numerology-firewall.md:39`. The memo's own
  post-skeptic draft inherited the "exactly one" undercount; it is corrected to THREE (header block; §2 flag; §6 NOTE).
- **EOR-3 (false-positive guard, added).** The bare token `053040` ALSO appears in two artifacts that are NOT
  defects: `01_BOOKS/BOOK_02...SPINE...md:1892` and `.../0033__02.28__born-epr-assumption-split.md:16`, both reading
  `15, 053040, 2013`. That is a *different, correctly numbered* paper (Müller–Masanes, *New J. Phys.* **15**, 053040,
  2013), verified verbatim on disk. Any grep-driven "fix" must match the full `13, 053040, 2011` string, never the
  bare token, or it would corrupt two correct citations. Guard added (header block; §2 flag).
- **EOR-4 (H2 overstated as OWNED, corrected).** §3.1 originally graded Hardy **H2 Simplicity** as OWNED via the
  "strongest single match" to M1's MDL/Kolmogorov minimality. Skeptic A1's "pun-not-identity" caveat applies here
  too: Hardy H2 minimizes `K` **as a function of `N`** (state-parameter / real-dimension count), whereas M1
  minimizes **description length** (00.2:21). Analogous minimality over *different objects*; the entailment is a
  reading, not a theorem. **Downgraded OWNED → PARTIAL (object-mismatch)** at §3.1 and reflected in §4. "Strongest
  informational match" is retained but explicitly de-coupled from identity.

### 9.2 Repairs applied (1:1 against the accepted repair list)

1. **Citation-defect LOCATION fixed.** Header block, §2 flag, and §6 NOTE now name the real defect sites and retract
   the false two-registry-rows claim. **Extended beyond the skeptic's own scope** to the verified THREE artifacts
   (EOR-2), since the skeptic's "exactly one" was itself an undercount.
2. **Blanket "corrected 053040→063001 in the registry rows" assertion retracted.** No such correction was needed —
   the rows were already 063001. The only artifacts requiring the fix are the three built docstring/prose sites; the
   memo now flags exactly those for the proposed (not applied) correction.
3. **H2-simplicity discounted with the pun-not-identity caveat.** Downgraded to PARTIAL with an explicit
   object-mismatch note (§3.1, §4); "strongest single match" no longer reads as identity.
4. **GAP-1 kept as-is.** The reversibility gap (Hardy H5 = MM4 = CDP C6-core UNOWNED, in tension with verbatim
   `00.2:55` "τ has no algebraic inverse ... unitarity recovered only as an emergent low-energy shadow") is correct,
   honestly load-bearing, and its dissipative/post-quantum failure-meaning is sound. No change (§3.1 H5, §3.2 MM4,
   §3.3 C6, §4 GAP-1, §6 failure_meaning).
5. **Proposal-only discipline confirmed and kept.** Verified on disk 2026-07-05: no `M1QMReconstructionBridge.lean`
   exists; zero `ASSUMP-M1-QM-RECONSTRUCTION` rows in any registry CSV. All Lean is a code block; all registry/ledger
   changes are proposals. Honored.

### 9.3 Verification ledger (on-disk, 2026-07-05)

| Fact | On-disk truth | Status |
|---|---|---|
| `CLAIM_TO_LEAN_MAP.csv:247` article no. | reads `063001` | already correct; no edit (EOR-1) |
| `LEAN_ASSUMPTION_LEDGER.csv:14` article no. | reads `063001` | already correct; no edit (EOR-1) |
| `M1InfoReconstructionBridge.lean:8` | reads `13, 053040, 2011` | DEFECT; proposed fix (EOR-2) |
| `BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md:473` | reads `13, 053040, 2011` | DEFECT; proposed fix (EOR-2) |
| `0012__00.9__anti-numerology-firewall.md:39` | reads `13, 053040, 2011` | DEFECT; proposed fix (EOR-2) |
| `BOOK_02...SPINE...md:1892` | reads `15, 053040, 2013` | CORRECT (different paper); do not touch (EOR-3) |
| `0033__02.28__born-epr-assumption-split.md:16` | reads `15, 053040, 2013` | CORRECT (different paper); do not touch (EOR-3) |
| `M1QMReconstructionBridge.lean` | does not exist | proposal-only honored |
| `ASSUMP-M1-QM-RECONSTRUCTION` in registries | 0 rows | proposal-only honored |
| `00.2:55` reversibility anchor | "τ has no algebraic inverse ... emergent low-energy shadow" | verbatim; GAP-1 sound |

### 9.4 Residual (what is open / what is now bridge-ledger-ready)

- **Bridge-ledger-ready (motion-ready as a proposal):** `ASSUMP-M1-QM-RECONSTRUCTION` (§6) is a strict, honestly
  labelled refinement of the parent `ASSUMP-M1-INFO-RECONSTRUCTION`, with a named minimal import (GAP-1/2/3), a
  physical failure-meaning, and a single discharge lemma. It is ready to be registered by the registry owner — with
  the corrected `053040`→`063001` fix applied to all THREE built sites at the same time (not by this memo).
- **Open (load-bearing, correctly labelled):** **GAP-1** — continuous reversibility of pure-state dynamics
  (Hardy H5 = MM4 = CDP C6-core). Unowned foundationally and in tension with `00.2:55`. Discharge lemma stated in §6;
  currently unproven. This is the single obstruction between bridge-made-explicit and CORE.
- **Open (restrictable, not obstructions):** GAP-2 (universal tomographic locality / subspace equivalence, owned
  only on the scene tensor) and GAP-3 (measurement closure vs. Born-only restriction). Both restrictable-to-scene;
  honest partials, not blockers.
- **No re-opened NO-GOs.** The `00.2:55` non-invertibility NO-GO is cited and worked *within* (it is the source of
  GAP-1's tension), never silently re-opened.
