import D0.Core.Phi
import D0.Claims.Q8DedekindMinimality
import D0.Claims.IcosianE8GramFinite
import Mathlib.Tactic

/-!
# D0-DIM8-NETWORK-001 — the dimension-8 forcing network (synthesis)

Prose: BOOK_02 §02.18.3 "The dimension-8 forcing network".

The corpus owns several order-8 / rank-8 facts in separate places — the octet `|Ω₈|=8`
(BOOK_01 §01.8), the unit-quaternion tower `Q₈ ⊂ 2T ⊂ 2I` and the icosian→`E_8` lattice
(BOOK_02 §02.18), the `E_8` Gram even-unimodularity (`D0-ICOSIAN-E8-GRAM-001`). A systematic
"Frobenius-class" audit shows these are not coincidences but one forcing of the number **8**,
sewn by a network of classical uniqueness/classification theorems:

  `{±} → ℤ₂` (Bott period 2) → `ABCD×{±} = 8 = |Ω₈|` (Hurwitz 1,2,4,8 / Clifford & Bott-KO
  period 8) → `Q₈ ⊂ 2T ⊂ 2I` (Dedekind + icosians) → `E_8` (Mordell uniqueness) → triality
  `Spin(8)` (three 8-dimensional representations `V, Δ_+, Δ_-`).

This module machine-checks the **arithmetic skeleton** of the network and reuses the proved
leaves; the periodicity/triality theorems themselves are external (named in prose, owned by
the classical sources), not re-proved here.

HONEST scope (and the anti-numerology caveat of BOOK_00 §00.9): the network forces the number
**8** and the rank-8 even-unimodular target. It does **NOT** contain "3 fermion generations"
(the `3` of triality is the number of 8-dim reps of `D₄`, not families) nor the causal
threshold `C_max=3/8` — both are explicitly rejected forcing-links.
-/

namespace D0.Synthesis

open D0
open D0.Claims
open Matrix

/-! ## The octet: `8 = 2·4` (`ABCD × {±}`), the Hurwitz dimension. -/

/-- `|Ω₈| = |ABCD| · |{±}| = 4·2 = 8` — the octet, sitting at the Hurwitz division-algebra
dimension `8` (the last of `1,2,4,8`). -/
theorem octet_is_eight : (8 : ℕ) = 2 * 4 := by decide

/-! ## The unit-quaternion tower `Q₈ ⊂ 2T ⊂ 2I`: orders `8 ∣ 24 ∣ 120`. -/

/-- Orders of the exact unit-quaternion tower `Q₈ ⊂ 2T ⊂ 2I` (binary tetrahedral / binary
icosahedral): `8 ∣ 24` and `24 ∣ 120`, so `Q₈` sits at the base of the tower ending in the
`120` icosians (vertices of the 600-cell). -/
theorem tower_orders_divide : (8 ∣ 24) ∧ (24 ∣ 120) := by decide

/-- The tower indices: `[2T:Q₈]=3`, `[2I:2T]=5`, `[2I:Q₈]=15`. -/
theorem tower_indices : (24 / 8 = 3) ∧ (120 / 24 = 5) ∧ (120 / 8 = 15) := by decide

/-- `Z(Q₈) = {±1}` is the single ℤ₂ at the base of the tower (reused leaf). -/
theorem tower_base_center_z2 : q8Center.card = 2 := by
  rw [q8_center_pm1]; decide

/-! ## The rank-8 target: the `E_8` Gram is even unimodular (reused leaf). -/

/-- The `E_8` Gram (rank `8 = 2·4`) is symmetric, even (diagonal `2`) and unimodular
(`det = 1`) — the icosian ring's lattice, reused from `D0-ICOSIAN-E8-GRAM-001`. -/
theorem rank8_even_unimodular :
    e8Gramᵀ = e8Gram ∧ (∀ i, e8Gram i i = 2) ∧ Matrix.det e8Gram = 1 ∧ (8 : ℕ) = 2 * 4 :=
  icosian_e8_gram_finite

/-! ## Triality of `Spin(8)` (`D₄`): three 8-dimensional representations. -/

/-- The `D₄` Dynkin diagram as the star `K_{1,3}`: the central node (`0`) is joined to three
legs (`1,2,3`). Its outer-automorphism group `Out(Spin(8)) ≅ S₃` permutes the three legs =
the three 8-dimensional representations `V, Δ_+, Δ_-`. -/
def d4deg : Fin 4 → ℕ
  | 0 => 3
  | 1 => 1
  | 2 => 1
  | 3 => 1

/-- The central node of `D₄` has degree `3` (it meets all three legs). -/
theorem d4_center_degree_three : d4deg 0 = 3 := rfl

/-- `D₄` has exactly three legs (degree-1 nodes) — the three 8-dimensional representations
permuted by triality. -/
theorem d4_three_legs :
    (Finset.univ.filter (fun i : Fin 4 => d4deg i = 1)).card = 3 := by decide

/-- The triality outer-automorphism group has order `|S₃| = 3! = 6`. -/
theorem triality_outer_order : Nat.factorial 3 = 6 := by decide

/-! ## The network, assembled. -/

/-- **D0-DIM8-NETWORK-001 (synthesis).** The arithmetic skeleton of the dimension-8 forcing
network: the octet `8 = 2·4`; the unit-quaternion tower `8 ∣ 24 ∣ 120` with `Z(Q₈)=ℤ₂` at the
base; the rank-8 even-unimodular `E_8` Gram; and the three legs of `D₄` (triality's three
8-dim reps, `|S₃|=6`). The classical periodicity/uniqueness theorems that *force* this skeleton
— Hurwitz (1,2,4,8), Clifford & Bott period 8, Mordell (`E_8` unique), Spin(8) triality — are
external owners named in BOOK_02 §02.18.3. -/
theorem dim8_network :
    ((8 : ℕ) = 2 * 4) ∧
    ((8 ∣ 24) ∧ (24 ∣ 120)) ∧
    (q8Center.card = 2) ∧
    (Matrix.det e8Gram = 1 ∧ (∀ i, e8Gram i i = 2)) ∧
    ((Finset.univ.filter (fun i : Fin 4 => d4deg i = 1)).card = 3 ∧ Nat.factorial 3 = 6) :=
  ⟨octet_is_eight, tower_orders_divide, tower_base_center_z2,
    ⟨rank8_even_unimodular.2.2.1, rank8_even_unimodular.2.1⟩,
    ⟨d4_three_legs, triality_outer_order⟩⟩

end D0.Synthesis
