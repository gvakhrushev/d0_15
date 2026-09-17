import D0.Representation.GoldenCoherentMemory

/-! Equal final channels need not be equivalent internal processes. The separating intervention
is replacement of the retained system by a prepared zero-bit state; it has an internal reversible
SWAP implementation if the previous system is retained in the auxiliary register. -/
namespace D0.Representation.GoldenProcessContext

open D0.Representation.GoldenCoherentMemory

abbrev Bloch := ℝ × ℝ × ℝ

def channel (a p : ℝ) (r : Bloch) : Bloch :=
  (0, 0, retainedContrast a p r.1 r.2.2)

def preparedZero : Bloch := (0,0,1)

def resetRetained (_ : Bloch) : Bloch := preparedZero

/-- Process A applies the same recorded golden channel before and after intervention. -/
def processA (a p : ℝ) (intervention : Bloch → Bloch) (r : Bloch) : Bloch :=
  channel a p (intervention (channel a p r))

/-- Process B idles before intervention and applies the two-step channel afterwards. -/
def processB (a p : ℝ) (intervention : Bloch → Bloch) (r : Bloch) : Bloch :=
  channel a p (channel a p (intervention r))

theorem same_endpoint_channel (a p : ℝ) :
    processA a p id = processB a p id := rfl

theorem reset_context_readouts (a p : ℝ) (r : Bloch) :
    (processA a p resetRetained r).2.2 = contrastCoefficient p ∧
    (processB a p resetRetained r).2.2 = (contrastCoefficient p)^2 := by
  simp [processA, processB, resetRetained, preparedZero, channel, retainedContrast]
  ring

theorem golden_contrast_strict (p : ℝ) (hp : p+p^2=1) (hp0 : 0<p) (hp1 : p<1) :
    0 < contrastCoefficient p ∧ contrastCoefficient p < 1 := by
  have he := D0.Representation.GoldenOrderInterferometer.golden_cube p hp
  constructor
  · change 0 < p-p^2
    rw [he]
    positivity
  · unfold contrastCoefficient
    nlinarith [sq_nonneg p]

/-- Closed separating witness: equality of endpoints does not imply operational equivalence. -/
theorem endpoint_equivalence_not_process_equivalence (a p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) (hp1 : p<1) (r : Bloch) :
    processA a p id = processB a p id ∧
    processA a p resetRetained r ≠ processB a p resetRetained r := by
  refine ⟨same_endpoint_channel a p, ?_⟩
  intro h
  have hc := golden_contrast_strict p hp hp0 hp1
  have hr := reset_context_readouts a p r
  have hv := congrArg (fun b : Bloch => b.2.2) h
  dsimp only at hv
  rw [hr.1, hr.2] at hv
  nlinarith

/-- The apparent reset is the retained marginal of a reversible internal exchange. -/
theorem internal_reset_keeps_previous (r : Bloch) :
    Equiv.prodComm Bloch Bloch (r,preparedZero) = (preparedZero,r) := rfl

end D0.Representation.GoldenProcessContext
