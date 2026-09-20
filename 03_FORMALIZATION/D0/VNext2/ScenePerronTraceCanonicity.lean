import Mathlib.Data.Real.Basic
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic
import D0.Claims.Signature31Split

/-!
# D0.VNext2.ScenePerronTraceCanonicity

Theoretical owner: `D0-SCENE-PERRON-TRACE-CANONICITY-001`.

Canonicity of the positive Perron eigenvector profile and spectral radius on the
scene graph $K(9,11,13)$:
1. Define `PositiveScenePerronProfile` with positive entries $(x_9, x_{11}, x_{13}, \rho)$,
   the 3 zone eigen-equations, and standard normalization $9 x_9 + 11 x_{11} + 13 x_{13} = 1$.
2. Prove the closed form:
   $$( \rho + 9 ) x_9 = 1, \quad ( \rho + 11 ) x_{11} = 1, \quad ( \rho + 13 ) x_{13} = 1.$$
3. Prove that $\rho$ satisfies the exact scene transport cubic:
   $$\rho^3 - 359 \rho - 2574 = 0.$$
4. Prove that no positive root lies in $(0, 20]$ via exact algebraic factorization.
5. Prove strict monotonicity of the transport cubic on $[20, \infty)$ via difference identity.
6. Prove existence and uniqueness of the positive Perron root $\rho_{\mathrm{scene}} \in (20, 24)$
   and uniqueness of the normalized profile.
7. Prove `full_positive_eigenprofile_zone_constant`: any eigenvector of `Adj31` with non-zero
   eigenvalue is strictly constant on each zone fiber.
-/

namespace D0.VNext2.ScenePerronTraceCanonicity

open D0.Claims

/-- The transport cubic polynomial whose root is the scene Perron eigenvalue:
$P(x) = x^3 - 359 x - 2574$. -/
def sceneTransportCubic (x : ℝ) : ℝ :=
  x ^ 3 - 359 * x - 2574

/-- Positive Perron profile on the 3 zones of $K(9,11,13)$. -/
structure PositiveScenePerronProfile where
  x9 : ℝ
  x11 : ℝ
  x13 : ℝ
  rho : ℝ
  hx9_pos : 0 < x9
  hx11_pos : 0 < x11
  hx13_pos : 0 < x13
  hrho_pos : 0 < rho
  eq9 : 11 * x11 + 13 * x13 = rho * x9
  eq11 : 9 * x9 + 13 * x13 = rho * x11
  eq13 : 9 * x9 + 11 * x11 = rho * x13
  norm : 9 * x9 + 11 * x11 + 13 * x13 = 1

/-- Closed-form relation between the profile components and the eigenvalue:
$(\rho + 9) x_9 = 1$, $(\rho + 11) x_{11} = 1$, $(\rho + 13) x_{13} = 1$. -/
theorem scene_perron_closed_form (p : PositiveScenePerronProfile) :
    (p.rho + 9) * p.x9 = 1 ∧
    (p.rho + 11) * p.x11 = 1 ∧
    (p.rho + 13) * p.x13 = 1 := by
  have h9 : (p.rho + 9) * p.x9 = 1 := by
    calc (p.rho + 9) * p.x9 = p.rho * p.x9 + 9 * p.x9 := by ring
    _ = (11 * p.x11 + 13 * p.x13) + 9 * p.x9 := by rw [← p.eq9]
    _ = 9 * p.x9 + 11 * p.x11 + 13 * p.x13 := by ring
    _ = 1 := p.norm
  have h11 : (p.rho + 11) * p.x11 = 1 := by
    calc (p.rho + 11) * p.x11 = p.rho * p.x11 + 11 * p.x11 := by ring
    _ = (9 * p.x9 + 13 * p.x13) + 11 * p.x11 := by rw [← p.eq11]
    _ = 9 * p.x9 + 11 * p.x11 + 13 * p.x13 := by ring
    _ = 1 := p.norm
  have h13 : (p.rho + 13) * p.x13 = 1 := by
    calc (p.rho + 13) * p.x13 = p.rho * p.x13 + 13 * p.x13 := by ring
    _ = (9 * p.x9 + 11 * p.x11) + 13 * p.x13 := by rw [← p.eq13]
    _ = 9 * p.x9 + 11 * p.x11 + 13 * p.x13 := by ring
    _ = 1 := p.norm
  exact ⟨h9, h11, h13⟩

