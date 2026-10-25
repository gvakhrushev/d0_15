import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.ArchiveRoleEquivalence
import D0.Algebra.FiniteGramTangent
import Mathlib.Analysis.Calculus.FDeriv.Pow
import Mathlib.Analysis.Matrix.Normed

/-!
# Finite solder Gram completion of the centered coframe readout

The exact polynomial tangent is the existing `coframeMetricReadout`. The right
Lorentz action is on solder matrices, not a claimed action on pre-centered
coframes. The Gram matrix can be degenerate for arbitrary perturbations. No
physical metric, Cartan connection, constitutive law, nonlinear diffeomorphism
covariance, or observer representation is asserted.

Directional centering does not preserve arbitrary sitewise skew fields.
Readout-nullity below is unconditional for constant frame directions and
conditional on a literal centered lift for variable directions. No odd-cycle
kernel equality or removal of the even-cycle Nyquist residue is asserted.

Every symmetric Role-matrix direction is attained at every site by one
constant coframe field. The resulting nonlinear metric path has the exact
quadratic remainder recorded below; this is finite algebra, not a physical
metric selection or continuum field equation.
-/

namespace D0.Geometry
open D0
open scoped BigOperators
noncomputable section

def roleLorentzSign (r : Role) : ℝ := (roleSign (roleRoleSigEquiv r) : ℝ)
@[simp] theorem roleLorentzSign_A : roleLorentzSign A = 1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_A, roleSign]
@[simp] theorem roleLorentzSign_B : roleLorentzSign B = -1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_B, roleSign]
@[simp] theorem roleLorentzSign_C : roleLorentzSign C = -1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_C, roleSign]
@[simp] theorem roleLorentzSign_D : roleLorentzSign D = -1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_D, roleSign]

theorem roleLorentzSign_mul_self (r : Role) : roleLorentzSign r * roleLorentzSign r = 1 := by
  rcases r with ⟨a,b⟩
  fin_cases a <;> fin_cases b <;> norm_num [roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]

def roleLorentzMetric : Matrix Role Role ℝ := Matrix.diagonal roleLorentzSign
@[simp] theorem roleLorentzMetric_diagonal (r : Role) :
    roleLorentzMetric r r = roleLorentzSign r := Matrix.diagonal_apply_eq _ _
@[simp] theorem roleLorentzMetric_transpose : roleLorentzMetric.transpose = roleLorentzMetric := by
  exact Matrix.diagonal_transpose _
@[simp] theorem roleLorentzMetric_sq : roleLorentzMetric * roleLorentzMetric = 1 := by
  rw [roleLorentzMetric, Matrix.diagonal_mul_diagonal]
  simp only [roleLorentzSign_mul_self]
  exact Matrix.diagonal_one

