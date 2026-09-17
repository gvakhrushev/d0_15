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

end D0.Representation.GoldenCoherentMemory
