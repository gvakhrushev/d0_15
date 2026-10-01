# Flat quarter-wave correlation measures have zero quadratic metric defect

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
This is an analytic corollary of the exact
[identity-quarter nonlinear certificate](A4D_IDENTITY_QUARTER_NONLINEAR_RESPONSE.md)
and the conditional shift-correlation law in the primary task memo. It
extends the flat **quadratic response** cancellation from one coherent
four-phase field to arbitrary positive mixtures and slowly modulated
quarter-wave amplitudes. It does not prove that such a measure comes from
an exact joint-critical sequence.

## Polarization of the exact zero coefficient

At `Q=eta`, let `z_+=(i,i,i,i)` and `z_-=(-i,-i,-i,-i)`. The literal flat
joint symbol `(H_eta(z);C_eta(z))` has a four-complex-dimensional kernel
`W_+` at `z_+`, with conjugate kernel `W_-` at `z_-`. The eight real
coordinates `(a_0,...,a_3,b_0,...,b_3)` in the cited exact certificate
parameterize every real field made from this conjugate pair.

For each of the ten owner Gram-metric components `alpha`, let `B_alpha`
be the Hermitian sesquilinear coefficient of the **zero-character** part
of the quadratic connection-to-metric readout on `W_+`. Its diagonal
`u* B_alpha u` is, up to the fixed real-pair convention, the phase mean
of the quadratic metric Euler coefficient for the real field
`u*z_+^x + conjugate(u)*z_-^x`.

The exact certificate evaluates all 36 real quadratic center monomials
and checks that every one of the ten phase-mean metric coefficients is
zero. It also checks `C_eta(1)=0`, so the quadratic normal-range
correction cannot alter this zero-frequency readout. Thus
`u* B_alpha u=0` for every `u in W_+`. Complex polarization gives the
stronger operator identity

\[
\boxed{B_\alpha|_{W_+}=0\qquad(\alpha=1,\ldots,10).}
\]

This is stronger than cancellation for a particular coherent cosine or
sine wave. If `nu_x` is **any** positive Hermitian matrix-valued
shift-correlation measure supported at `z_+` on `W_+` and at `z_-` on
`W_-`, then for every smooth metric test field `q`,

\[
\boxed{\int_x\int_z
 \operatorname{tr}\bigl(D_QH_\eta(z)[q(x)]\,d\nu_x(z)\bigr)=0.}
\]

No rank-one or coherent-phase assumption on `nu_x` is needed. The
conjugate term uses the same real-field convention already fixed in the
conditional correlation law; there is no second multiplicity factor.
Slow variation of the amplitude changes the spatial density of the
measure, not this fibrewise zero identity.

## Conditional response consequence and exact boundary

Specialize the primary memo's conditional subsequence law to the flat
background `g=eta`, the identity smooth comparator, and bounded link logs
`A_h=h b_h` with weak-zero `b_h`. Retain its **sitewise** source bound,
strong linear Euler residuals and compact chart hypotheses. If every
subsequential correlation measure of `b_h` is supported in the two
quarter kernels above, its quadratic defect integral is zero by the
boxed identity. The tested normalized response difference therefore
converges to zero **distributionally**. The statement permits arbitrary
positive mixtures of the four kernel directions at the quarter pair;
it is not restricted to globally repeated four-phase fields.

This corollary does not control the unweighted owner component-sum norm,
does not include other Bloch kernels, and does not extend the fibrewise
identity from `eta` to a fixed nonconstant curved metric. The exact
nonlinear result on strictly repeated four-phase fields has a separate,
stronger sum-norm residual estimate; it cannot be applied cell by cell
across varying envelopes without bounding cross-cell Euler rows. The
global curved joint-response terminal remains open.

The later [generic-coframe theorem]
(A4D_IDENTITY_QUARTER_GENERIC_COFRAME_RESPONSE.md) proves this full
quarter-kernel **quadratic** identity for all constant coframes near
`eta`; the nonlinear eight-axis classification still belongs only to
the flat repeated four-phase chart.

Replay of the exact input:

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_quarter_nonlinear_response_check.py --expect 02_REGISTRY/research/certificates/a4d_identity_quarter_nonlinear_response_results.json
```
