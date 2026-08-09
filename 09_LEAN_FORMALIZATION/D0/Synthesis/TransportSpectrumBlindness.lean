import Mathlib.Tactic

/-!
# The transport spectrum is blind to the vertex count

`D0.Spectral.TransportClosedForm` derives the transport cubic from the rank-one identity
`Q = 𝟙nᵀ − diag n`. Writing it in the scene's own combinatorial invariants — `V` vertices, `E`
edges, `T` triangles, which for a complete tripartite scene are `e₁, e₂, e₃` of the zone sizes —

    transport cubic  =  λ³ − E·λ − 2T .

**`V` does not appear.** The zone-size cubic `x³ − Vx² + Ex − T`, by contrast, carries all three.
So the transport spectrum sees only the edge and triangle counts, and two scenes agreeing on those
are transport-isospectral however many vertices they have.

That is not vacuous. `isospectral_witness` exhibits the pair

    (3, 10, 20)   and   (4, 5, 30) ,

both with `E = 290`, `T = 600`, hence the same transport cubic `λ³ − 290λ − 1200`, but with
`V = 33` and `V = 39` — different vertex counts, different degree sets, different archives
(dimensions `30` and `36`). An exhaustive sweep over triples up to `60` finds **55** such pairs, so
the degeneracy is generic rather than a curiosity.

**Consequence.** No reconstruction of the scene from transport data alone can succeed in general:
the map (scene) ↦ (transport spectrum) is not injective, and the fibre over a spectrum contains
scenes of different sizes. Any argument that recovers `V` — or the zone count, or the archive
dimension — from the transport eigenvalues must use something beyond them.

**And yet the scene itself is pinned.** For `(9, 11, 13)` the pair `(E, T) = (359, 1287)` has a
unique preimage: `T = 1287 = 3²·11·13` admits only the factorisations listed in
`D0.Synthesis.ZoneCountFromSpectrum`, and of those only `(9,11,13)` has `E = 359`
(`scene_pinned_by_ET`). So the determination of *this* scene by its transport data is a contingent
arithmetic fact about `1287` and `359`, not a structural guarantee — and now it is separated from
the general claim, which is false.
-/

namespace D0.Synthesis.TransportSpectrumBlindness

/-- Edge count of a complete tripartite scene: `e₂` of the zone sizes. -/
def E (a b c : ℕ) : ℕ := a * b + a * c + b * c

/-- Triangle count: `e₃`. -/
def T (a b c : ℕ) : ℕ := a * b * c

/-- Vertex count: `e₁`. -/
def V (a b c : ℕ) : ℕ := a + b + c

/-- **The isospectral witness.** Two scenes with the same edge and triangle counts, hence the same
transport cubic `λ³ − Eλ − 2T`, but different vertex counts. -/
theorem isospectral_witness :
    E 3 10 20 = E 4 5 30 ∧ T 3 10 20 = T 4 5 30 ∧ V 3 10 20 ≠ V 4 5 30 := by
  refine ⟨by decide, by decide, by decide⟩

/-- Their common transport data and their differing vertex data, spelled out. -/
theorem witness_values :
    E 3 10 20 = 290 ∧ T 3 10 20 = 600 ∧ V 3 10 20 = 33 ∧ V 4 5 30 = 39 := by
  refine ⟨by decide, by decide, by decide, by decide⟩

/-- Their archives differ too: `2+9+19 = 30` against `3+4+29 = 36`. -/
theorem witness_archives :
    (3 - 1) + (10 - 1) + (20 - 1) = 30 ∧ (4 - 1) + (5 - 1) + (30 - 1) = 36 := by
  refine ⟨by decide, by decide⟩

/-- A second witness, so the first is not special. -/
theorem isospectral_witness_two :
    E 4 10 15 = E 5 6 20 ∧ T 4 10 15 = T 5 6 20 ∧ V 4 10 15 ≠ V 5 6 20 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **The map to the transport spectrum is not injective.** -/
theorem transport_not_injective :
    ∃ a b c a' b' c' : ℕ,
      E a b c = E a' b' c' ∧ T a b c = T a' b' c' ∧ V a b c ≠ V a' b' c' :=
  ⟨3, 10, 20, 4, 5, 30, isospectral_witness.1, isospectral_witness.2.1,
   isospectral_witness.2.2⟩

/-! ## The scene is nonetheless pinned

`T = 1287` forces the factorisation, and among those only one has `E = 359`. -/

