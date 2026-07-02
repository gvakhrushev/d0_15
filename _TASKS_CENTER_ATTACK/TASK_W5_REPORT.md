# TASK W5 — Annotated bibliography: external theorem-owners for T1 and the time↔flavor link

**Scope.** Web literature sweep (WebSearch/WebFetch). Primary sources only, arXiv IDs where
available. For each item: full citation, exact-or-faithful theorem statement, hypotheses, and one
mapping line to a D0 claim/book section. This is an *owner* catalogue: D0 discipline (BOOK_00
§00.8 / §00.9) explicitly allows citing external owners for known math — nothing here is
"confirmed/derived" on D0's behalf; these are candidate owners to be attached, not promotions.

**Convention.** In the statements below: `A` = adjacency matrix, `D` = diagonal degree matrix,
`Q = D − I`, `B` (a.k.a. `H`, `W`, `T`) = the Hashimoto / non-backtracking edge-adjacency matrix
indexed by the `2|E|` directed edges, `n = |V|`, `m = |E|`, rank `r = m − n + 1`. On the D0 carrier
K(9,11,13): `n = 33`, `m = |E| = 359`, `2m = 718`, `r = 359 − 33 + 1 = 327`, and `m − n = 326`.

---

## THREAD A — Non-backtracking / Ihara zeta (feeds T1)

D0 need (from README): promote the non-backtracking (Hashimoto) history family to the CANONICAL
scene refinement rule, with the Ihara–Bass identity as the Ξ-intertwiner between the 718-dim edge
transfer and the 33-dim scene data (A, D). Machine-verified numeric facts already in hand:
`det(I − uB) = (1 − u²)^326 · det(I − uA + u²(D − I))` at u = 1/3, 1/7, −2/5; spec(B) has Perron
≈ 20.8335 and 653 unit-modulus eigenvalues.

### A1 — Hashimoto (1989) & Bass (1992): the Ihara–Bass determinant formula (irregular graphs)

**Citations.**
- K. Hashimoto, "Zeta functions of finite graphs and representations of p-adic groups," in
  *Automorphic Forms and Geometry of Arithmetic Varieties*, Adv. Stud. Pure Math. **15** (1989),
  211–280. (First determinant formula / edge-matrix `B` for general graphs.)
- H. Bass, "The Ihara–Selberg zeta function of a tree lattice," *Internat. J. Math.* **3** (1992),
  no. 6, 717–797. (The three-term vertex-space determinant identity.)
- Y. Ihara, "On discrete subgroups of the two by two projective linear group over p-adic fields,"
  *J. Math. Soc. Japan* **18** (1966), 219–235 (original, regular case only).

**Exact statement (Ihara–Bass, general finite graph).** For a finite graph `X` with adjacency
matrix `A`, degree matrix `D`, `n = |V|`, `m = |E|`,

  `Z_X(u)^{-1} = (1 − u²)^{m − n} · det(I − uA + u²(D − I))`,

and equivalently in edge space `Z_X(u)^{-1} = det(I − uB)`, where `B` is the `2m × 2m` Hashimoto
edge-adjacency matrix `B_{(e,f)} = 1` iff `ter(e) = org(f)` and `f ≠ e⁻¹` (i.e. non-backtracking),
`0` otherwise. Hence the master intertwiner

  `det(I − uB) = (1 − u²)^{m − n} · det(I − uA + u²(D − I))`.

**Hypotheses.** The identity holds for any finite graph (Bass proves it via the two-term block
factorization of `(I − uB)` against the `n`-space; no regularity is needed — the `D` in the middle
factor carries the irregularity). Standard normalizations in Terras / Kotani–Sunada add: `X`
**connected**, **no degree-1 vertices** (minimum degree `≥ 2`, so the zeta has no trivial tails),
and one usually excludes the trivial-cycle degeneracies by taking `X` with rank `r = m − n + 1 ≥ 1`
(i.e. not a tree/forest). The determinant identity itself is a polynomial identity valid without the
min-degree-2 assumption; the min-degree-2 assumption is what makes the *zeta* (the Euler product over
primes) well-behaved and the `(1 − u²)` factor non-dividing (see A5).

