<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 01 — Condensed Foundations, Finite Registration, and Construction of the Finite Incidence Graph

> Scope: Finite/profinite support, graph birth, retained/archive split, and terminal-role construction.
> Claim discipline: This book owns support construction; matter, gravity, and empirical claims are downstream.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 01.0 Active support/foundation layer

Book 01 is support and foundation only. It does not prove matter, gravity or cosmology claims. It supplies the finite/profinite carrier on which later books build operators.

```text
finite/profinite support -> graph birth -> retained/traced split -> P_N,Q_N -> finite tick U_N -> Book 02 feedback operator
```

At finite stage `N`:

```text
H_N = H_N^ret direct_sum H_N^tr,
P_N + Q_N = I,
P_N Q_N = 0.
```

`P_N` is the retained/readout projection. `Q_N` is the traced/archive projection. `U_N` is the finite tick. The handoff to Book 02 is:

```text
F_N = P_N U_N^dagger Q_N U_N P_N.
```

The support may be read as condensed/profinite quasicrystalline support: finite local pieces are visible, while projective/profinite organization prevents replacing the theory by a primitive smooth background lattice.

Finite Born support owners:

```text
D0.finite_effect_born_readout_unique
D0.finite_effect_born_no_hidden_response
```

## 01.1 Standard-language reading of the foundation

The foundational object is a profinite support represented as a condensed set on profinite test objects:

```math
S_{D0}=\varprojlim_N S_N,\qquad
\underline S_{D0}(T)=\operatorname{Hom}_{\mathrm{cont}}(T,S_{D0}).
```

A physical observable is not an arbitrary morphism out of this object. It is an element of an admissible subfunctor:

```math
\operatorname{Obs}^{D0}(S_{D0})\subset \operatorname{Obs}(S_{D0}),
```

with finite-stage factorization, projection compatibility, a positive response operator, and a halt quotient. Thus D0 words `registration`, `readout`, `four terminal roles A,B,C,D`, and `eight oriented terminal-role states Ω8` are local names for finite instruments and quotient data on this profinite/condensed support.

### 01.1.0 Σ as the realizability gate, not invented physics

The condensed support above is downstream. Upstream of every D0 object is a single criterion: the **distinguishability structure Σ**. Σ is not an attempt to "invent physics." It is the realizability gate that any theory claiming to describe distinguishable objects is obliged to implement. A theory that asserts it has objects, measurements, or memory but fails to realize the components of Σ is either a tautology or a non-reproducible fantasy with no operational content [^b01-1]. The gate is applied with the prologue tool kit: the M1 ban on exogenous parameters (DEF-0.2.2 forcing-by-contradiction) and the ⊥-reduction proof protocol. Σ is where M1 is first turned on every component.

**Object-type → C\* code table (what breaks under M1).** Before Σ is even stated formally, M1 already forces every theory to not merely *exist* but to register and type its own assertions. Each object type must be fixed as a code in `C*`, or the theory collapses:

| object type | status | fixed as code in `C*` | what breaks if unfixed (⊥M1) |
|---|---|---|---|
| inference rule | DEF/AX | code of the derivation template | proof not reproducible; "why does this follow?" needs an external oracle |
| axiom | AX | axiom code `c_AX` | axiom and consequence indistinguishable; everything is "true by fiat" |
| theorem | THE | theorem code `c_THE` + derivation ref | provability lost; "true as consequence" vs "written arbitrarily" indistinguishable |
| experiment | OBS | result code `c_OBS` in frame `L_n` | not reproducible; "repeated" ≡ "learned nothing", no record to compare |
| whole theory | SYS | code of the assertion set | two theories differing only in what is accepted cannot be told apart |

Each "breaks" entry is an exogenous-catalog demand, hence ⊥M1; fixing the code is forced. Status: CORE-FORCING [^b01-2]. The canonization rule `Can(s) := min_⪯ [s]_≡` is forced by the same fork: without it, equivalent records `R(n)=s`, `R(m)=t` (`s ≡ t`) read as distinct events with no "same object" criterion, so identity would need an exogenous synonym catalog — ⊥M1 [^b01-3].

### 01.1.1 Σ is not a tautology (per-component bottom-reduction)

Σ is not a redefinition of the word "distinguishability." It is the set of conditions without which the act of distinguishing is technically impossible. The proof is a component-wise ⊥-reduction: assume a working theory `T` that denies a component of Σ.

- **Drop History (¬R):** no event fixation, life "in the moment." Then "event A happened" cannot be told from "event A was dreamt"; there is no before/after base for comparison. Crash: reproducibility violated (DEF 0.3.3).
- **Drop Code (¬C\*):** no single record format. Two observers' results land in incompatible formats; comparing them needs a translation dictionary which, if not part of the theory, is an exogenous parameter. Crash: ⊥M1.
- **Drop Test (¬Δ):** no comparison procedure. "Prediction matched fact" is unsayable. Crash: theory not falsifiable.

Each dropped component independently collapses reproducibility, code-consistency, or falsifiability. Therefore Σ is the unavoidable skeleton of any operational system — load-bearing, not decorative. Status: CORE-FORCING [^b01-4].

### 01.1.2 The distinguishability tuple Σ (DEF 1.1.1)

The distinguishability structure is the tuple

```math
\Sigma = (C,\; C^*,\; D_{\min},\; \Delta,\; R,\; O),
```

with each slot a forced component, not a modeling choice [^b01-5]:

1. `C` — fixed **finite** alphabet of elementary symbols.
2. `C*` — space of all finite strings over `C` (the code universe).
3. `D_min(X) := Can(Enc(X))` — minimal-description map; the unique way to refer to an object, sending `X` to its canonical code.
4. `Δ : C* × C* → {0,1}` — binary distinguishability predicate, `Δ(s,t)=0` indistinguishable, `=1` distinguishable, with reflexivity `Δ(s,s)=0`.
5. `R : ℕ → 𝒫(C*)` — history (order memory); maps time step `n` to a frame `L_n`, the set of codes of objects fixed so far.
6. `O := (Gr(R), Query_O)` — observer (access interface); extracts data from `R` and applies `Δ`. `Query_O` is a computable realization of the projection `π_O`: it fixes which predicates are admissible, hence which distinctions an observer can reach. `Query_O` is **not** an external catalog — it adds no data, it only reads `R` [^b01-6].

This tuple is the architectural spine of the foundation. The condensed/profinite support `S_{D0}` and the `A,B,C,D` / `Ω8` instrument names at the top of this section are the downstream reading of `(C, C*, D_min, Δ, R, O)` once the finite stages `S_N` are assembled. The five functional maturity levels are `L1` Code (`C`), `L2` Canon (`D_min`), `L3` Test (`Δ`), `L4` History (`R`), `L5` Access (`O`) — organization levels, not space dimensions.

### 01.1.3 The binary-fork proof method (the reusable forcing template)

Necessity of every Σ component is proved by one schema, the **binary fork** — the standard three-branch M1 contradiction template that generates the individual results below [^b01-7]:

- **Branch A — component absent:** show the set of distinguishable objects cannot be specified or fixed (realizability violated).
- **Branch B — component present:** show it suffices to build the model.
- **Branch C — component replaced by an alternative:** show the alternative demands an external catalog (⊥M1).

Branch A kills "do without it," branch C kills "swap it for something exogenous," branch B confirms sufficiency. The sections that follow are instances of this one template; this is the meta-method, kept here so the individual necessity proofs are not isolated facts.

### 01.1.4 Single code space `C*` is forced (LEM 1.1.5.2)

A realizable universe must have a single code ontology. ⊥-fork: suppose there is no single space — two irreducible formats `C₁*`, `C₂*`. To compare `A ∈ C₁*` with `B ∈ C₂*`, `Δ(A,B)` is undefined (different types), so a translation mechanism `T : C₁* ↔ C₂*` is required.

- If `T` is an algorithm inside the theory, then `C_total = C₁ ∪ C₂ ∪ T` *is* the sought single space — back to the thesis.
- If `T` is not an algorithm, it is an exogenous parameter set of correspondence rules — a manual gluing of worlds — ⊥M1.

Either way `C*` is single. Status: CORE-FORCING [^b01-8]. Existence of `Can` is not observer arbitrariness: in a finite alphabet under a fixed order ⪯ (length + lexicographic) the minimum of any non-empty equivalence class exists as a mathematical fact [^b01-9].

### 01.1.5 CORE Δ is a bit, not a probability (LEM 1.1.7.2)

Fundamental distinguishability is a bit (0/1), not a probability. ⊥-proof: suppose in CORE, `Δ` returns a probability `p ∈ [0,1]`. The system must still decide — write the event into `R` or not, did the detector fire? Given `Δ(s,t)=0.7`, is that yes or no? A decision needs a threshold `T_thresh` (`p > T_thresh ⇒ 1`); the value of `T_thresh` (0.5? 0.95?) is a free parameter with no internal source — an exogenous threshold catalog, ⊥M1. Hence in the minimal model only absolute (binary) distinguishability is admissible; probabilities are statistics layered over History (BRIDGE), not foundation. Status: CORE-FORCING [^b01-10].

**CORE vs FORMALISM scoping (do not over-read binarity).** Binarity of *verification* does not force all mathematics to be 2-valued. Multi-valued and continuous FORMALISM layers — probabilities, amplitudes, measures, geometries, categories — stay admissible. The corpus requirement is the projection condition: any admissible non-binary mathematics must (1) carry an explicit projection onto the PASS/FAIL distinguishability criterion, (2) hide no knobs in encoding / precision / stopping rule / calibration, and (3) supply these as internal corpus elements (CORE/FORMALISM/BRIDGE), not exogenous parameters. So a D0 dispute is never about "is the world binary" but about correctness of the stated projection and absence of hidden parameters [^b01-11]. An **event** is an element of `{0,1}` in CORE (a finite distinguishability test outcome); a **state** is a FORMALISM object (distribution, amplitudes) parameterizing event statistics — INV_3 binds events, not state representations. History is itself forced (no `R` ⇒ no time index `n` ⇒ no algorithm, no before/after, no causality — forcing: GOLDEN LEM 1.1.8.3), and the observer is forced (History with no access leaves past measurements unusable; distinguishability loses connectivity — forcing: GOLDEN LEM 1.1.9.2/1.1.9.3, BOOK-I-ARCHITECTURE).

### 01.1.6 No hidden parameters (THE 1.1.11.B)

A new parameter `Y` ("hidden variable") that does not change `Δ` but "enriches the essence" cannot be added. ⊥-proof on the extension `Σ' = (Σ, Y)`, by dichotomy:

1. **`Y` does not change `Δ`-outcomes.** Then `(s, Y₁)` and `(s, Y₂)` are indistinguishable for the Σ protocol, so `D_min` (canonization) is obliged to discard `Y` as description noise (synonyms). `Y` is eliminated automatically.
2. **`Y` changes `Δ`-outcomes.** Then a change of `Y` is itself a distinguishability event, so it must be written into History `R`, so `Y` has a code in `C*`.

Either the parameter does not exist (canonized away by `D_min`) or it is part of the code (written into History `R`). There are no invisible parameters steering the world past History. Status: CORE-FORCING [^b01-12]. This is the general foundational no-hidden-variable theorem; the narrow "no hidden mass scale / no post-hoc permutation" CKM guardrail owned by BOOK_02 is one downstream instance of it, not the source. Worked instance: introducing "data types" (int vs real) either changes `Δ` (`1` vs `1.0` not comparable) — then the type is written into the code — or it does not — then types are fictitious and erased by canonization [^b01-13].

### 01.1.7 Summary of the forced foundation

For any operational theory to exist, M1 forces, via the binary fork:

1. **Single code** (`C*`) — else a translator catalog.
2. **Binarity** (`Δ ∈ {0,1}` in CORE) — else a threshold catalog.
3. **History** (`R`) — else no causality.
4. **Observer** (`O`) — else no access to experience.

The condensed/profinite support and the `A,B,C,D` / `Ω8` finite-instrument language of this book are the standard-language reading of exactly this forced skeleton; the dynamics of transitions and the derivation of `φ` are built on it downstream.
## 01.2 Role of this book

Book 01 is the first construction book. Book 00 states the entry contract; Book 01 constructs the first mathematical object to which that contract applies. The construction is deliberately before particle ontology, smooth geometry, continuum fields and SI calibration.

Definition. The primitive object is a finite-verifiable registration system. In mathematical language, D0 starts from a profinite/condensed support equipped with a restricted class of admissible morphisms and finite detector operators. In physical language, this is the minimal structure required for a completed measurement record.

The proof path of the book is:

\[
\text{no-monopoly verification}\Rightarrow
S_{D0}^{\varphi}\Rightarrow
\mathcal M^{D0}\subset\mathcal M\Rightarrow
\mathcal H_N,\mathcal D_N,R_N\Rightarrow
x^2=x+1\Rightarrow
\delta_0\Rightarrow
four terminal roles A,B,C,D\times\{\pm\}\Rightarrow
\Omega_8\Rightarrow
V_9\Rightarrow
K(9,11,13).
\]

The feedback-return object is derived, not primitive, and it is kept distinct
from the positive response operator `R_N = D_N^dagger D_N`:

```text
F_N = P_N U_N^dagger Q_N U_N P_N
```

ABCD determines what can be terminally registered; `F_N` determines what returns from the non-registered complement, with the internal feedback resolvent forced by the retained/traced split. Book 01 only hands this retained/traced split to downstream operator books; it does not import matter masses, electroweak constants, baryon data, cosmological surveys or neutrino passports.

### What "mass/energy" is allowed to mean before calibration

The construction must say what an objective magnitude IS in a world that is nothing but completed records — before any SI unit, any continuum, any field. There is exactly one answer that imports no external catalog: the magnitude of a state is its information complexity, i.e. the length of its minimal admissible code.

Definition (F_0, owned here). For a state X with minimal code `D_min(X)`,

\[
F_0(X) := |D_{\min}(X)|.
\]

This is the only objective measure of "mass" or "energy" available in a code world [^b01-14]. Any other proposed magnitude either coincides with a length-of-code up to format conventions, or it ranks states by a yardstick that is not derivable from the records themselves — which is an external catalog and is M1-forbidden (DEF-0.2.2). Status: FORCED (it is the unique catalog-free magnitude).

`F_0` is sub-additive, not additive, and the gap is exactly the binding-energy reading. Composition `X ⊕ Y` glues the two minimal codes via the canonical self-delimiting pairing `Pair`, so

\[
F_0(X\oplus Y)\le F_0(X)+F_0(Y)+|\mathrm{EncLen}(F_0(X))|,
\]

where `EncLen` is the prefix-free length code already fixed by the record format [^b01-15]. The extra term `|EncLen(F_0(X))|` — the self-delimiting prefix that lets the glued code be reparsed unambiguously — is the pre-image of physical binding energy (the mass defect of the join). Because `|EncLen(n)| = O(log n)`, this binding term is strictly logarithmic and vanishes under BRIDGE scale-calibration [^b01-16]. That is the honest origin of why a macroscopic `F` may be treated as additive: the defect is real but log-suppressed, not zero. Status: FORCED.

This is the conceptual ground floor for every later energy/mass reading in the corpus; it must live here and is not cited away.

### Why the construction is linear: superposition is forced, not assumed

Interaction in D0 is not a term you add to an equation. It is forced to be absent at the level of the connection law, and to re-appear only as a topological/structural effect downstream (the graph, ABCD, the K-scene). The argument is a contradiction proof against any catalog-dependent coupling [^b01-17].

A connection law is realized by a mediator `P(S,T)`: the minimal state describing the link between two given states `S` and `T` (DEF 2.2.1, owned here).

Arity is forced to 2 [^b01-18]. Three cases exhaust the alternatives, and two of them are eliminated by contradiction:

1. If `P` does not depend on its input, it cannot distinguish the pair `(S,T)` and so is not a connection law at all.
2. If `P` depends on only one argument, it describes internal evolution, not a binary "between" relation.
3. If `P` demands a third argument `U`, then at fixed `S,T` the value of `U` must be supplied separately; if `U` is not derivable from the task data and prior definitions it is an exogenous parameter, which M1 forbids (DEF-0.2.2).

Hence the minimal arity of a connection law is exactly 2. Status: FORCED.

