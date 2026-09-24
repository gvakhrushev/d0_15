import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic
import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.ArchiveRolePhaseGroup

/-!
# Transverse Hessian modulus

`d_f` on uncentered coframes has kernel the constant internal vectors, image
dimension `4 (L^4 - 1)` and codimension `12 L^4 + 4`. The squared plaquette curl
vanishes on `im d_f` because forward differences commute. A concrete coframe has
nonzero curl, so it lies outside that image.

Vanishing of this curl does not produce a Lorentz-covariant deformation.
-/

namespace D0.Geometry

open scoped BigOperators

noncomputable section

def coframeDifferential (N : ℕ) : LocalRoleVector N →ₗ[ℝ] LocalCoframeField N where
  toFun := forwardGaugeCoframe N
  map_add' xi eta := by
    funext x r a
    simp only [forwardGaugeCoframe, Pi.add_apply]
    have h := congrFun (forwardDifference_add N r (fun y => xi y a) (fun y => eta y a)) x
    simpa [Pi.add_apply] using h
  map_smul' t xi := by
    funext x r a
    simp only [forwardGaugeCoframe, Pi.smul_apply, RingHom.id_apply]
    have h := congrFun (forwardDifference_smul N r t (fun y => xi y a)) x
    simpa [Pi.smul_apply] using h

lemma forwardDifferenceScale_ne_zero (N : ℕ) : forwardDifferenceScale N ≠ 0 := by
  simp only [forwardDifferenceScale, archiveFibers]
  exact_mod_cast (show N + 2 ≠ 0 by omega)

theorem coframeDifferential_apply (N : ℕ) (xi : LocalRoleVector N) :
    coframeDifferential N xi = forwardGaugeCoframe N xi := rfl

theorem coframeDifferential_ker_iff (N : ℕ) (xi : LocalRoleVector N) :
    coframeDifferential N xi = 0 ↔
      ∀ a r x, xi (roleTranslatePlus N r x) a = xi x a := by
  constructor
  · intro h a r x
    have happ := congrFun (congrFun (congrFun h x) r) a
    simp only [coframeDifferential_apply, forwardGaugeCoframe, forwardDifference_apply,
      Pi.zero_apply] at happ
    have hmul := mul_eq_zero.mp happ
    cases hmul with
    | inl h0 => exact absurd h0 (forwardDifferenceScale_ne_zero N)
    | inr hsub =>
        exact sub_eq_zero.mp hsub
  · intro h
    funext x r a
    simp only [coframeDifferential_apply, forwardGaugeCoframe, forwardDifference_apply, h,
      sub_self, mul_zero, Pi.zero_apply]

private lemma invariant_nsmul {N : ℕ} (f : ArchiveRolePhaseGroup N → ℝ)
    (g : ArchiveRolePhaseGroup N) (h : ∀ x, f (x + g) = f x) :
    ∀ k : ℕ, ∀ x, f (x + k • g) = f x := by
  intro k
  induction k with
  | zero =>
      intro x
      simp
  | succ k ih =>
      intro x
      rw [succ_nsmul, ← add_assoc, h, ih]

private lemma phase_decompose (N : ℕ) (v : ArchiveRolePhaseGroup N) :
    v = ∑ r : Role, (v r).val • roleStep N r := by
  funext s
  simp only [Finset.sum_apply, Pi.smul_apply, roleStep]
  rw [Finset.sum_eq_single s]
  · simpa using (ZMod.natCast_zmod_val (v s)).symm
  · intro r _ hr
    simp [if_neg (Ne.symm hr)]
  · intro hs
    exact absurd (Finset.mem_univ _) hs

private lemma translationInvariant_const (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ)
    (h : ∀ r x, f (roleTranslatePlus N r x) = f x) (x : ArchiveRolePhaseGroup N) :
    f x = f 0 := by
  classical
  have hstep : ∀ r x, f (x + roleStep N r) = f x := by
    intro r x
    simpa [roleTranslatePlus_apply] using h r x
  have hsum : ∀ t : Finset Role,
      f (∑ r ∈ t, (x r).val • roleStep N r) = f 0 := by
    intro t
    induction t using Finset.induction with
    | empty => simp
    | @insert r t hr ih =>
        rw [Finset.sum_insert hr, add_comm]
        have hmove := invariant_nsmul f (roleStep N r) (hstep r) (x r).val
          (∑ s ∈ t, (x s).val • roleStep N s)
        rw [ih] at hmove
        exact hmove
  have hdec := phase_decompose N x
  rw [hdec]
  exact hsum Finset.univ

