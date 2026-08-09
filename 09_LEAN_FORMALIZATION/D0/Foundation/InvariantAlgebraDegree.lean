import D0.Foundation.InvariantMinimal
import Mathlib.Combinatorics.SimpleGraph.Finite

/-!
# The full invariant algebra of the frozen `K(9,11,13)` scene

This module upgrades the orbit-level statement in
`D0.Foundation.InvariantMinimal` to an exact function-level classification.
For the concrete graph on `Fin 33`, every rational-valued function invariant
under **every graph automorphism** is represented by one and only one
quadratic polynomial in the computed vertex degree.

The result is deliberately local and non-circular:

* the graph is rebuilt from the existing adjacency relation;
* invariance quantifies over the full `SimpleGraph.Iso` automorphism type, not
  only over the literal generator list;
* the coefficients are explicit Lagrange interpolation coefficients at the
  three actually computed degree values `20`, `22`, and `24`;
* `two_degree_values_do_not_force_unique_quadratic` records that the
  uniqueness conclusion genuinely uses three distinct degree values.

**Honest scope.** This is a theorem about the already frozen finite scene
`K(9,11,13)`. It does not derive that scene, the number of zones, or the
choice of degree as an owned observable. In particular, it must not be used
as an upper-embedding argument for a scene-count reduction that is supposed
to construct those data independently.
-/

namespace D0.Foundation.InvariantAlgebraDegree

open D0.Foundation.InvariantMinimal

/-! ## The graph and its full automorphism group -/

/-- The frozen scene as a `SimpleGraph`: vertices are adjacent exactly when
they lie in different zones. -/
def sceneGraph : SimpleGraph (Fin 33) where
  Adj := adj
  symm := fun _ _ h => h.symm
  loopless := ⟨fun _ h => h rfl⟩

instance : DecidableRel sceneGraph.Adj := fun i j => by
  change Decidable (adj i j)
  infer_instance

/-- Full graph automorphisms of the frozen scene. -/
abbrev GraphAut := sceneGraph ≃g sceneGraph

/-- A rational function is invariant under every graph automorphism. -/
def GraphAutInvariant (f : Fin 33 → ℚ) : Prop :=
  ∀ σ : GraphAut, ∀ i, f (σ i) = f i

/-- The `SimpleGraph` degree is definitionally the already owned, computed
degree observable. -/
theorem sceneGraph_degree_eq_deg (i : Fin 33) : sceneGraph.degree i = deg i := by
  change
    (sceneGraph.neighborFinset i).card =
      (Finset.univ.filter (fun j => adj i j)).card
  rw [SimpleGraph.neighborFinset_eq_filter]
  rfl

/-- Every full graph automorphism preserves the owned degree observable. -/
theorem graphAut_preserves_degree (σ : GraphAut) (i : Fin 33) :
    deg (σ i) = deg i := by
  rw [← sceneGraph_degree_eq_deg (σ i), ← sceneGraph_degree_eq_deg i]
  exact σ.degree_eq i

/-! ## Degree fibres are exactly the full-automorphism orbits -/

/-- On this frozen scene, equal degree is equivalent to equal zone. -/
theorem degree_eq_iff_zone :
    ∀ i j : Fin 33, (deg i = deg j ↔ zoneOf i = zoneOf j) := by
  native_decide

/-- Swapping two vertices in the same zone preserves the zone map everywhere. -/
theorem swap_preserves_zone :
    ∀ i j : Fin 33, zoneOf i = zoneOf j →
      ∀ x : Fin 33, zoneOf (Equiv.swap i j x) = zoneOf x := by
  native_decide

/-- A transposition inside one zone, packaged as a genuine graph
automorphism. -/
def swapGraphAutOfSameZone (i j : Fin 33) (h : zoneOf i = zoneOf j) :
    GraphAut where
  toEquiv := Equiv.swap i j
  map_rel_iff' := by
    intro x y
    change
      (zoneOf (Equiv.swap i j x) ≠ zoneOf (Equiv.swap i j y) ↔
        zoneOf x ≠ zoneOf y)
    rw [swap_preserves_zone i j h x, swap_preserves_zone i j h y]

/-- A function invariant under the full graph automorphism group is constant
on every degree fibre. -/
theorem graphAutInvariant_constant_on_degree_fibers
    (f : Fin 33 → ℚ) (hf : GraphAutInvariant f)
    {i j : Fin 33} (hdeg : deg i = deg j) :
    f i = f j := by
  by_cases hij : i = j
  · simp [hij]
  · have hzone : zoneOf i = zoneOf j := (degree_eq_iff_zone i j).mp hdeg
    have hs := hf (swapGraphAutOfSameZone i j hzone) i
    have hswap : swapGraphAutOfSameZone i j hzone i = j := by
      simp [swapGraphAutOfSameZone]
    rw [hswap] at hs
    exact hs.symm

/-! ## Explicit quadratic interpolation -/

/-- A quadratic polynomial, represented by its coefficients. -/
@[ext] structure QuadraticCoefficients where
  a : ℚ
  b : ℚ
  c : ℚ
deriving DecidableEq

/-- Evaluate a quadratic coefficient triple at the degree of a scene vertex. -/
def QuadraticCoefficients.eval (q : QuadraticCoefficients) (i : Fin 33) : ℚ :=
  q.a + q.b * (deg i : ℚ) + q.c * (deg i : ℚ) ^ 2

/-- A chosen vertex of degree `20`. -/
def degree20Vertex : Fin 33 := 20

/-- A chosen vertex of degree `22`. -/
def degree22Vertex : Fin 33 := 9

