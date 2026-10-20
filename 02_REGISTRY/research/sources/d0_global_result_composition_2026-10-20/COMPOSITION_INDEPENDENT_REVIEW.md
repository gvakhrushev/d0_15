# Independent review of the global composition and operational writer bound

20 October 2026. Existing scientific owner #334. Read-only review of the
root's global primary and operational proof, and checkpoint_integration's
holonomy contribution. **Verdict: ACCEPT within the stated mathematical
and physical scopes.** No outstanding mathematical correction was found
in the frozen versions below.

## 1. Independence, exact targets, and validation scope

The reviewer authored `FULL_PRICE_COMPOSITION.md` and its finite-ledger
checker. Those are explicitly **not independently certified by this
review**. This receipt reviews their use and typing in the root's primary,
the separately authored operational reconstruction/writer composition,
and the separately authored holonomy/source contribution. It does not
promote physical D0-to-GR closure or re-certify the historical owners.

Paths are relative to `/workspace/scratch/98370b00de99/d0_global_synthesis`.

| Reviewed artifact | SHA-256 |
|---|---|
| `02_REGISTRY/research/A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md` | `aa593fa464a4d7e067d0a1ba763121fd229192b6d5c79d6f9b20d06469cb1d25` |
| `02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/OPERATIONAL_CURVATURE_RECOVERY.md` | `79719b99ac3b24e904d90eb91a688aaad4820704f117d37fa82380aa52ed6007` |
| `02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/HOLONOMY_SOURCE_AND_REFINEMENT.md` | `1d38287ed2b98c782dcc8bdd82c3e267e81f6381af522c891cde6aa8c33dd8a5` |
| `02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/SOURCE_INPUTS.json` | `8c5c38809b809cb409df5adb750bfd4ccb962f8e44d465753a7442e4b38ec42e` |

All 32 manifest snapshots were checked for the recorded raw-byte length and
SHA-256. This was an integrity check, not a scientific replay. No historical
geometry, compiler, spectrum, Lean, new packet checker or repository suite
was run for this review. No shared worktree or remote file was changed.

The new writer input was read directly at
`origin/exp/a4d-joint-response-continuation-2026-10-16`, resolved to
`f09e83e5fefc1d5840a516d2038b3791b45fb31e`. Its proof SHA-256 is
`89406be7d000892ba4ac062f19bb03dd86d8c9d3f04bc8a7b8de39dd07b66a2a`;
its accompanying review is
`4391eb6c105af077d306454791e8abaf32a5207fb04a2e0b8b442ec7c0853e8e`.
The current Julia odds/Book continuation input at that commit has SHA-256
`adf886cc490e1cfaab62a18d693063d3287c44ba6396a6f026ce8e357b0ce48c`.

## 2. Operational inverse and its actual norm

The three-outcome marginal retains abort and has total variation exactly
`r |B(t)-B(t_tilde)|`. Independently differentiating `B=4t^2(1-t^2)` gives
`B'=8t(1-2t^2)`, decreasing from `2` to `16/27` on `[1/2,2/3]`.
Combining this with the supplied linear dependence of `t` on `H` proves
both sides of OPERATIONAL (5), its chosen-branch inverse (6), and the
`27/16` inverse-error factor. The upper bound is correctly restricted to
the three-outcome marginal; the full tape has only the corresponding
lower comparison from marginalization.

For the two paid opposite probes, dividing each `q` by its own nonzero
increment cancels the same unknown matter derivative. Opposite signs give
`(1/|delta_+|+1/|delta_-|)/|delta_+-delta_-|=1/|delta_+ delta_-|`.
This verifies the paired sensitivity and its error propagation. The
known amplitudes, supplied live-query binding, preparation and actual
extra controller letters remain hypotheses, rather than free cloning or
an unknown-amplitude oracle.

The five-point inverse follows directly by even/odd sums on the axes and
the `(a,a)` value. The coefficient bounds and transverse Hessian estimate
follow from its row absolute sums. The nine-point extension correctly
includes the quartic `xy(x^2-y^2)` missed by the first five points.
Eliminating the constant and the two axis cubics gives the displayed
nonzero determinant `3456 a^18` and row sums; their Hessian contributions
are bounded by `12/a^2+16R/a^3+12R^2/a^4`. This is an algebraic check of
the stated finite polynomial inverse, not a replay of the geometry owner.

