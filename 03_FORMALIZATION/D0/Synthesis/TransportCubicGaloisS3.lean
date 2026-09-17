import Mathlib.FieldTheory.PolynomialGaloisGroup
import Mathlib.GroupTheory.SpecificGroups.Cyclic
import Mathlib.LinearAlgebra.Vandermonde
import D0.Synthesis.TransportCubicGalois

/-!
# Transport cubic Galois endgame: the Vandermonde parity obstruction

This module targets the sole remaining internal edge for the transport cubic:
exclude the order-three alternative by constructing the Vandermonde square root
of the polynomial discriminant in the splitting field and proving that an
order-three Galois group would fix it.
-/

namespace D0.Synthesis.TransportCubicGaloisS3

open Polynomial
open D0.Synthesis.TransportFieldNoGolden
open D0.Synthesis.TransportCubicGalois

abbrev TransportSplit := Pcubic.SplittingField

local instance : Fact ((Pcubic.map (algebraMap ℚ TransportSplit)).Splits) :=
  ⟨SplittingField.splits Pcubic⟩

local instance : Pcubic.IsSplittingField ℚ Pcubic.SplittingField :=
  Polynomial.IsSplittingField.splittingField Pcubic

local instance : IsGalois ℚ Pcubic.SplittingField :=
  IsGalois.of_separable_splitting_field Pcubic_separable

theorem rootSet_card : Fintype.card (Pcubic.rootSet TransportSplit) = 3 := by
  have h := card_rootSet_eq_natDegree (K := TransportSplit)
    Pcubic_separable (SplittingField.splits Pcubic)
  simpa [Pcubic_natDegree] using h

noncomputable def rootEquiv : Fin 3 ≃ Pcubic.rootSet TransportSplit :=
  Fintype.equivOfCardEq (by simpa using rootSet_card.symm)

noncomputable def root (i : Fin 3) : TransportSplit :=
  (rootEquiv i).1

theorem root_injective : Function.Injective root := by
  intro i j hij
  apply rootEquiv.injective
  exact Subtype.ext hij

theorem root_aeval (i : Fin 3) : aeval (root i) Pcubic = 0 :=
  aeval_eq_zero_of_mem_rootSet (rootEquiv i).2

theorem root_cubic (i : Fin 3) :
    root i ^ 3 - 359 * root i - 2574 = 0 := by
  have h := root_aeval i
  simp [Pcubic, aeval_def] at h
  linear_combination h

theorem root_ne {i j : Fin 3} (hij : i ≠ j) : root i ≠ root j :=
  root_injective.ne hij

/-- Subtracting the cubic equation at two distinct roots gives the depressed-cubic
pair relation `rᵢ² + rᵢrⱼ + rⱼ² = 359`. -/
theorem pair_relation {i j : Fin 3} (hij : i ≠ j) :
    root i ^ 2 + root i * root j + root j ^ 2 = 359 := by
  have hi := root_cubic i
  have hj := root_cubic j
  have hprod :
      (root i - root j) *
        (root i ^ 2 + root i * root j + root j ^ 2 - 359) = 0 := by
    calc
      _ = (root i ^ 3 - 359 * root i - 2574) -
          (root j ^ 3 - 359 * root j - 2574) := by ring
      _ = 0 := by rw [hi, hj]; ring
  have hdiff : root i - root j ≠ 0 := sub_ne_zero.mpr (root_ne hij)
  exact sub_eq_zero.mp ((mul_eq_zero.mp hprod).resolve_left hdiff)

