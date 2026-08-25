import D0.Tower.DetectionQuadratic

/-!
# Factor/block size law for the extension product (Lean lift of the 7th pass, DRAFT v2 post-skeptic)

Source: `_TASKS_CENTER_ATTACK/RAISE_GAP_E_MINIMALITY_MEMO.md` Sub-lemmas 2 and 3 (theorem-grade in
prose + `raise_gap_e_minimality_check.py`; never lifted to Lean). Carrier: the cardinality/
coordinate model the memo itself uses, `P = D₂ × D₂ × {±} ≅ ℤ₂³`, realized as `Fin 3 → Fin 2`.

Machine-checked here (post-skeptic #14 requalification — R1..R5 applied):
* **Group-grade size exclusion (Lagrange).** EVERY additive subgroup of the carrier — hence every
  direct factor, coordinate or not (e.g. the diagonal summand `⟨(1,1,1)⟩`) — has card dividing 8:
  sizes 3, 5, 6 are impossible (`no_subgroup_size_three_five_six`).
* **Coordinate factor sizes.** Coordinate factors have sizes `2^|s| ∈ {1,2,4,8}`; the proper
  non-trivial COORDINATE sizes are `{2,4}`, and both are realized (`ladder_coordinates_realized`).
* **Block-count law + uniformity.** A coordinate projection partitions the carrier into `2^|s|`
  fibers of equal size `2^(3−|s|)`: block-count 3 never occurs, and every coordinate
  fiber-partition is UNIFORM (kernel `decide`, no compiler trust).
* **X₃ shape separation.** The multiset `{1,1,6}` differs from every coordinate fiber-partition
  shape `replicate (2^k) (2^(3−k))`.

Disclosed inputs and narrated steps (NOT machine-checked here):
* The identity of `{1,1,6}` as the block-size multiset of the Aut-orbit fusion `X₃` (the
  conjugacy-class partition of the role group) is derived in `raise_gap_e_minimality_check.py`
  (full Aut(Q₈) enumeration, `Aut.orbit_sizes_1_1_6`, `X3.is_partition`, `X3.is_aut_invariant`)
  and enters this module as a DEFINITION (`X3blockSizes`).
* The reduction "a carrier bijection preserves the block-size multiset" (so shape inequality
  kills X₃-as-coordinate-projection under any labeling) is narrated, as in the memo.
* Krull–Schmidt UNIQUENESS of the decomposition is NOT formalized; only the size arithmetic and
  the Lagrange bound are.

What this module does NOT claim (the 7th pass's central finding, §3 ownership hinge): it does NOT
assert `AdmExt(X) ⟺ X is a proper direct factor of P` — that domain sentence is not derivable
from minimality (MUT-1) and is owned only via the 12th-pass port-route at operative grade. The
port-route ambient (dyad powers under the comparison-kind cap) and the factor-lattice ambient are
DISTINCT; this module CORROBORATES the `{2,4}` size-set from the second ambient, it does not
compose with `port_power_exhaustion` by any Lean term. Note also: the X₃ tower `(9,11,12)` is
already dead unconditionally by the owned parity ban (GAPE-1011 EoR); the X₃ leg here is
corroboration of its categorical separation, not the operative kill.
-/

namespace D0.Tower

/-- The cardinality/coordinate model of the extension product `P = D₂ × D₂ × {±} ≅ ℤ₂³`. -/
abbrev ExtProduct := Fin 3 → Fin 2

/-- **Group-grade exclusion (Lagrange).** Every additive subgroup of the carrier — hence every
direct factor, coordinate or NOT (the diagonal summand `⟨(1,1,1)⟩` included) — has cardinality
dividing 8: no subgroup of size 3, 5, or 6 exists. This is the general form of the 7th pass's
size exclusion, strictly stronger than the coordinate enumeration below. -/
theorem no_subgroup_size_three_five_six (H : AddSubgroup ExtProduct) :
    Nat.card H ≠ 3 ∧ Nat.card H ≠ 5 ∧ Nat.card H ≠ 6 := by
  have hd : Nat.card H ∣ Nat.card ExtProduct := AddSubgroup.card_addSubgroup_dvd_card H
  have h8 : Nat.card ExtProduct = 8 := by
    simp [Nat.card_eq_fintype_card]
  rw [h8] at hd
  refine ⟨?_, ?_, ?_⟩ <;> intro h <;> rw [h] at hd <;> revert hd <;> decide

/-- Coordinate restriction: the projection of `x` onto the coordinate subset `s` (off-`s`
coordinates flattened to `0`). Its fibers are the coordinate fiber-partition of `s`. -/
def restrictTo (s : Finset (Fin 3)) (x : ExtProduct) : ExtProduct :=
  fun i => if i ∈ s then x i else 0

/-- **Coordinate size-set.** Every coordinate factor size `2^|s|` lies in `{1, 2, 4, 8}`. -/
theorem factor_sizes (s : Finset (Fin 3)) :
    2 ^ s.card = 1 ∨ 2 ^ s.card = 2 ∨ 2 ^ s.card = 4 ∨ 2 ^ s.card = 8 := by
  have h : s.card ≤ 3 := le_trans (Finset.card_le_univ s) (by simp)
  interval_cases h : s.card <;> simp

/-- **Proper coordinate sizes.** Proper non-trivial coordinate factors have size `2` or `4` —
the owned ladder sizes (`D₂`, `ABCD = D₂²`). Realization of both: `ladder_coordinates_realized`. -/
theorem proper_factor_sizes (s : Finset (Fin 3)) (h1 : 1 ≤ s.card) (h2 : s.card ≤ 2) :
    2 ^ s.card = 2 ∨ 2 ^ s.card = 4 := by
  interval_cases h : s.card <;> simp

/-- **Realization.** Both proper coordinate sizes occur: a 1-coordinate subset (size 2) and a
2-coordinate subset (size 4) exist — `{2,4}` is exactly the proper coordinate size-set, not
merely an upper bound. -/
theorem ladder_coordinates_realized :
    (∃ s : Finset (Fin 3), s.card = 1 ∧ 2 ^ s.card = 2) ∧
    (∃ s : Finset (Fin 3), s.card = 2 ∧ 2 ^ s.card = 4) :=
  ⟨⟨{0}, by simp⟩, ⟨{0, 1}, by simp⟩⟩

/-- **Block-count law.** The coordinate fiber-partition of `s` has exactly `2^|s|` blocks
(kernel-checked). -/
theorem block_count (s : Finset (Fin 3)) :
    (Finset.univ.image (restrictTo s)).card = 2 ^ s.card := by
  revert s; decide

/-- **Uniformity.** Every block of a coordinate fiber-partition has the same size `2^(3−|s|)`:
coordinate projections are UNIFORM partitions (kernel-checked). -/
theorem coord_fibers_uniform (s : Finset (Fin 3)) :
    ∀ y ∈ Finset.univ.image (restrictTo s),
      (Finset.univ.filter (fun x => restrictTo s x = y)).card = 2 ^ (3 - s.card) := by
  revert s; decide

/-- The block-size multiset `(1, 1, 6)`. DISCLOSED INPUT: its identity as the block-size multiset
of the Aut-orbit fusion `X₃` (the conjugacy-class partition `{{+1},{−1},{±i,±j,±k}}` of the role
group) is derived in `raise_gap_e_minimality_check.py` (Aut(Q₈) enumeration), not in Lean. -/
def X3blockSizes : Multiset ℕ := {1, 1, 6}

/-- **X₃ shape separation.** The multiset `{1,1,6}` differs from every coordinate fiber-partition
shape `replicate (2^k) (2^(3−k))`, `k ≤ 3`. With the narrated reduction (a carrier bijection
preserves block-size multisets) this separates the fusion from every coordinate projection under
any relabeling. Corroborative: the X₃ tower is already dead by the owned parity ban. -/
theorem X3_not_factor_shape :
    ∀ k ∈ Finset.range 4, X3blockSizes ≠ Multiset.replicate (2 ^ k) (2 ^ (3 - k)) := by
  decide

/-- **Contrast (owned alphabets ARE coordinate-shaped).** `ABCD` blocks `(2,2,2,2)` and the sign
dyad blocks `(4,4)` both equal a coordinate fiber-partition shape. -/
theorem owned_alphabets_factor_shaped :
    ({2, 2, 2, 2} : Multiset ℕ) = Multiset.replicate (2 ^ 2) (2 ^ (3 - 2)) ∧
    ({4, 4} : Multiset ℕ) = Multiset.replicate (2 ^ 1) (2 ^ (3 - 1)) := by
  decide

/-- **Factor/block size law (bundle).** Lagrange group-grade exclusion of sizes 3/5/6 for ALL
subgroups; proper coordinate sizes `{2,4}` (both realized); `{1,1,6}` matches no coordinate
fiber shape. CORROBORATES the port-route size-set `{2,4}` from the factor-lattice ambient — the
two ambients are distinct and are not composed by any Lean term (see header). -/
theorem factor_block_law :
    (∀ H : AddSubgroup ExtProduct, Nat.card H ≠ 3 ∧ Nat.card H ≠ 5 ∧ Nat.card H ≠ 6) ∧
    (∀ s : Finset (Fin 3), 1 ≤ s.card → s.card ≤ 2 → 2 ^ s.card = 2 ∨ 2 ^ s.card = 4) ∧
    (∀ k ∈ Finset.range 4, X3blockSizes ≠ Multiset.replicate (2 ^ k) (2 ^ (3 - k))) :=
  ⟨no_subgroup_size_three_five_six, proper_factor_sizes, X3_not_factor_shape⟩

end D0.Tower
