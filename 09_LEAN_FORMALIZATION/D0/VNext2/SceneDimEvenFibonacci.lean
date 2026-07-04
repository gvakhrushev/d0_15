import Mathlib.Tactic

/-!
# D0-SCENE-DIM-EVEN-FIBONACCI-FORCING-001 — |V(scene)| = 33 = F₉ − 1, a forced +2-graded convergence

The scene `K(9,11,13)` has `|V| = 9 + 11 + 13 = 33`. The AF Dirac² tower (golden-mean SFT, scale ratio φ,
`D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001` + `D0-PERRON-SCALE-FLOW-OWNER-001`, both CERT-CLOSED) has its
Dirac² eigenvalues on the **even** powers `{φ⁰, φ², φ⁴, φ⁶}` with eigenspace multiplicities the
**even-indexed Fibonacci** numbers `{F₂, F₄, F₆, F₈} = {1, 3, 8, 21}`.

Both partitions of 33 are `+2`-graded, and the shared `+2` has a single proven root: the M1 orientation-bit
prohibition (a `+1` step would demand an external `ℤ₂` sign catalog, forbidden by M1). This file records the
arithmetic backbone of that convergence:

* the scene dimension `9 + 11 + 13 = 33`;
* the even-indexed Fibonacci partial sum `F₂ + F₄ + F₆ + F₈ = 33`;
* the closed form `33 = F₉ − 1` (the classical identity `∑_{k=1}^{n} F_{2k} = F_{2n+1} − 1` at `n = 4`);
* the algebra/eigenspace gap `dim (M₅ ⊕ M₃) = 5² + 3² = 34 = F₉ = 33 + 1` (the `+1` is the kernel mode).

Honest scope: this is a **dimension + grading** statement. It does NOT assert spectral congruence — the mass
profiles differ (scene `{1,12,10,8,2}` over 5 bands vs AF `{1,3,8,21}` over 4), and refining the coarse
scene band into the fine AF ladder is the separate NO-GO `D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`. The
algebra-level anchor stays refuted (`D0-VNEXT-33-SCENE-ANCHOR-NOGO-001`); this claim is orthogonal to it.
-/

namespace D0.VNext2.SceneDimEvenFibonacci

/-- The scene vertex count is the sum of the three zone sizes. -/
def sceneDim : ℕ := 9 + 11 + 13

/-- The even-indexed Fibonacci multiplicities of the AF Dirac² eigenspaces, summed. -/
def evenFibSum : ℕ := Nat.fib 2 + Nat.fib 4 + Nat.fib 6 + Nat.fib 8

/-- The AF matrix-algebra dimension `dim (M₅ ⊕ M₃) = 5² + 3²`. -/
def afAlgebraDim : ℕ := 5 ^ 2 + 3 ^ 2

/-- The scene has 33 vertices. -/
theorem scene_dim_eq : sceneDim = 33 := by decide

/-- The even-indexed Fibonacci multiplicities sum to 33. -/
theorem even_fib_sum_eq : evenFibSum = 33 := by decide

/-- The closed form: `33 = F₉ − 1`. -/
theorem f9_minus_one_eq : Nat.fib 9 - 1 = 33 := by decide

/-- **The dimension bridge**: scene dimension = even-Fibonacci eigenspace dimension = `F₉ − 1`. -/
theorem scene_dim_even_fibonacci_forcing :
    sceneDim = evenFibSum ∧ evenFibSum = Nat.fib 9 - 1 := by
  constructor <;> decide

/-- The even-index partial-sum identity `∑_{k=1}^{n} F_{2k} = F_{2n+1} − 1`, checked at `n = 1..4`
    (n = 4 is the scene case). -/
theorem even_fib_partial_sums :
    Nat.fib 2 = Nat.fib 3 - 1 ∧
    Nat.fib 2 + Nat.fib 4 = Nat.fib 5 - 1 ∧
    Nat.fib 2 + Nat.fib 4 + Nat.fib 6 = Nat.fib 7 - 1 ∧
    Nat.fib 2 + Nat.fib 4 + Nat.fib 6 + Nat.fib 8 = Nat.fib 9 - 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- The AF algebra dimension is `F₉ = 34 = 33 + 1`: one more than the eigenspace dimension (the `+1` is the
    kernel mode). The algebra anchor stays refuted; the eigenspace bridge is the orthogonal positive fact. -/
theorem algebra_is_eigenspace_plus_one :
    afAlgebraDim = Nat.fib 9 ∧ afAlgebraDim = sceneDim + 1 := by
  constructor <;> decide

end D0.VNext2.SceneDimEvenFibonacci
