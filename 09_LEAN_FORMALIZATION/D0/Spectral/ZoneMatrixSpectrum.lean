import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic
import D0.Core.Phi
import D0.Dynamics.PisotContraction
import D0.Geometry.SceneActiveEigenvalues

/-!
# D0-LAPLACIAN-SPECTRUM-FIX-001 — exact spectrum of the 3×3 row-stochastic zone matrix

BOOK_02 §02.18.4 (reforge of researcher doc 2 §02.21 ERROR). Python certificate:
`05_CERTS/vp_laplacian_3x3_correct.py`.

The error: "char.poly of zone matrix `M` → `φ⁻¹`". This is wrong because `M` is **row-stochastic**
(every row sums to 1), so its Perron eigenvalue is exactly `1` and `φ⁻¹ ≈ 0.618` is not even in its
spectrum. The fix REFORGES (does not discard) the error into a clean separation of THREE conflated
numbers:

* `spec(M) = {1, −1/2 ± √10/40} ≈ {1, −0.421, −0.579}` — all `|λ| ≤ 1` (this module);
* the S_DE relaxation window `{≈1.42, ≈1.58}` = `eig(I − M) = 1 − eig(M)`, i.e. the `λ ↦ 1−λ`
  image of the scene active eigenvalues `3/2 ± √10/40` of `D0.scene_active_eigenvalue_±` (Book 08);
