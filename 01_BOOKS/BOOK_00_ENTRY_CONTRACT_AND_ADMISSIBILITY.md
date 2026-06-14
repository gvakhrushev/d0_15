<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 00 — Entry Contract and Admissibility Discipline

> Scope: Entry contract, admissibility rules, claim language, and publication guardrails.
> Claim discipline: This book owns reading rules, not physical-sector closure.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 00.16 Active entry contract

D0 v15 is a finite-observability framework over condensed/profinite quasicrystalline support. The primitive object is the finite/profinite support with admissible projections and finite tick maps. The closed-vacuum feedback operator

```text
F_N = P_N U_N^dagger Q_N U_N P_N
```

is not the primitive support. It is the central derived dynamical operator of v15.

The reader may ignore D0 mnemonics and follow:

```text
support -> projection -> finite operator -> response law -> sector reduction -> bridge/passport.
```

Every major physical phrase in the corpus must follow:

```text
standard object -> finite D0 operator -> theorem/sector law -> bridge/passport boundary
```

Forbidden:

```text
D0 slogan -> metaphor -> status row
```

Book 00 fixes the public contract: finite support is prior to dynamics; the retained/traced split produces `P_N` and `Q_N`; `R_N = D_N^dagger D_N` is positive readout/Born response; `F_N = P_N U_N^dagger Q_N U_N P_N` is feedback return / unitarity defect; `U_eff = P_N U_N P_N` is compressed nonunitary pole dynamics; `mathsf P_fb = beta^(-1) partial_V log Z_N` is feedback pressure; external comparison is a bridge/passport layer.

The v15 master synthesis is `03_THEORY_MAP/D0_v15_MASTER_SYNTHESIS.md`. The publication outline is `03_THEORY_MAP/D0_v15_PUBLICATION_OUTLINE.md`.

## 00.0 Publication entry status

v16 keeps the condensed φ-vacuum support as a finite/profinite quasicrystalline hull; the active dynamics are derived later through `F_N`, not inserted as primitive smooth space.

**Status:** `SCIENTIFIC-FRONT-MATTER / PROCESS-ARCHITECTURE`.

**Current constructive closure entry guide.**  The active archive now has a
machine-checkable final bridge index:

```text
D0.Bridge.D0_FINAL_FOUNDATION_INDEX
```

That index imports and checks the closed theorem groups for topological
primitives, variation/stress/Poisson, matter source and localization, operator
origin, scalar/vector/edge equations, gauge kinetic positivity, finite
Wilson-link covariance, graded-incidence Bianchi closure, entropy cosmology,
the spectral GR ladder, SM-facing finite gauge decomposition, typed SI calibration and the observable-transfer boundary.  Book
00 should therefore be read as the entry contract to the current typed-closure
foundation entry: major claims must cite one of a Lean theorem, a finite
certificate, an explicit no-go, or a bridge/comparison protocol/external-data status cell.

The closure count is generated from `HARD_CLOSURE_TARGETS.csv` and the hard-closure runner. Book 00 deliberately does not treat counts as a proof object: the active requirement is that each major claim names its theorem/cert/no-go/bridge owner and that obsolete prose cannot return through the synchronization guards.

Book 00 is not a physical sector of D0.  It is the entrance contract for the corpus: it states what counts as a D0 claim, how finite measurement is admitted, how later bridge languages are read, and how the books prevent numerical coincidence from being promoted into theory.

The active theoretical books are Books 01--08.  Book 00 does not replace their proofs.  It fixes the reading order and the admissibility rules under which those proofs are to be interpreted.

D0 detector/vacuum support is a finite information quasicrystal.  The finite
information quasicrystal owner includes `quasicrystal_order_not_periodic_lattice`.

## 00.1 Standard-language protocol

D0 uses a compact internal vocabulary, but the active scientific corpus must be readable in standard mathematical and physical language. Therefore every D0-local term is introduced as an abbreviation for a standard object:

```math
\begin{aligned}
\text{archive} &:= \text{traced-out complement / unresolved environment},\\
\text{forgetting} &:= \text{conditional expectation, partial trace, or RG coarse-graining},\\
\text{readout} &:= \text{positive operator-valued instrument outcome},\\
\text{terminal readout} &:= \text{rank-reducing absorbing measurement channel},\\
\text{comparison protocol} &:= \text{external comparison protocol},\\
\text{carrier} &:= \text{representation carrier or compact Lie carrier algebra}.
\end{aligned}
```

The D0 name is the framework identifier. The proof is the support object, the operator, the response functional, the quotient or coupling, and the falsification condition. A reader may ignore the D0 mnemonic and follow the standard object alone.

### The three status layers: CORE / FORMALISM / BRIDGE

The dictionary above is not free: each standard object is admitted at exactly one of three status layers, and the layer fixes what a claim is allowed to depend on. This is the status calculus that disciplines the whole active corpus [^b00-1].

**CORE (constructive axiomatics).** CORE fixes only constructive objects and procedures derivable from BOOK_01 without exogenous parameters: finite codes and the canonicalization `D_min`; finite graphs and operators on finite sets; computable distinguishability tests and finite sums. CORE is where M1 actually bites — physics is what survives self-distinguishability without an external catalog (M1; DEF-0.2.2 forcing-by-contradiction), so a CORE object must be exhibitable as a finite construction, not posited.

**M1+ (the primitivity ban).** M1+ is the admissibility refinement of M1 used throughout the books: in CORE it is *forbidden* to introduce `\(\mathbb{R}\)`, `\(i\)`, `\(\hbar\)`, `\(c\)`, `\(G\)` as primitive entities. These are not banned from the theory — they are admissible only as BRIDGE representations, downstream of a fixed calibration. Status: FORCED. The argument is by contradiction: a continuum primitive carries an uncountable label set, which is exactly an external catalog that M1 refuses; admitting one as CORE would smuggle in the comparison standard the theory is required to construct [^b00-2]. The five continuum constants therefore enter as BRIDGE units (see BOOK_00 §00.12 bridge austerity), never as CORE sources.

**FORMALISM (algebraic representation).** FORMALISM is the set of mathematical representations into which CORE embeds *without changing the class of distinguishable outcomes*: Hilbert representations, spectral triples, `\(\zeta\)`-regularization; continuum approximations (heat kernel, smooth limits) **provided** the limiting procedure and a falsification criterion are stated; standard theorems (Gleason, spectral decomposition) admitted as bridge-theorems, never as new axioms. FORMALISM is a language, not a source: any invariant it computes must already be a CORE invariant.

**BRIDGE (phenomenological mapping).** BRIDGE maps CORE/FORMALISM invariants to familiar physical quantities and units (SI, etc.). Every BRIDGE step must (i) fix its calibration regimen explicitly, (ii) separate tuning parameters from check parameters, (iii) preserve a binary PASS/FAIL at the distinguishability level [^b00-3]. The constructive ordering proof object > finite/profinite construction > certificate > comparison protocol is owned by §00.13 — this layer is its status face, not a second copy.

### Finite-observer language: localized packets, not global modes

