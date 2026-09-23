import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic
import D0.Geometry.A4DRolePairMetricCarrier
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

/-! ## Square equals the open-path curvature

`d_Ω = L ∑_r c_r† (T_r - I)`, so
`d_Ω² = L² ∑_{r<s} c_r† c_s† [T_r, T_s]`.
The strict order is the owned role code `Role ↪ Fin 4`.
Flat plaquettes force `d_Ω² = 0`. The converse is not claimed.
-/

def transportCommutator (U : LinkConnection N ℝ V) (r s : Role)
    (ψ : CoeffCochain N V) : CoeffCochain N V :=
  coeffTransport U r (coeffTransport U s ψ) - coeffTransport U s (coeffTransport U r ψ)

/-- `[T_r, T_s] ψ(x) = F_rs(x) ψ(x+r+s)`. -/
theorem dConn_sq_apply_eq_curvature (U : LinkConnection N ℝ V) (r s : Role)
    (ψ : CoeffCochain N V) (x : ArchiveRolePhaseGroup N) (ket : ArchiveFockState) :
    transportCommutator U r s ψ x ket =
      openCurvature U r s x
        (ψ (roleTranslatePlus N s (roleTranslatePlus N r x)) ket) :=
  coeffTransport_commutator U r s ψ x ket

theorem coeffTransport_sub (U : LinkConnection N ℝ V) (r : Role)
    (ψ φ : CoeffCochain N V) :
    coeffTransport U r (ψ - φ) = coeffTransport U r ψ - coeffTransport U r φ := by
  funext x ket
  simp [coeffTransport, map_sub]

theorem coeffTransport_sum {ι : Type*} [Fintype ι] (U : LinkConnection N ℝ V) (r : Role)
    (ψ : ι → CoeffCochain N V) :
    coeffTransport U r (∑ i, ψ i) = ∑ i, coeffTransport U r (ψ i) := by
  funext x ket
  simp [coeffTransport, map_sum, Finset.sum_apply]

theorem coeffCreate_sub (r : Role) (ψ φ : CoeffCochain N V) :
    coeffCreate r (ψ - φ) = coeffCreate r ψ - coeffCreate r φ := by
  funext x bra
  simp only [coeffCreate, Pi.sub_apply, Finset.sum_sub_distrib, smul_sub]

theorem coeffCreate_sum {ι : Type*} [Fintype ι] (r : Role)
    (ψ : ι → CoeffCochain N V) :
    coeffCreate r (∑ i, ψ i) = ∑ i, coeffCreate r (ψ i) := by
  funext x bra
  simp only [coeffCreate, Finset.sum_apply]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro ket _
  rw [Finset.smul_sum]

theorem coeffCreate_smul (r : Role) (c : ℝ) (ψ : CoeffCochain N V) :
    coeffCreate r (c • ψ) = c • coeffCreate r ψ := by
  funext x bra
  simp only [coeffCreate, Pi.smul_apply, Finset.smul_sum, smul_smul, mul_comm c]

theorem coeffCreate_zero (r : Role) : coeffCreate r (0 : CoeffCochain N V) = 0 := by
  funext x bra
  simp [coeffCreate]

theorem coeffShift_sum {ι : Type*} [Fintype ι] (U : LinkConnection N ℝ V) (r : Role)
    (ψ : ι → CoeffCochain N V) :
    coeffShift U r (∑ i, ψ i) = ∑ i, coeffShift U r (ψ i) := by
  simp [coeffShift, coeffTransport_sum, Finset.sum_sub_distrib]

theorem coeffShift_smul (U : LinkConnection N ℝ V) (r : Role) (c : ℝ)
    (ψ : CoeffCochain N V) :
    coeffShift U r (c • ψ) = c • coeffShift U r ψ := by
  funext x ket
  simp [coeffShift, coeffTransport, map_smul, smul_sub]

theorem coeffCreate_anticomm (r s : Role) (ψ : CoeffCochain N V) :
    coeffCreate r (coeffCreate s ψ) + coeffCreate s (coeffCreate r ψ) = 0 := by
  funext x bra
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [coeffCreate_comp, coeffCreate_comp, ← Finset.sum_add_distrib]
  refine Finset.sum_eq_zero ?_
  intro ket _
  rw [← add_smul, createProduct_antisym, zero_smul]

theorem coeffCreate_sq_zero (r : Role) (ψ : CoeffCochain N V) :
    coeffCreate r (coeffCreate r ψ) = 0 := by
  funext x bra
  rw [coeffCreate_comp]
  refine Finset.sum_eq_zero ?_
  intro ket _
  rw [createProduct_diag, zero_smul]

