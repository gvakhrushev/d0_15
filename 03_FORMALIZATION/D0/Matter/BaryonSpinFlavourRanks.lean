import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Prod
import Mathlib.Tactic

/-!
# D0-CVFT-F3B — baryon spin/flavour multiplet ranks (the SU(6) `56 = 40 ⊕ 16`)

Multiset-count (sorted-triple) cardinalities for the baryon 3-index sector: with `n` labels the
symmetric 3-index combinations number `C(n+2,3)`. The physics content is the SU(6) baryon-multiplet
decomposition: flavour-`SU(3)` decuplet `10`, spin doubling `4`, the spin-flavour `40 = 10·4`
(decuplet × spin-3/2), the full `SU(6)` `56`, and `56 − 40 = 16` (the octet sector). All exact finite
counts (`decide`/`native_decide`), generalizing the proven `BaryonS3Symmetrizer` decuplet-10 idiom to
a parametric subtype (avoiding 56 hand-written constructors).
-/

namespace D0.Matter

/-- Sorted (multiset) triples over `n` labels: `{(a,b,c) : a ≤ b ≤ c}`. Counts the symmetric
3-index combinations `C(n+2,3)`. -/
def SortedTripleN (n : ℕ) : Type :=
  {t : Fin n × Fin n × Fin n // t.1 ≤ t.2.1 ∧ t.2.1 ≤ t.2.2}

instance (n : ℕ) : Fintype (SortedTripleN n) := by unfold SortedTripleN; infer_instance
instance (n : ℕ) : DecidableEq (SortedTripleN n) := by unfold SortedTripleN; infer_instance

/-- Spin doubling: sorted triples over 2 labels number `4` (`C(4,3)`). -/
theorem spin_sorted_card : Fintype.card (SortedTripleN 2) = 4 := by decide

/-- Flavour decuplet: sorted triples over 3 labels number `10` (`C(5,3)`). -/
theorem flavour_sorted_card : Fintype.card (SortedTripleN 3) = 10 := by decide

/-- The full SU(6) sector: sorted triples over 6 labels number `56` (`C(8,3)`). -/
theorem six_sorted_card : Fintype.card (SortedTripleN 6) = 56 := by native_decide

/-- **D0-CVFT-F3B.** The baryon spin/flavour multiplet ranks: spin `4`, flavour decuplet `10`,
spin-flavour `40 = 10·4`, full SU(6) `56`, and `56 − 40 = 16` (the octet sector). -/
theorem baryon_spin_flavour_ranks :
    Fintype.card (SortedTripleN 2) = 4 ∧
    Fintype.card (SortedTripleN 3) = 10 ∧
    Fintype.card (SortedTripleN 6) = 56 ∧
    (10 * 4 = 40) ∧ (56 - 40 = 16) :=
  ⟨spin_sorted_card, flavour_sorted_card, six_sorted_card, by norm_num, by norm_num⟩

end D0.Matter
