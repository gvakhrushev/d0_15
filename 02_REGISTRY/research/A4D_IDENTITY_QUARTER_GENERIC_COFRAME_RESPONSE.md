# Curved-frozen identity quarter block: four role lines and zero quadratic response

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
This is an exact symbolic theorem for the full diagonal-quarter **linear
joint kernel and its quadratic phase-mean metric readout** at the identity
connection, for constant coframes near the standard one. It promotes the
previous flat all-center and curved-frozen Y-line null statements to the
whole four-complex-dimensional quarter block. It does not assert a
nonlinear stationary branch on a varying curved metric.

## Full quarter kernel at a generic nearby coframe

Let `S=(s0,s1,s2,s3)` be a constant coframe with 16 independent real
entries. For each role `r`, list the other three roles as `a<b<c`, put
`u_r=s_b-s_a`, `v_r=s_c-s_a`, and define the Lorentz generator

\[
T_r(S)=v_r u_r^{\flat}-u_r v_r^{\flat},
\qquad u^\flat=u^{T}\eta.
\]

At `S=I`, these are the owned four role generators

\[
\begin{aligned}
T_0&=J_{12}-J_{13}+J_{23},&T_1&=K_2-K_3+J_{23},\\
T_2&=K_1-K_3+J_{13},&T_3&=K_1-K_2+J_{12}.
\end{aligned}
\]

Let `H_S(i)` be the literal 24-by-24 connection Hessian at the diagonal
quarter character and `C_S^{cof}(i)` the 16-by-24 mixed coframe-to-link
block, with the owner opposite mixed-phase placement. The new certificate
builds both from the star pairing with **symbolic S**. It checks

\[
\boxed{H_S(i)(e_r\otimes T_r(S))=0,
\quad C_S^{cof}(i)(e_r\otimes T_r(S))=0
\quad(r=0,1,2,3)}
\]

as polynomial identities in all 16 coframe entries, for all 24+16 rows.
At `S=I` its connection block exactly matches the independent flat
owner, and the 16 mixed rows reduce under the Gram lift to the owner's
ten correctly placed metric rows. The latter full joint stack has exact
rank 20 at `I`. A nonzero 20-minor persists on an open coframe
neighborhood; the four displayed role-supported vectors remain
independent there and force rank at most 20. Hence the **entire** joint
quarter kernel has exactly those four complex lines throughout that
neighborhood. The same argument applies in the nondegenerate Gram
section, since its ten-row stack has rank 20 at `I` and the four vectors
remain in its kernel.

This is a local constant-coframe rank theorem. At special distant
coframes additional kernel directions have not been excluded.

## Why the whole kernel has zero mean quadratic response

For a real quarter-wave field on these lines, write the log increment on
role `r` and phase `p` as

\[
X_r(p)=(a_r,b_r,-a_r,-b_r)_p\,T_r(S).
\]

At a face `(r,s)` its four ordered plaquette logarithms are
`(X_r(p),X_s(p+1),-X_r(p+1),-X_s(p))`. The second odd-curvature
coefficient is the exact BCH commutator sum
`F^(2)=1/2 sum_{i<j}[L_i,L_j]`. An identity in the **free associative
algebra**, before choosing any Lorentz matrices, gives

\[
\boxed{\frac14\sum_{p=0}^{3}F_{rs}^{(2)}(p)
 =\tfrac12\bigl([A_s,B_s]-[A_r,B_r]\bigr),}
\]

where `A_r=a_rT_r(S)` and `B_r=b_rT_r(S)`. All cross-role commutators
cancel in the phase mean. Each remaining within-role commutator vanishes
because its cosine and sine amplitudes are scalar multiples of the
same generator. The certificate checks the full word identity for all
six faces, not a sample of numerical matrices.

This cancellation uses the actual joint-kernel structure. In a hostile
quarter-wave control with `A_0=K1`, `B_0=K2` on one role, the within-role
commutator is nonzero. At the standard coframe the phase-mean solder
Euler has entries `+1/2` and `-1/2` in `(column 1, time component)` and
`(column 2, time component)`, and its Gram projection is nonzero. The
checker certifies both values. Thus quarter periodicity by itself does
not make all metric responses vanish.

The action's coframe dependence at this order is the solder-area pairing
with `F^(2)`. A uniform coframe variation extracts the phase-mean
coframe Euler output, so the displayed facewise zero makes **all 16
mean coframe components** zero, and therefore all ten Gram metric
components. Polarization gives the Hermitian fibre identity

\[
\boxed{D_QH_Q(i,i,i,i)[q]\big|_{W_Q}=0}
\]

for every metric test `q` and the entire four-complex-dimensional joint
quarter kernel `W_Q`, at every `Q` in the stated chart. The real
conjugate character obeys the same identity. This explains the exact
zero of all 36 flat quadratic mean coefficients in the separate
identity-quarter nonlinear owner, and extends that **quadratic** zero
to nearby nonflat constant coframes. It does not extend that owner's
eight-axis nonlinear classification to variable `Q`.

## Conditional curved response consequence

Take a fixed smooth metric `g(x)` with its Gram coframe ranging over a
compact subset of the chart. The primary memo's conditional
shift-correlation law uses the frozen `D_QH_{g(x)}(z)` in its quadratic
defect integral. If a positive correlation measure of bounded
`O(h)` link-log deviations is supported at the diagonal quarter pair
and in the **full** transported joint kernels `W_{g(x)}` and their
conjugates, the integrand vanishes pointwise by the boxed identity.
Under that law's independently prescribed sitewise source, strong
Euler-residual, weak-zero and compact-chart hypotheses, the normalized
metric response difference converges to zero distributionally on this
genuinely curved background. The measure may mix all four role lines
incoherently and vary slowly in space; it need not be rank one.

This is a necessary microlocal decoupling mechanism, not a proof that an
exact nonlinear joint-critical sequence realizes such a measure.
Other Bloch supports, finite-amplitude microstructure, fast aliases,
and the unweighted owner-sum `o(h^2)` estimate remain unproved. The
task-level positive/no-go terminal remains open.

The [exact certificate](certificates/a4d_identity_quarter_generic_coframe_response_check.py)
and [pinned result](certificates/a4d_identity_quarter_generic_coframe_response_results.json)
replay in under a few seconds:

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_quarter_generic_coframe_response_check.py
```