/-- The three enumerated roots have zero sum, as forced directly by the depressed cubic. -/
theorem roots_sum_zero :
    root 0 + root 1 + root 2 = 0 := by
  have h01 : root 0 ^ 2 + root 0 * root 1 + root 1 ^ 2 = 359 :=
    pair_relation (by decide : (0 : Fin 3) ≠ 1)
  have h02 : root 0 ^ 2 + root 0 * root 2 + root 2 ^ 2 = 359 :=
    pair_relation (by decide : (0 : Fin 3) ≠ 2)
  have hprod :
      (root 1 - root 2) * (root 0 + root 1 + root 2) = 0 := by
    calc
      _ = (root 0 ^ 2 + root 0 * root 1 + root 1 ^ 2) -
          (root 0 ^ 2 + root 0 * root 2 + root 2 ^ 2) := by ring
      _ = 0 := by rw [h01, h02]; ring
  have hdiff : root 1 - root 2 ≠ 0 :=
    sub_ne_zero.mpr (root_ne (by decide : (1 : Fin 3) ≠ 2))
  exact (mul_eq_zero.mp hprod).resolve_left hdiff

/-- The second elementary symmetric function of the roots is `-359`. -/
theorem roots_pair_sum :
    root 0 * root 1 + root 0 * root 2 + root 1 * root 2 = -359 := by
  have h01 : root 0 ^ 2 + root 0 * root 1 + root 1 ^ 2 = 359 :=
    pair_relation (by decide : (0 : Fin 3) ≠ 1)
  have hr2 : root 2 = -(root 0 + root 1) := by
    linear_combination roots_sum_zero
  rw [hr2]
  linear_combination -h01

/-- The product of the three roots is `2574`. -/
theorem roots_product :
    root 0 * root 1 * root 2 = 2574 := by
  have h01 : root 0 ^ 2 + root 0 * root 1 + root 1 ^ 2 = 359 :=
    pair_relation (by decide : (0 : Fin 3) ≠ 1)
  have h0 := root_cubic (0 : Fin 3)
  have hr2 : root 2 = -(root 0 + root 1) := by
    linear_combination roots_sum_zero
  rw [hr2]
  linear_combination h0 - root 0 * h01

/-- The oriented Vandermonde product of the three roots. -/
noncomputable def vandermondeDelta : TransportSplit :=
  (root 1 - root 0) * (root 2 - root 0) * (root 2 - root 1)

theorem det_vandermonde_root :
    (Matrix.vandermonde root).det = vandermondeDelta := by
  rw [Matrix.det_vandermonde]
  simp [vandermondeDelta, Fin.prod_univ_succ]

/-- The Vandermonde square is the genuine polynomial discriminant. This is derived
from the three root equations themselves rather than imported as an external
Galois-discriminant criterion. -/
theorem vandermondeDelta_sq :
    vandermondeDelta ^ 2 =
      algebraMap ℚ TransportSplit (Polynomial.discr Pcubic) := by
  rw [transport_discr_eq]
  calc
    vandermondeDelta ^ 2 =
        (root 0 + root 1 + root 2) ^ 2 *
            (root 0 * root 1 + root 0 * root 2 + root 1 * root 2) ^ 2
          - 4 * (root 0 * root 1 + root 0 * root 2 + root 1 * root 2) ^ 3
          - 4 * (root 0 + root 1 + root 2) ^ 3 * (root 0 * root 1 * root 2)
          - 27 * (root 0 * root 1 * root 2) ^ 2
          + 18 * (root 0 + root 1 + root 2) *
              (root 0 * root 1 + root 0 * root 2 + root 1 * root 2) *
              (root 0 * root 1 * root 2) := by
          simp only [vandermondeDelta]
          ring
    _ = 6185264 := by
      rw [roots_sum_zero, roots_pair_sum, roots_product]
      norm_num
    _ = algebraMap ℚ TransportSplit 6185264 := by norm_num

/-- The canonical (non-transported) action of `Gal(Pcubic)` on the roots in its
own splitting field. This avoids the auxiliary superfield action instance. -/
noncomputable def canonicalRootAction :
    Pcubic.Gal →* Equiv.Perm (Pcubic.rootSet TransportSplit) := by
  letI : MulAction Pcubic.Gal (Pcubic.rootSet TransportSplit) :=
    Polynomial.Gal.galActionAux Pcubic
  exact MulAction.toPermHom _ _