Linearity then follows from the same no-catalog pressure [^b01-19]. Suppose one tries to introduce an interaction term `G(S,T)`:

\[
P(S,T)=S\oplus T\oplus G(S,T).
\]

To specify `G` the theory must answer: which functional form (product, power, log?) and which coupling constant `γ`? A coupling `γ` that is not derived from the properties of `S` and `T` is a fundamental constant and must be written into the exogenous-constants catalog — forbidden. Worse, once one term `γ_1(S·T)` is admitted there is no catalog-free reason to forbid `γ_2(S^2·T)`, `γ_3(S·T^2)`, …; any rule for truncating the Taylor series ("the first term dominates") presupposes a priori knowledge of scales, i.e. a catalog again (EX-0.4.3 infinite regress). The series is therefore infinite and arbitrary unless every interaction term is dropped:

\[
P(S,T)=aS\oplus bT.
\]

Linear superposition is not a simplification — it is the unique mediator form with no hidden parameters. Status: FORCED. Symmetry of the link (`S→T` and `T→S` are one process) forces `a=b`, and M1 normalization removes the residual scale constant `a` by choice of units, giving the CORE form `P(S,T)=S⊕T` [^b01-20]. Nonlinearity, equivalently any genuine coupling constant at the connection law, is an M1 violation; real interaction is forced to enter as a topological effect, which is precisely what the incidence graph and the ABCD roles below deliver.

Downstream of this, the quadratic two-branch relation `p + p^2 = 1` (giving `φ` and `δ_0`) is read off the BRIDGE iteration of this same linear mediator (kept in §01.6); it is the scale-self-similarity of `P`, not a re-introduced nonlinear term.

### Construction proper

The book therefore proves construction of the finite incidence graph from finite registration, not by choosing a convenient graph, but by imposing the obligations of address, comparison, halt, response and invariant readout — over a mediator that is forced to be linear, with magnitudes forced to be code-lengths.
## 01.3 No-monopoly verification and the measurement dyad

A physical record cannot be a monopoly assertion. A single unopposed line of information has no internal way to distinguish state from registration, source from detector, or signal from unchecked naming. The first admissible object is therefore a dyad: two independently addressable sides plus a comparison.

D0 writes this as a detector/object exchange:

\[
D\otimes O\longrightarrow O\oplus\mathfrak q.
\]

Here `D` is not a laboratory instrument in the late sense; it is the minimal detector role. `O` is not a particle at this layer; it is the object role presented to comparison. The symbol `\mathfrak q` is the irreducible addressable record quantum. The dyad closes only when the comparison produces a finite registration.

This gives the no-monopoly theorem:

\[
\text{interaction}\Rightarrow\text{information},\qquad
\text{information}\Rightarrow\text{detector/register}.
\]

The converse guardrail is equally important. D0 does not allow a bare information line to count as physics:

\[
\text{information line}\not\Rightarrow\text{physics}.
\]

Physics begins only when the information line enters a finite detector/register relation and admits a positive response functional.

## 01.4 Condensed/profinite support

The support of the first detector is an inverse system of finite address words. Let

\[
S_n=\{A,B\}^n,
\]

with projection maps

\[
\pi_{n+1,n}:S_{n+1}\to S_n.
\]

The profinite support is

\[
S_{D0}=\varprojlim_n S_n=\{A,B\}^{\mathbb N}.
\]

D0 does not use the ambient condensed mapping space without restriction. The physical subfunctor is the D0-admissible one:

\[
\mathcal M^{D0}(S_{D0}^{\varphi})\subset \mathcal M(S_{D0}).
\]

A morphism is D0-admissible only if it is visible through finite stages, has a halt quotient, produces a positive quadratic response, respects direct/return asymmetry, and does not introduce a second hidden calibration section.

The weighted detector path object is

\[
\boxed{ S_{D0}^{\varphi}=(S_{D0},\mu_{\varphi}) }
\]

where cylinder weights are

\[
\mu_{\varphi}([w])=\prod_{i=1}^{|w|}\mu(w_i),\qquad
\mu(A)=p,
\qquad
\mu(B)=p^2,
\qquad
p+p^2=1.
\]

Thus the continuum is not rejected. It is demoted from ontology to test object: a continuum statement is physical only after it factors through finite D0-admissible registration.

### 01.4.0 No hidden points: the inverse limit *is* the support (forced)

The demotion above is not a stylistic choice — it is forced. The owner statement is the no-hidden-points theorem on the profinite support `S_{D0}=\varprojlim_n S_n`: the inverse limit carries *all* operational reality, and there are no "hidden points between the nodes" that the tower fails to register.

**[THE 01.4.0] No hidden points / consistency of the support.** Let `x,y\in S_{D0}` and write `\pi_k(x)` for the image of `x` under the canonical projection `S_{D0}\to S_k`. If `\pi_k(x)=\pi_k(y)` for every finite stage `k`, then `x=y`. Equivalently: two states equal under every `\pi_k` are the same state, and the support is exactly `\varprojlim_n S_n` with no residual fibre of "true continuum points" sitting underneath it.

*Status: CORE-FORCING [^b01-22].*

*Forcing (M1, by contradiction).* Suppose toward contradiction that `x\neq y` yet `\pi_k(x)=\pi_k(y)` for all `k` — i.e. the two are counted as *different points of the "true continuum"* while remaining indistinguishable at every finite stage. To register that difference at all, some test must separate them. But every admissible test factors through a finite stage `S_k` (descent obligation 1 of §01.4.1), and there all results coincide by hypothesis. So no D0-admissible procedure outputs the distinction. To keep `x\neq y` one must therefore *adjoin an external label* — an index `\ell(x)\neq\ell(y)` not produced by any finite-stage readout. That label is an **External Catalog of differences**: a distinction the theory must carry but no internal test can generate. This is exactly the object M1 forbids (physics = what survives the requirement to distinguish itself *without an external catalog*). Contradiction. Hence `x=y`. ∎

Two consequences, both load-bearing downstream:

1. **The continuum is a tower of refinements, not a bag of points.** `S_{D0}` is the limit of distinguishing stages, and its points *are* the coherent threads through `\{\pi_{n+1,n}\}` — nothing finer is real. Actual infinity never enters as a completed set; it enters only as the inverse system `\{S_n,\pi_{n+1,n}\}` itself. This is the support-level statement of which the §01.4 "test object, not ontology" reading, and the later no-hidden-response Born form (§01.17.1), are downstream specializations.
2. **κ-equivalence replaces `\mathbb R`.** Because separation is finite-stage, numerical equality is read at finite resolution: sequences over `\mathbb Q(\varphi)` that agree to `\varphi^{-k}` at every depth define the same κ-number. A residual gap below every `\varphi^{-k}` is, by THE 01.4.0, not a real distinction — it would be an external catalog of differences. The role of `\mathbb R` is thus taken by κ-classes of pro-observables, not by a postulated point-set.

*Status note: THE 01.4.0 is a continuum-level structural forcing with no finite numerical witness of its own (it asserts the* absence *of a separating test). It is carried as [^b01-21] — the existing fractal-tick continuum certificates test the refinement dynamics, not the no-hidden-points identification, and are NOT cited as a witness here.*

### 01.4.1 The D0 condensed site and admissible subfunctor

The previous paragraph gives the support.  The present paragraph fixes the category-level meaning.  Let `\mathsf{ProfFin}` denote the test category of finite sets and profinite limits with continuous maps, equipped with the usual finite-cover topology.  D0 uses the condensed representative

\[
\underline S_{D0}:\mathsf{ProfFin}^{op}\to\mathsf{Set},
\qquad
T\mapsto\operatorname{Hom}_{\mathrm{cont}}(T,S_{D0}).
\]

At finite stage `N`, every admissible section must factor through a clopen quotient:

\[
T\times S_{D0}\longrightarrow T\times S_N\longrightarrow V_N,
\]

where `V_N` is a finite readout object or a finite-dimensional vector space assigned to the detector stage.  The full ambient condensed mapping object is too large because it contains maps with no finite halt, no positive response, and no stable terminal quotient.

D0 therefore uses the subfunctor

\[
\underline{\mathrm{Obs}}^{D0}(S_{D0}^{\varphi})(T)
\subset
\underline{\mathrm{Obs}}(S_{D0})(T)
\]

whose sections are exactly those satisfying the following descent obligations:

1. **finite quotient:** locally on `T`, the section factors through some `S_N`;
2. **operator lift:** the finite factor carries a channel `\mathcal D_N` on `\mathcal H_N=\mathbb C^{S_N}`;
3. **positive response:** `R_N=\mathcal D_N^\dagger\mathcal D_N`;
4. **projection compatibility:** refinement from `N+1` to `N` preserves the readout after applying the projection `S_{N+1}\to S_N`;
5. **halt quotient:** the comparison has a terminal finite quotient, rather than an infinite request for metadata;
6. **single section:** dimensionful external representatives factor through the declared D0 section, not through a hidden second scale.

This is the point at which condensed mathematics enters the physical theory.  A continuum expression is allowed as a test object or an external representative only after it descends to a D0-admissible finite-stage section.  Conversely, a finite numerical expression that does not define such a section is not a physical D0 theorem.

## 01.4a Condensed φ-quasicrystalline support

The D0 condensed/profinite support is a finite information quasicrystal. It is not a smooth primitive continuum and it is not a periodic lattice.

The primitive return phase is φ-rigid:

```math
\alpha_{D0}=\varphi^{-2},
\qquad
\Delta\theta=\frac{2\pi}{\varphi^2}.
```

Because this phase is irrational and has the golden continued-fraction class, it suppresses low-denominator rational locking. The unresolved archive geometry therefore does not collapse into uncontrolled periodic arms.

Visible spatial branches appear only when a finite readout quotient chooses a return modulus `q`. The residue classes modulo `q` become detector-visible geometry:

```text
ordered tick chain
-> irrational φ phase
-> finite return modulus
-> residue branches
-> visible spatial arms
-> tiling-hull patches
```

Thus D0 geometry is finite, ordered, aperiodic and readout-generated. Smooth macro-geometry is the coarse-grained shadow of this non-resonant finite branch order.
### 01.4.2 four terminal roles A,B,C,D as a natural operator cycle over the condensed support

The four terminal roles A,B,C,D roles live inside this admissible subfunctor.  Let `T_\varphi` and `T_\psi` be the two branch endomorphisms of the finite comparison module.  Their finite-stage representatives must form a compatible family

\[
P_{N+1,N}T_{\bullet,N+1}=T_{\bullet,N}P_{N+1,N},
\]

where `P_{N+1,N}:\mathcal H_{N+1}\to\mathcal H_N` is induced by the projection of address words.  Thus the four operators

\[
A_\Sigma=T_\varphi+T_\psi,
\quad
B_N=T_\varphi T_\psi,
\quad
C_+=T_\varphi^2-T_\varphi,
\quad
D_-=T_\psi^2-T_\psi
\]

are not merely scalar equations.  They are natural finite-stage obligations of the condensed detector object.  Removing one of them breaks a different descent condition: `A_\Sigma` breaks the unit section, `B_N` breaks conjugate coupling, `C_+` breaks forward refinement, and `D_-` breaks return/halt descent.

## 01.5 Finite Hilbert stage, response and halt

At finite stage `N` the detector has the finite support

\[
S_N=\{A,B\}^N
\]

and finite state space

\[
\mathcal H_N=\mathbb C^{S_N}.
\]

A detector channel is a finite operator

\[
\mathcal D_N:\mathcal H_N\to \mathcal H_N,
\]

with positive response

\[
R_N=\mathcal D_N^\dagger\mathcal D_N.
\]

For an event projector `\Pi_a`, the finite readout law is

\[
P_N(a)=\frac{\operatorname{Tr}(\Pi_aR_N)}{\operatorname{Tr}(R_N)}.
\]

The amplitude layer, archive layer and probability layer are separated:

\[
\rho_N=|\psi_N\rangle\langle\psi_N|,
\]

\[
\Delta(\rho_N)=\operatorname{diag}(\mu_\varphi([w])),
\]

\[
P_N(a)=\operatorname{Tr}(\Pi_aR_N)/\operatorname{Tr}(R_N).
\]

The archive map `\Delta` is not a loss of rigor. It is the finite operation by which non-terminal continuum metadata is removed from active readout and stored as forgotten/addressed structure. The halt quotient is the statement that a registration is completed when further refinement cannot change the finite event class without violating the D0 admissibility constraints.

## 01.6 Minimal positive-response closure and the equation `p+p^2=1`

The quadratic branch equation is a theorem of the D0 primitive detector skeleton, not an isolated numerical choice. The primitive skeleton consists of the following finite obligations.

The same quadratic response equation `x^2+x-1=0` that defines the finite response split also gives the time automorphism spectrum of `T = [[0,1],[1,-1]]`; the time layer uses the conjugate pair only through finite integer traces.

**Finite stage.** A registration must factor through some finite quotient `S_N` of the profinite support.

**Non-monopoly dyad.** A record cannot be only a direct assertion. It must contain a direct branch and a return branch which checks the direct branch.

**Constructive composition.** Primitive branch weights are produced by finite composition of registered channels. Non-integer powers are not primitive finite-stage morphisms.

**Positive response.** A completed readout is a positive response

```math
R_N=\mathcal D_N^\dagger\mathcal D_N.
```

Thus the first primitive self-return of one registered channel is quadratic. If the direct branch has weight `p`, the first admissible return branch has weight

```math
p\cdot p=p^2.
```

**Single halt.** The primitive audit has one direct exposure and one positive self-return. Additional powers such as `p^3` or `p^4` describe further unresolved iterations before halt; they are runtime descendants, not the primitive return.

**Normalization.** The primitive two-branch audit has one unit section, hence

```math
p+p^2=1.
```

The solution in the physical interval is unique. Since

```math
f(p)=p^2+p-1,
\qquad
f'(p)=2p+1>0\quad (0<p<1),
```

there is exactly one root in `(0,1)`:

```math
p=\frac{\sqrt5-1}{2}=\varphi^{-1}.
```

The conjugate scalar representative is

```math
\psi=1-\varphi=\frac{1-\sqrt5}{2}.
```

The direct and return branch weights are therefore

```math
p_+=\varphi^{-1},
\qquad
p_-=\varphi^{-2},
\qquad
p_++p_-=1.
```

The detector asymmetry quantum is the centered half-gap

```math
\delta_0=\frac{p_+-p_-}{2}=\frac{\sqrt5-2}{2}=\frac1{2\varphi^3}.
```

This is the active convention. The formula `\delta_0=\varphi^{-3}` is not the active D0 convention and is not admissible. The closure `p+p^2=1` together with `\delta_0=1/(2\varphi^3)` is verified by the finite certificate, which asserts `abs(p+p^2-1)<1e-12` and `abs(\delta_0-1/(2\varphi^3))<1e-12`.

### 01.6.0 The mediator forces linear superposition before any branch weight exists [^b01-23]

Before the branch equation can even be posed one must fix the *form* of the law that connects two registered states. M1 forces that form, and it forces it to be **linear**.

**Arity is exactly 2** [^b01-24]. A connection law `P` between given states `S,T` cannot ignore its input (then it does not distinguish the pair, so it is not a connection law), cannot depend on one argument only (that is internal evolution, not a binary "between" relation), and cannot demand a third argument `U`: with `S,T` fixed, a `U` not derived from the data is an exogenous parameter, which is forbidden by M1. Hence the primitive mediator is binary, `P(S,T)`.

**No interaction term — linear superposition is forced** [^b01-25]. Suppose one tries to introduce interaction by adding a coupling term,

```math
P(S,T)=S\oplus T\oplus G(S,T).
```

To pin down `G` the theory must answer: which functional form (product? power? log?), and with which coupling constant `\gamma`? A `\gamma` not derived from `S,T` is a fundamental constant and must be written into an external Catalog of constants — `\bot M1`. Worse, the choice does not terminate: if `\gamma_1(S\cdot T)` is admitted, nothing forbids `\gamma_2(S^2\cdot T)` or `\gamma_3(S\cdot T^2)`; any argument that truncates the Taylor series at the first term ("it is the largest") presupposes a priori knowledge of scales, i.e. a Catalog again. Without a catalog one is left with `P=S\oplus T+\sum_i c_i G_i`, an infinite arbitrary series. The unique form that requires no choice of function and no coupling parameter is the one with **no interaction term**:

