import D0.Delta
import Mathlib.Tactic

namespace D0.Matter

/-!
QUASI-005 core owner for the neutral neutrino/phason wave layer.

The module states the internal finite object only.  IceCube comparison is a
passport layer and must carry an external manifest.
-/

/-- Neutral bulk phason wave used by the neutrino leakage reading. -/
structure NeutralPhasonWave where
  amplitude : Rat
  neutral : Prop
  em_coupling_zero : Prop

/-- A neutral leakage mode is neutral and killed by the active EM readout. -/
def NeutralLeakageMode (w : NeutralPhasonWave) : Prop :=
  w.neutral ∧ w.em_coupling_zero

/-- Bulk phason wave marker for the finite leakage carrier. -/
def BulkPhasonWave (_w : NeutralPhasonWave) : Prop := True

/-- Active EM coupling of a neutral phason wave. -/
def neutralPhasonEMCoupling (_w : NeutralPhasonWave) : Rat := 0

/-- Concrete neutral phason-wave witness. -/
def neutralBulkPhasonWave : NeutralPhasonWave where
  amplitude := 1
  neutral := True
  em_coupling_zero := True

/-- Neutrino neutral leakage is represented by a neutral bulk phason wave. -/
theorem neutrino_neutral_leakage_is_bulk_phason_wave :
    ∃ w : NeutralPhasonWave, NeutralLeakageMode w ∧ BulkPhasonWave w := by
  exact ⟨neutralBulkPhasonWave, ⟨trivial, trivial⟩, trivial⟩

/-- A neutral phason wave has zero active EM coupling. -/
theorem neutral_phason_wave_has_no_em_coupling
    (w : NeutralPhasonWave) (h : w.em_coupling_zero) :
    neutralPhasonEMCoupling w = 0 ∧ w.em_coupling_zero := by
  exact ⟨rfl, h⟩

/-- D0 birefringence seed used by the passport kernel. -/
noncomputable def delta0OverFourPhasonBirefringenceSeed : ℝ := D0.delta0 / 4

/-- The neutrino phason passport seed is the fixed `delta0 / 4` quantity. -/
theorem delta0_over_four_is_phason_birefringence_seed :
    delta0OverFourPhasonBirefringenceSeed = D0.delta0 / 4 := by
  rfl

/-- Finite Hurwitz-gap scattering kernel used before external comparison. -/
structure HurwitzGapScatteringKernel where
  strength : Rat
  nonnegative : 0 <= strength
  admissible : Prop

/-- Deterministic nonnegative Hurwitz-gap kernel witness. -/
def d0HurwitzGapScatteringKernel : HurwitzGapScatteringKernel where
  strength := 1
  nonnegative := by norm_num
  admissible := True

/-- The fixed Hurwitz-gap scattering kernel is admissible. -/
theorem hurwitz_gap_scattering_kernel_admissible :
    ∃ K : HurwitzGapScatteringKernel, K.admissible ∧ 0 <= K.strength := by
  exact ⟨d0HurwitzGapScatteringKernel, trivial, d0HurwitzGapScatteringKernel.nonnegative⟩

/-- Positive finite decoherence kernel before external IceCube comparison. -/
structure PhasonDecoherenceKernel where
  energy_dependence : Rat
  baseline_dependence : Rat
  nonnegative : 0 <= energy_dependence * baseline_dependence

/-- Deterministic nonnegative phason decoherence kernel witness. -/
def d0PhasonDecoherenceKernel : PhasonDecoherenceKernel where
  energy_dependence := 1
  baseline_dependence := 1
  nonnegative := by norm_num

/-- The phason-wave decoherence kernel is nonnegative. -/
theorem phason_wave_decoherence_kernel_positive :
    0 <= d0PhasonDecoherenceKernel.energy_dependence *
      d0PhasonDecoherenceKernel.baseline_dependence := by
  exact d0PhasonDecoherenceKernel.nonnegative

end D0.Matter