A consequence of M1+ that the protocol must state explicitly. On a compact discrete scene the global harmonic basis — Fourier modes, infinite-duration eigenmodes — is admissible FORMALISM language, but applying it to a *finite* observer requires an external truncation-or-precision rule: where to cut the mode sum, to what accuracy. That cutoff rule is an external catalog, so an unqualified global-mode description violates M1+ unless it carries an explicit internal procedure. Status: FORCED [^b00-4].

The CORE-compatible language of finiteness is therefore the localized spectral packet (wavelet basis): a basis that localizes simultaneously in scale and in diffusion "time" and so carries a built-in UV/IR regularization with no external catalog. The choice "wavelet packets over global modes" is not a modeling preference — it is the only finite-observer language consistent with the no-external-catalog law. Status: FORCED. Cert obligation for the explicit UV/IR-bound statement: PROOF-TARGET (cert obligation open).

## 00.2 Primitive thesis

D0 is a finite-observability framework over a condensed/profinite φ-quasicrystalline tiling hull.

Its primitive object is not a smooth continuum, not a particle field and not a string vacuum.
Its primitive object is finite detector readout over a condensed/profinite support (the physical model is the condensed φ-quasicrystalline tiling hull).

### What question the corpus answers

D0 does not postulate physical laws "by analogy" with the observed world. It asks the prior question: *what criteria must any theory satisfy to be finite, verifiable, and free of observer arbitrariness?* The whole corpus is the answer to that question, and the answer is driven by exactly two principles [^b00-9]:

- **M1** — no exogenous parameters: no background dependence, no external catalog. Physics is *what survives the requirement to distinguish itself without outside help.* The question "why is the world this way?" changes grammar under M1: the world is the fixed point of "describe yourself, borrowing nothing from outside" — not "which laws did someone pick," but **which structure is uniquely compatible with its own existence as a record.**
- **M1+** — the constructive recursion stop rule: descriptions canonicalize to the minimal record `Can(S)` rather than recursing without end [^b00-10].

D0 is architectural, not a competitor to QM/GR/SM: it fixes the minimal distinguishability-and-self-consistency skeleton on which any theory becomes formally checkable, comparable and auditable [^b00-11]. Upper-floor theories are admitted as FORMALISM/BRIDGE layers (continuum, fields, integrals, metrics, Lagrangians) provided each declares its internal projection onto a PASS/FAIL test.

### M1 is the single law, read on two levels

M1 is not one axiom among several; it is **the single law**, and everything else is the theory of survival under it. M1 manifests on two levels that must be held together [^b00-12]:

- **Algebraically** — minimality (MDL/Kolmogorov): the shortest record, empty catalog.
- **Operationally** — no hidden degrees of freedom: it is forbidden to keep a side-register "which one of."

φ and M1 are *one object read statically and dynamically* (duality lemma; φ forcing owned in BOOK_01 §01.6, from `p+p^2=1`). The self-description equation `p^2+p=1` is not a branch-balance: it **defines the object through its own dynamics** — whole = one act + the act applied to itself. Not "an object that has a dynamics," but "an object that **is** its own recursion." Falling = looping = rational capture = keeping a repetition catalog = ⊥M1.

### Method: forcing-by-contradiction, not enumeration

The corpus is built by forcing, not by search. This is the dividing line between a THE-claim and a HYP-claim, and it is easy to mistake for numerology if missed [^b00-13].

- **Enumeration (forbidden as proof):** "K(9,11,13) is better than other graphs" — bottomless; one can always answer "but you didn't try this one." Search proves nothing.
- **Forcing (DEF 0.2.2 schema):** assume `¬X`; show `¬X` requires extra structure `θ` not fixed by prior DEF/THE; `θ` affects distinguishable outcomes, hence is an exogenous parameter; that contradicts M1; therefore `X`. This strikes not at candidates but at **any** alternative at once, through the single property "requires a catalog."

Worked forcings (these are derivations, not associations):

- *Why 4 roles?* Fewer — the act leaves no distinguishable record, or requires external memory.
- *Why Q₈?* A non-normal subgroup yields conjugate copies, hence a "which copy" catalog, hence ⊥M1; what survives is the Hamiltonian non-abelian group ⇒ Q₈ (Dedekind-1897 minimality).
- *Why the torus?* Memory of two independent loops; a torus is abelian ⇒ loop order is not encoded ⇒ defect.
- *Why stop at 13?* **Not** "because 15 is worse." Three zones because there are exactly three structural necessities (defect, memory, shell); there is no fourth role, so no fourth zone.

Operational rule for any reviewer [^b00-14]: when scoring a claim, do not ask "does the number match," ask "which `¬X` is impossible here, and why does it require a catalog." If a forcing exists, it is a THE-candidate; if only a numerical coincidence exists, it is HYP and owes an E-account.

### The Finite Holographic Self-Reading Principle

The two-level M1 reading concentrates into one rigid operator rule [^b00-15]:

> **Finite Holographic Self-Reading Principle.** Physical information is realized exclusively through a finite holographic readout whose response preserves a symplectic (area-preserving) form across the cut between the retained (active) sector and the archive (traced) sector. The detector must read itself autonomously — hidden states and external memory backgrounds are strictly forbidden.

From this principle the structural spine emerges by exact algebraic obstruction, not by choice. Two of these routes give independent (non-algebraic) derivations of facts BOOK_01 forces algebraically:

1. **2D Gleason closure.** A non-degenerate symplectic form requires a minimal 2D phase space; enforcing area-preservation there topologically forces the quadratic Born response (the Born/quadratic-response closure is owned in §00.13; this route corroborates it from the symplectic side). [^b00-5] for the symplectic-route statement.
2. **Fibonacci fusion bottleneck.** The strict absence of hidden memory forces the readout to obey the minimal non-trivial topological fusion rule `τ ⊗ τ = 1 ⊕ τ`, isolating φ as the exact minimal quantum dimension permitted by the Jones subfactor index. This is a *second* route to φ, independent of the algebraic forcing `p+p^2=1` owned in BOOK_01 §01.6. [^b00-6] for the fusion/Jones route.
3. **Discrete Darboux extensions.** The structural carrier expands strictly via conjugate symplectic pairs (`+2`), generating the unique `K(9,11,13)` tripartite tensor network — a topological route to the scene that BOOK_01 reaches combinatorially (three necessities ⇒ three zones; scene owned in BOOK_01 §01.8). [^b00-7] for the Darboux-route statement.
4. **Topological index.** The dimensionless action cycle emerges as the homological rank-nullity index of this holographic carrier (rank 3 = space, nullity 30 = traced archive); the action section `Λ_act = 38` is owned in BOOK_03 §03.18, not re-derived here.

Because the principle forces the Fibonacci rule `τ ⊗ τ = 1 ⊕ τ`, the readout operation `τ` has no algebraic inverse: the fundamental symmetry is a **non-invertible categorical symmetry**, so structural time-irreversibility is an algebraic inevitability rather than a statistical artifact, and unitarity is recovered only as an emergent low-energy shadow. [^b00-8].

### Carried objects and the feedback layer

The integer time automorphism T generates the φ/Galois split, Lucas trace layers, Lefschetz scene counts and trace-heat gravity.
Observable sectors are represented by standard finite objects over this support: positive measurement outcomes, defect classes, holonomies, domain-wall operators, K0 gap labels and boundary-capacity saturation.  When a finite sector is split into retained and traced-out parts, the downstream closed-vacuum feedback layer may form the derived return-defect operator

