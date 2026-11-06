# Local moved-D roots and finite specialization

The positive moved-D left and right Julia roots have explicit local algebra representatives whose images agree with the previously verified complex roots and with both explicit modular matrices. Equality of the modular matrices with the source Lagrange implementation remains open.

A generic theorem proves that a nonzero determinant after a ring specialization, with an injective embedding of the same coefficient ring into an integral domain, gives independent mapped rows. The nonzero specialized determinant is a premise, not yet established for the 128 source histories. Source coefficients, word evaluation, the fixed witness determinant and its independently checked certificate remain open. No map from complex numbers into a finite field is claimed.

Narrow Lean checks used an existing dependency cache and independent read-only reviews found no defects. The generic theorem axiom diagnostics reported `propext`, `Classical.choice`, `Quot.sound`; diagnostic print directives are omitted from the published module. For the moved-D module the checked blob `5b65f3156d8a7ddc9d0994a07d9696439ee07d95` differs from the committed source only by trailing blank-line removal. Provenance-guarded final integration is not yet complete. Physical admission remains open; owner #334 and `GR_closed=false` are unchanged.
