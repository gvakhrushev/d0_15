import Mathlib.LinearAlgebra.Matrix.ToLin
import D0.Geometry.FinitePrimalDualHodgeParent
import D0.Geometry.ArchiveMetricMeasureHodgeLift
import D0.Geometry.ArchiveWeightedHodgeDirac
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.Analysis.Calculus.Deriv.Slope

/-! Source classification of the existing mixed parent action, after exposing
its actual supplied bilinear pairing. No new native action is installed.
The positive scalar form is an explicit class hypothesis, not a physical
constitutive law deduced from an arithmetic Hodge capstone. -/
open scoped BigOperators Topology
open Filter
open D0.Geometry
namespace D0.Research.NativeParentSource
noncomputable section
variable {n : Type*} [Fintype n]
set_option linter.unusedSectionVars false

def pair (x y : n → ℝ) : ℝ := ∑ i, x i*y i

lemma pair_symm (x y : n → ℝ) : pair x y=pair y x := by
  simp [pair, mul_comm]

lemma pair_add_left (x y z : n → ℝ) : pair (x+y) z=pair x z+pair y z := by
  simp [pair, add_mul, Finset.sum_add_distrib]

lemma pair_add_right (x y z : n → ℝ) : pair x (y+z)=pair x y+pair x z := by
  simp [pair, mul_add, Finset.sum_add_distrib]

lemma pair_sub_right (x y z : n → ℝ) : pair x (y-z)=pair x y-pair x z := by
  simp [pair, mul_sub, Finset.sum_sub_distrib]

lemma pair_smul_left (t : ℝ) (x y : n → ℝ) : pair (t • x) y=t*pair x y := by
  simp [pair, Finset.mul_sum, mul_assoc]

lemma pair_smul_right (t : ℝ) (x y : n → ℝ) : pair x (t • y)=t*pair x y := by
  rw [pair_symm, pair_smul_left, pair_symm]

lemma pair_zero_iff (x : n → ℝ) : pair x x=0 ↔ x=0 := by
  constructor
  · intro h
    funext i
    have hi := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => mul_self_nonneg (x i))).mp h i
      (Finset.mem_univ i)
    exact mul_self_eq_zero.mp hi
  · intro h; simp [pair, h]

lemma pair_nondegenerate_right (x : n → ℝ) (h : ∀ v, pair v x=0) : x=0 :=
  (pair_zero_iff x).mp (h x)

abbrev End (n : Type*) := (n → ℝ) →ₗ[ℝ] (n → ℝ)

/-- A coordinate expression for the existing mixedPrimalDualAction. -/
def parentForm (M K : End n) (ψ χ lm : n → ℝ) : ℝ :=
  (1/2 : ℝ)*pair χ (M χ)+pair lm (M χ-K ψ)

/-- Every supplied linear pairing and every owner composition bind literally.
R need not be injective here: K is the visible operator R d_D star1 d_P. -/
theorem literal_owner_binding {p q r : Type*} [Fintype p] [Fintype q] [Fintype r]
    (A : FinitePrimalDualHodgeData n p q r)
    (R : (r → ℝ) →ₗ[ℝ] (n → ℝ)) (ψ χ lm : n → ℝ) :
    mixedPrimalDualAction (fun x y => pair x (R y)) A ψ χ lm =
      parentForm (R.comp A.star0) (R.comp (A.dD.comp (A.star1.comp A.dP))) ψ χ lm := by
  simp [mixedPrimalDualAction, mixedCodifferentialConstraint, parentForm, map_sub]

def Symmetric (M : End n) : Prop := ∀ x y, pair x (M y)=pair y (M x)
def StrictPositive (M : End n) : Prop := ∀ x, x≠0 → 0<pair x (M x)

def fieldVariation (K : End n) (lm v : n → ℝ) : ℝ := -pair lm (K v)
def auxiliaryVariation (M : End n) (χ lm v : n → ℝ) : ℝ :=
  pair v (M χ)+pair lm (M v)
def multiplierVariation (M K : End n) (ψ χ v : n → ℝ) : ℝ :=
  pair v (M χ-K ψ)

theorem field_exact_variation (M K : End n) (ψ χ lm v : n → ℝ) (t : ℝ) :
    parentForm M K (ψ+t • v) χ lm = parentForm M K ψ χ lm+t*fieldVariation K lm v := by
  simp only [parentForm, fieldVariation, map_add, map_smul, pair_sub_right,
    pair_add_right, pair_smul_right]
  ring

theorem auxiliary_exact_variation (M K : End n) (hM : Symmetric M)
    (ψ χ lm v : n → ℝ) (t : ℝ) :
    parentForm M K ψ (χ+t • v) lm = parentForm M K ψ χ lm+
      t*auxiliaryVariation M χ lm v+(t^2/2)*pair v (M v) := by
  simp only [parentForm, auxiliaryVariation, map_add, map_smul, pair_sub_right,
    pair_add_left, pair_add_right, pair_smul_left, pair_smul_right]
  rw [hM χ v]
  ring