```math
P(S,T)=aS\oplus bT.
```

Linear superposition is therefore not a simplification but the only construction free of hidden parameters. Interaction must re-enter not as a term in the equation but as a **topological effect** (see CHAPTER I.4 / the defect and holonomy layers), never as an algebraic coupling.

**Coefficients `a=b=1`** [^b01-26]. Symmetry `S\leftrightarrow T` of the connection (no external field) gives `(a-b)(F(S)-F(T))=0`; since `S\ne T`, `a=b`. A common scale `a\ne1` is a free scale constant requiring a catalog, removed by the `F`-calibration of units, so `a=1`. Hence `P(S,T)=S\oplus T`.

This is the precondition for everything below: only because the mediator is linear is a *branch weight* `p` a well-defined scalar at all. The quadratic `p+p^2=1` is the self-return audit of this linear mediator, not of some unspecified nonlinear coupling.

### 01.6.1 Why alternative branch equations are not primitive D0 equations

The equation is not selected because it is pretty. It is selected because all competing primitive equations violate one of the finite-detector obligations.

| candidate | failure |
|---|---|
| `p+p=1` | no positive self-return; symmetric naming rather than verification |
| `p+p^k=1`, `k>2` | hidden intermediate memory before halt; an iterated runtime, not the first return |
| `p+p^\alpha=1`, non-integer `\alpha` | not a finite constructive channel composition on the profinite stages |
| `p+q=1`, free `q` | second hidden branch scale; violates single-section closure |

Thus the primitive assumptions of D0 are the finite detector obligations. The scalar branch equation is the first theorem of those obligations.

### 01.6.1a Two independent forcings of `\varphi` [^b01-27]

The golden ratio is forced from M1 by **two independent routes**, and they agree. Either alone fixes `\varphi`; the agreement is what removes the last suspicion of numerology.

**Route A — channel balance (the route above).** Memory of depth 1 admits exactly two channels: direct registration of weight `p`, and the first self-return of weight `p^2`. Exhausting the unit section, `p+p^2=1`, gives `p=\varphi^{-1}`. This is the detector-skeleton derivation of §01.6.

**Route B — continued-fraction MDL-optimum.** A constant carried by the support must itself be catalog-free. The continued fraction `\varphi=[1;1,1,1,\dots]` is the **unique** irrational whose list of partial quotients is empty of content (all `1`s): it is the MDL-optimum, the irrational that stores no extra digits. By Hurwitz's theorem it is simultaneously the irrational maximally resistant to rational capture,

```math
\liminf_{q\to\infty} q^2\,\bigl|\varphi-\tfrac pq\bigr|=\frac1{\sqrt5},
```

the largest such constant — and this resistance holds at *every* finite truncation depth, so `\varphi` is compatible with the inverse limit of the carrier. A support whose scale ratio were captured by any rational `p/q` would, at some finite stage, be indistinguishable from a periodic catalog entry; only `\varphi` evades capture at all depths.

The two THE derivations meet: the MDL-optimal irrational (Route B) is exactly the fixed point of the depth-1 self-return audit (Route A). The same `\varphi` underwrites the phase generator used later (Hurwitz extremality reappears in §01.21), but here it is forced *from M1 directly*, not assumed for the phase.

### 01.6.1b Gleason-2D loophole and the Fibonacci fusion route [^b01-28]

There is a third, categorical, forcing of the same equation, and it closes a known loophole.

**Phase-blindness forces the quadratic.** By the finite holographic self-reading principle a primitive amplitude needs a minimal 2D phase space `z=(x,y)`. Gleason's theorem derives the quadratic Born response only for `D\ge3` and **fails in 2D** — the standard loophole. D0 closes it: a phase-blind self-reading response in 2D must preserve symplectic area, which uniquely forces the quadratic form

```math
Q(z)=x^2+y^2.
```

Phase-blindness `\Rightarrow` quadratic response is the same conclusion reached structurally in §01.17.1a; here it is reached by closing Gleason's dimensional gap. The *uniqueness* leg is now machine-checked: the quarter-turn `J(x,y)=(-y,x)` is the area-preserving `SL(2,ℤ)` generator, and any quadratic `a x^2 + b xy + c y^2` invariant under `J` is forced to `a=c`, `b=0` — so `x^2+y^2` is the *unique* `J`-invariant form up to scale (existence of the phase-blind response is owned upstream). What remains a theorem-target is the *categorical* uniqueness below (Ostrik/Ising), whose fusion-category machinery is not yet in the formal kernel.

**Fibonacci fusion forces `d=\varphi`.** Because the automaton is strictly self-reading, registration acts on itself. To forbid hidden external memory the readout channel must satisfy the minimal algebraic closure known in TQFT as the Fibonacci fusion rule,

```math
\tau\otimes\tau=1\oplus\tau.
```

Taking quantum dimensions gives `d^2=1+d`, hence `d=\varphi`; normalized to unit probability capacity this is again `p+p^2=1`.

**Uniqueness (Ostrik 2003) and Ising-exclusion.** The minimal non-trivial fusion rule with exactly two simple objects and non-trivial self-fusion is uniquely the Fibonacci category (Ostrik 2003, classification of small fusion categories). The Ising category (three simple objects) is excluded: it admits an additional non-trivial fermion `\psi`, which is an extra hidden state, violating the no-bare-information-line axiom. Thus Fibonacci is the unique solution, and `\varphi` is forced a third time.

**External anchor (corroboration, not derivation).** The one laboratory system where `E8` and `φ` appear together corroborates this structure: the transverse-field Ising chain `CoNb₂O₆` at quantum criticality realises Zamolodchikov's emergent `E8` mass spectrum, whose leading ratio is `m₂/m₁ = 2cos(π/5) = φ` (Coldea et al., Science **327** (2010) 177). The same golden ratio D0 forces by `p + p² = 1` governs an experimentally observed `E8` critical spectrum. This is an empirical passport, not a derivation — the D0 icosian→`E8` step itself remains an external-gap bridge (the relevant genus-uniqueness is not yet in the formal kernel).

### 01.6.1c The cascade: each floor forced by the insufficiency of the previous [^b01-29]

The branch equation is not a detail of one layer; it is the seed of the whole spine. The architecture is not *assembled* from parts — it is the *unfolding* of a single requirement, each floor born from the insufficiency of the one below. In one line:

> distinguish `\Rightarrow` leave a trace `\Rightarrow` a trace without comparison is not a trace `\Rightarrow` comparison needs memory `\Rightarrow` memory needs a return with a distinguishable outcome (a holonomy bit) `\Rightarrow` return without an external clock `\Rightarrow` the scale ratio is the fixed point of refinement (`\varphi`) `\Rightarrow` memory of two independent loops `\Rightarrow` torus `\Rightarrow` the torus is abelian, so order is not encoded `\Rightarrow` defect `\Rightarrow` circulation needs closure `\Rightarrow` shell `\Rightarrow` three insufficiencies = three zones `\Rightarrow` carrier `K(9,11,13)` `\Rightarrow` spectrum (rank 3 = space, kernel 30 = dark archive) `\Rightarrow` every observable = an invariant of this single construction.

At the seed of this chain, `p^2+p=1` is to be read at its deepest: **not** a balance of two branches but a **self-description** — the definition of an object through its own dynamics. The whole equals one act plus the act applied to itself. Not "an object that *has* a dynamics" but "an object that *is* its own recursion": existence as self-consistent repetition. From this single quadratic everything downstream follows as its representation theory:

- **time** = depth of recursion (the `T^2` time layer, §VI/§01.14);
- **mass** = number of turns;
- **generations** = defect classes;
- **orientation** = sign of the discriminant;
- **`\delta_0`** = displacement of the cut;
- **symmetry** = the Galois group of the equation.

Status: PROOF-TARGET for the full cascade as a single theorem (the individual links — dyad, `\varphi` closure, torus, `K(9,11,13)` rank 3 / nullity 30 — are each established and cert-backed elsewhere in this book; the unifying "each floor forced by the previous" statement is the open obligation). Engine: `\varphi`-recursion. Transmission: `Q_8`. Body: the 9-11-13 shell tower. Dark memory: the kernel of the adjacency operator.

### 01.6.2 Recursive distinguishability and the detector ladder

Define

```math
\delta^{(0)}=\delta_0,
\qquad
\delta^{(n+1)}=\delta_0\delta^{(n)}.
```

Then

```math
\delta^{(n)}=\delta_0^{n+1},
\qquad
\frac{\delta^{(n+1)}}{\delta^{(n)}}=\delta_0.
```

The dimension-graded detector quantum is therefore

```math
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
```

It gives

```math
Q(1)=2\delta_0,
\quad
Q(2)=\varphi^{-2},
\quad
Q(3)=\varphi^{-1},
\quad
Q(4)=1,
\quad
Q(5)=\varphi.
```

The factor `2` is structural: `\delta_0` is half of the branch asymmetry, while `2\delta_0` is the full one-dimensional branch gap.

The split is not numerology. It is the unique minimal normalized finite two-branch audit with a quadratic positive-return response — forced four ways: by the finite detector obligations (§01.6), by channel balance and the continued-fraction MDL-optimum (§01.6.1a), by the Fibonacci fusion rule closing Gleason's 2D loophole (§01.6.1b), and as the self-description seed of the full cascade (§01.6.1c).
## 01.7 The four terminal roles A,B,C,D operator roles

The pair `\varphi,\psi` gives a scalar presentation of the quadratic relation, but D0 does not use the four `A,B,C,D` entries merely as four algebraic equations.  At the scalar level some relations imply others.  At the detector level, however, the four entries are four typed operator roles in one completed readout cycle.

Let `T_\varphi` and `T_\psi` denote the two conjugate branch operators acting on the finite two-branch comparison module.  The four `A,B,C,D` roles are:

\[
A_\Sigma:\quad T_\varphi+T_\psi=I,
\]

\[
B_N:\quad T_\varphi T_\psi=-I,
\]

\[
C_+:\quad T_\varphi^2=T_\varphi+I,
\]

\[
D_-:\quad T_\psi^2=T_\psi+I.
\]

They reduce on scalar representatives to

\[
A:\ \varphi+\psi=1,
\qquad
B:\ \varphi\psi=-1,
\qquad
C:\ \varphi^2=\varphi+1,
\qquad
D:\ \psi^2=\psi+1.
\]

The point is not algebraic independence.  The point is operator completeness:

| role | operator obligation | failure if removed |
|---|---|---|
| `A_\Sigma` | additive normalization / unit section | no finite unit, no normalized halt |
| `B_N` | multiplicative conjugate coupling / norm section | branches become unrelated labels |
| `C_+` | forward branch self-return recursion | no positive branch runtime calculus |
| `D_-` | return branch self-return recursion | no conjugate return / no closed cycle |

Thus `\{A,B,C,D\}` is the minimal four-role operator cycle of the `\varphi` detector relation.  It is not a claim that four scalar equations are independent axioms.  It is a claim that a completed finite detector cycle requires four typed roles: normalization, conjugate coupling, forward recurrence and return recurrence.

The centered distinguishability quantum is then the half-gap of the two normalized branches:

\[
p_+=\varphi^{-1},
\qquad
p_-=\varphi^{-2},
\qquad
p_++p_-=1,
\]

\[
\delta_0={p_+-p_-\over2}={\sqrt5-2\over2}={1\over2\varphi^3}.
\]

Equivalently,

\[
p_+=\frac12+\delta_0,
\qquad
p_-=\frac12-\delta_0.
\]

The factor `2` is therefore not a convention: it is the passage from full branch asymmetry to centered half-gap.

The dimension-graded quantum follows from the same centered split:

\[
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
\]

This is the active `\varphi`-ladder relation used downstream.

### 01.7.1 Terminal two-port realization of `\{A,B,C,D\}`

The physical two-port detector gives a terminal representation of the same four-role cycle.  For two inputs and two outputs there are four terminal registration roles:

\[
A=(3,3),\qquad
B=(4,4),\qquad
C=(3,4),\qquad
D=(4,3).
\]

This representation is not a new axiom and not a proof by analogy.  It says that the abstract four-role operator cycle has a minimal terminal readout realization: two coalescent roles and two separated/exchange roles.  The sign/phase branch then gives

\[
\Omega_8=\{A,B,C,D\}\times\{+,-\}.
\]

The associated role representatives are recorded as

\[
U_A=Id,
\qquad
U_B=I,
\qquad
U_C=J,
\qquad
U_D=K.
\]

The detector closure is therefore not `8` as a graph vertex count.  It is a closed signed terminal role cycle.  The graph begins only after this cycle is lifted.

### 01.7.1A `\Omega_8\cong Q_8`: the role group is forced, not declared

The labels `Id,I,J,K` are not a decoration.  The signed terminal role space `\Omega_8=\{A,B,C,D\}\times\{+,-\}` is *strictly isomorphic* to the quaternion group `Q_8=\{\pm1,\pm i,\pm j,\pm k\}` under

\[
A\mapsto 1,\qquad B\mapsto i,\qquad C\mapsto j,\qquad D\mapsto k,
\]

and this isomorphism is **forced by M1**, not picked from a menu.  Status: **THEOREM** [^b01-30].

The forcing has two M1 reads and one classical theorem that globalizes them.

1. **Normality is forbiddance of a conjugate catalog.**  A non-normal subgroup carries distinct conjugate copies `gHg^{-1}`.  Telling those copies apart requires an external catalog of conjugates — exactly the catalog M1 (DEF-0.2.2) forbids.  So *every* subgroup of the role group must be normal: the group is **Hamiltonian** (Dedekind sense).

2. **Order memory forbids commutativity.**  A completed readout records the *order* of its operations (which branch resolved first); that order-memory obligation, already carried by the forward/return split `C_+/D_-`, forces the role group to be **non-abelian**.

These two constraints — Hamiltonian *and* non-abelian — leave essentially no room.  An exact finite enumeration of the non-abelian groups of order `\le 8` (explicit multiplication tables, no floats, discharged by the finite certificate) gives the count of non-normal proper subgroups:

\[
S_3:\ 3,\qquad D_4:\ 4,\qquad Q_8:\ 0.
\]

`Q_8` is the **unique** non-abelian group of order `\le8` with zero non-normal subgroups.  Dedekind (1897) then globalizes: *every* Hamiltonian group contains `Q_8` as a factor, so the minimality is not an artifact of stopping the scan at order `8` — it is absolute.  Hence `\Omega_8\cong Q_8` is a theorem, and the `+/-` orientation bit is the central `\{\pm1\}`, not an extra fitted degree of freedom.

### 01.7.1B Triple identity: order-memory, orientation and remainder are one `\mathbb Z_2`

Inside `Q_8` the three canonical structural subgroups collapse to a single copy of `\mathbb Z_2`:

\[
[Q_8,Q_8]\;=\;Z(Q_8)\;=\;\Phi(Q_8)\;=\;\{\pm1\}.
\]

Status: **THEOREM** [^b01-31].  The three objects are:

| object | what it records |
|---|---|
| `[Q_8,Q_8]` (commutator) | **order memory** — the non-commutativity remainder of read/write order |
| `Z(Q_8)` (center) | the **orientation** `+/-` bit of `\Omega_8` |
| `\Phi(Q_8)` (Frattini) | the **non-generating remainder** left after the role generators |

That three independent group-theoretic objects coincide on one `\mathbb Z_2` is the cleanest possible M1 signature: three structural objects without three separate catalogs.  The `+/-` of `\Omega_8` *is* the memory of read/write order — orientation and order memory are not two facts, they are one.

### 01.7.1C Spin-`1/2` and three transport directions from `Q_8`

The quaternion relations `i^2=j^2=k^2=-1` are not inert.  A squared half-turn lands on the central `-1`, so a single `2\pi` rotation is **not** the identity while `4\pi` is:

\[
i^2=-1\ \Rightarrow\ 2\pi\neq\mathrm{id},\quad 4\pi=\mathrm{id}.
\]

This is **fermionic statistics read straight off the orientation bit of the scene**: the `4\pi` periodicity is the central `\mathbb Z_2` of §01.7.1B, the spinor double-cover leaf index.  Status: **COROLLARY** [^b01-32].  The three pure-imaginary axes `i,j,k` are the **three transport directions** of the readout; this is the same `3` as `rank(A)=3` of the scene incidence matrix (cf. §01.8, `rank(A)=3,\ nullity(A)=30`).  Macroscopic `3`-space is the pushforward of the pure-imaginary subspace of `Q_8`.  The explicit map (`\Omega_8`-orientation groupoid `\to Z(Q_8)`) closing the spinor leaf to the holonomy parity is not yet written.  Status of that last step: **PROOF-TARGET (cert obligation open)**.