**maps to D0 claim/step:** T1 (README lines 8–9); the machine-verified identity
`det(I − uB) = (1 − u²)^326 · det(I − uA + u²(D − I))` (README line 16). This is the *named owner* of
the Ξ-intertwiner row. On K(9,11,13) the exponent `m − n = 326` matches the verified `(1−u²)^326`
exactly.

---

### A2 — Kotani–Sunada (2000): spectral structure of B for irregular graphs

**Citation.** M. Kotani, T. Sunada, "Zeta functions of finite graphs," *J. Math. Sci. Univ. Tokyo*
**7** (2000), 7–25.

**Exact statement (poles / Perron / unit-circle band).** Let `X` be a finite connected graph that
is not a cycle ("non-circuit"), with minimum degree `d_m` and maximum degree `d_M` (`d_m ≥ 2`). Let
`α` be the Perron–Frobenius eigenvalue of `B` (equivalently `α = 1/R` where `R` is the radius of
convergence of `Z_X`). Then:

1. `d_m − 1 ≤ α ≤ d_M − 1`, and `u = α^{-1}` is a **simple** pole of `Z_X(u)` (Perron value simple);
2. every pole `u` of `Z_X` satisfies `α^{-1} ≤ |u| ≤ 1`;
3. every pole `u` on the "imaginary/Ramanujan band" satisfies
   `(d_M − 1)^{-1/2} ≤ |u| ≤ (d_m − 1)^{-1/2}`.

Equivalently for the eigenvalues of `B`: the spectral radius is `α ∈ [d_m − 1, d_M − 1]`, simple;
the non-trivial eigenvalues live in the annulus `1 ≤ |λ| ≤ α`, and the "RH band" eigenvalues have
modulus in `[(d_m − 1)^{1/2}, (d_M − 1)^{1/2}]`. Kotani–Sunada also record the trivial eigenvalues
`±1` (see A5) and give the reciprocity/functional-equation structure.

**Hypotheses.** Finite, connected, `d_m ≥ 2`, not a single cycle. (The two-sided degree bounds are
what make this the correct owner for an *irregular* carrier — they degenerate to the exact Ramanujan
value only when `d_m = d_M`.)

**maps to D0 claim/step:** T1 spectral audit — owns the statement that spec(B) has a simple Perron
value bounded by the degree extremes and a structured unit-modulus band. On K(9,11,13) the verified
Perron ≈ 20.8335 and the 653 unit-modulus eigenvalues (README lines 17–18) are the objects
Kotani–Sunada bound: with the vacuum cubic giving `A`-spectral radius ≈ 21.837 and the `B`-Perron
≈ 20.8335, an owner-row can cite K–S for "Perron simple, degree-bounded" rather than re-deriving it.
**Mismatch flag:** K–S bounds are stated for connected graphs; the K(9,11,13) carrier must be
connected with `d_m ≥ 2` for clauses (1)–(3) to apply verbatim (see Risks).

---

### A3 — Angel–Friedman–Hoory (2015): NB spectrum of the universal cover

**Citation.** O. Angel, J. Friedman, S. Hoory, "The non-backtracking spectrum of the universal cover
of a graph," *Trans. Amer. Math. Soc.* **367** (2015), no. 6, 4287–4318. arXiv:0712.0192.

**Exact statement (faithful).** Let `H` be the universal cover (a tree) of a finite graph, and `B`
its non-backtracking operator. Then the spectral radius of `B` equals `√(gr)`, where `gr` is the
growth rate of the tree. Crucially: when the base graph is **not regular**, the spectrum of `B` on
the cover **can have positive (2-D) measure in the complex plane**, unlike the regular case (where it
is a union of circles/isolated arcs). Outside the spectrum, the associated Green function has
"periodic decay ratios" (a computable "ratio system" characterizing spectral membership).

