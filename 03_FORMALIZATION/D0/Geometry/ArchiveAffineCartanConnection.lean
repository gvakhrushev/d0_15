import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveChainCurvature
import D0.Geometry.A4DCoframeParentConstraint

/-!
# Affine Cartan link geometry

Finite affine maps `z ↦ U z + a` on the existing archive chain.

Stored data stay pulls: the link at `x` in direction `r` sends the fibre at
`x + r` to the fibre at `x`. Path words use `ChainStep` in that order.
Forward and backward slots are not identified, including at period two.

The flat translation gauge reproduces `forwardGaugeCoframe` by an exact finite
identity. That identity is the owned forward difference. It is not a continuum
derivative and it is not finite Diff.

Open torsion gauges by `T' = g_x T - F' b_y`. The translation term is absent
only when `F'` kills `b_y`. Based torsion is `t = T + (I - P) b`, so it agrees
with open torsion only when `P` fixes `b`.
-/

namespace D0.Geometry

open D0

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Affine map `z ↦ lin z + shift`. -/
@[ext]
structure AffineCartanMap (K V : Type*) [Field K] [AddCommGroup V] [Module K V] where
  lin : V ≃ₗ[K] V
  shift : V

namespace AffineCartanMap

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Apply `(U, a)` on the left of a vector. -/
def apply (φ : AffineCartanMap K V) (z : V) : V :=
  φ.lin z + φ.shift

/-- Composition applies the right factor first: `(U, a)(V, b) = (U V, a + U b)`. -/
def mul (φ ψ : AffineCartanMap K V) : AffineCartanMap K V where
  lin := ψ.lin.trans φ.lin
  shift := φ.shift + φ.lin ψ.shift

/-- Identity affine map. -/
def one : AffineCartanMap K V where
  lin := LinearEquiv.refl K V
  shift := 0

/-- Inverse `(U, a)⁻¹ = (U⁻¹, -U⁻¹ a)`. -/
def inv (φ : AffineCartanMap K V) : AffineCartanMap K V where
  lin := φ.lin.symm
  shift := -φ.lin.symm φ.shift

instance : Mul (AffineCartanMap K V) := ⟨mul⟩

instance : One (AffineCartanMap K V) := ⟨one⟩

instance : Inv (AffineCartanMap K V) := ⟨inv⟩

@[simp] theorem mul_lin (φ ψ : AffineCartanMap K V) :
    (φ * ψ).lin = ψ.lin.trans φ.lin := rfl

@[simp] theorem mul_shift (φ ψ : AffineCartanMap K V) :
    (φ * ψ).shift = φ.shift + φ.lin ψ.shift := rfl

@[simp] theorem one_lin : (1 : AffineCartanMap K V).lin = LinearEquiv.refl K V := rfl

@[simp] theorem one_shift : (1 : AffineCartanMap K V).shift = 0 := rfl

@[simp] theorem inv_lin (φ : AffineCartanMap K V) : (φ⁻¹).lin = φ.lin.symm := rfl

@[simp] theorem inv_shift (φ : AffineCartanMap K V) :
    (φ⁻¹).shift = -φ.lin.symm φ.shift := rfl

@[simp] theorem apply_mul (φ ψ : AffineCartanMap K V) (z : V) :
    apply (φ * ψ) z = apply φ (apply ψ z) := by
  simp only [apply, mul_lin, mul_shift, LinearEquiv.trans_apply, map_add]
  abel

theorem affine_mul_assoc (φ ψ ρ : AffineCartanMap K V) :
    φ * ψ * ρ = φ * (ψ * ρ) := by
  ext
  · simp [LinearEquiv.trans_assoc]
  · simp only [mul_shift, mul_lin, LinearEquiv.trans_apply, map_add]
    abel

@[simp] theorem affine_one_mul (φ : AffineCartanMap K V) : 1 * φ = φ := by
  ext <;> simp

@[simp] theorem affine_mul_one (φ : AffineCartanMap K V) : φ * 1 = φ := by
  ext <;> simp

@[simp] theorem affine_inv_one : (1 : AffineCartanMap K V)⁻¹ = 1 := by
  ext <;> simp

theorem affine_inv_mul (φ : AffineCartanMap K V) : φ⁻¹ * φ = 1 := by
  ext
  · simp
  · simp only [mul_shift, inv_shift, inv_lin, one_shift, LinearEquiv.symm_apply_apply]
    abel

theorem affine_mul_inv (φ : AffineCartanMap K V) : φ * φ⁻¹ = 1 := by
  ext
  · simp
  · simp only [mul_shift, inv_shift, inv_lin, one_shift, LinearEquiv.apply_symm_apply,
      map_neg]
    abel

theorem affine_inv_inv (φ : AffineCartanMap K V) : φ⁻¹⁻¹ = φ := by
  ext
  · simp
  · simp [map_neg]