```math
F_N=P_NU_N^\dagger Q_NU_NP_N,\qquad Q_N=I-P_N.
```

This feedback object is not primitive support and is not the Born/readout response.  The same retained/archive split also distinguishes the positive readout/Born response `R_N=D_N^\dagger D_N` and the compressed effective dynamics `U_{eff}=P_NU_NP_N` from this feedback resolvent (F_N feedback operator owned in BOOK_01 §01.2).

Closed-vacuum feedback owner: `D0.Dynamics.InternalFeedbackResolvent`. The no-external-boundary rule is `external_mirror_model_forbidden`: because the support has no outside, every attempted escape from the retained sector can only reappear as internal boundary response. This is M1 read operationally — there is no outside to escape to, hence no external catalog to escape into.

RG, spectral-action, cosmology and gauge-facing physical language is assembled only in `D0.Bridge.InterpretationSpine.InterpretationPackage`; it may not be inserted directly into a core theorem row.
## 00.3 Admissible measurement skeleton

A continuum-measurement skeleton is the scale-connectivity structure required for a continuum to be measured by a finite detector:

```math
\mathfrak C_x=(\mathcal S_x,\rho_x,\Delta_x),
\qquad
\mathcal S_x=\{Q_0x^k:k\in\mathbb Z\},
\qquad
\rho_x(Q_k)=Q_{k+1}=xQ_k.
```

The statement is not that a mathematical continuum is only this countable skeleton.  The statement is that physical resolution requires a law of scale-connectivity before it can be compared by a finite detector.

```math
\boxed{
\text{continuity is not point-density; continuity is lawful scale-connectivity.}
}
```

The first detector closure is constrained by four obligations: finite binary distinguishability, self-return, internal unit closure, and absence of a hidden coefficient.  If the direct channel has weight `p`, the minimal return/comparison channel has weight `p^2`, and internal closure gives

```math
p+p^2=1.
```

Thus

```math
p=\frac{\sqrt5-1}{2}=\varphi^{-1},
\qquad
x=\frac1p=\varphi,
\qquad
\varphi^2=\varphi+1.
```

The detector asymmetry quantum is fixed, not fitted:

```math
\delta_0=\frac{\varphi^{-1}-\varphi^{-2}}{2}=\frac{\sqrt5-2}{2}.
```

Book 00 uses this as a gateway theorem.  Book 01 constructs the finite support and scene; Book 05 owns the proof and uniqueness audits.

## 00.4 Condensed/profinite placement

The upstream object is not a smooth carrier.  The upstream test object is a weighted profinite detector support:

```math
S_{D0}=\{A,B\}^{\mathbb N},
\qquad
S_{D0}^\varphi=(S_{D0},\mu_\varphi),
\qquad
\mu(A)=\varphi^{-1},\quad \mu(B)=\varphi^{-2}.
```

The ambient condensed test functor

```math
\underline X(S)=\operatorname{Hom}_{Top}(S,X)
```

is too broad to be physics.  D0 uses a constrained finite-readout subfunctor

```math
\boxed{
\underline M^{D0}(S_{D0}^\varphi)\subset \underline M(S_{D0})
}
```

with finite factorization, φ self-return, quadratic response, single-section discipline, gate stationarity, archive/active separation, and explicit falsification hooks.

This is the placement rule for the rest of the corpus: carrier geometries, Standard Model language, GR, cosmology, scattering and survey likelihoods are downstream tests or shadows of constrained finite readout.  They are not alternative foundations.

## 00.4a D0 vacuum as condensed φ-quasicrystalline tiling hull

The D0 vacuum is the condensed/profinite hull of all admissible finite detector registrations.

The smooth spacetime manifold is a macro readout shadow.
The active visible geometry is obtained by φ cut-and-project projection from the archive/profinite support.

The tiling hull of this support is the carrier on which spectral operators, phason defects, holonomies, domain walls and archive pressure modes live.

## 00.5 Terminal alphabet and scene orientation

The first finite detector result is recorded in terminal roles, not in an unbounded continuum of untyped metadata.  The four roles are retained because they test four distinct failure modes of one quadratic closure:

| Role | Function in the detector grammar |
|---|---|
| A | unit normalization |
| B | conjugate-root coupling |
| C | active-branch recursion |
| D | archive/conjugate-branch recursion |

Together with the sign/conjugate branch they form

```math
ABCD\times\{+,-\}\Rightarrow\Omega_8.
```

Observed addressability requires a witness/basepoint:

```math
\Omega_8+\omega_0=V_9,
```

and the finite scene is oriented by the odd addressed runtime ladder

```math
V_9\rightarrow V_{11}\rightarrow V_{13},
\qquad
K(9,11,13).
```

Book 00 states this chain only as the entrance map.  Book 01 constructs it; Book 05 proves the finite-operator spine; Book 02 turns it into action/runtime operators.

## 00.6 The scientific reading order

Historical source numbers are retained only in migration manifests. The canonical proof dependency order is:

```text
00 entry contract
01 condensed finite support and graph birth
02 mathematical proof spine and invariant calculus
03 finite action operators and scene dynamics
04 spectrum, matter and finite selector theory
05 certificate discipline and negative controls
06 evolution, forgetting and time
07 gravity, finite geometry and Einstein macro-interface
08 cosmology, archive pressure and observable transfer
```

This order prevents later sector closures from being mistaken for first principles. A result is admitted only when its support, operator, normalization, proof/certificate owner, bridge type, and falsification hook are explicit.

### 00.6A Why M1 is forced, not chosen (AIT grounding)

M1 is not a philosophical preference. It is forced by contradiction with the self-reading requirement.

Claim: physics may admit an external catalog of empirical continuous constants. Then there must be an external memory (an Oracle) holding those constants and, in general, resolving arbitrary halting to read them back. But the law itself requires the system to distinguish itself with no external catalog (DEF-0.2.2; forcing-by-contradiction). An Oracle for arbitrary halting is exactly such an external catalog. Contradiction. So no exogenous parameter may enter — which is M1.

Stated in Algorithmic Information Theory: let `K(T)` be the Kolmogorov complexity of a theory `T`. A theory that imports an empirical catalog carries `K_catalog > 0` — the catalog cannot be regenerated from the theory's own finite primitives, so it would need that forbidden external store. D0 is generated from finite algorithmic primitives only, so `K_catalog = 0`. By Solomonoff induction (`P(T) \propto 2^{-K(T)}`), the admissible structure is the one with empty external catalog: the minimal-complexity, maximal-probability distinguishable structure. Any nonempty catalog is a strictly less probable, exogenously parameterized theory — and, by the contradiction above, inadmissible.

This is why M1 is a derived spine and not an axiom of taste: admitting the Oracle re-admits the external parameter the law forbids.

[^b00-17]
[^b00-16]

## 00.7 Relation to established physics

D0 does not ask the reader to discard quantum theory, QFT, the Standard Model, or general relativity.  It changes their logical placement:

```math
D0\overset{\mathcal D_Q}{\longrightarrow}QM/QFT\overset{\mathcal D_C}{\longrightarrow}classical/GR/cosmology.
```

A Standard-Model comparison uses a typed dressing functor, not a hidden fit:

