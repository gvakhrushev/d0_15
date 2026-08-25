import Mathlib.Data.Finite.Perm
import D0.Synthesis.YukawaQualitativeSelectorNoGo

/-!
# Yukawa selection ladder: qualitative (infinite) → spectral (≤6) → labeled (unique)

`YukawaQualitativeSelectorNoGo` showed the presently-owned *qualitative* profile
(equality pattern + rationality) collapses an infinite rational family of coefficient
triples. This module measures exactly how much more the *spectral* data — the eigenvalue
multiset of the operator `a+bQ+cQ²` — actually determines, and isolates the single missing
primitive.

On a fixed transport root frame `R` with the labeled eigenvalue map
`orderedEig k i = a + b·λᵢ + c·λᵢ²`:

* **Labeled spectrum ⇒ unique.** `orderedEig` is injective in `(a,b,c)` (Vandermonde on
  three distinct roots).
* **Unordered spectrum ⇒ finite, ≤ 6.** Two triples share the eigenvalue multiset iff their
  labeled images differ by a root permutation, so each spectral fiber injects into
  `Perm (Fin 3)` and has at most `6` elements.
* **Qualitative profile ⇒ infinite.** The fiber of the owned qualitative profile is infinite.

Net: spectral data is strictly stronger than the qualitative profile (∞ → ≤6), but a
*unique* coefficient triple still requires the one missing datum — a canonical ordering
(generation labeling) of the three transport roots.
-/

namespace D0.Synthesis.YukawaSpectralFiber

open D0.Synthesis.YukawaQualitativeSelectorNoGo

variable (R : TransportRootFrame)

/-- The labeled eigenvalue vector of the equivariant Yukawa operator. -/
def orderedEig (k : YukawaCoeff) (i : Fin 3) : ℝ := yukawaValue k (R.root i)

/-- **Labeled spectrum determines the coefficients.** Three distinct roots make the
coefficient-to-labeled-eigenvalue map injective (a Vandermonde elimination). -/
theorem orderedEig_injective : Function.Injective (orderedEig R) := by
  intro k l h
  have e0 := congrFun h 0
  have e1 := congrFun h 1
  have e2 := congrFun h 2
  simp only [orderedEig, yukawaValue] at e0 e1 e2
  set l0 := R.root 0 with hl0
  set l1 := R.root 1 with hl1
  set l2 := R.root 2 with hl2
  have h01 : l0 ≠ l1 := R.injective.ne (by decide)
  have h02 : l0 ≠ l2 := R.injective.ne (by decide)
  have h12 : l1 ≠ l2 := R.injective.ne (by decide)
  have key1 :
      (l1 - l0) * (((k.b : ℝ) - l.b) + ((k.c : ℝ) - l.c) * (l1 + l0)) = 0 := by
    linear_combination e1 - e0
  have hBC1 : ((k.b : ℝ) - l.b) + ((k.c : ℝ) - l.c) * (l1 + l0) = 0 :=
    (mul_eq_zero.1 key1).resolve_left (sub_ne_zero.2 h01.symm)
  have key2 :
      (l2 - l0) * (((k.b : ℝ) - l.b) + ((k.c : ℝ) - l.c) * (l2 + l0)) = 0 := by
    linear_combination e2 - e0
  have hBC2 : ((k.b : ℝ) - l.b) + ((k.c : ℝ) - l.c) * (l2 + l0) = 0 :=
    (mul_eq_zero.1 key2).resolve_left (sub_ne_zero.2 h02.symm)
  have hCC : ((k.c : ℝ) - l.c) * (l2 - l1) = 0 := by
    linear_combination hBC2 - hBC1
  have hc : (k.c : ℝ) - l.c = 0 :=
    (mul_eq_zero.1 hCC).resolve_right (sub_ne_zero.2 h12.symm)
  have hb : (k.b : ℝ) - l.b = 0 := by
    linear_combination hBC1 - (l1 + l0) * hc
  have ha : (k.a : ℝ) - l.a = 0 := by
    linear_combination e0 - l0 * hb - l0 ^ 2 * hc
  have hca : k.a = l.a := by exact_mod_cast sub_eq_zero.1 ha
  have hcb : k.b = l.b := by exact_mod_cast sub_eq_zero.1 hb
  have hcc : k.c = l.c := by exact_mod_cast sub_eq_zero.1 hc
  cases k
  cases l
  simp_all

/-- Two coefficient triples have the same **unordered** transport spectrum. -/
def SameSpectrum (k l : YukawaCoeff) : Prop :=
  ∃ σ : Equiv.Perm (Fin 3), ∀ i, orderedEig R l i = orderedEig R k (σ i)

/-- **The spectral fiber injects into `Perm (Fin 3)`**: the assignment of the realizing
permutation is injective on any spectral fiber. -/
theorem spectral_choose_injective (k : YukawaCoeff) :
    Function.Injective
      (fun l : {l // SameSpectrum R k l} => Classical.choose l.2) := by
  intro l m hlm
  apply Subtype.ext
  apply orderedEig_injective R
  funext i
  have hlm' : Classical.choose l.2 = Classical.choose m.2 := hlm
  have hl := Classical.choose_spec l.2 i
  have hm := Classical.choose_spec m.2 i
  rw [hl, hlm', ← hm]

/-- **Unordered spectrum ⇒ finite fiber.** -/
theorem spectral_fiber_finite (k : YukawaCoeff) :
    {l | SameSpectrum R k l}.Finite := by
  classical
  rw [← Set.finite_coe_iff]
  exact Finite.of_injective _ (spectral_choose_injective R k)

/-- **Unordered spectrum ⇒ at most six coefficient triples.** -/
theorem spectral_fiber_card_le_six (k : YukawaCoeff) :
    Nat.card {l // SameSpectrum R k l} ≤ 6 := by
  classical
  have hp : Nat.card (Equiv.Perm (Fin 3)) = 6 := by
    rw [Nat.card_perm, Nat.card_eq_fintype_card, Fintype.card_fin]
    rfl
  calc Nat.card {l // SameSpectrum R k l}
      ≤ Nat.card (Equiv.Perm (Fin 3)) :=
        Nat.card_le_card_of_injective _ (spectral_choose_injective R k)
    _ = 6 := hp

/-- **Qualitative profile ⇒ infinite fiber**: the presently-owned qualitative data does not
even cut the coefficient space down to a finite set. -/
theorem qualitative_fiber_infinite :
    {l | OwnedProfileEquivalent R (affineFamily 0) l}.Infinite := by
  apply Set.infinite_of_injective_forall_mem affineFamily_injective
  intro t
  exact affineFamily_profile_collapse R 0 t

/-- **Capstone (T33): the Yukawa selection ladder.** On an actual transport root frame:
the labeled spectrum pins the coefficients uniquely; the unordered spectrum cuts the fiber to
at most six; and the owned qualitative profile leaves an infinite fiber. The exact residual
primitive is therefore a canonical ordering (generation labeling) of the three roots. -/
theorem yukawa_selection_ladder :
    ∃ R : TransportRootFrame,
      Function.Injective (orderedEig R)
        ∧ (∀ k, {l | SameSpectrum R k l}.Finite)
        ∧ (∀ k, Nat.card {l // SameSpectrum R k l} ≤ 6)
        ∧ {l | OwnedProfileEquivalent R (affineFamily 0) l}.Infinite := by
  obtain ⟨R⟩ := transportRootFrame_exists
  exact ⟨R, orderedEig_injective R, spectral_fiber_finite R,
    spectral_fiber_card_le_six R, qualitative_fiber_infinite R⟩

end D0.Synthesis.YukawaSpectralFiber
