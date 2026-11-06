# Compiled moving-projector declarations — 4 November 2026

The inventory was extracted from the compiled public import `D0.All` at clean
snapshot `56f095dcdbb9eef66a002d612ed45727e58f481c` using Lean 4.30.0. It contains eight exact declarations
from `MovingProjectorBookPrice`, `MovingProjectorBookPriceDensityBridge`, and
`MovingProjectorVariableParameters`; each has its elaborated type, binders, normalized
conclusion, source range, type/proof dependencies, and axiom closure in
[`lean_declaration_inventory.json`](lean_declaration_inventory.json).

The original fixed-parameter result is the derivative of the unchanged finite Book03
heat-plus-log-determinant price. Its thermal source is
`−Re Tr(ρ (dΔ − [K,Δ]))`, and its feedback source is
`2z Re Tr(R C† Q (dU − [K,U]) P)`, with `K=[dP,P]`, `C=QUP`,
`R=(I−z C†C)⁻¹`, `Q=I−P`. The statement retains differentiability of all three curves,
Hermiticity of `Δ` at the evaluation point, local idempotence/self-adjointness of `P`,
`β ≠ 0`, and the determinant slit-plane chart. The isometric-cut specialization derives
the needed chart from `0 ≤ z < 1` and `U†U=I`.

The variable-parameter theorem also varies `β` and `z`: it adds the exact `β'` heat
coefficient `−log Z/β² − Re Tr(ρΔ)/β` and the `z'` coefficient
`Re Tr(R C†C)`. Those are proved as components of the same price derivative.

The trust footprint for all eight declarations is exactly
`Classical.choice`, `Quot.sound`, and `propext`; no axiom-free result is claimed. Existing
`formal_support.csv` rows locate the three modules. The exact-name inventory emits no
claim-ID crosswalk, so this checkpoint does not attach a claim or assembly application
without an owned matching statement. It remains finite matrix analysis and does not
select physical price/admission or close `GR_closed`.

Lean source digest: `deb9e9f8d99b486bd1e1a36e2da8c8f79732ba4cc79635348ae617cfee6eb073`. Collector SHA-256:
`eaca24662aaac57575c8ca9d1071f8e3df07039f50b02d57fa945cf1fa6d430b`. Full source pins and inventory hash are in
[`replay_manifest.json`](replay_manifest.json).
