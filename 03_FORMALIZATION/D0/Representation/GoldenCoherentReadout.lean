import D0.Representation.GoldenCoherentMemory

/-! Native #334 extension extracted without changing the accepted base owner.
Original declarations: `03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean` at
`07f2f2b15b7050a612d0075aa73db8dc46087a95`.
The shared definitions are imported from their maintained main modules. -/

namespace D0.Representation.GoldenCoherentMemory

open Matrix D0.Representation.GoldenRelativeChannel

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