```math
\mathfrak D_{SM}^{D0}(\tau)[O]
=
\mathcal P_{phase}(\tau)
\mathcal R_{SM}(s_K(\tau);\Lambda_{act})[O]
\mathcal P_{name}.
```

The functor may apply ordinary radiative, renormalization and naming conventions.  It may not change the D0 support operator, choose a post-hoc permutation, or introduce a second mass/action scale.

## 00.8 Proof ownership and promotion discipline

D0 separates proof, calculation and comparison.  A certificate can verify arithmetic, finite matrices, dependency graphs and tolerances.  It does not by itself prove uniqueness of the selected expression.

```math
\text{proof of selection}\ne\text{certificate of calculation}.
```

### The admissible proof protocol

D0 admits exactly one proof protocol, and bans the rest.  Proof by "obviousness" is forbidden: a result is never licensed because it looks evident, is conventional, or matches a textbook.  The only admissible engine is **Reduction-to-Contradiction-with-Realizability** [^b00-19].  Status: METHODOLOGICAL-LAW (this is the forcing engine the M1 gate exists to protect; without it "THE/LEM/DEF" lose their meaning — see COR 0.4.3, owner GOLDEN §0.4).

This ban is what M1 protects.  M1 (no obligatory external catalog) is a statement about admissibility, not about physics; the proof protocol is the procedure that turns M1 into an actual derivation.  A claim that cannot be forced by this protocol is at most a HYP, never a THE.

### DEF-0.2.2 — forcing-by-contradiction via exogenous parameterization

The load-bearing recipe of the whole corpus is the named 5-step schema [^b00-20].  To prove a statement `X`:

```text
(i)   assume not-X;
(ii)  show that computing / reproducing the result then requires extra structure theta,
      not derivable from previously introduced DEF/LEM/THE;
(iii) fix that theta affects distinguishable outcomes, hence theta is an exogenous
      parameter in the sense of DEF 0.3.1;
(iv)  theta therefore violates M1 (THE 0.4.1);
(v)   so not-X is impossible and X is forced.  []
```

Status: CORE-FORCING-SCHEMA.  This is "forcing = contradiction via exogenous parameterization" stated as an explicit, reusable recipe rather than as ad hoc per-result contradiction arguments.  Every forced claim in the corpus — phi from p+p^2=1, delta0, Q8~Omega8 minimality, the K(9,11,13) scene, the toral time generator — instantiates this schema with a different θ.  When a section says "(forced)" it means: the negation demands an undefined, outcome-affecting structure, and that structure is an exogenous catalog M1 forbids.

The exogenous-parameter test (DEF 0.3.1, owner GOLDEN §0.3) is the hinge of step (iii)–(iv): θ counts as exogenous iff it (1) is not derived inside the corpus, (2) affects a distinguishable result or a law's formulation, and (3) is not an unavoidable part of the distinguishability protocol.  A required-but-not-distinguishing addition is, by LEM 0.4.1a (the dichotomy of an added structure K), exactly a hidden external catalog and falls to M1.

### THE-0.4.5 — the minimality / canonicity template

Uniqueness and minimality claims are not asserted per-result; they are forced by one reusable template [^b00-21]:

```text
(A) assume an equivalent description of smaller complexity, or of other structure;
(B) show it either violates M1 (introduces an obligatory selection super-structure / catalog)
    or contradicts the canonization rule (DEF 0.5.x ordering, owner GOLDEN §0.5);
(C) conclude the chosen description is minimal-canonical.
```

Status: CORE-FORCING-SCHEMA.  This is why D0 does not argue by enumeration of alternatives: the family of M1-equivalent extensions is infinite (EX 0.4.3 / LEM 0.4.4, owner GOLDEN §0.4), so "variant 1 is wrong, variant 2 is wrong, ... therefore mine is right" never terminates.  The protocol does not *choose the best* description — it *takes the only admissible one* by ruling out every cheaper or alternative competitor through M1 or the canon order.  Minimality claims in this corpus (Q8 = the Dedekind-1897 minimal example; the K(9,11,13) rank-3 / nullity-30 scene) are instances of THE 0.4.5, not standalone assertions.

### Promotion discipline

An active theorem requires both a proof of admissibility (forced by the protocol above) and a reproducibility/falsification hook.  The minimal promotion chain is

```math
\text{finite support}\rightarrow\text{operator}\rightarrow\text{stationarity or trace theorem}\rightarrow\text{certificate}\rightarrow\text{typed bridge}\rightarrow\text{falsification hook}.
```

A certificate sits at one link only: it discharges the *calculation* obligation (arithmetic, finite matrices, dependency graphs, tolerances).  It never discharges the *selection* obligation — that is owned by the DEF-0.2.2 / THE-0.4.5 forcing schemata above.  A forcing claim still lacking its calculation cert carries `[^b00-18]`; it is never backed by a fabricated cert token.

Mapped Book 00 claims are:

| Claim ID | Status | Claim | Certificates / ledgers |
|---|---|---|---|
| `D0-FOUND-001` | CORE-FOUNDATION | No-monopoly verification algebra | (see canonical registry); minimal Popper/dyad certs |
| `D0-FOUND-002` | CORE-FOUNDATION | Minimal addressable record split | (see canonical registry) |
| `D0-FOUND-003` | CORE-FOUNDATION | Minimal continuum-measurement skeleton | (see canonical registry) |
| `D0-SCENE-001` | CORE-SUPPORT | Omega8 detector cycle | d0_core_certificates.py; (see canonical registry) |
| `D0-SCENE-002` | CORE-ACTION | J_scene selects K(9,11,13) | d0_graph.py; d0_core_certificates.py; (see canonical registry) |
| `D0-META-001` | DIAGNOSTIC-ONLY | Active corpus integrity and reader-orientation checks | vp_book*; vp_*refactor*; vp_full_book_audit* |
| `D0-PROOF-PROTOCOL` | METHODOLOGICAL-LAW | Only Reduction-to-Contradiction-with-Realizability admitted; "obviousness" banned (GOLDEN §0.2) | n/a (protocol-level; gates every THE) |
| `D0-FORCING-SCHEMA` | CORE-FORCING-SCHEMA | DEF-0.2.2 5-step forcing via exogenous theta; THE-0.4.5 minimality/canonicity template (GOLDEN DEF 0.2.2 / THE 0.4.5) | n/a (schema instantiated per forced result) |
## 00.9 Anti-numerology firewall

A numerical match is not a theorem.  A D0 expression may be promoted only when the admissible search space and uniqueness reason are stated.

```math
\text{admissible grammar}+\text{finite support}+S_{gate}\text{ or }\operatorname{Tr}_K\text{ selection}\Rightarrow\text{unique readout}.
```

The hostile-reading question is mandatory:

```math
\text{Could a different admissible finite expression hit the same benchmark?}
```

If the answer is yes, the result remains a stress test.  If the answer is no, the active book must show the M1, gate, trace, finite-spectrum or stationarity reason why alternatives fail.

### The law the firewall enforces: M1

The firewall is not a heuristic — it is the operational face of the single law the whole D0 spine is forced from. BOOK_00 owns the statement of that law; everything below states *why* the firewall facts (no-monopoly, no fitted catalog) hold.