theorem affine_inv_mul_mul (φ ψ : AffineCartanMap K V) :
    (φ * ψ)⁻¹ = ψ⁻¹ * φ⁻¹ := by
  ext
  · simp [LinearEquiv.trans_assoc]
  · simp only [inv_shift, mul_lin, mul_shift, inv_lin, LinearEquiv.symm_trans_apply, map_add,
      map_neg, LinearEquiv.symm_apply_apply]
    abel

theorem conj_mul_conj (a φ b ψ c : AffineCartanMap K V) :
    (a * φ * b⁻¹) * (b * ψ * c⁻¹) = a * (φ * ψ) * c⁻¹ := by
  calc
    (a * φ * b⁻¹) * (b * ψ * c⁻¹) =
        a * φ * (b⁻¹ * b) * ψ * c⁻¹ := by
          simp only [affine_mul_assoc]
    _ = a * φ * 1 * ψ * c⁻¹ := by rw [affine_inv_mul]
    _ = a * φ * ψ * c⁻¹ := by simp [affine_mul_one]
    _ = a * (φ * ψ) * c⁻¹ := by simp [affine_mul_assoc]

end AffineCartanMap

variable {N : ℕ}

/-- Affine link: site and positive role to an affine pull `V_{x+r} → V_x`. -/
abbrev AffineCartanConnection (N : ℕ) (K V : Type*)
    [Field K] [AddCommGroup V] [Module K V] :=
  ArchiveRolePhaseGroup N → Role → AffineCartanMap K V

/-- Affine node gauge `h_x = (g_x, b_x)`. -/
abbrev AffineNodeGauge (N : ℕ) (K V : Type*)
    [Field K] [AddCommGroup V] [Module K V] :=
  ArchiveRolePhaseGroup N → AffineCartanMap K V

/-- Target of one existing `ChainStep`. Forward and backward stay distinct. -/
def stepTarget (N : ℕ) : ChainStep → ArchiveRolePhaseGroup N → ArchiveRolePhaseGroup N
  | .fwd r, x => roleTranslatePlus N r x
  | .bwd r, x => roleTranslateMinus N r x

/-- Endpoint of a `ChainStep` word, in the same left-to-right order as `pathTransport`. -/
def pathEnd (N : ℕ) : List ChainStep → ArchiveRolePhaseGroup N → ArchiveRolePhaseGroup N
  | [], x => x
  | s :: rest, x => pathEnd N rest (stepTarget N s x)

@[simp] theorem pathEnd_nil (x : ArchiveRolePhaseGroup N) : pathEnd N [] x = x := rfl

@[simp] theorem pathEnd_cons (s : ChainStep) (rest : List ChainStep)
    (x : ArchiveRolePhaseGroup N) :
    pathEnd N (s :: rest) x = pathEnd N rest (stepTarget N s x) := rfl