/-- Row r is centered along the existing backward r-link average. -/
def centeredCoframeMatrix (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  fun r a => backwardAverage N r (fun y => e y r a) x
@[simp] theorem centeredCoframeMatrix_apply (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    centeredCoframeMatrix N e x r a = backwardAverage N r (fun y => e y r a) x := rfl

theorem coframeMetricReadout_eq_centered_add_transpose (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    (coframeMetricReadout N e x).toMatrix =
      centeredCoframeMatrix N e x + (centeredCoframeMatrix N e x).transpose := rfl
@[simp] theorem centeredCoframeMatrix_zero (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N 0 x = 0 := by
  ext r a
  simp [centeredCoframeMatrix, backwardAverage]

@[simp] theorem centeredCoframeMatrix_constant (N : ℕ)
    (C : Matrix Role Role ℝ) (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N (fun _ r a => C r a) x = C := by
  ext r a
  simp [centeredCoframeMatrix, backwardAverage]

@[simp] theorem centeredCoframeMatrix_smul (N : ℕ) (e : LocalCoframeField N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N (t • e) x = t • centeredCoframeMatrix N e x := by
  ext r a
  simp [centeredCoframeMatrix, backwardAverage]
  ring

def solderMatrix (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    Matrix Role Role ℝ := roleLorentzMetric + centeredCoframeMatrix N e x
@[simp] theorem solderMatrix_zero (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    solderMatrix N 0 x = roleLorentzMetric := by simp [solderMatrix]

/-- Nonlinear candidate; nondegeneracy is not automatic for arbitrary e. -/
def solderMetricMatrix (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    Matrix Role Role ℝ := D0.Algebra.finiteGram roleLorentzMetric (solderMatrix N e x)

theorem solderMetric_symmetric (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    (solderMetricMatrix N e x).transpose = solderMetricMatrix N e x := by
  exact D0.Algebra.finiteGram_symmetric roleLorentzMetric (solderMatrix N e x)
    roleLorentzMetric_transpose

theorem solderMetric_expand (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N e x = roleLorentzMetric + centeredCoframeMatrix N e x +
      (centeredCoframeMatrix N e x).transpose +
      centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose := by
  rw [solderMetricMatrix, solderMatrix]
  have hExpand := D0.Algebra.finiteGram_smul_expand roleLorentzMetric
    (centeredCoframeMatrix N e x) (1 : ℝ)
    roleLorentzMetric_transpose roleLorentzMetric_sq
  simp only [one_smul, one_pow] at hExpand
  rw [hExpand]
  abel

theorem solderMetric_minus_background (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N e x - roleLorentzMetric = (coframeMetricReadout N e x).toMatrix +
      centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose := by
  rw [solderMetric_expand, coframeMetricReadout_eq_centered_add_transpose]
  abel

/-- Exact algebraic flat tangent: the linear coefficient is the frozen readout. -/
theorem solderMetric_smul_expand (N : ℕ) (e : LocalCoframeField N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (t • e) x - roleLorentzMetric =
      t • (coframeMetricReadout N e x).toMatrix + t^2 •
        (centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose) := by
  rw [solderMetricMatrix, solderMatrix, centeredCoframeMatrix_smul]
  rw [D0.Algebra.finiteGram_smul_expand roleLorentzMetric
    (centeredCoframeMatrix N e x) t roleLorentzMetric_transpose roleLorentzMetric_sq]
  rw [coframeMetricReadout_eq_centered_add_transpose]
  abel

/-- Difference quotient with its exact remainder, requiring no calculus API. -/
theorem solderMetric_flat_tangent (N : ℕ) (e : LocalCoframeField N)
    (t : ℝ) (ht : t ≠ 0) (x : ArchiveRolePhaseGroup N) :
    t⁻¹ • (solderMetricMatrix N (t • e) x - roleLorentzMetric) =
      (coframeMetricReadout N e x).toMatrix + t •
        (centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose) := by
  rw [solderMetric_smul_expand]
  simp [smul_add, smul_smul, pow_two, ht]

/-- Every symmetric metric direction is the readout of one constant coframe
field at every site. The witness is explicit: its components are `q/2`.
This is a surjectivity statement for the finite linear readout only. -/
theorem coframeMetricReadout_realizes_symmetric (N : ℕ)
    (q : Matrix Role Role ℝ) (hq : q.transpose = q) :
    ∃ e : LocalCoframeField N,
      ∀ x : ArchiveRolePhaseGroup N, (coframeMetricReadout N e x).toMatrix = q := by
  let C : Matrix Role Role ℝ := (2 : ℝ)⁻¹ • q
  refine ⟨fun _ r a => C r a, ?_⟩
  intro x
  rw [coframeMetricReadout_eq_centered_add_transpose]
  rw [centeredCoframeMatrix_constant]
  simpa [C] using D0.Algebra.symmetricMatrix_half q hq

/-- Exact composition of the finite symmetric-direction witness with the
nonlinear solder Gram path. Every symmetric `q` is its linear coefficient,
and the only finite-parameter error is the displayed quadratic term. -/
theorem solderMetric_realizes_symmetric_tangent (N : ℕ)
    (q : Matrix Role Role ℝ) (hq : q.transpose = q) :
    ∃ e : LocalCoframeField N,
      (∀ x : ArchiveRolePhaseGroup N,
        (coframeMetricReadout N e x).toMatrix = q) ∧
      (∀ x : ArchiveRolePhaseGroup N, ∀ t : ℝ,
        solderMetricMatrix N (t • e) x - roleLorentzMetric =
          t • q + t^2 •
            (centeredCoframeMatrix N e x * roleLorentzMetric *
              (centeredCoframeMatrix N e x).transpose)) ∧
      (∀ x : ArchiveRolePhaseGroup N, ∀ t : ℝ, t ≠ 0 →
        t⁻¹ • (solderMetricMatrix N (t • e) x - roleLorentzMetric) =
          q + t • (centeredCoframeMatrix N e x * roleLorentzMetric *
            (centeredCoframeMatrix N e x).transpose)) := by
  obtain ⟨e, he⟩ := coframeMetricReadout_realizes_symmetric N q hq
  refine ⟨e, he, ?_, ?_⟩
  · intro x t
    rw [solderMetric_smul_expand, he x]
  · intro x t ht
    rw [solderMetric_flat_tangent N e t ht x, he x]

/-! ## Source-convention adapter for the nonlinear J² metric tangent

The pinned J² bridge writes its flat metric coordinate as
`Q(Θ) = Θ η Θᵀ`, with source perturbation `Θ = 1 + H` and
`H(q) = q η / 2`. The existing finite solder carrier uses the equivalent
right-`η` frame `Θ' = Θ η`; its perturbation is therefore `E = H η = q/2`.
The lemmas below prove this exact reindexing and retain the quadratic
remainder. They do not prove that the selected finite action supplies this
carrier, its nondegeneracy premise, or a physical source/metric selection.
-/

/-- The pinned flat-frame metric convention `Q(1 + H) = (1 + H)η(1 + H)ᵀ`. -/
def j2DetectorMetricPath (H : Matrix Role Role ℝ) : Matrix Role Role ℝ :=
  D0.Algebra.finiteGram roleLorentzMetric (1 + H)

theorem j2DetectorMetricPath_smul_expand (H : Matrix Role Role ℝ) (t : ℝ) :
    j2DetectorMetricPath (t • H) =
      roleLorentzMetric + t • (H * roleLorentzMetric + roleLorentzMetric * H.transpose) +
        t^2 • (H * roleLorentzMetric * H.transpose) := by
  exact D0.Algebra.finiteGram_one_smul_expand roleLorentzMetric H t

/-- The coframe perturbation used by the pinned #201 detector convention. -/
def j2DetectorCoframeDirection (q : Matrix Role Role ℝ) : Matrix Role Role ℝ :=
  ((2 : ℝ)⁻¹ • q) * roleLorentzMetric

theorem j2DetectorCoframeDirection_right_eta (q : Matrix Role Role ℝ) :
    j2DetectorCoframeDirection q * roleLorentzMetric = (2 : ℝ)⁻¹ • q := by
  dsimp [j2DetectorCoframeDirection]
  rw [Matrix.mul_assoc, roleLorentzMetric_sq, Matrix.mul_one]

theorem j2DetectorCoframeDirection_metric_tangent (q : Matrix Role Role ℝ)
    (hq : q.transpose = q) :
    j2DetectorCoframeDirection q * roleLorentzMetric +
      roleLorentzMetric * (j2DetectorCoframeDirection q).transpose = q := by
  have hleft := j2DetectorCoframeDirection_right_eta q
  have hright : roleLorentzMetric * (j2DetectorCoframeDirection q).transpose =
      (2 : ℝ)⁻¹ • q := by
    dsimp [j2DetectorCoframeDirection]
    rw [Matrix.transpose_mul, Matrix.transpose_smul, roleLorentzMetric_transpose, hq]
    rw [← Matrix.mul_assoc, roleLorentzMetric_sq, Matrix.one_mul]
  calc
    _ = (2 : ℝ)⁻¹ • q + (2 : ℝ)⁻¹ • q := by rw [hleft, hright]
    _ = q := by
      simpa [Matrix.transpose_smul, hq] using D0.Algebra.symmetricMatrix_half q hq

/-- The pinned symmetric metric direction has the exact finite J² expansion;
the displayed quadratic term is retained rather than discarded. -/
theorem j2DetectorMetricPath_symmetric_tangent (q : Matrix Role Role ℝ)
    (hq : q.transpose = q) (t : ℝ) :
    j2DetectorMetricPath (t • j2DetectorCoframeDirection q) =
      roleLorentzMetric + t • q + t^2 •
        (j2DetectorCoframeDirection q * roleLorentzMetric *
          (j2DetectorCoframeDirection q).transpose) := by
  rw [j2DetectorMetricPath_smul_expand,
    j2DetectorCoframeDirection_metric_tangent q hq]

theorem j2DetectorMetricPath_symmetric_difference_quotient
    (q : Matrix Role Role ℝ) (hq : q.transpose = q) (t : ℝ) (ht : t ≠ 0) :
    t⁻¹ • (j2DetectorMetricPath (t • j2DetectorCoframeDirection q) -
      roleLorentzMetric) =
      q + t • (j2DetectorCoframeDirection q * roleLorentzMetric *
        (j2DetectorCoframeDirection q).transpose) := by
  rw [j2DetectorMetricPath_symmetric_tangent q hq t]
  have hcancel : roleLorentzMetric + t • q + t^2 •
      (j2DetectorCoframeDirection q * roleLorentzMetric *
        (j2DetectorCoframeDirection q).transpose) - roleLorentzMetric =
      t • q + t^2 • (j2DetectorCoframeDirection q * roleLorentzMetric *
        (j2DetectorCoframeDirection q).transpose) := by
    abel
  rw [hcancel]
  simp [smul_add, smul_smul, pow_two, ht]

section J2MetricPathDerivative

local instance : NormedAddCommGroup (Matrix Role Role ℝ) := Matrix.normedAddCommGroup
local instance : NormedSpace ℝ (Matrix Role Role ℝ) := Matrix.normedSpace

/-- Directional Fréchet derivative of the source Gram path at the flat frame.
The derivative map sends a scalar path parameter to that scalar times the
full linear coefficient; the exact quadratic remainder gives the limit. -/
theorem j2DetectorMetricPath_hasFDerivAt_direction (H : Matrix Role Role ℝ) :
    HasFDerivAt (fun t : ℝ => j2DetectorMetricPath (t • H))
      ((1 : ℝ →L[ℝ] ℝ).smulRight
        (H * roleLorentzMetric + roleLorentzMetric * H.transpose)) 0 := by
  let L : Matrix Role Role ℝ := H * roleLorentzMetric + roleLorentzMetric * H.transpose
  let R : Matrix Role Role ℝ := H * roleLorentzMetric * H.transpose
  have hlinear : HasFDerivAt (fun t : ℝ => t • L)
      ((1 : ℝ →L[ℝ] ℝ).smulRight L) 0 := by
    simpa using (hasFDerivAt_id (0 : ℝ)).smul_const L
  have hpow : HasFDerivAt (fun t : ℝ => t ^ 2)
      (0 : ℝ →L[ℝ] ℝ) 0 := by
    simpa using (hasFDerivAt_pow (𝕜 := ℝ) 2 (x := (0 : ℝ)))
  have hquadratic : HasFDerivAt (fun t : ℝ => t ^ 2 • R)
      (0 : ℝ →L[ℝ] Matrix Role Role ℝ) 0 := by
    simpa using hpow.smul_const R
  have hconstant : HasFDerivAt (fun _ : ℝ => roleLorentzMetric)
      (0 : ℝ →L[ℝ] Matrix Role Role ℝ) 0 :=
    hasFDerivAt_const _ _
  have hpolynomial_eq :
      (fun t : ℝ => roleLorentzMetric + t • L + t ^ 2 • R) =
        ((fun _ : ℝ => roleLorentzMetric) + (fun t : ℝ => t • L) +
          (fun t : ℝ => t ^ 2 • R)) := by
    funext t
    rfl
  have hpolynomial_sum := (hconstant.add hlinear).add hquadratic
  have hpolynomial : HasFDerivAt
      (fun t : ℝ => roleLorentzMetric + t • L + t ^ 2 • R)
      ((1 : ℝ →L[ℝ] ℝ).smulRight L) 0 := by
    rw [hpolynomial_eq]
    exact hpolynomial_sum.congr_fderiv (by abel)
  have hpath : (fun t : ℝ => j2DetectorMetricPath (t • H)) =
      (fun t : ℝ => roleLorentzMetric + t • L + t ^ 2 • R) := by
    funext t
    dsimp [L, R]
    exact j2DetectorMetricPath_smul_expand H t
  rw [hpath]
  exact hpolynomial

/-- On the pinned symmetric direction `H(q)=qη/2`, the directional
derivative above evaluates to `q`. -/
theorem j2DetectorMetricPath_hasFDerivAt_symmetric_direction
    (q : Matrix Role Role ℝ) (hq : q.transpose = q) :
    HasFDerivAt
      (fun t : ℝ => j2DetectorMetricPath (t • j2DetectorCoframeDirection q))
      ((1 : ℝ →L[ℝ] ℝ).smulRight q) 0 := by
  have h := j2DetectorMetricPath_hasFDerivAt_direction
    (j2DetectorCoframeDirection q)
  rw [j2DetectorCoframeDirection_metric_tangent q hq] at h
  exact h

end J2MetricPathDerivative

/-- The role-indexed solder carrier is the pinned flat-frame carrier after
right multiplication by `η`, which is an exact Lorentz isometry. -/
theorem solderMetricMatrix_constant_j2DetectorMetricPath
    (N : ℕ) (H : Matrix Role Role ℝ) (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (t • fun _ r a => (H * roleLorentzMetric) r a) x =
      j2DetectorMetricPath (t • H) := by
  have hframe : roleLorentzMetric + t • (H * roleLorentzMetric) =
      (1 + t • H) * roleLorentzMetric := by
    simp [Matrix.add_mul]
  have hη_isometry : roleLorentzMetric * roleLorentzMetric *
      roleLorentzMetric.transpose = roleLorentzMetric := by
    simp [roleLorentzMetric_transpose, roleLorentzMetric_sq]
  calc
    solderMetricMatrix N (t • fun _ r a => (H * roleLorentzMetric) r a) x =
        D0.Algebra.finiteGram roleLorentzMetric
          (roleLorentzMetric + t • (H * roleLorentzMetric)) := by
      simp [solderMetricMatrix, solderMatrix, centeredCoframeMatrix_smul,
        centeredCoframeMatrix_constant]
    _ = D0.Algebra.finiteGram roleLorentzMetric ((1 + t • H) * roleLorentzMetric) := by
      rw [hframe]
    _ = D0.Algebra.finiteGram roleLorentzMetric (1 + t • H) :=
      D0.Algebra.finiteGram_right_invariant roleLorentzMetric (1 + t • H)
        roleLorentzMetric hη_isometry
    _ = j2DetectorMetricPath (t • H) := rfl

/-- An explicit Lean adapter from the source's `q` direction into the existing
finite solder readout and nonlinear Gram path. -/
theorem j2DetectorMetricPath_symmetric_solder_adapter (N : ℕ)
    (q : Matrix Role Role ℝ) (hq : q.transpose = q) :
    ∃ e : LocalCoframeField N,
      (∀ x : ArchiveRolePhaseGroup N, (coframeMetricReadout N e x).toMatrix = q) ∧
      (∀ x : ArchiveRolePhaseGroup N, ∀ t : ℝ,
        solderMetricMatrix N (t • e) x =
          j2DetectorMetricPath (t • j2DetectorCoframeDirection q)) := by
  let H : Matrix Role Role ℝ := j2DetectorCoframeDirection q
  have hleft : H * roleLorentzMetric = (2 : ℝ)⁻¹ • q := by
    dsimp [H, j2DetectorCoframeDirection]
    rw [Matrix.mul_assoc, roleLorentzMetric_sq, Matrix.mul_one]
  refine ⟨fun _ r a => (H * roleLorentzMetric) r a, ?_, ?_⟩
  · intro x
    rw [coframeMetricReadout_eq_centered_add_transpose,
      centeredCoframeMatrix_constant, hleft]
    exact D0.Algebra.symmetricMatrix_half q hq
  · intro x t
    exact solderMetricMatrix_constant_j2DetectorMetricPath N H t x

theorem solderMetric_forwardGauge_flat_tangent (N : ℕ) (xi : LocalRoleVector N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (t • forwardGaugeCoframe N xi) x - roleLorentzMetric =
      t • (symmetricRoleGradient N xi x).toMatrix + t^2 •
        (centeredCoframeMatrix N (forwardGaugeCoframe N xi) x * roleLorentzMetric *
          (centeredCoframeMatrix N (forwardGaugeCoframe N xi) x).transpose) := by
  rw [solderMetric_smul_expand, coframeMetricReadout_forwardGauge]

def IsRoleLorentz (Λ : Matrix Role Role ℝ) : Prop :=
  Λ * roleLorentzMetric * Λ.transpose = roleLorentzMetric

/-- Right frame action on arbitrary solder matrices, pointwise at each site. -/
theorem solderGram_right_lorentz_invariant (Θ Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    (Θ * Λ) * roleLorentzMetric * (Θ * Λ).transpose = Θ * roleLorentzMetric * Θ.transpose := by
  simpa [D0.Algebra.finiteGram, IsRoleLorentz] using
    D0.Algebra.finiteGram_right_invariant roleLorentzMetric Θ Λ hΛ

/-- At the flat solder η, the right-action variation is ηa. -/
def IsRoleLorentzTangent (a : Matrix Role Role ℝ) : Prop :=
  a.transpose * roleLorentzMetric + roleLorentzMetric * a = 0

theorem lorentzTangent_flat_solder_skew (a : Matrix Role Role ℝ) (ha : IsRoleLorentzTangent a) :
    roleLorentzMetric * a + (roleLorentzMetric * a).transpose = 0 := by
  simpa [IsRoleLorentzTangent, Matrix.transpose_mul, add_comm] using ha

/-- The tangent convention also kills the linear term of ΛηΛᵀ.
This connects the ηa flat-solder variation to the finite right action above. -/
theorem lorentzTangent_right_condition (a : Matrix Role Role ℝ) (ha : IsRoleLorentzTangent a) :
    a * roleLorentzMetric + roleLorentzMetric * a.transpose = 0 := by
  have hsandwich :
      roleLorentzMetric * (a.transpose * roleLorentzMetric + roleLorentzMetric * a) *
          roleLorentzMetric = a * roleLorentzMetric + roleLorentzMetric * a.transpose := by
    rw [Matrix.mul_add, Matrix.add_mul]
    simp only [← Matrix.mul_assoc, roleLorentzMetric_sq, Matrix.one_mul]
    rw [Matrix.mul_assoc (roleLorentzMetric * a.transpose) roleLorentzMetric roleLorentzMetric,
      roleLorentzMetric_sq, Matrix.mul_one]
    abel
  rw [← hsandwich, ha]
  simp

/-- Variable frame fields are readout-null if a literal centered lift is supplied. -/
theorem lorentzTangent_centeredLift_readout_zero (N : ℕ) (e : LocalCoframeField N)
    (a : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (ha : ∀ x, IsRoleLorentzTangent (a x))
    (he : ∀ x, centeredCoframeMatrix N e x = roleLorentzMetric * a x) :
    ∀ x, (coframeMetricReadout N e x).toMatrix = 0 := by
  intro x
  rw [coframeMetricReadout_eq_centered_add_transpose, he]
  exact lorentzTangent_flat_solder_skew _ (ha x)

/-- Constant pre-centered frame directions genuinely lie in the frozen readout kernel. -/
theorem lorentzTangent_centeredReadout_zero (N : ℕ) (a : Matrix Role Role ℝ)
    (ha : IsRoleLorentzTangent a) :
    ∀ x, (coframeMetricReadout N (fun _ => roleLorentzMetric * a) x).toMatrix = 0 := by
  apply lorentzTangent_centeredLift_readout_zero N _ (fun _ => a) (fun _ => ha)
  intro x
  ext r s
  simp [centeredCoframeMatrix, backwardAverage]

/-! ## Exact six-dimensional Lorentz tangent space -/

/-- This is a frame tangent carrier, not the symmetric metric shear carrier. -/
def roleSkewMatrices : Submodule ℝ (Matrix Role Role ℝ) where
  carrier := {m | ∀ a b, m a b = -m b a}
  zero_mem' := by intro a b; simp
  add_mem' := by
    intro m n hm hn a b
    simp only [Matrix.add_apply, hm a b, hn a b]
    ring
  smul_mem' := by
    intro t m hm a b
    simp only [Matrix.smul_apply, smul_eq_mul, hm a b]
    ring

def roleLorentzTangentSpace : Submodule ℝ (Matrix Role Role ℝ) where
  carrier := {a | IsRoleLorentzTangent a}
  zero_mem' := by simp [IsRoleLorentzTangent]
  add_mem' := by
    intro a b ha hb
    change a.transpose * roleLorentzMetric + roleLorentzMetric * a = 0 at ha
    change b.transpose * roleLorentzMetric + roleLorentzMetric * b = 0 at hb
    change (a + b).transpose * roleLorentzMetric + roleLorentzMetric * (a + b) = 0
    simp only [Matrix.transpose_add, Matrix.add_mul, Matrix.mul_add]
    calc
      _ = (a.transpose * roleLorentzMetric + roleLorentzMetric * a) +
          (b.transpose * roleLorentzMetric + roleLorentzMetric * b) := by abel
      _ = 0 := by rw [ha, hb, add_zero]
  smul_mem' := by
    intro t a ha
    simpa [IsRoleLorentzTangent, Matrix.transpose_smul, Matrix.smul_mul, Matrix.mul_smul,
      ← smul_add] using congrArg (fun m => t • m) ha

abbrev RoleLorentzTangent := roleLorentzTangentSpace

def lorentzTangentEquivSkew : RoleLorentzTangent ≃ₗ[ℝ] roleSkewMatrices where
  toFun a := ⟨roleLorentzMetric * a.val, by
    intro r s
    have h := congrArg (fun m : Matrix Role Role ℝ => m r s)
      (lorentzTangent_flat_solder_skew a.val a.property)
    simp only [Matrix.add_apply, Matrix.transpose_apply, Matrix.zero_apply] at h
    linarith⟩
  invFun e := ⟨roleLorentzMetric * e.val, by
    change (roleLorentzMetric * e.val).transpose * roleLorentzMetric +
      roleLorentzMetric * (roleLorentzMetric * e.val) = 0
    rw [Matrix.transpose_mul, roleLorentzMetric_transpose,
      Matrix.mul_assoc e.val.transpose roleLorentzMetric roleLorentzMetric,
      roleLorentzMetric_sq, Matrix.mul_one, ← Matrix.mul_assoc,
      roleLorentzMetric_sq, Matrix.one_mul]
    ext r s
    have h := e.property r s
    simp only [Matrix.add_apply, Matrix.transpose_apply, Matrix.zero_apply]
    linarith⟩
  left_inv a := by apply Subtype.ext; simp [← Matrix.mul_assoc]
  right_inv e := by apply Subtype.ext; simp [← Matrix.mul_assoc]
  map_add' a b := by apply Subtype.ext; exact Matrix.mul_add _ _ _
  map_smul' t a := by apply Subtype.ext; exact Matrix.mul_smul _ _ _

/-- Six independent coordinates use RolePair only as a finite index set.
The resulting matrix is antisymmetric, never identified with symmetric shear. -/
def skewFromRolePairs (u : RolePair → ℝ) : Matrix Role Role ℝ :=
  fun a b => if h : a = b then 0 else
    if roleCode a < roleCode b then u (rolePairOfDistinct a b h)
    else -u (rolePairOfDistinct a b h)

theorem skewFromRolePairs_skew (u : RolePair → ℝ) : skewFromRolePairs u ∈ roleSkewMatrices := by
  intro a b
  by_cases h : a = b
  · subst b; simp [skewFromRolePairs]
  · have hcode : roleCode a ≠ roleCode b := fun he => h (roleCode_injective he)
    rcases lt_or_gt_of_ne hcode with hab | hba
    · simp [skewFromRolePairs, h, Ne.symm h, hab, not_lt_of_ge hab.le,
        rolePairOfDistinct_swap a b h]
    · simp [skewFromRolePairs, h, Ne.symm h, hba, not_lt_of_ge hba.le,
        rolePairOfDistinct_swap a b h]

@[simp] theorem skewFromRolePairs_upper (u : RolePair → ℝ) (p : RolePair) :
    skewFromRolePairs u p.val.1 p.val.2 = u p := by
  simp [skewFromRolePairs, rolePair_ne p, p.property, rolePairOfDistinct_ordered]

def rolePairsEquivSkew : (RolePair → ℝ) ≃ₗ[ℝ] roleSkewMatrices where
  toFun u := ⟨skewFromRolePairs u, skewFromRolePairs_skew u⟩
  invFun e p := e.val p.val.1 p.val.2
  left_inv u := by funext p; exact skewFromRolePairs_upper u p
  right_inv e := by
    apply Subtype.ext
    funext a b
    change skewFromRolePairs (fun p => e.val p.val.1 p.val.2) a b = e.val a b
    by_cases h : a = b
    · subst b
      have hdiag := e.property a a
      simp only [skewFromRolePairs, dite_true]
      linarith
    · by_cases hab : roleCode a < roleCode b
      · simp [skewFromRolePairs, h, hab, rolePairOfDistinct]
      · have hba : roleCode b < roleCode a :=
          (lt_or_gt_of_ne (fun he => h (roleCode_injective he))).resolve_left hab
        simpa [skewFromRolePairs, h, hab, rolePairOfDistinct] using (e.property a b).symm
  map_add' u v := by
    apply Subtype.ext
    funext a b
    by_cases h : a = b <;> by_cases hab : roleCode a < roleCode b <;>
      simp [skewFromRolePairs, h, hab, add_comm]
  map_smul' t u := by
    apply Subtype.ext
    funext a b
    by_cases h : a = b <;> by_cases hab : roleCode a < roleCode b <;>
      simp [skewFromRolePairs, h, hab]

/-- Structural coordinate equivalence, not a dimension-only identification. -/
def rolePairsEquivLorentzTangent : (RolePair → ℝ) ≃ₗ[ℝ] RoleLorentzTangent :=
  rolePairsEquivSkew.trans lorentzTangentEquivSkew.symm

theorem roleLorentzTangent_finrank : Module.finrank ℝ RoleLorentzTangent = 6 := by
  rw [← rolePairsEquivLorentzTangent.finrank_eq, Module.finrank_pi, rolePair_card]

/-- Dimension of independent centered frame tangents; no pre-centering lift is implicit. -/
theorem localLorentzTangentField_finrank (N : ℕ) :
    Module.finrank ℝ (ArchiveRolePhaseGroup N → RoleLorentzTangent) = 6 * archiveModes N := by
  rw [Module.finrank_pi_fintype]
  simp [roleLorentzTangent_finrank, archiveModes, Nat.mul_comm]

end
end D0.Geometry
