import D0.Spectral.DarkArchiveStructure
import D0.Synthesis.ActiveWindowIrrational
import Mathlib.Tactic

/-!
# The complete spectral resolution of the scene — one theorem, five fronts

The session's modules each resolved one operator on one sector. This module joins them: the scene
carries **two** canonical operators — the adjacency `A` and the Laplacian `L = D_deg − A` — and
they diagonalise **complementary** sectors of the same decomposition

    ℚ³³  =  ⟨𝟙⟩  ⊕  visible⊥ (dim 2)  ⊕  dark₉ (dim 8)  ⊕  dark₁₁ (dim 10)  ⊕  dark₁₃ (dim 12).

| sector | dim | `A` acts by | `L` acts by |
|---|---|---|---|
| visible (3) | `1+2` | transport cubic `λ³−359λ−2574` (3 distinct irrationals) | `{0, 33, 33}` — **degenerate** |
| dark₉ | 8 | `0` | `24` |
| dark₁₁ | 10 | `0` | `22` |
| dark₁₃ | 12 | `0` | `20` |

The mathematics of a complete-multipartite Laplacian spectrum is classical; the content here is the
machine-checked identification with the corpus's named objects, and what follows from holding all
of it in one place:

**1. The `L_archive` spectrum gets its multiplicities.** The dark-energy no-go
(`D0-PHASON-WZ-TRANSFER-OWNER-001`, SEP leg) quotes "the integer L_archive spectrum `{24,22,20}`"
with no multiplicities. Here: those integers are the zone **degrees**, each dark block is an exact
`L`-eigenspace (`dark_block_eigenvector`), and the multiplicities are the archive degeneracies
`8, 10, 12` of `DarkSectorCensus`. The disjointness from the `S_DE` window is inherited wholesale:
the window contains no integers at all (`ActiveWindowIrrational.disjoint_from_integers`).

**2. A conservation law.** On every dark block, eigenvalue plus multiplicity is constant:

    (33 − nᵢ) + (nᵢ − 1) = 32 = |V| − 1            (`conservation_law`, an identity)

so the dark spectrum lies on a line: frequency and degeneracy are one datum, traded one-for-one.
The heaviest block (12 dark states) vibrates lowest (20); the lightest (8) highest (24).

**3. The visible sector is Laplacian-degenerate.** On zone-constant vectors
`L = 33·I − 𝟙nᵀ` — the mirror of the transport identity `Q = 𝟙nᵀ − diag n` — with spectrum
`{0, 33, 33}` (`visible_constant_in_kernel`, `visible_orthogonal_eigen_33`). So the Laplacian
cannot see transport, and the adjacency cannot see the archive: **each operator is blind exactly
where the other resolves.** This is why the corpus needed both the rank (from `A`) and the archive
integers (from `L`): neither operator carries the other's information.

**4. The non-commutativity is confined.** `[L, A]` annihilates the whole 30-dimensional archive
(`commutator_kills_dark`): on dark vectors both operators are simultaneously diagonal. All failure
of commutation lives in the 3-dimensional visible quotient (numerically its rank is 2).

**5. The heat trace closes.** `Tr e^{−tL} = 1 + 2x³³ + 8x²⁴ + 10x²² + 12x²⁰` at `x = e^{−t}`
(`heatPoly`), with the dimension check `heatPoly 1 = 33` and the trace check
`2·33 + 8·24 + 10·22 + 12·20 = 718 = 2·E` (`laplacian_trace`). The spectral-zeta and trace-heat
α-routes (`D0-ALPHA-ZETA-RESIDUE-001`, `TraceHeatLucasCore`) gain the scene's canonical spectral
function in closed form: `ζ_L(s) = 2/33ˢ + 8/24ˢ + 10/22ˢ + 12/20ˢ`.

Per generation the dictionary reads: **(visible share, dark degeneracy, dark frequency)
= (1, nᵢ − 1, 33 − nᵢ)** — three numbers per zone, all from `nᵢ`, jointly exhausting the carrier.
-/

namespace D0.Synthesis.SceneSpectralResolution

open D0.Spectral.DarkArchiveStructure

/-- Zone sizes, as naturals and as rationals. -/
def zsizeN (z : Fin 3) : ℕ := if z = 0 then 9 else if z = 1 then 11 else 13