**Hypotheses.** `H` = tree covering a finite graph; the positive-measure phenomenon is precisely the
*irregular* case. No min-degree-2 needed for the growth-rate identity, but the interesting spectral
geometry appears once degrees vary.

**maps to D0 claim/step:** T1 canonicity/uniqueness thread — this is the owner for "the NB operator's
spectrum is genuinely richer than `A`'s for irregular carriers, so the NB refinement is not
reducible to the adjacency walk." It supports (does not prove) the claim that on an irregular scene
like K(9,11,13) the NB history family carries strictly more information than `A`.
**Note:** this is a statement about the *infinite cover*, not the finite `B`; use it as motivation
for canonicity, not as the finite-spectrum owner (that is A2).

---

### A4 — Bordenave–Lelarge–Massoulié (2015+): non-backtracking spectral redemption

**Citation.** C. Bordenave, M. Lelarge, L. Massoulié, "Non-backtracking spectrum of random graphs:
community detection and non-regular Ramanujan graphs," *Ann. Probab.* **46** (2018), no. 1, 1–71;
FOCS 2015. arXiv:1501.06087.

**Exact statement (faithful, Theorems 3–4).** In the sparse regime (edges ∝ vertices, bounded mean
degree `α > 1`):

- **Erdős–Rényi `G(n, α/n)`:** the largest eigenvalue of `B` satisfies `λ₁(B) = α + o(1)`; **all
  remaining eigenvalues** satisfy `|λᵢ(B)| ≤ √α + o(1)`. I.e. one informative eigenvalue detaches at
  the mean degree; the rest are confined to the disk of radius `√α = √(Perron)`.
- **Stochastic Block Model (r communities, mean-progeny matrix M):** `λ_k(B) = μ_k + o(1)` for the
  `k` with `μ_k² > α` (the informative, community-carrying eigenvalues, `μ_k` = eigenvalues of `M`),
  while for all other `k`, `|λ_k(B)| ≤ √α + o(1)`. Community detection succeeds via the leading
  eigenvectors exactly above the Kesten–Stigum threshold `μ₂² > α` — confirming the "spectral
  redemption" conjecture where the adjacency matrix `A` fails (its spectrum is swamped by
  high-degree vertices).

**Hypotheses.** Sparse random graphs, fixed mean degree `α > 1`; asymptotic (`n → ∞`) statements.
The clean separation "bulk ≤ √(Perron), informative eigenvalues outside" is the structural content.

**maps to D0 claim/step:** T1 canonicity — the sharpest *quantitative* owner for "why the NB operator
is the right walk operator": its bulk sits at `√(Perron)` and only structurally-meaningful modes
detach, whereas `A` does not separate. Deterministic analogue on K(9,11,13): the verified `B`-Perron
≈ 20.8335 with the next eigenvalues ≈ −10.11, −6.15, ±i√23 (README line 18) is exactly the
"one Perron mode + detached informative modes above the `√(Perron) ≈ 4.56` scale" picture.
**Mismatch flag:** BLM is a *random-graph asymptotic* theorem; K(9,11,13) is a single deterministic
graph, so BLM owns the *conceptual* separation principle, not a literal bound (use A2 for the
deterministic bound).

---

### A5 — Trivial ±1 eigenvalues of B (multiplicity `m − n`) and the `(1 − u²)` factor

**Citations.**
- Bass (1992) as above (the `(1 − u²)^{m−n}` factor originates here).
- Terras, *Zeta Functions of Graphs: A Stroll through the Garden*, Cambridge Studies in Adv. Math.
  **128**, CUP (2010) — Prop. on the `(1 − u²)` factor.
- Y. Cooper, "Properties determined by the Ihara zeta function of a graph," *Electron. J. Combin.*
  **16** (2009), #R84 (records: for a connected non-bipartite graph with `d_m ≥ 2`, `(1 − u²)` does
  **not** divide `det(I − uA + u²Q)`).