theorem multiplier_exact_variation (M K : End n) (ψ χ lm v : n → ℝ) (t : ℝ) :
    parentForm M K ψ χ (lm+t • v) = parentForm M K ψ χ lm+
      t*multiplierVariation M K ψ χ v := by
  simp only [parentForm, multiplierVariation, pair_add_left, pair_smul_left]
  ring

theorem field_first_variation (M K : End n) (ψ χ lm v : n → ℝ) :
    HasDerivAt (fun t : ℝ => parentForm M K (ψ+t • v) χ lm) (fieldVariation K lm v) 0 := by
  simp_rw [field_exact_variation]
  convert (hasDerivAt_const (0 : ℝ) (parentForm M K ψ χ lm)).add
    ((hasDerivAt_id (0 : ℝ)).mul_const (fieldVariation K lm v)) using 1; simp

theorem auxiliary_first_variation (M K : End n) (hM : Symmetric M)
    (ψ χ lm v : n → ℝ) :
    HasDerivAt (fun t : ℝ => parentForm M K ψ (χ+t • v) lm)
      (auxiliaryVariation M χ lm v) 0 := by
  simp_rw [auxiliary_exact_variation M K hM]
  convert ((hasDerivAt_const (0 : ℝ) (parentForm M K ψ χ lm)).add
    ((hasDerivAt_id (0 : ℝ)).mul_const (auxiliaryVariation M χ lm v))).add
    ((((hasDerivAt_id (0 : ℝ)).pow 2).div_const 2).mul_const (pair v (M v))) using 1;
    simp [id]

theorem multiplier_first_variation (M K : End n) (ψ χ lm v : n → ℝ) :
    HasDerivAt (fun t : ℝ => parentForm M K ψ χ (lm+t • v))
      (multiplierVariation M K ψ χ v) 0 := by
  simp_rw [multiplier_exact_variation]
  convert (hasDerivAt_const (0 : ℝ) (parentForm M K ψ χ lm)).add
    ((hasDerivAt_id (0 : ℝ)).mul_const (multiplierVariation M K ψ χ v)) using 1; simp

def FullFieldGate (M K : End n) (ψ χ lm : n → ℝ) : Prop :=
  (∀ v, deriv (fun t : ℝ => parentForm M K (ψ+t • v) χ lm) 0=0) ∧
  (∀ v, deriv (fun t : ℝ => parentForm M K ψ (χ+t • v) lm) 0=0) ∧
  (∀ v, deriv (fun t : ℝ => parentForm M K ψ χ (lm+t • v)) 0=0)

theorem actual_gate_equations (M K : End n) (hM : Symmetric M) (ψ χ lm : n → ℝ) :
    FullFieldGate M K ψ χ lm ↔
      (∀ v, pair lm (K v)=0) ∧ M (χ+lm)=0 ∧ M χ=K ψ := by
  simp only [FullFieldGate, (field_first_variation M K ψ χ lm _).deriv,
    (auxiliary_first_variation M K hM ψ χ lm _).deriv,
    (multiplier_first_variation M K ψ χ lm _).deriv,
    fieldVariation, auxiliaryVariation, multiplierVariation, neg_eq_zero]
  have hs : ∀ v, pair v (M χ)+pair lm (M v)=pair v (M (χ+lm)) := by
    intro v; rw [hM lm v, map_add, pair_add_right]
  simp_rw [hs]
  constructor
  · rintro ⟨hψ,hχ,hlm⟩
    exact ⟨hψ, pair_nondegenerate_right _ hχ,
      sub_eq_zero.mp (pair_nondegenerate_right _ hlm)⟩
  · rintro ⟨hψ,hχ,hlm⟩
    refine ⟨hψ, ?_, ?_⟩ <;> intro v <;> simp [hχ, hlm, pair]

/-- Identity needed for quantitative residual control; no inverse of K. -/
theorem coercive_euler_identity (M K : End n)
    (ψ χ lm : n → ℝ) :
    pair χ (M χ) = auxiliaryVariation M χ lm χ-
      multiplierVariation M K ψ χ lm+fieldVariation K lm ψ := by
  simp only [auxiliaryVariation, multiplierVariation, fieldVariation, pair_sub_right]
  ring

theorem strict_positive_nondegenerate (M : End n) (hM : StrictPositive M)
    (x : n → ℝ) (hx : M x=0) : x=0 := by
  by_contra h
  have hp := hM x h
  simp [hx, pair] at hp

/-- Complete pointwise root set, for any geometry dependence of the inputs. -/
theorem positive_full_gate (M K : End n) (hM : Symmetric M) (hpos : StrictPositive M)
    (ψ χ lm : n → ℝ) :
    FullFieldGate M K ψ χ lm ↔ χ=0 ∧ lm=0 ∧ K ψ=0 := by
  rw [actual_gate_equations M K hM]
  constructor
  · rintro ⟨hψ,hχ,hlm⟩
    have hsum := strict_positive_nondegenerate M hpos (χ+lm) hχ
    have hlmχ : lm=-χ := by
      funext i
      have hh := congrFun hsum i
      simp only [Pi.add_apply, Pi.zero_apply] at hh
      change lm i = -χ i
      linarith
    have hq : pair χ (M χ)=0 := by
      have hh := hψ ψ
      rw [← hlm, hlmχ] at hh
      have hneg : pair (-χ) (M χ) = -pair χ (M χ) := by simp [pair, Finset.sum_neg_distrib]
      rw [hneg] at hh
      exact neg_eq_zero.mp hh
    have hc : χ=0 := by
      by_contra hh
      have hp := hpos χ hh
      linarith
    refine ⟨hc, ?_, ?_⟩
    · simp [hlmχ, hc]
    · simpa [hc] using hlm.symm
  · rintro ⟨rfl,rfl,hψ⟩
    simp [hψ, pair]

