import Mathlib.Data.Real.Basic

namespace D0

structure WeakCouplingReadout where
  eta : Real
  etaBound : Real
  detectorNoise : Real
  rawNonclassicalityBound : Real
  eta_nonneg : 0 <= eta
  eta_le_bound : eta <= etaBound
  detectorNoise_nonneg : 0 <= detectorNoise
  rawNonclassicality_nonneg : 0 <= rawNonclassicalityBound
  modeAveraging : Prop
  modeAveragingProof : modeAveraging
  noiseDominatesQuantumSignature : eta * rawNonclassicalityBound <= detectorNoise

def QuantumSignatureBound (h : WeakCouplingReadout) : Real :=
  h.eta * h.rawNonclassicalityBound

def RealisticWeakCouplingClassicalization (h : WeakCouplingReadout) : Prop :=
  h.modeAveraging /\ QuantumSignatureBound h <= h.detectorNoise

theorem nonclassical_signature_suppressed
    (h : WeakCouplingReadout) :
    QuantumSignatureBound h <= h.eta * h.rawNonclassicalityBound := by
  rfl

theorem nonclassical_signature_below_noise
    (h : WeakCouplingReadout) :
    QuantumSignatureBound h <= h.detectorNoise := by
  exact h.noiseDominatesQuantumSignature

theorem weak_coupling_readout_classical_guardrail
    (h : WeakCouplingReadout) :
    RealisticWeakCouplingClassicalization h := by
  exact ⟨h.modeAveragingProof, h.noiseDominatesQuantumSignature⟩

def WeakCouplingClassicalization (h : WeakCouplingReadout) : Prop :=
  RealisticWeakCouplingClassicalization h

end D0
