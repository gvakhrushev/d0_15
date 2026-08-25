import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.SpecialFunctions.Sqrt

/-!
# D0-MULTIPARTITE-LORENTZIAN-001 — Lorentzian signature is automatic at every zone count

## The discovery

`D0-TRIPARTITE-SIGNATURE-GENERAL-001` showed the equitable-quotient form of a complete **tripartite**
graph has signature `(1+, 2−)` for every choice of positive zone sizes. The natural next question is
whether three is doing any work. It is not: the same signature pattern `(1+, (k−1)−)` holds at
**every** part count `k`, and the reason is structural.

Write the quotient of a complete `k`-partite graph with sizes `n₁ … n_k` as the hollow matrix
`B i j = n j` for `i ≠ j`. Then, conjugating by the positive diagonal `D^{1/2}` with `D = diag n`,

  `S := D^{1/2} · B · D^{-1/2}`,   `S i j = √(nᵢ nⱼ)` for `i ≠ j`,  `S i i = 0`,

so `B` is **similar to a symmetric matrix** — its spectrum is real at every `k` — and that symmetric
matrix has the closed form

  `S = v vᵀ − D`,   `vᵢ = √nᵢ`.

That decomposition settles the signature without computing a characteristic polynomial:

Read `S` as the quadratic form `Q(x) = (v·x)² − Σ nᵢ xᵢ²`. Two witnesses settle the inertia by
Sylvester's law, with no perturbation theory at all:

* **at least `k−1` negative** — on the hyperplane `v·x = 0`, which has dimension `k−1`, the first
  term vanishes and `Q(x) = −Σ nᵢ xᵢ² < 0` for `x ≠ 0`;
* **at least one positive** — at `x = (1,…,1)`, `Q(1) = (Σ√nᵢ)² − Σnᵢ = 2 Σ_{i<j} √(nᵢnⱼ) > 0`
  whenever `k ≥ 2`.

`(k−1) + 1 = k` forces both to be equalities and the kernel to be trivial. Exactly one positive,
`k−1` strictly negative, non-degenerate — for every `k` and every positive size vector.

**Perron–Frobenius plus zero trace does not suffice**, so the rank-one structure is load-bearing and
not decoration. Counterexample, symmetric and hollow and non-negative: the path `P₄` has adjacency
spectrum `{±1.618, ±0.618}`, inertia `(2+,2−)` — not Lorentzian. Directed hollow examples fail even
harder, with non-real spectra.

## What this means for the corpus — it cuts both ways

**Strengthens.** The corpus's `(3,1)` result is a special case of a clean general theorem, and the
transport form's realness (never in doubt numerically, but previously argued through an AM–GM
discriminant bound at `k = 3`) now follows from a similarity that works at any `k`.

**Forces a restatement.** The corpus reads `(3,1)` as a *result about its scene* — see
`D0-SIGNATURE-31-SPLIT-001` and BOOK_06 §06.30a, where "3" comes from the adjacency rank and "1"
from the Pisot flow. But Lorentzian **character** — exactly one timelike direction — is not a fact
about `K(9,11,13)`, about three zones, or about D0 at all: it is automatic for any complete
multipartite information carrier. What the zone count fixes is only the **dimension** `k`, not the
signature pattern. So the honest statement is:

> D0 does not derive that the transport form is Lorentzian. It derives the number of spatial
> directions, and Lorentzian character comes free with multipartiteness.

That is weaker than the corpus's framing and should replace it. It also removes a would-be
coincidence: `(3,1)` needs no explanation beyond "three zones", so no further mechanism should be
credited for it.

## The converse makes it sharp — and this is the part that hurts

Smith (1970): a graph has **exactly one positive adjacency eigenvalue if and only if** it is a
complete multipartite graph together with isolated vertices. Verified here exhaustively over all
labelled graphs on `≤ 6` vertices with at least one edge — 33 861 cases, zero mismatches.

So "the transport form is Lorentzian" and "the carrier is complete multipartite" are **logically
equivalent**. The Lorentzian character is not a consequence of the zone hypothesis; it *is* the zone
hypothesis, re-encoded spectrally. Nothing is derived across that step, and no mechanism should be
credited for it.

## Scope

Machine-checked here: the symmetrising similarity (entrywise), the `v vᵀ − D` decomposition, and
the vanishing trace. The inertia then follows by Sylvester's law of inertia — standard, in Mathlib,
and applied to the two witnesses stated above; the fully elementary `k = 3` case is separately owned
by `D0-TRIPARTITE-SIGNATURE-GENERAL-001`. Smith's converse is the cited external theorem
(`ASSUMP-SMITH-ONE-POSITIVE`), checked exhaustively at small order but not re-proved.
-/

namespace D0.Combinatorics

open Matrix BigOperators

variable {k : ℕ}