/-- The full constitutive derivative, not only the stationary action value. -/
def constitutiveResponse (U V : End n) (ψ χ lm : n → ℝ) : ℝ :=
  (1/2 : ℝ)*pair χ (U χ)+pair lm (U χ-V ψ)

theorem constitutive_exact_variation (M K U V : End n) (ψ χ lm : n → ℝ) (t : ℝ) :
    parentForm (M+t • U) (K+t • V) ψ χ lm = parentForm M K ψ χ lm+
      t*constitutiveResponse U V ψ χ lm := by
  simp only [parentForm, constitutiveResponse, LinearMap.add_apply,
    LinearMap.smul_apply, pair_sub_right, pair_add_right, pair_smul_right]
  ring

theorem constitutive_first_variation (M K U V : End n) (ψ χ lm : n → ℝ) :
    HasDerivAt (fun t : ℝ => parentForm (M+t • U) (K+t • V) ψ χ lm)
      (constitutiveResponse U V ψ χ lm) 0 := by
  simp_rw [constitutive_exact_variation]
  convert (hasDerivAt_const (0 : ℝ) (parentForm M K ψ χ lm)).add
    ((hasDerivAt_id (0 : ℝ)).mul_const (constitutiveResponse U V ψ χ lm)) using 1; simp

theorem positive_source_zero (M K U V : End n) (hM : Symmetric M) (hpos : StrictPositive M)
    (ψ χ lm : n → ℝ) (h : FullFieldGate M K ψ χ lm) :
    constitutiveResponse U V ψ χ lm=0 := by
  obtain ⟨rfl,rfl,_⟩ := (positive_full_gate M K hM hpos ψ χ lm).mp h
  simp [constitutiveResponse, pair]

/-- Nondegenerate indefinite M: complete remaining kernel relation. -/
theorem invertible_full_gate (M : (n → ℝ) ≃ₗ[ℝ] (n → ℝ)) (K : End n)
    (hM : Symmetric M.toLinearMap) (ψ χ lm : n → ℝ) :
    FullFieldGate M.toLinearMap K ψ χ lm ↔
      χ=M.symm (K ψ) ∧ lm=-(M.symm (K ψ)) ∧ ∀ v, pair (M.symm (K ψ)) (K v)=0 := by
  rw [actual_gate_equations M.toLinearMap K hM]
  constructor
  · rintro ⟨hψ,hχ,hlm⟩
    have hc : χ=M.symm (K ψ) := by rw [← hlm]; exact (M.symm_apply_apply χ).symm
    have hsum : χ+lm=0 := M.injective (by simpa using hχ)
    have hl : lm=-χ := by
      funext i
      have hh := congrFun hsum i
      simp only [Pi.add_apply, Pi.zero_apply] at hh
      change lm i = -χ i
      linarith
    refine ⟨hc, by rw [hl, hc], ?_⟩
    intro v
    have hh := hψ v
    rw [hl, hc] at hh
    simpa [pair, Finset.sum_neg_distrib] using hh
  · rintro ⟨rfl,rfl,hψ⟩
    refine ⟨?_, ?_, ?_⟩
    · intro v; simpa [pair, Finset.sum_neg_distrib] using hψ v
    · simp
    · exact M.apply_symm_apply (K ψ)

theorem on_shell_constitutive_relation (U V : End n) (ψ χ : n → ℝ) :
    constitutiveResponse U V ψ χ (-χ) =
      -(1/2 : ℝ)*pair χ (U χ)+pair χ (V ψ) := by
  simp [constitutiveResponse, pair, mul_sub, Finset.sum_add_distrib, Finset.sum_neg_distrib]
  ring

theorem independent_identity_response_detects_auxiliary (ψ χ : n → ℝ) :
    constitutiveResponse LinearMap.id 0 ψ χ (-χ)=0 ↔ χ=0 := by
  rw [on_shell_constitutive_relation]
  have hz : pair χ ((0 : End n) ψ)=0 := by simp [pair]
  rw [hz, add_zero]
  change -(1/2 : ℝ)*pair χ χ=0 ↔ χ=0
  rw [mul_eq_zero, or_iff_right (by norm_num : -(1/2 : ℝ)≠0), pair_zero_iff]

