import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Algebra.FibonacciAFTower
import D0.Core.Phi

set_option linter.unusedSimpArgs false
set_option linter.unusedVariables false

/-!
# D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001 — finite-real pairing scope (Phase A2)

This module retains the scalar golden identities and a generic conditional algebraic pairing identity.
Its first-step example constructs a real algebra map and checks the associated functional pairing;
its diagonal block and trace calculations are specializations of the shared all-level block API in
`D0.Algebra.FibonacciAFTower`.
The generic lemma assumes multiplication, star, map, and trace-preservation facts as inputs. It does
not construct a positive state, a complex AF C*-inductive limit, a GNS quotient/completion, or a
Hilbert-space isometry. The broader canonical Perron-GNS tower claim remains open under this owner.
-/
namespace D0.VNext.PerronGNSTower

open Matrix D0

/-- **Conditional algebraic pairing identity** for a supplied trace-preserving star map. This is not
a construction of GNS spaces or an isometry of Hilbert completions. -/
theorem gns_refinement_isometry {A B : Type*} [Mul A] [Mul B] [Star A] [Star B]
    (tauA : A → ℝ) (tauB : B → ℝ) (iota : A → B)
    (hmul : ∀ x y : A, iota (x * y) = iota x * iota y)
    (hstar : ∀ x : A, iota (star x) = star (iota x))
    (htr : ∀ a : A, tauB (iota a) = tauA a) :
    ∀ x y : A, tauB (star (iota y) * iota x) = tauA (star y * x) :=
  D0.Algebra.FibonacciAFTower.gns_refinement_isometry tauA tauB iota hmul hstar htr

theorem phi_ne_zero : phi ≠ 0 := D0.Algebra.FibonacciAFTower.phi_ne_zero

/-- **The Perron eigenvalue relation** `M_φ v = φ v` for `v = (φ,1)`, i.e. its content `φ·φ = φ + 1`. -/
theorem perron_eigenvalue_relation : phi * phi = phi + 1 := by
  rw [← pow_two]; exact phi_sq

/-- **The Perron trace is refinement-compatible**: the trace vectors `t_N = (φ,1)`, `t_{N+1} = φ⁻¹(φ,1)`
satisfy `M_φ t_{N+1} = t_N`, which reduces to the scalar identities `1 + φ⁻¹ = φ` (top component) and
`φ⁻¹·φ = 1` (bottom component). Hence `τ_{N+1} ∘ ι_N = τ_N`. -/
theorem perron_trace_compatible_with_refinement :
    1 + phi⁻¹ = phi ∧ phi⁻¹ * phi = 1 :=
  D0.Algebra.FibonacciAFTower.perron_trace_consistency