/-- The Perron eigenvalue $\rho$ strictly satisfies the transport cubic:
$\rho^3 - 359 \rho - 2574 = 0$. -/
theorem scene_perron_cubic (p : PositiveScenePerronProfile) :
    sceneTransportCubic p.rho = 0 := by
  obtain ⟨h9, h11, h13⟩ := scene_perron_closed_form p
  have hx9 : p.x9 = 1 / (p.rho + 9) := by
    have h_ne : p.rho + 9 ≠ 0 := by linarith [p.hrho_pos]
    exact eq_one_div_of_mul_eq_one_right h9
  have hx11 : p.x11 = 1 / (p.rho + 11) := by
    have h_ne : p.rho + 11 ≠ 0 := by linarith [p.hrho_pos]
    exact eq_one_div_of_mul_eq_one_right h11
  have hx13 : p.x13 = 1 / (p.rho + 13) := by
    have h_ne : p.rho + 13 ≠ 0 := by linarith [p.hrho_pos]
    exact eq_one_div_of_mul_eq_one_right h13
  have h_norm := p.norm
  rw [hx9, hx11, hx13] at h_norm
  have h_d9 : p.rho + 9 ≠ 0 := by linarith [p.hrho_pos]
  have h_d11 : p.rho + 11 ≠ 0 := by linarith [p.hrho_pos]
  have h_d13 : p.rho + 13 ≠ 0 := by linarith [p.hrho_pos]
  unfold sceneTransportCubic
  have h_poly : (p.rho ^ 3 - 359 * p.rho - 2574) =
      ((p.rho + 9) * (p.rho + 11) * (p.rho + 13)) *
      (1 - (9 * (1 / (p.rho + 9)) + 11 * (1 / (p.rho + 11)) + 13 * (1 / (p.rho + 13)))) := by
    field_simp
    ring
  rw [h_poly, h_norm, sub_self, mul_zero]

/-- Algebraic factorization of the cubic relative to $x = 20$:
$P(x) - P(20) = (x - 20)(x^2 + 20x + 41)$. -/
theorem scene_cubic_diff_twenty (x : ℝ) :
    sceneTransportCubic x - sceneTransportCubic 20 = (x - 20) * (x ^ 2 + 20 * x + 41) := by
  unfold sceneTransportCubic
  ring

/-- The transport cubic has no positive root $\le 20$: for all $x \in (0, 20]$, $P(x) < 0$. -/
theorem scene_cubic_no_positive_root_le_20 (x : ℝ) (hx_pos : 0 < x) (hx_le : x ≤ 20) :
    sceneTransportCubic x < 0 := by
  have h20 : sceneTransportCubic 20 = -1754 := by
    unfold sceneTransportCubic
    norm_num
  have h_factor := scene_cubic_diff_twenty x
  have h_quad : 0 < x ^ 2 + 20 * x + 41 := by
    have h1 : 0 ≤ x ^ 2 := sq_nonneg x
    have h2 : 0 < 20 * x := mul_pos (by norm_num) hx_pos
    linarith
  have h_diff_le : (x - 20) * (x ^ 2 + 20 * x + 41) ≤ 0 := by
    have h_sub : x - 20 ≤ 0 := by linarith
    exact mul_nonpos_of_nonpos_of_nonneg h_sub (le_of_lt h_quad)
  have h_val : sceneTransportCubic x = -1754 + (x - 20) * (x ^ 2 + 20 * x + 41) := by
    rw [← h20]
    linarith [h_factor]
  calc sceneTransportCubic x ≤ -1754 := by linarith [h_val, h_diff_le]
  _ < 0 := by norm_num

/-- Pure algebraic difference identity for the cubic:
$P(y) - P(x) = (y - x)(y^2 + xy + x^2 - 359)$. -/
theorem scene_cubic_diff_identity (x y : ℝ) :
    sceneTransportCubic y - sceneTransportCubic x =
      (y - x) * (y ^ 2 + x * y + x ^ 2 - 359) := by
  unfold sceneTransportCubic
  ring

/-- Strict monotonicity of the transport cubic on $[20, \infty)$ without calculus. -/
theorem scene_cubic_strictMono_ge_20 {x y : ℝ} (hx : 20 ≤ x) (hxy : x < y) :
    sceneTransportCubic x < sceneTransportCubic y := by
  have h_id := scene_cubic_diff_identity x y
  have h_sub_pos : 0 < y - x := sub_pos.mpr hxy
  have hy_ge : 20 < y := lt_of_le_of_lt hx hxy
  have hx2 : 400 ≤ x ^ 2 := by
    nlinarith
  have hy2 : 400 < y ^ 2 := by
    nlinarith
  have hxy_prod : 400 < x * y := by
    nlinarith
  have h_quad : 0 < y ^ 2 + x * y + x ^ 2 - 359 := by
    linarith
  have h_prod_pos : 0 < (y - x) * (y ^ 2 + x * y + x ^ 2 - 359) :=
    mul_pos h_sub_pos h_quad
  rw [← h_id] at h_prod_pos
  linarith