/-- Full raw constraint follows only if the supplied pairing separates it. -/
theorem actual_constraint_of_injective_pairing {p q r : Type*}
    [Fintype p] [Fintype q] [Fintype r]
    (A : FinitePrimalDualHodgeData n p q r)
    (R : (r → ℝ) →ₗ[ℝ] (n → ℝ)) (hR : Function.Injective R)
    (hM : Symmetric (R.comp A.star0)) (ψ χ lm : n → ℝ)
    (h : FullFieldGate (R.comp A.star0) (R.comp (A.dD.comp (A.star1.comp A.dP))) ψ χ lm) :
    mixedCodifferentialConstraint A ψ χ=0 := by
  have hc := (actual_gate_equations _ _ hM ψ χ lm).mp h
  apply hR
  simpa [mixedCodifferentialConstraint, map_sub, sub_eq_zero] using hc.2.2

def diagonal (w : n → ℝ) : End n where
  toFun x := fun i => w i*x i
  map_add' x y := by funext i; simp; ring
  map_smul' t x := by funext i; simp; ring

theorem diagonal_symmetric (w : n → ℝ) : Symmetric (diagonal w) := by
  intro x y
  apply Finset.sum_congr rfl
  intro i _
  simp [diagonal]
  ring

theorem positive_diagonal (w : n → ℝ) (hw : ∀ i, 0<w i) : StrictPositive (diagonal w) := by
  intro x hx
  have hi : ∃ i, x i≠0 := by
    by_contra h
    push Not at h
    apply hx; funext i; exact h i
  obtain ⟨i,hi⟩ := hi
  apply Finset.sum_pos'
  · intro j _
    change 0≤x j*(w j*x j)
    nlinarith [mul_nonneg (le_of_lt (hw j)) (sq_nonneg (x j))]
  · refine ⟨i, Finset.mem_univ i, ?_⟩
    change 0<x i*(w i*x i)
    nlinarith [mul_pos (hw i) (sq_pos_of_ne_zero hi)]

theorem literal_scalar_hodge_positive (μ : n → ℝ) (hμ : ∀ i, 0<μ i) :
    StrictPositive (diagonal (fun i => hodgeMetricMeasureWeight 0 (μ i) 1)) := by
  simp_rw [hodge_weight_0_eq_mu]
  exact positive_diagonal μ hμ