theorem coeffShift_commutator (U : LinkConnection N ℝ V) (r s : Role)
    (ψ : CoeffCochain N V) :
    coeffShift U r (coeffShift U s ψ) - coeffShift U s (coeffShift U r ψ) =
      transportCommutator U r s ψ := by
  simp only [coeffShift, transportCommutator, coeffTransport_sub]
  abel

theorem coeffCreate_shift_comm (U : LinkConnection N ℝ V) (r s : Role)
    (ψ : CoeffCochain N V) :
    coeffShift U r (coeffCreate s ψ) = coeffCreate s (coeffShift U r ψ) := by
  simp only [coeffShift, coeffCreate_sub]
  rw [coeffCreate_transport_comm]

theorem dConn_eq_sum (U : LinkConnection N ℝ V) (ψ : CoeffCochain N V) :
    dConn U ψ =
      forwardDifferenceScale N • ∑ r : Role, coeffCreate r (coeffShift U r ψ) := by
  funext x bra
  simp only [dConn, Pi.smul_apply, Finset.sum_apply]

theorem dConn_sq_expand (U : LinkConnection N ℝ V) (ψ : CoeffCochain N V) :
    dConn U (dConn U ψ) =
      (forwardDifferenceScale N * forwardDifferenceScale N) •
        ∑ r : Role, ∑ s : Role,
          coeffCreate r (coeffCreate s (coeffShift U r (coeffShift U s ψ))) := by
  rw [dConn_eq_sum]
  have hshift : ∀ r,
      coeffShift U r (dConn U ψ) =
        forwardDifferenceScale N •
          ∑ s : Role, coeffCreate s (coeffShift U r (coeffShift U s ψ)) := by
    intro r
    rw [dConn_eq_sum, coeffShift_smul, coeffShift_sum]
    refine congrArg (fun t => forwardDifferenceScale N • t) ?_
    refine Finset.sum_congr rfl ?_
    intro s _
    exact coeffCreate_shift_comm U r s (coeffShift U s ψ)
  simp only [hshift, coeffCreate_smul, coeffCreate_sum]
  rw [Finset.smul_sum]
  simp only [Finset.smul_sum, smul_smul]

private theorem sum_role_gt_reindex {M : Type*} [AddCommGroup M] (f : Role → Role → M) :
    (∑ r : Role, ∑ s ∈ Finset.univ.filter (fun s => roleCode s < roleCode r), f r s) =
      ∑ r : Role, ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f s r := by
  classical
  simp only [Finset.sum_filter]
  rw [Finset.sum_comm]

private theorem sum_role_pairs {M : Type*} [AddCommGroup M] (f : Role → Role → M)
    (hdiag : ∀ r, f r r = 0) :
    (∑ r : Role, ∑ s : Role, f r s) =
      ∑ r : Role, ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s),
        (f r s + f s r) := by
  classical
  have hpart : ∀ r s,
      f r s =
        (if roleCode r < roleCode s then f r s else 0) +
        (if roleCode s < roleCode r then f r s else 0) +
        (if roleCode s = roleCode r then f r s else 0) := by
    intro r s
    rcases lt_trichotomy (roleCode r) (roleCode s) with h | h | h
    · have hne : roleCode s ≠ roleCode r := (ne_of_lt h).symm
      have hlt : ¬ roleCode s < roleCode r := not_lt_of_gt h
      simp [h, hne, hlt]
    · simp [h]
    · have hne : roleCode s ≠ roleCode r := ne_of_lt h
      have hlt : ¬ roleCode r < roleCode s := not_lt_of_gt h
      simp [h, hne, hlt]
  have hsum : ∀ r, (∑ s, f r s) =
      (∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s) +
      (∑ s ∈ Finset.univ.filter (fun s => roleCode s < roleCode r), f r s) +
      (∑ s ∈ Finset.univ.filter (fun s => roleCode s = roleCode r), f r s) := by
    intro r
    simp only [Finset.sum_filter]
    rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    intro s _
    exact hpart r s
  have hdiagSum : ∀ r,
      (∑ s ∈ Finset.univ.filter (fun s => roleCode s = roleCode r), f r s) = f r r := by
    intro r
    have hset :
        Finset.univ.filter (fun s => roleCode s = roleCode r) = {r} := by
      ext s
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton]
      constructor
      · intro hs
        exact roleCode_injective hs
      · intro hs
        simp [hs]
    rw [hset, Finset.sum_singleton]
  simp only [hsum, hdiagSum, hdiag, add_zero]
  have hsplit :
      (∑ r, ((∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s) +
          ∑ s ∈ Finset.univ.filter (fun s => roleCode s < roleCode r), f r s)) =
        (∑ r, ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s) +
          ∑ r, ∑ s ∈ Finset.univ.filter (fun s => roleCode s < roleCode r), f r s :=
    Finset.sum_add_distrib (s := (Finset.univ : Finset Role))
      (f := fun r => ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s)
      (g := fun r => ∑ s ∈ Finset.univ.filter (fun s => roleCode s < roleCode r), f r s)
  rw [hsplit, sum_role_gt_reindex]
  have hmerge :
      (∑ r, ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s) +
          ∑ r, ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f s r =
        ∑ r, ((∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s) +
          ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f s r) :=
    (Finset.sum_add_distrib (s := (Finset.univ : Finset Role))
      (f := fun r => ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f r s)
      (g := fun r => ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s), f s r)).symm
  rw [hmerge]
  refine Finset.sum_congr rfl ?_
  intro r _
  exact (Finset.sum_add_distrib
      (s := Finset.univ.filter (fun s : Role => roleCode r < roleCode s))
      (f := fun s : Role => f r s) (g := fun s : Role => f s r)).symm