**Independent forcing-owner for the three imaginary axes (Frobenius 1877).**  That `Q_8` has *exactly* three pure-imaginary generators `i,j,k` is not only an internal count: it is also forced from outside by the **Frobenius theorem** — the only finite-dimensional *associative division algebras* over `\mathbb R` are `\mathbb R` (dim 1), `\mathbb C` (dim 2), `\mathbb H` (dim 4), and *no other*, in particular none of dimension 3.  The quaternions `\mathbb H` are therefore the **maximal** associative division algebra over `\mathbb R`, and `Q_8` is exactly their unit group; the imaginary part `\mathrm{Im}(\mathbb H)=\mathrm{span}\{i,j,k\}` is `3`-dimensional — the three reversible transport directions `=\mathrm{rank}=3=` space, the one real axis `=` time.  So the `3` of space is forced by a classical structure theorem, not chosen: claim `D0-FROBENIUS-DIVISION-3D-001` (BRIDGE owner-edge, `ASSUMP-FROBENIUS-1877`; Lean `D0.Foundation.FrobeniusDivision3D` proves the finite Hamilton relations `i^2=j^2=k^2=ijk=-1` and `\mathrm{Im}`-dim `=3`; cert `vp_frobenius_division_3d.py`).  This is a second independent channel to `\mathrm{rank}=3` beside the `Q_8`/Dedekind route here and the tripartite graph-rank, all converging on the tower stop at three zones (§01.19a "third channel"; `D0-TOWER-STOP-NOEXT-001`).  **Honest gap:** the `\mathbb H\to\mathbb O` octonion step (would it force the octet `|\Omega_8|=8`?) is **HYP, not a forcing** — `\dim\mathbb O=8` (algebra dimension) and `|\Omega_8|=|Q_8|=8` (group order) are two *different* eights, and the octet claim needs them identified first.

We do **not** import the Leech/`\Lambda_{24}`-projection or "Ramanujan-expander" framing for the `30`-nullity here: those are overshoot-adjacent and not forced.  The forced content is `\Omega_8\cong Q_8`, the triple `\mathbb Z_2` identity, the spinor/rank-`3` corollary above, and the Frobenius owner-edge for the three imaginary axes.

### 01.7.2 Proof cell: eight oriented terminal-role states Ω8 detector cycle

**Claim.**  The first closed detector cycle is the signed four-role cycle

```math
\Omega_8=\{A,B,C,D\}\times\{+,-\}\ \cong\ Q_8,
```

with `A\mapsto1,\ B\mapsto i,\ C\mapsto j,\ D\mapsto k` and the `+/-` orientation bit equal to the central `\{\pm1\}`.  The group identification is forced, not declared (see §01.7.1A; discharged by the finite certificate).

**Support.**  The support is the terminal four-role readout algebra obtained after the `\varphi` halt quotient.  Its two-port representation is

```math
A=(3,3),\qquad B=(4,4),\qquad C=(3,4),\qquad D=(4,3).
```

**Probe/gate.**  The finite probe is the two-input/two-output detector role comparison.  The sign branch is the orientation/phase branch of the same finite comparison, not an extra fitted degree of freedom.

**Finite operator.**  The four typed branch operators are `A_\Sigma`, `B_N`, `C_+`, `D_-`.  They have scalar shadows `\varphi+\psi=1`, `\varphi\psi=-1`, `\varphi^2=\varphi+1`, and `\psi^2=\psi+1`, but their D0 role is operator-complete rather than algebraically independent.  The terminal representatives `U_A,U_B,U_C,U_D` give four terminal role classes.  Tensoring with the sign representation gives exactly eight signed classes.

**Quadratic readout.**  Observable readout is not the role label itself but the positive response of the corresponding finite channel.  Bosonic and fermionic two-particle quotients select different surviving subspaces of this same eight-state cycle.

**Quotient.**  The quotient is the halt from unresolved continuum metadata to the finite signed terminal role algebra.  The construction of the finite incidence graph marker `V_9` comes only after this quotient.

**Falsification hook.**  If the minimal terminal detector role algebra can be completed without one of the four typed roles `A_\Sigma,B_N,C_+,D_-`, or if the two-port terminal representation requires fewer or more than four pre-sign roles, then the scene-cycle claim fails.  Equally, if a non-abelian Hamiltonian group *smaller* than `Q_8` exists, or if any non-abelian group of order `\le8` other than `Q_8` has zero non-normal subgroups, the `\Omega_8\cong Q_8` forcing of §01.7.1A fails (the finite certificate enumerates the counter and would catch it).  A downstream graph or carrier theorem may not repair either failure.

## 01.8 From eight oriented terminal-role states Ω8 to V9 and construction of the finite incidence graph

The signed detector cycle must acquire a graph-birth marker:

\[
V_9=\Omega_8+\omega_0.
\]

Thus

\[
8\quad\text{belongs to detector closure},
\]

while

\[
9\quad\text{belongs to construction of the finite incidence graph}.
\]

The scene is selected by a finite variational obligation, not by a fitted polynomial. The scene functional is

\[
J_{scene}=(\Omega-8)^2+(n_1-\Omega-1)^2+(n_2-n_1-2)^2+(n_3-n_2-2)^2+J_{coup}.
\]

The admissible order constraint is

\[
0<\Omega<n_1<n_2<n_3.
\]

The minimum is

\[
(\Omega,n_1,n_2,n_3)=(8,9,11,13).
\]

Hence

\[
\Omega_8\rightarrow (V_9,V_{11},V_{13})\rightarrow K(9,11,13).
\]

For the selected scene,

\[
|V|=33,
\qquad
|E|=9\cdot11+9\cdot13+11\cdot13=359,
\qquad
|T|=9\cdot11\cdot13=1287.
\]

The graph invariants used downstream include

\[
|V|=33,\qquad rank(A)=3,\qquad nullity(A)=30,\qquad \gamma=10,
\]

and the shell degrees

\[
d_9=24,\qquad d_{11}=22,\qquad d_{13}=20.
\]

Book 01 stops at construction of the finite incidence graph. The action, boundary, matter, gravity and cosmology books may use this scene, but they may not refit it.

## 01.9 Internal causality and the single line/tick section

The internal metrological section is defined before SI calibration:

\[
\ell_0=1,\qquad \tau_0=1,
\]

and therefore

\[
\boxed{c_{D0}=\ell_0/\tau_0=1.}
\]

This is not an external speed postulate. It is the statement that two independent finite records can be compared only through one common invariant line/tick section. External SI speed is a section map:

\[
c_{SI}:\quad [\ell_0]/[\tau_0]\mapsto \mathrm{m/s}.
\]

At the causal-information level, photon and neutrino roles must not be confused with rest-mass ontology. The photon is the neutral line without rest return:

\[
T_B^\gamma=I,
\qquad
D_B^\gamma=T_B^\gamma-I=0,
\]

so

\[
m_\gamma^2\propto \|D_B^\gamma\gamma\|^2=0.
\]

The neutrino is a neutral return without electromagnetic charge. Both appear only after the line/tick and detector support have already been constructed.

## 01.10 Boundary, mass forgetting and cross-book placement

Book 01 does not use downstream bridge formulas to define the foundation. It keeps only the handoff map needed by later books.

| object | Book 01 role | owner book |
|---|---|---|
| boundary/mass forgetting factor (retired q_mass) | now Boundary Residual Eigenvalue r_∂ | Books 03, 04, 07 (migration note in audit) |
| baryon-boundary information coefficient `I_B` | handed off as boundary-response data | Books 03, 04 |
| residual smallness order `I_12` | kept as a finite-cycle audit scale | Books 03, 05 |
| electron terminal coefficient `C_e=1/38` | section dictionary, not a foundation axiom | Books 03, 04 |
| non-reduced Compton section and `Λ_act` | single-section metrology bridge | Book 03 |
| finite circle audit `π_0` | phase-closure audit, not continuum replacement | Books 02, 05 |

The foundation rule is simple: Book 01 constructs support, response and construction of the finite incidence graph. It does not import mass, baryon, electroweak or cosmological bridges back into the primitive layer.
## 01.11 Contradiction theorems

Book 01 closes by rejecting three common false starts.

### 01.11.1 No interaction without information

Any interaction that cannot alter or constrain an addressable registration is not physical inside D0.

### 01.11.2 No information without detector/register

A bare information line is not a physical event. It becomes physical only through finite detector response.

### 01.11.3 Particles are not the bottom layer

Particles are stable re-detection classes over finite detector records. They are not primitive objects of Book 01.

## 01.12 Active guardrails

1. Do not derive `\varphi` from aesthetic decorative φ numerology. Derive it from minimal non-monopoly self-return closure.
2. Do not use `\delta_0=\varphi^{-3}`. The active convention is `\delta_0=1/(2\varphi^3)`.
3. Do not read `\Omega_8` as a graph. It is detector closure; `V_9` is construction of the finite incidence graph.
4. Do not use `K(9,11,13)` as a chosen model space. It is selected by scene obligations.
5. Do not introduce a second scale anchor. `c_{D0}=1`, `\ell_0=1`, `\tau_0=1` are internal; SI values are section maps.
6. Do not treat bridge formulas like `q_{mass}`, `I_B`, `38`, or `\pi_0` as foundation primitives. They are preserved here as cross-references.

## 01.13 Claim coverage from theorem database

| Claim | Status | Name | Forbidden shortcut | Primary/related certs |
|---|---:|---|---|---|
| `D0-FOUND-001` | CORE-FOUNDATION | No-monopoly verification algebra | Do not derive phi from generic unitary contact, Helstrom scans, or entropy linearity alone. | (see canonical registry); minimal Popper/dyad certs |
| `D0-FOUND-002` | CORE-FOUNDATION | Minimal addressable record split | Do not use delta0=phi^-3; active convention is 1/(2 phi^3). | (see canonical registry) |
| `D0-SCENE-001` | CORE-SUPPORT | eight oriented terminal-role states Ω8 detector cycle | Do not treat phi alone as physical geometry before eight oriented terminal-role states Ω8 closure. | d0_core_certificates.py; (see canonical registry) |
| `D0-SCENE-002` | CORE-ACTION | J_scene selects K(9,11,13) | Do not read J_scene as fitted polynomial for later constants. | d0_graph.py; d0_core_certificates.py; (see canonical registry) |
| `D0-METRO-001` | CORE-FOUNDATION | Single causal line/tick invariant | Do not count c as a second sector anchor. | vp_c_time_length_single_section_closure.py |
| `D0-METRO-002` | SINGLE-SECTION-OUTPUT | Lambda_act single action section | No proton, W/Z, Planck, G_N, H0, or dark anchor as second scale. | vp_c_time_length_single_section_closure.py |

## 01.14 Integrated theorem: φ-rigidity and dimension-graded detector quantum

This rigidity theorem belongs in the foundation book because it answers the first external objection to the φ split: whether the value can be perturbed and compensated later by a convention.

Let

```math
C(x)=x^2-x-1,
```

and compare the three detector definitions which coincide at the φ point:

```math
p_+(x)+p_-(x)=x^{-1}+x^{-2},
```

```math
\delta_{split}(x)=\frac{x^{-1}-x^{-2}}2,
\qquad
\delta_{linear}(x)=x-\frac32,
```

```math
\delta_{norm}(x)=\frac{x^{-1}-x^{-2}}{2(x^{-1}+x^{-2})}.
```

At

```math
x=\varphi,
\qquad
\varphi^2-\varphi-1=0,
\qquad
\varphi^{-1}+\varphi^{-2}=1,
```

these definitions collapse to the same detector quantum

```math
\delta_0=\frac{\varphi^{-1}-\varphi^{-2}}2
=\varphi-\frac32
=\frac1{2\varphi^3}.
```

Away from \(\varphi\), normalization, algebraic closure and detector asymmetry no longer agree.  Therefore a shifted value of \(\varphi\) is not another member of a smooth D0 family; it requires a new external catalogue choosing which definition to preserve.  Such a catalogue violates the no-monopoly verification rule.

### φ is cement, not an ingredient [^b01-35]

φ is not one constant among the constants of D0; it is the cement — the thing the construction stands on at every point. The reason a perturbed φ is not a "nearby theory" is that φ is **one object showing four independent mathematical faces**, and each face is forced from a different branch of mathematics yet returns the same root. None is decorative; each one carries a structural floor of the spine.

- **Algebra / Galois face.** \(\varphi^2=\varphi+1\): Vieta pair on \(C(x)=x^2-x-1\), roots \(\varphi,\psi=1-\varphi\), invariant under \(\mathrm{Gal}(\mathbb Q(\sqrt5)/\mathbb Q)=\mathbb Z_2\). Floor it carries: flavor, the ABCD role alphabet. Status: CERT-BACKED (forcing cert: `vp_vieta_galois_abcd.py`).
- **Arithmetic face.** \(\varphi=[1;1,1,\dots]\): minimal continued fraction (MDL), Hurwitz-maximal irrationality, Lucas/Fibonacci convergents. Floor it carries: \(\alpha\), the \(+2\) step. Status: CERT-BACKED (forcing cert: `vp_v1142_hurwitz_phi_phase_rigidity.py`).
- **Dynamics face.** \(\varphi\) is the fixed point of \(r=1+1/r\), the last KAM torus to break. Floor it carries: time. [^b01-33].
- **Topology face.** \(Q_8\), the spinor sheet, the icosians → \(E_8\). Floor it carries: spin, the carrier. Status: CERT-BACKED downstream (Q8→E8 spine; this face is cited, not re-derived, here).

The four faces are why rigidity is not a coincidence: to move φ you must simultaneously break the Galois pairing, spoil Hurwitz-optimality, unhinge the KAM fixed point and detune the \(E_8\) lattice — four unrelated failures at once, each killing one floor of the spine. There is no single convention that absorbs all four; that is exactly the catalogue the no-monopoly rule forbids.

**φ/M1 duality lemma** [^b01-36]. On the class of rotation numbers, M1 has a unique fixed point, and it is \(\varphi\); conversely, φ-rotation is the unique dynamics under which M1 is satisfiable at every finite depth. The two directions pin φ from both sides — value and dynamics — so neither can be slid without breaking the law M1 itself, not merely a downstream formula. [^b01-34].

### δ₀ is the price of the rotation-minus-rest duality [^b01-37]

The detector quantum δ₀ above is not just an algebraic offset; it is a measured distance. Unity has two canonical cuts:

- the **symmetric** cut \(\tfrac12:\tfrac12\) — the fair coin, invariant under \(x\mapsto 1-x\);
- the **golden** cut \(\varphi^{-1}:\varphi^{-2}\) — the rotation that does not fall, invariant under the Galois swap \(\varphi\leftrightarrow\psi\).

δ₀ is the norm-distance between these two cuts:

```math
\delta_0=\Bigl|\tfrac12-\varphi^{-1}\Bigr|=\frac{\sqrt5-2}2=\varphi-\frac32=\frac1{2\varphi^3}.
```

So δ₀ is the **price of the duality "rotation minus rest"** — how far the self-consistent cut of unity sits from the symmetric one. The self-consistent cut is not symmetric; \(\varphi^{-1}\neq\tfrac12\). Status: CERT-BACKED (forcing cert: `vp_vieta_galois_abcd.py` derives δ₀ as the forced, non-fitted cut offset, and shows the \(\varphi^{-1}:\varphi^{-2}\) cut is symmetric only under the Galois \(\mathbb Z_2\), not under \(x\mapsto 1-x\)).

**Why there is something rather than equal nothing.** The CP-violating coordinate of the universe is this same gap, run through three zones:

```math
\bar\eta=3\,\delta_0.
```

Matter–antimatter asymmetry exists **because the self-consistent cut of unity is not symmetric**: the coin is charged by exactly δ₀, and that charge — not dynamical accident — is the reason there is something rather than an even balance of nothing. The whole downstream theory is the unfolding of the single fact \(\varphi^{-1}\neq\tfrac12\). Status: PROOF-TARGET (cert obligation open: the \(\bar\eta=3\delta_0\) baryon-asymmetry reading needs its own exact-arithmetic cert; do not cite a baryon-form-factor cert as its forcing).