/-- The diagonal 2-by-2 block in the first Fibonacci refinement step. -/
def firstRefinementDiagonal (x y : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![x, 0; 0, y]

private def firstRefinementScalarMatrix (x : ℝ) : Matrix (Fin 1) (Fin 1) ℝ :=
  fun _ _ => x

private theorem firstRefinementScalarMatrix_mul (x y : ℝ) :
    firstRefinementScalarMatrix x * firstRefinementScalarMatrix y =
      firstRefinementScalarMatrix (x * y) := by
  ext i j
  fin_cases i
  fin_cases j
  simp [firstRefinementScalarMatrix, Matrix.mul_apply]

private theorem firstRefinementScalarMatrix_star (x : ℝ) :
    star (firstRefinementScalarMatrix x) = firstRefinementScalarMatrix x := by
  ext i j
  fin_cases i
  fin_cases j
  simp [firstRefinementScalarMatrix]

private theorem firstRefinementDiagonal_eq_sharedBlock (x y : ℝ) :
    firstRefinementDiagonal x y =
      D0.Algebra.FibonacciAFTower.fibonacciBlockMatrix
        (firstRefinementScalarMatrix x) (firstRefinementScalarMatrix y) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [firstRefinementDiagonal, firstRefinementScalarMatrix,
      D0.Algebra.FibonacciAFTower.fibonacciBlockMatrix,
      Matrix.reindexAlgEquiv_apply, finSumFinEquiv, Fin.addCases]

/-- The first finite Bratteli step, from two scalar blocks to `M₂(ℝ) × ℝ`:
`(x,y) ↦ (diag(x,y),x)`, with multiplicities given by `Mφ = !![1,1;1,0]`. -/
def firstRefinementMap (z : ℝ × ℝ) : Matrix (Fin 2) (Fin 2) ℝ × ℝ :=
  (firstRefinementDiagonal z.1 z.2, z.1)

/-- The level-zero Perron trace functional for the finite step. -/
noncomputable def firstRefinementTrace0 (z : ℝ × ℝ) : ℝ := phi * z.1 + z.2

/-- The level-one Perron trace functional, scaled by `φ⁻¹` for refinement compatibility. -/
noncomputable def firstRefinementTrace1 (z : Matrix (Fin 2) (Fin 2) ℝ × ℝ) : ℝ :=
  phi⁻¹ * (phi * Matrix.trace z.1 + z.2)

theorem firstRefinementDiagonal_mul (x y u v : ℝ) :
    firstRefinementDiagonal x y * firstRefinementDiagonal u v =
      firstRefinementDiagonal (x * u) (y * v) := by
  rw [firstRefinementDiagonal_eq_sharedBlock x y,
    firstRefinementDiagonal_eq_sharedBlock u v,
    firstRefinementDiagonal_eq_sharedBlock (x * u) (y * v),
    D0.Algebra.FibonacciAFTower.fibonacciBlockMatrix_mul,
    firstRefinementScalarMatrix_mul, firstRefinementScalarMatrix_mul]

theorem firstRefinementDiagonal_star (x y : ℝ) :
    star (firstRefinementDiagonal x y) = firstRefinementDiagonal x y := by
  rw [firstRefinementDiagonal_eq_sharedBlock x y,
    D0.Algebra.FibonacciAFTower.fibonacciBlockMatrix_star,
    firstRefinementScalarMatrix_star, firstRefinementScalarMatrix_star,
    ← firstRefinementDiagonal_eq_sharedBlock x y]

theorem firstRefinementDiagonal_trace (x y : ℝ) :
    Matrix.trace (firstRefinementDiagonal x y) = x + y := by
  rw [firstRefinementDiagonal_eq_sharedBlock,
    D0.Algebra.FibonacciAFTower.trace_fibonacciBlockMatrix]
  simp [firstRefinementScalarMatrix, Matrix.trace]

theorem firstRefinementMap_mul (z w : ℝ × ℝ) :
    firstRefinementMap (z * w) = firstRefinementMap z * firstRefinementMap w := by
  rcases z with ⟨x, y⟩
  rcases w with ⟨u, v⟩
  apply Prod.ext
  · exact (firstRefinementDiagonal_mul x y u v).symm
  · rfl

theorem firstRefinementMap_star (z : ℝ × ℝ) :
    firstRefinementMap (star z) = star (firstRefinementMap z) := by
  rcases z with ⟨x, y⟩
  have hsource : star (x, y) = (x, y) := by ext <;> simp
  have htarget : star (firstRefinementMap (x, y)) = firstRefinementMap (x, y) := by
    apply Prod.ext
    · exact firstRefinementDiagonal_star x y
    · simp
  rw [hsource, htarget]

/-- The concrete first refinement is a unital ring homomorphism. -/
def firstRefinementRingHom : (ℝ × ℝ) →+* (Matrix (Fin 2) (Fin 2) ℝ × ℝ) where
  toFun := firstRefinementMap
  map_one' := by
    apply Prod.ext
    · ext i j
      fin_cases i <;> fin_cases j <;> simp [firstRefinementMap, firstRefinementDiagonal]
    · rfl
  map_mul' := firstRefinementMap_mul
  map_zero' := by
    apply Prod.ext
    · ext i j
      fin_cases i <;> fin_cases j <;> simp [firstRefinementMap, firstRefinementDiagonal]
    · rfl
  map_add' := by
    intro z w
    rcases z with ⟨x, y⟩
    rcases w with ⟨u, v⟩
    apply Prod.ext
    · ext i j
      fin_cases i <;> fin_cases j <;> simp [firstRefinementMap, firstRefinementDiagonal]
    · rfl

theorem firstRefinementMap_injective : Function.Injective firstRefinementMap := by
  intro z w h
  rcases z with ⟨x, y⟩
  rcases w with ⟨u, v⟩
  have hx : x = u := congrArg Prod.snd h
  have hmatrix : firstRefinementDiagonal x y = firstRefinementDiagonal u v := congrArg Prod.fst h
  have hy : y = v := by
    have hentry := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 1) hmatrix
    simpa [firstRefinementDiagonal] using hentry
  exact Prod.ext hx hy

