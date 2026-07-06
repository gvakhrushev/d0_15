import D0.VNext.FibonacciAFAlgebra
import Mathlib.Tactic

/-!
# D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 — no canonical comparison map (Phase C, Outcome D)

The frozen D0 finite Laplacian lives on the FIXED K(9,11,13) scene: a `33`-dimensional carrier with
spectrum `{0:1, 20:12, 22:10, 24:8, 33:2}` (`1+12+10+8+2 = 33`). The Fibonacci AF/GNS carrier is an
INDUCTIVE tower whose dimension `dim A_N = 2,5,13,34,…` grows without bound and **skips 33**
(`dim A_2 = 13 < 33 < 34 = dim A_3`). So no AF level has the D0 Laplacian's dimension, and the two towers
run in opposite directions (AF inductive/growing vs the D0 scene fixed, and the D0 support tower inverse/
projective). Hence there is **no canonical comparison map `Ξ_N`** intertwining the AF Dirac/Laplacian with
the frozen D0 Laplacian.

**Outcome D**: the recovered Fibonacci AF tower is a correct symbolic/FORMALISM object, but it is NOT the
inductive completion of the frozen D0 Laplacian dynamics. The Dirac-compatible lift is obstructed; a
canonical comparison map is a further new primitive. (No carrier identified by name; no comparison
inferred from equal dimensions — there are none.)
-/

namespace D0.VNext.AFD0LaplacianComparisonNoGo

open D0.VNext.FibonacciAFAlgebra

/-- The frozen D0 K(9,11,13) Laplacian carrier dimension `= 1+12+10+8+2 = 33` (fixed scene). -/
def d0LaplacianDim : ℕ := 1 + 12 + 10 + 8 + 2

theorem d0_laplacian_dim_eq : d0LaplacianDim = 33 := by decide

/-- **The AF tower skips the D0 Laplacian dimension**: `dim A_2 = 13 < 33 < 34 = dim A_3`, so no AF level
carrier matches the fixed `33`-dim D0 Laplacian. -/
theorem af_skips_d0_dim :
    dimA 2 = 13 ∧ dimA 3 = 34 ∧ dimA 2 < d0LaplacianDim ∧ d0LaplacianDim < dimA 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- **D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 (Outcome D, NO-GO).** No canonical comparison map
`Ξ_N` exists: the D0 Laplacian dimension `33` is strictly bracketed by consecutive AF dimensions
(`13 < 33 < 34`), so no AF level carrier matches it, and the towers run in opposite directions. The
Dirac-compatible lift of the frozen D0 Laplacian is obstructed — the AF tower is FORMALISM-only. -/
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
  simp only [dimA, pc]
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
      simp only [pc, ih, Prod.mk.injEq]
      refine ⟨?_, trivial⟩
      rw [Nat.fib_add_two (n := n + 1), show n + 1 + 1 = n + 2 from rfl]
      exact Nat.add_comm _ _

/-- **T2A.6 typed separator: `dimA n = F(2n+3)`** — the AF dimensions are exactly the
odd-indexed Fibonacci numbers `2, 5, 13, 34, 89, 233, …` (`F(m+1)² + F(m)² = F(2m+1)`
with `m = n+1`). -/
theorem dimA_eq_fib (n : ℕ) : dimA n = Nat.fib (2 * n + 3) := by
  have h : 2 * n + 3 = 2 * (n + 1) + 1 := by ring
  rw [dimA, pc_eq_fib n, h, Nat.fib_two_mul_add_one]

/-- **THE TOTAL 33-SKIP (T2A totality closure): `dimA N ≠ 33` for ALL `N`** — not just
`N ≤ 3`. Once above (`dimA 3 = 34 > 33`), strictly-monotone stays above; below,
`2, 5, 13` are checked. So NO AF level ever matches the frozen D0 Laplacian dimension. -/
theorem af_skips_d0_dim_total : ∀ N, dimA N ≠ d0LaplacianDim := by
  intro N h
  rw [d0_laplacian_dim_eq] at h
  rcases Nat.lt_or_ge N 3 with hN | hN
  · interval_cases N <;> simp_all [dimA, pc]
  · have h34 : dimA 3 ≤ dimA N := dimA_strictMono.monotone hN
    have : dimA 3 = 34 := by decide
    omega

/-- **D0-VNEXT-DIRAC-LAPLACIAN-COMPATIBILITY-OWNER-001 (Outcome D, NO-GO — TOTAL form).**
The `N ≤ 3` quantifier of `laplacian_tower_compatibility_no_go` is closed to ALL levels:
the D0 Laplacian dimension `33` is bracketed (`13 < 33 < 34`) and the tower is strictly
monotone with `dimA = F(2·+3)`, so **no AF level at any depth** matches the frozen scene.
The comparison map `Ξ_N` is obstructed unconditionally in the level index. -/
theorem laplacian_tower_compatibility_no_go_total :
    d0LaplacianDim = 33
      ∧ StrictMono dimA
      ∧ (∀ n, dimA n = Nat.fib (2 * n + 3))
      ∧ (∀ N, dimA N ≠ d0LaplacianDim) :=
  ⟨d0_laplacian_dim_eq, dimA_strictMono, dimA_eq_fib, af_skips_d0_dim_total⟩

end D0.VNext.AFD0LaplacianComparisonNoGo