**Exact statement.** The eigenvalue `+1` and (for non-bipartite `X`) `−1` occur in spec(B) as
"trivial" eigenvalues with combined extra multiplicity `m − n = |E| − |V|`, arising from the
`(1 − u²)^{m − n}` prefactor; the "genuine" NB eigenvalues are the roots of
`det(I − uA + u²(D − I)) = 0` (a quadratic-eigenvalue / `2n × 2n` companion problem). For a connected
non-bipartite graph with minimum degree `≥ 2`, `(1 − u²)` does not divide the three-term
determinant, so the trivial and non-trivial spectra are cleanly separated.

**Hypotheses.** Finite connected graph; non-dividing clause needs non-bipartite + `d_m ≥ 2`.

**maps to D0 claim/step:** T1 spectral bookkeeping — owns "the 653 unit-modulus eigenvalues" census
(README line 18) and the exponent `326 = m − n` in the verified identity. On K(9,11,13),
`m − n = 326`; the `(1 − u²)^326` factor contributes `326` copies of `+1` and (if non-bipartite)
`326` of `−1` toward the unit-modulus count — an owner-row can pin part of the 653 unit-modulus
eigenvalues to this trivial family and leave the remainder to the genuine ±i√23 / band modes.

---

### A6 — Watanabe–Fukumizu: weighted/typed graph zeta; the CONCEPTUAL owner of the typed return-channel

**Citations.**
- Y. Watanabe, K. Fukumizu, "Graph Zeta Function in the Bethe Free Energy and Loopy Belief
  Propagation," *NIPS 22* (2009). arXiv:1002.3307.
- Y. Watanabe, K. Fukumizu, "Loopy Belief Propagation, Bethe Free Energy and Graph Zeta Function,"
  (expanded) arXiv:1103.0605.

**Exact statement (faithful).** Define the *edge zeta function* with **matrix/typed weights**: to each
directed-edge transition `e' → e` (with `t(e') = s(e)` and `t(e') ≠ t(e)`, i.e. **non-backtracking**)
assign a matrix weight `u_{e'→e}`; then `ζ_H(u) = ∏_{p ∈ P_H} det(I − π(p))^{-1}` over prime cycles
`p`, `π(p)` = product of the weights around `p`. Their results:

- **Theorem 6 (weighted Ihara–Bass):** `ζ_G(u)^{-1} = det(I − M(u))` where `M(u)` is the weighted
  edge (directed-transition) operator — the weighted/typed generalization of the Hashimoto matrix.
- **Bethe-zeta formula (their Thm ~11):** the Hessian of the Bethe free energy equals the reciprocal
  of the edge zeta up to a positive factor: `det(Hessian of F_Bethe) = (positive) · ζ_G(u)^{-1}`,
  which they use to characterize positive-definiteness / local stability of loopy-BP fixed points.

**On the "typed return channel."** Honest read: in Watanabe–Fukumizu the immediate backtrack
`e followed by e⁻¹` is **excluded structurally** by the non-backtracking constraint `t(e') ≠ t(e)`;
it is **not** carried as a separate typed channel. So this is the correct owner for the *weighted/
typed non-backtracking operator* and the master weighted-Bass identity, but it does **not**
independently own "immediate backtracks as a distinct typed p²-return channel." The `u²(D − I)`
middle term of Bass is the algebraic residue of the backtrack degrees of freedom; the cleanest
external owner for treating that term as a *channel* is the Bass factorization itself (A1) plus the
deformed-Laplacian reading `L(u) = (1 − u²)I + u²D − uA` (Watanabe/Storm/Bass), where `u²D` is the
degree-weighted return term.

**Hypotheses.** Finite graph; weights per directed transition; the Bethe-zeta identity holds for the
multinomial/Gaussian graphical-model class they treat.