theorem firstRefinementRingHom_injective : Function.Injective firstRefinementRingHom := by
  intro z w h
  apply firstRefinementMap_injective
  simpa [firstRefinementRingHom] using h

theorem firstRefinementMap_trace_preserving (z : ℝ × ℝ) :
    firstRefinementTrace1 (firstRefinementMap z) = firstRefinementTrace0 z := by
  rcases z with ⟨x, y⟩
  change phi⁻¹ * (phi * Matrix.trace (firstRefinementDiagonal x y) + x) = phi * x + y
  rw [firstRefinementDiagonal_trace]
  rcases perron_trace_compatible_with_refinement with ⟨hphi, hinv⟩
  calc
    phi⁻¹ * (phi * (x + y) + x) = (phi⁻¹ * phi) * (x + y) + phi⁻¹ * x := by ring
    _ = x + y + phi⁻¹ * x := by rw [hinv]; ring
    _ = (1 + phi⁻¹) * x + y := by ring
    _ = phi * x + y := by rw [hphi]

/-- The concrete first finite refinement preserves its Perron trace pairing, by the
shared generic trace-preserving star-map theorem. This proves one finite step only. -/
theorem fibonacci_first_refinement_pairing :
    ∀ x y : ℝ × ℝ,
      firstRefinementTrace1 (star (firstRefinementRingHom y) * firstRefinementRingHom x) =
        firstRefinementTrace0 (star y * x) :=
  D0.Algebra.FibonacciAFTower.gns_refinement_isometry
    firstRefinementTrace0 firstRefinementTrace1 firstRefinementRingHom
    (by intro x y; exact firstRefinementRingHom.map_mul x y)
    (by intro x; simpa [firstRefinementRingHom] using firstRefinementMap_star x)
    (by intro x; simpa [firstRefinementRingHom] using firstRefinementMap_trace_preserving x)

/-- **D0-VNEXT-AF-GNS-ISOMETRY-OWNER-001 (retained finite-real scope).** This theorem combines the
golden scalar identities with the generic conditional algebraic pairing identity. The finite-real
Fibonacci refinement application is recorded by the core declarations. No positive state, AF limit,
GNS quotient/completion, or Hilbert-space isometry is constructed; the former broader tower claim
remains open under this owner. -/
theorem perron_gns_tower_owner :
    (1 + phi⁻¹ = phi ∧ phi⁻¹ * phi = 1)
      ∧ (∀ {A B : Type} [inst : Mul A] [inst2 : Mul B] [inst3 : Star A] [inst4 : Star B]
          (tauA : A → ℝ) (tauB : B → ℝ) (iota : A → B),
          (∀ x y : A, iota (x * y) = iota x * iota y) →
          (∀ x : A, iota (star x) = star (iota x)) →
          (∀ a : A, tauB (iota a) = tauA a) →
          ∀ x y : A, tauB (star (iota y) * iota x) = tauA (star y * x)) := by
  refine ⟨perron_trace_compatible_with_refinement, ?_⟩
  intro A B _ _ _ _ tauA tauB iota hmul hstar htr
  exact gns_refinement_isometry tauA tauB iota hmul hstar htr

end D0.VNext.PerronGNSTower
