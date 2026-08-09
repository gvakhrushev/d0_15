import D0.Synthesis.YukawaCommutantSpectrum
import D0.Synthesis.TransportForkEndgame
import Mathlib.FieldTheory.IntermediateField.Adjoin.Basic
import Mathlib.Algebra.Polynomial.SpecificDegree
import Mathlib.FieldTheory.Minpoly.Field
import Mathlib.Tactic

/-!
# The transport field has no golden element: `φ ∉ ℚ(λ)` for every transport eigenvalue

`TransportNotGolden` kills point candidates (`λ ∈ ℚ(√5)` shapes) and its own retraction note
forbids wider readings; the fork-endgame skeptic (2026-08-02) recorded the honest upgrade path:
the transport cubic has PRIME degree 3, so its root field has no quadratic subfield. This
module delivers that upgrade — the universal that was twice KILLED as an overclaim ("no scenic
operator can supply the factor") is here proved in a form exhausted by construction: **field
membership**. The GENERAL export is `no_quadratic_element_in_transport_field` (NO element of
quadratic minimal-polynomial degree lies in `ℚ⟮λ⟯` — the full recorded lead); `φ`, `φ⁻¹` are
its instances.

* `phi_not_in_transport_field` — for every real root `λ` of `λ³ − 359λ − 2574`:
  `φ ∉ ℚ⟮λ⟯`. Mechanism: the cubic is irreducible over ℚ (degree 3, no rational root — the
  full-ℚ statement `no_rational_root_rat`), so `[ℚ⟮λ⟯ : ℚ] = 3`; the golden ratio has minimal
  polynomial `X² − X − 1` (irreducible via `goldenRatio_irrational`), so `φ ∈ ℚ⟮λ⟯` would force
  `2 ∣ 3`.
* `phi_inv_not_in_transport_field` — likewise `φ⁻¹ ∉ ℚ⟮λ⟯` (`φ = φ⁻¹ + 1`).

Since `ℚ⟮λ⟯` is exactly the set of values of rational functions of `λ` **with rational
coefficients** (standard field fact, docstring grade), this closes the whole class "some
polynomial/rational function of a transport eigenvalue with rational coefficients equals `φ` or
`φ⁻¹`, or any quadratic-degree element" — the per-crossing `φ⁻¹` of the α-line's door-2 route
cannot be manufactured from a single transport eigenvalue by any rational-coefficient
rational-function reading. Scope: one eigenvalue at a time (`ℚ⟮λ⟯`, not the splitting field
with several roots — symmetric functions of SEVERAL roots are rational and out of scope; the
splitting-field statement is a possible further step, not claimed). "Transport eigenvalue" =
root of the owned charpoly (`JointCommutant.Q_charpoly_coeffs`); the eigenvalue↔root reading is
the same spectral-mapping convention flagged docstring-grade in `YukawaCommutantSpectrum`.
Consumers: obligation (i) of `D0-ALPHA-SEAM-FORM-FORCED-001` (negative leg, now field-grade);
`TransportNotGolden`'s ℚ(√5)-exclusion instances become corollaries (its bracket sign table is
separate and NOT subsumed).
-/

namespace D0.Synthesis.TransportFieldNoGolden

open Real Polynomial IntermediateField
open scoped goldenRatio
open D0.Synthesis.YukawaCommutantSpectrum

/-- The transport cubic as a rational polynomial. -/
noncomputable def Pcubic : Polynomial ℚ := X ^ 3 - (C 359 * X + C 2574)

/-- The golden quadratic as a rational polynomial. -/
noncomputable def Qquad : Polynomial ℚ := X ^ 2 - (X + C 1)

theorem Pcubic_natDegree : Pcubic.natDegree = 3 := by
  unfold Pcubic
  compute_degree!

theorem Pcubic_monic : Pcubic.Monic := by
  unfold Pcubic
  apply monic_X_pow_sub
  apply lt_of_le_of_lt (b := (1 : WithBot ℕ))
  · compute_degree
  · decide

theorem Qquad_natDegree : Qquad.natDegree = 2 := by
  unfold Qquad
  compute_degree!

