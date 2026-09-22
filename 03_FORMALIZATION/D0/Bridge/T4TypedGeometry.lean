import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Geometry.Manifold.VectorBundle.Riemannian
import Mathlib.LinearAlgebra.QuadraticForm.Signature
import D0.Geometry.A4DSymRoleCentralDifference

namespace D0.Bridge

open D0
open Bundle
open scoped Bundle ContDiff Manifold

noncomputable section

/-!
Typed fixed-torus geometry for the finite local response layer.

This module deliberately stops at actual smooth metric data and pointwise tensor types.  It does
not introduce a jet wrapper, a limit, frame erasure, or an Einstein/Lovelock object.
-/

/-- The fixed smooth four-torus used by the local comparison layer. -/
abbrev T4 := (Circle × Circle) × (Circle × Circle)

abbrev T4E :=
  ((EuclideanSpace ℝ (Fin 1) × EuclideanSpace ℝ (Fin 1)) ×
    (EuclideanSpace ℝ (Fin 1) × EuclideanSpace ℝ (Fin 1)))

abbrev T4ChartModel :=
  ModelProd (ModelProd (EuclideanSpace ℝ (Fin 1)) (EuclideanSpace ℝ (Fin 1)))
    (ModelProd (EuclideanSpace ℝ (Fin 1)) (EuclideanSpace ℝ (Fin 1)))

/-- The product manifold model inherited from the four pinned smooth circle factors. -/
abbrev T4I := ((𝓡 1).prod (𝓡 1)).prod ((𝓡 1).prod (𝓡 1))

example : ChartedSpace T4ChartModel T4 := inferInstance

example : IsManifold T4I ω T4 := inferInstance

abbrev T4Tangent (x : T4) := TangentSpace T4I x

/-- A concrete covariant 2-tensor at a point of `T4`. -/
abbrev Cov2At (x : T4) := LinearMap.BilinForm ℝ (T4Tangent x)

/-- A covariant 2-tensor carrying literal symmetry of its actual bilinear form. -/
structure SymCov2At (x : T4) where
  toBilin : Cov2At x
  symmetric : ∀ v w, toBilin v w = toBilin w v

@[ext] theorem SymCov2At.ext {x : T4} {A B : SymCov2At x}
    (h : A.toBilin = B.toBilin) : A = B := by
  cases A
  cases B
  simp only at h
  subst h
  rfl

theorem SymCov2At.entry_symmetric {x : T4} (A : SymCov2At x)
    (v w : T4Tangent x) : A.toBilin v w = A.toBilin w v :=
  A.symmetric v w

abbrev T4MetricFiber :=
  T4E →L[ℝ] T4E →L[ℝ] ℝ

abbrev T4MetricSection :=
  (x : T4) → T4Tangent x →L[ℝ] T4Tangent x →L[ℝ] ℝ

def continuousBilinToBilin {V : Type*} [AddCommGroup V] [Module ℝ V]
    [TopologicalSpace V] [ContinuousAdd V] [ContinuousSMul ℝ V]
    (B : V →L[ℝ] V →L[ℝ] ℝ) : LinearMap.BilinForm ℝ V :=
  { toFun := fun v => (B v).toLinearMap
    map_add' := by
      intro v w
      ext z
      simp
    map_smul' := by
      intro a v
      ext z
      simp }

/-- An actual nondegenerate bilinear form has no nonzero vector orthogonal to every vector. -/
def BilinNondegenerate {V : Type*} [AddCommGroup V] [Module ℝ V]
    (B : LinearMap.BilinForm ℝ V) : Prop :=
  ∀ v, (∀ w, B v w = 0) → v = 0

/--
An actual smooth Lorentz metric data package on the fixed torus.

The load-bearing field is the dependent family of continuous bilinear maps on the actual tangent
fibres.  Symmetry, nondegeneracy, and the two quadratic-form signature indices are attached to that
family, while `smooth` uses the same bundle-section shape as Mathlib's smooth Riemannian metric.
-/
structure SmoothLorentzMetric where
  bilinear : T4MetricSection
  symmetric : ∀ x v w, bilinear x v w = bilinear x w v
  nondegenerate : ∀ x, BilinNondegenerate (continuousBilinToBilin (bilinear x))
  sigPos : ∀ x, sigPos (continuousBilinToBilin (bilinear x)).toQuadraticMap = 1
  sigNeg : ∀ x, sigNeg (continuousBilinToBilin (bilinear x)).toQuadraticMap = 3
  smooth : ContMDiff T4I (T4I.prod 𝓘(ℝ, T4MetricFiber)) ω
    (fun x => TotalSpace.mk' T4MetricFiber (E := fun _ : T4 => T4MetricFiber) x (bilinear x))

abbrev SmoothMetric := SmoothLorentzMetric

def metricBilin (g : SmoothLorentzMetric) (x : T4) : Cov2At x :=
  continuousBilinToBilin (g.bilinear x)

theorem metricBilin_symmetric (g : SmoothLorentzMetric) (x : T4)
    (v w : T4Tangent x) : metricBilin g x v w = metricBilin g x w v :=
  g.symmetric x v w

theorem metricBilin_nondegenerate (g : SmoothLorentzMetric) (x : T4) :
    BilinNondegenerate (metricBilin g x) :=
  g.nondegenerate x

theorem metricBilin_sigPos (g : SmoothLorentzMetric) (x : T4) :
    sigPos (metricBilin g x).toQuadraticMap = 1 :=
  g.sigPos x

theorem metricBilin_sigNeg (g : SmoothLorentzMetric) (x : T4) :
    sigNeg (metricBilin g x).toQuadraticMap = 3 :=
  g.sigNeg x

end
end D0.Bridge
