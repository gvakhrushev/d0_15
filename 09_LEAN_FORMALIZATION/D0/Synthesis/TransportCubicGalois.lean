import Mathlib.FieldTheory.PolynomialGaloisGroup
import Mathlib.RingTheory.Polynomial.Resultant.Basic
import Mathlib.Tactic.NormNum.IsSquare
import D0.Synthesis.TransportFieldNoGolden

/-!
# Transport cubic Galois group: internal order/degree confinement

The transport/metric cubic `Pcubic = X³ − 359X − 2574` (owner `D0-SCENE-JOINT-COMMUTANT-SIX-001`;
irreducible over `ℚ` at `TransportFieldNoGolden.Pcubic_irreducible`) controls the golden no-go
`D0-TRANSPORT-SPLITTING-FIELD-NOGO-001` (T19), whose external owner edge is the classification
`irreducible + non-square discriminant ⇒ Gal = S₃ ⇒ unique quadratic subfield`.

This module discharges internally the **order/degree confinement** part of that classification,
leaving only the discriminant-sign step external:

* `Pcubic_separable` — char-0 irreducible is separable;
* `Pcubic_gal_card_eq_finrank` — `|Gal(Pcubic)| = [SplittingField : ℚ]`;
* `three_dvd_card` — `3 ∣ |Gal|` (irreducible of prime degree 3);
* `card_gal_le_six` — `|Gal| ≤ 6` (the Galois action embeds faithfully in `S₃` on the three
  roots of the separable cubic);
* `card_gal_three_or_six` — hence `|Gal| ∈ {3, 6}`;
* `finrank_splitting_three_or_six` — equivalently `[SplittingField : ℚ] ∈ {3, 6}`.

So the transport Galois group is `A₃` (order 3) or `S₃` (order 6) **and nothing else**, proved
with clean axioms and no bridge. The single remaining external input for T19 is precisely the
discriminant-sign criterion selecting `S₃` over `A₃` (mathlib has no ready
`square-discriminant ↔ Gal ⊆ Aₙ` theorem); everything else is now internal.
-/

namespace D0.Synthesis.TransportCubicGalois

open Polynomial
open D0.Synthesis.TransportFieldNoGolden

/-- The transport cubic is separable (char 0, irreducible). -/
theorem Pcubic_separable : Pcubic.Separable := Pcubic_irreducible.separable

/-- `|Gal(Pcubic)| = [SplittingField : ℚ]` for the separable transport cubic. -/
theorem Pcubic_gal_card_eq_finrank :
    Nat.card Pcubic.Gal = Module.finrank ℚ Pcubic.SplittingField :=
  Gal.card_of_separable Pcubic_separable

/-- `3 ∣ |Gal(Pcubic)|` — irreducible of prime degree 3. -/
theorem three_dvd_card : 3 ∣ Nat.card Pcubic.Gal := by
  have := Gal.prime_degree_dvd_card (F := ℚ) Pcubic_irreducible
    (by rw [Pcubic_natDegree]; norm_num)
  rwa [Pcubic_natDegree] at this

/-- `|Gal(Pcubic)| ≤ 6` — the Galois action is a faithful permutation of the three roots. -/
theorem card_gal_le_six : Nat.card Pcubic.Gal ≤ 6 := by
  classical
  haveI : Fact ((Pcubic.map (algebraMap ℚ Pcubic.SplittingField)).Splits) :=
    ⟨SplittingField.splits Pcubic⟩
  have hle := Nat.card_le_card_of_injective _
    (Gal.galActionHom_injective Pcubic Pcubic.SplittingField)
  have hcardroot := card_rootSet_eq_natDegree (K := Pcubic.SplittingField)
    Pcubic_separable (SplittingField.splits Pcubic)
  rw [Pcubic_natDegree] at hcardroot
  have hroot3 : Nat.card (Pcubic.rootSet Pcubic.SplittingField) = 3 := by
    rw [Nat.card_eq_fintype_card]; simpa using hcardroot
  have hperm : Nat.card (Equiv.Perm (Pcubic.rootSet Pcubic.SplittingField)) = 6 := by
    rw [Nat.card_eq_fintype_card, Fintype.card_perm, ← Nat.card_eq_fintype_card, hroot3]; decide
  omega