* the envelope fractal tick `φ⁻¹ = (√5−1)/2` (Book 06 §06.2), a DIFFERENT operator, proved here NOT
  to be an eigenvalue of `M` (the cert's `FAIL_PHI_INV` negative control).

The matrix `M = [[0, 11/24, 13/24], [9/22, 0, 13/22], [9/20, 11/20, 0]]` has zero diagonal and the
zone labels `9,11,13` as off-diagonal numerators (row denominators `24=11+13, 22=9+13, 20=9+11`). Its
elementary symmetric functions `e₁ = tr = 0`, `e₂ = Σ minors₂ = −121/160`, `e₃ = det = 39/160` give
the monic charpoly `λ³ − (121/160)λ − 39/160`, which factors EXACTLY as `(λ−1)(λ²+λ+39/160)`.

**Scope (honest).** The arithmetic core (stochasticity, the symmetric functions, the factorization,
the two active roots, the `λ↦1−λ` transport, and `φ⁻¹ ∉ spec(M)`) is machine-checked here. The
*physical identifications* (this window IS the S_DE relaxation spectrum; `φ⁻¹` IS the Book-06 envelope
tick) are modeling assignments and stay in the cert.
-/

namespace D0.Spectral

open scoped BigOperators

/-- The row-stochastic 3×3 zone/transport matrix `M` over `ℚ`. -/
def zoneTransport : Matrix (Fin 3) (Fin 3) ℚ :=
  !![0, 11 / 24, 13 / 24;
     9 / 22, 0, 13 / 22;
     9 / 20, 11 / 20, 0]

/-- Sum of the three principal `2×2` minors `e₂` of `M`. -/
def sumPrincipalMinors2 : ℚ :=
  (zoneTransport 0 0 * zoneTransport 1 1 - zoneTransport 0 1 * zoneTransport 1 0)
    + (zoneTransport 0 0 * zoneTransport 2 2 - zoneTransport 0 2 * zoneTransport 2 0)
    + (zoneTransport 1 1 * zoneTransport 2 2 - zoneTransport 1 2 * zoneTransport 2 1)

/-- **Row-stochastic.** Every row of `M` sums to `1`, so the Perron eigenvalue is exactly `1`
(this is the qualitative heart of the fix: `ρ(M)=1`, not `φ⁻¹`). -/
theorem zoneTransport_row_stochastic : ∀ i, ∑ j, zoneTransport i j = 1 := by native_decide

/-- `e₁ = tr M = 0` (zero diagonal). -/
theorem zoneTransport_trace : zoneTransport.trace = 0 := by native_decide

/-- `e₂ = Σ minors₂ = −121/160`. -/
theorem zoneTransport_minors2 : sumPrincipalMinors2 = -121 / 160 := by native_decide

/-- `e₃ = det M = 39/160` (the cert's `1287/5280 = 39/160`). -/
theorem zoneTransport_det : zoneTransport.det = 39 / 160 := by native_decide

/-- **Charpoly factorization.** The monic charpoly `λ³ − e₁λ² + e₂λ − e₃ = λ³ − (121/160)λ − 39/160`
(with `e₁=0`, `e₂=−121/160`, `e₃=39/160` grounded above) factors exactly as `(λ−1)(λ²+λ+39/160)`. -/
theorem charpoly_factor (lam : ℚ) :
    (lam - 1) * (lam ^ 2 + lam + 39 / 160) = lam ^ 3 - (121 / 160) * lam - 39 / 160 := by ring

/-- `λ = 1` is a root of the charpoly (the row-stochastic Perron eigenvalue). -/
theorem eigenvalue_one : (1 : ℚ) ^ 3 - (121 / 160) * 1 - 39 / 160 = 0 := by norm_num

/-- **Active eigenvalue `−1/2 + √10/40`** is a root of the quadratic factor `λ²+λ+39/160`. -/
theorem active_eigenvalue_plus :
    (-1 / 2 + Real.sqrt 10 / 40) ^ 2 + (-1 / 2 + Real.sqrt 10 / 40) + 39 / 160 = 0 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (1 / 1600 : ℝ) * h

/-- **Active eigenvalue `−1/2 − √10/40`** is a root of the quadratic factor `λ²+λ+39/160`. -/
theorem active_eigenvalue_minus :
    (-1 / 2 - Real.sqrt 10 / 40) ^ 2 + (-1 / 2 - Real.sqrt 10 / 40) + 39 / 160 = 0 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (1 / 1600 : ℝ) * h

/-- **`λ ↦ 1−λ` transport identity** (Book 02 ↔ Book 08): the active quadratic `λ²+λ+39/160`
is the monic image of the scene S_DE quadratic `160μ²−480μ+359` under `λ = 1−μ`. -/
theorem active_transport (mu : ℝ) :
    (1 - mu) ^ 2 + (1 - mu) + 39 / 160 = (160 * mu ^ 2 - 480 * mu + 359) / 160 := by ring

/-- The eigenvalue `1 − (3/2 + √10/40) = −1/2 − √10/40` of `M`, obtained by transporting the scene
active eigenvalue `3/2 + √10/40` (a root of `160μ²−480μ+359`) via `λ↦1−λ`. -/
theorem active_from_scene_plus :
    (1 - (3 / 2 + Real.sqrt 10 / 40)) ^ 2 + (1 - (3 / 2 + Real.sqrt 10 / 40)) + 39 / 160 = 0 := by
  rw [active_transport, scene_active_eigenvalue_plus]; norm_num

/-- The eigenvalue `1 − (3/2 − √10/40) = −1/2 + √10/40` of `M`, transported from the scene active
eigenvalue `3/2 − √10/40` via `λ↦1−λ`. -/
theorem active_from_scene_minus :
    (1 - (3 / 2 - Real.sqrt 10 / 40)) ^ 2 + (1 - (3 / 2 - Real.sqrt 10 / 40)) + 39 / 160 = 0 := by
  rw [active_transport, scene_active_eigenvalue_minus]; norm_num

/-- `φ⁻¹ = (√5−1)/2` satisfies `x² + x − 1 = 0`. -/
theorem primitiveRoot_quadratic : primitiveRoot ^ 2 + primitiveRoot - 1 = 0 := by
  unfold primitiveRoot
  linear_combination (1 / 4 : ℝ) * sqrt_five_sq

/-- Hence `(φ⁻¹)³ = 2·φ⁻¹ − 1`. -/
theorem primitiveRoot_cubed : primitiveRoot ^ 3 = 2 * primitiveRoot - 1 := by
  linear_combination (primitiveRoot - 1) * primitiveRoot_quadratic

/-- **Charpoly value at `φ⁻¹`.** `p(φ⁻¹) = (199/160)(φ⁻¹ − 1)`. -/
theorem phi_inv_charpoly_value :
    primitiveRoot ^ 3 - (121 / 160) * primitiveRoot - 39 / 160
      = (199 / 160) * (primitiveRoot - 1) := by
  rw [primitiveRoot_cubed]; ring

/-- `φ⁻¹ < 1` (since `√5 < 3`). -/
theorem primitiveRoot_lt_one : primitiveRoot < 1 := by
  unfold primitiveRoot
  have h := sqrt_five_lt_three
  linarith

/-- **Negative control (the error correction).** `φ⁻¹` is NOT an eigenvalue of `M`: the charpoly
does not vanish there, `p(φ⁻¹) = (199/160)(φ⁻¹−1) ≠ 0`. -/
theorem phi_inv_not_eigenvalue :
    primitiveRoot ^ 3 - (121 / 160) * primitiveRoot - 39 / 160 ≠ 0 := by
  rw [phi_inv_charpoly_value]
  have hne : primitiveRoot - 1 ≠ 0 := by
    have := primitiveRoot_lt_one; intro hc; linarith
  exact mul_ne_zero (by norm_num) hne

/-- **D0-LAPLACIAN-SPECTRUM-FIX-001.** The 3×3 zone matrix `M` is row-stochastic; its elementary
symmetric functions are `e₁=0`, `e₂=−121/160`, `e₃=39/160`; its charpoly `λ³−(121/160)λ−39/160`
factors as `(λ−1)(λ²+λ+39/160)`; and `φ⁻¹` is NOT a root (the original error, corrected). -/
theorem laplacian_3x3_correct :
    (∀ i, ∑ j, zoneTransport i j = 1) ∧
    zoneTransport.trace = 0 ∧
    sumPrincipalMinors2 = -121 / 160 ∧
    zoneTransport.det = 39 / 160 ∧
    (∀ lam : ℚ, (lam - 1) * (lam ^ 2 + lam + 39 / 160)
       = lam ^ 3 - (121 / 160) * lam - 39 / 160) ∧
    primitiveRoot ^ 3 - (121 / 160) * primitiveRoot - 39 / 160 ≠ 0 :=
  ⟨zoneTransport_row_stochastic, zoneTransport_trace, zoneTransport_minors2,
   zoneTransport_det, charpoly_factor, phi_inv_not_eigenvalue⟩

end D0.Spectral