### Dimension-graded detector quantum

The dimension-graded detector quantum is retained as a foundation invariant:

```math
Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}.
```

Hence

```math
Q(1)=\varphi^{-3}=2\delta_0,
\quad
Q(2)=\varphi^{-2},
\quad
Q(3)=\varphi^{-1},
\quad
Q(4)=1,
\quad
Q(5)=\varphi.
```

The factor of two is structural: \(\delta_0\) is half of the two-branch asymmetry, while \(Q(1)=2\delta_0\) is the full one-dimensional quantum.  The quantum equals 1 exactly at \(D=4\), centered on the four-role budget \(|\mathrm{ABCD}|=4\); the binary quantum sits at \(D=1\) as \(\varphi^{-3}=2\delta_0\); and the same δ₀ generates the descending cascade \(\delta_{-n}=\delta_0^{\,n+1}\). This is the integrated ``φ-ladder quantization'' guardrail. Status: CERT-BACKED (forcing cert: `vp_dim_ladder_compact.py`, exact arithmetic in \(\mathbb Q(\varphi)\), verifies \(Q(D)=2\delta_0\varphi^{D-1}=\varphi^{D-4}\) for \(D=1..8\) and \(Q(4)=1\)).

### Unity split → space (symmetric) + time (antisymmetric δ₀) [^b01-37]

The two cuts above are not only a rigidity device; they are the **root of the space/time split** (claim `D0-UNITY-SPLIT-SPACETIME-001`, LEM). Write any cut of the unit as \(1=(\tfrac12+s)+(\tfrac12-s)\). The **symmetric** part \((\tfrac12,\tfrac12)\) is invariant under exchanging the two sides \(a\leftrightarrow b\) — swapping sides changes nothing, transport is reversible, there is no arrow ⇒ **space**. The **antisymmetric** part \(s=\delta_0\) *changes sign* under \(a\leftrightarrow b\) — the swap singles out a direction ⇒ **time**, an arrow of magnitude \(\delta_0\). The operator reading is exact: \(T=\begin{psmallmatrix}0&1\\1&-1\end{psmallmatrix}\) has \(\det T=-1=\psi\varphi\) (Vieta) and spectrum \(\{\varphi^{-1},-\varphi\}\) (roots of \(\lambda^2+\lambda-1\)); the positive eigenvalue is the symmetric (space) mode, the single **negative** eigenvalue is the sign-flip = the one **arrow of time**, and \(\det=-1\) forces *exactly one* sign change. Lean `D0.Synthesis.UnitySplitSpacetime` (`unity_split_spacetime`) proves \(\delta_0=\varphi^{-1}-\tfrac12=(\sqrt5-2)/2\) exactly, \(\det T=-1=\psi\varphi\), and the two eigenvalues with their signs; cert `vp_unity_split_spacetime.py` (can-FAIL; the \(s=0\) control restores \(\varphi^{-2}+\varphi^{-1}=1\), reversible, no arrow). **Honest level — LEM:** the step "the symmetric \(\mathbb S_2\)-invariant *is specifically* rank-3 adjacency" routes to the rank-3 = causal-cone node, which is **already FORCED** (`D0-RANK3-CAUSAL-CONE-FORCING-001`, §07.51.3); so the residual is that one identification and the cone-speed (Connes) unit, **not** a fresh open gap. The BTC transition-asymmetry (\(\varphi^{-2}(1-\delta_0)+\varphi^{-1}(1+\delta_0)\neq1\)) is a confirmation on data, not a derivation. Not promoted past LEM.

### Degree-2 from the detection act (the type-theoretic 2nd channel) [^b01-35]

The quadratic recursion \(C(x)=x^2-x-1\) at the head of this section also has a **type-theoretic** origin — a fifth independent route to \(p^2+p=1\) (claim `D0-DETECTION-QUADRATIC-001`, CORE), and the one that reads the *degree* off the act of detection. A detection has exactly two comparison kinds: by **membership** (\(\in\)) — levels "existence-class" vs "event-in-class" are different categories (Russell hierarchy), so they compare *linearly*, against a reference of belonging (degree 1, the term \(p\)); and by **value** — two events inside the *same* class cannot be separated by membership (each belongs), only by their mutual value, a bilinear form = area (degree 2, the term \(p^2\)). Unity is exhausted by the direct and the mutual contribution, \(p+p^2=1\), root \(p=1/\varphi\). The degree is *exactly* 2 because there are *exactly two* comparison kinds: a would-be third is a degree-3 term \(p^3=2p-1\), which reduces into \(\mathrm{span}\{1,p\}\) (runtime iteration, BOOK_01:556) and is therefore not an independent slot. So the tower closes on three levels by **exhaustion of comparison kinds**, not by enumeration — an independent reading of the same no-go that stops the zone tower at three (`D0-TOWER-STOP-NOEXT-001`, §05.6 obligation 5). Lean `D0.Tower.DetectionQuadratic` (`detection_quadratic`) reuses the CORE tower-stop algebra (`degree2_closure`, `p_cubed_reduces`) and adds `|{membership, value}| = 2`; cert `vp_detection_quadratic_types.py` (can-FAIL). **Honest boundary:** the decidable algebra is the CORE tower-stop content; the categorical "two kinds exhaust degree-2" is the *forcing reading* (DEF-0.2.2 style), an independent channel that **strengthens** obligation 5 — it is not a separate machine-checked categorical theorem and does not replace the no-go.

**Theorem 12.1 — φ-rigidity.**  The φ root is structurally isolated as the unique point where finite detector normalization, quadratic recursion and detector asymmetry coincide.  Perturbing the root separates these three definitions — and simultaneously breaks all four faces of φ (Galois, arithmetic, dynamics, topology) — before any particle or cosmological formula is used. Equivalently, by the φ/M1 duality lemma the perturbation breaks the law M1 itself, not a convention layered on top of it.
## 01.15 Condensed/profinite formal specification

D0 uses condensed/profinite language as a formal support layer, not as terminology.  Let `Prof` be the category of profinite sets with continuous maps.  The D0 support is a filtered inverse system

\[
S_{D0}=\varprojlim_N S_N,
\qquad
S_N=\{A,B,C,D\}^{N}/\sim_N,
\]

where the equivalence relation is generated only by finite halt, address-stability and role-preserving quotient relations.

The associated representable test functor is

\[
\underline S_{D0}(T)=\operatorname{Hom}_{cont}(T,S_{D0})
\]

for profinite test objects `T`.  The physically admissible observables are not all maps out of this functor.  They form a subfunctor

\[
\operatorname{Obs}^{D0}\subset \operatorname{Obs}
\]

whose sections satisfy the following finite obligations:

1. finite-stage factorization through some `S_N` before comparison;
2. lift to a finite operator family `D_N` compatible with projections;
3. positive response `R_N=D_N^\dagger D_N`;
4. trace or finite quadratic readout;
5. halt quotient and stable re-detection class;
6. naturality under finite refinements:

\[
P_{N+1,N}D_{N+1}=D_NP_{N+1,N},
\qquad
P_{N+1,N}R_{N+1}=R_NP_{N+1,N}.
\]

The `four terminal roles A,B,C,D` cycle is therefore a natural finite-stage operator cycle, not a detached alphabet.  Its four duties are normalization, conjugate coupling, forward recurrence and return recurrence.  Their scalar equations may be algebraically related, but their operator roles are distinct in the admissible detector cycle.

## 01.16 Condensed finite stages and response-order comparison

The D0 condensed/profinite support is not used merely to name an infinite object. It supplies finite stages on which external comparisons can be tested. For a finite quotient `S_N`, every admissible comparison must be phrased in terms of finite response tests:

```math
\Phi_N(\rho)=F(\operatorname{Tr}(\rho R_{N,a_1}),\ldots,\operatorname{Tr}(\rho R_{N,a_k})),
\qquad F\ \text{convex}.
```

A continuum or external observable is admitted only through a projective family of finite approximations preserving these response tests. This adds a bridge-level condition to the D0-admissible subfunctor:

```math
\underline{Obs}^{D0}_{bridge}
\subset
\underline{Obs}^{D0}
\subset
\underline{Obs}.
```

Thus the condensed support does not authorize arbitrary continuum dressing. It forces a finite response-order comparison at each stage.

## 01.17 Finite-frame Born and EPR closures

The foundational detector stage now carries two executed finite proof cells.

### 01.17.1 Finite-frame Born 2.0: effects, coarse-graining and tensor consistency

The detector-stage Born rule is now stated at the finite-effect level, not merely as a two-channel or raw-list normalization.  A finite D0 readout consists of:

```text
finite outcome support I
finite detector support S
nonnegative effects E_i(s) >= 0
nonnegative detector state R(s) >= 0
strictly positive total response Σ_i Σ_s E_i(s)R(s) > 0
```

The raw response of outcome `i` is therefore

```math
r_i=\sum_{s\in S}E_i(s)R(s).
```

The probability readout is forced to be

```math
p_i=\frac{r_i}{\sum_j r_j}.
```

This is not imported from Hilbert-space quantum mechanics.  The matrix trace expression

```math
P_N(a)=\frac{\operatorname{Tr}(\Pi_aR_N)}{\operatorname{Tr}(R_N)}
```

is now only the matrix presentation of the finite-effect sum.  The Lean owner is

```text
D0.finite_effect_born_readout_unique
```

with the no-hidden-response form

```text
D0.finite_effect_born_no_hidden_response
```

This closes the previous weakness: D0 now identifies the finite effect frame that supplies the responses and forbids a second hidden positive state or probability functional at the same detector stage.

Coarse-graining is also not a new probability postulate.  If a map `π : I -> K` merges fine outcomes into a coarse outcome `k`, the coarse response is the aggregate

```math
r_k^{coarse}=\sum_{i:\,\pi(i)=k}r_i.
```

The coarse probability must be the normalized aggregate response.  The Lean owner is

```text
D0.finite_coarse_born_readout_unique
```

Therefore a calculation cannot normalize before and after coarse-graining using different hidden rules.  The same finite response object controls both levels.

Tensor/product readout is treated the same way.  Once a finite product response over `I x K` is frozen, the joint probability assignment is unique:

```text
D0.finite_tensor_born_readout_unique
```

A nonlinear or power readout, for example a rule of the form `p_i ∝ r_i^q`, is admissible only if it still satisfies the response-recovery equation

```math
p_i\sum_jr_j=r_i.
```

At fixed response this collapses pointwise to the Born weight.  If it differs anywhere, it is not a D0 readout.  The Lean owner is

```text
D0.finite_power_readout_no_alternative
```

The active claim is therefore finite and exact:

```text
finite effects + positivity + response recovery + coarse/tensor consistency
=> unique normalized detector readout;
no independent probability knob;
no alternative power readout at fixed response.
```


### 01.17.1a Born 3.0: phase blindness forces the quadratic response

The previous finite-effect theorem still assumed that a positive raw response had already been supplied.  The measurement-theory gap was therefore not the normalization step; it was the origin of the raw response itself.  The active closure is now one level earlier.

At one finite detector atom the amplitude is a two-component phase quadrature

```math
z=(x,y).
```

The most general quadratic detector response on this atom is

```math
Q(z)=a x^2+bxy+c y^2.
```

A detector readout cannot depend on the arbitrary internal quarter-turn of the phase quadrature,

```math
(x,y)\mapsto(-y,x).
```

Imposing `Q(x,y)=Q(-y,x)` for all finite amplitudes gives, by evaluating at `(1,0)` and `(1,1)`,

```math
a=c,\qquad b=0.
```

Hence every phase-blind quadratic detector response has the forced form

```math
Q(z)=a(x^2+y^2).
```

After unit calibration of the detector channel,

```math
Q(z)=x^2+y^2.
```

This is the finite D0 content of the usual `D†D` response.  The probability rule is then not postulated: a finite family of amplitude channels first produces raw responses

```math
r_i=\sum_s\bigl(x_{i,s}^2+y_{i,s}^2\bigr),
```

and the already-proved finite Born readout gives

```math
p_i={r_i\over\sum_j r_j}.
```

The Lean owners are

```text
D0.phase_blind_quadratic_response_is_norm_sq_scaled
D0.unit_phase_blind_quadratic_response_is_norm_sq
D0.finite_amplitude_born_readout_unique
D0.finite_amplitude_born_no_alternative
```

The closure is therefore stronger than finite normalization.  D0 now has the chain

```text
finite phase quadrature
+ quadratic detector closure
+ internal phase blindness
=> squared-norm response D†D
=> unique finite Born normalization.
```

What remains outside this finite theorem is not the Born rule itself, but only the continuum Hilbert-space presentation and analytic-limit comparison.

### 01.17.2 Shared-support EPR representation

Before geometric projection, an entangled pair is a shared finite support, not two independent objects connected by a signal in a pre-existing continuum. With Pauli-stage observables

```math
A_0=\sigma_z,\quad A_1=\sigma_x,\quad
B_0=(\sigma_z+\sigma_x)/\sqrt2,\quad
B_1=(\sigma_z-\sigma_x)/\sqrt2,
```

the finite CHSH operator

```math
\mathcal C=A_0\otimes(B_0+B_1)+A_1\otimes(B_0-B_1)
```

satisfies

```math
\|\mathcal C\|=2\sqrt2.
```

The D0 statement is therefore not superluminal collapse. It is finite shared-support correlation before the metric shadow is taken.

Entangled readouts are shared-support effects before metric projection.
Two visible regions may be distant after metric projection while still sharing the same archive/cut-and-project source.
No superluminal update is required; the correlation is a support identity before the metric readout.

## 01.18 Spatial branch emergence from finite phase return

D0 does not treat spatial arms, rays, or coordinate branches as primitive continuum objects. A finite ordered registration chain can acquire visible spatial structure when it is read through a cyclic phase quotient. If the tick index is `n` and the phase is `n mod τ`, a near-return `qв‰€mτ` decomposes the tick line into residue branches `n=a+tq`. The phase drift along each branch is controlled by `q-mτ`.

For the D0 circumference surrogate `τ_0=2π_0`, the first nontrivial stable return `44≈7τ_0` yields `φ_Euler(44)=20` admissible branches. This gives the terminal shell count `d_13=20` a dynamical phase-unfolding interpretation: it is the admissible branch count of the first stable finite return, not a free shell label.

## 01.19 Phase-unfolding master chain

D0 no longer treats spatial branching as a primitive geometric background.  An ordered finite registration can generate visible geometry through a phase quotient.  For a phase circumference \(\tau\), the map

\[
U_\tau(n)=(n,n\bmod \tau)
\]

turns the one-dimensional tick sequence into a branch foliation whenever an integer pair \((q,m)\) satisfies \(|q-m\tau|\ll 1\).  The residue classes modulo \(q\) are the coherent branches.  An admissibility filter selects the branches visible to the detector.

The strengthened chain is:

```text
tick order
-> irrational phi^-2 phase
-> finite return modulus
-> residue branches
-> detector-visible geometry.
```

The irrational phase is not an optional decoration.  It prevents rational
locking before the detector chooses a finite quotient.  The finite quotient is
then what makes branches visible: residue classes modulo `q` are geometry only
after the readout modulus is fixed.

The D0 structural return

\[
q_T=|four terminal roles A,B,C,D|\,|V_{11}|=4\cdot11=44,
\qquad
m_T=|four terminal roles A,B,C,D|+\operatorname{rank}(A_K)=4+3=7
\]

is the first terminal phase-return window.  Its admissible coprime branch count is

\[
\varphi_E(44)=20=d_{13}.
\]

Thus the terminal shell degree is the branch count of the first stable phase unfolding.

The second return is

\[
q_{EW}=2(|four terminal roles A,B,C,D|+1)(2|V|+|four terminal roles A,B,C,D|+1)=710,
\qquad
m_{EW}=(|four terminal roles A,B,C,D|+1)d_{13}+|V_{13}|=113.
\]

Since \(710/113\) is a near-return for the Euclidean phase circumference, and

\[
\varphi_E(710)=280=|\Omega_8|\cdot 35,
\]

the electroweak radial depth is the per-\(\Omega_8\)-sector branch depth:

\[
D_{EW}=35.
\]

