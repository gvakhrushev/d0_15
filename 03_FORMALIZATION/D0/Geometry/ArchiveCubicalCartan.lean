import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveCubicalDifferential

namespace D0.Geometry

open D0
open scoped BigOperators

/-!
# D0.Geometry.ArchiveCubicalCartan

Forward finite Cartan calculus on the literal archive cubical cochain carrier.

  i_xi = sum_r M_(xi^r) c_r
  L_xi^f = d_f i_xi + i_xi d_f

The capstone in this module is only the finite coframe/metric reconstruction
`cartanMetricVariation = symmetricRoleGradient`.  It does not assert Hodge-action Ward
covariance, stress conservation, continuum Diff invariance, state selection, or Einstein
coupling.
-/

/-- CAR contraction with a site-dependent role vector. -/
noncomputable def contraction (N : ℕ) (xi : LocalRoleVector N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    ∑ r : Role,
      xi p.1 r *
        (∑ ket : ArchiveFockState,
          carAnnihilate r p.2 ket * ψ (p.1, ket))

@[simp] theorem contraction_zero (N : ℕ) (xi : LocalRoleVector N) :
    contraction N xi (0 : ArchiveCochain N) = 0 := by
  funext p
  simp [contraction]

theorem contraction_add (N : ℕ) (xi : LocalRoleVector N)
    (ψ φ : ArchiveCochain N) :
    contraction N xi (ψ + φ) =
      contraction N xi ψ + contraction N xi φ := by
  funext p
  simp [contraction]
  ring

theorem contraction_smul (N : ℕ) (xi : LocalRoleVector N)
    (c : ℝ) (ψ : ArchiveCochain N) :
    contraction N xi (c • ψ) = c • contraction N xi ψ := by
  funext p
  simp [contraction]
  ring

/-- Contraction at a site only sees the vector and cochain at that site. -/
theorem contraction_point_congr (N : ℕ)
    (xi eta : LocalRoleVector N) (ψ φ : ArchiveCochain N)
    (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState)
    (hxi : ∀ r, xi x r = eta x r)
    (hψ : ∀ ket, ψ (x, ket) = φ (x, ket)) :
    contraction N xi ψ (x, bra) = contraction N eta φ (x, bra) := by
  unfold contraction
  apply Finset.sum_congr rfl
  intro r hr
  rw [hxi r]
  congr 1
  apply Finset.sum_congr rfl
  intro ket hk
  rw [hψ ket]

/-- Contraction lowers a positive homogeneous degree by one. -/
theorem contraction_degree_lower (N k : ℕ) (xi : LocalRoleVector N)
    (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N (k + 1) ψ) :
    HomogeneousCochain N k (contraction N xi ψ) := by
  classical
  intro x bra hbra
  unfold contraction
  apply Finset.sum_eq_zero
  intro r hr
  apply mul_eq_zero_of_right
  apply Finset.sum_eq_zero
  intro ket hk
  by_cases hc : carAnnihilate r bra ket = 0
  · simp [hc]
  · have hdeg := carAnnihilate_degree_lower r bra ket hc
    have hket : fockDegree ket ≠ k + 1 := by
      intro hkdeg
      apply hbra
      omega
    have hx := hψ x ket hket
    simp [hc, hx]

/-- A degree-zero cochain is killed by contraction. -/
theorem contraction_degree_zero (N : ℕ) (xi : LocalRoleVector N)
    (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N 0 ψ) :
    contraction N xi ψ = 0 := by
  classical
  funext p
  unfold contraction
  apply Finset.sum_eq_zero
  intro r hr
  apply mul_eq_zero_of_right
  apply Finset.sum_eq_zero
  intro ket hk
  by_cases hc : carAnnihilate r p.2 ket = 0
  · simp [hc]
  · have hdeg := carAnnihilate_degree_lower r p.2 ket hc
    have hket : fockDegree ket ≠ 0 := by omega
    have hx := hψ p.1 ket hket
    simp [hc, hx]

/-- Forward Cartan operator L_xi^f = d i_xi + i_xi d. -/
noncomputable def cartanForward (N : ℕ) (xi : LocalRoleVector N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  dForward N (contraction N xi ψ) +
    contraction N xi (dForward N ψ)

/-- Degree preservation of the forward Cartan operator. -/
theorem cartanForward_degree_preserving (N k : ℕ) (xi : LocalRoleVector N)
    (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cartanForward N xi ψ) := by
  cases k with
  | zero =>
      have hi0 : contraction N xi ψ = 0 :=
        contraction_degree_zero N xi ψ hψ
      have hfirst :
          HomogeneousCochain N 0 (dForward N (contraction N xi ψ)) := by
        rw [hi0, dForward_zero]
        exact homogeneousCochain_zero N 0
      have hd :
          HomogeneousCochain N 1 (dForward N ψ) := by
        simpa using dForward_degree_raise N 0 ψ hψ
      have hsecond :
          HomogeneousCochain N 0 (contraction N xi (dForward N ψ)) := by
        exact contraction_degree_lower N 0 xi (dForward N ψ) (by simpa using hd)
      simpa [cartanForward] using
        homogeneousCochain_add N 0
          (dForward N (contraction N xi ψ))
          (contraction N xi (dForward N ψ)) hfirst hsecond
  | succ k =>
      have hψ' : HomogeneousCochain N (k + 1) ψ := by
        simpa [Nat.succ_eq_add_one] using hψ
      have hi :
          HomogeneousCochain N k (contraction N xi ψ) :=
        contraction_degree_lower N k xi ψ hψ'
      have hfirst :
          HomogeneousCochain N (k + 1)
            (dForward N (contraction N xi ψ)) :=
        dForward_degree_raise N k (contraction N xi ψ) hi
      have hd :
          HomogeneousCochain N ((k + 1) + 1) (dForward N ψ) :=
        dForward_degree_raise N (k + 1) ψ hψ'
      have hsecond :
          HomogeneousCochain N (k + 1)
            (contraction N xi (dForward N ψ)) :=
        contraction_degree_lower N (k + 1) xi (dForward N ψ) hd
      simpa [cartanForward, Nat.succ_eq_add_one] using
        homogeneousCochain_add N (k + 1)
          (dForward N (contraction N xi ψ))
          (contraction N xi (dForward N ψ)) hfirst hsecond

/-- Cartan is radius one: at x it uses only x and the four forward neighbours. -/
theorem cartanForward_radius_one (N : ℕ)
    (xi eta : LocalRoleVector N) (ψ φ : ArchiveCochain N)
    (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState)
    (hxi :
      ∀ r s,
        xi x s = eta x s ∧
        xi (roleTranslatePlus N r x) s =
          eta (roleTranslatePlus N r x) s)
    (hψ :
      ∀ r ket,
        ψ (x, ket) = φ (x, ket) ∧
        ψ (roleTranslatePlus N r x, ket) =
          φ (roleTranslatePlus N r x, ket)) :
    cartanForward N xi ψ (x, bra) =
      cartanForward N eta φ (x, bra) := by
  have hfirst :
      dForward N (contraction N xi ψ) (x, bra) =
        dForward N (contraction N eta φ) (x, bra) := by
    apply dForward_radius_one
    intro r ket
    constructor
    · apply contraction_point_congr N xi eta ψ φ x ket
      · intro s
        exact (hxi r s).1
      · intro state
        exact (hψ r state).1
    · apply contraction_point_congr N xi eta ψ φ
        (roleTranslatePlus N r x) ket
      · intro s
        exact (hxi r s).2
      · intro state
        exact (hψ r state).2
  have hsecond :
      contraction N xi (dForward N ψ) (x, bra) =
        contraction N eta (dForward N φ) (x, bra) := by
    apply contraction_point_congr N xi eta (dForward N ψ) (dForward N φ) x bra
    · intro s
      exact (hxi D0.A s).1
    · intro ket
      exact dForward_radius_one N ψ φ x ket hψ
  simpa [cartanForward] using
    congrArg₂ (fun a b : ℝ => a + b) hfirst hsecond

/-- Exact cochain identity d L_xi^f = L_xi^f d, using only d_f^2 = 0. -/
theorem dForward_cartan_comm (N : ℕ) (xi : LocalRoleVector N)
    (ψ : ArchiveCochain N) :
    dForward N (cartanForward N xi ψ) =
      cartanForward N xi (dForward N ψ) := by
  calc
    dForward N (cartanForward N xi ψ) =
        dForward N (dForward N (contraction N xi ψ)) +
          dForward N (contraction N xi (dForward N ψ)) := by
            rw [cartanForward, dForward_add]
    _ = dForward N (contraction N xi (dForward N ψ)) := by
          rw [dForward_sq_zero]
          simp
    _ = dForward N (contraction N xi (dForward N ψ)) +
          contraction N xi (dForward N (dForward N ψ)) := by
          rw [dForward_sq_zero]
          simp
    _ = cartanForward N xi (dForward N ψ) := rfl

/-! ## Constant-vector reduction -/

/-- Site-independent role vector. -/
def constantRoleVector (N : ℕ) (v : Role → ℝ) : LocalRoleVector N :=
  fun _ r => v r

/-- Pure forward transport by a constant role vector. -/
noncomputable def constantForwardTransport (N : ℕ) (v : Role → ℝ)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    ∑ r : Role,
      v r * forwardDifference N r (fun x => ψ (x, p.2)) p.1

/-- Mixed CAR reduces the constant-vector Cartan operator to ordinary forward transport. -/
theorem cartanForward_constant_vector (N : ℕ) (v : Role → ℝ)
    (ψ : ArchiveCochain N) :
    cartanForward N (constantRoleVector N v) ψ =
      constantForwardTransport N v ψ := by
  -- Expand d i + i d; translation commutes with the constant coefficients.
  -- The Fock coefficient is {c_r,c_s†}=δ_rs I.
  sorry

/-! ## Constant coframes and centered reconstruction -/

/-- Constant basis coframe theta^b represented by the singleton Fock state {b}. -/
def constantCoframe (N : ℕ) (b : Role) : ArchiveCochain N :=
  fun p => if p.2 = singletonFockState b then 1 else 0

/-- Contraction of a constant basis coframe reads the b-component of xi. -/
theorem contraction_constantCoframe (N : ℕ) (xi : LocalRoleVector N) (b : Role) :
    contraction N xi (constantCoframe N b) =
      scalarCochain N (fun x => xi x b) := by
  classical
  funext p
  unfold contraction
  have hinner : ∀ r : Role,
      (∑ ket : ArchiveFockState,
        carAnnihilate r p.2 ket * constantCoframe N b (p.1, ket)) =
        carAnnihilate r p.2 (singletonFockState b) := by
    intro r
    rw [Finset.sum_eq_single (singletonFockState b)]
    · simp [constantCoframe]
    · intro ket _ hket
      simp [constantCoframe, hket]
    · simp
  simp_rw [hinner, carAnnihilate_singleton]
  rw [Finset.sum_eq_single b]
  · simp [roleDelta, fockIdentity, scalarCochain]
  · intro r _ hr
    simp [roleDelta, hr]
  · simp

/-- Constant coframes are d_f-closed. -/
theorem dForward_constantCoframe (N : ℕ) (b : Role) :
    dForward N (constantCoframe N b) = 0 := by
  funext p
  unfold dForward forwardCreateDirection
  apply Finset.sum_eq_zero
  intro r hr
  apply Finset.sum_eq_zero
  intro ket hk
  have hconst :
      forwardDifference N r
        (fun x => constantCoframe N b (x, ket)) = 0 := by
    apply forwardDifference_const
  rw [hconst]
  simp

/-- Finite constant-coframe Cartan identity L_xi theta^b = d_f(xi^b). -/
theorem cartanForward_constantCoframe (N : ℕ)
    (xi : LocalRoleVector N) (b : Role) :
    cartanForward N xi (constantCoframe N b) =
      dForward N (scalarCochain N (fun x => xi x b)) := by
  unfold cartanForward
  rw [contraction_constantCoframe, dForward_constantCoframe]
  simp

/-- Centered coefficient of the Cartan variation of theta^b in direction a. -/
noncomputable def centeredCoframeVariation (N : ℕ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (a b : Role) : ℝ :=
  centerOneForm N (cartanForward N xi (constantCoframe N b)) x a

/-- Exact reconstruction of the centered derivative from the forward Cartan coframe. -/
theorem centeredCoframeVariation_eq_centeredDifference (N : ℕ)
    (xi : LocalRoleVector N) (x : ArchiveRolePhaseGroup N) (a b : Role) :
    centeredCoframeVariation N xi x a b =
      centeredDifference N a (fun y => xi y b) x := by
  unfold centeredCoframeVariation
  rw [cartanForward_constantCoframe]
  have h := centerOneForm_dForward_scalar N (fun y => xi y b)
  exact congrFun (congrFun h x) a

/-- Symmetrized metric variation reconstructed from the centered Cartan coframe response. -/
noncomputable def cartanMetricVariation (N : ℕ)
    (xi : LocalRoleVector N) : LocalSymRoleField N :=
  fun x =>
    { toMatrix := fun a b =>
        centeredCoframeVariation N xi x a b +
          centeredCoframeVariation N xi x b a
      symmetric := by
        intro a b
        ring }

/-- Capstone: the Cartan/coframe construction is exactly the existing centered metric gauge. -/
theorem cartanMetricVariation_eq_symmetricRoleGradient (N : ℕ)
    (xi : LocalRoleVector N) :
    cartanMetricVariation N xi = symmetricRoleGradient N xi := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  change
    centeredCoframeVariation N xi x a b +
        centeredCoframeVariation N xi x b a =
      centeredDifference N a (fun y => xi y b) x +
        centeredDifference N b (fun y => xi y a) x
  rw [centeredCoframeVariation_eq_centeredDifference,
    centeredCoframeVariation_eq_centeredDifference]

end D0.Geometry
