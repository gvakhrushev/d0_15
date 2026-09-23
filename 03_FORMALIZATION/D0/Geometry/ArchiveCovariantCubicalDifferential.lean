import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveChainCurvature
import D0.Geometry.ArchiveCubicalDifferential

/-!
# Coefficient covariant cubical differential

Creators act on `ArchiveFockState`. Links act on the separate coefficient fibre `V`.

`dConn U = L ∑_r c_r† (T_r - I)`.

The square is the open-path curvature. A curved link is not claimed to be nilpotent.
The Cartan commutator keeps the `ι d² - d² ι` term.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

variable {N : ℕ} {V : Type*} [AddCommGroup V] [Module ℝ V]

abbrev CoeffCochain (N : ℕ) (V : Type*) :=
  ArchiveRolePhaseGroup N → ArchiveFockState → V

def coeffCreate (r : Role) (ψ : CoeffCochain N V) : CoeffCochain N V :=
  fun x bra => ∑ ket : ArchiveFockState, carCreate r bra ket • ψ x ket

def coeffTransport (U : LinkConnection N ℝ V) (r : Role)
    (ψ : CoeffCochain N V) : CoeffCochain N V :=
  fun x ket => (U x r) (ψ (roleTranslatePlus N r x) ket)

def coeffShift (U : LinkConnection N ℝ V) (r : Role)
    (ψ : CoeffCochain N V) : CoeffCochain N V :=
  coeffTransport U r ψ - ψ

/-- `d_Ω = L ∑_r c_r† (T_r - I)`. -/
def dConn (U : LinkConnection N ℝ V) (ψ : CoeffCochain N V) : CoeffCochain N V :=
  fun x bra => forwardDifferenceScale N •
    ∑ r : Role, coeffCreate r (coeffShift U r ψ) x bra

def gaugeCoeff (g : NodeGauge N ℝ V) (ψ : CoeffCochain N V) : CoeffCochain N V :=
  fun x ket => (g x) (ψ x ket)

def createProduct (r s : Role) (bra ket : ArchiveFockState) : ℝ :=
  ∑ mid : ArchiveFockState, carCreate r bra mid * carCreate s mid ket

theorem createProduct_antisym (r s : Role) (bra ket : ArchiveFockState) :
    createProduct r s bra ket + createProduct s r bra ket = 0 := by
  simpa [createProduct, anticommutator] using car_create_anticommutator r s bra ket

theorem createProduct_diag (r : Role) (bra ket : ArchiveFockState) :
    createProduct r r bra ket = 0 := by
  have h := createProduct_antisym r r bra ket
  linear_combination h / 2

theorem coeffCreate_transport_comm (U : LinkConnection N ℝ V) (r s : Role)
    (ψ : CoeffCochain N V) :
    coeffTransport U r (coeffCreate s ψ) = coeffCreate s (coeffTransport U r ψ) := by
  funext x bra
  simp only [coeffTransport, coeffCreate, map_sum, map_smul]

