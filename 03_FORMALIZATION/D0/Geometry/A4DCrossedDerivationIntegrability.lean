import Mathlib.Tactic
import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.A4DScalarBackgroundWordMixing
import D0.Geometry.A4DSymRoleCentralDifference
import D0.Geometry.ArchiveCubicalDifferential

/-!
# Scalar crossed first-jet integrability boundary

The degree-zero vertical law inherited from the owned scalar commutator is

`δ_e(U_t) = -(1/L) ∑_r M_{e_t^r} D_r U_t`,

with `D_r = (L/2) (U_r - U_r⁻¹)`. Preserving the compressed torus relations
`U_t^L = I` and `U_s U_t = U_t U_s` forces a zero cycle sum in direction `t`
and the plaquette identity `(U_s - I) e_t^r = (U_t - I) e_s^r`, for period
`L ≥ 3`. Pure gauge `e = d_f ξ` satisfies both. Constant and curl witnesses at
`L = 3` and `L = 5` show each constraint is load-bearing.

At `L = 2` every `D_r` vanishes, so this formula is the zero derivation and
does not impose the cycle-sum constraint. Nothing here is a universal no-go
for other crossed actions, and closedness plus zero periods is not promoted
to exactness.
-/

namespace D0.Geometry

open D0
open Matrix
open scoped BigOperators

section ScalarBridge

variable {n : ℕ} [NeZero n]

private lemma bridge_shift_mul_shiftT :
    scalarCycleShift n * (scalarCycleShift n)ᵀ = 1 := by
  ext i j
  rw [Matrix.mul_apply, Finset.sum_eq_single (i + 1)]
  · simp only [scalarCycleShift, Matrix.transpose_apply, Matrix.one_apply]
    by_cases hij : i = j
    · simp [hij]
    · have hstep : i + 1 ≠ j + 1 := fun h => hij (add_right_cancel h)
      simp [hij, hstep]
  · intro k _ hk
    simp [scalarCycleShift, hk]
  · intro h
    exact absurd (Finset.mem_univ _) h

private lemma bridge_shiftT_mul_shift :
    (scalarCycleShift n)ᵀ * scalarCycleShift n = 1 :=
  (mul_eq_one_comm).mp bridge_shift_mul_shiftT

private lemma bridge_D_mul_shift :
    scalarCycleD n * scalarCycleShift n =
      ((n : ℚ) / 2) • (scalarCycleShift n * scalarCycleShift n - 1) := by
  rw [scalarCycleD, Matrix.smul_mul, sub_mul, bridge_shiftT_mul_shift]

/-- The memo coefficient `-(1/L) M_h D U` is the owned scalar commutator. -/
theorem scalarCandidate_eq_wordMixing (v : Fin n → ℚ) :
    (-(1 / (n : ℚ))) •
        (scalarCycleMul (scalarDisplacement v) * scalarCycleD n *
          scalarCycleShift n) =
      scalarCycleG v * scalarCycleShift n -
        scalarCycleShift n * scalarCycleG v := by
  rw [scalarBackground_wordMixing, mul_assoc, bridge_D_mul_shift, Matrix.mul_smul, smul_smul]
  congr 1
  have hn0 : (n : ℚ) ≠ 0 := by exact_mod_cast (NeZero.ne n)
  field_simp [hn0]

end ScalarBridge

noncomputable section RolePhase

variable {N : ℕ}

def shiftBy (v : ArchiveRolePhaseGroup N) (f : ArchiveRolePhaseGroup N → ℝ) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => f (x + v)

