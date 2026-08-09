# Scene structure — what is proved, and where

Read this before re-deriving anything about `K(9,11,13)`. Every module below is built and
`sorry`-free; the numbers are reproduced in one shot by `tools/d0_scene_invariants.py`.

## The 33-dimensional carrier, accounted for

| piece | dim | module | statement |
|---|---|---|---|
| visible | 3 | `D0.Synthesis.ZoneIsGeneration` | one zone-constant direction per zone |
| dark (archive) | 30 | `D0.Spectral.DarkArchiveStructure` | `ker A` = zone-balanced vectors, blocks `nᵢ−1` |
| per zone | `nᵢ` | `ZoneIsGeneration.decomposition` | `1 + (nᵢ−1) = nᵢ`, split unique |

The visible/dark division is not a reading of the spectrum — it is the isotypic split of each zone.
`no_invariant_vector_in_archive`: the archive contains no `Aut`-invariant vector, which is why
`R^Aut` has dimension 3 and no more.

## The visible sector in closed form

`D0.Spectral.TransportClosedForm`

* `Q = 𝟙nᵀ − diag n` — rank-one update of the zone-size diagonal (`transport_rank_one`);
* secular equation `Σ nᵢ/(nᵢ+λ) = 1` **is** the transport cubic `λ³ − e₂λ − 2e₃`
  (`secular_eq_cubic`);
* eigenvector for a root: `xᵢ ∝ 1/(nᵢ+λ)` (`secular_root_gives_eigenvector`).

`D0.Spectral.TransportSelfAdjoint`: `D·Q = Qᵀ·D` with `D = diag n` — the transport operator is
self-adjoint in the zone-size measure, so the eigenvalues are real and the generation→transport
change of basis is a parameter-free `O(3)`. It is **not** CKM-like (`not_hierarchical`); every row
maximum is below 0.81 against CKM's 0.97+.

`D0.Spectral.TransportNotGolden`: no transport eigenvalue lies in `ℚ(√5) = ℚ(φ)`. A plain fact —
the earlier reading of it as a limit on the `φ`-engine is retracted inside that module.

## The dark sector, counted

`D0.Synthesis.DarkSectorCensus` — degeneracies `8, 10, 12` (`= nᵢ − 1`), summing to the owned
nullity 30, one equivariant coupling each, no fourth possible. Ties to `PhasonMode = TorusShell`
via the corpus's own `torusShell_zoneSize_ladder`, so the generation index and the archive index
are the same index.

`D0.Spectral.JointCommutant` — centralising `Aut` **and** the adjacency leaves `6 = 3 + 3`:
three spectral projections of `Q` (its cubic is irreducible, `no_rational_root` over all 48
divisors) plus one scalar per archive block. The `Aut`-commutant alone is the corpus's `12 = 3²+1+1+1`.

## One symmetric-function calculus

`D0.Synthesis.SymmetricFunctionCalculus` — the transport cubic, the `√(528·440·480) = 10560`
normalisation and the §04.2 active eigenvalues are three faces of `e₂, e₃`, tied by

    ∏(N − nᵢ) = N·e₂ − e₃          (`degree_product`, proved by `ring`)

so `359 = e₂`, `2574 = 2e₃`, `10560 = ∏deg`, `det S = 2e₃/∏deg = 39/160`, active product
`= 2N·e₂/(N·e₂ − e₃) = 359/160`.

`D0.Synthesis.ActiveSplittingFromDistinctness` — the degeneracy gap is a sum of squares,
`N·e₂ − 9e₃ = a(b−c)² + b(c−a)² + c(a−b)²`, zero **iff** the zones are equal. So distinct zone
sizes are simultaneously what makes the zones rigid in `Aut` and what splits the active spectrum;
at the scene the gap is 264.

## Zone count and sizes

* `D0.Synthesis.ZoneCountFromSpectrum` — `(D, H) = (1287, 960)` has a unique preimage across **all**
  part counts, so the multiplicative pair forces `k = 3`.
* `D0.Synthesis.ZoneCountCompleteness` — the completeness argument needs no enumeration: `5 ∣ H`
  forces the part 11, `3 ∣ H` forces 13, and the remainder admits only `[9]`.
