import Mathlib.Tactic

/-!
# D0-SM-HYPERCHARGE-ROW-OWNER-001 — the hypercharge row is the unique anomaly-free 5-field assignment

The one-generation **five-field** Weyl content `(Q_L, u_R^c, d_R^c, L_L, e_R^c)` (no right-neutral
`ν_R`), with colour×doublet multiplicities `(6,3,3,2,1)`, is constrained by the four gauge anomaly
conditions: `SU(3)²–Y`, `SU(2)²–Y`, gravitational–`Y` (all linear), and `U(1)_Y³` (cubic). The three
LINEAR conditions cut the charge space to the 2-parameter family

  `Y_Q = a,  Y_u = −a+t,  Y_d = −a−t,  Y_L = −3a,  Y_e = 6a`,

and the cubic condition factors **exactly** as `Σ mult·Y³ = −18·a·(t−3a)·(t+3a)`. So the anomaly-free
rays are precisely `{a=0} ∪ {t = 3a} ∪ {t = −3a}`. Excluding the degenerate `a=0` branch (which leaves
the quark doublet uncharged, `Y_Q=0`) and fixing the `u↔d` labeling to the `t = −3a` branch, the
electron-readout normalization `Y_e = 1` (so `a = 1/6`) gives the **unique** row

  `(1/6, −2/3, 1/3, −1/2, 1)`.

HONEST BOUNDS. Uniqueness is up to (i) overall normalization (electron readout), (ii) the `u↔d`
labeling convention (`t → −t`), and (iii) exclusion of the degenerate `Y_Q=0` branch. The row is the
OUTPUT of the anomaly solve, never an imported Standard-Model table. The 2-dimensional anomaly-free
space found when a right-neutral `ν_R` is ADDED is the `B−L` direction (`D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`);
this owner is the 5-field statement where that freedom is absent. No measured charge, PDG datum, or
246 GeV enters — only `ℚ`/`ring` algebra.
-/

namespace D0.Matter.SMHyperchargeRowOwner

/-- Colour×doublet multiplicities of the 5-field content `(Q_L, u_R^c, d_R^c, L_L, e_R^c)`. -/
def multQ : ℚ := 6
def multU : ℚ := 3
def multD : ℚ := 3
def multL : ℚ := 2
def multE : ℚ := 1

/-- The 2-parameter LINEAR-anomaly-free family (`a,t`): the general solution of the three linear
conditions `SU(3)²` `2Y_Q+Y_u+Y_d=0`, `SU(2)²` `3Y_Q+Y_L=0`, grav `Σ mult·Y=0`. -/
def YQ (a t : ℚ) : ℚ := a
def YU (a t : ℚ) : ℚ := -a + t
def YD (a t : ℚ) : ℚ := -a - t
def YL (a t : ℚ) : ℚ := -3 * a
def YE (a t : ℚ) : ℚ := 6 * a

/-- **The three linear anomaly conditions vanish identically** on the `(a,t)` family (it IS their
solution space). -/
theorem linear_anomalies_vanish (a t : ℚ) :
    (2 * YQ a t + YU a t + YD a t = 0)
      ∧ (3 * YQ a t + YL a t = 0)
      ∧ (multQ * YQ a t + multU * YU a t + multD * YD a t + multL * YL a t + multE * YE a t = 0) := by
  refine ⟨?_, ?_, ?_⟩ <;> simp only [YQ, YU, YD, YL, YE, multQ, multU, multD, multL, multE] <;> ring

/-- The cubic `U(1)_Y³` anomaly `Σ mult·Y³` on the `(a,t)` family. -/
def cubicAnomaly (a t : ℚ) : ℚ :=
  multQ * (YQ a t)^3 + multU * (YU a t)^3 + multD * (YD a t)^3 + multL * (YL a t)^3 + multE * (YE a t)^3

/-- **The cubic anomaly factors exactly**: `Σ mult·Y³ = −18·a·(t−3a)·(t+3a)` — a `ring` identity. -/
theorem cubic_anomaly_factored (a t : ℚ) :
    cubicAnomaly a t = -18 * a * (t - 3 * a) * (t + 3 * a) := by
  simp only [cubicAnomaly, YQ, YU, YD, YL, YE, multQ, multU, multD, multL, multE]; ring

/-- **Classification of anomaly-free rays**: the cubic vanishes on the linear family iff
`a = 0` (degenerate, `Y_Q=0`), or `t = 3a` (u↔d swap), or `t = −3a` (the SM branch). -/
theorem anomaly_free_rays (a t : ℚ) :
    cubicAnomaly a t = 0 ↔ a = 0 ∨ t = 3 * a ∨ t = -3 * a := by
  rw [cubic_anomaly_factored]
  constructor
  · intro h
    rcases mul_eq_zero.1 h with h1 | h2
    · rcases mul_eq_zero.1 h1 with h3 | h4
      · left; rcases mul_eq_zero.1 h3 with h5 | h6
        · exact absurd h5 (by norm_num)
        · exact h6
      · right; left; linarith [sub_eq_zero.1 h4]
    · right; right; linarith [add_eq_zero_iff_eq_neg.1 h2]
  · rintro (h | h | h) <;> subst h <;> ring

/-- The Standard-Model hypercharge branch: `t = −3a` with electron normalization `Y_e = 1` (so `a = 1/6`). -/
theorem sm_row_unique_on_branch :
    YQ (1/6) (-(1/2)) = 1/6
      ∧ YU (1/6) (-(1/2)) = -2/3
      ∧ YD (1/6) (-(1/2)) = 1/3
      ∧ YL (1/6) (-(1/2)) = -1/2
      ∧ YE (1/6) (-(1/2)) = 1
      ∧ (-(1/2) : ℚ) = -3 * (1/6)
      ∧ cubicAnomaly (1/6) (-(1/2)) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    norm_num [YQ, YU, YD, YL, YE, cubicAnomaly, multQ, multU, multD, multL, multE]

/-- **D0-SM-HYPERCHARGE-ROW-OWNER-001.** The hypercharge row is the unique anomaly-free assignment of
the 5-field content, up to normalization (electron `Y_e=1`), the `u↔d` labeling (`t=−3a` vs `t=3a`), and
exclusion of the degenerate `a=0` branch: the cubic factors as `−18a(t−3a)(t+3a)`, and the
electron-normalized non-degenerate SM branch is `(1/6,−2/3,1/3,−1/2,1)`. The row is derived, not imported. -/
theorem sm_hypercharge_row_owner :
    (∀ a t : ℚ, cubicAnomaly a t = -18 * a * (t - 3 * a) * (t + 3 * a))
      ∧ (∀ a t : ℚ, cubicAnomaly a t = 0 ↔ a = 0 ∨ t = 3 * a ∨ t = -3 * a)
      ∧ (YQ (1/6) (-(1/2)), YU (1/6) (-(1/2)), YD (1/6) (-(1/2)), YL (1/6) (-(1/2)), YE (1/6) (-(1/2)))
          = (1/6, -2/3, 1/3, -1/2, 1) := by
  refine ⟨cubic_anomaly_factored, anomaly_free_rays, ?_⟩
  simp only [YQ, YU, YD, YL, YE, Prod.mk.injEq]; refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> norm_num

end D0.Matter.SMHyperchargeRowOwner