The text retains the midpoint/source-index distinction and measures the
radial coefficient independently of Einstein's equation. Its continuum
estimate keeps the actual positive `L_min,h`; no unsupported lower bound
on the Golden increment is inserted. Arbitrary grid profiles and time
regularity are explicitly outside the stronger polynomial estimate.

## 3. New writer/probability composition

The writer premise is correctly typed as whole-operator endpoint
isometry preserving **coordinate** `Q`, with the declared field dictionary.
It is not derived from a one-state norm, a fixed internal Gram, or the
mere existence of the diagnostic actuator.

Whitening the reachable form gives `-I+2nn^T/(n^Tn)`, hence trace `-2`,
determinant `-1`, and a compact endpoint image. Frobenius trace
Cauchy--Schwarz therefore supplies the factor `1/2` in OPERATIONAL (21).
For the actual null-to-rest calibration, direct inversion gives
`(Q_H0^-1)_vv=1/(2 kappa)` and trace defect `-(H-H0)/2`. Consequently

    dist_QH0(q_H,R_QH0) >= |H-H0|/4 >= TV(P(H),P(H0))/(8 L).

The second inequality correctly uses the **upper** probability bound in
(5), with the same probe, readiness, preparation derivative and calibration
at both field values. It does not claim this numerical bound for the
distance of the entire fine tape. The error-certified positive-part
version is an immediate triangle inequality.

The scalar-density escape is also excluded under the same fixed-Q
hypothesis: `det q=-det Q` and `det q_H=-kappa^4` force positive
`kappa=kappa0`, then the trace forces `H=H0`. The explicit moving-Q matrix
is correct and is retained as an escape from the hypothesis, not excluded
by it. Inherited copies/closure and the impossibility of a paid-graph
limit follow from the already-proved field-coordinate gap. No conclusion
about every native writer or every stationary-law route is asserted.

## 4. Prospective minimality, full ambient source, and loop price

The final primary now calls the Gamma price-graph theorem **a sufficient
explicit bridge** for the proposed realization route. This matches the
owner: approximation of fields alone is insufficient; approximation of
their same-initial, same-goal complete prices gives the minimum. An
independently derived native stationary/constraint law need not factor
through this sufficient theorem.

The minimum-exclusion application correctly requires a source-neutral
completion to vanish as the **entire ambient covector at every nearby
point of the primary family**. Its pullback to that family alone would
not suffice. With a differentiable gradient, this gives `P=Q=0` in the
residual Hessian block, incompatible with the displayed PSD inequality
when `cA != 0`. This is consistent with the separate C1 plateau theorem;
the text does not infer full entropy C2 regularity from a first source.

The six odds have the original diagonal derivative
`-2 sqrt(2)/ln(phi)`. Their common analytic inverse composed with the
original star formula proves an equality of geometric functions and
therefore all existing jets. The `phi^2` coframe weight comes from `v wedge
v` at fixed independent links. It supplies neither independent physical
field-writing gates nor Book valuation. REST/co-transport and rare-event
estimation cost restrictions remain explicit. The final publication note
also correctly credits the concurrent owner for the all-jet inverse.

The paid-repeat formula uses full n-edge attempts and fresh actual input
preparation, not early-aborted partial calls. On the original boost,
`Tr(P^T P)/4=cosh^2(xi)` gives the stated primitive-call source and flat
second derivative; other cost and Info must supply the displayed source
cocycle if full price descends. The action-weight argument in HOLONOMY
section 7 is valid under its stated reduced-action hypotheses and is not
presented as an already-proved physical scale law.

Finally, the primary's new two-ending Book gate retains equality of the
**continuation partition weights**, not equality only of continuation
minima. The sign `S_- - S_+ = -O_a` follows from `K=phi^(-S)` conditional
on the unproved actual relative binding `K_-/K_+=q_-/q_+`. Neither Born
probabilities alone nor this relative binding selects the absolute
normalizer, the mean aggregation, or the soldered action. The final
primary keeps these distinctions explicit.

## 5. Accepted use and retained boundary

The reviewed composition may be integrated as a bounded mathematical
checkpoint: operational reconstruction, a quantitative fixed-pairing
writer obstruction, an ambient geometric source identity, and explicit
tests for the complete valuation and admitted variation map. It does not
close compulsory native Info/valuation, physical field realization,
metric-only source descent, or the physical specialization of the GR
consumer. Those remaining interfaces are stated in the final primary
rather than silently supplied by the observation inverse.
