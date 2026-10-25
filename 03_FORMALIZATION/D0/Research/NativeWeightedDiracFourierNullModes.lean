import D0.Geometry.ArchiveLorentzianCARDiracApplication
import D0.Research.NativeWeightedDiracBoundary

namespace D0.Research.NativeWeightedDiracFourierNullModes

open D0.Geometry

/-!
# Exact CAR contraction on null Fourier fibres

Source: `A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md`, §4 Eq. (5) and §5, pinned at
commit `db3091aded8f6cfe8d39dcd973ccf30ec40dfb08`, blob
`2de670c0e2f9a53104be8105a3554cdd9aaa85e7`.

The geometric module constructs the actual sixteen-component complex fibre
operator and proves its CAR contraction for any selected nonzero forward
multiplier. This module composes that application with the owned generic
nilpotent-kernel theorem. The remaining mode-selection premise is explicit:
the caller supplies a role whose forward multiplier is nonzero.
-/

noncomputable section

/-- Every nonzero product momentum has an actual role with nonzero forward
multiplier. The role is derived from the momentum rather than supplied as an
extra premise. -/
theorem exists_role_with_nonzero_forward_multiplier
    (N : ℕ) (k : Role → ZMod (archiveFibers N)) (hk : k ≠ 0) :
    ∃ r, archiveFourierForwardMultiplier N k r ≠ 0 := by
  classical
  have hcoordinate : ∃ r, k r ≠ 0 := by
    by_contra hnone
    push Not at hnone
    apply hk
    funext r
    exact hnone r
  obtain ⟨r, hr⟩ := hcoordinate
  exact ⟨r, (archiveFourierForwardMultiplier_ne_zero_iff N k r).2 hr⟩

/-- A zero-symbol Fourier fibre has equal kernel and range whenever one of
its actual forward CAR multipliers is nonzero. -/
theorem null_mode_kernel_eq_range
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) (r : Role)
    (hsymbol : roleWeightedArchiveFourierSymbol N w k = 0)
    (hforward : archiveFourierForwardMultiplier N k r ≠ 0) :
    LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k) =
      LinearMap.range (roleWeightedArchiveFourierFockActionLinear N w k) := by
  let D := roleWeightedArchiveFourierFockActionLinear N w k
  let K := roleWeightedArchiveFourierCARContraction N k r
  have hD : ∀ v, D (D v) = 0 := by
    intro v
    have hsquare := congrArg (fun T => T v)
      (roleWeightedArchiveFourierFockActionLinear_square N w k)
    simpa [D, LinearMap.comp_apply, LinearMap.id_apply, Pi.smul_apply, hsymbol]
      using hsquare
  have hK : ∀ v, D (K v) + K (D v) = v := by
    intro v
    have hcontract := congrArg (fun T => T v)
      (roleWeightedArchiveFourierFockActionLinear_contraction N w k r hforward)
    simpa [D, K, LinearMap.comp_apply, LinearMap.id_apply] using hcontract
  simpa [D] using
    NativeWeightedDiracBoundary.null_mode_kernel_eq_range D K hD hK

/-- A nonconstant zero-symbol fibre has equal kernel and range: the required
contracting role follows from the nonzero momentum coordinates. -/
theorem null_mode_kernel_eq_range_of_nonzero_momentum
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : roleWeightedArchiveFourierSymbol N w k = 0) (hk : k ≠ 0) :
    LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k) =
      LinearMap.range (roleWeightedArchiveFourierFockActionLinear N w k) := by
  obtain ⟨r, hforward⟩ := exists_role_with_nonzero_forward_multiplier N k hk
  exact null_mode_kernel_eq_range N w k r hsymbol hforward

