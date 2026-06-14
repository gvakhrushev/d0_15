import D0.Matter.PhasonStrainGenerations
import D0.Bridge.TickGaugeLorentz

namespace D0.NoGo

/-!
Integrated negative-control suite.

These are not new positive closure claims.  The module collects already owned
no-go boundaries and one finite isolated-phason control so risky shortcuts can
be checked as one fast slice.

Scope note (2026-06-15 build-hygiene): the rank-one Higgs scalar-projector no-go
was removed from the Lean suite — its `FiniteScalarProjector` / `GaugeCompatible`
API was never formalized (reference-only since base-v14, never compiled). That
control stays covered by the Python cert `vp_no_go_stress_test_suite.py` and is an
open Lean theorem-target. The three controls below are Lean-proved.
-/

/-- One isolated phason mode, used only as a negative control. -/
abbrev IsolatedPhasonMode := Fin 1

/-- The isolated-phason control has one mode, not the D0 three-mode carrier. -/
theorem isolated_phason_mode_card_eq_one :
    Fintype.card IsolatedPhasonMode = 1 := by
  simp [IsolatedPhasonMode]

/-- Ordered triple over one isolated mode. -/
abbrev IsolatedPhasonTriple : Type :=
  Prod IsolatedPhasonMode (Prod IsolatedPhasonMode IsolatedPhasonMode)

/-- The isolated-phason ordered triple remains one-dimensional. -/
theorem isolated_phason_triple_card_eq_one :
    Fintype.card IsolatedPhasonTriple = 1 := by
  simp [IsolatedPhasonTriple, IsolatedPhasonMode]

/-- A single isolated phason cannot replace the three generation/phason modes. -/
theorem no_go_isolated_phason_generation_carrier :
    Fintype.card IsolatedPhasonMode ≠
      Fintype.card D0.Matter.GenerationPhasonMode := by
  rw [isolated_phason_mode_card_eq_one,
    D0.Matter.generation_phason_mode_card_eq_three]
  norm_num

/-- A single isolated phason cannot replace the S3 baryon symmetric sector. -/
theorem no_go_isolated_phason_baryon_s3_sector :
    Fintype.card IsolatedPhasonTriple ≠
      Fintype.card D0.Matter.BaryonPhasonSymmetricSector := by
  rw [isolated_phason_triple_card_eq_one,
    D0.Matter.baryon_phason_symmetric_sector_dim_eq_ten]
  norm_num

/-- Stable suite-facing name for the Euclidean signature export no-go. -/
theorem no_go_euclidean_signature_export
    (C : D0.Bridge.FiniteLorentzTickGaugeClosure) :
    D0.roleSignature ≠ (4, 0) := by
  exact D0.Bridge.finite_lorentz_tick_gauge_no_euclidean_export C

/-- Combined finite negative-control package. -/
structure NoGoStressTestSuite where
  isolated_generation :
    Fintype.card IsolatedPhasonMode ≠
      Fintype.card D0.Matter.GenerationPhasonMode
  isolated_baryon_s3 :
    Fintype.card IsolatedPhasonTriple ≠
      Fintype.card D0.Matter.BaryonPhasonSymmetricSector
  euclidean_signature :
    forall _C : D0.Bridge.FiniteLorentzTickGaugeClosure,
      D0.roleSignature ≠ (4, 0)

/-- Machine-checkable no-go stress suite. -/
def noGoStressTestSuite : NoGoStressTestSuite where
  isolated_generation := no_go_isolated_phason_generation_carrier
  isolated_baryon_s3 := no_go_isolated_phason_baryon_s3_sector
  euclidean_signature := no_go_euclidean_signature_export

/-- The finite no-go stress suite closes the three Lean-backed negative controls:
isolated-phason generation, isolated-phason baryon S3 sector, and Euclidean
signature export. (The rank-one Higgs scalar-projector control is cert-level only;
see the scope note above.) -/
theorem no_go_stress_test_suite_closed :
    Fintype.card IsolatedPhasonMode ≠
      Fintype.card D0.Matter.GenerationPhasonMode ∧
    Fintype.card IsolatedPhasonTriple ≠
      Fintype.card D0.Matter.BaryonPhasonSymmetricSector ∧
    (forall _C : D0.Bridge.FiniteLorentzTickGaugeClosure,
      D0.roleSignature ≠ (4, 0)) := by
  exact
    ⟨noGoStressTestSuite.isolated_generation,
      noGoStressTestSuite.isolated_baryon_s3,
      noGoStressTestSuite.euclidean_signature⟩

end D0.NoGo
