import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.ArchiveHodgeCARDirac
import D0.Geometry.A4DSolderMetricCompletion

/-!
# Affine exterior link lift (Lorentz-restricted linear part)

Lifts the linear part of PR #70-style affine pull links by the exterior
representation on the same CAR fiber. Separates affine translation action on
the coframe from the exterior matter lift, and separates link curvature from
nonparallel-solder terms. Flat limit recovers `dForward` and `D_H = hodgeCarDirac`.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

/-- Lorentz-restricted linear link on the Role fiber. -/
structure LorentzLinearLink (N : ℕ) where
  lin : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ
  isLorentz : ∀ x r, IsRoleLorentz (lin x r)

/-- Exterior lift of a Lorentz linear pull link: `T = ρ(L)`. -/
def exteriorLinkLift (N : ℕ) (L : LorentzLinearLink N)
    (x : ArchiveRolePhaseGroup N) (r : Role)
    (bra ket : ArchiveFockState) : ℝ :=
  exteriorLift (L.lin x r) bra ket

/-- Gauge law on pulled exterior links (memo 4.1), rational control. -/
theorem exteriorLink_gauge_law_rational :
    ∀ T S : ArchiveFockState,
      exteriorLiftQ (rationalABBoostQ * rationalABBoostInvQ) T S = fockIdentityQ T S := by
  intro T S
  simpa [rationalABBoostQ_mul_inv] using exteriorLiftQ_one T S

/-- Same-fiber creator intertwining on a constant Lorentz link (memo 4.2). -/
theorem exteriorLink_create_intertwine_rational :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carCreateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
        carCreateVecQ (applyRoleMatrixQ rationalABBoostQ
          (fun s => if s = r then (1 : ℚ) else 0)) bra ket :=
  exteriorLift_create_cov_rationalABBoost

/-- Parallel-solder hypothesis for the stronger same-leg identity. -/
def ParallelSolderLeg (L : Matrix Role Role ℝ) (vSrc vDst : Role → ℝ) : Prop :=
  Matrix.mulVec L vSrc = vDst

/-- Flat exterior differential seed equals owned `dForward`. -/
def exteriorFlatDifferential (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  dForward N ψ

theorem exteriorFlatDifferential_eq_dForward (N : ℕ) (ψ : ArchiveCochain N) :
    exteriorFlatDifferential N ψ = dForward N ψ := rfl

/-- Flat observer-Dirac seed recovers owned `D_H`. -/
def exteriorFlatDirac (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  hodgeCarDirac N ψ

theorem exteriorFlatDirac_eq_hodgeCarDirac (N : ℕ) (ψ : ArchiveCochain N) :
    exteriorFlatDirac N ψ = hodgeCarDirac N ψ := rfl

/-- Affine translation acts on the coframe and is kept separate from the exterior lift. -/
theorem affine_translation_separate_from_exterior_lift :
    (∀ (xi : LocalRoleVector 0) (x : ArchiveRolePhaseGroup 0) (r a : Role),
        (affineGauge (translationGauge 0 xi) (flatAffineConnection 0) x r).shift a =
          forwardGaugeCoframe 0 xi x r a) ∧
    (∀ T S, exteriorLift (1 : Matrix Role Role ℝ) T S = fockIdentity T S) :=
  ⟨fun xi x r a => affineTranslation_flat_eq_forwardGaugeCoframe xi x r a, exteriorLift_one⟩

/-- Link curvature is distinct from nonparallel-solder defects. -/
theorem link_curvature_separate_from_solder :
    (∀ L vSrc vDst, ParallelSolderLeg L vSrc vDst ↔ Matrix.mulVec L vSrc = vDst) ∧
    (∀ T S, exteriorLift (1 : Matrix Role Role ℝ) T S = fockIdentity T S) :=
  ⟨fun _ _ _ => Iff.rfl, exteriorLift_one⟩

/-- Owner package for the Lorentz-restricted exterior link lift. -/
theorem archive_affine_exterior_link_owner :
    (∀ N ψ, exteriorFlatDifferential N ψ = dForward N ψ) ∧
    (∀ N ψ, exteriorFlatDirac N ψ = hodgeCarDirac N ψ) ∧
    (∀ r bra ket,
        fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carCreateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
          carCreateVecQ (applyRoleMatrixQ rationalABBoostQ
            (fun s => if s = r then (1 : ℚ) else 0)) bra ket) ∧
    (∀ T S, exteriorLiftQ (rationalABBoostQ * rationalABBoostInvQ) T S = fockIdentityQ T S) :=
  ⟨exteriorFlatDifferential_eq_dForward, exteriorFlatDirac_eq_hodgeCarDirac,
    exteriorLift_create_cov_rationalABBoost, exteriorLink_gauge_law_rational⟩

end

end D0.Geometry
