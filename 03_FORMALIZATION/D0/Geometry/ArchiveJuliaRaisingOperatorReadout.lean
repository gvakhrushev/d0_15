import D0.Geometry.A4DNilpotentAffineMatterLift

/-!
# Julia raising query: exact vacuum readout on the finite carrier

This is a model-level application of Eq. (26) in the source pinned at
`02_REGISTRY/research/D0_GR_PRIMARY_POSITIVE_CASE.md` and recorded in PR #334,
commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, file
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`.
The exact consumer is §5.1 of
`02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`.

On the existing 16-state exterior carrier, the frame lift fixes the vacuum and
creation from the vacuum is the exterior generator `ι u`. Applying `ιInv`
therefore recovers `u` exactly. Equality of the complete query operators
implies equality of their shifts, for arbitrary linear frame equivalences.

The proved statement covers only this finite-carrier vacuum readout. It does
not formalize the full Lorentz null inverse (28), its all-jet extension,
coframe/metric recovery, the complete variational pullback, source or price
maps, physical admission, or GR selection.
-/

namespace D0.Geometry

open D0
open ExteriorAlgebra

noncomputable section

/-- Finite-carrier realization of the raising query `C†(u) ρ(M)`. -/
def archiveJuliaRaisingQuery (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) :=
  (archiveExteriorCreatorLM u).comp (archiveExteriorFrameLift M)

/-- Read the degree-one vector from a finite-carrier state. -/
def archiveJuliaVacuumVectorReadout (ψ : ArchiveFockState → ℝ) : RoleSpace :=
  ιInv (archiveFockExteriorEquiv ψ)

/-- The frame lift leaves the vacuum fixed before creation acts. -/
theorem archiveJuliaRaisingQuery_on_vacuum (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)) =
      archiveExteriorCreator u (Pi.single fockVacuumState (1 : ℝ)) := by
  change archiveExteriorCreator u
      (archiveExteriorFrameLift M (Pi.single fockVacuumState (1 : ℝ))) = _
  rw [archiveExteriorFrameLift_vacuum]

/-- Exact model form of the vacuum identity `X |0⟩ = C(u) |0⟩` in Eq. (26). -/
theorem archiveJuliaRaisingQuery_vacuum_exterior (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveFockExteriorEquiv
        (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) =
      ι ℝ u := by
  rw [archiveJuliaRaisingQuery_on_vacuum]
  exact archiveExteriorCreator_on_vacuum_eq_ι u

/-- The exact vector readout of the query's vacuum response is its shift. -/
theorem archiveJuliaVacuumVectorReadout_query (u : RoleSpace)
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveJuliaVacuumVectorReadout
        (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) = u := by
  change ιInv (archiveFockExteriorEquiv
    (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ)))) = u
  rw [archiveJuliaRaisingQuery_vacuum_exterior]
  exact ExteriorAlgebra.ι_leftInverse u

/-- The complete query operator determines its shift on the finite carrier. -/
theorem archiveJuliaRaisingQuery_shift_injective
    (u v : RoleSpace) (M N : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (h : archiveJuliaRaisingQuery u M = archiveJuliaRaisingQuery v N) :
    u = v := by
  calc
    u = archiveJuliaVacuumVectorReadout
        (archiveJuliaRaisingQuery u M (Pi.single fockVacuumState (1 : ℝ))) :=
          (archiveJuliaVacuumVectorReadout_query u M).symm
    _ = archiveJuliaVacuumVectorReadout
        (archiveJuliaRaisingQuery v N (Pi.single fockVacuumState (1 : ℝ))) := by
          rw [h]
    _ = v := archiveJuliaVacuumVectorReadout_query v N

end

end D0.Geometry