theorem dConn_sq_eq_curvature (U : LinkConnection N ℝ V) (ψ : CoeffCochain N V) :
    dConn U (dConn U ψ) =
      (forwardDifferenceScale N * forwardDifferenceScale N) •
        ∑ r : Role, ∑ s ∈ Finset.univ.filter (fun s => roleCode r < roleCode s),
          coeffCreate r (coeffCreate s (transportCommutator U r s ψ)) := by
  rw [dConn_sq_expand]
  refine congrArg
      (fun t => (forwardDifferenceScale N * forwardDifferenceScale N) • t) ?_
  let f : Role → Role → CoeffCochain N V := fun r s =>
    coeffCreate r (coeffCreate s (coeffShift U r (coeffShift U s ψ)))
  have hdiag : ∀ r, f r r = 0 := by
    intro r
    simpa [f] using coeffCreate_sq_zero r (coeffShift U r (coeffShift U r ψ))
  rw [show (∑ r, ∑ s, coeffCreate r (coeffCreate s (coeffShift U r (coeffShift U s ψ))) =
      ∑ r, ∑ s, f r s) by rfl]
  rw [sum_role_pairs f hdiag]
  refine Finset.sum_congr rfl ?_
  intro r _
  refine Finset.sum_congr rfl ?_
  intro s _
  let A := coeffShift U r (coeffShift U s ψ)
  let B := coeffShift U s (coeffShift U r ψ)
  have hanti := coeffCreate_anticomm r s B
  calc
    f r s + f s r =
        coeffCreate r (coeffCreate s A) + coeffCreate s (coeffCreate r B) := by
          rfl
    _ = coeffCreate r (coeffCreate s A) +
          (-coeffCreate r (coeffCreate s B)) := by
          rw [eq_neg_of_add_eq_zero_right hanti]
    _ = coeffCreate r (coeffCreate s A) - coeffCreate r (coeffCreate s B) := by
          rw [sub_eq_add_neg]
    _ = coeffCreate r (coeffCreate s A - coeffCreate s B) := by
          rw [← coeffCreate_sub]
    _ = coeffCreate r (coeffCreate s (A - B)) := by
          rw [← coeffCreate_sub]
    _ = coeffCreate r (coeffCreate s (transportCommutator U r s ψ)) := by
          rw [show A - B = transportCommutator U r s ψ by
            simpa [A, B] using coeffShift_commutator U r s ψ]

/-- Vanishing open-path curvature forces `d_Ω² = 0`.
The converse needs a richness hypothesis on coefficient sections and is not claimed. -/
theorem dConn_sq_zero_of_flat (U : LinkConnection N ℝ V)
    (hF : ∀ r s (x : ArchiveRolePhaseGroup N), openCurvature U r s x = 0)
    (ψ : CoeffCochain N V) :
    dConn U (dConn U ψ) = 0 := by
  rw [dConn_sq_eq_curvature]
  simp only [smul_eq_zero]
  right
  refine Finset.sum_eq_zero ?_
  intro r _
  refine Finset.sum_eq_zero ?_
  intro s _
  have hcomm : transportCommutator U r s ψ = 0 := by
    funext x ket
    rw [dConn_sq_apply_eq_curvature]
    simp [hF]
  simp [hcomm, coeffCreate_zero]

end

end D0.Geometry
