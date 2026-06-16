import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic
import D0.Core.FiniteTypes

/-!
# D0-IM-004 — Möbius witness topological halting (orbit-averaged trace emission)

BOOK_01/06. Python certificate: `05_CERTS/vp_mobius_witness_topological_halting.py`.

The cert builds the 8 signed roles `Ω₈ = Role × sign` (`|Ω₈| = 8`, extended by the witness to `V₉`),
the trace-emission operator `F = diag(1,2,…,8)`, and the 8 cyclic-shift permutation matrices `P_k`
(`P_k[a,b] = 1 ⇔ a = b + k mod 8`). It then forms the **orbit average over the cyclic group**
`E = (1/8) Σ_k P_k F P_kᵀ` and asserts `P_k E P_kᵀ = E` for every shift (the "topological halting
quotient": the orbit-averaged emission is a fixed point of the role cycle).

Each conjugation `P_k F P_kᵀ` is `diag` with the entries cyclically permuted, so averaging over all 8
shifts sends every diagonal slot to the mean `(1+2+…+8)/8 = 36/8 = 9/2`; hence `E = (9/2)·I` — a scalar
matrix, which is trivially invariant under every shift. This module machine-checks exactly that finite
ℚ identity (and the `9/2` emission value), grounding the `|Ω₈| = 8` dimension in `D0.Core.FiniteTypes`.

**Scope (honest).** The finite linear-algebra core (the orbit average is the scalar `(9/2)·I`, and is
shift-invariant) is proved here. The *interpretation* — that this fixed point IS a "topological halting
quotient" of the Möbius witness dynamics — is the modeling reading and stays in the cert.
-/

namespace D0.Topology

open scoped BigOperators
open Matrix

/-- Trace-emission operator `F = diag(1,2,…,8)` over `ℚ` (slot `i` emits `i+1`). -/
def emissionDiag : Matrix (Fin 8) (Fin 8) ℚ := Matrix.diagonal (fun i => (i : ℚ) + 1)

/-- Cyclic shift-by-`k` permutation matrix `P_k[a,b] = 1 ⇔ a = b + k` (addition mod 8). -/
def shiftMat (k : Fin 8) : Matrix (Fin 8) (Fin 8) ℚ :=
  Matrix.of (fun a b => if a = b + k then (1 : ℚ) else 0)

/-- The orbit average of `F` over the cyclic group: `E = (1/8) Σ_k P_k F P_kᵀ`. -/
def orbitAverage : Matrix (Fin 8) (Fin 8) ℚ :=
  (1 / 8 : ℚ) • ∑ k : Fin 8, shiftMat k * emissionDiag * (shiftMat k)ᵀ

/-- The 8 signed roles `Ω₈` number `8` (the cycle length), reusing `D0.Core.FiniteTypes`. -/
theorem signed_roles_card : Fintype.card Omega8 = 8 := card_omega8

/-- The total trace emission `1+2+…+8 = 36`. -/
theorem emission_total : ∑ i : Fin 8, ((i : ℚ) + 1) = 36 := by native_decide

/-- The orbit-averaged emission per slot is `36/8 = 9/2`. -/
theorem orbit_averaged_emission : (∑ i : Fin 8, ((i : ℚ) + 1)) / 8 = 9 / 2 := by
  rw [emission_total]; norm_num

/-- **Orbit average is the scalar `(9/2)·I`.** `E = (1/8) Σ_k P_k F P_kᵀ = (9/2)·1`. -/
theorem orbit_average_is_scalar :
    orbitAverage = (9 / 2 : ℚ) • (1 : Matrix (Fin 8) (Fin 8) ℚ) := by native_decide

/-- **Shift invariance (topological halting fixed point).** `P_k E P_kᵀ = E` for every shift `k`. -/
theorem orbit_average_shift_invariant :
    ∀ k : Fin 8, shiftMat k * orbitAverage * (shiftMat k)ᵀ = orbitAverage := by native_decide

/-- **D0-IM-004.** The orbit-averaged trace emission over the 8 signed roles is the scalar matrix
`(9/2)·I` (emission value `36/8 = 9/2`), and it is a fixed point of every cyclic shift — the finite
linear-algebra core of the Möbius witness topological-halting quotient. -/
theorem witness_halting_cert :
    Fintype.card Omega8 = 8 ∧
    (∑ i : Fin 8, ((i : ℚ) + 1)) / 8 = 9 / 2 ∧
    orbitAverage = (9 / 2 : ℚ) • (1 : Matrix (Fin 8) (Fin 8) ℚ) ∧
    (∀ k : Fin 8, shiftMat k * orbitAverage * (shiftMat k)ᵀ = orbitAverage) :=
  ⟨signed_roles_card, orbit_averaged_emission, orbit_average_is_scalar,
   orbit_average_shift_invariant⟩

end D0.Topology