/-- A continuous family of exact critical roots has zero pointwise source in
the transport direction. No derivative of the root or rank assumption is used. -/
theorem continuous_critical_root_source {n : Type*} [Fintype n]
    (H : ℝ → n → n → ℝ) (H' : n → n → ℝ) (z : ℝ → n → ℝ)
    (hd : ∀ i j, HasDerivAt (fun q => H q i j) (H' i j) 0)
    (hz : ∀ i, ContinuousAt (fun q => z q i) 0)
    (hs : ∀ i j, H 0 i j=H 0 j i)
    (hr0 : ∀ i, ∑ j, H 0 i j*z 0 j=0)
    (hr : ∀ᶠ q in (𝓝[≠] (0 : ℝ)), ∀ i, ∑ j, H q i j*z q j=0) :
    ∑ i, ∑ j, z 0 i*H' i j*z 0 j=0 := by
  have hnow (q : ℝ) (hq : ∀ i, ∑ j, H q i j*z q j=0) :
      ∑ i, ∑ j, z 0 i*H q i j*z q j=0 := by
    apply Finset.sum_eq_zero
    intro i _
    calc
      ∑ j, z 0 i*H q i j*z q j = z 0 i*(∑ j, H q i j*z q j) := by
        simp [Finset.mul_sum, mul_assoc]
      _ = 0 := by rw [hq]; ring
  have hbase (q : ℝ) : ∑ i, ∑ j, z 0 i*H 0 i j*z q j=0 := by
    rw [Finset.sum_comm]
    apply Finset.sum_eq_zero
    intro j _
    calc
      ∑ i, z 0 i*H 0 i j*z q j = (∑ i, H 0 j i*z 0 i)*z q j := by
        rw [Finset.sum_mul]
        apply Finset.sum_congr rfl
        intro i _
        rw [hs i j]
        ring
      _ = 0 := by rw [hr0]; ring
  have hf (q : ℝ) (hq : ∀ i, ∑ j, H q i j*z q j=0) :
      ∑ i, ∑ j, z 0 i*(q⁻¹*(H q i j-H 0 i j))*z q j=0 := by
    calc
      _ = q⁻¹*((∑ i, ∑ j, z 0 i*H q i j*z q j)-
            (∑ i, ∑ j, z 0 i*H 0 i j*z q j)) := by
        simp only [← Finset.sum_sub_distrib, Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        apply Finset.sum_congr rfl
        intro j _
        ring
      _ = 0 := by rw [hnow q hq, hbase]; ring
  have ht (i j : n) : Tendsto (fun q : ℝ => q⁻¹*(H q i j-H 0 i j))
      (𝓝[≠] 0) (𝓝 (H' i j)) := by
    simpa only [zero_add, smul_eq_mul] using (hd i j).tendsto_slope_zero
  have hl : Tendsto (fun q : ℝ => ∑ i, ∑ j, z 0 i*(q⁻¹*(H q i j-H 0 i j))*z q j)
      (𝓝[≠] 0) (𝓝 (∑ i, ∑ j, z 0 i*H' i j*z 0 j)) := by
    apply tendsto_finsetSum
    intro i _
    apply tendsto_finsetSum
    intro j _
    exact (tendsto_const_nhds.mul (ht i j)).mul ((hz j).tendsto.mono_left nhdsWithin_le_nhds)
  have hzero : Tendsto (fun q : ℝ => ∑ i, ∑ j, z 0 i*(q⁻¹*(H q i j-H 0 i j))*z q j)
      (𝓝[≠] 0) (𝓝 0) :=
    tendsto_const_nhds.congr' (hr.mono (fun q hq => (hf q hq).symm))
  exact tendsto_nhds_unique hl hzero

end

noncomputable section FieldFrames
variable {n : Type*} [Fintype n] [DecidableEq n]
set_option linter.unusedSectionVars false

/-- The actual Euclidean transpose, not a supplied covariance premise. -/
def transposed (A : End n) : End n :=
  Matrix.toLin' (LinearMap.toMatrix' A).transpose

lemma pair_transposed (A : End n) (x y : n → ℝ) :
    pair x (transposed A y)=pair (A x) y := by
  have h := Matrix.dotProduct_transpose_mulVec (LinearMap.toMatrix' A) x y
  simpa [pair, transposed, dotProduct, mul_comm] using h

def congruence (P M : End n) : End n := (transposed P).comp (M.comp P)

lemma pair_congruence (P M : End n) (x y : n → ℝ) :
    pair x (congruence P M y)=pair (P x) (M (P y)) := by
  exact pair_transposed P x (M (P y))

theorem congruence_symmetric (P M : End n) (hM : Symmetric M) :
    Symmetric (congruence P M) := by
  intro x y
  simp only [pair_congruence]
  exact hM (P x) (P y)

/-- Exact action identity without field equations, positivity or invertible M. -/
theorem parent_congruence (P M K : End n) (ψ χ lm : n → ℝ) :
    parentForm (congruence P M) (congruence P K) ψ χ lm =
      parentForm M K (P ψ) (P χ) (P lm) := by
  simp only [parentForm, pair_sub_right, pair_congruence]

theorem response_congruence (P U V : End n) (ψ χ lm : n → ℝ) :
    constitutiveResponse (congruence P U) (congruence P V) ψ χ lm =
      constitutiveResponse U V (P ψ) (P χ) (P lm) := by
  exact parent_congruence P U V ψ χ lm

lemma field_congruence (P K : End n) (lm v : n → ℝ) :
    fieldVariation (congruence P K) lm v=fieldVariation K (P lm) (P v) := by
  simp only [fieldVariation, pair_congruence]

lemma auxiliary_congruence (P M : End n) (χ lm v : n → ℝ) :
    auxiliaryVariation (congruence P M) χ lm v=
      auxiliaryVariation M (P χ) (P lm) (P v) := by
  simp only [auxiliaryVariation, pair_congruence]

lemma multiplier_congruence (P M K : End n) (ψ χ v : n → ℝ) :
    multiplierVariation (congruence P M) (congruence P K) ψ χ v=
      multiplierVariation M K (P ψ) (P χ) (P v) := by
  simp only [multiplierVariation, pair_sub_right, pair_congruence]

theorem actual_gate_variations (M K : End n) (hM : Symmetric M)
    (ψ χ lm : n → ℝ) :
    FullFieldGate M K ψ χ lm ↔
      (∀ v, fieldVariation K lm v=0) ∧
      (∀ v, auxiliaryVariation M χ lm v=0) ∧
      (∀ v, multiplierVariation M K ψ χ v=0) := by
  simp only [FullFieldGate, (field_first_variation M K ψ χ lm _).deriv,
    (auxiliary_first_variation M K hM ψ χ lm _).deriv,
    (multiplier_first_variation M K ψ χ lm _).deriv]

/-- Bijection of all full field roots, including singular/indefinite M. -/
theorem full_gate_congruence (P : (n → ℝ) ≃ₗ[ℝ] (n → ℝ))
    (M K : End n) (hM : Symmetric M) (ψ χ lm : n → ℝ) :
    FullFieldGate (congruence P.toLinearMap M) (congruence P.toLinearMap K) ψ χ lm ↔
      FullFieldGate M K (P ψ) (P χ) (P lm) := by
  rw [actual_gate_variations _ _ (congruence_symmetric P.toLinearMap M hM),
    actual_gate_variations M K hM]
  simp only [field_congruence, auxiliary_congruence, multiplier_congruence]
  constructor
  · rintro ⟨hp,hc,hl⟩
    exact ⟨fun v => by simpa using hp (P.symm v),
      fun v => by simpa using hc (P.symm v), fun v => by simpa using hl (P.symm v)⟩
  · rintro ⟨hp,hc,hl⟩
    exact ⟨fun v => hp (P v), fun v => hc (P v), fun v => hl (P v)⟩

/-- Q sends old fields to new fields, so at Q=1 the pulled operator jet is
U-A^T M-M A. A is the logarithmic derivative Q^{-1} dQ. -/
def frameJet (A M U : End n) : End n := U-(transposed A).comp M-M.comp A

lemma pair_frameJet (A M U : End n) (x y : n → ℝ) :
    pair x (frameJet A M U y)=pair x (U y)-pair (A x) (M y)-pair x (M (A y)) := by
  simp only [frameJet, LinearMap.sub_apply, LinearMap.comp_apply, pair_sub_right,
    pair_transposed]

/-- Exact defect identity, derived from the literal action before using a gate. -/
theorem frame_off_shell_defect (A M K U V : End n) (hM : Symmetric M)
    (ψ χ lm : n → ℝ) :
    constitutiveResponse (frameJet A M U) (frameJet A K V) ψ χ lm =
      constitutiveResponse U V ψ χ lm-fieldVariation K lm (A ψ)-
        auxiliaryVariation M χ lm (A χ)-multiplierVariation M K ψ χ (A lm) := by
  simp only [constitutiveResponse, fieldVariation, auxiliaryVariation,
    multiplierVariation, pair_sub_right, pair_frameJet]
  rw [hM χ (A χ)]
  ring

theorem full_gate_frame_source (A M K U V : End n) (hM : Symmetric M)
    (ψ χ lm : n → ℝ) (h : FullFieldGate M K ψ χ lm) :
    constitutiveResponse (frameJet A M U) (frameJet A K V) ψ χ lm =
      constitutiveResponse U V ψ χ lm := by
  obtain ⟨hp,hc,hl⟩ := (actual_gate_variations M K hM ψ χ lm).mp h
  rw [frame_off_shell_defect A M K U V hM, hp, hc, hl, sub_zero, sub_zero, sub_zero]

/-- Arbitrary frame value P=Q^{-1}; no restriction to translations or to a
selected list of background directions. -/
theorem full_gate_background_source (P : (n → ℝ) ≃ₗ[ℝ] (n → ℝ))
    (A M K U V : End n) (hM : Symmetric M) (ψ χ lm : n → ℝ)
    (h : FullFieldGate M K (P ψ) (P χ) (P lm)) :
    constitutiveResponse (congruence P.toLinearMap (frameJet A M U))
      (congruence P.toLinearMap (frameJet A K V)) ψ χ lm =
      constitutiveResponse U V (P ψ) (P χ) (P lm) := by
  rw [response_congruence]
  exact full_gate_frame_source A M K U V hM (P ψ) (P χ) (P lm) h

/-- A fixed seed transported solely through arbitrary invertible field frames
has zero source in every background direction, even for indefinite/singular M. -/
theorem transported_fixed_seed_source_zero (P : (n → ℝ) ≃ₗ[ℝ] (n → ℝ))
    (A M K : End n) (hM : Symmetric M) (ψ χ lm : n → ℝ)
    (h : FullFieldGate M K (P ψ) (P χ) (P lm)) :
    constitutiveResponse (congruence P.toLinearMap (frameJet A M 0))
      (congruence P.toLinearMap (frameJet A K 0)) ψ χ lm=0 := by
  rw [full_gate_background_source P A M K 0 0 hM ψ χ lm h]
  simp [constitutiveResponse, pair]

/-- Literal connection/metric Euler equations with the same geometric term.
The frame term is removed by actual matter equations, not a new response gate. -/
theorem joint_gate_frame_equivalence {B : Type*}
    (P : (n → ℝ) ≃ₗ[ℝ] (n → ℝ)) (M K : End n) (hM : Symmetric M)
    (A U V : B → End n) (geometryVariation : B → ℝ) (ψ χ lm : n → ℝ) :
    (FullFieldGate (congruence P.toLinearMap M) (congruence P.toLinearMap K) ψ χ lm ∧
      ∀ b, geometryVariation b+constitutiveResponse
        (congruence P.toLinearMap (frameJet (A b) M (U b)))
        (congruence P.toLinearMap (frameJet (A b) K (V b))) ψ χ lm=0) ↔
    (FullFieldGate M K (P ψ) (P χ) (P lm) ∧
      ∀ b, geometryVariation b+constitutiveResponse (U b) (V b) (P ψ) (P χ) (P lm)=0) := by
  rw [full_gate_congruence P M K hM]
  constructor <;> rintro ⟨h,hb⟩
  · refine ⟨h, fun b => ?_⟩
    simpa only [full_gate_background_source P (A b) M K (U b) (V b) hM ψ χ lm h] using hb b
  · refine ⟨h, fun b => ?_⟩
    simpa only [full_gate_background_source P (A b) M K (U b) (V b) hM ψ χ lm h] using hb b

/-- Each endpoint may have its own invertible frame; no field gate is needed. -/
theorem corresponding_endpoint_contrast (P0 P1 M0 M1 K0 K1 : End n)
    (ψ0 χ0 lm0 ψ1 χ1 lm1 : n → ℝ) :
    parentForm (congruence P1 M1) (congruence P1 K1) ψ1 χ1 lm1-
      parentForm (congruence P0 M0) (congruence P0 K0) ψ0 χ0 lm0 =
    parentForm M1 K1 (P1 ψ1) (P1 χ1) (P1 lm1)-
      parentForm M0 K0 (P0 ψ0) (P0 χ0) (P0 lm0) := by
  simp only [parent_congruence]

/-- Transport every actual owner slot, retaining arbitrary rectangular pairing. -/
def reframeData {p q r : Type*} [Fintype p] [Fintype q] [Fintype r]
    (D : FinitePrimalDualHodgeData n p q r)
    (Q0 : (n → ℝ) ≃ₗ[ℝ] (n → ℝ)) (Q1 : (p → ℝ) ≃ₗ[ℝ] (p → ℝ))
    (T3 : (q → ℝ) ≃ₗ[ℝ] (q → ℝ)) (T4 : (r → ℝ) ≃ₗ[ℝ] (r → ℝ)) :
    FinitePrimalDualHodgeData n p q r where
  dP := Q1.toLinearMap.comp (D.dP.comp Q0.symm.toLinearMap)
  dD := T4.toLinearMap.comp (D.dD.comp T3.symm.toLinearMap)
  star0 := T4.toLinearMap.comp (D.star0.comp Q0.symm.toLinearMap)
  star1 := T3.toLinearMap.comp (D.star1.comp Q1.symm.toLinearMap)

def reframePairing {r : Type*} [Fintype r]
    (R : (r → ℝ) →ₗ[ℝ] (n → ℝ))
    (Q0 : (n → ℝ) ≃ₗ[ℝ] (n → ℝ)) (T4 : (r → ℝ) ≃ₗ[ℝ] (r → ℝ)) :
    (r → ℝ) →ₗ[ℝ] (n → ℝ) :=
  (transposed Q0.symm.toLinearMap).comp (R.comp T4.symm.toLinearMap)

theorem reframed_visible_operators {p q r : Type*} [Fintype p] [Fintype q] [Fintype r]
    (D : FinitePrimalDualHodgeData n p q r) (R : (r → ℝ) →ₗ[ℝ] (n → ℝ))
    (Q0 : (n → ℝ) ≃ₗ[ℝ] (n → ℝ)) (Q1 : (p → ℝ) ≃ₗ[ℝ] (p → ℝ))
    (T3 : (q → ℝ) ≃ₗ[ℝ] (q → ℝ)) (T4 : (r → ℝ) ≃ₗ[ℝ] (r → ℝ)) :
    let D' := reframeData D Q0 Q1 T3 T4
    let R' := reframePairing R Q0 T4
    R'.comp D'.star0 = congruence Q0.symm.toLinearMap (R.comp D.star0) ∧
    R'.comp (D'.dD.comp (D'.star1.comp D'.dP)) =
      congruence Q0.symm.toLinearMap (R.comp (D.dD.comp (D.star1.comp D.dP))) := by
  constructor <;> ext x <;> simp [reframeData, reframePairing, congruence]

theorem literal_reframed_owner {p q r : Type*} [Fintype p] [Fintype q] [Fintype r]
    (D : FinitePrimalDualHodgeData n p q r) (R : (r → ℝ) →ₗ[ℝ] (n → ℝ))
    (Q0 : (n → ℝ) ≃ₗ[ℝ] (n → ℝ)) (Q1 : (p → ℝ) ≃ₗ[ℝ] (p → ℝ))
    (T3 : (q → ℝ) ≃ₗ[ℝ] (q → ℝ)) (T4 : (r → ℝ) ≃ₗ[ℝ] (r → ℝ))
    (ψ χ lm : n → ℝ) :
    mixedPrimalDualAction (fun x y => pair x (reframePairing R Q0 T4 y))
      (reframeData D Q0 Q1 T3 T4) (Q0 ψ) (Q0 χ) (Q0 lm) =
    mixedPrimalDualAction (fun x y => pair x (R y)) D ψ χ lm := by
  rw [literal_owner_binding, literal_owner_binding]
  have h := reframed_visible_operators D R Q0 Q1 T3 T4
  dsimp only at h
  rw [h.1, h.2, parent_congruence]
  simp

def fullFieldTangent (M K : End n) (ψ χ lm vp vc vl : n → ℝ) : ℝ :=
  fieldVariation K lm vp+auxiliaryVariation M χ lm vc+multiplierVariation M K ψ χ vl

theorem simultaneous_exact_variation (M K : End n) (hM : Symmetric M)
    (ψ χ lm vp vc vl : n → ℝ) (t : ℝ) :
    parentForm M K (ψ+t • vp) (χ+t • vc) (lm+t • vl) =
      parentForm M K ψ χ lm+t*fullFieldTangent M K ψ χ lm vp vc vl+
        t^2*parentForm M K vp vc vl := by
  simp only [parentForm, fullFieldTangent, fieldVariation, auxiliaryVariation,
    multiplierVariation, map_add, map_smul, pair_sub_right, pair_add_left,
    pair_add_right, pair_smul_left, pair_smul_right]
  rw [hM χ vc]
  ring

/-- The source defect is an actual derivative of the simultaneous operator
and field path. U is symmetric because M(t) remains in the declared class. -/
theorem simultaneous_background_first_variation (M K U V : End n)
    (hM : Symmetric M) (hU : Symmetric U) (ψ χ lm vp vc vl : n → ℝ) :
    HasDerivAt
      (fun t : ℝ => parentForm (M+t • U) (K+t • V) (ψ+t • vp) (χ+t • vc) (lm+t • vl))
      (constitutiveResponse U V ψ χ lm+fullFieldTangent M K ψ χ lm vp vc vl) 0 := by
  have hf : ∀ t : ℝ, parentForm (M+t • U) (K+t • V) (ψ+t • vp) (χ+t • vc) (lm+t • vl) =
      (parentForm M K ψ χ lm+t*fullFieldTangent M K ψ χ lm vp vc vl+t^2*parentForm M K vp vc vl)+
      t*(parentForm U V ψ χ lm+t*fullFieldTangent U V ψ χ lm vp vc vl+t^2*parentForm U V vp vc vl) := by
    intro t
    rw [constitutive_exact_variation]
    change parentForm M K (ψ+t • vp) (χ+t • vc) (lm+t • vl)+
      t*parentForm U V (ψ+t • vp) (χ+t • vc) (lm+t • vl)=_
    rw [simultaneous_exact_variation M K hM, simultaneous_exact_variation U V hU]
  simp_rw [hf]
  have hp (a b c : ℝ) : HasDerivAt (fun t : ℝ => a+t*b+t^2*c) b 0 := by
    convert ((hasDerivAt_const (0 : ℝ) a).add ((hasDerivAt_id (0 : ℝ)).mul_const b)).add
      (((hasDerivAt_id (0 : ℝ)).pow 2).mul_const c) using 1; simp
  convert (hp _ _ _).add ((hasDerivAt_id (0 : ℝ)).mul (hp _ _ _)) using 1;
    simp [constitutiveResponse, parentForm, add_comm]

end FieldFrames
end D0.Research.NativeParentSource

#print axioms D0.Research.NativeParentSource.literal_owner_binding
#print axioms D0.Research.NativeParentSource.field_first_variation
#print axioms D0.Research.NativeParentSource.auxiliary_first_variation
#print axioms D0.Research.NativeParentSource.multiplier_first_variation
#print axioms D0.Research.NativeParentSource.actual_gate_equations
#print axioms D0.Research.NativeParentSource.coercive_euler_identity
#print axioms D0.Research.NativeParentSource.positive_full_gate
#print axioms D0.Research.NativeParentSource.constitutive_exact_variation
#print axioms D0.Research.NativeParentSource.constitutive_first_variation
#print axioms D0.Research.NativeParentSource.positive_source_zero
#print axioms D0.Research.NativeParentSource.invertible_full_gate
#print axioms D0.Research.NativeParentSource.on_shell_constitutive_relation
#print axioms D0.Research.NativeParentSource.literal_scalar_hodge_positive
#print axioms D0.Research.NativeParentSource.independent_identity_response_detects_auxiliary
#print axioms D0.Research.NativeParentSource.actual_constraint_of_injective_pairing
#print axioms D0.Research.NativeParentSource.continuous_critical_root_source
#check D0.Research.NativeParentSource.continuous_critical_root_source
#check D0.Research.NativeParentSource.literal_owner_binding
#check D0.Research.NativeParentSource.actual_gate_equations
#check D0.Research.NativeParentSource.positive_full_gate
#check D0.Research.NativeParentSource.positive_source_zero
#check D0.Research.NativeParentSource.invertible_full_gate
#check D0.Geometry.archive_weighted_hodge_dirac_owner

#print axioms D0.Research.NativeParentSource.pair_transposed
#print axioms D0.Research.NativeParentSource.congruence_symmetric
#print axioms D0.Research.NativeParentSource.parent_congruence
#print axioms D0.Research.NativeParentSource.response_congruence
#print axioms D0.Research.NativeParentSource.actual_gate_variations
#print axioms D0.Research.NativeParentSource.full_gate_congruence
#print axioms D0.Research.NativeParentSource.frame_off_shell_defect
#print axioms D0.Research.NativeParentSource.full_gate_frame_source
#print axioms D0.Research.NativeParentSource.full_gate_background_source
#print axioms D0.Research.NativeParentSource.joint_gate_frame_equivalence
#print axioms D0.Research.NativeParentSource.corresponding_endpoint_contrast
#print axioms D0.Research.NativeParentSource.reframed_visible_operators
#print axioms D0.Research.NativeParentSource.literal_reframed_owner
#print axioms D0.Research.NativeParentSource.simultaneous_exact_variation
#print axioms D0.Research.NativeParentSource.simultaneous_background_first_variation
#check D0.Research.NativeParentSource.full_gate_congruence
#check D0.Research.NativeParentSource.frame_off_shell_defect
#check D0.Research.NativeParentSource.full_gate_frame_source
#check D0.Research.NativeParentSource.full_gate_background_source
#check D0.Research.NativeParentSource.joint_gate_frame_equivalence
#check D0.Research.NativeParentSource.corresponding_endpoint_contrast
#check D0.Research.NativeParentSource.reframed_visible_operators
#check D0.Research.NativeParentSource.literal_reframed_owner
#check D0.Research.NativeParentSource.simultaneous_exact_variation
#check D0.Research.NativeParentSource.simultaneous_background_first_variation

#print axioms D0.Research.NativeParentSource.transported_fixed_seed_source_zero
#check D0.Research.NativeParentSource.transported_fixed_seed_source_zero