* `D0.Synthesis.HomologicalReadingClassBoundary` — the **additive** pair `(V, H) = (33, 960)` does
  *not* force the count: `[3,5,9,16]` and `[2,2,4,5,9,11]` realise it. The corpus's
  `M1HomologicalSceneReading` is therefore sharply class-relative, and this supplies the witness
  its own controls lacked.

## Supporting results closing named corpus gaps

* `D0.Foundation.PartitionAlgebra` — unital subalgebras of `ℚ^V` are exactly partition algebras
  (finite Stone–Weierstrass), the fact `InvariantMinimal.lean:32` cites without formalizing.
* `D0.Foundation.ZoneConnectivity` — the 30 within-zone adjacent transpositions have the zones as
  their orbits, the fact `InvariantGenerationBridge.lean:42` cites without formalizing.
* `D0.Spectral.SubcriticalTraceClass` — `Summable ↔ a ≤ 2`, closing "not-Summable at the wall not
  formalized" and supplying the core-carrier object.
* `D0.Foundation.CascadeFloorOrientationParity` — the `+2` address step as a cascade floor.

## Dead ends, recorded so they are not re-attempted

* `D0.Foundation.SceneCountRouteNoGo` — comparing cascade obligations as **propositions** caps the
  count at 2 (`Iff` has two classes on `Prop`), and both interpretation arrows of
  `SceneCountReduction` are vacuous because their antecedents are theorems.
* `D0.Foundation.DiscriminationRetyping` — pair-indexed distinctness is **uninhabitable**.
* `D0.Foundation.DiscriminationKinds` — sort-indexed distinctness is **circular** (hypothesis
  equivalent to conclusion).
* `D0.Foundation.LadderRunLength` — the ladder stops at 15 for generic reasons
  (`stop_at_fifteen_is_generic`); five unrelated constraints give the same run length, so the
  agreement is arithmetic richness of 15, not structure.

## The capstone: complete spectral resolution (`D0.Synthesis.SceneSpectralResolution`)

The two canonical operators diagonalise complementary sectors of one decomposition
`ℚ³³ = ⟨𝟙⟩ ⊕ vis⊥(2) ⊕ dark₉(8) ⊕ dark₁₁(10) ⊕ dark₁₃(12)`:

| sector | dim | adjacency `A` | Laplacian `L` |
|---|---|---|---|
| visible | 1+2 | transport cubic (3 irrationals) | `{0, 33, 33}` degenerate |
| dark blocks | 8/10/12 | `0` | `24/22/20` = zone degrees |

* conservation law on every dark block: eigenvalue + multiplicity = 32 = |V|−1;
* visible Laplacian is `33·I − 𝟙nᵀ` — mirror of `Q = 𝟙nᵀ − diag n`;
* `[L, A]` annihilates the archive (`commutator_kills_dark`) — non-commutativity confined to the
  3-dim visible quotient;
* heat trace closed: `1 + 2x³³ + 8x²⁴ + 10x²² + 12x²⁰`, trace check `718 = 2E`;
* SEP leg of the dark-energy no-go gets its multiplicities: `L_archive = {24,22,20}` with
  `{8,10,12}`, window integer-free.

## The dark-EOS chain (conditional and unconditional branches)

`DarkSectorCensus → RoleOrientationEOS → DarkEOSDiscreteSet → LambdaCDMExcluded →
RoleModelDiscrimination → RoleAssignmentNarrowing → DarkEOSMagnitudeFree`

* **Unconditional**: ΛCDM excluded by the degeneracies alone (ratio model: `w = −1` needs `s = 15`,
  not a subset sum of `{8,10,12}`).
* **Conditional on |w| = φ (a reading; the row owns only the sign)**: eight values `−φ + s/30`,
  ΛCDM excluded by irrationality of φ, minimal deviation `φ − 8/5` (Fibonacci convergent error),
  narrowed to `w = 3/5 − φ ≈ −1.018` via the owned radial order.

## The α-front bridge: no equivariant seam (`D0.Synthesis.EquivariantSeamNoGo`)