/-- The same null-fibre application gives half the complex Fock dimension.
For the sixteen-state carrier this is eight. -/
theorem null_mode_kernel_half_dimension
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) (r : Role)
    (hsymbol : roleWeightedArchiveFourierSymbol N w k = 0)
    (hforward : archiveFourierForwardMultiplier N k r ≠ 0) :
    2 * Module.finrank ℂ
        (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k)) =
      Module.finrank ℂ (ArchiveFockState → ℂ) := by
  let D := roleWeightedArchiveFourierFockActionLinear N w k
  let K := roleWeightedArchiveFourierCARContraction N k r
  have hD : ∀ v, D (D v) = 0 := by
    intro v
    have hsquare := congrArg (fun T => T v)
      (roleWeightedArchiveFourierFockActionLinear_square N w k)
    simpa [D, LinearMap.comp_apply, LinearMap.id_apply, Pi.smul_apply, hsymbol]
      using hsquare
  have hK : ∀ v, D (K v) + K (D v) = v := by
    intro v
    have hcontract := congrArg (fun T => T v)
      (roleWeightedArchiveFourierFockActionLinear_contraction N w k r hforward)
    simpa [D, K, LinearMap.comp_apply, LinearMap.id_apply] using hcontract
  simpa [D] using
    NativeWeightedDiracBoundary.null_mode_kernel_half_dimension D K hD hK

/-- The nonconstant zero-symbol application also has equal half dimensions,
with the contraction role derived from the momentum. -/
theorem null_mode_kernel_half_dimension_of_nonzero_momentum
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : roleWeightedArchiveFourierSymbol N w k = 0) (hk : k ≠ 0) :
    2 * Module.finrank ℂ
        (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k)) =
      Module.finrank ℂ (ArchiveFockState → ℂ) := by
  obtain ⟨r, hforward⟩ := exists_role_with_nonzero_forward_multiplier N k hk
  exact null_mode_kernel_half_dimension N w k r hsymbol hforward

theorem archiveFockProfile_complex_finrank :
    Module.finrank ℂ (ArchiveFockState → ℂ) = 16 := by
  rw [Module.finrank_fintype_fun_eq_card, card_archive_fock_state]

/-- The zero-momentum Fourier fibre has no forward or backward difference,
so its actual profile operator is zero. -/
theorem roleWeightedArchiveFourierFockActionLinear_eq_zero_at_zero (N : ℕ)
    (w : Role → ℝ) :
    roleWeightedArchiveFourierFockActionLinear N w 0 = 0 := by
  apply LinearMap.ext
  intro v
  funext S
  simp [roleWeightedArchiveFourierFockActionLinear,
    archiveFourierForwardMultiplier, archiveFourierBackwardMultiplier,
    FiniteCycleFourier.cycleChar_zero_left]

/-- The zero momentum retains the entire sixteen-dimensional Fock kernel. -/
theorem roleWeightedArchiveFourierFockActionLinear_ker_finrank_at_zero (N : ℕ)
    (w : Role → ℝ) :
    Module.finrank ℂ
      (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w 0)) = 16 := by
  rw [roleWeightedArchiveFourierFockActionLinear_eq_zero_at_zero]
  rw [LinearMap.ker_zero, finrank_top, archiveFockProfile_complex_finrank]

/-- The explicit inverse of a non-null Fourier-fibre Dirac map. -/
noncomputable def roleWeightedArchiveFourierFockActionLinearInverse (N : ℕ)
    (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) :
    (ArchiveFockState → ℂ) →ₗ[ℂ] (ArchiveFockState → ℂ) :=
  (Complex.ofReal (roleWeightedArchiveFourierSymbol N w k))⁻¹ •
    roleWeightedArchiveFourierFockActionLinear N w k