def roleSkew (r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x =>
    (archiveFibers N : ℝ) / 2 *
      (f (x + roleStep N r) - f (x - roleStep N r))

def cycleStep (t : Role) (k : ZMod (archiveFibers N)) : ArchiveRolePhaseGroup N :=
  fun s => if s = t then k else 0

def cycleSum (t : Role) (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) : ℝ :=
  ∑ k : ZMod (archiveFibers N), f (x + cycleStep t k)

def edgeIncrement (s : Role) (f : ArchiveRolePhaseGroup N → ℝ)
    (x : ArchiveRolePhaseGroup N) : ℝ :=
  f (x + roleStep N s) - f x

def translateCoframe (v : ArchiveRolePhaseGroup N) (e : LocalCoframeField N) :
    LocalCoframeField N :=
  fun x s a => e (x + v) s a

/-- Degree-zero candidate `-(1/L) ∑_r M_{e_t^r} D_r`. -/
def scalarShiftResponse (e : LocalCoframeField N) (t : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  fun x =>
    - (1 / (archiveFibers N : ℝ)) *
      ∑ r : Role, e x t r * roleSkew r ψ x

def conjugatedShiftResponse (v : ArchiveRolePhaseGroup N) (e : LocalCoframeField N)
    (t : Role) (ψ : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  shiftBy v (scalarShiftResponse e t (shiftBy (-v) ψ))

def leibnizCycleObstruction (e : LocalCoframeField N) (t : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  ∑ k : ZMod (archiveFibers N),
    conjugatedShiftResponse (cycleStep t k) e t ψ

def commuteObstruction (e : LocalCoframeField N) (s t : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) : ArchiveRolePhaseGroup N → ℝ :=
  (scalarShiftResponse e s ψ -
      scalarShiftResponse (translateCoframe (roleStep N t) e) s ψ) -
    (scalarShiftResponse e t ψ -
      scalarShiftResponse (translateCoframe (roleStep N s) e) t ψ)

private lemma period_ne_zero : (archiveFibers N : ℝ) ≠ 0 := by
  exact_mod_cast (NeZero.ne (archiveFibers N))

private lemma two_ne_zero_zmod (hL : 3 ≤ archiveFibers N) :
    (2 : ZMod (archiveFibers N)) ≠ 0 := by
  intro h
  have hdiv : archiveFibers N ∣ 2 := (ZMod.natCast_eq_zero_iff 2 _).mp h
  have : archiveFibers N ≤ 2 := Nat.le_of_dvd (by decide) hdiv
  omega

private lemma one_ne_neg_one_zmod (hL : 3 ≤ archiveFibers N) :
    (1 : ZMod (archiveFibers N)) ≠ -1 := by
  intro h
  apply two_ne_zero_zmod hL
  have h2 : (1 : ZMod (archiveFibers N)) + 1 = (-1) + 1 := congrArg (fun z => z + 1) h
  simpa using h2

private lemma coord_add_step (x : ArchiveRolePhaseGroup N) (r : Role) :
    (x + roleStep N r) r = x r + 1 := by
  simp [roleStep]

private lemma coord_sub_step (x : ArchiveRolePhaseGroup N) (r : Role) :
    (x - roleStep N r) r = x r - 1 := by
  simp [roleStep, sub_eq_add_neg]

private lemma coord_add_other (x : ArchiveRolePhaseGroup N) {r s : Role} (hs : s ≠ r) :
    (x + roleStep N s) r = x r := by
  simp only [Pi.add_apply, roleStep, if_neg (Ne.symm hs), add_zero]

private lemma coord_sub_other (x : ArchiveRolePhaseGroup N) {r s : Role} (hs : s ≠ r) :
    (x - roleStep N s) r = x r := by
  simp only [Pi.sub_apply, roleStep, if_neg (Ne.symm hs), sub_zero]

private lemma cycleStep_self (t : Role) (k : ZMod (archiveFibers N)) :
    cycleStep t k t = k := by
  simp [cycleStep]

private lemma cycleStep_other {s t : Role} (hs : s ≠ t) (k : ZMod (archiveFibers N)) :
    cycleStep t k s = 0 := by
  simp [cycleStep, hs]

private lemma add_cycleStep_self (x : ArchiveRolePhaseGroup N) (t : Role)
    (k : ZMod (archiveFibers N)) :
    (x + cycleStep t k) t = x t + k := by
  simp [cycleStep]

private lemma add_cycleStep_other (x : ArchiveRolePhaseGroup N) {s t : Role}
    (hs : s ≠ t) (k : ZMod (archiveFibers N)) :
    (x + cycleStep t k) s = x s := by
  simp [cycleStep, hs]

def descentAxisProbe (r : Role) (a : ZMod (archiveFibers N)) : ArchiveRolePhaseGroup N → ℝ :=
  fun y => if y r = a + 1 then (2 : ℝ) / (archiveFibers N : ℝ) else 0

theorem roleSkew_descentAxisProbe (hL : 3 ≤ archiveFibers N) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    roleSkew r (descentAxisProbe r (x r)) x = 1 := by
  have hne : x r - 1 ≠ x r + 1 := by
    intro h
    rw [sub_eq_add_neg] at h
    exact one_ne_neg_one_zmod hL (add_left_cancel h).symm
  have hplus : descentAxisProbe r (x r) (x + roleStep N r) = (2 : ℝ) / (archiveFibers N : ℝ) := by
    simp only [descentAxisProbe, coord_add_step, if_true]
  have hminus : descentAxisProbe r (x r) (x - roleStep N r) = 0 := by
    simp only [descentAxisProbe, coord_sub_step, if_neg hne]
  simp only [roleSkew, hplus, hminus]
  field_simp [period_ne_zero]
  ring

theorem roleSkew_descentAxisProbe_other (hL : 3 ≤ archiveFibers N) (r s : Role)
    (hs : s ≠ r) (x : ArchiveRolePhaseGroup N) :
    roleSkew s (descentAxisProbe r (x r)) x = 0 := by
  have hone : (1 : ZMod (archiveFibers N)) ≠ 0 := by
    intro h
    have hdiv : archiveFibers N ∣ 1 := (ZMod.natCast_eq_zero_iff 1 _).mp h
    have : archiveFibers N ≤ 1 := Nat.le_of_dvd (by decide) hdiv
    omega
  have hplus : descentAxisProbe r (x r) (x + roleStep N s) = 0 := by
    simp [descentAxisProbe, coord_add_other x hs, hone]
  have hminus : descentAxisProbe r (x r) (x - roleStep N s) = 0 := by
    simp [descentAxisProbe, coord_sub_other x hs, hone]
  simp [roleSkew, hplus, hminus]

theorem roleSkew_separates (hL : 3 ≤ archiveFibers N)
    (f : Role → ArchiveRolePhaseGroup N → ℝ)
    (h : ∀ ψ x, ∑ r : Role, f r x * roleSkew r ψ x = 0) :
    ∀ r x, f r x = 0 := by
  intro r x
  have hψ := h (descentAxisProbe r (x r)) x
  rw [Finset.sum_eq_single r] at hψ
  · rw [roleSkew_descentAxisProbe hL r x] at hψ
    simpa using hψ
  · intro s _ hs
    rw [roleSkew_descentAxisProbe_other hL r s hs x]
    ring
  · intro hmiss
    exact absurd (Finset.mem_univ r) hmiss

theorem roleSkew_shift (r : Role) (v x : ArchiveRolePhaseGroup N)
    (ψ : ArchiveRolePhaseGroup N → ℝ) :
    roleSkew r (shiftBy (-v) ψ) (x + v) = roleSkew r ψ x := by
  simp only [roleSkew, shiftBy]
  congr 1
  apply congrArg₂ Sub.sub
  · congr 1
    abel
  · congr 1
    abel

theorem conjugated_eq_translated (v : ArchiveRolePhaseGroup N) (e : LocalCoframeField N)
    (t : Role) (ψ : ArchiveRolePhaseGroup N → ℝ) :
    conjugatedShiftResponse v e t ψ =
      scalarShiftResponse (translateCoframe v e) t ψ := by
  funext x
  simp only [conjugatedShiftResponse, shiftBy, scalarShiftResponse, translateCoframe]
  congr 1
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [roleSkew_shift r v x]

theorem leibnizCycleObstruction_expand (e : LocalCoframeField N) (t : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    leibnizCycleObstruction e t ψ x =
      - (1 / (archiveFibers N : ℝ)) *
        ∑ r : Role, cycleSum t (fun y => e y t r) x * roleSkew r ψ x := by
  simp only [leibnizCycleObstruction, conjugated_eq_translated]
  rw [Finset.sum_apply]
  simp only [scalarShiftResponse, translateCoframe]
  rw [← Finset.mul_sum, Finset.sum_comm]
  simp_rw [← Finset.sum_mul]
  rfl

theorem cycle_relation_forces_zero_period (hL : 3 ≤ archiveFibers N)
    (e : LocalCoframeField N) (t : Role)
    (hpres : ∀ ψ, leibnizCycleObstruction e t ψ = 0) :
    ∀ r x, cycleSum t (fun y => e y t r) x = 0 := by
  let f : Role → ArchiveRolePhaseGroup N → ℝ :=
    fun r x => cycleSum t (fun y => e y t r) x
  have hsum : ∀ ψ x, ∑ r, f r x * roleSkew r ψ x = 0 := by
    intro ψ x
    have hzero := congrFun (hpres ψ) x
    rw [leibnizCycleObstruction_expand] at hzero
    have hc : - (1 / (archiveFibers N : ℝ)) ≠ 0 :=
      neg_ne_zero.mpr (div_ne_zero one_ne_zero period_ne_zero)
    rw [Pi.zero_apply] at hzero
    simpa [f] using (mul_eq_zero.mp hzero).resolve_left hc
  exact roleSkew_separates hL f hsum

private lemma response_sub (e : LocalCoframeField N) (v : ArchiveRolePhaseGroup N)
    (t : Role) (ψ : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    scalarShiftResponse e t ψ x - scalarShiftResponse (translateCoframe v e) t ψ x =
      - (1 / (archiveFibers N : ℝ)) *
        ∑ r : Role, (e x t r - e (x + v) t r) * roleSkew r ψ x := by
  simp only [scalarShiftResponse, translateCoframe]
  calc
    - (1 / (archiveFibers N : ℝ)) * ∑ r, e x t r * roleSkew r ψ x -
        - (1 / (archiveFibers N : ℝ)) * ∑ r, e (x + v) t r * roleSkew r ψ x =
        ∑ r, (- (1 / (archiveFibers N : ℝ)) * (e x t r * roleSkew r ψ x)) -
          ∑ r, (- (1 / (archiveFibers N : ℝ)) * (e (x + v) t r * roleSkew r ψ x)) := by
            simp_rw [Finset.mul_sum]
    _ = ∑ r, (- (1 / (archiveFibers N : ℝ)) * (e x t r * roleSkew r ψ x) -
          - (1 / (archiveFibers N : ℝ)) * (e (x + v) t r * roleSkew r ψ x)) := by
            rw [← Finset.sum_sub_distrib]
    _ = ∑ r, - (1 / (archiveFibers N : ℝ)) *
          ((e x t r - e (x + v) t r) * roleSkew r ψ x) := by
            refine Finset.sum_congr rfl ?_
            intro r _
            ring
    _ = - (1 / (archiveFibers N : ℝ)) *
          ∑ r, (e x t r - e (x + v) t r) * roleSkew r ψ x := by
            rw [← Finset.mul_sum]

theorem commuteObstruction_expand (e : LocalCoframeField N) (s t : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    commuteObstruction e s t ψ x =
      (1 / (archiveFibers N : ℝ)) *
        ∑ r : Role,
          (edgeIncrement t (fun y => e y s r) x -
            edgeIncrement s (fun y => e y t r) x) *
            roleSkew r ψ x := by
  simp only [commuteObstruction, Pi.sub_apply]
  rw [response_sub, response_sub]
  calc
    - (1 / (archiveFibers N : ℝ)) *
          ∑ r, (e x s r - e (x + roleStep N t) s r) * roleSkew r ψ x -
        - (1 / (archiveFibers N : ℝ)) *
          ∑ r, (e x t r - e (x + roleStep N s) t r) * roleSkew r ψ x =
        ∑ r, (- (1 / (archiveFibers N : ℝ)) *
            ((e x s r - e (x + roleStep N t) s r) * roleSkew r ψ x) -
          - (1 / (archiveFibers N : ℝ)) *
            ((e x t r - e (x + roleStep N s) t r) * roleSkew r ψ x)) := by
          simp_rw [Finset.mul_sum]
          rw [← Finset.sum_sub_distrib]
    _ = ∑ r, (1 / (archiveFibers N : ℝ)) *
          ((edgeIncrement t (fun y => e y s r) x -
              edgeIncrement s (fun y => e y t r) x) *
            roleSkew r ψ x) := by
          refine Finset.sum_congr rfl ?_
          intro r _
          simp only [edgeIncrement]
          ring
    _ = (1 / (archiveFibers N : ℝ)) *
          ∑ r, (edgeIncrement t (fun y => e y s r) x -
              edgeIncrement s (fun y => e y t r) x) *
            roleSkew r ψ x := by
          rw [← Finset.mul_sum]

theorem commute_relation_forces_plaquette (hL : 3 ≤ archiveFibers N)
    (e : LocalCoframeField N) (s t : Role)
    (hpres : ∀ ψ, commuteObstruction e s t ψ = 0) :
    ∀ r x,
      edgeIncrement s (fun y => e y t r) x =
        edgeIncrement t (fun y => e y s r) x := by
  intro r x
  let f : Role → ArchiveRolePhaseGroup N → ℝ :=
    fun q z =>
      edgeIncrement t (fun y => e y s q) z - edgeIncrement s (fun y => e y t q) z
  have hsum : ∀ ψ z, ∑ q, f q z * roleSkew q ψ z = 0 := by
    intro ψ z
    have hzero := congrFun (hpres ψ) z
    rw [commuteObstruction_expand] at hzero
    have hc : (1 / (archiveFibers N : ℝ)) ≠ 0 :=
      div_ne_zero one_ne_zero period_ne_zero
    rw [Pi.zero_apply] at hzero
    simpa [f] using (mul_eq_zero.mp hzero).resolve_left hc
  have hz : f r x = 0 := roleSkew_separates hL f hsum r x
  have hdiff : edgeIncrement t (fun y => e y s r) x -
      edgeIncrement s (fun y => e y t r) x = 0 := by
    simpa [f] using hz
  exact (sub_eq_zero.mp hdiff).symm

theorem zero_period_kills_cycle_obstruction (e : LocalCoframeField N) (t : Role)
    (hper : ∀ r x, cycleSum t (fun y => e y t r) x = 0)
    (ψ : ArchiveRolePhaseGroup N → ℝ) :
    leibnizCycleObstruction e t ψ = 0 := by
  funext x
  rw [leibnizCycleObstruction_expand]
  simp [hper]

theorem plaquette_kills_commute_obstruction (e : LocalCoframeField N) (s t : Role)
    (hpl : ∀ r x,
      edgeIncrement s (fun y => e y t r) x =
        edgeIncrement t (fun y => e y s r) x)
    (ψ : ArchiveRolePhaseGroup N → ℝ) :
    commuteObstruction e s t ψ = 0 := by
  funext x
  rw [commuteObstruction_expand]
  simp [hpl, sub_self]

theorem pureGauge_edge_closed (xi : LocalRoleVector N) (s t a : Role)
    (x : ArchiveRolePhaseGroup N) :
    edgeIncrement s (fun y => forwardGaugeCoframe N xi y t a) x =
      edgeIncrement t (fun y => forwardGaugeCoframe N xi y s a) x := by
  simp only [edgeIncrement, forwardGaugeCoframe, forwardDifference_apply, forwardDifferenceScale,
    roleTranslatePlus_apply]
  have hcomm : x + roleStep N s + roleStep N t = x + roleStep N t + roleStep N s := by
    abel
  rw [hcomm]
  ring

theorem pureGauge_cycleSum_zero (xi : LocalRoleVector N) (t a : Role)
    (x : ArchiveRolePhaseGroup N) :
    cycleSum t (fun y => forwardGaugeCoframe N xi y t a) x = 0 := by
  simp only [cycleSum, forwardGaugeCoframe, forwardDifference_apply, forwardDifferenceScale]
  have hstep : ∀ k : ZMod (archiveFibers N),
      x + cycleStep t k + roleStep N t = x + cycleStep t (k + 1) := by
    intro k
    funext s
    by_cases hs : s = t
    · subst hs
      simp [cycleStep, roleStep, add_assoc, add_comm, add_left_comm]
    · simp [cycleStep, roleStep, hs]
  have hsum : ∑ k : ZMod (archiveFibers N),
      xi (x + cycleStep t (k + 1)) a =
        ∑ k : ZMod (archiveFibers N), xi (x + cycleStep t k) a := by
    simpa [add_comm, add_left_comm, add_assoc] using
      (Equiv.sum_comp (Equiv.addRight (1 : ZMod (archiveFibers N)))
        (fun k => xi (x + cycleStep t k) a))
  calc
    ∑ k, (archiveFibers N : ℝ) *
        (xi (x + cycleStep t k + roleStep N t) a - xi (x + cycleStep t k) a) =
        (archiveFibers N : ℝ) * ∑ k,
          (xi (x + cycleStep t (k + 1)) a - xi (x + cycleStep t k) a) := by
            simp_rw [hstep, Finset.mul_sum]
    _ = (archiveFibers N : ℝ) *
        ((∑ k, xi (x + cycleStep t (k + 1)) a) -
          ∑ k, xi (x + cycleStep t k) a) := by
            rw [Finset.sum_sub_distrib]
    _ = (archiveFibers N : ℝ) * 0 := by rw [hsum, sub_self]
    _ = 0 := by ring

theorem pureGauge_preserves_relations (xi : LocalRoleVector N) (s t : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) :
    leibnizCycleObstruction (forwardGaugeCoframe N xi) t ψ = 0 ∧
      commuteObstruction (forwardGaugeCoframe N xi) s t ψ = 0 := by
  refine ⟨zero_period_kills_cycle_obstruction _ _ ?_ _,
      plaquette_kills_commute_obstruction _ _ _ ?_ _⟩
  · intro r x
    exact pureGauge_cycleSum_zero xi t r x
  · intro r x
    exact pureGauge_edge_closed xi s t r x

private lemma neg_step_eq_step_period_two (h : archiveFibers N = 2) (r : Role) :
    - roleStep N r = roleStep N r := by
  funext s
  by_cases hs : s = r
  · subst hs
    simp only [roleStep, Pi.neg_apply, if_true]
    have h2 : (2 : ZMod (archiveFibers N)) = 0 :=
      (ZMod.natCast_eq_zero_iff 2 _).mpr (by simpa [h] using (dvd_refl (2 : ℕ)))
    have hsum : (1 : ZMod (archiveFibers N)) + 1 = 0 := by
      simpa [one_add_one_eq_two] using h2
    exact ((eq_neg_iff_add_eq_zero).mpr hsum).symm
  · simp only [roleStep, Pi.neg_apply, if_neg hs, neg_zero]

theorem roleSkew_period_two (h : archiveFibers N = 2) (r : Role)
    (ψ : ArchiveRolePhaseGroup N → ℝ) :
    roleSkew r ψ = 0 := by
  funext x
  have hstep := neg_step_eq_step_period_two h r
  have hxm : x - roleStep N r = x + roleStep N r := by
    rw [sub_eq_add_neg, hstep]
  simp only [roleSkew, hxm, sub_self, mul_zero, Pi.zero_apply]

theorem scalarShiftResponse_period_two (h : archiveFibers N = 2)
    (e : LocalCoframeField N) (t : Role) (ψ : ArchiveRolePhaseGroup N → ℝ) :
    scalarShiftResponse e t ψ = 0 := by
  funext x
  simp [scalarShiftResponse, roleSkew_period_two h]

/-- Constant `A`-edge. Its cycle sum is the period, while every increment vanishes. -/
def harmonicEdge : LocalCoframeField N :=
  fun _ r a => if r = A ∧ a = A then 1 else 0

theorem harmonicEdge_cycleSum (x : ArchiveRolePhaseGroup N) :
    cycleSum A (fun y => harmonicEdge y A A) x = (archiveFibers N : ℝ) := by
  unfold cycleSum harmonicEdge
  simp only [if_true, and_true]
  simp [Finset.sum_const, Finset.card_univ, ZMod.card, nsmul_eq_mul]

theorem harmonicEdge_cycleSum_ne_zero (x : ArchiveRolePhaseGroup N) :
    cycleSum A (fun y => harmonicEdge y A A) x ≠ 0 := by
  rw [harmonicEdge_cycleSum]
  exact_mod_cast (NeZero.ne (archiveFibers N))

theorem harmonicEdge_increment_zero (s : Role) (x : ArchiveRolePhaseGroup N) :
    edgeIncrement s (fun y => harmonicEdge y A A) x = 0 := by
  simp [edgeIncrement, harmonicEdge]

theorem harmonicEdge_blocks_cycle (hL : 3 ≤ archiveFibers N) :
    ∃ ψ : ArchiveRolePhaseGroup N → ℝ,
      leibnizCycleObstruction harmonicEdge A ψ ≠ 0 := by
  refine ⟨descentAxisProbe A 0, ?_⟩
  intro hzero
  have hAt := congrFun hzero (0 : ArchiveRolePhaseGroup N)
  rw [leibnizCycleObstruction_expand] at hAt
  have hc : - (1 / (archiveFibers N : ℝ)) ≠ 0 :=
    neg_ne_zero.mpr (div_ne_zero one_ne_zero period_ne_zero)
  rw [Pi.zero_apply] at hAt
  have hS := (mul_eq_zero.mp hAt).resolve_left hc
  rw [Finset.sum_eq_single A] at hS
  · have hskew := roleSkew_descentAxisProbe hL A (0 : ArchiveRolePhaseGroup N)
    simp only [Pi.zero_apply] at hskew
    rw [harmonicEdge_cycleSum, hskew] at hS
    exact_mod_cast (NeZero.ne (archiveFibers N)) (by simpa using hS)
  · intro r _ hr
    simp only [harmonicEdge, hr, cycleSum, and_false, if_false, Finset.sum_const_zero, zero_mul]
  · intro hmiss
    exact absurd (Finset.mem_univ A) hmiss

/-- Dipole on the `A`-edge: value `1` at the origin and `-1` at `e_A`. -/
def curlEdge : LocalCoframeField N :=
  fun x r a =>
    if r = A ∧ a = A ∧ x = 0 then 1
    else if r = A ∧ a = A ∧ x = roleStep N A then -1
    else 0

private lemma zmod_zero_ne_one : (0 : ZMod (archiveFibers N)) ≠ 1 := by
  intro h
  have hdiv : archiveFibers N ∣ 1 := (ZMod.natCast_eq_zero_iff 1 _).mp (by simpa using h.symm)
  have : archiveFibers N ≤ 1 := Nat.le_of_dvd (by decide) hdiv
  simp [archiveFibers] at this

private lemma onAxis (x : ArchiveRolePhaseGroup N) :
    (∀ s : Role, s ≠ A → x s = 0) ∨ ∃ s : Role, s ≠ A ∧ x s ≠ 0 := by
  classical
  by_cases h : ∀ s : Role, s ≠ A → x s = 0
  · exact Or.inl h
  · right
    by_contra hno
    apply h
    intro s hs
    by_contra hs0
    exact hno ⟨s, hs, hs0⟩

theorem curlEdge_cycleSum_A (x : ArchiveRolePhaseGroup N) :
    cycleSum A (fun y => curlEdge y A A) x = 0 := by
  classical
  rcases onAxis x with haxis | ⟨s, hs, hsx⟩
  · have h0 : x + cycleStep A (-x A) = 0 := by
      funext q
      by_cases hq : q = A
      · subst hq
        simp [cycleStep]
      · simp [cycleStep, hq, haxis q hq]
    have h1 : x + cycleStep A (1 - x A) = roleStep N A := by
      funext q
      by_cases hq : q = A
      · subst hq
        simp [cycleStep, roleStep]
      · simp [cycleStep, roleStep, hq, haxis q hq]
    have hne : (-x A : ZMod (archiveFibers N)) ≠ 1 - x A := by
      intro h
      apply zmod_zero_ne_one (N := N)
      have h' := congrArg (fun z : ZMod (archiveFibers N) => z + x A) h
      simpa [add_comm, add_left_comm, add_assoc] using h'
    have hmem0 : -x A ∈ (Finset.univ : Finset (ZMod (archiveFibers N))) := Finset.mem_univ _
    have hmem1 : (1 - x A) ∈ (Finset.univ.erase (-x A)) := by
      exact Finset.mem_erase.mpr ⟨hne.symm, Finset.mem_univ _⟩
    have hfun : ∀ k : ZMod (archiveFibers N),
        curlEdge (x + cycleStep A k) A A =
          if k = -x A then 1 else if k = 1 - x A then -1 else 0 := by
      intro k
      by_cases hk0 : k = -x A
      · simp [curlEdge, hk0, h0]
      · by_cases hk1 : k = 1 - x A
        · have hstep0 : roleStep N A ≠ 0 := by
            intro hstep
            have := congrFun hstep A
            simp [roleStep] at this
            exact zmod_zero_ne_one (N := N) this.symm
          have hval : curlEdge (roleStep N A) A A = -1 := by
            simp only [curlEdge, hstep0, and_false, and_true, if_false, if_true]
          rw [hk1, h1, hval, if_neg hne.symm, if_pos rfl]
        · have hnot0 : x + cycleStep A k ≠ 0 := by
            intro h
            have := congrFun h A
            simp [cycleStep] at this
            apply hk0
            exact (neg_eq_of_add_eq_zero_left (by simpa [add_comm] using this)).symm
          have hnot1 : x + cycleStep A k ≠ roleStep N A := by
            intro h
            have := congrFun h A
            simp [cycleStep, roleStep] at this
            apply hk1
            have hadd : x A + k = 1 := this
            have : k + x A = 1 := by simpa [add_comm] using hadd
            exact eq_sub_of_add_eq this
          simp [curlEdge, hnot0, hnot1, hk0, hk1]
    simp only [cycleSum, hfun]
    rw [← Finset.add_sum_erase _ _ hmem0, ← Finset.add_sum_erase _ _ hmem1]
    have hrest : ∑ m ∈ ((Finset.univ : Finset (ZMod (archiveFibers N))).erase (-x A)).erase (1 - x A),
        (if m = -x A then (1 : ℝ) else if m = 1 - x A then -1 else 0) = 0 := by
      apply Finset.sum_eq_zero
      intro m hm
      have hm0 : m ≠ -x A := (Finset.mem_erase.mp (Finset.mem_of_mem_erase hm)).1
      have hm1 : m ≠ 1 - x A := (Finset.mem_erase.mp hm).1
      simp [hm0, hm1]
    have h10 : (1 : ZMod (archiveFibers N)) ≠ 0 := (zmod_zero_ne_one (N := N)).symm
    simp [if_neg h10, hrest]
  · simp only [cycleSum]
    apply Finset.sum_eq_zero
    intro k _
    have hnot0 : x + cycleStep A k ≠ 0 := by
      intro h
      have := congrFun h s
      simp [cycleStep, hs] at this
      exact hsx this
    have hnot1 : x + cycleStep A k ≠ roleStep N A := by
      intro h
      have := congrFun h s
      simp [cycleStep, roleStep, hs] at this
      exact hsx this
    simp [curlEdge, hnot0, hnot1]

theorem curlEdge_other_component_zero (b : Role) (hb : b ≠ A)
    (x : ArchiveRolePhaseGroup N) :
    cycleSum A (fun y => curlEdge y A b) x = 0 := by
  simp [cycleSum, curlEdge, hb]

theorem curlEdge_blocks_plaquette (hL : 3 ≤ archiveFibers N) :
    ∃ ψ : ArchiveRolePhaseGroup N → ℝ,
      commuteObstruction curlEdge A B ψ ≠ 0 ∧
        leibnizCycleObstruction curlEdge A ψ = 0 := by
  refine ⟨descentAxisProbe A 0, ?_, ?_⟩
  · intro hzero
    have hAt := congrFun hzero (0 : ArchiveRolePhaseGroup N)
    rw [commuteObstruction_expand] at hAt
    have hc : (1 / (archiveFibers N : ℝ)) ≠ 0 :=
      div_ne_zero one_ne_zero period_ne_zero
    rw [Pi.zero_apply] at hAt
    have hS := (mul_eq_zero.mp hAt).resolve_left hc
    rw [Finset.sum_eq_single A] at hS
    · have hskew := roleSkew_descentAxisProbe hL A (0 : ArchiveRolePhaseGroup N)
      simp only [Pi.zero_apply] at hskew
      rw [hskew] at hS
      have hB0 : roleStep N B ≠ (0 : ArchiveRolePhaseGroup N) := by
        intro h
        have := congrFun h B
        simp [roleStep] at this
        exact zmod_zero_ne_one (N := N) this.symm
      have hAB : A ≠ B := by decide
      have hBA : roleStep N B ≠ roleStep N A := by
        intro h
        have hA := congrFun h A
        simp [roleStep, hAB] at hA
        exact zmod_zero_ne_one (N := N) hA
      have hAB : B ≠ A := by decide
      have hinc : edgeIncrement B (fun y => curlEdge y A A) (0 : ArchiveRolePhaseGroup N) -
          edgeIncrement A (fun y => curlEdge y B A) (0 : ArchiveRolePhaseGroup N) = -1 := by
        simp [edgeIncrement, curlEdge, hB0, hBA, hAB]
      rw [hinc] at hS
      norm_num at hS
    · intro r _ hr
      have hzeroDir : ∀ (s : Role) (y : ArchiveRolePhaseGroup N), curlEdge y s r = 0 := by
        intro s y
        simp [curlEdge, hr]
      simp only [edgeIncrement]
      simp only [hzeroDir, sub_self, zero_mul]
    · intro hmiss
      exact absurd (Finset.mem_univ A) hmiss
  · apply zero_period_kills_cycle_obstruction
    intro r x
    by_cases hr : r = A
    · subst hr
      exact curlEdge_cycleSum_A x
    · simpa [curlEdge, hr] using curlEdge_other_component_zero r hr x

theorem harmonic_period_three :
    cycleSum (N := 1) A (fun y => harmonicEdge y A A) 0 = 3 := by
  rw [harmonicEdge_cycleSum]
  simp [archiveFibers]

theorem harmonic_period_five :
    cycleSum (N := 3) A (fun y => harmonicEdge y A A) 0 = 5 := by
  rw [harmonicEdge_cycleSum]
  simp [archiveFibers]

theorem curl_period_three :
    (∃ ψ, commuteObstruction (N := 1) curlEdge A B ψ ≠ 0) ∧
      (∀ x, cycleSum (N := 1) A (fun y => curlEdge y A A) x = 0) := by
  refine ⟨?_, fun x => curlEdge_cycleSum_A x⟩
  have hL : 3 ≤ archiveFibers 1 := by simp [archiveFibers]
  obtain ⟨ψ, hcom, _⟩ := curlEdge_blocks_plaquette (N := 1) hL
  exact ⟨ψ, hcom⟩

theorem curl_period_five :
    (∃ ψ, commuteObstruction (N := 3) curlEdge A B ψ ≠ 0) ∧
      (∀ x, cycleSum (N := 3) A (fun y => curlEdge y A A) x = 0) := by
  refine ⟨?_, fun x => curlEdge_cycleSum_A x⟩
  have hL : 3 ≤ archiveFibers 3 := by simp [archiveFibers]
  obtain ⟨ψ, hcom, _⟩ := curlEdge_blocks_plaquette (N := 3) hL
  exact ⟨ψ, hcom⟩

theorem period_two_formula_is_zero (e : LocalCoframeField 0) (t : Role)
    (ψ : ArchiveRolePhaseGroup 0 → ℝ) :
    scalarShiftResponse e t ψ = 0 :=
  scalarShiftResponse_period_two (by simp [archiveFibers]) e t ψ

/-- For `L ≥ 3`, preservation of the compressed shift relations forces the
cycle-sum and plaquette constraints, pure gauge satisfies them, and each
constraint has a hostile witness. `L = 2` makes this formula identically zero. -/
theorem scalarCrossedFirstJet_integrability_boundary :
    (∀ (v : Fin 5 → ℚ),
      (-(1 / (5 : ℚ))) •
          (scalarCycleMul (scalarDisplacement v) * scalarCycleD 5 * scalarCycleShift 5) =
        scalarCycleG v * scalarCycleShift 5 - scalarCycleShift 5 * scalarCycleG v) ∧
      (∀ (xi : LocalRoleVector 1) (s t : Role) (ψ : ArchiveRolePhaseGroup 1 → ℝ),
        leibnizCycleObstruction (forwardGaugeCoframe 1 xi) t ψ = 0 ∧
          commuteObstruction (forwardGaugeCoframe 1 xi) s t ψ = 0) ∧
      (∀ (xi : LocalRoleVector 3) (s t : Role) (ψ : ArchiveRolePhaseGroup 3 → ℝ),
        leibnizCycleObstruction (forwardGaugeCoframe 3 xi) t ψ = 0 ∧
          commuteObstruction (forwardGaugeCoframe 3 xi) s t ψ = 0) ∧
      cycleSum (N := 1) A (fun y => harmonicEdge y A A) 0 = 3 ∧
      cycleSum (N := 3) A (fun y => harmonicEdge y A A) 0 = 5 ∧
      (∃ ψ, commuteObstruction (N := 1) curlEdge A B ψ ≠ 0) ∧
      (∀ x, cycleSum (N := 1) A (fun y => curlEdge y A A) x = 0) ∧
      (∃ ψ, commuteObstruction (N := 3) curlEdge A B ψ ≠ 0) ∧
      (∀ x, cycleSum (N := 3) A (fun y => curlEdge y A A) x = 0) ∧
      (∀ (e : LocalCoframeField 0) (t : Role) (ψ : ArchiveRolePhaseGroup 0 → ℝ),
        scalarShiftResponse e t ψ = 0) := by
  refine ⟨fun v => scalarCandidate_eq_wordMixing v,
    fun xi s t ψ => pureGauge_preserves_relations xi s t ψ,
    fun xi s t ψ => pureGauge_preserves_relations xi s t ψ,
    harmonic_period_three, harmonic_period_five, ?_, ?_, ?_, ?_,
    fun e t ψ => period_two_formula_is_zero e t ψ⟩
  · exact curl_period_three.1
  · exact curl_period_three.2
  · exact curl_period_five.1
  · exact curl_period_five.2

end RolePhase

end D0.Geometry
