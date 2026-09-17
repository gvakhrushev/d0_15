import D0.SelfReading.RawSceneGraph
import Mathlib.Tactic

/-!
# D0-SELF-READING-NO-STIPULATION-001 — provenance firewall

The forced outputs are NOT literals. `commutantDim` is DEFINED as the cardinality of the image of `pairClass`
over all index pairs (the raw `Aut` pair-orbit count) — `commutant_is_pair_orbit_count` is `rfl` — and is
proven `= 12` by `native_decide`. Likewise `2|E|` and `trace(A²)` are raw sums over the concrete adjacency.
This is the provenance chain raw-object → raw-map → derived-construction → output-theorem, replacing the prior
hand-written isotypic list.
-/

namespace D0.SelfReading.SelfReadingNoStipulation

open D0.SelfReading.RawSceneGraph

/-- The commutant dimension is the pair-orbit count BY DEFINITION (not a literal). -/
theorem commutant_is_pair_orbit_count :
    commutantDim = (Finset.univ.image pairClass).card := rfl

/-- **No stipulation.** Each forced output is a raw computation on the concrete `K(9,11,13)` object:
commutant 12 = pair-orbit count, `2|E| = 718`, `trace(A²) = 718` — all `native_decide` derived. -/
theorem no_stipulation_forced_outputs :
    commutantDim = 12 ∧ commutantDim = (Finset.univ.image pairClass).card ∧
      (∑ i : Fin 33, degree i) = 718 ∧
      (∑ i : Fin 33, ∑ k : Fin 33, Aadj i k * Aadj k i) = 718 :=
  ⟨commutant_dim_raw, rfl, two_edges, trace_A_sq⟩

end D0.SelfReading.SelfReadingNoStipulation