/-- When the exact Fourier symbol is nonzero, the scaled Dirac map is a
two-sided inverse on the actual complex profile space. -/
theorem roleWeightedArchiveFourierFockActionLinear_inverse_spec
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : roleWeightedArchiveFourierSymbol N w k ≠ 0) :
    (roleWeightedArchiveFourierFockActionLinear N w k).comp
        (roleWeightedArchiveFourierFockActionLinearInverse N w k) = LinearMap.id ∧
    (roleWeightedArchiveFourierFockActionLinearInverse N w k).comp
        (roleWeightedArchiveFourierFockActionLinear N w k) = LinearMap.id := by
  let D := roleWeightedArchiveFourierFockActionLinear N w k
  let c : ℂ := Complex.ofReal (roleWeightedArchiveFourierSymbol N w k)
  have hc : c ≠ 0 := by
    dsimp [c]
    exact_mod_cast hsymbol
  have hsquare : D.comp D = c • LinearMap.id := by
    simpa [D, c] using roleWeightedArchiveFourierFockActionLinear_square N w k
  have hleft : D.comp (c⁻¹ • D) = LinearMap.id := by
    calc
      D.comp (c⁻¹ • D) = c⁻¹ • (D.comp D) := by rw [LinearMap.comp_smul]
      _ = c⁻¹ • (c • LinearMap.id) := by rw [hsquare]
      _ = LinearMap.id := by rw [smul_smul]; simp [hc]
  have hright : (c⁻¹ • D).comp D = LinearMap.id := by
    calc
      (c⁻¹ • D).comp D = c⁻¹ • (D.comp D) := by rw [LinearMap.smul_comp]
      _ = c⁻¹ • (c • LinearMap.id) := by rw [hsquare]
      _ = LinearMap.id := by rw [smul_smul]; simp [hc]
  constructor
  · simpa [roleWeightedArchiveFourierFockActionLinearInverse, D, c] using hleft
  · simpa [roleWeightedArchiveFourierFockActionLinearInverse, D, c] using hright

/-- A nonzero Fourier symbol makes the actual finite profile map injective. -/
theorem roleWeightedArchiveFourierFockActionLinear_ker_eq_bot_of_nonzero_symbol
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : roleWeightedArchiveFourierSymbol N w k ≠ 0) :
    LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k) = ⊥ := by
  apply LinearMap.ker_eq_bot.mpr
  intro v u huv
  have hinv := roleWeightedArchiveFourierFockActionLinear_inverse_spec N w k hsymbol
  have hcancel := congrArg (roleWeightedArchiveFourierFockActionLinearInverse N w k) huv
  have hrestore (x : ArchiveFockState → ℂ) :
      roleWeightedArchiveFourierFockActionLinearInverse N w k
          (roleWeightedArchiveFourierFockActionLinear N w k x) = x := by
    have h := congrArg (fun T : (ArchiveFockState → ℂ) →ₗ[ℂ]
        (ArchiveFockState → ℂ) => T x) hinv.2
    simpa [LinearMap.comp_apply, LinearMap.id_apply] using h
  calc
    v = roleWeightedArchiveFourierFockActionLinearInverse N w k
        (roleWeightedArchiveFourierFockActionLinear N w k v) := (hrestore v).symm
    _ = roleWeightedArchiveFourierFockActionLinearInverse N w k
        (roleWeightedArchiveFourierFockActionLinear N w k u) := hcancel
    _ = u := hrestore u

/-- The non-null fibre therefore has zero-dimensional complex kernel. -/
theorem roleWeightedArchiveFourierFockActionLinear_ker_finrank_zero_of_nonzero_symbol
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : roleWeightedArchiveFourierSymbol N w k ≠ 0) :
    Module.finrank ℂ
      (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k)) = 0 := by
  rw [roleWeightedArchiveFourierFockActionLinear_ker_eq_bot_of_nonzero_symbol
    N w k hsymbol]
  simp

/-- Exact eight-dimensional complex kernel for every supplied zero-symbol
fibre with a nonzero forward multiplier. -/
theorem null_mode_kernel_finrank
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) (r : Role)
    (hsymbol : roleWeightedArchiveFourierSymbol N w k = 0)
    (hforward : archiveFourierForwardMultiplier N k r ≠ 0) :
    Module.finrank ℂ
      (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k)) = 8 := by
  have h := null_mode_kernel_half_dimension N w k r hsymbol hforward
  rw [archiveFockProfile_complex_finrank] at h
  omega