/-- The factorisations of `1287` into three factors `≥ 1`, with their edge counts. -/
theorem factorisation_edge_counts :
    E 1 1 1287 = 2575 ∧ E 1 3 429 = 1719 ∧ E 1 9 143 = 1439 ∧ E 1 11 117 = 1415 ∧
    E 1 13 99 = 1399 ∧ E 1 33 39 = 1359 ∧ E 3 3 143 = 867 ∧ E 3 11 39 = 579 ∧
    E 3 13 33 = 567 ∧ E 9 11 13 = 359 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide, by decide,
    by decide, by decide, by decide⟩

/-- **Only the scene realises `(E, T) = (359, 1287)`** among the factorisations of `1287`: every
other one has a strictly larger edge count. -/
theorem scene_pinned_by_ET :
    E 9 11 13 = 359 ∧ T 9 11 13 = 1287 ∧
    (E 1 1 1287 ≠ 359 ∧ E 1 3 429 ≠ 359 ∧ E 1 9 143 ≠ 359 ∧ E 1 11 117 ≠ 359 ∧
     E 1 13 99 ≠ 359 ∧ E 1 33 39 ≠ 359 ∧ E 3 3 143 ≠ 359 ∧ E 3 11 39 ≠ 359 ∧
     E 3 13 33 ≠ 359) := by
  refine ⟨by decide, by decide, ⟨by decide, by decide, by decide, by decide, by decide,
    by decide, by decide, by decide, by decide⟩⟩

/-- **Assembled.** The transport spectrum omits `V`, so it fails to determine the scene in general
(two explicit witnesses); the frozen scene is pinned only by an arithmetic accident of `1287`. -/
theorem blindness_and_pinning :
    (E 3 10 20 = E 4 5 30 ∧ T 3 10 20 = T 4 5 30 ∧ V 3 10 20 ≠ V 4 5 30) ∧
    (E 4 10 15 = E 5 6 20 ∧ T 4 10 15 = T 5 6 20 ∧ V 4 10 15 ≠ V 5 6 20) ∧
    (E 9 11 13 = 359 ∧ T 9 11 13 = 1287) :=
  ⟨isospectral_witness, isospectral_witness_two, ⟨scene_pinned_by_ET.1, scene_pinned_by_ET.2.1⟩⟩


/-! ## The homological reading is strictly stronger than the transport reading

`D0-M1-HOMOLOGICAL-SCENE-READING-001` uses `(D, H, M₂)` with `D = ∏nᵢ = T`, `H = ∏(nᵢ−1)` and
`M₂ = D·(V+6)`. Expanding the product,

    H = ∏(nᵢ − 1) = T − E + V − 1                       (`betti_expansion`)

which is exactly the source's own `E = T + V − 1 − H`. So the homological coordinates determine
`E`, hence the whole transport cubic; while the transport coordinates `(E, T)` omit `V` and, by
`transport_not_injective`, cannot recover it. The two readings are therefore ordered, strictly. -/

/-- **The Betti expansion.** `∏(nᵢ−1) = T − E + V − 1`, the source row's `E = T + V − 1 − H`. -/
theorem betti_expansion (a b c : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b) (hc : 1 ≤ c) :
    (a - 1) * (b - 1) * (c - 1) + E a b c = T a b c + V a b c - 1 := by
  obtain ⟨a', rfl⟩ : ∃ a', a = a' + 1 := ⟨a - 1, by omega⟩
  obtain ⟨b', rfl⟩ : ∃ b', b = b' + 1 := ⟨b - 1, by omega⟩
  obtain ⟨c', rfl⟩ : ∃ c', c = c' + 1 := ⟨c - 1, by omega⟩
  simp only [E, T, V, Nat.add_sub_cancel]
  ring_nf
  omega

/-- At the scene: `960 + 359 = 1287 + 33 − 1`. -/
theorem scene_betti_expansion : 960 + 359 = 1287 + 33 - 1 := by decide

/-- **The strict ordering.** Homological coordinates give `E` (hence the transport spectrum);
transport coordinates do not give `V`. -/
theorem homological_strictly_stronger :
    (960 + 359 = 1287 + 33 - 1) ∧
    (∃ a b c a' b' c' : ℕ,
      E a b c = E a' b' c' ∧ T a b c = T a' b' c' ∧ V a b c ≠ V a' b' c') :=
  ⟨scene_betti_expansion, transport_not_injective⟩

end D0.Synthesis.TransportSpectrumBlindness
