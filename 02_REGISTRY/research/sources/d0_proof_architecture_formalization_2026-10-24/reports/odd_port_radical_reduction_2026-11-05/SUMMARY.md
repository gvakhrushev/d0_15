# Odd-port radical reduction

`D0.Geometry.OriginalBookEffectRadicalReduction` constructs an explicit
reduced operator for each actual source port: the even branch retains its
source formula and the odd branch uses `−2p V` with a positive scalar weight
`p`. For every matrix update, including the odd anchor, and every finite
chronological path, the actual effect equals the reduced effect multiplied by
the product of its port weights. Those weights are strictly positive. Thus,
for any indexed family of paths, complex linear independence of actual effects
is equivalent to independence of the reduced effects. Independence itself is
not assumed or proved.

This cancellation is about Heisenberg effects; the original Kraus operators
and coherent cross-port interference are not identified with reduced ones.
The reduced definitions remove `sqrt(p)` explicitly, while the underlying
source V still carries the analytic/Julia data and the other root q. Membership
in a specific coefficient ring, a faithful embedding into ℂ and transfer of a
finite-field minor remain to be proved. In particular eight modular checks do
not themselves establish the complex lower bound. Rank equality, physical
admission, clock/work and #334 remain open; `GR_closed=false`.

Exact-file narrow Lean and axiom checks passed with `propext`,
`Classical.choice`, `Quot.sound`; independent read-only review checked both
ports, anchor, chronological induction, positive weights and independence iff.
A final integration build for the added module remains required.