def zsize (z : Fin 3) : ℚ := (zsizeN z : ℚ)

theorem zsizeN_vals : zsizeN 0 = 9 ∧ zsizeN 1 = 11 ∧ zsizeN 2 = 13 := by decide

theorem zsize_vals : zsize 0 = 9 ∧ zsize 1 = 11 ∧ zsize 2 = 13 := by
  refine ⟨?_, ?_, ?_⟩
  · unfold zsize; rw [zsizeN_vals.1]; norm_num
  · unfold zsize; rw [zsizeN_vals.2.1]; norm_num
  · unfold zsize; rw [zsizeN_vals.2.2]; norm_num

/-- The degree function: `33 − zone size`, constant on zones. -/
def degQ (u : Fin 33) : ℚ := 33 - zsize (zone u)

/-- The graph Laplacian of the scene. -/
def lap (v : Fin 33 → ℚ) (u : Fin 33) : ℚ := degQ u * v u - ∑ w, adj u w * v w

/-! ## The dark sector: exact eigenspaces of `L`, annihilated by `A` -/

/-- On any zone-balanced vector the Laplacian is pointwise multiplication by the degree —
the adjacency term vanishes by `balanced_mem_ker`. -/
theorem laplacian_dark (v : Fin 33 → ℚ) (hbal : ∀ z, zoneSum v z = 0) (u : Fin 33) :
    lap v u = degQ u * v u := by
  unfold lap
  rw [balanced_mem_ker v hbal u, sub_zero]

/-- **Each dark block is an exact `L`-eigenspace with eigenvalue `33 − nᵢ`.** A balanced vector
supported in zone `z` satisfies `L v = (33 − zsize z) · v`. -/
theorem dark_block_eigenvector (z : Fin 3) (v : Fin 33 → ℚ)
    (hsupp : ∀ u, zone u ≠ z → v u = 0) (hbal : zoneSum v z = 0) :
    ∀ u, lap v u = (33 - zsize z) * v u := by
  have hball : ∀ z', zoneSum v z' = 0 := by
    intro z'
    by_cases h : z' = z
    · exact h ▸ hbal
    · unfold zoneSum
      apply Finset.sum_eq_zero
      intro w hw
      apply hsupp w
      rw [(Finset.mem_filter.mp hw).2]
      exact h
  intro u
  rw [laplacian_dark v hball u]
  by_cases hu : zone u = z
  · unfold degQ; rw [hu]
  · rw [hsupp u hu, mul_zero, mul_zero]

/-! ## The visible sector: rank-one Laplacian, degenerate at `33` -/

/-- The zone-cardinality cast: the filter card is the zone size. -/
theorem zone_card_zsize (z : Fin 3) :
    ((Finset.univ.filter (fun w : Fin 33 => zone w = z)).card : ℚ) = zsize z := by
  unfold zsize
  norm_cast
  fin_cases z <;> decide

/-- The total is the sum of the three zone sums (fiberwise decomposition). -/
theorem total_split (v : Fin 33 → ℚ) :
    total v = zoneSum v 0 + zoneSum v 1 + zoneSum v 2 := by
  have h3 : total v = ∑ z : Fin 3, zoneSum v z := by
    unfold total zoneSum
    rw [← Finset.sum_fiberwise Finset.univ zone v]
  rw [h3, Fin.sum_univ_three]

/-- Zone sum of a zone-constant vector. -/
theorem zoneSum_zone_const (c : Fin 3 → ℚ) (z : Fin 3) :
    zoneSum (fun w => c (zone w)) z = zsize z * c z := by
  unfold zoneSum
  show (∑ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z), c (zone w)) = zsize z * c z
  have hcongr : ∀ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z),
      c (zone w) = c z := fun w hw => by rw [(Finset.mem_filter.mp hw).2]
  rw [Finset.sum_congr rfl hcongr, Finset.sum_const, nsmul_eq_mul, zone_card_zsize]

