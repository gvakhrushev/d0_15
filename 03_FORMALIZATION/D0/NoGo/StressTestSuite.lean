import D0.Matter.PhasonStrainGenerations
import D0.Bridge.TickGaugeLorentz

namespace D0.NoGo

/-!
Integrated negative-control suite.

These are not new positive closure claims.  The module collects already owned
no-go boundaries and one finite isolated-phason control so risky shortcuts can
be checked as one fast slice.

Scope note (2026-06-15 build-hygiene): the rank-one Higgs scalar-projector no-go was temporarily
removed from the Lean suite — its `FiniteScalarProjector` / `GaugeCompatible` API was never
formalized (reference-only since base-v14). It is now **formalized below** (Iter-15): a scalar
projector on the SU(2) doublet index is a kept-component mask, and a rank-one mask cannot commute
with the weak swap, so it is not gauge-compatible. All four controls are Lean-proved.
-/

/-! ### Rank-one Higgs scalar-projector no-go

A finite scalar projector on the SU(2) doublet index `Fin 2` is the mask of components it keeps.
The weak/gauge generator is the doublet swap. A projector is gauge-compatible iff it commutes with
the swap. A rank-one mask keeps one direction and so cannot commute with the swap — the obstruction
to a single-direction Higgs/scalar projector. (Finite model of cert `vp_no_go_stress_test_suite.py`.) -/

/-- SU(2) doublet index. -/
abbrev DoubletIndex := Fin 2

/-- A finite scalar projector = the mask of kept doublet components. -/
abbrev FiniteScalarProjector := Bool × Bool

/-- Rank = number of kept components. -/
def projectorRank (m : FiniteScalarProjector) : Nat := (if m.1 then 1 else 0) + (if m.2 then 1 else 0)

/-- Does the projector keep direction `x`? -/
def keeps (m : FiniteScalarProjector) (x : DoubletIndex) : Bool := if x = 0 then m.1 else m.2

/-- Project `x`: keep it (`some x`) or drop it (`none`). -/
def project (m : FiniteScalarProjector) (x : DoubletIndex) : Option DoubletIndex :=
  if keeps m x then some x else none

/-- The weak/gauge generator: the doublet swap. -/
def weakSwap (x : DoubletIndex) : DoubletIndex := if x = 0 then 1 else 0

/-- Gauge-compatible iff the projector commutes with the weak swap on every direction. -/
def GaugeCompatible (m : FiniteScalarProjector) : Bool :=
  (List.finRange 2).all (fun x => project m (weakSwap x) == (project m x).map weakSwap)

/-- **Rank-one Higgs scalar-projector no-go.** No rank-one scalar projector is gauge-compatible:
selecting a single SU(2) doublet direction cannot commute with the weak swap. -/
theorem no_go_rank_one_higgs_scalar_projector :
    ∀ m : FiniteScalarProjector, projectorRank m = 1 → GaugeCompatible m = false := by decide

/-- Negative control: the full rank-two doublet projector IS gauge-compatible. -/
theorem rank_two_full_doublet_gauge_compatible : GaugeCompatible (true, true) = true := by decide

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
  rank_one_scalar_projector :
    forall m : FiniteScalarProjector, projectorRank m = 1 → GaugeCompatible m = false

/-- Machine-checkable no-go stress suite. -/
def noGoStressTestSuite : NoGoStressTestSuite where
  isolated_generation := no_go_isolated_phason_generation_carrier
  isolated_baryon_s3 := no_go_isolated_phason_baryon_s3_sector
  euclidean_signature := no_go_euclidean_signature_export
  rank_one_scalar_projector := no_go_rank_one_higgs_scalar_projector

/-- The finite no-go stress suite closes the four Lean-backed negative controls:
isolated-phason generation, isolated-phason baryon S3 sector, Euclidean signature export, and the
rank-one Higgs scalar-projector obstruction. -/
theorem no_go_stress_test_suite_closed :
    Fintype.card IsolatedPhasonMode ≠
      Fintype.card D0.Matter.GenerationPhasonMode ∧
    Fintype.card IsolatedPhasonTriple ≠
      Fintype.card D0.Matter.BaryonPhasonSymmetricSector ∧
    (forall _C : D0.Bridge.FiniteLorentzTickGaugeClosure,
      D0.roleSignature ≠ (4, 0)) ∧
    (forall m : FiniteScalarProjector, projectorRank m = 1 → GaugeCompatible m = false) := by
  exact
    ⟨noGoStressTestSuite.isolated_generation,
      noGoStressTestSuite.isolated_baryon_s3,
      noGoStressTestSuite.euclidean_signature,
      noGoStressTestSuite.rank_one_scalar_projector⟩

end D0.NoGo
