namespace D0.Bridge

namespace BridgeAssumption

/-- External owner: complex quantum mechanics is NOT optional — real-vector-space QM is ruled
out experimentally. Renou et al., *Nature* 600, 625 (2021) (theory); Chen et al., *Phys. Rev.
Lett.* 128, 040403 (43σ violation of the real-number bound); Li et al. (5.30σ, strict
locality). In the D0 lens this owns the genuine imaginary/complex structure D0 carries (the
toral `det = -1`, the `i` in the phase quotient): the complex unit is forced, not chosen. -/
structure ComplexQMNecessity where
  /-- D0-side anchor: D0 carries a genuine complex/imaginary structure (not real-only). -/
  d0ComplexStructure : Prop
  /-- External: real-vector-space QM is experimentally excluded (complex QM necessary). -/
  realQMRuledOut : Prop
  d0Witness : d0ComplexStructure
  cited : realQMRuledOut

end BridgeAssumption

abbrev ComplexQMNecessity := BridgeAssumption.ComplexQMNecessity

/-- Conditional bridge: given D0's complex structure and the experimental exclusion of
real-number QM (assumed), the complex unit is forced. Proved only relative to
`ASSUMP-COMPLEX-QM`. NAMED GAP: the experiments assume the standard QM postulates (2025
critique), so the forcing is conditional on that framework. -/
theorem complex_qm_conditional (h : ComplexQMNecessity) :
    h.d0ComplexStructure ∧ h.realQMRuledOut :=
  ⟨h.d0Witness, h.cited⟩

end D0.Bridge
