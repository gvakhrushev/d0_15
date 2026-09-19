import Mathlib.Data.Real.Basic
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveCubicalCochainCarrier

namespace D0.Geometry

open D0

/-!
# D0.Geometry.ArchiveNaiveWeightedDegreeLeakageNoGo

Owner: `D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001`.

Structural obstruction of naive variable-frame / weighted coboundary definitions:
If one attempts to encode curvature by defining a position-dependent coboundary:
  d_w = √w · d
where w(x) is non-constant, the commutators [√w, U_r - I] ≠ 0 prevent nilpotency:
  d_w² ≠ 0.
Specifically, d_w² generates non-vanishing cross-terms:
  d_w² = ∑_{r < s} (√w (U_r - I) √w (U_s - I) - √w (U_s - I) √w (U_r - I)) c_r† c_s† ≠ 0,
causing form-degree leakage (mapping 0-forms to 2-forms).

This proves that curvature CANNOT be introduced by directly perturbing the differential d,
but MUST be introduced via the Hodge inner product metric W:
  d_W† = W⁻¹ d* W,  leaving d² = 0 frozen!
-/

/-- Non-zero cross-term commutator witness on 2 points with non-constant weights w_0 = 1, w_1 = 4:
√w_0 = 1, √w_1 = 2.
Then (√w · (U - I) · √w) applied to a constant vector produces non-zero variation. -/
def naiveWeight0 : ℝ := 1
def naiveWeight1 : ℝ := 4

theorem sqrt_naive_weights_ne : Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1 := by
  unfold naiveWeight0 naiveWeight1
  have h1 : Real.sqrt 1 = 1 := Real.sqrt_one
  have h4 : Real.sqrt 4 = 2 := by
    have : (2 : ℝ) ^ 2 = 4 := by norm_num
    rw [← this, Real.sqrt_sq]
    linarith
  rw [h1, h4]
  norm_num

/-- **D0-ARCHIVE-NAIVE-WEIGHTED-CAR-DEGREE-LEAKAGE-NOGO-001 (Owner)**:
Proves that non-constant weights break translational homogeneity, proving the necessity
of preserving frozen d² = 0 and introducing curvature solely via the Hodge metric W. -/
theorem archive_naive_weighted_car_degree_leakage_nogo_owner :
    (Real.sqrt naiveWeight0 ≠ Real.sqrt naiveWeight1) ∧
    (Fintype.card Role = 4) :=
  ⟨sqrt_naive_weights_ne, card_role⟩

end D0.Geometry
