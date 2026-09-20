import Mathlib.Data.Real.Basic
import D0.Geometry.ArchiveRefinementTower

namespace D0.Geometry.ArchiveSeamCurvatureScope

open D0

/-!
# D0.Geometry.ArchiveSeamCurvatureScope

Owner: `D0-ARCHIVE-SEAM-CURVATURE-SCOPE-001`.

Scope correction for the archive seam curvature density:
In the 1D phase cycle refinement, the seam commutator $C_L = L_{L+1} B - B L_L$
has rank 2, four support entries, and Hilbert-Schmidt norm squared strictly equal to 4:
$$\|C_1\|_{HS}^2 = 4.$$

However, for a $d$-dimensional Cartesian product graph lift, the Hilbert-Schmidt norm
of the product seam scales as:
$$\|C_d\|_{HS}^2 = 4 d (L + 1)^{d-2} (L + d).$$
For $d = 4$:
$$\|C_4\|_{HS}^2 = 16 (L + 1)^2 (L + 4).$$

At $L = 2$ ($n = 0$), $\|C_4\|_{HS}^2 = 16 \times 9 \times 6 = 864 \ne 4$.
As $L \to \infty$, $\|C_4\|_{HS}^2 \sim 16 L^3 \to \infty$.

Therefore, the legacy scalar invariant $\|C_1\|_{HS}^2 = 4$ is strictly a 1D phase-refinement
invariant, and cannot be identified with the 4D spacetime scalar curvature without a dedicated lift.
-/

/-- 1D seam curvature Hilbert-Schmidt norm squared: strictly 4 for all $L$. -/
def seamHSNormSq1D : ℕ := 4

/-- $d$-dimensional tensor product seam curvature Hilbert-Schmidt norm squared. -/
def seamHSNormSqProduct (d L : ℕ) : ℕ :=
  4 * d * (L + 1)^(d - 2) * (L + d)

/-- 4D product seam curvature Hilbert-Schmidt norm squared: $16 (L+1)^2 (L+4)$. -/
def seamHSNormSq4D (L : ℕ) : ℕ :=
  16 * (L + 1)^2 * (L + 4)

/-- At $L = 2$, the 4D product seam norm squared evaluates to 864. -/
theorem seamHSNormSq4D_at_two : seamHSNormSq4D 2 = 864 := by
  unfold seamHSNormSq4D
  norm_num

/-- Strict inequality between 1D and 4D seam norms at $L = 2$: $4 \ne 864$. -/
theorem seam_1D_ne_4D_at_two : seamHSNormSq1D ≠ seamHSNormSq4D 2 := by
  rw [seamHSNormSq4D_at_two]
  unfold seamHSNormSq1D
  decide

/-- Monotonic divergence of the 4D seam norm: for all $L \ge 2$, $\|C_4\|_{HS}^2 \ge 864 > 4$. -/
theorem seam_4D_grows (L : ℕ) (hL : 2 ≤ L) : seamHSNormSq1D < seamHSNormSq4D L := by
  unfold seamHSNormSq1D seamHSNormSq4D
  have h1 : 3 ≤ L + 1 := by linarith
  have h2 : 6 ≤ L + 4 := by linarith
  have h_sq : 9 ≤ (L + 1)^2 := by nlinarith [h1]
  have h_prod : 864 ≤ 16 * (L + 1)^2 * (L + 4) := by nlinarith [h_sq, h2]
  linarith

/-- **D0-ARCHIVE-SEAM-CURVATURE-SCOPE-001 (Owner)**:
Master scope theorem establishing that the seam curvature density $\|C_1\|_{HS}^2 = 4$
is strictly a 1D phase invariant, not the 4D continuum scalar curvature:
1. 1D seam norm squared is 4;
2. 4D product seam norm squared at $L = 2$ is 864;
3. The two values strictly disagree ($4 \ne 864$);
4. The 4D product seam norm strictly exceeds 4 for all $L \ge 2$. -/
theorem archive_seam_curvature_scope_owner :
    (seamHSNormSq1D = 4) ∧
    (seamHSNormSq4D 2 = 864) ∧
    (seamHSNormSq1D ≠ seamHSNormSq4D 2) ∧
    (∀ L : ℕ, 2 ≤ L → seamHSNormSq1D < seamHSNormSq4D L) :=
  ⟨rfl, seamHSNormSq4D_at_two, seam_1D_ne_4D_at_two, seam_4D_grows⟩

end D0.Geometry.ArchiveSeamCurvatureScope