/-- The root action conjugated from the root subtype to `Fin 3`. -/
noncomputable def rootPermHom : Pcubic.Gal →* Equiv.Perm (Fin 3) :=
  rootEquiv.symm.permCongrHom.toMonoidHom.comp canonicalRootAction

/-- The Galois action on roots, transported to the fixed enumeration `Fin 3`. -/
noncomputable def rootPerm (σ : Pcubic.Gal) : Equiv.Perm (Fin 3) :=
  rootPermHom σ

theorem rootPerm_apply (σ : Pcubic.Gal) (i : Fin 3) :
    root (rootPerm σ i) = σ (root i) := by
  have hconj :
      rootPerm σ i =
        rootEquiv.symm (canonicalRootAction σ (rootEquiv i)) := by
    simp [rootPerm, rootPermHom, Equiv.permCongrHom_coe]
  rw [hconj]
  simp only [root, Equiv.apply_symm_apply]
  change ↑(canonicalRootAction σ (rootEquiv i)) = σ ↑(rootEquiv i)
  simp only [canonicalRootAction]
  rfl

/-- If the Galois group had order three, every induced root permutation would
be even: its cube is the identity, so its sign cannot be `-1`. -/
theorem rootPerm_sign_eq_one_of_card_three
    (hcard : Nat.card Pcubic.Gal = 3) (σ : Pcubic.Gal) :
    Equiv.Perm.sign (rootPerm σ) = 1 := by
  have hσ : σ ^ 3 = 1 := by
    have h := pow_card_eq_one' (x := σ)
    rwa [hcard] at h
  have hp : rootPerm σ ^ 3 = 1 := by
    rw [show rootPerm σ = rootPermHom σ from rfl, ← map_pow, hσ, map_one]
  have hs : Equiv.Perm.sign (rootPerm σ) ^ 3 = 1 := by
    rw [← map_pow, hp, map_one]
  rcases Int.units_eq_one_or (Equiv.Perm.sign (rootPerm σ)) with h | h
  · exact h
  · rw [h] at hs
    norm_num at hs

/-- Every Galois automorphism acts on the oriented Vandermonde by the sign of
its induced root permutation. -/
theorem map_vandermondeDelta (σ : Pcubic.Gal) :
    σ vandermondeDelta =
      (Equiv.Perm.sign (rootPerm σ) : TransportSplit) * vandermondeDelta := by
  have hmatrix :
      σ.mapMatrix (Matrix.vandermonde root) =
        (Matrix.vandermonde root).submatrix (rootPerm σ) id := by
    ext i j
    simp only [AlgEquiv.mapMatrix_apply, Matrix.map_apply, Matrix.vandermonde_apply,
      Matrix.submatrix_apply, id_eq, map_pow]
    rw [rootPerm_apply]
    rfl
  calc
    σ vandermondeDelta =
        σ (Matrix.vandermonde root).det := by rw [det_vandermonde_root]
    _ = (σ.mapMatrix (Matrix.vandermonde root)).det := σ.map_det _
    _ = ((Matrix.vandermonde root).submatrix (rootPerm σ) id).det := by rw [hmatrix]
    _ = (Equiv.Perm.sign (rootPerm σ) : TransportSplit) *
        (Matrix.vandermonde root).det := Matrix.det_permute _ _
    _ = (Equiv.Perm.sign (rootPerm σ) : TransportSplit) * vandermondeDelta := by
      rw [det_vandermonde_root]

/-- Under the order-three hypothesis, the Vandermonde square root is fixed by
the full Galois group. -/
theorem vandermondeDelta_fixed_of_card_three
    (hcard : Nat.card Pcubic.Gal = 3) (σ : Pcubic.Gal) :
    σ vandermondeDelta = vandermondeDelta := by
  rw [map_vandermondeDelta, rootPerm_sign_eq_one_of_card_three hcard]
  norm_num

