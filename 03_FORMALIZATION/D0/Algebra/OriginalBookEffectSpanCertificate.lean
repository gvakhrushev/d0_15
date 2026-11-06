import D0.Algebra.OriginalBookResidueJuliaPairs
import D0.Algebra.OriginalBookResidueWords

/-! A finite certificate for the complex span of the actual source effects.
The matrix evaluated here uses the two constructed Julia specializations and
the original chronological updates. A checked packed equality can therefore
be combined with a numerical nonvanishing proof without importing a
hypothesis on the complex rank or on individual source operators. -/

open Matrix
open D0.Algebra.OriginalBookResidueJuliaPairs D0.Algebra.OriginalBookResidueWords
open D0.Algebra.OriginalBookLocalEffectWords
open D0.Geometry.OriginalBookEffectSpanUpper

namespace D0.Algebra.OriginalBookEffectSpanCertificate

abbrev FixedPaths := Fin 128 → List (Fin 128)
abbrev FixedCoordinates := Fin 128 → Fin 16 × Fin 16

theorem source_span_of_packed_certificate (paths : FixedPaths) (coord : FixedCoordinates)
    (A : Matrix (Fin 128) (Fin 128) (ZMod 1009))
    (hentries : computedTable (residueRowPair false) (residueRowPair true) paths coord =
      Vector.ofFn (fun i => Vector.ofFn (A i))) (hdet : A.det ≠ 0) :
    Module.finrank ℂ sourceEffectSpan = 128 ∧ sourceEffectSpan = evenSubmodule := by
  have htable := computedRows_eq_of_table _ _ paths coord A hentries
  rw [computedRows_eq_residueRows _ _ localRowPair_mod_plus localRowPair_mod_minus] at htable
  have hdim := sourceEffectSpan_finrank_of_residue_det paths coord (by rwa [htable])
  exact ⟨hdim, Submodule.eq_of_le_of_finrank_le sourceEffectSpan_le_even
    (hdim ▸ evenSubmodule_finrank_le)⟩

end D0.Algebra.OriginalBookEffectSpanCertificate