**maps to D0 claim/step:** T1's typed `p²`-return channel (README line 27 / brief Thread A item 4).
Watanabe–Fukumizu is the owner of the **weighted/typed** Ihara–Bass and of the concrete role of the
`u²`-degree term; but the depth-2 identity `Σd² − Σd(d−1) = 2|E|` (README) has **no dedicated
external owner treating backtracks as a separate channel** — the literature folds backtracks into the
Bass `u²(D − I)` correction rather than typing them. **Record this as a partial null** (see Risks).

---

## THREAD B — Modular A₅ / golden-ratio flavor (feeds D0-MODULAR-TIME-FLAVOR-001, MECH-LIMIT)

D0 need: the corpus proves flavor `A₅ ≅ PSL(2,5)` (icosian route) and the toral time generator as a
golden hyperbolic element of GL(2,ℤ), and flags the full time↔flavor identification as its named open
gap (BOOK_06 §06.30a). This thread catalogues the modular-flavor owner (B1–B3) and tests whether the
specific time↔flavor bridge already exists (B4).

### B1 — Feruglio (2017): modular-invariance flavor paradigm

**Citation.** F. Feruglio, "Are neutrino masses modular forms?", DFPD-2017/TH/09; in *From My Vast
Repertoire… Guido Altarelli's Legacy* (World Scientific, 2019), 227–266. arXiv:1706.08749.

**Exact statement (faithful, key equations).**
- `SL(2,ℤ)` generators `S = ((0,1),(−1,0))`, `T = ((1,1),(0,1))`, acting on the modulus by
  `S: τ → −1/τ`, `T: τ → τ + 1`, with relations `S² = 1`, `(ST)³ = 1`.
- Principal congruence subgroup `Γ(N) = { γ ∈ SL(2,ℤ) : γ ≡ I (mod N) }`; the **finite modular
  group** `Γ_N ≡ Γ̄ / Γ̄(N)`, with the small-level isomorphisms
  `Γ₂ ≅ S₃`, `Γ₃ ≅ A₄`, `Γ₄ ≅ S₄`, **`Γ₅ ≅ A₅`** (`|A₅| = 60`).
- A chiral supermultiplet transforms with modular weight `−k_I` and unitary rep `ρ^(I)` of `Γ_N`:
  `φ^(I) → (cτ + d)^{−k_I} ρ^(I)(γ) φ^(I)`.
- Yukawa couplings must be **modular forms** of weight `k_Y = k_{I₁} + … + k_{Iₙ}` and level `N`,
  transforming as `Y(γτ) = (cτ + d)^{k_Y} ρ(γ) Y(τ)`, with `ρ × ρ^{I₁} × … × ρ^{Iₙ} ⊃ 1`.

**Hypotheses.** N = 1 SUSY, exact modular invariance; flavor structure fixed by the single modulus
VEV `⟨τ⟩` plus modular-weight assignments; the finite group `Γ_N` acts on generation indices.

**maps to D0 claim/step:** D0-MODULAR-TIME-FLAVOR-001 / BOOK_06 §06.30a — Feruglio is the named owner
of the paradigm "finite modular group `Γ_N` from `SL(2,ℤ)/Γ(N)` acts as flavor symmetry," and
supplies the **exact `Γ₅ ≅ A₅` identification** that D0's icosian route also reaches. It owns the
flavor side of the bridge; it does **not** identify `τ`-modular dynamics with a *time* generator
(see B4).

---

### B2 — Golden-ratio mixing from A₅ (Everett–Stuart; Ding–Everett–Stuart; Feruglio et al.)

**Citations.**
- L. L. Everett, A. J. Stuart, "Icosahedral (A₅) family symmetry and the golden ratio prediction for
  solar neutrino mixing," *Phys. Rev. D* **79** (2009) 085005. arXiv:0812.1057.
- G.-J. Ding, L. L. Everett, A. J. Stuart, "Golden ratio neutrino mixing and A₅ flavor symmetry,"
  *Nucl. Phys. B* **857** (2012) 219. arXiv:1110.1688.