theorem pathEnd_append (p q : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    pathEnd N (p ++ q) x = pathEnd N q (pathEnd N p x) := by
  induction p generalizing x with
  | nil => rfl
  | cons s rest ih =>
      simp only [List.cons_append, pathEnd_cons, ih]

/-- Affine pull of one oriented step. Backward is the inverse of the stored forward link. -/
def affineStepMap (A : AffineCartanConnection N K V) :
    ChainStep → ArchiveRolePhaseGroup N → AffineCartanMap K V
  | .fwd r, x => A x r
  | .bwd r, x => (A (roleTranslateMinus N r x) r)⁻¹

/-- Left-to-right affine path value. Later steps act on the vector first. -/
def affinePath (A : AffineCartanConnection N K V) :
    List ChainStep → ArchiveRolePhaseGroup N → AffineCartanMap K V
  | [], _ => 1
  | s :: rest, x => affineStepMap A s x * affinePath A rest (stepTarget N s x)

/-- Covariant translation sum `θ₁ + U₁ θ₂ + U₁ U₂ θ₃ + ⋯`. -/
def covariantShift (A : AffineCartanConnection N K V) :
    List ChainStep → ArchiveRolePhaseGroup N → V
  | [], _ => 0
  | s :: rest, x =>
      (affineStepMap A s x).shift +
        (affineStepMap A s x).lin (covariantShift A rest (stepTarget N s x))

/-- Linear path factor `U₁ ⋯ Uₘ`, applied rightmost first. -/
def covariantLin (A : AffineCartanConnection N K V) :
    List ChainStep → ArchiveRolePhaseGroup N → V ≃ₗ[K] V
  | [], _ => LinearEquiv.refl K V
  | s :: rest, x =>
      (covariantLin A rest (stepTarget N s x)).trans (affineStepMap A s x).lin

theorem affinePath_append (A : AffineCartanConnection N K V)
    (p q : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    affinePath A (p ++ q) x = affinePath A p x * affinePath A q (pathEnd N p x) := by
  induction p generalizing x with
  | nil => simp [affinePath, AffineCartanMap.affine_one_mul]
  | cons s rest ih =>
      simp only [List.cons_append, affinePath, pathEnd_cons, ih, AffineCartanMap.affine_mul_assoc]

theorem stepTarget_reverse (s : ChainStep) (x : ArchiveRolePhaseGroup N) :
    stepTarget N (reverseStep s) (stepTarget N s x) = x := by
  cases s with
  | fwd r => simp [stepTarget, reverseStep, roleTranslate_inverse_minus]
  | bwd r => simp [stepTarget, reverseStep, roleTranslate_inverse_plus]

theorem pathEnd_reverse (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    pathEnd N ((steps.map reverseStep).reverse) (pathEnd N steps x) = x := by
  induction steps generalizing x with
  | nil => simp
  | cons s rest ih =>
      simp only [List.map_cons, List.reverse_cons, pathEnd_cons, pathEnd_append, pathEnd_nil]
      rw [ih]
      exact stepTarget_reverse s x

theorem affineStepMap_reverse (A : AffineCartanConnection N K V)
    (s : ChainStep) (x : ArchiveRolePhaseGroup N) :
    affineStepMap A (reverseStep s) (stepTarget N s x) = (affineStepMap A s x)⁻¹ := by
  cases s with
  | fwd r =>
      simp [affineStepMap, reverseStep, stepTarget, roleTranslate_inverse_minus]
  | bwd r =>
      simp [affineStepMap, reverseStep, stepTarget, roleTranslate_inverse_plus,
        AffineCartanMap.affine_inv_inv]

theorem affinePath_reverse (A : AffineCartanConnection N K V)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    affinePath A ((steps.map reverseStep).reverse) (pathEnd N steps x) =
      (affinePath A steps x)⁻¹ := by
  induction steps generalizing x with
  | nil => simp [affinePath, AffineCartanMap.affine_inv_one]
  | cons s rest ih =>
      calc
        affinePath A (((s :: rest).map reverseStep).reverse) (pathEnd N (s :: rest) x) =
            affinePath A ((rest.map reverseStep).reverse ++ [reverseStep s])
              (pathEnd N rest (stepTarget N s x)) := by
              simp [pathEnd_cons, List.map_cons, List.reverse_cons]
        _ = affinePath A (rest.map reverseStep).reverse (pathEnd N rest (stepTarget N s x)) *
              affineStepMap A (reverseStep s)
                (pathEnd N (rest.map reverseStep).reverse (pathEnd N rest (stepTarget N s x))) := by
              rw [affinePath_append]
              simp [affinePath, pathEnd]
        _ = (affinePath A rest (stepTarget N s x))⁻¹ *
              (affineStepMap A s x)⁻¹ := by
              rw [ih, pathEnd_reverse, affineStepMap_reverse]
        _ = (affineStepMap A s x * affinePath A rest (stepTarget N s x))⁻¹ := by
              symm
              exact AffineCartanMap.affine_inv_mul_mul _ _
        _ = (affinePath A (s :: rest) x)⁻¹ := by simp [affinePath]

theorem affinePath_shift_eq_covariant_sum (A : AffineCartanConnection N K V)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    (affinePath A steps x).shift = covariantShift A steps x := by
  induction steps generalizing x with
  | nil => simp [affinePath, covariantShift]
  | cons s rest ih =>
      simp only [affinePath, covariantShift, AffineCartanMap.mul_shift, ih]

theorem affinePath_lin_eq_covariant (A : AffineCartanConnection N K V)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    (affinePath A steps x).lin = covariantLin A steps x := by
  induction steps generalizing x with
  | nil => simp [affinePath, covariantLin]
  | cons s rest ih =>
      simp only [affinePath, covariantLin, AffineCartanMap.mul_lin, ih]

/-- Conjugation `U'_{xy} = h_x U_{xy} h_y⁻¹` on one positive link. -/
def affineGaugeLink (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (x : ArchiveRolePhaseGroup N) (r : Role) : AffineCartanMap K V :=
  h x * A x r * (h (roleTranslatePlus N r x))⁻¹

def affineGauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V) :
    AffineCartanConnection N K V :=
  fun x r => affineGaugeLink h A x r

theorem affineGauge_lin (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    (affineGauge h A x r).lin =
      ((h (roleTranslatePlus N r x)).lin.symm).trans
        ((A x r).lin.trans (h x).lin) := by
  simp [affineGauge, affineGaugeLink]

theorem affineGauge_shift (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    (affineGauge h A x r).shift =
      (h x).lin (A x r).shift + (h x).shift -
        (affineGauge h A x r).lin (h (roleTranslatePlus N r x)).shift := by
  simp only [affineGauge, affineGaugeLink, AffineCartanMap.mul_shift, AffineCartanMap.mul_lin,
    AffineCartanMap.inv_shift, AffineCartanMap.inv_lin, LinearEquiv.trans_apply, map_add, map_neg,
    LinearEquiv.apply_symm_apply]
  abel

theorem affineStepMap_gauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (s : ChainStep) (x : ArchiveRolePhaseGroup N) :
    affineStepMap (affineGauge h A) s x =
      h x * affineStepMap A s x * (h (stepTarget N s x))⁻¹ := by
  cases s with
  | fwd r =>
      simp [affineStepMap, affineGauge, affineGaugeLink, stepTarget]
  | bwd r =>
      have hback :
          affineStepMap (affineGauge h A) (ChainStep.bwd r) x =
            (h (roleTranslateMinus N r x) * A (roleTranslateMinus N r x) r *
              (h x)⁻¹)⁻¹ := by
        simp [affineStepMap, affineGauge, affineGaugeLink, stepTarget,
          roleTranslate_inverse_plus]
      rw [hback, AffineCartanMap.affine_inv_mul_mul, AffineCartanMap.affine_inv_mul_mul,
        AffineCartanMap.affine_inv_inv]
      simp [affineStepMap, stepTarget, AffineCartanMap.affine_mul_assoc]

theorem affinePath_gauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (steps : List ChainStep) (x : ArchiveRolePhaseGroup N) :
    affinePath (affineGauge h A) steps x =
      h x * affinePath A steps x * (h (pathEnd N steps x))⁻¹ := by
  induction steps generalizing x with
  | nil =>
      simp [affinePath, AffineCartanMap.affine_mul_one, AffineCartanMap.affine_mul_inv]
  | cons s rest ih =>
      simp only [affinePath, pathEnd_cons, affineStepMap_gauge, ih]
      exact AffineCartanMap.conj_mul_conj _ _ _ _ _

/-! ## Flat translation gauge is the owned forward coframe

`U = I`, `g = I`, and `b_x = -L ξ(x)` give the exact finite identity
`θ'_r - θ_r = L (ξ(x+r) - ξ(x))`. This is `forwardGaugeCoframe`, not a derivative.
-/

noncomputable def flatAffineConnection (N : ℕ) : AffineCartanConnection N ℝ (Role → ℝ) :=
  fun _ _ => 1

/-- Node translation `b_x = -L ξ(x)` with trivial linear gauge. -/
noncomputable def translationGauge (N : ℕ) (xi : LocalRoleVector N) :
    AffineNodeGauge N ℝ (Role → ℝ) :=
  fun x =>
    { lin := LinearEquiv.refl ℝ (Role → ℝ)
      shift := -forwardDifferenceScale N • xi x }

theorem affineTranslation_shift_difference (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r : Role) :
    (affineGauge (translationGauge N xi) (flatAffineConnection N) x r).shift -
        (flatAffineConnection N x r).shift =
      fun a => forwardDifferenceScale N * (xi (roleTranslatePlus N r x) a - xi x a) := by
  ext a
  simp only [affineGauge, affineGaugeLink, flatAffineConnection, translationGauge,
    AffineCartanMap.mul_shift, AffineCartanMap.mul_lin, AffineCartanMap.inv_shift,
    AffineCartanMap.one_lin, AffineCartanMap.one_shift, LinearEquiv.trans_apply,
    LinearEquiv.refl_apply, LinearEquiv.refl_symm, map_neg, map_zero, Pi.sub_apply,
    Pi.smul_apply, smul_eq_mul, add_zero, zero_add, sub_zero]
  simp [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, sub_eq_add_neg]
  ring

/-- Exact finite weld of the flat affine translation to `forwardGaugeCoframe`. -/
theorem affineTranslation_flat_eq_forwardGaugeCoframe (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    (affineGauge (translationGauge N xi) (flatAffineConnection N) x r).shift a =
      forwardGaugeCoframe N xi x r a := by
  have hdiff := congrFun (affineTranslation_shift_difference xi x r) a
  simp only [flatAffineConnection, AffineCartanMap.one_shift, sub_zero, Pi.sub_apply] at hdiff
  simpa [forwardGaugeCoframe, forwardDifference_apply] using hdiff

/-! ## Open curvature and torsion of an affine square

The two positive square words stay unquotiented. `F` is their linear difference
and `T` is their translation difference.
-/

def affineSquareA (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : AffineCartanMap K V :=
  affinePath A [ChainStep.fwd r, ChainStep.fwd s] x

def affineSquareB (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : AffineCartanMap K V :=
  affinePath A [ChainStep.fwd s, ChainStep.fwd r] x

def squareFar (N : ℕ) (r s : Role) (x : ArchiveRolePhaseGroup N) : ArchiveRolePhaseGroup N :=
  roleTranslatePlus N s (roleTranslatePlus N r x)

theorem pathEnd_squareA (r s : Role) (x : ArchiveRolePhaseGroup N) :
    pathEnd N [ChainStep.fwd r, ChainStep.fwd s] x = squareFar N r s x := by
  simp [pathEnd, stepTarget, squareFar]

theorem pathEnd_squareB (r s : Role) (x : ArchiveRolePhaseGroup N) :
    pathEnd N [ChainStep.fwd s, ChainStep.fwd r] x = squareFar N r s x := by
  simp [pathEnd, stepTarget, squareFar, roleTranslate_comm]

theorem affineSquareA_eq (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    affineSquareA A r s x = A x r * A (roleTranslatePlus N r x) s := by
  simp [affineSquareA, affinePath, affineStepMap, stepTarget, AffineCartanMap.affine_mul_one]

theorem affineSquareB_eq (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    affineSquareB A r s x = A x s * A (roleTranslatePlus N s x) r := by
  simp [affineSquareB, affinePath, affineStepMap, stepTarget, AffineCartanMap.affine_mul_one]

/-- Linear open curvature `F = A - B`. -/
def affineOpenCurvature (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : V →ₗ[K] V :=
  (affineSquareA A r s x).lin.toLinearMap - (affineSquareB A r s x).lin.toLinearMap

/-- Translation defect `T = a - b`. -/
def affineOpenTorsion (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : V :=
  (affineSquareA A r s x).shift - (affineSquareB A r s x).shift

theorem affineOpenTorsion_expand (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    affineOpenTorsion A r s x =
      (A x r).shift + (A x r).lin (A (roleTranslatePlus N r x) s).shift -
        ((A x s).shift + (A x s).lin (A (roleTranslatePlus N s x) r).shift) := by
  simp [affineOpenTorsion, affineSquareA_eq, affineSquareB_eq, AffineCartanMap.mul_shift]

theorem affineOpen_eq_zero_iff_square_values_eq (A : AffineCartanConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    affineOpenCurvature A r s x = 0 ∧ affineOpenTorsion A r s x = 0 ↔
      affineSquareA A r s x = affineSquareB A r s x := by
  constructor
  · intro ⟨hF, hT⟩
    apply AffineCartanMap.ext
    · exact LinearEquiv.toLinearMap_injective (sub_eq_zero.mp hF)
    · exact sub_eq_zero.mp hT
  · intro h
    refine ⟨?_, ?_⟩
    · simp [affineOpenCurvature, h]
    · simp [affineOpenTorsion, h]

theorem affineSquare_gauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    affineSquareA (affineGauge h A) r s x =
      h x * affineSquareA A r s x * (h (squareFar N r s x))⁻¹ ∧
    affineSquareB (affineGauge h A) r s x =
      h x * affineSquareB A r s x * (h (squareFar N r s x))⁻¹ := by
  constructor
  · have hpath := affinePath_gauge h A [ChainStep.fwd r, ChainStep.fwd s] x
    rw [pathEnd_squareA] at hpath
    simpa [affineSquareA] using hpath
  · have hpath := affinePath_gauge h A [ChainStep.fwd s, ChainStep.fwd r] x
    rw [pathEnd_squareB] at hpath
    simpa [affineSquareB] using hpath

theorem affineOpenCurvature_gauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    affineOpenCurvature (affineGauge h A) r s x =
      (h x).lin.toLinearMap.comp
        ((affineOpenCurvature A r s x).comp
          (h (squareFar N r s x)).lin.symm.toLinearMap) := by
  ext v
  obtain ⟨hA, hB⟩ := affineSquare_gauge h A r s x
  simp only [affineOpenCurvature, LinearMap.sub_apply, LinearMap.comp_apply,
    LinearEquiv.coe_toLinearMap, hA, hB, AffineCartanMap.mul_lin, AffineCartanMap.inv_lin,
    LinearEquiv.trans_apply, map_sub]

theorem affineOpenTorsion_gauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    affineOpenTorsion (affineGauge h A) r s x =
      (h x).lin (affineOpenTorsion A r s x) -
        affineOpenCurvature (affineGauge h A) r s x (h (squareFar N r s x)).shift := by
  obtain ⟨hA, hB⟩ := affineSquare_gauge h A r s x
  have hshift (φ : AffineCartanMap K V) :
      (h x * φ * (h (squareFar N r s x))⁻¹).shift =
        (h x).lin φ.shift + (h x).shift -
          (h x * φ * (h (squareFar N r s x))⁻¹).lin (h (squareFar N r s x)).shift := by
    simp only [AffineCartanMap.mul_shift, AffineCartanMap.mul_lin, AffineCartanMap.inv_shift,
      AffineCartanMap.inv_lin, LinearEquiv.trans_apply, map_neg, LinearEquiv.apply_symm_apply]
    abel
  simp only [affineOpenTorsion, hA, hB, hshift, affineOpenCurvature, LinearMap.sub_apply,
    LinearEquiv.coe_toLinearMap, map_sub]
  abel

/-- If the gauged torsion were the pure vector `g_x T`, then `F'` would kill `b_y`. -/
theorem openTorsion_pure_vector_implies_curvature_kills_shift
    (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N)
    (hpure : affineOpenTorsion (affineGauge h A) r s x =
      (h x).lin (affineOpenTorsion A r s x)) :
    affineOpenCurvature (affineGauge h A) r s x (h (squareFar N r s x)).shift = 0 := by
  have hlaw := affineOpenTorsion_gauge h A r s x
  rw [hpure] at hlaw
  exact sub_eq_self.mp hlaw.symm

noncomputable def ratScale (c : ℚ) (hc : c ≠ 0) : ℚ ≃ₗ[ℚ] ℚ where
  toFun z := c * z
  invFun z := c⁻¹ * z
  left_inv z := by field_simp [hc]
  right_inv z := by field_simp [hc]
  map_add' z w := by ring
  map_smul' a z := by simp [mul_left_comm, mul_assoc]

/-- A positive role step does not fix the zero site. -/
theorem roleTranslate_zero_ne (t : Role) :
    roleTranslatePlus 0 t (fun _ => (0 : ZMod (archiveFibers 0))) ≠ fun _ => 0 := by
  intro hxt
  have hcoord := congrFun hxt t
  simp only [roleTranslatePlus_apply, Pi.add_apply, roleStep] at hcoord
  have hone : (1 : ZMod (archiveFibers 0)) = 0 := by simpa using hcoord
  have hdiv : archiveFibers 0 ∣ 1 :=
    (ZMod.natCast_eq_zero_iff (1 : ℕ) (archiveFibers 0)).mp (by simpa using hone)
  exact absurd (Nat.dvd_one.mp hdiv) (by decide : archiveFibers 0 ≠ 1)

/-- Curvature can mix the far translation into open torsion, so `T' ≠ g_x T`. -/
theorem openTorsion_gauge_not_pure_vector :
    ∃ (r s : Role) (x : ArchiveRolePhaseGroup 0)
      (A : AffineCartanConnection 0 ℚ ℚ) (h : AffineNodeGauge 0 ℚ ℚ),
      affineOpenTorsion A r s x = 0 ∧
      affineOpenCurvature (affineGauge h A) r s x (h (squareFar 0 r s x)).shift ≠ 0 ∧
      affineOpenTorsion (affineGauge h A) r s x ≠
        (h x).lin (affineOpenTorsion A r s x) := by
  let r : Role := (0, 0)
  let s : Role := (0, 1)
  let x : ArchiveRolePhaseGroup 0 := fun _ => 0
  let two : ℚ ≃ₗ[ℚ] ℚ := ratScale 2 (by norm_num)
  have hsr : s ≠ r := by decide
  let A : AffineCartanConnection 0 ℚ ℚ := fun y t =>
    if y = x ∧ t = r then { lin := two, shift := 0 } else 1
  let yfar : ArchiveRolePhaseGroup 0 := squareFar 0 r s x
  have hyfar : yfar ≠ x := by
    intro hxy
    have hcoord := congrFun hxy r
    simp only [yfar, squareFar, roleTranslatePlus_apply, Pi.add_apply, roleStep, x, hsr] at hcoord
    have hone : (1 : ZMod (archiveFibers 0)) = 0 := by simpa using hcoord
    have hdiv : archiveFibers 0 ∣ 1 :=
      (ZMod.natCast_eq_zero_iff (1 : ℕ) (archiveFibers 0)).mp (by simpa using hone)
    exact absurd (Nat.dvd_one.mp hdiv) (by decide : archiveFibers 0 ≠ 1)
  have hA : affineSquareA A r s x = { lin := two, shift := 0 } := by
    simp only [affineSquareA_eq, A]
    rw [if_pos (by simp)]
    rw [if_neg (by rintro ⟨hxy, _⟩; exact roleTranslate_zero_ne r hxy)]
    simp [AffineCartanMap.mul_shift, AffineCartanMap.mul_lin, LinearEquiv.refl_apply]
  have hB : affineSquareB A r s x = 1 := by
    simp only [affineSquareB_eq, A]
    rw [if_neg (by rintro ⟨_, hts⟩; exact hsr hts)]
    rw [if_neg (by rintro ⟨hxy, _⟩; exact roleTranslate_zero_ne s hxy)]
    simp
  let hG : AffineNodeGauge 0 ℚ ℚ := fun z =>
    if z = yfar then { lin := LinearEquiv.refl ℚ ℚ, shift := 1 } else 1
  have hgx : (hG x).lin = LinearEquiv.refl ℚ ℚ := by
    simp [hG, if_neg (Ne.symm hyfar)]
  have hgy : (hG yfar).lin = LinearEquiv.refl ℚ ℚ := by simp [hG]
  have hb : (hG yfar).shift = 1 := by simp [hG]
  have hT : affineOpenTorsion A r s x = 0 := by simp [affineOpenTorsion, hA, hB]
  have hF : affineOpenCurvature A r s x 1 = 1 := by
    simp [affineOpenCurvature, hA, hB, LinearMap.sub_apply, two, ratScale]
    norm_num
  have hhit : affineOpenCurvature (affineGauge hG A) r s x (hG yfar).shift = 1 := by
    rw [hb]
    have hraw := (LinearMap.ext_iff.mp (affineOpenCurvature_gauge hG A r s x)) (1 : ℚ)
    rw [hgx, hgy] at hraw
    simp only [LinearMap.comp_apply, LinearEquiv.coe_toLinearMap, LinearEquiv.refl_apply,
      LinearEquiv.refl_symm] at hraw
    rw [hF] at hraw
    exact hraw
  refine ⟨r, s, x, A, hG, hT, ?_, ?_⟩
  · rw [hhit]
    exact one_ne_zero
  · intro hpure
    have h0 := openTorsion_pure_vector_implies_curvature_kills_shift hG A r s x hpure
    rw [hhit] at h0
    exact one_ne_zero h0

/-! ## Based affine holonomy

`(P, t) = (A, a)(B, b)⁻¹` is based at the starting fibre.
`F = (P - I) B` and `t = T + (I - P) b` keep the two torsion tensors distinct.
-/

def affineBasedHolonomy (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : AffineCartanMap K V :=
  affineSquareA A r s x * (affineSquareB A r s x)⁻¹

theorem affineBasedHolonomy_lin (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    (affineBasedHolonomy A r s x).lin =
      ((affineSquareB A r s x).lin.symm).trans (affineSquareA A r s x).lin := by
  simp [affineBasedHolonomy]

theorem affineBasedHolonomy_shift (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    (affineBasedHolonomy A r s x).shift =
      (affineSquareA A r s x).shift -
        (affineBasedHolonomy A r s x).lin (affineSquareB A r s x).shift := by
  simp only [affineBasedHolonomy, AffineCartanMap.mul_shift, AffineCartanMap.inv_shift,
    AffineCartanMap.mul_lin, LinearEquiv.trans_apply, map_neg]
  abel

theorem open_based_curvature_relation (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    affineOpenCurvature A r s x =
      ((affineBasedHolonomy A r s x).lin.toLinearMap - (LinearMap.id : V →ₗ[K] V)).comp
        (affineSquareB A r s x).lin.toLinearMap := by
  ext v
  simp only [affineOpenCurvature, affineBasedHolonomy_lin, LinearMap.sub_apply,
    LinearMap.comp_apply, LinearMap.id_apply, LinearEquiv.coe_toLinearMap, LinearEquiv.trans_apply]
  rw [LinearEquiv.symm_apply_apply]

theorem open_based_torsion_relation (A : AffineCartanConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    (affineBasedHolonomy A r s x).shift =
      affineOpenTorsion A r s x +
        ((LinearMap.id : V →ₗ[K] V) - (affineBasedHolonomy A r s x).lin.toLinearMap)
          (affineSquareB A r s x).shift := by
  simp only [affineOpenTorsion, affineBasedHolonomy_shift, LinearMap.sub_apply, LinearMap.id_apply,
    LinearEquiv.coe_toLinearMap]
  abel

theorem affineBasedHolonomy_gauge (h : AffineNodeGauge N K V) (A : AffineCartanConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    affineBasedHolonomy (affineGauge h A) r s x =
      h x * affineBasedHolonomy A r s x * (h x)⁻¹ := by
  obtain ⟨hA, hB⟩ := affineSquare_gauge h A r s x
  simp only [affineBasedHolonomy, hA, hB]
  calc
    (h x * affineSquareA A r s x * (h (squareFar N r s x))⁻¹) *
        (h x * affineSquareB A r s x * (h (squareFar N r s x))⁻¹)⁻¹ =
      (h x * affineSquareA A r s x * (h (squareFar N r s x))⁻¹) *
        ((h (squareFar N r s x)) * (affineSquareB A r s x)⁻¹ * (h x)⁻¹) := by
          rw [AffineCartanMap.affine_inv_mul_mul, AffineCartanMap.affine_inv_mul_mul,
            AffineCartanMap.affine_inv_inv]
          simp [AffineCartanMap.affine_mul_assoc]
    _ = h x * (affineSquareA A r s x * (affineSquareB A r s x)⁻¹) * (h x)⁻¹ := by
          simpa [AffineCartanMap.affine_mul_assoc] using
            AffineCartanMap.conj_mul_conj (h x) (affineSquareA A r s x)
              (h (squareFar N r s x)) (affineSquareB A r s x)⁻¹ (h x)

/-- Based gauge law `P' = g_x P g_x⁻¹` and `t' = g_x t + (I - P') b_x`. -/
theorem affineBasedHolonomy_gauge_lin (h : AffineNodeGauge N K V)
    (A : AffineCartanConnection N K V) (r s : Role) (x : ArchiveRolePhaseGroup N) :
    (affineBasedHolonomy (affineGauge h A) r s x).lin =
      ((h x).lin.symm).trans
        ((affineBasedHolonomy A r s x).lin.trans (h x).lin) := by
  simp [affineBasedHolonomy_gauge]

theorem affineBasedHolonomy_gauge_shift (h : AffineNodeGauge N K V)
    (A : AffineCartanConnection N K V) (r s : Role) (x : ArchiveRolePhaseGroup N) :
    (affineBasedHolonomy (affineGauge h A) r s x).shift =
      (h x).lin (affineBasedHolonomy A r s x).shift +
        ((LinearMap.id : V →ₗ[K] V) -
            (affineBasedHolonomy (affineGauge h A) r s x).lin.toLinearMap)
          (h x).shift := by
  rw [affineBasedHolonomy_gauge]
  simp only [AffineCartanMap.mul_shift, AffineCartanMap.mul_lin, AffineCartanMap.inv_shift,
    AffineCartanMap.inv_lin, LinearEquiv.trans_apply, map_neg, LinearEquiv.apply_symm_apply,
    LinearMap.sub_apply, LinearMap.id_apply, LinearEquiv.coe_toLinearMap]
  abel

/-- Based and open torsion differ when `(I - P)` moves the square-`B` translation. -/
theorem based_torsion_ne_open_torsion
    (A : AffineCartanConnection N K V) (r s : Role) (x : ArchiveRolePhaseGroup N)
    (hmove : ((LinearMap.id : V →ₗ[K] V) - (affineBasedHolonomy A r s x).lin.toLinearMap)
        (affineSquareB A r s x).shift ≠ 0) :
    (affineBasedHolonomy A r s x).shift ≠ affineOpenTorsion A r s x := by
  intro hEq
  have hrel := open_based_torsion_relation A r s x
  rw [hEq] at hrel
  apply hmove
  have hzero :
      ((LinearMap.id : V →ₗ[K] V) - (affineBasedHolonomy A r s x).lin.toLinearMap)
          (affineSquareB A r s x).shift = 0 := by
    apply add_left_cancel (a := affineOpenTorsion A r s x)
    simpa [add_zero] using hrel.symm
  exact hzero

theorem based_torsion_ne_open_torsion_witness :
    ∃ φ ψ : AffineCartanMap ℚ ℚ,
      (φ * ψ⁻¹).lin ≠ LinearEquiv.refl ℚ ℚ ∧
      (φ * ψ⁻¹).shift ≠ φ.shift - ψ.shift := by
  let two : ℚ ≃ₗ[ℚ] ℚ := ratScale 2 (by norm_num)
  let φ : AffineCartanMap ℚ ℚ := { lin := two, shift := 0 }
  let ψ : AffineCartanMap ℚ ℚ := { lin := LinearEquiv.refl ℚ ℚ, shift := 1 }
  refine ⟨φ, ψ, ?_, ?_⟩
  · intro hlin
    have happly := congrFun (congrArg DFunLike.coe hlin) (1 : ℚ)
    simp [φ, ψ, two, ratScale, AffineCartanMap.mul_lin, AffineCartanMap.inv_lin,
      LinearEquiv.trans_apply, LinearEquiv.refl_apply] at happly
  · intro hshift
    simp [φ, ψ, two, ratScale, AffineCartanMap.mul_shift, AffineCartanMap.inv_shift,
      AffineCartanMap.mul_lin, LinearEquiv.trans_apply, LinearEquiv.refl_apply, map_neg] at hshift

/-! ## Period two keeps both oriented slots -/

theorem affine_oriented_links_not_collapsed_at_period_two
    (hL : archiveFibers N = 2) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N r (roleTranslatePlus N r x) = x ∧
      ∃ A : AffineCartanConnection N ℂ ℂ,
        A x r ≠ A (roleTranslatePlus N r x) r := by
  obtain ⟨hret, hslot⟩ := oriented_links_not_collapsed_at_period_two hL r x
  refine ⟨hret, ?_⟩
  rcases hslot with ⟨U, hU⟩
  refine ⟨fun y t => { lin := U y t, shift := 0 }, ?_⟩
  intro hEq
  exact hU (congrArg AffineCartanMap.lin hEq)

theorem affine_period_two_square_uses_both_slots
    (hL : archiveFibers N = 2) (A : AffineCartanConnection N K V) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    affineSquareA A r r x = A x r * A (roleTranslatePlus N r x) r ∧
      roleTranslatePlus N r (roleTranslatePlus N r x) = x := by
  exact ⟨affineSquareA_eq A r r x, period_two_double_step hL r x⟩

end D0.Geometry