This section upgrades phase unfolding from an illustration to a structural theorem: later scale depths are repeated applications of the same finite tick \(\to\) phase quotient \(\to\) return modulus \(\to\) residue branch \(\to\) quotient mechanism.

The Lean owner establishes that the φ phase is non-periodic, that the finite return modulus unfolds branches, and that the quasicrystal order is not a periodic lattice.

## 01.19a Cut-and-project origin of visible branches

Phase unfolding is a cut-and-project mechanism, not a visual metaphor. The ordered tick chain supplies a non-periodic φ phase; a finite readout quotient chooses a return modulus; the quotient residues become detector-visible branches.

```text
higher-dimensional archive support
-> irrational φ active slice
-> finite quotient window
-> residue branches modulo q
-> visible spatial arms
-> tiling-hull patches
```

The active slice is irrational, so it is not a translational lattice. The quotient window is finite, so the detector still sees coherent branch order. This is the D0 sense in which smooth macro-geometry is the coarse-grained shadow of ordered aperiodic finite support.

### 01.19a.1 The cut-project slope is forced to φ⁻², not chosen

The slice angle is not a free dial. The primitive positive-response theorem gives `p+p²=1`, so the only admissible return branch is `α_{D0}=p²=φ⁻²` [^b01-38]. The cut-and-project window therefore inherits the φ⁻² slope by force, not by fit: the active slice is the φ⁻²-irrational line, and Hurwitz/continued-fraction extremality of the φ class makes it the *maximally* non-resonant slope — the one slice that refuses low-denominator rational locking before a finite quotient is imposed. Status: **FORCED** (the slope is the response-equation root, not an aperiodic-tiling input).

### 01.19a.2 The carrier and time are one object [^b01-39]

The cut-and-project carrier of this section is **not a second structure layered beside** the time torus `T=[[0,1],[1,-1]]`. They are the same object seen two ways — spatially as a quasicrystal, dynamically as a toral automorphism.

The bridge is an exact symbolic identity, checked letter-by-letter, not an analogy:

- The time operator `T` has golden-slope eigendirections, namely `φ⁻¹` and `−φ` (the conjugate pair of the response equation `x²+x−1=0` re-used by the time layer).
- The Fibonacci **substitution** word generated by `a→ab, b→a` and the Sturmian **cut-and-project** word of slope `φ⁻²` coincide **letter-by-letter**, now verified *exactly* to 4000 symbols by an executable certificate using exact integer floors `⌊kφ⌋=(k+⌊√(5k²)⌋)//2` (no floating point), under the canonical tile↔letter relabelling, with the rare-letter frequency equal to `φ⁻²` and a rational-slope negative control. The conjugate `ψ=−1/φ` is Pisot, `|ψ|=φ⁻¹<1` — the contracting direction that gives time its arrow.

Therefore the phase unfolding of Book 01 — the irrational `φ⁻²` phase opening into residue branches — *is* exactly the symbolic dynamics of the golden foliation of the time torus:

```text
quasicrystal carrier (space, seen statically)
   ==  symbolic dynamics of  ==
golden foliation of the time torus T (time, seen dynamically)
```

Carrier (the quasicrystal) and time (the toral automorphism) are **one object, seen spatially versus dynamically**. The branch foliation that the detector reads as visible spatial arms is the same foliation whose return map the time operator iterates. Status: **CORE-FORCING / THE** [^b01-40].

The same `φ⁻²` rotation is also the address-defect of the memory torus on its own return: for odd `n`, `φⁿ=Lₙ+φ⁻ⁿ`, and at `n=5` this reads `φ⁵=11+φ⁻⁵`, i.e. the torus address `|V_{11}|=11` plus its integrality defect `ξ₅=φ⁻⁵`, with `Tr(T⁵)=−L₅=−11` landing the fifth time-return exactly on the torus address [^b01-41]. This is why the slice that unfolds space and the operator that advances time share the golden slope: they are the spatial and temporal faces of the same return.

### 01.19a.3 Declared gap

The letter-by-letter coincidence is now closed by an **exact, executable** certificate (4000 symbols, exact integer floors — not a 40-symbol eyeball) and the slope is force-derived, so the *symbolic* identity is no longer empirical. What remains an obligation is the **topological/measure conjugacy**: that the `φ⁻²` circle rotation is formally conjugate to the return map of the golden foliation of `T` is one page of standard ergodic mechanics (Sturm / Morse–Hedlund; golden-mean shift, Vershik) whose machinery is not yet in the formal kernel. Status: **PROOF-TARGET (topological conjugacy open; exact symbolic coincidence certified)** — promotion needs the conjugacy written out, not a new numeric check.

The carrier side is verified by finite certificates covering φ-phase non-periodicity with finite return branches and the operator origin of the quasicrystal phenomenology; the time-side address identity is closed by its own finite certificate. The Lean owner packages the carrier.

### 01.19a.4 The quasicrystal carrier is FORCED, not a convenience [FORCING]

The cut-and-project carrier above is not one admissible choice among many — it is forced, and the lattice "bridge" is thereby upgraded to a forcing (claim `D0-QUASICRYSTAL-CARRIER-FORCING-001`). The chain: (i) **finite is rigorous-only** — non-perturbative gauge theory is defined with full mathematical rigour *only* on a finite lattice (Wilson 1974; the continuum Yang–Mills mass gap is an open Clay problem), so a finite carrier is the only one carrying rigorous meaning; (ii) **no preferred step** — a periodic lattice carries an arbitrary spacing `a` and needs the limit `a→0`, whereas a quasicrystal is self-similar by `φ` (inflation `[[1,1],[1,0]]`, Perron eigenvalue `φ`, `A/B→φ`) with no distinguished unit and no `a→0` limit; (iii) **M1** forbids the hand-chosen `a` as exogenous, so the carrier *must* be aperiodic-self-similar; (iv) aperiodic order + long-range order + 5-fold symmetry **⇒ `φ`** (Penrose / de Bruijn cut-and-project, `2cos(π/5)=φ`; Shechtman, Nobel 2011). So `φ` is forced from non-perturbative rigour + M1, not postulated — a new external channel to `φ` alongside Hurwitz extremality, the Jones index, KAM, and the quadratic Pisot property. (cert `vp_quasicrystal_carrier_forcing.py`.)

Leg (i) — "finite is rigorous-only" — is now carried as its **own explicit owner-edge**: claim `D0-LATTICE-FINITENESS-BRIDGE-001` (BRIDGE, `ASSUMP-WILSON-LATTICE-1974`; cert `vp_lattice_finiteness_bridge.py`), the "why-finite" leg that **composes** with the "why-φ" forcing here. Wilson's lattice rigor and the open continuum Yang–Mills mass gap (Clay) are the external owners; D0's contribution is removing the arbitrary-spacing freedom by M1. Splitting the bridge out keeps the carrier-forcing chain auditable: the *finiteness* rests on a cited external theorem, the *self-similarity-to-φ* is the D0 forcing.

