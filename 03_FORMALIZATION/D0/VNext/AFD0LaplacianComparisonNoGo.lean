import D0.VNext.FibonacciAFAlgebra
import Mathlib.Tactic

/-!
# D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 — finite dimension separation (Outcome D scope)

The frozen D0 finite Laplacian carrier has dimension 33. This module proves that the Fibonacci
finite-level carriers have dimensions 2, 5, 13, 34, … and that no level has dimension 33. It rules
out an identification that requires an equal-dimensional AF level. It does not rule out arbitrary
linear maps between different dimensions or prove that no canonical comparison map exists without a
specified map class and compatibility conditions. The broader comparison-map question remains under
its existing primitive owner.

This module also does not construct a GNS Hilbert tower. Finite-real Perron pairing preservation is
an algebraic identity and is not a Hilbert-space isometry.
-/
namespace D0.VNext.AFD0LaplacianComparisonNoGo

open D0.VNext.FibonacciAFAlgebra

/-- The frozen D0 K(9,11,13) Laplacian carrier dimension `= 1+12+10+8+2 = 33` (fixed scene). -/
def d0LaplacianDim : ℕ := 1 + 12 + 10 + 8 + 2

theorem d0_laplacian_dim_eq : d0LaplacianDim = 33 := by decide

/-- **The AF tower skips the D0 Laplacian dimension**: `dim A_2 = 13 < 33 < 34 = dim A_3`, so no AF
level has the same finite dimension as the fixed D0 carrier. This rules out an equal-dimension
identification, not arbitrary maps between different dimensions. -/
theorem af_skips_d0_dim :
    dimA 2 = 13 ∧ dimA 3 = 34 ∧ dimA 2 < d0LaplacianDim ∧ d0LaplacianDim < dimA 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 (narrow dimension-separation result).**
The theorem records the 33-dimensional D0 carrier and proves that the finite AF-level dimensions
straddle 33, with no match through level 3. The total theorem below proves no AF level has dimension
33. These facts rule out comparison constructions that require equal dimensions; they do not prove
that no arbitrary or canonical comparison map can exist. That stronger claim needs a specified map
class and compatibility conditions. -/
theorem laplacian_tower_compatibility_no_go :
    d0LaplacianDim = 33
      ∧ dimA 2 < d0LaplacianDim ∧ d0LaplacianDim < dimA 3
      ∧ (∀ N, N ≤ 3 → dimA N ≠ d0LaplacianDim) := by
  refine ⟨d0_laplacian_dim_eq, (af_skips_d0_dim.2.2.1), af_skips_d0_dim.2.2.2, ?_⟩
  intro N hN
  interval_cases N <;> decide

/-! ### F4 wave (2026-07-06): totality of the 33-skip — W4_DECOMPOSITION_MEMO.md T2A