/-- The order-three alternative would force the polynomial discriminant to be
a rational square. -/
theorem discr_isSquare_of_card_three
    (hcard : Nat.card Pcubic.Gal = 3) :
    IsSquare (Polynomial.discr Pcubic) := by
  have hfixed : ∀ σ : Pcubic.Gal, σ vandermondeDelta = vandermondeDelta :=
    vandermondeDelta_fixed_of_card_three hcard
  have hmem :
      vandermondeDelta ∈ Set.range (algebraMap ℚ TransportSplit) :=
    (IsGalois.mem_range_algebraMap_iff_fixed vandermondeDelta).2 hfixed
  obtain ⟨q, hq⟩ := hmem
  refine ⟨q, ?_⟩
  apply (algebraMap ℚ TransportSplit).injective
  calc
    algebraMap ℚ TransportSplit (Polynomial.discr Pcubic) =
        vandermondeDelta ^ 2 := vandermondeDelta_sq.symm
    _ = (algebraMap ℚ TransportSplit q) ^ 2 := by rw [hq]
    _ = algebraMap ℚ TransportSplit (q * q) := by simp [pow_two]

/-- The order-three branch is impossible because it would make the already
proved non-square discriminant a square. -/
theorem gal_card_ne_three : Nat.card Pcubic.Gal ≠ 3 := by
  intro hcard
  exact transport_discr_not_square (discr_isSquare_of_card_three hcard)

/-- **Transport Galois order closure.** The group has order exactly six. -/
theorem transport_gal_card_eq_six : Nat.card Pcubic.Gal = 6 :=
  card_gal_three_or_six.resolve_left gal_card_ne_three

/-- Therefore the splitting field has degree exactly six over `ℚ`. -/
theorem transport_splitting_finrank_eq_six :
    Module.finrank ℚ TransportSplit = 6 := by
  rw [← Pcubic_gal_card_eq_finrank, transport_gal_card_eq_six]

/-- The enumerated root action is faithful. -/
theorem rootPermHom_injective : Function.Injective rootPermHom := by
  intro σ τ hστ
  apply Gal.ext
  intro x hx
  obtain ⟨i, hi⟩ := rootEquiv.surjective ⟨x, hx⟩
  have hix : root i = x := congrArg Subtype.val hi
  rw [← hix, ← rootPerm_apply σ i, ← rootPerm_apply τ i]
  congr 1
  exact congrArg (fun p : Equiv.Perm (Fin 3) => p i) hστ

theorem rootPermHom_bijective : Function.Bijective rootPermHom := by
  apply (Fintype.bijective_iff_injective_and_card rootPermHom).2
  refine ⟨rootPermHom_injective, ?_⟩
  calc
    Fintype.card Pcubic.Gal = Nat.card Pcubic.Gal :=
      Nat.card_eq_fintype_card.symm
    _ = 6 := transport_gal_card_eq_six
    _ = (Fintype.card (Fin 3)).factorial := by decide
    _ = Fintype.card (Equiv.Perm (Fin 3)) := Fintype.card_perm.symm

/-- Concrete classification: the transport Galois group is the full symmetric
group on its three roots. -/
noncomputable def transportGalEquivS3 :
    Pcubic.Gal ≃* Equiv.Perm (Fin 3) :=
  MulEquiv.ofBijective rootPermHom rootPermHom_bijective

/-- Capstone: the transport cubic has full `S₃` Galois group, degree-six
splitting field, genuine non-square discriminant, and an explicit faithful
root-action equivalence. No external Galois-discriminant theorem is assumed. -/
theorem transport_cubic_galois_S3 :
    Nat.card Pcubic.Gal = 6
      ∧ Module.finrank ℚ TransportSplit = 6
      ∧ Nonempty (Pcubic.Gal ≃* Equiv.Perm (Fin 3))
      ∧ Polynomial.discr Pcubic = 6185264
      ∧ ¬ IsSquare (Polynomial.discr Pcubic) :=
  ⟨transport_gal_card_eq_six, transport_splitting_finrank_eq_six,
    ⟨transportGalEquivS3⟩, transport_discr_eq, transport_discr_not_square⟩

/-! ## Internal exclusion of `√5` and `√10` (closing the T19 owner edge)