**Exogenous parameter — the thing M1 forbids [^b00-24].** An *exogenous parameter* (background dependence) is required-but-underivable structure — a constant table, an exception list, an external label, an index-scheme, a choice rule — satisfying all three clauses at once:

1. it is **not derived** inside the corpus (does not follow from the axioms);
2. it **affects the result** or the statement of the laws;
3. it is **not an inevitable part of the distinguishability protocol**.

Canonical example: the Standard-Model list of particle masses is exogenous — the theory does not explain it, it reads it from a catalogue [^b00-25]. A parameter `K` counts as *mandatory* [^b00-26] when without `K` you cannot (1) compute a claimed quantity, (2) run a `VER`/`CHK`, or (3) let an independent executor reproduce the result from the published corpus. Anything else is an optional format convention and may not appear as a necessary part of a law.

**M1 — the central correctness law [^b00-27].** *Principle M1 = ban on a mandatory external catalogue.* This is the central correctness rule of the axiomatic base, the blade that severs infinitely-flexible non-falsifiable extensions:

```math
\text{If two constructions give the same class of distinguishable outcomes, the one requiring an extra mandatory external catalogue/parameter is inadmissible.}
```

"No-monopoly verification" and "no fitted catalogue" are downstream *effects* of M1; M1 itself is the named theorem they descend from.

**M1 = MDL for physical laws [^b00-28].** Let `K(·)` be (conditional) Kolmogorov complexity in a fixed universal language. Adding an underivable `theta` moves the law from `K(T)` to `K(T) + K(theta | T)` — it strictly increases the minimal description length. M1 forbids exactly such increases at an unchanged distinguishable class. So M1 is a Minimum-Description-Length principle for physical laws, not an aesthetic preference. This is the precise WHY the firewall has teeth: a numerological add-on is, formally, longer code at equal predictive content.

**External corroboration of M1 (cited owners, not re-derived).** M1's finite-distinguishability premise is not only a self-imposed economy — it is the exact hypothesis from which quantum theory is *reconstructed* externally. The operational reconstruction theorems — Hardy (arXiv:quant-ph/0101012), Dakić–Brukner, Masanes–Müller (*New J. Phys.* 13, 053040, 2011), Chiribella–D'Ariano–Perinotti (*Phys. Rev. A* 84, 012311, 2011) — show that a **finite information capacity** of an elementary system, plus continuity and tomographic locality, *uniquely* yields the complex Hilbert-space structure of QM. So the finite-capacity law M1 has, as a downstream theorem, the entire structure of QM (owner edge `D0-M1-INFO-RECONSTRUCTION-001`, `ASSUMP-M1-INFO-RECONSTRUCTION`). Relatedly, that structure must be **complex**, not real: real-vector-space QM is experimentally excluded (Renou et al., *Nature* 600, 625, 2021; Chen et al., *Phys. Rev. Lett.* 128, 040403, 43σ; Li et al., 5.30σ) — owner edge `D0-COMPLEX-QM-FORCING-001`, `ASSUMP-COMPLEX-QM`. Honest scope: these are **cited external owners** (the reconstructions assume continuity + tomographic locality; the experiments assume the standard QM postulates), corroborating the D0 axiomatic base, not derived inside D0 — BRIDGE, never core.

**The dichotomy blade [^b00-29].** Add structure `K` to a construction. Exactly one holds:

- **(A)** `K` **changes** the class of distinguishable outcomes → `K` is contentful and *must* be derived/justified inside the corpus; or
- **(B)** `K` **does not change** the distinguishable class → `K` carries no distinguishability; if it is nonetheless mandatory (DEF 0.3.1a) it is an external catalogue (DEF 0.3.1) and is banned by M1.

Proof (by contradiction): suppose an exogenous parameter is mandatory yet distinguishability-neutral. Then (1) the catalogue cannot be falsified through distinguishability — it changes no `0`-vs-`1` outcome; (2) it is required for the theory to run; (3) therefore the theory's operation depends on an underivable, untestable convention; (4) this violates DEF 0.3.3 (no dependence on hidden conventions). Contradiction [^b00-30]. This dichotomy is the operational decision procedure the firewall executes on every candidate add-on.

**Why M1 is the keystone, not a physics claim [^b00-31].** Without M1 there is no *end* of definition and no *end* of proof: any statement can be modified forever by external corrections (`a = b + c -> a = b + c + c1 + c2 + ...`). Then three distinctions collapse — axiom vs ad-hoc assumption, theorem vs fit, refutation vs rescue-by-new-parameter. So M1 is not an assertion about physics; it is the **minimal condition under which the THE/LEM/DEF language is meaningful at all** [^b00-32]. This is the deepest justification of the entire method.

**The infinite-recursion intuition pump [^b00-33].** Format conventions (symbol order, alphabet) are allowed when they add no information [^b00-34]. But a description `A = B + C` is equivalent to an *infinite* family `A = B + C + 0`, `A = B + C + eps_1(interaction_1)`, ..., `A = B + C + ad_hoc_n`. At every step `n` an opponent asks "why did you stop here? why not term `n+1`?" To answer "term `n+1` is zero" you need a justification: if it is derived, fine; if not, zeroing the term is an arbitrary choice — an element of an external catalogue of zeros [^b00-35]. M1 is what terminates the recursion. This is the intuition that makes M1 *necessary*, not merely convenient.

**Take the only-possible, never the best [^b00-36].** A theory cannot be proved by enumeration of alternatives ("variant 1 fails, variant 2 fails, ... so mine is right"): since the family of equivalent extensions is infinite (EX 0.4.3), the enumeration never terminates. The only way to a finite theory is to forbid every add-on that needs external specification — **we do not "select the best", we "take the only-possible"** [^b00-37]. This is the forcing-vs-fitting distinction the hostile-reading question above is the field form of: a "yes" answer means selection survived, a "no" answer means the object was forced.

**M1+ — canonization is the only admissible addition [^b00-38].** The constructive companion that halts the description recursion. Let `S` be the set of all representations of one and the same distinguishable object. Then (1) any mandatory in-class distinction not reducible to choosing `Can(S) := min_{<=}(S)` is a banned external catalogue (by M1); (2) to stop the infinite recursion (EX 0.4.3) one *must* fix a canonical representative [^b00-39]. Proof: not fixing a canon forces you to store the *choice* of a specific spelling; that choice does not affect meaning but costs memory and demands an index — and the choice-index is itself an exogenous parameter. Taking the minimal element automatically removes the index. So M1+ is the second half of the foundational law: M1 forbids the catalogue, M1+ removes the last surviving one (the representative-choice index). The ordering `<=` (length-first, then lexicographic) is itself format, not content [^b00-40].

### The science/numerology boundary is instrumental, not aesthetic

`phi` as a *forced* constant is numerology by no measure: extreme irrationality by Hurwitz (a theorem), the quantum dimension of Fibonacci anyons, the last KAM torus, Shechtman quasicrystals (Nobel), the `E8`-spectrum mass ratio measured in CoNb2O6 (Coldea 2010, an experiment). That is not a "pretty number" — it is measurable physical fact plus proved mathematics. Numerology does not begin with `phi`; it begins with the *manner of use* [^b00-41].