/-- Existence and uniqueness of the positive Perron eigenvalue $\rho_{\mathrm{scene}} > 0$. -/
theorem scene_positive_perron_root_exists_unique :
    ∃! rho : ℝ, 0 < rho ∧ sceneTransportCubic rho = 0 := by
  have hcont : Continuous sceneTransportCubic := by
    unfold sceneTransportCubic
    continuity
  have h20_neg : sceneTransportCubic 20 ≤ 0 := by
    unfold sceneTransportCubic; norm_num
  have h24_pos : 0 ≤ sceneTransportCubic 24 := by
    unfold sceneTransportCubic; norm_num
  have h_ivt := intermediate_value_Icc (by norm_num : (20 : ℝ) ≤ 24) hcont.continuousOn
      (by rw [Set.mem_Icc]; exact ⟨h20_neg, h24_pos⟩)
  obtain ⟨r, hr_icc, hr_root⟩ := h_ivt
  have hr_pos : 0 < r := by linarith [hr_icc.1]
  refine ⟨r, ⟨hr_pos, hr_root⟩, ?_⟩
  intro r' ⟨hr'_pos, hr'_root⟩
  rcases lt_trichotomy r' r with hlt | heq | hgt
  · by_cases hr'_le20 : r' ≤ 20
    · have h_neg := scene_cubic_no_positive_root_le_20 r' hr'_pos hr'_le20
      linarith [hr'_root]
    · have hr'_ge20 : 20 ≤ r' := le_of_not_ge hr'_le20
      have h_mono := scene_cubic_strictMono_ge_20 hr'_ge20 hlt
      linarith [hr'_root, hr_root]
  · exact heq
  · by_cases hr_le20 : r ≤ 20
    · have h_neg := scene_cubic_no_positive_root_le_20 r hr_pos hr_le20
      linarith [hr_root]
    · have hr_ge20 : 20 ≤ r := le_of_not_ge hr_le20
      have h_mono := scene_cubic_strictMono_ge_20 hr_ge20 hgt
      linarith [hr'_root, hr_root]

/-- Canonical scene Perron eigenvalue $\rho_{\mathrm{scene}}$. -/
noncomputable def sceneRho : ℝ :=
  Classical.choose scene_positive_perron_root_exists_unique.exists

theorem sceneRho_pos : 0 < sceneRho :=
  (Classical.choose_spec scene_positive_perron_root_exists_unique.exists).1

theorem sceneRho_cubic : sceneTransportCubic sceneRho = 0 :=
  (Classical.choose_spec scene_positive_perron_root_exists_unique.exists).2

/-- Any normalized positive Perron profile is uniquely determined by `sceneRho`. -/
theorem normalized_scene_perron_profile_unique (p : PositiveScenePerronProfile) :
    p.rho = sceneRho ∧
    p.x9 = 1 / (sceneRho + 9) ∧
    p.x11 = 1 / (sceneRho + 11) ∧
    p.x13 = 1 / (sceneRho + 13) := by
  have h_root := scene_perron_cubic p
  have h_uniq := scene_positive_perron_root_exists_unique.unique
      ⟨p.hrho_pos, h_root⟩ ⟨sceneRho_pos, sceneRho_cubic⟩
  obtain ⟨h9, h11, h13⟩ := scene_perron_closed_form p
  rw [h_uniq] at h9 h11 h13
  have hx9 : p.x9 = 1 / (sceneRho + 9) := eq_one_div_of_mul_eq_one_right h9
  have hx11 : p.x11 = 1 / (sceneRho + 11) := eq_one_div_of_mul_eq_one_right h11
  have hx13 : p.x13 = 1 / (sceneRho + 13) := eq_one_div_of_mul_eq_one_right h13
  exact ⟨h_uniq, hx9, hx11, hx13⟩

/-- Full-scene adjacency rows are identical within each zone. -/
theorem adj31_rows_zone_constant (i j : Fin 33) (h_zone : zone31 i = zone31 j) (k : Fin 33) :
    (Adj31 i k : ℝ) = (Adj31 j k : ℝ) := by
  have h_mat : Adj31 i k = Adj31 j k := by
    simp only [Adj31, Matrix.of_apply]
    rw [h_zone]
  rw [h_mat]

/-- **Full-scene positive eigenprofile zone constancy.**
Any eigenvector of `Adj31` with non-zero eigenvalue is strictly constant on each zone fiber. -/
theorem full_positive_eigenprofile_zone_constant
    (x : Fin 33 → ℝ) (rho : ℝ) (hrho : rho ≠ 0)
    (heig : ∀ i, (∑ j, (Adj31 i j : ℝ) * x j) = rho * x i) :
    ∀ i j, zone31 i = zone31 j → x i = x j := by
  intro i j h_zone
  have h_row_sum : (∑ k, (Adj31 i k : ℝ) * x k) = (∑ k, (Adj31 j k : ℝ) * x k) := by
    refine Finset.sum_congr rfl ?_
    intro k _
    rw [adj31_rows_zone_constant i j h_zone k]
  have hi := heig i
  have hj := heig j
  rw [h_row_sum] at hi
  have h_eq : rho * x i = rho * x j := by linarith [hi, hj]
  exact mul_left_cancel₀ hrho h_eq

/-- Canonical full-scene positive Perron profile on `Fin 33`. -/
noncomputable def fullScenePerronVector (i : Fin 33) : ℝ :=
  match zone31 i with
  | 0 => 1 / (sceneRho + 9)
  | 1 => 1 / (sceneRho + 11)
  | 2 => 1 / (sceneRho + 13)

/-- Full scene Perron vector entries are strictly positive. -/
theorem fullScenePerronVector_pos (i : Fin 33) : 0 < fullScenePerronVector i := by
  unfold fullScenePerronVector
  have hpos : 0 < sceneRho := sceneRho_pos
  split
  · exact one_div_pos.mpr (by linarith)
  · exact one_div_pos.mpr (by linarith)
  · exact one_div_pos.mpr (by linarith)

theorem sum_cind31_zone0 : (∑ i : Fin 33, Cind31 i 0) = 9 := by native_decide
theorem sum_cind31_zone1 : (∑ i : Fin 33, Cind31 i 1) = 11 := by native_decide
theorem sum_cind31_zone2 : (∑ i : Fin 33, Cind31 i 2) = 13 := by native_decide

/-- The zone-weighted Perron sum identity:
$9 / (\rho + 9) + 11 / (\rho + 11) + 13 / (\rho + 13) = 1$. -/
theorem sceneRho_profile_sum_eq_one :
    9 * (1 / (sceneRho + 9)) + 11 * (1 / (sceneRho + 11)) + 13 * (1 / (sceneRho + 13)) = 1 := by
  have hcub := sceneRho_cubic
  unfold sceneTransportCubic at hcub
  have h_d9 : sceneRho + 9 ≠ 0 := by linarith [sceneRho_pos]
  have h_d11 : sceneRho + 11 ≠ 0 := by linarith [sceneRho_pos]
  have h_d13 : sceneRho + 13 ≠ 0 := by linarith [sceneRho_pos]
  have h_prod_pos : 0 < (sceneRho + 9) * (sceneRho + 11) * (sceneRho + 13) := by
    have h1 : 0 < sceneRho + 9 := by linarith [sceneRho_pos]
    have h2 : 0 < sceneRho + 11 := by linarith [sceneRho_pos]
    have h3 : 0 < sceneRho + 13 := by linarith [sceneRho_pos]
    exact mul_pos (mul_pos h1 h2) h3
  have h_prod_ne : (sceneRho + 9) * (sceneRho + 11) * (sceneRho + 13) ≠ 0 := ne_of_gt h_prod_pos
  have h_poly : (sceneRho ^ 3 - 359 * sceneRho - 2574) =
      ((sceneRho + 9) * (sceneRho + 11) * (sceneRho + 13)) *
      (1 - (9 * (1 / (sceneRho + 9)) + 11 * (1 / (sceneRho + 11)) + 13 * (1 / (sceneRho + 13)))) := by
    field_simp
    ring
  rw [h_poly] at hcub
  have h_diff_zero : 1 - (9 * (1 / (sceneRho + 9)) + 11 * (1 / (sceneRho + 11)) + 13 * (1 / (sceneRho + 13))) = 0 := by
    cases mul_eq_zero.mp hcub with
    | inl h => exact False.elim (h_prod_ne h)
    | inr h => exact h
  linarith [h_diff_zero]

/-- Decomposition of fullScenePerronVector in terms of Cind31 indicators. -/
theorem fullScenePerronVector_eq_cind31 (i : Fin 33) :
    fullScenePerronVector i =
      (Cind31 i 0 : ℝ) * (1 / (sceneRho + 9)) +
      (Cind31 i 1 : ℝ) * (1 / (sceneRho + 11)) +
      (Cind31 i 2 : ℝ) * (1 / (sceneRho + 13)) := by
  have hz : zone31 i = 0 ∨ zone31 i = 1 ∨ zone31 i = 2 := by
    revert i
    decide
  rcases hz with h | h | h
  · have h0 : Cind31 i 0 = 1 := by simp [Cind31, h]
    have h1 : Cind31 i 1 = 0 := by
      have : zone31 i ≠ 1 := by rw [h]; decide
      simp [Cind31, this]
    have h2 : Cind31 i 2 = 0 := by
      have : zone31 i ≠ 2 := by rw [h]; decide
      simp [Cind31, this]
    unfold fullScenePerronVector
    rw [h, h0, h1, h2]
    push_cast
    ring
  · have h0 : Cind31 i 0 = 0 := by
      have : zone31 i ≠ 0 := by rw [h]; decide
      simp [Cind31, this]
    have h1 : Cind31 i 1 = 1 := by simp [Cind31, h]
    have h2 : Cind31 i 2 = 0 := by
      have : zone31 i ≠ 2 := by rw [h]; decide
      simp [Cind31, this]
    unfold fullScenePerronVector
    rw [h, h0, h1, h2]
    push_cast
    ring
  · have h0 : Cind31 i 0 = 0 := by
      have : zone31 i ≠ 0 := by rw [h]; decide
      simp [Cind31, this]
    have h1 : Cind31 i 1 = 0 := by
      have : zone31 i ≠ 1 := by rw [h]; decide
      simp [Cind31, this]
    have h2 : Cind31 i 2 = 1 := by simp [Cind31, h]
    unfold fullScenePerronVector
    rw [h, h0, h1, h2]
    push_cast
    ring

/-- Total mass of the canonical full scene Perron vector equals 1. -/
theorem fullScenePerronVector_sum_eq_one :
    (∑ i : Fin 33, fullScenePerronVector i) = 1 := by
  have h_sum_split : (∑ i : Fin 33, fullScenePerronVector i) =
      (∑ i : Fin 33, (Cind31 i 0 : ℝ)) * (1 / (sceneRho + 9)) +
      (∑ i : Fin 33, (Cind31 i 1 : ℝ)) * (1 / (sceneRho + 11)) +
      (∑ i : Fin 33, (Cind31 i 2 : ℝ)) * (1 / (sceneRho + 13)) := by
    simp_rw [fullScenePerronVector_eq_cind31]
    rw [Finset.sum_add_distrib, Finset.sum_add_distrib]
    rw [← Finset.sum_mul, ← Finset.sum_mul, ← Finset.sum_mul]
  have h0 : (∑ i : Fin 33, (Cind31 i 0 : ℝ)) = 9 := by
    have h := sum_cind31_zone0
    exact_mod_cast h
  have h1 : (∑ i : Fin 33, (Cind31 i 1 : ℝ)) = 11 := by
    have h := sum_cind31_zone1
    exact_mod_cast h
  have h2 : (∑ i : Fin 33, (Cind31 i 2 : ℝ)) = 13 := by
    have h := sum_cind31_zone2
    exact_mod_cast h
  rw [h_sum_split, h0, h1, h2]
  exact sceneRho_profile_sum_eq_one

/-- **D0-SCENE-PERRON-TRACE-CANONICITY-001 (CORE-FORMALIZED).**
The positive Perron profile on the tripartite scene graph $K(9,11,13)$ exists, is unique,
satisfies the exact transport cubic, and forces zone constancy on all 33 vertices. -/
theorem scene_perron_trace_canonicity_owner :
    (∃! rho : ℝ, 0 < rho ∧ sceneTransportCubic rho = 0) ∧
    (∀ p : PositiveScenePerronProfile, p.rho = sceneRho ∧
      p.x9 = 1 / (sceneRho + 9) ∧
      p.x11 = 1 / (sceneRho + 11) ∧
      p.x13 = 1 / (sceneRho + 13)) ∧
    (∀ (x : Fin 33 → ℝ) (rho : ℝ), rho ≠ 0 →
      (∀ i, (∑ j, (Adj31 i j : ℝ) * x j) = rho * x i) →
      ∀ i j, zone31 i = zone31 j → x i = x j) :=
  ⟨scene_positive_perron_root_exists_unique,
   normalized_scene_perron_profile_unique,
   full_positive_eigenprofile_zone_constant⟩

end D0.VNext2.ScenePerronTraceCanonicity
