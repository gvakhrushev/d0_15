namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the Connes reconstruction theorem (A. Connes, *On the spectral
characterization of manifolds*, arXiv:0810.2088, 2008; conjectured 1996). The classical
theorem: a commutative real spectral triple `(A,H,D)` satisfying the axioms (regularity,
dimension, order-one, orientability, finiteness, Poincaré duality) is canonically isomorphic
to the spectral triple `(C^∞(M), L²(M,S), D̸)` of a compact oriented Riemannian spin manifold,
and the metric is recovered by the Connes distance `d(x,y)=sup{|f(x)-f(y)| : ‖[D,f]‖≤1}` —
i.e. "metric = spectrum of the Dirac operator", a bijection. This owns the gravity-geometry
link of D0 (BOOK_07 §07.33/§07.51): the rank-3=causal-cone / Connes-distance identification of
`D0-COMPACTNESS-LIMIT-001` stays a NAMED GAP whose external owner is this theorem. -/
structure ConnesReconstruction where
  /-- D0-side anchor: D0 carries a finite (commutative) spectral triple. -/
  d0FiniteSpectralTriple : Prop
  /-- External: metric = Connes distance from the Dirac spectrum (spectral triple ↔ spin
  manifold bijection). -/
  metricEqualsSpectrum : Prop
  d0Witness : d0FiniteSpectralTriple
  cited : metricEqualsSpectrum

end BridgeAssumption

abbrev ConnesReconstruction := BridgeAssumption.ConnesReconstruction

/-- Conditional bridge: given the D0 finite spectral triple and the Connes reconstruction
theorem (assumed), the metric is determined by the Dirac spectrum. The conclusion is proved
ONLY relative to the declared external assumption (`ASSUMP-CONNES-RECONSTRUCTION`). -/
theorem connes_reconstruction_conditional (h : ConnesReconstruction) :
    h.d0FiniteSpectralTriple ∧ h.metricEqualsSpectrum :=
  ⟨h.d0Witness, h.cited⟩

end D0.Bridge