theorem Qquad_monic : Qquad.Monic := by
  unfold Qquad
  apply monic_X_pow_sub
  apply lt_of_le_of_lt (b := (1 : WithBot ℕ))
  · compute_degree
  · decide

theorem Pcubic_aeval (lam : ℝ) (hl : lam ^ 3 - 359 * lam - 2574 = 0) :
    Polynomial.aeval lam Pcubic = 0 := by
  unfold Pcubic
  simp only [map_sub, map_add, map_mul, map_pow, aeval_X, aeval_C]
  have h359 : (algebraMap ℚ ℝ) 359 = 359 := by norm_num
  have h2574 : (algebraMap ℚ ℝ) 2574 = 2574 := by norm_num
  rw [h359, h2574]
  linarith [hl]

theorem Pcubic_no_root : ∀ r : ℚ, ¬ Pcubic.IsRoot r := by
  intro r hr
  unfold Pcubic at hr
  simp only [IsRoot, eval_sub, eval_add, eval_mul, eval_pow, eval_X, eval_C] at hr
  exact no_rational_root_rat r (by linarith [hr])

theorem Pcubic_irreducible : Irreducible Pcubic :=
  Polynomial.irreducible_of_degree_le_three_of_not_isRoot
    (by rw [Pcubic_natDegree]; decide) Pcubic_no_root

/-- The golden quadratic has no rational root: a rational root `r` would factor the quadratic
as `(X − r)(X − (1 − r))`, making `φ` itself rational. -/
theorem Qquad_no_root : ∀ r : ℚ, ¬ Qquad.IsRoot r := by
  intro r hr
  unfold Qquad at hr
  simp only [IsRoot, eval_sub, eval_add, eval_pow, eval_X, eval_C] at hr
  have hR : (r : ℝ) ^ 2 - ((r : ℝ) + 1) = 0 := by exact_mod_cast hr
  have hfac : (φ - r) * (φ - (1 - (r : ℝ))) = 0 := by
    linear_combination goldenRatio_sq - hR
  rcases mul_eq_zero.mp hfac with h1 | h1
  · exact goldenRatio_irrational ⟨r, (sub_eq_zero.mp h1).symm⟩
  · refine goldenRatio_irrational ⟨1 - r, ?_⟩
    have := sub_eq_zero.mp h1
    push_cast
    linarith [this]

theorem Qquad_irreducible : Irreducible Qquad :=
  Polynomial.irreducible_of_degree_le_three_of_not_isRoot
    (by rw [Qquad_natDegree]; decide) Qquad_no_root

theorem Qquad_aeval_phi : Polynomial.aeval φ Qquad = 0 := by
  unfold Qquad
  simp only [map_sub, map_add, map_pow, aeval_X, aeval_C]
  have := goldenRatio_sq
  push_cast
  linarith [this]

/-- **`φ` is not in the field generated by any transport eigenvalue**: `[ℚ⟮λ⟯:ℚ] = 3` admits no
quadratic subextension. -/
theorem phi_not_in_transport_field (lam : ℝ) (hl : lam ^ 3 - 359 * lam - 2574 = 0) :
    φ ∉ IntermediateField.adjoin ℚ {lam} := by
  intro hmem
  have haev := Pcubic_aeval lam hl
  have hlint : IsIntegral ℚ lam := ⟨Pcubic, Pcubic_monic, haev⟩
  have hminP : minpoly ℚ lam = Pcubic :=
    (minpoly.eq_of_irreducible_of_monic Pcubic_irreducible haev Pcubic_monic).symm
  haveI : FiniteDimensional ℚ (IntermediateField.adjoin ℚ {lam}) :=
    IntermediateField.adjoin.finiteDimensional hlint
  have hrank : Module.finrank ℚ (IntermediateField.adjoin ℚ {lam}) = 3 := by
    rw [IntermediateField.adjoin.finrank hlint, hminP, Pcubic_natDegree]
  set K := IntermediateField.adjoin ℚ {lam} with hK
  let x : K := ⟨φ, hmem⟩
  have hxint : IsIntegral ℚ x := IsIntegral.of_finite ℚ x
  have hinj : Function.Injective (algebraMap K ℝ) := (algebraMap K ℝ).injective
  have hcoe : (algebraMap K ℝ) x = φ := rfl
  have hminx : minpoly ℚ x = Qquad := by
    have h1 : minpoly ℚ ((algebraMap K ℝ) x) = minpoly ℚ x := minpoly.algebraMap_eq hinj x
    rw [hcoe] at h1
    rw [← h1]
    exact (minpoly.eq_of_irreducible_of_monic Qquad_irreducible Qquad_aeval_phi Qquad_monic).symm
  have hdvd := minpoly.degree_dvd hxint
  rw [hminx, Qquad_natDegree, hrank] at hdvd
  norm_num at hdvd