/-- The transport Galois group is nontrivial (`|Gal| ≥ 1`). -/
theorem card_gal_pos : 1 ≤ Nat.card Pcubic.Gal := by
  rw [Pcubic_gal_card_eq_finrank]; exact Module.finrank_pos

/-- The transport Galois group has order exactly `3` (i.e. `A₃`) or `6` (i.e. `S₃`). -/
theorem card_gal_three_or_six : Nat.card Pcubic.Gal = 3 ∨ Nat.card Pcubic.Gal = 6 := by
  obtain ⟨k, hk⟩ := three_dvd_card
  have h6 := card_gal_le_six
  have h1 := card_gal_pos
  omega

/-- Equivalently, the transport splitting field has degree `3` or `6` over `ℚ`. -/
theorem finrank_splitting_three_or_six :
    Module.finrank ℚ Pcubic.SplittingField = 3 ∨ Module.finrank ℚ Pcubic.SplittingField = 6 := by
  rw [← Pcubic_gal_card_eq_finrank]; exact card_gal_three_or_six

/-! ## The genuine polynomial discriminant of the transport cubic

`Polynomial.discr` (mathlib's resultant/Sylvester discriminant) of `Pcubic` equals the value
`6185264` owned by T19 via the ad-hoc coefficient expression `−4p³−27q²`, and it is not a
rational square. This internalizes the T19 discriminant into the *actual* polynomial
discriminant. The remaining external step for full `S₃` is only the general Galois–discriminant
parity theorem (`Gal ⊆ Aₙ ↔ discr is a square`), which mathlib does not provide. -/

/-- The transport cubic has degree exactly `3`. -/
theorem Pcubic_degree_three : Pcubic.degree = 3 := by
  rw [degree_eq_natDegree Pcubic_monic.ne_zero, Pcubic_natDegree]; rfl

/-- Mathlib's genuine polynomial discriminant of the transport cubic equals `6185264`
(the value owned as `−4p³−27q²` at T19). -/
theorem transport_discr_eq : Polynomial.discr Pcubic = 6185264 := by
  rw [Polynomial.discr_of_degree_eq_three Pcubic_degree_three]
  have h0 : Pcubic.coeff 0 = -2574 := by simp [Pcubic, Polynomial.coeff_X_pow, Polynomial.coeff_C]
  have h1 : Pcubic.coeff 1 = -359 := by simp [Pcubic, Polynomial.coeff_X_pow, Polynomial.coeff_C]
  have h2 : Pcubic.coeff 2 = 0 := by simp [Pcubic, Polynomial.coeff_X_pow, Polynomial.coeff_C]
  have h3 : Pcubic.coeff 3 = 1 := by simp [Pcubic, Polynomial.coeff_X_pow]
  rw [h0, h1, h2, h3]; norm_num

/-- The transport cubic's polynomial discriminant is not a rational square. -/
theorem transport_discr_not_square : ¬ IsSquare (Polynomial.discr Pcubic) := by
  rw [transport_discr_eq]; norm_num

/-- Capstone: the internal order/degree confinement of the transport cubic's Galois group.
Only the discriminant-sign selection of `S₃` over `A₃` remains external. The discriminant
itself is now the genuine `Polynomial.discr`, internal and non-square. -/
theorem transport_cubic_galois_confinement :
    Nat.card Pcubic.Gal = Module.finrank ℚ Pcubic.SplittingField
      ∧ 3 ∣ Nat.card Pcubic.Gal
      ∧ Nat.card Pcubic.Gal ≤ 6
      ∧ (Nat.card Pcubic.Gal = 3 ∨ Nat.card Pcubic.Gal = 6)
      ∧ Polynomial.discr Pcubic = 6185264
      ∧ ¬ IsSquare (Polynomial.discr Pcubic) :=
  ⟨Pcubic_gal_card_eq_finrank, three_dvd_card, card_gal_le_six, card_gal_three_or_six,
    transport_discr_eq, transport_discr_not_square⟩

end D0.Synthesis.TransportCubicGalois