- (variant, D₁₀) A. Datta, F.-S. Ling, P. Ramond and Kajiyama–Raidal–Strumia, `cos θ₁₂ = φ/2`.

**Exact statement.** The A₅ (icosahedral) golden-ratio pattern predicts the solar angle
`tan θ₁₂ = 1/φ`, i.e. `θ₁₂ = arctan(1/φ) ≈ 31.7°` (with `φ = (1+√5)/2`), together with **maximal
atmospheric** `θ₂₃ = 45°` and **vanishing reactor** `θ₁₃ = 0` at leading order. (This is the
"GR1" variant; equivalently `cot θ₁₂ = φ`. A distinct "GR2" variant from D₁₀ gives `cos θ₁₂ = φ/2`,
`θ₁₂ = 36° = π/5` — record both, but the A₅-native one is `tan θ₁₂ = 1/φ`.) The pattern arises from
the **residual/stabilizer symmetry** of the A₅-invariant neutrino and charged-lepton mass matrices:
a `Z₂ × Z₂` (Klein) residual subgroup in the neutrino sector and a distinct residual in the charged
sector, whose misalignment fixes the golden solar rotation.

**Hypotheses.** A₅ flavor symmetry with specified flavon VEV alignments; leading-order (corrections
lift `θ₁₃` from 0).

**maps to D0 claim/step:** D0-MODULAR-TIME-FLAVOR-001 — owner for "A₅ flavor ⟹ golden-ratio mixing
angle," and the specific appearance of `1/φ` (`tan θ₁₂ = 1/φ`) that matches D0's ℚ(φ) flavor field.
The `φ⁻¹`/`φ⁻²` structure that D0 flags is exactly the `tan θ₁₂ = 1/φ` (and `tan²θ₁₂ = φ⁻²`)
prediction here. **Note:** these are conventional (non-modular) A₅ flavor models; the *modular*-A₅
golden-ratio analogues appear in Ding–Feruglio-lineage level-5 modular papers (B3).

---

### B3 — Level-5 modular forms and the icosahedron (classical A₅ ↔ level-5)

**Citations.**
- P. P. Novichkov, S. T. Petcov, et al. / G.-J. Ding, S. F. King, X.-G. Liu, "Modular A₅ symmetry
  for flavour model building," *JHEP* **04** (2019) 174. arXiv:1812.02158.
- J. T. Penedo, S. T. Petcov, "Lepton masses and mixing from modular S₄ symmetry" and
  Novichkov–Penedo–Petcov–Titov, "Modular invariant models of lepton masses at levels 4 and 5,"
  *JHEP* **02** (2020) 001. arXiv:1908.11867.
- Classical: F. Klein, *Lectures on the Icosahedron* (1884) — the icosahedral/`A₅ ↔ level-5`
  correspondence and the 12 cusps as icosahedron vertices.

**Exact statement (faithful).** The finite modular group `Γ₅ ≅ A₅` (order 60), irreps
`{1, 3, 3', 4, 5}`. The space of modular forms of level 5 and weight `k` has dimension `5k + 1`; at
lowest non-trivial weight `k = 2` this is dimension `11`, decomposing under A₅ as
`5 ⊕ 3 ⊕ 3'` (a quintuplet `Y_5^{(2)}` plus triplets `Y_3^{(2)}, Y_{3'}^{(2)}`). The ring is
generated by two algebraically independent weight-`1/5` forms `F₁(τ), F₂(τ)` (each weight-`k`
level-5 form is a degree-`5k` polynomial in `F₁, F₂`). Geometrically, **level 5 has 12 cusps = the
12 vertices of the icosahedron**, realizing the classical Klein `A₅ ↔ level-5` correspondence.

**Hypotheses.** Standard modular-forms-of-level-N theory; `Γ₅ ≅ A₅` via `SL(2,ℤ)/Γ(5)` (mod the
center for the inhomogeneous group).