The theorem above quantifies only `N ≤ 3`; the W4 wave closed ALL `N` at script grade via
the recurrence identity `dimA(n+1) − dimA(n) = a(a+2b) > 0` (T2A.3-4), `dimA 3 = 34 > 33`
(T2A.5), and the typed separator `dimA n = F(2n+3)` — odd-indexed Fibonacci, and `33` is
not one (T2A.6). The lemmas below are the named Lean lift ("`dimA_strictMono` + unbounded
`∀ N, dimA N ≠ 33` — a one-lemma upgrade of the `N ≤ 3` quantifier", memo §2a). -/

/-- Both path-count components are positive at every level (induction: `(a,b) ↦ (a+b,a)`
from `(1,1)`). -/
theorem pc_pos : ∀ n, 1 ≤ (pc n).1 ∧ 1 ≤ (pc n).2 := by
  intro n
  induction n with
  | zero => exact ⟨le_refl 1, le_refl 1⟩
  | succ n ih => exact ⟨Nat.le_add_right_of_le ih.1, ih.1⟩

/-- **The T2A.3 recurrence identity, exact and additive:**
`dimA (n+1) = dimA n + a·(a + 2b)` where `(a, b) = pc n`.
(`(a+b)² + a² = (a² + b²) + a(a + 2b)`.) -/
theorem dimA_succ (n : ℕ) :
    dimA (n + 1) = dimA n + (pc n).1 * ((pc n).1 + 2 * (pc n).2) := by
  simp only [dimA, pc, D0.Algebra.FibonacciAFTower.dimA,
    D0.Algebra.FibonacciAFTower.pathCount]
  ring

/-- **T2A.4: strict monotonicity of the AF dimension tower** — the increment `a(a+2b)` is
positive since `a ≥ 1`. -/
theorem dimA_strictMono : StrictMono dimA := by
  apply strictMono_nat_of_lt_succ
  intro n
  rw [dimA_succ n]
  have ha := (pc_pos n).1
  have : 1 ≤ (pc n).1 * ((pc n).1 + 2 * (pc n).2) :=
    Nat.one_le_iff_ne_zero.mpr (Nat.mul_ne_zero (by omega) (by omega))
  omega

/-- The path-count vector is the Fibonacci pair: `pc n = (F(n+2), F(n+1))`. -/
theorem pc_eq_fib : ∀ n, pc n = (Nat.fib (n + 2), Nat.fib (n + 1)) := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [pc, D0.Algebra.FibonacciAFTower.pathCount, ih, Prod.mk.injEq]
      refine ⟨?_, trivial⟩
      rw [Nat.fib_add_two (n := n + 1), show n + 1 + 1 = n + 2 from rfl]
      exact Nat.add_comm _ _

/-- **T2A.6 typed separator: `dimA n = F(2n+3)`** — the AF dimensions are exactly the
odd-indexed Fibonacci numbers `2, 5, 13, 34, 89, 233, …` (`F(m+1)² + F(m)² = F(2m+1)`
with `m = n+1`). -/
theorem dimA_eq_fib (n : ℕ) : dimA n = Nat.fib (2 * n + 3) := by
  have h : 2 * n + 3 = 2 * (n + 1) + 1 := by ring
  change (pc n).1 ^ 2 + (pc n).2 ^ 2 = Nat.fib (2 * n + 3)
  rw [pc_eq_fib n, h, Nat.fib_two_mul_add_one]

/-- **THE TOTAL 33-SKIP:** `dimA N ≠ 33` for every `N`. This proves there is no equal-dimensional
AF level for the fixed D0 carrier; it does not rule out maps between spaces of different dimensions. -/
theorem af_skips_d0_dim_total : ∀ N, dimA N ≠ d0LaplacianDim := by
  intro N h
  rw [d0_laplacian_dim_eq] at h
  rcases Nat.lt_or_ge N 3 with hN | hN
  · interval_cases N <;>
      simp_all [dimA, D0.Algebra.FibonacciAFTower.dimA,
        D0.Algebra.FibonacciAFTower.pathCount]
  · have h34 : dimA 3 ≤ dimA N := dimA_strictMono.monotone hN
    have : dimA 3 = 34 := by decide
    omega

/-- **D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 (Outcome D, NO-GO — TOTAL form).**
The `N ≤ 3` quantifier of `laplacian_tower_compatibility_no_go` is closed to ALL levels:
the D0 Laplacian dimension `33` is bracketed (`13 < 33 < 34`) and the tower is strictly
monotone with `dimA = F(2·+3)`, so **no AF level at any depth** has dimension `33`.
This rules out equal-dimensional identifications only; existence or nonexistence of an
arbitrary or canonical comparison map `Ξ_N` remains open. -/
theorem laplacian_tower_compatibility_no_go_total :
    d0LaplacianDim = 33
      ∧ StrictMono dimA
      ∧ (∀ n, dimA n = Nat.fib (2 * n + 3))
      ∧ (∀ N, dimA N ≠ d0LaplacianDim) :=
  ⟨d0_laplacian_dim_eq, dimA_strictMono, dimA_eq_fib, af_skips_d0_dim_total⟩

end D0.VNext.AFD0LaplacianComparisonNoGo