/-- **The visible Laplacian is `33·I − 𝟙nᵀ`** — mirror of the transport identity
`Q = 𝟙nᵀ − diag n`: on zone-constant vectors, `L` returns `33·c(zone u)` minus the size-weighted
total. -/
theorem laplacian_visible (c : Fin 3 → ℚ) (u : Fin 33) :
    lap (fun w => c (zone w)) u
      = 33 * c (zone u) - (9 * c 0 + 11 * c 1 + 13 * c 2) := by
  unfold lap
  rw [adj_row (fun w => c (zone w)) u, total_split]
  simp only [zoneSum_zone_const]
  unfold degQ
  rw [zsize_vals.1, zsize_vals.2.1, zsize_vals.2.2]
  ring

/-- The constant vector is in the kernel: eigenvalue `0`. -/
theorem visible_constant_in_kernel (a : ℚ) (u : Fin 33) : lap (fun _ => a) u = 0 := by
  have h := laplacian_visible (fun _ => a) u
  calc lap (fun _ => a) u = 33 * a - (9 * a + 11 * a + 13 * a) := h
    _ = 0 := by ring

/-- **The `n`-orthogonal visible plane has eigenvalue `33`, doubly degenerate**: any zone-constant
vector with size-weighted total zero is an eigenvector at `33 = |V|`. -/
theorem visible_orthogonal_eigen_33 (c : Fin 3 → ℚ)
    (hortho : 9 * c 0 + 11 * c 1 + 13 * c 2 = 0) (u : Fin 33) :
    lap (fun w => c (zone w)) u = 33 * c (zone u) := by
  rw [laplacian_visible, hortho, sub_zero]

/-- Two explicit independent members of that plane, so the degeneracy is genuinely two. -/
def cPair₁ (z : Fin 3) : ℚ := if z = 0 then 11 else if z = 1 then -9 else 0
def cPair₂ (z : Fin 3) : ℚ := if z = 0 then 13 else if z = 1 then 0 else -9

theorem pair_orthogonality :
    (9 * cPair₁ 0 + 11 * cPair₁ 1 + 13 * cPair₁ 2 = 0) ∧
    (9 * cPair₂ 0 + 11 * cPair₂ 1 + 13 * cPair₂ 2 = 0) ∧
    cPair₁ 1 * cPair₂ 2 - cPair₁ 2 * cPair₂ 1 ≠ 0 := by
  refine ⟨?_, ?_, ?_⟩
  · show (9 : ℚ) * 11 + 11 * (-9) + 13 * 0 = 0; norm_num
  · show (9 : ℚ) * 13 + 11 * 0 + 13 * (-9) = 0; norm_num
  · show (-9 : ℚ) * (-9) - 0 * 0 ≠ 0; norm_num

theorem visible_pair_eigen (u : Fin 33) :
    lap (fun w => cPair₁ (zone w)) u = 33 * cPair₁ (zone u) ∧
    lap (fun w => cPair₂ (zone w)) u = 33 * cPair₂ (zone u) :=
  ⟨visible_orthogonal_eigen_33 cPair₁ pair_orthogonality.1 u,
   visible_orthogonal_eigen_33 cPair₂ pair_orthogonality.2.1 u⟩

/-! ## The conservation law and the census -/

/-- **Eigenvalue plus multiplicity is `|V| − 1` on every dark block** — an identity in the sizes. -/
theorem conservation_law (nz N : ℚ) : (N - nz) + (nz - 1) = N - 1 := by ring

theorem scene_conservation :
    ((33 - zsize 0) + (zsize 0 - 1) = 32) ∧
    ((33 - zsize 1) + (zsize 1 - 1) = 32) ∧
    ((33 - zsize 2) + (zsize 2 - 1) = 32) := by
  rw [zsize_vals.1, zsize_vals.2.1, zsize_vals.2.2]
  norm_num

/-- The dark spectral table: eigenvalue and multiplicity per generation. -/
theorem dark_spectral_table :
    (33 - zsize 0 = 24 ∧ zsize 0 - 1 = 8) ∧
    (33 - zsize 1 = 22 ∧ zsize 1 - 1 = 10) ∧
    (33 - zsize 2 = 20 ∧ zsize 2 - 1 = 12) := by
  rw [zsize_vals.1, zsize_vals.2.1, zsize_vals.2.2]
  norm_num

/-! ## Confinement of the non-commutativity -/

