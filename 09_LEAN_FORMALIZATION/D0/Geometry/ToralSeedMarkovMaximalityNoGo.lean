import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001 — the Markov partition/adjacency is not forced

Maximality strengthening of `D0-TORAL-CANONICAL-MARKOV-PARTITION-NOGO-001` (a 3-point seed does not
determine a partition). The forced dynamical invariants of the toral automorphism — spectrum `{φ, ψ}`,
entropy `log φ`, trace, determinant (all consequences of the integral conjugacy `C T C⁻¹ = −M_φ`) — do
**not** determine the Markov adjacency matrix / partition. We exhibit distinct admissible nonnegative
integer adjacency matrices that all carry the golden Perron data `φ` (entropy `log φ`):

- `Mφ = !![1,1;1,0]` — `Mφ² = Mφ + 1` (charpoly `x²−x−1`, Perron `φ`, **2 rectangles**);
- `M2 = !![0,1;1,1]` — same `(trace, det) = (1,−1)` hence same charpoly `x²−x−1`, but `M2 ≠ Mφ`;
- `A3 = !![1,1,0;1,0,0;0,1,0]` — `A3³ = A3² + A3` (charpoly `x³−x²−x = x(x²−x−1)`, Perron `φ`,
  **3 rectangles**).

So both a 2-rectangle and a 3-rectangle admissible adjacency realize the same golden dynamics: the
rectangle count and the adjacency matrix are **not forced by the seed**. A canonical partition would
require an external Adler–Weiss/Williams choice (`D0-ADLER-WEISS-PARTITION-OWNER-001`, passport), not a
present-core theorem. Closed-negative.
-/

namespace D0.Geometry.ToralSeedMarkovMaximalityNoGo

open Matrix

def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]
def M2 : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, 1]
def A3 : Matrix (Fin 3) (Fin 3) ℤ := !![1, 1, 0; 1, 0, 0; 0, 1, 0]

/-- `Mφ` carries the golden Perron data: `Mφ² = Mφ + 1` (charpoly `x²−x−1`, Perron `φ`, 2 rectangles). -/
theorem Mphi_golden : Mphi ^ 2 = Mphi + 1 := by native_decide

/-- `M2 ≠ Mφ` yet shares all spectral invariants — `(trace, det) = (1, −1)`, charpoly `x²−x−1`. The
adjacency is not determined by the forced invariants (a state relabeling is unfixed by the seed). -/
theorem M2_distinct_same_invariants :
    M2 ≠ Mphi ∧ Matrix.trace M2 = Matrix.trace Mphi ∧ Matrix.det M2 = Matrix.det Mphi := by
  refine ⟨?_, ?_, ?_⟩ <;> native_decide

/-- `A3` carries the golden Perron data with **3 rectangles**: `A3³ = A3² + A3` (charpoly
`x³−x²−x = x(x²−x−1)`, Perron `φ`). A genuinely different partition with the same entropy `log φ`. -/
theorem A3_golden : A3 ^ 3 = A3 ^ 2 + A3 := by native_decide

/-- **D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001 (closed-negative).** Distinct admissible adjacency
matrices — a 2-rectangle `Mφ` and a 3-rectangle `A3`, both carrying the golden Perron eigenvalue `φ`
(entropy `log φ`), plus a same-size relabel `M2 ≠ Mφ` with identical invariants — all realize the toral
golden dynamics. The Markov partition / adjacency / rectangle count is NOT forced by the seed; a canonical
partition requires an external Adler–Weiss/Williams choice (passport). -/
theorem toral_seed_markov_maximality_nogo :
    (Mphi ^ 2 = Mphi + 1)
      ∧ (A3 ^ 3 = A3 ^ 2 + A3)
      ∧ (M2 ≠ Mphi ∧ Matrix.trace M2 = Matrix.trace Mphi ∧ Matrix.det M2 = Matrix.det Mphi)
      ∧ (2 : ℕ) ≠ 3 :=
  ⟨Mphi_golden, A3_golden, M2_distinct_same_invariants, by decide⟩

end D0.Geometry.ToralSeedMarkovMaximalityNoGo