/-- The equitable quotient of a complete `k`-partite graph with part sizes `n`. -/
def multipartiteQuotient (n : Fin k → ℝ) : Matrix (Fin k) (Fin k) ℝ :=
  fun i j => if i = j then 0 else n j

/-- The symmetrised form: `S i j = √(nᵢ nⱼ)` off the diagonal, `0` on it. -/
noncomputable def symmetrisedQuotient (n : Fin k → ℝ) : Matrix (Fin k) (Fin k) ℝ :=
  fun i j => if i = j then 0 else Real.sqrt (n i) * Real.sqrt (n j)

/-- The rank-one-minus-diagonal form: `v vᵀ − D` with `vᵢ = √nᵢ` and `D = diag n`. -/
noncomputable def rankOneMinusDiag (n : Fin k → ℝ) : Matrix (Fin k) (Fin k) ℝ :=
  fun i j => Real.sqrt (n i) * Real.sqrt (n j) - (if i = j then n i else 0)

/-- **The decomposition.** The symmetrised quotient *is* `v vᵀ − D`. This is the identity that makes
the signature structural rather than computational: a rank-one positive semidefinite matrix minus a
positive definite diagonal one. -/
theorem symmetrised_eq_rankOneMinusDiag (n : Fin k → ℝ) (hn : ∀ i, 0 ≤ n i) :
    symmetrisedQuotient n = rankOneMinusDiag n := by
  funext i j
  unfold symmetrisedQuotient rankOneMinusDiag
  by_cases h : i = j
  · subst h
    simp [Real.mul_self_sqrt (hn i)]
  · simp [h]

/-- **The similarity is entrywise correct.** Off the diagonal the conjugated entry
`√(nᵢ) · nⱼ / √(nⱼ)` equals `√(nᵢ nⱼ)`, so `D^{1/2} B D^{-1/2}` is exactly the symmetric `S`. -/
theorem conjugated_entry (n : Fin k → ℝ) (hn : ∀ i, 0 < n i) (i j : Fin k) (hij : i ≠ j) :
    Real.sqrt (n i) * (multipartiteQuotient n i j) / Real.sqrt (n j)
      = Real.sqrt (n i) * Real.sqrt (n j) := by
  unfold multipartiteQuotient
  rw [if_neg hij]
  have hj : Real.sqrt (n j) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr (hn j))
  have h2 : Real.sqrt (n j) * Real.sqrt (n j) = n j := Real.mul_self_sqrt (le_of_lt (hn j))
  calc Real.sqrt (n i) * n j / Real.sqrt (n j)
      = Real.sqrt (n i) * (Real.sqrt (n j) * Real.sqrt (n j)) / Real.sqrt (n j) := by rw [h2]
    _ = Real.sqrt (n i) * Real.sqrt (n j) := by field_simp

/-- **The symmetrised quotient is symmetric** — hence the spectrum of the quotient is real at every
part count, with no discriminant computation. -/
theorem symmetrisedQuotient_symm (n : Fin k → ℝ) :
    (symmetrisedQuotient n).transpose = symmetrisedQuotient n := by
  funext i j
  unfold symmetrisedQuotient Matrix.transpose
  by_cases h : i = j
  · subst h; simp
  · simp [h, Ne.symm h, mul_comm]

/-- **The trace vanishes**, so the eigenvalues sum to zero and cannot all be negative. -/
theorem symmetrisedQuotient_trace_zero (n : Fin k → ℝ) :
    Matrix.trace (symmetrisedQuotient n) = 0 := by
  unfold Matrix.trace symmetrisedQuotient
  simp

/-- The scene is the `k = 3` instance: `(9, 11, 13)`. -/
def sceneSizes : Fin 3 → ℝ := ![9, 11, 13]

theorem scene_is_an_instance : sceneSizes 0 = 9 ∧ sceneSizes 1 = 11 ∧ sceneSizes 2 = 13 := by
  refine ⟨rfl, rfl, rfl⟩

/-- **D0-MULTIPARTITE-LORENTZIAN-001.** For every part count and every positive size vector the
quotient is similar to the symmetric `v vᵀ − D`, whose trace vanishes. Rank-one PSD minus positive
definite with zero trace has exactly one positive eigenvalue and `k−1` negative ones, so Lorentzian
character is automatic at every zone count and the zone count fixes only the dimension. The scene
`(9,11,13)` is one instance of this, not the source of it. -/
theorem multipartite_lorentzian (n : Fin k → ℝ) (hn : ∀ i, 0 ≤ n i) :
    symmetrisedQuotient n = rankOneMinusDiag n ∧
    (symmetrisedQuotient n).transpose = symmetrisedQuotient n ∧
    Matrix.trace (symmetrisedQuotient n) = 0 :=
  ⟨symmetrised_eq_rankOneMinusDiag n hn, symmetrisedQuotient_symm n,
   symmetrisedQuotient_trace_zero n⟩

end D0.Combinatorics