theorem coframeDifferential_ker_constant (N : ℕ) (xi : LocalRoleVector N) :
    coframeDifferential N xi = 0 ↔ ∀ x a, xi x a = xi 0 a := by
  constructor
  · intro h x a
    have hinv := (coframeDifferential_ker_iff N xi).1 h a
    exact translationInvariant_const N (fun y => xi y a) (fun r y => hinv r y) x
  · intro h
    apply (coframeDifferential_ker_iff N xi).2
    intro a r x
    rw [h (roleTranslatePlus N r x) a, h x a]

def constantInternalVector (N : ℕ) (c : Role → ℝ) : LocalRoleVector N :=
  fun _ a => c a

theorem constantInternalVector_ker (N : ℕ) (c : Role → ℝ) :
    coframeDifferential N (constantInternalVector N c) = 0 := by
  apply (coframeDifferential_ker_constant N _).2
  intro x a
  rfl

noncomputable def coframeKernelEquiv (N : ℕ) :
    (Role → ℝ) ≃ₗ[ℝ] LinearMap.ker (coframeDifferential N) where
  toFun c := ⟨constantInternalVector N c, by
    rw [LinearMap.mem_ker]
    exact constantInternalVector_ker N c⟩
  invFun ξ := fun a => ξ.1 0 a
  left_inv c := by
    funext a
    rfl
  right_inv ξ := by
    ext x a
    have hker : coframeDifferential N ξ.1 = 0 := by
      simpa [LinearMap.mem_ker] using ξ.2
    have hx := (coframeDifferential_ker_constant N ξ.1).1 hker x a
    simpa [constantInternalVector] using hx.symm
  map_add' c d := by
    ext x a
    rfl
  map_smul' t c := by
    ext x a
    simp [constantInternalVector, Pi.smul_apply, smul_eq_mul]

private lemma finrank_role_arrow : Module.finrank ℝ (Role → ℝ) = 4 := by
  rw [Module.finrank_pi ℝ, card_role]

private lemma finrank_nested_role :
    Module.finrank ℝ (Role → Role → ℝ) = 16 := by
  rw [Module.finrank_pi_fintype ℝ]
  simp only [finrank_role_arrow, Finset.sum_const, Finset.card_univ, card_role]
  norm_num

theorem localRoleVector_finrank (N : ℕ) :
    Module.finrank ℝ (LocalRoleVector N) = 4 * archiveModes N := by
  rw [Module.finrank_pi_fintype ℝ]
  simp only [finrank_role_arrow, Finset.sum_const, Finset.card_univ,
    card_archive_role_phase_group, smul_eq_mul, Nat.mul_comm]

theorem localCoframe_finrank (N : ℕ) :
    Module.finrank ℝ (LocalCoframeField N) = 16 * archiveModes N := by
  rw [Module.finrank_pi_fintype ℝ]
  simp only [finrank_nested_role, Finset.sum_const, Finset.card_univ,
    card_archive_role_phase_group, smul_eq_mul, Nat.mul_comm]

theorem coframeDifferential_finrank_ker (N : ℕ) :
    Module.finrank ℝ (LinearMap.ker (coframeDifferential N)) = 4 := by
  rw [← LinearEquiv.finrank_eq (coframeKernelEquiv N), finrank_role_arrow]

theorem coframeDifferential_finrank_range (N : ℕ) :
    Module.finrank ℝ (LinearMap.range (coframeDifferential N)) =
      4 * (archiveModes N - 1) := by
  have hrank := LinearMap.finrank_range_add_finrank_ker (coframeDifferential N)
  rw [localRoleVector_finrank, coframeDifferential_finrank_ker] at hrank
  have hmode : 1 ≤ archiveModes N := by
    rw [archiveModes, archiveFibers]
    exact Nat.one_le_pow 4 (N + 2) (Nat.succ_pos (N + 1))
  have ⟨k, hk⟩ := Nat.le.dest hmode
  have hrange := Nat.eq_sub_of_add_eq hrank
  have hsub : (1 + k) - 1 = k := by rw [Nat.add_comm, Nat.add_sub_cancel]
  rw [hrange, ← hk, Nat.mul_add, hsub, Nat.mul_one, Nat.add_comm, Nat.add_sub_cancel]