**maps to D0 claim/step:** D0-MODULAR-TIME-FLAVOR-001 / icosian route — owner for the classical
identification `A₅ ≅ Γ₅ ≅ PSL(2,5)` and the level-5/icosahedron dictionary. This is the
mathematically clean bridge object linking D0's icosian A₅ to the modular-forms side; it is the
strongest existing "shared object" between D0's flavor group and the modular apparatus.

---

### B4 — Hyperbolic SL(2,ℤ) (Anosov/toral) element ↔ finite-level flavor quotient: **NULL**

**Search target.** A primary-literature theorem in which a *specific hyperbolic* element of
`SL(2,ℤ)` (a toral/Anosov automorphism — a "cat map", e.g. `((2,1),(1,1))` or a golden/Fibonacci
element with irrational eigenvalue `φ²`/trace ≥ 3) is identified as a **time-evolution generator**
whose reduction mod `N` (or whose associated finite quotient) acts as a **flavor symmetry** (e.g.
`A₅` at `N = 5`).

**Finding: this link does not exist in the primary literature (honest null).** What exists is
adjacent but structurally different:

1. **Modular flavor symmetry (Feruglio lineage, B1–B3):** here `SL(2,ℤ)` is the *full modular group*
   acting on a **static modulus VEV `τ`** (a field, not a time coordinate); the flavor group is the
   finite quotient `Γ_N = SL(2,ℤ)/Γ(N)`. No single hyperbolic element is singled out; there is no
   time evolution — `τ` is frozen at a fixed point.
2. **Magnetized-torus / Narain modular flavor (Kobayashi et al., arXiv:2003.04174 and
   arXiv:2006.03059 "eclectic"):** flavor symmetry as `⟨S², T^N, (ST^N)²⟩` = rotational outer
   automorphisms of the Narain space group. Again the modular group acts on internal geometry, not as
   a hyperbolic time map.
3. **Hyperbolic toral automorphisms / cat maps (Anosov, ergodic theory):** studied as chaotic
   dynamics on `𝕋²`; the golden/Fibonacci trace connection to `ℚ(√5)` and `φ` is classical
   (systole of `SL(2,ℤ)\ℍ`, Fibonacci trace map), but **never** coupled to a finite-level flavor
   quotient acting on fermion generations.
4. **Speculative/adjacent recent items** (e.g. "quantum cosmology as automorphic dynamics,"
   arXiv:2405.09833; "MTG time-fiber-bundle" flavor-from-holonomy notes) treat modular/automorphic
   time and flavor in the same breath, but **none** states the specific theorem: "this hyperbolic
   `SL(2,ℤ)` element, as the time generator, has finite quotient `A₅` acting as the flavor group."
   They are motivational, not owners.

**Consequence for D0.** The time↔flavor identification (BOOK_06 §06.30a) is, as of this sweep,
**genuinely novel** — there is no external theorem to attach as owner. The two halves have separate
owners (Feruglio B1 for flavor-from-`Γ_N`; classical Anosov/toral-automorphism theory for the
hyperbolic time generator), but the *bridge* — a single hyperbolic element whose finite-level
reduction is the flavor group — is unowned in the literature. This is a valuable, honest null: the
D0 gap is real and not a rediscovery.

**maps to D0 claim/step:** D0-MODULAR-TIME-FLAVOR-001 / BOOK_06 §06.30a — records the MECH-LIMIT gap
as genuinely open (no external owner found for the bridge).

---

## RANKED SHORTLIST — 3 external theorems most likely to become named owners of D0 rows

1. **Ihara–Bass determinant formula (Hashimoto 1989 / Bass 1992)** — A1.
   Owns the Ξ-intertwiner row directly:
   `det(I − uB) = (1 − u²)^{m−n} · det(I − uA + u²(D − I))`, the *exact* identity D0 already verified
   numerically (`m − n = 326` on K(9,11,13)). Highest-confidence owner; no regularity assumption in
   the core polynomial identity. **This is the primary named owner for T1.**

