import D0.Representation.GoldenRelativeChannel

/-!
# Golden contrast is transferred into joint correlations by reversible recording

An internal blank record is coupled by the existing basis CNOT after the golden gate.
The full four-dimensional operator is orthogonal. In Bloch coordinates, the locally
retained contrast and two joint correlations preserve the complete squared Bloch length.
This is a finite apparatus theorem with explicit gate, blank preparation and readouts.
It does not identify the record with cosmological dark matter or derive those resources from M1.
-/
namespace D0.Representation.GoldenCoherentMemory

open Matrix D0.Representation.GoldenRelativeChannel

/-- Basis order: system/record = 00,01,10,11. Golden gate then controlled recording. -/
def fullStep (a p : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![a,0,-p,0; 0,a,0,-p; 0,p,0,a; p,0,a,0]

theorem fullStep_orthogonal (a p : ℝ) (ha : a^2 = p) (hp : p+p^2=1) :
    (fullStep a p).transpose * fullStep a p = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [fullStep, Matrix.mul_apply, Fin.sum_univ_succ] <;> nlinarith

/-- A blank record is retained in the joint state, rather than discarded. -/
theorem blank_record_evolution (a p u v : ℝ) :
    (fullStep a p).mulVec ![u,0,v,0] = ![a*u-p*v,0,0,p*u+a*v] := by
  ext i
  fin_cases i <;>
    simp [fullStep, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

def contrastCoefficient (p : ℝ) : ℝ := p-p^2
def correlationCoefficient (a p : ℝ) : ℝ := 2*a*p

def retainedContrast (a p x z : ℝ) : ℝ :=
  contrastCoefficient p*z - correlationCoefficient a p*x
def jointX (a p x z : ℝ) : ℝ :=
  correlationCoefficient a p*z + contrastCoefficient p*x

theorem coefficients_close (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (contrastCoefficient p)^2 + (correlationCoefficient a p)^2 = 1 := by
  unfold contrastCoefficient correlationCoefficient
  nlinarith [congrArg (fun t : ℝ => 4*t*p^2) ha,
    congrArg (fun t : ℝ => t^2) hp]

/-- Local Z, joint X⊗X, and joint Y⊗X are the complete input Bloch coordinates
after a rotation. The imaginary coherence y is carried by the third readout. -/
theorem complete_correlation_balance (a p x y z : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    (retainedContrast a p x z)^2 + (jointX a p x z)^2 + y^2 =
      x^2+y^2+z^2 := by
  have hc := coefficients_close a p ha hp
  unfold retainedContrast jointX
  nlinarith [congrArg (fun t : ℝ => t*x^2) hc,
    congrArg (fun t : ℝ => t*z^2) hc]

theorem golden_transfer_weights (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (contrastCoefficient p)^2 = 4*(delta p)^2 ∧
    (correlationCoefficient a p)^2 = 8*delta p := by
  constructor
  · unfold contrastCoefficient delta
    ring
  · have hd := twice_delta p hp
    unfold correlationCoefficient
    nlinarith [congrArg (fun t : ℝ => t*p^2) ha]

/-- For diagonal inputs, the visible and joint contributions have no free allocation parameter. -/
theorem diagonal_information_split (a p z : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (retainedContrast a p 0 z)^2 = 4*(delta p)^2*z^2 ∧
    (jointX a p 0 z)^2 = 8*delta p*z^2 := by
  have h := golden_transfer_weights a p ha hp
  simp only [retainedContrast, jointX, mul_zero, sub_zero, add_zero, mul_pow]
  exact ⟨congrArg (fun t : ℝ => t*z^2) h.1,
    congrArg (fun t : ℝ => t*z^2) h.2⟩

/-- The original coherent input is reconstructed from joint readouts, including y. -/
theorem joint_readouts_reconstruct (a p x z : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) :
    contrastCoefficient p*jointX a p x z -
        correlationCoefficient a p*retainedContrast a p x z = x ∧
    correlationCoefficient a p*jointX a p x z +
        contrastCoefficient p*retainedContrast a p x z = z := by
  have hc := coefficients_close a p ha hp
  unfold jointX retainedContrast
  constructor <;> nlinarith [congrArg (fun t : ℝ => t*x) hc,
    congrArg (fun t : ℝ => t*z) hc]


/-! ## Genuine literal Golden readout: what is and is not redundant

This uses the EXISTING Fin4 fullStep's already proved Bloch-correlation
identities, not a guessed Q8 action or a new quantum gate.  The
locally-visible Z contrast by itself is NOT faithful to the original
Bloch input.  The EXISTING joint X⊗X and Y⊗X records restore the
missing information.  It is MDL-unsound to throw them away when the
joint Golden memory test is among admissible comparisons.

The two witness LINES in M1 are not the three different Bloch
readout COMPONENTS; a line may compare a complete vector signature.
-/

/-- Entire exact three-real-coordinate original Golden retained-readout
signature: local Z, joint X⊗X, joint Y⊗X.  The third component records
the existing imaginary coherence y, not a new third witness line. -/
def goldenBlochSignature (a p x y z : ℝ) : ℝ × ℝ × ℝ :=
  (retainedContrast a p x z, jointX a p x z, y)

/-- The actual joint original Golden signature is faithful to its
entire (x,y,z) Bloch source, without introducing an external detector
family, provided the Golden gate satisfies its existing identity. -/
theorem golden_complete_bloch_readout_injective (a p : ℝ)
    (ha : a^2 = p) (hp : p+p^2=1)
    (x y z x' y' z' : ℝ)
    (h : goldenBlochSignature a p x y z =
         goldenBlochSignature a p x' y' z') :
    x = x' ∧ y = y' ∧ z = z' := by
  have hr : retainedContrast a p x z =
      retainedContrast a p x' z' := congrArg Prod.fst h
  have hj : jointX a p x z = jointX a p x' z' :=
    congrArg (fun q : ℝ × ℝ × ℝ => q.2.1) h
  have hy : y = y' :=
    congrArg (fun q : ℝ × ℝ × ℝ => q.2.2) h
  have hx0 := (joint_readouts_reconstruct a p x z ha hp).1
  have hx1 := (joint_readouts_reconstruct a p x' z' ha hp).1
  have hz0 := (joint_readouts_reconstruct a p x z ha hp).2
  have hz1 := (joint_readouts_reconstruct a p x' z' ha hp).2
  constructor
  · calc
      x = contrastCoefficient p * jointX a p x z -
          correlationCoefficient a p * retainedContrast a p x z := hx0.symm
      _ = contrastCoefficient p * jointX a p x' z' -
          correlationCoefficient a p * retainedContrast a p x' z' := by rw [hj, hr]
      _ = x' := hx1
  constructor
  · exact hy
  · calc
      z = correlationCoefficient a p * jointX a p x z +
          contrastCoefficient p * retainedContrast a p x z := hz0.symm
      _ = correlationCoefficient a p * jointX a p x' z' +
          contrastCoefficient p * retainedContrast a p x' z' := by rw [hj, hr]
      _ = z' := hz1

/-- A genuine ORIGINAL-channel counterexample: the pure Bloch direction
(x,z)=(c,s), c=p-p², s=2ap, is completely invisible in the visible
local-Z output relative to zero Bloch source, but differs in the
already-owned recorded joint X⊗X correlation by exactly ONE. -/
theorem golden_local_channel_hides_exact_joint_distinction (a p : ℝ)
    (ha : a^2 = p) (hp : p+p^2=1) :
    retainedContrast a p (contrastCoefficient p)
       (correlationCoefficient a p) =
       retainedContrast a p 0 0 ∧
    jointX a p (contrastCoefficient p)
       (correlationCoefficient a p) = 1 ∧
    jointX a p 0 0 = 0 := by
  have hc := coefficients_close a p ha hp
  constructor
  · unfold retainedContrast
    ring
  constructor
  · unfold jointX
    nlinarith
  · simp [jointX]


end D0.Representation.GoldenCoherentMemory