theorem coframeDifferential_codimension (N : ℕ) :
    Module.finrank ℝ (LocalCoframeField N ⧸ LinearMap.range (coframeDifferential N)) =
      12 * archiveModes N + 4 := by
  have hquot :=
    (LinearMap.range (coframeDifferential N)).finrank_quotient_add_finrank
  rw [localCoframe_finrank, coframeDifferential_finrank_range] at hquot
  have hmode : 1 ≤ archiveModes N := by
    rw [archiveModes, archiveFibers]
    exact Nat.one_le_pow 4 (N + 2) (Nat.succ_pos (N + 1))
  have ⟨k, hk⟩ := Nat.le.dest hmode
  have hq := Nat.eq_sub_of_add_eq hquot
  have hsub : (1 + k) - 1 = k := by rw [Nat.add_comm, Nat.add_sub_cancel]
  rw [hq, ← hk, hsub, Nat.mul_add, Nat.mul_one]
  omega

/-- Unsquired plaquette curl. -/
def plaquetteCurl (N : ℕ) (e : LocalCoframeField N) (r s a : Role)
    (x : ArchiveRolePhaseGroup N) : ℝ :=
  forwardDifference N r (fun y => e y s a) x -
    forwardDifference N s (fun y => e y r a) x

/-- Squared curl, the transverse witness density. -/
def plaquetteCurlSquare (N : ℕ) (e : LocalCoframeField N) (r s a : Role)
    (x : ArchiveRolePhaseGroup N) : ℝ :=
  plaquetteCurl N e r s a x ^ 2

theorem exactCoframe_plaquetteCurl_zero (N : ℕ) (xi : LocalRoleVector N) (r s a : Role)
    (x : ArchiveRolePhaseGroup N) :
    plaquetteCurl N (forwardGaugeCoframe N xi) r s a x = 0 := by
  simp only [plaquetteCurl, forwardGaugeCoframe]
  have hcomm := congrFun (forwardDifference_comm N r s (fun y => xi y a)) x
  rw [hcomm]
  ring

theorem exactCoframe_plaquetteCurlSquare_zero (N : ℕ) (xi : LocalRoleVector N)
    (r s a : Role) (x : ArchiveRolePhaseGroup N) :
    plaquetteCurlSquare N (forwardGaugeCoframe N xi) r s a x = 0 := by
  simp [plaquetteCurlSquare, exactCoframe_plaquetteCurl_zero]

/-- A coframe supported on one B-component along the A-axis. -/
def transverseCurlWitness (N : ℕ) : LocalCoframeField N :=
  fun x r a => if r = B ∧ a = A ∧ x A = 0 then 1 else 0

theorem transverseCurlWitness_nonzero (N : ℕ) :
    plaquetteCurl N (transverseCurlWitness N) A B A 0 ≠ 0 := by
  have hAB : A ≠ B := by decide
  have hne : (1 : ZMod (archiveFibers N)) ≠ 0 := by
    intro h
    have hdiv : archiveFibers N ∣ 1 := (ZMod.natCast_eq_zero_iff 1 (archiveFibers N)).mp h
    have : archiveFibers N ≤ 1 := Nat.le_of_dvd (by decide) hdiv
    simp [archiveFibers] at this
  simp only [plaquetteCurl, forwardDifference_apply, transverseCurlWitness, roleTranslatePlus_apply]
  simp [roleStep, hAB, hne]
  exact forwardDifferenceScale_ne_zero N

theorem transverseCurlWitness_outside_image (N : ℕ) :
    ∀ xi : LocalRoleVector N, forwardGaugeCoframe N xi ≠ transverseCurlWitness N := by
  intro xi h
  have hcurl := exactCoframe_plaquetteCurl_zero N xi A B A 0
  rw [h] at hcurl
  exact transverseCurlWitness_nonzero N hcurl

end

end D0.Geometry