With `Gal ≃ S₃` internal, the last external step of `D0-TRANSPORT-SPLITTING-FIELD-NOGO-001`
— identifying the unique quadratic subfield — is now discharged directly by a character
argument, without importing the subgroup-lattice classification. -/

/-- **Character rigidity of `S₃`.** Any homomorphism `Perm (Fin 3) →* ℤˣ` is either trivial
or the sign character. This is the abelianization `S₃ᵃᵇ = ℤ/2` in the exact form consumed
below: all transpositions are conjugate (so `P` is constant on them) and they generate. -/
theorem perm3_hom_eq_one_or_sign (P : Equiv.Perm (Fin 3) →* ℤˣ) :
    (∀ τ, P τ = 1) ∨ (∀ τ, P τ = Equiv.Perm.sign τ) := by
  have hconj : ∀ x y : Fin 3, x ≠ y → P (Equiv.swap x y) = P (Equiv.swap 0 1) := by
    intro x y hxy
    have hIC : IsConj (Equiv.swap (0 : Fin 3) 1) (Equiv.swap x y) :=
      Equiv.Perm.isConj_swap (by decide) hxy
    rw [isConj_iff] at hIC
    obtain ⟨c, hc⟩ := hIC
    have hP := congrArg P hc
    rw [map_mul, map_mul, map_inv] at hP
    rw [← hP, mul_comm (P c) (P (Equiv.swap 0 1)), mul_assoc, mul_inv_cancel, mul_one]
  have ha2 : (P (Equiv.swap 0 1)) ^ 2 = 1 := by
    have h1 : (Equiv.swap (0 : Fin 3) 1) ^ 2 = 1 := by decide
    rw [← map_pow, h1, map_one]
  rcases Int.units_eq_one_or (P (Equiv.swap 0 1)) with ha | ha
  · left
    intro τ
    refine Equiv.Perm.swap_induction_on τ ?_ ?_
    · exact map_one P
    · intro g x y hxy hg
      rw [map_mul, hconj x y hxy, ha, one_mul, hg]
  · right
    intro τ
    refine Equiv.Perm.swap_induction_on τ ?_ ?_
    · rw [map_one, Equiv.Perm.sign_one]
    · intro g x y hxy hg
      rw [map_mul, map_mul, hconj x y hxy, ha, hg, Equiv.Perm.sign_swap hxy]

