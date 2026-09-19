import Mathlib.Tactic
import D0.SelfReading.TypedCapacityRawScene
import D0.Representation.CompatibleInvolutionClassification

/-!
# Owned orientation descends trivially to the three-zone generation quotient

The typed scene remembers the carrier construction

  V9  = Omega8 + Witness
  V11 = V9 + Dyad
  V13 = V9 + Role,

while the graph/generation quotient remembers only the zone constructor.

There is therefore a canonical pointwise extension of the owned Omega8
orientation flip to all three typed capacity carriers: flip the orientation
bit on the Omega8 summand and fix every added witness/dyad/role element.

This extension is genuinely nontrivial upstairs, but it preserves every zone
constructor.  Consequently every set-level action induced on the quotient
Fin 3 of zones is exactly the identity.  Its linear action on the generation
quotient is therefore scalar +I (the nc=12 scalar branch), not a non-scalar
(2,1) grading.

This closes an important false route: the missing generation grading cannot
be obtained by simply descending the already-owned pointwise orientation
action through the typed scene quotient.  A nontrivial Fourier-sector ->
generation-fibre identification is extra representation provenance, not the
ordinary quotient action.
-/

namespace D0.Representation.OrientationZoneDescentNoGo

open D0.SelfReading.TypedCapacityRawScene
open D0.Representation.CompatibleInvolutionClassification

abbrev M3 := Matrix (Fin 3) (Fin 3) ℚ

/-- Pointwise owned orientation flip on Omega8 = Role x Bool. -/
def flipOmegaPoint (x : D0.Omega8) : D0.Omega8 :=
  (x.1, !x.2)

/-- Extend orientation through V9 = Omega8 + Witness. -/
def flipV9 : D0.V9 → D0.V9
  | Sum.inl x => Sum.inl (flipOmegaPoint x)
  | Sum.inr w => Sum.inr w

/-- Extend through V11 = V9 + Dyad, fixing the added dyad. -/
def flipV11 : D0.V11 → D0.V11
  | Sum.inl x => Sum.inl (flipV9 x)
  | Sum.inr d => Sum.inr d

/-- Extend through V13 = V9 + Role, fixing the added role block. -/
def flipV13 : D0.V13 → D0.V13
  | Sum.inl x => Sum.inl (flipV9 x)
  | Sum.inr r => Sum.inr r

/-- Canonical orientation extension to the typed 33-vertex carrier. -/
def flipTyped : TypedVertex → TypedVertex
  | .zone9 x => .zone9 (flipV9 x)
  | .zone11 x => .zone11 (flipV11 x)
  | .zone13 x => .zone13 (flipV13 x)

theorem flipOmegaPoint_involutive (x : D0.Omega8) :
    flipOmegaPoint (flipOmegaPoint x) = x := by
  rcases x with ⟨r, o⟩
  cases o <;> rfl

theorem flipV9_involutive (x : D0.V9) :
    flipV9 (flipV9 x) = x := by
  rcases x with x | w
  · simp [flipV9, flipOmegaPoint_involutive]
  · rfl

theorem flipV11_involutive (x : D0.V11) :
    flipV11 (flipV11 x) = x := by
  rcases x with x | d
  · simp [flipV11, flipV9_involutive]
  · rfl

theorem flipV13_involutive (x : D0.V13) :
    flipV13 (flipV13 x) = x := by
  rcases x with x | r
  · simp [flipV13, flipV9_involutive]
  · rfl

theorem flipTyped_involutive (x : TypedVertex) :
    flipTyped (flipTyped x) = x := by
  rcases x with x | x | x
  · simp [flipTyped, flipV9_involutive]
  · simp [flipTyped, flipV11_involutive]
  · simp [flipTyped, flipV13_involutive]

/-- A concrete upstream point on which orientation acts nontrivially. -/
def omegaPlus : D0.Omega8 := ((0, 0), false)

theorem orientation_is_nontrivial_upstairs :
    flipOmegaPoint omegaPlus ≠ omegaPlus := by
  native_decide

/-- Crucial descent fact: orientation never changes the scene zone. -/
theorem flipTyped_preserves_zone (x : TypedVertex) :
    typedZone (flipTyped x) = typedZone x := by
  rcases x with x | x | x <;> rfl

/-- Hence the complete-tripartite graph itself is unchanged. -/
theorem flipTyped_preserves_adjacency (i j : TypedVertex) :
    typedAdj (flipTyped i) (flipTyped j) = typedAdj i j := by
  unfold typedAdj
  rw [flipTyped_preserves_zone i, flipTyped_preserves_zone j]

/-- Any purported action on the three zone labels induced by the pointwise
orientation extension is forced to be the identity. -/
theorem induced_zone_action_eq_id
    (τ : Fin 3 → Fin 3)
    (hτ : ∀ x : TypedVertex,
      typedZone (flipTyped x) = τ (typedZone x)) :
    τ = id := by
  funext z
  fin_cases z
  · have h := hτ (.zone9 (Sum.inr PUnit.unit))
    simpa [flipTyped, typedZone] using h.symm
  · have h := hτ (.zone11 (Sum.inr (0 : D0.Dyad)))
    simpa [flipTyped, typedZone] using h.symm
  · have h := hτ (.zone13 (Sum.inr ((0, 0) : D0.Role)))
    simpa [flipTyped, typedZone] using h.symm

/-- The ordinary linear quotient action is therefore scalar +I. -/
def directZoneOrientation : M3 := (1 : M3)

theorem direct_zone_orientation_scalar :
    directZoneOrientation = (1 : M3) := rfl

/-- Scalar descent lands on the nc=12 branch, not the non-scalar nc=8 branch. -/
theorem direct_zone_orientation_nc_twelve :
    ncReadout directZoneOrientation = 12 := by
  native_decide

/-- Concrete graph-level loss of the terminal subset: an Omega8 point and the
halt witness live in the same zone and have identical adjacency rows. -/
def omegaAsV9 : D0.V9 := Sum.inl omegaPlus
def haltAsV9 : D0.V9 := Sum.inr PUnit.unit

theorem omega_and_halt_same_graph_row :
    ∀ y : TypedVertex,
      typedAdj (.zone9 omegaAsV9) y =
        typedAdj (.zone9 haltAsV9) y := by
  intro y
  rcases y with y | y | y <;> rfl

/-- Capstone no-go: orientation is nontrivial on the typed terminal carrier,
but ordinary descent through the scene/generation quotient is necessarily
trivial and scalar. -/
theorem orientation_zone_descent_nogo :
    flipOmegaPoint omegaPlus ≠ omegaPlus ∧
    (∀ x : TypedVertex, typedZone (flipTyped x) = typedZone x) ∧
    (∀ i j : TypedVertex,
      typedAdj (flipTyped i) (flipTyped j) = typedAdj i j) ∧
    (∀ (τ : Fin 3 → Fin 3),
      (∀ x : TypedVertex,
        typedZone (flipTyped x) = τ (typedZone x)) →
      τ = id) ∧
    ncReadout directZoneOrientation = 12 :=
  ⟨orientation_is_nontrivial_upstairs,
    flipTyped_preserves_zone,
    flipTyped_preserves_adjacency,
    induced_zone_action_eq_id,
    direct_zone_orientation_nc_twelve⟩

end D0.Representation.OrientationZoneDescentNoGo