2. **Kotani–Sunada (2000) spectral bounds** — A2.
   Owns the deterministic finite-B spectral row: Perron simple, `d_m − 1 ≤ α ≤ d_M − 1`, structured
   unit-modulus / RH band. Directly bounds the verified Perron ≈ 20.8335 and organizes the 653
   unit-modulus eigenvalues. Best deterministic owner for the irregular carrier.

3. **Feruglio (2017) modular-flavor paradigm + `Γ₅ ≅ A₅`** — B1 (with B3 as the level-5/icosahedron
   dictionary). Owns the flavor half of D0-MODULAR-TIME-FLAVOR-001: finite modular group
   `Γ_N = SL(2,ℤ)/Γ(N)` as flavor symmetry, with the exact `Γ₅ ≅ A₅` that D0's icosian route reaches
   independently. (The golden-ratio angle `tan θ₁₂ = 1/φ`, B2, is a close secondary owner for the
   φ-mixing row.)

**Honorable mention / conceptual owner:** Bordenave–Lelarge–Massoulié (A4) for *why NB is canonical*
(bulk at `√Perron`, informative modes detach where `A` fails) — strongest canonicity argument, but
random-graph-asymptotic, so conceptual not literal.

## MISMATCH RISKS

- **`d_m ≥ 2` (min-degree-2) hypothesis (A2, A5, A6).** Kotani–Sunada's degree bounds, the
  `(1 − u²)`-non-dividing clause, and the well-posed Euler product all assume **minimum degree ≥ 2**
  (no leaves) and **connectedness**. If any D0 carrier derived from K(9,11,13) (e.g. a sub-scene or a
  witness-extended 8-point carrier from T2) has a **degree-1 vertex** or is **disconnected**, clauses
  A2(1)–(3) and the clean ±1 bookkeeping (A5) fail verbatim and would need the general Bass identity
  (A1, which survives) plus a case-by-case tail analysis. **Action for architect:** confirm
  K(9,11,13) is connected with `d_m ≥ 2` before citing A2/A5 as verbatim owners. (The core Bass
  identity A1 has no such requirement, so the Ξ-intertwiner row is safe regardless.)
- **Bipartite/non-bipartite (A5).** The `−1` trivial multiplicity and the non-dividing clause need
  **non-bipartite**. If the carrier is bipartite, the `−1` bookkeeping differs; verify parity before
  attributing the full `2·326` trivial unit-modulus count.
- **Random vs deterministic (A4).** BLM is asymptotic over random ensembles; it cannot be cited as a
  literal bound on a single deterministic graph. Use it for the canonicity *principle* only; use A2
  for deterministic bounds.
- **Cover vs finite graph (A3).** Angel–Friedman–Hoory concerns the *infinite universal cover*, not
  the finite `B`. Do not cite it for finite-spectrum claims; it owns the "NB is strictly richer for
  irregular graphs" motivation only.
- **Typed return-channel: partial null (A6).** No external owner treats immediate backtracks as a
  *separately-typed* channel; the literature (Watanabe–Fukumizu, Bass deformed Laplacian) folds them
  into the `u²(D − I)` / `u²D` correction. D0's typed `p²`-return framing is, in the typing sense,
  **unowned** — attach A1/A6 for the algebra, but flag the *typed-channel* interpretation as a D0
  construct without an external mirror.
- **Time↔flavor bridge: full null (B4).** No external theorem links a hyperbolic/Anosov `SL(2,ℤ)`
  time generator to a finite-level flavor quotient. The bridge in BOOK_06 §06.30a has **no owner** —
  do not attach one; the gap is genuinely novel.

---

*Discipline note (BOOK_00 §00.8 / §00.9): nothing above is promoted to "confirmed/derived." These
are candidate external owners with exact statements and hypotheses; the two recorded nulls (typed
return-channel partial null A6; time↔flavor full null B4) are reported with the same care as the
positive owners. Primary sources only; blog/speculative items explicitly labelled as non-owners.*
