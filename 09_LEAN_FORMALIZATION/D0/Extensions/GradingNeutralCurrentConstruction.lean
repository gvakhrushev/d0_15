import D0.Extensions.RawCommutantWedderburn
import D0.Extensions.RepresentationReadoutExtension
import Mathlib.Tactic

/-!
# D0-GRADING-NEUTRAL-CURRENT-001 — Lane G terminal (G2)

On the DERIVED `M₃` block (`RawCommutantWedderburn`: block dim `9 = 3²`), a `ℤ₂`-grading has signature
`(p,q)` with `p+q = 3`; the grading-even neutral-current count is `nc(p,q) = p²+q²+3`. Two admissible
signatures give `nc(2,1)=8 ≠ nc(3,0)=12`, both anomaly-free and `S₃`-symmetric — terminal **G2**
(two-completion). `N_active` is NOT read from rank: it is the grading-dependent count, hence not forced.
-/

namespace D0.Extensions.GradingNeutralCurrentConstruction

open D0.Extensions.RawCommutantWedderburn D0.Extensions.RepresentationReadoutExtension

/-- The grading lives on the derived `M₃` block (dim `9 = 3²`, from the diagonal-class count). -/
theorem grading_on_derived_M3 : blockDims.head! = diagonalClasses ^ 2 ∧ diagonalClasses = 3 :=
  ⟨M3_block_from_diagonal, diagonal_classes_three⟩

/-- **Terminal G2.** Two admissible grading signatures give divergent neutral-current counts `8 ≠ 12`; the
active-channel content is grading-dependent, not a rank fact. -/
theorem grading_neutral_current_G2 :
    ncCount 2 1 = 8 ∧ ncCount 3 0 = 12 ∧ ncCount 2 1 ≠ ncCount 3 0 ∧ blockDims.head! = 9 :=
  ⟨nc_signature_21, nc_signature_30, nc_divergent, by decide⟩

end D0.Extensions.GradingNeutralCurrentConstruction