- **Numerology:** a `phi`-combination back-fitted from a rich stock of small integers with no look-elsewhere accounting. (Calibration case: `710 = 2·355`, `113` read as *free integers* fit to `2·(355/113)`, a known approximation of `pi`, is numerology. The discriminant is **grammar-priority** (§05.8.R): the claim `D0-EW-WINDOW-FORCING-001` (§07.23) instead reads both numbers as *closed named-invariant expressions* — `710 = 2·D_Σ·(2|V|+D_Σ)`, `113 = (|ABCD|+1)·d₁₃+|V₁₃|`, zero free numbers — plus continued-fraction minimality of the `2π` near-return. That is forcing *iff* the invariant grammar was fixed independently of the `2π` target; a reader who rejects grammar-priority reads it as this failure example. The two readings are distinguished only by whether the grammar is prior, never by the closeness of the fit.)
- **Science:** a forced constant with a frozen protocol, OR a number that entered the data *after* the grammar was frozen, with honest E-accounting.

**E-accounting (mandatory for every `HYP`, forcing: transfer D0_PHILOSOPHY §4).** Declare the grammar of admissible expressions *before* looking at the data; then compute

```math
E[\text{accidental}] = (\text{local density})\times 2\,|\text{miss}|
```

— the expected number of chance hits no worse than the one found. In isolation `E ~ 1` is noise. Strength comes *only* from family-coherence plus out-of-sample (numbers that were never targets, measured by independent processes). This is how the CKM quadruple became strong: `gamma, beta, alpha, J` are independent consequences of four constants — a coherent family, not four separate fits. The CKM-quadruple coherence is held by an existing finite certificate carrying its own external-convention firewall passport. The general E-accounting *procedure* itself has no cert owner. [^b00-22]

**Self-guillotine — the machine must kill its own finds [^b00-42].** Two worked rejections from this corpus, kept as the firewall's calibration:

- `sin^2 theta_12 = 9/40` — **rejected**: `40` lives only on the degree scale, i.e. a Babylonian catalogue; failing clause 3 of DEF 0.3.1 it is an exogenous label, banned by M1.
- `|lambda_3|/|lambda_2| ~ 2/phi` — **discarded**: `0.15%` miss with large `E`; E-accounting kills it as noise.

M1 thus acts as an automatic numerology filter, and the operational rule is absolute: **a cert that cannot return `FAIL` is not a cert** [^b00-43]. [^b00-23]

### Rejected forcing-links — the external-theorem audit (kept as calibration)

A systematic search for classical *forcing-owner* theorems (uniqueness/classification) that
could own D0 links (the "Frobenius-class" audit) produced genuine owners — Jones index for
`phi` (§01.21.3), Mordell for `E_8` (§02.18), Connes/Tomita–Takesaki for geometry/time — but
also a list of links the audit **refused**, because a number-coincidence or a structural
resemblance is not forcing. They are recorded here so the same coincidences are not re-proposed:

- **Leech lattice `Λ₂₄` ↔ readout kernel `K=30`** — *rejected as forcing.* `Λ₂₄` has rank 24;
  the scene kernel `K(9,11,13)` has nullity 30. `24 ≠ 30`, and D0 carries no 24-dimensional
  object, so the link is a *theme* (both are even-unimodular-lattice topics), not a forcing.
  (Distinct from the legitimate `E_8 → Λ₂₄` lattice tower of BOOK_02 §02.18, which is a *cited
  external construction* (Wilson 2009; Conway–Sloane), not a `K=30` identification.)
- **`Spin(8)` triality ⇒ exactly 3 fermion generations** — *rejected (HYP).* The "3" of triality
  is the number of 8-dimensional representations of `D₄` (`V, Δ_+, Δ_−`) permuted by
  `Out(Spin(8)) ≅ S₃` — **not** the number of fermion families. It is a content-coincidence of
  the integer 3; triality is a valid member of the *dimension-8* network (§02.18.3) for the
  number **8**, never for the number 3.
- **`C_max = 3/8` from Weinberg / Weinberg–Witten** — *rejected as the owner of the value.* The
  soft-graviton and Weinberg–Witten theorems force spin-2 and general covariance, not the causal-
  compactness threshold. `3/8 = rank/|Ω₈|` is forced by the D0 posing (`D0-COMPACTNESS-DEF-FORCING-001`),
  not by the spin-2 theorems; the value `3/8` must not be attributed to Weinberg.
- **Pisot substitution conjecture for `≥3` letters** — *open, not usable as a forcing.* Pure-
  discrete-spectrum (the time-layer forcing) is a theorem only for the 2-letter / degree-2 case
  (Hollander–Solomyak 2003), which covers `phi`. A `≥3`-letter Pisot forcing is an OPEN
  conjecture; the time-layer forcing stays scoped to degree-2.
- **Frobenius integrability theorem** — *structural scaffold, not an owner.* Involutivity ⇔
  integrability (unique maximal leaf) supports the golden-foliation picture, but forces no
  specific D0 object; it is a prop, not a forcing-owner, and is cited as such only.

The review-side rule that licenses this list is BOOK_05 §05.8.R: a critique may lower or refuse
a link only by **failing forcing-uniqueness (a named second object)** or by **naming an open
gap** — never by enumerating coincidences. Each refusal above names exactly why forcing fails.

(Owner note: BOOK_01 owns `phi`-from-`(p+p^2=1)`, `delta0`, the `F_N` feedback operator and the role alphabet; BOOK_03 owns `Lambda_act`. BOOK_00 keeps M1/M1+ and the admissibility contract — the law and its firewall — and cites the downstream `phi`-facts rather than re-deriving them.)
## 00.9a Gap-label firewall

A spectral number is admissible only if it is owned by:

1. a frozen finite operator;
2. a tiling-hull carrier;
3. a K-theory / K0 Gap Label or explicit spectral certificate;
4. an optional external passport.

K-theory and Gap Labeling cannot tune an operator after comparison.
They label spectra of frozen operators.

## 00.10 Benchmark closure table

The following table orients the reader.  It is not a proof table and must not be used as a selection principle.

| Object | D0 status | Readout/observable-transfer role | External comparison role | Used as input? |
|---|---|---:|---|---|
| electron full cycle | section dictionary | `Λ_act=38 m_e c^2` | SI unit section | yes, section only |
| neutron lifetime | single-section prediction | `877.8706191589381 s` | bottle/beam lifetime | no |
| `M_Z` | bare EW radial readout | `91180.882562 MeV` | pole/RG dressing | no |
| `M_W` | bare EW ratio readout | `80359.420522 MeV` | pole/RG dressing | no |
| `m_μ/m_e` | lepton generation readout | `206.769987111730` | PDG mass comparison | no |
| scalar amplitude | survey comparison protocol | `2.0553825512209827×10^-9` | CLASS/CAMB likelihood | no |
| Newton coupling | Planck-shadow bridge | `G_N^{D0}` | CODATA stress test | no |
| Born probabilities | internal theorem | finite trace ratio | QM/QFT shadow | no |

## 00.11 Spectrum before transfer

External observables are usually not the bare static coefficient.  They are the coefficient after a finite spectral transfer:

```math
\boxed{
\text{closed static coefficient}\rightarrow\text{finite spectrum}\rightarrow S_{DE}\text{/heat-trace window}\rightarrow\text{typed transfer}\rightarrow\text{observable comparison protocol}.
}
```

