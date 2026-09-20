import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic
import D0.Core.FiniteTypes

/-!
# D0-ARCHIVE-TENSOR-RG-METRIC-MEASURE-001 & D0-ARCHIVE-TENSOR-SEAM-CROSS-ROLE-CURVATURE-NOGO-001

## Tensor Seam Metric-Measure Structure and Separability / Cross-Role Curvature No-Go

In $d$-dimensional cubical refinement with the 1D mass matrix $M = \operatorname{diag}(2, 1, \dots, 1)$:
1. The 1D seam weight is $m(j) = \text{if } j = 0 \text{ then } 2 \text{ else } 1$.
2. The product mass measure is $\mu(x) = \prod_{s=1}^d m(x_s)$.
3. The directional conductance field is $c_r(x) = \prod_{s \ne r} m(x_s) = \frac{\mu(x)}{m(x_r)}$.
4. The principal inverse metric coefficient is $g^{rr}(x) = \frac{c_r(x)}{\mu(x)} = \frac{1}{m(x_r)}$.
5. Therefore the effective metric components are $g_{rr}(x) = m(x_r)$.

### Cross-Role Curvature No-Go:
For any $s \ne r$, the metric component $g_{rr}(x)$ depends only on the coordinate $x_r$, so:
$$\partial_s g_{rr} = 0 \quad (s \ne r).$$
In particular, all mixed finite differences vanish:
$$\Delta_s g_{rr} = 0, \qquad \Delta_s \Delta_r \log g_{rr} = 0 \quad (s \ne r).$$

Hence coordinatewise tensor refinement generates no cross-role metric coupling:
the metric is an intrinsically flat product of 1D metrics plus a scalar measure/dilaton density,
not genuine spacetime/Riemann curvature.
-/

namespace D0.Geometry.ArchiveTensorSeamCrossRoleNoGo

/-- 1D seam mass factor: 2 at the seam boundary $j = 0$, 1 in the bulk. -/
def m (j : ℕ) : ℝ :=
  if j = 0 then 2 else 1

theorem m_pos (j : ℕ) : 0 < m j := by
  unfold m
  split_ifs <;> norm_num

/-- Point in a 4D torus lattice $\mathbb{Z}_L^4$ represented as a coordinate vector. -/
abbrev Point4 := Fin 4 → ℕ

/-- Full product scalar mass density: $\mu(x) = \prod_{s=0}^3 m(x_s)$. -/
noncomputable def mu (x : Point4) : ℝ :=
  ∏ s : Fin 4, m (x s)

theorem mu_pos (x : Point4) : 0 < mu x := by
  unfold mu
  apply Finset.prod_pos
  intro s _
  exact m_pos (x s)

/-- Directional edge conductance field along role direction $r$:
$$c_r(x) = \prod_{s \ne r} m(x_s).$$ -/
noncomputable def conductance (r : Fin 4) (x : Point4) : ℝ :=
  ∏ s ∈ (Finset.univ.erase r), m (x s)

theorem conductance_pos (r : Fin 4) (x : Point4) : 0 < conductance r x := by
  unfold conductance
  apply Finset.prod_pos
  intro s _
  exact m_pos (x s)

/-- Conductance satisfies $c_r(x) = \frac{\mu(x)}{m(x_r)}$. -/
theorem conductance_eq_mu_div_m (r : Fin 4) (x : Point4) :
    conductance r x = mu x / m (x r) := by
  unfold mu conductance
  have h_split : (∏ s : Fin 4, m (x s)) = m (x r) * ∏ s ∈ (Finset.univ.erase r), m (x s) := by
    exact (Finset.mul_prod_erase Finset.univ (fun s => m (x s)) (Finset.mem_univ r)).symm
  rw [h_split]
  have hm_ne : m (x r) ≠ 0 := ne_of_gt (m_pos (x r))
  exact (mul_div_cancel_left₀ (∏ s ∈ Finset.univ.erase r, m (x s)) hm_ne).symm

/-- Effective metric tensor components: $g_{rr}(x) = \frac{\mu(x)}{c_r(x)} = m(x_r)$. -/
noncomputable def metricComponent (r : Fin 4) (x : Point4) : ℝ :=
  mu x / conductance r x

/-- **D0-ARCHIVE-TENSOR-RG-METRIC-MEASURE-001**:
The metric component $g_{rr}(x)$ is identically equal to the single-variable 1D seam factor $m(x_r)$. -/
theorem metric_component_eq_1d_seam (r : Fin 4) (x : Point4) :
    metricComponent r x = m (x r) := by
  unfold metricComponent
  rw [conductance_eq_mu_div_m]
  have hm_ne : m (x r) ≠ 0 := ne_of_gt (m_pos (x r))
  have hmu_ne : mu x ≠ 0 := ne_of_gt (mu_pos x)
  field_simp [hm_ne, hmu_ne]

/-- Partial finite variation along coordinate $s$: shifting the $s$-th coordinate. -/
def shiftCoordinate (s : Fin 4) (step : ℕ) (x : Point4) : Point4 :=
  fun i => if i = s then x s + step else x i

/-- **D0-ARCHIVE-TENSOR-SEAM-CROSS-ROLE-CURVATURE-NOGO-001**:
Cross-role variation of the metric component $g_{rr}$ under shifts of $s \ne r$ vanishes identically.
Coordinatewise tensor refinement produces zero cross-role metric coupling. -/
theorem cross_role_variation_vanishes (r s : Fin 4) (hrs : s ≠ r) (step : ℕ) (x : Point4) :
    metricComponent r (shiftCoordinate s step x) = metricComponent r x := by
  rw [metric_component_eq_1d_seam, metric_component_eq_1d_seam]
  unfold shiftCoordinate
  simp [hrs.symm]

/-- Mixed finite difference $\Delta_s g_{rr} = 0$ for $s \ne r$. -/
theorem mixed_finite_difference_zero (r s : Fin 4) (hrs : s ≠ r) (step : ℕ) (x : Point4) :
    metricComponent r (shiftCoordinate s step x) - metricComponent r x = 0 := by
  rw [cross_role_variation_vanishes r s hrs step x, sub_self]

/-- Master No-Go: The tensor seam geometry is separable and intrinsically flat. -/
theorem tensor_seam_cross_role_nogo :
    (∀ r : Fin 4, ∀ x : Point4, metricComponent r x = m (x r)) ∧
    (∀ r s : Fin 4, s ≠ r → ∀ (step : ℕ) (x : Point4),
      metricComponent r (shiftCoordinate s step x) - metricComponent r x = 0) :=
  ⟨metric_component_eq_1d_seam, fun r s hrs step x => mixed_finite_difference_zero r s hrs step x⟩

end D0.Geometry.ArchiveTensorSeamCrossRoleNoGo
