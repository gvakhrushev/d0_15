import D0.Foundation.M1Predicate
import D0.Spectral.AlphaProfiniteSpectralTower
import D0.Tower.NoExtension
import Mathlib.Tactic

/-!
# No-extension boundary: a real repeat no-go and a degree-two counterexample

This module separates the two claims previously conflated in `NoExtension`.

1. **Repeated indistinguishable copies.** A canonical constraint on copies must be invariant under
   relabelling. On a type with at least two copies, no such constraint can M1-force one copy:
   swapping the forced copy with another preserves admissibility and contradicts uniqueness. This
   closes the repeat branch as an actual theorem about `M1Forced`, rather than as the cardinality
   observation `|S₂| > 1`.

2. **A new type from a higher power.** Quadratic algebraic rank does not bound the number of
   distinct algebra elements. For `p = φ⁻¹`, the sequence `pⁿ` is strictly decreasing and hence
   injective. In particular `1`, `p`, `p²`, and `p³` are four distinct values even though
   `p³ = 2p - 1` lies in `span {1,p}`. Therefore `p³` reduction cannot by itself identify a fourth
   type with a repeated one.

The first result is positive progress. The second is a no-go for the old CASE-1 argument: an
additional semantic theorem classifying structural necessity types is required before the
three-zone upper bound can be recovered.
-/

namespace D0.Tower.NoExtensionBoundary

open D0
open D0.Foundation
open D0.Spectral.AlphaProfiniteSpectralTower

/-- A constraint on indistinguishable copies is canonical only if every relabelling preserves it. -/
def CopyRelabellingInvariant {α : Type} (Forced : α → Prop) : Prop :=
  ∀ (σ : Equiv.Perm α) (x : α), Forced x ↔ Forced (σ x)

/-- **Repeat branch, general form.** On any nontrivial copy type, a relabelling-invariant
constraint cannot M1-force one distinguished copy. The proof uses the transposition exchanging the
purported answer with a different copy. -/
theorem no_m1_forced_copy_under_full_relabelling
    {α : Type} [Nontrivial α] (Forced : α → Prop)
    (hInvariant : CopyRelabellingInvariant Forced) :
    ¬ ∃ a, M1Forced Forced a := by
  classical
  rintro ⟨a, ha⟩
  obtain ⟨b, hba⟩ := exists_ne a
  let σ : Equiv.Perm α := Equiv.swap a b
  have hFb : Forced b := by
    have hMoved : Forced (σ a) := (hInvariant σ a).mp ha.forced
    simpa [σ, hba, Ne.symm hba] using hMoved
  exact hba (ha.unique b hFb)

/-- Exact two-copy instance used by the zone-repeat argument. -/
theorem repeated_zone_type_not_m1_forced
    (Forced : Fin 2 → Prop)
    (hInvariant : CopyRelabellingInvariant Forced) :
    ¬ ∃ a, M1Forced Forced a :=
  no_m1_forced_copy_under_full_relabelling Forced hInvariant

/-- Cardinal form used downstream: if a finite family admits an M1-forced copy under a fully
relabelling-invariant constraint, then it has fewer than two members. This derives the numerical
copy cap from semantic hypotheses instead of assuming `m < 2`. -/
theorem m1_forced_copy_family_has_card_lt_two
    (m : ℕ) (Forced : Fin m → Prop)
    (hInvariant : CopyRelabellingInvariant Forced)
    (hForced : ∃ a, M1Forced Forced a) :
    m < 2 := by
  by_contra h
  have hm : 2 ≤ m := by omega
  letI : Nontrivial (Fin m) := Fin.nontrivial_iff_two_le.mpr hm
  exact no_m1_forced_copy_under_full_relabelling Forced hInvariant hForced

/-- Equivalent constructive reading: forcing one copy necessarily breaks copy-relabelling
symmetry, so it imports a label or other symmetry-breaking datum. -/
theorem forced_copy_requires_symmetry_breaking
    {α : Type} [Nontrivial α] {Forced : α → Prop} {a : α}
    (ha : M1Forced Forced a) :
    ¬ CopyRelabellingInvariant Forced := by
  intro hInvariant
  exact no_m1_forced_copy_under_full_relabelling Forced hInvariant ⟨a, ha⟩

/-- Negative control: once an external label is admitted, copy `0` can be forced. The constraint is
not relabelling-invariant, exactly identifying the forbidden extra datum. -/
def labelledFirstCopy : Fin 2 → Prop := fun i => i = 0

theorem labelled_first_copy_m1_forced :
    M1Forced labelledFirstCopy 0 where
  forced := rfl
  unique := by
    intro b hb
    exact hb

theorem labelled_first_copy_breaks_relabelling :
    ¬ CopyRelabellingInvariant labelledFirstCopy :=
  forced_copy_requires_symmetry_breaking labelled_first_copy_m1_forced

/-! ## Degree two does not imply only three values -/

/-- The golden inverse powers are strictly decreasing because `0 < φ⁻¹ < 1`. -/
theorem phi_inverse_powers_strictAnti :
    StrictAnti (fun n : ℕ => phi⁻¹ ^ n) :=
  pow_right_strictAnti₀ phi_inv_pos phi_inv_lt_one

/-- Consequently every power is a distinct algebra element. -/
theorem phi_inverse_powers_injective :
    Function.Injective (fun n : ℕ => phi⁻¹ ^ n) :=
  phi_inverse_powers_strictAnti.injective

/-- Arbitrarily long finite families of distinct powers exist inside the same quadratic algebra. -/
noncomputable def firstPowerEmbedding (n : ℕ) : Fin n ↪ ℝ where
  toFun i := phi⁻¹ ^ i.val
  inj' := by
    intro i j hij
    exact Fin.ext (phi_inverse_powers_injective hij)

/-- The proposed fourth value `p³` is distinct from all three advertised values `1`, `p`, `p²`. -/
theorem p_cubed_is_not_a_repeat_of_first_three :
    phi⁻¹ ^ 3 ≠ 1 ∧
    phi⁻¹ ^ 3 ≠ phi⁻¹ ∧
    phi⁻¹ ^ 3 ≠ phi⁻¹ ^ 2 := by
  constructor
  · intro h
    have h' : phi⁻¹ ^ 3 = phi⁻¹ ^ 0 := by simpa using h
    have : (3 : ℕ) = 0 := phi_inverse_powers_injective h'
    omega
  · constructor
    · intro h
      have h' : phi⁻¹ ^ 3 = phi⁻¹ ^ 1 := by simpa using h
      have : (3 : ℕ) = 1 := phi_inverse_powers_injective h'
      omega
    · intro h
      have : (3 : ℕ) = 2 := phi_inverse_powers_injective h
      omega

/-- **CASE-1 countertheorem.** The reduction identity is true, but it coexists with four distinct
values and indeed with an injection of every finite cardinality into the same power ladder.
Therefore "lies in a rank-two span" does not entail "is a repeated value/type". -/
theorem degree_two_reduction_does_not_bound_value_count :
    (phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1) ∧
    (phi⁻¹ ^ 3 ≠ 1 ∧ phi⁻¹ ^ 3 ≠ phi⁻¹ ∧ phi⁻¹ ^ 3 ≠ phi⁻¹ ^ 2) ∧
    (∀ n : ℕ, Nonempty (Fin n ↪ ℝ)) :=
  ⟨D0.Tower.p_cubed_reduces,
   p_cubed_is_not_a_repeat_of_first_three,
   fun n => ⟨firstPowerEmbedding n⟩⟩

end D0.Tower.NoExtensionBoundary