/-- A chosen vertex of degree `24`. -/
def degree24Vertex : Fin 33 := 0

@[simp] theorem deg_degree20Vertex : deg degree20Vertex = 20 := by native_decide
@[simp] theorem deg_degree22Vertex : deg degree22Vertex = 22 := by native_decide
@[simp] theorem deg_degree24Vertex : deg degree24Vertex = 24 := by native_decide

/-- Every vertex has one of the three interpolation degrees. -/
theorem degree_cases :
    ∀ i : Fin 33, deg i = 20 ∨ deg i = 22 ∨ deg i = 24 := by
  native_decide

/-- Explicit Lagrange interpolation coefficients at degrees `20`, `22`, `24`. -/
def interpolation (f : Fin 33 → ℚ) : QuadraticCoefficients where
  a :=
    66 * f degree20Vertex -
      120 * f degree22Vertex +
      55 * f degree24Vertex
  b :=
    (-23 * f degree20Vertex +
      44 * f degree22Vertex -
      21 * f degree24Vertex) / 4
  c :=
    (f degree20Vertex -
      2 * f degree22Vertex +
      f degree24Vertex) / 8

/-- The explicit interpolation polynomial agrees with every full
graph-automorphism-invariant rational function. -/
theorem graphAut_invariant_eq_interpolation
    (f : Fin 33 → ℚ) (hf : GraphAutInvariant f) :
    ∀ i, f i = (interpolation f).eval i := by
  intro i
  rcases degree_cases i with h20 | h22 | h24
  · have hi : f i = f degree20Vertex :=
      graphAutInvariant_constant_on_degree_fibers f hf
        (h20.trans deg_degree20Vertex.symm)
    rw [hi]
    simp only [QuadraticCoefficients.eval, interpolation, h20, Nat.cast_ofNat]
    ring
  · have hi : f i = f degree22Vertex :=
      graphAutInvariant_constant_on_degree_fibers f hf
        (h22.trans deg_degree22Vertex.symm)
    rw [hi]
    simp only [QuadraticCoefficients.eval, interpolation, h22, Nat.cast_ofNat]
    ring
  · have hi : f i = f degree24Vertex :=
      graphAutInvariant_constant_on_degree_fibers f hf
        (h24.trans deg_degree24Vertex.symm)
    rw [hi]
    simp only [QuadraticCoefficients.eval, interpolation, h24, Nat.cast_ofNat]
    ring

/-- Three scene degree values determine the quadratic coefficients uniquely. -/
theorem quadratic_representation_unique
    (q q' : QuadraticCoefficients)
    (h : ∀ i : Fin 33, q.eval i = q'.eval i) :
    q = q' := by
  have h20 := h degree20Vertex
  have h22 := h degree22Vertex
  have h24 := h degree24Vertex
  simp only [QuadraticCoefficients.eval, deg_degree20Vertex, deg_degree22Vertex,
    deg_degree24Vertex, Nat.cast_ofNat] at h20 h22 h24
  apply QuadraticCoefficients.ext
  · linarith
  · linarith
  · linarith

/-- **Fixed-algebra classification.** A rational function on the frozen scene
is invariant under every graph automorphism iff it is represented by a unique
quadratic polynomial in the computed degree. -/
theorem graphAut_invariant_iff_existsUnique_quadratic (f : Fin 33 → ℚ) :
    GraphAutInvariant f ↔
      ∃! q : QuadraticCoefficients, ∀ i, f i = q.eval i := by
  constructor
  · intro hf
    refine ⟨interpolation f, graphAut_invariant_eq_interpolation f hf, ?_⟩
    intro q hq
    apply quadratic_representation_unique q (interpolation f)
    intro i
    rw [← hq i, ← graphAut_invariant_eq_interpolation f hf i]
  · rintro ⟨q, hq, _⟩
    intro σ i
    rw [hq (σ i), hq i]
    simp only [QuadraticCoefficients.eval, graphAut_preserves_degree σ i]

/-- A concise alias emphasizing the invariant-algebra interpretation:
the full fixed algebra is generated, as a vector space and pointwise algebra,
by `1`, `degree`, and `degree²`. -/
theorem degree_generates_full_invariant_algebra (f : Fin 33 → ℚ) :
    GraphAutInvariant f ↔
      ∃! q : QuadraticCoefficients, ∀ i, f i = q.eval i :=
  graphAut_invariant_iff_existsUnique_quadratic f

/-! ## Negative control: why three values matter -/

/-- A two-point toy "degree" with values `0` and `1`. -/
def twoPointDegree (i : Fin 2) : ℚ := i

/-- Evaluation of a coefficient triple on the two-point toy degree. -/
def QuadraticCoefficients.evalTwoPoint
    (q : QuadraticCoefficients) (i : Fin 2) : ℚ :=
  q.a + q.b * twoPointDegree i + q.c * twoPointDegree i ^ 2

/-- With only two degree values, distinct quadratics can define the same
function. Thus uniqueness above is not a formal artefact: the third distinct
degree value is load-bearing. -/
theorem two_degree_values_do_not_force_unique_quadratic :
    ∃ q q' : QuadraticCoefficients,
      q ≠ q' ∧ ∀ i : Fin 2, q.evalTwoPoint i = q'.evalTwoPoint i := by
  refine ⟨⟨0, 0, 0⟩, ⟨0, -1, 1⟩, ?_, ?_⟩
  · decide
  · intro i
    fin_cases i <;> norm_num [QuadraticCoefficients.evalTwoPoint, twoPointDegree]

end D0.Foundation.InvariantAlgebraDegree