theorem coeffCreate_comp (r s : Role) (ψ : CoeffCochain N V)
    (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState) :
    coeffCreate r (coeffCreate s ψ) x bra =
      ∑ ket : ArchiveFockState, createProduct r s bra ket • ψ x ket := by
  classical
  simp only [coeffCreate, createProduct]
  have hsum :
      (∑ mid, carCreate r bra mid • ∑ ket, carCreate s mid ket • ψ x ket) =
        ∑ mid, ∑ ket, (carCreate r bra mid * carCreate s mid ket) • ψ x ket := by
    refine Finset.sum_congr rfl ?_
    intro mid _
    rw [Finset.smul_sum]
    refine Finset.sum_congr rfl ?_
    intro ket _
    simp [smul_smul]
  rw [hsum, Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro ket _
  rw [← Finset.sum_smul]

theorem coeffTransport_commutator (U : LinkConnection N ℝ V) (r s : Role)
    (ψ : CoeffCochain N V) (x : ArchiveRolePhaseGroup N) (ket : ArchiveFockState) :
    coeffTransport U r (coeffTransport U s ψ) x ket -
        coeffTransport U s (coeffTransport U r ψ) x ket =
      openCurvature U r s x
        (ψ (roleTranslatePlus N s (roleTranslatePlus N r x)) ket) := by
  simpa [coeffTransport] using
    transport_commutator_apply U r s (fun y => ψ y ket) x

theorem dConn_add (U : LinkConnection N ℝ V) (ψ φ : CoeffCochain N V) :
    dConn U (ψ + φ) = dConn U ψ + dConn U φ := by
  funext x bra
  simp only [dConn, coeffCreate, coeffShift, coeffTransport, Pi.add_apply, map_add]
  rw [← smul_add, ← Finset.sum_add_distrib]
  refine congrArg (fun t => forwardDifferenceScale N • t) ?_
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  simp only [coeffTransport, map_add, Pi.add_apply, Pi.sub_apply]
  module

theorem dConn_smul (U : LinkConnection N ℝ V) (c : ℝ) (ψ : CoeffCochain N V) :
    dConn U (c • ψ) = c • dConn U ψ := by
  funext x bra
  simp only [dConn, coeffCreate, coeffShift, coeffTransport, Pi.smul_apply, Pi.sub_apply]
  rw [smul_comm c (forwardDifferenceScale N)]
  congr 1
  rw [Finset.smul_sum]
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [Finset.smul_sum]
  refine Finset.sum_congr rfl ?_
  intro ket _
  simp [map_smul, smul_sub, smul_smul, mul_comm c]

def CoeffHomogeneous (k : ℕ) (ψ : CoeffCochain N V) : Prop :=
  ∀ x ket, fockDegree ket ≠ k → ψ x ket = 0

theorem dConn_raises_degree (U : LinkConnection N ℝ V) (k : ℕ)
    (ψ : CoeffCochain N V) (hψ : CoeffHomogeneous k ψ) :
    CoeffHomogeneous (k + 1) (dConn U ψ) := by
  intro x bra hdeg
  simp only [dConn, coeffCreate, coeffShift, coeffTransport, Pi.sub_apply]
  rw [smul_eq_zero]
  right
  refine Finset.sum_eq_zero ?_
  intro r _
  refine Finset.sum_eq_zero ?_
  intro ket _
  by_cases hc : carCreate r bra ket = 0
  · rw [hc]
    simp
  · have hdeg' := carCreate_degree_raise r bra ket hc
    have hket : fockDegree ket ≠ k := by
      intro hk
      apply hdeg
      omega
    simp [hψ x ket hket, hψ _ ket hket]

theorem dConn_radius_one (U : LinkConnection N ℝ V) (ψ φ : CoeffCochain N V)
    (x : ArchiveRolePhaseGroup N)
    (h : ∀ r ket, ψ x ket = φ x ket ∧
      ψ (roleTranslatePlus N r x) ket = φ (roleTranslatePlus N r x) ket) :
    dConn U ψ x = dConn U φ x := by
  funext bra
  simp only [dConn, coeffCreate, coeffShift, coeffTransport, Pi.sub_apply]
  refine congrArg (fun t => forwardDifferenceScale N • t) ?_
  refine Finset.sum_congr rfl ?_
  intro r _
  refine Finset.sum_congr rfl ?_
  intro ket _
  rw [(h r ket).1, (h r ket).2]

theorem dConn_trivial_eq_dForward (ψ : ArchiveCochain N)
    (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState) :
    dConn (trivialLink N ℝ ℝ) (fun y ket => ψ (y, ket)) x bra =
      dForward N ψ (x, bra) := by
  classical
  simp only [dConn, coeffCreate, coeffShift, coeffTransport, trivialLink,
    LinearEquiv.refl_apply, dForward, forwardCreateDirection, forwardDifference_apply,
    Pi.sub_apply]
  rw [Finset.smul_sum]
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [Finset.smul_sum]
  refine Finset.sum_congr rfl ?_
  intro ket _
  simp only [smul_sub, Algebra.smul_mul_assoc, smul_eq_mul]
  ring

theorem coeffTransport_gauge (g : NodeGauge N ℝ V) (U : LinkConnection N ℝ V)
    (r : Role) (ψ : CoeffCochain N V) :
    coeffTransport (fun y t => gaugeLink g U y t) r (gaugeCoeff g ψ) =
      gaugeCoeff g (coeffTransport U r ψ) := by
  funext x ket
  simpa [coeffTransport, gaugeCoeff] using
    congrFun (transport_gauge g U r (fun y => ψ y ket)) x

theorem dConn_gauge (g : NodeGauge N ℝ V) (U : LinkConnection N ℝ V)
    (ψ : CoeffCochain N V) :
    dConn (fun y t => gaugeLink g U y t) (gaugeCoeff g ψ) =
      gaugeCoeff g (dConn U ψ) := by
  funext x bra
  simp only [dConn, gaugeCoeff, coeffCreate, coeffShift, Pi.sub_apply, map_smul, map_sum,
    map_sub]
  refine congrArg (fun t => forwardDifferenceScale N • t) ?_
  refine Finset.sum_congr rfl ?_
  intro r _
  refine Finset.sum_congr rfl ?_
  intro ket _
  have htr := congrFun (congrFun (coeffTransport_gauge g U r ψ) x) ket
  rw [htr]
  simp [gaugeCoeff, map_sub]

/-- `[dι + ιd, d] = ι d² - d² ι`. The curvature term is not cancelled. -/
theorem operator_cartan_curvature {α : Type*} [AddCommGroup α]
    (d ι : α → α) (a : α) :
    (d (ι (d a)) + ι (d (d a))) - (d (d (ι a)) + d (ι (d a))) =
      ι (d (d a)) - d (d (ι a)) := by
  abel

def cartanGenerator (dOp ι : CoeffCochain N V → CoeffCochain N V)
    (ψ : CoeffCochain N V) : CoeffCochain N V :=
  dOp (ι ψ) + ι (dOp ψ)

theorem cartanConn_comm_dConn (ι : CoeffCochain N V → CoeffCochain N V)
    (U : LinkConnection N ℝ V) (ψ : CoeffCochain N V) :
    cartanGenerator (dConn U) ι (dConn U ψ) -
        dConn U (cartanGenerator (dConn U) ι ψ) =
      ι (dConn U (dConn U ψ)) - dConn U (dConn U (ι ψ)) := by
  simp only [cartanGenerator]
  rw [dConn_add]
  exact operator_cartan_curvature (dConn U) ι ψ

end

end D0.Geometry