/-- Exact eight-dimensional complex kernel on every supplied nonconstant
zero-symbol archive Fourier fibre. The role needed for the CAR contraction is
constructed from nonzero momentum. -/
theorem null_mode_kernel_finrank_of_nonzero_momentum
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : roleWeightedArchiveFourierSymbol N w k = 0) (hk : k ≠ 0) :
    Module.finrank ℂ
      (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k)) = 8 := by
  obtain ⟨r, hforward⟩ := exists_role_with_nonzero_forward_multiplier N k hk
  exact null_mode_kernel_finrank N w k r hsymbol hforward

/-- Complete per-fibre complex kernel-dimension classification for the
role-weighted operator: zero momentum contributes 16, nonconstant null fibres
contribute 8, and non-null fibres contribute 0. -/
theorem roleWeightedArchiveFourierFockActionLinear_kernel_finrank_cases
    (N : ℕ) (w : Role → ℝ) (k : Role → ZMod (archiveFibers N)) :
    Module.finrank ℂ
        (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N w k)) =
      if k = 0 then 16 else
        if roleWeightedArchiveFourierSymbol N w k = 0 then 8 else 0 := by
  by_cases hk : k = 0
  · subst k
    simp [roleWeightedArchiveFourierFockActionLinear_ker_finrank_at_zero]
  · by_cases hsymbol : roleWeightedArchiveFourierSymbol N w k = 0
    · rw [if_neg hk, if_pos hsymbol]
      exact null_mode_kernel_finrank_of_nonzero_momentum N w k hsymbol hk
    · rw [if_neg hk, if_neg hsymbol]
      exact roleWeightedArchiveFourierFockActionLinear_ker_finrank_zero_of_nonzero_symbol
        N w k hsymbol

/-- The same three-case kernel-dimension theorem specialized to the
repository's exact role signs and Eq. (5) symbol. -/
theorem archiveLorentzian_kernel_finrank_cases
    (N : ℕ) (k : Role → ZMod (archiveFibers N)) :
    Module.finrank ℂ
        (LinearMap.ker
          (roleWeightedArchiveFourierFockActionLinear N roleLorentzSign k)) =
      if k = 0 then 16 else
        if archiveLorentzianFourierSymbol N k = 0 then 8 else 0 := by
  simpa [roleWeightedArchiveFourierSymbol_lorentzian] using
    roleWeightedArchiveFourierFockActionLinear_kernel_finrank_cases
      N roleLorentzSign k

/-- Eq. (7)'s kernel/range and rank-eight conclusion for the repository's
role-signed archive Fourier operator, conditional on its exact Eq. (5) null
symbol and a nonzero product momentum. -/
theorem archiveLorentzian_nonzero_null_mode_classification
    (N : ℕ) (k : Role → ZMod (archiveFibers N))
    (hsymbol : archiveLorentzianFourierSymbol N k = 0) (hk : k ≠ 0) :
    LinearMap.ker
        (roleWeightedArchiveFourierFockActionLinear N roleLorentzSign k) =
      LinearMap.range
        (roleWeightedArchiveFourierFockActionLinear N roleLorentzSign k) ∧
    Module.finrank ℂ
        (LinearMap.ker (roleWeightedArchiveFourierFockActionLinear N roleLorentzSign k)) = 8 ∧
    Module.finrank ℂ
        (LinearMap.range (roleWeightedArchiveFourierFockActionLinear N roleLorentzSign k)) = 8 := by
  have hweighted : roleWeightedArchiveFourierSymbol N roleLorentzSign k = 0 := by
    rw [roleWeightedArchiveFourierSymbol_lorentzian]
    exact hsymbol
  have hker := null_mode_kernel_eq_range_of_nonzero_momentum
    N roleLorentzSign k hweighted hk
  have hker_dim := null_mode_kernel_finrank_of_nonzero_momentum
    N roleLorentzSign k hweighted hk
  refine ⟨hker, hker_dim, ?_⟩
  rw [← hker]
  exact hker_dim

end

end D0.Research.NativeWeightedDiracFourierNullModes
