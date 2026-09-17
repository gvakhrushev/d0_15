namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of `M1` itself: the operational reconstruction theorems of quantum theory.
A finite information capacity of an elementary system + continuous reversible dynamics +
tomographic locality uniquely yield the complex Hilbert-space structure of QM (Hardy
arXiv:quant-ph/0101012; Dakić–Brukner 2011; Masanes–Müller, *New J. Phys.* 13, 053040, 2011;
Chiribella–D'Ariano–Perinotti, *Phys. Rev. A* 84, 012311, 2011). In the D0 lens this is an
external forcing of `M1` itself: the no-external-catalogue law's finite-distinguishability
premise is exactly the "finite information capacity" hypothesis from which QM's structure is
reconstructed — the strongest external support of the D0 axiomatic base. -/
structure M1InfoReconstruction where
  /-- D0-side anchor: `M1` = finite distinguishability capacity of an elementary system. -/
  m1FiniteCapacity : Prop
  /-- External: finite capacity + continuity + tomographic locality ⇒ complex Hilbert QM. -/
  reconstructsComplexQM : Prop
  d0Witness : m1FiniteCapacity
  cited : reconstructsComplexQM

end BridgeAssumption

abbrev M1InfoReconstruction := BridgeAssumption.M1InfoReconstruction

/-- Conditional bridge: given `M1`'s finite-capacity premise and the operational reconstruction
theorems (assumed), QM's complex structure follows. Proved only relative to
`ASSUMP-M1-INFO-RECONSTRUCTION`. This routes the foundational reading "M1 ⇒ QM structure" to a
cited family of classical reconstruction theorems, not a D0-internal derivation. -/
theorem m1_info_reconstruction_conditional (h : M1InfoReconstruction) :
    h.m1FiniteCapacity ∧ h.reconstructsComplexQM :=
  ⟨h.d0Witness, h.cited⟩

end D0.Bridge