Every operator equivariant under the same-zone swaps (which generate `Aut`) is block-diagonal
across the active(3)/archive(30) split: balanced→balanced (`archive_invariant`),
zone-constant→zone-constant (`visible_invariant`). Hence the Feshbach couplings `B, C` of the
α-front `W_eff(z)` vanish for every equivariant operator, `W_eff` is `z`-independent, and its seam
residue is zero. **The `2¹¹` active–archive pairing must break the scene's symmetry** — the
corpus's "EXTERNAL Dixmier extraction" (`ASSUMP-DIXMIER-TRACE`) is a proved necessity within the
equivariant class, not a modelling choice. Operator-level face of the commutant count
`12 = 3² + 1 + 1 + 1`, proved by direct swap arguments, no representation theory.

## The three-level Hodge assembly (`D0.Synthesis.HodgeThreeLevelSpectrum`)

See the reviewer strategy (`REVIEWER_STRATEGY_2026_08.md`): P₂ factorises as
`(8+x⁹)(10+x¹¹)(12+x¹³)`; McKean–Singer `P₀ − P₁ + P₂ = 961` for all x; `b₁ = 0`; doubling law at
level 1. The middle spectrum `Δ₁ = {9¹²⁰, 11⁹⁶, 13⁸⁰, 20²⁴, 22²⁰, 24¹⁶, 33³}` verified exactly.

## Session 2026-08-02: gravity closure + α endgame + matter equivariance

**Campaign 1 (gravity), complete.** `SceneHeatKernel` (projector partition, zoneHeat closed
forms, `zetaL`: ζ(0)=32, ζ(−1)=718, ζ(−2)=16426, ζ(1)=239/165) · `SceneTraceHeatCapacity`
(first concrete `FiniteArchiveGraph`; cuts n_z(33−n_z); horizon structure decided: zone unions
sub-horizon, full scene + co-vertex saturate; Lucas defect of full scene = 30 = archive dim) ·
`SceneSpectralAction` — first instantiation of the rows-91/92 ladder: a₀ = 718 = 2E,
a₂ = 16426 = 15708 + 2·**359**; the discrete EH action proxy **is the edge count** — the same
owned object as the α_top numerator (`α_top⁻¹ = 359φ⁻² − ξ₅`). Shared-object bridge gravity↔α.

**Campaign 2 (α endgame), through the adversarial loop** (1 KILL accepted+repaired, confirm
CLEAN — see `TRANSPORT_FORK_ENDGAME_MEMO.md`). `TransportForkEndgame`: door-5 double
instability; two-12 no-merge ([8,3,1] ≠ [9,1,1,1], centres 1≠4, deriveds 11≠8); toral stable
root φ⁻¹ (exclusivity + matrix wire + trace_T17 = −L₁₇); 12 = L₅+1 from the ξ₅ return (+1
anonymous); φ⁻¹/−φ not transport-cubic roots (scoped to the cubic). **Door-2 route reduced to
one named residual: PRIM-SEAM-CROSSING-TICK-IDENTIFICATION**; door 1 remains the live rival.

**Campaign 3 (matter equivariance), 2/3 — post-skeptic scoping.** `EquivariantHyperchargeCarrier`
— carrier audit for the owned 5-value hypercharge row over THREE classes: equivariant vertex
functions ≤3 values (no-go), symmetric edge weights ≤3 (no-go), directed edge functions ≤6
(pass). Counting does not make the directed current unique among ALL carriers (ordered triangles
and 2-paths also pass); it closes the two coarser classes below the PROOF-TARGET's own named
EXACT-MISSING object. Bounds cite the owned pair-orbit count (RAW-SCENE-GRAPH) and
zone-indicator minimality (F7). Under the 6-field convention (ν_R = 0) the gate saturates:
directed carriers must be injective on the six classes. `EquivariantMatrixStructure` — the
operator-level normal form of the commutant (≤ 12 structure constants 3+3+6, swap-generated, no
Schur); archive action = scalar `diagC−offC` per zone; **the archive block of the 33-scene is
abelian** — no equivariant non-commuting archive pair. The Higgs blocker itself is typed on
M₂(ZMod 44) (J2 firewall: NOT the 33-scene) and is untouched; the theorem closes only the
hypothetical 33-scene analogue.