The allowed order is:

1. identify the already closed static coefficient;
2. identify the finite operator and active spectrum;
3. derive the transfer window from `S_DE`, heat trace, memory pressure, or the sector's finite return spectrum;
4. declare the typed transfer operator;
5. test holdouts and negative controls;
6. integrate the theorem only after the above survives.

The BAO/S_DE closure is the canonical example of the method.  It does not license arbitrary future fitting.

## 00.12 Bridge austerity

All external bridges are typed.  The following are downstream applications of finite readout, not new foundations:

- Standard Model and QFT: dressing and operator-comparison languages after finite support and response are fixed.
- General relativity: covariance and heat-trace forgetting shadow of finite line exchange.
- F-theory/carrier geometry: tested carrier application, not the source of D0.
- Cosmology: survey readout of archive pressure and finite-window transfer.
- Collider physics: transition probability, area section, luminosity/PDF/cuts/detector pipeline.

No bridge may introduce a hidden second anchor, a target-table fit, a new free forgetting map, or a post-hoc naming permutation.

## 00.13 Constructive formalization and EFT-matching discipline

D0 uses finite and profinite constructions as the normative layer of the theory.  Physical claims are not allowed to depend on an uncomputable continuum object, on an unrestricted choice principle, or on a hidden infinite regulator.  The continuum language used by established physics is therefore treated as a comparison and evolution language, not as the primitive source of a D0 invariant.

The constructive hierarchy is:

```text
proof object
> finite/profinite construction
> executable certificate
> external numerical comparison protocol
```

A proof object owns the theorem.  A certificate evaluates a finite invariant or a finite operator identity.  A comparison protocol compares the resulting invariant with an external convention, experiment, table or renormalization scheme.  This separation is part of the anti-numerology firewall: a floating-point comparison cannot replace a proof object, and a proof object cannot be demoted into a fit.

### CORE and BRIDGE: the admissibility split is forced, not a style choice

The constructive hierarchy is enforced by a two-layer typing of every promoted claim.  This split is not editorial taste; it is the only way M1 (no exogenous catalog) survives contact with SI/PDG observables, and D0 fixes its two layers by definition [^b00-44].

**CORE.**  A CORE statement is derivable *only* from the axioms and constructions of the corpus inside the internal algebra — typically `\mathbb Q(\varphi)` (the field BOOK_01 forces from `p+p^2=1`; see BOOK_01 §01.6) and the finite combinatorial objects of the scene `K(9,11,13)` — with no appeal to external numerical constants and no hand-chosen SI scale.  A CORE statement must be:

1. **finite/constructive** — it is an explicit construction, not an existence claim resting on choice or a continuum limit;
2. **representation-invariant** — invariant under any computable bijective re-encoding `f` of codes that preserves meaning-equivalence and the distinguishability bit `\Delta` [^b00-45]; changing alphabet/encoding moves only the carrier, never the `{0,1}` content;
3. **internally self-consistent under the `\varepsilon^2` gluing threshold** — *if two independent derivations of the same quantity disagree by more than `\varepsilon^2`, they are not the same statement* [^b00-46].  `\varepsilon^2` is the inter-derivation agreement scale, not a fit tolerance: it is what makes "two routes to the same invariant" a checkable identity rather than a coincidence.

The forcing behind the CORE definition is M1+ canonicalization (GOLDEN THE 0.5.4): any obligatory distinction inside a meaning-equivalence class `S` that does not reduce to selecting the canonical representative `\mathrm{Can}(S)` is a forbidden external catalog.  Refusing to fix a canon forces the corpus to store the *choice* of one particular record — an exogenous index with no effect on meaning — which M1 prohibits.  Hence the canonical (minimal-code) representative is taken automatically, and only algorithmic minimization, never "intuitive simplicity," is admissible [^b00-47].

**BRIDGE.**  A BRIDGE statement is the *packaging* of a CORE invariant into a standard observable (SI units, PDG parameters, cosmological `\Omega`, spectra, `H(z)`, and so on).  A BRIDGE statement is admissible only if it carries both:

1. **an explicit translation/calibration protocol** — what is fixed as the scale, which data are used only to set the convention, and which data remain a genuine test rather than an input;
2. **an independent falsification criterion** — a stated observation that refutes *this specific* BRIDGE variant, written so the translation cannot be silently re-tuned after the fact.

A BRIDGE object is an external-comparison object *unless a separate D0 theorem proves more*.  It may use the standard field content, beta functions and scheme conventions of the Standard Model; it may not introduce a hidden scale, a new field, a fitted threshold, or a post-hoc scheme switch.  Status: a claim that has only a CORE derivation but no discharged BRIDGE protocol is PROOF-TARGET at the bridge layer until both clauses above are supplied.

### Proof-assistant target

The intended formalization target is compatible with proof-assistant logic.  In a Lean/Coq-style reading, a foundational D0 theorem is a type inhabited by an explicit construction; a core certificate is a finite computation over algebraic numbers, matrices, graphs or finite spectra; an empirical comparison protocol is an exported comparison layer.  D0 does not claim that the present monograph has already been fully formalized in Lean.  It claims the stronger architectural requirement that promoted core claims must be expressible without nonconstructive physical primitives — which is exactly clause (i)/(ii) of the CORE definition above made into a typing obligation.

### The QFT/EFT bridge is one instance of the BRIDGE layer

The relation to quantum field theory is handled by the same discipline.  D0 does not reject QFT or the Standard Model.  It assigns them a typed role: the EFT-matching functor below is a *BRIDGE object in the sense of DEF 19.0.2*, and inherits both of that layer's obligations.  A D0 core invariant gives a finite ultraviolet boundary object.  A QFT/EFT dressing functor transports that object to the infrared convention used by an experimental comparison.  The bridge is therefore written as

```math
O_{\mathrm{D0}}^{\mathrm{bare}}
\;\xrightarrow{\;\mathfrak D_{\mathrm{SM}}^{D0}(\mathsf S,\mu,\Lambda_{\mathrm{act}})\;}\;
O_{\mathrm{SM}}^{\mathsf S}(\mu),
```

where `\mathsf S` is an explicitly declared renormalization scheme, `\mu` is the comparison scale, and `\Lambda_{\mathrm{act}}` is the single D0 action section (owned in BOOK_03).  The functor is a bridge/external-comparison object unless a separate D0 theorem proves more.  It may use the standard field content, beta functions and scheme conventions of the Standard Model; it may not introduce a hidden scale, a new field, a fitted threshold, or a post-hoc scheme switch.  The declared scheme `\mathsf S` discharges BRIDGE clause (1); a stated mismatch at the comparison scale `\mu` that would refute this matching discharges BRIDGE clause (2).

This is the publication rule: D0 may use established QFT as a Wilsonian infrared evolution engine, but every use must say what is core, what is bridge, what is scheme-dependent, and what would falsify the comparison protocol.
## 00.14 Rosetta stone for standard physics language

D0 uses finite-registration terminology because its primitive object is a finite detector record rather than a continuum Lagrangian.  For external communication these terms must always be translated into standard mathematical and physical language before a result is presented as a bridge claim.