**Open remainder — the explicit projection (honest dual, outcome b).** The principled forcing is closed; one technical screw is open — identifying the *specific* scene `K(9,11,13)` with a *specific* cut-and-project (claim `D0-QUASICRYSTAL-PROJECTION-001`). The standard icosahedral `6D→3D` projection is built and has **rank 3** (the physical slice, matching the carrier's rank 3 — exact minor `det=−2φ²≠0`; cert `vp_icosahedral_cutproject.py`). But it is `6D→3D`, so its internal space is `3`-dimensional, **not** `30`: `K(9,11,13)` is `33`-dimensional (`rank 3 + nullity 30`), so reproducing the nullity `30` would need a `33D→3D` cut-and-project, not the `6D` icosahedral one. The agreement `nullity 30 = ` icosahedron **edges** (`V=12,E=30,F=20`) is strong *support* but a coincidence of the integer `30`, not a derivation.

**Resolved (separation), not left open.** The question — is `K(9,11,13)` itself a `33D→3D` icosahedral cut-and-project with `A₅` symmetry on its rank-3 image? — is now answered **no**, decidably (claim `D0-CARRIER-NOT-ICOSAHEDRAL-001`, Lean `D0.Claims.CarrierNotIcosahedral`, cert `vp_carrier_not_icosahedral.py`). `Aut(K(9,11,13)) = S₉×S₁₁×S₁₃`, and because the zone sizes are *distinct* (`9≠11≠13`) the induced symmetry on the three zone-classes — the entire symmetry the rank-3 physical image can inherit — is the **trivial** group (only the identity preserves the size assignment). The icosahedral group `A₅` has order `60`; it cannot embed into the trivial induced symmetry (`60>1`), so `K(9,11,13)` carries **no** icosahedral symmetry on its rank-3 image and is **not** the icosahedral cut-and-project. The obstruction is exactly the size-asymmetry: an *equal*-zone `K(n,n,n)` would admit the full `S₃` zone-swap, but `9≠11≠13` kills it. So the icosahedral `A₅` belongs to the **flavor/`E₈`** side (the level-5 modular group `Γ₅≅A₅`, §06.30a, `D0-MODULAR-TIME-FLAVOR-001`), not the carrier; the `rank=3` convergence (carrier rank-3 ↔ icosahedral 3D-slice dimension) is **kept** as a real third channel to "3", and `nullity 30 = ` edges is a **confirmed coincidence**. The named gap is closed by a sharp negative — the same honest discipline that resolved the `γ`-packing probe and the `V_CKM U_PMNS^T=I` reading.

**Third channel to the triple.** The `3D` physical slice (`A₅ = 2I/\{\pm1\} = \mathrm{PSL}(2,5) ⊂ SO(3)`) is a third independent route to `rank = 3`, alongside Frobenius (`ℍ` has three imaginary axes) and the linear-algebra theorem (the rank of a complete tripartite graph is its number of parts). With the tower-stop no-go (`D0-TOWER-STOP-NOEXT-001`, three zones) these are four manifestations of one `3`. And the icosahedral quasicrystal slices `E₈` (Elser–Sloane), the *same* `E₈` the icosian role lattice generates (BOOK_02 §02.18) — one object yields both the role lattice and the carrier slice (consistency, cert `vp_e8_quasicrystal_slice.py`; not a new derivation of the zones). The three channels are independent forcings — their convergence strengthens, it is not summed as a single proof.
## 01.20 Capacity closure of four terminal roles A,B,C,D, Ω8 and V9

The terminal readout alphabet is fixed by finite information capacity. A primitive two-port detector has a binary terminal dyad `D2`. The complete terminal role set is therefore `D2 × D2`, with four roles. This is the four terminal roles A,B,C,D alphabet:

\[
four terminal roles A,B,C,D=D_2\times D_2,
\qquad |four terminal roles A,B,C,D|=4.
\]

The four roles are not a list to be chosen — they are forced as the minimal self-sufficient act of record: reading (A), read (B), trace (C), reference (D). Fewer than four leaves the act without a distinguishable record, or requires an external memory to hold the missing role. That is the catalog M1 forbids [^b01-45].

The orientation/phase extension adds the unique sign bit:

\[
\Omega_8=four terminal roles A,B,C,D\times\{+,-\},
\qquad |\Omega_8|=8.
\]

The sign bit `{+,−}` is the irreversibility of write/erase; it is the one bit that distinguishes the act from its undo, and no further bit can be added without an exogenous orientation catalog. Hence `Ω8 = ABCD × {±}`, `|Ω8|=8` [^b01-46].

A reusable shell also requires a stationary marked witness section `ω0`. Hence

\[
V_9=\Omega_8\sqcup\{\omega_0\},
\qquad |V_9|=9.
\]

The next two shell extensions are the only primitive unresolved capacities over the pointed shell: the direct/return dyad and the full terminal role square. Therefore

\[
V_{11}=V_9\sqcup D_2,
\qquad
V_{13}=V_9\sqcup four terminal roles A,B,C,D.
\]

This gives the first complete scene sizes `(9,11,13)`. The construction rules out alternatives: `V8` has no basepoint, `V10` has an extra hidden marker, `V11` cannot be replaced by `V10` without losing direct/return capacity, and `V13` cannot be replaced by `V12` without losing one terminal role.

- **Certificate (count side)**: `05_CERTS/vp_v1141_abcd_omega8_v9_phi_capacity.py` checks the full capacity ladder `ABCD=D2×D2=4`, `Ω8=8`, `V9=9`, `V11=11`, `V13=13`, total `|V|=33`, and the V8/V10 exclusions as finite-capacity gaps. Status: VERIFIED (count).

### Orbital rigidity: K(9,11,13) is the unique vacuum graph

The scene is the complete tripartite graph

\[
G:=K(9,11,13),\qquad V=V_9\sqcup V_{11}\sqcup V_{13}.
\]

The scene sizes above fix only the *partition*; they do not yet fix which edges exist. The graph is forced — not selected — by a single orbital argument over the VACUUM contract [^b01-47]. Fix the partition `V = V9 ⊔ V11 ⊔ V13` and consider simple loopless graphs on `V`. Three obligations:

- **(C1) Exchangeability.** No permutation inside a part may change the physics, i.e. the adjacency matrix `A` is invariant under `S9 × S11 × S13`. A part-internal exception would name a privileged vertex — an exogenous parameter — violating M1.
- **(C2) Role-closure.** The three roles must be mutually reachable; a missing between-part block would require an external protocol "how/when to carry distinguishability across roles."
- **(C3) No-subaddress.** No new distinguishable sub-address of connectivity may be introduced inside a part, or the addresses 9/11/13 stop being minimal.

The argument is orbital, not enumerative:

1. From **(C1)**, `A` is constant on the orbits of `S9 × S11 × S13`. Hence every block `A|_{Vi×Vj}` is block-constant: for `i≠j` it is all-zeros or all-ones; for `i=j` it is the empty or the complete graph on `Vi`.
2. From **(C3)**, any within-part edge creates the distinguishable binary property "neighbour-inside-part / neighbour-outside-part," which is not codable in the original addressing without an extra marker (an external distinguishability catalog). So `A|_{Vi×Vi}=0` for `i∈{9,11,13}`.
3. From **(C2)**, any all-zeros between-part block `A|_{Vi×Vj}=0` (`i≠j`) would leave roles `Vi`, `Vj` non-interacting; closing the scene would then need an external coupling protocol. So all between-part blocks are all-ones.

Therefore `A` is exactly `K(9,11,13)` — empty within parts, complete between parts. This is "the shape of emptiness" at the given addressing. **[^b01-42]** — the orbital-uniqueness theorem is now discharged by a finite certificate and Lean module: step 1 (block-constancy under `S9×S11×S13`) is verified by exhaustion on a faithful model, and steps 2–3 collapse to the *unique* loopless-and-complete block pattern, the complete tripartite graph with `|E| = 359` (Lean-proved). Role = orbit ⇒ unique scene is closed; only the M1 no-extension meta-step (why the tower stops, BOOK_05 §05.6 obl. 5) remains a theorem-target.

**Equivalent information reading (REM 17.0.1.A.1).** Any incomplete between-part block is a *Catalog of Prohibitions* (a list of missing edges); any within-part edge is a *Catalog of Privileges* (a list of allowed exceptions). `K(9,11,13)` is the unique configuration carrying neither catalog [^b01-48].

**Adjacency matrix (DEF 17.0.2).** The block-constant form forced above is

\[
A=\begin{pmatrix}
0_{9\times 9} & \mathbf{1}_{9\times 11} & \mathbf{1}_{9\times 13}\\
\mathbf{1}_{11\times 9} & 0_{11\times 11} & \mathbf{1}_{11\times 13}\\
\mathbf{1}_{13\times 9} & \mathbf{1}_{13\times 11} & 0_{13\times 13}
\end{pmatrix},
\]

with `0_{a×b}` the zero block and `1_{a×b}` the all-ones (full between-part) block (forcing: GOLDEN DEF 17.0.2; claim `D0-SCENE-002` `J_scene selects K(9,11,13)`).

### Carrier invariants and honest spectrum

The forced graph has fixed finite invariants [^b01-49]:

- Vertices `|V|=33`; edges `9·11 + 9·13 + 11·13 = 359` (prime); triangles `9·11·13 = 1287`.
- **Adjacency rank = 3, nullity = 30.** The three nonzero blocks collapse `A` onto a rank-3 image; the remaining 30 directions lie in the kernel.
- Nonzero eigenvalues of `A`: `{21.837, −9.758, −12.079}` (the rank-3 spectrum; the other 30 eigenvalues are 0).

**Honesty disclaimers (do not over-claim).**

- The scene is **NOT** a Ramanujan graph: `|λ2| = 12.079 > 2√(d−1) = 9.59`. The correct spectral property is *rank 3 + spectral gap*, not the Ramanujan bound.
- The "homological index 38" is **NOT** a graph invariant: the cycle (cyclomatic) rank of `K(9,11,13)` is `359 − 33 + 1 = 327`. The number `38 = 2(2γ−1)` at `γ=10` is a *derived count*, an output of the scene arithmetic, not a property read off the graph.

**[^b01-43]** for the spectral/invariant package — the eigenvalues and rank/nullity are linear-algebra facts of the forced `A`, but no standalone `vp_*` scene-spectrum cert is registered here; the detailed Rank–Nullity and quenched-spectrum derivations are owned downstream (BOOK_03, Spectral Core of the Scene).

### Terminal-window weld: d₁₃ = 20 = φ_E(44) and m_s/m_d

The degree of every 13-shell vertex is `d13 = |V9| + |V11| = 9 + 11 = 20`. This count coincides with a group-units count, and the coincidence is the seam that forces the strange/down mass ratio [^b01-50].

- **THE-A (owner, here).** Terminal window `q_T = ABCD · V11 = 4·11 = 44`; admissible branches form the unit group `G = (ℤ/44)*` with `|G| = φ_E(44) = 20 = d13`.
- **THE-B (computed).** `G ≅ ℤ2 × ℤ2 × ℤ5`. The catalog-free (characteristic) subgroups are exactly `{1}`, the 2-torsion `T` (order **4**), the squares `F` (order **5**), and `G` (**20**); every other subgroup (three ℤ2, three ℤ10) requires choosing an instance = a catalog. The M1-admissible symmetry-class spectrum is `{1, 4, 5, 20}`, and the window factorizes `20 = 4 × 5 = |ABCD| × D_Σ` — the same 4 and 5 that built the defect address `9 = 4 + 5` return as torsion and odd part (a non-trivial internal echo). The product of all units mod 44 is `+1`: the window is globally phase-neutral, with no free residual bit.
- **LEM-D (the one declared gap).** Orientation-blindness (THE 3.11.B: flavour structure must be blind to an external ℤ2 orientation bit) excludes the T-charged class (cost 4). The cost-5 class is excluded by address-aliasing: winding 5 collides with the operational address `D_Σ = 5`, so using a role-address as a flavour winding is a scene pointer collision = hidden memory (grammar 01.11C). What remains: the trivial class (`W ∝ 1`, generation 1) and the full catalog-free class (`W ∝ 20`, generation 2). **The aliasing step is stated but not formalized — this is a soft joint of the corpus, alongside the role lists and the +2 parity.**
- **COR-E.** Hence `m_s/m_d = 20`, exact.

**[^b01-44]** — the weld chain (group structure, symmetry-class spectrum, LEM-D, m_s/m_d=20) is not yet discharged by a registered `vp_*` cert; the LEM-D aliasing gap is explicitly open. The `φ_E(44)=20=d13` count itself is certified by `05_CERTS/vp_v1141_abcd_omega8_v9_phi_capacity.py`. The empirical cross-check (lattice `m_s/m_d = 20.01 ± 0.55`, 0.03σ) and the Gatto–Sartori–Tonina Cabibbo bridge `sinθ_C = 1/√20` are downstream comparisons, not part of the forcing.

## 01.21 Hurwitz-rigid phase generator and non-resonant spatial unfolding

The normalized D0 phase generator is not an arbitrary irrational angle.  The
primitive positive-response theorem gives `p+p²=1`, hence the return branch is

```math
\alpha_{D0}=p^2=\varphi^{-2}.
```

The physical phase increment is therefore `2π/φ²`.  By the Hurwitz/continued-
fraction extremality of the `φ` class, this rotation is maximally resistant to
low-denominator rational locking.  In D0 terminology, it is the admissible phase
increment that suppresses uncontrolled metric arms in the unresolved complement.

In the active formalization this is the information-quasicrystal phase: the Lean
owner proves that the φ phase is non-periodic and packages it with the finite
return branch counts.  D0 geometry is therefore ordered but aperiodic before it
is smoothed.

This does not eliminate finite branches.  Branches appear only after a finite
readout quotient chooses a return modulus.  Thus the same chain has two layers:

```text
φ^{-2} irrational rotation  > non-resonant archive smoothing;
finite return modulus q  > residue branch geometry.
```

This closes the compatibility between macroscopic smoothness and finite branch
unfolding.

The Hurwitz extremality of the increment `\alpha_{D0}=\varphi^{-2}` is verified by
the finite certificate, which computes the continued fraction of
`\varphi^{-2}`, its convergents `p/q`, and confirms the Hurwitz ratio
`q^2|\varphi^{-2}-p/q|\to1/\sqrt5` — the maximal liminf, i.e. the slowest possible
rational capture. The non-resonance is not a softening assumption; it is the
extremal value attained.

### 01.21.1 Duality lemma `φ/M1`: the operational and the algebraic minimizer coincide [^b01-52]

The phase generator is fixed twice over, from two unrelated directions, and the
two answers are the *same* `\varphi`. This is the forcing the bare statement
`\alpha_{D0}=\varphi^{-2}` hides, and it is why the rotation cannot be retuned.

- **Algebraic side.** `\varphi` minimizes the catalog: it is the MDL/Hurwitz
  minimizer, the irrational whose continued fraction `[1;1,1,1,\dots]` stores no
  content and whose rational capture is slowest (`\liminf q^2|\varphi-p/q|=1/\sqrt5`,
  the largest possible). This is the route established as a theorem in §01.6.1a and
  cert-backed for the phase by the finite certificate.
- **Operational side.** `M1` selects `\varphi` dynamically: the requirement that a
  registration distinguish itself without an external catalog has, on the class of
  rotation numbers, the single fixed point `\varphi` (the depth-1 self-return audit
  `p+p^2=1` of §01.6, §01.6.1a). `M1` is not a numerical optimizer; it is the
  no-external-catalog law itself.

**Lemma (`D0-PHI-M1-DUALITY-001`, forcing: GOLDEN/DOSSIER VII.2).** `M1` restricted
to the class of rotation numbers has a unique fixed point, equal to `\varphi`.
Conversely, `\varphi`-rotation is the unique dynamics under which `M1` is
simultaneously satisfiable at *every* finite depth — any rational `p/q` rotation is
captured at some finite stage, becoming indistinguishable from a periodic catalog
entry, hence `\bot M1`. The two characterizations name the same object: the
algebraic minimizer (Hurwitz/MDL) is the operational fixed point (`M1`).

The "at every finite depth" clause is the load-bearing one: Hurwitz extremality is
the statement that `\varphi`'s convergents resist capture at *all* truncations,
which is exactly compatibility with the inverse limit of the carrier. The dynamical
counterpart is the **KAM last-torus** fact — the golden-rotation torus is the last to
survive perturbation precisely because its winding number is the most badly
approximable (Greene 1979; MacKay). Operationally non-captured-at-all-depths and
dynamically last-torus-standing are the same property read on the two sides of the
duality.

**`\delta_0` as the discrepancy of the two `M1`-canonical cuts.** The two sides do
not give the same unit cut, and `\delta_0` is precisely the gap between them. `M1`
admits two canonical cuts of the unit: the *symmetric* cut `1/2` (the
naming/parity-balanced cut) and the *self-consistent* cut `\varphi^{-1}` (the cut
that survives its own return audit). Their centered discrepancy is the detector
asymmetry quantum owned in §01.6,

```math
\delta_0=\frac{p_+-p_-}{2}=\varphi^{-1}-\tfrac12=\frac{\sqrt5-2}{2}=\frac1{2\varphi^3}.
```

So `\delta_0` is not an extra input: it is the *norm of the discrepancy* between the
`M1`-symmetric and the `M1`-self-consistent readings of the same unit. The cut would
be `1/2` if naming alone sufficed; it is `\varphi^{-1}` because the cut must survive
its own return; the irreducible difference is `\delta_0`.

[^b01-51]. Three of the four pieces are
established: Hurwitz/MDL minimality (PROVED, discharged by the finite
certificate), the `M1` fixed point on rotation numbers
(§01.6.1a), and the KAM last-torus closure (Greene/MacKay, external). The open
obligation is the single conjugacy statement binding the `M1` self-return audit to
the renormalization return-map of the golden foliation (Morse–Hedlund / Greene
standard, to be stated as one theorem). The metaphor is exact: the coin neither
falls (`M1`) and turns as `\varphi`.

### 01.21.2 The phase unfolding is the symbolic dynamics of the time torus [^b01-53]

The non-resonant unfolding above is not a separate construction laid over the time
layer — it *is* the time layer read symbolically. The eigen-directions of the toral
generator `T=[[0,1],[1,-1]]` have golden slopes `(\varphi^{-1},-\varphi)`, and the
Fibonacci substitution word `a\to ab,\ b\to a` agrees letter-for-letter with the
Sturmian word of slope `\varphi^{-2}` (checked to 40 symbols). Therefore the
phase unfolding of this chapter is the symbolic dynamics of the golden foliation of
the time torus: **carrier (quasicrystal) and time (automorphism) are one object**,
not two layers that happen to share a constant.

This is the same `\varphi^{-2}` increment as the phase generator, now exhibited as a
return map. It also supplies the conjugacy that §01.21.1 leaves open in dynamical
form: the rotation by `\varphi^{-2}` is the first-return map of the golden foliation
(Morse–Hedlund, standard; golden-mean shift, Vershik). The open obligation is the
formal conjugacy `\varphi^{-2}`-rotation `\cong` foliation return map, which is the
dynamical half of the duality lemma.

### 01.21.3 `φ` as a quantized index value (Jones subfactor index) [forcing-owner]

The two characterizations of §01.21.1 — `\varphi` as the Hurwitz/MDL minimizer and as
the `M1` fixed point — are joined by a third, independent both of approximation theory
and of `M1`: `\varphi` is a *quantized* value. Jones' subfactor index theorem (V. F. R.
Jones, *Index for subfactors*, Invent. Math. **72**(1), 1–25, 1983) forces the index
`[M:N]` of a type-II₁ subfactor to lie, in the interval `[1,4)`, in the discrete series
`\{4\cos^2(\pi/n) : n=3,4,5,\dots\}`. The `n=5` slot is

```math
4\cos^2(\pi/5)=\tfrac{3+\sqrt5}{2}=\varphi^2,
```

the **first** irrational ("golden") member — `n=3,4` give the integers `1,2`; `n=6`
gives `3`. It is the squared quantum dimension `d_\tau=\varphi` of the Fibonacci
category, the unique unitary modular tensor category with a single non-trivial simple
object of dimension `>1`, where `d_\tau` is forced as the positive root of the fusion
relation `x^2=x+1` (`\tau\otimes\tau=\mathbf1\oplus\tau`).

This is a forcing-**owner** edge, not a derivation inside D0: the D0-forced `\varphi`
sits exactly at the forced `n=5` slot of an external quantization, so "`\varphi` is
golden" is corroborated by a third, categorically-quantized channel. The `n=5` value is
closed exactly — `(3+\sqrt5)/2=\varphi^2=\varphi+1` (claim `D0-JONES-INDEX-PHI-001`, cert
`vp_jones_index_phi_finite.py` + Lean `D0.Claims.JonesIndexPhi`). **Honest scope:** the
quantization *obstruction* itself — that no index in the open `(1,4)` exists other than
the `4\cos^2(\pi/n)` series — is the external classical theorem (owner
`ASSUMP-JONES-INDEX`, Jones 1983), cited not re-proved (BOOK_05 §05.8.R). Together with
Hurwitz extremality (§01.21.1), the Pisot/Sturmian symbolic dynamics (§01.21.2), and the
icosian→`E_8` embedding (BOOK_02 §02.18), `\varphi` is forced through four independent
channels — the "`\varphi`-network".

### 01.21.4 `I_f = \log\varphi`: the Fibonacci-anyon route to the information rate [LEM]

The toral symbolic dynamics of §01.21.2 fixes the information rate `I_f = h_{KS} = \log\varphi`
from the automorphism side; there is a second, independent route to the *same* number from the
fusion side. The Fibonacci anyon's quantum dimension `d_\tau = \varphi` is the unique positive
root of the fusion relation `d^2 = d + 1` (`\tau\otimes\tau = \mathbf1\oplus\tau`; Nayak,
Simon, Stern, Freedman, Das Sarma, *Rev. Mod. Phys.* **80**, 1083, 2008), so the dimension of
the `n`-anyon fusion space grows as `\varphi^n` and the distinguishability gained per step is
`\log\varphi`. On the automorphism side the toral generator `T=\begin{psmallmatrix}0&1\\1&-1\end{psmallmatrix}`
has characteristic polynomial `x^2 + x - 1` (trace `-1`, det `-1`), eigenvalue of largest
magnitude `-\varphi`, hence spectral radius `|{-\varphi}| = \varphi` and `h_{KS} = \log\varphi`.
Two independent computations land on one number:

```math
I_f \;=\; \log\varphi \;=\; h_{KS} \;=\; \log|\lambda_{\max}(T)|.
```

This is closed at the **algebraic** level (claim `D0-FIBONACCI-IF-FORCING-001`, cert
`vp_fibonacci_if_bridge.py` + Lean `D0.Claims.FibonacciIfBridge`): `\varphi^2 = \varphi + 1`
(fusion), `(-\varphi)^2 + (-\varphi) - 1 = 0` (toral), `|{-\varphi}| = \varphi`. Note the two
quadratics differ by a sign — the fusion root solves `x^2 - x - 1`, the toral root solves
`x^2 + x - 1`; `\varphi` and `-\varphi` are *different roots sharing the magnitude* `\varphi`,
not the same root. **Honest scope (status LEM, not THE):** both routes give `\log\varphi`, but
the isomorphism between the Fibonacci-category state growth (`\sim\varphi^n`) and the symbolic
dynamics of `T` (`h_{KS}=\log\varphi`) is **not constructed** here. In D0, distinguishability
*is* information, so "growth of distinguishable states" and "rate of information production"
*should* be one object — but that map must be exhibited, not postulated. Until it is, this is a
lemma with a named gap (the categorical↔toral isomorphism), corroborating but not forcing
`I_f`. This is the deep-research mechanism filter applied honestly: a coincident `\log\varphi`
from two sides is a strong lemma, not a theorem, until the bridge map is written. It promotes
the GW horizontal-hum target (BOOK_09): `I_f` is not a bare number but an information-dimension
of growth — pending the isomorphism, a named LEM.
## 01.22 Forced return windows and non-post-hoc phase unfolding

The phase-unfolding windows used by D0 are not chosen by searching for rational approximants to a circle.  They are forced by terminal capacity.

Let the direct/return dyad have cardinality `D2=2`.  Then the terminal role square has cardinality

```math
|four terminal roles A,B,C,D|=D_2^2=4,
```

the oriented terminal set is

```math
|\Omega_8|=2|four terminal roles A,B,C,D|=8,
```

and the pointed witness shell is

```math
V_9=|\Omega_8|+1=9.
```

The first dyadic extension and terminal-role extension are

```math
V_{11}=V_9+D_2=11,
\qquad
V_{13}=V_9+|four terminal roles A,B,C,D|=13.
```

The first terminal phase-return modulus must saturate all unsiged terminal roles over the first moving dyadic shell.  Therefore

```math
q_T=\operatorname{lcm}(|four terminal roles A,B,C,D|,V_{11})=4\cdot 11=44.
```

The turn count is fixed by terminal role closure plus the three incidence directions of the scene:

```math
m_T=|four terminal roles A,B,C,D|+\operatorname{rank}(A_K)=4+3=7.
```

Thus `44/7` is checked as a phase near-return only after `44` and `7` have been capacity-derived.  Its admissible branch count is

```math
\varphi_{Euler}(44)=20=d_{13}.
```

The second return window is similarly forced after the terminal shell exists.  Define the pointed terminal alphabet

```math
B=|four terminal roles A,B,C,D|+1=5
```

and the bilateral scene line

```math
L=2|V|+B=2\cdot 33+5=71.
```