/-- **No square root of a non-square `d` in the transport splitting field**, provided `d`
and `d · Δ` are both non-square in `ℚ` (`Δ = 6185264`). The proof: any `s` with `s² = d`
gives a character `σ ↦ σs/s : Gal → {±1}`; by `perm3_hom_eq_one_or_sign` it is trivial
(forcing `d` square) or equals the sign character (forcing `s = q·δ`, whence `d·Δ` square). -/
theorem sqrt_not_mem_of_not_square {d : ℚ}
    (hd : ¬ IsSquare d) (hdΔ : ¬ IsSquare (d * 6185264)) :
    ¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit d := by
  classical
  rintro ⟨s, hs⟩
  have hs0 : s ≠ 0 := by
    rintro rfl
    apply hd
    have hz : algebraMap ℚ TransportSplit d = 0 := by rw [← hs]; ring
    have hd0 : d = 0 :=
      (algebraMap ℚ TransportSplit).injective (hz.trans (map_zero _).symm)
    exact hd0 ▸ ⟨0, by ring⟩
  have hneg : (-s) ≠ s := by
    intro h
    apply hs0
    have h2 : (2 : TransportSplit) * s = 0 := by linear_combination -h
    have h20 : (2 : TransportSplit) ≠ 0 := by norm_num
    exact (mul_eq_zero.1 h2).resolve_left h20
  have hsig : ∀ σ : Pcubic.Gal, σ s = s ∨ σ s = -s := by
    intro σ
    have h2 : σ s * σ s = s * s := by
      have hpow : σ (s ^ 2) = s ^ 2 := by rw [hs]; exact σ.commutes d
      rw [map_pow, pow_two, pow_two] at hpow
      exact hpow
    have hfac : (σ s - s) * (σ s + s) = 0 := by linear_combination h2
    rcases mul_eq_zero.1 hfac with h | h
    · exact Or.inl (sub_eq_zero.1 h)
    · exact Or.inr (add_eq_zero_iff_eq_neg.1 h)
  have hmul : ∀ σ τ : Pcubic.Gal,
      (if (σ * τ) s = s then (1 : ℤˣ) else -1)
        = (if σ s = s then (1 : ℤˣ) else -1) * (if τ s = s then (1 : ℤˣ) else -1) := by
    intro σ τ
    have key : (σ * τ) s = σ (τ s) := rfl
    by_cases hσ : σ s = s <;> by_cases hτ : τ s = s
    · have h0 : (σ * τ) s = s := by rw [key, hτ, hσ]
      rw [if_pos h0, if_pos hσ, if_pos hτ, mul_one]
    · have hτn : τ s = -s := (hsig τ).resolve_left hτ
      have h0 : (σ * τ) s = -s := by rw [key, hτn, map_neg, hσ]
      have hne : (σ * τ) s ≠ s := by rw [h0]; exact hneg
      rw [if_neg hne, if_pos hσ, if_neg hτ, one_mul]
    · have hσn : σ s = -s := (hsig σ).resolve_left hσ
      have h0 : (σ * τ) s = -s := by rw [key, hτ, hσn]
      have hne : (σ * τ) s ≠ s := by rw [h0]; exact hneg
      rw [if_neg hne, if_neg hσ, if_pos hτ, mul_one]
    · have hσn : σ s = -s := (hsig σ).resolve_left hσ
      have hτn : τ s = -s := (hsig τ).resolve_left hτ
      have h0 : (σ * τ) s = s := by rw [key, hτn, map_neg, hσn, neg_neg]
      rw [if_pos h0, if_neg hσ, if_neg hτ]; decide
  set χ : Pcubic.Gal →* ℤˣ :=
    MonoidHom.mk' (fun σ => if σ s = s then (1 : ℤˣ) else -1) hmul with hχdef
  have hχval : ∀ σ, χ σ = (if σ s = s then (1 : ℤˣ) else -1) := fun _ => rfl
  have charAct : ∀ σ : Pcubic.Gal,
      σ s = ((χ σ : ℤ) : TransportSplit) * s := by
    intro σ
    by_cases h : σ s = s
    · have hc : ((χ σ : ℤ) : TransportSplit) = 1 := by rw [hχval, if_pos h]; simp
      rw [hc, one_mul]; exact h
    · have hn : σ s = -s := (hsig σ).resolve_left h
      have hc : ((χ σ : ℤ) : TransportSplit) = -1 := by rw [hχval, if_neg h]; simp
      rw [hc, hn]; ring
  set e := transportGalEquivS3 with he
  set Q : Equiv.Perm (Fin 3) →* ℤˣ := χ.comp e.symm.toMonoidHom with hQdef
  have heq : ∀ σ : Pcubic.Gal, e σ = rootPerm σ := fun _ => rfl
  have hδ0 : vandermondeDelta ≠ 0 := by
    intro h0
    have hsq := vandermondeDelta_sq
    rw [h0, transport_discr_eq] at hsq
    have hz : algebraMap ℚ TransportSplit (6185264 : ℚ) = 0 := by rw [← hsq]; ring
    have hz2 : (6185264 : ℚ) = 0 :=
      (algebraMap ℚ TransportSplit).injective (hz.trans (map_zero _).symm)
    norm_num at hz2
  rcases perm3_hom_eq_one_or_sign Q with hQ | hQ
  · have hall : ∀ σ : Pcubic.Gal, σ s = s := by
      intro σ
      have h := hQ (e σ)
      simp only [hQdef, MonoidHom.comp_apply, MulEquiv.coe_toMonoidHom,
        MulEquiv.symm_apply_apply] at h
      rw [charAct σ, h]; simp
    have hmem : s ∈ Set.range (algebraMap ℚ TransportSplit) :=
      (IsGalois.mem_range_algebraMap_iff_fixed s).2 hall
    obtain ⟨q, hq⟩ := hmem
    have hkey : algebraMap ℚ TransportSplit (q ^ 2) = algebraMap ℚ TransportSplit d := by
      rw [map_pow, hq, hs]
    have hqd : q ^ 2 = d := (algebraMap ℚ TransportSplit).injective hkey
    exact hd ⟨q, by rw [← hqd, pow_two]⟩
  · have hchi : ∀ σ : Pcubic.Gal, χ σ = Equiv.Perm.sign (rootPerm σ) := by
      intro σ
      have h := hQ (e σ)
      simp only [hQdef, MonoidHom.comp_apply, MulEquiv.coe_toMonoidHom,
        MulEquiv.symm_apply_apply] at h
      rw [heq σ] at h; exact h
    have hfixt : ∀ σ : Pcubic.Gal,
        σ (s * vandermondeDelta⁻¹) = s * vandermondeDelta⁻¹ := by
      intro σ
      have hc0 : ((Equiv.Perm.sign (rootPerm σ) : ℤ) : TransportSplit) ≠ 0 := by
        rcases Int.units_eq_one_or (Equiv.Perm.sign (rootPerm σ)) with h | h <;>
          rw [h] <;> simp
      rw [map_mul, map_inv₀, charAct σ, map_vandermondeDelta σ, hchi σ]
      field_simp
    have hmem : s * vandermondeDelta⁻¹ ∈ Set.range (algebraMap ℚ TransportSplit) :=
      (IsGalois.mem_range_algebraMap_iff_fixed _).2 hfixt
    obtain ⟨q, hq⟩ := hmem
    have hsq : algebraMap ℚ TransportSplit q * vandermondeDelta = s := by
      rw [hq, inv_mul_cancel_right₀ hδ0 s]
    have hδ2 : vandermondeDelta ^ 2 = algebraMap ℚ TransportSplit 6185264 := by
      rw [vandermondeDelta_sq, transport_discr_eq]
    have hkey : algebraMap ℚ TransportSplit (q ^ 2 * 6185264)
        = algebraMap ℚ TransportSplit d := by
      calc algebraMap ℚ TransportSplit (q ^ 2 * 6185264)
          = (algebraMap ℚ TransportSplit q) ^ 2 * algebraMap ℚ TransportSplit 6185264 := by
            rw [map_mul, map_pow]
        _ = (algebraMap ℚ TransportSplit q * vandermondeDelta) ^ 2 := by rw [← hδ2]; ring
        _ = s ^ 2 := by rw [hsq]
        _ = algebraMap ℚ TransportSplit d := hs
    have hdq : d = q ^ 2 * 6185264 :=
      ((algebraMap ℚ TransportSplit).injective hkey).symm
    exact hdΔ ⟨q * 6185264, by rw [hdq]; ring⟩

/-- `√5 ∉ K`: the transport splitting field contains no square root of `5`. -/
theorem sqrt5_not_mem :
    ¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit 5 :=
  sqrt_not_mem_of_not_square (by norm_num) (by norm_num)

/-- `√10 ∉ K`: the transport splitting field contains no square root of `10`. -/
theorem sqrt10_not_mem :
    ¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit 10 :=
  sqrt_not_mem_of_not_square (by norm_num) (by norm_num)

/-- **Capstone (T30): the transport splitting field is golden- and DE-window-free, internally.**
`√5` and `√10` both lie outside `K`, proved without the external unique-quadratic-subfield
classification: only the internal `Gal = S₃` fact and the two non-square certificates are used. -/
theorem transport_splitting_excludes_sqrt5_sqrt10 :
    (¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit 5)
      ∧ (¬ ∃ s : TransportSplit, s ^ 2 = algebraMap ℚ TransportSplit 10) :=
  ⟨sqrt5_not_mem, sqrt10_not_mem⟩

end D0.Synthesis.TransportCubicGaloisS3
