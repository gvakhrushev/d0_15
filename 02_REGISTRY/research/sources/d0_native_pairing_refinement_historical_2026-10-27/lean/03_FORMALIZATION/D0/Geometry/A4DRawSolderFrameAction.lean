import Mathlib.Tactic
import D0.Geometry.A4DSolderMetricCompletion
import D0.Geometry.A4DPathCovariantHodge

/-!
# Raw solder frame action and centering defect

The frame acts on the uncentered solder field at each site.  Centering is a
separate averaging operation, and its failure to commute with a varying frame
is recorded exactly.  No raw field is replaced by its centered readout.
-/

namespace D0.Geometry

open D0
noncomputable section

/-- Right action on raw row/coframe data, with site fixed. -/
def rawCoframeFrameAction (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ) : LocalCoframeField N :=
  fun x r a => ∑ b : Role, e x r b * Λ x b a

/-- The raw solder matrix retains the uncentered coframe at the indicated site. -/
def rawSolderMatrix (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  fun r a => roleLorentzMetric r a + e x r a

/-- Active right frame action on the *whole* uncentered solder, including its
flat background.  Subtracting `eta` returns the perturbation coordinates. -/
def rawFullSolderFrameAction (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ) : LocalCoframeField N :=
  fun x r a => (rawSolderMatrix N e x * Λ x) r a - roleLorentzMetric r a

theorem rawFullSolderFrameAction_matrix (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N (rawFullSolderFrameAction N e Λ) x =
      rawSolderMatrix N e x * Λ x := by
  ext r a
  simp [rawSolderMatrix, rawFullSolderFrameAction]

/-- A row covector acts on the right by `Λ`; its paired vector acts by a
right inverse `K`.  This is a common-fibre statement at a fixed site. -/
theorem rawSolder_row_vector_pairing (Θ Λ K : Matrix Role Role ℝ)
    (hK : Λ * K = 1) (v : Role → ℝ) :
    (Θ * Λ).mulVec (K.mulVec v) = Θ.mulVec v := by
  rw [Matrix.mulVec_mulVec, Matrix.mul_assoc, hK,
    Matrix.mul_one]

/-- Pointwise transported centered field. -/
def transportedCenteredCoframe (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  fun r a => ∑ b : Role, centeredCoframeMatrix N e x r b * Λ x b a

/-- The pointwise-varying frame centering defect. -/
def centeredFrameDefect (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  centeredCoframeMatrix N (rawCoframeFrameAction N e Λ) x -
    transportedCenteredCoframe N e Λ x

theorem rawCoframeFrameAction_site (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) :
    rawCoframeFrameAction N e Λ x =
      fun r a => ∑ b : Role, e x r b * Λ x b a := rfl

theorem rawSolderMatrix_frame (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) :
    rawSolderMatrix N (rawCoframeFrameAction N e Λ) x =
      fun r a => roleLorentzMetric r a + ∑ b : Role, e x r b * Λ x b a := rfl

/-- Exact defect: only the remote endpoint contributes, because the center is
the backward two-point average. -/
theorem centeredFrameDefect_endpoint_formula (N : ℕ)
    (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) :
    centeredFrameDefect N e Λ x = fun r a =>
      (∑ b : Role, e (roleTranslateMinus N r x) r b *
        (Λ (roleTranslateMinus N r x) b a - Λ x b a)) / 2 := by
  ext r a
  simp [centeredFrameDefect, transportedCenteredCoframe, centeredCoframeMatrix,
    rawCoframeFrameAction, backwardAverage]
  let u : Role → ℝ := fun b => e x r b
  let v : Role → ℝ := fun b => e (roleTranslateMinus N r x) r b
  let w : Role → ℝ := fun b => Λ x b a
  let w' : Role → ℝ := fun b => Λ (roleTranslateMinus N r x) b a
  have hc : (∑ b : Role, (u b + v b) / 2 * w b) =
      ((∑ b : Role, u b * w b) + (∑ b : Role, v b * w b)) / 2 := by
    calc
      _ = ∑ b : Role, (u b * w b + v b * w b) / 2 := by
        apply Finset.sum_congr rfl
        intro b hb
        ring
      _ = _ := by rw [← Finset.sum_add_distrib, Finset.sum_div]
  have hd : (∑ b : Role, v b * (w' b - w b)) / 2 =
      ((∑ b : Role, v b * w' b) - (∑ b : Role, v b * w b)) / 2 := by
    congr 1
    simp_rw [mul_sub]
    rw [Finset.sum_sub_distrib]
  simp only [u, v, w, w'] at hc hd
  rw [hc, hd]
  ring

/-- Transported-center repair identity: the centered value after a varying
sitewise frame is the pointwise transport of the old centered value plus the
explicit endpoint defect. -/
theorem centeredFrameDefect_transport_repair (N : ℕ)
    (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N (rawCoframeFrameAction N e Λ) x =
      transportedCenteredCoframe N e Λ x + centeredFrameDefect N e Λ x := by
  rw [centeredFrameDefect]
  ext r a
  simp [Matrix.add_apply, Matrix.sub_apply]

/-- A constant frame has no centering defect. -/
theorem centeredFrameDefect_constant (N : ℕ) (e : LocalCoframeField N)
    (Λ : Matrix Role Role ℝ) (x : ArchiveRolePhaseGroup N) :
    centeredFrameDefect N e (fun _ => Λ) x = 0 := by
  rw [centeredFrameDefect_endpoint_formula]
  ext r a
  simp

/-- A pointwise Lorentz frame leaves the raw solder Gram unchanged.  The input
is already soldered; this is the established right-action identity. -/
theorem rawSolderGram_frame_invariant (Θ Λ : Matrix Role Role ℝ)
    (hΛ : IsRoleLorentz Λ) :
    (Θ * Λ) * roleLorentzMetric * (Θ * Λ).transpose =
      Θ * roleLorentzMetric * Θ.transpose :=
  solderGram_right_lorentz_invariant Θ Λ hΛ

/-- Transported center `Θ̂_r(x) = ½ (E_r(x) + E_r(x−r) R_{x−r→x})`.
`R` is a row pull into the indicated site, not an affine Cartan shift. -/
def transportedSolderCenter (N : ℕ)
    (E : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (Rpull : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  fun r a =>
    (E x r a +
      (E (roleTranslateMinus N r x) * Rpull (roleTranslateMinus N r x) r) r a) / 2

/-- If the row pull transforms by `R' = Λ_{x−r}⁻¹ R Λ_x`, the transported
center transforms by the same right frame as the raw solder. -/
theorem transportedSolderCenter_covariance (N : ℕ)
    (E : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (Rpull Rpull' : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N)
    (hΛ : ∀ y, IsUnit (Λ y).det)
    (hR : ∀ r, Rpull' (roleTranslateMinus N r x) r =
      (Λ (roleTranslateMinus N r x))⁻¹ * Rpull (roleTranslateMinus N r x) r * Λ x) :
    transportedSolderCenter N (fun y => E y * Λ y) Rpull' x =
      transportedSolderCenter N E Rpull x * Λ x := by
  ext r a
  let y := roleTranslateMinus N r x
  have hy : IsUnit (Λ y).det := hΛ y
  have hcancel : Λ y * (Λ y)⁻¹ = 1 := Matrix.mul_nonsing_inv (Λ y) hy
  have hpull : E y * Λ y * Rpull' y r = E y * Rpull y r * Λ x := by
    rw [hR r]
    calc
      E y * Λ y * ((Λ y)⁻¹ * Rpull y r * Λ x) =
          E y * (Λ y * ((Λ y)⁻¹ * Rpull y r * Λ x)) := by rw [Matrix.mul_assoc]
      _ = E y * (Λ y * ((Λ y)⁻¹ * Rpull y r) * Λ x) := by
            rw [← Matrix.mul_assoc (Λ y) ((Λ y)⁻¹ * Rpull y r) (Λ x)]
      _ = E y * ((Λ y * (Λ y)⁻¹) * Rpull y r * Λ x) := by
            rw [← Matrix.mul_assoc (Λ y) ((Λ y)⁻¹) (Rpull y r)]
      _ = E y * (1 * Rpull y r * Λ x) := by rw [hcancel]
      _ = E y * (Rpull y r * Λ x) := by rw [Matrix.one_mul]
      _ = E y * Rpull y r * Λ x := by rw [← Matrix.mul_assoc]
  have hdiv (t : Role → ℝ) :
      (∑ b : Role, (t b / 2) * Λ x b a) = (∑ b : Role, t b * Λ x b a) / 2 := by
    have hterm : ∀ b, (t b / 2) * Λ x b a = (t b * Λ x b a) * (2 : ℝ)⁻¹ := by
      intro b
      rw [div_mul_eq_mul_div, div_eq_mul_inv]
    rw [Finset.sum_congr rfl (fun b _ => hterm b), div_eq_mul_inv]
    exact (Finset.sum_mul Finset.univ (fun b => t b * Λ x b a) ((2 : ℝ)⁻¹)).symm
  calc
    transportedSolderCenter N (fun z => E z * Λ z) Rpull' x r a =
        ((E x * Λ x) r a + ((E y * Λ y) * Rpull' y r) r a) / 2 := by
          rfl
    _ = ((E x * Λ x) r a + (E y * Rpull y r * Λ x) r a) / 2 := by
          rw [show (E y * Λ y) * Rpull' y r = E y * Rpull y r * Λ x from hpull]
    _ = (∑ b : Role, (E x r b + (E y * Rpull y r) r b) * Λ x b a) / 2 := by
          refine congrArg (fun z => z / 2) ?_
          rw [Matrix.mul_apply, Matrix.mul_apply, ← Finset.sum_add_distrib]
          refine Finset.sum_congr rfl ?_
          intro b _
          exact (add_mul (E x r b) ((E y * Rpull y r) r b) (Λ x b a)).symm
    _ = ∑ b : Role, ((E x r b + (E y * Rpull y r) r b) / 2) * Λ x b a :=
          (hdiv (fun b => E x r b + (E y * Rpull y r) r b)).symm
    _ = (transportedSolderCenter N E Rpull x * Λ x) r a := by
          rw [Matrix.mul_apply]
          refine Finset.sum_congr rfl ?_
          intro b _
          rfl

theorem rawTransportedCenter_covariance (N : ℕ) (e : LocalCoframeField N)
    (Λ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (Rpull Rpull' : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N)
    (hΛ : ∀ y, IsUnit (Λ y).det)
    (hR : ∀ r, Rpull' (roleTranslateMinus N r x) r =
      (Λ (roleTranslateMinus N r x))⁻¹ * Rpull (roleTranslateMinus N r x) r * Λ x) :
    transportedSolderCenter N
        (fun y => rawSolderMatrix N (rawFullSolderFrameAction N e Λ) y) Rpull' x =
      transportedSolderCenter N (fun y => rawSolderMatrix N e y) Rpull x * Λ x := by
  have hE : (fun y => rawSolderMatrix N (rawFullSolderFrameAction N e Λ) y) =
      fun y => rawSolderMatrix N e y * Λ y := by
    funext y
    exact rawFullSolderFrameAction_matrix N e Λ y
  rw [hE]
  exact transportedSolderCenter_covariance N (fun y => rawSolderMatrix N e y) Λ Rpull Rpull' x hΛ hR

/-- The raw L=2 Nyquist coframe remains an explicit nonzero field even though
its centered solder readout vanishes. -/
theorem rawNyquist_is_not_centered_data :
    periodTwoNyquistCoframe 0 A A = -2 ∧
      (∀ x : ArchiveRolePhaseGroup 0,
        centeredCoframeMatrix 0 periodTwoNyquistCoframe x = 0) := by
  refine ⟨?_, periodTwoNyquist_centeredCoframe_zero⟩
  norm_num [periodTwoNyquistCoframe, A]

end
end D0.Geometry