A full oriented return must include the two-sided orientation, the pointed terminal alphabet and the full bilateral scene line:

```math
q_{EW}=2BL=2\cdot 5\cdot 71=710.
```

The associated turn count is

```math
m_{EW}=B d_{13}+V_{13}=5\cdot 20+13=113.
```

Therefore the second return ratio `710/113` is also not selected by approximation; it is checked after the capacity derivation.  Its admissible branch count is

```math
\varphi_{Euler}(710)=280,
\qquad
280/|\Omega_8|=35.
```

This gives the electroweak radial depth as the per-oriented-role branch depth of the second forced return window.

### The address step is forced to `+2` — the orientation-class no-sign-catalog argument (forcing: GOLDEN THE 3.11.B / COR 3.13.B(1), BOOK-I-ARCHITECTURE)

The capacity construction above lands the scene on the spectrum `9, 11, 13` through the `Ω₈`-plus-basepoint / dyad `D₂` / terminal-role-square route.  That route fixes the *cardinalities*.  A second, independent forcing fixes the *step* between successive addresses: the address ladder is forced to advance by `+2`, never `+1`, because a `+1` step would demand an external orientation bit — a sign catalog — which is `⊥M1`.

The argument is a reduction to holonomy parity.  In the discrete CORE world the powers `φ^n` are approximated by the integer Lucas numbers `L_n`, and the approximation defect carries an exact `Z₂`-orientation class:

```math
L_n=\varphi^n+\psi^n,\quad \psi=-\varphi^{-1}
\ \Longrightarrow\
\epsilon_n:=\varphi^n-L_n=-\psi^n=(-1)^{n+1}\varphi^{-n}.
```

So the sign of the defect alternates with `n`: at `n=5` the holonomy parity is `+`, at `n=6` it is `−`.  Now attempt a unit junction step `5 → 6`.  The orientation/torsion class flips, and to splice the two layers across that flip one must supply an external orientation bit (an element of `Z₂`) that is **not** contained in the address itself.  Importing that bit is exactly importing an external significance/sign catalog, and is forbidden by M1 (DEF-0.2.2 forcing-by-contradiction).  The step `5 → 7` preserves the orientation class, so the splice closes with no exogenous parameter.  Hence the minimal admissible junction step is `+2`, and the address ladder is

```math
\underbrace{4+5=9}_{\text{defect}}\ \xrightarrow{+2}\ \underbrace{11}_{\text{torus-memory}}\ \xrightarrow{+2}\ \underbrace{13}_{\text{shell}} .
```

Any other step requires an external splice-control parameter, hence `⊥M1`.  This is the same `9, 11, 13` the capacity route produces, so the two derivations are mutually reinforcing: capacity sets the cardinalities, orientation-parity sets the increment, and neither leans on the other.  In topological language the `+2` step is precisely the condition that the heat-trace time-splice be *orientable* — a cylinder, not a twist — so no global `Z₂`-direction convention is needed to run the evolution [^b01-54].  Status: CORE-FORCING (forcing: GOLDEN THE 3.11.B and COR 3.13.B(1)–(2), BOOK-I-ARCHITECTURE; ⊥-proof via `(-1)^n` orientation parity, no sign catalog).

### Cycle normalization `ν* = 1/9` and the `40°` phase step (forcing: GOLDEN THE 3.13.A / COR 3.13.B(3), BOOK-I-ARCHITECTURE)

The return windows above are read against a phase circle, and the discretization of that circle is itself forced — it is not a free choice of resolution.  In the base zone the address count is `D = 9` (the defect shell `V_9`), giving `9` distinguishable address positions by definition of the address.  The internal addressor — the canonical scene cycle `γ*` — must visit those positions.  Two failure modes bracket the step count `N`:

- `N < 9`: at least two address positions are glued onto one cycle step, so distinct addresses become indistinguishable.  Loss of distinguishability is `⊥M1`.
- `N > 9`: the cycle has "empty" steps that correspond to no address.  To tell an empty step from a significant one the cycle would need an external **catalog of significance**, which is `⊥M1`.

The single survivor is `N = D = 9`.  Therefore the cycle normalization, as the per-address fraction of the cycle, is

```math
\nu^*=\frac{1}{\mathfrak{D}}=\frac{1}{9},
```

and the BRIDGE angle-packing of that fraction is the phase increment

```math
v^*:=\frac{2\pi}{9}=\frac{360^\circ}{9}=40^\circ .
```

The `40°` step is a *representation* of the phase fraction, not a new CORE object: it adds no axiom, only writes `ν*` as an angle.  This `9`-step quantization is what makes the return ratios `44/7` and `710/113` well-posed *near-returns of a fixed discrete cycle* rather than approximants chosen post hoc to a continuum circle.  Status: CORE-FORCING (forcing: GOLDEN THE 3.13.A and COR 3.13.B(3), BOOK-I-ARCHITECTURE; ⊥-proof, glue-vs-catalog fork; `N<9` ⇒ address collapse, `N>9` ⇒ significance catalog).

Taken together the three forcings close the non-post-hoc claim of this section: capacity fixes the address cardinalities `9, 11, 13`, the `(-1)^n` orientation parity fixes the `+2` step that connects them, and the glue-vs-catalog fork fixes the `9`-step cycle (`ν*=1/9`, `40°`) against which every return window is checked — all three derived before any ratio is evaluated, none of them a fitted parameter.
## 01.23 Final finite-support closures

The following finite-support structures and operators close the foundation of the D0 vacuum:

### Lorentz carrier from terminal role capacity
The terminal role capacity `four terminal roles A,B,C,D = D₂ × D₂` fixes the minimal external quadratic carrier:
$$\eta = \operatorname{diag}(+1,-1,-1,-1).$$
- **Role in the chain**: It is the finite carrier forced by the terminal role obligations of the detector.
- **Guardrail**: A Lorentz-facing bridge is admissible only after a finite Clifford realization satisfies $\{\gamma^\mu,\gamma^\nu\} = 2\eta^{\mu\nu}I$. It does not postulate a background spacetime.

### Projective closure of the two-branch defect plane
The active branch, return branch, and their distinguishability gap form the three nonzero rays of the two-dimensional branch-defect plane over $\mathbb{F}_2$.
- **Lean Owner**: `D0.Spectrum.BranchDefectProjectiveGeneration` (`BranchDefectProjectiveGeneration`).
- **Guardrail**: This is the algebraic origin of the core generation index; it is not a graph-spectrum claim and not a mass formula.

### Topological tick-gauge and archive floor projection
The archive tick parameter is fixed as a topological gauge convention: $\eta = 1$.
- **Lean Owners**: `D0.Geometry.ArchiveTickGaugeFixing` (`eta_absorbs_into_response`), `D0.Probability.ArchiveFloorWaterFilling` (`waterFill_preserves_floor`, `waterFill_mass_if_root`), `D0.Cosmology.ArchiveHomogeneousState` (`canonical_archive_density_is_uniform`).
- **Guardrail**: Changing $\eta$ is not a physical readout. Ad hoc localization coefficients do not define the D0 core density and cannot mutate the topological tick-gauge.

### Born readout as finite effect-frame theorem
A finite detector supplies effects, a detector state, raw responses, coarse-grained responses, and product responses before probability is reported.
- **Lean Owner**: `D0.Core.BornFiniteEffects` (`finite_effect_born_readout_unique`, `finite_coarse_born_readout_unique`, `finite_tensor_born_readout_unique`, `finite_power_readout_no_alternative`).
- **Guardrail**: Probability is not a free normalization convention or a downstream passport weight. Under fixed finite response, every admissible readout collapses to the same Born weight.

### Born 4.0 composition to norm-square
The phase-blind quadratic response of a finite phase-quadrature atom.
- **Lean Owner**: `D0.Core.BornQuadraticOrigin` (`phase_blind_quadratic_response_is_norm_sq_scaled`, `unit_phase_blind_quadratic_response_is_norm_sq`).
- **Certificate**: `05_CERTS/vp_born_quadratic_origin.py` (`PASS_BORN_QUADRATIC_ORIGIN`).
- **Guardrail**: Parallelogram quadratic response and quarter-turn phase blindness select the unit norm-square response before Born normalization.

### Torus shell overlap response (Torus Shell Overlap And Born Readout)
The generation/flavour overlap is a finite phase-blind quadratic response: $O_{ij} = |\langle\text{phase}_i | \text{mixed}_j\rangle|^2$.
- **Lean Owner**: `D0.Matter.GenerationOverlapResponseOrigin` (`torus_shell_noncommutativity_forces_nonpermutation_overlap_source`).
- **Guardrail**: The torus supplies the finite shell carrier and noncommuting selector source; Born readout supplies the normalized quadratic response.

### Fixed detector time ladder
The detector is fixed; the division ladder evolves by $T^n$:
$$\psi_n = T^n \psi_0,\qquad R_n = D^\dagger D(\psi_n),\qquad D_{n+1} = D_n = D.$$
The detector is fixed; the division ladder evolves by T^n.
Readout is D^dagger D applied to the T^n-state.
- **Lean Owner**: `D0.Core.FixedDetectorTimeLadder`.
- **Guardrail**: The detector itself is not a hidden dynamical parameter and cannot be retuned between ticks.

### Cut-and-project quasicrystal operator origin
Aperiodic geometry generated by $\varphi^{-2}$ irrational phase return:
- **Lean Owner**: `D0.Physics.QuasicrystalPhenomenology` (`quasicrystal_phenomenology_operator_origin`, `D0PhiCutProject`, cut-and-project quasicrystal geometry).
- **Certificate**: `05_CERTS/vp_quasicrystal_phenomenology_operator_origin.py` (`PASS_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN`).
- **Guardrail**: Generational inflation, archive phason strain, chiral window offset, phason-flip drag, and fractional charge weights are read from a common cut-and-project vacuum support.

## 01.24 Mobius-Witness topological halting

The signed terminal role cycle is

\[
\Omega_8=ABCD\times\{+,-\}.
\]

The witness/basepoint \(\omega_0\) gives the first addressable graph-birth shell

\[
V_9=\Omega_8\sqcup\{\omega_0\}.
\]

Continuous circulation inside \(\Omega_8\) accumulates the logarithmic trace gradient. The finite event occurs when the circulation closes against \(\omega_0\); this is the terminal halt quotient. The archive sector is not external emptiness. It is the traced complement inside the same finite support, whose self-organization supplies the topological memory layer used downstream by Core-13, tiling hulls, phason strain and boundary capacity.

**Witness Halt Proof (corrected orbit average, Researcher A integration).**
Because the trace gradient has traversed the full signed role cycle before halt, the emitted archive trace is an orbit-averaged shell emission over the group \(G_8\) of symmetries of \(\Omega_8\):

\[
E_\Omega = \frac{1}{|G_8|} \sum_{g \in G_8} P_g F_N P_g^\dagger.
\]

This average is invariant, but it is **not** a scalar multiple of the identity unless irreducibility of the representation on the trace space is separately proved.


## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b01-1]: forcing: GOLDEN §1.1.0, THE 1.1.0b, BOOK-I-ARCHITECTURE
[^b01-2]: forcing: GOLDEN §1.1.0a, BOOK-I-ARCHITECTURE; ⊥-proof
[^b01-3]: forcing: GOLDEN LEM 1.1.0a.1, BOOK-I-ARCHITECTURE
[^b01-4]: forcing: GOLDEN THE 1.1.0b, BOOK-I-ARCHITECTURE; ⊥-proof, per-component
[^b01-5]: forcing: GOLDEN DEF 1.1.1, BOOK-I-ARCHITECTURE
[^b01-6]: forcing: GOLDEN LEM 1.1.1a, BOOK-I-ARCHITECTURE
[^b01-7]: forcing: GOLDEN §1.1.3, BOOK-I-ARCHITECTURE
[^b01-8]: forcing: GOLDEN LEM 1.1.5.2, BOOK-I-ARCHITECTURE; ⊥-fork
[^b01-9]: forcing: GOLDEN LEM 1.1.6.4, BOOK-I-ARCHITECTURE
[^b01-10]: forcing: GOLDEN LEM 1.1.7.2, BOOK-I-ARCHITECTURE; ⊥-proof
[^b01-11]: forcing: GOLDEN COR 1.1.7.2.B + DEF 1.1.7.E, BOOK-I-ARCHITECTURE
[^b01-12]: forcing: GOLDEN THE 1.1.11.B, BOOK-I-ARCHITECTURE; ⊥-dichotomy
[^b01-13]: forcing: GOLDEN §1.1.11B', BOOK-I-ARCHITECTURE
[^b01-14]: forcing: GOLDEN THE 2.1.3
[^b01-15]: no new parameter; forcing: GOLDEN LEM 2.1.3c
[^b01-16]: forcing: GOLDEN COR 2.1.3d
[^b01-17]: forcing: GOLDEN §2.2
[^b01-18]: forcing: GOLDEN THE 2.2.1
[^b01-19]: forcing: GOLDEN LEM 2.2.2b
[^b01-20]: forcing: GOLDEN LEM 2.2.3
[^b01-21]: open obligation — cert obligation open
[^b01-22]: forcing: GOLDEN THE II.4.APPX5.14.3, BOOK-II-MECHANISM; M1 / DEF-0.2.2 forcing-by-contradiction
[^b01-23]: forcing: GOLDEN LEM 2.2.2b
[^b01-24]: forcing: GOLDEN THE 2.2.1
[^b01-25]: forcing: GOLDEN LEM 2.2.2b
[^b01-26]: forcing: GOLDEN LEM 2.2.3
[^b01-27]: forcing: GOLDEN/DOSSIER I.1, two THE derivations
[^b01-28]: forcing: GOLDEN/v17 §01.5
[^b01-29]: forcing: GOLDEN/PHILOSOPHY §3
[^b01-30]: forcing: GOLDEN THE 17; cert `vp_q8_dedekind_minimality.py`
[^b01-31]: exact, cert `vp_q8_dedekind_minimality.py`; forcing: GOLDEN THE 18
[^b01-32]: forcing: GOLDEN COR 19; algebra carried by cert `vp_q8_dedekind_minimality.py`
[^b01-33]: open obligation — fixed-point + KAM legs proved; cert obligation open for the joint statement
[^b01-34]: open obligation — three of four legs proved — Hurwitz in Lean, the fixed point, KAM; cert obligation open for the remaining leg
[^b01-35]: forcing: GOLDEN D0-PHILOSOPHY-AND-METHOD §5
[^b01-36]: forcing: GOLDEN D0-PHILOSOPHY-AND-METHOD §5; THE-target
[^b01-37]: forcing: GOLDEN D0-PHILOSOPHY-AND-METHOD §5
[^b01-38]: forcing: GOLDEN/v17 §01.21; cf. 01.21
[^b01-39]: forcing: GOLDEN THE 37, D0-CKM-INTERFACE-ITERATION-REPORT §37
[^b01-40]: forcing: GOLDEN THE 37; M1 / DEF-0.2.2 forcing-by-contradiction — a separate space-vs-time catalog would be an external label, M1-forbidden
[^b01-41]: forcing: GOLDEN THE 36, ITERATION-REPORT §36; cert `vp_xi5_torus_defect.py` — exact ℤ[φ] arithmetic, zero float
[^b01-42]: open obligation — cert obligation open
[^b01-43]: open obligation — cert obligation open
[^b01-44]: open obligation — cert obligation open
[^b01-45]: forcing: GOLDEN THE I.3 / claim `D0-Q8-DEDEKIND-MINIMALITY-001`
[^b01-46]: forcing: GOLDEN THE I.3; claim `D0-SCENE-001`
[^b01-47]: forcing: GOLDEN THE 17.0.1.A "Uniqueness of vacuum connectivity without a catalog"
[^b01-48]: forcing: GOLDEN REM 17.0.1.A.1
[^b01-49]: forcing: transfer D0-THEORY-DOSSIER I.2
[^b01-50]: forcing: transfer D0-CKM-INTERFACE THE-A…COR-E; owner BOOK_01
[^b01-51]: open obligation — cert obligation open
[^b01-52]: forcing: GOLDEN/DOSSIER VII.2
[^b01-53]: forcing: GOLDEN/DOSSIER VI.3
[^b01-54]: forcing: GOLDEN REM 3.11.B.T, BOOK-I-ARCHITECTURE
