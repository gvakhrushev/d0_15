import D0.Representation.GoldenCoherentMemory
import D0.Foundation.EmpiricalTheoryFactorization

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


/-! ## Typed connection to the canonical future-MDL quotient

Use ONLY the already formalized Golden reduced process A/B, the
already formalized internal reset intervention and their current
local Z readout. No Q8, spinor states or new continuous controls.
This is a PROCESS-context comparison, NOT a claim that a native
paid G0 fullStep physically performs the intervention.

The process-order label Bool is hidden at the current observation.
Applying the existing reset context as ONE mathematical intervention
renders it visible. Thus quotienting A/B by equal endpoints loses a
future recorded distinction.
-/

open D0.Foundation.EmpiricalTheoryFactorization

/-- Existing GoldenProcessContext future-test family.
The Boolean action chooses already-defined identity/reset intervention.
The hidden Bool in State labels existing protocol A/B, not a third witness. -/
def goldenContextFutureExecution (a p : ℝ) : FutureExecution where
  State := Bool × Bloch
  Action := Bool
  Test := Unit
  Outcome := ℝ
  step := fun intervene s =>
    (s.1, if s.1
      then processB a p (if intervene then resetRetained else id) s.2
      else processA a p (if intervene then resetRetained else id) s.2)
  observe := fun s _ => s.2.2.2

/-- The two original Golden process-order carriers are indistinguishable
by the CURRENT local Z readout. -/
theorem golden_context_processes_same_now (a p : ℝ) (r : Bloch) :
    (goldenContextFutureExecution a p).observe (false,r) () =
    (goldenContextFutureExecution a p).observe (true,r) () := rfl

/-- The SAME original reset context separates present-identical
process histories after ONE mathematical intervention, with
the literal native Golden contrast coefficient p-p². -/
theorem golden_context_processes_different_future (a p : ℝ)
    (hp : p+p^2=1) (hp0 : 0<p) (hp1 : p<1) (r : Bloch) :
    (goldenContextFutureExecution a p).profile (false,r) ≠
      (goldenContextFutureExecution a p).profile (true,r) := by
  intro h
  have hr := reset_context_readouts a p r
  have hc := golden_contrast_strict p hp hp0 hp1
  have hh : (processA a p resetRetained r).2.2 =
      (processB a p resetRetained r).2.2 :=
    congrFun (congrFun h [true]) ()
  rw [hr.1, hr.2] at hh
  have hs : 0 < contrastCoefficient p * (1 - contrastCoefficient p) :=
    mul_pos hc.1 (sub_pos.mpr hc.2)
  nlinarith


end D0.Representation.GoldenProcessContext