| D0 term | Standard mathematical/physical reading | Status warning |
|---|---|---|
| condensed/profinite support | inverse system of finite test spaces; finite quotients of a profinite object | not a smooth spacetime primitive |
| D0-admissible subfunctor | finite-factorizing observable functor with response, halt and projection compatibility | not all continuous maps are physical observables |
| archive complement | traced-out / unresolved / quotient sector of a finite measurement | not a hidden matter sector by default |
| forgetting map | finite quotient, partial trace, decoherence map, or Wilsonian coarse-graining depending on sector | the sector must declare which one is used |
| terminal-destructive readout | inelastic/projection-like terminal response; a positive trace of a finite operator | not a reusable numerical correction |
| archive pressure | boundary/complement response entering a finite window or survey transfer | not a primitive dark fluid unless a separate operator is declared |
| dressing functor | EFT/RG/scheme-dependent comparison map from a bare D0 object to an external observable | cannot introduce new fields, scales or fitted exponents |
| comparison protocol | typed comparison with an external table, covariance, experiment or survey | not identical to a core theorem |

This table is not an analogy layer.  It is a bridge discipline.  A manuscript or book section may use D0 terms internally, but every external-facing claim must include its standard-language translation, bridge status and falsification hook.

## 00.23 Theory-improvement rule: no decorative layer

A pure change of status vocabulary is not theory improvement.  A claim improves
only when a proof owner, no-go, executable certificate or external passport
removes a concrete ambiguity.

Book 04 carries named finite selectors for the charged-lepton electron terminal,
the electroweak depth, the proton readout, the neutron archive sibling and the
beta-unlock depth.  Such selectors named as abstract labels are not enough: each
must discharge a concrete ambiguity through its proof owner or certificate.

CKM basis origin: the finite basis-origin selectors establish that the candidate
origin matrix is unique and that no free matrix survives at a fixed basis origin,
so the up/down bases are selected rather than fitted.

Finite spin-2 derivation: the finite weak-field quotient yields a transverse-traceless
representative and a closed conserved-stress spin-2 coupling, which replace the
forbidden shortcut "Poisson-like response therefore GR".

## 00.15 Assertion discipline

The monograph uses a two-layer assertion policy. A theorem may be internally closed when its finite proof cell is complete. An external comparison claim is stronger: it also requires the appropriate certificate, bridge declaration, data manifest and falsification hook.

This prevents the common failure mode in which a strong internal invariant is advertised as a fully reproduced external measurement. The canonical chain is:

```text
support -> admissible operator -> positive response or finite trace -> quotient/window -> certificate/owner -> typed bridge -> falsification hook
```

**Born quadratic-response closure.** D0 no longer treats the raw Born response as a supplied positive list. A finite phase-quadrature atom admits the general quadratic response `a x^2+bxy+c y^2`; internal quarter-turn phase blindness forces `a=c` and `b=0`, hence the response is a scalar multiple of `x^2+y^2`, and unit calibration gives the finite `D†D` response. Only after this step does finite normalization produce probabilities.

## 00.17 Self-substrate trace and informational mechanics

D0 assumes no external vacuum, no external observer and no background arena. Motion is the production of an internal trace by the same finite substrate that continues to evolve. A detector is an internal terminal readout node; an observer is not a primitive.

For a retained/traced split

\[
\mathcal H_N=\mathcal H_N^{ret}\oplus\mathcal H_N^{tr},
\qquad
P_N+Q_N=I,
\]

the trace intensity of a retained state \(\psi\) is

\[
\langle\psi,F_N\psi\rangle=\|Q_NU_NP_N\psi\|^2,
\qquad
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N).
\]

A finite event exists when internal circulation becomes addressable as such a trace. This entry principle supplies the ontological layer for CVFT and informational mechanics.


## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b00-1]: forcing: GOLDEN THE II.G.1-3
[^b00-2]: forcing: GOLDEN THE II.G.1
[^b00-3]: forcing: GOLDEN THE II.G.3
[^b00-4]: forcing: GOLDEN REM II.G.2.A
[^b00-5]: open obligation — cert obligation open
[^b00-6]: open obligation — cert obligation open
[^b00-7]: open obligation — cert obligation open
[^b00-8]: open obligation — cert obligation open
[^b00-9]: forcing: GOLDEN §0.0 / GOLDEN THE 0.5.4
[^b00-10]: forcing: GOLDEN THE 0.5.4; canonicalization discipline owned in §00.13 CORE typing
[^b00-11]: forcing: GOLDEN REM 0.0.A
[^b00-12]: forcing: GOLDEN, D0-PHILOSOPHY-AND-METHOD §1
[^b00-13]: forcing: GOLDEN DEF 0.2.2, D0-PHILOSOPHY-AND-METHOD §2
[^b00-14]: forcing: D0-PHILOSOPHY-AND-METHOD §2
[^b00-15]: forcing: v17 BOOK-00 §00.2, route-status PROOF-TARGET where noted
[^b00-16]: open obligation — cert obligation open
[^b00-17]: forcing: v17 BOOK-00 §00.2
[^b00-18]: open obligation — cert obligation open
[^b00-19]: forcing: GOLDEN §0.2
[^b00-20]: forcing: GOLDEN DEF 0.2.2
[^b00-21]: forcing: GOLDEN THE 0.4.5, the synthesis of M1+ with the reduction perp
[^b00-22]: open obligation — cert obligation open
[^b00-23]: open obligation — cert obligation open
[^b00-24]: forcing: GOLDEN DEF 0.3.1
[^b00-25]: forcing: GOLDEN DEF 0.3.1
[^b00-26]: forcing: GOLDEN DEF 0.3.1a
[^b00-27]: forcing: GOLDEN §0.4, THE 0.4.1
[^b00-28]: forcing: GOLDEN REM 0.4.1.MDL
[^b00-29]: forcing: GOLDEN LEM 0.4.1a
[^b00-30]: forcing: GOLDEN LEM 0.4.1a
[^b00-31]: forcing: GOLDEN COR 0.4.3
[^b00-32]: forcing: GOLDEN COR 0.4.3
[^b00-33]: forcing: GOLDEN COR 0.4.2 + EX 0.4.3
[^b00-34]: forcing: GOLDEN COR 0.4.2
[^b00-35]: forcing: GOLDEN EX 0.4.3
[^b00-36]: forcing: GOLDEN LEM 0.4.4
[^b00-37]: forcing: GOLDEN LEM 0.4.4
[^b00-38]: forcing: GOLDEN THE 0.5.4
[^b00-39]: forcing: GOLDEN THE 0.5.4
[^b00-40]: forcing: GOLDEN COR 0.4.2
[^b00-41]: forcing: transfer D0_PHILOSOPHY §4
[^b00-42]: forcing: transfer D0_PHILOSOPHY §4
[^b00-43]: forcing: transfer D0_PHILOSOPHY §4
[^b00-44]: forcing: GOLDEN THE 0.5.4 / DEF 19.0.1 / DEF 19.0.2
[^b00-45]: forcing: GOLDEN LEM 0.5.7a
[^b00-46]: forcing: GOLDEN DEF 19.0.1; the threshold itself is owned in BOOK III / `\Lambda_{\mathrm{act}}` accounting, see BOOK_03
[^b00-47]: forcing: GOLDEN THE 0.5.6