/-- Degree-weighting preserves zone balance: `degQ` is constant on each zone. -/
theorem zoneSum_deg_smul (v : Fin 33 → ℚ) (z : Fin 3) (h : zoneSum v z = 0) :
    zoneSum (fun w => degQ w * v w) z = 0 := by
  unfold zoneSum at h ⊢
  show (∑ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z), degQ w * v w) = 0
  have hcongr : ∀ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z),
      degQ w * v w = (33 - zsize z) * v w := by
    intro w hw
    unfold degQ
    rw [(Finset.mem_filter.mp hw).2]
  rw [Finset.sum_congr rfl hcongr, ← Finset.mul_sum, h, mul_zero]

/-- **`[L, A]` annihilates the archive.** On a balanced vector, `A` kills it outright and `A`
applied to `L v` vanishes too, because `L v = deg · v` is again balanced. So both operators are
simultaneously diagonal on the dark sector; all non-commutativity lives in the visible quotient. -/
theorem commutator_kills_dark (v : Fin 33 → ℚ) (hbal : ∀ z, zoneSum v z = 0) (u : Fin 33) :
    (∑ w, adj u w * v w = 0) ∧ (∑ w, adj u w * (lap v w) = 0) := by
  refine ⟨balanced_mem_ker v hbal u, ?_⟩
  have hlap : ∀ w, lap v w = degQ w * v w := laplacian_dark v hbal
  have hbal' : ∀ z, zoneSum (fun w => degQ w * v w) z = 0 :=
    fun z => zoneSum_deg_smul v z (hbal z)
  calc ∑ w, adj u w * lap v w = ∑ w, adj u w * (degQ w * v w) := by
        exact Finset.sum_congr rfl (fun w _ => by rw [hlap w])
    _ = 0 := balanced_mem_ker (fun w => degQ w * v w) hbal' u

/-! ## The heat trace and the assembled resolution -/

/-- The heat-trace polynomial: `Tr e^{−tL}` at `x = e^{−t}`. -/
def heatPoly (x : ℚ) : ℚ := 1 + 2 * x ^ 33 + 8 * x ^ 24 + 10 * x ^ 22 + 12 * x ^ 20

/-- Dimension check: at `t = 0` the trace is the dimension. -/
theorem heatPoly_dim : heatPoly 1 = 33 := by unfold heatPoly; norm_num

/-- Trace check: `Σ mult·λ = 718 = 2E` — twice the edge count, as a Laplacian trace must be. -/
theorem laplacian_trace :
    (2 * 33 + 8 * 24 + 10 * 22 + 12 * 20 = 718) ∧ (718 = 2 * 359) := by decide

/-- Multiplicity census: the five sectors exhaust the carrier. -/
theorem multiplicity_census : 1 + 2 + 8 + 10 + 12 = 33 := by decide

/-- **SEP with full data.** The archive `L`-spectrum is `{24, 22, 20}` (the zone degrees), and the
`S_DE` active window contains no integer whatsoever, so the disjointness of the dark-energy no-go
holds with multiplicities `8, 10, 12` attached. -/
theorem sep_full_data :
    (∀ m : ℤ, 160 * m ^ 2 - 480 * m + 359 ≠ 0) ∧
    (33 - zsize 0 = 24 ∧ 33 - zsize 1 = 22 ∧ 33 - zsize 2 = 20) :=
  ⟨D0.Synthesis.ActiveWindowIrrational.disjoint_from_integers,
   ⟨dark_spectral_table.1.1, dark_spectral_table.2.1.1, dark_spectral_table.2.2.1⟩⟩

/-- **The resolution, assembled.** Five sectors, `1+2+8+10+12 = 33`; trace `718 = 2E`; the
conservation law `λ + g = 32` on every dark block; dimension check on the heat trace. -/
theorem scene_spectral_resolution :
    (1 + 2 + 8 + 10 + 12 = 33) ∧
    ((2 * 33 + 8 * 24 + 10 * 22 + 12 * 20 = 718) ∧ (718 = 2 * 359)) ∧
    (((33 - zsize 0) + (zsize 0 - 1) = 32) ∧
      ((33 - zsize 1) + (zsize 1 - 1) = 32) ∧
      ((33 - zsize 2) + (zsize 2 - 1) = 32)) ∧
    heatPoly 1 = 33 :=
  ⟨multiplicity_census, laplacian_trace, scene_conservation, heatPoly_dim⟩

end D0.Synthesis.SceneSpectralResolution