/-- **Neither is `φ⁻¹`**: `φ = φ⁻¹ + 1` and intermediate fields are closed under `+ 1`. -/
theorem phi_inv_not_in_transport_field (lam : ℝ) (hl : lam ^ 3 - 359 * lam - 2574 = 0) :
    (φ⁻¹ : ℝ) ∉ IntermediateField.adjoin ℚ {lam} := by
  intro h
  apply phi_not_in_transport_field lam hl
  have hphi : (φ : ℝ) = φ⁻¹ + 1 := by
    rw [D0.Synthesis.TransportForkEndgame.phi_inv_eq]
    ring
  rw [hphi]
  exact add_mem h (one_mem _)

/-- **The general export**: NO element whose minimal polynomial over `ℚ` has degree 2 lies in
a single-eigenvalue transport field — `[ℚ⟮λ⟯ : ℚ] = 3` admits no quadratic subextension. The
golden units are instances. -/
theorem no_quadratic_element_in_transport_field (lam : ℝ)
    (hl : lam ^ 3 - 359 * lam - 2574 = 0)
    (y : ℝ) (hydeg : (minpoly ℚ y).natDegree = 2) :
    y ∉ IntermediateField.adjoin ℚ {lam} := by
  intro hmem
  have haev := Pcubic_aeval lam hl
  have hlint : IsIntegral ℚ lam := ⟨Pcubic, Pcubic_monic, haev⟩
  have hminP : minpoly ℚ lam = Pcubic :=
    (minpoly.eq_of_irreducible_of_monic Pcubic_irreducible haev Pcubic_monic).symm
  haveI : FiniteDimensional ℚ (IntermediateField.adjoin ℚ {lam}) :=
    IntermediateField.adjoin.finiteDimensional hlint
  have hrank : Module.finrank ℚ (IntermediateField.adjoin ℚ {lam}) = 3 := by
    rw [IntermediateField.adjoin.finrank hlint, hminP, Pcubic_natDegree]
  set K := IntermediateField.adjoin ℚ {lam} with hK
  let x : K := ⟨y, hmem⟩
  have hxint : IsIntegral ℚ x := IsIntegral.of_finite ℚ x
  have hinj : Function.Injective (algebraMap K ℝ) := (algebraMap K ℝ).injective
  have hminx : minpoly ℚ x = minpoly ℚ y := by
    have h1 : minpoly ℚ ((algebraMap K ℝ) x) = minpoly ℚ x := minpoly.algebraMap_eq hinj x
    rw [show (algebraMap K ℝ) x = y from rfl] at h1
    exact h1.symm
  have hdvd := minpoly.degree_dvd hxint
  rw [hminx, hydeg, hrank] at hdvd
  norm_num at hdvd

/-- **Assembled**: the golden units are absent from every single-eigenvalue transport field. -/
theorem transport_field_no_golden :
    ∀ lam : ℝ, lam ^ 3 - 359 * lam - 2574 = 0 →
      φ ∉ IntermediateField.adjoin ℚ {lam} ∧
      (φ⁻¹ : ℝ) ∉ IntermediateField.adjoin ℚ {lam} :=
  fun lam hl => ⟨phi_not_in_transport_field lam hl, phi_inv_not_in_transport_field lam hl⟩

end D0.Synthesis.TransportFieldNoGolden
